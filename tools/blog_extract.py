#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-off (2026-09-13): lift the writing out of the 54 hand-built post pages
into tools/blog/posts/<slug>.json, so that tools/gen_blog.py can render every
post and the index from ONE template. Nothing in the text is changed here;
the body HTML is copied byte for byte between the art-body markers.

Run once. After this the JSON files are the source of truth and the pages
under src/blog/ are generated output — edit the JSON, run gen_blog.py."""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "blog", "posts")
os.makedirs(OUT, exist_ok=True)
covers = json.load(open(os.path.join(ROOT, "tools", "blog_covers.json"), encoding="utf-8"))

def one(pat, s, flags=re.S):
    m = re.search(pat, s, flags)
    return m.group(1).strip() if m else None

n = 0
for path in sorted(glob.glob(os.path.join(ROOT, "src", "blog", "*", "index.html"))):
    slug = os.path.basename(os.path.dirname(path))
    s = open(path, encoding="utf-8").read()
    post = {"slug": slug,
            "category": one(r'data-i18n="blog\.cat\.([a-z]+)"', s),
            "date": one(r'"datePublished":"(\d{4}-\d{2}-\d{2})"', s),
            "updated": None,
            "keywords": one(r'<meta name="keywords" content="([^"]*)"', s),
            "cover": {"category": covers.get(slug, {}).get("category"), "glyph": covers.get(slug, {}).get("glyph"), "pal": covers.get(slug, {}).get("pal")}}
    for lang in ("en", "es"):
        title = one(r'<h1 class="art-title reveal" data-lang-block="%s"[^>]*>(.*?)</h1>' % lang, s)
        lead = one(r'<p class="art-lead reveal" data-lang-block="%s"[^>]*>(.*?)</p>' % lang, s)
        body = one(r'<div class="art-body reveal" data-lang-block="%s"[^>]*>\n?(.*?)\n?\s*</div>\s*(?=<div class="art-body|<aside)' % lang, s)
        assert title and lead and body, (slug, lang, bool(title), bool(lead), bool(body))
        assert "key-takeaways" in body, (slug, lang)
        post[lang] = {"title": title, "lead": lead, "body": body}
    assert post["category"] and post["date"], slug
    json.dump(post, open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n += 1
print("extracted", n, "posts ->", OUT)
