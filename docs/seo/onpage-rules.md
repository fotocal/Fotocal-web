# On-page placement rules

Source: MASTER PROMPT v3, section B (9 November 2026). Every page created or edited from now on follows these rules: the rollout PARTs, the Monday routine, new pages. The build helps:
- **`tools/check_site.py` fails** on a title over 60 characters, a meta description over 155, a missing description, or a missing or non-reciprocal hreflang set.
- **It prints "on-page notes"** (never a failure) for:
  - no H1, or more than one;
  - an `<img>` without alt;
  - the page's primary keyword missing from the title, the H1 or the first 100 words.

  The full list: `python3 tools/check_site.py --notes`, or `python3 tools/seo/onpage_lint.py [kind]`. A page touched in a run must end with **zero notes**.

## B.1 Keyword map: one primary per URL (anti-cannibalisation)

The table lives in **`docs/seo/keyword-map.md`** (generated from §B.1 into `docs/seo/keywords.csv`, `primary_keyword=yes`). It is the single source, so it is not copied here.

Each URL owns one primary keyword. Secondaries may repeat across pages only as natural mentions, never in another page's title or H1.

**Rule:** before writing any title, H1 or new page, grep `docs/seo/keyword-map.md`. If the primary already belongs to another URL, don't use it. Link to that URL instead.

## B.2 Where keywords go (every page type)

| Element | Rule |
|---|---|
| `<title>` | ≤ 60 characters. **Primary keyword first.** Then one differentiator (number, "gratis", "por 100 g", "mujer y hombre", year for comparisons). Use the "— Fotocal" or "\| Fotocal" brand suffix only if it still fits within 60 characters; drop it on dish and calculator pages if it pushes out a modifier. Keep it close to the H1 so Google doesn't rewrite it. |
| Meta description | ≤ 155 characters. Primary (or a close variant) in the first sentence, **one concrete fact** (kcal, formula, price), then a CTA ("Calcúlalo gratis", "Mira la ración real", "Pruébala gratis en Android"). No ALL CAPS, no emoji spam. |
| H1 | One per page. Contains the primary keyword, written naturally. It can be a little longer than the title. |
| First 100 words / "Respuesta rápida" | The first sentence answers the main question with the number or the result (it's the snippet and AI-citation candidate). It contains the primary keyword plus 1 secondary. Keep it at 40–60 words. |
| H2/H3 | Each H2 answers one sub-question people ask (taken from A.2/A.3, e.g. "¿Cuánto déficit calórico para perder 1 kg?"). Put 2–4 secondaries in H2s, never the same one twice. |
| Images | File name in kebab-case with the keyword (e.g. `paella-valenciana-racion-307g.webp`). Alt text describes the image in natural Spanish or English and includes the dish or feature name. Set width and height, use WebP, and `loading="lazy"` except on the hero. Never change existing image URLs that are already indexed. Add new files instead, and only update the `src` when the page is edited anyway. |
| FAQ | 4–6 questions taken word-for-word or nearly from PAA (A.3), each answered in 1–3 sentences with a number where possible. Keep the FAQPage JSON-LD matching the visible text exactly (no rich result is expected; this is for clarity and for AI). |
| Internal links | Every page links to: its hub, 2–4 siblings and 1 calculator. **The anchor text is the target page's primary keyword**, or a natural variant ("calcula tu déficit calórico", not "aquí"). Hubs (home, `/calorias/`, `/calculadoras/`, `/comparativa/`) link to every child. The home links to the 8 calculators, the top 12 dishes, `/comparativa/` and `/calorias/`. |
| Breadcrumb | Visible breadcrumb plus BreadcrumbList: Inicio › Calorías › Paella valenciana (EN: Home › Calories › Valencian paella). The last item matches the H1's short form. |
| URL | **Keep every existing URL.** New pages get a short, lowercase Spanish slug with no accents (EN twin: same slug under `/en/`, matching the site's existing pattern). |
| Open Graph / Twitter | `og:title` = the title (it may skip the brand). `og:description` = the meta description. `og:image` = 1200×630 per page type. `og:locale` = es_ES or en_GB/en_US, with `og:locale:alternate`. |
| hreflang | Reciprocal es ↔ en plus x-default → ES on both twins. The canonical is self-referencing. The EN twin targets the **EN primary from B.1** (translated intent, not a word-for-word translation). |
| Schema | Keep the current types. Dates (`datePublished`/`dateModified`) must be real. `author` → the person or Organization page. Don't add `aggregateRating` unless it's real and visible. |

## B.3 Templates by page type (with filled examples)

**Calculator (ES)**
- Title: `Calculadora de {X}: {modificador que la gente teclea}` (≤60)
- Meta: `Calcula {X} {en segundos/gratis}: {fórmula o dato}. {Diferenciador}. Sin registro.` (≤155)
- H1: `Calculadora de {X} {modificador}`
- Ex 1. Title: `Calculadora TMB y GET: metabolismo basal, mujer y hombre`. Meta: `Calcula tu metabolismo basal (TMB) y tu gasto diario (GET) con Mifflin-St Jeor o Katch-McArdle. Gratis, sin registro y con un ejemplo real.` H1: `Calculadora de TMB y GET (metabolismo basal)`
- Ex 2. Title: `Peso ideal según tu altura: calculadora y tabla`. Meta: `Descubre tu peso ideal según tu altura y sexo, con el rango de IMC saludable y una tabla de 1,50 a 1,95 m. Gratis y sin registro.` H1: `Peso ideal según tu altura: calculadora y tabla para mujer y hombre`. Only promise the table once it exists on the page.

**Calculator (EN)**
- Title: `{X} Calculator: {modifier}` · Meta: `Work out your {X} in seconds with {formula}. {Differentiator}. Free, no sign-up.`
- Ex 1. Title: `BMR Calculator: Basal Metabolic Rate for Women & Men`. Meta: `Work out your basal metabolic rate (BMR) and daily burn (TDEE) with Mifflin-St Jeor or Katch-McArdle. Free, no sign-up, with a worked example.`
- Ex 2. Title: `Calorie Deficit Calculator for Women and Men (Free)`. Meta: `Find your maintenance calories, a safe deficit for your sex and weight, and how long it would take to reach your goal. Free and no sign-up.`

**Dish (ES)**
- Title: `Calorías de {la/del} {plato}: ración, 100 g y {variante top}` (≤60). The variant comes from autocomplete (Mercadona, con cebolla, marisco…) and only if the page covers it with sourced data.
- Meta: `Una ración de {plato} ({g} g) tiene {kcal} kcal, {kcal100} por 100 g: {P} g de proteínas, {HC} g de hidratos y {G} g de grasas. {Gancho}.`
- H1: `Calorías de {la/del} {plato}`, or `… : {kcal} kcal por ración` if it fits naturally.
- Ex 1. Title: `Calorías de la paella: valenciana, marisco, mixta y 100 g` (only once the page has marisco/mixta sections with sourced data; until then keep the current title). Meta: `Una ración de paella valenciana (307 g) tiene 515 kcal, 168 por 100 g. Compárala con la de marisco y la mixta y mira cómo aligerarla.`
- Ex 2. Title: `Calorías de las croquetas de jamón: por unidad y 100 g`. Meta: use the real figures from the existing page, plus the hook `Cuántas kcal tienen 2, 4 o 5 croquetas.`

**Dish (EN)**
- Title: `Calories in {English name} ({Spanish name}): per serving` or `Calories in {English name}: per Serving & 100 g`
- Ex 1. Title: `Calories in Paella (Valencian): per Serving & 100 g`. Meta: `A serving of Valencian paella (307 g) has 515 kcal, 168 per 100 g, with 31.9 g protein. Is paella high in calories? See the real serving.` H1: `Calories in Valencian paella (paella valenciana)`
- Ex 2. Title: `Calories in Spanish Omelette (Tortilla de Patatas)`. Meta: `A serving of Spanish omelette (150 g) has 248 kcal, 165 per 100 g. Per slice, with onion, 3–6 eggs and the Mercadona one, with sources.` H1: `Calories in Spanish omelette (tortilla de patatas)`

**Home**
- ES title: `Contador de calorías con foto, gratis \| Fotocal`, or keep the current `Contador de calorías gratis: con una foto, sin pesar nada` if Search Console shows its CTR is at or above the site average. **Change the home title at most once per 6 weeks.**
- ES meta (keep the current one; it's good): `Haz una foto al plato y Fotocal cuenta calorías y macros en segundos. Gratis, sin tarjeta: 2 escaneos con IA, 1 por voz al día; código de barras ilimitado.`
- ES H1: `El contador de calorías con foto, gratis y sin pesar nada`
- EN title: `Photo Calorie Counter App: Free, No Weighing \| Fotocal`. EN meta: keep the current one. EN H1: `The free photo calorie counter: snap your plate, get calories`

**Feature (scan-food)**
- ES title: `Contar calorías con foto: escáner de comida con IA gratis`. ES meta: `Haz una foto al plato y obtén calorías, macros e ingredientes en segundos, sin pesar. Gratis: 2 escaneos con IA al día. Descárgala en Android.`
- EN title: `AI Food Scanner: Count Calories from a Photo (Free)`

**Comparison / listicle (ES)**
- Title: `Mejor app para contar calorías en 2026: {N} probadas` (only say "probadas" if you have truly installed and tested them; otherwise use `comparadas`).
- Meta: `Comparamos {N} apps para contar calorías en España: foto con IA, código de barras, precio en euros y qué incluye gratis. Actualizado {mes} 2026.`
- Ex 2. Title: `Alternativas a MyFitnessPal en 2026: {N} apps gratis y pago` (with N=10, 59 characters)

**Blog (ES)**
- Title: `{Pregunta o tema en castellano}: {gancho}` (≤60). Ex: `¿Cuánta proteína necesitas al día? Por kilo y objetivo`
- EN example: `How Much Protein Do You Need a Day? By Weight & Goal`

## House rules that sit on top (from the owner, still in force)

- No invented ratings, user counts, reviews, awards, "nº 1" or medical promises. Never a rating in JSON-LD unless it is real, visible and dated.
- Every number comes from the app's sourced data or an official page with the date it was checked. Competitor facts say "según su web, consultado el DD/MM/AAAA".
- Wherever "gratis" appears, the free plan's limits are on the same screen: 2 AI scans and 1 voice log a day, barcode and Coach Kal unlimited, no card.
- No phone number anywhere: contact is fotocal.app@gmail.com and the form only (the build fails otherwise).
- Never delete a page or change, rename or redirect a URL.
- Page changes are logged in `docs/seo/onpage-changes.csv`: date, URL, field, old value, new value, primary keyword, PART. (`onpage.csv` is the audit output, regenerated by `tools/seo/onpage_audit.py`, so a log kept there would be overwritten.)
