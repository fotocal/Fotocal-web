# Six-month SEO plan for getfotocal.com (from November 2026)

Plain English. Each month has a goal and a short weekly list for the owner. Tasks for the site itself (new pages, fixes) are done in the repository and checked by the build before they go live.

Ranking takes time. Expect the first movement in Search Console after 4–8 weeks, and real traffic after 3–6 months. Backlinks and time matter more than anything else on this list.

## Month 1: foundations and research (November 2026)

Goal: Google and Bing know every page, and we know which words to chase.

Already done this round:
- Methodology page, comparison pages, guides hub and calculator widget.
- "Respuesta rápida" boxes on every dish and calculator page.
- Source links on every dish, calculator and methodology page.
- The footer "Lo más buscado" list.
- IndexNow on every deploy.
- `docs/seo/keywords.csv` (353 keywords) and `docs/seo/gaps.md` (30 gaps).

Owner, every week:
- Monday: the weekly blog post (the existing task keeps running).
- Once:
  - Resubmit the sitemap in Search Console.
  - Add the site to Bing Webmaster Tools; it can import from Search Console in one click.
  - Note this month's numbers in `docs/seo/kpis.md`.
- Once: publish the first Web 2.0 article (`docs/seo/backlinks/web20/README.md` gives the order).
- Once: create the Product Hunt and AlternativeTo listings (`docs/seo/backlinks/directories.md`).
- Check that every social profile links to getfotocal.com.

## Months 2–3: scale the content and start links (December 2026 – January 2027)

Goal: more pages that answer real searches, and the first real links.

Site:
- Add 4–6 dish pages a week, priority 1 rows first in `keywords.csv`. Use only foods with a full ingredient breakdown in the app (`gen_dishes.figures()` shows `composed: True`).
- Publish 2 blog posts a week from `docs/seo/drafts/`, then new drafts from the keyword clusters.
- Refresh the comparison facts before 9 December 2026: the check gets stale 90 days after 10 September. Re-read each maker's own pages and update `tools/compare_data.json` with the new date.

Owner, every week:
- 1 Web 2.0 article, at most; space them out.
- Send 3–5 outreach emails (`docs/seo/backlinks/outreach.md`), personalised.
- Answer 1–2 real questions on Reddit or Quora, and say you are the maker.
- Log every link in `docs/seo/backlinks/tracker.csv`.

Once a month:
- Run the AI visibility test (`docs/seo/ai-visibility.md`).
- Record the numbers in `kpis.md`.

## Months 4–6: expand and refresh (February – April 2027)

Goal: 120–150 dish pages, the best posts refreshed, links that keep coming.

Site:
- Keep 4–6 dish pages a week until about 150. Then refresh instead of adding: re-check any page whose app figure changed.
- In Search Console → Performance, find pages with many impressions but a low click rate.
  - Rewrite their title and description, and check the answer box answers the query people actually type.
- Find pages ranking 8–20, and give each one more internal links and a better first paragraph.
- New comparison pages only for apps whose own site we have read and dated, the same rules as `tools/compare_data.json`.

Owner:
- A Product Hunt launch, once the listing has screenshots and a short video.
- A widget push: the 20 blogs and dietitians from the outreach file.
- Local Madrid press and startup lists (`docs/seo/backlinks/mentions.md`).
- Optional: an "Estudio: lo que comen los españoles" built from anonymised, aggregated app numbers. Only if you approve it and the privacy policy allows it.

## Every month, the same short review (30 minutes)

1. Search Console:
   - clicks, impressions and position for the top 30 keywords (`kpis.md`)
   - pages indexed versus submitted
   - new errors
2. Play Console → Store listing acquisition: installs by `utm_medium` (home, features, blog, tool, dish, compare…).
3. Ask ChatGPT, Gemini and Perplexity the 20 questions in `ai-visibility.md` and record whether Fotocal is named.
4. Add new links to `tracker.csv`, and check the old ones still exist.
5. Pick next month's 10 dish pages and 8 posts from `keywords.csv`.
