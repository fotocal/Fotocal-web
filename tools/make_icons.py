#!/usr/bin/env python3
"""
Render every logo asset the site needs from one master.

    python3 tools/make_icons.py <master.png>

The master is the brand mark on a fully transparent ground. Everything
below is generated from it, so re-running after a logo change is the whole
update — there is no hand-cropped file to keep in step.

TWO TREATMENTS, ON PURPOSE
  tab icons (favicon.svg, 16/32/48, .ico)  transparent, full bleed
      The mark is fully saturated colour with no white and no black in
      it, so the same transparent asset reads correctly on a white tab
      bar and on a black one, unchanged. A tile behind it is what made
      the tab icon a dark square. (Judged at real 16px on light and dark
      surfaces before shipping: the ring holds on both; the yellow-green
      arc is the thinnest segment on white but the ring stays closed.)

  home-screen icons (apple-touch, 192/512, maskable)  opaque cream
      These two MUST stay opaque: iOS composites a transparent
      apple-touch-icon onto black — which would reproduce the exact
      black-square failure — and the maskable icon has to fill its own
      safe area or the launcher shows holes. Cream #FDF9F0, like the
      app's own launcher icon.

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
CREAM = (255, 255, 255)     # --bg, the site's ground (white since the palette re-token)
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

    # ── browser tab: the bare mark, transparent, full bleed — at 16px
    #    every pixel spent on margin is a pixel the ring cannot use ──
    for s in (16, 32, 48):
        save(render(master, s), os.path.join(OUT, "favicon-%d.png" % s))

    ico = os.path.join(OUT, "favicon.ico")
    render(master, 48).save(ico, sizes=[(16, 16), (32, 32), (48, 48)])
    print("  %-38s 16+32+48" % os.path.relpath(ico, ROOT))

    # ── home-screen icons: cream, SQUARE ──
    #    Cream, not ink: on a real phone the ink tile read as a black square,
    #    and the app's own launcher icon is the mark on a light tile — the
    #    website's home-screen icon should look like the app it opens.
    #    Square because iOS masks apple-touch-icon itself and Android masks
    #    the manifest icons; pre-rounding would put a tile inside a mask.
    save(render(master, 180, CREAM, 0.12), os.path.join(OUT, "apple-touch-icon.png"))
    save(render(master, 192, CREAM, 0.12), os.path.join(OUT, "icon-192.png"))
    save(render(master, 512, CREAM, 0.12), os.path.join(OUT, "icon-512.png"))

    # The maskable variant promises Android the mark survives ANY mask the
    # launcher applies. The spec's guaranteed-visible region is the centred
    # circle of 80% diameter, so prove it rather than eyeball it.
    #
    # The assertion runs against the FILE AS WRITTEN, reopened from disk —
    # not the in-memory image it was saved from. A guard that inspects the
    # buffer approves whatever the encoder then does to it; this project
    # has already shipped one guard that contained the exact defect it
    # guarded, so this one checks the artefact, never the intention.
    MASK_PAD = 0.17
    mask_path = os.path.join(OUT, "icon-512-maskable.png")
    save(render(master, 512, CREAM, MASK_PAD), mask_path)
    mk = Image.open(mask_path).convert("RGB")
    if mk.size != (512, 512):
        os.remove(mask_path)
        raise SystemExit("maskable icon on disk is %r, not 512x512" % (mk.size,))
    px, r2 = mk.load(), (0.4 * 512) ** 2
    bad = 0
    for y in range(512):
        for x in range(512):
            if (x - 255.5) ** 2 + (y - 255.5) ** 2 > r2:
                p_ = px[x, y]
                if abs(p_[0]-CREAM[0]) > 8 or abs(p_[1]-CREAM[1]) > 8 or abs(p_[2]-CREAM[2]) > 8:
                    bad += 1
    if bad:
        os.remove(mask_path)   # never leave an artefact its own check rejected
        raise SystemExit("maskable icon: %d mark pixels outside the safe circle — raise MASK_PAD" % bad)
    print("  %-38s safe-circle verified on disk" % os.path.relpath(mask_path, ROOT))

    # ── favicon.svg — no tile, no theme query, on purpose ──
    # The mark is embedded as a data-URI PNG (an SVG favicon may not fetch
    # external images, and a gradient illustration does not vectorise).
    # There used to be an adaptive ink tile here, hidden on dark themes;
    # it is gone because the mark needs no adapting: fully saturated
    # colour with no white and no black in it reads the same on a light
    # tab bar and a dark one. One transparent asset is the whole answer.
    import base64, io
    buf = io.BytesIO()
    render(master, 96).save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">\n'
        '  <title>Fotocal</title>\n'
        '  <!-- Regenerate with tools/make_icons.py - do not hand-edit. -->\n'
        '  <image width="96" height="96" href="data:image/png;base64,%s"/>\n'
        '</svg>\n' % b64)
    p = os.path.join(OUT, "favicon.svg")
    open(p, "w", encoding="utf-8").write(svg)
    print("  %-38s %.1f KB (transparent)" % ("assets/favicon.svg", len(svg) / 1024))


if __name__ == "__main__":
    main()
