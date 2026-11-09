# SEO KPIs and how to read them

There was no Search Console access from the build environment, so no baseline numbers are recorded yet. Fill in the "Baseline" column the first time you do the monthly review, with the date. Never estimate: leave a cell empty if you can't read it.

## The numbers

| KPI | Where | Baseline (date: ____) | Month 1 | Month 2 | Month 3 | Month 6 |
|---|---|---|---|---|---|---|
| Impressions, last 28 days | Search Console → Performance (Web) | | | | | |
| Clicks, last 28 days | same | | | | | |
| Average CTR | same | | | | | |
| Average position | same | | | | | |
| Pages indexed / submitted | Search Console → Pages / Sitemaps | / 300 | | | | |
| Pages with impressions | Performance → Pages tab, count rows | | | | | |
| Installs from the website | Play Console → Statistics → Store listing acquisition, filter utm_source = web | | | | | |
| Installs by page type | same, split by utm_medium: home, features, blog, tool, dish, compare, calculadoras, calorias | | | | | |
| Referring domains | Search Console → Links → Top linking sites | | | | | |
| AI assistants naming Fotocal | `docs/seo/ai-visibility.md` test, out of 60 (20 questions × 3 assistants) | | | | | |

## The top 30 keywords to follow

Thirty priority-1 rows of `docs/seo/keywords.csv` whose target page exists: seven calculators, six app queries, five guides and twelve dishes. Claude reads them every month from the Search Console export (see "Where the numbers come from" below). To look one up by hand in Search Console:
1. Go to Performance and add a Query filter, using "Query containing" with the keyword.
2. Note its clicks, impressions and position.

| Keyword | Target page | Baseline position | M1 | M2 | M3 | M6 |
|---|---|---|---|---|---|---|
| calculadora de calorías | /calculadoras/calorias-diarias/ | | | | | |
| cuántas calorías necesito al día | /calculadoras/calorias-diarias/ | | | | | |
| calculadora imc | /calculadoras/imc/ | | | | | |
| calculadora déficit calórico | /calculadoras/deficit-calorico/ | | | | | |
| calculadora macros para perder grasa | /calculadoras/macros/ | | | | | |
| cuánta proteína necesito al día | /calculadoras/proteinas/ | | | | | |
| peso saludable para mi altura | /calculadoras/peso-saludable/ | | | | | |
| app contar calorías con foto | / and /features/scan-food/ | | | | | |
| app para contar calorías gratis | / and /blog/app-contar-calorias-gratis/ | | | | | |
| mejor app para contar calorías gratis | /comparativa/ | | | | | |
| alternativa a myfitnesspal | /comparativa/fotocal-vs-myfitnesspal/ | | | | | |
| registrar comida por voz | /features/voice-logging/ | | | | | |
| app contar calorías comida española | / | | | | | |
| cómo contar calorías sin pesar | /blog/track-calories-without-weighing/ | | | | | |
| déficit de 500 calorías | /blog/deficit-500-calorias-dia/ | | | | | |
| calorías menú del día | /blog/calorias-menu-del-dia/ | | | | | |
| calorías de las tapas | /blog/calorias-de-las-tapas/ | | | | | |
| calorías desayuno español | /blog/calorias-desayuno-espanol/ | | | | | |
| calorías tortilla de patatas | /calorias/tortilla-de-patatas/ | | | | | |
| calorías paella | /calorias/paella-valenciana/ | | | | | |
| calorías croquetas de jamón | /calorias/croquetas-de-jamon/ | | | | | |
| calorías cocido madrileño | /calorias/cocido-madrileno/ | | | | | |
| calorías patatas bravas | /calorias/patatas-bravas/ | | | | | |
| calorías lentejas | /calorias/lentejas-estofadas/ | | | | | |
| calorías gazpacho | /calorias/gazpacho/ | | | | | |
| calorías churros con chocolate | /calorias/churros-con-chocolate/ | | | | | |
| calorías ensaladilla rusa | /calorias/ensaladilla-rusa/ | | | | | |
| calorías pulpo a la gallega | /calorias/pulpo-a-la-gallega/ | | | | | |
| calorías salmorejo | /calorias/salmorejo/ | | | | | |
| tabla de calorías comida española | /calorias/tabla-de-calorias/ | | | | | |

## How to read them

- **Impressions up, clicks flat:** you rank, but the snippet does not convince. Rewrite the title and description of the pages with the most impressions.
- **Position 8–20:** close to page one. Give the page more internal links and a sharper first paragraph, and check its answer box.
- **Indexed is well below submitted:** open Search Console → Pages and read the reason ("Crawled, currently not indexed" usually means the page needs more unique value or links).
- **Installs:** compare `utm_medium` values. A page type that brings traffic but no installs needs a better download card or copy, not more pages.

## Setup steps (once)

1. Resubmit the sitemap: Search Console → Sitemaps → `https://getfotocal.com/sitemap.xml` → Submit.
2. Bing Webmaster Tools: sign in at bing.com/webmasters, then "Import from Google Search Console". IndexNow already sends Bing every changed page on each deploy.
3. Optional, Looker Studio: create a report with the "Search Console" connector (site impression and URL impression tables) for a one-page monthly dashboard.

## Where the numbers come from (from November 2026)

Claude owns the SEO plan and has no Search Console or Play Console login. The owner's assistant exports the numbers once a month (first Monday, before 09:00 Madrid) and uploads them to the repository; the monthly routine reads them the same day. Steps are in `docs/seo/ASSISTANT.md`, task M1.

- `docs/seo/gsc/<YYYY-MM>/`: the Search Console Performance export (last 28 days, Web), unzipped: `Queries.csv`, `Pages.csv`, `Countries.csv`, `Devices.csv`, `Dates.csv`, plus `Chart.csv` if present.
- `docs/seo/gsc/<YYYY-MM>/indexing.txt`: two numbers copied by hand from Search Console → Pages: indexed and not indexed.
- `docs/seo/ai-checks/<YYYY-MM>.csv`: the AI visibility test (task M2).

If a month's folder is missing, the monthly routine fills nothing in, says so in `monthly-report.md`, and keeps the previous priorities.
