#!/usr/bin/env python3
"""Pinned defects: every check here is a defect that was found on the live
site once (dates in the comments) and must never come back. Imported and run
by tools/check_site.py; each function calls fail()/warn() from there.

Rendered output only: these read the built pages, never the sources."""
import glob, html as H, json, os, posixpath, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://getfotocal.com/"


def built_pages():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        if rel.startswith(("src/", "tools/", "node_modules/")):
            continue
        out.append(rel)
    return out


def text_of(fragment):
    return H.unescape(re.sub(r"<[^>]+>", " ", fragment)).strip()


def run(fail, warn):
    rels = built_pages()
    pages = {rel: open(os.path.join(ROOT, rel), encoding="utf-8").read() for rel in rels}
    noindex = {rel for rel, h in pages.items() if 'content="noindex' in h}
    indexable = [rel for rel in rels if rel not in noindex]
    appdata = json.load(open(os.path.join(ROOT, "tools", "dishes", "app-data.json"), encoding="utf-8"))
    hand_count = len(appdata.get("hand") or appdata.get("dishes") or appdata.get("foods") or [])

    # ── 1. empty anchors (FAQ nav item, live, 28-10-2026: a key missing from
    #      the dictionary rendered as <a href="/faq/"></a> on every page) ──
    for rel, h in pages.items():
        for m in re.finditer(r"<a\b([^>]*)>(.*?)</a>", h, re.S):
            attrs, inner = m.group(1), m.group(2)
            if text_of(inner):
                continue
            if re.search(r'aria-label="[^"]+"', attrs) or re.search(r'<img\b[^>]*\balt="[^"]+"', inner) or "<svg" in inner:
                continue
            fail(rel, "empty anchor: <a%s>" % attrs[:80])
                
    # ── 2. anchor text that says nothing ("click here", "aquí") ──
    BAD = {"click here", "here", "aquí", "haz clic aquí", "pincha aquí", "pulsa aquí", "link", "enlace", "more", "más"}
    for rel, h in pages.items():
        for m in re.finditer(r"<a\b[^>]*>(.*?)</a>", h, re.S):
            t = text_of(m.group(1)).lower().strip(" .→›»")
            if t in BAD:
                fail(rel, "anchor text %r says nothing about the destination" % t)

    # ── 3. body links to a noindex / redirect stub (crawlers follow them into
    #      a dead end) ──
    # a stub is a noindex page that redirects (meta refresh); a noindex,follow
    # hub kept for navigation is a real page and may be linked
    stubs = {("/" + r[:-len("index.html")]) for r in noindex if r != "404.html" and 'http-equiv="refresh"' in pages[r]}
    for rel in indexable:
        h = pages[rel]
        main = re.search(r"<main\b.*?</main>", h, re.S)
        body = main.group(0) if main else h
        d = "/" + posixpath.dirname(rel) + "/" if posixpath.dirname(rel) else "/"
        for href in re.findall(r'<a [^>]*href="([^"#?]+)"', body):
            u = href.replace("https://getfotocal.com", "") if href.startswith("http") else href
            if u.startswith("http"):
                continue
            u = u if u.startswith("/") else posixpath.normpath(posixpath.join(d, u))
            if not u.endswith("/"):
                u += "/"
            if u in stubs:
                fail(rel, "links to the noindex/redirect stub %s from the page body" % u)

    # ── 4. leftovers that must never ship ──
    LEFT = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b|\{\{|\bundefined\b|\[object Object\]|\bNaN\b|>null<|[Ll]orem ipsum")  # case-sensitive: "Todo lo que" is Spanish
    for rel, h in pages.items():
        body = re.sub(r"<script\b.*?</script>", "", h, flags=re.S)
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        m = LEFT.search(body)
        if m:
            fail(rel, "placeholder or leak in the output: %r" % body[max(0, m.start() - 30):m.end() + 30])

    # ── 5. headings: exactly one H1, no skipped level ──
    for rel in indexable:
        body = re.sub(r"<script\b.*?</script>", "", pages[rel], flags=re.S)
        hs = [int(x) for x in re.findall(r"<h([1-6])\b", body)]
        if hs.count(1) != 1:
            fail(rel, "%d <h1> elements" % hs.count(1))
        for a, b in zip(hs, hs[1:]):
            if b > a + 1:
                fail(rel, "heading level skips from h%d to h%d" % (a, b))
                break

    # ── 6. share card per page, existing, and not the shared one (27-10-2026) ──
    seen = {}
    for rel in indexable:
        h = pages[rel]
        m = re.search(r'<meta property="og:image" content="([^"]+)"', h)
        if not m:
            fail(rel, "no og:image"); continue
        url = m.group(1)
        path = url.replace(SITE, "")
        if not os.path.isfile(os.path.join(ROOT, path)):
            fail(rel, "og:image file missing: %s" % path)
        if path.startswith("assets/og-image"):
            fail(rel, "still uses the shared og:image; run node tools/gen_og.mjs then build again")
        if url in seen:
            fail(rel, "og:image shared with %s" % seen[url])
        seen.setdefault(url, rel)
        tw = re.search(r'<meta name="twitter:image" content="([^"]+)"', h)
        if tw and tw.group(1) != url:
            fail(rel, "twitter:image differs from og:image")

    # ── 7. images: alt attribute, width and height, file present ──
    for rel, h in pages.items():
        d = posixpath.dirname(rel)
        for tag in re.findall(r"<img\b[^>]*>", h):
            a = dict(re.findall(r'([a-zA-Z-]+)="([^"]*)"', tag))
            if "alt" not in a:
                fail(rel, "image without alt attribute: %s" % a.get("src", "")[-60:])
            if not a.get("width") or not a.get("height"):
                fail(rel, "image without width/height: %s" % a.get("src", "")[-60:])
            src = a.get("src", "")
            if src and not src.startswith(("http", "data:")):
                p = src.lstrip("/") if src.startswith("/") else posixpath.normpath(posixpath.join(d, src))
                if not os.path.isfile(os.path.join(ROOT, p)):
                    fail(rel, "image file missing: %s" % p)

    # ── 8. FAQPage schema must describe questions that are on the page ──
    for rel in indexable:
        h = pages[rel]
        visible = text_of(re.sub(r"<script\b.*?</script>", "", h, flags=re.S))
        visible_n = re.sub(r"\s+", " ", visible)
        for sc in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
            try:
                j = json.loads(sc)
            except Exception:
                continue
            if j.get("@type") == "FAQPage":
                for q in j.get("mainEntity", []):
                    name = re.sub(r"\s+", " ", (q.get("name") or "").strip())
                    if not name or not (q.get("acceptedAnswer") or {}).get("text"):
                        fail(rel, "FAQPage entry without question or answer"); break
                    if name[:60] not in visible_n:
                        fail(rel, "FAQPage question not on the page: %r" % name[:60]); break
            if j.get("@type") == "BreadcrumbList":
                items = j.get("itemListElement", [])
                if any(not it.get("name") for it in items):
                    fail(rel, "BreadcrumbList item without name")
                if items and items[-1].get("item", "").rstrip("/") != (SITE + rel[:-len("index.html")]).rstrip("/"):
                    fail(rel, "BreadcrumbList last item is %r, not this page" % items[-1].get("item"))

    # ── 9. every dictionary key the JavaScript asks for exists in BOTH
    #      languages (the FAQ label, 28-10-2026) ──
    js = "".join(open(os.path.join(ROOT, "assets", "js", f), encoding="utf-8").read() for f in ("layout.js", "main.js", "calc.js", "contact-form.js"))
    used = set(re.findall(r'\bt\(\s*"([a-zA-Z0-9_.-]+)"', js)) | set(re.findall(r'key:\s*"([a-zA-Z0-9_.-]+)"', js))
    dic = open(os.path.join(ROOT, "assets", "js", "i18n.js"), encoding="utf-8").read()
    for lang in ("en", "es"):
        m = re.search(r'\n\s*"?%s"?:\s*\{' % lang, dic)
        seg = dic[m.end():]
        nxt = re.search(r'\n  "?(?:en|es)"?:\s*\{', seg)
        seg = seg[:nxt.start()] if nxt else seg
        keys = set(re.findall(r'"([a-zA-Z0-9_.-]+)":\s*"', seg))
        for k in sorted(used - keys):
            fail("assets/js/i18n.js", "key %r used by the JavaScript is missing from the %s dictionary (renders as an empty label)" % (k, lang))

    # ── 10. the pre-rendered language switcher points at this page's twin ──
    for rel in indexable:
        h = pages[rel]
        alts = dict(re.findall(r'<link rel="alternate" hreflang="(es|en)" href="%s([^"]*)">' % re.escape(SITE), h))
        for l in ("es", "en"):
            m = re.search(r'class="lang-item" role="option" href="([^"]*)" hreflang="%s"' % l, h)
            if not m:
                continue
            want = "/" + alts[l] if l in alts else ("/en/" if l == "en" else "/")
            if m.group(1) != want:
                fail(rel, "language switcher %s points at %s, expected %s" % (l, m.group(1), want))

    # ── 11. facts that must agree on every page ──
    for rel in indexable:
        t = text_of(re.sub(r"<script\b.*?</script>", "", pages[rel], flags=re.S))
        for price in re.findall(r"(\d+[.,]\d\d)\s?€|€\s?(\d+[.,]\d\d)", t):
            v = (price[0] or price[1]).replace(",", ".")
            if v not in ("6.99", "34.99", "2.92"):  # 2.92 = 34.99 / 12, the yearly plan per month
                fail(rel, "price %s € is not one of the two plan prices" % v)
        for m in re.finditer(r"(\d+)\s+(?:escaneos?|photo scans?|scans?)\b[^.]{0,30}\b(?:al día|a day|por día|per day)", t):
            if m.group(1) != "2":
                fail(rel, "free-plan scan limit stated as %s a day (it is 2): %r" % (m.group(1), m.group(0)))
        for m in re.finditer(r"(\d+)\s+(?:registros? por voz|voice logs?)\b[^.]{0,20}\b(?:al día|a day)", t):
            if m.group(1) != "1":
                fail(rel, "voice-log limit stated as %s a day (it is 1): %r" % (m.group(1), m.group(0)))
        for m in re.finditer(r"(\d[\d.,]*)\s*(?:kcal|calorías|calories)\s+(?:por|per|a)\s+(?:kilo|kg)\b", t):
            if m.group(1).replace(".", "").replace(",", "") != "7700":
                fail(rel, "kcal per kilo stated as %s (it is 7,700)" % m.group(1))
        if hand_count:
            for m in re.finditer(r"(\d{3})\s+(?:platos|alimentos y platos|dishes|foods)\b", t):
                if m.group(1) != str(hand_count) and abs(int(m.group(1)) - hand_count) < 60:
                    fail(rel, "dish count %s disagrees with the app's %d" % (m.group(1), hand_count))

    # ── 12. language of the page vs its text (heuristic, warn) ──
    for rel in indexable:
        t = " " + re.sub(r"\s+", " ", text_of(re.sub(r"<script\b.*?</script>", "", pages[rel], flags=re.S)).lower()) + " "
        en = sum(t.count(w) for w in (" the ", " and ", " with ", " your ", " you ", " of the "))
        es = sum(t.count(w) for w in (" el ", " la ", " los ", " las ", " que ", " con ", " para "))
        if rel.startswith("en/") and es > en:
            warn(rel, "reads as Spanish (%d es / %d en markers)" % (es, en))
        if not rel.startswith("en/") and en > es:
            warn(rel, "reads as English (%d en / %d es markers)" % (en, es))
    # ── 13. no dead stylesheet or script: every file in assets/css and
    #      assets/js is loaded by a source page, by a bundle, or by the build ──
    srcs = "".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(ROOT, "src", "**", "*.html"), recursive=True))
    bundler = open(os.path.join(ROOT, "tools", "bundle_assets.py"), encoding="utf-8").read()
    for f in sorted(glob.glob(os.path.join(ROOT, "assets", "css", "*.css")) + glob.glob(os.path.join(ROOT, "assets", "js", "*.js"))):
        name = os.path.basename(f)
        if name not in srcs and '"%s"' % name[:-4] not in bundler and name not in ("fonts.css", "i18n-pages.js"):
            fail("assets", "%s is loaded by no page and no bundle (dead file)" % name)
    return len(rels)
