# tools/

Small maintenance scripts. Nothing here runs at build or request time —
the site stays a plain static bundle. Run these locally with Python 3
from the repository root when you need to regenerate assets.

## blog_covers.py — blog cover art

Generates the unique SVG cover for a blog post. Every post in
`/blog/<slug>/` has one at `assets/img/blog/<slug>.svg`, used as both
the listing card thumbnail and the article header image.

A cover is a composition of four things, so no two posts look alike:

| ingredient | where it comes from |
|---|---|
| glyph      | chosen from `GLYPHS` to match the post's topic |
| palette    | one of seven warm palettes in `PALETTES` |
| geometry   | one of four background layouts |
| accent dots| seeded from the slug, so a slug always renders identically |

Covers carry **no text**: the category is rendered next to the image as
a translated chip, so the artwork works in English and Spanish alike.

### Add a cover for a new post

```python
import sys; sys.path.insert(0, "tools")
from blog_covers import cover_svg
open("assets/img/blog/my-new-slug.svg", "w", encoding="utf-8").write(
    cover_svg("my-new-slug", "Nutrition", glyph="sprout", pal=3)
)
```

`glyph` and `pal` are optional — omit them and both are derived from the
slug. Pass them explicitly to keep the (glyph, palette) pair unique
against the covers that already exist; `GLYPHS.keys()` lists the 35
available motifs.

### Regenerate every cover

Useful after editing a palette or a glyph path. Keep each post's
existing `glyph`/`pal` pairing so the art does not shuffle around:

```bash
python3 tools/regen_covers.py
```

## What Premium includes — one source (2026-09-14)

`tools/premium_features.json` holds the nine Premium lines, word for word
the FEATURES array in the app's `app/paywall.tsx`, with a gate reference
and a one-sentence explanation each. `tools/premium_list.py` renders them
into the subscription page (the list above the plan cards and the Premium
section) and into `assets/js/i18n-pages.js` (`sub.pl*`, `sub.plb*`);
`check_site.py` fails if either is stale and, when the app checkout is on
disk at the path in `app_source`, if the titles differ from the app's
array. When the app list changes: change the JSON in the same sitting,
run `python3 tools/premium_list.py`, then build. Never write the Premium
list out by hand anywhere else on the site; sentences elsewhere that
mention Premium (home FAQ, the AI page, About, the product JSON-LD) must
stay shorter than this list, never longer.

## Blog — one template, tools/gen_blog.py (2026-09-14)

The 53 posts, nine series hubs and the index are GENERATED. The writing
lives in `tools/blog/posts/<slug>.json` (slug, category, date, optional
`updated`, keywords, optional `caution`, and per language the title,
the one-line lead and the body HTML). `tools/gen_blog.py` renders
`src/blog/<slug>/index.html`, `src/blog/series/<id>/index.html` and
`src/blog/index.html` from one template; `tools/build_site.py` then
renders both trees. To change the template, edit gen_blog.py and run
it; to change a post, edit its JSON, set `updated`, and run it. Never
edit src/blog/ by hand — the next run overwrites it.

**Series** (`tools/blog/series.json`) are the reading order. Every live
post is in exactly one series (the generator asserts it); a post's
previous/next links follow the series, never the date, and the first
and last post of a series point at its hub. Each series sits under one
of six filter chips — calories, weightloss, nutrition, eating, mindset,
movement — named by `blog.cat.<key>` in assets/js/i18n-pages.js; a
post's `category` must match its series' `category`. Series titles are
also i18n keys (`blog.series.t.<id>`) because the hub's breadcrumb
JSON-LD needs them as tokens.

**Retiring a post**: move its JSON to `tools/blog/retired/`, add
`{"old-slug": "target-slug"}` to `tools/blog/redirects.json`, and take
it out of series.json. The old URL then renders a noindex redirect stub
to the target and never 404s. Same rule for merges.
`tools/blog_extract.py` is the one-off that lifted the writing out of
the old hand-built pages; it is kept for the record.

## Spanish blog translations (historical)

`tools/blog_es/b1.py … b9.py` hold the Spanish title, lead and body for
every post, keyed by slug. `tools/inject_es.py` writes them into the
article pages: each post ends up with both languages wrapped in
`[data-lang-block]` elements, and `assets/js/main.js` shows whichever
matches the language switch. A post with no Spanish entry falls back to
English rather than rendering blank.

Re-run after editing a translation (from the repository root):

```bash
python3 tools/inject_es.py
```

The script is idempotent — it strips its own previous injection before
writing, so running it twice is safe.
