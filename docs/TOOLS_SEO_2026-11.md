# Free calculators and food pages: report (7 November 2026)

Branch `tools-seo`. No page was deleted and no URL changed. Every new page is in the sitemap.

## What changed, in plain words

- **Eight calculators, in Spanish and English.** Four are new: proteins, water, BMR and healthy weight. The four existing ones were rebuilt. Each one:
  - gives exactly the same numbers as the app, because it uses the app's own code (`plan.ts`, `water.ts`). I checked this against the app on 20,000 random people and found no differences.
  - shows its result instantly, with no account, and sends nothing anywhere.
  - has a link you can share with your numbers filled in (for example `?peso=80&altura=175`).
  - explains the formula with a worked example, says what to do with the number, and has 4–5 questions, its sources (WHO, EFSA, Mifflin-St Jeor 1990) and links to dish pages.
- **Below each result, a card that leads to the app**, for example "¿Quieres cumplir tus 1.438 kcal sin pesar comida?".
  - Its button is "Descárgala gratis en Google Play". Next to it are the free-plan limits: 2 AI scans a day, 1 voice log a day, barcode scanner and Coach Kal unlimited, no card.
  - The link is tagged `utm_source=web&utm_medium=tool&utm_campaign=<calculator>`, so Play Console shows which calculator brought each install.
- **On phones, a slim "Descargar" bar** appears only once the result has scrolled out of view, so it never covers the inputs.
- **"Calculadoras" / "Calculators" is in the main menu**, next to Blog. Both footers link it, and both home pages link all eight calculators.
- **`/calculadoras/` is now a grid of cards**: an icon, one line of text and "Calcular →" for each calculator.
- **Dish pages:**
  - Every page now has the card "Haz una foto de tu <plato> y Fotocal lo calcula", a link to the daily-calories calculator, and nutrition data that search engines can read (`MenuItem` + `NutritionInformation`).
  - Twelve new dishes, all from app rows built ingredient by ingredient from USDA/CIQUAL data, so no figures were invented: cruasán, magdalena, salmón a la plancha, macarrones con tomate, espaguetis a la boloñesa, pollo asado, potaje de garbanzos, ensalada mixta, manzana, almendras, pizza and arroz a la cubana. That takes the total from 41 to 53.
- **Menu scan** is hidden on the site (removed from the features list, the subscription page and the comparison table), to match the app, where it is switched off.
- **Fixed along the way:**
  - The free-plan wording on dish pages left out the 1 voice log a day; it now includes it.
  - The site's dark colours, which nothing switches on yet, were broken on most pages; they now work if the theme is ever turned on. Visitors currently see no change.

## New and updated URLs

Spanish pages, with the English page at the same path under `/en/`:

| Calculator | Spanish | English |
|---|---|---|
| Hub | /calculadoras/ (updated) | /en/calculadoras/ (new) |
| Daily calories | /calculadoras/calorias-diarias/ (updated) | /en/calculadoras/calorias-diarias/ (new) |
| Calorie deficit | /calculadoras/deficit-calorico/ (updated) | /en/calculadoras/deficit-calorico/ (new) |
| BMI | /calculadoras/imc/ (updated) | /en/calculadoras/imc/ (new) |
| Protein | /calculadoras/proteinas/ (new) | /en/calculadoras/proteinas/ (new) |
| Macros | /calculadoras/macros/ (updated) | /en/calculadoras/macros/ (new) |
| Water | /calculadoras/agua/ (new) | /en/calculadoras/agua/ (new) |
| BMR | /calculadoras/tmb/ (new) | /en/calculadoras/tmb/ (new) |
| Healthy weight | /calculadoras/peso-saludable/ (new) | /en/calculadoras/peso-saludable/ (new) |

New dish pages (Spanish only, like the other dish pages):

- /calorias/croissant/
- /calorias/magdalena/
- /calorias/salmon-a-la-plancha/
- /calorias/macarrones-con-tomate/
- /calorias/espaguetis-bolonesa/
- /calorias/pollo-asado/
- /calorias/potaje-de-garbanzos/
- /calorias/ensalada-mixta/
- /calorias/manzana/
- /calorias/almendras/
- /calorias/pizza/
- /calorias/arroz-a-la-cubana/

All 41 existing dish pages were updated (card, link and nutrition data).

The sitemap went from 201 to 226 URLs.

## Lighthouse, phone settings

Scores are for performance / accessibility / best practices / SEO.

"Before" is the main branch served locally, because the live site cannot be reached from this environment. "After" is this branch. Lab scores move a few points from run to run.

| Page | Before | After |
|---|---|---|
| /calculadoras/calorias-diarias/ | 92 / 100 / 100 / 100 | 95 / 100 / 100 / 100 |
| /calculadoras/deficit-calorico/ | 94 / 100 / 100 / 100 | 94 / 100 / 100 / 100 |
| /calculadoras/imc/ | 95 / 100 / 100 / 100 | 93 / 100 / 100 / 100 |
| /calculadoras/macros/ | 95 / 100 / 100 / 100 | 95 / 100 / 100 / 100 |
| /calculadoras/ (hub) | 95 / 100 / 100 / 100 | 97 / 100 / 100 / 100 |
| /calculadoras/proteinas/ | new | 93 / 100 / 100 / 100 |
| /calculadoras/agua/ | new | 94 / 100 / 100 / 100 |
| /calculadoras/tmb/ | new | 93 / 100 / 100 / 100 |
| /calculadoras/peso-saludable/ | new | 94 / 100 / 100 / 100 |
| /en/calculadoras/ (hub) | new | 95 / 100 / 100 / 100 |
| /en/calculadoras/calorias-diarias/ | new | 94 / 100 / 100 / 100 |
| /en/calculadoras/imc/ | new | 92 / 100 / 100 / 100 |
| /en/calculadoras/macros/ | new | 94 / 100 / 100 / 100 |
| /en/calculadoras/agua/ | new | 94 / 100 / 100 / 100 |
| /calorias/tortilla-de-patatas/ | 94 / 100 / 100 / 100 | 94 / 100 / 100 / 100 |
| /calorias/pizza/ (new) | new | 94 / 100 / 100 / 100 |
| /calorias/croissant/ (new) | new | 95 / 100 / 100 / 100 |

Layout shift is 0: each page is built with its default result already filled in, so nothing moves when the script loads.

## Checks that passed

- `check_site`: 246 pages, 0 problems. It covers links, hreflang, descriptions of 155 characters or fewer, and the facts and prices.
- `check_mobile`: 27 pages at 360 px.
- `check_calcs`: 47 values worked out by hand from the app's code, in both languages. It also checks:
  - the shareable URL parameters
  - English number format
  - that the first paint shows the same result the script computes
- `check_contact`.

## Screenshots

`docs/tools/` holds each calculator and the hub on a phone and on a desktop, in light and dark. File names follow `<slug>-<mobile|desktop>-<light|dark>.jpg`.

The dark shots switch on the site's dark theme by hand, because visitors don't get a dark theme yet.

## What to watch in Search Console

Results take weeks to months.

- **Queries** to watch in Performance → Search results, filtered by query:
  - "calculadora de calorías", "calculadora calorias diarias"
  - "calculadora imc"
  - "calculadora deficit calorico" (also with "mujer")
  - "calculadora proteinas", "cuanta agua beber al dia", "calculadora tmb", "peso ideal"
  - "calorías de <plato>", for example "calorías croissant" or "calorías pizza"
- **Pages report:** filter on `/calculadoras/` and `/en/calculadoras/` to see the new pages being indexed.
- **Enhancements:** FAQ and Breadcrumb items. The `NutritionInformation` data does not produce a special search result, but it helps search engines and AI answers quote the right figures.

## Owner steps

1. Resubmit `https://getfotocal.com/sitemap.xml` in Search Console (Sitemaps → resubmit).
2. Optional: in Play Console → Store listing acquisition, the `utm_campaign` values show which calculator, or which dish page (`utm_medium=dish`), brought each install.
