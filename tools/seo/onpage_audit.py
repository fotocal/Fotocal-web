#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""On-page SEO audit of every indexable page, both languages (seo-ranking,
2026-11). Writes docs/seo/onpage.csv: one row per page, one column per check,
"pass" / "fail" / "n/a", and prints a summary.

    python3 tools/seo/onpage_audit.py

Checks (the round's checklist):
  title_len        <title> at most 60 characters
  title_has_kw     the H1's main words appear in the title (keyword in both)
  one_h1           exactly one <h1>
  answer_first     a direct answer in the first 100 words of the main text
                   (an answer box, or a lead that states a number/fact)
  desc_len         meta description 70–155 characters
  headings         no skipped heading level (h2 -> h4)
  images           every <img> has alt, width and height; images after the
                   first are lazy-loaded; photos are WebP/AVIF
  internal_links   at least 3 internal links in the main content
  outbound_source  dish, calculator and methodology pages link at least one
                   authoritative source (USDA, CIQUAL, EFSA, WHO, AESAN,
                   BEDCA, a DOI or a national academy)
  schema           the structured data expected for the page type
  updated          a visible updated date on dish, calculator, blog,
                   methodology and comparison pages
  method_link      dish and calculator pages link /metodologia/
"""
import csv, glob, html as H, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "docs", "seo", "onpage.csv")
STOP = set("de la el los las del y en a por para con un una tu tus al calculadora calculator the of and for to in your how what is calorías calories — fotocal".split())
AUTH = re.compile(r'href="https?://(?:[a-z.]*\.)?(?:fdc\.nal\.usda\.gov|ciqual\.anses\.fr|efsa\.europa\.eu|doi\.org|who\.int|aesan\.gob\.es|bedca\.net|nap\.nationalacademies\.org|nationalacademies\.org|ncbi\.nlm\.nih\.gov)')


def kind(rel):
    r = rel[3:] if rel.startswith("en/") else rel
    if r.startswith("calorias/tabla-de-calorias/") or r == "calorias/index.html":
        return "dish-hub"
    if r.startswith("calorias/"):
        return "dish"
    if r == "calculadoras/index.html":
        return "calc-hub"
    if r.startswith("calculadoras/"):
        return "calc"
    if r.startswith("blog/") and r != "blog/index.html" and not r.startswith("blog/series/"):
        return "post"
    if r.startswith("metodologia/"):
        return "method"
    if r.startswith("comparativa/"):
        return "compare"
    return "page"


EXPECT = {"dish": ["Article", "BreadcrumbList", "NutritionInformation"], "calc": ["WebApplication", "FAQPage", "BreadcrumbList"],
          "post": ["BlogPosting", "BreadcrumbList"], "method": ["Article", "BreadcrumbList"], "compare": ["Article", "BreadcrumbList"],
          "dish-hub": ["BreadcrumbList"], "calc-hub": ["CollectionPage", "BreadcrumbList"], "page": []}


def words(s):
    return [w for w in re.findall(r"[a-záéíóúñü0-9]+", s.lower()) if w not in STOP and len(w) > 2]


def main_text(h):
    m = re.search(r'<main\b.*?</main>', h, re.S)
    return m.group(0) if m else h


def audit(rel, h):
    k = kind(rel)
    row = {"page": "/" + rel[:-len("index.html")], "type": k}
    title = H.unescape(re.search(r"<title>(.*?)</title>", h, re.S).group(1))
    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", h, re.S)
    desc = H.unescape((re.search(r'<meta name="description" content="([^"]*)"', h) or [None, ""])[1])
    main = main_text(h)
    row["title_len"] = "pass" if len(title) <= 60 else "fail"
    h1 = H.unescape(re.sub(r"<[^>]+>", "", h1s[0])) if h1s else ""
    kw, tw = set(words(h1)), set(words(title))
    lead = words(h1)[:1]                       # the head word of the H1 (a gloss may follow)
    row["title_has_kw"] = "n/a" if not kw else ("pass" if (len(kw & tw) / len(kw) >= 0.5 or (lead and all(w in tw for w in lead))) else "fail")
    row["one_h1"] = "pass" if len(h1s) == 1 else "fail"
    first = " ".join(H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|nav)\b.*?</\1>", "", main, flags=re.S))).split()[:100])
    has_box = 'class="answer-box' in main
    row["answer_first"] = "pass" if has_box or re.search(r"\d", first) or k == "page" else "fail"
    row["desc_len"] = "pass" if 70 <= len(desc) <= 155 else "fail"
    levels = [int(x) for x in re.findall(r"<h([1-6])\b", main)]
    row["headings"] = "pass" if all(b - a <= 1 for a, b in zip(levels, levels[1:])) else "fail"
    imgs = re.findall(r"<img\b[^>]*>", main)
    ok = True
    for i, t in enumerate(imgs):
        if 'alt="' not in t or 'width="' not in t or 'height="' not in t:
            ok = False
        src = (re.search(r'src="([^"]+)"', t) or [None, ""])[1]
        if re.search(r"\.(jpe?g|png)(\?|$)", src) and "logo" not in src and "icon" not in src:
            ok = False
        if i > 0 and 'loading="lazy"' not in t and "dl-logo" not in t:
            ok = False
    row["images"] = "pass" if ok else "fail"
    links = [x for x in re.findall(r'<a\b[^>]*href="([^"#]*)"', main) if x and not re.match(r'(?:[a-z]+:|//)', x)]
    legal = re.search(r"(privacy-policy|terms|account-deletion)/", rel)
    row["internal_links"] = "n/a" if legal else ("pass" if len(links) >= 3 else "fail")
    row["outbound_source"] = ("pass" if AUTH.search(main) else "fail") if k in ("dish", "calc", "method") else "n/a"
    types = set(re.findall(r'"@type":\s*"([A-Za-z]+)"', h))
    need = EXPECT.get(k, [])
    row["schema"] = "pass" if all(t in types for t in need) else "fail"
    row["updated"] = ("pass" if (re.search(r"Actualizado|Updated", main) or (k == "post" and re.search(r'class="post-meta[^"]*">\s*<span>\s*<time datetime=', main))) else "fail") if k in ("dish", "calc", "post", "method", "compare") else "n/a"
    row["method_link"] = ("pass" if "metodologia/" in main else "fail") if k in ("dish", "calc") else "n/a"
    return row


def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        if rel.startswith(("src/", "tools/", "docs/", "node_modules/")):
            continue
        h = open(f, encoding="utf-8").read()
        if 'content="noindex' in h:
            continue
        rows.append(audit(rel, h))
    cols = ["page", "type", "title_len", "title_has_kw", "one_h1", "answer_first", "desc_len", "headings", "images", "internal_links", "outbound_source", "schema", "updated", "method_link"]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("%d pages audited -> docs/seo/onpage.csv" % len(rows))
    fails = 0
    for c in cols[2:]:
        bad = [r["page"] for r in rows if r[c] == "fail"]
        fails += len(bad)
        print("  %-16s %3d fail%s" % (c, len(bad), ("  e.g. " + ", ".join(bad[:4])) if bad else ""))
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() and "--strict" in sys.argv else 0)
