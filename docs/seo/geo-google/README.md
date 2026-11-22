# Google AI features (AI Overviews / AI Mode): GEO round, 22 Nov 2026

## What Google says
Source pages: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) and the Search Central blog post [Top ways to ensure your content performs well in Google's AI experiences on Search](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) (May 2025). Google's own optimisation guide is also in the same docs: [Optimizing your website for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).
This session's network blocks developers.google.com, so the pages were read through search results and not loaded directly. All the sources agree on these points:

- A page can appear as a link in AI Overviews or AI Mode only if it is **indexed and eligible to show with a snippet**. There are **no additional technical requirements**.
- You need **no special files** (llms.txt, "AI text files") and **no special schema**. Our `llms.txt` stays as it is: it does no harm.
- The controls are the normal ones: `nosnippet`, `data-nosnippet`, `max-snippet` and `noindex`.
- What Google asks for: useful content that only you can offer; good page experience; content that can be crawled; and structured data that matches the visible text.
- Measurement: AI-features traffic is counted in Search Console under "Web". The new "Search generative AI" report is already in our export at `docs/seo/gsc/2026-11/generative-ai-*.csv`.

## 1. Eligibility: all 326 sitemap URLs pass
Checked with `tools/seo/ai_eligibility.mjs`; per-URL results are in `eligibility.csv`. Every URL passes all of these:
- returns 200;
- robots allows indexing and snippets;
- no `nosnippet`, `max-snippet:0` or `data-nosnippet`;
- the main text is 100 % present with JavaScript turned off.

`robots.txt` allows Googlebot and Google-Extended. The 33 `noindex` pages are the deliberate ones (series hubs, 2 thin posts, recipe, embeds), and none of them is in the sitemap. **Nothing failed, so nothing needed fixing.**

## 2. Query fan-out (ES first, EN twins added the same way)

| Topic → main page | Sub-question | Answered? |
|---|---|---|
| **Contar calorías** → /blog/how-to-count-calories-accurately/ | ¿Cómo empezar? | yes (summary) |
| | ¿Cuántas calorías necesito? | yes (step 1 + calculator) |
| | ¿Hay que pesar? | yes (step 2) |
| | ¿Cómo contar comiendo fuera / comida casera? | yes (step 4) |
| | ¿Cuánto cambia el total si la ración es mayor? | **added** H2 + Datos box |
| | ¿Se puede sin báscula? | **added** FAQ |
| | ¿Cuánto tiempo hay que contar? | **added** FAQ |
| | ¿Qué app usar? | **added** FAQ (free limits on screen) |
| | ¿Se cuenta el aceite? | **added** FAQ |
| **Calorías de un plato** → /calorias/ | ¿Cuántas calorías tiene un plato? | yes (quick answer) |
| | ¿Cuál tiene más? | yes (top 10) |
| | ¿Cuáles tienen menos? | **added** H2, 5 lightest main dishes |
| | ¿De qué dependen? / ¿cuánto pone el aceite? | **added** H2 + Datos box |
| | ¿Tapas, desayunos? | yes (group tables) |
| | ¿Cómo calcular mi ración? | yes («Cómo leer la tabla») |
| | ¿Un menú del día? | yes (link to post) |
| **Escanear comida** → /features/scan-food/ + /scan-barcode/ | ¿Cómo escanear comida? | yes (FAQ) |
| | ¿Qué app cuenta calorías con foto? / ¿mejor IA? | yes (FAQ) |
| | ¿Es precisa? | yes (FAQ) |
| | ¿Restaurante y platos mezclados? | yes (FAQ) |
| | ¿Es gratis? | yes (limits shown on screen) |
| | ¿Código de barras gratis? ¿Gasta escaneos? | yes (FAQ) |
| | ¿Y si el producto no está? | yes (FAQ) |
| | ¿Hay versión para iPhone? | **added** FAQ (Android only) |
| | ¿De dónde sale el error? / ¿envasados? | **added** link line to the cluster |
| **Peso ideal / IMC** → /calculadoras/peso-saludable/ + /imc/ | ¿Cuál es mi peso ideal? | yes |
| | ¿Cómo se calcula? | yes |
| | ¿Tabla por altura? | yes |
| | ¿Mujer y hombre? ¿Edad? | yes |
| | ¿Cuántos kilos me sobran? | yes |
| | ¿Qué IMC es normal? ¿Deportistas? | yes |
| | ¿Diferencia IMC / peso ideal? | **added** FAQ |
| **TMB / TDEE / déficit** → /calculadoras/tmb/, /calorias-diarias/, /deficit-calorico/ | ¿Qué es la TMB? ¿Cómo sacarla? | yes |
| | ¿TMB o GET/TDEE? | yes |
| | ¿Cuántas calorías para adelgazar? | yes |
| | ¿Déficit para 1 kg? ¿Déficit recomendado? ¿500 kcal? | yes |
| | ¿Comer por debajo de la TMB? | yes |
| | ¿Cada cuánto recalcular? | **added** FAQ (−50 kcal TMB per 5 kg, Mifflin) |
| **Alimentos saciantes** → /blog/best-foods-for-weight-loss/ | ¿Cuáles sacian más con menos calorías? | yes |
| | ¿Qué es la densidad calórica? | yes |
| | ¿Lista con calorías? | yes |
| | ¿Calorías negativas? ¿Qué racionar? | yes |
| | ¿Cuánta comida son 400 kcal? | **added** H2 + Datos box |
| | ¿Qué cenar que sacie? | **added** H3 + link to light dinners |
| | ¿Qué picar entre horas? | **added** H3 + link to snacks |

**Clusters (hub → detail → calculator → app):** every main page now links the others in its topic and has the Google Play card. The links added this round:
- scan-food → barcode scanner and the photo-accuracy post;
- TMB → the deficit post;
- best-foods → the deficit calculator.

## 3. «Datos de Fotocal» boxes
The boxes are computed at build time by `tools/fotocal_data.py`. They use the same `figures()` and `compose()` as the dish pages, so they cannot drift from the tables. They draw on the app's food catalogue only; **no user data** is used.
- **/calorias/ (ES+EN), the olive oil box:** the app works out 158 dishes ingredient by ingredient. Of those, 60 contain olive oil. In half of them the oil gives at least 25 % of the calories, and in 15 it gives more than a third. 10 g of oil = 88 kcal. The table shows 6 dishes, from pimientos de Padrón (74 %) to sopa castellana (31 %).
- **how-to-count (ES+EN), ±25 % portion:** the table covers 5 dishes. On a main dish the gap between a serving 25 % smaller and one 25 % larger reaches 258 kcal (paella).
- **best-foods (ES+EN), what 400 kcal gets you:** 1,110 g of gazpacho, compared with 70 g of almonds (7 foods in all).

Pictures: `shots/` (phone + laptop).

## 4. Structured data = visible text
`tools/seo/check_schema_visible.py` checks the structured data on all 326 indexable pages against the visible text:
- 938 FAQ items, each question and answer visible in the page's own language;
- the app is marked Android, prices match `pricing.json`, and there is no aggregateRating.

Fixed: the Article `headline` was the page title on 18 pages (dish pages, methodology, comparisons). It is now the visible H1.

## 5. Images
New real app screens (avif/webp), each with Spanish/English alt text and width/height:
- 7 calculators (all except water);
- the dish hub;
- 2 posts (blog covers are decorative SVGs with empty alt, so these screens are their only content images).

Feature pages and the home page already had screens.

Not changed: the 60 dish pages have no food photo. We have no real photo of each dish, and the owner rejected showing a different dish from the app on the share cards.

## 6. Page experience
`tools/seo/check_overlays.mjs` checked 15 key pages on a phone (Pixel 7):
- the fixed bars (download bar, calculator bar) never cover more than 6 % of the screen (13 % when the language hint also shows);
- the main text can always be scrolled clear of them;
- each page has exactly one H1.

Articles and calculators show "Actualizado / Updated" with the date and "Por Fotocal, Madrid".

## 7. Baseline (Search Console export, 3 months to ~20 Nov)

| Topic | Queries | Clicks | Impressions |
|---|---|---|---|
| Contar calorías | 25 | 0 | 106 |
| Calorías de un plato / comida española | 2 | 0 | 5 |
| Escanear comida (non-brand) | 25 | 0 | 59 |
| Peso ideal / IMC | 0 | 0 | 0 |
| TMB / TDEE / déficit | 16 | 0 | 25 |
| Alimentos saciantes | 7 | 0 | 38 |

The "Search generative AI" report gives impressions per page: the home page 89, /en/ 40, /calorias/ 15, /blog/calorias-menu-del-dia/ 9. Compare with the export the owner sends around 20 Dec.
