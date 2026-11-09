# Six-month SEO plan for getfotocal.com (November 2026 – April 2027)

Plain English. Since 9 November 2026, **Claude owns this plan end to end**. A weekly routine every Monday and a monthly review on the first Monday do the site work (`tools/seo/RUNBOOK-weekly-post.md`). The owner's assistant does the few steps that need the owner's browser: Search Console, posting links and directory forms. Their list is `docs/seo/ASSISTANT.md`. The owner does not need to do any SEO task. He only answers the rare question the weekly line raises.

Ranking takes time. Expect the first movement in Search Console after 4–8 weeks, and real traffic after 3–6 months. Links and steady new pages matter more than anything else here.

## Who does what

| Every… | Claude (automatic) | Owner's assistant (browser) |
|---|---|---|
| Monday | 1 blog post (ES + EN); 4–6 dish pages (ES + EN); 1 older page refreshed; build, checks, deploy, sitemap and IndexNow; a line in `weekly-log.md`; a one-line message to the owner | — |
| Week | — | 2 directory listings (`backlinks/directories.md`) |
| Second Tuesday | — | 1 Web 2.0 article (`backlinks/web20/`) |
| First Monday of the month | the monthly review: `kpis.md`, keyword priorities, a 5-line summary in `monthly-report.md` | before 09:00: Search Console export and the AI check (`ASSISTANT.md` M1–M3) |
| Quarter | re-check the comparison facts (`tools/compare_data.json`) and the AI "new page needed" rows | — |

## Month 1: foundations (November 2026)

Goal: Google and Bing know every page, and the routine runs on its own.

Done:
- Methodology page, comparison pages, guides hub and calculator widget.
- Answer boxes and source links on every dish and calculator page.
- The footer "Lo más buscado" list, and IndexNow on every deploy.
- `keywords.csv` (353 keywords), `gaps.md` (30 gaps), `onpage.csv` (all pages).
- The 6 Web 2.0 articles, the directory pack and the outreach drafts.
- 9 Nov: the A1 post, 5 new dish pages (58 in total) and the weekly routine extended.

Assistant, once:
- Resubmit the sitemap.
- Bing Webmaster Tools import.
- Check the social profiles.

Assistant, from 17 Nov:
- The first Web 2.0 article (Blogger).
- Directories, two a week.

## Months 2–3: scale the content and the links (December 2026 – January 2027)

Goal: about 100 dish pages, the cluster posts and the drafts published, and the first real links.

Claude, every Monday:
- Blog posts in this order: the remaining cluster articles (C3, E1, E2, A2, B2), then the six drafts in `docs/seo/drafts/`, then new topics from research.
- Dish pages: priority-1 rows of `keywords.csv` first (`tools/seo/dish_queue.py`).
- The weekly refresh.

Claude, by 9 December: refresh the comparison facts. They go stale 90 days after 10 September.

Assistant:
- Web 2.0 articles #2 and #3 in December, #4 and #5 in January.
- Directories until the list is done.
- First monthly export on 7 December.

## Months 4–6: expand and refresh (February – April 2027)

Goal: about 150 dish pages, the best pages sharpened from real Search Console data, and links that keep coming.

Claude:
- Dish pages until about 150, then two refreshes a week instead.
- The monthly review steers the refreshes:
  - pages at position 8–20 get more internal links and a sharper first paragraph;
  - pages with many impressions and few clicks get a new title and description.
- New comparison pages only for apps whose own site has been read and dated.
- Later, only if the first ones work: the bigger templates from `gaps.md`, i.e. the walking and body-fat calculators, the 1,500 kcal menu guide, and the fruit and drink hubs.

Assistant: Web 2.0 article #6 (Dev.to, after the owner approves the text), and the monthly exports.

Owner, only if he wants to: the Product Hunt launch day, and the outreach and press emails in `backlinks/outreach.md` and `backlinks/mentions.md`. They go out in his name, so they are not automated.

## Changes made by the monthly review

The monthly routine adds one row per month: what it changed in the keyword priorities or the plan, and why.

| Month | Change | Why (data) |
|---|---|---|
| Nov 2026 | Start: dish queue = priority 1 rows of `keywords.csv`; posts = cluster plan, then drafts | No Search Console data yet |
