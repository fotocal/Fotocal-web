#!/usr/bin/env python3
"""
Wrap a raw app screenshot in the site's Android device frame.

    python3 tools/frame_screen.py <raw.png|jpg> <out.webp> [cut=Y] [width=W]

One tool for every real screenshot on the site, so the whole series reads
as the same device: a punch-hole Android — the app is Android-only, and
framing its screens inside an iPhone notch was one of the defects this
series of replacements exists to fix.

What it draws, all sizes relative to the screenshot's own width so any
capture resolution lands identically:

  body          ink #1B2340 rounded slab, uniform bezel
  status strip  a short band above the app UI in the app's own background
                colour (sampled from the screenshot's top rows — captures
                have the OS status bar trimmed), carrying the punch-hole
                camera dot. Nothing else: no fabricated clock or battery.
  shadow        soft baked drop shadow, because the ground is transparent
                and the CSS card behind it cannot shadow a shape it
                cannot see
  ground        transparent, so the .illus card's warm gradient shows
                around the device

  cut=Y         drop every screenshot row below Y and let the phone run
                off the bottom edge of the canvas — the "cropped at the
                card edge" crop. Omit to render the whole device.
  width=W       output width in px (default 760 ≈ 2x the widest CSS
                display size). Encoded as WebP q82 with alpha.
"""

import sys
from PIL import Image, ImageDraw, ImageFilter

INK = (27, 35, 64)


def frame(shot, cut=None):
    if cut:
        shot = shot.crop((0, 0, shot.width, cut))
    w = shot.width
    rel = lambda f: round(w * f)

    b = rel(0.024)            # bezel
    R = rel(0.102)            # body corner radius
    st = rel(0.082)           # status strip height
    hole = rel(0.039)         # punch-hole diameter
    m = rel(0.093)            # side margin (room for the shadow)
    mt = rel(0.089)           # top margin

    # sample the app's background from the top rows of the capture, so the
    # strip continues the UI instead of guessing a hex that will drift
    top = shot.convert("RGB").crop((0, 0, w, 4)).resize((1, 1), Image.LANCZOS)
    bg = top.getpixel((0, 0))

    body_w = w + 2 * b
    body_h = b + st + shot.height + (b if not cut else 0)
    cw = body_w + 2 * m
    ch = mt + body_h + (mt if not cut else 0)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))

    # body rectangle; when cut, push its bottom past the canvas so the
    # bottom corners' rounding happens off-stage and the edge stays square
    x0, y0 = m, mt
    x1, y1 = m + body_w, mt + body_h + (R + b if cut else 0)

    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [x0, y0 + rel(0.016), x1, y1 + rel(0.016)], R, fill=(20, 16, 30, 92))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(rel(0.040))))

    body = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(body).rounded_rectangle([x0, y0, x1, y1], R, fill=INK + (255,))
    canvas.alpha_composite(body)

    # screen = status strip + capture, with its top corners rounded to sit
    # inside the bezel; bottom corners only when the whole device shows
    screen = Image.new("RGB", (w, st + shot.height), bg)
    screen.paste(shot.convert("RGB"), (0, st))
    r = R - b
    k = 2
    mask = Image.new("L", (w * k, screen.height * k), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, w * k - 1, (screen.height + (0 if not cut else r)) * k - 1],
        r * k, fill=255)
    sc = screen.convert("RGBA")
    sc.putalpha(mask.resize(screen.size, Image.LANCZOS))
    canvas.alpha_composite(sc, (m + b, mt + b))

    # punch-hole camera, centred in the strip
    dot = Image.new("L", (hole * 4, hole * 4), 0)
    ImageDraw.Draw(dot).ellipse([0, 0, hole * 4 - 1, hole * 4 - 1], 255)
    lens = Image.new("RGBA", (hole, hole), (12, 16, 34, 255))
    lens.putalpha(dot.resize((hole, hole), Image.LANCZOS))
    canvas.alpha_composite(lens, (m + b + (w - hole) // 2, mt + b + (st - hole) // 2))
    return canvas


def main():
    args = [a for a in sys.argv[1:] if "=" not in a]
    opts = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    if len(args) != 2:
        sys.exit(__doc__)
    out_w = int(opts.get("width", 760))
    img = frame(Image.open(args[0]), cut=int(opts["cut"]) if "cut" in opts else None)
    img = img.resize((out_w, round(img.height * out_w / img.width)), Image.LANCZOS)
    img.save(args[1], quality=82, method=6)
    print("%s  %dx%d" % (args[1], *img.size))


if __name__ == "__main__":
    main()
