"""Structured data must match the visible text (Google: AI features and
structured data guidelines; GEO round 22-11-2026).

For every built page: each FAQPage question and answer appears in the
visible text of its language; Article/BlogPosting headline matches the H1;
SoftwareApplication says Android, and every offer price is one of the prices
in tools/pricing.json (or 0 for the free plan).
    python3 tools/seo/check_schema_visible.py"""
import glob, html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PR = json.load(open(os.path.join(ROOT, "tools", "pricing.json")))
prices = {0.0}
def walk(o):
    if isinstance(o, dict):
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
    elif isinstance(o, (int, float)) and not isinstance(o, bool): prices.add(float(o))
    elif isinstance(o, str) and re.fullmatch(r"\d+(\.\d+)?", o): prices.add(float(o))
walk(PR)
INLINE = re.compile(r"</?(a|strong|em|b|i|span|abbr|sup|sub|small)\b[^>]*>")
norm = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", INLINE.sub("", s)))).strip().lower()
bad, n_faq, n_pages = [], 0, 0
files = [f for f in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)
         if not re.search(r"/(src|docs|node_modules|tools)/", f.replace(ROOT, ""))]
for f in files:
    h = open(f, encoding="utf-8").read()
    if 'noindex' in (re.search(r'<meta name="robots" content="([^"]*)"', h) or [None, ""])[1]:
        continue
    n_pages += 1
    lang = (re.search(r'<html[^>]*lang="(\w+)', h) or [None, "es"])[1]
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<head.*?</head>", " ", h, flags=re.S)
    # keep only blocks for this page's language
    other = "en" if lang == "es" else "es"
    body = re.sub(r'<(\w+)[^>]*data-lang-block="%s".*?</\1>' % other, " ", body, flags=re.S)
    vis = norm(body)
    rel = f.replace(ROOT + "/", "")
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: d = json.loads(b)
        except Exception as e: bad.append((rel, "bad JSON-LD")); continue
        for x in (d.get("@graph", [d]) if isinstance(d, dict) else d):
            t = x.get("@type")
            if t == "FAQPage":
                for q in x["mainEntity"]:
                    n_faq += 1
                    for part in (q["name"], q["acceptedAnswer"]["text"]):
                        p = norm(part)[:80]
                        if p not in vis: bad.append((rel, "FAQ text not visible: " + p[:60]))
            if t in ("Article", "BlogPosting"):
                h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
                if h1 and norm(x.get("headline", ""))[:40] not in norm(h1.group(1)) and norm(h1.group(1))[:40] not in norm(x.get("headline", "")):
                    bad.append((rel, "headline ≠ H1: %s | %s" % (x.get("headline"), norm(h1.group(1))[:60])))
            if t in ("SoftwareApplication", "MobileApplication"):
                if "android" not in json.dumps(x.get("operatingSystem", "")).lower(): bad.append((rel, "app not marked Android"))
                if "aggregateRating" in x: bad.append((rel, "aggregateRating present"))
                offs = x.get("offers", [])
                for o in (offs if isinstance(offs, list) else [offs]):
                    if float(o.get("price", 0)) not in prices: bad.append((rel, "price %s not in pricing.json" % o.get("price")))
for r in bad: print("  ", *r)
print("%s — %d indexable pages, %d FAQ items, %d problem(s)" % ("OK" if not bad else "FAIL", n_pages, n_faq, len(bad)))
sys.exit(1 if bad else 0)
