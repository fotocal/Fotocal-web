# SEO master plan: status (9 November 2026)

Claude owns the plan from today. "Done" means it is live on getfotocal.com or written in `docs/seo/`. "Running" means the weekly or monthly routine carries it forward (`tools/seo/RUNBOOK-weekly-post.md`).

| # | Section | Status | Note |
|---|---|---|---|
| 1 | Keyword research | Done | `keywords.csv` has 353 keywords with intent, page, priority and difficulty. Google Suggest was not reachable, so no volumes are claimed. The monthly review re-ranks the list from Search Console data. |
| 2 | Competitor gaps | Done | `gaps.md` lists 30 gaps. The cheap ones (single dish pages) now flow through the weekly dish queue. The new templates (walking and body-fat calculators, the 1,500 kcal menu, fruit and drink hubs) are scheduled for months 4–6. |
| 3 | On-page checklist | Done | `onpage.csv` covers 316 pages with 0 fails on 11 of 12 checks. The calculator hub and blog index H1s now carry their keyword. 12 brand pages keep their slogan H1 on purpose; the keyword is in their title. |
| 4 | Content plan | Running | Done: /metodologia/, comparison pages, 58 dish pages and 3 new posts this round. Running: 1 post and 4–6 dish pages every Monday until about 150. Six drafts are queued after the cluster plan. "2 posts a week" became 1 a week by the owner's earlier decision. |
| 5 | Technical SEO + IndexNow | Done | Sitemap rebuilt on every build, hreflang, canonicals, no orphans, and every page at most 2 clicks deep. IndexNow pings on each deploy (the wait-and-retry fix went live today). |
| 6 | Internal linking | Done, and running | /guias/ hub, footer "Lo más buscado", and dish↔post↔calculator links. The weekly refresh adds links to each new page. |
| 7 | AEO / GEO | Done, and running | Answer boxes on every dish and calculator page, `llms.txt`, AI crawlers allowed, and `ai-visibility.md` (20 questions). The monthly check is done by the assistant (`ai-checks/`). |
| 8A | Backlinks: Web 2.0 | Ready, not posted | 6 articles in `backlinks/web20/`, each self-contained: title, body, tags, link URLs and anchors, posting steps. First post Tue 17 Nov (assistant). |
| 8B | Backlinks: directories | Ready, not submitted | `backlinks/directories.md` has paste-ready ES/EN texts and step-by-step forms for 8 sites; two a week (assistant). |
| 8C | Backlinks: earned links | Ready, owner's choice | `backlinks/outreach.md` (15 lists, 20 blogs and dietitians, widget offer) and `mentions.md` (20). These go out in the owner's name, so they are not automated. |
| 8D | Backlinks: tracker | Done | `backlinks/tracker.csv` has 76 targets, including the 6 Web 2.0 posts with their dates. The assistant logs; the monthly review reads it. |
| 9 | Conversion | Done | UTM per page type on every Play link, the phone Play button and the download card. The A/B copy variants are written (`conversion.md`) but not running: the site has no testing tool, and installs by `utm_medium` in Play Console are the measure. |
| 10 | Measurement | Running | `kpis.md` has the full top-30 keyword table, `plan-6-months.md`, `weekly-log.md` and `monthly-report.md`. The baseline waits for the first Search Console export (assistant, Mon 7 Dec). |

## v3 on-page rollout (master prompt v3, section C)

Last updated: 14 November 2026.

| PART | What | Status |
|---|---|---|
| 0–2 | Inventory, keyword map (one primary per URL), on-page rules and lint | Done (9 Nov) |
| 3–5 | Striking-distance pages, calculators batch 1 and 2 | Done (9–10 Nov) |
| 6–7 | `/comparativa/` hub, features, EN home H1, English dish titles | Done (10 Nov) |
| 8–10 | All 58 Spanish dish pages: "por 100 g y por ración" sections and FAQ; hub and table top-10 lists | Done (11–14 Nov) |
| 11 | Blog, Spanish batch 1: 14 posts, headline and title carry the primary keyword | Done (14 Nov) |
| 12 | Blog, Spanish batch 2: 14 posts retitled; no Spanish post has an on-page note left | Done (14 Nov) |
| 13 | Blog, English: 19 posts retitled; no English post has an on-page note left | Done (14 Nov) |
| 14 | Blog meta descriptions (35) and the English calorie chart title | Done (14 Nov) |
| 15 | Methodology and about: who writes, who reviews (nobody with a health qualification, stated plainly), corrections, last-reviewed date. Named author and reviewer bios are NOT added: they need real names and credentials from the owner | Done, except bios (14 Nov) |
| D4 | New article «calorías para adelgazar mujer» (ES + EN), table computed from the calculator | Done (14 Nov) |
| D6 | English dish hub: computed top-10 lists; English tapas article already existed | Done (14 Nov) |
| D7 | Calorie table upgrade: printable view was already there; top-10 lists added in PART 10. No PDF (not generated from site data) | Done (14 Nov) |
| D1–D3 | Competitor pages (MyFitnessPal alternatives, Cal AI and Yazio reviews) | Not started: needs fresh, dated competitor facts and the owner's go-ahead |
| D5 | New dish pages, 2–3 a week | Running (Monday routine) |
| D8 | Web photo-scanner demo | Owner decision, not for the agent to build |
<!-- v3-rows -->

Also live outside the numbered PARTs: yearly offer from `tools/pricing.json` (11 Nov), calculator result layout, header at 200 % text, Search Console fixes (no language redirect, schema dates with time zone, inlined home CSS, balanced related-dish links), five strengthened posts (13 Nov).

## Files in `docs/seo/`

| File | What it is |
|---|---|
| `STATUS.md` | this table |
| `ASSISTANT.md` | the browser tasks for the owner's assistant, step by step |
| `keywords.csv` | 353 keywords; dish rows drive the weekly dish queue |
| `gaps.md` | 30 competitor gaps |
| `onpage.csv` | on-page audit of every page (re-run: `python3 tools/seo/onpage_audit.py`) |
| `ai-visibility.md` | 20 AI questions, the test protocol, what to change |
| `ai-checks/TEMPLATE.csv` | the monthly AI check, one row per question and assistant |
| `gsc/` | the monthly Search Console exports (assistant uploads) |
| `plan-6-months.md` | who does what, month by month, plus the monthly change log |
| `kpis.md` | the numbers to track and the top 30 keywords |
| `weekly-log.md` | one line per Monday |
| `monthly-report.md` | five plain-English lines per month for the owner |
| `conversion.md` | UTM scheme and copy variants |
| `drafts/` | 8 blog drafts (2 published, 6 queued) |
| `backlinks/web20/` | README (rules and schedule) and 6 articles |
| `backlinks/directories.md` | directory steps and texts |
| `backlinks/outreach.md`, `backlinks/mentions.md` | email and mention drafts (owner's name) |
| `backlinks/tracker.csv` | every link target and its status |
