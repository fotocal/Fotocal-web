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
