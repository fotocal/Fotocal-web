# Runbook: the weekly SEO routine (every Monday) and the monthly review

Set up on 26 October 2026 at the owner's request for one blog post a week;
extended on 9 November 2026 when the owner handed Claude the whole SEO
plan. Every Monday: one blog post (§2–3), 4–6 new dish pages (§3b), one
older page refreshed (§3c), build and deploy with the sitemap and IndexNow
(§4), one line in `docs/seo/weekly-log.md` (§5). The first Monday of each
month also runs the monthly review (§6). The few browser-only steps
(Search Console, posting links, directories) belong to the owner's
assistant and are listed in `docs/seo/ASSISTANT.md`: never wait for them. A scheduled task wakes
the standing Claude Code cloud session that already holds push access to
this repository every Monday at 08:38 (Europe/Madrid) and follows this
file. (A fresh-session variant was tried twice the same day and could not
push: a new session starts with no repository credentials. Do not switch
back to it without re-testing.) A second task on Tuesday at 09:41 checks
that Monday's post landed and runs the procedure if it did not.
It has no end date. One post per week, not two. No approval needed per
post; the owner gets one line when it is live, or the reason it is not.
Work directly on `main` (the routine's changes are additive and fully
checked before the push); larger changes go on a branch and are merged
only when every check passes.

## 0 · Non-negotiables (from the owner, all still in force)

- Spanish first, written for Spain. Since the lang-ux round (8-11-2026)
  every Spanish page has an English twin, blog included: write the
  Spanish post first, then a faithful English version in the same JSON
  (the URL stays the Spanish slug under /en/blog/).
- Real figures only: the app's own data (`tools/dishes/app-data.json`,
  the published `/calorias/` pages, the calculators' worked examples) or
  a real source quoted with its name and the date it was checked. Nothing
  invented, nothing copied from a competitor. No search volumes, ever.
- Do not name competitors. Criteria plus Fotocal is enough.
- Wherever "gratis" appears, the limits must be on the same screen: 2 AI
  scans a day, 1 voice log a day, barcode and Coach Kal unlimited, no card.
- Never type a price. Write `{{price:month}}`, `{{price:year}}` (the yearly
  price in force today) or `{{price:year_month}}`; add `{{offer:note}}` after
  the yearly price where the page states the price as a fact. The values
  and any dated offer live in `tools/pricing.json` (see `tools/pricing.py`).
- No testimonials, review counts, download numbers or awards. Never a
  rating in JSON-LD. The email fotocal.app@gmail.com only on Contact and
  legal pages.
- Every post supports exactly one money page and links to it in the first
  third of the text. The five money pages and their clusters are in
  `tools/seo/plan-clusters.md`.
- Same quality bar as `/blog/calorias-menu-del-dia/` and
  `/blog/calorias-de-las-tapas/` (read both before writing).
- Never leave the site broken. `tools/check_site.py` must end with
  `0 warning(s)`. Never delete or stub working code. Do not touch the app
  repository, its version or build number.
- Commit footer on every commit, two lines: `Co-Authored-By: <the Claude
  model actually serving this session, e.g. Claude Fable 5.1 or Claude
  Sonnet 5.5> <noreply@anthropic.com>` and `Claude-Session: <the URL of
  the session doing the work>`. Name the real model, never assume one.

## 0b · On-page rules (summary of `docs/seo/onpage-rules.md`; read it in full once)

1. One primary keyword per URL: look it up in `docs/seo/keyword-map.md` before writing; never use another URL's primary in a title or H1.
2. Title ≤ 60 characters, primary keyword first, then one differentiator; close to the H1.
3. Meta description ≤ 155: primary in the first sentence, one concrete fact (kcal, formula, price), then a call to action.
4. Exactly one H1, containing the primary keyword naturally.
5. The first 40–60 words answer the question with the number (the answer box), with the primary and one secondary.
6. Each H2 answers one real question from `docs/seo/serp-notes.md` or `keywords.csv` (source PAA/autocomplete).
7. FAQ: 4–6 real questions answered in 1–3 sentences, JSON-LD identical to the visible text.
8. Links: hub + 2–4 siblings + 1 calculator, with the target's primary keyword as the anchor.
9. Images: alt text with the dish or feature name, width/height, WebP, lazy below the fold.
10. A page you touched ends with **zero on-page notes** (`python3 tools/check_site.py --notes`), and the change is logged in `docs/seo/onpage-changes.csv`.

## 1 · Set up (5 minutes)

```
cd /home/user/Fotocal-web || git clone https://github.com/fotocal/Fotocal-web /home/user/Fotocal-web
git checkout main && git pull origin main
```
If the clone is missing and cannot be made, stop and report that.

Before writing anything, prove you can publish:
```
git push --dry-run origin main     # authenticates against the push endpoint, changes nothing
```
"Everything up-to-date" means access is fine. (Until 9-11-2026 this step
force-pushed `main` to the standing branch `test/weekly-push-check`; the
session's safety filter now refuses force pushes, and the dry run proves
the same thing without one.)
If the push is refused for credentials, call the `add_repo` tool
(claude-code-remote) with owner `fotocal`, repo `Fotocal-web`,
access `push`, then retry once. If it is still refused, stop and report
exactly that: do not write the post into a repository you cannot push to.
`main` has a ruleset that blocks force pushes and deletions; the runbook
never does either, so it does not affect you.

## 2 · Choose the post (10 minutes)

1. Open `tools/seo/plan-clusters.md`. Take the **first article in "Orden y
   calendario" that is not yet marked published** (the status block at the
   top says which are done). Skip B2 while the owner has not sent its four
   Spanish captures, and say so in the report.
2. When the planned list is exhausted, **do not stop and do not repeat a
   topic.** Do fresh research:
   - Read `tools/seo/keyword-map.md` (§1 says what the search tool can and
     cannot see: it is a Brave index, not google.es; no volumes).
   - Run 8–12 searches on Spanish, Spain-specific questions around the five
     money pages (dishes and drinks people search "cuántas calorías tiene",
     "déficit calórico" variants, "app para contar calorías" variants,
     "adelgazar" questions). Prefer questions the owner has observed in
     google.es autocomplete or "Otras preguntas" (keyword-map §7 and the
     dated owner notes); the owner may add new ones to the map.
   - Check the topic is not already covered: `tools/seo/titles-descriptions.md`
     and `tools/blog/posts/*.json`.
   - Add the chosen topic to `tools/seo/keyword-map.md` under a section
     "§8 · Cola de temas (añadidos por el runbook semanal)": phrase,
     intent, questions to answer, who ranks (with the date), difficulty,
     money page. Then also append it to the plan's calendar table.
3. Between the plan and fresh research come the six finished drafts in
   `docs/seo/drafts/` that are not published yet (01 menú 1.500 kcal,
   02 alimentos con más proteína, 04 fruta de temporada, 05 déficit para
   perder 5 kilos, 07 merienda, 08 postres españoles), in that order.
   Re-check every figure against the app before using one: drafts can go
   stale when the app data changes. Draft 01 also answers question 18 of
   `docs/seo/ai-visibility.md`.
4. One post. If two look equally good, take the one with the weaker first
   page of results.

## 3 · Write it (the bulk of the work)

- File: `tools/blog/posts/<slug>.json`, slug in Spanish, lower case,
  hyphens. Copy the structure of `calorias-menu-del-dia.json`.
- Fields: `slug`, no `langs` (posts are bilingual: provide `en` too, with
  `seo.en`, `en.title`, `en.lead`, `en.body` and `faq.en`), `category` (one of the series categories in
  `tools/blog/series.json`), `date` and `updated` = today, `keywords`,
  `cover` (`category` label, `glyph` from `tools/blog_covers.py` GLYPHS,
  `pal` 0–6), `seo.es.title` ≤ 60 characters and `seo.es.desc` 140–155
  characters (measure with Python, not by eye; the build trims anything
  over 155), `es.title` (the H1, the
  question as people ask it in Spain), `es.lead`, `es.body`, `faq.es`
  (3 real questions with real answers; none invented to fill the schema),
  `caution: true` only for deficits, rates of loss, fasting, cravings or
  binge eating.
- Body: 1,200–1,800 words, `<h2>` sections, `<ul>`/`<ol>` for figures,
  ends with `<h2>Ideas clave</h2>`. Figures per serving as served, with
  grams, from the app. Links: the money page in the first third; at least
  eight links to `/calorias/<slug>/`, `/calculadoras/…/` or sibling posts,
  all relative (`../../calorias/x/`, `../other-post/`).
- Add the slug to exactly one series in `tools/blog/series.json` (`posts`
  list, and a `notes` entry in both languages). Add the cover to
  `tools/blog_covers.json`.
- Mark it in `tools/seo/plan-clusters.md` (status block at the top:
  published date and URL).

## 3b · New dish pages (2–3 a week while indexing catches up)

**Since 9 Nov 2026 (MASTER PROMPT v3, section C): 2–3 new dish pages a
week, only from `docs/seo/dish-priority.txt`,** until Search Console shows
"not indexed" below about 25 % of URLs (it was 90 of 220 known on
9 Nov). Indexing quality comes before volume. Above that line, go back to
4–6 a week from `keywords.csv` priority, up to about 150 dishes.

```
python3 tools/seo/dish_queue.py 10
```
lists the next candidates: the `dish-priority.txt` list first, then
`docs/seo/keywords.csv` order (priority 1 first; foods with a full
ingredient breakdown before foods with only the app's reference
figure). Skip a "hand" entry unless its figure can be tied to a sourced
row; say so in the log.

**Uniqueness test (spam-policy rule; every page must pass it).** A page
needs its own sourced numbers, a real-serving section (`portion`), a
comparison with similar dishes (`compare` plus a `lighter` or `drivers`
sentence that names one), and at least three FAQ answers that are unique
to this dish and taken from real questions (People also ask in
`docs/seo/serp-notes.md` once it exists). Variations ("100 g",
"Mercadona", "con cebolla", "4 huevos") go in as **sections of the
existing page**, never as new URLs.

Before choosing a title or H1, grep `docs/seo/keyword-map.md` (once it
exists): never use another URL's primary keyword.

For each one, add an entry to `tools/dishes/dishes.json` (append at the
end; copy the shape of the last entry, e.g. `merluza-en-salsa-verde`):
- `slug` = the app id, `app_id`, `name`, `article`, 1–2 real `aliases`,
  `status: "ready"`, `published` and `updated` = today.
- `compare`: 3–4 app dish ids people weigh it against. `blog`: 2–3 post
  slugs that exist in `tools/blog/posts/` (the generator stops on an
  unknown one). `calc`: `macros`, `calorias-diarias` or `deficit-calorico`.
- `portion`, `drivers`, `lighter`: short Spanish paragraphs. Every number
  is a placeholder (`{g}`, `{kcal}`, `{per100}`, `{protein}`, `{carbs}`,
  `{fat}`, `{kcal:<other-id>}`, `{per100*3}`), never typed by hand, except
  ingredient grams read from the app recipe
  (`tools/dishes/app-data.json` → `recipes[<id>]`) or kcal you compute
  from a food's `per100` row. Describe only ingredients the recipe has.
- `faq`: three real questions with answers built from the placeholders,
  and directions ("más que…") checked against the figures.
- English: in `tools/dishes/en.json` add `gloss[<slug>]` (a short English
  explanation), `group_of[<slug>]` (one of the five `groups`), and any
  ingredient name `python3 tools/gen_dishes.py` reports as missing. Edit
  with `json.load` / `json.dump(..., ensure_ascii=False, indent=1)` and
  check that `git diff` shows only additions.

Then run `python3 tools/gen_dishes.py`. Each new dish must print its line
`/calorias/<slug>/ … kcal`. Afterwards run
`python3 tools/seo/dish_queue.py --mark`, which sets those keyword rows
to `existing`.

## 3c · Refresh one older page

Pick one page, in this order of preference:
1. Once Search Console data exists (`docs/seo/gsc/`): a page at position
   8–20 with impressions, or one with many impressions and a low click
   rate. Rewrite its title and description for the query people actually
   type.
2. Otherwise: the dish page or JSON blog post with the oldest `updated`
   date.

Then:
- Sharpen its answer box so the first sentence answers the question with
  the number and the grams.
- Add 2–3 internal links, especially to this week's new pages; also link
  this week's new dish pages from one or two older pages that mention
  them.
- Set `updated` to today.

Never change a URL or remove a page. Hand-written posts in `src/blog/`
(the English-slug originals with no JSON) are refreshed in the same way,
in `src/`, keeping both language blocks.

## 4 · Build, verify, publish

```
python3 tools/regen_covers.py
python3 tools/gen_blog.py
python3 tools/gen_dishes.py      # only if dishes.json changed
python3 tools/bundle_assets.py   # only if anything in assets/css or assets/js changed
node tools/render_chrome.mjs     # only if layout.js or a nav/footer label changed (needs the local server)
python3 tools/gen_avif.py        # only if a new WebP screenshot was added
python3 tools/build_site.py
python3 -m http.server 8765 &    # the share cards render through a local server
node tools/gen_og.mjs            # one share card per page; new post = new card
python3 tools/build_site.py      # second pass picks up the new card
python3 tools/check_site.py      # must print "OK — … 0 warning(s)"; it runs tools/check_pins.py
node tools/check_lang.mjs        # language switcher, both trees
python3 tools/seo/onpage_audit.py  # no new "fail" rows for this week's pages
node tools/check_mobile.mjs      # 360 px layout: no overflow, no tap target under 24 px
node tools/check_calcs.mjs       # the four calculators still give the right answers
node tools/calcs/check_extra.mjs # the tables on the calculator pages still match calc.js
python3 tools/check_calc_layout.py # no calculator result scrolls sideways at 360 or 1280 px, no number breaks (starts its own server)
node tools/audit_header_zoom.mjs  # no page type scrolls sideways on a phone, at normal text or at 200 % text
python3 tools/check_og.py          # every page has og:title, og:description and a 1200x630 card under 300 KB, with alt text
node tools/check_contact.mjs     # the contact form still submits (intercepted, nothing sent)
python3 tools/seo/site_tree.py
python3 tools/seo/titles.py
```
(If `node tools/gen_og.mjs` cannot run, the post still publishes with the
shared card; say so in the report.)
Then check: `blog/<slug>/index.html` exists; for a Spanish-only post,
`en/blog/<slug>/` does not exist and `grep -r "<slug>" en/ --include=index.html`
finds no `href` to it; the `<title>` and description are the seo ones;
`FAQPage` is in the page. Commit (one commit, clear message, the footer),
`git push -u origin main`, then watch the "Deploy to GitHub Pages" run
until it is green. `gh` is not available in the cloud session: use the
GitHub MCP tools (`actions_list` with `list_workflow_runs` and
`deploy.yml`, then `actions_get` with `get_workflow_run`). The session
cannot open getfotocal.com itself, so a green run is the confirmation. The
build rewrites `sitemap.xml` on every run, and the deploy's last step pings
IndexNow with every changed page. That step never fails the deploy;
check its log line ("IndexNow: … URLs, HTTP 200/202") and mention any
other result in the report. If the run is red, fix it in the same session;
never leave a red deploy. If GitHub Pages itself times out ("syncing_files"
then "Timeout reached"), re-run it once from the Actions API; if it fails
again, report it, because that is GitHub's side.

## 5 · Weekly log and report

Add one row at the top of the table in `docs/seo/weekly-log.md`: the date,
the post and its keyword, the new dish pages and their keywords, the
refreshed page, the dish count and the deploy run. Commit it with the
week's work (or in a second small commit once the deploy is green).

Then send the owner one line:

Live: `https://getfotocal.com/blog/<slug>/` — supports `<money page>`
(cluster X) · +N dish pages · refreshed `<page>`

Add a second line only if something needs the owner (for example, B2
waiting on captures, a figure that needs a label photo, or a deploy that
GitHub could not finish).

## 6 · First Monday of the month: the monthly review

Run it after the weekly work, the same day.
1. Read the newest `docs/seo/gsc/<YYYY-MM>/` (uploaded by the assistant;
   `docs/seo/ASSISTANT.md` task M1) and `docs/seo/ai-checks/<YYYY-MM>.csv`
   (task M2). If they are missing, write "no data this month" and skip
   steps 2–3.
2. Fill in this month's column in `docs/seo/kpis.md`, using only numbers
   read from those files: never an estimate.
3. Adjust next month's priorities in `docs/seo/keywords.csv`:
   - a query with impressions that has no page of its own: add a row, or
     raise it to priority 1;
   - a target page at position 8–20: priority 1, so it is first in line
     for §3c refreshes;
   - a dish keyword with no impressions after three months: drop it one
     priority.

   Add a row to `docs/seo/plan-6-months.md` → "Changes made by the
   monthly review" saying what you changed and why.
4. Write five plain-English lines for the owner at the top of
   `docs/seo/monthly-report.md`, under "## <Month YYYY>":
   1. traffic, compared with last month;
   2. what was published;
   3. links won (from `docs/seo/backlinks/tracker.csv`);
   4. what the AI assistants say about Fotocal;
   5. next month's focus.

   No jargon, and no number that is not in the files.
5. Review `tracker.csv`. For every row the assistant set to `live`,
   check the URL appears in Search Console → Links once that data is
   exported. Flag in the report any `to do` row older than 60 days.
6. Every three months, also re-check `tools/compare_data.json` (the
   comparison pages warn 90 days after its date) and
   `docs/seo/ai-visibility.md` "New page needed" rows.

Add a third report line on these Mondays: "Monthly report:
docs/seo/monthly-report.md (<one-line headline>)".

If the week fails for any reason (no clone, build error that cannot be
fixed, no sound topic, deploy red), say exactly why in that line instead
of staying silent, and leave `main` in a working state. If only part
fails (say, the post is live but a dish page would not build), publish
what passed and say what did not.
