"""JATS XML -> texte normalise (corpus/text/<PMCID>.txt), puis mise en file.

Format du texte : une ligne par paragraphe ; '## Titre' pour les sections ;
'[TABLE] ...' puis une ligne par rangee de tableau, cellules separees par ' | '.

    python -I sections.py
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402

EXP_HEADING = re.compile(
    r"experiment|method|synthes|preparation|fabrication|procedure|materials", re.I)
EXP_WORDS = re.compile(
    r"was dissolved|were dissolved|autoclave|calcin|stirred|centrifug|was added|were added|"
    r"dried at|annealed|sintered|heated (at|to)|dropwise|furnace|dispersed in|mixed with|"
    r"transferred (in)?to|was grown|were grown|deposited", re.I)
NOISE_HEADING = re.compile(
    r"^(references|acknowledge?ments?|author'?s?'? contributions?|contributor information|"
    r"conflicts? of interest|competing interests?|funding|data availability( statement)?|"
    r"associated data|additional information|supplementary (materials?|information)|"
    r"supporting information|electronic supplementary material)$", re.I)
SKIP = {"xref", "ref-list", "fig", "graphic", "supplementary-material", "fn", "table-wrap-foot"}
MIN_CHARS = 8000


def local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def flat(el, skip_refs=True):
    """Texte d'un element, en ignorant les renvois bibliographiques."""
    parts = []

    def walk(e):
        name = local(e.tag)
        if name == "xref" and skip_refs and e.get("ref-type") == "bibr":
            pass
        elif name in ("fig", "table-wrap", "supplementary-material", "graphic"):
            pass
        else:
            if e.text:
                parts.append(e.text)
            for c in e:
                walk(c)
        if e.tail and e is not el:
            parts.append(e.tail)

    walk(el)
    return db.norm("".join(parts))


def table_lines(tw):
    lines = []
    label = tw.find("label")
    caption = tw.find("caption")
    head = " ".join(x for x in (flat(label) if label is not None else "",
                                flat(caption) if caption is not None else "") if x)
    lines.append(f"[TABLE] {head}".strip())
    for tr in tw.iter("tr"):
        cells = [flat(c) for c in tr if local(c.tag) in ("td", "th")]
        if any(cells):
            lines.append(" | ".join(cells))
    return lines


def walk_body(el, lines, depth=0):
    for child in el:
        name = local(child.tag)
        if name == "sec":
            title = child.find("title")
            if title is not None and NOISE_HEADING.match(flat(title)):
                continue
            if title is not None and flat(title):
                lines.append(f"## {flat(title)}")
            walk_body(child, lines, depth + 1)
        elif name == "p":
            # les tableaux et listes peuvent etre imbriques dans un paragraphe
            txt = flat(child)
            if txt:
                lines.append(txt)
            for tw in child.iter("table-wrap"):
                lines.extend(table_lines(tw))
        elif name == "table-wrap":
            lines.extend(table_lines(child))
        elif name in ("list", "boxed-text", "disp-quote", "table-wrap-group", "fig-group"):
            walk_body(child, lines, depth)
        elif name == "list-item":
            walk_body(child, lines, depth)
        elif name == "title" or name in SKIP:
            continue


def convert(pmcid):
    """Retourne (texte, raison_de_rejet)."""
    data = (db.XML_DIR / f"{pmcid}.xml").read_bytes()
    if b"<!ENTITY" in data:
        return None, "xml_suspect"
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return None, "xml_invalide"
    for e in root.iter():
        e.tag = local(e.tag)
    if "review" in (root.get("article-type") or ""):
        return None, "revue"
    body = root.find("body")
    if body is None:
        return None, "pas_de_corps"
    title = root.find(".//article-title")
    lines = [f"# {flat(title)}" if title is not None else f"# {pmcid}"]
    abstract = root.find(".//abstract")
    if abstract is not None and flat(abstract):
        lines += ["## Abstract", flat(abstract)]
    walk_body(body, lines)
    # tableaux flottants hors du corps
    for fg in root.findall("floats-group"):
        for tw in fg.iter("table-wrap"):
            lines.extend(table_lines(tw))
    lines = [db.norm(l) for l in lines if db.norm(l)]
    text = "\n".join(lines)
    if len(text) < MIN_CHARS:
        return None, "texte_trop_court"
    headings = [l for l in lines if l.startswith("## ")]
    # tri grossier : l'extracteur ecarte lui-meme les protocoles trop minces
    hits = len(EXP_WORDS.findall(text))
    if hits < (1 if any(EXP_HEADING.search(h) for h in headings) else 4):
        return None, "pas_de_protocole_detaille"
    return text, None


def main():
    con = db.connect()
    rows = con.execute("SELECT pmcid FROM papers WHERE status = 'fetched'").fetchall()
    ok = 0
    for r in rows:
        text, reason = convert(r["pmcid"])
        if reason:
            con.execute("UPDATE papers SET status='rejected', reject_reason=? WHERE pmcid=?",
                        (reason, r["pmcid"]))
        else:
            (db.TEXT_DIR / f"{r['pmcid']}.txt").write_text(text, encoding="utf-8")
            con.execute("UPDATE papers SET status='queued', text_chars=? WHERE pmcid=?",
                        (len(text), r["pmcid"]))
            ok += 1
        con.commit()
    print(f"convertis: {ok}  ecartes: {len(rows) - ok}")


if __name__ == "__main__":
    main()
