#!/usr/bin/env python3
"""
Build the four dedicated feature pages and their translations.

WHY A GENERATOR
Each page carries ~50 strings in two languages. Hand-writing eight
half-pages guarantees the EN and ES versions drift — a heading gets
reworded on one side only, a key gets added to one dictionary and not
the other. Emitting the HTML *and* the i18n block from the same table
makes parity structural instead of something you have to remember.

    python3 tools/gen_feature_pages.py

Writes:
    features/<slug>/index.html          (x4)
    tools/feature_pages_i18n.js         (paste-ready dictionary block)

The i18n block is written to tools/ rather than spliced into
assets/js/i18n-pages.js automatically — splicing a generated block into
a hand-edited file is how you lose hand edits.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAY = "https://play.google.com/store/apps/details?id=com.fotokal.app"

PLAY_SVG = (
    '<svg viewBox="0 0 32 34" class="play-badge-icon" aria-hidden="true">'
    '<path d="M2.6 1.2C1.9 1.9 1.5 3 1.5 4.4v25.2c0 1.4.4 2.5 1.1 3.2l.2.2 14.1-14.1v-.6L2.8 1l-.2.2z" fill="#00D7FE"/>'
    '<path d="M21.6 21.6l-4.7-4.7v-.6l4.7-4.7.1.1 5.6 3.2c1.6.9 1.6 2.4 0 3.3l-5.6 3.2-.1.2z" fill="#FFCE00"/>'
    '<path d="M21.7 21.5L16.9 16.7 2.6 31 2.6 31c.5.6 1.4.6 2.4.1l16.7-9.6" fill="#FF3A44"/>'
    '<path d="M21.7 12.1L5 2.5C4 1.9 3.1 2 2.6 2.6l14.3 14.1 4.8-4.6z" fill="#00F076"/></svg>'
)

# ── Icon library ────────────────────────────────────────────────────
# Stroke icons, 24-grid, drawn to match the weight of the ones already
# on the site. Keyed by name so the content table stays readable.
def _i(d):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>')

ICONS = {
    "mic":      _i('<path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M19 10v1a7 7 0 0 1-14 0v-1"/><path d="M12 18v4"/>'),
    "list":     _i('<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>'),
    "scale":    _i('<path d="M12 3v18"/><path d="M5 7h14"/><path d="M8 7l-4 7a4 4 0 0 0 8 0z"/><path d="M16 7l-4 7a4 4 0 0 0 8 0z" transform="translate(4)"/>'),
    "flame":    _i('<path d="M12 22a7 7 0 0 0 7-7c0-4-3-6-4-9-2 2-3 3-3 5 0-2-1-3-2-4-1 3-5 5-5 8a7 7 0 0 0 7 7z"/>'),
    "rings":    _i('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>'),
    "clock":    _i('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 1.9"/>'),
    "pot":      _i('<path d="M4 10h16v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M2 10h20"/><path d="M8 6c0-1.5 1-2 1-3M12 6c0-1.5 1-2 1-3M16 6c0-1.5 1-2 1-3"/>'),
    "slice":    _i('<circle cx="12" cy="12" r="9"/><path d="M12 3v9l6.4 6.4"/>'),
    "leaf":     _i('<path d="M4 20c0-8 5-14 16-15 0 10-5 15-12 15a5 5 0 0 1-4-1z"/><path d="M9 15c2-3 5-5 8-6"/>'),
    "pill":     _i('<path d="M9 3h6M12 3v4"/><path d="M6 12a6 6 0 0 1 12 0v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4z"/><path d="M6 14h12"/>'),
    "camera":   _i('<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>'),
    "gauge":    _i('<path d="M12 21a9 9 0 1 1 9-9"/><path d="M12 12l5-3"/><path d="M12 12v.01"/><path d="M21 12h-3"/>'),
    "layers":   _i('<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>'),
    "wave":     _i('<path d="M2 12c2.5-4 5-4 7.5 0s5 4 7.5 0 5-4 5 0"/><path d="M2 17c2.5-4 5-4 7.5 0s5 4 7.5 0 5-4 5 0" opacity=".55"/>'),
    "alert":    _i('<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'),
    "chat":     _i('<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9.2 9.2 0 0 1-4.1-.9L3 20.5l1.6-4.5A8.4 8.4 0 0 1 3.7 11 8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/>'),
    "users":    _i('<path d="M16 20v-1.5a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4V20"/><circle cx="9" cy="7" r="3.4"/><path d="M22 20v-1.5a4 4 0 0 0-3-3.9"/><path d="M16.5 3.7a4 4 0 0 1 0 7"/>'),
    "barcode":  _i('<path d="M3 6v12M6.5 6v12M10 6v9M13.5 6v12M17 6v9M20.5 6v12"/>'),
    "database": _i('<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>'),
    "infinity": _i('<path d="M7.5 15.5a3.5 3.5 0 1 1 0-7c3 0 3.9 3.5 6.9 3.5a3.5 3.5 0 1 0 0-7c-3 0-3.9 3.5-6.9 3.5"/>'),
    "pencil":   _i('<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>'),
    "globe":    _i('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18z"/>'),
    "bookmark": _i('<path d="M19 21l-7-4.5L5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>'),
    "swap":     _i('<path d="M7 4L3 8l4 4"/><path d="M3 8h13a4 4 0 0 1 0 8h-1"/><path d="M17 20l4-4-4-4" opacity=".55"/>'),
}


# ── Content ─────────────────────────────────────────────────────────
# Every field exists in both "en" and "es". A missing key raises at
# build time rather than shipping a half-translated page.

PAGES = [
{
 "slug": "voice-logging",
 "img": "voice-logging.webp",
 "nav": "nav.voiceLogging",
 "related": ["track-calories-without-weighing", "common-calorie-counting-mistakes", "how-to-count-calories-accurately"],
 "cards": ["pencil", "list", "scale", "flame", "rings", "clock"],
 "en": {
  "navLabel": "Voice logging",
  "metaTitle": "Voice food logging — say what you ate, in any language | Fotocal",
  "metaDesc": "Speak your meal and Fotocal detects the language, transcribes it, identifies every food and quantity, estimates calories and macros, and logs it to any meal. Hands-free, in seconds.",
  "kicker": "Voice logging",
  "h1": 'Just say what you ate — <em class="accent">in any language</em>.',
  "lead": "Tap the microphone and talk normally. Fotocal works out which language you spoke, writes it down, picks out every food and the amount of it, estimates the calories and macros, and files the whole thing under the meal you choose. No typing, no searching, no scrolling a database.",
  "shotAlt": "A microphone with sound waves carrying food across to a phone showing a logged meal",
  "stepsKicker": "How it works",
  "stepsTitle": 'Four seconds of talking, <em class="accent">nothing else</em>.',
  "stepsSub": "The whole point is that you do not have to change how you describe food. Say it the way you would say it to a person.",
  "steps": [
    ("Tap the microphone", "It sits on the logging screen alongside photo and barcode. Nothing to set up, no wake word, no separate account to connect."),
    ("Talk like a person", "“Two scrambled eggs, a slice of rye toast and a flat white.” No app grammar, no unit conversions, no picking items off a list. Ordinary sentences are the input format."),
    ("It works out the language", "You never set one first. Speak Spanish today and English tomorrow, or switch mid-sentence because a dish only has a name in one of them — Fotocal detects what it heard and transcribes in that language."),
    ("Check it, then send it to a meal", "You get the transcript and every item it found with its quantity. Fix anything that looks wrong, choose Breakfast, Lunch, Dinner or Snack, and save."),
  ],
  "getKicker": "What you get",
  "getTitle": "A full entry, not a rough note.",
  "getSub": "Voice logging produces exactly what a photo scan produces — an itemised, editable meal with real numbers behind it.",
  "cards": [
    ("The transcript", "Exactly what it heard, in the language you spoke, so it is always obvious why it logged what it logged."),
    ("Every food, separated", "One line per item rather than one lump. “Chicken salad with dressing” comes back as chicken, salad and dressing, each with its own numbers."),
    ("Real quantities", "“A handful of almonds”, “two slices”, “a large coffee” — spoken amounts are read as amounts and converted into grams or millilitres."),
    ("Calories per item and in total", "Each food carries its own figure, so you can see which part of the meal actually cost you rather than only the final number."),
    ("The full macro split", "Protein, carbs and fat for the entry, added into the day's rings the moment you save it."),
    ("Any meal, any time", "Breakfast, Lunch, Dinner or Snack — including logging last night's dinner over this morning's coffee."),
  ],
  "recKicker": "After you save",
  "recTitle": "It becomes part of the day, immediately.",
  "recBody": "A spoken entry is not a second-class one. The moment you save it, it is the same object as a photographed meal, and everything downstream treats it that way.",
  "recList": [
    "Your calories-left figure recalculates on the spot, along with the protein, carb and fat rings.",
    "Coach Kal can see it. Ask “what should I have for dinner?” and the answer accounts for what you just said you ate.",
    "It feeds the Recommendations tab, which suggests changes based on where your day is actually short rather than on a generic template.",
    "It counts toward your Weekly Report, so a week logged by voice is as complete as a week logged by camera.",
  ],
  "faqTitle": "Questions about voice logging",
  "faq": [
    ("Which languages does it understand?", "It detects the language automatically instead of asking you to choose one, so you can speak whichever language the food actually has a name in. That matters more than it sounds — plenty of dishes have no good translation, and describing them in their own language gives a better result than describing them in English."),
    ("Do I have to phrase it a particular way?", "No. Full sentences, half sentences and lists all work. You do not need to say units, though saying them helps: “200 grams of rice” will always beat “some rice”."),
    ("What if it mishears something?", "Nothing is saved until you tap save. Until then every detected item can be edited, re-weighed or removed, and you can add anything it missed by hand."),
    ("Does it need an internet connection?", "Yes. Both the transcription and the nutrition estimate happen on our side, so voice logging needs a connection to work."),
  ],
  "ctaTitle": "Log your next meal without typing a word.",
  "ctaBody": "Fotocal is free to start, with a 5-day free trial on the paid plans.",
  "relatedTitle": "Keep reading",
  "relatedSub": "Short, practical reads that go deeper on tracking without the busywork.",
  "relatedTitles": ["Track calories without weighing everything", "Common calorie-counting mistakes", "How to count calories accurately"],
 },
 "es": {
  "navLabel": "Registro por voz",
  "metaTitle": "Registro por voz — di lo que has comido, en cualquier idioma | Fotocal",
  "metaDesc": "Habla y Fotocal detecta el idioma, lo transcribe, identifica cada alimento y su cantidad, estima calorías y macros y lo registra en la comida que elijas. Sin manos, en segundos.",
  "kicker": "Registro por voz",
  "h1": 'Solo di lo que has comido — <em class="accent">en cualquier idioma</em>.',
  "lead": "Toca el micrófono y habla con normalidad. Fotocal averigua en qué idioma has hablado, lo transcribe, identifica cada alimento y su cantidad, estima las calorías y los macros y lo guarda en la comida que elijas. Sin escribir, sin buscar, sin recorrer una base de datos.",
  "shotAlt": "Un micrófono cuyas ondas llevan alimentos hasta un móvil que muestra la comida registrada",
  "stepsKicker": "Cómo funciona",
  "stepsTitle": 'Cuatro segundos hablando y <em class="accent">nada más</em>.',
  "stepsSub": "La idea es justo esa: que no tengas que cambiar tu forma de describir la comida. Dílo como se lo dirías a una persona.",
  "steps": [
    ("Toca el micrófono", "Está en la pantalla de registro, junto a la foto y el código de barras. Nada que configurar, ninguna palabra de activación, ninguna cuenta aparte que conectar."),
    ("Habla como hablas", "«Dos huevos revueltos, una tostada de centeno y un café con leche.» Sin fórmulas, sin conversiones de unidades, sin elegir de una lista. Las frases normales son el formato de entrada."),
    ("Detecta el idioma solo", "No eliges ninguno antes. Habla hoy en español y mañana en inglés, o cambia a media frase porque un plato solo tiene nombre en uno de los dos: Fotocal reconoce lo que ha oído y lo transcribe en ese idioma."),
    ("Revísalo y mándalo a una comida", "Verás la transcripción y cada alimento detectado con su cantidad. Corrige lo que no cuadre, elige Desayuno, Comida, Cena o Snack y guárdalo."),
  ],
  "getKicker": "Qué obtienes",
  "getTitle": "Un registro completo, no una nota rápida.",
  "getSub": "El registro por voz produce exactamente lo mismo que un escaneo por foto: una comida detallada, editable y con números reales detrás.",
  "cards": [
    ("La transcripción", "Exactamente lo que ha oído, en el idioma en que hablaste, para que siempre sepas por qué ha registrado lo que ha registrado."),
    ("Cada alimento, por separado", "Una línea por alimento en lugar de un bloque. «Ensalada de pollo con aliño» vuelve como pollo, ensalada y aliño, cada uno con sus números."),
    ("Cantidades de verdad", "«Un puñado de almendras», «dos rebanadas», «un café grande»: las cantidades habladas se leen como cantidades y se convierten a gramos o mililitros."),
    ("Calorías por alimento y totales", "Cada alimento lleva su propia cifra, así que ves qué parte de la comida te ha costado de verdad, no solo el número final."),
    ("El reparto completo de macros", "Proteínas, carbohidratos y grasas del registro, sumados a los anillos del día en cuanto lo guardas."),
    ("Cualquier comida, a cualquier hora", "Desayuno, Comida, Cena o Snack, incluido registrar la cena de anoche con el café de esta mañana."),
  ],
  "recKicker": "Después de guardar",
  "recTitle": "Pasa a formar parte del día al instante.",
  "recBody": "Un registro por voz no es de segunda. En cuanto lo guardas es el mismo objeto que una comida fotografiada, y todo lo que viene después lo trata igual.",
  "recList": [
    "Tus calorías restantes se recalculan al momento, junto con los anillos de proteínas, carbohidratos y grasas.",
    "Coach Kal lo ve. Pregúntale «¿qué ceno hoy?» y la respuesta tendrá en cuenta lo que acabas de decir que has comido.",
    "Alimenta la pestaña de Recomendaciones, que propone cambios según dónde se queda corto tu día de verdad, no según una plantilla genérica.",
    "Cuenta para tu Informe Semanal, así que una semana registrada por voz está tan completa como una registrada con la cámara.",
  ],
  "faqTitle": "Preguntas sobre el registro por voz",
  "faq": [
    ("¿Qué idiomas entiende?", "Detecta el idioma automáticamente en vez de pedirte que elijas uno, así que puedes hablar en el idioma en el que el alimento realmente tiene nombre. Importa más de lo que parece: muchos platos no tienen una buena traducción, y describirlos en su idioma da mejor resultado que describirlos en inglés."),
    ("¿Tengo que decirlo de alguna forma concreta?", "No. Funcionan las frases completas, las frases a medias y las listas. No hace falta decir las unidades, aunque ayuda: «200 gramos de arroz» siempre será mejor que «un poco de arroz»."),
    ("¿Y si entiende mal algo?", "No se guarda nada hasta que tocas guardar. Hasta entonces puedes editar, repesar o eliminar cualquier alimento detectado, y añadir a mano lo que se haya dejado."),
    ("¿Necesita conexión a internet?", "Sí. Tanto la transcripción como la estimación nutricional se hacen en nuestro lado, así que el registro por voz necesita conexión."),
  ],
  "ctaTitle": "Registra tu próxima comida sin escribir una palabra.",
  "ctaBody": "Fotocal es gratis para empezar, con una prueba gratis de 5 días en los planes de pago.",
  "relatedTitle": "Sigue leyendo",
  "relatedSub": "Lecturas breves y prácticas sobre cómo registrar sin que se convierta en trabajo.",
  "relatedTitles": ["Cuenta calorías sin pesarlo todo", "Errores habituales al contar calorías", "Cómo contar calorías con precisión"],
 },
},
{
 "slug": "recipe",
 "img": "recipe.webp",
 "nav": "nav.recipe",
 "related": ["batch-cooking-save-time-eat-better", "meal-prep-for-beginners", "portion-control-simple-tricks"],
 "cards": ["pot", "slice", "rings", "pill", "list", "bookmark"],
 "en": {
  "navLabel": "Recipes",
  "metaTitle": "Recipe nutrition — turn any home recipe into full nutrition | Fotocal",
  "metaDesc": "Add or photograph a recipe and Fotocal works out the total and per-serving calories, macros and micronutrients, then saves it so logging it again takes one tap.",
  "kicker": "Recipes",
  "h1": 'Your own recipes, <em class="accent">fully worked out</em> — once.',
  "lead": "Home cooking is the part most calorie apps quietly give up on. Add a recipe by typing it, pasting it or photographing it, tell Fotocal how many servings it makes, and it works out what the whole dish contains and what one serving contains — calories, macros and micronutrients. Then it saves it, so the next time you cook it, logging costs one tap.",
  "shotAlt": "A finished bowl surrounded by its raw ingredients, with a macro ring and a saved recipe card floating above",
  "stepsKicker": "How it works",
  "stepsTitle": 'Cook it once, <em class="accent">solve it forever</em>.',
  "stepsSub": "The work happens the first time. Every time after that, your own recipe behaves like any other food in the database.",
  "steps": [
    ("Add the recipe", "Type the ingredients out, paste them in from wherever you found them, or photograph a written or printed recipe and let Fotocal read it off the page."),
    ("Say how much it makes", "Set the number of servings, or the finished weight if that is easier to measure. This is the step that turns a pot of food into a portion you can actually log."),
    ("Fotocal does the arithmetic", "Every ingredient is matched and totalled — calories, protein, carbs and fat, plus the micronutrient picture for the finished dish."),
    ("Save it once, reuse it forever", "The recipe goes into your library. Cooking it again is a single tap, and you can log half a serving or two servings without redoing any of the work."),
  ],
  "getKicker": "What you get",
  "getTitle": "The pot and the plate, separately.",
  "getSub": "Knowing what you cooked and knowing what you ate are two different numbers. Fotocal gives you both.",
  "cards": [
    ("Whole-dish nutrition", "The total for the pot, tray or bowl — genuinely useful when you are cooking for a household and want to know what you actually made."),
    ("Per-serving nutrition", "The figure you will actually log, calculated from the servings you set rather than estimated after the fact."),
    ("Macros, split", "Protein, carbs and fat, shown per serving and for the whole dish, so scaling up or down never means recalculating."),
    ("Micronutrients", "The vitamin and mineral picture for the finished dish, not just the headline calorie count."),
    ("Ingredient-level detail", "Every ingredient keeps its own numbers, so you can see which one is carrying the calories before you decide to change anything."),
    ("A reusable library entry", "Home recipes stop being the hard part of tracking. Your Tuesday chilli is logged as fast as a banana."),
  ],
  "recKicker": "Making it better",
  "recTitle": "Change one ingredient, see the whole dish move.",
  "recBody": "Because the recipe is stored as its parts rather than as one number, you can experiment with it instead of just recording it.",
  "recList": [
    "Swap an ingredient or change an amount and the totals — whole dish and per serving — update straight away.",
    "The per-ingredient breakdown shows you where the calories actually sit, which is often not where people assume.",
    "Coach Kal can look at a saved recipe and suggest specific, realistic changes: more protein, less added fat, a higher-fibre swap.",
    "Logged servings feed the same day totals, rings and Weekly Report as everything else — a home-cooked week is as measurable as a packaged one.",
  ],
  "faqTitle": "Questions about recipes",
  "faq": [
    ("Can it read a recipe from a photo?", "Yes. Photograph a handwritten card, a page from a cookbook or a screenshot, and Fotocal reads the ingredients off it. You get the chance to correct anything before it is saved."),
    ("What if I change the recipe later?", "Open it and edit it. Ingredients, amounts and serving count can all be changed, and the totals recalculate. Meals you already logged keep the numbers they were logged with."),
    ("How accurate is it?", "It is as accurate as the ingredient list you give it. “200 g chicken breast” produces a much better result than “some chicken”, and weighing the two or three biggest items is usually enough to make the whole dish reliable."),
    ("Can I log half a serving?", "Yes. Servings are adjustable at the point of logging, so half, one and a half or two all work without touching the saved recipe."),
  ],
  "ctaTitle": "Put your own cooking on the map.",
  "ctaBody": "Fotocal is free to start, with a 5-day free trial on the paid plans.",
  "relatedTitle": "Keep reading",
  "relatedSub": "Practical guides for people who cook their own food.",
  "relatedTitles": ["Batch cooking: save time, eat better", "Meal prep for beginners", "Portion control: simple tricks"],
 },
 "es": {
  "navLabel": "Recetas",
  "metaTitle": "Nutrición de recetas — convierte cualquier receta casera en nutrición completa | Fotocal",
  "metaDesc": "Añade o fotografía una receta y Fotocal calcula las calorías, macros y micronutrientes totales y por ración, y la guarda para que registrarla otra vez sea un toque.",
  "kicker": "Recetas",
  "h1": 'Tus propias recetas, <em class="accent">resueltas del todo</em> — una sola vez.',
  "lead": "La comida casera es justo la parte que casi todas las apps de calorías abandonan en silencio. Añade una receta escribiéndola, pegándola o fotografiándola, dile a Fotocal cuántas raciones salen y calculará qué contiene el plato entero y qué contiene una ración: calorías, macros y micronutrientes. Luego la guarda, y la próxima vez que la cocines registrarla cuesta un toque.",
  "shotAlt": "Un bol terminado rodeado de sus ingredientes crudos, con un anillo de macros y una ficha de receta guardada flotando encima",
  "stepsKicker": "Cómo funciona",
  "stepsTitle": 'Cocina una vez, <em class="accent">resuelto para siempre</em>.',
  "stepsSub": "El trabajo ocurre la primera vez. A partir de ahí, tu receta se comporta como cualquier otro alimento de la base de datos.",
  "steps": [
    ("Añade la receta", "Escribe los ingredientes, pégalos de donde los hayas encontrado o fotografía una receta escrita o impresa y deja que Fotocal la lea."),
    ("Di cuánto sale", "Indica el número de raciones, o el peso final si te resulta más fácil medirlo. Este es el paso que convierte una olla de comida en una ración que puedes registrar."),
    ("Fotocal hace las cuentas", "Cada ingrediente se identifica y se suma: calorías, proteínas, carbohidratos y grasas, más el perfil de micronutrientes del plato terminado."),
    ("Guárdala una vez y reutilízala siempre", "La receta pasa a tu biblioteca. Volver a cocinarla es un solo toque, y puedes registrar media ración o dos sin repetir nada del trabajo."),
  ],
  "getKicker": "Qué obtienes",
  "getTitle": "La olla y el plato, por separado.",
  "getSub": "Saber qué has cocinado y saber qué has comido son dos números distintos. Fotocal te da los dos.",
  "cards": [
    ("Nutrición del plato entero", "El total de la olla, la bandeja o el bol: muy útil cuando cocinas para toda la casa y quieres saber qué has hecho de verdad."),
    ("Nutrición por ración", "La cifra que vas a registrar realmente, calculada a partir de las raciones que has indicado y no estimada a posteriori."),
    ("Macros, desglosados", "Proteínas, carbohidratos y grasas, por ración y del plato entero, para que subir o bajar la cantidad nunca implique recalcular."),
    ("Micronutrientes", "El perfil de vitaminas y minerales del plato terminado, no solo el titular de las calorías."),
    ("Detalle por ingrediente", "Cada ingrediente conserva sus propios números, así que ves cuál carga con las calorías antes de decidir cambiar nada."),
    ("Una entrada reutilizable", "Las recetas caseras dejan de ser la parte difícil. Tu chili de los martes se registra tan rápido como un plátano."),
  ],
  "recKicker": "Mejorarla",
  "recTitle": "Cambia un ingrediente y mira cómo se mueve el plato entero.",
  "recBody": "Como la receta se guarda por sus partes y no como un solo número, puedes experimentar con ella en lugar de limitarte a anotarla.",
  "recList": [
    "Cambia un ingrediente o una cantidad y los totales — del plato entero y por ración — se actualizan al momento.",
    "El desglose por ingrediente te enseña dónde están las calorías de verdad, que casi nunca es donde uno cree.",
    "Coach Kal puede mirar una receta guardada y proponer cambios concretos y realistas: más proteína, menos grasa añadida, un cambio con más fibra.",
    "Las raciones registradas alimentan los mismos totales, anillos e Informe Semanal que todo lo demás: una semana de comida casera es tan medible como una de productos envasados.",
  ],
  "faqTitle": "Preguntas sobre recetas",
  "faq": [
    ("¿Puede leer una receta de una foto?", "Sí. Fotografía una ficha escrita a mano, una página de un libro de cocina o una captura de pantalla y Fotocal leerá los ingredientes. Puedes corregir lo que haga falta antes de guardarla."),
    ("¿Y si luego cambio la receta?", "Ábrela y edítala. Ingredientes, cantidades y número de raciones se pueden cambiar y los totales se recalculan. Las comidas ya registradas conservan los números con los que se registraron."),
    ("¿Cómo de precisa es?", "Tan precisa como la lista de ingredientes que le des. «200 g de pechuga de pollo» da un resultado mucho mejor que «algo de pollo», y pesar los dos o tres ingredientes principales suele bastar para que el plato entero sea fiable."),
    ("¿Puedo registrar media ración?", "Sí. Las raciones se ajustan en el momento de registrar, así que media, una y media o dos funcionan sin tocar la receta guardada."),
  ],
  "ctaTitle": "Pon tu propia cocina en el mapa.",
  "ctaBody": "Fotocal es gratis para empezar, con una prueba gratis de 5 días en los planes de pago.",
  "relatedTitle": "Sigue leyendo",
  "relatedSub": "Guías prácticas para quien se cocina su propia comida.",
  "relatedTitles": ["Batch cooking: gana tiempo y come mejor", "Meal prep para principiantes", "Control de raciones: trucos sencillos"],
 },
},
{
 "slug": "scan-food",
 "img": "scan-food.webp",
 "nav": "nav.scanFood",
 "related": ["how-to-count-calories-accurately", "what-a-balanced-plate-looks-like", "why-micronutrients-matter"],
 "cards": ["camera", "scale", "flame", "pill", "gauge", "layers", "wave", "alert", "chat"],
 "en": {
  "navLabel": "Scan food",
  "metaTitle": "Photo food scanning — one picture, the whole nutrition read | Fotocal",
  "metaDesc": "Photograph any meal and Fotocal identifies the dish and ingredients, estimates the portion and returns calories, macros, micronutrients, a health score, NOVA level, glycemic load, allergens and a healthier swap.",
  "kicker": "Photo scan",
  "h1": 'Point the camera. <em class="accent">Get the whole plate</em>.',
  "lead": "One photograph is the entire input. Fotocal identifies the dish and the ingredients in it, estimates how much is on the plate, and hands back a complete read: calories, macros, around eight micronutrients, a health score, how processed the food is, its glycemic load, any allergens it can see, a short summary from your coach and one realistic swap. Nothing is saved until you say so.",
  "shotAlt": "A phone photographing a balanced bowl, with nutrition badges rising out of the plate",
  "stepsKicker": "How it works",
  "stepsTitle": 'A photo in, <em class="accent">a full picture out</em>.',
  "stepsSub": "Home-cooked, restaurant, takeaway or last night's leftovers — the input is always the same, and so is the effort.",
  "steps": [
    ("Photograph the plate", "Whatever is in front of you, however it was made. No good lighting required, no arranging the food, no reference coin next to the bowl."),
    ("The AI reads it", "It identifies the dish, separates out the ingredients it can see, and estimates the portion from what is on the plate."),
    ("Move the portion to match", "The estimate is a starting point, not a verdict. Drag it to what you actually ate — or split the dish between the people sharing it and log only your share."),
    ("Correct anything, then save", "Every detected ingredient can be edited, swapped or removed, and you can add what the camera could not see. It is a draft until you save it."),
  ],
  "getKicker": "What you get",
  "getTitle": "Nine things, from one photograph.",
  "getSub": "Most trackers stop at a calorie count. The useful part is usually everything after it.",
  "cards": [
    ("The dish and its ingredients", "Named individually rather than as one blob, so you can see what it thinks it is looking at."),
    ("A portion estimate you can move", "Read from the plate rather than assumed from an average serving — and adjustable in one gesture if it is off."),
    ("Calories and macros", "The headline figure plus the protein, carb and fat split behind it."),
    ("Around eight micronutrients", "Fibre, sugar, sodium, saturated fat and the rest of the picture most calorie trackers leave out entirely."),
    ("A health score", "One number for how the meal stacks up overall, so you can compare two dishes without reading two tables."),
    ("NOVA processing level", "How processed the food is — a genuinely different question from how many calories it holds, and one that matters over months."),
    ("Glycemic load", "How much this particular portion is likely to move your blood sugar, based on the amount actually in front of you."),
    ("Allergens", "Flagged from the ingredients it detects, so a shared or unfamiliar dish is not a guess."),
    ("A coach summary and one swap", "A plain-language read on the meal, plus a single specific change that would improve it — not a lecture, one suggestion."),
  ],
  "recKicker": "How the advice works",
  "recTitle": "The suggestion knows what else you ate today.",
  "recBody": "A swap is only worth anything if it fits the rest of your day. Fotocal's recommendations are generated against your actual goals and your actual diary, not against a general idea of healthy eating.",
  "recList": [
    "Your targets come first: the same meal gets different advice if you are cutting, maintaining or building.",
    "It reads the rest of the day. If you are already short on protein at 8pm, the swap will be about protein.",
    "It suggests one change, not a rewrite. Something you could realistically do next time, phrased as a choice rather than a rule.",
    "Everything you scan feeds the Recommendations tab and your Weekly Report, so the advice gets more specific the longer you log.",
  ],
  "faqTitle": "Questions about photo scanning",
  "faq": [
    ("How accurate is a photo estimate?", "It is an estimate, and we would rather say so than pretend otherwise. For everyday tracking it is close enough to be useful, and the portion slider closes most of the remaining gap. If a meal really matters, weigh the main component and adjust."),
    ("What if it gets an ingredient wrong?", "Fix it. Every detected item is editable before you save — change it, re-weigh it, delete it, or add something it missed. Corrections take a couple of seconds and the totals update as you go."),
    ("Does it work on restaurant and mixed dishes?", "Yes, and that is where it earns its keep. A curry, a stir-fry or a plate of tapas has no barcode and no label, which is exactly the situation database-search apps handle worst."),
    ("Is anything logged automatically?", "No. A scan produces a draft. Nothing enters your diary, your rings or your totals until you tap save."),
  ],
  "ctaTitle": "Photograph your next meal and see the whole thing.",
  "ctaBody": "Fotocal is free to start, with a 5-day free trial on the paid plans.",
  "relatedTitle": "Keep reading",
  "relatedSub": "The thinking behind the numbers on the screen.",
  "relatedTitles": ["How to count calories accurately", "What a balanced plate looks like", "Why micronutrients matter"],
 },
 "es": {
  "navLabel": "Escanear comida",
  "metaTitle": "Escaneo de comida por foto — una imagen, la lectura nutricional completa | Fotocal",
  "metaDesc": "Fotografía cualquier comida y Fotocal identifica el plato y los ingredientes, estima la ración y devuelve calorías, macros, micronutrientes, puntuación de salud, nivel NOVA, carga glucémica, alérgenos y una alternativa más sana.",
  "kicker": "Escaneo por foto",
  "h1": 'Apunta con la cámara. <em class="accent">Llévate el plato entero</em>.',
  "lead": "Una fotografía es toda la entrada. Fotocal identifica el plato y los ingredientes que lo componen, estima cuánto hay servido y devuelve una lectura completa: calorías, macros, unos ocho micronutrientes, una puntuación de salud, el nivel de procesamiento del alimento, su carga glucémica, los alérgenos que detecta, un resumen breve de tu coach y una alternativa realista. No se guarda nada hasta que tú lo digas.",
  "shotAlt": "Un móvil fotografiando un bol equilibrado, con insignias nutricionales saliendo del plato",
  "stepsKicker": "Cómo funciona",
  "stepsTitle": 'Entra una foto, <em class="accent">sale el cuadro completo</em>.',
  "stepsSub": "Casero, de restaurante, para llevar o las sobras de anoche: la entrada siempre es la misma y el esfuerzo también.",
  "steps": [
    ("Fotografía el plato", "Lo que tengas delante, esté hecho como esté. Sin buena luz, sin colocar la comida, sin poner una moneda al lado como referencia."),
    ("La IA lo lee", "Identifica el plato, separa los ingredientes que ve y estima la ración a partir de lo que hay servido."),
    ("Ajusta la ración", "La estimación es un punto de partida, no una sentencia. Muévela hasta lo que realmente has comido, o reparte el plato entre las personas que lo comparten y registra solo tu parte."),
    ("Corrige lo que haga falta y guarda", "Puedes editar, cambiar o quitar cualquier ingrediente detectado, y añadir lo que la cámara no podía ver. Es un borrador hasta que lo guardas."),
  ],
  "getKicker": "Qué obtienes",
  "getTitle": "Nueve cosas, de una sola foto.",
  "getSub": "Casi todas las apps se quedan en el recuento de calorías. Lo útil suele ser todo lo que viene después.",
  "cards": [
    ("El plato y sus ingredientes", "Nombrados uno a uno y no como un bloque, para que veas qué cree que está mirando."),
    ("Una ración estimada que puedes mover", "Leída del plato en vez de supuesta a partir de una ración media, y ajustable con un gesto si no cuadra."),
    ("Calorías y macros", "La cifra principal más el reparto de proteínas, carbohidratos y grasas que hay detrás."),
    ("Unos ocho micronutrientes", "Fibra, azúcar, sodio, grasas saturadas y el resto del cuadro que la mayoría de contadores de calorías ignora por completo."),
    ("Una puntuación de salud", "Un solo número de cómo queda la comida en conjunto, para comparar dos platos sin leer dos tablas."),
    ("Nivel de procesamiento NOVA", "Cuán procesado está el alimento: una pregunta muy distinta de cuántas calorías tiene, y que pesa a lo largo de los meses."),
    ("Carga glucémica", "Cuánto es probable que esta ración concreta te mueva el azúcar en sangre, según la cantidad que tienes delante."),
    ("Alérgenos", "Señalados a partir de los ingredientes que detecta, para que un plato compartido o desconocido no sea una apuesta."),
    ("Un resumen del coach y un cambio", "Una lectura en lenguaje llano de la comida y un único cambio concreto que la mejoraría. No es un sermón: es una sugerencia."),
  ],
  "recKicker": "Cómo funcionan los consejos",
  "recTitle": "La sugerencia sabe qué más has comido hoy.",
  "recBody": "Un cambio solo sirve si encaja con el resto de tu día. Las recomendaciones de Fotocal se generan con tus objetivos reales y tu diario real, no con una idea general de comer sano.",
  "recList": [
    "Tus objetivos van primero: la misma comida recibe un consejo distinto si estás en déficit, en mantenimiento o ganando masa.",
    "Lee el resto del día. Si a las ocho de la tarde vas corto de proteína, el cambio irá de proteína.",
    "Propone un cambio, no una reescritura. Algo que podrías hacer de verdad la próxima vez, planteado como una opción y no como una norma.",
    "Todo lo que escaneas alimenta la pestaña de Recomendaciones y tu Informe Semanal, así que el consejo se vuelve más concreto cuanto más registras.",
  ],
  "faqTitle": "Preguntas sobre el escaneo por foto",
  "faq": [
    ("¿Cuánta precisión tiene una estimación por foto?", "Es una estimación, y preferimos decirlo a fingir lo contrario. Para el seguimiento del día a día es lo bastante buena como para ser útil, y el control de ración cierra casi toda la diferencia que queda. Si una comida importa de verdad, pesa el ingrediente principal y ajústalo."),
    ("¿Y si se equivoca con un ingrediente?", "Lo corriges. Todo lo detectado es editable antes de guardar: cámbialo, repésalo, bórralo o añade lo que se haya dejado. Corregir lleva un par de segundos y los totales se actualizan sobre la marcha."),
    ("¿Funciona con platos de restaurante y platos mezclados?", "Sí, y ahí es donde más se nota. Un curry, un salteado o unas tapas no tienen código de barras ni etiqueta, que es justo la situación que peor resuelven las apps de buscar en una base de datos."),
    ("¿Se registra algo automáticamente?", "No. Un escaneo produce un borrador. No entra nada en tu diario, en tus anillos ni en tus totales hasta que tocas guardar."),
  ],
  "ctaTitle": "Fotografía tu próxima comida y velo todo.",
  "ctaBody": "Fotocal es gratis para empezar, con una prueba gratis de 5 días en los planes de pago.",
  "relatedTitle": "Sigue leyendo",
  "relatedSub": "Lo que hay detrás de los números de la pantalla.",
  "relatedTitles": ["Cómo contar calorías con precisión", "Qué aspecto tiene un plato equilibrado", "Por qué importan los micronutrientes"],
 },
},
{
 "slug": "scan-barcode",
 "img": "scan-barcode.webp",
 "nav": "nav.scanBarcode",
 "related": ["how-to-read-nutrition-labels", "how-to-build-a-healthy-grocery-list", "added-sugar-vs-natural-sugar"],
 "cards": ["barcode", "flame", "rings", "list", "alert", "infinity"],
 "en": {
  "navLabel": "Scan barcode",
  "metaTitle": "Barcode scanning — instant nutrition for packaged food | Fotocal",
  "metaDesc": "Scan any packaged product's barcode for instant calories, macros, ingredients and allergens from a large product database. Free, unlimited, and it never uses your AI scan quota.",
  "kicker": "Barcode scan",
  "h1": 'Packaged food, <em class="accent">already solved</em>.',
  "lead": "Point the camera at the barcode on any packet and the nutrition comes straight back — calories, macros, the ingredient list and the allergens, read from a large product database rather than estimated. It is free, it is unlimited, and it never touches your AI scan allowance.",
  "shotAlt": "A phone scanning the barcode on a packet, with the product's nutrition appearing beside it",
  "stepsKicker": "How it works",
  "stepsTitle": 'Four seconds, <em class="accent">most of them holding the packet</em>.',
  "stepsSub": "Anything with a barcode is the easy case. There is no estimating involved — the numbers come off the product record.",
  "steps": [
    ("Point at the barcode", "Anywhere on the pack, any angle you can hold it at. It reads as soon as the code is in frame."),
    ("The product comes back", "Name, brand and the full nutrition record, pulled from the database rather than worked out from a photo."),
    ("Set the amount", "Per 100 g, per the serving printed on the label, or the amount you are actually having. Half a packet is half a packet."),
    ("Log it to a meal", "Straight into Breakfast, Lunch, Dinner or Snack, where it joins everything else in the day."),
  ],
  "getKicker": "What you get",
  "getTitle": "Label numbers, without reading the label.",
  "getSub": "Everything on the back of the pack, in a form you can actually compare and track.",
  "cards": [
    ("Instant identification", "The product recognised by its barcode, so there is no searching, no near-miss database entries and no picking between eight versions of the same yoghurt."),
    ("Calories", "The headline number, for the amount you set rather than only per 100 g."),
    ("Full macro breakdown", "Protein, carbs and fat, straight into the day's rings."),
    ("The ingredient list", "What is actually in it, in the order it is in it — which is often more revealing than the calorie count."),
    ("Allergens", "Called out from the product record, so you are not scanning small print in a supermarket aisle."),
    ("Free and unlimited", "Barcode scanning is not metered and does not consume an AI scan. Scan a whole shopping basket if you want to — it costs nothing."),
  ],
  "recKicker": "Where it earns its keep",
  "recTitle": "Two products, one decision, four seconds.",
  "recBody": "The real use for barcode scanning is not logging — it is deciding. Standing in an aisle with a packet in each hand is the moment a nutrition label is worth something, and it is also the moment nobody reads one.",
  "recList": [
    "Scan both and compare the actual numbers instead of the marketing on the front of the pack.",
    "Because it is unlimited and free, there is no reason not to scan something you are only considering.",
    "Anything you do log feeds the same day totals, rings and Weekly Report as a photographed meal.",
    "Coach Kal can see your logged packaged foods, so “why is my sodium high this week?” has a real answer rather than a guess.",
  ],
  "faqTitle": "Questions about barcode scanning",
  "faq": [
    ("Is barcode scanning included in the free plan?", "Yes, and it is unlimited. It is not a trial feature, it is not capped per day, and it does not use up AI scans."),
    ("Does it use my AI scan quota?", "No. Barcode lookups and AI photo scans are completely separate. Scanning a hundred barcodes leaves your AI scans untouched."),
    ("What if a product is not in the database?", "It happens, particularly with small local brands. You can photograph the food instead, or add the item by hand from the label — either way you are not stuck."),
    ("Does it work outside my country?", "The database is international and covers a very large range of packaged products, so most supermarket items scan wherever you are. Regional and own-brand products are the most likely gaps."),
  ],
  "ctaTitle": "Scan the packet. Skip the small print.",
  "ctaBody": "Fotocal is free to start, with a 5-day free trial on the paid plans.",
  "relatedTitle": "Keep reading",
  "relatedSub": "How to get more out of what is printed on the pack.",
  "relatedTitles": ["How to read nutrition labels", "How to build a healthy grocery list", "Added sugar vs natural sugar"],
 },
 "es": {
  "navLabel": "Escanear código",
  "metaTitle": "Escaneo de código de barras — nutrición instantánea de productos envasados | Fotocal",
  "metaDesc": "Escanea el código de barras de cualquier producto envasado y obtén al instante calorías, macros, ingredientes y alérgenos de una gran base de datos. Gratis, ilimitado y sin gastar tu cuota de IA.",
  "kicker": "Escaneo de código",
  "h1": 'Los productos envasados, <em class="accent">ya resueltos</em>.',
  "lead": "Apunta con la cámara al código de barras de cualquier paquete y la nutrición vuelve al instante: calorías, macros, la lista de ingredientes y los alérgenos, leídos de una gran base de datos de productos en lugar de estimados. Es gratis, es ilimitado y nunca toca tu cuota de escaneos con IA.",
  "shotAlt": "Un móvil escaneando el código de barras de un paquete, con la nutrición del producto apareciendo al lado",
  "stepsKicker": "Cómo funciona",
  "stepsTitle": 'Cuatro segundos, <em class="accent">casi todos sujetando el paquete</em>.',
  "stepsSub": "Todo lo que lleva código de barras es el caso fácil. Aquí no se estima nada: los números salen de la ficha del producto.",
  "steps": [
    ("Apunta al código", "En cualquier parte del paquete y en cualquier ángulo en que puedas sujetarlo. Lo lee en cuanto el código entra en cuadro."),
    ("Aparece el producto", "Nombre, marca y la ficha nutricional completa, sacada de la base de datos y no deducida de una foto."),
    ("Indica la cantidad", "Por 100 g, por la ración impresa en la etiqueta o por lo que realmente vas a tomar. Medio paquete es medio paquete."),
    ("Regístralo en una comida", "Directo a Desayuno, Comida, Cena o Snack, donde se suma a todo lo demás del día."),
  ],
  "getKicker": "Qué obtienes",
  "getTitle": "Los números de la etiqueta, sin leer la etiqueta.",
  "getSub": "Todo lo que hay en la parte de atrás del paquete, en un formato que sí puedes comparar y registrar.",
  "cards": [
    ("Identificación instantánea", "El producto reconocido por su código: sin buscar, sin entradas parecidas pero no iguales y sin elegir entre ocho versiones del mismo yogur."),
    ("Calorías", "La cifra principal, para la cantidad que tú indiques y no solo por 100 g."),
    ("Desglose completo de macros", "Proteínas, carbohidratos y grasas, directos a los anillos del día."),
    ("La lista de ingredientes", "Lo que lleva de verdad y en el orden en que lo lleva, que a menudo dice más que el recuento de calorías."),
    ("Alérgenos", "Señalados desde la ficha del producto, para que no tengas que leer letra pequeña en mitad de un pasillo."),
    ("Gratis e ilimitado", "El escaneo de códigos no se mide ni consume un escaneo con IA. Escanea la compra entera si quieres: no cuesta nada."),
  ],
  "recKicker": "Dónde vale de verdad",
  "recTitle": "Dos productos, una decisión, cuatro segundos.",
  "recBody": "El uso real del escaneo de códigos no es registrar: es decidir. Estar en un pasillo con un paquete en cada mano es el momento en que una etiqueta nutricional vale algo, y también el momento en que nadie la lee.",
  "recList": [
    "Escanea los dos y compara los números reales en vez del marketing de la parte de delante.",
    "Como es gratis e ilimitado, no hay ningún motivo para no escanear algo que solo te estás planteando.",
    "Todo lo que sí registres alimenta los mismos totales, anillos e Informe Semanal que una comida fotografiada.",
    "Coach Kal ve los productos envasados que registras, así que «¿por qué llevo tanto sodio esta semana?» tiene una respuesta real y no una suposición.",
  ],
  "faqTitle": "Preguntas sobre el escaneo de códigos",
  "faq": [
    ("¿El escaneo de códigos entra en el plan gratuito?", "Sí, y es ilimitado. No es una función de prueba, no tiene tope diario y no gasta escaneos con IA."),
    ("¿Consume mi cuota de escaneos con IA?", "No. Las búsquedas por código y los escaneos con IA son cosas totalmente separadas. Escanear cien códigos deja tus escaneos con IA intactos."),
    ("¿Y si un producto no está en la base de datos?", "Pasa, sobre todo con marcas locales pequeñas. Puedes fotografiar el alimento o añadirlo a mano desde la etiqueta: en cualquier caso no te quedas bloqueado."),
    ("¿Funciona fuera de mi país?", "La base de datos es internacional y cubre una gama muy amplia de productos envasados, así que la mayoría de artículos de supermercado se escanean estés donde estés. Los productos regionales y de marca blanca son los huecos más probables."),
  ],
  "ctaTitle": "Escanea el paquete. Ahórrate la letra pequeña.",
  "ctaBody": "Fotocal es gratis para empezar, con una prueba gratis de 5 días en los planes de pago.",
  "relatedTitle": "Sigue leyendo",
  "relatedSub": "Cómo sacarle más a lo que viene impreso en el paquete.",
  "relatedTitles": ["Cómo leer las etiquetas nutricionales", "Cómo hacer una lista de la compra sana", "Azúcar añadido vs azúcar natural"],
 },
},
]


# ── Build ───────────────────────────────────────────────────────────

def esc(s):
    """Escape for an HTML attribute value."""
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def check(page):
    """Both languages must define exactly the same fields, and every list
    field must be the same length. Catches a half-finished translation at
    build time instead of at read time."""
    en, es = page["en"], page["es"]
    if set(en) != set(es):
        raise SystemExit(f"{page['slug']}: field mismatch {set(en) ^ set(es)}")
    for k, v in en.items():
        if isinstance(v, list) and len(v) != len(es[k]):
            raise SystemExit(f"{page['slug']}.{k}: {len(v)} EN vs {len(es[k])} ES")
    if len(en["cards"]) != len(page["cards"]):
        raise SystemExit(f"{page['slug']}: {len(en['cards'])} cards but {len(page['cards'])} icons")
    if len(en["relatedTitles"]) != len(page["related"]):
        raise SystemExit(f"{page['slug']}: related titles/slugs mismatch")


def i18n_entries(page):
    """Flatten one page's content into dictionary keys, EN and ES together."""
    p = "fp." + page["slug"] + "."
    out = {"en": {}, "es": {}}
    for lang in ("en", "es"):
        d, o = page[lang], out[lang]
        for k in ("kicker", "h1", "lead", "shotAlt", "stepsKicker", "stepsTitle", "stepsSub",
                  "getKicker", "getTitle", "getSub", "recKicker", "recTitle", "recBody",
                  "faqTitle", "ctaTitle", "ctaBody", "relatedTitle", "relatedSub", "navLabel"):
            o[p + k] = d[k]
        for i, (h, b) in enumerate(d["steps"], 1):
            o[p + "s%dt" % i] = h
            o[p + "s%db" % i] = b
        for i, (h, b) in enumerate(d["cards"], 1):
            o[p + "c%dt" % i] = h
            o[p + "c%db" % i] = b
        for i, t in enumerate(d["recList"], 1):
            o[p + "r%d" % i] = t
        for i, (q, a) in enumerate(d["faq"], 1):
            o[p + "q%d" % i] = q
            o[p + "a%d" % i] = a
        for i, t in enumerate(d["relatedTitles"], 1):
            o[p + "rel%d" % i] = t
    return out


def build_html(page):
    slug, en, p = page["slug"], page["en"], "fp." + page["slug"] + "."
    url = "https://getfotocal.com/features/%s/" % slug

    steps = "\n".join(
        '          <div class="sp-step reveal"%s>\n'
        '            <div class="sp-step-n">%d</div>\n'
        '            <h3 data-i18n="%ss%dt">%s</h3>\n'
        '            <p data-i18n="%ss%db">%s</p>\n'
        '          </div>' % (
            ' style="--rd:.%ds"' % i if i else "", i + 1, p, i + 1, esc_text(en["steps"][i][0]),
            p, i + 1, esc_text(en["steps"][i][1]))
        for i in range(len(en["steps"])))

    cards = "\n".join(
        '          <div class="sp-card reveal"%s>\n'
        '            <div class="sp-card-ico">%s</div>\n'
        '            <h3 data-i18n="%sc%dt">%s</h3>\n'
        '            <p data-i18n="%sc%db">%s</p>\n'
        '          </div>' % (
            ' style="--rd:.%ds"' % (i % 3) if i % 3 else "", ICONS[page["cards"][i]],
            p, i + 1, esc_text(en["cards"][i][0]), p, i + 1, esc_text(en["cards"][i][1]))
        for i in range(len(en["cards"])))

    reclist = "\n".join(
        '            <li data-i18n="%sr%d">%s</li>' % (p, i + 1, esc_text(en["recList"][i]))
        for i in range(len(en["recList"])))

    faq = "\n".join(
        '          <details class="faq-item reveal">\n'
        '            <summary><span data-i18n="%sq%d">%s</span><i class="faq-plus" aria-hidden="true"></i></summary>\n'
        '            <p data-i18n="%sa%d">%s</p>\n'
        '          </details>' % (p, i + 1, esc_text(en["faq"][i][0]), p, i + 1, esc_text(en["faq"][i][1]))
        for i in range(len(en["faq"])))

    related = "\n".join(
        '          <a class="fc-rcard reveal" href="../../blog/%s/">\n'
        '            <span class="fc-rkicker" data-i18n="feat.article">Article</span>\n'
        '            <span class="fc-rtitle" data-i18n="%srel%d">%s</span>\n'
        '            <span class="fc-rarrow" data-i18n="feat.read">Read →</span>\n'
        '          </a>' % (page["related"][i], p, i + 1, esc_text(en["relatedTitles"][i]))
        for i in range(len(page["related"])))

    # FAQPage structured data, built from the same source as the visible FAQ
    faq_ld = ",\n".join(
        '    {\n      "@type": "Question",\n      "name": %s,\n'
        '      "acceptedAnswer": { "@type": "Answer", "text": %s }\n    }' % (json_str(q), json_str(a))
        for q, a in en["faq"])

    return TEMPLATE.format(
        slug=slug, url=url, p=p,
        metaTitle=esc(en["metaTitle"]), metaDesc=esc(en["metaDesc"]),
        kicker=esc_text(en["kicker"]), h1=en["h1"], lead=esc_text(en["lead"]),
        img=page["img"], shotAlt=esc(en["shotAlt"]),
        stepsKicker=esc_text(en["stepsKicker"]), stepsTitle=en["stepsTitle"], stepsSub=esc_text(en["stepsSub"]),
        getKicker=esc_text(en["getKicker"]), getTitle=esc_text(en["getTitle"]), getSub=esc_text(en["getSub"]),
        recKicker=esc_text(en["recKicker"]), recTitle=esc_text(en["recTitle"]), recBody=esc_text(en["recBody"]),
        faqTitle=esc_text(en["faqTitle"]),
        ctaTitle=esc_text(en["ctaTitle"]), ctaBody=esc_text(en["ctaBody"]),
        relatedTitle=esc_text(en["relatedTitle"]), relatedSub=esc_text(en["relatedSub"]),
        steps=steps, cards=cards, reclist=reclist, faq=faq, related=related,
        faq_ld=faq_ld, play=PLAY, playsvg=PLAY_SVG,
    )


def esc_text(s):
    """Escape for HTML text content (leaves nothing unescaped that matters)."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)


TEMPLATE = '''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{metaTitle}</title>
  <meta name="description" content="{metaDesc}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{url}">
  <link rel="alternate" hreflang="es" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{metaTitle}">
  <meta property="og:description" content="{metaDesc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://getfotocal.com/assets/img/features/{img}">
  <meta name="twitter:card" content="summary_large_image">

  <meta name="theme-color" content="#FDF9F0">

  <link rel="icon" type="image/png" href="../../assets/img/logo.png">
  <link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg">
  <link rel="apple-touch-icon" href="../../assets/img/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/site.css">
  <link rel="stylesheet" href="../../assets/css/home.css">
  <link rel="stylesheet" href="../../assets/css/pages.css">
  <link rel="stylesheet" href="../../assets/css/sections.css">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{faq_ld}
    ]
  }}
  </script>
</head>
<body>

  <div id="site-nav"></div>

  <main id="main">

    <!-- ═══════════════════ HERO ═══════════════════ -->
    <section class="fp-hero">
      <div class="container">
        <div class="fp-hero-copy">
          <span class="kicker reveal" data-i18n="{p}kicker">{kicker}</span>
          <h1 class="reveal" data-i18n-html="{p}h1">{h1}</h1>
          <p class="lead reveal" data-i18n="{p}lead">{lead}</p>
          <div class="fp-hero-actions reveal">
            <a class="play-badge" href="{play}" target="_blank" rel="noopener noreferrer" aria-label="Get Fotocal on Google Play">
              {playsvg}
              <span class="play-badge-text"><small data-i18n="cta.badgeTop">GET IT ON</small><strong>Google Play</strong></span>
            </a>
            <a class="btn btn-outline" href="../" data-i18n="sp.allFeatures">All features</a>
          </div>
        </div>

        <figure class="fp-shot reveal">
          <span class="fp-shot-glow" aria-hidden="true"></span>
          <span class="shot-card">
            <img src="../../assets/img/features/{img}" width="1400" height="933"
                 fetchpriority="high" decoding="async"
                 alt="{shotAlt}" data-i18n-alt="{p}shotAlt">
          </span>
        </figure>
      </div>
    </section>

    <!-- ═══════════════════ HOW IT WORKS ═══════════════════ -->
    <section class="section section-alt">
      <div class="container">
        <div class="text-center">
          <span class="kicker reveal" data-i18n="{p}stepsKicker">{stepsKicker}</span>
          <h2 class="section-title reveal" data-i18n-html="{p}stepsTitle">{stepsTitle}</h2>
          <p class="section-sub mx-auto reveal" data-i18n="{p}stepsSub">{stepsSub}</p>
        </div>
        <div class="sp-steps">
{steps}
        </div>
      </div>
    </section>

    <!-- ═══════════════════ WHAT YOU GET ═══════════════════ -->
    <section class="section">
      <div class="container">
        <div class="text-center">
          <span class="kicker reveal" data-i18n="{p}getKicker">{getKicker}</span>
          <h2 class="section-title reveal" data-i18n="{p}getTitle">{getTitle}</h2>
          <p class="section-sub mx-auto reveal" data-i18n="{p}getSub">{getSub}</p>
        </div>
        <div class="sp-cards">
{cards}
        </div>
      </div>
    </section>

    <!-- ═══════════════════ HOW THE ADVICE WORKS ═══════════════════ -->
    <section class="section section-alt">
      <div class="container-narrow">
        <div class="fp-rec reveal">
          <span class="pill" data-i18n="{p}recKicker">{recKicker}</span>
          <h2 data-i18n="{p}recTitle">{recTitle}</h2>
          <p data-i18n="{p}recBody">{recBody}</p>
          <ul class="check-list">
{reclist}
          </ul>
        </div>
      </div>
    </section>

    <!-- ═══════════════════ FAQ ═══════════════════ -->
    <section class="section">
      <div class="container-narrow">
        <div class="text-center">
          <h2 class="section-title reveal" data-i18n="{p}faqTitle">{faqTitle}</h2>
        </div>
        <div class="faq-list">
{faq}
        </div>
      </div>
    </section>

    <!-- ═══════════════════ RELATED READING ═══════════════════ -->
    <section class="section section-alt">
      <div class="container">
        <div class="text-center">
          <span class="kicker reveal" data-i18n="feat.guides">Guides</span>
          <h2 class="section-title reveal" data-i18n="{p}relatedTitle">{relatedTitle}</h2>
          <p class="section-sub mx-auto reveal" data-i18n="{p}relatedSub">{relatedSub}</p>
        </div>
        <div class="fc-related">
{related}
        </div>
      </div>
    </section>

    <!-- ═══════════════════ FINAL CTA ═══════════════════ -->
    <section class="final-cta">
      <div class="container">
        <div class="final-inner reveal">
          <h2 data-i18n="{p}ctaTitle">{ctaTitle}</h2>
          <p data-i18n="{p}ctaBody">{ctaBody}</p>
          <a class="play-badge play-badge-light" href="{play}" target="_blank" rel="noopener noreferrer" style="margin-inline:auto;display:inline-flex" aria-label="Get Fotocal on Google Play">
            {playsvg}
            <span class="play-badge-text"><small data-i18n="cta.badgeTop">GET IT ON</small><strong>Google Play</strong></span>
          </a>
        </div>
      </div>
    </section>

  </main>

  <div id="site-footer"></div>

  <script src="../../assets/js/i18n.js"></script>
  <script src="../../assets/js/i18n-pages.js"></script>
  <script src="../../assets/js/layout.js" data-page="features"></script>
  <script src="../../assets/js/main.js"></script>
</body>
</html>
'''


def main():
    all_i18n = {"en": {}, "es": {}}
    for page in PAGES:
        check(page)
        d = os.path.join(ROOT, "features", page["slug"])
        os.makedirs(d, exist_ok=True)
        html = build_html(page)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        e = i18n_entries(page)
        for lang in ("en", "es"):
            all_i18n[lang].update(e[lang])
        print("wrote features/%s/index.html  (%d keys)" % (page["slug"], len(e["en"])))

    if set(all_i18n["en"]) != set(all_i18n["es"]):
        raise SystemExit("key parity broken")

    def block(lang):
        lines = []
        for k in all_i18n["en"]:           # EN order, so the two halves line up
            v = all_i18n[lang][k]
            lines.append('      %s: %s,' % (json_str(k), json_str(v)))
        return "\n".join(lines)

    out = os.path.join(ROOT, "tools", "feature_pages_i18n.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("/* GENERATED by tools/gen_feature_pages.py — paste into assets/js/i18n-pages.js */\n\n")
        f.write("/* ===== EN ===== */\n" + block("en") + "\n\n")
        f.write("/* ===== ES ===== */\n" + block("es") + "\n")
    print("\n%d keys per language -> tools/feature_pages_i18n.js" % len(all_i18n["en"]))


if __name__ == "__main__":
    main()
