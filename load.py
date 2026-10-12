"""Validation et chargement d'une extraction (extractions/<PMCID>.json) dans la base.

    python -I load.py check PMC1234567     # validation seule, rien n'est ecrit
    python -I load.py load  PMC1234567     # validation puis insertion (remplace l'existant)

Toute citation doit etre une sous-chaine exacte du texte normalise de l'article
(corpus/text/<PMCID>.txt), aux espaces pres. Une seule erreur bloque le chargement.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402

ANNOT_TYPES = {"resume", "objectif_etude", "pourquoi_ces_donnees", "comparaison_branches",
               "tendance_observee", "conclusion_auteurs", "limite_reproductibilite"}
ANNOT_REQUIRED = ("resume", "objectif_etude", "pourquoi_ces_donnees")
NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
WORKUP = re.compile(r"wash|dry|filter|centrifug|calcin|anneal|sinter|rinse|collect|evaporat|quench", re.I)

TEMP_UNITS = {"°c": lambda v: v + 273.15, "c": lambda v: v + 273.15, "k": lambda v: v,
              "°f": lambda v: (v - 32) * 5 / 9 + 273.15}
TIME_UNITS = {"s": 1, "sec": 1, "min": 60, "h": 3600, "hr": 3600, "hours": 3600, "hour": 3600,
              "d": 86400, "day": 86400, "days": 86400, "week": 604800, "weeks": 604800}
PRESSURE_UNITS = {"pa": 1, "kpa": 1e3, "mpa": 1e6, "gpa": 1e9, "bar": 1e5, "mbar": 100,
                  "atm": 101325, "torr": 133.322, "psi": 6894.76}
RATE_UNITS = {"°c/min": 1 / 60, "k/min": 1 / 60, "°c min-1": 1 / 60, "°c min−1": 1 / 60,
              "°c/h": 1 / 3600, "k/h": 1 / 3600, "°c/s": 1, "k/s": 1}


def to_si(name, value, unit):
    """Valeur normalisee quand la conversion est sans ambiguite, sinon (None, None)."""
    if value is None or not unit:
        return None, None
    u = unit.strip().lower().replace("º", "°").replace("˚", "°").replace(" ", "") \
        if "/" in unit else unit.strip().lower().replace("º", "°").replace("˚", "°")
    if "rate" in name or "ramp" in name:
        return (value * RATE_UNITS[u], "K/s") if u in RATE_UNITS else (None, None)
    if "temperature" in name:
        return (TEMP_UNITS[u](value), "K") if u in TEMP_UNITS else (None, None)
    if "duration" in name or name.endswith("time"):
        return (value * TIME_UNITS[u], "s") if u in TIME_UNITS else (None, None)
    if "pressure" in name:
        return (value * PRESSURE_UNITS[u], "Pa") if u in PRESSURE_UNITS else (None, None)
    return None, None


def number_forms(v):
    forms = set()
    if float(v).is_integer():
        i = int(v)
        forms |= {str(i), f"{i:,}", f"{i:,}".replace(",", " "), f"{i:,}".replace(",", " "),
                  f"{i}.0"}
    s = repr(float(v))
    forms |= {s, s.replace(".", ","), s.replace("-", "−"), f"{float(v):,}"}
    if s.startswith("0."):
        forms.add(s[1:])
    forms |= {f.replace("-", "−") for f in list(forms)}
    return forms


class Checker:
    def __init__(self, pmcid):
        self.pmcid = pmcid
        self.flat, self.raw = db.load_text(pmcid)
        self.errors, self.warnings = [], []
        self.n_quotes = 0

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")

    def quote(self, where, obj, required=True):
        """Verifie obj['quote'] et renvoie (quote, section, debut, fin)."""
        q = obj.get("quote")
        if not q or not isinstance(q, str) or not q.strip():
            if required:
                self.err(where, "citation manquante")
            return None, None, None, None
        q = db.norm(q)
        if len(q) < 8:
            self.err(where, f"citation trop courte pour etre tracable: {q!r}")
        pos = self.flat.find(q)
        self.n_quotes += 1
        if pos < 0:
            hint = ""
            for n in (40, 25, 15):
                p = self.flat.find(q[:n])
                if p >= 0:
                    hint = f" | texte de l'article a cet endroit: {self.flat[p:p + len(q) + 30]!r}"
                    break
            self.err(where, f"citation introuvable dans l'article: {q!r}{hint}")
            return q, None, None, None
        return q, db.section_at(self.raw, pos), pos, pos + len(q)

    def number(self, where, obj, key="value_num"):
        v = obj.get(key)
        if v is None:
            return None
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            self.err(where, f"{key} doit etre un nombre (sinon utiliser value_text): {v!r}")
            return None
        q = db.norm(obj.get("quote") or "")
        if q and not any(f in q for f in number_forms(v)):
            self.err(where, f"la valeur {v} n'apparait pas dans sa citation {q!r} "
                            "(ne rien deduire ni convertir : recopier la valeur ecrite, "
                            "ou utiliser value_text)")
        return float(v)


def validate(pmcid, data):
    c = Checker(pmcid)
    if data.get("pmcid") != pmcid:
        c.err("pmcid", f"attendu {pmcid}, trouve {data.get('pmcid')!r}")
    routes = data.get("routes")
    if not isinstance(routes, list) or not routes:
        c.err("routes", "aucune voie de synthese")
        return c, []
    labels = [r.get("label") for r in routes]
    if len(set(labels)) != len(labels) or not all(isinstance(l, str) and l for l in labels):
        c.err("routes", f"labels absents ou en double: {labels}")
        return c, []
    by_label = {r["label"]: r for r in routes}

    # arbre : parents existants, pas de cycle, ordre parents d'abord
    order, seen = [], set()
    for r in routes:
        chain, cur = [], r
        while cur is not None and cur["label"] not in seen:
            if cur["label"] in [x["label"] for x in chain]:
                c.err(f"route {r['label']}", "cycle dans les parents")
                return c, []
            chain.append(cur)
            p = cur.get("parent")
            if p is not None and p not in by_label:
                c.err(f"route {cur['label']}", f"parent inconnu: {p!r}")
                return c, []
            cur = by_label.get(p) if p else None
        for x in reversed(chain):
            seen.add(x["label"])
            order.append(x)

    def source(r, key):
        while r is not None and not r.get(key):
            r = by_label.get(r.get("parent")) if r.get("parent") else None
        return r

    for r in order:
        w = f"route {r['label']}"
        c.quote(w, r)
        mat = r.get("material") or {}
        if not mat.get("name"):
            c.err(w, "material.name manquant")
        if not r.get("method") and not r.get("parent"):
            c.err(w, "method manquant")
        y = r.get("yield")
        if y:
            c.quote(f"{w} yield", y)
            c.number(f"{w} yield", y, "value")
        steps = r.get("steps") or []
        if not r.get("parent"):
            if not steps:
                c.err(w, "une voie sans parent doit decrire ses etapes")
            if not r.get("reagents"):
                c.warn(w, "aucun reactif")
        else:
            if not r.get("variations"):
                c.err(w, "une branche doit declarer au moins une variation par rapport a son parent")
        if [s.get("order") for s in steps] != list(range(1, len(steps) + 1)):
            c.err(w, "les etapes doivent etre numerotees 1, 2, 3... sans trou")

        for i, g in enumerate(r.get("reagents") or []):
            wg = f"{w} reagent[{i}] {g.get('name')!r}"
            if not g.get("name"):
                c.err(wg, "name manquant")
            c.quote(wg, g)
            c.number(wg, g, "amount")
            if g.get("amount") is not None and not g.get("unit"):
                c.err(wg, "quantite sans unite")
            sq = c.quote(f"{wg} supplier_quote", {"quote": g.get("supplier_quote")}, required=False)[0] or ""
            for key in ("purity", "supplier"):
                if g.get(key) and db.norm(str(g[key])) not in db.norm(g.get("quote") or "") + " " + sq:
                    c.err(wg, f"{key} {g[key]!r} absent de quote et de supplier_quote : recopier la valeur "
                              "telle qu'ecrite et citer la phrase qui la donne dans supplier_quote")

        for s in steps:
            ws = f"{w} step {s.get('order')}"
            if not s.get("action"):
                c.err(ws, "action manquante")
            c.quote(ws, s)
            for j, p in enumerate(s.get("parameters") or []):
                wp = f"{ws} param[{j}] {p.get('name')!r}"
                name = p.get("name") or ""
                if not NAME_RE.match(name):
                    c.err(wp, "name doit etre en snake_case anglais (temperature, duration, ph...)")
                c.quote(wp, p)
                v = c.number(wp, p)
                if v is None and not p.get("value_text"):
                    c.err(wp, "ni value_num ni value_text")
                if v is not None:
                    if ("temperature" in name or "duration" in name or "rate" in name) and not p.get("unit"):
                        c.err(wp, "unite manquante")
                    if name == "ph" and not 0 <= v <= 14:
                        c.err(wp, f"pH hors de 0-14: {v}")
                    if "duration" in name and v <= 0:
                        c.err(wp, f"duree non positive: {v}")
                    si, _ = to_si(name, v, p.get("unit"))
                    if "temperature" in name and si is not None and not 0 < si < 4300:
                        c.err(wp, f"temperature physiquement impossible: {v} {p.get('unit')}")
            for j, e in enumerate(s.get("equipment") or []):
                we = f"{ws} equipment[{j}]"
                if not e.get("type"):
                    c.err(we, "type manquant")
                c.quote(we, e)

        src = source(by_label.get(r.get("parent")) if r.get("parent") else None, "steps")
        src_steps = (src or {}).get("steps") or []
        src_reag, anc = [], by_label.get(r.get("parent")) if r.get("parent") else None
        while anc is not None:
            src_reag += anc.get("reagents") or []
            anc = by_label.get(anc.get("parent")) if anc.get("parent") else None
        for i, v in enumerate(r.get("variations") or []):
            wv = f"{w} variation[{i}] {v.get('parameter')!r}"
            if not v.get("parameter"):
                c.err(wv, "parameter manquant")
            c.quote(wv, v)
            num = c.number(wv, v)
            if num is None and not v.get("value_text"):
                c.err(wv, "ni value_num ni value_text")
            so = v.get("step_order")
            names = {p.get("name") for s in src_steps for p in (s.get("parameters") or [])
                     if so is None or s.get("order") == so}
            names |= {g.get("name") for g in src_reag}
            if so is not None and so not in [s.get("order") for s in src_steps]:
                c.err(wv, f"step_order {so} n'existe pas dans le protocole herite")
            elif v.get("parameter") not in names:
                c.warn(wv, "ne correspond a aucun parametre ni reactif du protocole herite "
                           f"(noms disponibles: {sorted(n for n in names if n)}) ; "
                           "reprendre le meme nom si c'est le meme parametre")

        for key, field in (("characterizations", "technique"), ("outcomes", "property")):
            for i, o in enumerate(r.get(key) or []):
                wo = f"{w} {key}[{i}] {o.get(field)!r}"
                if not o.get(field):
                    c.err(wo, f"{field} manquant")
                c.quote(wo, o)
                if key == "outcomes":
                    v = c.number(wo, o)
                    if v is None and not o.get("value_text"):
                        c.err(wo, "ni value_num ni value_text")
        if not r.get("outcomes") and r.get("succeeded") is None:
            c.warn(w, "ni resultat (outcomes) ni indication de succes/echec")

    annots = data.get("annotations") or []
    types = [a.get("type") for a in annots if not a.get("route")]
    for t in ANNOT_REQUIRED:
        if t not in types:
            c.err("annotations", f"annotation d'article obligatoire absente: {t}")
    if any(r.get("parent") for r in routes) and \
            "comparaison_branches" not in [a.get("type") for a in annots]:
        c.err("annotations", "des branches existent : annotation comparaison_branches obligatoire")
    for i, a in enumerate(annots):
        wa = f"annotation[{i}] {a.get('type')!r}"
        if a.get("type") not in ANNOT_TYPES:
            c.err(wa, f"type inconnu (autorises: {sorted(ANNOT_TYPES)})")
        if not a.get("text") or len(a["text"]) < 40:
            c.err(wa, "texte absent ou trop court")
        if a.get("route") and a["route"] not in by_label:
            c.err(wa, f"route inconnue: {a['route']!r}")
        c.quote(wa, a, required=False)
    for i, d in enumerate(data.get("doubts") or []):
        if not d.get("issue"):
            c.err(f"doubts[{i}]", "issue manquant")
    return c, order


def completeness(route, by_label):
    """Part des informations necessaires a la reproduction qui sont presentes (0-1)."""
    def inherited(key):
        r = route
        while r is not None and not r.get(key):
            r = by_label.get(r.get("parent")) if r.get("parent") else None
        return (r or {}).get(key) or []

    # les reactifs propres a une branche (additif, dopant) s'ajoutent a ceux de ses ancetres
    reagents, r = [], route
    while r is not None:
        reagents += r.get("reagents") or []
        r = by_label.get(r.get("parent")) if r.get("parent") else None
    steps = inherited("steps")
    params = [p for s in steps for p in (s.get("parameters") or [])]
    precursors = [g for g in reagents if (g.get("role") or "").lower() not in ("solvent", "solvant")]
    checks = [
        bool(precursors) and all(g.get("amount") is not None or g.get("amount_text") for g in precursors),
        any((g.get("role") or "").lower() in ("solvent", "solvant") for g in reagents),
        any("temperature" in (p.get("name") or "") for p in params),
        any("duration" in (p.get("name") or "") for p in params),
        any(WORKUP.search(s.get("action") or "") for s in steps),
        bool((route.get("material") or {}).get("formula")),
        bool(route.get("outcomes") or route.get("characterizations")),
        len(steps) >= 3,
    ]
    return round(sum(checks) / len(checks), 3)


def material_id(con, m):
    vals = (m.get("name"), m.get("formula"), m.get("phase"), m.get("morphology"))
    row = con.execute("SELECT id FROM materials WHERE name IS ? AND formula IS ? AND phase IS ?"
                      " AND morphology IS ?", vals).fetchone()
    if row:
        if m.get("family"):
            con.execute("UPDATE materials SET family = COALESCE(family, ?) WHERE id = ?",
                        (m["family"], row["id"]))
        return row["id"]
    return con.execute("INSERT INTO materials (name, formula, phase, morphology, family)"
                       " VALUES (?,?,?,?,?)", vals + (m.get("family"),)).lastrowid


def insert(con, pmcid, data, order, c):
    paper = con.execute("SELECT * FROM papers WHERE pmcid = ?", (pmcid,)).fetchone()
    if paper is None:
        raise SystemExit(f"{pmcid} absent de la table papers")
    pid = paper["id"]
    # un rechargement ne doit pas rouvrir les doutes deja tranches
    solved = {d["issue"]: d["resolution"] for d in con.execute(
        "SELECT issue, resolution FROM doubts WHERE paper_id=? AND status='resolved'", (pid,))}
    for t in ("synthesis_routes", "annotations", "doubts"):
        con.execute(f"DELETE FROM {t} WHERE paper_id = ?", (pid,))
    by_label = {r["label"]: r for r in order}
    ids = {}

    def q(obj, required=True):
        return c.quote("", obj, required)

    for r in order:
        quote = q(r)
        y = r.get("yield") or {}
        ids[r["label"]] = rid = con.execute(
            "INSERT INTO synthesis_routes (paper_id, material_id, parent_route_id, branch_label,"
            " is_baseline, method, scale, yield_value, yield_unit, yield_quote, succeeded,"
            " missing_fields, completeness_score, quote, section, char_start, char_end)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid, material_id(con, r.get("material") or {}), ids.get(r.get("parent")), r["label"],
             int(bool(r.get("is_baseline", not r.get("parent")))),
             r.get("method") or by_label.get(r.get("parent"), {}).get("method"), r.get("scale"),
             y.get("value"), y.get("unit"), db.norm(y["quote"]) if y.get("quote") else None,
             None if r.get("succeeded") is None else int(bool(r["succeeded"])),
             json.dumps(r.get("missing_fields") or [], ensure_ascii=False),
             completeness(r, by_label)) + quote).lastrowid
        for v in r.get("variations") or []:
            con.execute(
                "INSERT INTO route_variations (route_id, parameter, step_order, value_num, value_text,"
                " unit, parent_value, quote, section, char_start, char_end) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (rid, v["parameter"], v.get("step_order"), v.get("value_num"), v.get("value_text"),
                 v.get("unit"), None if v.get("parent_value") is None else str(v["parent_value"])) + q(v))
        for g in r.get("reagents") or []:
            con.execute(
                "INSERT INTO reagents (route_id, name, formula, role, amount, unit, amount_text, purity,"
                " supplier, supplier_quote, quote, section, char_start, char_end)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (rid, g["name"], g.get("formula"), g.get("role"), g.get("amount"), g.get("unit"),
                 g.get("amount_text"), g.get("purity"), g.get("supplier"),
                 db.norm(g["supplier_quote"]) if g.get("supplier_quote") else None) + q(g))
        for s in r.get("steps") or []:
            sid = con.execute(
                "INSERT INTO steps (route_id, step_order, action, description, quote, section,"
                " char_start, char_end) VALUES (?,?,?,?,?,?,?,?)",
                (rid, s["order"], s["action"], s.get("description")) + q(s)).lastrowid
            for p in s.get("parameters") or []:
                si, usi = to_si(p["name"], p.get("value_num"), p.get("unit"))
                con.execute(
                    "INSERT INTO parameters (step_id, name, value_num, value_text, unit, value_si,"
                    " unit_si, quote, section, char_start, char_end) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (sid, p["name"], p.get("value_num"), p.get("value_text"), p.get("unit"), si, usi) + q(p))
            for e in s.get("equipment") or []:
                con.execute(
                    "INSERT INTO equipment (step_id, type, detail, quote, section, char_start, char_end)"
                    " VALUES (?,?,?,?,?,?,?)", (sid, e["type"], e.get("detail")) + q(e))
        for o in r.get("characterizations") or []:
            con.execute(
                "INSERT INTO characterizations (route_id, technique, result, quote, section, char_start,"
                " char_end) VALUES (?,?,?,?,?,?,?)", (rid, o["technique"], o.get("result")) + q(o))
        for o in r.get("outcomes") or []:
            con.execute(
                "INSERT INTO outcomes (route_id, property, value_num, value_text, unit, quote, section,"
                " char_start, char_end) VALUES (?,?,?,?,?,?,?,?,?)",
                (rid, o["property"], o.get("value_num"), o.get("value_text"), o.get("unit")) + q(o))
    for a in data.get("annotations") or []:
        con.execute(
            "INSERT INTO annotations (paper_id, route_id, type, text, quote, section, char_start, char_end)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (pid, ids.get(a.get("route")), a["type"], a["text"]) + q(a, required=False))
    for d in data.get("doubts") or []:
        con.execute("INSERT INTO doubts (paper_id, location, issue, resolution, status) VALUES (?,?,?,?,?)",
                    (pid, d.get("where"), d["issue"], solved.get(d["issue"]),
                     "resolved" if d["issue"] in solved else "open"))
    seq = paper["seq"]
    if seq is None:
        seq = con.execute("SELECT COALESCE(MAX(seq), 0) + 1 FROM papers").fetchone()[0]
    con.execute("UPDATE papers SET status='extracted', seq=?, palier=?, extracted_at=? WHERE id=?",
                (seq, (seq - 1) // db.PALIER_SIZE + 1, db.now(), pid))
    con.commit()
    return seq


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("check", "load"):
        raise SystemExit(__doc__)
    mode, pmcid = sys.argv[1], sys.argv[2]
    path = db.EXTRACT_DIR / f"{pmcid}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"ERREUR lecture {path.name}: {e}")
    c, order = validate(pmcid, data)
    for w in c.warnings:
        print("AVERTISSEMENT", w)
    for e in c.errors:
        print("ERREUR", e)
    n_branch = sum(1 for r in order if r.get("parent"))
    print(f"{pmcid}: {len(order)} voies ({n_branch} branches), {c.n_quotes} citations verifiees, "
          f"{len(c.errors)} erreurs, {len(c.warnings)} avertissements, "
          f"{len(data.get('doubts') or [])} doutes")
    if c.errors:
        raise SystemExit(1)
    if mode == "load":
        seq = insert(db.connect(), pmcid, data, order, c)
        print(f"charge (publication n°{seq})")


if __name__ == "__main__":
    main()
