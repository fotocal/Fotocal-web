#!/usr/bin/env python3
"""
Render every logo asset the site needs from one master.

    python3 tools/make_icons.py <master.png>

The master is the brand mark on a fully transparent ground. Everything
below is generated from it, so re-running after a logo change is the whole
update — there is no hand-cropped file to keep in step.

TWO TREATMENTS, ON PURPOSE
  in-page (nav, footer, sticky bar)  transparent, full bleed
      The mark sits directly on cream. Anything behind it — a tile, a
      radius, a shadow — reads as a white box on a warm background, which
      is what the previous app-icon-style asset forced.

  icons (favicon, apple-touch, PWA)  solid ink #1B2340
      A tab is 16px of silhouette. Transparent, the thin multicoloured
      ring loses definition against a light tab bar, and iOS composites a
      transparent touch icon onto black anyway. Ink keeps one recognisable
      shape in light and dark browser themes both.

Sizes are rendered at their real pixel size rather than scaled in the
browser: a 96px source squeezed into 16px by the tab bar is mush.
"""

import os
import sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_IMG = os.path.join(ROOT, "assets", "img")
OUT = os.path.join(ROOT, "assets")

INK = (27, 35, 64)          # --ink, the site's dark
LOGO_SIZES = (32, 64, 96)   # nav is 32 CSS px, sticky bar 40 -> 1x/2x/3x


def load_master(path):
    """Trim to the mark and centre it in a square, so every downstream
    render is framed identically regardless of the export's own padding."""
    m = Image.open(path).convert("RGBA")
    box = m.getbbox()
    if box:
        m = m.crop(box)
    w, h = m.size
    s = max(w, h)
    sq = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sq.alpha_composite(m, ((s - w) // 2, (s - h) // 2))
    return sq


def render(master, size, bg=None, pad=0.0, radius=0):
    """One icon. pad is a fraction of the canvas left clear on each side."""
    inner = max(1, round(size * (1 - 2 * pad)))
    art = master.resize((inner, inner), Image.LANCZOS)
    if bg is None:
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    else:
        canvas = Image.new("RGBA", (size, size), bg + (255,))
        if radius:
            # Draw the corner mask at 4x and downsample: a rounded rect drawn
            # straight at 16px has visibly jagged corners.
            k = 4
            mask = Image.new("L", (size * k, size * k), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                [0, 0, size * k - 1, size * k - 1], radius * k, fill=255)
            canvas.putalpha(mask.resize((size, size), Image.LANCZOS))
    off = (size - inner) // 2
    canvas.alpha_composite(art, (off, off))
    return canvas


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True)
    print("  %-38s %s" % (os.path.relpath(path, ROOT), "%dx%d" % img.size))


def main():
    # The master lives in tools/ rather than assets/: it is a build input,
    # and the deploy workflow drops tools/ from the artifact, so a 1 MB
    # source file is never served to anyone.
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tools/logo-master.png")
    master = load_master(src)
    print("master %dx%d -> assets" % master.size)

    # ── in-page mark: transparent, full bleed ──
    for s in LOGO_SIZES:
        save(render(master, s), os.path.join(OUT_IMG, "logo-%d.png" % s))
    # logo.png keeps its name and its URL: the Organization and BlogPosting
    # structured data on 56 pages point at it, and anything outside the repo
    # that ever linked the old file now resolves to the new mark. 512 because
    # that is what the Organization schema declares, and a declaration that
    # does not match the file is the kind of thing Search Console flags.
    save(render(master, 512), os.path.join(OUT_IMG, "logo.png"))

    # ── browser tab: ink tile, lightly rounded, tighter padding the smaller
    #    it gets because at 16px there is no room to spend on margin ──
    for s, pad, r in ((16, 0.06, 3), (32, 0.09, 6), (48, 0.09, 9)):
        save(render(master, s, INK, pad, r), os.path.join(OUT, "favicon-%d.png" % s))

    ico = os.path.join(OUT, "favicon.ico")
    render(master, 48, INK, 0.09, 9).save(
        ico, sizes=[(16, 16), (32, 32), (48, 48)])
    print("  %-38s 16+32+48" % os.path.relpath(ico, ROOT))

    # ── home-screen icons: ink, SQUARE ──
    #    iOS applies its own corner mask to apple-touch-icon and Android
    #    launchers mask the PWA icons, so pre-rounding them would show a
    #    rounded tile inside a rounded mask. Padding is generous enough that
    #    a circular mask does not clip the mark.
    save(render(master, 180, INK, 0.12), os.path.join(OUT, "apple-touch-icon.png"))
    save(render(master, 192, INK, 0.14), os.path.join(OUT, "icon-192.png"))
    save(render(master, 512, INK, 0.14), os.path.join(OUT, "icon-512.png"))

    # ── favicon.svg ──
    # Kept as an SVG wrapping a PNG, exactly as before: every one of the 72
    # pages already links this path, and an SVG favicon may not fetch an
    # external image, so the bitmap has to be inlined. The artwork is a
    # gradient illustration, not something that vectorises faithfully.
    import base64, io
    buf = io.BytesIO()
    render(master, 96, INK, 0.09, 18).save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">\n'
        '  <title>Fotocal</title>\n'
        '  <!-- The Fotocal mark. Embedded as a data URI on purpose: an SVG\n'
        '       favicon may not fetch external images, and every page already\n'
        '       points at this one file, so the logo updates everywhere\n'
        '       without touching any page markup.\n'
        '       Regenerate with tools/make_icons.py — do not hand-edit. -->\n'
        '  <image width="96" height="96" href="data:image/png;base64,%s"/>\n'
        '</svg>\n' % b64)
    p = os.path.join(OUT, "favicon.svg")
    open(p, "w", encoding="utf-8").write(svg)
    print("  %-38s %.1f KB" % ("assets/favicon.svg", len(svg) / 1024))


if __name__ == "__main__":
    main()
