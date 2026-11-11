# -*- coding: utf-8 -*-
"""Computed sections for the calculator pages (MASTER PROMPT v3, PART 4).

Each section answers a question people type (docs/seo/serp-notes.md,
keywords.csv source=PAA/autocomplete) with a table worked out here from the
same formulas as assets/js/calc.js, so the figures can never drift from
what the calculator itself returns:

  Mifflin-St Jeor   BMR = 10·kg + 6.25·cm − 5·age + 5 (men) / − 161 (women)
  activity          ×1.2  ×1.375  ×1.465  ×1.55  ×1.725
  1 kg of weight    7,700 kcal
  healthy range     BMI 18.5 to 24.9 (WHO), rounded to the kilo
  Harris-Benedict   revised by Roza and Shizgal (1984), shown for comparison

EXTRA[slug][lang] is appended after the page's own body; FAQ_EXTRA adds
questions to its FAQ (and so to its FAQPage JSON-LD, which is built from
the same list).
"""


def n(v, lang, dec=0):
    s = ("{:,.%df}" % dec).format(v)
    return s if lang == "en" else s.replace(",", "§").replace(".", ",").replace("§", ".")


def mifflin(sex, kg, cm, age):
    return 10 * kg + 6.25 * cm - 5 * age + (5 if sex == "m" else -161)


def harris(sex, kg, cm, age):   # Roza & Shizgal 1984
    return (88.362 + 13.397 * kg + 4.799 * cm - 5.677 * age) if sex == "m" else (447.593 + 9.247 * kg + 3.098 * cm - 4.330 * age)


def table(head, rows):
    return ('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr>%s</tr></thead><tbody>\n%s\n      </tbody></table></div>'
            % ("".join('<th scope="col">%s</th>' % h for h in head),
               "\n".join("        <tr>%s</tr>" % "".join(("<th scope=\"row\">%s</th>" if i == 0 else "<td>%s</td>") % c for i, c in enumerate(r)) for r in rows)))


W, M = ("f", 65, 165), ("m", 80, 178)     # the two example people of the tables
AGES = (25, 35, 45, 55, 65)
ACTS = {"es": [("Sentado casi todo el día", 1.2), ("De pie a ratos", 1.375), ("Casi siempre de pie", 1.465), ("En movimiento todo el día", 1.55), ("Trabajo físico duro", 1.725)],
        "en": [("Sitting most of the day", 1.2), ("On your feet sometimes", 1.375), ("Standing most of the day", 1.465), ("Moving all day", 1.55), ("Hard physical work", 1.725)]}


def daily(lang):
    es = lang == "es"
    rows = []
    for a in AGES:
        w, m = mifflin(*W, a), mifflin(*M, a)
        rows.append([("%d años" if es else "Age %d") % a, n(round(w * 1.2), lang), n(round(w * 1.375), lang), n(round(m * 1.2), lang), n(round(m * 1.375), lang)])
    ex_m, ex_h = mifflin("f", 70, 165, 35), harris("f", 70, 165, 35)
    if es:
        return "\n".join([
            '      <h2 id="no-engordar">¿Cuántas calorías debo comer al día para no engordar?</h2>',
            '      <p>Las de tu mantenimiento: lo que gastas. Comiendo eso, el peso se queda donde está. Depende de tu sexo, edad, altura, peso y de cómo es tu día, así que la tabla es solo una orientación para dos personas concretas: una mujer de 1,65 m y 65 kg y un hombre de 1,78 m y 80 kg. Son estimaciones con la fórmula de Mifflin-St Jeor; para tu cifra, usa la calculadora de arriba.</p>',
            table(["Edad", "Mujer, sentada", "Mujer, de pie a ratos", "Hombre, sentado", "Hombre, de pie a ratos"], rows),
            '      <p>En kcal al día. Cada diez años el gasto baja entre 60 y 70 kcal, con el mismo peso y la misma actividad. Si lo que buscas es perder peso, el siguiente paso es la <a href="../deficit-calorico/">calculadora de déficit calórico</a>; si quieres ver solo lo que gastas en reposo, la <a href="../tmb/">calculadora de TMB</a>.</p>',
            '      <h2 id="harris-benedict">¿Mifflin-St Jeor o Harris-Benedict?</h2>',
            '      <p>Son dos fórmulas para lo mismo, la tasa metabólica basal. La de Harris-Benedict es de 1919 y se revisó en 1984; la de Mifflin-St Jeor es de 1990 y es la que usa esta calculadora y la app. Para la mujer del ejemplo (35 años, 165 cm, 70 kg), Mifflin-St Jeor da %s kcal en reposo y Harris-Benedict revisada, %s: unas %s kcal más. La diferencia es pequeña, pero explica por qué dos calculadoras no siempre coinciden.</p>'
            % (n(round(ex_m), lang), n(round(ex_h), lang), n(round(ex_h) - round(ex_m), lang)),
        ])
    return "\n".join([
        '      <h2 id="maintain">How many calories should I eat a day to keep my weight?</h2>',
        '      <p>Your maintenance calories: what you burn. Eat that and your weight stays where it is. It depends on your sex, age, height, weight and what your day is like, so this table is only a guide for two specific people: a woman of 1.65 m and 65 kg and a man of 1.78 m and 80 kg. These are estimates from the Mifflin-St Jeor equation; for your own number, use the calculator above.</p>',
        table(["Age", "Woman, sitting", "Woman, on her feet sometimes", "Man, sitting", "Man, on his feet sometimes"], rows),
        '      <p>In kcal a day. Every ten years the daily burn drops by 60 to 70 kcal, at the same weight and activity. To lose weight, the next step is the <a href="../deficit-calorico/">calorie deficit calculator</a>; to see only what you burn at rest, the <a href="../tmb/">BMR calculator</a>.</p>',
        '      <h2 id="harris-benedict">Mifflin-St Jeor or Harris-Benedict?</h2>',
        '      <p>They are two equations for the same thing, basal metabolic rate. Harris-Benedict dates from 1919 and was revised in 1984; Mifflin-St Jeor is from 1990 and is the one this calculator and the app use. For the woman in the example (35 years, 165 cm, 70 kg), Mifflin-St Jeor gives %s kcal at rest and revised Harris-Benedict %s: about %s kcal more. The gap is small, but it explains why two calculators do not always agree.</p>'
        % (n(round(ex_m), lang), n(round(ex_h), lang), n(round(ex_h) - round(ex_m), lang)),
    ])


def deficit(lang):
    es = lang == "es"
    rows = []
    for pace, name in ((0.25, "Suave" if es else "Gentle"), (0.5, "Recomendado" if es else "Recommended"), (0.75, "Rápido" if es else "Fast")):
        kcal = pace * 7700 / 7
        rows.append([name, ("%s kg por semana" if es else "%s kg a week") % n(pace, lang, 2), n(round(kcal), lang), ("%s días" if es else "%s days") % n(round(7 / pace), lang)])
    if es:
        return "\n".join([
            '      <h2 id="perder-1-kg">¿Cuánto déficit calórico hace falta para perder 1 kg?</h2>',
            '      <p>Unas 7.700 kcal en total. No se hacen en un día: se reparten. Cuanto mayor es el déficit diario, antes llega el kilo, pero más cuesta sostenerlo. Estos son los tres ritmos de la calculadora:</p>',
            table(["Ritmo", "Pérdida", "Déficit al día (kcal)", "Tiempo para perder 1 kg"], rows),
            '      <p>Perder 1 kilo por semana pediría unas 1.100 kcal menos al día. Para casi todo el mundo eso es más de la cuarta parte de lo que gasta, así que la calculadora no lo propone: se queda en el límite del 25 % y nunca baja de 1.200 kcal en la mujer ni de 1.500 en el hombre. Qué comer con ese déficit, plato por plato, está en <a href="../../blog/deficit-500-calorias-dia/">la guía del déficit de 500 calorías</a>, y el porqué, en <a href="../../blog/calorie-deficit-for-fat-loss/">qué es el déficit calórico y cómo hacerlo</a>.</p>',
        ])
    return "\n".join([
        '      <h2 id="lose-1-kg">How big a calorie deficit do you need to lose 1 kg?</h2>',
        '      <p>About 7,700 kcal in total. Not in a day: you spread it out. The bigger the daily deficit, the sooner the kilo goes, and the harder it is to keep up. These are the calculator\'s three paces:</p>',
        table(["Pace", "Loss", "Daily deficit (kcal)", "Time to lose 1 kg"], rows),
        '      <p>Losing 1 kilo a week would take about 1,100 kcal less a day. For almost everyone that is more than a quarter of what they burn, so the calculator does not offer it: it stops at the 25% limit and never goes below 1,200 kcal for women or 1,500 for men. What to eat on that deficit, dish by dish, is in <a href="../../blog/deficit-500-calorias-dia/">the 500-calorie deficit guide</a>, and the reasoning in <a href="../../blog/calorie-deficit-for-fat-loss/">the calorie deficit explained</a>.</p>',
    ])


def bmr(lang):
    es = lang == "es"
    w, m = mifflin("f", 70, 165, 35), mifflin("m", 85, 178, 35)
    rows = [[name, "× " + n(f, lang, 3).rstrip("0").rstrip(",."), n(round(w * f), lang), n(round(m * f), lang)] for name, f in ACTS[lang]]
    if es:
        return "\n".join([
            '      <h2 id="tmb-get">TMB y GET: cuál es la diferencia</h2>',
            '      <p>La TMB (tasa metabólica basal) es lo que gastas en reposo total. El GET (gasto energético total, TDEE en inglés) es lo que gastas en un día de verdad: la TMB multiplicada por un factor según cómo te mueves. La calculadora te da las dos cifras. Para las dos personas del ejemplo, con una TMB de %s kcal (mujer, 35 años, 165 cm, 70 kg) y %s kcal (hombre, 35 años, 178 cm, 85 kg):</p>' % (n(round(w), lang), n(round(m), lang)),
            table(["Tu día", "Factor", "GET mujer (kcal)", "GET hombre (kcal)"], rows),
            '      <p>El GET es tu mantenimiento: la cifra contra la que se mide un déficit. Si quieres afinarlo con tu objetivo, sigue en la <a href="../calorias-diarias/">calculadora de calorías diarias</a>.</p>',
            '      <h2 id="mujer-hombre">TMB en la mujer y en el hombre</h2>',
            '      <p>La fórmula es la misma salvo el último término: +5 en el hombre y −161 en la mujer. A igual edad, altura y peso, la TMB de una mujer sale 166 kcal más baja, porque de media tiene menos masa muscular. Si conoces tu porcentaje de grasa, la fórmula de Katch-McArdle parte de tu masa magra y ya no necesita el sexo.</p>',
        ])
    return "\n".join([
        '      <h2 id="bmr-tdee">BMR and TDEE: what is the difference?</h2>',
        '      <p>BMR (basal metabolic rate) is what you burn at complete rest. TDEE (total daily energy expenditure) is what you burn on a real day: BMR times a factor for how you move. The calculator gives you both. For the two people in the example, with a BMR of %s kcal (woman, 35 years, 165 cm, 70 kg) and %s kcal (man, 35 years, 178 cm, 85 kg):</p>' % (n(round(w), lang), n(round(m), lang)),
        table(["Your day", "Factor", "TDEE, woman (kcal)", "TDEE, man (kcal)"], rows),
        '      <p>TDEE is your maintenance: the number a deficit is measured against. To set it against your goal, carry on to the <a href="../calorias-diarias/">daily calorie calculator</a>.</p>',
        '      <h2 id="women-men">BMR for women and for men</h2>',
        '      <p>The equation is the same except for the last term: +5 for men and −161 for women. At the same age, height and weight, a woman\'s BMR comes out 166 kcal lower, because on average she carries less muscle. If you know your body fat percentage, the Katch-McArdle equation starts from lean mass and no longer needs your sex.</p>',
    ])


def ideal(lang):
    es = lang == "es"
    rows = []
    for cm in range(150, 200, 5):
        h = cm / 100.0
        lo, hi = round(18.5 * h * h), round(24.9 * h * h)
        rows.append([n(h, lang, 2) + " m", ("%d a %d kg" if es else "%d to %d kg") % (lo, hi), "%d kg" % round(21.7 * h * h)])
    if es:
        return "\n".join([
            '      <h2 id="tabla">Tabla de peso ideal según la altura</h2>',
            '      <p>El peso que da un IMC de 18,5 a 24,9, de 1,50 a 1,95 m. La tercera columna es el centro del rango (IMC 21,7), por si buscas una sola cifra de referencia: no es un objetivo.</p>',
            table(["Altura", "Rango de peso saludable", "Centro del rango"], rows),
            '      <h2 id="mujer-hombre">Peso ideal en la mujer y en el hombre</h2>',
            '      <p>La OMS usa el mismo rango de IMC para mujeres y hombres adultos, así que la tabla vale para los dos. Lo que cambia es dónde suele caer cada uno dentro del rango: a igual altura, un hombre tiene de media más masa muscular y pesa más con la misma grasa. Por eso una mujer de 1,65 m suele estar bien en la mitad baja de su rango (de 50 a 68 kg) y un hombre de 1,80 m, en la mitad alta del suyo (de 60 a 81 kg).</p>',
            '      <h2 id="edad">¿Cambia el peso ideal con la edad?</h2>',
            '      <p>El rango de la OMS es para adultos de cualquier edad. No sirve para menores de 18 años, que se valoran con tablas de crecimiento por edad y sexo, ni durante el embarazo. A partir de los 65, muchos geriatras prefieren un IMC algo más alto; consúltalo con tu médico.</p>',
        ])
    return "\n".join([
        '      <h2 id="chart">Ideal weight by height chart</h2>',
        '      <p>The weight that gives a BMI of 18.5 to 24.9, from 1.50 to 1.95 m. The third column is the middle of the range (BMI 21.7), in case you want a single reference figure: it is not a target.</p>',
        table(["Height", "Healthy weight range", "Middle of the range"], rows),
        '      <h2 id="women-men">Ideal weight for women and for men</h2>',
        '      <p>The WHO uses the same BMI range for adult women and men, so the chart works for both. What differs is where each tends to sit inside the range: at the same height, a man carries more muscle on average and weighs more at the same body fat. That is why a woman of 1.65 m is often comfortable in the lower half of her range (50 to 68 kg) and a man of 1.80 m in the upper half of his (60 to 81 kg).</p>',
        '      <h2 id="age">Does ideal weight change with age?</h2>',
        '      <p>The WHO range is for adults of any age. It does not apply to under-18s, who are assessed with growth charts by age and sex, or during pregnancy. From 65 on, many geriatricians prefer a slightly higher BMI; ask your doctor.</p>',
    ])


EXTRA = {"calorias-diarias": {l: daily(l) for l in ("es", "en")},
         "deficit-calorico": {l: deficit(l) for l in ("es", "en")},
         "tmb": {l: bmr(l) for l in ("es", "en")},
         "peso-saludable": {l: ideal(l) for l in ("es", "en")}}

FAQ_EXTRA = {
    "calorias-diarias": {
        "es": [("¿Cuántas calorías gasto al día en reposo?", "Es tu tasa metabólica basal: entre el 58 y el 83 % de lo que gastas en un día, según cuánto te muevas. La mujer del ejemplo gasta 1.395 kcal en reposo y 1.918 en total. La <a href=\"../tmb/\">calculadora de TMB</a> te da la tuya.")],
        "en": [("How many calories do I burn a day at rest?", "That is your basal metabolic rate: 58 to 83% of what you burn in a day, depending on how much you move. The woman in the example burns 1,395 kcal at rest and 1,918 in total. The <a href=\"../tmb/\">BMR calculator</a> gives you yours.")]},
    "deficit-calorico": {
        "es": [("¿Cómo calcular el déficit calórico según mi peso?", "Primero tu mantenimiento, que depende de tu peso, altura, edad, sexo y actividad. Después se resta el déficit: entre el 0,5 % y el 1 % de tu peso a la semana es un ritmo sensato. Con 80 kg, eso son de 0,4 a 0,8 kg semanales.")],
        "en": [("How do I work out my calorie deficit for my weight?", "First your maintenance, which depends on your weight, height, age, sex and activity. Then subtract the deficit: 0.5% to 1% of your weight a week is a sensible pace. At 80 kg, that is 0.4 to 0.8 kg a week.")]},
}


# ── PART 5: IMC, macros, proteínas, agua ─────────────────────────────
# Ports of calc.js plan()/macros()/water() for the cases the tables use
# (maintain / lose 0.5 kg a week / build muscle, balanced split, no body
# fat given). tools/calcs/check_extra.mjs compares them with calc.js.
FACTOR = {"sedentary": 1.2, "light": 1.375, "standing": 1.465, "active": 1.55, "hard": 1.725}
WATER_RATIO = {"sedentary": 1.0, "light": 1.1, "standing": 1.1, "active": 1.25, "hard": 1.5}
P_PER_KG = {"lose": 2.0, "maintain": 1.6, "build_muscle": 2.0}
FAT_PCT = {"lose": 0.25, "maintain": 0.275, "build_muscle": 0.25}


def jsround(x):
    import math
    return int(math.floor(x + 0.5))


def plan(sex, age, cm, kg, activity, goal):
    tdee = mifflin(sex, kg, cm, age) * FACTOR[activity]
    daily = tdee - min(0.5 * 7700 / 7, tdee * 0.25) if goal == "lose" else (tdee * 1.1 if goal == "build_muscle" else tdee)
    kcal = jsround(max(daily, 1500 if sex == "m" else 1200))
    hm = cm / 100.0
    ref = 25 * hm * hm if kg / (hm * hm) > 25 else kg
    p = jsround(P_PER_KG[goal] * ref)
    f = jsround(FAT_PCT[goal] * kcal / 9)
    c = jsround((kcal - 4 * p - 9 * f) / 4)
    return {"kcal": kcal, "protein": p, "fat": f, "carbs": c}


def water_ml(sex, age, cm, kg, activity):
    kcal = plan(sex, age, cm, kg, activity, "maintain")["kcal"]
    floor = jsround((2500 if sex == "m" else 2000) * 0.8)
    return jsround(max(min(kcal * WATER_RATIO[activity] * 0.8, 4000), floor))


def bmi(lang):
    es = lang == "es"
    rows = []
    for cm in range(150, 200, 5):
        h2 = (cm / 100.0) ** 2
        rows.append([n(cm / 100.0, lang, 2) + " m", ("%d a %d kg" if es else "%d to %d kg") % (round(18.5 * h2), round(24.9 * h2)),
                     ("desde %d kg" if es else "from %d kg") % jsround(25 * h2 + 0.5), ("desde %d kg" if es else "from %d kg") % jsround(30 * h2 + 0.5)])
    if es:
        return "\n".join([
            '      <h2 id="tabla-imc">Tabla de IMC por altura</h2>',
            '      <p>Los kilos que corresponden a cada rango de la OMS según tu altura, para adultos. Busca tu altura y mira en qué columna cae tu peso.</p>',
            table(["Altura", "Peso normal (IMC 18,5 a 24,9)", "Sobrepeso (IMC 25)", "Obesidad (IMC 30)"], rows),
            '      <h2 id="mujer-hombre">IMC en la mujer y en el hombre</h2>',
            '      <p>La fórmula y los rangos de la OMS son los mismos para mujeres y hombres adultos. Lo que cambia es lo que hay detrás de la cifra: con el mismo IMC, una mujer tiene de media más grasa corporal que un hombre, y un hombre con mucho músculo puede salir en sobrepeso sin que le sobre grasa. Por eso el IMC orienta y no diagnostica.</p>',
            '      <h2 id="edad">¿Cambia el IMC con la edad?</h2>',
            '      <p>La cuenta no cambia; lo que cambia es cómo se lee. Entre los 18 y los 65 años se usan los rangos de la tabla. En menores de 18 no sirven: se valoran con percentiles por edad y sexo, y eso lo hace el pediatra. A partir de los 65, un IMC algo más alto puede ser adecuado; consúltalo con tu médico. Tampoco se aplica durante el embarazo.</p>',
        ])
    return "\n".join([
        '      <h2 id="bmi-chart">BMI chart by height</h2>',
        '      <p>The kilos that match each WHO band for your height, for adults. Find your height and see which column your weight falls in.</p>',
        table(["Height", "Normal weight (BMI 18.5 to 24.9)", "Overweight (BMI 25)", "Obesity (BMI 30)"], rows),
        '      <h2 id="women-men">BMI for women and for men</h2>',
        '      <p>The formula and the WHO bands are the same for adult women and men. What differs is what sits behind the number: at the same BMI a woman carries more body fat on average than a man, and a muscular man can land in the overweight band without excess fat. That is why BMI is a guide, not a diagnosis.</p>',
        '      <h2 id="age">Does BMI change with age?</h2>',
        '      <p>The sum does not change; how you read it does. From 18 to 65 the bands in the chart apply. Under 18 they do not: children are assessed with percentiles by age and sex, which is a paediatrician\'s job. From 65 on, a slightly higher BMI can be appropriate; ask your doctor. It does not apply during pregnancy either.</p>',
    ])


def protein(lang):
    es = lang == "es"
    rows = [["%d kg" % kg, "%d g" % jsround(0.83 * kg), "%d g" % jsround(1.6 * kg), "%d g" % jsround(2.0 * kg)] for kg in range(50, 100, 10)]
    if es:
        return "\n".join([
            '      <h2 id="por-kilo">¿Cuántas proteínas por kilo de peso necesito al día?</h2>',
            '      <p>Depende de tu objetivo. El mínimo para un adulto sano son 0,83 g por kilo (EFSA). Para mantenerte, la calculadora usa 1,6 g por kilo, y para perder grasa o ganar músculo, 2,0 g por kilo. En gramos al día:</p>',
            table(["Tu peso", "Mínimo (0,83 g/kg)", "Mantener (1,6 g/kg)", "Perder grasa o ganar músculo (2,0 g/kg)"], rows),
            '      <p>La tabla vale si tu IMC es de 25 o menos. Con sobrepeso, la calculadora no usa tu peso total sino el que tendrías con un IMC de 25, para no inflar la cifra. Para repartir esos gramos junto con la grasa y los hidratos, sigue en la <a href="../macros/">calculadora de macros</a>.</p>',
        ])
    return "\n".join([
        '      <h2 id="per-kilo">How much protein per kilo of body weight do I need a day?</h2>',
        '      <p>It depends on your goal. The minimum for a healthy adult is 0.83 g per kilo (EFSA). To maintain, the calculator uses 1.6 g per kilo, and to lose fat or build muscle, 2.0 g per kilo. In grams a day:</p>',
        table(["Your weight", "Minimum (0.83 g/kg)", "Maintain (1.6 g/kg)", "Lose fat or build muscle (2.0 g/kg)"], rows),
        '      <p>The table holds if your BMI is 25 or under. If you are overweight, the calculator does not use your total weight but the weight you would have at a BMI of 25, so the figure is not inflated. To split those grams alongside fat and carbs, carry on to the <a href="../macros/">macro calculator</a>.</p>',
    ])


def macro(lang):
    es = lang == "es"
    names = {"lose": ("Perder grasa (0,5 kg por semana)", "Lose fat (0.5 kg a week)"), "maintain": ("Mantener", "Maintain"), "build_muscle": ("Ganar músculo", "Build muscle")}
    rows = []
    for g in ("lose", "maintain", "build_muscle"):
        p = plan("f", 35, 165, 70, "light", g)
        rows.append([names[g][0 if es else 1], n(p["kcal"], lang), "%d g" % p["protein"], "%d g" % p["fat"], "%d g" % p["carbs"]])
    if es:
        return "\n".join([
            '      <h2 id="objetivo">Macros para perder grasa, mantener o ganar músculo</h2>',
            '      <p>El reparto cambia con el objetivo. Para la misma persona (mujer, 35 años, 165 cm, 70 kg, de pie a ratos), esto es lo que da la calculadora, con calorías y macros a la vez:</p>',
            table(["Objetivo", "Calorías al día", "Proteínas", "Grasas", "Hidratos"], rows),
            '      <p>Para perder grasa sube la proteína (2,0 g por kilo) y baja el total de calorías; los hidratos son lo que queda. Las calorías salen de la <a href="../calorias-diarias/">calculadora de calorías diarias</a> y del <a href="../deficit-calorico/">déficit calórico</a>; si ya tienes tu cifra, escríbela arriba.</p>',
        ])
    return "\n".join([
        '      <h2 id="goal">Macros to lose fat, maintain or build muscle</h2>',
        '      <p>The split changes with the goal. For the same person (woman, 35 years, 165 cm, 70 kg, on her feet sometimes), this is what the calculator gives, calories and macros together:</p>',
        table(["Goal", "Calories a day", "Protein", "Fat", "Carbs"], rows),
        '      <p>To lose fat, protein goes up (2.0 g per kilo) and total calories come down; carbs are what is left. The calories come from the <a href="../calorias-diarias/">daily calorie calculator</a> and the <a href="../deficit-calorico/">calorie deficit</a>; if you already have your number, type it in above.</p>',
    ])


def water(lang):
    es = lang == "es"
    rows = []
    for kg in range(50, 110, 10):
        w, m = water_ml("f", 35, 165, kg, "light"), water_ml("m", 35, 178, kg, "light")
        rows.append(["%d kg" % kg, ("%s litros" if es else "%s litres") % n(w / 1000.0, lang, 1), ("%s litros" if es else "%s litres") % n(m / 1000.0, lang, 1)])
    w70, m70 = water_ml("f", 35, 165, 70, "light"), water_ml("m", 35, 178, 70, "light")
    if es:
        return "\n".join([
            '      <h2 id="segun-peso">¿Cuánta agua beber al día según tu peso?</h2>',
            '      <p>Cuanto más pesas, más gastas y más agua necesitas. La tabla es para una mujer de 1,65 m y un hombre de 1,78 m, de 35 años y de pie a ratos. Son litros de bebida al día, sin contar el agua de la comida:</p>',
            table(["Tu peso", "Mujer", "Hombre"], rows),
            '      <p>Si pesas 70 kilos, eso son unos %s litros si eres mujer y %s si eres hombre: entre %d y %d vasos de 250 ml. En los pesos bajos la cifra no baja del mínimo de la EFSA (1,6 litros en la mujer y 2 en el hombre). Con calor o ejercicio intenso necesitas más; elige una actividad mayor en la calculadora.</p>'
            % (n(w70 / 1000.0, lang, 1), n(m70 / 1000.0, lang, 1), -(-w70 // 250), -(-m70 // 250)),
        ])
    return "\n".join([
        '      <h2 id="by-weight">How much water to drink a day for your weight</h2>',
        '      <p>The more you weigh, the more you burn and the more water you need. The table is for a woman of 1.65 m and a man of 1.78 m, aged 35 and on their feet sometimes. These are litres of drink a day, not counting the water in food:</p>',
        table(["Your weight", "Woman", "Man"], rows),
        '      <p>At 70 kilos, that is about %s litres for a woman and %s for a man: %d to %d glasses of 250 ml. At lower weights the figure never drops below the EFSA minimum (1.6 litres for women, 2 for men). In heat or with hard exercise you need more; pick a higher activity level in the calculator.</p>'
        % (n(w70 / 1000.0, lang, 1), n(m70 / 1000.0, lang, 1), -(-w70 // 250), -(-m70 // 250)),
    ])


EXTRA.update({"imc": {l: bmi(l) for l in ("es", "en")}, "proteinas": {l: protein(l) for l in ("es", "en")},
              "macros": {l: macro(l) for l in ("es", "en")}, "agua": {l: water(l) for l in ("es", "en")}})
