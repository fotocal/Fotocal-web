# -*- coding: utf-8 -*-
"""«Datos de Fotocal» boxes (GEO round, 22-11-2026).

Small statistics worked out from the app's own food catalogue
(tools/dishes/app-data.json: the dishes, their servings and their
ingredient-by-ingredient recipes, with USDA / CIQUAL rows). NOT from user
data: nothing here reads what anybody logged.

Every figure is computed at build time with gen_dishes.figures() and
compose(), the same functions the dish pages use, so a box can never drift
from the tables it sits next to. Used by:
  · gen_dishes.hub_page / dishes_en.hub        box("oil", lang, prefix)
  · gen_blog (marker <!--datos:NAME--> in a post body)  box(NAME, lang, prefix)
"""
import json
import os
import statistics as st

import gen_dishes as G

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READY = {d["app_id"]: d["slug"] for d in json.load(open(os.path.join(ROOT, "tools", "dishes", "dishes.json"), encoding="utf-8"))["dishes"]
         if d.get("status") == "ready"}
GROUP_OF = json.load(open(os.path.join(ROOT, "tools", "dishes", "en.json"), encoding="utf-8"))["group_of"]
OIL = "aceite_oliva"
OIL_10G = G.FOODS[OIL]["per100"]["kcal"] / 10          # kcal in 10 g of olive oil


def num(x, lang, dec=0):
    s = ("{:,.%df}" % dec).format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".") if lang == "es" else s


def name(app_id, lang):
    h = G.HAND[app_id]
    s = h["name_es"] if lang == "es" else h["name_en"]
    return s[0].upper() + s[1:]


def link(app_id, lang, prefix):
    nm = name(app_id, lang)
    return '<a href="%s%s/">%s</a>' % (prefix, READY[app_id], nm) if app_id in READY else nm


def frame(lang, title, inner, note_extra=""):
    lab = "Datos de Fotocal" if lang == "es" else "Fotocal data"
    note = ("Cálculo propio sobre la base de datos de alimentos de la app (raciones de Fotocal, cifras de USDA y CIQUAL). "
            "No usa datos de ningún usuario." if lang == "es" else
            "Our own calculation on the app's food database (Fotocal servings, USDA and CIQUAL figures). "
            "It uses no user data.")
    return ('      <aside class="datos-box reveal" aria-label="%s">\n        <p class="datos-kicker">%s</p>\n        <p class="datos-title">%s</p>\n%s\n'
            '        <p class="datos-note">%s%s</p>\n      </aside>') % (lab, lab, title, inner, note, note_extra)


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '        <div class="table-wrap"><table class="datos-table"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (h, b)


# ── 1. how much of a dish's calories the olive oil brings (hub) ─────
def oil_stats():
    composed, rows = 0, []
    for app_id, rec in G.RECIPES.items():
        if app_id not in G.HAND or app_id == "aceite-de-oliva":
            continue
        f = G.figures(app_id)
        if not f["composed"]:
            continue
        composed += 1
        oil = [l for l in rec if l["foodId"] == OIL]
        if oil:
            _, v = G.compose(oil)
            rows.append({"id": app_id, "kcal": f["kcal"], "oil_g": sum(l["grams"] for l in oil), "oil_kcal": v["kcal"], "share": v["kcal"] / f["kcal"]})
    shares = sorted(r["share"] for r in rows)
    return {"composed": composed, "with_oil": len(rows), "median": st.median(shares),
            "over_third": sum(1 for s in shares if s >= 1 / 3), "rows": rows}


def box_oil(lang, prefix):
    s = oil_stats()
    es = lang == "es"
    pub = sorted((r for r in s["rows"] if r["id"] in READY and GROUP_OF.get(READY[r["id"]]) in ("platos", "tapas")), key=lambda r: -r["share"])[:6]
    rows = [[link(r["id"], lang, prefix), num(r["kcal"], lang), "%s g · %s kcal" % (num(r["oil_g"], lang), num(r["oil_kcal"], lang)),
             "%s %%" % num(r["share"] * 100, lang) if es else "%s%%" % num(r["share"] * 100, lang)] for r in pub]
    pct = lambda x: ("%s %%" if es else "%s%%") % num(x * 100, lang)
    if es:
        title = "De dónde salen las calorías de un plato: el aceite"
        p = ('        <p>De los %d platos y alimentos que la app calcula ingrediente a ingrediente, %d llevan aceite de oliva. '
             'En la mitad de ellos el aceite pone al menos el %s de las calorías del plato, y en %d pasa de un tercio. '
             'Cada 10 g de aceite son %s kcal: por eso el mismo plato puede variar tanto de una cocina a otra.</p>') % (
            s["composed"], s["with_oil"], pct(s["median"]), s["over_third"], num(OIL_10G, lang))
        head = ["Plato", "kcal por ración", "Aceite", "Parte del aceite"]
    else:
        title = "Where a dish's calories come from: the oil"
        p = ('        <p>Of the %d dishes and foods the app works out ingredient by ingredient, %d contain olive oil. '
             'In half of them the oil brings at least %s of the dish\'s calories, and in %d it is over a third. '
             'Every 10 g of oil is %s kcal: that is why the same dish can vary so much from one kitchen to another.</p>') % (
            s["composed"], s["with_oil"], pct(s["median"]), s["over_third"], num(OIL_10G, lang))
        head = ["Dish", "kcal per serving", "Oil", "Share from oil"]
    return frame(lang, title, p + "\n" + table(head, rows))


# ── 2. how much the portion changes the total (how to count) ────────
PORTION_IDS = ["paella-valenciana", "lentejas-estofadas", "macarrones-con-tomate", "tortilla-espanola", "patatas-bravas"]


def box_portion(lang, prefix):
    es = lang == "es"
    rows, diffs = [], []
    for i in PORTION_IDS:
        f = G.figures(i)
        lo, hi = f["kcal"] * 0.75, f["kcal"] * 1.25
        diffs.append(hi - lo)
        rows.append([link(i, lang, prefix), "%s g · %s kcal" % (num(f["serving_g"], lang), num(f["kcal"], lang)),
                     num(lo, lang), num(hi, lang), ("+%s kcal" % num(hi - lo, lang))])
    mx = max(diffs)
    if es:
        title = "Cuánto cambia el total si te sirves más o menos"
        p = ('        <p>La misma comida, con la ración de la app, servida un 25 %% más pequeña o un 25 %% más grande. '
             'Ese margen es fácil de cometer a ojo, y en un plato principal llega a %s kcal entre una ración y otra. '
             'Además, cada 10 g de aceite que se van en la sartén suman %s kcal. Por eso conviene pesar al principio: '
             'el error de la ración pesa más que el de la base de datos.</p>') % (num(mx, lang), num(OIL_10G, lang))
        head = ["Plato", "Ración de Fotocal", "25 % menos (kcal)", "25 % más (kcal)", "Diferencia"]
    else:
        title = "How much the total changes if you serve yourself more or less"
        p = ('        <p>The same meal, with the app\'s serving, made 25%% smaller or 25%% bigger. '
             'That margin is easy to get wrong by eye, and on a main dish it reaches %s kcal from one serving to the other. '
             'On top of that, every 10 g of oil that goes into the pan adds %s kcal. That is why it pays to weigh at first: '
             'the portion error weighs more than the database error.</p>') % (num(mx, lang), num(OIL_10G, lang))
        head = ["Dish", "Fotocal serving", "25% less (kcal)", "25% more (kcal)", "Difference"]
    return frame(lang, title, p + "\n" + table(head, rows))


# ── 3. what 400 kcal buys (satiating foods) ─────────────────────────
KCAL_400_IDS = ["gazpacho", "manzana", "merluza-a-la-plancha", "lentejas-estofadas", "patatas-bravas", "croissant", "almendras"]


def box_400(lang, prefix):
    es = lang == "es"
    rows = []
    for i in KCAL_400_IDS:
        f = G.figures(i)
        g = 400 / f["per100"] * 100
        rows.append([link(i, lang, prefix), num(f["per100"], lang), num(round(g, -1), lang) + " g",
                     num(400 / f["kcal"], lang, 1)])
    if es:
        title = "Qué te dan 400 kcal, alimento por alimento"
        p = ('        <p>Las mismas 400 kcal, en gramos de comida y en raciones de la app. Arriba, lo que llena el plato; '
             'abajo, lo que concentra las calorías en poco volumen. Es la densidad calórica de la que habla este artículo, con cifras.</p>')
        head = ["Alimento", "kcal por 100 g", "400 kcal son", "Raciones de Fotocal"]
    else:
        title = "What 400 kcal gets you, food by food"
        p = ('        <p>The same 400 kcal, in grams of food and in app servings. At the top, what fills the plate; '
             'at the bottom, what packs the calories into a small volume. It is the calorie density this article is about, in numbers.</p>')
        head = ["Food", "kcal per 100 g", "400 kcal is", "Fotocal servings"]
    return frame(lang, title, p + "\n" + table(head, rows))


BOXES = {"oil": box_oil, "portion": box_portion, "400": box_400}


def box(key, lang, prefix):
    return BOXES[key](lang, prefix)


if __name__ == "__main__":
    s = oil_stats()
    print({k: v for k, v in s.items() if k != "rows"})
    for k in BOXES:
        print(box(k, "es", "../../calorias/"))


# ── real app screens for pages without a content image (GEO round) ──
# Same files and the same alt text as the feature pages that already show
# them (assets/img/screens/, real captures of the app).
SHOTS = {
    "home-day": ("app-home-day", (440, 660), 440, 650,
                 "Pantalla real de la app: el inicio tras guardar, 682 kcal ingeridas y 817 restantes, con el desayuno y la comida registrados frente a su objetivo",
                 "Real app screen: the home after saving, 682 kcal eaten and 817 left, with breakfast and lunch logged against their targets",
                 "En la app, tu objetivo de calorías del día y lo que te queda, comida a comida.",
                 "In the app, your calorie target for the day and what you have left, meal by meal."),
    "progress": ("app-progress", (600, 900), 600, 1124,
                 "Pantalla real de la app: Mi progreso, 1.214 kcal al día de media en los últimos 7 días frente a un objetivo de 1.411, comidas registradas 7 de 7 días, y la meta de peso, 3,1 de 7,4 kg",
                 "Real app screen: My progress, 1,214 kcal a day on average over the last 7 days against a 1,411 target, meals logged 7 of 7 days, and the weight goal, 3.1 of 7.4 kg",
                 "En la app, la media de calorías de la semana y el avance hacia tu meta de peso.",
                 "In the app, the week's average calories and your progress towards your weight goal."),
    "macros": ("app-macros", (700, 1080), 700, 1034,
               "Pantalla real de la app: la tarjeta Nutrición Avanzada en la pantalla de inicio, con proteína, carbohidratos y grasas en anillos frente al objetivo del día",
               "Real app screen: the Advanced Nutrition card on the home screen, protein, carbs and fat as rings against the day's targets",
               "En la app, la proteína, los hidratos y las grasas del día frente a tu objetivo.",
               "In the app, the day's protein, carbs and fat against your target."),
    "portion": ("app-portion", (440, 660), 440, 629,
                "Pantalla real de la app: la hoja de porción personalizada sobre la foto del plato, multiplicador de ×0,5 a ×3, 450 g, 600 kcal y los macros que lo siguen, y el número de personas",
                "Real app screen: the custom portion sheet over the plate photo, multiplier from ×0.5 to ×3, 450 g, 600 kcal and the macros following it, and the number of people",
                "En la app, la ración se corrige antes de guardar: los gramos y las calorías cambian a la vez.",
                "In the app, you correct the portion before saving: grams and calories change together."),
    "detail": ("app-detail", (440, 660), 440, 790,
               "Pantalla real de la app: el detalle de un tazón de pollo, «¿Qué lleva que no ves?»: azúcar, grasa saturada, sal, fibra y colesterol, y después vitaminas y minerales como porcentaje de la referencia diaria",
               "Real app screen: the detail of a chicken bowl, 'What is in it that you cannot see?': sugar, saturated fat, salt, fibre and cholesterol, then vitamins and minerals as a share of the daily reference",
               "En la app, el detalle de cada comida: fibra, azúcar, grasa saturada y sal, además de las calorías.",
               "In the app, the detail of each meal: fibre, sugar, saturated fat and salt, as well as the calories."),
}


def shot(key, lang):
    stem, (w1, w2), w, h, alt_es, alt_en, cap_es, cap_en = SHOTS[key]
    alt, cap = (alt_es, cap_es) if lang == "es" else (alt_en, cap_en)
    p = "/assets/img/screens/%s-%%d-%s.%%s" % (stem, lang)
    return ('      <figure class="app-shot reveal"><picture><source type="image/avif" srcset="%s %dw, %s %dw" sizes="220px">'
            '<img src="%s" srcset="%s %dw, %s %dw" sizes="220px" width="%d" height="%d" loading="lazy" decoding="async" alt="%s"></picture>'
            '<figcaption>%s</figcaption></figure>') % (
        p % (w1, "avif"), w1, p % (w2, "avif"), w2, p % (w1, "webp"), p % (w1, "webp"), w1, p % (w2, "webp"), w2, w, h, alt.replace('"', "&quot;"), cap)
