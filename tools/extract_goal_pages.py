#!/usr/bin/env python3
"""
Pull every translatable string out of the three goal pages.

Step 1 of translating them. This only READS — it writes a JSON manifest
of (key, tag, needs_html, english) so the Spanish can be written against
the exact English that is on the page, rather than against a paraphrase
of it. tools/translate_goal_pages.py then does the rewriting.

    python3 tools/extract_goal_pages.py > tools/goal_pages_en.json
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = {
    "weight-loss": "wl",
    "nutrition-diet": "nd",
    "lifestyle-mindset": "lm",
}

# Elements that hold copy. Deliberately narrow: <a> is handled separately
# because most links on these pages are CTAs that already have shared keys.
TAGS = ("h1", "h2", "h3", "h4", "p", "li", "span")

# Classes whose text is structural/shared and must NOT get a per-page key.
SKIP_CLASS = re.compile(r'\b(play-badge-text|fc-rkicker|fc-rarrow|nav-|lang-|sep)\b')


def inner_text(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def extract(slug):
    path = os.path.join(ROOT, "features", slug, "index.html")
    s = open(path, encoding="utf-8").read()
    body = s[s.index("<main"):s.index("</main>")]

    items, seen, n = [], set(), 0
    for m in re.finditer(r"<(%s)\b([^>]*)>(.*?)</\1>" % "|".join(TAGS), body, re.S):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if "data-i18n" in attrs:          # already translated
            continue
        if SKIP_CLASS.search(attrs):
            continue
        txt = inner_text(inner)
        if len(txt) < 3:
            continue
        # nested block tags mean this is a wrapper, not a leaf string
        if re.search(r"<(p|h[1-4]|ul|ol|li|div|section)\b", inner):
            continue
        if inner in seen:
            continue
        seen.add(inner)
        n += 1
        items.append({
            "key": "sp.%s.t%02d" % (slug, n),
            "tag": tag,
            # markup inside means it must go in via innerHTML
            "html": bool(re.search(r"<\w", inner)),
            "en": inner.strip(),
            "text": txt,
        })
    return items


def main():
    out = {}
    for slug in PAGES:
        out[slug] = extract(slug)
        print("%-20s %d strings" % (slug, len(out[slug])), file=sys.stderr)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
