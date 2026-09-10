#!/usr/bin/env python3
"""
Turn a raw app capture into the screen image a CSS device frame holds.

    python3 tools/screen_crop.py <raw> <out.webp> trim=<px> cut=<px> [width=W] [strip=1]

  trim=T   drop the OS status bar (T raw rows off the top)
  cut=Y    keep rows up to Y (raw coordinates, after trim) — the nearest
           quiet row at or after Y is used, so the cut never lands on a
           card; the row actually used is printed
  strip=1  add a status strip above the UI in the app's own background
           colour, sampled from the capture, so the frame's punch-hole
           sits on plain ground and not on the app's header
  width=W  output width (default 640)

The frame itself is CSS (.dev-frame in assets/css/site.css): one frame
style for dark and light sections, and the image carries the screen only.
tools/frame_screen.py (the baked frame) remains for the other pages.
"""
import sys
from PIL import Image


def quiet_row(im, target, x_frac=(0.08, 0.92), thresh=0.985, span=400):
    """First row at/after target where ≥98.5% of the screen width is one
    colour (bucketed), scanning up to `span` rows down."""
    px = im.convert("RGB").load()
    x0, x1 = int(im.width * x_frac[0]), int(im.width * x_frac[1])
    for y in range(target, min(im.height, target + span)):
        cols = {}
        for x in range(x0, x1, 2):
            r, g, b = px[x, y]
            k = (r >> 3, g >> 3, b >> 3)
            cols[k] = cols.get(k, 0) + 1
        if max(cols.values()) / ((x1 - x0) // 2) >= thresh:
            return y
    return target


def main():
    args = [a for a in sys.argv[1:] if "=" not in a]
    opts = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    src, out = args
    im = Image.open(src).convert("RGB")
    trim = int(opts.get("trim", 0))
    im = im.crop((0, trim, im.width, im.height))
    cut = int(opts["cut"]) if "cut" in opts else im.height
    used = quiet_row(im, cut) if "cut" in opts else cut
    im = im.crop((0, 0, im.width, used))
    if opts.get("strip", "1") == "1":
        st = round(im.width * 0.082)
        bg = im.crop((0, 0, im.width, 4)).resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        canvas = Image.new("RGB", (im.width, im.height + st), bg)
        canvas.paste(im, (0, st))
        im = canvas
    w = int(opts.get("width", 640))
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(out, "WEBP", quality=82, method=6)
    print("%-44s %dx%d  cut row %d (asked %d)" % (out, im.width, im.height, used, cut))


if __name__ == "__main__":
    main()
