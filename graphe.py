"""Graphe precurseurs -> etapes (parametres) -> materiau pour chaque voie d'une publication.

    python -I graphe.py PMC1234567     # ecrit graphes/PMC1234567.html (diagrammes Mermaid)

Une voie de base = un diagramme (reactifs, etapes avec leurs parametres, materiau obtenu) ;
ses branches = un second diagramme (ce qui change par rapport au parent).
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402

OUT = db.ROOT / "graphes"


def lab(s, n=70):
    """Texte sur pour un libelle Mermaid."""
    s = " ".join(str(s or "").split())
    s = s if len(s) <= n else s[:n - 1] + "…"
    return s.replace('"', "'").replace("#", "№").replace("<", "‹").replace(">", "›")


def val(r):
    v = r["value_text"] if r["value_num"] is None else f"{r['value_num']:g}"
    return f"{v} {r['unit'] or ''}".strip()


def route_graph(con, r):
    q = lambda sql, *a: con.execute(sql, a).fetchall()
    L = ["flowchart LR"]
    steps = q("SELECT * FROM steps WHERE route_id=? ORDER BY step_order", r["id"])
    target = f"S{steps[0]['id']}" if steps else "M"
    for g in q("SELECT * FROM reagents WHERE route_id=? ORDER BY id", r["id"]):
        amount = g["amount_text"] if g["amount"] is None else f"{g['amount']:g} {g['unit'] or ''}"
        L.append(f'  R{g["id"]}(["{lab(g["name"], 45)}<br/>{lab(amount or "quantité non citée", 30)}"]):::reactif')
        L.append(f'  R{g["id"]} -->|"{lab(g["role"] or "réactif", 20)}"| {target}')
    for i, s in enumerate(steps):
        ps = [f"{lab(p['name'], 25)} : {lab(val(p), 30)}" for p in q(
            "SELECT * FROM parameters WHERE step_id=? ORDER BY id", s["id"])][:6]
        L.append(f'  S{s["id"]}["<b>{s["step_order"]}. {lab(s["action"], 25)}</b>' + "".join("<br/>" + p for p in ps) + '"]:::etape')
        L.append(f'  S{s["id"]} --> ' + (f'S{steps[i + 1]["id"]}' if i + 1 < len(steps) else "M"))
    m = con.execute("SELECT * FROM materials WHERE id=?", (r["material_id"],)).fetchone()
    name = f"{lab(m['name'], 50)}<br/>{lab(m['formula'] or '', 30)}" if m else lab(r["branch_label"])
    L.append(f'  M{{{{"{name}"}}}}:::materiau')
    for o in q("SELECT * FROM outcomes WHERE route_id=? ORDER BY id LIMIT 6", r["id"]):
        L.append(f'  O{o["id"]}["{lab(o["property"], 35)} : {lab(val(o), 30)}"]:::resultat')
        L.append(f'  M -.-> O{o["id"]}')
    return L


def branch_graph(con, r):
    kids = con.execute("SELECT * FROM synthesis_routes WHERE parent_route_id=? ORDER BY id", (r["id"],)).fetchall()
    if not kids:
        return None
    L = ["flowchart LR", f'  B{r["id"]}{{{{"{lab(r["branch_label"])}"}}}}:::materiau']
    todo = list(kids)
    while todo:
        k = todo.pop(0)
        vs = [f"{lab(v['parameter'], 25)} = {lab(val(v), 25)}" for v in con.execute(
            "SELECT * FROM route_variations WHERE route_id=? ORDER BY id", (k["id"],))][:4]
        L.append(f'  B{k["id"]}["{lab(k["branch_label"])}"]:::etape')
        L.append(f'  B{k["parent_route_id"]} -->|"{"<br/>".join(vs) or "étapes propres"}"| B{k["id"]}')
        todo += con.execute("SELECT * FROM synthesis_routes WHERE parent_route_id=? ORDER BY id", (k["id"],)).fetchall()
    return L


CSS = ("classDef reactif fill:#e8f1fb,stroke:#3b6ea5,color:#102a43\n"
       "  classDef etape fill:#fff7e0,stroke:#b7791f,color:#3d2c00\n"
       "  classDef materiau fill:#e3f6e8,stroke:#2f855a,color:#123524\n"
       "  classDef resultat fill:#f4f4f5,stroke:#71717a,color:#27272a")


def main():
    pmcid = sys.argv[1]
    con = db.connect()
    p = con.execute("SELECT * FROM papers WHERE pmcid=?", (pmcid,)).fetchone()
    parts = [f"<h1>{html.escape(pmcid)} — {html.escape(p['title'] or '')}</h1>"]
    for r in con.execute("SELECT * FROM synthesis_routes WHERE paper_id=? AND parent_route_id IS NULL ORDER BY id", (p["id"],)):
        parts.append(f"<h2>Voie : {html.escape(r['branch_label'])}</h2>")
        for g in (route_graph(con, r), branch_graph(con, r)):
            if g:
                parts.append('<pre class="mermaid">' + html.escape("\n".join(g + ["  " + CSS])) + "</pre>")
    OUT.mkdir(exist_ok=True)
    out = OUT / f"{pmcid}.html"
    out.write_text(
        "<!doctype html><meta charset='utf-8'><title>Graphe " + pmcid + "</title>"
        "<style>body{font-family:system-ui,sans-serif;margin:16px;background:#fff;color:#111}"
        "h1{font-size:18px}h2{font-size:15px;margin-top:28px}pre.mermaid{overflow-x:auto}</style>"
        + "\n".join(parts) +
        "<script src='https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js'></script>"
        "<script>mermaid.initialize({startOnLoad:true,securityLevel:'loose',flowchart:{htmlLabels:true}});</script>",
        encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
