#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the eight calculators and their hub, in Spanish and English.

    python3 tools/gen_calcs.py           # writes src/calculadoras/**/index.html
    python3 tools/build_site.py          # renders /calculadoras/ and /en/calculadoras/

The arithmetic lives in assets/js/calc.js and runs in the visitor's browser:
no account, nothing sent. It is the app's arithmetic (plan.ts, water.ts),
checked against the app's code.

The copy is in tools/calcs/content.py. Each source page holds both
languages as data-lang-block="es|en" blocks; tools/build_site.py keeps one per
tree.

Lang-ux round (2026-11): the owner, as a first-time visitor, did not see
that the hub cards open tools and found the pages text-heavy. So: the tool
is a card right under the H1 with EMPTY inputs (an example in the
placeholder), a big "Calcular" button, a short message under any wrong
field, plain-word labels (the technical names stay in the explanation), the
result card with the app download card inside it, and the long text below
the tool. The hub opens with a quick BMI tool and cards that say "Usar
calculadora"."""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_dishes import ld_block, ORG, esc, TITLE_MAX, SITE, ROOT, PLAY, download_card  # noqa: E402
from calcs.content import CALCS, SOURCES  # noqa: E402

SRC = os.path.join(ROOT, "src", "calculadoras")
PUB = "2026-10-13"
MOD = "2026-11-08"
DESC_MAX = 155
LANGS = ("es", "en")

# ── words that are not page copy ─────────────────────────────────────
UI = {
    "es": {
        "home": "Inicio", "calcs": "Calculadoras", "crumbs": "Migas de pan", "result": "Tu resultado",
        "empty": "Rellena tus datos y pulsa <b>Calcular</b>. El resultado aparecerá aquí.",
        "share": "Copiar enlace con estos datos", "copied": "Enlace copiado",
        "faq": "Preguntas frecuentes", "sources": "Fuentes", "related": "Más calculadoras y tablas", "calc": "Calculadora",
        "table": "Tabla", "table_t": "Calorías de los platos españoles, por ración y por 100 g", "blog": "Del blog",
        "disclaimer": "Orientativo, no sustituye a un profesional sanitario. No vale para menores de 18 años, embarazo o lactancia, ni si has tenido un trastorno de la conducta alimentaria.",
        "sticky": "Fotocal cuenta tus calorías con una foto", "sticky_btn": "Descargar",
        "go": "Calcular", "how": "¿Cómo se calcula?", "eg": "ej.", "pick": "Elige una opción",
        "sex": "Sexo", "f": "Mujer", "m": "Hombre", "age": "Edad", "height": "Altura", "weight": "Peso",
        "weight_opt": "Tu peso (opcional)", "activity": "¿Cómo es tu día a día?", "goal": "Tu objetivo",
        "pace": "¿A qué ritmo?", "target": "Peso que quieres alcanzar", "bf": "% de grasa corporal (opcional)", "split": "Tipo de dieta",
        "kcal": "Tus propias calorías (opcional)",
        "units": {"age": "años", "height": "cm", "weight": "kg", "target": "kg", "bf": "%", "kcal": "kcal"},
        "ph": {"age": "35", "height": "170", "weight": "70", "target": "65", "bf": "25", "kcal": "2000"},
        "err": {"sex": "Elige mujer u hombre.", "age": "Introduce una edad entre 18 y 90 años.", "height": "Introduce una altura entre 130 y 230 cm.",
                "weight": "Introduce un peso entre 35 y 250 kg.", "target": "Introduce un peso objetivo entre 35 y 250 kg.",
                "activity": "Elige cómo es tu día a día.", "bf": "Introduce un porcentaje entre 3 y 60, o déjalo vacío.",
                "kcal": "Introduce entre 1.000 y 6.000 kcal, o déjalo vacío."},
        "goals": [("lose", "Perder peso"), ("maintain", "Mantener mi peso"), ("gain", "Ganar peso"), ("build_muscle", "Ganar músculo")],
        "paces": [("0.25", "Suave: 0,25 kg por semana"), ("0.5", "Recomendado: 0,5 kg por semana"), ("0.75", "Rápido: 0,75 kg por semana")],
        "splits": [("balanced", "Equilibrada"), ("high_protein", "Alta en proteína"), ("low_carb", "Baja en hidratos"), ("keto", "Cetogénica")],
        "hint_kcal": "Vacío = las calculadas", "hint_bf": "Si lo sabes",
        "acts": [("sedentary", "Sedentario: trabajo sentado, poco movimiento"), ("light", "Ligero: de pie a ratos, algún paseo"),
                 ("standing", "Moderado: casi todo el día de pie"), ("active", "Activo: en movimiento todo el día"),
                 ("hard", "Muy activo: trabajo físico duro")],
        "how_act": "Tu gasto diario es tu metabolismo basal (fórmula de Mifflin-St Jeor) multiplicado por tu actividad: ×1,2 sedentario, ×1,375 ligero, ×1,465 moderado, ×1,55 activo y ×1,725 muy activo. El ejercicio no se cuenta aquí: se suma aparte el día que lo haces. El detalle, debajo.",
        "how_plain": "El detalle de la fórmula y un ejemplo resuelto están debajo de la calculadora.",
        "use": "Usar calculadora",
    },
    "en": {
        "home": "Home", "calcs": "Calculators", "crumbs": "Breadcrumb", "result": "Your result",
        "empty": "Fill in your details and tap <b>Calculate</b>. Your result appears here.",
        "share": "Copy a link with these numbers", "copied": "Link copied",
        "faq": "Frequently asked questions", "sources": "Sources", "related": "More calculators and tables", "calc": "Calculator",
        "table": "Table", "table_t": "Calories in Spanish dishes, per serving and per 100 g", "blog": "From the blog",
        "disclaimer": "For guidance only; not a substitute for a health professional. Not for under-18s, pregnancy or breastfeeding, or if you have had an eating disorder.",
        "sticky": "Fotocal counts your calories from a photo", "sticky_btn": "Download",
        "go": "Calculate", "how": "How is it worked out?", "eg": "e.g.", "pick": "Choose one",
        "sex": "Sex", "f": "Woman", "m": "Man", "age": "Age", "height": "Height", "weight": "Weight",
        "weight_opt": "Your weight (optional)", "activity": "What is your day like?", "goal": "Your goal",
        "pace": "How fast?", "target": "Weight you want to reach", "bf": "Body fat % (optional)", "split": "Type of diet",
        "kcal": "Your own calories (optional)",
        "units": {"age": "years", "height": "cm", "weight": "kg", "target": "kg", "bf": "%", "kcal": "kcal"},
        "ph": {"age": "35", "height": "170", "weight": "70", "target": "65", "bf": "25", "kcal": "2000"},
        "err": {"sex": "Choose woman or man.", "age": "Enter an age between 18 and 90.", "height": "Enter a height between 130 and 230 cm.",
                "weight": "Enter a weight between 35 and 250 kg.", "target": "Enter a target weight between 35 and 250 kg.",
                "activity": "Choose what your day is like.", "bf": "Enter a percentage between 3 and 60, or leave it empty.",
                "kcal": "Enter between 1,000 and 6,000 kcal, or leave it empty."},
        "goals": [("lose", "Lose weight"), ("maintain", "Keep my weight"), ("gain", "Gain weight"), ("build_muscle", "Build muscle")],
        "paces": [("0.25", "Gentle: 0.25 kg a week"), ("0.5", "Recommended: 0.5 kg a week"), ("0.75", "Fast: 0.75 kg a week")],
        "splits": [("balanced", "Balanced"), ("high_protein", "High protein"), ("low_carb", "Low carb"), ("keto", "Keto")],
        "hint_kcal": "Empty = the calculated ones", "hint_bf": "If you know it",
        "acts": [("sedentary", "Sedentary: desk job, little movement"), ("light", "Light: on your feet sometimes, some walking"),
                 ("standing", "Moderate: on your feet most of the day"), ("active", "Active: moving all day"),
                 ("hard", "Very active: hard physical work")],
        "how_act": "Your daily burn is your basal metabolism (Mifflin-St Jeor equation) times your activity: ×1.2 sedentary, ×1.375 light, ×1.465 moderate, ×1.55 active and ×1.725 very active. Workouts are not counted here: add them on the days you do them. The details are below.",
        "how_plain": "The formula and a worked example are below the calculator.",
        "use": "Use the calculator",
    },
}

# ── the result card of each calculator: main line, rows, warnings ─────
# rows: (key, label, unit, highlighted); a row may carry a warn key, shown
# only when that warning is on (the BMR "with your body fat" row)
OUT = {
 "tdee": {
  "es": {"main": "kcal al día para mantener tu peso", "rows": [
          ("bmr", "En reposo (metabolismo basal)", "kcal", False),
          ("lose25", "Para perder 0,25 kg por semana", "kcal", False),
          ("lose50", "Para perder 0,5 kg por semana", "kcal", True),
          ("gain25", "Para ganar 0,25 kg por semana", "kcal", False)],
         "warn": {"floor": 'Para perder medio kilo bajarías de <b data-out="floor">1.200</b> kcal al día, el mínimo que usamos, así que la cifra se queda ahí, igual que en la app. Elige un ritmo más suave. Para bajar de ese mínimo, hazlo con un profesional sanitario.'}},
  "en": {"main": "kcal a day to keep your weight", "rows": [
          ("bmr", "At rest (basal metabolism)", "kcal", False),
          ("lose25", "To lose 0.25 kg a week", "kcal", False),
          ("lose50", "To lose 0.5 kg a week", "kcal", True),
          ("gain25", "To gain 0.25 kg a week", "kcal", False)],
         "warn": {"floor": 'Losing half a kilo would take you below <b data-out="floor">1,200</b> kcal a day, the minimum we use, so the number stays there, as in the app. Pick a gentler pace. To go lower, do it with a health professional.'}}},
 "deficit": {
  "es": {"main": "kcal al día para perder peso", "rows": [
          ("tdee", "Lo que gastas al día", "kcal", False),
          ("deficit", "Lo que recortas al día", "kcal", False),
          ("kgweek", "Lo que perderías por semana", "kg", True),
          ("pct", "De tu peso cada semana", "%", False),
          ("weeks", "Semanas hasta tu objetivo", "", False),
          ("months", "Meses, más o menos", "", False)],
         "warn": {"floor": 'Tu objetivo quedaría por debajo de <b data-out="floor">1.200</b> kcal al día, el mínimo que usamos, así que se queda ahí, igual que en la app. Elige un ritmo más suave. No bajes de ese mínimo sin un médico o dietista.',
                  "fast": "Perderías más del 1 % de tu peso por semana. Es más rápido de lo que recomiendan las guías para no perder músculo. Elige un ritmo más suave.",
                  "capped": "Ese ritmo pedía recortar más de la cuarta parte de lo que gastas. El recorte se queda en esa cuarta parte, como en la app, y perderás algo más despacio.",
                  "lowbmi": 'Ese peso objetivo es bajo para tu altura. El rango saludable empieza en <b data-out="hmin">50</b> kg. Coméntalo con un profesional sanitario.',
                  "notlose": "Pon un peso objetivo menor que tu peso actual para calcular el déficit."}},
  "en": {"main": "kcal a day to lose weight", "rows": [
          ("tdee", "What you burn a day", "kcal", False),
          ("deficit", "What you cut a day", "kcal", False),
          ("kgweek", "What you would lose a week", "kg", True),
          ("pct", "Of your weight each week", "%", False),
          ("weeks", "Weeks to your goal", "", False),
          ("months", "Months, roughly", "", False)],
         "warn": {"floor": 'Your target would fall below <b data-out="floor">1,200</b> kcal a day, the minimum we use, so it stays there, as in the app. Pick a gentler pace. Do not go below that minimum without a doctor or dietitian.',
                  "fast": "You would lose more than 1% of your weight a week. That is faster than guidelines advise to keep muscle. Pick a gentler pace.",
                  "capped": "That pace needed a cut of more than a quarter of what you burn. The cut stays at that quarter, as in the app, so you will lose a bit more slowly.",
                  "lowbmi": 'That target weight is low for your height. The healthy range starts at <b data-out="hmin">50</b> kg. Talk it over with a health professional.',
                  "notlose": "Enter a target weight below your current weight to work out a deficit."}}},
 "bmi": {
  "es": {"main": "de IMC", "cats": ["Bajo peso", "Peso normal", "Sobrepeso", "Obesidad grado I", "Obesidad grado II", "Obesidad grado III"],
         "rows": [("range", "Peso saludable para tu altura", "kg", True)], "warn": {}},
  "en": {"main": "BMI", "cats": ["Underweight", "Normal weight", "Overweight", "Obesity class I", "Obesity class II", "Obesity class III"],
         "rows": [("range", "Healthy weight for your height", "kg", True)], "warn": {}}},
 "protein": {
  "es": {"main": "g de proteína al día", "rows": [
          ("meal3", "En cada comida, si haces tres", "g", True),
          ("meal4", "En cada comida, si haces cuatro", "g", False),
          ("prange", "Rango para gente activa", "g", False),
          ("efsa", "Mínimo diario recomendado", "g", False),
          ("gkg", "Gramos por kilo", "g/kg", False),
          ("ref", "Peso usado para la cuenta", "kg", False)],
         "warn": {"ref": "Como tu IMC pasa de 25, la cuenta usa el peso que tendrías con un IMC de 25. La proteína que necesitas depende del músculo, no de la grasa. Así lo hace también la app."}},
  "en": {"main": "g of protein a day", "rows": [
          ("meal3", "At each meal, over three meals", "g", True),
          ("meal4", "At each meal, over four meals", "g", False),
          ("prange", "Range for active people", "g", False),
          ("efsa", "Recommended daily minimum", "g", False),
          ("gkg", "Grams per kilo", "g/kg", False),
          ("ref", "Weight used for the sum", "kg", False)],
         "warn": {"ref": "Your BMI is above 25, so the sum uses the weight you would have at a BMI of 25. The protein you need follows muscle, not fat. The app does the same."}}},
 "macros": {
  "es": {"main": "kcal al día", "macros": [("p", "Proteínas"), ("c", "Hidratos"), ("f", "Grasas")],
         "rows": [("tdee", "Lo que gastas al día", "kcal", False)],
         "warn": {"floor": 'Tus calorías quedarían por debajo de <b data-out="floor">1.200</b> kcal, el mínimo que usamos, así que se quedan ahí, igual que en la app. No bajes de ese mínimo sin un profesional sanitario.',
                  "dropped": "Con estas calorías, la proteína deja poco sitio. La grasa baja al mínimo, el 20 %, igual que en la app."}},
  "en": {"main": "kcal a day", "macros": [("p", "Protein"), ("c", "Carbs"), ("f", "Fat")],
         "rows": [("tdee", "What you burn a day", "kcal", False)],
         "warn": {"floor": 'Your calories would fall below <b data-out="floor">1,200</b> kcal, the minimum we use, so they stay there, as in the app. Do not go below that minimum without a health professional.',
                  "dropped": "At these calories, protein leaves little room. Fat drops to its minimum, 20%, as in the app."}}},
 "water": {
  "es": {"main": "litros de bebida al día", "rows": [
          ("glasses", "Vasos de 250 ml", "", True),
          ("ml", "En mililitros", "ml", False),
          ("kcal", "Según tus calorías del día", "kcal", False)],
         "warn": {"floor": 'Tu cálculo sale por debajo del mínimo recomendado para ti, así que el objetivo se queda en <b data-out="wfloor">1.600</b> ml.',
                  "cap": "Tu cálculo pasa de 4 litros, así que el objetivo se queda en 4 litros, el máximo de la app."}},
  "en": {"main": "litres of drinks a day", "rows": [
          ("glasses", "250 ml glasses", "", True),
          ("ml", "In millilitres", "ml", False),
          ("kcal", "Based on your daily calories", "kcal", False)],
         "warn": {"floor": 'Your figure is below the recommended minimum for you, so the target stays at <b data-out="wfloor">1,600</b> ml.',
                  "cap": "Your figure is above 4 litres, so the target stays at 4 litres, the app's maximum."}}},
 "bmr": {
  "es": {"main": "kcal al día en reposo", "rows": [
          ("mifflin", "Según tu edad, altura y peso", "kcal", False),
          ("katch", "Con tu % de grasa corporal", "kcal", False, "katch")],
         "acts_h": "Con tu actividad, gastas al día:", "warn": {}},
  "en": {"main": "kcal a day at rest", "rows": [
          ("mifflin", "From your age, height and weight", "kcal", False),
          ("katch", "With your body fat %", "kcal", False, "katch")],
         "acts_h": "With your activity, you burn a day:", "warn": {}}},
 "healthy": {
  "es": {"main": "kg, tu rango de peso saludable", "rows": [
          ("bmi", "Tu IMC", "", False, "inside over under"),
          ("mid", "Peso en el centro del rango", "kg", False)],
         "warn": {"inside": "Estás dentro del rango saludable para tu altura.",
                  "over": 'Estás <span data-warn="gap-kg">unos <b data-out="gap">3</b> kg</span><span data-warn="gap-small">menos de 1 kg</span> por encima del rango.',
                  "under": 'Estás <span data-warn="gap-kg">unos <b data-out="gap">3</b> kg</span><span data-warn="gap-small">menos de 1 kg</span> por debajo del rango. Si no es tu constitución de siempre, habla con un profesional sanitario.'}},
  "en": {"main": "kg, your healthy weight range", "rows": [
          ("bmi", "Your BMI", "", False, "inside over under"),
          ("mid", "Weight in the middle of the range", "kg", False)],
         "warn": {"inside": "You are inside the healthy range for your height.",
                  "over": 'You are <span data-warn="gap-kg">about <b data-out="gap">3</b> kg</span><span data-warn="gap-small">less than 1 kg</span> above the range.',
                  "under": 'You are <span data-warn="gap-kg">about <b data-out="gap">3</b> kg</span><span data-warn="gap-small">less than 1 kg</span> below the range. If that is not how you have always been, talk to a health professional.'}}},
}

BRIDGE_SUB = {
    "es": {"kcal": "Haz una foto y Fotocal cuenta las calorías por ti.", "protein": "Haz una foto y Fotocal cuenta la proteína de cada plato por ti.",
           "water": "Fotocal lleva el agua del día junto a tus comidas: un toque por vaso.", "other": "Haz una foto de cada plato y Fotocal cuenta las calorías por ti."},
    "en": {"kcal": "Snap a photo and Fotocal counts the calories for you.", "protein": "Snap a photo and Fotocal counts the protein in each dish for you.",
           "water": "Fotocal tracks your water next to your meals: one tap per glass.", "other": "Snap a photo of each dish and Fotocal counts the calories for you."},
}
BRIDGE_KIND = {"tdee": "kcal", "deficit": "kcal", "macros": "kcal", "protein": "protein", "water": "water", "bmi": "other", "bmr": "other", "healthy": "other"}
# the fields that only matter for some goals: shown when the goal is one of these
GOAL_ONLY = {("macros", "pace"): "lose gain"}

ICONS = {
    "flame": '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.5 1.5-4 2.5-5 .3 1.6 1.2 2.6 2.5 3-1-3 0-6.5 0-8z"/>',
    "trend": '<path d="M3 7l6 6 4-4 8 8"/><path d="M15 17h6v-6"/>',
    "scale": '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M8 9a4 4 0 0 1 8 0"/><path d="M12 9l1.5-2"/>',
    "egg": '<path d="M12 3c3.5 0 6.5 5.5 6.5 10a6.5 6.5 0 0 1-13 0C5.5 8.5 8.5 3 12 3z"/>',
    "pie": '<path d="M12 3v9h9"/><path d="M20.5 15.5A9 9 0 1 1 8.5 3.7"/>',
    "drop": '<path d="M12 3s6.5 7 6.5 11.5a6.5 6.5 0 0 1-13 0C5.5 10 12 3 12 3z"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/><path d="M5 12h4l1.5-2.5L13 15l1.5-3H19"/>',
    "ruler": '<path d="M4 16L16 4l4 4L8 20z"/><path d="M8 12l2 2M11 9l2 2M14 6l2 2"/>',
}


def icon(name):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICONS[name]


def strip(s):
    return re.sub(r"<[^>]+>", "", s)


def play(campaign):
    return PLAY + "&utm_source=web&utm_medium=tool&utm_campaign=" + campaign


def needs():
    js = "const C=require(process.argv[1]);process.stdout.write(JSON.stringify({n:C.NEEDS,k:C.KIND_DEFAULTS}));"
    out = subprocess.run(["node", "-e", js, os.path.join(ROOT, "assets", "js", "calc.js")], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


NEEDS = None


# ── the form ─────────────────────────────────────────────────────────
def form(kind, lang, slug, mini=False):
    u = UI[lang]
    pid = (slug[:3] + ("-mini" if mini else ""))
    out_id = "out-%s%s" % (lang, "-mini" if mini else "")
    goal_default = NEEDS["k"].get(kind, {}).get("goal", "lose")
    o = ['      <form class="calc%s" data-calc="%s" data-out="%s"%s novalidate aria-label="%s">' % (" calc-mini" if mini else "", kind, out_id, " data-mini" if mini else "", esc(u["calc"])),
         '        <div class="calc-grid">']
    for k in NEEDS["n"][kind]:
        fid = "%s-%s-%s" % (pid, k, lang)
        err = '<p class="calc-err" id="%s-err" data-err-for="%s" hidden>%s</p>' % (fid, k, u["err"].get(k, "")) if k in u["err"] else ""
        desc = ' aria-describedby="%s-err"' % fid if err else ""
        if k == "sex":
            o.append('          <fieldset class="calc-field wide"%s><legend>%s</legend><div class="calc-seg">' % (desc, u["sex"]))
            for v in ("f", "m"):
                o.append('            <input type="radio" name="sex" id="%s-%s" value="%s"><label for="%s-%s">%s</label>' % (fid, v, v, fid, v, u[v]))
            o.append('          </div>%s</fieldset>' % err)
        elif k in ("activity", "goal", "pace", "split"):
            only = GOAL_ONLY.get((kind, k))
            if k == "activity":
                opts, cur = u["acts"], ""
            else:
                opts = {"goal": u["goals"], "pace": u["paces"], "split": u["splits"]}[k]
                cur = {"goal": goal_default, "pace": "0.5", "split": "balanced"}[k]
            wide = " wide" if k in ("activity", "pace", "goal") else ""
            o.append('          <div class="calc-field%s"%s><label for="%s">%s</label><select id="%s" name="%s"%s>' % (wide, (' data-goals="%s"' % only) if only else "", fid, esc(u[k]), fid, k, desc))
            if k == "activity":
                o.append('            <option value="" selected disabled>%s</option>' % u["pick"])
            for v, lab in opts:
                o.append('            <option value="%s"%s>%s</option>' % (v, " selected" if v == cur else "", esc(lab)))
            o.append('          </select>%s</div>' % err)
        else:
            label = u["weight_opt"] if (k == "weight" and kind == "healthy") else u[k]
            if "(" not in label:
                label = "%s (%s)" % (label, u["units"][k])
            ph = {"kcal": u["hint_kcal"], "bf": u["hint_bf"]}.get(k) or "%s %s" % (u["eg"], u["ph"][k])
            # age, height and weight share one row when all three are asked,
            # so the button and the result stay near the first screen
            third = " third" if (k in ("age", "height", "weight") and "age" in NEEDS["n"][kind]) else ""
            o.append('          <div class="calc-field%s"><label for="%s">%s</label><input id="%s" name="%s" type="text" inputmode="decimal" autocomplete="off" placeholder="%s"%s%s>%s</div>'
                     % (third, fid, esc(label), fid, k, esc(ph), desc, ' data-dec=","' if lang == "es" else "", err))
    o.append('        </div>')
    o.append('        <button class="btn btn-cta calc-go" type="submit">%s</button>' % u["go"])
    if not mini:
        o.append('        <details class="calc-how"><summary>%s</summary><p>%s</p></details>' % (u["how"], u["how_act"] if "activity" in NEEDS["n"][kind] else u["how_plain"]))
    o.append('      </form>')
    return "\n".join(o)


def result(c, lang, mini=False):
    kind, u, spec = c["kind"], UI[lang], OUT[c["kind"]][lang]
    out_id = "out-%s%s" % (lang, "-mini" if mini else "")
    o = ['      <section class="calc-out" id="%s" data-state="empty" tabindex="-1" aria-labelledby="%s-h">' % (out_id, out_id),
         '        <h2 class="calc-out-h" id="%s-h">%s</h2>' % (out_id, u["result"]),
         '        <p class="calc-empty">%s</p>' % u["empty"],
         '        <div class="calc-res">',
         '        <p class="calc-main" aria-live="polite"><b data-out="main">—</b> <span>%s</span></p>' % spec["main"]]
    if kind == "bmi":
        o.append('        <p class="calc-cat">%s</p>' % "".join('<span data-cat="%d" hidden>%s</span>' % (i, esc(t)) for i, t in enumerate(spec["cats"])))
    if kind == "macros":
        o.append('        <div class="calc-macros">')
        for k, lab in spec["macros"]:
            o.append('          <div class="calc-macro m-%s"><b><span data-out="%s">—</span> g</b><span>%s · <span data-out="%sk">—</span> kcal · <span data-out="%sp">—</span> %%</span></div>' % (k, k, lab, k, k))
        o.append('        </div>')
        o.append('        <div class="dp-bar" aria-hidden="true">%s</div>' % "".join('<span class="%s" data-bar="%s" style="width:33.3%%"></span>' % (k, k) for k in ("p", "c", "f")))
    if not mini:
        o.append('        <div class="calc-rows">')
        for row in spec["rows"]:
            key, lab, unit, hl = row[:4]
            only = row[4] if len(row) > 4 else None
            if key in ("range", "prange"):
                val = '<span data-out="lo">—</span>–<span data-out="hi">—</span>'
            else:
                val = '<span data-out="%s">—</span>' % key
            attr = (' data-warn="%s" hidden' % only) if only and " " not in only else ""
            o.append('          <div class="calc-row%s"%s><span>%s</span><b>%s%s</b></div>' % (" is-hl" if hl else "", attr, esc(lab), val, (" " + unit) if unit else ""))
        if kind == "bmr":
            o.append('          <p class="calc-rows-h">%s</p>' % spec["acts_h"])
            for (a, lab) in u["acts"]:
                o.append('          <div class="calc-row%s"><span>%s</span><b><span data-out="t_%s">—</span> kcal</b></div>' % (" is-hl" if a == "light" else "", esc(lab.split(":")[0]), a))
        o.append('        </div>')
        for wk, html in spec["warn"].items():
            o.append('        <p class="calc-warn" data-warn="%s" hidden>%s</p>' % (wk, html))
        o.append('        <button class="calc-share" type="button" data-calc-share><span class="calc-share-a">%s</span><span class="calc-share-b">%s</span></button>' % (u["share"], u["copied"]))
        head = esc(c[lang]["bridge"]).replace("{X}", '<b data-out="bridge">—</b>')
        o.append(download_card(lang, head, BRIDGE_SUB[lang][BRIDGE_KIND[kind]], play(c["slug"]), "dl-in-result"))
    else:
        o.append('        <div class="calc-rows"><div class="calc-row is-hl"><span>%s</span><b><span data-out="lo">—</span>–<span data-out="hi">—</span> kg</b></div></div>' % esc(spec["rows"][0][1]))
        o.append('        <p class="calc-mini-more"><a href="%s/">%s →</a></p>' % (c["slug"], "Más detalle en la calculadora de IMC" if lang == "es" else "More detail in the BMI calculator"))
    o.append('        </div>')
    o.append('      </section>')
    return "\n".join(o)


def jsonld(c, lang, desc):
    L = c[lang]
    url = SITE + "calculadoras/%s/" % c["slug"]
    u = UI[lang]
    crumbs = [(u["home"], SITE), (u["calcs"], SITE + "calculadoras/"), (L["h1"], url)]
    return "\n".join([
        ld_block({"@context": "https://schema.org", "@type": "WebApplication", "name": L["h1"], "url": url, "description": desc,
                  "applicationCategory": "HealthApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
                  "isAccessibleForFree": True, "inLanguage": lang, "datePublished": PUB, "dateModified": MOD,
                  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "publisher": ORG}),
        ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": x[0], "item": x[1]} for i, x in enumerate(crumbs)]}),
        ld_block({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in L["faq"]]}),
    ])


def head(depth, meta, path):
    up = "../" * depth
    url = SITE + path
    es = meta["es"]
    return """<!DOCTYPE html>
<!-- GENERATED by tools/gen_calcs.py from tools/calcs/content.py — do not edit here. -->
<html lang="es" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!--# meta %s -->
  <title>%s</title>
  <meta name="description" content="%s">
  <link rel="canonical" href="%s">
  <link rel="alternate" hreflang="es" href="%s">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Fotocal">
  <meta property="og:title" content="%s">
  <meta property="og:description" content="%s">
  <meta property="og:url" content="%s">
  <meta property="og:image" content="https://getfotocal.com/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%s">
  <meta name="twitter:description" content="%s">
  <meta name="twitter:image" content="https://getfotocal.com/assets/og-image.png">
  <meta name="theme-color" media="(prefers-color-scheme: light)" content="#FFFFFF">
  <meta name="theme-color" media="(prefers-color-scheme: dark)" content="#121212">
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
<body class="page-fx page-post page-calc">
<div id="site-nav"></div>
""" % (json.dumps(meta, ensure_ascii=False), esc(es["title"]), esc(es["desc"]), url, url, esc(es["title"]), esc(es["desc"]), url,
       esc(es["title"]), esc(es["desc"]), up, up, up, up, up, up, up, up, up, up, up, up)


def foot(depth):
    up = "../" * depth
    return """
<div id="site-footer"></div>
<script src="%sassets/js/i18n.js"></script>
<script src="%sassets/js/layout.js" data-page="calculadoras"></script>
<script src="%sassets/js/main.js"></script>
<script src="%sassets/js/calc.js"></script>
</body>
</html>
""" % (up, up, up, up)


def titled(t):
    return t + " — Fotocal" if len(t) + len(" — Fotocal") <= TITLE_MAX else t


def check_meta(slug, lang, title, desc):
    assert len(title) <= TITLE_MAX, (slug, lang, len(title), title)
    assert 110 <= len(desc) <= DESC_MAX, (slug, lang, len(desc), desc)


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def blog_title(slug, lang):
    p = os.path.join(ROOT, "tools", "blog", "posts", slug + ".json")
    if not os.path.isfile(p):
        sys.exit("calculator links to an unknown blog post: %s" % slug)
    j = json.load(open(p, encoding="utf-8"))
    return (j.get(lang) or j["es"])["title"]


def page_lang(c, lang):
    L, u = c[lang], UI[lang]
    title, desc = titled(L["title"]), L["desc"]
    check_meta(c["slug"], lang, title, desc)
    o = ['  <div class="calc-lang" data-lang-block="%s">' % lang]
    o.append('    <header class="calc-head container">')
    o.append('      <nav class="post-crumbs" aria-label="%s"><a href="../../">%s</a><span class="sep" aria-hidden="true">/</span><a href="../">%s</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">%s</a></nav>'
             % (u["crumbs"], u["home"], u["calcs"], esc(L["short"])))
    o.append('      <h1 class="calc-title">%s</h1>' % esc(L["h1"]))
    o.append('      <p class="calc-lead">%s</p>' % esc(L["lead"]))
    o.append('    </header>')
    o.append('    <div class="container calc-page">')
    o.append('     <div class="calc-tool">')
    o.append(form(c["kind"], lang, c["slug"]))
    o.append(result(c, lang))
    o.append('     </div>')
    o.append('     <p class="calc-disclaimer">%s</p>' % u["disclaimer"])
    o.append('     <div class="calc-text post-body">')
    o.append(L["body"])
    o.append('      <h2 id="faq">%s</h2>\n      <div class="faq-list">' % u["faq"])
    for q, a in L["faq"]:
        o.append('        <details class="faq-item"><summary><span>%s</span><i class="faq-plus" aria-hidden="true"></i></summary><p>%s</p></details>' % (esc(q), a))
    o.append('      </div>')
    o.append('      <section class="dp-src" id="%s"><h2>%s</h2><ul>%s</ul></section>' % ("fuentes" if lang == "es" else "sources", u["sources"], "".join("<li>%s</li>" % SOURCES[s][lang] for s in c["sources"])))
    o.append('      <nav class="dp-related" aria-label="%s">\n        <h2>%s</h2>\n        <div class="post-nav">' % (u["related"], u["related"]))
    for x in CALCS:
        if x["slug"] != c["slug"]:
            o.append('          <a class="post-nav-item" href="../%s/"><small>%s</small><strong>%s</strong></a>' % (x["slug"], u["calc"], esc(x[lang]["h1"])))
    o.append('          <a class="post-nav-item" href="../../calorias/"><small>%s</small><strong>%s</strong></a>' % (u["table"], u["table_t"]))
    for b in c["blog"]:
        o.append('          <a class="post-nav-item" href="../../blog/%s/"><small>%s</small><strong>%s</strong></a>' % (b, u["blog"], esc(blog_title(b, lang))))
    o.append('        </div>\n      </nav>')
    o.append('     </div>')
    o.append('    </div>')
    o.append(jsonld(c, lang, desc))
    o.append('  </div>')
    body_words = words(L["body"]) + sum(words(q) + words(a) for q, a in L["faq"])
    return "\n".join(o), (title, desc), body_words


def sticky(slug):
    return "\n".join('<div class="calc-sticky" data-lang-block="%s"><img src="/assets/img/logo-64.png" width="36" height="36" alt="" decoding="async"><span>%s</span><a class="btn btn-cta" href="%s" target="_blank" rel="noopener">%s</a></div>'
                     % (l, UI[l]["sticky"], esc(play(slug + "-sticky")), UI[l]["sticky_btn"]) for l in LANGS)


def page(c):
    parts, meta, counts = [], {}, {}
    for lang in LANGS:
        html, (t, d), n = page_lang(c, lang)
        parts.append(html)
        meta[lang] = {"title": t, "desc": d}
        counts[lang] = n
    out = [head(2, meta, "calculadoras/%s/" % c["slug"])]
    out.append('\n<main id="main" class="calc-main-wrap">')
    out.extend(parts)
    out.append('</main>')
    out.append(sticky(c["slug"]))
    out.append(foot(2))
    return "\n".join(out), counts


HUB = {
    "es": {"title": "Calculadoras de calorías, IMC, macros y agua",
           "desc": "Ocho calculadoras sin registro: calorías diarias, déficit calórico, IMC, proteínas, macros, agua, TMB y peso saludable, con las mismas fórmulas que la app.",
           "h1": "Calcula en segundos, gratis y sin registro",
           "lead": "Ocho calculadoras de calorías, IMC, macros y más. Escribe tus datos y tendrás el resultado al momento. No se envía nada y dan los mismos números que la app Fotocal.",
           "quick": "Prueba ahora: tu IMC", "all": "Las ocho calculadoras",
           "body": """
      <h2>En qué orden usarlas</h2>
      <p>Empieza por las <a href="calorias-diarias/">calorías diarias</a>: es la base de todo lo demás. Si quieres perder grasa, sigue con el <a href="deficit-calorico/">déficit calórico</a>, que te dice cuánto recortar y cuánto tardarás. Las <a href="proteinas/">proteínas</a> y los <a href="macros/">macros</a> reparten esas calorías. El <a href="imc/">IMC</a> y el <a href="peso-saludable/">peso saludable</a> te dicen dónde estás. La <a href="tmb/">TMB</a> explica de dónde sale tu gasto, y la de <a href="agua/">agua</a>, cuánto beber.</p>
      <h2>De dónde salen estos números</h2>
      <p>De las mismas fórmulas que usa la app Fotocal: Mifflin-St Jeor (1990) para el metabolismo, los rangos de IMC de la OMS y las referencias de la EFSA para la proteína y el agua. Cada calculadora explica su fórmula con un ejemplo y cita sus fuentes. Para saber cuánto tiene lo que comes, está la <a href="../calorias/">tabla de calorías de platos españoles</a>.</p>""",
           "disclaimer": "Orientativo, no sustituye a un profesional sanitario."},
    "en": {"title": "Calorie, BMI, macro and water calculators",
           "desc": "Eight calculators, no sign-up: daily calories, calorie deficit, BMI, protein, macros, water, BMR and healthy weight, with the same formulas as the app.",
           "h1": "Work it out in seconds, free and with no sign-up",
           "lead": "Eight calculators for calories, BMI, macros and more. Type in your details and get the result straight away. Nothing is sent anywhere, and they give the same numbers as the Fotocal app.",
           "quick": "Try it now: your BMI", "all": "All eight calculators",
           "body": """
      <h2>Which order to use them in</h2>
      <p>Start with <a href="calorias-diarias/">daily calories</a>: it is the base for everything else. To lose fat, go on to the <a href="deficit-calorico/">calorie deficit</a>, which tells you how much to cut and how long it takes. <a href="proteinas/">Protein</a> and <a href="macros/">macros</a> split those calories. <a href="imc/">BMI</a> and <a href="peso-saludable/">healthy weight</a> show where you stand. <a href="tmb/">BMR</a> explains where your energy use comes from, and <a href="agua/">water</a> how much to drink.</p>
      <h2>Where these numbers come from</h2>
      <p>From the same formulas the Fotocal app uses: Mifflin-St Jeor (1990) for metabolism, the WHO BMI bands and EFSA references for protein and water. Each calculator explains its formula with a worked example and cites its sources. For what is in your food, see the <a href="../calorias/">table of calories in Spanish dishes</a>.</p>""",
           "disclaimer": "For guidance only; not a substitute for a health professional."},
}


def hub():
    meta, parts = {}, []
    bmi = next(c for c in CALCS if c["kind"] == "bmi")
    for lang in LANGS:
        H, u = HUB[lang], UI[lang]
        title = titled(H["title"])
        check_meta("hub", lang, title, H["desc"])
        meta[lang] = {"title": title, "desc": H["desc"]}
        url = SITE + "calculadoras/"
        o = ['  <div class="calc-lang" data-lang-block="%s">' % lang]
        o.append('    <header class="calc-head container">')
        o.append('      <nav class="post-crumbs" aria-label="%s"><a href="../">%s</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">%s</a></nav>' % (u["crumbs"], u["home"], u["calcs"]))
        o.append('      <h1 class="calc-title">%s</h1>' % esc(H["h1"]))
        o.append('      <p class="calc-lead">%s</p>' % esc(H["lead"]))
        o.append('    </header>')
        o.append('    <div class="container">')
        o.append('      <section class="calc-quick" aria-labelledby="quick-%s"><h2 class="calc-quick-h" id="quick-%s">%s</h2><div class="calc-quick-in">' % (lang, lang, H["quick"]))
        o.append(form("bmi", lang, "imc", mini=True))
        o.append(result(bmi, lang, mini=True))
        o.append('      </div></section>')
        o.append('      <h2 class="calc-cards-h">%s</h2>' % H["all"])
        o.append('      <ul class="calc-cards">')
        for c in CALCS:
            o.append('        <li><a class="calc-card" href="%s/"><span class="calc-card-ico">%s</span><strong>%s</strong><span class="calc-card-t">%s</span><span class="btn btn-cta calc-card-go">%s</span></a></li>'
                     % (c["slug"], icon(c["icon"]), esc(c[lang]["h1"]), esc(c[lang]["card"]), u["use"]))
        o.append('      </ul>')
        o.append(download_card(lang, "¿Quieres saber cuánto comes de verdad, sin pesar la comida?" if lang == "es" else "Want to know what you really eat, without weighing food?",
                               BRIDGE_SUB[lang]["other"], play("hub")))
        o.append('      <div class="post-body calc-hub-text">%s\n      <p class="calc-disclaimer">%s</p>\n      </div>' % (H["body"], H["disclaimer"]))
        o.append('    </div>')
        o.append(ld_block({"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": H["desc"], "inLanguage": lang, "url": url, "publisher": ORG,
                           "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c[lang]["h1"], "url": SITE + "calculadoras/%s/" % c["slug"]} for i, c in enumerate(CALCS)]}}))
        o.append(ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": SITE}, {"@type": "ListItem", "position": 2, "name": u["calcs"], "item": url}]}))
        o.append('  </div>')
        parts.append("\n".join(o))
    out = [head(1, meta, "calculadoras/"), '\n<main id="main" class="calc-main-wrap calc-hub">'] + parts + ["</main>", foot(1)]
    return "\n".join(out)


def main():
    global NEEDS
    NEEDS = needs()
    if os.path.isdir(SRC):
        for base, dirs, files in os.walk(SRC, topdown=False):
            for f in files:
                os.remove(os.path.join(base, f))
            for d in dirs:
                os.rmdir(os.path.join(base, d))
    for c in CALCS:
        p = os.path.join(SRC, c["slug"])
        os.makedirs(p, exist_ok=True)
        html, counts = page(c)
        open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(html)
        print("  /calculadoras/%-18s words es %d · en %d" % (c["slug"] + "/", counts["es"], counts["en"]))
    open(os.path.join(SRC, "index.html"), "w", encoding="utf-8").write(hub())
    print("%d calculators + hub -> src/calculadoras/ (es + en)" % len(CALCS))


if __name__ == "__main__":
    main()
