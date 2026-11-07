#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the eight calculators and their hub, in Spanish and English.

    python3 tools/gen_calcs.py           # writes src/calculadoras/**/index.html
    python3 tools/build_site.py          # renders /calculadoras/ and /en/calculadoras/

The arithmetic lives in assets/js/calc.js and runs in the visitor's browser:
no account, nothing sent. It is the app's arithmetic (plan.ts, water.ts),
checked against the app's code. This script runs the same file under Node to
pre-render each page's default result, so the first paint already shows the
right numbers and nothing moves when the script arrives.

The copy is in tools/calcs/content.py. Each source page holds both
languages as data-lang-block="es|en" blocks; tools/build_site.py keeps one per
tree. (Spanish-only until the tools-seo round, 2026-11; the old Spanish copy
is kept in tools/calcs/legacy-es.json.)"""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_dishes import ld_block, ORG, esc, TITLE_MAX, SITE, ROOT, PLAY  # noqa: E402
from calcs.content import CALCS, SOURCES, ACT_ROWS  # noqa: E402

SRC = os.path.join(ROOT, "src", "calculadoras")
PUB = "2026-10-13"
MOD = "2026-11-07"
DESC_MAX = 155
LANGS = ("es", "en")

# ── words that are not page copy ─────────────────────────────────────
UI = {
    "es": {
        "home": "Inicio", "calcs": "Calculadoras", "crumbs": "Migas de pan", "result": "Tu resultado",
        "share": "Copiar enlace con estos datos", "copied": "Enlace copiado",
        "faq": "Preguntas frecuentes", "sources": "Fuentes", "related": "Seguir por aquí", "calc": "Calculadora",
        "table": "Tabla", "table_t": "Calorías de los platos españoles, por ración y por 100 g", "blog": "Del blog",
        "disclaimer": "Orientativo, no sustituye a un profesional sanitario. No vale para menores de 18 años, embarazo o lactancia, ni si has tenido un trastorno de la conducta alimentaria.",
        "cta": "Descárgala gratis en Google Play",
        "free": "Plan gratis, sin tarjeta: 2 escaneos con IA al día, 1 registro por voz al día, código de barras y Coach Kal sin límite. Solo Android.",
        "sticky": "Fotocal: haz una foto y cuenta las calorías", "sticky_btn": "Descargar",
        "go": "Calcular",
        "sex": "Sexo", "f": "Mujer", "m": "Hombre", "age": "Edad (años)", "height": "Altura (cm)", "weight": "Peso (kg)",
        "weight_opt": "Tu peso (kg, opcional)", "activity": "Tu día a día (sin contar el ejercicio)", "goal": "Objetivo",
        "pace": "Ritmo", "target": "Peso objetivo (kg)", "bf": "Grasa corporal (%, opcional)", "split": "Reparto",
        "kcal": "Calorías propias (opcional)",
        "goals": [("lose", "Perder peso"), ("maintain", "Mantener mi peso"), ("gain", "Ganar peso"), ("build_muscle", "Ganar músculo")],
        "paces": [("0.25", "0,25 kg/semana · suave"), ("0.5", "0,5 kg/semana · recomendado"), ("0.75", "0,75 kg/semana · intenso")],
        "splits": [("balanced", "Equilibrado"), ("high_protein", "Alto en proteína"), ("low_carb", "Bajo en hidratos"), ("keto", "Cetogénico")],
        "hint_kcal": "Vacío = las calculadas", "hint_bf": "Vacío = Mifflin-St Jeor",
    },
    "en": {
        "home": "Home", "calcs": "Calculators", "crumbs": "Breadcrumb", "result": "Your result",
        "share": "Copy a link with these numbers", "copied": "Link copied",
        "faq": "Frequently asked questions", "sources": "Sources", "related": "Keep going", "calc": "Calculator",
        "table": "Table", "table_t": "Calories in Spanish dishes, per serving and per 100 g (in Spanish)", "blog": "From the blog",
        "disclaimer": "For guidance only; not a substitute for a health professional. Not for under-18s, pregnancy or breastfeeding, or if you have had an eating disorder.",
        "cta": "Get it free on Google Play",
        "free": "Free plan, no card: 2 AI scans a day, 1 voice log a day, unlimited barcode scanner and Coach Kal. Android only.",
        "sticky": "Fotocal: snap a photo, get the calories", "sticky_btn": "Download",
        "go": "Calculate",
        "sex": "Sex", "f": "Woman", "m": "Man", "age": "Age (years)", "height": "Height (cm)", "weight": "Weight (kg)",
        "weight_opt": "Your weight (kg, optional)", "activity": "Your day-to-day (not counting workouts)", "goal": "Goal",
        "pace": "Pace", "target": "Target weight (kg)", "bf": "Body fat (%, optional)", "split": "Split",
        "kcal": "Your own calories (optional)",
        "goals": [("lose", "Lose weight"), ("maintain", "Keep my weight"), ("gain", "Gain weight"), ("build_muscle", "Build muscle")],
        "paces": [("0.25", "0.25 kg/week · gentle"), ("0.5", "0.5 kg/week · recommended"), ("0.75", "0.75 kg/week · intense")],
        "splits": [("balanced", "Balanced"), ("high_protein", "High protein"), ("low_carb", "Low carb"), ("keto", "Keto")],
        "hint_kcal": "Empty = the calculated ones", "hint_bf": "Empty = Mifflin-St Jeor",
    },
}

# ── the result card of each calculator: main line, rows, warnings ─────
# rows: (key, label, unit, highlighted)
OUT = {
 "tdee": {
  "es": {"main": "kcal al día para mantener tu peso", "rows": [
          ("bmr", "Metabolismo basal (TMB)", "kcal", False),
          ("lose25", "Para perder 0,25 kg por semana", "kcal", False),
          ("lose50", "Para perder 0,5 kg por semana", "kcal", True),
          ("gain25", "Para ganar 0,25 kg por semana", "kcal", False)],
         "warn": {"floor": 'Para perder medio kilo bajarías del suelo de <b data-out="floor">1.200</b> kcal al día: la cifra se queda en ese suelo, como en la app. Elige un ritmo más suave y, si quieres bajar más, hazlo con un profesional sanitario.'}},
  "en": {"main": "kcal a day to keep your weight", "rows": [
          ("bmr", "Basal metabolic rate (BMR)", "kcal", False),
          ("lose25", "To lose 0.25 kg a week", "kcal", False),
          ("lose50", "To lose 0.5 kg a week", "kcal", True),
          ("gain25", "To gain 0.25 kg a week", "kcal", False)],
         "warn": {"floor": 'Losing half a kilo would take you below the floor of <b data-out="floor">1,200</b> kcal a day: the number stays at that floor, as in the app. Pick a gentler pace and, to go lower, do it with a health professional.'}}},
 "deficit": {
  "es": {"main": "kcal al día para perder peso", "rows": [
          ("tdee", "Tu mantenimiento", "kcal", False),
          ("deficit", "Déficit diario", "kcal", False),
          ("kgweek", "Pérdida estimada", "kg/semana", True),
          ("pct", "De tu peso cada semana", "%", False),
          ("weeks", "Semanas hasta tu objetivo", "", False),
          ("months", "Meses, aproximadamente", "", False)],
         "warn": {"floor": 'Tu objetivo quedaría por debajo de <b data-out="floor">1.200</b> kcal al día, el mínimo que usa la app: se queda en ese suelo. No bajes de ahí sin un médico o dietista; elige un ritmo más suave.',
                  "fast": "Vas a más del 1 % de tu peso por semana: es más de lo que recomiendan las guías para conservar músculo. Elige un ritmo más suave.",
                  "capped": "El ritmo que pides pasa del 25 % de tu gasto, así que el recorte se queda en ese 25 %, como en la app: perderás algo más despacio.",
                  "lowbmi": 'Tu peso objetivo daría un IMC por debajo de 18,5. Para tu altura, el rango saludable empieza en <b data-out="hmin">50</b> kg: consúltalo con un profesional sanitario.',
                  "notlose": "Pon un peso objetivo menor que tu peso actual para calcular un déficit."}},
  "en": {"main": "kcal a day to lose weight", "rows": [
          ("tdee", "Your maintenance", "kcal", False),
          ("deficit", "Daily deficit", "kcal", False),
          ("kgweek", "Estimated loss", "kg/week", True),
          ("pct", "Of your weight each week", "%", False),
          ("weeks", "Weeks to your goal", "", False),
          ("months", "Months, roughly", "", False)],
         "warn": {"floor": 'Your target would fall below <b data-out="floor">1,200</b> kcal a day, the minimum the app uses: it stays at that floor. Do not go lower without a doctor or dietitian; pick a gentler pace.',
                  "fast": "You are going faster than 1% of your weight a week: more than guidelines advise to keep muscle. Pick a gentler pace.",
                  "capped": "The pace you asked for is more than 25% of what you burn, so the cut stays at that 25%, as in the app: you will lose a bit more slowly.",
                  "lowbmi": 'Your target weight would give a BMI under 18.5. For your height the healthy range starts at <b data-out="hmin">50</b> kg: check it with a health professional.',
                  "notlose": "Enter a target weight below your current weight to work out a deficit."}}},
 "bmi": {
  "es": {"main": "de IMC", "cats": ["Bajo peso", "Peso normal", "Sobrepeso", "Obesidad grado I", "Obesidad grado II", "Obesidad grado III"],
         "rows": [("range", "Peso normal para tu altura", "kg", True)], "warn": {}},
  "en": {"main": "BMI", "cats": ["Underweight", "Normal weight", "Overweight", "Obesity class I", "Obesity class II", "Obesity class III"],
         "rows": [("range", "Normal weight for your height", "kg", True)], "warn": {}}},
 "protein": {
  "es": {"main": "g de proteína al día", "rows": [
          ("gkg", "Gramos por kilo de referencia", "g/kg", False),
          ("ref", "Peso de referencia", "kg", False),
          ("prange", "Rango de 1,2 a 2,0 g/kg", "g", False),
          ("efsa", "Mínimo EFSA (0,83 g/kg)", "g", False),
          ("meal3", "Por comida, en tres comidas", "g", True),
          ("meal4", "Por comida, en cuatro comidas", "g", False)],
         "warn": {"ref": "Tu IMC pasa de 25, así que la proteína se calcula sobre el peso que tendrías con un IMC de 25: la necesidad sigue a la masa magra, no a la grasa. Es la regla de la app."}},
  "en": {"main": "g of protein a day", "rows": [
          ("gkg", "Grams per reference kilo", "g/kg", False),
          ("ref", "Reference weight", "kg", False),
          ("prange", "Range from 1.2 to 2.0 g/kg", "g", False),
          ("efsa", "EFSA minimum (0.83 g/kg)", "g", False),
          ("meal3", "Per meal, over three meals", "g", True),
          ("meal4", "Per meal, over four meals", "g", False)],
         "warn": {"ref": "Your BMI is above 25, so protein is worked out on the weight you would have at a BMI of 25: needs follow lean mass, not fat. That is the app's rule."}}},
 "macros": {
  "es": {"main": "kcal al día", "macros": [("p", "Proteínas"), ("c", "Hidratos"), ("f", "Grasas")],
         "rows": [("tdee", "Tu mantenimiento", "kcal", False)],
         "warn": {"floor": 'Tus calorías quedarían por debajo de <b data-out="floor">1.200</b> kcal y se suben a ese suelo, como en la app. No bajes de ahí sin un profesional sanitario.',
                  "dropped": "Con estas calorías la proteína deja poco sitio: la grasa baja al 20 %, el mínimo, como hace la app."}},
  "en": {"main": "kcal a day", "macros": [("p", "Protein"), ("c", "Carbs"), ("f", "Fat")],
         "rows": [("tdee", "Your maintenance", "kcal", False)],
         "warn": {"floor": 'Your calories would fall below <b data-out="floor">1,200</b> kcal and are raised to that floor, as in the app. Do not go lower without a health professional.',
                  "dropped": "At these calories protein leaves little room: fat drops to 20%, the minimum, as the app does."}}},
 "water": {
  "es": {"main": "litros de bebida al día", "rows": [
          ("ml", "En mililitros", "ml", False),
          ("glasses", "Vasos de 250 ml", "", True),
          ("kcal", "Calculado sobre", "kcal", False),
          ("ratio", "Agua por kcal", "ml", False)],
         "warn": {"floor": 'Tu cálculo queda por debajo del mínimo de la EFSA para ti, así que el objetivo se queda en <b data-out="wfloor">1.600</b> ml.',
                  "cap": "Tu cálculo pasa de 4 litros, así que el objetivo se queda en 4.000 ml, el máximo de la app."}},
  "en": {"main": "litres of drinks a day", "rows": [
          ("ml", "In millilitres", "ml", False),
          ("glasses", "250 ml glasses", "", True),
          ("kcal", "Worked out on", "kcal", False),
          ("ratio", "Water per kcal", "ml", False)],
         "warn": {"floor": 'Your figure falls below the EFSA minimum for you, so the target stays at <b data-out="wfloor">1,600</b> ml.',
                  "cap": "Your figure is above 4 litres, so the target stays at 4,000 ml, the app's maximum."}}},
 "bmr": {
  "es": {"main": "kcal al día en reposo", "rows": [
          ("mifflin", "Mifflin-St Jeor", "kcal", False),
          ("katch", "Katch-McArdle (con tu grasa)", "kcal", False)],
         "warn": {"katch": "Has puesto tu grasa corporal: el resultado usa Katch-McArdle, como la app."}},
  "en": {"main": "kcal a day at rest", "rows": [
          ("mifflin", "Mifflin-St Jeor", "kcal", False),
          ("katch", "Katch-McArdle (with your body fat)", "kcal", False)],
         "warn": {"katch": "You entered your body fat: the result uses Katch-McArdle, as the app does."}}},
 "healthy": {
  "es": {"main": "kg, tu rango de peso saludable", "rows": [
          ("bmi", "Tu IMC actual", "", False),
          ("mid", "Mitad del rango (IMC 22)", "kg", False)],
         "warn": {"inside": "Estás dentro del rango saludable para tu altura.",
                  "over": 'Estás <b data-out="gap">2,0</b> kg por encima del límite alto del rango.',
                  "under": 'Estás <b data-out="gap">2,0</b> kg por debajo del límite bajo del rango: si no es tu constitución de siempre, habla con un profesional sanitario.'}},
  "en": {"main": "kg, your healthy weight range", "rows": [
          ("bmi", "Your current BMI", "", False),
          ("mid", "Middle of the range (BMI 22)", "kg", False)],
         "warn": {"inside": "You are inside the healthy range for your height.",
                  "over": 'You are <b data-out="gap">2.0</b> kg above the top of the range.',
                  "under": 'You are <b data-out="gap">2.0</b> kg below the bottom of the range: if that is not how you have always been, talk to a health professional.'}}},
}

BRIDGE_SUB = {
    "es": {"kcal": "Haz una foto y Fotocal las cuenta por ti.", "protein": "Haz una foto y Fotocal cuenta la proteína de cada plato por ti.",
           "water": "Fotocal lleva el agua del día junto a tus comidas: un toque por vaso.", "other": "Haz una foto de cada plato y Fotocal cuenta las calorías por ti."},
    "en": {"kcal": "Snap a photo and Fotocal counts them for you.", "protein": "Snap a photo and Fotocal counts the protein in each dish for you.",
           "water": "Fotocal tracks your water next to your meals: one tap per glass.", "other": "Snap a photo of each dish and Fotocal counts the calories for you."},
}
BRIDGE_KIND = {"tdee": "kcal", "deficit": "kcal", "macros": "kcal", "protein": "protein", "water": "water", "bmi": "other", "bmr": "other", "healthy": "other"}

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


# ── default results, from calc.js itself ─────────────────────────────
def defaults():
    js = ("const C=require(process.argv[1]);const o={};"
          "for(const k of Object.keys(C.NEEDS)){o[k]={};for(const l of ['es','en'])o[k][l]=C.compute(k,{},l);}"
          "o._d=C.DEFAULTS;o._k=C.KIND_DEFAULTS;o._n=C.NEEDS;process.stdout.write(JSON.stringify(o));")
    out = subprocess.run(["node", "-e", js, os.path.join(ROOT, "assets", "js", "calc.js")], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


DEF = None
NUM_LIMITS = {"age": (18, 90), "height": (130, 230), "weight": (35, 250), "target": (35, 250), "bf": (3, 60), "kcal": (1000, 6000)}


def num_str(v, lang):
    s = ("%g" % v) if v is not None else ""
    return s.replace(".", ",") if lang == "es" else s


# ── the form ─────────────────────────────────────────────────────────
def form(kind, lang, slug):
    u, d = UI[lang], dict(DEF["_d"], **DEF["_k"].get(kind, {}))
    pid = slug[:3]
    o = ['      <form class="calc" data-calc="%s" novalidate aria-label="%s">' % (kind, esc(u["calc"])), '        <div class="calc-grid">']
    for k in DEF["_n"][kind]:
        fid = "%s-%s-%s" % (pid, k, lang)
        if k == "sex":
            o.append('          <fieldset class="calc-field wide"><legend>%s</legend><div class="calc-seg">' % u["sex"])
            for v in ("f", "m"):
                o.append('            <input type="radio" name="sex" id="%s-%s" value="%s"%s><label for="%s-%s">%s</label>' % (fid, v, v, " checked" if d["sex"] == v else "", fid, v, u[v]))
            o.append('          </div></fieldset>')
        elif k in ("activity", "goal", "pace", "split"):
            opts = {"activity": [(a, lab + " (×" + f + ")") for a, lab, f in ACT_ROWS[lang]], "goal": u["goals"], "pace": u["paces"], "split": u["splits"]}[k]
            cur = str(d[k]) if k != "pace" else ("%g" % d[k])
            wide = " wide" if k in ("activity", "pace") else ""
            o.append('          <div class="calc-field%s"><label for="%s">%s</label><select id="%s" name="%s">' % (wide, fid, esc(u[k]), fid, k))
            for v, lab in opts:
                o.append('            <option value="%s"%s>%s</option>' % (v, " selected" if v == cur else "", esc(lab)))
            o.append('          </select></div>')
        else:
            label = u["weight_opt"] if (k == "weight" and kind == "healthy") else u[k]
            val = d[k] if k not in ("bf", "kcal") else None
            hint = {"kcal": u["hint_kcal"], "bf": u["hint_bf"]}.get(k)
            o.append('          <div class="calc-field"><label for="%s">%s</label><input id="%s" name="%s" type="text" inputmode="decimal" autocomplete="off" value="%s"%s%s></div>'
                     % (fid, esc(label), fid, k, num_str(val, lang), (' placeholder="%s"' % esc(hint)) if hint else "", ' data-dec=","' if lang == "es" else ""))
    o.append('        </div>')
    o.append('      </form>')
    return "\n".join(o)


def result(c, lang):
    kind, u, spec = c["kind"], UI[lang], OUT[c["kind"]][lang]
    r = DEF[kind][lang]
    v = r["out"]
    o = ['      <section class="calc-out" data-calc-out="%s" aria-labelledby="res-%s">' % (kind, lang),
         '        <h2 class="calc-out-h" id="res-%s">%s</h2>' % (lang, u["result"]),
         '        <p class="calc-main" aria-live="polite"><b data-out="main">%s</b> <span>%s</span></p>' % (v["main"], spec["main"])]
    if kind == "bmi":
        o.append('        <p class="calc-cat">%s</p>' % "".join('<span data-cat="%d"%s>%s</span>' % (i, "" if i == r["cat"] else " hidden", esc(t)) for i, t in enumerate(spec["cats"])))
    if kind == "macros":
        o.append('        <div class="calc-macros">')
        for k, lab in spec["macros"]:
            o.append('          <div class="calc-macro m-%s"><b><span data-out="%s">%s</span> g</b><span>%s · <span data-out="%sk">%s</span> kcal · <span data-out="%sp">%s</span> %%</span></div>'
                     % (k, k, v[k], lab, k, v[k + "k"], k, v[k + "p"]))
        o.append('        </div>')
        o.append('        <div class="dp-bar" aria-hidden="true">%s</div>' % "".join('<span class="%s" data-bar="%s" style="width:%.1f%%"></span>' % (k, k, r["bars"][k]) for k in ("p", "c", "f")))
    o.append('        <div class="calc-rows">')
    for key, lab, unit, hl in spec["rows"]:
        if key in ("range", "prange"):
            val = '<span data-out="lo">%s</span>–<span data-out="hi">%s</span>' % (v["lo"], v["hi"])
        else:
            val = '<span data-out="%s">%s</span>' % (key, v[key])
        o.append('          <div class="calc-row%s"><span>%s</span><b>%s%s</b></div>' % (" is-hl" if hl else "", esc(lab), val, (" " + unit) if unit else ""))
    if kind == "bmr":
        for a, lab, f in ACT_ROWS[lang]:
            o.append('          <div class="calc-row%s"><span>%s (×%s)</span><b><span data-out="t_%s">%s</span> kcal</b></div>' % (" is-hl" if a == "light" else "", esc(lab), f, a, v["t_" + a]))
    o.append('        </div>')
    for wk, html in spec["warn"].items():
        html = re.sub(r'(<b data-out="([a-z]+)">)[^<]*(</b>)', lambda m: m.group(1) + v[m.group(2)] + m.group(3), html)
        o.append('        <p class="calc-warn" data-warn="%s"%s>%s</p>' % (wk, "" if wk in r["warn"] else " hidden", html))
    o.append('        <button class="calc-share" type="button" data-calc-share><span class="calc-share-a">%s</span><span class="calc-share-b">%s</span></button>' % (u["share"], u["copied"]))
    # the bridge to the app
    head = esc(c[lang]["bridge"]).replace("{X}", '<b data-out="bridge">%s</b>' % v.get("bridge", ""))
    o.append('        <div class="calc-bridge">')
    o.append('          <p class="calc-bridge-h">%s</p>' % head)
    o.append('          <p>%s</p>' % BRIDGE_SUB[lang][BRIDGE_KIND[kind]])
    o.append('          <a class="btn btn-cta" href="%s" target="_blank" rel="noopener">%s</a>' % (esc(play(c["slug"])), u["cta"]))
    o.append('          <p class="calc-bridge-note">%s</p>' % u["free"])
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


def foot(depth, calc=True):
    up = "../" * depth
    return """
<div id="site-footer"></div>
<script src="%sassets/js/i18n.js"></script>
<script src="%sassets/js/layout.js" data-page="calculadoras"></script>
<script src="%sassets/js/main.js"></script>%s
</body>
</html>
""" % (up, up, up, ('\n<script src="%sassets/js/calc.js"></script>' % up) if calc else "")


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
    o.append('      <p class="calc-disclaimer">%s</p>' % u["disclaimer"])
    o.append('     </div>')
    o.append('     <div class="calc-text post-body">')
    o.append(L["body"])
    o.append('      <h2 id="faq">%s</h2>\n      <div class="faq-list">' % u["faq"])
    for i, (q, a) in enumerate(L["faq"]):
        o.append('        <details class="faq-item"%s><summary><span>%s</span><i class="faq-plus" aria-hidden="true"></i></summary><p>%s</p></details>' % (" open" if i == 0 else "", esc(q), a))
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
    return "\n".join('<div class="calc-sticky" data-lang-block="%s"><span>%s</span><a class="btn btn-cta" href="%s" target="_blank" rel="noopener">%s</a></div>'
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
           "h1": "Calculadoras de calorías, IMC, macros y más",
           "lead": "Ocho calculadoras para las preguntas que llegan antes de cualquier dieta. Funcionan aquí, en la página, sin registro y sin enviar tus datos, y dan los mismos números que la app Fotocal.",
           "go": "Calcular →",
           "body": """
      <h2>En qué orden usarlas</h2>
      <p>Primero las <a href="calorias-diarias/">calorías diarias</a>, la base de todo lo demás. Si quieres perder grasa, después el <a href="deficit-calorico/">déficit calórico</a>, que te dice cuánto recortar y cuánto tardarás. Las <a href="proteinas/">proteínas</a> y los <a href="macros/">macros</a> reparten esas calorías. El <a href="imc/">IMC</a> y el <a href="peso-saludable/">peso saludable</a> te sitúan; la <a href="tmb/">TMB</a> explica de dónde sale tu gasto, y la de <a href="agua/">agua</a> te dice cuánto beber.</p>
      <h2>De dónde salen estos números</h2>
      <p>De las mismas fórmulas que usa la app Fotocal: Mifflin-St Jeor (1990) para el metabolismo, los rangos de IMC de la OMS, y las referencias de la EFSA para la proteína y el agua. Cada calculadora explica su fórmula con un ejemplo y cita sus fuentes. Si quieres los datos de lo que comes, la <a href="../calorias/">tabla de calorías de platos españoles</a>.</p>""",
           "disclaimer": "Orientativo, no sustituye a un profesional sanitario."},
    "en": {"title": "Calorie, BMI, macro and water calculators",
           "desc": "Eight calculators, no sign-up: daily calories, calorie deficit, BMI, protein, macros, water, BMR and healthy weight, with the same formulas as the app.",
           "h1": "Calorie, BMI and macro calculators",
           "lead": "Eight calculators for the questions that come before any diet. They work here, in the page, with no sign-up and nothing sent anywhere, and give the same numbers as the Fotocal app.",
           "go": "Calculate →",
           "body": """
      <h2>Which order to use them in</h2>
      <p>First <a href="calorias-diarias/">daily calories</a>, the base for everything else. To lose fat, then the <a href="deficit-calorico/">calorie deficit</a>, which tells you how much to cut and how long it takes. <a href="proteinas/">Protein</a> and <a href="macros/">macros</a> split those calories. <a href="imc/">BMI</a> and <a href="peso-saludable/">healthy weight</a> show where you stand; <a href="tmb/">BMR</a> explains where your energy use comes from, and <a href="agua/">water</a> tells you how much to drink.</p>
      <h2>Where these numbers come from</h2>
      <p>From the same formulas the Fotocal app uses: Mifflin-St Jeor (1990) for metabolism, the WHO BMI bands, and EFSA references for protein and water. Each calculator explains its formula with a worked example and cites its sources. For the numbers of what you eat, the <a href="../calorias/">table of calories in Spanish dishes</a> (in Spanish).</p>""",
           "disclaimer": "For guidance only; not a substitute for a health professional."},
}


def hub():
    meta, parts = {}, []
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
        o.append('      <ul class="calc-cards">')
        for c in CALCS:
            o.append('        <li><a class="calc-card" href="%s/"><span class="calc-card-ico">%s</span><strong>%s</strong><span class="calc-card-t">%s</span><span class="calc-card-go">%s</span></a></li>'
                     % (c["slug"], icon(c["icon"]), esc(c[lang]["h1"]), esc(c[lang]["card"]), H["go"]))
        o.append('      </ul>')
        o.append('      <div class="post-body calc-hub-text">%s\n      <p class="calc-disclaimer">%s</p>\n      </div>' % (H["body"], H["disclaimer"]))
        o.append('    </div>')
        o.append(ld_block({"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": H["desc"], "inLanguage": lang, "url": url, "publisher": ORG,
                           "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c[lang]["h1"], "url": SITE + "calculadoras/%s/" % c["slug"]} for i, c in enumerate(CALCS)]}}))
        o.append(ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": SITE}, {"@type": "ListItem", "position": 2, "name": u["calcs"], "item": url}]}))
        o.append('  </div>')
        parts.append("\n".join(o))
    out = [head(1, meta, "calculadoras/"), '\n<main id="main" class="calc-main-wrap calc-hub">'] + parts + ["</main>", foot(1, calc=False)]
    return "\n".join(out)


def main():
    global DEF
    DEF = defaults()
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
