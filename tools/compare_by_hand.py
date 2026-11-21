"""/comparativa/fotocal-vs-contar-a-mano/: counting calories by hand (food
scale, labels, a notebook or a spreadsheet) against counting them with
Fotocal. Written for the GEO round of 21-11-2026. Honest on purpose: by
hand is the more accurate method when you weigh, and the page says so.

Facts used here, and where they come from:
  · free-plan limits and prices: the {{price:…}} tokens (tools/pricing.json)
    and the free limits stated everywhere on the site
  · 218 dishes and foods with Spanish servings: tools/dishes (HAND)
  · where photo error comes from: /blog/photo-calorie-apps-accuracy/
No time-per-meal figures and no accuracy percentages: none are measured."""

SLUG = "fotocal-vs-contar-a-mano"
UPDATED = "2026-11-21"

META = {
    "es": {"title": "Contar calorías a mano o con app: Fotocal frente al papel",
           "desc": "¿Contar calorías a mano o con una app? Lo que gana cada método en precisión, tiempo y coste, cuándo conviene pesar y cuándo basta una foto."},
    "en": {"title": "Count Calories by Hand or With an App? Fotocal vs Paper",
           "desc": "Should you count calories by hand or with an app? What each method wins on accuracy, time and cost, when to weigh, and when a photo is enough."},
}

H1 = {"es": "Contar calorías a mano o con una app: qué gana cada método",
      "en": "Counting calories by hand or with an app: what each method wins"}

LEAD = {"es": "Una comparación honesta entre pesar y apuntar tú mismo y hacer una foto con Fotocal. A mano se gana en precisión; con la app, en tiempo. Aquí está cuándo compensa cada uno.",
        "en": "An honest comparison between weighing and logging it yourself and taking a photo with Fotocal. By hand you win on accuracy; with the app, on time. Here is when each one is worth it."}

QUICK = {"es": "Contar calorías a mano, con báscula de cocina y etiquetas, es el método más preciso si pesas de verdad, y no cuesta nada más que tiempo. Con una app de foto como Fotocal se tarda mucho menos y no hace falta pesar, a cambio de que la ración es una estimación que puedes corregir. Para la mayoría, lo que funciona es mezclar los dos.",
         "en": "Counting calories by hand, with a kitchen scale and labels, is the most accurate method if you really weigh, and it costs nothing but time. With a photo app like Fotocal it takes far less time and you do not need to weigh, in exchange for a portion that is an estimate you can correct. For most people, what works is mixing the two."}

ROWS = {
    "es": [("Precisión", "La más alta si pesas cada ingrediente y usas la etiqueta o una base de datos fiable.", "La app identifica bien el plato; la ración es una estimación. Puedes corregir ingredientes y gramos antes de guardar."),
           ("Tiempo por comida", "Pesar, buscar cada ingrediente y sumar. En un plato de cuchara son muchos pasos.", "Una foto y una revisión rápida. También código de barras y registro por voz."),
           ("Comer fuera", "Difícil: no puedes pesar en un restaurante y hay que estimar a ojo.", "Funciona igual con el plato delante: haces la foto donde estés."),
           ("Platos españoles", "Tienes que desmontar el cocido o la paella en ingredientes y gramos.", "218 platos y alimentos con la ración tal como se sirve en España, sumados ingrediente a ingrediente."),
           ("Coste", "Gratis (una libreta o una hoja de cálculo; la báscula, si no la tienes, aparte).", "Plan gratis sin tarjeta ni caducidad: 2 escaneos con IA y 1 registro por voz al día; código de barras y Coach Kal sin límite. Premium: {{price:month}} al mes o {{price:year}} al año{{offer:note}}."),
           ("Lo que aprendes", "Mucho: pesar unas semanas enseña cuánto es una ración de verdad.", "Menos sobre gramos, más sobre el conjunto del día: lo que te queda y de dónde vienen las calorías.")],
    "en": [("Accuracy", "The highest, if you weigh every ingredient and use the label or a reliable database.", "The app identifies the dish well; the portion is an estimate. You can correct ingredients and grams before saving."),
           ("Time per meal", "Weigh, look up each ingredient and add it up. A stew is a lot of steps.", "One photo and a quick check. Barcode scanning and voice logging too."),
           ("Eating out", "Hard: you cannot weigh in a restaurant, so you estimate by eye.", "Works the same with the plate in front of you: you take the photo wherever you are."),
           ("Spanish dishes", "You have to break a cocido or a paella down into ingredients and grams.", "218 dishes and foods with the portion as served in Spain, added up ingredient by ingredient."),
           ("Cost", "Free (a notebook or a spreadsheet; the scale, if you do not have one, extra).", "Free plan with no card and no expiry: 2 AI scans and 1 voice log a day; barcode scanner and Coach Kal unlimited. Premium: {{price:month}} a month or {{price:year}} a year{{offer:note}}."),
           ("What you learn", "A lot: weighing for a few weeks teaches you what a real portion is.", "Less about grams, more about the whole day: what you have left and where the calories come from.")],
}

BODY = {
    "es": """      <h2>Cuándo es mejor contar a mano</h2>
      <ul><li>Cocinas casi todo en casa y ya tienes báscula de cocina.</li>
          <li>Necesitas la cifra más exacta posible, por ejemplo porque vas a ajustar el déficit de 100 en 100 kcal.</li>
          <li>Estás aprendiendo cuánto es una ración: unas semanas pesando enseñan más que cualquier app.</li>
          <li>No quieres depender de ninguna app ni de límites diarios.</li></ul>
      <p>Si eliges este camino, <a href="../../blog/how-to-count-calories-accurately/">cómo contar calorías con precisión</a> explica qué pesar, cómo leer una etiqueta y qué errores importan de verdad.</p>
      <h2>Cuándo es mejor una app de foto</h2>
      <ul><li>Comes fuera a menudo, o en casa de otros, donde no vas a sacar una báscula.</li>
          <li>Tus comidas son platos mezclados (guisos, arroces, bocadillos) que cuesta desmontar en ingredientes.</li>
          <li>Lo que te hizo abandonar otras veces fue el tiempo de apuntar, no la falta de precisión.</li></ul>
      <p>El error de una foto está sobre todo en la ración, no en reconocer el plato; <a href="../../blog/photo-calorie-apps-accuracy/">¿son precisas las apps de calorías con foto?</a> explica de dónde sale y cómo reducirlo. Y si no tienes báscula, <a href="../../blog/track-calories-without-weighing/">cómo contar calorías sin pesar la comida</a> da las referencias con la mano.</p>
      <h2>Lo que mejor funciona: los dos</h2>
      <p>Pesa en casa una o dos semanas para calibrar el ojo y usa la foto cuando comas fuera o no tengas tiempo. Así la app te ahorra el trabajo y tú sabes cuándo una ración parece demasiado pequeña o grande. Antes de empezar con cualquiera de los dos, la <a href="../../calculadoras/calorias-diarias/">calculadora de calorías diarias</a> te dice cuánto gastas, y la <a href="../../calorias/tabla-de-calorias/">tabla de calorías</a> tiene las cifras de cada plato para consultar a mano.</p>""",
    "en": """      <h2>When counting by hand is better</h2>
      <ul><li>You cook almost everything at home and already own a kitchen scale.</li>
          <li>You need the most exact figure possible, for example because you are adjusting your deficit 100 kcal at a time.</li>
          <li>You are learning what a portion looks like: a few weeks of weighing teaches more than any app.</li>
          <li>You do not want to depend on any app or on daily limits.</li></ul>
      <p>If you go this way, <a href="../../blog/how-to-count-calories-accurately/">how to count calories accurately</a> explains what to weigh, how to read a label and which errors really matter.</p>
      <h2>When a photo app is better</h2>
      <ul><li>You eat out often, or at other people's homes, where you will not get a scale out.</li>
          <li>Your meals are mixed dishes (stews, rice dishes, sandwiches) that are hard to break down into ingredients.</li>
          <li>What made you give up before was the time it took to log, not a lack of accuracy.</li></ul>
      <p>A photo's error is mostly in the portion, not in recognising the dish; <a href="../../blog/photo-calorie-apps-accuracy/">are photo calorie apps accurate?</a> explains where it comes from and how to reduce it. And if you have no scale, <a href="../../blog/track-calories-without-weighing/">how to count calories without weighing food</a> gives the hand references.</p>
      <h2>What works best: both</h2>
      <p>Weigh at home for a week or two to train your eye, and use the photo when you eat out or are short of time. That way the app saves you the work and you can tell when a portion looks too small or too big. Before starting either way, the <a href="../../calculadoras/calorias-diarias/">daily calorie calculator</a> tells you what you burn, and the <a href="../../calorias/tabla-de-calorias/">food calorie chart</a> has each dish's figures to look up by hand.</p>""",
}

FAQ = {
    "es": [("¿Es mejor contar calorías a mano o con una app?", "A mano, con báscula, es más preciso; con una app de foto se tarda mucho menos. Lo que mejor funciona para la mayoría es pesar en casa unas semanas y usar la foto cuando se come fuera."),
           ("¿Son exactas las apps que cuentan calorías con una foto?", "Reconocen bien el plato, pero la ración es una estimación. En Fotocal puedes corregir los ingredientes y los gramos antes de guardar."),
           ("¿Se puede contar calorías sin báscula?", "Sí: con referencias de la mano, con las raciones de una tabla o con una foto. Se pierde algo de precisión, pero es mucho más fácil de mantener."),
           ("¿Cuánto cuesta contar calorías con Fotocal?", "El plan gratis no pide tarjeta ni caduca: 2 escaneos con IA y 1 registro por voz al día; código de barras y Coach Kal sin límite. Premium cuesta {{price:month}} al mes o {{price:year}} al año{{offer:note}}.")],
    "en": [("Is it better to count calories by hand or with an app?", "By hand, with a scale, is more accurate; with a photo app it takes far less time. What works best for most people is weighing at home for a few weeks and using the photo when eating out."),
           ("Are apps that count calories from a photo accurate?", "They recognise the dish well, but the portion is an estimate. In Fotocal you can correct the ingredients and grams before saving."),
           ("Can you count calories without a scale?", "Yes: with hand references, with the servings in a table, or with a photo. You lose some accuracy, but it is much easier to keep up."),
           ("How much does counting calories with Fotocal cost?", "The free plan needs no card and does not expire: 2 AI scans and 1 voice log a day; barcode scanner and Coach Kal unlimited. Premium costs {{price:month}} a month or {{price:year}} a year{{offer:note}}.")],
}
