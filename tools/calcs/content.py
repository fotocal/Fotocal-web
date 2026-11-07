# -*- coding: utf-8 -*-
"""Copy for the eight calculators, Spanish and English (tools/gen_calcs.py).

Every number in a worked example was produced by assets/js/calc.js, which
runs the app's own formulas (fotocal/Fotocal src/logic/plan.ts and
src/lib/water.ts; checked against them on 20,000 random profiles on
2026-11-07). If a formula changes in the app, change calc.js, re-run
tools/check_calcs.mjs and re-read these examples.

Links are written relative to /calculadoras/<slug>/. The build keeps links
to the Spanish-only dish pages on the Spanish URL in the English tree."""

SOURCES = {
    "mifflin": {"es": 'Mifflin MD, St Jeor ST y cols. «A new predictive equation for resting energy expenditure in healthy individuals». <em>Am J Clin Nutr</em> 1990; 51(2): 241-247.',
                "en": 'Mifflin MD, St Jeor ST et al. "A new predictive equation for resting energy expenditure in healthy individuals". <em>Am J Clin Nutr</em> 1990; 51(2): 241-247.'},
    "who_bmi": {"es": 'Organización Mundial de la Salud. <em>Obesidad y sobrepeso</em>, nota descriptiva, y clasificación del IMC para adultos.',
                "en": 'World Health Organization. <em>Obesity and overweight</em>, fact sheet, and the adult BMI classification.'},
    "efsa_protein": {"es": 'EFSA, Panel NDA. «Scientific Opinion on Dietary Reference Values for protein». <em>EFSA Journal</em> 2012; 10(2): 2557 (0,83 g/kg al día para adultos).',
                     "en": 'EFSA NDA Panel. "Scientific Opinion on Dietary Reference Values for protein". <em>EFSA Journal</em> 2012; 10(2): 2557 (0.83 g/kg a day for adults).'},
    "issn_protein": {"es": 'Jäger R y cols. «International Society of Sports Nutrition Position Stand: protein and exercise». <em>J Int Soc Sports Nutr</em> 2017; 14: 20 (1,4-2,0 g/kg en personas que entrenan).',
                     "en": 'Jäger R et al. "International Society of Sports Nutrition Position Stand: protein and exercise". <em>J Int Soc Sports Nutr</em> 2017; 14: 20 (1.4-2.0 g/kg for people who train).'},
    "efsa_water": {"es": 'EFSA, Panel NDA. «Scientific Opinion on Dietary Reference Values for water». <em>EFSA Journal</em> 2010; 8(3): 1459 (2,0 L al día mujeres, 2,5 L hombres, agua total).',
                   "en": 'EFSA NDA Panel. "Scientific Opinion on Dietary Reference Values for water". <em>EFSA Journal</em> 2010; 8(3): 1459 (2.0 L a day for women, 2.5 L for men, total water).'},
    "iom_water": {"es": 'Institute of Medicine. <em>Dietary Reference Intakes for Water, Potassium, Sodium, Chloride and Sulfate</em>, 2005 (1,0 a 1,5 ml de agua por kcal gastada).',
                  "en": 'Institute of Medicine. <em>Dietary Reference Intakes for Water, Potassium, Sodium, Chloride and Sulfate</em>, 2005 (1.0 to 1.5 ml of water per kcal spent).'},
    "efsa_fat": {"es": 'EFSA, Panel NDA. «Scientific Opinion on Dietary Reference Values for fats». <em>EFSA Journal</em> 2010; 8(3): 1461 (grasa: 20-35 % de la energía).',
                 "en": 'EFSA NDA Panel. "Scientific Opinion on Dietary Reference Values for fats". <em>EFSA Journal</em> 2010; 8(3): 1461 (fat: 20-35% of energy).'},
    "katch": {"es": 'Katch-McArdle: TMB = 370 + 21,6 × masa magra (kg). McArdle WD, Katch FI, Katch VL. <em>Exercise Physiology</em>.',
              "en": 'Katch-McArdle: BMR = 370 + 21.6 × lean mass (kg). McArdle WD, Katch FI, Katch VL. <em>Exercise Physiology</em>.'},
    "wishnofsky": {"es": 'Wishnofsky M. «Caloric equivalents of gained or lost weight». <em>Am J Clin Nutr</em> 1958; 6(5): 542-546 (unas 7.700 kcal por kilo).',
                   "en": 'Wishnofsky M. "Caloric equivalents of gained or lost weight". <em>Am J Clin Nutr</em> 1958; 6(5): 542-546 (about 7,700 kcal per kilo).'},
}

ACT_ROWS = {
    "es": [("sedentary", "Casi siempre sentado", "1,2"), ("light", "De pie a ratos", "1,375"), ("standing", "Casi siempre de pie", "1,465"),
           ("active", "En movimiento todo el día", "1,55"), ("hard", "Trabajo físico duro", "1,725")],
    "en": [("sedentary", "Mostly sitting", "1.2"), ("light", "On my feet sometimes", "1.375"), ("standing", "Mostly standing", "1.465"),
           ("active", "Moving all day", "1.55"), ("hard", "Hard physical work", "1.725")],
}

CALCS = [
# ───────────────────────────────────────────────────────────── calorías diarias
{"slug": "calorias-diarias", "kind": "tdee", "icon": "flame",
 "dishes": ["tortilla-de-patatas", "paella-valenciana", "lentejas-estofadas", "cafe-con-leche"],
 "blog": ["tdee-how-many-calories-you-need", "understanding-your-basal-metabolic-rate", "how-many-calories-does-exercise-burn"],
 "sources": ["mifflin", "wishnofsky"],
 "es": {
  "short": "Calorías diarias", "card": "Tu mantenimiento y las cifras para perder o ganar peso despacio.",
  "title": "Calculadora de calorías diarias (Mifflin-St Jeor)",
  "desc": "Calcula cuántas calorías necesitas al día para mantener, perder o ganar peso, con la fórmula de Mifflin-St Jeor y la misma cuenta que la app Fotocal.",
  "h1": "Calculadora de calorías diarias",
  "lead": "Cuántas calorías gastas al día y cuántas comer para perder o ganar peso despacio. Gratis, en la página y sin enviar tus datos.",
  "bridge": "¿Quieres cumplir tus {X} kcal sin pesar comida?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <p>En dos pasos. Primero la tasa metabólica basal (TMB), lo que gastas en reposo, con la ecuación de Mifflin-St Jeor (1990), la que mejor acierta en adultos sanos según las revisiones de dietética:</p>
      <div class="calc-formula"><code>TMB = 10 × kg + 6,25 × cm − 5 × años + 5 (hombre) / − 161 (mujer)</code></div>
      <p>Después se multiplica por un factor según cómo es tu día a día, sin contar el ejercicio: 1,2 si pasas el día sentado, 1,375 si estás de pie a ratos, 1,465 si casi siempre de pie, 1,55 si te mueves todo el día y 1,725 con trabajo físico duro. El resultado es tu mantenimiento, el gasto diario total o TDEE.</p>
      <p>Para perder peso, la calculadora resta lo que corresponde a 0,25 o 0,5 kg por semana (7.700 kcal por kilo, repartidas en 7 días), pero nunca más del 25 % de tu mantenimiento, y nunca te deja por debajo de 1.200 kcal si eres mujer o 1.500 si eres hombre. Son las mismas reglas que usa la app Fotocal, así que el número de aquí es el que verás allí.</p>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Una mujer de 35 años, 165 cm y 70 kg que está de pie a ratos: TMB = 700 + 1.031,25 − 175 − 161 = 1.395 kcal. Por 1,375 da un mantenimiento de 1.918 kcal. Para perder medio kilo a la semana harían falta 550 kcal menos, pero eso pasa del 25 % de su gasto, así que el recorte se queda en 480: su objetivo son 1.438 kcal. Para perder un cuarto de kilo, 1.643 kcal.</p>
      <p>Un hombre de 35 años, 178 cm y 85 kg que se mueve todo el día gasta unas 2.778 kcal; con 550 menos, 2.228 kcal al día, pierde medio kilo por semana.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>Tómalo como punto de partida, no como verdad: el error de cualquier fórmula ronda el 10 % en una persona concreta. Come durante dos o tres semanas lo que te sale, apuntándolo todo, y mira la media semanal de la báscula. Si no se mueve y querías perder, recorta 100 o 200 kcal más; si bajas más rápido del 1 % de tu peso a la semana, come algo más. Para repartir esa cifra en proteínas, grasas e hidratos, usa la <a href="../macros/">calculadora de macros</a>; para saber cuánto tarda, la de <a href="../deficit-calorico/">déficit calórico</a>.</p>
      <p>Y para saber cuánto comes de verdad, ayuda tener a mano las calorías de lo que se come aquí: una <a href="../../calorias/tortilla-de-patatas/">ración de tortilla de patatas</a>, un <a href="../../calorias/paella-valenciana/">plato de paella</a>, unas <a href="../../calorias/lentejas-estofadas/">lentejas estofadas</a> o el <a href="../../calorias/cafe-con-leche/">café con leche</a> de cada mañana.</p>""",
  "faq": [
   ("¿Cuántas calorías debo comer al día para adelgazar?", "Las de tu mantenimiento menos un recorte moderado: lo que corresponde a un cuarto o medio kilo por semana, sin pasar del 25 % de tu gasto. La calculadora te da las dos cifras. Si te sale por debajo de 1.200 kcal (mujer) o 1.500 (hombre), no bajes más sin un profesional sanitario: baja el ritmo."),
   ("¿Es lo mismo que el TDEE?", "Sí. TDEE son las siglas en inglés de gasto energético diario total: lo que gastas en un día contando el metabolismo basal, la digestión y todo lo que te mueves. Aquí lo llamamos mantenimiento, porque es la cifra con la que ni pierdes ni ganas peso."),
   ("¿Por qué me sale distinto que en otra calculadora?", "Porque usan otra fórmula (Harris-Benedict suele dar más) u otros factores de actividad. Ninguna acierta tu cifra exacta: el error típico a nivel individual ronda el 10 %. Toma el resultado como punto de partida y ajústalo con la báscula a las dos o tres semanas."),
   ("¿Cuento el ejercicio dentro de la actividad?", "No. El factor describe tu día a día: trabajo, desplazamientos, tareas. El ejercicio se suma aparte el día que lo haces, que es como lo hace la app. Si lo metes en los dos sitios, lo cuentas dos veces."),
   ("¿Da el mismo número que la app Fotocal?", "Sí, para los mismos datos. Usa las mismas fórmulas y los mismos límites: el factor de actividad, el tope del 25 % y los suelos de 1.200 y 1.500 kcal. En la app puedes además fijar un peso objetivo y una fecha."),
  ]},
 "en": {
  "short": "Daily calories", "card": "Your maintenance, and the numbers to lose or gain weight slowly.",
  "title": "Daily calorie calculator (Mifflin-St Jeor)",
  "desc": "Work out how many calories you need a day to maintain, lose or gain weight, with the Mifflin-St Jeor equation and the same maths as the Fotocal app.",
  "h1": "Daily calorie calculator",
  "lead": "How many calories you burn a day, and how many to eat to lose or gain weight slowly. Free, in the page, nothing sent anywhere.",
  "bridge": "Want to hit your {X} kcal without weighing food?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <p>In two steps. First the basal metabolic rate (BMR), what you burn at rest, with the Mifflin-St Jeor equation (1990), the one dietetics reviews find most accurate for healthy adults:</p>
      <div class="calc-formula"><code>BMR = 10 × kg + 6.25 × cm − 5 × age + 5 (man) / − 161 (woman)</code></div>
      <p>Then it is multiplied by a factor for your day-to-day, not counting workouts: 1.2 if you sit most of the day, 1.375 if you are on your feet sometimes, 1.465 if mostly standing, 1.55 if you move all day and 1.725 for hard physical work. The result is your maintenance, your total daily energy expenditure or TDEE.</p>
      <p>To lose weight, the calculator takes off what 0.25 or 0.5 kg a week takes (7,700 kcal per kilo, spread over 7 days), but never more than 25% of your maintenance, and it never goes below 1,200 kcal for a woman or 1,500 for a man. These are the rules the Fotocal app uses, so the number here is the one you will see there.</p>
      <h2 id="example">A worked example</h2>
      <p>A 35-year-old woman, 165 cm and 70 kg, on her feet sometimes: BMR = 700 + 1,031.25 − 175 − 161 = 1,395 kcal. Times 1.375 gives a maintenance of 1,918 kcal. Losing half a kilo a week would need 550 kcal less, but that is more than 25% of what she burns, so the cut stays at 480: her target is 1,438 kcal. For a quarter of a kilo, 1,643 kcal.</p>
      <p>A 35-year-old man, 178 cm and 85 kg, who moves all day burns about 2,778 kcal; with 550 less, 2,228 kcal a day, he loses half a kilo a week.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>Treat it as a starting point, not the truth: any formula is off by around 10% for a given person. Eat what it gives you for two or three weeks, logging everything, and watch your weekly average on the scale. If it does not move and you wanted to lose, cut 100 or 200 kcal more; if you lose faster than 1% of your weight a week, eat a little more. To split the number into protein, fat and carbs, use the <a href="../macros/">macro calculator</a>; to see how long it takes, the <a href="../deficit-calorico/">calorie deficit calculator</a>.</p>
      <p>To know what you really eat, it helps to know the calories of everyday Spanish food: a <a href="../../calorias/tortilla-de-patatas/">serving of tortilla de patatas</a>, a <a href="../../calorias/paella-valenciana/">plate of paella</a>, <a href="../../calorias/lentejas-estofadas/">lentil stew</a> or a morning <a href="../../calorias/cafe-con-leche/">café con leche</a> (those pages are in Spanish).</p>""",
  "faq": [
   ("How many calories should I eat a day to lose weight?", "Your maintenance minus a moderate cut: what a quarter or half a kilo a week takes, never more than 25% of what you burn. The calculator gives you both numbers. If you land below 1,200 kcal (women) or 1,500 (men), do not go lower without a health professional: slow the pace instead."),
   ("Is this the same as TDEE?", "Yes. TDEE stands for total daily energy expenditure: what you burn in a day counting your basal metabolism, digestion and all your movement. Here we call it maintenance, because it is the number at which you neither lose nor gain."),
   ("Why does another calculator give me a different number?", "Because it uses another equation (Harris-Benedict usually gives more) or other activity factors. None gets your exact number: the typical error for one person is around 10%. Take the result as a starting point and adjust it with the scale after two or three weeks."),
   ("Do I count exercise in the activity level?", "No. The factor describes your day-to-day: work, commuting, chores. Exercise is added separately on the days you do it, which is how the app does it. Count it in both places and you count it twice."),
   ("Does it give the same number as the Fotocal app?", "Yes, for the same inputs. It uses the same equations and the same limits: the activity factor, the 25% cap and the 1,200 and 1,500 kcal floors. In the app you can also set a target weight and a date."),
  ]}},
# ───────────────────────────────────────────────────────────── déficit calórico
{"slug": "deficit-calorico", "kind": "deficit", "icon": "trend",
 "dishes": ["ensaladilla-rusa", "gazpacho", "tortilla-francesa", "huevo-cocido", "patatas-bravas"],
 "blog": ["calorie-deficit-for-fat-loss", "how-fast-should-you-lose-weight", "the-truth-about-starvation-mode"],
 "sources": ["mifflin", "wishnofsky"],
 "es": {
  "short": "Déficit calórico", "card": "Cuánto recortar, a qué ritmo y cuánto tardarías en llegar a tu peso.",
  "title": "Calculadora de déficit calórico: mujer y hombre, gratis",
  "desc": "Calcula tu déficit calórico para perder peso: mantenimiento, cuánto recortar según tu sexo y peso, y cuánto tardarías. Gratis, sin registro y con ejemplos.",
  "h1": "Calculadora de déficit calórico: mujer y hombre",
  "lead": "Cuántas calorías comer para perder peso a un ritmo sensato y cuánto tardarías en llegar a tu objetivo.",
  "bridge": "¿Quieres cumplir tus {X} kcal sin pesar comida?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <p>Primero tu mantenimiento: la tasa metabólica basal de Mifflin-St Jeor multiplicada por tu nivel de actividad diaria. Después el recorte:</p>
      <div class="calc-formula"><code>déficit diario = ritmo (kg/semana) × 7.700 ÷ 7</code><br><code>tope: 25 % del mantenimiento &nbsp;·&nbsp; suelo: 1.200 kcal (mujer) / 1.500 kcal (hombre)</code></div>
      <p>Con medio kilo a la semana salen 550 kcal al día; con un cuarto, 275; con tres cuartos, 825. Si eso supera la cuarta parte de lo que gastas, se queda en esa cuarta parte, y si el objetivo cae por debajo del suelo, se sube al suelo. Es lo que hace la app Fotocal con tu plan. El tiempo se estima con el déficit que de verdad aplicas, no con el que pediste.</p>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Una mujer de 35 años, 165 cm y 70 kg, de pie a ratos, que quiere llegar a 63 kg a medio kilo por semana. Su mantenimiento son 1.918 kcal; las 550 kcal pedidas pasan del 25 %, así que el recorte se queda en 480 y el objetivo en 1.438 kcal. Eso son unos 0,44 kg por semana, el 0,62 % de su peso, y unas 17 semanas para los 7 kilos.</p>
      <p>Un hombre de 35 años, 178 cm y 85 kg, que se mueve todo el día y quiere llegar a 78 kg: mantenimiento 2.778 kcal, objetivo 2.228, medio kilo por semana (el 0,59 % de su peso) y unas 14 semanas.</p>
      <h2 id="mujer-hombre">Déficit calórico en la mujer y en el hombre</h2>
      <p>La regla es la misma para los dos. Lo que cambia es el punto de partida: a igual edad, altura, peso y actividad, la fórmula asigna a una mujer unas 166 kcal menos de gasto al día, y como las mujeres suelen pesar menos, el tope del 25 % y el suelo de 1.200 kcal se alcanzan antes. Por eso la calculadora pide el sexo.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>Un ritmo de entre el 0,5 % y el 1 % de tu peso a la semana es el que recomiendan las guías de nutrición deportiva para perder grasa conservando músculo; si la calculadora te dice que vas más rápido, baja el ritmo. Reparte el objetivo con la <a href="../macros/">calculadora de macros</a> y prioriza la proteína (la <a href="../proteinas/">calculadora de proteínas</a> te da los gramos). Platos que caben bien en un déficit: <a href="../../calorias/gazpacho/">gazpacho</a>, <a href="../../calorias/tortilla-francesa/">tortilla francesa</a> o un <a href="../../calorias/huevo-cocido/">huevo cocido</a>; y conviene medir los que no: la <a href="../../calorias/ensaladilla-rusa/">ensaladilla rusa</a> o las <a href="../../calorias/patatas-bravas/">patatas bravas</a>.</p>""",
  "faq": [
   ("¿Cuántas calorías debo quemar para bajar 1 kilo?", "Unas 7.700 kcal de déficit acumulado, entre comer menos y moverte más; no hace falta «quemarlas» en el gimnasio. Con 550 kcal menos al día tardas unas dos semanas; con 275, un mes. La báscula no sigue la regla al pie de la letra: las primeras semanas baja más, por agua, y después menos."),
   ("¿Cuál es el déficit calórico recomendado para bajar de peso?", "El que te hace perder entre el 0,5 % y el 1 % de tu peso a la semana, sin pasar del 25 % de tu gasto ni bajar de 1.200 kcal (mujer) o 1.500 (hombre). Con 70 kg son de 350 a 700 g a la semana. Más rápido se lleva peor y se recupera antes."),
   ("¿Cuánto adelgazo con un déficit de 500 calorías por día?", "Unos 450 g a la semana sobre el papel (3.500 kcal entre 7.700), alrededor de dos kilos al mes. Para una mujer de 55 kg es casi el ritmo máximo sensato; para un hombre de 100 kg es un ritmo suave."),
   ("¿Y si me sale por debajo de 1.200 o 1.500 kcal?", "La calculadora, como la app, sube el objetivo a ese suelo y te avisa. Comer menos de eso de forma mantenida no es buena idea sin un médico o un dietista detrás: elige un ritmo más suave o reparte el déficit entre comer algo menos y moverte algo más."),
   ("¿De dónde sale lo de 7.700 kcal por kilo?", "De una estimación clásica (Wishnofsky, 1958) de la energía que guarda un kilo de tejido graso. Sirve para dimensionar el recorte, no para predecir la báscula: el cuerpo gasta menos a medida que pesas menos."),
  ]},
 "en": {
  "short": "Calorie deficit", "card": "How much to cut, at what pace, and how long to reach your weight.",
  "title": "Calorie deficit calculator for women and men",
  "desc": "Work out your calorie deficit to lose weight: maintenance, how much to cut for your sex and weight, and how long it takes. Free, no sign-up, with examples.",
  "h1": "Calorie deficit calculator for women and men",
  "lead": "How many calories to eat to lose weight at a sensible pace, and how long it takes to reach your goal.",
  "bridge": "Want to hit your {X} kcal without weighing food?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <p>First your maintenance: the Mifflin-St Jeor basal metabolic rate times your day-to-day activity level. Then the cut:</p>
      <div class="calc-formula"><code>daily deficit = pace (kg/week) × 7,700 ÷ 7</code><br><code>cap: 25% of maintenance &nbsp;·&nbsp; floor: 1,200 kcal (women) / 1,500 kcal (men)</code></div>
      <p>Half a kilo a week is 550 kcal a day; a quarter, 275; three quarters, 825. If that is more than a quarter of what you burn, it stays at that quarter, and if the target falls below the floor, it is raised to the floor. That is what the Fotocal app does with your plan. The time is estimated with the deficit you actually apply, not the one you asked for.</p>
      <h2 id="example">A worked example</h2>
      <p>A 35-year-old woman, 165 cm and 70 kg, on her feet sometimes, who wants to reach 63 kg at half a kilo a week. Her maintenance is 1,918 kcal; the 550 kcal she asked for is over 25%, so the cut stays at 480 and the target at 1,438 kcal. That is about 0.44 kg a week, 0.62% of her weight, and some 17 weeks for the 7 kilos.</p>
      <p>A 35-year-old man, 178 cm and 85 kg, who moves all day and wants to reach 78 kg: maintenance 2,778 kcal, target 2,228, half a kilo a week (0.59% of his weight) and about 14 weeks.</p>
      <h2 id="women-men">Calorie deficit for women and for men</h2>
      <p>The rule is the same for both. What changes is the starting point: at the same age, height, weight and activity, the equation gives a woman about 166 kcal less a day, and since women tend to weigh less, the 25% cap and the 1,200 kcal floor are reached sooner. That is why the calculator asks for your sex.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>Losing between 0.5% and 1% of your weight a week is what sports nutrition guidelines recommend to lose fat and keep muscle; if the calculator says you are going faster, slow down. Split the target with the <a href="../macros/">macro calculator</a> and put protein first (the <a href="../proteinas/">protein calculator</a> gives you the grams). Spanish dishes that fit a deficit well: <a href="../../calorias/gazpacho/">gazpacho</a>, a <a href="../../calorias/tortilla-francesa/">plain omelette</a> or a <a href="../../calorias/huevo-cocido/">boiled egg</a>; and ones worth measuring: <a href="../../calorias/ensaladilla-rusa/">ensaladilla rusa</a> or <a href="../../calorias/patatas-bravas/">patatas bravas</a> (pages in Spanish).</p>""",
  "faq": [
   ("How many calories do I need to burn to lose 1 kilo?", "About 7,700 kcal of accumulated deficit, between eating less and moving more; you do not need to burn them in the gym. With 550 kcal less a day it takes about two weeks; with 275, a month. The scale does not follow the rule exactly: it drops faster at first, from water, and slower later."),
   ("What calorie deficit is recommended to lose weight?", "The one that makes you lose between 0.5% and 1% of your weight a week, never more than 25% of what you burn and never below 1,200 kcal (women) or 1,500 (men). At 70 kg that is 350 to 700 g a week. Faster is harder to keep and comes back sooner."),
   ("How much will I lose with a 500-calorie daily deficit?", "About 450 g a week on paper (3,500 kcal divided by 7,700), around two kilos a month. For a 55 kg woman that is close to the fastest sensible pace; for a 100 kg man it is a gentle one."),
   ("What if my target is below 1,200 or 1,500 kcal?", "The calculator, like the app, raises the target to that floor and tells you so. Eating less than that for a long time is not a good idea without a doctor or dietitian: pick a slower pace or split the deficit between eating a bit less and moving a bit more."),
   ("Where does 7,700 kcal per kilo come from?", "From a classic estimate (Wishnofsky, 1958) of the energy stored in a kilo of body fat. It is good for sizing the cut, not for predicting the scale: your body burns less as you weigh less."),
  ]}},
# ───────────────────────────────────────────────────────────── IMC
{"slug": "imc", "kind": "bmi", "icon": "scale",
 "dishes": ["cocido-madrileno", "fabada-asturiana", "salmorejo"],
 "blog": ["why-the-scale-is-not-the-whole-story", "how-to-lose-weight-sustainably", "building-muscle-while-losing-fat"],
 "sources": ["who_bmi"],
 "es": {
  "short": "IMC", "card": "Tu índice de masa corporal y el rango de la OMS en el que cae.",
  "title": "Calculadora de IMC (índice de masa corporal)",
  "desc": "Calcula tu índice de masa corporal con tu peso y altura, mira en qué rango de la OMS cae y qué peso da un IMC normal. Y lo que el IMC no te dice.",
  "h1": "Calculadora de IMC",
  "lead": "Tu índice de masa corporal, el rango de la Organización Mundial de la Salud en el que cae y el peso que te dejaría en el normal.",
  "bridge": "¿Quieres llegar a tu rango sin pesar la comida?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <div class="calc-formula"><code>IMC = peso (kg) ÷ altura (m)²</code></div>
      <p>El resultado se compara con los rangos de la Organización Mundial de la Salud para adultos:</p>
      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">IMC</th><th scope="col">Clasificación OMS</th></tr></thead><tbody>
        <tr data-bmi-band="0"><td>menos de 18,5</td><td>Bajo peso</td></tr>
        <tr data-bmi-band="1"><td>18,5 a 24,9</td><td>Peso normal</td></tr>
        <tr data-bmi-band="2"><td>25,0 a 29,9</td><td>Sobrepeso</td></tr>
        <tr data-bmi-band="3"><td>30,0 a 34,9</td><td>Obesidad grado I</td></tr>
        <tr data-bmi-band="4"><td>35,0 a 39,9</td><td>Obesidad grado II</td></tr>
        <tr data-bmi-band="5"><td>40 o más</td><td>Obesidad grado III</td></tr>
      </tbody></table></div>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Con 75 kg y 1,70 m: 75 ÷ (1,70 × 1,70) = 26,0, sobrepeso según la OMS. Con esa altura, el peso normal va de 53 a 72 kg (IMC de 18,5 a 24,9), así que le sobrarían unos 3 kilos para entrar en el rango, no 20.</p>
      <h2 id="limites">Lo que el IMC no puede decirte</h2>
      <p>Es una relación entre dos números y no sabe de qué está hecho tu peso. Una persona que entrena fuerza puede dar sobrepeso con muy poca grasa; otra con IMC normal puede llevar demasiada grasa abdominal. Tampoco distingue edad (a partir de los 65 los puntos de corte se discuten), sexo ni origen étnico, para el que algunas sociedades proponen cortes más bajos. No vale para menores de 18 años ni en el embarazo.</p>
      <p>Si tu IMC sale alto y no te cuadra, mide la cintura: por encima de 102 cm en hombres y 88 cm en mujeres es un dato de riesgo por sí solo.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>Úsalo para situarte, no para fijarte un objetivo exacto: la <a href="../peso-saludable/">calculadora de peso saludable</a> te da el rango completo para tu altura. Si quieres moverte hacia él, el número útil es el de calorías: tu <a href="../calorias-diarias/">mantenimiento</a> y el <a href="../deficit-calorico/">déficit</a> que te toca. Los platos de cuchara como el <a href="../../calorias/cocido-madrileno/">cocido madrileño</a> o la <a href="../../calorias/fabada-asturiana/">fabada</a> caben, sabiendo lo que tienen; el <a href="../../calorias/salmorejo/">salmorejo</a> lleva más aceite del que parece.</p>""",
  "faq": [
   ("¿Qué IMC es normal?", "Entre 18,5 y 24,9 según la OMS para adultos. Por debajo de 18,5 es bajo peso; de 25 a 29,9, sobrepeso; a partir de 30, obesidad, en tres grados. La calculadora te dice en qué rango estás y qué peso te dejaría dentro del normal con tu altura."),
   ("¿Sirve el IMC si hago mucho deporte?", "Peor que para la media. El IMC no distingue músculo de grasa: una persona musculada puede dar sobrepeso con poca grasa corporal. En ese caso dicen más el perímetro de cintura, cómo te queda la ropa o una medición de composición corporal."),
   ("¿Vale para niños, embarazadas o mayores de 65?", "No con estos rangos. En menores de 18 se usan percentiles por edad y sexo; en el embarazo no aplica; y a partir de los 65 años los puntos de corte se discuten. En esos casos, el pediatra o el médico."),
   ("¿Es lo mismo IMC que porcentaje de grasa?", "No. El IMC solo mira peso y altura. El porcentaje de grasa mide qué parte del peso es grasa y necesita otra medición (bioimpedancia, pliegues o DEXA). Si lo conoces, la <a href=\"../tmb/\">calculadora de TMB</a> lo usa para afinar tu gasto."),
  ]},
 "en": {
  "short": "BMI", "card": "Your body mass index and the WHO band it falls in.",
  "title": "BMI calculator (body mass index)",
  "desc": "Work out your body mass index from your weight and height, see which WHO band it falls in and what weight gives a normal BMI. And what BMI cannot tell you.",
  "h1": "BMI calculator",
  "lead": "Your body mass index, the World Health Organization band it falls in and the weight that would put you in the normal range.",
  "bridge": "Want to reach your range without weighing food?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <div class="calc-formula"><code>BMI = weight (kg) ÷ height (m)²</code></div>
      <p>The result is compared with the World Health Organization bands for adults:</p>
      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">BMI</th><th scope="col">WHO classification</th></tr></thead><tbody>
        <tr data-bmi-band="0"><td>under 18.5</td><td>Underweight</td></tr>
        <tr data-bmi-band="1"><td>18.5 to 24.9</td><td>Normal weight</td></tr>
        <tr data-bmi-band="2"><td>25.0 to 29.9</td><td>Overweight</td></tr>
        <tr data-bmi-band="3"><td>30.0 to 34.9</td><td>Obesity class I</td></tr>
        <tr data-bmi-band="4"><td>35.0 to 39.9</td><td>Obesity class II</td></tr>
        <tr data-bmi-band="5"><td>40 or more</td><td>Obesity class III</td></tr>
      </tbody></table></div>
      <h2 id="example">A worked example</h2>
      <p>At 75 kg and 1.70 m: 75 ÷ (1.70 × 1.70) = 26.0, overweight by the WHO bands. At that height the normal range runs from 53 to 72 kg (BMI 18.5 to 24.9), so about 3 kilos would bring this person into the range, not 20.</p>
      <h2 id="limits">What BMI cannot tell you</h2>
      <p>It is a ratio of two numbers and does not know what your weight is made of. Someone who lifts weights can read as overweight with very little fat; someone with a normal BMI can carry too much belly fat. It ignores age (above 65 the cut-offs are debated), sex and ethnicity, for which some bodies propose lower cut-offs. It does not apply under 18 or in pregnancy.</p>
      <p>If your BMI comes out high and that does not fit, measure your waist: above 102 cm for men and 88 cm for women is a risk marker on its own.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>Use it to see where you stand, not to set an exact goal: the <a href="../peso-saludable/">healthy weight calculator</a> gives you the full range for your height. If you want to move towards it, the useful number is calories: your <a href="../calorias-diarias/">maintenance</a> and the <a href="../deficit-calorico/">deficit</a> that suits you. Hearty Spanish stews like <a href="../../calorias/cocido-madrileno/">cocido madrileño</a> or <a href="../../calorias/fabada-asturiana/">fabada</a> fit, once you know what is in them; <a href="../../calorias/salmorejo/">salmorejo</a> carries more olive oil than it looks (pages in Spanish).</p>""",
  "faq": [
   ("What BMI is normal?", "Between 18.5 and 24.9 by the WHO adult bands. Under 18.5 is underweight; 25 to 29.9, overweight; from 30, obesity, in three classes. The calculator tells you which band you are in and what weight would put you in the normal range for your height."),
   ("Is BMI useful if I do a lot of sport?", "Less than for most people. BMI cannot tell muscle from fat: a muscular person can read as overweight with little body fat. Waist size, how your clothes fit or a body composition measurement say more."),
   ("Does it work for children, pregnancy or over 65?", "Not with these bands. Under 18, percentiles by age and sex are used; in pregnancy it does not apply; and above 65 the cut-offs are debated. In those cases, ask a paediatrician or doctor."),
   ("Is BMI the same as body fat percentage?", "No. BMI only looks at weight and height. Body fat percentage measures how much of your weight is fat and needs another measurement (bioimpedance, skinfolds or DEXA). If you know it, the <a href=\"../tmb/\">BMR calculator</a> uses it to refine your energy use."),
  ]}},
# ───────────────────────────────────────────────────────────── proteínas
{"slug": "proteinas", "kind": "protein", "icon": "egg",
 "dishes": ["huevo-cocido", "pulpo-a-la-gallega", "jamon-serrano", "lentejas-estofadas", "gambas-al-ajillo"],
 "blog": ["macronutrients-101", "building-muscle-while-losing-fat", "calorie-deficit-for-fat-loss"],
 "sources": ["efsa_protein", "issn_protein"],
 "es": {
  "short": "Proteínas", "card": "Los gramos de proteína al día para tu peso y tu objetivo.",
  "title": "Calculadora de proteínas: cuánta proteína al día",
  "desc": "Calcula cuántos gramos de proteína necesitas al día según tu peso y objetivo, de 1,2 a 2,0 g por kilo, con el mínimo de la EFSA y la cuenta de la app.",
  "h1": "Calculadora de proteínas",
  "lead": "Cuántos gramos de proteína comer al día para tu peso y tu objetivo, con el mínimo oficial y el rango para quien entrena.",
  "bridge": "¿Quieres llegar a tus {X} g de proteína sin pesar comida?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <div class="calc-formula"><code>proteína (g) = g/kg según objetivo × peso de referencia</code><br><code>perder o ganar músculo: 2,0 g/kg &nbsp;·&nbsp; mantener o ganar peso: 1,6 g/kg</code></div>
      <p>El peso de referencia es tu peso real, salvo que tu IMC pase de 25: entonces se usa el peso que tendrías con un IMC de 25. La razón es que la necesidad de proteína depende sobre todo de la masa magra, no de la grasa, y multiplicar por el peso total en alguien con sobrepeso da cifras infladas. Es la regla de la app Fotocal.</p>
      <p>La calculadora te muestra además el rango de 1,2 a 2,0 g/kg, donde se mueven las recomendaciones para adultos activos (la Sociedad Internacional de Nutrición Deportiva habla de 1,4 a 2,0 g/kg para quien entrena), y el mínimo de la EFSA para adultos: 0,83 g por kilo de peso al día. Ese mínimo evita carencias; no es lo óptimo para conservar músculo mientras pierdes peso.</p>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Una persona de 80 kg y 175 cm que quiere perder peso tiene un IMC de 26,1, así que su peso de referencia son 76,6 kg (IMC 25 a su altura). Con 2,0 g/kg: 153 g de proteína al día, unos 51 g en cada una de tres comidas. Su mínimo EFSA serían 66 g. Otra de 70 kg y 170 cm que solo quiere mantener: 1,6 × 70 = 112 g al día.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>Repártelo en tres o cuatro comidas: llegar a 25 o 40 g por comida es más fácil que concentrarlo en la cena. Un <a href="../../calorias/huevo-cocido/">huevo cocido</a> aporta unos 7 g; una ración de <a href="../../calorias/pulpo-a-la-gallega/">pulpo a la gallega</a>, de <a href="../../calorias/gambas-al-ajillo/">gambas al ajillo</a> o de <a href="../../calorias/jamon-serrano/">jamón serrano</a> bastante más, y las <a href="../../calorias/lentejas-estofadas/">lentejas</a> suman proteína vegetal con fibra. Si estás en déficit, encaja estos gramos dentro de tus calorías con la <a href="../macros/">calculadora de macros</a>.</p>""",
  "faq": [
   ("¿Cuánta proteína necesito al día?", "El mínimo para un adulto sano es 0,83 g por kilo de peso (EFSA). Para conservar músculo mientras pierdes peso o si entrenas fuerza, entre 1,6 y 2,0 g por kilo. La calculadora usa 2,0 g/kg para perder peso o ganar músculo y 1,6 g/kg para mantener, como la app."),
   ("¿Por qué no usa mi peso total si tengo sobrepeso?", "Porque la proteína se necesita sobre todo para la masa magra. Con un IMC por encima de 25 se calcula sobre el peso que tendrías con IMC 25 a tu altura; así la cifra no se infla con kilos que son grasa."),
   ("¿Es malo comer mucha proteína?", "En personas sanas, hasta unos 2 g/kg al día no hay pruebas de daño. Si tienes una enfermedad renal o te han pedido limitar la proteína, sigue lo que te diga tu médico, no esta calculadora."),
   ("¿Cuánta proteína por comida?", "Entre 25 y 40 g por comida es una referencia práctica; repartirla en tres o cuatro tomas ayuda más que acumularla. La calculadora te da la cifra dividida entre tres y entre cuatro comidas."),
  ]},
 "en": {
  "short": "Protein", "card": "Grams of protein a day for your weight and goal.",
  "title": "Protein calculator: how much protein a day",
  "desc": "Work out how many grams of protein you need a day for your weight and goal, from 1.2 to 2.0 g per kilo, with the EFSA minimum and the app's maths.",
  "h1": "Protein calculator",
  "lead": "How many grams of protein to eat a day for your weight and goal, with the official minimum and the range for people who train.",
  "bridge": "Want to hit your {X} g of protein without weighing food?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <div class="calc-formula"><code>protein (g) = g/kg for your goal × reference weight</code><br><code>lose or build muscle: 2.0 g/kg &nbsp;·&nbsp; maintain or gain weight: 1.6 g/kg</code></div>
      <p>The reference weight is your real weight, unless your BMI is above 25: then it is the weight you would have at a BMI of 25. Protein needs follow lean mass, not fat, and multiplying by total weight in someone overweight gives inflated numbers. This is the Fotocal app's rule.</p>
      <p>The calculator also shows the 1.2 to 2.0 g/kg range where advice for active adults sits (the International Society of Sports Nutrition gives 1.4 to 2.0 g/kg for people who train), and the EFSA minimum for adults: 0.83 g per kilo of body weight a day. That minimum prevents deficiency; it is not the best amount to keep muscle while you lose weight.</p>
      <h2 id="example">A worked example</h2>
      <p>Someone of 80 kg and 175 cm who wants to lose weight has a BMI of 26.1, so their reference weight is 76.6 kg (BMI 25 at their height). At 2.0 g/kg: 153 g of protein a day, about 51 g at each of three meals. Their EFSA minimum would be 66 g. Someone of 70 kg and 170 cm who just wants to maintain: 1.6 × 70 = 112 g a day.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>Split it over three or four meals: 25 to 40 g a meal is easier than loading it all into dinner. A <a href="../../calorias/huevo-cocido/">boiled egg</a> gives about 7 g; a serving of <a href="../../calorias/pulpo-a-la-gallega/">Galician-style octopus</a>, <a href="../../calorias/gambas-al-ajillo/">garlic prawns</a> or <a href="../../calorias/jamon-serrano/">serrano ham</a> a good deal more, and <a href="../../calorias/lentejas-estofadas/">lentils</a> add plant protein with fibre (pages in Spanish). If you are in a deficit, fit these grams inside your calories with the <a href="../macros/">macro calculator</a>.</p>""",
  "faq": [
   ("How much protein do I need a day?", "The minimum for a healthy adult is 0.83 g per kilo of body weight (EFSA). To keep muscle while losing weight or if you lift, 1.6 to 2.0 g per kilo. The calculator uses 2.0 g/kg to lose weight or build muscle and 1.6 g/kg to maintain, like the app."),
   ("Why does it not use my full weight if I am overweight?", "Because protein is needed mostly for lean mass. With a BMI above 25 it is worked out on the weight you would have at BMI 25 for your height, so the number is not inflated by kilos of fat."),
   ("Is a lot of protein bad for you?", "In healthy people there is no evidence of harm up to about 2 g/kg a day. If you have kidney disease or have been told to limit protein, follow your doctor, not this calculator."),
   ("How much protein per meal?", "25 to 40 g a meal is a practical guide; spreading it over three or four meals helps more than piling it up. The calculator shows the number divided over three and over four meals."),
  ]}},
# ───────────────────────────────────────────────────────────── macros
{"slug": "macros", "kind": "macros", "icon": "pie",
 "dishes": ["paella-valenciana", "tostada-con-tomate-y-aceite", "aceite-de-oliva", "barra-de-pan"],
 "blog": ["macronutrients-101", "calorie-deficit-for-fat-loss", "tdee-how-many-calories-you-need"],
 "sources": ["mifflin", "efsa_fat", "issn_protein"],
 "es": {
  "short": "Macros", "card": "Gramos de proteínas, grasas e hidratos para tu objetivo.",
  "title": "Calculadora de macros: proteínas, grasas e hidratos",
  "desc": "Calcula tus macros: gramos de proteínas, grasas e hidratos al día según tu objetivo y tus calorías, con el mismo reparto que la app Fotocal. Sin registro.",
  "h1": "Calculadora de macros",
  "lead": "Tus calorías repartidas en gramos de proteínas, grasas e hidratos según tu objetivo, con el mismo reparto que la app.",
  "bridge": "¿Quieres cumplir tus {X} kcal sin pesar comida?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <p>Primero las calorías, como en la <a href="../calorias-diarias/">calculadora de calorías diarias</a> (o las que escribas tú). Después, en este orden:</p>
      <div class="calc-formula"><code>proteína = 2,0 g/kg (perder, músculo) o 1,6 g/kg (mantener, ganar) × peso de referencia</code><br><code>grasa &nbsp;&nbsp;&nbsp;= 25 % (perder, músculo) o 27,5 % (mantener, ganar) de las kcal ÷ 9</code><br><code>hidratos = el resto ÷ 4</code></div>
      <p>La proteína va primero y por kilo porque es lo que protege el músculo; el peso de referencia es el que tendrías con un IMC de 25 si el tuyo es mayor. La grasa va como porcentaje, dentro del 20-35 % que da la EFSA. Los hidratos son lo que queda. Si no queda nada, la grasa baja al 20 %. Los repartos bajo en hidratos (25 % de las kcal) y cetogénico (10 %) fijan los hidratos y dejan la grasa como resto. Todo es igual que en la app Fotocal.</p>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Una mujer de 70 kg y 170 cm que quiere mantener con 2.000 kcal y reparto equilibrado: proteína 1,6 × 70 = 112 g (448 kcal); grasa 27,5 % de 2.000 = 550 kcal, 61 g; hidratos (2.000 − 448 − 549) ÷ 4 = 251 g. Un hombre de 85 kg y 178 cm que quiere perder, con 2.228 kcal: su IMC es 26,8, así que la proteína se calcula sobre 79,2 kg, 158 g; grasa 62 g; hidratos 260 g.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>Prioriza en este orden: calorías, proteína, y el resto con margen. Clavar los hidratos y la grasa al gramo no cambia el resultado; llegar a la proteína y no pasarte de calorías, sí. Las grasas se escapan fácil: una cucharada (10 ml) de <a href="../../calorias/aceite-de-oliva/">aceite de oliva</a> son 80 kcal, y una <a href="../../calorias/tostada-con-tomate-y-aceite/">tostada con tomate y aceite</a> lleva más de lo que parece. El <a href="../../calorias/barra-de-pan/">pan</a> y la <a href="../../calorias/paella-valenciana/">paella</a> son sobre todo hidratos. Para la cifra de proteína por separado, la <a href="../proteinas/">calculadora de proteínas</a>.</p>""",
  "faq": [
   ("¿Qué son los macros?", "Los macronutrientes: proteínas y carbohidratos (4 kcal por gramo) y grasas (9 kcal por gramo). El alcohol aporta 7 kcal por gramo, pero no se cuenta como macro objetivo. Repartir las calorías en macros ayuda a que una dieta funcione, no solo a que cuadre."),
   ("¿Cuál es el mejor reparto para perder grasa?", "El que tiene suficiente proteína y que puedes mantener. El equilibrado de la calculadora (2,0 g/kg de proteína, 25 % de grasa) funciona para casi todo el mundo; el bajo en hidratos o el cetogénico no queman más grasa a igualdad de calorías, solo cambian lo que comes."),
   ("¿Por qué mis hidratos salen tan altos o tan bajos?", "Porque son el resto: dependen de las calorías y de la proteína. Con pocas calorías y mucho peso, queda poco para los hidratos; si no queda nada, la grasa baja al 20 %, como en la app."),
   ("¿Puedo poner mis propias calorías?", "Sí. Si escribes una cifra en «Calorías propias», se reparten esas en lugar de las calculadas. Útil si ya tienes un objetivo de tu dietista."),
  ]},
 "en": {
  "short": "Macros", "card": "Grams of protein, fat and carbs for your goal.",
  "title": "Macro calculator: protein, fat and carbs",
  "desc": "Work out your macros: grams of protein, fat and carbs a day for your goal and calories, with the same split as the Fotocal app. Free, no sign-up.",
  "h1": "Macro calculator",
  "lead": "Your calories split into grams of protein, fat and carbs for your goal, with the same split as the app.",
  "bridge": "Want to hit your {X} kcal without weighing food?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <p>Calories first, as in the <a href="../calorias-diarias/">daily calorie calculator</a> (or the ones you type in). Then, in this order:</p>
      <div class="calc-formula"><code>protein = 2.0 g/kg (lose, muscle) or 1.6 g/kg (maintain, gain) × reference weight</code><br><code>fat &nbsp;&nbsp;&nbsp;&nbsp;= 25% (lose, muscle) or 27.5% (maintain, gain) of kcal ÷ 9</code><br><code>carbs &nbsp;&nbsp;= what is left ÷ 4</code></div>
      <p>Protein goes first and per kilo because it protects muscle; the reference weight is what you would weigh at a BMI of 25 if yours is higher. Fat goes as a share, inside EFSA's 20-35%. Carbs are what is left. If nothing is left, fat drops to 20%. The low-carb (25% of kcal) and keto (10%) splits fix the carbs and leave fat as the rest. All the same as in the Fotocal app.</p>
      <h2 id="example">A worked example</h2>
      <p>A woman of 70 kg and 170 cm maintaining on 2,000 kcal with the balanced split: protein 1.6 × 70 = 112 g (448 kcal); fat 27.5% of 2,000 = 550 kcal, 61 g; carbs (2,000 − 448 − 549) ÷ 4 = 251 g. A man of 85 kg and 178 cm losing weight on 2,228 kcal: his BMI is 26.8, so protein is worked out on 79.2 kg, 158 g; fat 62 g; carbs 260 g.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>Prioritise in this order: calories, protein, and the rest with some slack. Hitting carbs and fat to the gram does not change the outcome; reaching your protein and staying within calories does. Fat slips in easily: a 10 ml spoon of <a href="../../calorias/aceite-de-oliva/">olive oil</a> is 80 kcal, and a <a href="../../calorias/tostada-con-tomate-y-aceite/">toast with tomato and oil</a> carries more than it looks. <a href="../../calorias/barra-de-pan/">Bread</a> and <a href="../../calorias/paella-valenciana/">paella</a> are mostly carbs (pages in Spanish). For protein on its own, the <a href="../proteinas/">protein calculator</a>.</p>""",
  "faq": [
   ("What are macros?", "Macronutrients: protein and carbohydrate (4 kcal per gram) and fat (9 kcal per gram). Alcohol gives 7 kcal per gram but is not a macro target. Splitting calories into macros helps a diet work, not just add up."),
   ("What is the best split to lose fat?", "One with enough protein that you can keep up. The balanced split here (2.0 g/kg of protein, 25% fat) works for almost everyone; low-carb or keto do not burn more fat at the same calories, they only change what you eat."),
   ("Why are my carbs so high or so low?", "Because they are what is left: they depend on calories and protein. With few calories and a high weight, little is left for carbs; if nothing is left, fat drops to 20%, as in the app."),
   ("Can I use my own calories?", "Yes. If you type a number into \"Your own calories\", that is split instead of the calculated one. Useful if you already have a target from a dietitian."),
  ]}},
# ───────────────────────────────────────────────────────────── agua
{"slug": "agua", "kind": "water", "icon": "drop",
 "dishes": ["gazpacho", "cafe-con-leche", "cana-de-cerveza", "coca-cola-zero"],
 "blog": ["tdee-how-many-calories-you-need", "how-many-calories-does-exercise-burn", "how-to-lose-weight-sustainably"],
 "sources": ["efsa_water", "iom_water", "mifflin"],
 "es": {
  "short": "Agua", "card": "Cuánta agua beber al día según tu gasto y tu actividad.",
  "title": "Calculadora de agua: cuánta agua beber al día",
  "desc": "Calcula cuánta agua beber al día según tus calorías y tu actividad, con el mínimo de la EFSA y la misma fórmula que la app Fotocal. En litros y en vasos.",
  "h1": "Calculadora de agua",
  "lead": "Cuántos litros beber al día según lo que gastas y cómo te mueves, en litros y en vasos de 250 ml.",
  "bridge": "¿Quieres llevar la cuenta de tus {X} litros sin pensar?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <p>El agua que necesitas sigue a la energía que gastas: la referencia clásica, recogida por el Institute of Medicine de EE. UU., es de 1,0 a 1,5 ml de agua por cada kcal, más cuanto más te mueves. Como unas cuatro quintas partes del agua llegan bebiendo y el resto con la comida, el objetivo de bebida es:</p>
      <div class="calc-formula"><code>agua para beber (ml) = kcal objetivo × ml/kcal × 0,8</code><br><code>ml/kcal: 1,0 sentado · 1,1 de pie a ratos o casi siempre · 1,25 en movimiento · 1,5 trabajo duro</code><br><code>mínimo: 1.600 ml (mujer) / 2.000 ml (hombre) &nbsp;·&nbsp; máximo: 4.000 ml</code></div>
      <p>Las kcal son las de tu objetivo, calculadas como en la <a href="../calorias-diarias/">calculadora de calorías</a>. El mínimo es la ingesta adecuada de agua total de la EFSA (2,0 L mujeres, 2,5 L hombres) por 0,8: nadie recibe un objetivo por debajo. Es la fórmula exacta de la app Fotocal.</p>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Una mujer de 35 años, 165 cm y 70 kg, de pie a ratos, que mantiene su peso: 1.918 kcal × 1,1 × 0,8 = 1.688 ml, unos 1,7 litros o 7 vasos. Un hombre de 35 años, 178 cm y 85 kg, que se mueve todo el día: 2.778 kcal × 1,25 × 0,8 = 2.778 ml, unos 2,8 litros o 12 vasos.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>Es una referencia para un día normal, no una obligación al mililitro. Cuentan el agua, las infusiones, el <a href="../../calorias/cafe-con-leche/">café con leche</a>, los refrescos sin azúcar como la <a href="../../calorias/coca-cola-zero/">Coca-Cola Zero</a> y los platos con mucha agua, como el <a href="../../calorias/gazpacho/">gazpacho</a>. La <a href="../../calorias/cana-de-cerveza/">cerveza</a> lleva agua, pero el alcohol hace orinar más: no la cuentes como hidratación. Con calor fuerte o una sesión larga de ejercicio, bebe más de lo que sale aquí; la sed y una orina clara son buenas guías.</p>""",
  "faq": [
   ("¿Cuántos litros de agua hay que beber al día?", "Para la mayoría de los adultos, entre 1,6 y 3 litros de bebida al día. La EFSA fija una ingesta adecuada de agua total (bebida más comida) de 2,0 L para mujeres y 2,5 L para hombres; la calculadora ajusta a tu gasto y tu actividad."),
   ("¿Por qué no usa los 35 ml por kilo de peso?", "Porque esa regla no está en las referencias de la EFSA ni del Institute of Medicine. Las dos ligan el agua a la energía que gastas, que ya tiene en cuenta tu peso, altura, edad, sexo y actividad. La app Fotocal dejó de usar los 35 ml/kg por eso."),
   ("¿Cuentan el café y las infusiones?", "Sí. El café y el té hidratan casi como el agua en las cantidades normales. El alcohol es la excepción: aumenta la orina."),
   ("¿Se puede beber demasiada agua?", "Sí, aunque es raro: varios litros en poco tiempo pueden bajar el sodio en sangre. Por eso el objetivo tiene un máximo de 4 litros. Si tienes una enfermedad renal o cardíaca, sigue lo que te diga tu médico."),
  ]},
 "en": {
  "short": "Water", "card": "How much water to drink a day for what you burn and how you move.",
  "title": "Water intake calculator: how much water a day",
  "desc": "Work out how much water to drink a day from your calories and activity, with the EFSA minimum and the Fotocal app's formula. In litres and glasses.",
  "h1": "Water intake calculator",
  "lead": "How many litres to drink a day for what you burn and how you move, in litres and in 250 ml glasses.",
  "bridge": "Want to keep track of your {X} litres without thinking?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <p>The water you need follows the energy you burn: the classic reference, carried by the US Institute of Medicine, is 1.0 to 1.5 ml of water per kcal, more the more you move. Since about four fifths of water comes from drinks and the rest from food, the drinking target is:</p>
      <div class="calc-formula"><code>water to drink (ml) = target kcal × ml/kcal × 0.8</code><br><code>ml/kcal: 1.0 sitting · 1.1 on your feet sometimes or mostly · 1.25 moving all day · 1.5 hard work</code><br><code>minimum: 1,600 ml (women) / 2,000 ml (men) &nbsp;·&nbsp; maximum: 4,000 ml</code></div>
      <p>The kcal are your target, worked out as in the <a href="../calorias-diarias/">daily calorie calculator</a>. The minimum is EFSA's adequate intake of total water (2.0 L for women, 2.5 L for men) times 0.8: nobody gets a target below it. This is the Fotocal app's exact formula.</p>
      <h2 id="example">A worked example</h2>
      <p>A 35-year-old woman, 165 cm and 70 kg, on her feet sometimes, maintaining her weight: 1,918 kcal × 1.1 × 0.8 = 1,688 ml, about 1.7 litres or 7 glasses. A 35-year-old man, 178 cm and 85 kg, who moves all day: 2,778 kcal × 1.25 × 0.8 = 2,778 ml, about 2.8 litres or 12 glasses.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>It is a guide for a normal day, not a rule to the millilitre. Water, herbal teas, <a href="../../calorias/cafe-con-leche/">coffee with milk</a>, sugar-free drinks like <a href="../../calorias/coca-cola-zero/">Coca-Cola Zero</a> and watery dishes like <a href="../../calorias/gazpacho/">gazpacho</a> all count (pages in Spanish). <a href="../../calorias/cana-de-cerveza/">Beer</a> contains water, but alcohol makes you pass more: do not count it as hydration. In strong heat or after a long workout, drink more than this; thirst and pale urine are good guides.</p>""",
  "faq": [
   ("How many litres of water should I drink a day?", "For most adults, 1.6 to 3 litres of drinks a day. EFSA sets an adequate intake of total water (drinks plus food) of 2.0 L for women and 2.5 L for men; the calculator adjusts to your energy use and activity."),
   ("Why not 35 ml per kilo of body weight?", "Because that rule is not in the EFSA or Institute of Medicine references. Both tie water to the energy you burn, which already accounts for your weight, height, age, sex and activity. The Fotocal app dropped 35 ml/kg for that reason."),
   ("Do coffee and tea count?", "Yes. Coffee and tea hydrate almost as well as water in normal amounts. Alcohol is the exception: it increases urine."),
   ("Can you drink too much water?", "Yes, though it is rare: several litres in a short time can lower blood sodium. That is why the target is capped at 4 litres. If you have kidney or heart disease, follow your doctor."),
  ]}},
# ───────────────────────────────────────────────────────────── TMB
{"slug": "tmb", "kind": "bmr", "icon": "heart",
 "dishes": ["churros-con-chocolate", "croquetas-de-jamon", "torrijas"],
 "blog": ["understanding-your-basal-metabolic-rate", "tdee-how-many-calories-you-need", "the-truth-about-starvation-mode"],
 "sources": ["mifflin", "katch"],
 "es": {
  "short": "TMB", "card": "Tu metabolismo basal con Mifflin-St Jeor, o Katch-McArdle si sabes tu grasa.",
  "title": "Calculadora de TMB: tu metabolismo basal",
  "desc": "Calcula tu tasa metabólica basal (TMB) con Mifflin-St Jeor, o Katch-McArdle si sabes tu porcentaje de grasa, y tu gasto diario según tu actividad.",
  "h1": "Calculadora de TMB (metabolismo basal)",
  "lead": "Lo que gasta tu cuerpo en reposo absoluto, y lo que gastas al día según cómo te mueves.",
  "bridge": "¿Quieres comer según tu gasto sin pesar comida?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <p>La tasa metabólica basal (TMB) es la energía que gasta tu cuerpo en reposo: respirar, mantener la temperatura, el corazón, el cerebro. Para la mayoría de la gente es entre el 60 y el 70 % de lo que gasta en un día. La calculadora usa la ecuación de Mifflin-St Jeor (1990):</p>
      <div class="calc-formula"><code>TMB = 10 × kg + 6,25 × cm − 5 × años + 5 (hombre) / − 161 (mujer)</code></div>
      <p>Si escribes tu porcentaje de grasa (entre 3 y 60 %), usa en su lugar Katch-McArdle, que parte de la masa magra y acierta más en personas muy musculadas o con mucha grasa:</p>
      <div class="calc-formula"><code>TMB = 370 + 21,6 × peso × (1 − grasa % ÷ 100)</code></div>
      <p>Debajo te da el gasto diario con los cinco niveles de actividad de la app Fotocal, de 1,2 a 1,725. La app hace la misma elección: Katch-McArdle si tiene tu grasa corporal, Mifflin-St Jeor si no.</p>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Una mujer de 35 años, 165 cm y 70 kg: 700 + 1.031,25 − 175 − 161 = 1.395 kcal. Un hombre de 35 años, 178 cm y 85 kg: 850 + 1.112,5 − 175 + 5 = 1.793 kcal; si sabe que tiene un 20 % de grasa, su masa magra son 68 kg y Katch-McArdle da 370 + 21,6 × 68 = 1.839 kcal.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>No comas tu TMB: es lo que gastarías tumbado todo el día. El número para planificar es tu gasto diario (la TMB por tu actividad), que te da la <a href="../calorias-diarias/">calculadora de calorías diarias</a>, con las cifras para perder o ganar. Para hacerte una idea de la escala: una ración de <a href="../../calorias/churros-con-chocolate/">churros con chocolate</a>, unas <a href="../../calorias/croquetas-de-jamon/">croquetas de jamón</a> o una <a href="../../calorias/torrijas/">torrija</a> pueden ser una parte grande de una TMB.</p>""",
  "faq": [
   ("¿Qué es la TMB?", "La tasa metabólica basal: las calorías que tu cuerpo gasta en reposo completo para mantenerse vivo. No incluye la digestión ni el movimiento; por eso tu gasto diario es mayor."),
   ("¿Qué fórmula es más fiable?", "Para adultos sanos, Mifflin-St Jeor, según las revisiones de dietética. Si conoces tu porcentaje de grasa con una medición fiable, Katch-McArdle puede acertar más porque parte de la masa magra."),
   ("¿Debo comer menos que mi TMB para adelgazar?", "No. Comer por debajo de la TMB de forma mantenida no es buena idea sin supervisión. Para perder peso, el recorte se hace sobre el gasto diario, y nunca por debajo de 1.200 kcal en mujeres ni 1.500 en hombres."),
   ("¿Se puede subir la TMB?", "Un poco, ganando masa muscular: el músculo gasta más que la grasa en reposo. La edad la baja despacio. Las diferencias reales entre personas del mismo tamaño son pequeñas."),
  ]},
 "en": {
  "short": "BMR", "card": "Your basal metabolic rate with Mifflin-St Jeor, or Katch-McArdle if you know your body fat.",
  "title": "BMR calculator: your basal metabolic rate",
  "desc": "Work out your basal metabolic rate (BMR) with Mifflin-St Jeor, or Katch-McArdle if you know your body fat, and your daily burn at five activity levels.",
  "h1": "BMR calculator (basal metabolic rate)",
  "lead": "What your body burns at complete rest, and what you burn in a day depending on how you move.",
  "bridge": "Want to eat to what you burn without weighing food?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <p>Your basal metabolic rate (BMR) is the energy your body uses at rest: breathing, keeping warm, your heart, your brain. For most people it is 60 to 70% of what they burn in a day. The calculator uses the Mifflin-St Jeor equation (1990):</p>
      <div class="calc-formula"><code>BMR = 10 × kg + 6.25 × cm − 5 × age + 5 (man) / − 161 (woman)</code></div>
      <p>If you enter your body fat percentage (3 to 60%), it uses Katch-McArdle instead, which starts from lean mass and is more accurate for very muscular people or people with a lot of fat:</p>
      <div class="calc-formula"><code>BMR = 370 + 21.6 × weight × (1 − body fat % ÷ 100)</code></div>
      <p>Below it gives your daily energy use at the Fotocal app's five activity levels, from 1.2 to 1.725. The app makes the same choice: Katch-McArdle if it has your body fat, Mifflin-St Jeor if not.</p>
      <h2 id="example">A worked example</h2>
      <p>A 35-year-old woman, 165 cm and 70 kg: 700 + 1,031.25 − 175 − 161 = 1,395 kcal. A 35-year-old man, 178 cm and 85 kg: 850 + 1,112.5 − 175 + 5 = 1,793 kcal; if he knows he has 20% body fat, his lean mass is 68 kg and Katch-McArdle gives 370 + 21.6 × 68 = 1,839 kcal.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>Do not eat your BMR: it is what you would burn lying down all day. The number to plan with is your daily energy use (BMR times activity), which the <a href="../calorias-diarias/">daily calorie calculator</a> gives you, with the numbers to lose or gain. For a sense of scale: a serving of <a href="../../calorias/churros-con-chocolate/">churros with chocolate</a>, <a href="../../calorias/croquetas-de-jamon/">ham croquettes</a> or a <a href="../../calorias/torrijas/">torrija</a> can be a big share of a BMR (pages in Spanish).</p>""",
  "faq": [
   ("What is BMR?", "Basal metabolic rate: the calories your body burns at complete rest just to stay alive. It does not include digestion or movement, which is why your daily energy use is higher."),
   ("Which equation is most reliable?", "For healthy adults, Mifflin-St Jeor, according to dietetics reviews. If you know your body fat from a reliable measurement, Katch-McArdle can be closer because it starts from lean mass."),
   ("Should I eat less than my BMR to lose weight?", "No. Eating below your BMR for a long time is not a good idea without supervision. To lose weight the cut is made on your daily energy use, and never below 1,200 kcal for women or 1,500 for men."),
   ("Can I raise my BMR?", "A little, by gaining muscle: muscle burns more than fat at rest. Age lowers it slowly. Real differences between people of the same size are small."),
  ]}},
# ───────────────────────────────────────────────────────────── peso saludable
{"slug": "peso-saludable", "kind": "healthy", "icon": "ruler",
 "dishes": ["pulpo-a-la-gallega", "gazpacho", "lentejas-estofadas"],
 "blog": ["why-the-scale-is-not-the-whole-story", "how-to-lose-weight-sustainably", "how-fast-should-you-lose-weight"],
 "sources": ["who_bmi"],
 "es": {
  "short": "Peso saludable", "card": "El rango de peso saludable para tu altura, no un único «peso ideal».",
  "title": "Calculadora de peso saludable según tu altura",
  "desc": "Calcula tu rango de peso saludable según tu altura: el que da un IMC de 18,5 a 24,9 (OMS). Un rango, no un único peso ideal, y lo que te separa de él.",
  "h1": "Calculadora de peso saludable",
  "lead": "El rango de peso que la OMS considera saludable para tu altura. Un rango, no un número mágico.",
  "bridge": "¿Quieres acercarte a tu rango sin pesar comida?",
  "body": """
      <h2 id="como">Cómo se calcula</h2>
      <p>A partir del índice de masa corporal: la Organización Mundial de la Salud considera peso normal en adultos un IMC de 18,5 a 24,9. Despejando el peso:</p>
      <div class="calc-formula"><code>peso mínimo = 18,5 × altura (m)² &nbsp;·&nbsp; peso máximo = 24,9 × altura (m)²</code></div>
      <p>Se redondea al kilo, igual que hace la app Fotocal cuando te propone un peso objetivo. Si escribes tu peso actual, la calculadora te dice tu IMC y cuántos kilos te separan del rango, si estás fuera.</p>
      <h2 id="ejemplo">Un ejemplo</h2>
      <p>Con 1,70 m: 18,5 × 2,89 = 53 kg y 24,9 × 2,89 = 72 kg. Con 1,60 m, de 47 a 64 kg; con 1,80 m, de 60 a 81 kg. Una persona de 1,70 m y 80 kg tiene un IMC de 27,7 y está a 8 kg del límite alto del rango, no de un «peso ideal» de 60 y pico.</p>
      <h2 id="por-que-rango">Por qué un rango y no un peso ideal</h2>
      <p>Las fórmulas de «peso ideal» (Lorentz, Devine, Broca…) dan un único número que no tiene más base que el rango y suele ser más bajo de lo necesario. Dentro de esos 19 o 20 kilos de margen, lo que es mejor para ti depende de tu musculatura, tu complexión y tu historia; fuera, el IMC tampoco es un diagnóstico, por las mismas razones que explica la <a href="../imc/">calculadora de IMC</a>.</p>
      <h2 id="que-hacer">Qué hacer con este número</h2>
      <p>Si estás por encima, el primer objetivo razonable es el límite alto del rango, o perder un 5-10 % de tu peso, que ya mejora la salud. Calcula tu <a href="../deficit-calorico/">déficit</a> con ese objetivo y te dirá cuánto tardarías a un ritmo sensato. Platos que ayudan sin renunciar a comer bien: <a href="../../calorias/pulpo-a-la-gallega/">pulpo a la gallega</a>, <a href="../../calorias/gazpacho/">gazpacho</a>, <a href="../../calorias/lentejas-estofadas/">lentejas</a>. Si estás por debajo, habla con un profesional sanitario antes de cambiar tu dieta.</p>""",
  "faq": [
   ("¿Cuál es mi peso ideal según mi altura?", "No hay un único peso ideal: hay un rango saludable, el que da un IMC de 18,5 a 24,9. Para 1,65 m va de 50 a 68 kg. Dentro de ese rango, el mejor para ti depende de tu musculatura y complexión."),
   ("¿Sirve si soy muy musculado?", "Menos. Con mucha masa muscular puedes estar por encima del rango con poca grasa. En ese caso, el perímetro de cintura o una medición de composición corporal dicen más."),
   ("¿Y para mayores de 65?", "Los puntos de corte se discuten: un IMC algo más alto, hasta 27, no va asociado a peor salud en personas mayores. Consulta con tu médico antes de proponerte perder peso."),
   ("¿Cuánto tardaría en llegar al rango?", "Depende de cuántos kilos y del ritmo: a medio kilo por semana, unos 8 kg son unas 16 semanas. La <a href=\"../deficit-calorico/\">calculadora de déficit calórico</a> lo calcula con tus datos."),
  ]},
 "en": {
  "short": "Healthy weight", "card": "The healthy weight range for your height, not one \"ideal weight\".",
  "title": "Healthy weight calculator for your height",
  "desc": "Your healthy weight range for your height: a BMI of 18.5 to 24.9 by WHO bands. A range, not one ideal weight, and how far you are from it.",
  "h1": "Healthy weight calculator",
  "lead": "The weight range the WHO considers healthy for your height. A range, not a magic number.",
  "bridge": "Want to move towards your range without weighing food?",
  "body": """
      <h2 id="how">How it is calculated</h2>
      <p>From the body mass index: the World Health Organization considers a BMI of 18.5 to 24.9 normal weight for adults. Solving for weight:</p>
      <div class="calc-formula"><code>lowest = 18.5 × height (m)² &nbsp;·&nbsp; highest = 24.9 × height (m)²</code></div>
      <p>Rounded to the kilo, as the Fotocal app does when it suggests a target weight. If you enter your current weight, the calculator gives your BMI and how many kilos you are from the range, if you are outside it.</p>
      <h2 id="example">A worked example</h2>
      <p>At 1.70 m: 18.5 × 2.89 = 53 kg and 24.9 × 2.89 = 72 kg. At 1.60 m, 47 to 64 kg; at 1.80 m, 60 to 81 kg. Someone of 1.70 m and 80 kg has a BMI of 27.7 and is 8 kg from the top of the range, not from an "ideal weight" in the low sixties.</p>
      <h2 id="why-range">Why a range and not an ideal weight</h2>
      <p>"Ideal weight" formulas (Lorentz, Devine, Broca…) give a single number with no more basis than the range, and it is usually lower than it needs to be. Within those 19 or 20 kilos, what is best for you depends on your muscle, build and history; outside, BMI is not a diagnosis either, for the reasons the <a href="../imc/">BMI calculator</a> explains.</p>
      <h2 id="what-next">What to do with this number</h2>
      <p>If you are above it, a reasonable first goal is the top of the range, or losing 5-10% of your weight, which already improves health. Work out your <a href="../deficit-calorico/">deficit</a> with that goal and it will tell you how long it takes at a sensible pace. Spanish dishes that help without giving up good food: <a href="../../calorias/pulpo-a-la-gallega/">Galician-style octopus</a>, <a href="../../calorias/gazpacho/">gazpacho</a>, <a href="../../calorias/lentejas-estofadas/">lentil stew</a> (pages in Spanish). If you are below it, talk to a health professional before changing your diet.</p>""",
  "faq": [
   ("What is my ideal weight for my height?", "There is no single ideal weight: there is a healthy range, the one that gives a BMI of 18.5 to 24.9. At 1.65 m it runs from 50 to 68 kg. Within it, what is best for you depends on your muscle and build."),
   ("Does it work if I am very muscular?", "Less well. With a lot of muscle you can be above the range with little fat. Waist size or a body composition measurement say more."),
   ("What about over 65?", "The cut-offs are debated: a slightly higher BMI, up to 27, is not linked to worse health in older people. Talk to your doctor before setting out to lose weight."),
   ("How long would it take to reach the range?", "It depends on how many kilos and the pace: at half a kilo a week, 8 kg is about 16 weeks. The <a href=\"../deficit-calorico/\">calorie deficit calculator</a> works it out with your numbers."),
  ]}},
]
