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

Take the 30 priority-1 rows of `docs/seo/keywords.csv` that target pages which already exist. Track each one every month in Search Console:
1. Go to Performance and add a Query filter, using "Query containing" with the keyword.
2. Note its clicks, impressions and position.

| Keyword | Target page | Baseline position | M1 | M2 | M3 | M6 |
|---|---|---|---|---|---|---|
| calculadora de calorías | /calculadoras/calorias-diarias/ | | | | | |
| calculadora imc | /calculadoras/imc/ | | | | | |
| calculadora déficit calórico | /calculadoras/deficit-calorico/ | | | | | |
| calorías tortilla de patatas | /calorias/tortilla-de-patatas/ | | | | | |
| calorías paella | /calorias/paella-valenciana/ | | | | | |
| app contar calorías con foto | / | | | | | |
| … (25 more from keywords.csv) | | | | | | |

## How to read them

- **Impressions up, clicks flat:** you rank, but the snippet does not convince. Rewrite the title and description of the pages with the most impressions.
- **Position 8–20:** close to page one. Give the page more internal links and a sharper first paragraph, and check its answer box.
- **Indexed is well below submitted:** open Search Console → Pages and read the reason ("Crawled, currently not indexed" usually means the page needs more unique value or links).
- **Installs:** compare `utm_medium` values. A page type that brings traffic but no installs needs a better download card or copy, not more pages.

## Setup steps (once)

1. Resubmit the sitemap: Search Console → Sitemaps → `https://getfotocal.com/sitemap.xml` → Submit.
2. Bing Webmaster Tools: sign in at bing.com/webmasters, then "Import from Google Search Console". IndexNow already sends Bing every changed page on each deploy.
3. Optional, Looker Studio: create a report with the "Search Console" connector (site impression and URL impression tables) for a one-page monthly dashboard.
