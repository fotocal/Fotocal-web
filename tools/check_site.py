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
  9  language-variant assets land in the right tree — see below
 10  no colour literal outside the token blocks — see below

ON CHECK 9. A language-variant asset is any file whose basename ends in
-es or -en before the extension (home-hero-es.webp); that suffix is the
naming convention and it is what makes this check possible, so every new
per-language capture MUST carry it. Two assertions, both born from a
shipped defect this project produced twice on two different attributes:
  a  no rendered page may reference the OTHER language's variant, on any
     of the four asset surfaces — src, srcset candidates, href (covers
     preloads), and og:image/twitter:image content. The build attribute
     being resolved is not enough: it was resolved to the wrong value
     while this file reported green, because the old check had no
     opinion about values.
  b  every variant asset on disk must be referenced by at least one page
     of its own tree — an orphaned file is the same bug seen from the
     other side (coach-kal-chat-en.webp went unreferenced while /en/
     silently showed the Spanish chat).

ON CHECK 10. The palette is a two-scheme token set (light + dark) declared
in the :root blocks of assets/css/site.css, and every colour on the site
has to come from it — that is the only way a scheme can be switched, or a
tone re-decided, in one place. So: no hex, rgb()/rgba()/hsl() or named
colour may appear in any assets/css/*.css rule outside a :root block, nor
in any inline style="…" attribute in src/ (the legal pages are excluded —
they carry their own stylesheet by design and are out of scope). SVG
fill/stroke attributes are not checked: those are third-party marks
(flags, the Google Play badge) whose colours are not ours to tokenise.
A line may opt out with a comment containing "literal-ok:" followed by a
reason; the only legitimate reason so far is a mask-image, where #000 is
alpha, not a colour.
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
SRCSET = re.compile(r'\bsrcset="([^"]*)"')
META_IMG = re.compile(r'<meta\s+(?:property="og:image"|name="twitter:image")\s+content="([^"]*)"')
LANG_VARIANT = re.compile(r"-(es|en)\.[A-Za-z0-9]+$")


def urls_in(html):
    """Every internal URL a page depends on: href/src, srcset candidates,
    and og:image / twitter:image content.

    srcset was missed here once, and it is the worst kind of miss: the
    browser prefers a srcset candidate over src, so a dead one breaks the
    image while every other check still passes. The meta images are here
    for the same reason — every attribute surface that has NOT been
    covered is the one the next failure arrives on."""
    found = set(LINK.findall(html))
    for group in SRCSET.findall(html):
        for cand in group.split(","):
            cand = cand.strip()
            if cand:
                found.add(cand.split(None, 1)[0])
    for url in META_IMG.findall(html):
        # absolute site URLs in og:image resolve like root-relative paths
        if url.startswith(SITE):
            found.add("/" + url[len(SITE):])
        else:
            found.add(url)
    return found


def check_links(rel, html, lang, variant_refs):
    here = os.path.dirname(rel)
    for url in urls_in(html):
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
        m = LANG_VARIANT.search(os.path.basename(target))
        if m:
            if m.group(1) != lang:
                fail(rel, "references the %s-language asset %s from the %s tree"
                          % (m.group(1), url, lang))
            variant_refs[m.group(1)].add(target)


COLOUR = re.compile(
    r"#[0-9A-Fa-f]{3,8}\b|\b(?:rgba?|hsla?)\((?!\s*var\()|"
    r"(?<![\w-])(?:white|black|red|green|blue|orange|pink|gold|gray|grey|"
    r"yellow|purple|navy|silver|teal|lime|cyan|magenta|coral|salmon|ivory|"
    r"beige|tan|wheat|linen)(?![\w-])", re.I)
LEGAL = ("privacy-policy/", "terms/", "account-deletion/")


def check_colour_literals():
    """Check 10 — every colour comes from the :root token blocks."""
    css_dir = os.path.join(ROOT, "assets", "css")
    for f in sorted(os.listdir(css_dir)):
        if not f.endswith(".css"):
            continue
        rel = "assets/css/" + f
        raw = open(os.path.join(css_dir, f), encoding="utf-8").read()
        # blank comments but keep the newlines, so line numbers survive;
        # remember which lines opted out before their comment vanishes
        ok_lines = {i for i, line in enumerate(raw.split("\n"), 1) if "literal-ok:" in line}
        text = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), raw, flags=re.S)
        depth, in_root, selector = 0, False, ""
        for i, line in enumerate(text.split("\n"), 1):
            for ch in line:
                if ch == "{":
                    if depth == 0:
                        in_root = selector.strip().startswith(":root")
                    depth += 1
                    selector = ""
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        in_root = False
                elif depth == 0:
                    selector += ch
            if depth == 0 and not selector.strip():
                pass
            if in_root or i in ok_lines:
                continue
            m = COLOUR.search(line)
            if m:
                fail(rel, "line %d: colour literal %r outside the token blocks" % (i, m.group(0)))

    src_dir = os.path.join(ROOT, "src")
    for base, dirs, files in os.walk(src_dir):
        for f in files:
            if not f.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(base, f), ROOT).replace(os.sep, "/")
            if any(rel.startswith("src/" + l) for l in LEGAL):
                continue
            html = open(os.path.join(base, f), encoding="utf-8").read()
            for m in re.finditer(r'style="([^"]*)"', html):
                c = COLOUR.search(m.group(1))
                if c:
                    fail(rel, "line %d: colour literal %r in an inline style"
                              % (html.count("\n", 0, m.start()) + 1, c.group(0)))


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

    variant_refs = {"es": set(), "en": set()}
    noindex = set()

    for rel in rels:
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        lang = "en" if rel.startswith("en/") else "es"
        bare = rel[3:] if lang == "en" else rel
        self_url = SITE + ("en/" if lang == "en" else "") + public(bare)

        check_links(rel, html, lang, variant_refs)

        got = one(r'<html[^>]*\blang="([a-z-]+)"', html)
        if got != lang:
            fail(rel, "<html lang> is %r, tree is %r" % (got, lang))

        for attr in ("data-i18n", "data-i18n-html", "data-i18n-alt",
                     "data-i18n-ph", "data-i18n-aria", "data-i18n-src",
                     "data-lang-block", "data-srcset"):
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
        if not indexable:
            noindex.add(rel)

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

    # ── language-variant assets: none may be orphaned ──
    for base, dirs, files in os.walk(os.path.join(ROOT, "assets")):
        for f in files:
            m = LANG_VARIANT.search(f)
            if not m:
                continue
            p = os.path.relpath(os.path.join(base, f), ROOT).replace(os.sep, "/")
            if p not in variant_refs[m.group(1)]:
                fail(p, "%s-language asset exists on disk but no page of its "
                        "tree references it" % m.group(1))

    check_colour_literals()

    # ── sitemap ──
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(os.path.join(ROOT, "sitemap.xml"))
    locs = [u.find("s:loc", ns).text for u in tree.getroot().findall("s:url", ns)]
    if len(locs) != len(set(locs)):
        fail("sitemap.xml", "duplicate <loc> entries")
    listed = set(locs)
    expected = {SITE + ("en/" if r.startswith("en/") else "") + public(r[3:] if r.startswith("en/") else r)
                for r in rels if r not in noindex}
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
