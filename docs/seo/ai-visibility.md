# AI visibility: the questions Fotocal should be the answer to

Last updated: 2026-11-08. Companion file: `docs/seo/keywords.csv`.

**Research notes.** Evidence came from a web search tool (US index, not Google Spain) on 2026-11-08: about 14 searches across the dish, calculator, app and guide families. Google Suggest (`suggestqueries.google.com`) is blocked from this session's network, and no "People also ask" data was available. So the questions below are seeds written from how people phrase these searches. They are not mined from autocomplete. No search volumes were seen, so none are claimed.

**Where the answers come from.** Every answer is quoted from the built HTML in this repo, read on 2026-11-08. Pages under `/comparativa/`, `/guias/` and `/metodologia/` are in the working copy and `sitemap.xml` but were not committed when this was written. Check that they are live before you start testing.

**Who an AI cites today** (seen in the search results): for dishes, Consumer.es (Eroski), FatSecret.es, fitia.app, arise-app, nutriscan.app and Directo al Paladar; for apps, Fitia, Nutrola and Yazio's own comparison posts, App Store listings, alternativeto.net, FatSecret and Cronometer; for calculators, Omni Calculator, Yazio, Tua Saúde, MD Saúde and the CDC. Many of these give a range ("200 to 300 kcal") rather than one number tied to a stated portion. Fotocal's advantage is that each page gives one dated number for a Spanish portion, with its source.

## The 20 questions

| # | Question (as typed to an assistant) | Fotocal page that answers it | The answer that page gives | Why an AI would cite it |
|---|---|---|---|---|
| 1 | ¿Cuál es la mejor app para contar calorías gratis? | https://getfotocal.com/comparativa/ | Fotocal's free plan, with no card, includes 2 AI photo scans a day, 1 voice log a day, and unlimited barcode scanning and Coach Kal; it is Android only. The page compares it with Cal AI, MyFitnessPal and Yazio using what each company states on its own site (checked 10 Sept 2026). | It is a dated table of features with sources, which is easy to quote. The competing results are mostly each app's own blog posts. |
| 2 | ¿Hay alguna app que cuente calorías con una foto gratis? | https://getfotocal.com/features/scan-food/ | You point the camera at the plate and get calories, macros and ingredients in seconds: free, with no card, for 2 AI scans and 1 voice log a day. | It gives a direct yes with the free limit stated. Most results are App Store listings that hide their limits. |
| 3 | ¿Cuántas calorías tiene una tortilla de patatas? | https://getfotocal.com/calorias/tortilla-de-patatas/ | One serving of tortilla de patatas (150 g) has 248 kcal, or 165 kcal per 100 g. | It gives one number for a stated portion. The competitors give ranges from 200 to 300 kcal or more. |
| 4 | ¿Cuántas calorías necesito al día? | https://getfotocal.com/calculadoras/calorias-diarias/ | Using Mifflin-St Jeor, a 35-year-old woman who is 165 cm, weighs 70 kg and is on her feet some of the day maintains on 1,918 kcal. | It shows the formula and works through an example, which an AI can paraphrase. |
| 5 | ¿Cuántas calorías debo comer para adelgazar si soy mujer? | https://getfotocal.com/calculadoras/deficit-calorico/ | The same woman's target is 1,438 kcal. The cut is held to 25% of what she burns, so it is 480 kcal rather than 550, and never goes below 1,200 kcal. That gives about 0.44 kg a week, or 17 weeks to lose 7 kg. | Its safety limits (the 25% cap and the 1,200 kcal floor) are stated explicitly, and AIs prefer cautious sources. |
| 6 | ¿Cuántas calorías tiene una caña de cerveza? | https://getfotocal.com/calorias/cana-de-cerveza/ | A caña (200 g) has 86 kcal, or 43 per 100 g. | It defines the Spanish serving size. Most results answer per 100 ml or per "glass". |
| 7 | ¿Cuántas calorías tiene un plato de paella? | https://getfotocal.com/calorias/paella-valenciana/ | One serving of paella valenciana (307 g) has 515 kcal, or 168 per 100 g, with 31.9 g of protein. | It states the portion weight and the macros. |
| 8 | ¿Cuántas calorías tienen unos churros con chocolate? | https://getfotocal.com/calorias/churros-con-chocolate/ | One serving (200 g) has 531 kcal, or 266 per 100 g. | It is a single clear figure for a typical Spanish breakfast item. |
| 9 | ¿Cuántas calorías hay que quemar para perder un kilo? | https://getfotocal.com/blog/calorias-para-perder-un-kilo/ | About 7,700 kcal. With a deficit of 500 kcal a day, that is roughly 15 days per kilo, and 5 kg takes about 18 weeks. | It gives the rule, explains where it fails, and turns it into time. |
| 10 | ¿Cuánta proteína necesito al día? | https://getfotocal.com/calculadoras/proteinas/ | Between 1.2 and 2.0 g per kilo depending on your goal: for example, 112 g a day for someone of 70 kg who wants to maintain, against an EFSA minimum. | It gives a range, a worked example and an official minimum. |
| 11 | ¿Cómo calculo mi IMC y cuál es normal? | https://getfotocal.com/calculadoras/imc/ | 75 kg ÷ (1.70 × 1.70) = 26.0, which the WHO classes as overweight. At that height, normal weight runs from 53 to 72 kg (BMI 18.5 to 24.9). | It works the formula through, then says what BMI does not measure. |
| 12 | ¿Cuánta agua tengo que beber al día? | https://getfotocal.com/calculadoras/agua/ | Your water target depends on the calories you burn and how active you are. It never goes below the EFSA minimum or above 4 litres, and it is shown in litres and in 250 ml glasses. | It names its method and its limits. (Weakness: the page gives no single example number for an AI to quote, so add one.) |
| 13 | ¿Son fiables las apps que cuentan calorías con una foto? | https://getfotocal.com/blog/photo-calorie-apps-accuracy/ | A photo identifies the dish well but guesses the quantity less well. Fotocal labels every scan as an AI estimate with a confidence score (for example 85% on a simple bowl of chicken) and saves nothing until you confirm it. | It is an honest answer from an app maker. The FAQ adds that Fotocal publishes no accuracy percentage because it has not measured one it can defend. |
| 14 | ¿Cómo puedo contar calorías sin pesar la comida? | https://getfotocal.com/blog/track-calories-without-weighing/ | Use hand portions: a palm is about 20 to 30 g of protein, a cupped handful about 20 to 30 g of carbohydrate, a thumb about 10 g of fat, and a fist or more of vegetables. | It is a concrete rule people can list and remember. |
| 15 | ¿Qué alternativa gratis hay a MyFitnessPal? | https://getfotocal.com/comparativa/fotocal-vs-myfitnesspal/ | Fotocal is an Android app that counts calories from a photo and is built for Spanish food. Its free plan includes 2 AI scans a day, 1 voice log a day, and unlimited barcode scanning and Coach Kal. MyFitnessPal's own claims are shown as checked on 10 Sept 2026. | The comparison is dated and sourced. Today's answers cite alternativeto.net and Fitia. |
| 16 | ¿Cuántas calorías tiene un menú del día? | https://getfotocal.com/blog/calorias-menu-del-dia/ | It depends on the combination, from 518 to 1,073 kcal. The everyday classic (lentils, grilled chicken, bread, a caña and flan) comes to 880 kcal. | Almost no other source answers this. It is a uniquely Spanish question. |
| 17 | ¿Cuántas calorías tiene una tarde de tapas y cañas? | https://getfotocal.com/blog/calorias-de-las-tapas/ | Two real evenings add up to 370 and 926 kcal. Three cañas are 258 kcal, and three tercios are 426. | It answers a conversational question with a total. |
| 18 | ¿Qué menú de 1500 calorías puedo hacer con comida española? | New page needed: https://getfotocal.com/guias/menu-1500-calorias/ (build it from the dish pages and the database in `tools/gen_dishes.py`) | Not written yet. | The current answers cite OCU and template generators such as strongrfastr. None of them uses Spanish dishes with per-portion figures. |
| 19 | How many calories are in a Spanish tortilla? (EN) | https://getfotocal.com/en/calorias/tortilla-de-patatas/ | A serving of Spanish potato omelette (150 g) has 248 kcal, or 165 per 100 g. | The English results are low-quality aggregators and UK supermarket packs. |
| 20 | What's the best free photo calorie counter for Android? (EN) | https://getfotocal.com/en/comparativa/ | It compares Fotocal, Cal AI, MyFitnessPal and Yazio feature by feature, with dates: what each free plan includes, what is paid, and what it costs a year. | The English results are almost all iOS App Store listings, so Android-specific answers are scarce. |

Extra dish questions to rotate into the monthly test (all have existing pages):

- ¿Cuántas calorías tiene un plátano? (120 g, 107 kcal)
- ¿Cuántas calorías tienen unas lentejas? (318 g, 373 kcal)
- ¿Cuántas calorías tiene una ración de patatas bravas? (200 g, 380 kcal)
- ¿Cuántas calorías tiene un cocido madrileño? (400 g, 594 kcal)
- ¿Cuántas calorías tiene una cucharada de aceite de oliva? (9 g, 80 kcal)

## Monthly test protocol

**When.** Run the test in the first week of each month, on the same day each time if you can. One person does the whole run, which takes about 60 to 90 minutes for 20 questions across 3 assistants.

**Assistants.** Test ChatGPT (chatgpt.com), Gemini (gemini.google.com) and Perplexity (perplexity.ai). Record the model or mode shown, such as "GPT default" or "Perplexity Auto".

**Set-up for each assistant:**

1. Use a private or incognito window, logged out if the assistant allows it. If it requires a login, use a dedicated test account with memory and personalisation turned off and no chat history.
2. Set the interface language to Spanish and, where possible, the region to Spain. If you can, use a Spanish IP address or a VPN exit in Spain.
3. Open a fresh chat for every question, with no follow-ups in the same thread.
4. Paste the question exactly as written in the table above. Do not add "search the web" or mention Fotocal. Ask the English questions (19 and 20) in an English-locale session.
5. If the assistant offers web search and does not use it on its own, record that. Then ask the same question once more in a new chat with search turned on, and log it as a separate row with "(search on)" added after the assistant's name.

**What to record (one row per question per assistant):**

- the date
- the assistant and its mode
- the question number
- whether Fotocal is mentioned by name (yes or no)
- whether a getfotocal.com URL is cited, and which one
- the number the assistant gives, for dish and calculator questions
- which competitors are mentioned or cited
- notes

Save a screenshot or the shared link for each answer in which Fotocal appears.

**Scoring.** For each assistant, count the questions where Fotocal is mentioned and the questions where a getfotocal.com URL is cited. Track both counts month over month. A citation counts for more than a mention.

**What to change when Fotocal is not mentioned:**

| What you see | What to change |
|---|---|
| The assistant gives a number but cites Consumer.es, FatSecret or Fitia | Check that the Fotocal page states the answer in its first sentence, with the number and the portion in grams, as the dish pages already do. Make sure the page is in `sitemap.xml` and `llms.txt`, and is linked from `/calorias/tabla-de-calorias/` and from at least one blog post. Add the question, worded exactly as asked, as a heading or an FAQ entry. |
| The assistant gives a range ("200 to 300 kcal") and cites no one | Add a short section comparing ways of serving the dish (pincho, ración, 100 g, homemade or bar), so that Fotocal's page explains the range. |
| An app question names Yazio, MyFitnessPal, Fitia or FatSecret but not Fotocal | Assistants rely on third-party lists. Pursue listings on alternativeto.net and Spanish app roundups (androidphoria and similar), and keep the `/comparativa/` pages dated and current. Make sure the Play Store description uses the same words: "contar calorías con foto", "gratis", "comida española". |
| The assistant says no free photo app exists for Android | Make the home page, `/features/scan-food/` and `/faq/` say "Android" and "gratis: 2 escaneos al día" in plain text near the top, not only inside an image or a table. |
| A calculator question cites Omni or Yazio | Lead with the worked example (as `/calculadoras/calorias-diarias/` does) and make sure the page names the formula and the official sources (Mifflin-St Jeor, WHO, EFSA) in plain text. Add an example number to `/calculadoras/agua/`. |
| The answer is wrong or out of date about Fotocal (for example "it works on iPhone" or "it is paid") | Fix the matching sentence in `/faq/` and `llms.txt` so the correct fact is stated in one line. |
| A "new page needed" row is still unanswered | Build that page first (the 1,500 kcal menu; any dish pages with priority 1 in `keywords.csv`). |
| No change after 3 months of mentions without citations | Check that AI crawlers can reach the site: `robots.txt` must allow GPTBot, Google-Extended and PerplexityBot. Also check how fast the page responds to a request without JavaScript, since assistants read the HTML as served. |

Change only one or two things a month, and note them in the results table's notes column so the next month's result can be attributed to the change.

## Results table (blank template)

Copy this block for each monthly run.

| Date | Assistant (mode) | Q# | Question | Fotocal mentioned (yes/no) | Cited URL | Number given | Competitors mentioned | Notes / change made |
|---|---|---|---|---|---|---|---|---|
| | ChatGPT | 1 | ¿Cuál es la mejor app para contar calorías gratis? | | | | | |
| | Gemini | 1 | ¿Cuál es la mejor app para contar calorías gratis? | | | | | |
| | Perplexity | 1 | ¿Cuál es la mejor app para contar calorías gratis? | | | | | |
| | ChatGPT | 2 | | | | | | |
| | Gemini | 2 | | | | | | |
| | Perplexity | 2 | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |

**Monthly summary**

| Month | Assistant | Questions asked | Fotocal mentioned | getfotocal.com cited | Top competitor cited | Changes shipped since last run |
|---|---|---|---|---|---|---|
| | ChatGPT | 20 | | | | |
| | Gemini | 20 | | | | |
| | Perplexity | 20 | | | | |
