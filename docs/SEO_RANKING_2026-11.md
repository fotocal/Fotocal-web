# SEO and AI-search ranking round: report (8 November 2026)

Branch `seo-ranking`. No page was deleted and no URL changed. Every check passed before the merge:
- **Site check:** 328 pages, 164 Spanish + 164 English, 0 problems.
- **Phone check:** 27 pages at 360 px.
- **Language switcher:** 36 checks.
- **Calculators:** 56 checks.
- **Contact form:** passed.

**The honest summary:** the site is now in good shape for Google and for AI assistants. What decides ranking from here is **backlinks and time**. Expect the first movement in Search Console after 4–8 weeks, and real traffic after 3–6 months. Everything for the link work is ready to copy and paste, in `docs/seo/backlinks/`.

## What changed on the site

### New pages (Spanish + English)
- **`/metodologia/`:** where every number comes from, so readers and AI assistants have a page to cite.
  - Sources: USDA FoodData Central, 125 foods; CIQUAL 2025, 28 foods.
  - How a dish is summed, gram by gram, with cooking yields.
  - How the serving is set, and the 25% rule.
  - Every calculator formula, the rounding, the update policy, and who makes Fotocal.
- **`/comparativa/` and three "vs" pages:** Fotocal vs MyFitnessPal, vs Yazio and vs Cal AI.
  - They are built only from `tools/compare_data.json`: each maker's own site, dated 10 September 2026, with the source links shown.
  - There are no Lifesum or FatSecret pages, because we have no verified facts for them.
  - Each page gives an honest "which one to choose", including that Fotocal is Android only.
- **`/guias/`:** all blog posts grouped by topic, each group with its matching calculators. It is the hub for the blog clusters.
- **`/widget/`:** two free, embeddable calculators (calories and BMI) for bloggers and dietitians, with copy-paste code and a "Calculadora de Fotocal" credit link. The embed pages (`/embed/…`) are noindex.
- **Two new blog posts, in both languages:**
  - "¿Cuántas calorías tiene un bocadillo?"
  - "Cena ligera de menos de 500 calorías"

  Six more drafts wait in `docs/seo/drafts/`.

### Every dish and calculator page
- **"Respuesta rápida" box:** 40–60 words that answer the question with the page's own numbers. For example: "La paella valenciana tiene 515 kcal por ración (307 g)…". This is what AI answers and featured snippets quote.
- **A visible line:** "Actualizado: <date> · Por Fotocal, Madrid · Cómo calculamos" (the last part links the methodology).
- **Links to the real sources:**
  - USDA and CIQUAL on the dish pages
  - DOI or official links for Mifflin-St Jeor, WHO, EFSA, IOM and ISSN on the calculators

### Site-wide
- **Footer "Lo más buscado":** the 10 most-searched dishes and 4 calculators, one click from every page. The footer also links guides, comparison and methodology.
- **Blog posts:** each now links two dish pages it actually talks about, plus the calculator for its topic, in both languages. Before, there was one Spanish-only line, the same on every post.
- **Phones:** a small Google Play button sits in the header next to the menu. It is icon-only under 420 px, so it never pushes the layout.
- **UTM tags by page type:** every Play link carries `utm_medium` (home, features, blog, tool, dish, compare…), so Play Console shows which pages bring installs. Details are in `docs/seo/conversion.md`, with two copy variants ready to test.
- **IndexNow:** each deploy now tells Bing, Yandex and others which pages changed. It never blocks a deploy.
- **Entity facts and llms.txt:**
  - The Organization schema now states Madrid, and keeps the Play, Instagram, TikTok, YouTube and Facebook links.
  - `/llms.txt` lists the new pages.
  - AI crawlers (GPTBot, Google-Extended, PerplexityBot, ClaudeBot) were already allowed.

### Errors fixed along the way
- **Feature counts:** after the menu scan was hidden, the features page still said "9 funciones" / "nine features" in its title and in two sentences, and the subscription page said "Se activan nueve cosas". All now say eight.
- **Free-plan wording:** the app card on every blog post left out "1 registro por voz al día". It now has all four limits.
- **Blog index contrast:** a heading on the grey band was 4.39:1 against the 4.5:1 required; it is now 5.9:1. The blog index accessibility score went from 96 to 100.
- **Dish page dates:** their "updated" date now reflects today's real changes, so the sitemap `lastmod` is honest.

## Technical checks

| Check | Result |
|---|---|
| robots.txt and sitemap | OK. One sitemap of 304 URLs with es/en alternates; well under the 50,000 limit, so splitting it adds nothing. `lastmod` comes from each page's own modified date or its last commit. |
| Orphans and click depth | No orphans. Every page is at most **2 clicks** from the home page (the new /widget/ page was the only orphan; it is now linked from the calculator hub). |
| Canonicals, hreflang, 404s | OK, every page (site check). |
| Redirect chains | None. The two old blog redirects point straight at live articles. |
| Structured data | The type each page needs (Article, BlogPosting, WebApplication, FAQPage, NutritionInformation, BreadcrumbList, CollectionPage) is present on every page (`onpage.csv`). |
| On-page checklist | `docs/seo/onpage.csv`: 304 pages × 12 checks. 0 fails on title length, single H1, answer in the first 100 words, description length, heading order, images, internal links, outbound sources, schema, updated date and methodology link. |
| Title/H1 keyword match | 16 pages flagged. They are brand pages whose H1 is a slogan by design ("Una persona, una app…", "Calcula en segundos…"); the title carries the keyword. Your call whether to change those H1s. |

## Lighthouse (phone)

Scores are for performance / accessibility / best practices / SEO.

| Page | Score | Layout shift |
|---|---|---|
| Home `/` | 91 / 100 / 100 / 100 | 0.001 |
| `/calculadoras/calorias-diarias/` | 93 / 100 / 100 / 100 | 0 |
| `/calorias/tortilla-de-patatas/` | 93 / 100 / 100 / 100 | 0 |

The other key pages:

| Page | Performance | Layout shift |
|---|---|---|
| calculator hub | 95 | 0 |
| BMI calculator | 92 | 0 |
| dish hub | 95 | 0 |
| paella | 94 | 0 |
| blog index | 91 | 0.001 |
| scan-food | 86 | 0.003 |
| comparison hub | 96 | 0 |

**Important when you test speed yourself:** PageSpeed Insights and Lighthouse run as an English browser. The first-visit language switch sends them from a Spanish page to its English twin, and the measurement then includes that redirect. To test a Spanish page, add `?lang=es`, e.g. `https://getfotocal.com/calorias/paella-valenciana/?lang=es`. Real visitors are switched at most once. The previous round's Spanish Lighthouse figures were affected the same way.

The English home page shows a small layout shift, 0.058 (the "good" limit is 0.1). It was already on main: the hero text reflows when the web font arrives. Fixing it means tuning the fallback font, which is listed below as a next action.

## Files in `docs/seo/`

| File | What it is |
|---|---|
| `keywords.csv` | 353 keywords (300 Spanish, 53 English) with intent, target page, priority, difficulty and evidence; 199 are priority 1 |
| `gaps.md` | Top 30 gaps against Yazio, MyFitnessPal, FatSecret, Lifesum, Cal AI and Spanish blogs, and how to do each one better |
| `onpage.csv` | The pass/fail audit of all 304 pages; re-run with `python3 tools/seo/onpage_audit.py` |
| `ai-visibility.md` | 20 questions people ask AI, the page that answers each one, and a monthly test with a results table |
| `drafts/` | 8 Spanish blog drafts, 1,141–1,351 words each (2 published) |
| `backlinks/web20/` | 6 original Spanish articles for Blogger, WordPress.com, Medium, LinkedIn, Tumblr and Dev.to, with posting steps and a README on what these links can and can't do |
| `backlinks/directories.md` | 17 directories, with copy-paste descriptions in ES and EN (short and long) |
| `backlinks/outreach.md` | 15 Spanish "best apps" lists, 20 blogs, gyms and dietitians (widget offer), journalist platforms and forum rules, with Spanish email drafts |
| `backlinks/mentions.md` | 20 mention opportunities, each with a Spanish draft |
| `backlinks/tracker.csv` | 70 targets to log as links arrive |
| `plan-6-months.md` | Month-by-month checklist with weekly owner tasks |
| `kpis.md` | What to measure, where, and a blank baseline table |
| `conversion.md` | UTM scheme by page type, and two hero and button variants to test |

**Limits of this research:**
- This environment couldn't reach Google Suggest, Google Trends, Search Console or the competitors' websites.
- The keyword and gap work used a web search tool, which uses a US index, so difficulty is estimated and no search volumes are claimed.
- The directories, blogs and dietitians in the backlink files come from search results; none was opened. Check each URL before writing.
- `devto.md` tells the build story in your voice. Check every line is true before posting it.

## Top 10 next actions for you

1. **Resubmit the sitemap** in Search Console (Sitemaps → `https://getfotocal.com/sitemap.xml`). 304 URLs, including the new pages.
2. **Add the site to Bing Webmaster Tools** with "Import from Google Search Console". IndexNow already pings Bing on every deploy.
3. **Fill in the baseline** in `docs/seo/kpis.md` this week: impressions, clicks, position for the top 30 keywords, and installs by `utm_medium`.
4. **Product Hunt and AlternativeTo listings,** with the copy in `backlinks/directories.md`. These are the two strongest free links.
5. **Publish one Web 2.0 article a week,** in the order in `backlinks/web20/README.md`. Share each on your social profiles, and never batch them.
6. **Send the widget offer** to 3–5 blogs or dietitians a week, from `backlinks/outreach.md`. An embedded calculator with a credit link is the best link you can earn.
7. **Check every social profile** links to getfotocal.com (Instagram, TikTok, YouTube, Facebook, and X, Pinterest and LinkedIn if you create them).
8. **Refresh the comparison facts before 9 December 2026:** re-read the three makers' pages and update the date in `tools/compare_data.json`. The check warns after 90 days.
9. **Run the AI visibility test** in `docs/seo/ai-visibility.md` once a month, and record whether ChatGPT, Gemini and Perplexity name Fotocal.
10. **Keep the content pace:**
    - Two posts a week from `docs/seo/drafts/`, then new drafts from `keywords.csv`.
    - 4–6 new dish pages a week from the priority-1 rows, using only foods with a full ingredient breakdown in the app.
    - Optional, later: the English home font fix, and changing the 16 slogan H1s if you want the keyword in them.
