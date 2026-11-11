# -*- coding: utf-8 -*-
"""Copy of the /comparativa/ hub: "mejor app para contar calorías"
(MASTER PROMPT v3, PART 6).

Rules this page lives by:
  · Every competitor fact is one already in tools/compare_data.json: what
    the maker states on its own site, with the date it was read. Nothing is
    added from memory, reviews or third parties.
  · No numbered ranking and no "nº 1": the page says which app fits which
    need, and when another app is the better choice. The apps were
    compared from their makers' pages, not installed and tested, so the
    title says "comparadas", never "probadas".
  · Prices: only the ones a maker publishes. MyFitnessPal publishes US
    dollars; Yazio and Cal AI had no yearly price on the pages read.
  · When compare_data.json is refreshed, add a line to CHANGES and check
    every sentence here against the new rows.
"""

CHANGES = [  # newest first: (ISO date, es, en)
    ("2026-11-11", "La página pasa de tabla a guía: qué app encaja con cada necesidad, cuándo es mejor otra, método y preguntas. Los datos de las otras apps siguen siendo los comprobados el 10 de septiembre de 2026.",
     "The page becomes a guide instead of a table alone: which app fits each need, when another is better, the method and questions. The other apps' facts are still the ones checked on 10 September 2026."),
    ("2026-11-08", "Primera versión: tabla comparativa y tres páginas una a una.", "First version: the comparison table and three one-to-one pages."),
    ("2026-09-10", "Lectura de las webs de MyFitnessPal, Yazio y Cal AI. Se retiran dos precios de Yazio que ya no se podían comprobar.",
     "MyFitnessPal's, Yazio's and Cal AI's own sites read. Two Yazio prices that could no longer be verified were removed."),
]

FAQ = {
    "es": [
        ("¿Qué app es la mejor para contar calorías gratis?",
         "Depende de cómo apuntes. Para apuntar con una foto sin pagar, Fotocal incluye 2 escaneos con IA al día, 1 registro por voz al día, y código de barras y Coach Kal sin límite, sin tarjeta, solo en Android. Para apuntar con código de barras gratis, Yazio también lo incluye en su plan gratuito, según su web ({date})."),
        ("¿Cuál es la mejor IA para contar calorías?",
         "No hay una prueba independiente que las ordene, y aquí no las hemos medido una contra otra. Lo que sí se puede comparar es el acceso: en Fotocal el escaneo con IA es gratis dos veces al día; en MyFitnessPal y Yazio es parte del plan de pago, y Cal AI no publica precio en su web ({date})."),
        ("¿Es gratuita MyFitnessPal?",
         "Tiene funciones de pago. Según su propia web ({date}), el escáner de código de barras, el escaneo de comidas y el registro por voz son de Premium, que cuesta 79,99 dólares al año."),
        ("¿Es gratis Yazio?",
         "Su plan gratuito incluye el escáner de código de barras, según su web ({date}). El registro con IA, las vitaminas y minerales y los resúmenes semanales y mensuales son de Yazio Pro. No encontramos un precio anual publicado en las páginas que pudimos leer."),
        ("¿Dónde contar calorías gratis sin instalar nada?",
         "En esta web: las <a href=\"../calculadoras/\">calculadoras de nutrición gratis</a> te dan tu objetivo de calorías, y las <a href=\"../calorias/\">calorías de platos españoles</a>, lo que tiene cada plato por ración."),
    ],
    "en": [
        ("Which app is best for counting calories for free?",
         "It depends on how you log. To log from a photo without paying, Fotocal includes 2 AI scans a day, 1 voice log a day, and unlimited barcode scanner and Coach Kal, with no card, on Android only. For free barcode logging, Yazio also has it in its free plan, according to its site ({date})."),
        ("Which is the best AI for counting calories?",
         "No independent test ranks them, and we have not measured one against another here. What can be compared is access: on Fotocal the AI scan is free twice a day; on MyFitnessPal and Yazio it is part of the paid plan, and Cal AI publishes no price on its site ({date})."),
        ("Is MyFitnessPal free?",
         "It has paid features. According to its own site ({date}), the barcode scanner, Meal Scan and voice logging belong to Premium, which costs $79.99 a year."),
        ("Is Yazio free?",
         "Its free plan includes the barcode scanner, according to its site ({date}). AI tracking, vitamins and minerals, and weekly and monthly evaluations belong to Yazio Pro. We found no yearly price published on the pages we could read."),
        ("Where can I count calories for free without installing anything?",
         "On this site: the <a href=\"../calculadoras/\">free nutrition calculators</a> give you your calorie target, and <a href=\"../calorias/\">calories in Spanish food</a> shows what each dish has per serving."),
    ],
}

BODY = {
    "es": """      <h2>Qué app elegir según lo que necesites</h2>
      <p>No hay una app mejor para todo el mundo. Hay una que encaja con cómo comes y con cómo te resulta más fácil apuntar. Estas son las diferencias que de verdad cambian la decisión, con lo que declara cada fabricante en su web a fecha de {date}.</p>
      <h3>Si quieres apuntar con una foto sin pagar</h3>
      <p>Fotocal: el escaneo de comida con IA es gratis dos veces al día, sin tarjeta. En MyFitnessPal el escaneo de comidas es de Premium y solo funciona en inglés. En Yazio, el registro con IA es de Pro. En Cal AI la foto es el producto, pero su web no publica el precio. Así funciona el nuestro: <a href="../features/scan-food/">contar calorías con foto</a>.</p>
      <h3>Si casi todo lo que comes lleva código de barras</h3>
      <p>Fotocal y Yazio incluyen el escáner de código de barras en el plan gratis; en Fotocal no tiene límite. Cal AI también lo anuncia. En MyFitnessPal es de Premium desde octubre de 2022. Más detalle en el <a href="../features/scan-barcode/">escáner de código de barras de calorías</a>.</p>
      <h3>Si prefieres decirlo en voz alta</h3>
      <p>Fotocal incluye un registro por voz al día en el plan gratis, en español y en cualquier otro idioma. En MyFitnessPal el registro por voz es de Premium y solo en inglés. Yazio no lo anuncia para Android y Cal AI permite describir la comida escribiendo, no hablando.</p>
      <h3>Si quieres alguien a quien preguntar</h3>
      <p>Fotocal incluye Coach Kal, un coach de chat con IA, sin límite en el plan gratis. Ninguna de las otras tres anuncia un coach de chat en su web.</p>
      <h3>Si te importan las vitaminas, los minerales y el resumen de la semana</h3>
      <p>En MyFitnessPal y en Yazio, los micronutrientes y los resúmenes semanales son de pago. En Fotocal el plan gratis enseña parte y Premium abre el panel completo y la tabla nutricional entera del informe semanal. Cal AI no lo detalla.</p>
      <h2>Cuándo es mejor otra app</h2>
      <ul>
        <li><strong>Si usas iPhone.</strong> Fotocal solo existe para Android. Necesitas otra app.</li>
        <li><strong>Si llevas años apuntando en MyFitnessPal o en Yazio.</strong> Tu historial y tus comidas guardadas tienen valor. Cambiar tiene un coste, y solo compensa si lo que pagas ahora no lo usas.</li>
        <li><strong>Si comes sobre todo productos envasados de fuera de España.</strong> Lo fuerte de Fotocal son los platos de aquí, con sus raciones. Una base de datos enorme de productos de otros países puede servirte más.</li>
        <li><strong>Si quieres muchas fotos al día sin pagar.</strong> El plan gratis de Fotocal son dos escaneos con IA al día; el resto del día se apunta con código de barras, por voz o a mano.</li>
      </ul>
      <h2>Qué cuesta cada una</h2>
      <p>Solo ponemos los precios que cada fabricante publica. Fotocal Premium cuesta 6,99 € al mes o 34,99 € al año, con 5 días de prueba; el plan gratis no caduca ni pide tarjeta. MyFitnessPal publica Premium a 79,99 dólares al año y Premium+ a 99,99. Yazio cambia el precio según el país y no publicaba una cifra anual en las páginas que pudimos leer. Cal AI no publica precio en su web. Antes de pagar ninguna, mira el precio en euros en la pantalla de suscripción de Google Play: es el que cuenta. Cómo leer esa letra pequeña está en <a href="../blog/app-contar-calorias-gratis/">cómo saber si una app para contar calorías es gratis de verdad</a>.</p>
      <h2>Cómo hemos comparado</h2>
      <p>Somos parte interesada: Fotocal es nuestra app. Por eso la comparación sigue reglas que cualquiera puede comprobar:</p>
      <ul>
        <li>De las otras apps solo decimos lo que su fabricante declara en su propia web, con la fecha en que lo leímos ({date}). Las fuentes están enlazadas en cada página una a una.</li>
        <li>No las hemos instalado ni probado una contra otra, así que no decimos cuál acierta más con las calorías.</li>
        <li>La columna de Fotocal se lee del código de la app, no de nuestra publicidad.</li>
        <li>No usamos valoraciones, número de descargas ni opiniones de terceros.</li>
        <li>Cuando una web no dice algo, ponemos una raya, no una suposición.</li>
      </ul>
      <p>Las funciones y los precios cambian. Revisamos estos datos como mucho cada 90 días y apuntamos cada cambio al final de la página.</p>""",
    "en": """      <h2>Which app to choose for what you need</h2>
      <p>No app is best for everyone. One fits how you eat and how you find it easiest to log. These are the differences that really change the decision, from what each maker states on its site as of {date}.</p>
      <h3>If you want to log from a photo without paying</h3>
      <p>Fotocal: the AI food scan is free twice a day, with no card. On MyFitnessPal, Meal Scan is a Premium feature and works in English only. On Yazio, AI tracking is part of Pro. On Cal AI the photo is the product, but its site publishes no price. This is how ours works: the <a href="../features/scan-food/">AI food scanner</a>.</p>
      <h3>If most of what you eat has a barcode</h3>
      <p>Fotocal and Yazio include the barcode scanner in the free plan; on Fotocal it has no limit. Cal AI lists it too. On MyFitnessPal it has been Premium-only since October 2022. More on the <a href="../features/scan-barcode/">free barcode scanner calorie counter</a>.</p>
      <h3>If you would rather say it out loud</h3>
      <p>Fotocal includes one voice log a day in the free plan, in English, Spanish or any other language. On MyFitnessPal, voice logging is Premium and English only. Yazio does not list it for Android, and Cal AI lets you describe a meal by typing, not speaking.</p>
      <h3>If you want something to ask</h3>
      <p>Fotocal includes Coach Kal, an AI chat coach, unlimited on the free plan. None of the other three lists a chat coach on its site.</p>
      <h3>If you care about vitamins, minerals and a weekly summary</h3>
      <p>On MyFitnessPal and on Yazio, micronutrients and weekly summaries are paid. On Fotocal the free plan shows part of them, and Premium opens the full panel and the whole nutrition table of the weekly report. Cal AI does not say.</p>
      <h2>When another app is the better choice</h2>
      <ul>
        <li><strong>If you use an iPhone.</strong> Fotocal exists for Android only. You need another app.</li>
        <li><strong>If you have logged for years in MyFitnessPal or Yazio.</strong> Your history and saved meals are worth something. Switching has a cost, and it only pays if you do not use what you pay for now.</li>
        <li><strong>If you mostly eat packaged products from outside Spain.</strong> Fotocal's strength is Spanish dishes with their real servings. A very large database of other countries' products may serve you better.</li>
        <li><strong>If you want many photo scans a day without paying.</strong> Fotocal's free plan is two AI scans a day; the rest of the day goes in by barcode, by voice or by hand.</li>
      </ul>
      <h2>What each one costs</h2>
      <p>We only give the prices each maker publishes. Fotocal Premium costs €6.99 a month or €34.99 a year, with a 5-day trial; the free plan never expires and asks for no card. MyFitnessPal publishes Premium at $79.99 a year and Premium+ at $99.99. Yazio's price varies by country and no yearly figure was published on the pages we could read. Cal AI publishes no price on its site. Before paying for any of them, check the price on Google Play's subscription screen: that is the one that counts. How to read that small print is in <a href="../blog/app-contar-calorias-gratis/">how to tell if a calorie counting app is really free</a>.</p>
      <h2>How we compared</h2>
      <p>We have a stake: Fotocal is our app. So the comparison follows rules anyone can check:</p>
      <ul>
        <li>About the other apps we only say what the maker states on its own site, with the date we read it ({date}). The sources are linked on each one-to-one page.</li>
        <li>We have not installed and tested them against each other, so we do not say which is more accurate with calories.</li>
        <li>The Fotocal column is read off the app's code, not our marketing.</li>
        <li>We use no ratings, download counts or third-party reviews.</li>
        <li>Where a site does not say something, we put a dash, not a guess.</li>
      </ul>
      <p>Features and prices change. We review these facts at least every 90 days and note each change at the bottom of the page.</p>""",
}

META = {
    "es": {"title": "Mejor app para contar calorías en 2026: 4 comparadas",
           "desc": "Mejor app para contar calorías según lo que necesites: Fotocal, MyFitnessPal, Yazio y Cal AI, con lo que incluye gratis cada una, precios y fecha."},
    "en": {"title": "Best Calorie Counter App in 2026: 4 Compared",
           "desc": "The best calorie counter app for what you need: Fotocal, MyFitnessPal, Yazio and Cal AI, with what each includes for free, prices and the date checked."},
}
H1 = {"es": "Mejor app para contar calorías en 2026: 4 comparadas con fecha y fuentes",
      "en": "Best calorie counter app in 2026: 4 compared, dated and sourced"}
LEAD = {"es": "Cuál es la mejor app para contar calorías depende de cómo apuntes lo que comes. Aquí está lo que incluye cada una, gratis y de pago, según su propio fabricante y con la fecha en que lo comprobamos.",
        "en": "Which is the best calorie counter app depends on how you log what you eat. Here is what each one includes, free and paid, according to its own maker and with the date we checked."}
QUICK = {"es": "No hay una mejor app para contar calorías para todo el mundo. Para apuntar con una foto sin pagar, en Android, Fotocal incluye 2 escaneos con IA al día, 1 registro por voz al día, y código de barras y Coach Kal sin límite, sin tarjeta. Si usas iPhone o ya tienes años de registros en otra app, te conviene otra. Datos de las otras apps: sus propias webs, {date}.",
         "en": "No calorie counter app is best for everyone. To log from a photo without paying, on Android, Fotocal includes 2 AI scans a day, 1 voice log a day, and unlimited barcode scanner and Coach Kal, with no card. If you use an iPhone or already have years of logs in another app, another one suits you better. Other apps' facts: their own sites, {date}."}
