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
