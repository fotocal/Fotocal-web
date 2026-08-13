#!/usr/bin/env python3
"""
Static checks over the rendered output of tools/build_site.py.

    python3 tools/check_site.py

Everything here is something that has actually gone wrong at least once, or
that would go wrong silently — a broken /en/ asset path still renders a page,
just an unstyled one, and a missing hreflang leg costs nothing visible while
quietly telling Google the two trees are unrelated.

  1  every internal href/src resolves to a file that exists
  2  <html lang> matches the tree the file is in
  3  canonical points at the page's own URL
  4  hreflang es + en + x-default, all three, pointing at the pair
  5  no build attributes survived into the output
  6  title and description are present, non-empty and within Google's limits
  7  the two trees have exactly the same set of pages
  8  the sitemap lists every page in both trees and nothing that 404s
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://getfotocal.com/"
SKIP_DIRS = {".git", ".github", "src", "tools", "node_modules", "assets"}

fails = []
warns = []

def fail(page, msg):
    fails.append("%s: %s" % (page, msg))

# Warnings are copy judgements, not build errors: a headline three characters
# over the snippet limit is for a human to shorten, and failing the build on
# it would just teach everyone to ignore the build.
def warn(page, msg):
    warns.append("%s: %s" % (page, msg))


def pages():
    """Every rendered .html, as a path from the site root."""
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".html"):
                yield os.path.relpath(os.path.join(base, f), ROOT).replace(os.sep, "/")


def public(rel):
    return rel[:-len("index.html")] if rel.endswith("index.html") else rel


def exists(root_path):
    """Does a root-relative URL path resolve to a file on disk?"""
    p = os.path.join(ROOT, root_path)
    if root_path.endswith("/") or root_path == "":
        return os.path.isfile(os.path.join(p, "index.html"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))


EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#|$)", re.I)
LINK = re.compile(r'\b(?:href|src)="([^"]*)"')


def check_links(rel, html):
    here = os.path.dirname(rel)
    for url in set(LINK.findall(html)):
        if EXTERNAL.match(url):
            continue
        cut = min([i for i in (url.find("?"), url.find("#")) if i != -1] or [len(url)])
        path = url[:cut]
        if not path:
            continue
        if path.startswith("/"):
            target = path.lstrip("/")
        else:
            target = os.path.normpath(os.path.join(here, path)).replace(os.sep, "/")
            if target == ".":
                target = ""
            if path.endswith("/") and target and not target.endswith("/"):
                target += "/"
        if not exists(target):
            fail(rel, "dead link %s -> /%s" % (url, target))


def one(tag, html, group=1):
    m = re.search(tag, html, re.S | re.I)
    return m.group(group).strip() if m else None


def main():
    rels = sorted(pages())
    if not rels:
        sys.exit("no rendered pages found — run tools/build_site.py first")

    es = {r for r in rels if not r.startswith("en/")}
    en = {r[3:] for r in rels if r.startswith("en/")}
    for missing in sorted(es - en):
        fail("en/" + missing, "no English counterpart")
    for missing in sorted(en - es):
        fail(missing, "no Spanish counterpart")

    for rel in rels:
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        lang = "en" if rel.startswith("en/") else "es"
        bare = rel[3:] if lang == "en" else rel
        self_url = SITE + ("en/" if lang == "en" else "") + public(bare)

        check_links(rel, html)

        got = one(r'<html[^>]*\blang="([a-z-]+)"', html)
        if got != lang:
            fail(rel, "<html lang> is %r, tree is %r" % (got, lang))

        for attr in ("data-i18n", "data-i18n-html", "data-i18n-alt",
                     "data-i18n-ph", "data-i18n-aria", "data-lang-block"):
            if re.search(r'\b%s="' % attr, html):
                fail(rel, "%s survived into the output" % attr)
        if "{{i18n:" in html:
            fail(rel, "unresolved {{i18n:…}} token: %s"
                      % ", ".join(sorted(set(re.findall(r"\{\{i18n:([^}]+)\}\}", html)))))

        # Structured data has no visible failure mode — invalid JSON, or a
        # claim in the wrong language, just quietly stops earning anything.
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                data = json.loads(block)
            except ValueError as e:
                fail(rel, "invalid JSON-LD: %s" % e)
                continue
            if isinstance(data, dict) and data.get("inLanguage") != lang:
                fail(rel, "JSON-LD inLanguage is %r, tree is %r"
                          % (data.get("inLanguage"), lang))

        # A noindex page is not asking to be ranked, so it needs neither a
        # canonical nor hreflang — 404.html is the only one.
        indexable = "noindex" not in (one(r'<meta name="robots" content="([^"]*)"', html) or "")

        if indexable:
            canon = one(r'<link rel="canonical" href="([^"]*)"', html)
            if canon != self_url:
                fail(rel, "canonical is %r, should be %r" % (canon, self_url))

            alts = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', html))
            want = {
                "es": SITE + public(bare),
                "en": SITE + "en/" + public(bare),
                "x-default": SITE + public(bare),
            }
            if alts != want:
                fail(rel, "hreflang set is %r" % (alts,))

        title = one(r"<title>(.*?)</title>", html)
        desc = one(r'<meta name="description" content="([^"]*)"', html)
        if not title:
            fail(rel, "no <title>")
        elif len(title) > 62:
            warn(rel, "title %d chars, will truncate: %s" % (len(title), title))
        if not desc:
            fail(rel, "no meta description")
        elif len(desc) > 160:
            warn(rel, "description %d chars, will truncate" % len(desc))

    # ── sitemap ──
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(os.path.join(ROOT, "sitemap.xml"))
    locs = [u.find("s:loc", ns).text for u in tree.getroot().findall("s:url", ns)]
    if len(locs) != len(set(locs)):
        fail("sitemap.xml", "duplicate <loc> entries")
    listed = set(locs)
    expected = {SITE + ("en/" if r.startswith("en/") else "") + public(r[3:] if r.startswith("en/") else r)
                for r in rels if not r.endswith("404.html")}
    for miss in sorted(expected - listed):
        fail("sitemap.xml", "missing " + miss)
    for extra in sorted(listed - expected):
        fail("sitemap.xml", "lists a page that is not rendered: " + extra)

    for w in warns:
        print("warn  " + w)
    if fails:
        print("%d problem(s):" % len(fails))
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("OK — %d pages (%d es + %d en), %d sitemap URLs, %d warning(s)"
          % (len(rels), len(es), len(en), len(locs), len(warns)))


if __name__ == "__main__":
    main()
