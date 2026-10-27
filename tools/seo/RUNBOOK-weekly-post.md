# Runbook: one new Spanish blog post every Monday

Set up on 26 October 2026 at the owner's request. A scheduled task wakes
the standing Claude Code cloud session that already holds push access to
this repository every Monday at 08:38 (Europe/Madrid) and follows this
file. (A fresh-session variant was tried twice the same day and could not
push: a new session starts with no repository credentials. Do not switch
back to it without re-testing.) A second task on Tuesday at 09:41 checks
that Monday's post landed and runs the procedure if it did not.
It has no end date. One post per week, not two. No approval needed per
post; the owner gets one line when it is live, or the reason it is not.

## 0 · Non-negotiables (from the owner, all still in force)

- Spanish first, written for Spain. An English twin only where it
  genuinely serves an English query (a global question like "how many
  calories to lose a kilo"; never for menús, tapas, Mercadona, prices).
- Real figures only: the app's own data (`tools/dishes/app-data.json`,
  the published `/calorias/` pages, the calculators' worked examples) or
  a real source quoted with its name and the date it was checked. Nothing
  invented, nothing copied from a competitor. No search volumes, ever.
- Do not name competitors. Criteria plus Fotocal is enough.
- Wherever "gratis" appears, the limits must be on the same screen: 2 AI
  scans a day, 1 voice log a day, barcode and Coach Kal unlimited, no card.
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

## 1 · Set up (5 minutes)

```
cd /home/user/Fotocal-web || git clone https://github.com/fotocal/Fotocal-web /home/user/Fotocal-web
git checkout main && git pull origin main
```
If the clone is missing and cannot be made, stop and report that.

Before writing anything, prove you can publish: force-push `main` to the
standing test branch `test/weekly-push-check` (branch deletion is not
possible through the session's git proxy, so the same branch is reused
every week; force pushes are only blocked on `main`).
```
git push -f origin main:refs/heads/test/weekly-push-check
```
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
3. One post. If two look equally good, take the one with the weaker first
   page of results.

## 3 · Write it (the bulk of the work)

- File: `tools/blog/posts/<slug>.json`, slug in Spanish, lower case,
  hyphens. Copy the structure of `calorias-menu-del-dia.json`.
- Fields: `slug`, `langs: ["es"]` (omit for a bilingual post and then
  provide `en` too), `category` (one of the series categories in
  `tools/blog/series.json`), `date` and `updated` = today, `keywords`,
  `cover` (`category` label, `glyph` from `tools/blog_covers.py` GLYPHS,
  `pal` 0–6), `seo.es.title` ≤ 60 characters and `seo.es.desc` 150–160
  characters (measure with Python, not by eye), `es.title` (the H1, the
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
node tools/check_mobile.mjs      # 360 px layout: no overflow, no tap target under 24 px
node tools/check_calcs.mjs       # the four calculators still give the right answers
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
`git push -u origin main`, then `gh run watch` the "Deploy to GitHub
Pages" run until it is green. If it is red, fix it in the same session;
never leave a red deploy.

## 5 · Report (one line, every week)

Live: `https://getfotocal.com/blog/<slug>/` — supports `<money page>`
(cluster X). Add a second line only if something needs the owner (for
example, B2 waiting on captures, or a figure that needs a label photo).

If the week fails for any reason (no clone, build error that cannot be
fixed, no sound topic, deploy red), say exactly why in that line instead
of staying silent, and leave `main` in a working state.
