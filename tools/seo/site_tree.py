#!/usr/bin/env python3
"""Write tools/seo/site-tree.md: every URL the site serves, as a tree, from
the rendered output (not from a plan), with what is indexable and what is
not, and which Spanish pages have no English copy.

    python3 tools/seo/site_tree.py
"""
import os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from check_site import pages, public, SKIP_DIRS  # noqa: E402

OUT = os.path.join(ROOT, "tools", "seo", "site-tree.md")


def info(rel):
    html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    robots = re.search(r'<meta name="robots" content="([^"]*)"', html)
    refresh = 'http-equiv="refresh"' in html
    return {"title": title.group(1).strip() if title else "", "noindex": bool(robots and "noindex" in robots.group(1)), "refresh": refresh,
            "en": bool(re.search(r'hreflang="en"', html))}


def main():
    rels = sorted(pages())
    es = [r for r in rels if not r.startswith("en/")]
    en = {r[3:] for r in rels if r.startswith("en/")}
    groups = defaultdict(list)
    for r in es:
        top = r.split("/")[0] if "/" in r else "(raíz)"
        if r.startswith("blog/series/"):
            top = "blog/series"
        elif r.startswith("blog/"):
            top = "blog"
        groups[top].append(r)
    lines = ["# Árbol del sitio — generado por tools/seo/site_tree.py", "",
             "Leyenda: `ES+EN` ambas lenguas · `solo ES` sin copia inglesa (hreflang es + x-default) · `noindex` no se indexa · `→` redirección (meta refresh).",
             "", "Raíz: https://getfotocal.com/ (español). Inglés bajo /en/ con la misma estructura, salvo lo marcado `solo ES`.", ""]
    total_es = total_en = 0
    order = ["(raíz)", "features", "ai", "faq", "subscription", "calorias", "calculadoras", "blog", "blog/series", "about", "contact", "privacy-policy", "terms", "account-deletion"]
    for g in order + sorted(set(groups) - set(order)):
        if g not in groups:
            continue
        lines.append("## /%s" % ("" if g == "(raíz)" else g + "/"))
        lines.append("")
        for r in groups[g]:
            i = info(r)
            flags = []
            if i["noindex"]:
                flags.append("noindex")
            if i["refresh"]:
                flags.append("→ redirección")
            if r in en:
                flags.append("ES+EN")
                total_en += 1
            else:
                flags.append("solo ES")
            total_es += 1
            path = "/" + public(r)
            lines.append("- `%s` — %s  _%s_" % (path, i["title"].replace("|", "\\|"), " · ".join(flags)))
        lines.append("")
    lines.append("Total: %d páginas en español, %d con copia inglesa (%d URLs servidas)." % (total_es, total_en, total_es + total_en))
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("%s: %d es / %d en" % (os.path.relpath(OUT, ROOT), total_es, total_en))


if __name__ == "__main__":
    main()
