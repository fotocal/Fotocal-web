# -*- coding: utf-8 -*-
"""On-page rule notes (MASTER PROMPT v3, PART 2; rules in docs/seo/onpage-rules.md).

Called by tools/check_site.py for every indexable page. Each finding is a
*note*, never a build failure: the rollout PARTs fix them page by page,
and a page edited or created in a run must end with none.
(check_site.py already FAILS the build on a title over 60 characters, a
description over 155, a missing description and a missing or
non-reciprocal hreflang set; those are not repeated here.)

Notes:
  h1             no <h1>, or more than one
  img-alt        an <img> without an alt attribute (alt="" is allowed for
                 decorative images)
  kw-title       the page's primary keyword (docs/seo/keywords.csv,
  kw-h1          primary_keyword=yes; map in docs/seo/keyword-map.md) is not
  kw-first100    in the title / the H1 / the first 100 words of <main>

Keyword matching is word-based and forgiving: accents and case are ignored,
small words (de, la, con, the, in…) are skipped, and each remaining word
matches on its first five letters, so "calorías" matches "Calorías" and
"calorie" matches "calories", but every content word must be there.

    python3 tools/seo/onpage_lint.py            # list every note
    python3 tools/seo/onpage_lint.py kw-title   # only one kind
"""
import csv, html as H, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://getfotocal.com/"
STOP = set("de del la el los las lo un una unos unas con para por en y o a al que qué es son tu tus mi mis "
           "the of in for a an to and or how is are what your my with on by vs".split())


def _fold(s):
    s = unicodedata.normalize("NFD", H.unescape(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def words(s):
    return [w for w in re.findall(r"[a-z0-9]+", _fold(s))]


def _stems(ws):
    return {w[:5] for w in ws}


def has_kw(text, kw):
    need = [w for w in words(kw) if w not in STOP]
    have = _stems(words(text))
    return bool(need) and all(w[:5] in have for w in need)


def primaries():
    """rendered path (e.g. 'en/calorias/gazpacho/index.html') -> primary keyword"""
    out = {}
    p = os.path.join(ROOT, "docs", "seo", "keywords.csv")
    if not os.path.exists(p):
        return out
    for r in csv.DictReader(open(p, encoding="utf-8")):
        if r.get("primary_keyword") != "yes" or not r.get("page_url", "").startswith(SITE):
            continue
        rel = r["page_url"][len(SITE):] + "index.html"
        out[rel] = r["keyword"]
    return out


def main_text(html):
    m = re.search(r"<main\b.*?</main>", html, re.S)
    body = m.group(0) if m else html
    body = re.sub(r"<(script|style|nav|noscript)\b.*?</\1>", " ", body, flags=re.S)
    body = re.sub(r'<ol class="breadcrumb.*?</ol>', " ", body, flags=re.S)
    return " ".join(H.unescape(re.sub(r"<[^>]+>", " ", body)).split())


def lint(rel, html, prim):
    notes = []
    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S)
    if len(h1s) != 1:
        notes.append(("h1", "%d <h1> elements (want exactly 1)" % len(h1s)))
    m = re.search(r"<main\b.*?</main>", html, re.S)
    for tag in re.findall(r"<img\b[^>]*>", m.group(0) if m else html):
        if not re.search(r'\balt="', tag):
            src = (re.search(r'src="([^"]+)"', tag) or [None, "?"])[1]
            notes.append(("img-alt", "<img> without alt: %s" % src))
    kw = prim.get(rel)
    if kw:
        title = (re.search(r"<title>(.*?)</title>", html, re.S) or [None, ""])[1]
        h1 = re.sub(r"<[^>]+>", " ", h1s[0]) if h1s else ""
        first = " ".join(main_text(html).split()[:100])
        if not has_kw(title, kw):
            notes.append(("kw-title", "primary keyword «%s» not in the title" % kw))
        if not has_kw(h1, kw):
            notes.append(("kw-h1", "primary keyword «%s» not in the H1" % kw))
        if not has_kw(first, kw):
            notes.append(("kw-first100", "primary keyword «%s» not in the first 100 words" % kw))
    return notes


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    prim = primaries()
    n = 0
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in {".git", ".github", "src", "tools", "node_modules", "assets", "docs"}]
        if "index.html" not in files:
            continue
        rel = os.path.relpath(os.path.join(base, "index.html"), ROOT).replace(os.sep, "/")
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        if 'content="noindex' in html:
            continue
        for kind, msg in lint(rel, html, prim):
            if not only or kind == only:
                print("%-12s %s: %s" % (kind, rel, msg))
                n += 1
    print("%d on-page note(s)" % n)
