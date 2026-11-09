# Dev.to — Cómo construí una app de calorías (yo solo, desde Madrid)

- **Platform:** Dev.to (dev.to). Same text works on Hashnode if you prefer it; only use ONE of the two (do not post it twice).
- **Title:** Cómo construí una app de calorías yo solo, desde Madrid: decisiones, errores de enfoque y números aburridos
- **Tags (Dev.to allows 4, lowercase, no spaces or accents):** android, ai, buildinpublic, spanish
- **Links in the post (2):**
  1. "la ración de patatas bravas, desglosada ingrediente a ingrediente" → https://getfotocal.com/calorias/patatas-bravas/ (section "Decisión 2")
  2. "calculadora de metabolismo basal" → https://getfotocal.com/calculadoras/tmb/ (section "Decisión 3")
- **Number source:** bravas composition and totals from the app data (`g.figures('patatas-bravas')`); formulas from `assets/js/calc.js` (whose header says they are the app's formulas). Data sources named (USDA FoodData Central, CIQUAL) are the ones listed in the app data for that dish.

**IMPORTANT before posting:** this one is written in first person as *your* story. It only states facts from the brief and the repo, and keeps the "why" general. Read it once and change any sentence that is not exactly how it happened for you. Do not add download numbers, ratings or user quotes.

Copy everything between `ARTICLE START` and `ARTICLE END` (not those lines). Dev.to uses Markdown, so it pastes as is.

---

**▼ ARTICLE START — copy from the next line ▼**

Esto no es un hilo de "cómo llegué a X usuarios en 30 días". No tengo esa historia, y no la voy a inventar.

Es el relato de cómo hice Fotocal, una app Android para contar calorías con una foto de la comida. La he hecho yo solo, desde Madrid. Quiero contar las decisiones que tomé, por qué, y lo que todavía no está resuelto.

Si estás pensando en construir algo tú solo, quizá te sirva.

## El problema de partida

Contar calorías funciona. Lo difícil es seguir contando.

Las apps clásicas te piden buscar cada alimento, elegir entre veinte resultados parecidos y escribir los gramos. Con comida envasada, vale. Con un plato de lentejas de tu madre o una ración de bravas en un bar, se complica.

Y en España comemos mucho así: de menú, de tapas, de táper. Platos con varios ingredientes, sin etiqueta y sin báscula a mano.

Mi pregunta era sencilla: ¿cuánto se puede quitar del proceso sin que los números dejen de ser útiles?

## Decisión 1: la foto primero, pero no solo la foto

La idea central es hacer una foto del plato y obtener una estimación de calorías y macros.

Pronto quedó claro que la foto no sirve para todo:

- **Un yogur o unas galletas** traen etiqueta. Ahí lo exacto es leer el código de barras. Por eso la app tiene escáner.
- **A veces no puedes hacer foto.** Estás conduciendo, o ya te lo has comido. Para eso está el registro por voz: dices lo que has comido y queda apuntado.
- **Los números solos no ayudan mucho** si no sabes qué hacer con ellos. Por eso añadí un coach con IA, Coach Kal, al que puedes preguntar.

Foto, código de barras, voz y coach. Cuatro entradas para el mismo diario. La foto es la estrella, pero no tiene que hacerlo todo.

## Decisión 2: los números tienen que salir de algún sitio

Esto es lo menos vistoso y lo más importante.

Un plato español no es un alimento. Es una receta. Así que los platos de referencia se calculan ingrediente a ingrediente, con datos de bases públicas como USDA FoodData Central y CIQUAL.

Un ejemplo. Una ración de patatas bravas de 200 g se modela así:

- 150 g de patatas fritas
- 14 g de aceite de oliva
- 32 g de tomate frito
- 2 g de guindilla
- 2 g de ajo

Total: **380 kcal**, 4,7 g de proteína, 41,5 g de hidratos y 22,8 g de grasa. Si te interesa, aquí está [la ración de patatas bravas, desglosada ingrediente a ingrediente](https://getfotocal.com/calorias/patatas-bravas/).

¿Es exacto para *tu* bar? No. Cada cocina es distinta. Pero es un número razonado, con fuentes. Y eso permite discutirlo y mejorarlo.

La lección: si tu producto da números, alguien te preguntará de dónde salen. Mejor tener la respuesta escrita antes.

## Decisión 3: las fórmulas aburridas, bien hechas

Para saber cuánto debería comer cada persona, no inventé nada. Usé lo que ya está aceptado:

- **Metabolismo basal:** la ecuación de Mifflin-St Jeor.
- **Gasto diario:** el basal multiplicado por un factor de actividad, de 1,2 (sedentario) a 1,725 (muy activo).
- **Déficit:** kilos por semana × 7.700 ÷ 7. Un kilo son unas 7.700 kcal.
- **Un tope:** el déficit nunca pasa del 25 % del gasto diario.
- **Un suelo:** nunca por debajo de 1.200 kcal en mujeres ni de 1.500 kcal en hombres.

El tope y el suelo son las dos líneas de código que más me importan. Una app de calorías puede hacer daño si te dice que comas 900 kcal al día. Prefiero que te diga "ve más despacio".

Luego hice algo que recomiendo: saqué esas fórmulas a una web pública. Las calculadoras de getfotocal.com usan las mismas fórmulas que la app. Funcionan en el navegador, sin cuenta, y no envían tus datos a ningún sitio. Por ejemplo, la [calculadora de metabolismo basal](https://getfotocal.com/calculadoras/tmb/) hace exactamente el primer paso de la lista.

Así cualquiera puede comprobar los números sin instalar nada.

## Decisión 4: un plan gratis de verdad

No quería un "gratis" que en realidad es una prueba de siete días con la tarjeta dentro.

El plan gratuito de Fotocal no pide tarjeta y no caduca. Incluye:

- 2 escaneos de foto con IA al día.
- 1 registro por voz al día.
- Escáner de código de barras sin límite.
- Coach Kal sin límite.

Cada escaneo con IA tiene un coste para mí. Por eso el plan gratuito tiene un límite diario en fotos y voz. Lo demás no tiene límite.

Quien quiera más tiene el Premium: 6,99 € al mes o 34,99 € al año, con 5 días de prueba.

Los precios pueden cambiar con el tiempo. Lo que no quiero que cambie es que sean claros.

## Decisión 5: una sola plataforma

Fotocal está solo en Android, en Google Play.

Una persona sola no puede mantener bien dos apps nativas, una web, el soporte y el marketing a la vez. Así que elegí una plataforma, para hacerla bien. Si algún día hay versión para iPhone, será cuando pueda mantenerla con el mismo cuidado.

## Lo que todavía no está resuelto

Sería poco honesto no contarlo:

- **El aceite escondido.** Una foto no ve cuánto aceite hay en la sartén. Una cucharada son 80 kcal. Es el error más común al estimar, sea con foto o a ojo.
- **Las raciones.** Una foto da una estimación del tamaño. Un plato hondo engaña. Un plato grande también.
- **Los platos caseros.** Las lentejas de cada casa son distintas. El número es una referencia, no una verdad absoluta.

La forma de convivir con esto es la misma que con cualquier método: constancia. Un error pequeño y constante se corrige solo cuando miras la tendencia de tu peso durante semanas.

## Lo que aprendí (hasta ahora)

1. **Lo aburrido es el producto.** Las fuentes de datos, las fórmulas, los límites de seguridad. Nadie lo ve, pero todo depende de ello.
2. **La IA es una herramienta, no el producto.** La foto es solo la forma más rápida de llegar a un número útil.
3. **Escribe tus números en público.** Las calculadoras de la web me obligan a ser coherente con la app.
4. **No prometas lo que no tienes.** Ni reseñas inventadas, ni cifras infladas. Si el producto es útil, se notará.

Si estás construyendo algo tú solo, me encantaría leerte en los comentarios. Y si cuentas calorías y tienes Android, prueba la versión gratuita. Las críticas me sirven más que los aplausos.

**▲ ARTICLE END — copy down to the line above ▲**

---

## How to post it on Dev.to (step by step)

1. **Account.** Go to https://dev.to and click **Create account**. Sign up with GitHub or Google.
2. **Profile (first time only).** Avatar → **Settings → Profile**:
   - Name: your real name.
   - Bio: "Hago Fotocal, una app Android para contar calorías con una foto. Desde Madrid."
   - Website URL: `https://getfotocal.com`
   - Location: Madrid.
3. **New post.** Click **Create Post** (top right).
4. **Cover image (optional).** Click **Add a cover image**. Use a simple screenshot of the app or a photo you own. 1000×420 works well.
5. **Title.** Paste the title into "New post title here...".
6. **Tags.** In "Add up to 4 tags", type: `android`, `ai`, `buildinpublic`, `spanish`. (If a tag does not exist, Dev.to suggests similar ones; pick the closest.)
7. **Body.** Paste the article into the big box. Dev.to uses Markdown, so headings, bold, lists and links work as they are.
8. **Preview.** Click **Preview** (top) and check the two links.
9. **Language.** Dev.to has no language setting; the Spanish text and the `spanish` tag are enough.
10. **Publish.** Click **Publish**. Copy the URL into the README tracking table.
11. **Add the "read also" line.** Click **Edit** and add at the end:
    > Por cierto, escribí una lista de desayunos españoles de menos de 300 kcal: [enlace al post de Tumblr]
12. **Reply to every comment** in the first days. On Dev.to, comments and reactions are what make a post visible.

**If you use Hashnode instead:** sign up at https://hashnode.com, create a free blog, click **Write**, paste the same Markdown, add the same tags (Hashnode allows up to 5; you can add `startup`), and **Publish**. Do not publish it on both.

### Share it so it gets found

- **Instagram:** a Story or post with a photo of your workspace: "He escrito cómo construí Fotocal, yo solo. Sin cifras infladas." Link sticker in a Story.
- **TikTok:** a 30–60 second "build story" talking to camera: the 5 decisions, one sentence each. Link in profile.
- **YouTube:** the same as a Short; Dev.to URL in the description.
- **Facebook:** share the link on your page.
- **LinkedIn:** share the Dev.to link as a normal post (not a new article) a few days after publishing.
