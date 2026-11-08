#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pages of the seo-ranking round (2026-11), in Spanish and English:

    /metodologia/                 how every number on the site is made
    /guias/                       the guides hub: blog clusters + tools
    /comparativa/                 Fotocal and other calorie apps
    /comparativa/fotocal-vs-<x>/  one page per competitor in compare_data.json
    /widget/                      the free embeddable calculators, for bloggers
    /embed/calorias/, /embed/imc/ the iframe pages themselves (noindex)

    python3 tools/gen_pages.py && python3 tools/build_site.py

Facts come from the same files the rest of the site uses: the app data
(tools/dishes/app-data.json), the calculators (assets/js/calc.js), the
comparison facts (tools/compare_data.json, dated, read off each maker's
site; a competitor that is not in that file gets no page and no claim)."""
import datetime, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_calcs as GC                                        # noqa: E402
import gen_dishes as GD                                       # noqa: E402
from compare_table import cell as cmp_cell, date_text        # noqa: E402

ROOT, SITE, esc, ld_block, ORG = GD.ROOT, GD.SITE, GD.esc, GD.ld_block, GD.ORG
SRC = os.path.join(ROOT, "src")
TODAY = "2026-11-08"
LANGS = ("es", "en")
MONTHS = {"es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
          "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}


def fecha(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    return ("%d de %s de %d" if lang == "es" else "%d %s %d") % (d, MONTHS[lang][m - 1], y)


def foot(depth, page, calc=False):
    up = "../" * depth
    return """
<div id="site-footer"></div>
<script src="%sassets/js/i18n.js"></script>
<script src="%sassets/js/layout.js" data-page="%s"></script>
<script src="%sassets/js/main.js"></script>%s
</body>
</html>
""" % (up, up, page, up, ('\n<script src="%sassets/js/calc.js"></script>' % up) if calc else "")


def write(path, html):
    p = os.path.join(SRC, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html)
    print("  /" + path.replace("index.html", ""))


def crumbs_html(lang, items):
    lab = "Migas de pan" if lang == "es" else "Breadcrumb"
    parts = []
    for i, (name, href) in enumerate(items):
        cur = ' aria-current="page"' if i == len(items) - 1 else ""
        parts.append('<a href="%s"%s>%s</a>' % (href, cur, esc(name)))
    return '      <nav class="post-crumbs" aria-label="%s">%s</nav>' % (lab, '<span class="sep" aria-hidden="true">/</span>'.join(parts))


def crumbs_ld(items_abs):
    return ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items_abs)]})


def article(lang, h1, lead, body, updated, crumbs, ld, quick=None, extra_class=""):
    """A plain article page body inside one language block."""
    o = ['  <div class="calc-lang" data-lang-block="%s">' % lang, '    <article class="post %s">' % extra_class,
         '    <header class="post-head"><div class="container-narrow">', crumbs,
         '      <h1 class="post-title">%s</h1>' % esc(h1),
         '      <p class="post-lead">%s</p>' % lead,
         '      <p class="page-updated">%s</p>' % (("Actualizado: <time datetime=\"%s\">%s</time> · Por Fotocal, Madrid" if lang == "es" else
                                                     "Updated: <time datetime=\"%s\">%s</time> · By Fotocal, Madrid") % (updated, fecha(updated, lang))),
         '    </div></header>', '    <div class="container-narrow">']
    if quick:
        o.append('      <div class="answer-box"><p><strong>%s</strong> %s</p></div>' % ("Respuesta rápida:" if lang == "es" else "Quick answer:", quick))
    o += ['      <div class="post-body">', body, '      </div>', '    </div>', '    </article>', ld, '  </div>']
    return "\n".join(o)


def page(depth, path, meta, blocks, page_id, calc=False, noindex=False):
    head = GC.head(depth, meta, path)
    if noindex:
        head = head.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="robots" content="noindex, follow">', 1)
    return head + '\n<main id="main">\n' + "\n".join(blocks) + "\n</main>\n" + foot(depth, page_id, calc)


def check(meta):
    for l, m in meta.items():
        assert len(m["title"]) <= 60, (l, len(m["title"]), m["title"])
        assert 110 <= len(m["desc"]) <= 155, (l, len(m["desc"]), m["desc"])


# ── /metodologia/ ────────────────────────────────────────────────────
def metodologia():
    A = GD.APP
    dbs = {}
    for v in A["foods"].values():
        dbs[v["src"]["db"]] = dbs.get(v["src"]["db"], 0) + 1
    usda = dbs.get("USDA FoodData Central — SR Legacy", 0)
    ciqual = dbs.get("CIQUAL 2025 (ANSES)", 0)
    nfood, nhand = len(A["foods"]), len(A["hand"])
    ncomp = sum(1 for k in GD.HAND if GD.figures(k)["composed"])
    commit, cdate = A["_source"]["commit"], A["_source"]["commit_date"]
    meta = {"es": {"title": "Metodología: de dónde salen nuestras cifras — Fotocal",
                   "desc": "Cómo calcula Fotocal las calorías de cada plato y calculadora: fuentes (USDA, CIQUAL), raciones, fórmulas (Mifflin-St Jeor, OMS, EFSA) y actualizaciones."},
            "en": {"title": "Methodology: where our figures come from — Fotocal",
                   "desc": "How Fotocal works out the calories of every dish and calculator: sources (USDA, CIQUAL), servings, formulas (Mifflin-St Jeor, WHO, EFSA) and how we update."}}
    check(meta)
    body = {
     "es": """
      <h2 id="fuentes">Fuentes de los datos</h2>
      <p>Las cifras de los platos son las de la base de datos de la app Fotocal. Cada alimento básico es una fila de una base de datos pública de composición de alimentos:</p>
      <ul><li><strong><a href="https://fdc.nal.usda.gov/" target="_blank" rel="noopener">USDA FoodData Central</a></strong> (Departamento de Agricultura de EE. UU., SR Legacy): %(usda)d alimentos.</li>
          <li><strong><a href="https://ciqual.anses.fr/" target="_blank" rel="noopener">CIQUAL 2025</a></strong> (ANSES, la agencia francesa de seguridad alimentaria): %(ciqual)d alimentos, sobre todo productos europeos que USDA no recoge bien.</li></ul>
      <p>En total, %(nfood)d alimentos básicos. Cada página de plato dice qué filas usa y su referencia (por ejemplo <code>fdc:168878</code>), para que cualquiera pueda comprobarlas.</p>
      <h2 id="raciones">Cómo se calcula un plato</h2>
      <p>Un plato es una receta: gramos de cada ingrediente, tal como se sirve en España. La app suma la energía y los nutrientes de cada fila, gramo a gramo, aplicando el rendimiento de cocción (lo que pesa un alimento cocinado frente a crudo) y los factores de retención de nutrientes cuando el método de cocción lo pide.</p>
      <ul><li><strong>La ración</strong> es el peso total de esos ingredientes. Las calorías por ración y por 100 g salen siempre de ese mismo peso, así que las dos columnas cuadran.</li>
          <li><strong>La regla del 25 %%:</strong> la app tiene además una cifra de referencia para cada plato. Si la suma de ingredientes se aleja más de un 25 %% de esa referencia, no se mezclan fuentes: se muestra la referencia y la página lo dice. Hoy, %(ncomp)d de los %(nhand)d alimentos y platos de la tabla tienen desglose completo por ingredientes.</li>
          <li><strong>Las bebidas con alcohol</strong> llevan parte de su energía en el alcohol (7 kcal por gramo), que no es proteína, hidrato ni grasa. Las páginas lo muestran aparte, nunca escondido en los hidratos.</li></ul>
      <p>Son valores medios. Tu plato concreto puede tener más o menos aceite, otra receta u otro tamaño: por eso cada página explica qué pesa una ración y cómo cambia la cifra.</p>
      <h2 id="formulas">Las fórmulas de las calculadoras</h2>
      <p>Las <a href="../calculadoras/">calculadoras</a> usan el mismo código que la app, comprobado contra él en 20.000 perfiles al azar:</p>
      <ul><li><strong>Metabolismo basal:</strong> Mifflin-St Jeor (1990): 10 × kg + 6,25 × cm − 5 × edad + 5 (hombre) o − 161 (mujer). Con tu porcentaje de grasa, Katch-McArdle: 370 + 21,6 × masa magra.</li>
          <li><strong>Gasto diario:</strong> metabolismo basal × 1,2 / 1,375 / 1,465 / 1,55 / 1,725 según tu actividad diaria.</li>
          <li><strong>Perder peso:</strong> 7.700 kcal por kilo; el recorte nunca pasa del 25 %% del gasto, y el objetivo nunca baja de 1.200 kcal (mujer) ni 1.500 kcal (hombre).</li>
          <li><strong>Proteína:</strong> 2,0 g/kg para perder peso o ganar músculo y 1,6 g/kg para mantener, sobre el peso con IMC 25 si el tuyo es mayor. Mínimo de la EFSA: 0,83 g/kg.</li>
          <li><strong>Agua:</strong> calorías del día × 1,0–1,5 ml (según actividad) × 0,8, nunca por debajo de la ingesta adecuada de la EFSA × 0,8 ni por encima de 4 litros.</li>
          <li><strong>IMC y peso saludable:</strong> los rangos de la OMS para adultos (18,5 a 24,9).</li></ul>
      <p>La web redondea las calorías objetivo; la app las redondea hacia abajo, así que pueden diferir en 1 kcal.</p>
      <h2 id="actualizacion">Cómo lo actualizamos</h2>
      <ul><li>Las páginas se generan a partir de una copia fechada de la base de datos de la app. La actual es la del commit <code>%(commit)s</code> (%(cdate)s). Cuando la app cambia una cifra, las páginas se regeneran y cambia su fecha de actualización.</li>
          <li>Antes de publicar, un programa comprueba cada página: que las cifras de ración y de 100 g cuadran, que los precios y los límites del plan gratis son los mismos en toda la web, y que no hay enlaces rotos.</li>
          <li>Si ves un error, escríbenos desde la <a href="../contact/">página de contacto</a> y lo corregimos.</li></ul>
      <h2 id="quien">Quién hace Fotocal</h2>
      <p>Fotocal lo diseña y lo programa una sola persona, en Madrid (<a href="../about/">más sobre nosotros</a>). No somos un servicio médico: las cifras y las calculadoras son orientativas y no sustituyen a un profesional sanitario.</p>""",
     "en": """
      <h2 id="sources">Data sources</h2>
      <p>The dish figures are the ones in the Fotocal app's database. Each basic food is a row from a public food composition database:</p>
      <ul><li><strong><a href="https://fdc.nal.usda.gov/" target="_blank" rel="noopener">USDA FoodData Central</a></strong> (US Department of Agriculture, SR Legacy): %(usda)d foods.</li>
          <li><strong><a href="https://ciqual.anses.fr/" target="_blank" rel="noopener">CIQUAL 2025</a></strong> (ANSES, the French food safety agency): %(ciqual)d foods, mostly European products USDA does not cover well.</li></ul>
      <p>%(nfood)d basic foods in all. Every dish page says which rows it uses and their reference (for example <code>fdc:168878</code>), so anyone can check them.</p>
      <h2 id="servings">How a dish is worked out</h2>
      <p>A dish is a recipe: grams of each ingredient, as it is served in Spain. The app adds up the energy and nutrients of each row, gram by gram, applying cooking yields (what a food weighs cooked versus raw) and nutrient retention factors where the cooking method calls for them.</p>
      <ul><li><strong>The serving</strong> is the total weight of those ingredients. Calories per serving and per 100 g always come from that same weight, so the two columns agree.</li>
          <li><strong>The 25%% rule:</strong> the app also holds a reference figure for each dish. If the ingredient sum is more than 25%% away from it, sources are not mixed: the reference is shown and the page says so. Today %(ncomp)d of the %(nhand)d foods and dishes in the table have a full ingredient breakdown.</li>
          <li><strong>Alcoholic drinks</strong> carry part of their energy as alcohol (7 kcal per gram), which is not protein, carbohydrate or fat. The pages show it separately, never hidden in the carbs.</li></ul>
      <p>These are averages. Your own plate may have more or less oil, another recipe or another size: that is why every page explains what a serving weighs and how the number changes.</p>
      <h2 id="formulas">The calculators' formulas</h2>
      <p>The <a href="../calculadoras/">calculators</a> use the same code as the app, checked against it on 20,000 random profiles:</p>
      <ul><li><strong>Basal metabolism:</strong> Mifflin-St Jeor (1990): 10 × kg + 6.25 × cm − 5 × age + 5 (man) or − 161 (woman). With your body fat, Katch-McArdle: 370 + 21.6 × lean mass.</li>
          <li><strong>Daily burn:</strong> basal metabolism × 1.2 / 1.375 / 1.465 / 1.55 / 1.725 for your day-to-day activity.</li>
          <li><strong>Losing weight:</strong> 7,700 kcal per kilo; the cut is never more than 25%% of what you burn, and the target never goes below 1,200 kcal (women) or 1,500 kcal (men).</li>
          <li><strong>Protein:</strong> 2.0 g/kg to lose weight or build muscle and 1.6 g/kg to maintain, on the weight at BMI 25 if yours is higher. EFSA minimum: 0.83 g/kg.</li>
          <li><strong>Water:</strong> daily calories × 1.0–1.5 ml (by activity) × 0.8, never below EFSA's adequate intake × 0.8 or above 4 litres.</li>
          <li><strong>BMI and healthy weight:</strong> the WHO adult bands (18.5 to 24.9).</li></ul>
      <p>The website rounds calorie targets; the app rounds them down, so they can differ by 1 kcal.</p>
      <h2 id="updates">How we update</h2>
      <ul><li>Pages are generated from a dated copy of the app's database. The current one is commit <code>%(commit)s</code> (%(cdate)s). When the app changes a figure, the pages are regenerated and their update date changes.</li>
          <li>Before publishing, a program checks every page: that serving and per-100 g figures agree, that prices and free-plan limits are the same across the site, and that there are no broken links.</li>
          <li>If you spot an error, write to us from the <a href="../contact/">contact page</a> and we will fix it.</li></ul>
      <h2 id="who">Who makes Fotocal</h2>
      <p>Fotocal is designed and built by one person in Madrid (<a href="../about/">more about us</a>). We are not a medical service: the figures and calculators are for guidance and do not replace a health professional.</p>"""}
    vals = dict(usda=usda, ciqual=ciqual, nfood=nfood, nhand=nhand, ncomp=ncomp, commit=commit, cdate=cdate)
    quick = {"es": "Las calorías de cada plato salen de sumar, gramo a gramo, sus ingredientes en bases de datos públicas (USDA y CIQUAL), con la ración tal como se sirve en España. Las calculadoras usan las fórmulas de la app: Mifflin-St Jeor, los rangos de la OMS y las referencias de la EFSA.",
             "en": "Each dish's calories come from adding up its ingredients gram by gram, using public databases (USDA and CIQUAL), with the serving as it is served in Spain. The calculators use the app's formulas: Mifflin-St Jeor, the WHO bands and EFSA references."}
    blocks = []
    for l in LANGS:
        home, me = ("Inicio", "Metodología") if l == "es" else ("Home", "Methodology")
        ld = "\n".join([
            ld_block({"@context": "https://schema.org", "@type": "Article", "headline": meta[l]["title"].replace(" — Fotocal", ""), "description": meta[l]["desc"],
                      "inLanguage": l, "url": SITE + "metodologia/", "datePublished": TODAY, "dateModified": TODAY, "author": ORG, "publisher": ORG}),
            crumbs_ld([(home, SITE), (me, SITE + "metodologia/")])])
        h1 = "Cómo calculamos nuestras cifras" if l == "es" else "How we work out our figures"
        lead = ("De dónde salen las calorías de cada plato, cómo se fija la ración y qué fórmulas usan las calculadoras. Para que puedas comprobar cualquier número de esta web."
                if l == "es" else "Where each dish's calories come from, how the serving is set and which formulas the calculators use, so you can check any number on this site.")
        blocks.append(article(l, h1, lead, body[l] % vals, TODAY, crumbs_html(l, [(home, "../"), (me, "./")]), ld, quick[l]))
    write("metodologia/index.html", page(1, "metodologia/", meta, blocks, "metodologia"))


# ── /guias/ ──────────────────────────────────────────────────────────
CLUSTERS = [
    ("calories", {"es": "Contar calorías", "en": "Counting calories"}, ["calorias-diarias", "deficit-calorico"]),
    ("weightloss", {"es": "Perder peso", "en": "Losing weight"}, ["deficit-calorico", "peso-saludable"]),
    ("nutrition", {"es": "Nutrición", "en": "Nutrition"}, ["proteinas", "macros"]),
    ("eating", {"es": "Comer bien a diario", "en": "Everyday eating"}, ["calorias-diarias", "agua"]),
    ("movement", {"es": "Movimiento y descanso", "en": "Movement and sleep"}, ["tmb", "agua"]),
    ("mindset", {"es": "Hábitos y mentalidad", "en": "Habits and mindset"}, ["imc"]),
]


def guias():
    posts = []
    for f in glob.glob(os.path.join(ROOT, "tools", "blog", "posts", "*.json")):
        j = json.load(open(f, encoding="utf-8"))
        posts.append(j)
    posts.sort(key=lambda j: j.get("date", ""), reverse=True)
    calcs = {c["slug"]: c for c in GC.CALCS}
    meta = {"es": {"title": "Guías para contar calorías y comer mejor — Fotocal",
                   "desc": "Todas las guías de Fotocal por temas: contar calorías, perder peso, nutrición y comida española, con sus calculadoras y la tabla de calorías de platos."},
            "en": {"title": "Guides to counting calories and eating well — Fotocal",
                   "desc": "Every Fotocal guide by topic: counting calories, losing weight, nutrition and Spanish food, with the matching calculators and the dish calorie table."}}
    check(meta)
    blocks = []
    for l in LANGS:
        home, me = ("Inicio", "Guías") if l == "es" else ("Home", "Guides")
        body = []
        body.append('      <p>%s</p>' % ("Empieza por el tema que te interesa. Cada grupo tiene sus guías y las calculadoras que van con ellas. Para las calorías de lo que comes, está la <a href=\"../calorias/\">tabla de platos españoles</a>."
                                         if l == "es" else "Start with the topic you need. Each group has its guides and the calculators that go with them. For the calories of what you eat, see the <a href=\"../calorias/\">Spanish dish table</a>."))
        items = []
        for key, name, tools in CLUSTERS:
            ps = [p for p in posts if p.get("category") == key and (l in p)]
            if not ps:
                continue
            body.append('      <h2 id="%s">%s</h2>' % (key, name[l]))
            body.append('      <ul class="guide-list">')
            for p in ps:
                body.append('        <li><a href="../blog/%s/">%s</a><span>%s</span></li>' % (p["slug"], esc(p[l]["title"]), esc(re.sub(r"<[^>]+>", "", p[l]["lead"]))[:170].rsplit(" ", 1)[0] + "…"))
                items.append((p[l]["title"], SITE + "blog/%s/" % p["slug"]))
            body.append('      </ul>')
            body.append('      <p class="guide-tools">%s %s</p>' % ("Calculadoras para este tema:" if l == "es" else "Calculators for this topic:",
                        " · ".join('<a href="../calculadoras/%s/">%s</a>' % (t, esc(calcs[t][l]["h1"])) for t in tools)))
        ld = "\n".join([
            ld_block({"@context": "https://schema.org", "@type": "CollectionPage", "name": meta[l]["title"].replace(" — Fotocal", ""), "description": meta[l]["desc"],
                      "inLanguage": l, "url": SITE + "guias/", "publisher": ORG,
                      "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": u} for i, (n, u) in enumerate(items)]}}),
            crumbs_ld([(home, SITE), (me, SITE + "guias/")])])
        h1 = "Guías para contar calorías y comer mejor" if l == "es" else "Guides to counting calories and eating well"
        lead = ("Todo lo que hemos escrito, ordenado por temas, con cifras de comida española y las calculadoras al lado."
                if l == "es" else "Everything we have written, sorted by topic, with Spanish food figures and the calculators alongside.")
        blocks.append(article(l, h1, lead, "\n".join(body), TODAY, crumbs_html(l, [(home, "../"), (me, "./")]), ld, extra_class="guides"))
    write("guias/index.html", page(1, "guias/", meta, blocks, "blog"))


# ── /comparativa/ ────────────────────────────────────────────────────
VS = {"MyFitnessPal": "myfitnesspal", "Yazio": "yazio", "Cal AI": "cal-ai"}


def cmp_table(data, cols):
    th = "".join("<th>%s</th>" % esc(c) for c in cols)
    rows = []
    for row in data["rows"]:
        tds = cmp_cell("Fotocal", row["fotocal"], us=True) + "".join(cmp_cell(c, row["cells"][c]) for c in cols)
        rows.append('<tr%s><th data-i18n="%s"></th>%s</tr>' % (' class="compare-price"' if row["key"] == "cmp.r12" else "", row["key"], tds))
    return ('      <div class="compare-wrap"><table class="compare"><thead><tr><th class="col-feat" data-i18n="cmp.hFeat">Feature</th><th class="compare-us">Fotocal</th>%s</tr></thead><tbody>\n        %s\n      </tbody></table></div>'
            % (th, "\n        ".join(rows)))


def comparativa():
    data = json.load(open(os.path.join(ROOT, "tools", "compare_data.json"), encoding="utf-8"))
    checked = data["checked_on"]
    for comp, slug in VS.items():
        assert comp in data["columns"], comp
        meta = {"es": {"title": "Fotocal vs %s: comparativa de apps de calorías" % comp,
                       "desc": "Fotocal frente a %s, función a función: escaneo por foto, código de barras, voz, coach y precio, con lo que cada fabricante declara y la fecha." % comp},
                "en": {"title": "Fotocal vs %s: calorie app comparison" % comp,
                       "desc": "Fotocal and %s side by side: photo scanning, barcode, voice, coach and price, from what each maker states on its own site, with the date checked." % comp}}
        for l in LANGS:
            if len(meta[l]["title"]) > 60:
                meta[l]["title"] = "Fotocal vs %s: comparativa" % comp if l == "es" else "Fotocal vs %s: comparison" % comp
        check(meta)
        why = {r["key"]: r.get("why", "") for r in data["rows"]}
        blocks = []
        for l in LANGS:
            home, hub = ("Inicio", "Comparativa") if l == "es" else ("Home", "Comparison")
            name = "Fotocal vs %s" % comp
            d = date_text(checked, l)
            quick = ({"es": "Fotocal es una app de Android que cuenta calorías con una foto y está pensada para la comida española. Su plan gratis, sin tarjeta, incluye 2 escaneos con IA al día, 1 registro por voz al día, y código de barras y Coach Kal sin límite. Abajo, lo que %s declara en su propia web, comprobado el %s." % (comp, d),
                      "en": "Fotocal is an Android app that counts calories from a photo, built around Spanish food. Its free plan, with no card, includes 2 AI scans a day, 1 voice log a day, and unlimited barcode scanner and Coach Kal. Below is what %s states on its own site, checked on %s." % (comp, d)})[l]
            body = [cmp_table(data, [comp])]
            body.append('      <p class="dp-table-note">%s</p>' % esc(data["note"][l].replace("{date}", d)))
            body.append('      <h2>%s</h2>' % ("Qué significa cada fila" if l == "es" else "What each row means"))
            body.append('      <p>%s</p>' % ("Las notas de la tabla son las que usamos para la tabla comparativa de la página de inicio. Fuentes de %s: %s." % (comp, esc(data["checked_at"][comp]))
                                             if l == "es" else "These are the same notes behind the comparison table on the home page. %s sources: %s." % (comp, esc(data["checked_at"][comp]))))
            body.append('      <h2>%s</h2>' % ("¿Cuál elegir?" if l == "es" else "Which one to choose?"))
            body.append('      <p>%s</p>' % ({"es": "Depende de lo que necesites. Si quieres apuntar lo que comes con una foto, con raciones de comida española y sin pagar para empezar, Fotocal está hecha para eso. Si usas iPhone, Fotocal no está disponible: solo es para Android. Si ya tienes años de registros en %s, mirar qué te costaría cambiar también cuenta. Las funciones y precios de otras apps cambian: comprueba su web antes de decidir." % comp,
                                                "en": "It depends on what you need. If you want to log what you eat from a photo, with Spanish food servings and without paying to start, that is what Fotocal is built for. If you use an iPhone, Fotocal is not available: it is Android only. If you already have years of logs in %s, the cost of switching counts too. Other apps' features and prices change: check their site before you decide." % comp})[l])
            body.append('      <p>%s</p>' % ("Más comparativas en la <a href=\"../\">página de comparativas</a>, y cómo calculamos nuestras cifras en la <a href=\"../../metodologia/\">metodología</a>."
                                             if l == "es" else "More in the <a href=\"../\">comparison page</a>, and how we work out our figures in the <a href=\"../../metodologia/\">methodology</a>."))
            body.append(GD.download_card(l, "¿Quieres probarla?" if l == "es" else "Want to try it?",
                                         "Haz una foto y Fotocal cuenta las calorías por ti." if l == "es" else "Snap a photo and Fotocal counts the calories for you.",
                                         GD.PLAY + "&utm_source=web&utm_medium=compare&utm_campaign=vs-" + slug))
            ld = "\n".join([ld_block({"@context": "https://schema.org", "@type": "Article", "headline": meta[l]["title"].replace(" — Fotocal", ""), "description": meta[l]["desc"],
                                      "inLanguage": l, "url": SITE + "comparativa/fotocal-vs-%s/" % slug, "datePublished": TODAY, "dateModified": TODAY, "author": ORG, "publisher": ORG}),
                            crumbs_ld([(home, SITE), (hub, SITE + "comparativa/"), (name, SITE + "comparativa/fotocal-vs-%s/" % slug)])])
            h1 = name + (": ¿qué app para contar calorías elegir?" if l == "es" else ": which calorie app to choose?")
            lead = ("Una comparación con fecha y fuentes: lo que %s declara en su web frente a lo que hace Fotocal, leído del código de la app." % comp
                    if l == "es" else "A dated, sourced comparison: what %s states on its site versus what Fotocal does, read off the app's code." % comp)
            blocks.append(article(l, h1, lead, "\n".join(body), TODAY, crumbs_html(l, [(home, "../../"), (hub, "../"), (name, "./")]), ld, quick))
        write("comparativa/fotocal-vs-%s/index.html" % slug, page(2, "comparativa/fotocal-vs-%s/" % slug, meta, blocks, "comparativa"))

    meta = {"es": {"title": "Apps para contar calorías en España: comparativa",
                   "desc": "Fotocal, Cal AI, MyFitnessPal y Yazio, función a función y con fecha: qué incluye cada plan gratis, qué es de pago y cuánto cuesta al año."},
            "en": {"title": "Calorie counting apps in Spain: a comparison",
                   "desc": "Fotocal, Cal AI, MyFitnessPal and Yazio, feature by feature and dated: what each free plan includes, what is paid and what it costs a year."}}
    check(meta)
    blocks = []
    for l in LANGS:
        home, hub = ("Inicio", "Comparativa") if l == "es" else ("Home", "Comparison")
        d = date_text(checked, l)
        body = [cmp_table(data, data["columns"]), '      <p class="dp-table-note">%s</p>' % esc(data["note"][l].replace("{date}", d))]
        body.append('      <h2>%s</h2><ul>' % ("Comparaciones una a una" if l == "es" else "One-to-one comparisons"))
        for comp, slug in VS.items():
            body.append('        <li><a href="fotocal-vs-%s/">Fotocal vs %s</a></li>' % (slug, comp))
        body.append('      </ul>')
        body.append('      <h2>%s</h2>' % ("Cómo elegir app para contar calorías" if l == "es" else "How to choose a calorie counting app"))
        body.append('      <p>%s</p>' % ({"es": "Mira tres cosas: cuánto te cuesta apuntar una comida (una foto, un código de barras o escribirlo), si la base de datos conoce lo que comes tú (aquí, comida española con raciones reales) y qué incluye el plan gratis sin trucos. No publicamos un «ranking»: cada app encaja con una forma de comer distinta. La tabla dice lo que declara cada fabricante, con fecha.",
                                            "en": "Look at three things: how much effort logging a meal takes (a photo, a barcode or typing), whether the database knows what you eat (here, Spanish food with real servings) and what the free plan really includes. We do not publish a ranking: each app suits a different way of eating. The table shows what each maker states, with the date."})[l])
        ld = "\n".join([ld_block({"@context": "https://schema.org", "@type": "Article", "headline": meta[l]["title"], "description": meta[l]["desc"], "inLanguage": l,
                                  "url": SITE + "comparativa/", "datePublished": TODAY, "dateModified": TODAY, "author": ORG, "publisher": ORG}),
                        crumbs_ld([(home, SITE), (hub, SITE + "comparativa/")])])
        quick = ({"es": "Fotocal cuenta calorías con una foto y su plan gratis incluye 2 escaneos con IA al día, 1 registro por voz al día, y código de barras y Coach Kal sin límite, sin tarjeta. Solo para Android. La tabla compara sus funciones con Cal AI, MyFitnessPal y Yazio según lo que cada uno declara (%s)." % d,
                  "en": "Fotocal counts calories from a photo and its free plan includes 2 AI scans a day, 1 voice log a day, and unlimited barcode scanner and Coach Kal, with no card. Android only. The table compares its features with Cal AI, MyFitnessPal and Yazio from what each one states (%s)." % d})[l]
        h1 = "Apps para contar calorías en España: comparativa" if l == "es" else "Calorie counting apps in Spain: a comparison"
        lead = ("Lo que incluye cada app, gratis y de pago, según su propio fabricante y con la fecha en que lo comprobamos."
                if l == "es" else "What each app includes, free and paid, according to its own maker and with the date we checked.")
        blocks.append(article(l, h1, lead, "\n".join(body), TODAY, crumbs_html(l, [(home, "../"), (hub, "./")]), ld, quick))
    write("comparativa/index.html", page(1, "comparativa/", meta, blocks, "comparativa"))


# ── /widget/ and /embed/ ─────────────────────────────────────────────
EMBEDS = [("calorias", "calorias-diarias"), ("imc", "imc")]


def widget():
    GC.NEEDS = GC.needs()
    calcs = {c["slug"]: c for c in GC.CALCS}
    for path, slug in EMBEDS:
        c = calcs[slug]
        meta = {l: {"title": c[l]["h1"] + " (widget)", "desc": (c[l]["desc"])} for l in LANGS}
        blocks = []
        for l in LANGS:
            res = GC.result(c, l)
            res = re.sub(r'\n\s*<aside class="dl-card.*?</aside>', "", res, flags=re.S)
            res = re.sub(r'\n\s*<button class="calc-share".*?</button>', "", res, flags=re.S)
            credit = ('<p class="embed-credit"><a href="https://getfotocal.com/%scalculadoras/%s/" target="_blank" rel="noopener">%s</a></p>'
                      % ("en/" if l == "en" else "", slug, "Calculadora de Fotocal" if l == "es" else "Calculator by Fotocal"))
            blocks.append('  <div class="calc-lang embed" data-lang-block="%s">\n    <h1 class="embed-h">%s</h1>\n%s\n%s\n    %s\n  </div>' % (l, esc(c[l]["h1"]), GC.form(c["kind"], l, slug), res, credit))
        html = page(2, "embed/%s/" % path, meta, blocks, "embed", calc=True, noindex=True)
        html = html.replace('<body class="page-fx page-post page-calc">', '<body class="page-calc page-embed">').replace('<div id="site-nav"></div>\n', "").replace('\n<div id="site-footer"></div>', "")
        write("embed/%s/index.html" % path, html)

    meta = {"es": {"title": "Calculadora gratis para tu web — Fotocal",
                   "desc": "Pon en tu blog o en la web de tu consulta la calculadora de calorías o de IMC de Fotocal: gratis, sin registro, sin anuncios y sin enviar datos."},
            "en": {"title": "Free calculator widget for your site — Fotocal",
                   "desc": "Add Fotocal's calorie or BMI calculator to your blog or practice website: free, no sign-up, no ads and no data sent anywhere. Copy, paste, done."}}
    check(meta)
    blocks = []
    for l in LANGS:
        home, me = ("Inicio", "Widget") if l == "es" else ("Home", "Widget")
        body = ['      <p>%s</p>' % ("Si escribes sobre nutrición, entrenas a gente o tienes una consulta, puedes poner nuestras calculadoras en tu web. Son gratis, no llevan anuncios ni cookies de terceros, y los datos que se escriben no salen del navegador. Solo te pedimos que dejes el enlace de crédito debajo."
                                    if l == "es" else "If you write about nutrition, train people or run a practice, you can put our calculators on your site. They are free, carry no ads or third-party cookies, and what people type never leaves the browser. All we ask is that you keep the credit link underneath.")]
        for path, slug in EMBEDS:
            c = calcs[slug]
            src = "https://getfotocal.com/%sembed/%s/" % ("en/" if l == "en" else "", path)
            credit_url = "https://getfotocal.com/%scalculadoras/%s/" % ("en/" if l == "en" else "", slug)
            code = ('<iframe src="%s" title="%s" width="100%%" height="%d" style="border:0;max-width:560px" loading="lazy"></iframe>\n<p><a href="%s">%s</a></p>'
                    % (src, c[l]["h1"], 760 if path == "calorias" else 640, credit_url, "Calculadora de Fotocal" if l == "es" else "Calculator by Fotocal"))
            body.append('      <h2>%s</h2>' % esc(c[l]["h1"]))
            body.append('      <p>%s</p>' % ("Copia este código y pégalo en tu página (en WordPress, en un bloque «HTML personalizado»):" if l == "es" else "Copy this code and paste it into your page (in WordPress, in a \"Custom HTML\" block):"))
            body.append('      <pre class="embed-code"><code>%s</code></pre>' % esc(code))
            body.append('      <iframe src="../embed/%s/" title="%s" width="100%%" height="%d" style="border:0;max-width:560px" loading="lazy"></iframe>' % (path, esc(c[l]["h1"]), 760 if path == "calorias" else 640))
        body.append('      <h2>%s</h2>' % ("Condiciones" if l == "es" else "Terms"))
        body.append('      <ul><li>%s</li><li>%s</li><li>%s</li></ul>' % ((
            "Gratis, para webs personales, blogs, gimnasios y consultas.", "Mantén el enlace «Calculadora de Fotocal» visible debajo del widget.", "Las fórmulas están explicadas en nuestra <a href=\"../metodologia/\">metodología</a>. Son orientativas y no sustituyen a un profesional sanitario.")
            if l == "es" else (
            "Free, for personal sites, blogs, gyms and practices.", "Keep the \"Calculator by Fotocal\" link visible under the widget.", "The formulas are explained in our <a href=\"../metodologia/\">methodology</a>. They are for guidance and do not replace a health professional.")))
        ld = "\n".join([ld_block({"@context": "https://schema.org", "@type": "WebPage", "name": meta[l]["title"].replace(" — Fotocal", ""), "description": meta[l]["desc"],
                                  "inLanguage": l, "url": SITE + "widget/", "publisher": ORG}), crumbs_ld([(home, SITE), (me, SITE + "widget/")])])
        h1 = "Pon una calculadora gratis en tu web" if l == "es" else "Put a free calculator on your site"
        lead = ("Las calculadoras de calorías y de IMC de Fotocal, listas para copiar y pegar en tu blog o tu web."
                if l == "es" else "Fotocal's calorie and BMI calculators, ready to copy and paste into your blog or website.")
        blocks.append(article(l, h1, lead, "\n".join(body), TODAY, crumbs_html(l, [(home, "../"), (me, "./")]), ld))
    write("widget/index.html", page(1, "widget/", meta, blocks, "calculadoras"))


def main():
    metodologia()
    guias()
    comparativa()
    widget()


if __name__ == "__main__":
    main()
