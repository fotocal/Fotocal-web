#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the Spanish dish pages, /calorias/<slug>/, and their hub, /calorias/.

    python3 tools/gen_dishes.py          # writes src/calorias/**/index.html
    python3 tools/build_site.py          # then renders the Spanish tree

INPUTS
  tools/dishes/dishes.json    which dishes, their slugs, the editorial text
  tools/dishes/app-data.json  the app's figures (tools/dishes/sync_from_app.py)

THE ONE RULE ABOUT NUMBERS
Every figure on these pages is the one the app shows for the dish, computed
here with the app's own arithmetic (src/lib/foodCompose.ts + dishComposition.ts):
  · a dish with a recipe of food-table rows is the sum of grams × per-100 g
    values of those rows (USDA FoodData Central / CIQUAL 2025), a RAW row
    cooked by a method read at its raw weight (cooked ÷ yield);
  · that composition is used only when its energy is within 25 % of the
    dish's hand-entered energy; otherwise the hand figures stand;
  · a nutrient is reported only when every row has it.
Per-100 g values are derived from those. Nothing on a page is typed in by
hand except the prose, and the prose quotes numbers through placeholders
({kcal}, {per100}, {kcal:<app-id>}) so it cannot drift from the table.

Pages are Spanish-only (tools/build_site.py ES_ONLY): no English copy,
hreflang es + x-default, one sitemap entry."""
import html, json, math, os, re, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "calorias")
DISHES = json.load(open(os.path.join(ROOT, "tools", "dishes", "dishes.json"), encoding="utf-8"))["dishes"]
APP = json.load(open(os.path.join(ROOT, "tools", "dishes", "app-data.json"), encoding="utf-8"))
HAND = {h["id"]: h for h in APP["hand"]}
FOODS = APP["foods"]
RECIPES = APP["recipes"]
RETENTION = APP["retention"]
YIELD = APP["cook_yield"]
TOL = APP["_source"]["tolerance"]
SITE = "https://getfotocal.com/"
PLAY = "https://play.google.com/store/apps/details?id=com.fotokal.app"
TITLE_MAX = 60

CALCS = {
    "calorias-diarias": "Calculadora de calorías diarias",
    "deficit-calorico": "Calculadora de déficit calórico",
    "imc": "Calculadora de IMC",
    "macros": "Calculadora de macros",
    "proteinas": "Calculadora de proteínas",
    "agua": "Calculadora de agua",
    "tmb": "Calculadora de TMB (metabolismo basal)",
    "peso-saludable": "Calculadora de peso saludable",
}


# ── the app's arithmetic ────────────────────────────────────────────
def r1(v):
    """Math.round(v * 10) / 10 — the app's rounding, half up."""
    return None if v is None else math.floor(v * 10 + 0.5) / 10


def r0(v):
    return int(math.floor(v + 0.5))


def yield_of(line):
    f = FOODS[line["foodId"]]
    m = line.get("method")
    if not f.get("retn") or not m or m == "raw":
        return 1.0
    y = YIELD.get(f["group"], {}).get(m)
    return y if isinstance(y, (int, float)) and y > 0 else 1.0


def retention_factor(line, k):
    f = FOODS[line["foodId"]]
    m = line.get("method")
    code = f.get("retn", {}).get(m) if m else None
    if not code or code not in RETENTION:
        return 1.0
    pct = RETENTION[code].get(k)
    return pct / 100.0 if isinstance(pct, (int, float)) and pct >= 0 else 1.0


def compose(lines):
    keys = ["kcal", "protein", "carbs", "fat", "fiberG", "sugarG", "satFatG", "sodiumMg"]
    values = {}
    for k in keys:
        total, known = 0.0, True
        for l in lines:
            v = FOODS[l["foodId"]]["per100"].get(k)
            if v is None:
                known = False
                break
            total += (v * (l["grams"] / yield_of(l)) / 100.0) * retention_factor(l, k)
        values[k] = total if known else None
    grams = sum(l["grams"] for l in lines)
    return grams, values


def figures(app_id):
    """What the app shows for this dish, and where it came from."""
    h = HAND[app_id]
    out = {"name_app": h["name_es"], "serving_label": h["servingLabel"], "serving_g": h["servingGrams"],
           "composed": False, "rejected": False, "sources": [], "fiber": None, "sugar": None, "satfat": None, "salt": None}
    rec = RECIPES.get(app_id)
    if rec:
        grams, v = compose(rec)
        if v["kcal"] is not None and h["kcal"] > 0 and abs(v["kcal"] - h["kcal"]) / h["kcal"] <= TOL:
            out.update(composed=True, grams=grams, kcal=r0(v["kcal"]),
                       protein=r1(v["protein"]), carbs=r1(v["carbs"]), fat=r1(v["fat"]),
                       fiber=r1(v["fiberG"]), sugar=r1(v["sugarG"]), satfat=r1(v["satFatG"]),
                       salt=None if v["sodiumMg"] is None else r1(v["sodiumMg"] * 2.5 / 1000))
            out["sources"] = [{"grams": l["grams"], "es": FOODS[l["foodId"]]["es"], "db": FOODS[l["foodId"]]["src"]["db"],
                               "ref": FOODS[l["foodId"]]["src"]["ref"], "method": l.get("method")} for l in rec]
        elif v["kcal"] is not None:
            out["rejected"] = True
        if out["composed"]:
            if abs(grams - h["servingGrams"]) / h["servingGrams"] > 0.05:
                print("  note: %s composition weighs %d g, hand serving %d g" % (app_id, grams, h["servingGrams"]), file=sys.stderr)
    if not out["composed"]:
        out.update(grams=h["servingGrams"], kcal=r0(h["kcal"]), protein=h["protein_g"], carbs=h["carbs_g"], fat=h["fat_g"])
    g = out["grams"]
    # ONE weight for both columns (07-11-2026: paella showed "300 g, 515 kcal"
    # next to "168 kcal per 100 g", because the 515 kcal are the sum of 307 g
    # of ingredients). The serving shown is the weight the kcal belong to.
    out["serving_g"] = g
    out["per100"] = r0(out["kcal"] / g * 100)
    out["per100_p"] = r1(out["protein"] / g * 100)
    out["per100_c"] = r1(out["carbs"] / g * 100)
    out["per100_f"] = r1(out["fat"] / g * 100)
    # energy split, 4/4/9, normalised so the bar always sums to 100. A drink
    # with alcohol carries 7 kcal/g the macros do not show (the app's own
    # sanity check names this case): the gap between the row's energy and
    # 4/4/9 is shown as alcohol, never hidden inside "hidratos".
    e = {"p": out["protein"] * 4, "c": out["carbs"] * 4, "f": out["fat"] * 9}
    alc = bool(rec) and any(w in FOODS[l["foodId"]]["src"]["desc"].lower() for l in rec for w in ("beer", "wine", "alcohol"))
    if alc and out["kcal"] > sum(e.values()):
        e["a"] = out["kcal"] - sum(e.values())
    tot = sum(e.values()) or 1
    out["split"] = {k: round(v / tot * 100) for k, v in e.items()}
    out["split"].setdefault("a", 0)
    assert 0 <= out["kcal"] / g <= 9.01, app_id
    return out


# ── formatting ───────────────────────────────────────────────────────
def n(x, dec=None):
    """Spanish number: 1.650 and 8,3."""
    if x is None:
        return "—"
    if dec is None:
        dec = 0 if float(x).is_integer() or abs(x) >= 100 else 1
    s = ("{:,.%df}" % dec).format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def esc(s):
    return html.escape(str(s), quote=True)


def cap(s):
    return s[:1].upper() + s[1:]


def de(art):
    """'de' + article, with the contraction Spanish requires: de el -> del."""
    return "del" if art == "el" else "de " + art


def fecha(iso):
    y, m, d = iso.split("-")
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre"]
    return "%d de %s de %s" % (int(d), meses[int(m) - 1], y)


def blog_title(slug):
    p = os.path.join(ROOT, "tools", "blog", "posts", slug + ".json")
    if not os.path.isfile(p):
        sys.exit("dish links to an unknown blog post: %s" % slug)
    return json.load(open(p, encoding="utf-8"))["es"]["title"]


def fill(text, d, fig):
    """Numbers inside the editorial text, always from the figures:
    {kcal} {per100} {per1000} {g} {protein} {carbs} {fat} {name}
    {kcal:<app-id>}            another app dish's kcal per serving
    {kcal/4} {per100*3} …      simple arithmetic on this dish's kcal or per-100 g"""
    def rep(m):
        key, arg, op, k = m.group(1), m.group(2), m.group(3), m.group(4)
        if key == "name":
            return d["name"]
        src = figures(arg) if arg else fig
        base = {"kcal": src["kcal"], "per100": src["per100"], "per1000": src["per100"] * 10, "g": src["serving_g"],
                "protein": src["protein"], "carbs": src["carbs"], "fat": src["fat"]}
        v = base[key]
        if op:
            v = v * float(k) if op == "*" else v / float(k)
            return n(r0(v))
        return n(v)
    return re.sub(r"\{(kcal|per100|per1000|g|protein|carbs|fat|name)(?::([a-z0-9-]+))?(?:([*/])(\d+(?:\.\d+)?))?\}", rep, text)


# ── head ─────────────────────────────────────────────────────────────
def head(depth, title, desc, path, ld, og_type="article", extra=""):
    up = "../" * depth
    url = SITE + path
    return """<!DOCTYPE html>
<!-- GENERATED by tools/gen_dishes.py from tools/dishes/dishes.json + app-data.json — do not edit here. -->
<html lang="es" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!--# meta %s -->
  <title>%s</title>
  <meta name="description" content="%s">
  <link rel="canonical" href="%s">
  <link rel="alternate" hreflang="es" href="%s">
  <link rel="alternate" hreflang="x-default" href="%s">
  <meta property="og:type" content="%s">
  <meta property="og:site_name" content="Fotocal">
  <meta property="og:title" content="%s">
  <meta property="og:description" content="%s">
  <meta property="og:url" content="%s">
  <meta property="og:image" content="https://getfotocal.com/assets/og-image.png">
  <meta property="og:locale" content="es_ES">%s
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%s">
  <meta name="twitter:description" content="%s">
  <meta name="twitter:image" content="https://getfotocal.com/assets/og-image.png">
  <meta name="theme-color" media="(prefers-color-scheme: light)" content="#FFFFFF">
  <meta name="theme-color" media="(prefers-color-scheme: dark)" content="#121212">
%s
  <link rel="icon" type="image/png" sizes="32x32" href="%sassets/favicon-32.png?v=3">
  <link rel="icon" type="image/png" sizes="16x16" href="%sassets/favicon-16.png?v=3">
  <link rel="icon" href="%sassets/favicon.ico?v=3" sizes="32x32">
  <link rel="apple-touch-icon" sizes="180x180" href="%sassets/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="192x192" href="%sassets/icon-192.png">
  <link rel="manifest" href="%ssite.webmanifest">
  <link rel="stylesheet" href="%sassets/css/fonts.css">
  <link rel="stylesheet" href="%sassets/css/site.css">
  <link rel="stylesheet" href="%sassets/css/home.css">
  <link rel="stylesheet" href="%sassets/css/features.css">
  <link rel="stylesheet" href="%sassets/css/blog.css">
  <link rel="stylesheet" href="%sassets/css/tools.css">
</head>
<body class="page-fx page-post">
<div id="site-nav"></div>
""" % (json.dumps({"es": {"title": title, "desc": desc}}, ensure_ascii=False),
       esc(title), esc(desc), url, url, url, og_type, esc(title), esc(desc), url, extra,
       esc(title), esc(desc), ld, up, up, up, up, up, up, up, up, up, up, up, up)


def foot(depth):
    up = "../" * depth
    return """
<div id="site-footer"></div>
<script src="%sassets/js/i18n.js"></script>
<script src="%sassets/js/layout.js" data-page="calorias"></script>
<script src="%sassets/js/main.js"></script>
</body>
</html>
""" % (up, up, up)


def ld_block(obj):
    return '  <script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)


ORG = {"@type": "Organization", "@id": SITE + "#org", "name": "Fotocal", "url": SITE,
       "logo": {"@type": "ImageObject", "url": SITE + "assets/img/logo.png"}}

APP_ASIDE = """
      <aside class="ai-callout ai-callout-quiet post-app reveal">
        <div class="ai-callout-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h3l2-2h6l2 2h3v12H4z"/><circle cx="12" cy="13" r="3.5"/></svg></div>
        <div>
          <h3>Si quieres las calorías de tu plato, no las de la media</h3>
          <p>Fotocal estima la ración a partir de una foto, con los mismos datos de esta página, y te deja corregir cada ingrediente y sus gramos antes de guardar. El plan gratis no caduca ni pide tarjeta: 2 escaneos con IA al día, 1 registro por voz al día, y el escáner de códigos de barras y Coach Kal sin límite. Solo en Android.</p>
          <p><a href="%s" target="_blank" rel="noopener">Descárgala gratis</a> · <a href="{UP}features/scan-food/">Cómo funciona el escáner de comida</a></p>
        </div>
      </aside>""" % PLAY


PLAY_ICON = ('<svg class="dl-play" viewBox="0 0 32 34" aria-hidden="true">'
             '<path d="M2.6 1.2C1.9 1.9 1.5 3 1.5 4.4v25.2c0 1.4.4 2.5 1.1 3.2l.2.2 14.1-14.1v-.6L2.8 1l-.2.2z" fill="#00D7FE"/>'
             '<path d="M21.6 21.6l-4.7-4.7v-.6l4.7-4.7.1.1 5.6 3.2c1.6.9 1.6 2.4 0 3.3l-5.6 3.2-.1.2z" fill="#FFCE00"/>'
             '<path d="M21.7 21.5L16.9 16.7 2.6 31 2.6 31c.5.6 1.4.6 2.4.1l16.7-9.6" fill="#FF3A44"/>'
             '<path d="M21.7 12.1L5 2.5C4 1.9 3.1 2 2.6 2.6l14.3 14.1 4.8-4.6z" fill="#00F076"/></svg>')
DL = {
    "es": {"btn": "Descárgala gratis", "trust": "Gratis · sin tarjeta · Android",
           "limits": "Plan gratis: 2 escaneos con IA al día, 1 registro por voz al día, código de barras y Coach Kal sin límite.",
           "aria": "Descárgala gratis en Google Play"},
    "en": {"btn": "Get it free", "trust": "Free · no card · Android",
           "limits": "Free plan: 2 AI scans a day, 1 voice log a day, unlimited barcode scanner and Coach Kal.",
           "aria": "Get it free on Google Play"},
}


def download_card(lang, headline, sub, link, extra_class=""):
    """The app download card (lang-ux 4b, 2026-11): the app icon, a headline
    (personalised with the result on the calculators), one line, a big brand
    button with the Google Play mark, and the trust line. The free plan's
    limits sit on the same card, as every "gratis" on the site must."""
    t = DL[lang]
    return ("\n      <aside class=\"dl-card%s\">"
            "\n        <img class=\"dl-logo\" src=\"/assets/img/logo-96.png\" width=\"60\" height=\"60\" alt=\"\" decoding=\"async\">"
            "\n        <div class=\"dl-body\">"
            "\n          <p class=\"dl-h\">%s</p>"
            "\n          <p class=\"dl-sub\">%s</p>"
            "\n          <!--offer--><p class=\"offer-badge offer-badge-sm\">{{offer:badge}}</p><!--/offer-->"
            "\n          <a class=\"btn btn-cta dl-btn\" href=\"%s\" target=\"_blank\" rel=\"noopener\" aria-label=\"%s\">%s<span>%s</span></a>"
            "\n          <p class=\"dl-trust\">%s</p>"
            "\n          <p class=\"dl-limits\">%s</p>"
            "\n        </div>"
            "\n      </aside>") % ((" " + extra_class) if extra_class else "", headline, sub, esc(link), t["aria"], PLAY_ICON, t["btn"], t["trust"], t["limits"])


def bilingual(es_page, en_title, en_desc, en_ld, en_main):
    """One source page, two trees: the Spanish page as rendered so far, plus
    its English twin. The structured data moves from the head into each
    language's block, so the English tree never carries Spanish schema."""
    m = re.search(r"<!--# meta (\{.*?\}) -->", es_page)
    meta = json.loads(m.group(1))
    meta["en"] = {"title": en_title, "desc": en_desc}
    es_page = es_page.replace(m.group(0), "<!--# meta %s -->" % json.dumps(meta, ensure_ascii=False), 1)
    lds = re.findall(r'  <script type="application/ld\+json">.*?</script>\n', es_page, re.S)
    for x in lds:
        es_page = es_page.replace(x, "", 1)
    a = es_page.index('\n<main id="main">')
    b = es_page.index("</main>", a) + len("</main>")
    es_main = es_page[a:b]
    both = ('\n<div class="lang-root" data-lang-block="es">\n%s%s\n</div>\n<div class="lang-root" data-lang-block="en">\n%s\n%s\n</div>'
            % ("".join(lds), es_main, en_ld, en_main))
    return es_page[:a] + both + es_page[b:]


def dish_aside(d):
    """The app card on a dish page: 'Haz una foto de tu <plato> y Fotocal lo
    calcula' (tools-seo brief, 2026-11), same free-plan limits as APP_ASIDE."""
    tu = "tus" if d["article"] in ("las", "los") else "tu"
    link = PLAY + "&utm_source=web&utm_medium=dish&utm_campaign=" + d["slug"]
    return (APP_ASIDE.replace("{UP}", "../../")
            .replace("<h3>Si quieres las calorías de tu plato, no las de la media</h3>",
                     "<h3>Haz una foto de %s %s y Fotocal lo calcula</h3>" % (tu, esc(d["name"])))
            .replace('<a href="%s" target="_blank"' % PLAY, '<a href="%s" target="_blank"' % esc(link)))


def nutrition_ld(d, fig, url, name=None, lang="es", serving=None):
    """MenuItem + NutritionInformation for one serving, the app's figures."""
    dot = lambda x: ("%.1f" % x).rstrip("0").rstrip(".")   # machine-readable: a decimal point, no thousands separator
    g = lambda x: "%s g" % dot(x)
    nut = {"@type": "NutritionInformation", "servingSize": "%s (%s g)" % (serving or fig["serving_label"], dot(fig["serving_g"])),
           "calories": "%s kcal" % dot(fig["kcal"]), "proteinContent": g(fig["protein"]),
           "carbohydrateContent": g(fig["carbs"]), "fatContent": g(fig["fat"])}
    if fig["satfat"] is not None:
        nut["saturatedFatContent"] = g(fig["satfat"])
    if fig["sugar"] is not None:
        nut["sugarContent"] = g(fig["sugar"])
    if fig["fiber"] is not None:
        nut["fiberContent"] = g(fig["fiber"])
    if fig.get("salt") is not None:
        nut["sodiumContent"] = "%d mg" % round(fig["salt"] / 2.5 * 1000)
    return ld_block({"@context": "https://schema.org", "@type": "MenuItem", "name": name or cap(d["name"]), "url": url,
                     "inLanguage": lang, "nutrition": nut})


# ── one dish page ────────────────────────────────────────────────────
def dish_page(d, ready_by_app):
    fig = figures(d["app_id"])
    name, art = d["name"], d["article"]
    g = fig["serving_g"]
    path = "calorias/%s/" % d["slug"]
    url = SITE + path
    pub = d.get("published", date.today().isoformat())
    upd = d.get("updated", pub)

    title = d.get("title") or "Calorías %s %s: ración y 100 g" % (de(art), name)
    if len(title) + len(" — Fotocal") <= TITLE_MAX:
        title += " — Fotocal"
    assert len(title) <= TITLE_MAX, (d["slug"], len(title), title)

    macros = "%s g de proteínas, %s g de hidratos y %s g de grasas" % (n(fig["protein"]), n(fig["carbs"]), n(fig["fat"]))
    desc = d.get("desc")
    if not desc:
        bases = [
            "Una ración de %s (%s g) tiene %s kcal, %s por 100 g: %s." % (name, n(g), n(fig["kcal"]), n(fig["per100"]), macros),
            "Una ración de %s (%s g) tiene %s kcal, %s por 100 g: %s g de proteínas, %s de hidratos y %s de grasas." % (name, n(g), n(fig["kcal"]), n(fig["per100"]), n(fig["protein"]), n(fig["carbs"]), n(fig["fat"])),
            "%s (%s g): %s kcal, %s por 100 g; %s g de proteínas, %s de hidratos y %s de grasas." % (cap(name), n(g), n(fig["kcal"]), n(fig["per100"]), n(fig["protein"]), n(fig["carbs"]), n(fig["fat"])),
        ]
        tails = sorted({" Ración real, de dónde salen las calorías y comparación con platos parecidos.",
                        " Ración real, de dónde salen y comparación con platos parecidos.",
                        " Qué pesa una ración real y comparación con platos parecidos.",
                        " Ración real y comparación con platos parecidos.",
                        " Con la ración real y platos parecidos.",
                        " Qué pesa una ración de verdad.",
                        " Ración real y comparación.",
                        " Y qué pesa una ración real.",
                        " Y la ración de verdad.", " Y la ración real.", ""}, key=len, reverse=True)
        for base in bases:
            for tail in tails:
                if 140 <= len(base + tail) <= 160:
                    desc = base + tail
                    break
            if desc:
                break
    assert desc and 140 <= len(desc) <= 160, (d["slug"], len(desc or ""), desc)

    lead = ("Una ración de %s de %s g tiene %s kcal, %s kcal por cada 100 g: %s. "
            "Abajo, qué pesa una ración de verdad, de dónde salen las calorías y cómo queda frente a platos parecidos."
            % (name, n(g), n(fig["kcal"]), n(fig["per100"]), macros))

    # FAQ, with the numbers filled from the figures
    faq = [{"q": q["q"], "a": fill(q["a"], d, fig)} for q in d.get("faq", [])]

    # comparison rows: the dish first, then the named ones
    rows = [(cap(name), fig, True)]
    for cid in d.get("compare", []):
        if cid not in HAND:
            sys.exit("%s compares with an unknown app dish: %s" % (d["slug"], cid))
        rows.append((HAND[cid]["name_es"], figures(cid), False))

    crumbs = [("Inicio", SITE), ("Calorías de platos", SITE + "calorias/"), (cap(name), url)]
    ld = [
        ld_block({"@context": "https://schema.org", "@type": "Article", "headline": title.replace(" — Fotocal", ""),
                  "description": desc, "inLanguage": "es", "mainEntityOfPage": url, "url": url,
                  "datePublished": pub, "dateModified": upd, "author": ORG, "publisher": ORG,
                  "image": SITE + "assets/og-image.png",
                  "about": {"@type": "Thing", "name": cap(name)}}),
        ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c[0], "item": c[1]} for i, c in enumerate(crumbs)]}),
    ]
    ld.append(nutrition_ld(d, fig, url))
    if faq:
        ld.append(ld_block({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["a"])}} for f in faq]}))

    extra = '\n  <meta property="article:published_time" content="%s">\n  <meta property="article:modified_time" content="%s">' % (pub, upd)
    out = [head(2, title, desc, path, "\n".join(ld), "article", extra)]
    o = out.append

    o('\n<main id="main">\n  <article class="post dp">\n    <header class="post-head">\n      <div class="container-narrow">')
    o('        <nav class="post-crumbs reveal" aria-label="Migas de pan">'
      '<a href="../../">Inicio</a><span class="sep" aria-hidden="true">/</span>'
      '<a href="../">Calorías de platos</a><span class="sep" aria-hidden="true">/</span>'
      '<a href="./" aria-current="page">%s</a></nav>' % esc(cap(name)))
    o('        <h1 class="post-title reveal">Calorías %s %s</h1>' % (de(art), esc(name)))
    o('        <p class="post-lead reveal">%s</p>' % esc(lead))
    o('        <div class="post-meta reveal"><span>Actualizado <time datetime="%s">%s</time></span>'
      '<span class="dot" aria-hidden="true">&middot;</span><span>Por Fotocal, Madrid</span>'
      '<span class="dot" aria-hidden="true">&middot;</span><a href="../../metodologia/">Cómo calculamos</a></div>' % (upd, fecha(upd)))
    o('      </div>\n    </header>\n    <div class="container-narrow">')

    # the direct answer, 40–60 words, for readers and for AI answers (seo-ranking, 2026-11)
    o('      <div class="answer-box reveal"><p><strong>Respuesta rápida:</strong> %s tiene %s kcal por ración (%s g) y %s kcal por 100 g. '
      'La ración aporta %s g de proteínas, %s g de hidratos y %s g de grasas. Media ración son unas %s kcal; una ración y media, unas %s. '
      'Cifras de la base de datos de Fotocal, a partir de USDA y CIQUAL.</p></div>'
      % (esc(cap(name)), n(fig["kcal"]), n(g), n(fig["per100"]), n(fig["protein"]), n(fig["carbs"]), n(fig["fat"]), n(round(fig["kcal"] / 2)), n(round(fig["kcal"] * 1.5))))

    # figure cards
    o('      <div class="dp-kpis reveal">')
    o('        <div class="dp-kpi dp-kpi-main"><b>%s<small>kcal</small></b><span>por ración (%s, %s g)</span></div>' % (n(fig["kcal"]), esc(fig["serving_label"]), n(g)))
    o('        <div class="dp-kpi"><b>%s<small>kcal</small></b><span>por cada 100 g</span></div>' % n(fig["per100"]))
    o('        <div class="dp-kpi"><b>%s<small>g</small></b><span>proteínas por ración</span></div>' % n(fig["protein"]))
    o('        <div class="dp-kpi"><b>%s<small>g</small></b><span>grasas por ración</span></div>' % n(fig["fat"]))
    o('      </div>')

    # nutrition table
    o('      <div class="post-body reveal">')
    o('      <h2 id="valores">Valores nutricionales %s %s</h2>' % (de(art), esc(name)))
    o('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">&nbsp;</th><th scope="col">Por ración (%s g)</th><th scope="col">Por 100 g</th></tr></thead><tbody>' % n(g))
    o('        <tr><th scope="row">Calorías</th><td class="hl">%s kcal</td><td class="hl">%s kcal</td></tr>' % (n(fig["kcal"]), n(fig["per100"])))
    o('        <tr><th scope="row">Proteínas</th><td>%s g</td><td>%s g</td></tr>' % (n(fig["protein"]), n(fig["per100_p"])))
    o('        <tr><th scope="row">Hidratos de carbono</th><td>%s g</td><td>%s g</td></tr>' % (n(fig["carbs"]), n(fig["per100_c"])))
    if fig["sugar"] is not None:
        o('        <tr><th scope="row">&nbsp;&nbsp;de los cuales azúcares</th><td>%s g</td><td>%s g</td></tr>' % (n(fig["sugar"]), n(r1(fig["sugar"] / fig["grams"] * 100))))
    o('        <tr><th scope="row">Grasas</th><td>%s g</td><td>%s g</td></tr>' % (n(fig["fat"]), n(fig["per100_f"])))
    if fig["satfat"] is not None:
        o('        <tr><th scope="row">&nbsp;&nbsp;de las cuales saturadas</th><td>%s g</td><td>%s g</td></tr>' % (n(fig["satfat"]), n(r1(fig["satfat"] / fig["grams"] * 100))))
    if fig["fiber"] is not None:
        o('        <tr><th scope="row">Fibra</th><td>%s g</td><td>%s g</td></tr>' % (n(fig["fiber"]), n(r1(fig["fiber"] / fig["grams"] * 100))))
    if fig["salt"] is not None:
        o('        <tr><th scope="row">Sal</th><td>%s g</td><td>%s g</td></tr>' % (n(fig["salt"]), n(r1(fig["salt"] / fig["grams"] * 100))))
    o('      </tbody></table></div>')
    o('      <p class="dp-table-note">Valores medios. Tu plato concreto puede estar por encima o por debajo: la receta, el aceite y el tamaño de la ración mueven la cifra más que cualquier tabla. Las fuentes están al final de la página.</p>')

    # portion
    o('      <h2 id="racion">¿Cuánto es una ración de verdad?</h2>')
    o('      ' + fill(d["portion"], d, fig))

    # drivers
    sp = fig["split"]
    o('      <h2 id="origen">De dónde salen las calorías</h2>')
    if sp.get("a"):
        o('      <p>De cada 100 kcal de %s, unas %d vienen del alcohol, %d de los hidratos, %d de la proteína y %d de la grasa. El alcohol aporta 7 kcal por gramo y no aparece en la tabla de arriba porque no es proteína, hidrato ni grasa.</p>' % (esc(name), sp["a"], sp["c"], sp["p"], sp["f"]))
        o('      <div class="dp-bar" role="img" aria-label="Reparto de la energía: %d%% alcohol, %d%% hidratos, %d%% proteína, %d%% grasa">'
          '<span class="p" style="width:%d%%"></span><span class="c" style="width:%d%%"></span><span class="f" style="width:%d%%"></span><span class="a" style="width:%d%%"></span></div>' % (sp["a"], sp["c"], sp["p"], sp["f"], sp["p"], sp["c"], sp["f"], sp["a"]))
        o('      <div class="dp-legend"><span class="p"><i></i>Proteína %d%%</span><span class="c"><i></i>Hidratos %d%%</span><span class="f"><i></i>Grasa %d%%</span><span class="a"><i></i>Alcohol %d%%</span></div>' % (sp["p"], sp["c"], sp["f"], sp["a"]))
    else:
        o('      <p>De cada 100 kcal de %s, unas %d vienen de la grasa, %d de los hidratos y %d de la proteína.</p>' % (esc(name), sp["f"], sp["c"], sp["p"]))
        o('      <div class="dp-bar" role="img" aria-label="Reparto de la energía: %d%% proteína, %d%% hidratos, %d%% grasa">'
          '<span class="p" style="width:%d%%"></span><span class="c" style="width:%d%%"></span><span class="f" style="width:%d%%"></span></div>' % (sp["p"], sp["c"], sp["f"], sp["p"], sp["c"], sp["f"]))
        o('      <div class="dp-legend"><span class="p"><i></i>Proteína %d%%</span><span class="c"><i></i>Hidratos %d%%</span><span class="f"><i></i>Grasa %d%%</span></div>' % (sp["p"], sp["c"], sp["f"]))
    o('      ' + fill(d["drivers"], d, fig))

    # comparison
    o('      <h2 id="comparacion">Comparación con platos parecidos</h2>')
    o('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">Plato</th><th scope="col">Ración</th><th scope="col">kcal / ración</th><th scope="col">kcal / 100 g</th><th scope="col">Proteínas</th></tr></thead><tbody>')
    for label, f2, is_this in rows:
        slug2 = ready_by_app.get(next((k for k, v in HAND.items() if v["name_es"] == label), None))
        cell = ('<a href="../%s/">%s</a>' % (slug2, esc(label))) if (slug2 and not is_this) else esc(label)
        o('        <tr%s><td>%s</td><td>%s g</td><td class="hl">%s</td><td>%s</td><td>%s g</td></tr>'
          % (' class="is-this"' if is_this else "", cell, n(f2["serving_g"]), n(f2["kcal"]), n(f2["per100"]), n(f2["protein"])))
    o('      </tbody></table></div>')
    o('      <p class="dp-table-note">Todas las cifras salen de la misma base de datos, así que se pueden comparar entre sí; con cifras de webs distintas no se podría.</p>')

    # lighter
    if d.get("lighter"):
        o('      <h2 id="ligera">Cómo hacer%s más ligera' % ("la" if art == "la" else "lo" if art == "el" else "las" if art == "las" else "los"))
        out[-1] = out[-1].rstrip("ligera") + ("ligera" if art in ("la",) else "ligero" if art == "el" else "ligeras" if art == "las" else "ligeros") + "</h2>"
        o('      ' + fill(d["lighter"], d, fig))

    # long-tail sections (editorial, numbers filled from the figures)
    for sec in d.get("sections", []):
        o('      <h2 id="%s">%s</h2>' % (sec["id"], esc(sec["h2"])))
        o('      ' + fill(sec["html"], d, fig))

    # FAQ
    if faq:
        o('      <h2 id="preguntas">Preguntas frecuentes</h2>')
        o('      <div class="faq-list">')
        for i, f in enumerate(faq):
            o('        <details class="faq-item"%s><summary><span>%s</span><i class="faq-plus" aria-hidden="true"></i></summary><p>%s</p></details>' % (" open" if i == 0 else "", esc(f["q"]), f["a"]))
        o('      </div>')
    o('      </div>')  # post-body

    o(download_card("es", "Haz una foto de tu%s %s y Fotocal lo calcula" % ("s" if d["article"] in ("las", "los") else "", esc(d["name"])),
                    "Fotocal estima la ración a partir de una foto, con las cifras de esta página, y te deja corregir cada ingrediente y sus gramos antes de guardar.",
                    PLAY + "&utm_source=web&utm_medium=dish&utm_campaign=" + d["slug"]))

    # sources
    o('      <section class="dp-src reveal" id="fuentes">\n        <h2>De dónde salen estas cifras</h2>')
    o('        <p>Bases de datos públicas: <a href="https://fdc.nal.usda.gov/" target="_blank" rel="noopener">USDA FoodData Central</a> y <a href="https://ciqual.anses.fr/" target="_blank" rel="noopener">CIQUAL (ANSES)</a>. Cómo se suman y cómo se fija la ración: <a href="../../metodologia/">nuestra metodología</a>.</p>')
    if fig["composed"]:
        o('        <p>Son las que usa la app Fotocal para este plato: una ración estándar compuesta por filas de bases de datos públicas, sumadas gramo a gramo.</p><ul>')
        for s in fig["sources"]:
            o('          <li>%s g de %s — %s, %s%s</li>' % (n(s["grams"]), esc(s["es"]), esc(s["db"]), esc(s["ref"]), (" (%s)" % {"boiled": "cocido", "stewed": "guisado", "sauteed": "salteado", "fried": "frito", "grilled": "a la plancha", "baked": "al horno"}.get(s["method"], s["method"])) if s.get("method") else ""))
        o('        </ul><p>La ración (%s, %s g) la fija Fotocal. El valor por 100 g se deriva de la ración. Snapshot de la app: commit %s (%s).</p>' % (esc(fig["serving_label"]), n(g), APP["_source"]["commit"], APP["_source"]["commit_date"]))
    elif fig["rejected"]:
        o('        <p>Es la cifra de referencia que usa la app Fotocal para una ración de %s (%s g). El plato tiene una receta de ingredientes en la base de datos, pero su suma se aleja más de un 25 %% de la cifra de referencia (la regla de la app para no mezclar fuentes), así que la app muestra la referencia y esta página también. Por eso no hay fibra, azúcares ni sal. Snapshot de la app: commit %s (%s).</p>' % (esc(fig["serving_label"]), n(g), APP["_source"]["commit"], APP["_source"]["commit_date"]))
    else:
        o('        <p>Es la cifra de referencia que usa la app Fotocal para una ración de %s (%s g). Este plato no tiene todavía desglose por ingredientes en su base de datos, así que no se muestran fibra, azúcares ni sal. Snapshot de la app: commit %s (%s).</p>' % (esc(fig["serving_label"]), n(g), APP["_source"]["commit"], APP["_source"]["commit_date"]))
    o('        <p>Esta página es información general sobre alimentos, no consejo médico ni dietético.</p>\n      </section>')

    # related
    o('      <nav class="dp-related reveal" aria-label="Páginas relacionadas">\n        <h2>Seguir por aquí</h2>\n        <div class="post-nav">')
    others = [x for x in DISHES if x.get("status") == "ready" and x["slug"] != d["slug"]][:4]
    for x in others:
        o('          <a class="post-nav-item" href="../%s/"><small>Otro plato</small><strong>Calorías %s %s</strong></a>' % (x["slug"], de(x["article"]), esc(x["name"])))
    o('          <a class="post-nav-item" href="../"><small>Tabla</small><strong>Calorías de los platos españoles, por ración y por 100 g</strong></a>')
    # every dish page links the daily-calories calculator (tools-seo, 2026-11), plus its own pick
    for c in dict.fromkeys(["calorias-diarias", d.get("calc", "deficit-calorico")]):
        o('          <a class="post-nav-item" href="../../calculadoras/%s/"><small>Calculadora</small><strong>%s</strong></a>' % (c, CALCS[c]))
    for b in d.get("blog", [])[:3]:
        o('          <a class="post-nav-item" href="../../blog/%s/"><small>Del blog</small><strong>%s</strong></a>' % (b, esc(blog_title(b))))
    o('        </div>\n      </nav>')
    o('    </div>\n  </article>\n</main>')
    o(foot(2))
    return "\n".join(out), fig



# ── the printable table of everything the app has ────────────────────
SLOT_NAMES = [("desayuno", "Desayunos"), ("comida", "Comidas"), ("merienda", "Meriendas y aperitivos"), ("cena", "Cenas")]

def table_page(ready_by_app):
    title = "Tabla de calorías de alimentos y platos españoles"
    desc = ("Tabla de calorías para imprimir con los %d alimentos y platos españoles de la app Fotocal: ración, kcal por ración y por 100 g, "
            "proteínas, hidratos y grasas." % len(HAND))
    assert len(title) + 10 <= TITLE_MAX and 140 <= len(desc) <= 160, (len(title), len(desc))
    title += " — Fotocal"
    path = "calorias/tabla-de-calorias/"
    url = SITE + path
    crumbs = [("Inicio", SITE), ("Calorías de platos", SITE + "calorias/"), ("Tabla de calorías", url)]
    ld = [
        ld_block({"@context": "https://schema.org", "@type": "WebPage", "name": title.replace(" — Fotocal", ""), "description": desc,
                  "inLanguage": "es", "url": url, "dateModified": APP["_source"]["commit_date"], "publisher": ORG,
                  "isPartOf": {"@type": "WebSite", "@id": SITE + "#site"}}),
        ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c[0], "item": c[1]} for i, c in enumerate(crumbs)]}),
    ]
    extra = ("\n  <style>@media print{.site-header,#site-header,#site-footer,.dp-aside,.post-nav,.dp-related,.tbl-print,.post-crumbs,.skip{display:none!important}"
             ".dp-table{font-size:11px}.dp-table td,.dp-table th{padding:3px 6px}body{background:#fff}.post-head{padding-top:0}}"
             ".tbl-print{margin:1rem 0 0}</style>")
    out = [head(2, title, desc, path, "\n".join(ld), "website", extra)]
    o = out.append
    o('\n<main id="main">\n  <article class="post dp dp-hub">\n    <header class="post-head">\n      <div class="container-narrow">')
    o('        <nav class="post-crumbs reveal" aria-label="Migas de pan"><a href="../../">Inicio</a><span class="sep" aria-hidden="true">/</span>'
      '<a href="../">Calorías de platos</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">Tabla de calorías</a></nav>')
    o('        <h1 class="post-title reveal">Tabla de calorías de los alimentos y platos españoles</h1>')
    o('        <p class="post-lead reveal">Los %d alimentos y platos de la base de datos de Fotocal en una sola tabla, para consultar o imprimir: la ración tal como se sirve, sus calorías, '
      'las de 100 g para comparar, y proteínas, hidratos y grasas. Agrupados por el momento del día en que la app los propone.</p>' % len(HAND))
    o('        <p class="tbl-print reveal"><button type="button" class="btn btn-ghost" onclick="window.print()">Imprimir la tabla</button></p>')
    o('      </div>\n    </header>\n    <div class="container-narrow">')
    o('      <div class="post-body reveal">')
    o('      <p>Cada fila es una entrada de la app, con la ración que la app usa; las que tienen página propia están enlazadas. Las cifras por 100 g se derivan de la ración. Son valores medios: tu plato puede quedar por encima o por debajo según la receta, el aceite y el tamaño.</p>')
    for slot, label in SLOT_NAMES:
        rows = sorted([(k, v) for k, v in HAND.items() if v.get("primarySlot") == slot], key=lambda kv: kv[1]["name_es"].lower())
        if not rows:
            continue
        o('      <h2 id="%s">%s <small>(%d)</small></h2>' % (slot, label, len(rows)))
        o('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">Alimento o plato</th><th scope="col">Ración</th><th scope="col">kcal / ración</th><th scope="col">kcal / 100 g</th><th scope="col">Prot.</th><th scope="col">Hidr.</th><th scope="col">Grasa</th></tr></thead><tbody>')
        for k, v in rows:
            f = figures(k)
            slug = ready_by_app.get(k)
            name = ('<a href="../%s/">%s</a>' % (slug, esc(v["name_es"]))) if slug else esc(v["name_es"])
            o('        <tr><td>%s</td><td>%s, %s g</td><td class="hl">%s</td><td>%s</td><td>%s g</td><td>%s g</td><td>%s g</td></tr>'
              % (name, esc(f["serving_label"]), n(f["serving_g"]), n(f["kcal"]), n(f["per100"]), n(f["protein"]), n(f["carbs"]), n(f["fat"])))
        o('      </tbody></table></div>')
    o('      <h2 id="como-usar">Cómo usar la tabla</h2>')
    o('      <p>Para el día a día, mira la columna de la ración: es lo que apuntas si te comes el plato. Para comparar dos platos, mira la de 100 g. Y para una ración distinta de la de la tabla, pesa la tuya y multiplica: gramos por kcal de 100 g, entre 100. Las bebidas con alcohol llevan parte de su energía en el alcohol, que no aparece en los tres macros; su página lo desglosa.</p>')
    o('      <h2 id="fuentes">De dónde salen las cifras</h2>')
    o('      <p>Son las de la app Fotocal: cada entrada es una ración fijada por la app, compuesta por filas de bases de datos públicas (USDA FoodData Central y CIQUAL 2025) sumadas gramo a gramo, o su cifra de referencia cuando no hay receta. Snapshot de la app: commit %s (%s). Esta página es información general sobre alimentos, no consejo médico ni dietético.</p>' % (APP["_source"]["commit"], APP["_source"]["commit_date"]))
    o('      </div>')
    o(APP_ASIDE.replace("{UP}", "../../"))
    o('      <nav class="dp-related reveal" aria-label="Páginas relacionadas">\n        <h2>Seguir por aquí</h2>\n        <div class="post-nav">')
    o('          <a class="post-nav-item" href="../"><small>Por plato</small><strong>Calorías de los platos españoles, con su página</strong></a>')
    o('          <a class="post-nav-item" href="../../calculadoras/calorias-diarias/"><small>Calculadora</small><strong>%s</strong></a>' % CALCS["calorias-diarias"])
    o('          <a class="post-nav-item" href="../../calculadoras/deficit-calorico/"><small>Calculadora</small><strong>%s</strong></a>' % CALCS["deficit-calorico"])
    o('        </div>\n      </nav>')
    o('    </div>\n  </article>\n</main>')
    o(foot(2))
    return "\n".join(out)

# ── the hub ──────────────────────────────────────────────────────────
def hub_answer(ready, lang):
    """The hub's direct answer to "¿cuántas calorías tiene un plato?" (the
    query the page shows for in Search Console, Nov 2026), computed from the
    main-dish group so it can never drift from the tables below it."""
    import dishes_en
    mains = [(figures(d["app_id"]), d) for d in ready if dishes_en.EN["group_of"].get(d["slug"]) == "platos"]
    mains.sort(key=lambda t: t[0]["kcal"])
    lo, hi, mid = mains[0], mains[-1], mains[len(mains) // 2]
    es = lang == "es"
    fmt = n if es else dishes_en.ne
    nm = lambda t: '<a href="%s/">%s</a>' % (t[1]["slug"], t[1]["name"] if es else dishes_en.display(t[1]))
    text = ('<strong>Respuesta rápida:</strong> un plato de comida española tiene entre %s y %s kcal por ración: '
            'de %s (%s kcal, %s g) a %s (%s kcal, %s g). El plato del medio de los %d de esta tabla es %s, con %s kcal. '
            'Son las cifras de la base de datos de Fotocal, a partir de USDA y CIQUAL.') if es else (
            '<strong>Quick answer:</strong> a Spanish dish has between %s and %s kcal per serving: '
            'from %s (%s kcal, %s g) to %s (%s kcal, %s g). The middle dish of the %d in this table is %s, with %s kcal. '
            'Figures from the Fotocal database, built from USDA and CIQUAL.')
    return '      <div class="answer-box reveal"><p>%s</p></div>' % (text % (
        fmt(lo[0]["kcal"]), fmt(hi[0]["kcal"]), nm(lo), fmt(lo[0]["kcal"]), fmt(lo[0]["serving_g"]), nm(hi), fmt(hi[0]["kcal"]), fmt(hi[0]["serving_g"]),
        len(mains), nm(mid), fmt(mid[0]["kcal"])))


def hub_page(ready):
    title = "Calorías de platos españoles por ración real y por 100 g"
    desc = "Tabla de calorías de %d platos españoles con la ración que se sirve de verdad, por 100 g, proteínas, hidratos y grasas, y la fuente de cada cifra. Sin registro." % len(ready)
    assert len(title) <= TITLE_MAX and 140 <= len(desc) <= 160, (len(title), len(desc))
    path = "calorias/"
    url = SITE + path
    items = [{"@type": "ListItem", "position": i + 1, "name": "Calorías %s %s" % (de(d["article"]), d["name"]), "url": SITE + "calorias/%s/" % d["slug"]} for i, d in enumerate(ready)]
    ld = [
        ld_block({"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc,
                  "inLanguage": "es", "url": url, "publisher": ORG,
                  "mainEntity": {"@type": "ItemList", "itemListElement": items}}),
        ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Calorías de platos", "item": url}]}),
    ]
    out = [head(1, title, desc, path, "\n".join(ld), "website")]
    o = out.append
    o('\n<main id="main">\n  <article class="post dp dp-hub">\n    <header class="post-head">\n      <div class="container-narrow">')
    o('        <nav class="post-crumbs reveal" aria-label="Migas de pan"><a href="../">Inicio</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">Calorías de platos</a></nav>')
    o('        <h1 class="post-title reveal">Calorías de los platos españoles, por ración y por 100 g</h1>')
    o('        <p class="post-lead reveal">¿Cuántas calorías tiene un plato? Una tabla con lo que de verdad se come en España: la ración tal como se sirve, sus calorías, y las de 100 g para poder comparar. Cada plato tiene su página, con el reparto entre proteínas, hidratos y grasas, qué pesa una ración y con qué se parece.</p>')
    o('      </div>\n    </header>\n    <div class="container-narrow">')
    o('      <div class="post-body reveal">')
    import dishes_en
    o(hub_answer(ready, "es"))
    o(dishes_en.group_tables(ready, "es"))
    o('      <p class="dp-table-note">Por ración: la que fija la app Fotocal para cada plato, en gramos tal como se sirve. Las cifras salen de bases de datos públicas (USDA FoodData Central y CIQUAL 2025) sumadas ingrediente a ingrediente; cada página dice exactamente de qué filas.</p>')
    o('      <h2>Cómo leer la tabla</h2>')
    o('      <p>La columna que importa para el día a día es la de la ración: es lo que apuntas si te comes el plato. La de 100 g sirve para comparar platos entre sí y para calcular una ración distinta: pesa lo que tienes, multiplica por la cifra y divide entre 100.</p>')
    o('      <p>Son valores medios. Un cocido de una casa y el de otra no pesan lo mismo ni llevan el mismo chorizo, y una tortilla puede absorber el doble de aceite que otra. Si quieres el número de tu plato y no el de la media, la app lo estima a partir de una foto y te deja corregir los gramos.</p>')
    o('      <h2>Lo que suele sorprender</h2>')
    o('      <ul><li>El plato de cuchara no es el problema: lentejas, garbanzos o un cocido razonable quedan en el rango de una comida normal. Lo que dispara la cuenta es el embutido que lleva dentro y el pan de al lado.</li>'
      '<li>Lo frito pesa poco y suma mucho: cuatro croquetas o una ración de churros se acercan a un plato de lentejas.</li>'
      '<li>Las sopas frías son casi gratis: un bol de gazpacho tiene menos calorías que una tostada con aceite.</li></ul>')
    o('      <p>¿Quieres toda la base de datos de la app en una sola tabla, para consultar o imprimir? Está en la <a href="tabla-de-calorias/">tabla de calorías de alimentos y platos españoles</a>, con las %d entradas agrupadas por momento del día.</p>' % len(HAND))
    o('      <h2>Para seguir</h2>')
    o('      <p>Si la pregunta de fondo es cuánto deberías comer tú, y no cuánto tiene el plato, empieza por <a href="../calculadoras/">las ocho calculadoras</a>: la de <a href="../calculadoras/calorias-diarias/">calorías diarias</a> y la de <a href="../calculadoras/deficit-calorico/">déficit calórico</a> son las dos primeras.</p>')
    o('      <p>Con estas cifras ya sumadas, en el blog: <a href="../blog/calorias-menu-del-dia/">cuánto suma un menú del día, pieza a pieza</a>, <a href="../blog/calorias-de-las-tapas/">lo que cuesta una tarde de tapas</a>, <a href="../blog/best-foods-for-weight-loss/">los alimentos que sacian con menos calorías</a>, <a href="../blog/how-to-count-calories-accurately/">cómo contar calorías con precisión</a>, <a href="../blog/common-calorie-counting-mistakes/">los errores que más se repiten al contar</a> y <a href="../blog/track-calories-without-weighing/">cómo contar sin pesar cada comida</a>.</p>')
    o('      </div>')
    o(download_card("es", "¿Quieres las calorías de tu plato, no las de la media?", "Haz una foto y Fotocal cuenta las calorías por ti, con las cifras de estas páginas.",
                    PLAY + "&utm_source=web&utm_medium=dish&utm_campaign=hub"))
    o('      <p class="post-disclaimer reveal">Información general sobre alimentos, no consejo médico ni dietético.</p>')
    o('    </div>\n  </article>\n</main>')
    o(foot(1))
    return "\n".join(out)


def main():
    ready = [d for d in DISHES if d.get("status") == "ready"]
    slugs = [d["slug"] for d in DISHES]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    for d in DISHES:
        if d["app_id"] not in HAND:
            sys.exit("%s: app dish %s not in app-data.json" % (d["slug"], d["app_id"]))
    ready_by_app = {d["app_id"]: d["slug"] for d in ready}
    # clear and rewrite what we own
    if os.path.isdir(SRC):
        for base, dirs, files in os.walk(SRC, topdown=False):
            for f in files:
                os.remove(os.path.join(base, f))
            for dd in dirs:
                os.rmdir(os.path.join(base, dd))
    os.makedirs(SRC, exist_ok=True)
    import dishes_en
    for d in ready:
        page, fig = dish_page(d, ready_by_app)
        page = bilingual(page, *dishes_en.dish(d, fig, ready_by_app))
        p = os.path.join(SRC, d["slug"])
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(page)
        print("  /calorias/%s/  %s g -> %d kcal (%d/100 g)%s" % (d["slug"], n(fig["serving_g"]), fig["kcal"], fig["per100"], "" if fig["composed"] else ("  [hand figure; recipe rejected >25%]" if fig["rejected"] else "  [hand figure, no recipe]")))
    open(os.path.join(SRC, "index.html"), "w", encoding="utf-8").write(bilingual(hub_page(ready), *dishes_en.hub(ready)))
    tdir = os.path.join(SRC, "tabla-de-calorias"); os.makedirs(tdir, exist_ok=True)
    open(os.path.join(tdir, "index.html"), "w", encoding="utf-8").write(bilingual(table_page(ready_by_app), *dishes_en.table(ready_by_app)))
    print("%d dish pages + hub + table -> src/calorias/ (es + en)" % len(ready))


if __name__ == "__main__":
    main()
