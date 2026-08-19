#!/usr/bin/env python3
"""
Render the bilingual site into two indexable static trees.

    python3 tools/build_site.py

    src/**/*.html   ->   /**            Spanish  (default, market is Spain)
                    ->   /en/**         English

WHY THIS EXISTS
The site used to serve both languages from one URL and swap the text with
JavaScript. Google indexes what it is served, so only the default language
was ever indexable — Spanish keywords could not rank because there was no
Spanish document to rank. Two rendered trees fix that: each URL is one
language, in the HTML, with reciprocal hreflang.

WHY SPANISH SITS ON THE EXISTING SLUGS
GitHub Pages cannot issue 301s — only meta-refresh, which Google treats as
a weak signal. Moving Spanish to /es/ or to translated slugs would break
all 71 live URLs and force weak redirects for every one. Keeping the
existing paths means zero 404s and zero redirects, and the market being
targeted gets the URLs that already carry whatever equity exists. Slug
keywords are a far weaker signal than title, H1 and body — all of which
are Spanish now.

WHAT IT DOES PER PAGE
  · data-i18n        -> element text
  · data-i18n-html   -> element inner HTML
  · data-i18n-alt / -ph / -aria -> the matching attribute
  · data-lang-block  -> keep this language's block, drop the other
  · <html lang>, <title>, <meta description>, og/twitter title+description
  · canonical -> itself;  hreflang es + en + x-default -> the pair
  · internal links rewritten so an English page links to English pages

The i18n attributes are STRIPPED from the output. With the text baked in,
leaving them would let main.js re-translate the page on load from a stale
localStorage value and contradict the URL.
"""

import datetime
import html as htmllib
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
LANGS = ("es", "en")
DEFAULT = "es"                    # Spanish is the default tree, served at /
PREFIX = {"es": "", "en": "en/"}  # path prefix per tree
SITE = "https://getfotocal.com/"
TITLE_MAX = 62                    # beyond this Google truncates the snippet

# Directories the builder owns and rewrites on every run. Anything else at
# the repo root (assets, css, js, CNAME, robots.txt …) is left alone.
OWNED = ["about", "account-deletion", "ai", "blog", "contact", "features",
         "privacy-policy", "subscription", "terms", "en"]
OWNED_FILES = ["index.html", "404.html"]


# ── dictionary ──────────────────────────────────────────────────────
def load_dict():
    """Pull the two language dictionaries straight out of the JS files, so
    the build can never drift from what the site actually ships."""
    import subprocess
    js = """
      global.window = {};
      require(process.argv[1]); require(process.argv[2]);
      process.stdout.write(JSON.stringify(window.FOTOCAL_I18N));
    """
    out = subprocess.run(
        ["node", "-e", js,
         os.path.join(ROOT, "assets/js/i18n.js"),
         os.path.join(ROOT, "assets/js/i18n-pages.js")],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


# ── helpers ─────────────────────────────────────────────────────────
def esc_attr(s):
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def esc_text(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rel_to_root(rel_path, lang):
    """How many ../ to climb from this page back to its own tree root."""
    depth = rel_path.count("/")
    return "../" * depth if depth else ""


def page_url(rel_path, lang):
    """Absolute public URL for a source path in a given tree."""
    p = rel_path[:-len("index.html")] if rel_path.endswith("index.html") else rel_path
    return SITE + PREFIX[lang] + p


# ── the element rewriters ───────────────────────────────────────────
# Deliberately regex over a DOM parser: the pages carry hand-written
# formatting and comments that a parse/serialise round-trip would reflow,
# which would make every diff unreviewable. The patterns below are anchored
# on the exact attribute, so they only touch what they are aimed at.

TAG_WITH_KEY = re.compile(
    r'<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>[^>]*?\bdata-i18n(?P<kind>-html)?="(?P<key>[^"]+)"[^>]*?)>',
    re.S)


def strip_i18n_attrs(attrs):
    attrs = re.sub(r'\s+data-i18n(?:-html|-alt|-ph|-aria)?="[^"]*"', "", attrs)
    return attrs


def render_text_nodes(src, dic, missing):
    """Replace the inner content of every data-i18n / data-i18n-html element
    with its translation, and drop the attribute."""
    out = []
    i = 0
    for m in TAG_WITH_KEY.finditer(src):
        tag, attrs, kind, key = m.group("tag"), m.group("attrs"), m.group("kind"), m.group("key")
        val = dic.get(key)
        if val is None:
            missing.add(key)
            continue
        # find this element's matching close tag, allowing nested same-name tags
        start_body = m.end()
        depth = 1
        pos = start_body
        pat = re.compile(r"</?%s\b" % re.escape(tag), re.I)
        while depth and pos < len(src):
            mm = pat.search(src, pos)
            if not mm:
                break
            depth += -1 if src[mm.start():mm.start() + 2] == "</" else 1
            pos = mm.end()
        if depth:
            missing.add(key + " (unclosed <%s>)" % tag)
            continue
        end_body = src.rindex("</", start_body, pos)
        body = esc_text(val) if kind is None else val
        out.append(src[i:m.start()])
        out.append("<%s%s>%s" % (tag, strip_i18n_attrs(attrs), body))
        i = end_body
    out.append(src[i:])
    return "".join(out)


ATTR_MAP = {"alt": "alt", "ph": "placeholder", "aria": "aria-label"}


def render_attr_nodes(src, dic, missing):
    """data-i18n-alt / -ph / -aria set the corresponding real attribute."""
    def one(kind, target):
        nonlocal src
        pat = re.compile(r'<([a-zA-Z0-9]+)([^>]*?)\bdata-i18n-%s="([^"]+)"([^>]*?)>' % kind, re.S)
        def rep(m):
            tag, a, key, b = m.groups()
            val = dic.get(key)
            if val is None:
                missing.add(key)
                return m.group(0)
            attrs = a + b
            # replace an existing target attribute, or add one
            if re.search(r'\b%s="' % re.escape(target), attrs):
                attrs = re.sub(r'\b%s="[^"]*"' % re.escape(target),
                               '%s="%s"' % (target, esc_attr(val)), attrs, count=1)
            else:
                attrs = attrs.rstrip() + ' %s="%s"' % (target, esc_attr(val))
            return "<%s%s>" % (tag, strip_i18n_attrs(attrs))
        src = pat.sub(rep, src)
    for k, t in ATTR_MAP.items():
        one(k, t)
    return src


BLOCK_OPEN = re.compile(r'<(?P<tag>[a-zA-Z0-9]+)(?P<attrs>[^>]*?\bdata-lang-block="(?P<lang>[a-z]{2})"[^>]*?)>', re.S)


def render_lang_blocks(src, lang):
    """Keep this language's blocks (unwrapped of the marker + `hidden`),
    delete the other language's entirely."""
    while True:
        m = BLOCK_OPEN.search(src)
        if not m:
            return src
        tag, attrs, blang = m.group("tag"), m.group("attrs"), m.group("lang")
        start_body = m.end()
        depth, pos = 1, start_body
        pat = re.compile(r"</?%s\b" % re.escape(tag), re.I)
        while depth and pos < len(src):
            mm = pat.search(src, pos)
            if not mm:
                raise SystemExit("unclosed <%s data-lang-block>" % tag)
            depth += -1 if src[mm.start():mm.start() + 2] == "</" else 1
            pos = mm.end()
        end_tag_start = src.rindex("</", start_body, pos)
        if blang == lang:
            clean = re.sub(r'\s+data-lang-block="[a-z]{2}"', "", attrs)
            clean = re.sub(r"\s+hidden\b", "", clean)
            src = (src[:m.start()] + "<%s%s>" % (tag, clean) +
                   src[start_body:end_tag_start] + src[end_tag_start:pos] + src[pos:])
        else:
            src = src[:m.start()] + src[pos:]


# Files both trees share. There is exactly one copy of each, at the site
# root, so a link to one must never pick up a language prefix.
SHARED_ROOTS = ("assets/", "css/", "js/", "CNAME", "robots.txt", "sitemap.xml")

# Left alone entirely: other origins, page fragments, and non-http schemes.
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#|$)", re.I)


def rewrite_links(src, lang, rel_path):
    """Make every internal link resolve correctly from inside its own tree.

    The Spanish tree is the source tree moved nowhere, so its relative links
    already work and it is returned untouched.

    English is the interesting case. Pages are mirrored under /en/ but the
    assets are NOT — there is one copy at the root. So `../../assets/…`,
    which is right in /features/scan-food/, resolves to /en/assets/… from
    /en/features/scan-food/ and 404s. Every internal link is therefore
    resolved against the page's own directory and re-emitted root-absolute:
    shared files as /assets/…, pages as /en/….
    """
    if lang == DEFAULT:
        return src

    here = os.path.dirname(rel_path)            # e.g. "features/scan-food"

    def resolve(url):
        """url as written -> path from the site root, no leading slash."""
        if url.startswith("/"):
            return url.lstrip("/")
        p = os.path.normpath(os.path.join(here, url)).replace(os.sep, "/")
        if p == ".":
            return ""                            # "../" from a one-deep page = the root
        return p[2:] if p.startswith("./") else p

    def rep(m):
        attr, url = m.group(1), m.group(2)
        if EXTERNAL.match(url):
            return m.group(0)
        # keep any ?query#fragment attached to the end
        cut = min([i for i in (url.find("?"), url.find("#")) if i != -1] or [len(url)])
        path, tail = url[:cut], url[cut:]
        root = resolve(path)
        if path.endswith("/") and root and not root.endswith("/"):
            root += "/"                          # normpath eats the trailing slash
        if root.startswith(SHARED_ROOTS) or root in SHARED_ROOTS:
            return '%s="/%s%s"' % (attr, root, tail)
        return '%s="/%s%s%s"' % (attr, PREFIX[lang], root, tail)

    return re.sub(r'\b(href|src)="([^"]*)"', rep, src)


HEAD_PATTERNS = [
    (re.compile(r"<title>.*?</title>", re.S),                       '<title>{title}</title>'),
    (re.compile(r'<meta name="description" content="[^"]*">'),      '<meta name="description" content="{desc}">'),
    (re.compile(r'<meta property="og:title" content="[^"]*">'),     '<meta property="og:title" content="{title}">'),
    (re.compile(r'<meta property="og:description" content="[^"]*">'), '<meta property="og:description" content="{desc}">'),
    (re.compile(r'<meta name="twitter:title" content="[^"]*">'),    '<meta name="twitter:title" content="{title}">'),
    (re.compile(r'<meta name="twitter:description" content="[^"]*">'), '<meta name="twitter:description" content="{desc}">'),
]


def render_head(src, lang, rel_path, meta):
    t, d = esc_attr(meta["title"]), esc_attr(meta["desc"])
    # <title> takes text, not an attribute value
    src = HEAD_PATTERNS[0][0].sub(lambda _: "<title>%s</title>" % esc_text(meta["title"]), src, count=1)
    for pat, tpl in HEAD_PATTERNS[1:]:
        if pat.search(src):
            src = pat.sub(lambda _: tpl.format(title=t, desc=d), src, count=1)

    src = re.sub(r'<html([^>]*?)\slang="[a-z]{2}"', lambda m: "<html%s lang=\"%s\"" % (m.group(1), lang), src, count=1)

    # og:locale tells a social preview which language it is looking at, and
    # pairs with hreflang for anything reading Open Graph rather than link
    # tags. Only a dozen pages carried it by hand, so add it where it is
    # missing rather than asking 142 files to remember.
    loc = "es_ES" if lang == "es" else "en_US"
    alt = "en_US" if lang == "es" else "es_ES"
    if 'property="og:locale"' in src:
        src = re.sub(r'<meta property="og:locale" content="[^"]*">',
                     '<meta property="og:locale" content="%s">' % loc, src)
        src = re.sub(r'<meta property="og:locale:alternate" content="[^"]*">',
                     '<meta property="og:locale:alternate" content="%s">' % alt, src)
    else:
        src = re.sub(r"(</title>)",
                     '\\1\n  <meta property="og:locale" content="%s">'
                     '\n  <meta property="og:locale:alternate" content="%s">' % (loc, alt),
                     src, count=1)

    # canonical + reciprocal hreflang. x-default points at Spanish: it is the
    # default tree, and it is what a visitor with no matching locale should get.
    self_url = page_url(rel_path, lang)
    src = re.sub(r'<link rel="canonical" href="[^"]*">',
                 '<link rel="canonical" href="%s">' % self_url, src, count=1)
    alts = ('<link rel="alternate" hreflang="es" href="%s">\n'
            '  <link rel="alternate" hreflang="en" href="%s">\n'
            '  <link rel="alternate" hreflang="x-default" href="%s">'
            % (page_url(rel_path, "es"), page_url(rel_path, "en"), page_url(rel_path, "es")))
    src = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*'
                 r'(?:<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*)*',
                 alts + "\n  ", src, count=1)
    src = re.sub(r'<meta property="og:url" content="[^"]*">',
                 '<meta property="og:url" content="%s">' % self_url, src, count=1)

    # The shared share card has the tagline burned into it, so there is one
    # per language. Only the shared card is swapped — the eight pages that
    # point og:image at their own artwork keep it, and that artwork carries
    # no words to be in the wrong language.
    if lang != DEFAULT:
        src = src.replace(SITE + "assets/og-image.png",
                          SITE + "assets/og-image-%s.png" % lang)
    return src


# ── structured data ─────────────────────────────────────────────────
LD_BLOCK = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
TOKEN = re.compile(r"\{\{i18n:([A-Za-z0-9._-]+)\}\}")
SITE_URL = re.compile(re.escape(SITE) + r"(?!en/)(?!assets/)([^\"']*)")


def plain(s):
    """Dictionary values may carry markup (an <em> in a heading). Schema.org
    wants the words, not the emphasis."""
    return htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def render_jsonld(src, lang, rel_path, dic, missing, article=None):
    """Localise the structured data along with the page.

    Schema.org markup is a machine-readable claim about what the visitor is
    looking at. Leaving it in English on a Spanish page is not a cosmetic
    slip: the FAQ blocks are eligible for rich results, and Google checks
    them against the visible copy. Four things happen here.

      {{i18n:key}}   ->  the dictionary value for this language
      getfotocal.com URLs naming a page  ->  this tree's copy of that page
      inLanguage     ->  the tree's language, added if it was missing
      BlogPosting headline/description   ->  the article's own, per language

    The JSON is parsed and re-emitted rather than patched with regexes,
    because a half-escaped string here is invalid structured data — an error
    that shows up in Search Console weeks later, not in the browser.
    """
    def token(s):
        def rep(m):
            v = dic.get(m.group(1))
            if v is None:
                missing.add(m.group(1))
                return m.group(0)
            return plain(v)
        return TOKEN.sub(rep, s)

    def retarget(s):
        if lang == DEFAULT:
            return s
        return SITE_URL.sub(lambda m: SITE + PREFIX[lang] + m.group(1), s)

    def walk(node):
        if isinstance(node, str):
            return retarget(token(node))
        if isinstance(node, list):
            return [walk(x) for x in node]
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        return node

    def one(m):
        try:
            data = json.loads(m.group(2))
        except ValueError:
            return m.group(0)                    # not ours to fix; leave it
        data = walk(data)
        if isinstance(data, dict):
            if data.get("@type") == "BlogPosting" and article:
                title, desc = article
                if title:
                    data["headline"] = title
                if desc:
                    data["description"] = desc
            data.setdefault("inLanguage", lang)
        body = json.dumps(data, ensure_ascii=False, indent=2)
        return m.group(1) + "\n" + body + "\n  " + m.group(3)

    return LD_BLOCK.sub(one, src)


def blog_meta(src, lang):
    """Blog articles keep their title and summary inside the document as
    data-lang-block pairs, so derive the head from those rather than
    duplicating them in page_meta.json."""
    t = re.search(r'<h1[^>]*data-lang-block="%s"[^>]*>(.*?)</h1>' % lang, src, re.S)
    d = re.search(r'<p[^>]*class="art-lead"[^>]*data-lang-block="%s"[^>]*>(.*?)</p>' % lang, src, re.S)
    if not d:
        d = re.search(r'data-lang-block="%s"[^>]*>([^<]{60,240})</p>' % lang, src, re.S)
    clean = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
    title = clean(t.group(1)) if t else None
    desc = clean(d.group(1)) if d else None
    return title, desc


# ── sitemap ─────────────────────────────────────────────────────────
# Tuning kept from the hand-written sitemap it replaces. Longest prefix wins.
WEIGHTS = [
    ("privacy-policy/", "yearly",  "0.5"),
    ("terms/",          "yearly",  "0.5"),
    ("account-deletion/", "yearly", "0.5"),
    ("about/",          "monthly", "0.6"),
    ("contact/",        "monthly", "0.6"),
    ("subscription/",   "monthly", "0.8"),
    ("features/",       "monthly", "0.9"),
    ("ai/",             "monthly", "0.9"),   # a feature page, just not under features/
    ("blog/",           "monthly", "0.7"),
    ("",                "monthly", "0.7"),
]


def sitemap_entry(path):
    """changefreq + priority for a root-relative page path."""
    if path == "":
        return "monthly", "1.0"
    if path == "blog/":
        return "weekly", "0.8"
    for prefix, freq, pri in WEIGHTS:
        if path.startswith(prefix):
            return freq, pri
    return "monthly", "0.7"


def write_sitemap(srcs, lastmod):
    """One <url> per page per language, each declaring both alternates.

    Both trees are listed: the whole point of the split is that Google can
    index Spanish AND English. The xhtml:link alternates inside each entry
    say the same thing as the <link rel="alternate"> tags in the documents —
    Google wants the pairing confirmed from at least one of the two, and
    giving it both costs nothing.

    404.html is skipped: it is noindex, and a sitemap is a list of pages you
    want indexed."""
    NS = "http://www.w3.org/1999/xhtml"
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="%s">' % NS]
    for rel in srcs:
        if rel == "404.html":
            continue
        path = rel[:-len("index.html")] if rel.endswith("index.html") else rel
        freq, pri = sitemap_entry(path)
        for lang in LANGS:
            out.append("  <url>")
            out.append("    <loc>%s</loc>" % page_url(rel, lang))
            out.append("    <lastmod>%s</lastmod>" % lastmod)
            out.append("    <changefreq>%s</changefreq>" % freq)
            out.append("    <priority>%s</priority>" % pri)
            for alt in LANGS:
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                           % (alt, page_url(rel, alt)))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                       % page_url(rel, DEFAULT))
            out.append("  </url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    return sum(1 for r in srcs if r != "404.html") * len(LANGS)


def main():
    dic = load_dict()
    meta_all = json.load(open(os.path.join(ROOT, "tools", "page_meta.json"), encoding="utf-8"))

    srcs = []
    for base, _, files in os.walk(SRC):
        for f in files:
            if f.endswith(".html"):
                srcs.append(os.path.relpath(os.path.join(base, f), SRC).replace(os.sep, "/"))
    srcs.sort()

    # clear what we own, so a deleted source page cannot linger in the output
    for d in OWNED:
        p = os.path.join(ROOT, d)
        if os.path.isdir(p):
            shutil.rmtree(p)
    for f in OWNED_FILES:
        p = os.path.join(ROOT, f)
        if os.path.isfile(p):
            os.remove(p)

    missing = set()
    written = 0
    for rel in srcs:
        raw = open(os.path.join(SRC, rel), encoding="utf-8").read()
        for lang in LANGS:
            s = raw
            s = render_lang_blocks(s, lang)
            s = render_text_nodes(s, dic[lang], missing)
            s = render_attr_nodes(s, dic[lang], missing)

            article = None
            if rel in meta_all:
                m = meta_all[rel][lang]
            else:
                t, d = blog_meta(raw, lang)
                article = (t, d)
                if not t or not d:
                    raise SystemExit("no %s title/summary derivable for %s" % (lang, rel))
                # The brand suffix is nice-to-have; the headline is not. Add it
                # only when it fits, rather than spending the last ten
                # characters of the snippet on a word already in the domain.
                # Spanish headlines run ~15% longer than the English, so a
                # fixed suffix truncated a third of the articles.
                suffix = " — Fotocal"
                m = {"title": t + suffix if len(t) + len(suffix) <= TITLE_MAX else t,
                     "desc": d[:158]}
            s = render_head(s, lang, rel, m)
            s = render_jsonld(s, lang, rel, dic[lang], missing, article)
            s = rewrite_links(s, lang, rel)

            out = os.path.join(ROOT, PREFIX[lang], rel)
            os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
            open(out, "w", encoding="utf-8").write(s)
            written += 1

    if missing:
        print("MISSING KEYS:", file=sys.stderr)
        for k in sorted(missing):
            print("  " + k, file=sys.stderr)
        sys.exit(1)

    urls = write_sitemap(srcs, datetime.date.today().isoformat())

    print("%d source pages -> %d rendered (%s)" % (len(srcs), written, " + ".join(LANGS)))
    print("sitemap.xml -> %d URLs" % urls)
    return srcs


if __name__ == "__main__":
    main()
