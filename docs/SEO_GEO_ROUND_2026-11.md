# SEO + AI-search round — 5 November 2026

Branch `seo-round`, merged to `main` after `tools/check_site.py` (0 warnings),
`check_mobile.mjs`, `check_calcs.mjs` and `check_contact.mjs` all passed.

## What changed, before → after

| Item | Before | After |
|---|---|---|
| Lighthouse, home `/` (mobile) | Perf 74 · A11y 96 · BP 100 · SEO 100 | **Perf 90 · A11y 100 · BP 100 · SEO 100** |
| Lighthouse, `/en/` | 93 · 96 · 96 · 100 (4 console errors) | 88 · **100 · 100** · 100 (0 errors) |
| Lighthouse, `/calorias/` | 95 · 96 · 100 · 100 | 95 · **100** · 100 · 100 |
| Lighthouse, a blog post | 96 · 96 · 100 · 100 | 96 · **100** · 100 · 100 |
| Fonts on English pages | **broken**: inline font paths 404ed on every `/en/` page since 27-10 | fixed (absolute paths) and pinned |
| Descriptions over 155 characters | 106 of 199 pages | **0** (hand-rewritten where it mattered, the rest cut at a clause; the old fallback cut mid-word at 158) |
| Titles over 60 characters | 0 | 0 (now a hard failure in the checker) |
| Pages with valid JSON-LD | 199 / 199 | 201 / 201 |
| App schema | SoftwareApplication, no free-plan or trial detail, Play listed twice in `sameAs`, no TikTok | SoftwareApplication + MobileApplication, featureList, free plan and 5-day trial in the offers, `sameAs` deduplicated + TikTok. **No aggregateRating**: the Play rating cannot be verified from here and your standing rule is never a rating in JSON-LD. |
| FAQPage pages | 90 | 92 (+ the two new articles) · `/faq/` now opens with “¿Cómo funciona Fotocal?” |
| “Gratis” with all four limits | hero showed 3 of 4 (no voice log) | hero and every “gratis” description now show 2 scans + 1 voice log + barcode + coach |
| AI search | nothing specific | `/llms.txt`, a quotable “Qué es Fotocal / What Fotocal is” block on both home pages, explicit Allow for GPTBot, OAI-SearchBot, ChatGPT-User, Google-Extended, PerplexityBot, ClaudeBot, Applebot-Extended in `robots.txt` |
| Contrast / labels | footer headings 4.39:1, language button name hid its “ES” | 5.1:1; button name includes the code |

Lighthouse numbers are lab runs against the built site served locally
(simulated slow 4G, CPU ×4), not field data. `/en/` dropped from 93 to 88
because its fonts now actually load (a small, still “good” CLS of 0.058);
before, it was fast because it was broken.

**New articles** (Spanish, app figures from USDA FoodData Central and
CIQUAL 2025): `/blog/deficit-500-calorias-dia/` (this week's scheduled post),
`/blog/calorias-desayuno-espanol/` (café con leche, tostada, churros),
`/blog/calorias-para-perder-un-kilo/` (the 7,700 kcal figure, Wishnofsky
1958 and Hall et al., *Lancet* 2011). The three topics suggested in the brief
already had pages (`/calorias/paella-valenciana/`, `/calorias/tortilla-de-patatas/`,
`/calorias/cafe-con-leche/`, `/blog/track-calories-without-weighing/`,
`/blog/calorie-deficit-for-fat-loss/` + the deficit calculator), so they were
not duplicated. Ideas for later: menú del día for one person cooking at home;
calorías de la cena española típica; cuánto engorda el aceite de una sartén.

**New pins** (fail the build if they come back): description > 155 and
title > 60 are failures, not warnings; inline-style URLs must resolve; the
browser check fails on any 404.

## Your choice: AI crawlers

`robots.txt` now *explicitly* allows the AI crawlers (they were already
allowed by `User-agent: *`). If you prefer not to be used for AI training,
change `Allow` to `Disallow` for **GPTBot**, **Google-Extended** and
**Applebot-Extended** only; keep **OAI-SearchBot**, **ChatGPT-User** and
**PerplexityBot** allowed, because those are the ones that cite you in answers.

## What you must do in Search Console (15 minutes)

1. Sitemaps → resubmit `https://getfotocal.com/sitemap.xml` (201 URLs).
2. URL inspection → Request indexing for: `/`, `/faq/`,
   `/blog/deficit-500-calorias-dia/`, `/blog/calorias-desayuno-espanol/`,
   `/blog/calorias-para-perder-un-kilo/`.
3. Run Google's Rich Results Test on `https://getfotocal.com/` and
   `https://getfotocal.com/faq/` (it cannot be reached from my environment;
   the JSON-LD parses and matches the page on all 201 pages).

## How to track progress

Search Console → Performance → Search results, last 28 days, filter
**Query contains**: `calorías`, `contar calorías`, `foto`, `déficit`, `app`.
Watch impressions first (weeks 2–6), then position, then clicks (months
2–4). Compare against the 90-day baseline you sent on 28-10: 1,790
impressions, 10 clicks, position 28.1, Spanish 2.3 % of impressions.
For AI answers: once a month ask ChatGPT, Perplexity and Gemini
“mejor app para contar calorías con foto en España” and “cuántas calorías
tiene una tortilla de patatas” and note whether getfotocal.com is cited.

## Off-site: 10 actions only you can do

1. **Google Play listing**: the website link points at `https://getfotocal.com/`, the description repeats the same facts (free limits, prices, trial).
2. **Spanish app directories**: submit to Uptodown, Softonic and AppGallery-style Spanish catalogues with the same one-paragraph description.
3. **Product Hunt launch** on a Tuesday, with the photo-scan GIF; reply to every comment that day.
4. **Spanish nutrition blogs and dietitians**: offer the `/calorias/` table (free, no signup) as a resource; ask for a link, one by one, by email.
5. **A guest article** for a Spanish health or app blog: “cuántas calorías tiene un menú del día”, with a link back to the full table.
6. **Reddit r/spain, r/askspain, r/loseit**: answer real calorie questions with the table's figures; mention Fotocal only when asked which app, and say you make it.
7. **YouTube Short / TikTok / Instagram Reel**: 20 seconds photographing a tortilla de patatas, showing the result, ending on getfotocal.com.
8. **Forocoches / Mediavida / ForoParalelo nutrition threads**: same honesty rule as Reddit.
9. **Press**: a short note to Xataka Android, Andro4all and Hipertextual: “app made in Madrid that counts calories of Spanish food from a photo”.
10. **Google Business Profile**: only if Fotocal has a real address that can receive a postcard; an app with no premises is not eligible, and a fake one gets suspended.

Plain truth: on-page work is close to finished. What moves Spanish
rankings from here is **links from other sites and time**. Expect weeks for
the new pages to be indexed and two to four months before positions settle.
Nothing in this round changes that.
