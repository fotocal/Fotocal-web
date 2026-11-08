# Competitor gap analysis: getfotocal.com

Date of research: 2026-11-08. Branch: `seo-ranking`.

## How this was done, and its limits

- **Direct fetches failed.** Robots.txt fetches for yazio.com, fatsecret.es, lifesum.com, calai.app and myfitnesspal.com all failed. The session's network blocks those hosts (DNS "ENOTFOUND"). So we have **no robots.txt, no sitemaps and no page bodies** from any competitor. We did not retry.
- **Everything below comes from web search results seen on 2026-11-08.** That means result titles, URLs and the short snippets the search tool returned. We ran about 25 searches. Some were limited to one competitor's domain. Others were open Spanish queries on our main topics.
- **The search tool is US-based.** Rankings on google.es may differ. Treat the order of results as a rough signal, not a ranking report.
- **We have no search volume data.** The gap ranking uses judgement. It weighs how many competitors cover a topic, whether the query is a plain "cuántas calorías" question, and whether our app data can answer it well. Volumes are **inferred**, not measured.
- Anything we did not see in a result today is marked **(inference)**.

Our current site (from `sitemap.xml`): 8 calculators (agua, calorias-diarias, deficit-calorico, imc, macros, peso-saludable, proteinas, tmb), 53 `/calorias/` pages plus the hub and `tabla-de-calorias`, about 50 blog posts, feature pages. Every page has an `/en/` twin. There are **no `/guias/` or `/comparativa/` sections yet**. Proposals that use those paths would create new sections.

The app database (`tools/gen_dishes.py`, `HAND`) has 218 foods. 168 of them have no `/calorias/` page yet. Every dish or food page proposed below exists in that database. Serving sizes quoted are the app's own values.

---

## 1. What each competitor ranks with that we lack

### Yazio (yazio.com/es)
Seen in results today:
- **A huge food database, one page per food.** Pattern: `yazio.com/es/alimentos/<food>.html`, titled "<Food>: calorías y valor nutricional". Examples: `calabacin-cocinado-7522.html`, `tortilla.html`, `patata-cocinada.html`, `patatas-fritas-fritura-profunda.html`.
- **Category calorie tables.** Hub "Tabla de calorías de los alimentos" (`/es/start/alimentos`). Category pages for fruits, vegetables, cereals, sauces, fast food, "platos y comidas" (in the results these appeared under `/en/foods/...` with Spanish titles).
- **Product and landing pages in Spanish:** `/es/start/contador-calorias`, `/es/start/app-android`, `/es/start/app-ios`, `/es/start/diario-alimentos`.
- **A "best app" comparison in Spanish.** `/es/mejor-app-contar-calorias` ("Mejor app para contar calorías 2026: comparativa"). A snippet from it says photo logging is part of Yazio Pro. Another snippet says Cal AI belongs to MyFitnessPal. That second point is Yazio's claim; we have not checked it.
- Success stories (`/en/success-stories`) and a help centre covering how the calorie goal is calculated.
- **Gap we noticed:** a search on yazio.com for "tortilla de patatas" found no Spanish-omelette page. It returned "Tortilla" (about 385 kcal, protein-heavy, likely a plain omelette, **inference**) and "Tortita de patata". Yazio's database looks generic, not Spanish-dish-first (**inference**).

### FatSecret España (fatsecret.es)
Seen in results today:
- **It dominates dish queries in the results.** It appeared for "calorías tortilla de patatas", "croquetas de jamón", "paella valenciana", "pechuga de pollo a la plancha", "plátano", "huevo cocido", "churros" and "bocadillo de jamón".
- **Three page templates:**
  1. Generic food: `/calorías-nutrición/genérico/<food>` (for example `tortilla-de-patatas` at 126 kcal/100 g, `paella-valenciana` at 161 kcal/100 g, `croquetas-de-jamón` at 149 kcal per 85 g croquette).
  2. Brand products: `/calorías-nutrición/<brand>/<product>/100g`, with many Spanish supermarket brands (Hacendado, Lidl, Eroski, Carrefour, Dia, Palacios, Bonarea, La Cocinera).
  3. Recipes (`/recetas/...`) and user-shared menus (`Diary.aspx?pa=mealv...`).
- Weak points seen: some pages are old (one snippet showed a 2008 update). Brand pages differ a lot from each other. There is no clear single answer or explanation, only numbers.

### MyFitnessPal
Seen in results today:
- A Spanish homepage (`myfitnesspal.com/es/welcome/`). It claims a database of "más de 3 millones de alimentos".
- A help centre, mostly in English. It explains goal setting with net calories and minimum intakes (1,200/1,500).
- **Spanish community forum threads** (`community.myfitnesspal.com/es/discussion/...`, for example "Cenas con pocas Calorias"). These ranked for "cenas ligeras".
- **No Spanish food or dish pages appeared** in any of our open Spanish queries.

### Lifesum
Seen in results today:
- "Nutrition explained" hub in English (`lifesum.com/nutrition-explained/`), with a calorie intake calculator, a maintenance calories calculator and a recipe hub (`/nutrition-explained/recipes/`, with kcal per recipe).
- Spanish only on the help centre (`help.lifesum.com/es/...`) and a few old Spanish news posts (`/news/la-app-dietetica-...`).
- **No Spanish food or dish pages appeared** for our queries.

### Cal AI (calai.app)
Seen in results today:
- Homepage plus an English blog of **"best apps" listicles**: "14 Best Free Calorie And Macro Trackers", "28 Fitness Apps Like Myfitnesspal", "19 Apps like Weight Watchers", "Best Protein Tracker Apps". There are also how-tos: "How to Track Calorie Deficit", "How To Count Calories When Eating Out".
- Claims seen on its own pages: it uses the phone's depth sensor plus AI, is "90% accurate" on visible foods, and gives results "in under 15 seconds". These are company claims.
- **No Spanish site content appeared.** The Spanish presence we saw was App Store listings (the Mexican listing names Spanish as a supported language).

### Spanish media and blogs that rank for our queries
- **Consumer.es (Eroski Consumer).** Ranked for tortilla, plátano, paella, churros, croquetas, bocadillo, skyr vs yogur and alcohol calories. Templates: "¿Cuántas calorías tiene un plátano?" Q&A articles, a recipe database (titled "Más de 6.000 recetas con información nutricional"), and comparisons ("¿Es mejor el skyr que el yogur?", "Yogures griegos: ¿cuántas grasas y calorías contienen?").
- **Directo al Paladar.** Ranked for "calorías tortilla de patatas" with "Cuántas calorías tiene una tortilla de patatas (y cómo hacerla más ligera)". Also ranked for light-dinner lists ("Siete cenas ligeras... una para cada día de la semana").
- **Vitónica.** Ranked for menus and fruit queries. It runs a long **weekly-menu series by calorie level** ("Tu dieta semanal con Vitónica": 1500, 1800, 2000, 3500 kcal, mediterranean menus). It also has "¿Qué fruta es la menos calórica?", "23 recetas saludables con menos de 500 calorías" and "Las calorías de un huevo frito".
- **FitGeneration (fitgeneration.es).** Ranked for "calculadora déficit calórico", body fat, walking calories and beer. It has a **large calculator hub** (`/calculadoras/`): macros, IDR, cutting calories, protein for muscle, PSMF, keto carbs, carbs for diabetics, nutrient density, body fat (perimeters and skinfolds), and walking calories. It also has articles such as "¿La cerveza engorda?".
- **Programmatic app sites that also compete.** They are not on the brief, but they appeared again and again: **nutriscan.app/es** (per-food pages plus "Calorías de frutas por tipo: 33 frutas comparadas"), **fitia.app/es** (protein sources list, light-dinner guides), **arise-app.com/es/plato/** (thousands of dish pages, for example many "Pechuga de pollo a la plancha con ..." variants) and **strongrfastr.com/es** (one page per "Dieta <type> de <N> calorías", with PDF menus). Calculator sites (omnicalculator.com/es, enfaf.com, hacecuentas.com) dominate calculator queries.

### Patterns we lack, in short
1. Single-food pages for basics (chicken breast, fruit, fish) that people search one by one.
2. Head-to-head comparison pages (skyr vs yogur, sandía vs melón, huevo cocido vs frito, app vs app).
3. Menus at fixed calorie levels and "cenas ligeras" lists.
4. Lists and tables by nutrient (alimentos ricos en proteínas) and by category (frutas).
5. Activity calculators (walking, steps) and a body fat calculator.
6. A "cómo hacerla más ligera" angle on dish pages.

---

## 2. Top 30 gaps, ranked

"App data" means the serving in `gen_dishes.HAND`. All Spanish URLs get an `/en/` twin as usual.

| # | Gap | Competitors seen covering it | Example query | Our proposed page | How we do it better |
|---|-----|------------------------------|---------------|-------------------|---------------------|
| 1 | Grilled chicken breast | FatSecret (genérico + Gadis), Arise, Prospre | calorías pechuga de pollo a la plancha 150 g | /calorias/pechuga-de-pollo-a-la-plancha/ | Answer first: 1 fillet 150 g = 175 kcal, 33 g protein (app). Explain raw vs cooked weight, the main reason competitor figures differ (111 vs 165 kcal/100 g seen). Link to the protein calculator. |
| 2 | Walking / steps calorie calculator | Omni, enfaf, FitGeneration, hacecuentas, nutriscan | cuántas calorías se queman caminando | /calculadoras/calorias-caminando/ | MET method, citing the Compendium of Physical Activities. Show results as Spanish food equivalents ("1 caña = X min andando", using the 86 kcal caña from the app). Link to our existing exercise post. |
| 3 | 1500 kcal day menu | strongrfastr (many variants), Vitónica weekly menus | menú dieta 1500 calorías | /guias/menu-1500-calorias/ | Built only from app dishes with real servings (for example café con leche 200 ml 90 kcal, lentejas, merluza 180 g 140 kcal). Shows each day's total. Clear warning that 1500 is low for many people, plus a link to the calorías diarias calculator. |
| 4 | Skyr vs Greek yogurt | Consumer.es (two articles), nutriscan, fitia, Hola | calorías yogur griego vs skyr | /comparativa/skyr-vs-yogur-griego/ (+ /calorias/skyr-natural/) | Answer in one line, then a table: skyr 150 g = 93 kcal, 16.5 g protein, versus yogur griego con miel 150 g = 180 kcal (app). Note natural vs sweetened. Cite labels and BEDCA. |
| 5 | Lowest-calorie fruits | Vitónica, nutriscan (33 fruits), Marie Claire, zavamed | qué fruta tiene menos calorías | /comparativa/frutas-menos-caloricas/ | Per piece **and** per 100 g, using Spanish servings: sandía 250 g 75 kcal, melón 200 g 62, fresas 150 g 48, naranja 180 g 65, plátano 120 g 105 (app). Competitors mostly give per 100 g only. |
| 6 | Body fat % calculator | FitGeneration, zavamed, Omni, enfaf, HSN, coachway | calculadora porcentaje grasa corporal | /calculadoras/grasa-corporal/ | US Navy method, with the formula and source shown. Honest limits (DEXA is the reference). Link to IMC and peso saludable. |
| 7 | High-protein foods list | CUN, HSN, fitia, MyProtein | alimentos con más proteínas | /guias/alimentos-ricos-en-proteinas/ | Protein per real serving, not just per 100 g: pechuga de pavo 150 g 34 g, merluza 180 g 31 g, sepia 180 g 30 g, gambas 150 g 27 g, skyr 16.5 g (app). Sortable by protein per 100 kcal. Link to the proteínas calculator. |
| 8 | Light dinners list | Directo al Paladar, Vitónica, fitia, Consumer, MFP forum | cenas ligeras para adelgazar | /guias/cenas-ligeras/ | Only app "cena" dishes, with kcal per serving: crema de verduras 300 g 140 kcal, tortilla francesa 170, revuelto de espinacas 190, merluza 140 (app). Typical Spanish late dinner context. |
| 9 | Best calorie app in Spain | Yazio (/es/mejor-app-contar-calorias), Nutrola, foodcraft, calorie-trackers.com, Xataka | mejor app para contar calorías | /comparativa/mejores-apps-contar-calorias/ | Test each app on the same Spanish dishes (tortilla, cocido, menú del día) and publish the method and the date. Free vs paid features checked on the test date. Expands our existing post `/blog/choose-photo-calorie-counter/`. |
| 10 | Calories in drinks | Consumer ("¿Sabes cuántas calorías bebes?"), FitGeneration, Moncloa, vinetur | cuántas calorías tiene una caña | /guias/calorias-bebidas/ | One table of Spanish drink servings: caña 200 ml 86 kcal, tercio 142, copa de vino 150 ml 128, tinto de verano 108, Coca-Cola Zero 7, ColaCao con leche 150, café con leche 90 (app). Links to our existing drink pages. |
| 11 | Egg: boiled vs fried vs scrambled | Infobae, okdiario, hacecuentas (calculator), Vitónica | calorías huevo cocido vs frito | /comparativa/huevo-cocido-frito-revuelto/ (+ /calorias/huevos-revueltos/) | Huevo cocido 55 g 85 kcal, huevos revueltos (2 eggs) 120 g 200 kcal, tortilla francesa 170 kcal (app). Explains the added oil. Links to our existing huevo-cocido page. |
| 12 | Grilled hake | FatSecret-style generic pages (**inference**: not checked for hake) | calorías merluza a la plancha | /calorias/merluza-a-la-plancha/ | 1 serving 180 g = 140 kcal, 31 g protein (app). Compare with merluza a la romana, which is already in the app. |
| 13 | Seafood paella | FatSecret (many paella variants) | calorías paella de marisco | /calorias/paella-de-marisco/ | 300 g = 480 kcal (app). Compare with our paella valenciana page. Restaurant vs home serving. |
| 14 | Orange | FatSecret / Yazio per-food pattern (**inference** for orange itself) | cuántas calorías tiene una naranja | /calorias/naranja/ | 1 piece 180 g = 65 kcal (app). Whole fruit vs zumo natural (200 ml 90 kcal, app) answered on the same page. |
| 15 | Watermelon and melon | El Universo ("sandía o melón"), Vitónica, Marie Claire | calorías sandía / sandía o melón engorda | /calorias/sandia/, /calorias/melon/ | Sandía 250 g 75 kcal, melón 200 g 62 kcal (app). A short "cuál engorda más" block on each page. |
| 16 | Lentils with chorizo | FatSecret / Consumer recipe pattern (**inference**) | calorías lentejas con chorizo | /calorias/lentejas-con-chorizo/ | 330 g plate = 400 kcal (app). Shows how much the chorizo adds versus our existing lentejas estofadas page. |
| 17 | 1800 / 2000 kcal menus | Vitónica (1800, 2000 kcal), strongrfastr | menú 2000 calorías | /guias/menu-2000-calorias/ | Same method as gap 3. Only after gap 3 proves useful. Avoid an N-calorie page farm (see Risks). |
| 18 | Mediterranean weekly menu | Vitónica (several), Marie Claire, dietamediterranea.com | menú semanal dieta mediterránea adelgazar | /guias/menu-semanal-dieta-mediterranea/ | Real Spanish dishes with kcal per day. Cite PREDIMED and the official sources only for claims they support. |
| 19 | Fideuá | (**inference**: FatSecret-type generic pages; not checked) | calorías fideuá | /calorias/fideua/ | 300 g = 470 kcal (app). Compare with paella. Valencian context. |
| 20 | Fotocal vs Cal AI | Cal AI blog ("apps like MyFitnessPal" listicles), Yazio comparativa | cal ai alternativa / cal ai español | /comparativa/fotocal-vs-cal-ai/ | Honest, dated test on Spanish dishes. Android, Spanish-first. Quote Cal AI's claims only as their claims. |
| 21 | "How to make it lighter" | Directo al Paladar (tortilla), Consumer (boiled vs fried potato) | tortilla de patatas ligera calorías | existing /calorias/tortilla-de-patatas/ (new section, no new URL) | Show grams of oil absorbed and the kcal saved, using the app ingredient logic. Apply to croquetas, patatas bravas and churros pages too. |
| 22 | Category calorie hubs | Yazio (fruits, vegetables, cereals, fast food, dishes) | tabla de calorías frutas | /calorias/frutas/ (later: /calorias/legumbres/, /calorias/pescados/) | Each hub lists only foods that have a real page, with app servings. Not empty lists. |
| 23 | Calories in 10,000 steps | getfitcraft, abacktools, Omni (steps to kcal) | cuántas calorías se queman con 10000 pasos | /blog/calorias-10000-pasos/ | Uses the gap 2 calculator. Food equivalents from the app. |
| 24 | Fried fish (Andalusian) | (**inference**: not checked) | calorías pescaíto frito / boquerones fritos | /calorias/pescaito-frito/, /calorias/boquerones-fritos/ | Pescaíto 180 g 340 kcal; boquerones 150 g 280 kcal, 30 g protein (app). Tapa vs ración sizes. |
| 25 | Grilled beef / pork loin | Arise-type dish pages (**inference**) | calorías filete de ternera a la plancha | /calorias/filete-de-ternera-a-la-plancha/, /calorias/lomo-de-cerdo-a-la-plancha/ | Ternera 150 g 220 kcal, 38 g protein; lomo 150 g 200 kcal, 31 g (app). |
| 26 | Oats with milk | (**inference**: generic per-food pages) | calorías avena con leche | /calorias/avena-con-leche/ | 1 bowl 240 g = 250 kcal, 11 g protein (app). Compare with cereales con leche and ColaCao. |
| 27 | Avocado toast | Lifesum recipe ("avocado toast 336", English) | calorías tostada con aguacate | /calorias/tostada-con-aguacate/ | 110 g toast = 230 kcal (app). Compare with tostada con tomate y aceite (existing page). |
| 28 | Spanish puddings | Consumer recipe database (**inference** for these two) | calorías natillas / flan de huevo | /calorias/natillas/, /calorias/flan-de-huevo/ | Natillas 125 g 150 kcal; flan 100 g 145 kcal (app). Supermarket pot sizes. |
| 29 | Small fruits | nutriscan fruit comparison, Yazio fruit table | calorías fresas / uvas / mango | /calorias/fresas/, /calorias/uvas/, /calorias/mango/ | Fresas 150 g 48 kcal; uvas 120 g 82; mango 150 g 90 (app). Link to the uvas de Nochevieja context on the grapes page. |
| 30 | Tortilla sandwich | FatSecret / Arise "bocadillo" pattern (seen for jamón) | calorías bocadillo de tortilla | /calorias/bocadillo-de-tortilla/ | 200 g = 400 kcal (app). Bar vs home. Links to pincho de tortilla and bocadillo de jamón. |

Notes on the ranking:
- Gaps 1–11 have the most competitors seen in results today and need new templates (calculator, comparativa, guía) that also earn links. Gaps 12–30 are cheap, single-dish pages that reuse our `/calorias/` template.
- Do not build a page for `tortilla-espanola`. Our `/calorias/tortilla-de-patatas/` already covers it.

---

## 3. What we already do better

- **Spanish dishes first.** We have tortilla de patatas, cocido, fabada, callos, salmorejo, pincho de tortilla, caña, tinto de verano and more. Yazio returned no Spanish-omelette page today. MyFitnessPal, Lifesum and Cal AI showed no Spanish dish pages at all.
- **One clear answer per serving.** FatSecret shows dozens of brand pages with very different numbers. Our pages give one Spanish serving (ración, caña, pincho) up front. Our tortilla page title already covers "ración, 100 g, Mercadona".
- **Calculators on the same site as the dish data.** Only FitGeneration and Omni match us on calculators. They have no dish pages. The food apps have few or no Spanish calculators.
- **Bilingual twins.** Every page has an English version. Most Spanish media sites do not.
- **Spanish-life blog angles.** Menú del día, tapas and desayuno español are topics the international apps do not cover in Spanish.
- **Honest limits.** We already have posts on photo app accuracy and calorie-counting mistakes. Cal AI's "90% accurate" is an unsourced company claim.

Where we are weaker, honestly: far fewer foods than anyone, no brand/supermarket data, no recipes, no comparisons, no menus, a younger domain (**inference**: no backlink data checked).

---

## 4. Risks: what we must not copy

- **Thin programmatic pages.** Arise (many "Pechuga de pollo a la plancha con ..." variants) and strongrfastr (one page per diet type × calorie level) show the pattern. Do not make one page per small variation. One dish, one page, with real content. Category hubs list only foods that have a full page.
- **Brand page sprawl.** FatSecret's pages per brand and per 100 g suit a user database, not us. We have no brand data. Mention supermarket versions inside a dish page only when we can cite the label.
- **Unverifiable numbers and claims.** Do not copy competitor kcal figures. Use app data and cite sources (BEDCA, USDA, labels). Do not claim accuracy percentages for Fotocal unless we have tested them and published the method. Never repeat a competitor's claim (Cal AI's "90%", Yazio's "Cal AI belongs to MyFitnessPal") as fact. Quote it as theirs, with a date.
- **Comparison pages that go stale or turn unfair.** App features and prices change. Date every comparativa, test on the same dishes, and recheck every 6 months. No fake reviews or invented user testimonials. Yazio's success-stories page is not a model for us.
- **Keyword stuffing.** Do not repeat "calorías tortilla de patatas" variants in headings. One H1, natural Spanish, answer first.
- **Unsafe diet advice.** Low-calorie menus (1500 kcal) need a clear warning and a link to the calculator. Do not promise kg lost per week as a guarantee. Vitónica itself calls 1500 kcal "muy restrictiva".
- **Old data.** Several competitor pages are years old. We should show a "revisado" date on each page and keep it true.
- **Duplicate intent.** Check new pages against existing ones before building (for example tortilla-espanola vs tortilla-de-patatas, or `/blog/how-many-calories-does-exercise-burn/` vs the new walking calculator). Link them; do not compete with ourselves.
