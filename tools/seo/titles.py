#!/usr/bin/env python3
"""Write tools/seo/titles-descriptions.md: the <title> and meta description
of every rendered page, both trees, with lengths, so a reviewer can read
them in one place instead of opening 170 files.

    python3 tools/seo/titles.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from check_site import pages, public  # noqa: E402

OUT = os.path.join(ROOT, "tools", "seo", "titles-descriptions.md")


def main():
    rows = []
    for rel in sorted(pages()):
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        if 'content="noindex' in html:
            continue
        t = re.search(r"<title>(.*?)</title>", html, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', html)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        clean = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip() if x else ""
        rows.append(("/" + public(rel), clean(t.group(1)) if t else "", d.group(1) if d else "", clean(h1.group(1)) if h1 else ""))
    lines = ["# Títulos, descripciones y H1 de todas las páginas — generado por tools/seo/titles.py", "",
             "Límites: título ≤ 60 caracteres (con el sufijo « — Fotocal» solo cuando cabe), descripción 140–160. Las longitudes van entre paréntesis.", ""]
    for tree, label in (("", "## Español (raíz)"), ("/en/", "## English (/en/)")):
        lines += [label, ""]
        for path, t, d, h1 in rows:
            if (path.startswith("/en/")) != (tree == "/en/"):
                continue
            lines.append("### `%s`" % path)
            lines.append("- **Title** (%d): %s" % (len(t), t))
            lines.append("- **Description** (%d): %s" % (len(d), d))
            lines.append("- **H1**: %s" % h1)
            lines.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    long_t = [r for r in rows if len(r[1]) > 60]
    bad_d = [r for r in rows if not 140 <= len(r[2]) <= 160]
    print("%d pages; titles > 60: %d; descriptions outside 140–160: %d" % (len(rows), len(long_t), len(bad_d)))
    for r in bad_d[:20]:
        print("  desc %d  %s" % (len(r[2]), r[0]))


if __name__ == "__main__":
    main()
