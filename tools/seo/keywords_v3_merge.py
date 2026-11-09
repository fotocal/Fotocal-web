#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MASTER PROMPT v3, PART 1 (9 Nov 2026): merge the owner's live research
(Google autocomplete es-ES / en-US, People also ask, google.es results, all
gathered on 9 Nov 2026) into docs/seo/keywords.csv, and write the
anti-cannibalisation map docs/seo/keyword-map.md (one primary per URL).

Run once; it is idempotent (re-running gives the same file).

    python3 tools/seo/keywords_v3_merge.py

Columns kept: every original column and row. `priority` keeps 1/2/3
(= P1/P2/P3; tools/seo/dish_queue.py sorts on it). `intent` now uses the
v3 taxonomy (tool / dish-info / list-compare / review / how-to / brand /
app-download); the original value is kept in `intent_2026_11_08`.
Columns added: page_url, primary_keyword, secondary_keywords,
competitor_urls_ranking, cluster, source, date_checked, intent_2026_11_08.
Accent / article variants ("calorías paella" = "calorias de la paella")
are one row; the other spellings go to secondary_keywords.
"""
import csv, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "docs", "seo", "keywords.csv")
MAP = os.path.join(ROOT, "docs", "seo", "keyword-map.md")
SITE = "https://getfotocal.com"
TODAY = "2026-11-09"
EVID = "owner research 2026-11-09: Google autocomplete hl=es gl=es / hl=en gl=us, PAA and google.es results (MASTER PROMPT v3 §A)"


def norm(k):
    k = unicodedata.normalize("NFD", k.lower())
    k = "".join(c for c in k if unicodedata.category(c) != "Mn")
    k = re.sub(r"[¿?¡!.,:;()]", " ", k)
    return " ".join(w for w in k.split() if w not in {"de", "del", "la", "el", "los", "las", "un", "una"})


def url(path, lang="es"):
    if path.startswith("NEW:"):
        p = path[4:]
        return "NEW:" + ("/en" + p if lang == "en" else p)
    return SITE + ("/en" + path if lang == "en" else path)


# ── B.1: one primary per URL ─────────────────────────────────────────
# path: (primary ES, [secondaries ES], primary EN, cluster)
PAGES = {
    "/": ("contador de calorías con foto", ["contador de calorías gratis", "app contar calorías", "app contar calorías con foto gratis", "contar calorías con ia", "calorías y macros", "contar calorías sin pesar"], "photo calorie counter app", "app"),
    "/features/scan-food/": ("contar calorías con foto", ["escanear comida calorías", "calorías por foto", "escáner de calorías con ia", "qué aplicación mide calorías con una foto", "precisión"], "ai food scanner", "app-photo"),
    "/features/scan-barcode/": ("escáner código de barras calorías", ["escanear código de barras alimentos", "app escanear calorías gratis"], "free barcode scanner calorie counter", "app-barcode"),
    "/features/voice-logging/": ("contar calorías por voz", ["registrar comidas hablando", "dictar comidas", "registrar comida por voz"], "voice calorie tracker", "app-voice"),
    "/features/": ("funciones app contar calorías", ["contar calorías con foto, voz y código", "coach ia nutrición"], "calorie counter app features", "app"),
    "/features/weight-loss/": ("app para adelgazar contando calorías", ["app para adelgazar gratis", "perder peso contando calorías"], "weight loss calorie counter app", "app-weight-loss"),
    "/features/nutrition-diet/": ("app de dieta y macros", ["contador de macros", "panel de nutrición"], "macro tracker app", "app-nutrition"),
    "/features/lifestyle-mindset/": ("hábitos para adelgazar", ["comer mejor sin obsesionarse", "hábitos saludables app"], "healthy eating habits app", "app-habits"),
    "/calculadoras/": ("calculadoras de nutrición gratis", ["calculadora de calorías, imc y macros", "calculadoras sin registro"], "free nutrition calculators", "calc-hub"),
    "/calculadoras/calorias-diarias/": ("calculadora de calorías diarias", ["cuántas calorías debo comer al día", "calorías de mantenimiento", "calorías que gasto al día", "calculadora de calorías harris benedict", "calculadora de calorías mifflin st jeor", "gasto energético"], "daily calorie calculator", "calc-daily"),
    "/calculadoras/deficit-calorico/": ("calculadora de déficit calórico", ["déficit calórico mujer", "déficit calórico hombre", "cómo calcular el déficit calórico", "cuánto déficit calórico para perder 1 kg", "calorías para adelgazar", "calculadora déficit calórico y macros"], "calorie deficit calculator", "calc-deficit"),
    "/calculadoras/imc/": ("calculadora de imc", ["calculadora imc mujer", "calculadora imc hombre", "índice de masa corporal", "imc según edad", "tabla imc"], "bmi calculator", "calc-bmi"),
    "/calculadoras/macros/": ("calculadora de macros", ["calculadora de macros y calorías", "macros para perder grasa", "macros diarios", "proteínas grasas carbohidratos"], "macro calculator", "calc-macros"),
    "/calculadoras/proteinas/": ("calculadora de proteínas", ["proteínas por kilo de peso", "cuántas proteínas hay que tomar al día", "proteína para ganar músculo", "proteína para perder grasa"], "protein calculator", "calc-protein"),
    "/calculadoras/tmb/": ("calculadora tmb", ["metabolismo basal", "calculadora tmb y get", "tmb mujer", "tmb hombre", "mifflin st jeor", "harris benedict", "katch-mcardle"], "bmr calculator", "calc-bmr"),
    "/calculadoras/agua/": ("cuánta agua beber al día", ["calculadora de agua", "cuánta agua beber según tu peso", "si peso 70 kilos cuánta agua debo beber", "agua para bajar de peso", "agua con creatina"], "how much water to drink a day", "calc-water"),
    "/calculadoras/peso-saludable/": ("peso ideal según altura", ["calculadora peso ideal", "peso ideal mujer", "peso ideal hombre", "peso ideal según estatura y edad", "tabla de peso ideal"], "ideal weight by height", "calc-ideal-weight"),
    "/calorias/": ("calorías de platos españoles", ["tabla de calorías de comida española", "calorías por ración y por 100 g", "calorías de las tapas"], "calories in spanish food", "dish-hub"),
    "/calorias/tabla-de-calorias/": ("tabla de calorías de alimentos", ["tabla de calorías por 100 gramos", "tabla de calorías por alimentos y porciones", "tabla de calorías y proteínas", "alimentos con más calorías"], "food calorie chart", "dish-table"),
    "/comparativa/": ("mejor app para contar calorías", ["apps para contar calorías en españa", "mejor app para contar calorías con foto", "mejor app para contar calorías con ia", "mejor app para contar calorías gratis", "mejor app para contar calorías y macros", "mejor app para contar calorías 2026"], "best calorie counter app", "compare"),
    "/comparativa/fotocal-vs-myfitnesspal/": ("fotocal vs myfitnesspal", ["myfitnesspal o fotocal", "es gratuita myfitnesspal", "precio myfitnesspal premium"], "fotocal vs myfitnesspal", "compare"),
    "/comparativa/fotocal-vs-yazio/": ("fotocal vs yazio", ["es gratis yazio", "cuánto vale yazio"], "fotocal vs yazio", "compare"),
    "/comparativa/fotocal-vs-cal-ai/": ("fotocal vs cal ai", ["cal ai precio", "es gratis cal ai", "cal ai android"], "fotocal vs cal ai", "compare"),
    "/guias/": ("guías para contar calorías", ["cómo contar calorías", "cómo empezar a contar calorías"], "calorie counting guides", "guide"),
    # D list: new pages (PARTs after C). Owned now so nothing else takes them.
    "NEW:/comparativa/alternativas-myfitnesspal/": ("alternativa a myfitnesspal", ["alternativa gratuita a myfitnesspal", "alternativa gratis a myfitnesspal", "alternativas a myfitnesspal"], "myfitnesspal alternative", "compare"),
    "NEW:/comparativa/cal-ai-opiniones/": ("cal ai opiniones", ["cal ai es gratis", "cal ai es de pago", "cal ai precio app", "es fiable cal ai"], "cal ai alternative for android", "review"),
    "NEW:/comparativa/yazio-opiniones/": ("yazio opiniones", ["yazio es gratis", "yazio es de pago", "cuesta dinero yazio"], "yazio review", "review"),
    "NEW:/blog/calorias-para-adelgazar-mujer/": ("calorías para adelgazar mujer", ["cuántas calorías debe comer una mujer para adelgazar", "qué pasa si como 1500 calorías al día", "calorías para adelgazar 1 kilo por semana"], "calories to lose weight for women", "guide-women"),
}

# Blog posts: B.1 rows first, then a Spanish search phrase per post (the
# topic of its H1). Provisional for the rollout PARTs 11–14.
BLOG = {
    "app-contar-calorias-gratis": ("app para contar calorías gratis", ["contador de calorías gratis sin pagar", "qué incluye gratis cada app", "app calorías sin suscripción"], "free calorie counter app no subscription"),
    "calorie-deficit-for-fat-loss": ("déficit calórico qué es y cómo hacerlo", ["cómo hacer un déficit calórico", "qué comer en déficit calórico", "qué no comer en déficit calórico"], "calorie deficit explained"),
    "deficit-500-calorias-dia": ("déficit de 500 calorías", ["cuánto se adelgaza con 500 kcal de déficit", "déficit de 500 calorías qué comer"], "500 calorie deficit"),
    "calorias-para-perder-un-kilo": ("calorías para perder un kilo", ["7700 kcal mito o realidad", "perder 1 kilo por semana", "cuántas calorías hay que quemar para perder un kilo"], "calories to lose a kilo"),
    "how-much-protein-per-day": ("cuánta proteína necesito al día", ["proteína por kilo", "proteína para mujeres"], "how much protein per day"),
    "tdee-how-many-calories-you-need": ("qué es el tdee", ["get gasto energético total", "gasto calórico diario"], "what is tdee"),
    "understanding-your-basal-metabolic-rate": ("qué es el metabolismo basal", ["tmb qué es", "cómo subir el metabolismo"], "what is bmr"),
    "photo-calorie-apps-accuracy": ("son precisas las apps de calorías con foto", ["precisión ia calorías", "fiabilidad apps calorías foto"], "are photo calorie apps accurate"),
    "choose-photo-calorie-counter": ("cómo elegir una app de calorías con foto", ["qué mirar en una app de calorías", "precio y privacidad apps calorías"], "how to choose a photo calorie app"),
    "added-sugar-vs-natural-sugar": ("azúcar añadido vs natural", [], "added sugar vs natural sugar"),
    "best-foods-for-weight-loss": ("alimentos que sacian con pocas calorías", ["mejores alimentos para adelgazar"], "low calorie filling foods"),
    "building-muscle-while-losing-fat": ("ganar músculo y perder grasa a la vez", ["recomposición corporal"], "build muscle while losing fat"),
    "calorias-bocadillo": ("calorías bocadillo", ["cuántas calorías tiene un bocadillo"], "calories in a spanish sandwich bocadillo"),
    "calorias-de-las-tapas": ("calorías de las tapas", ["cuántas calorías tiene una tarde de cañas"], "calories in tapas"),
    "calorias-desayuno-espanol": ("calorías desayuno español", ["desayuno de bar calorías"], "spanish breakfast calories"),
    "calorias-menu-del-dia": ("calorías menú del día", [], "menu del dia calories"),
    "carbs-are-not-the-enemy": ("los carbohidratos engordan", [], "are carbs bad for weight loss"),
    "cardio-vs-strength-training-for-fat-loss": ("cardio o pesas para perder grasa", [], "cardio vs weights for fat loss"),
    "cena-ligera-menos-de-500-calorias": ("cena ligera menos de 500 calorías", ["cenas ligeras para adelgazar"], "light dinner under 500 calories"),
    "common-calorie-counting-mistakes": ("errores al contar calorías", [], "calorie counting mistakes"),
    "dietary-fat-how-much-and-which-kinds": ("cuánta grasa comer al día", ["grasas saludables"], "how much fat per day"),
    "do-calories-matter-or-food-quality": ("calorías o calidad de la comida", ["contar calorías funciona"], "calories vs food quality"),
    "do-you-need-to-exercise-to-lose-weight": ("adelgazar sin hacer ejercicio", [], "lose weight without exercise"),
    "does-meal-timing-matter-for-weight-loss": ("cenar tarde engorda", ["horario de las comidas para adelgazar"], "does meal timing matter for weight loss"),
    "does-protein-timing-matter": ("cuándo tomar proteína", [], "protein timing"),
    "eating-out-without-wrecking-your-diet": ("comer fuera sin engordar", [], "eating out on a diet"),
    "emotional-eating": ("comer por ansiedad", ["hambre emocional"], "emotional eating"),
    "fiber-the-underrated-nutrient": ("fibra para adelgazar", [], "fiber for weight loss"),
    "healthy-snacks-that-satisfy": ("snacks saludables que sacian", ["snacks saludables pocas calorías"], "healthy filling snacks"),
    "high-protein-breakfast-ideas": ("desayunos altos en proteína", [], "high protein breakfast ideas"),
    "high-protein-diet-benefits-and-how-to-start": ("dieta alta en proteínas", [], "high protein diet"),
    "how-fast-should-you-lose-weight": ("cuánto peso se puede perder en una semana", ["cuántos kilos se pueden perder en un mes"], "how fast can you lose weight"),
    "how-many-calories-does-exercise-burn": ("cuántas calorías quema el ejercicio", ["calorías quemadas caminando 1 hora"], "how many calories does exercise burn"),
    "how-sleep-affects-your-weight": ("dormir poco engorda", [], "how sleep affects weight"),
    "how-to-build-a-healthy-grocery-list": ("lista de la compra saludable", [], "healthy grocery list"),
    "how-to-count-calories-accurately": ("cómo contar calorías para principiantes", [], "how to count calories"),
    "how-to-eat-healthy-on-a-budget": ("comer sano y barato", [], "eat healthy on a budget"),
    "how-to-handle-cravings-without-guilt": ("cómo controlar los antojos", [], "how to handle cravings"),
    "how-to-lose-weight-sustainably": ("cómo adelgazar sin dietas", [], "how to lose weight sustainably"),
    "how-to-read-nutrition-labels": ("cómo leer etiquetas nutricionales", [], "how to read nutrition labels"),
    "how-to-set-your-macros-for-weight-loss": ("cómo calcular macros para perder peso", ["cómo calcular mis macros"], "how to set macros for weight loss"),
    "how-to-stay-consistent-with-healthy-habits": ("cómo ser constante con la dieta", [], "how to stay consistent with healthy habits"),
    "how-to-stop-overeating-at-night": ("cómo dejar de comer por la noche", [], "how to stop eating at night"),
    "hydration-and-weight": ("beber agua adelgaza", [], "does drinking water help weight loss"),
    "intermittent-fasting-what-the-evidence-says": ("ayuno intermitente qué dice la ciencia", ["ayuno intermitente funciona para adelgazar"], "intermittent fasting evidence"),
    "intuitive-eating-vs-calorie-counting": ("alimentación intuitiva o contar calorías", [], "intuitive eating vs calorie counting"),
    "low-carb-vs-low-fat": ("dieta baja en carbohidratos o baja en grasa", [], "low carb vs low fat"),
    "macronutrients-101": ("qué son los macronutrientes", [], "what are macronutrients"),
    "maintaining-weight-loss": ("cómo mantener el peso después de adelgazar", [], "how to maintain weight loss"),
    "meal-prep-for-beginners": ("meal prep para principiantes", [], "meal prep for beginners"),
    "mindful-eating-beginners-guide": ("alimentación consciente", [], "mindful eating"),
    "neat-the-hidden-calorie-burn": ("qué es el neat", [], "what is neat"),
    "plan-a-week-of-meals-in-30-minutes": ("planificar menú semanal", [], "plan a week of meals"),
    "portion-control-simple-tricks": ("controlar las raciones", ["método de la mano porciones"], "portion control tips"),
    "the-truth-about-detox-diets-and-cleanses": ("dietas détox funcionan", [], "do detox diets work"),
    "the-truth-about-starvation-mode": ("modo supervivencia metabolismo", ["modo ahorro metabolismo mito"], "starvation mode myth"),
    "track-calories-without-weighing": ("cómo contar calorías sin pesar", ["contar calorías sin báscula"], "how to count calories without weighing food"),
    "weight-loss-plateaus": ("estancamiento al perder peso", ["estancamiento perder peso qué hacer"], "weight loss plateau"),
    "what-a-balanced-plate-looks-like": ("plato equilibrado", ["plato de harvard"], "balanced plate"),
    "why-crash-diets-fail": ("por qué fallan las dietas", ["dietas exprés"], "why crash diets fail"),
    "why-micronutrients-matter": ("micronutrientes qué son", [], "why micronutrients matter"),
    "why-the-scale-is-not-the-whole-story": ("la báscula no baja pero adelgazo", [], "why the scale is not the whole story"),
}

EN_DISH = {  # English names people type (§A.2: "Spanish omelette", not "tortilla de patatas")
    "tortilla-de-patatas": "spanish omelette", "paella-valenciana": "paella", "croquetas-de-jamon": "spanish ham croquettes",
    "gambas-al-ajillo": "garlic prawns", "patatas-bravas": "patatas bravas", "churros-con-chocolate": "churros with chocolate",
    "gazpacho": "gazpacho", "salmorejo": "salmorejo", "cocido-madrileno": "cocido madrileño", "pulpo-a-la-gallega": "galician octopus",
    "jamon-serrano": "serrano ham", "calamares-a-la-romana": "fried calamari", "fabada-asturiana": "fabada", "pincho-de-tortilla": "a slice of spanish omelette",
}

# ── A.2 / A.3 / A.4: rows to add or update ───────────────────────────
# (keyword, lang, page path, intent, priority, source)
A = []
def add(path, intent, prio, src, lang, *kws):
    for k in kws:
        A.append((k, lang, path, intent, prio, src))

AC, PAA, SERP = "autocomplete", "PAA", "SERP"
# App / product (ES)
add("/", "app-download", 1, AC, "es", "contador de calorías gratis", "contador de calorías de alimentos", "contador de calorías online", "contador de calorías app", "app contar calorías", "app contar calorías ia gratis", "app contar calorías y macros", "app calorías gratis", "app cuenta calorías gratis", "app contador calorías gratis", "app calcular calorías gratis")
add("/", "app-download", 2, SERP, "es", "contador de calorías")
add("/features/scan-food/", "app-download", 1, AC, "es", "contador de calorías con foto gratis", "contador de calorías por foto", "app contar calorías con foto", "contar calorías con foto gratis", "contar calorías con foto online", "aplicación contar calorías con foto gratis", "apps para contar calorías con fotos gratis", "contador de calorías ia", "contador de calorías foto ia", "contador de calorías por ia gratis", "app contador de calorías ia", "escanear comida calorías gratis", "app escanear comida calorías", "escanear calorías", "app foto calorías gratis", "app escanear calorías gratis")
add("/comparativa/", "list-compare", 1, AC, "es", "mejor contador de calorías con ia", "mejor app calorías gratis", "mejor app para contar calorías con foto", "mejor app para contar calorías y macros", "mejor app para contar calorías gratis", "mejor app para contar calorías y macros gratis", "mejor app para contar calorías y proteínas", "mejor app para contar calorías con ia", "mejor app para contar calorías españa")
add("NEW:/comparativa/alternativas-myfitnesspal/", "list-compare", 1, AC, "es", "alternativa gratuita a myfitnesspal", "alternativa gratis a myfitnesspal")
add("NEW:/comparativa/yazio-opiniones/", "review", 2, AC, "es", "yazio opiniones", "yazio es gratis", "yazio es de pago", "yazio pro")
add("NEW:/comparativa/cal-ai-opiniones/", "review", 1, AC, "es", "cal ai es gratis", "cal ai es de pago", "cal ai precio", "cal ai opiniones")
# Calculators (ES)
add("/calculadoras/calorias-diarias/", "tool", 1, AC, "es", "calculadora de calorías harris benedict", "calculadora de calorías diarias", "calculadora de calorías para perder peso", "calculadora de calorías y macros", "calculadora de calorías en mantenimiento", "calculadora de calorías basales", "calculadora de calorías para ganar masa muscular", "calculadora de calorías en reposo", "calculadora de calorías recomposición corporal", "calculadora de calorías que consume mi cuerpo", "cuántas calorías debo comer al día", "cuántas calorías debo comer al día para bajar de peso", "cuántas calorías debo comer para ganar masa muscular", "calcular calorías que gasto al día", "cuántas calorías gasto al día", "calorías que gasto al día en reposo")
add("/calculadoras/deficit-calorico/", "tool", 1, AC, "es", "calculadora de calorías para déficit calórico", "cuántas calorías debo comer para estar en déficit calórico", "calorías para adelgazar 1 kilo por semana", "calorías para adelgazar 2 kilos por semana", "calorías para adelgazar calculadora", "déficit calórico para perder peso", "cómo calcular déficit calórico", "déficit calórico mujer", "déficit calórico hombre", "déficit calórico para perder grasa", "calculadora déficit calórico gratis", "calculadora déficit calórico y macros", "calculadora déficit calórico harris benedict", "calculadora déficit calórico para bajar de peso")
add("/blog/calorie-deficit-for-fat-loss/", "how-to", 2, AC, "es", "déficit calórico dieta", "cómo hacer déficit calórico")
add("/calculadoras/imc/", "tool", 1, AC, "es", "calculadora imc mujer", "calculadora imc hombre", "calculadora imc con edad", "calculadora imc mujer por edad", "calculadora imc hombre edad")
add("/calculadoras/tmb/", "tool", 1, AC, "es", "calculadora tmb hombre", "calculadora tmb mujer", "calculadora tmb harris benedict", "calculadora tmb mifflin st jeor", "calculadora tmb y get", "calculadora tmb por nivel de actividad")
add("/calculadoras/macros/", "tool", 1, AC, "es", "calculadora macros gratis", "calculadora macros y calorías", "calculadora macros diarios", "calculadora macros keto")
add("/calculadoras/proteinas/", "tool", 1, AC, "es", "calculadora proteínas por peso", "calculadora proteínas gratis", "calculadora proteínas grasas carbohidratos", "cuántas proteínas hay que tomar al día", "cuántas proteínas se necesitan al día", "cuántas proteínas tengo que comer al día")
add("/calculadoras/agua/", "tool", 1, AC, "es", "cuánta agua beber al día según tu peso", "cuánta agua beber al día calculadora", "cuánta agua beber al día para bajar de peso", "cuánta agua beber al día con creatina", "cuánta agua beber al día máximo", "cuánta agua beber al día en verano")
add("/calculadoras/peso-saludable/", "tool", 1, AC, "es", "peso ideal según altura", "peso ideal según estatura y edad", "peso ideal mujer", "peso ideal hombre", "peso ideal para hombre de 1.80", "peso ideal mujer 1.70", "peso ideal mujer de 1.60")
add("NEW:/blog/calorias-para-adelgazar-mujer/", "how-to", 1, AC, "es", "calorías para adelgazar mujer", "calorías para adelgazar un kilo", "calorías para adelgazar al día", "calorías máximas para adelgazar", "cuántas calorías debo comer para adelgazar")
# Dishes (ES)
add("/calorias/paella-valenciana/", "dish-info", 1, SERP, "es", "calorías paella")
add("/calorias/paella-valenciana/", "dish-info", 1, AC, "es", "calorías paella valenciana", "calorías paella mercadona", "calorías paella 100 gramos", "calorías paella de carne", "calorías paella de verduras", "calorías paella de pescado")
add("/calorias/tortilla-de-patatas/", "dish-info", 1, AC, "es", "calorías tortilla de patatas con cebolla mercadona", "calorías tortilla de patatas mercadona", "calorías tortilla de patatas casera", "calorías tortilla de patatas 3 huevos", "calorías tortilla de patatas 4 huevos", "calorías tortilla de patatas 6 huevos", "calorías tortilla de patatas con cebolla", "calorías tortilla de patatas al microondas")
add("/calorias/tabla-de-calorias/", "dish-info", 1, AC, "es", "tabla de calorías de alimentos", "tabla de calorías por alimentos y porciones", "tabla de calorías por 100 gramos", "tabla de calorías pdf", "tabla de calorías frutas", "tabla de calorías y proteínas")
add("/calorias/huevo-cocido/", "dish-info", 1, AC, "es", "calorías de un huevo", "calorías huevo cocido")
add("/calorias/platano/", "dish-info", 1, AC, "es", "calorías de un plátano")
add("/calorias/cana-de-cerveza/", "dish-info", 1, AC, "es", "calorías de una cerveza")
add("/calorias/manzana/", "dish-info", 1, AC, "es", "calorías de una manzana")
add("/calculadoras/calorias-diarias/", "tool", 2, AC, "es", "calorías de mantenimiento")
for slug, kw in [("paella-de-marisco", "calorías paella marisco"), ("hamburguesa-casera-con-patatas", "calorías hamburguesa"), ("sandwich-de-atun", "calorías sándwich de atún"),
                 ("pechuga-de-pollo-a-la-plancha", "calorías filete de pollo"), ("filete-de-ternera-a-la-plancha", "calorías filete de ternera"), ("judias-verdes-con-patata", "calorías judías verdes"),
                 ("lomo-de-cerdo-a-la-plancha", "calorías lomo"), ("boquerones-fritos", "calorías boquerones"), ("ensaimada", "calorías ensaimada"), ("napolitana-de-chocolate", "calorías napolitana"),
                 ("garbanzos-con-espinacas", "calorías garbanzos"), ("tostada-con-aguacate", "calorías aguacate"), ("melon", "calorías melón"), ("sandia", "calorías sandía"),
                 ("mandarinas", "calorías mandarina"), ("galletas-maria", "calorías galletas"), ("donut-glaseado", "calorías donut"), ("avena-con-leche", "calorías avena")]:
    add("NEW:/calorias/%s/" % slug, "dish-info", 2, AC, "es", kw)
# Not in the app yet: kept as research, no page until the app has sourced figures.
for kw in ["calorías kebab", "calorías dürüm", "calorías lata de atún", "calorías horchata", "calorías aceitunas", "calorías fuet", "calorías queso manchego", "calorías boniato", "calorías helado", "calorías palomitas", "calorías arroz blanco", "calorías paella mixta", "calorías burrata", "calorías dorada", "calorías dátil", "calorías arándanos", "calorías melocotón", "calorías gofre", "calorías zanahoria", "calorías fanta", "calorías espárragos", "calorías castañas", "calorías oreja", "calorías guisantes", "calorías habas", "calorías pan integral", "calorías leche", "calorías zumo"]:
    add("NEW:/calorias/(not-in-app)/", "dish-info", 3, AC, "es", kw)
# PAA (ES) → FAQ material for the page that owns the topic
add("/comparativa/", "list-compare", 1, PAA, "es", "qué app es la mejor para contar calorías gratis", "cuál es la mejor aplicación para contar calorías", "dónde contar calorías gratis")
add("/blog/app-contar-calorias-gratis/", "how-to", 2, PAA, "es", "cómo puedo medir mis calorías gratis")
add("/blog/how-to-count-calories-accurately/", "how-to", 2, PAA, "es", "cómo contar las calorías")
add("/features/scan-food/", "app-download", 1, PAA, "es", "qué aplicación mide calorías con una foto", "cuál es la mejor ia para contar calorías")
add("/comparativa/fotocal-vs-myfitnesspal/", "list-compare", 2, PAA, "es", "es gratuita myfitnesspal", "cuánto vale myfitnesspal premium")
add("NEW:/comparativa/alternativas-myfitnesspal/", "list-compare", 2, PAA, "es", "cuáles son las alternativas a myfitnesspal", "qué app es mejor myfitnesspal o fatsecret")
add("/calculadoras/deficit-calorico/", "tool", 1, PAA, "es", "cómo calcular el déficit calórico según mi peso", "cuánto déficit calórico para perder 1 kg", "cómo puedo calcular mi déficit calórico gratis")
add("/blog/calorie-deficit-for-fat-loss/", "how-to", 2, PAA, "es", "es bueno quemar 700 calorías en un día", "cómo se hace un déficit calórico", "qué comer para lograr un déficit calórico", "qué no comer en déficit calórico")
add("NEW:/blog/calorias-para-adelgazar-mujer/", "how-to", 1, PAA, "es", "qué pasa si como 1500 calorías al día", "cuántas calorías tiene que quemar una mujer al día")
add("/blog/calorias-para-perder-un-kilo/", "how-to", 1, PAA, "es", "cuántas calorías tengo que perder para bajar 1 kilo", "cuántas calorías debo quemar para bajar 1 kilo")
add("/calculadoras/calorias-diarias/", "tool", 1, PAA, "es", "cuántas calorías debo consumir al día para no engordar")
add("/calculadoras/tmb/", "tool", 2, PAA, "es", "qué es la tmb")
add("/calculadoras/agua/", "tool", 1, PAA, "es", "cuánta agua debo beber", "cómo saber si me falta agua en el cuerpo", "si peso 70 kilos cuánta agua debo beber al día", "cuál es el mejor horario para beber agua")
add("/calculadoras/peso-saludable/", "tool", 1, PAA, "es", "cómo saber tu peso ideal según tu estatura y edad", "cuál es la tabla de peso ideal según la edad y la altura")
add("/calculadoras/imc/", "tool", 2, PAA, "es", "cómo puedo calcular mi imc según mi edad peso y altura")
add("/calorias/paella-valenciana/", "dish-info", 1, PAA, "es", "engorda mucho la paella", "es buena la paella para la dieta", "cuántas calorías tienen 300 g de paella", "cuántas calorías hay en 100 gramos de paella")
add("/calorias/tortilla-de-patatas/", "dish-info", 1, PAA, "es", "cuánto pesa una porción de 100 kcal de tortilla", "cuánto es un trozo de 100 calorías de tortilla", "cuántas calorías tienen 200 g de tortilla de patatas")
add("/calorias/croquetas-de-jamon/", "dish-info", 1, PAA, "es", "cuántas kcal puede tener una croqueta", "cuántas kcal tienen 4 croquetas", "cuántas calorías tienen 2 croquetas de cocido")
add("/calorias/lentejas-estofadas/", "dish-info", 1, PAA, "es", "puedes comer lentejas a dieta", "cuántas calorías son 100 g de lentejas cocidas", "cuántas calorías lleva un plato de lentejas", "qué tiene más calorías el arroz o las lentejas")
add("/calorias/huevo-cocido/", "dish-info", 1, PAA, "es", "cuánto son 2 huevos en calorías", "cuánto aportan 3 huevos")
add("/calorias/tortilla-francesa/", "dish-info", 1, PAA, "es", "qué engorda más un huevo frito o una tortilla francesa")
add("/calorias/tabla-de-calorias/", "dish-info", 1, PAA, "es", "cuáles son los 10 alimentos con más calorías")
add("NEW:/comparativa/cal-ai-opiniones/", "review", 1, PAA, "es", "cal ai vale la pena o es una estafa", "cal ai es fiable para contar calorías", "cuánto se paga en cal ai", "es gratuita la aplicación cal ai")
add("NEW:/comparativa/yazio-opiniones/", "review", 2, PAA, "es", "cuesta dinero yazio", "es gratuita la aplicación yazio", "cuánto vale yazio")
# EN
add("/en/", "app-download", 1, AC, "en", "calorie counter app free", "calorie counter app no subscription", "calorie counter app free no subscription")
add("/en/features/scan-barcode/", "app-download", 1, AC, "en", "calorie counter app with free barcode scanner")
add("/en/features/scan-food/", "app-download", 1, AC, "en", "ai food scanner app", "ai food scanner calories free", "ai food scanner app free", "photo calorie counter app free", "photo calorie counter app free no subscription", "photo calorie counter app free android", "photo calorie counter accuracy")
add("/en/calculadoras/deficit-calorico/", "tool", 1, AC, "en", "calorie deficit calculator for weight loss", "calorie deficit calculator tdee", "calorie deficit calculator free", "calorie deficit calculator for women")
add("/en/calculadoras/tmb/", "tool", 1, AC, "en", "bmr calculator for women", "bmr calculator with body fat", "bmr calculator mifflin-st jeor")
add("/en/calculadoras/macros/", "tool", 1, AC, "en", "macro calculator for weight loss", "macro calculator women", "macro calculator body recomp")
add("/en/calculadoras/proteinas/", "tool", 1, AC, "en", "protein calculator for weight loss", "protein calculator muscle growth", "protein calculator weight loss female")
add("NEW:/en/comparativa/alternativas-myfitnesspal/", "list-compare", 1, AC, "en", "myfitnesspal alternative 2026", "myfitnesspal alternative with barcode scanner free", "myfitnesspal alternative europe", "myfitnesspal alternative android")
add("NEW:/en/comparativa/cal-ai-opiniones/", "review", 1, AC, "en", "cal ai alternative for android", "best cal ai alternative", "is there a cal ai app for android")
add("/en/calorias/tortilla-de-patatas/", "dish-info", 1, AC, "en", "calories in spanish omelette", "calories in spanish tortilla", "how many calories does a 3-egg omelette have", "is a spanish omelette good for you")
add("/en/calorias/paella-valenciana/", "dish-info", 1, AC, "en", "calories in paella", "is paella healthy or unhealthy", "is paella high in calories")
add("/en/calorias/barra-de-pan/", "dish-info", 2, AC, "en", "calories in spanish bread")
add("/en/features/scan-food/", "app-download", 1, PAA, "en", "is there a free app that counts calories with a picture", "can i take a picture of my food and get a calorie count", "is there a free ai food scanner", "which ai food scanner is the best", "are ai food scanners accurate")
add("NEW:/en/comparativa/alternativas-myfitnesspal/", "list-compare", 2, PAA, "en", "is there a better free app than myfitnesspal")

# A.4 competitors (google.es / google.com top results, 9 Nov 2026)
COMP = {
    "contador de calorías": "labdeiters.com (nutricalculadora)|imss.gob.mx (calculadora)|play.google.com (MyFitnessPal)|tabladecalorias.net|apps.apple.com (Yazio)|ESN calculadora|yazio.com/es/contador-calorias|calor-ia.com",
    "app contar calorías gratis": "play.google.com|apps.apple.com|myfitnesspal.com/es|beyondtype1.org (5 apps)|yazio.com|nutriscan blog",
    "contar calorías con foto": "fitatu blog|play.google.com|calsy-app.com/es/food-calorie-scanner|apps.apple.com|reddit.com/r/loseit|calorix.ai|eatlog.app|xataka.com",
    "calculadora de calorías diarias": "imss.gob.mx|clinicamonleon (TMB)|fitgeneration (Harris-Benedict)|sanidad.gob.es|dokport|labdeiters|nxtlevel",
    "calculadora de déficit calórico": "enfaf|zavamed|imss.gob.mx|clinicassegura|dokport|omnicalculator.com|mdsaude|fitgeneration",
    "calculadora de imc": "texasheart|fundaciondelcorazon.com|hablandodeobesidad|quironsalud|cdc.gov (child)|seedo.es|nestlehealthscience|seen.es",
    "calculadora de macros": "hsnstore|nutricare|fitgeneration|alphasupplements|fatnessonline|escuelaculturismonatural",
    "calculadora de proteínas": "nxtlevel|dinamicprotein|nestlehealthscience|micron-app|nutren",
    "calculadora tmb": "clinicamonleon|zavamed|INS Perú|apollohospitals|davidrojas.es|omnicalculator.com",
    "cuánta agua beber al día": "mayoclinic.org (es)|segurcaixaadeslas|tuasaude (calculadora)|mspbs.gov.py|sanitas",
    "peso ideal según altura": "tuasaude.com|yazio.com (calculadora peso ideal)|seen.es|hablandodeobesidad|zavamed",
    "calorías para adelgazar mujer": "mdsaude.com|msdmanuals (tabla)|naturadika|imss.gob.mx|tuasaude|mayoclinic|esbeltic|atida",
    "cuántas calorías debo comer al día": "sanidad.gob.es|imss.gob.mx|msdmanuals|tuasaude|sendahealth|enfaf|qchara",
    "calorías paella": "tuarrocero|fatsecret.es|carmenai.org|nutrola|calzen.ai|tabaq.ai|thefork blog|fankal",
    "calorías tortilla de patatas": "fatsecret.es|directoalpaladar|centrosaludnutricional|instagram reel|consumer.es|nutriscan|cestaverde",
    "tabla de calorías de alimentos": "tabladecalorias.net|elmundo recetas|imss.gob.mx|myprotein|msdmanuals|sanidad.gob.es|labdeiters",
    "mejor app para contar calorías": "nalgene iberia (top 5)|play.google.com|beyondtype1|pccomponentes blog|fitia|apps.apple.com|reddit.com/r/askspain|applicantes",
    "alternativa a myfitnesspal": "wayoai|reddit|fitia.app|trainera.fit|calorix.ai (10 apps, 5,169 words)|mochi-zen|bodly|tu1plan",
    "cal ai opiniones": "reddit (×3)|caliro.dev|apps.apple.com|myclaw.ai|play.google.com|kibora.app",
    "yazio opiniones": "trustpilot|darwin-nutrition|apps.apple.com|play.google.com|reddit|xataka|nutrola",
    "escanear comida calorías": "nutriscan|yuka|play.google.com|scancal.app|openfoodfacts|platelens",
    "calorías croquetas jamón": "fatsecret.es|croquetasricas|lne.es|caliro.dev|menshealth|eatbetter|nutrola",
    "calorías lentejas estofadas": "fatsecret.es|elespanol|myprotein|yazio.com/alimentos|eatbetter|nutrola",
    "calorías huevo cocido": "institutohuevo|fatsecret.es|myprotein|yazio.com/alimentos",
    "calories in paella": "fatsecret|welling.ai|reddit|eatbetter.app|cleaneatingmag|paellafromvalencia|nutritionvalue",
    "calories in spanish omelette": "eatbetter.app|nutracheck",
    "cal ai alternative for android": "platelens|empirical.health|reddit|eesel.ai|amyfoodjournal|nutriscan|getkalohealth|nutrola",
    "myfitnesspal alternative": "reddit|eatthismuch blog|foodnoms|mavr.app|mynetdiary|nutriscan|eated.io",
    "photo calorie counter app": "play.google.com|apps.apple.com|wondershare|reddit|amyfoodjournal|bitepal.app",
}
DO_NOT_TARGET = {"apk", "niños", "embarazada", "orina", "creatinina", "premium gratis"}


def intent_of(r):
    k, fam, u = r["keyword"].lower(), r["family"], r.get("page_url") or r["target_url"]
    if "fotocal" in k and " vs " not in k and "o fotocal" not in k:
        return "brand"
    if fam == "dish":
        return "dish-info"
    if fam == "calculator" or "/calculadoras/" in u:
        return "tool"
    if "opiniones" in k or "review" in k or "es fiable" in k:
        return "review"
    if fam == "app" and any(w in k for w in ("mejor", "alternativ", " o ", " vs ", "precio", "gratis vs")):
        return "list-compare"
    if fam == "app":
        return "app-download"
    return "how-to"


def cluster_of(u, fam):
    p = re.sub(r"^NEW:", "", u).replace(SITE, "")
    p = p[3:] if p.startswith("/en/") else p
    for path, v in PAGES.items():
        if re.sub(r"^NEW:", "", path) == p:
            return v[3]
    if p.startswith("/calorias/"):
        return "dish"
    if p.startswith("/blog/"):
        return "guide"
    return fam or "app"


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    base = ["keyword", "lang", "family", "intent", "target_url", "target_status", "priority", "difficulty", "difficulty_note", "evidence"]
    new_cols = ["page_url", "primary_keyword", "secondary_keywords", "competitor_urls_ranking", "cluster", "source", "date_checked", "intent_2026_11_08"]
    already = "page_url" in rows[0]
    if not already:
        for r in rows:
            r["intent_2026_11_08"] = r["intent"]
            r["page_url"] = r["target_url"] if r["target_status"] == "existing" else "NEW:" + r["target_url"].replace(SITE, "")
            r["primary_keyword"] = "no"
            r["secondary_keywords"] = ""
            r["competitor_urls_ranking"] = ""
            r["source"] = "existing"
            r["date_checked"] = "2026-11-08"
    idx = {}
    merged = []
    for r in rows:   # accent / article variants already in the file → one row
        key = (r["lang"], norm(r["keyword"]))
        if key in idx:
            keep = idx[key]
            sec = [s for s in keep["secondary_keywords"].split("|") if s]
            if r["keyword"] not in sec and r["keyword"] != keep["keyword"]:
                sec.append(r["keyword"])
            keep["secondary_keywords"] = "|".join(sec)
            continue
        idx[key] = r
        merged.append(r)
    rows = merged

    def upsert(k, lang, path, intent, prio, src, force_url=False):
        key = (lang, norm(k))
        page = path if path.startswith("NEW:") else SITE + path   # EN paths already start with /en/
        if key in idx:
            r = idx[key]
            if r["keyword"] != k:
                sec = [s for s in r["secondary_keywords"].split("|") if s]
                if k not in sec:
                    sec.append(k)
                r["secondary_keywords"] = "|".join(sec)
            if src not in r["source"].split("|"):
                r["source"] = "|".join([s for s in r["source"].split("|") if s] + [src])
            r["date_checked"] = TODAY
            if force_url:
                r["page_url"] = page
            return r
        fam = "dish" if "/calorias/" in page else ("calculator" if "/calculadoras/" in page else ("guide" if "/blog/" in page or "/guias/" in page else "app"))
        tu = page.replace("NEW:", SITE) if page.startswith("NEW:") else page
        r = {"keyword": k, "lang": lang, "family": fam, "intent": intent, "target_url": tu,
             "target_status": "new" if page.startswith("NEW:") else "existing", "priority": str(prio),
             "difficulty": "", "difficulty_note": "not assessed (added from the 9 Nov research)", "evidence": EVID,
             "page_url": page, "primary_keyword": "no", "secondary_keywords": "", "competitor_urls_ranking": "",
             "source": src, "date_checked": TODAY, "intent_2026_11_08": ""}
        if any(w in k for w in DO_NOT_TARGET):
            return None
        idx[key] = r
        rows.append(r)
        return r

    for k, lang, path, intent, prio, src in A:
        upsert(k, lang, path, intent, prio, src)

    # primaries (B.1): the owner of a keyword wins its row
    primaries = []   # (path_es, primary_es, secs, primary_en, cluster)
    for path, (pes, secs, pen, cl) in PAGES.items():
        primaries.append((path, pes, secs, pen, cl))
    for slug, (pes, secs, pen) in BLOG.items():
        primaries.append(("/blog/%s/" % slug, pes, secs, pen, "guide"))
    dishes = json.load(open(os.path.join(ROOT, "tools", "dishes", "dishes.json"), encoding="utf-8"))["dishes"]
    gloss = json.load(open(os.path.join(ROOT, "tools", "dishes", "en.json"), encoding="utf-8"))["gloss"]
    for d in dishes:
        typed = "calorías " + d["name"]
        en = "calories in " + EN_DISH.get(d["slug"], gloss.get(d["slug"], d["name"]).lower())
        primaries.append(("/calorias/%s/" % d["slug"], typed, [typed + " por 100 g", typed + " por ración", "engorda " + d["name"], "proteínas " + d["name"]], en, "dish"))
    for path, pes, secs, pen, cl in primaries:
        enpath = "NEW:/en" + path[4:] if path.startswith("NEW:") else "/en" + path
        r = upsert(pes, "es", path, None, 1, "existing", force_url=True) if (("es", norm(pes)) in idx) else upsert(pes, "es", path, None, 1, "map", force_url=True)
        r["primary_keyword"] = "yes"
        r["secondary_keywords"] = "|".join(dict.fromkeys([s for s in r["secondary_keywords"].split("|") if s] + secs))
        r2 = upsert(pen, "en", enpath, None, 1, "map", force_url=True)
        r2["primary_keyword"] = "yes"
    for r in rows:
        if not r.get("intent") or r["intent"] in ("informational", "commercial"):
            r["intent"] = intent_of(r)
        elif r["intent"] == "tool" and r["family"] != "calculator" and "/calculadoras/" not in r["page_url"]:
            r["intent"] = intent_of(r)
        r["cluster"] = cluster_of(r["page_url"], r["family"])
        c = COMP.get(r["keyword"]) or COMP.get(next((k for k in COMP if norm(k) == norm(r["keyword"])), ""), "")
        if c:
            r["competitor_urls_ranking"] = c
            if "SERP" not in r["source"].split("|"):
                r["source"] += "|SERP"
            r["date_checked"] = TODAY
    with open(CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=base + new_cols)
        w.writeheader()
        w.writerows(rows)
    write_map(primaries)
    print("%d rows" % len(rows))


def write_map(primaries):
    L = ["# Keyword map: one primary keyword per URL (anti-cannibalisation)", "",
         "Source: MASTER PROMPT v3 §B.1, applied on 9 November 2026 by `tools/seo/keywords_v3_merge.py` (the same rows are marked `primary_keyword=yes` in `keywords.csv`).", "",
         "**The rule.** Before writing a title, an H1 or a new page, find its keyword here.",
         "- If the keyword is another URL's primary, don't use it: link to that URL instead, with its primary keyword as the anchor text.",
         "- A secondary may appear on other pages as a natural mention, never in another page's title or H1.", "",
         "Rows marked *provisional* (blog posts outside §B.1, and the English names of most dishes) are a Spanish or English search phrase for the page's topic. The rollout PARTs (6 for English dishes, 11–14 for blog posts) confirm or replace them; update this file and the CSV when they do.", "",
         "| URL (ES; the EN twin mirrors it under /en/) | Primary ES | Secondaries ES | Primary EN |", "|---|---|---|---|"]
    B1 = set(PAGES) | {"/blog/%s/" % s for s in list(BLOG)[:9]}
    for path, pes, secs, pen, cl in primaries:
        prov = "" if path in B1 else " *(provisional)*"
        if path.startswith("/calorias/") and path not in PAGES:
            slug = path.split("/")[2]
            prov = "" if slug in EN_DISH else " *(EN provisional, PART 6)*"
        shown = ("**new page:** `%s`" % path[4:]) if path.startswith("NEW:") else ("`%s`" % path)
        L.append("| %s | %s | %s | %s%s |" % (shown, pes, " · ".join(secs) or "—", pen, prov))
    L += ["", "`/metodologia/`, `/about/`, `/contact/`, `/faq/`, `/subscription/`, legal pages and `/widget/` are trust and utility pages: no keyword target, never use a money keyword in their title.", "",
          "**Dish pages.** The primary is the phrase people type (\"calorías paella\"). The title and H1 use the natural form (\"Calorías de la paella\"); it is the same query to Google. Variations (100 g, Mercadona, con cebolla, 3/4/6 huevos, por unidad) are sections of the page, never new URLs."]
    open(MAP, "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
