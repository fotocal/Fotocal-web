#!/usr/bin/env python3
"""
Turn a raw app capture into the screen image a CSS device frame holds.

    python3 tools/screen_crop.py <raw> <out.webp> trim=<px> cut=<px> [width=W] [strip=1]

  trim=T   drop the OS status bar (T raw rows off the top)
  top=Y    start the crop at raw row Y (after trim) instead of the top —
           for a screen whose interesting part is further down; the
           status strip is still drawn above it
  cut=Y    keep rows up to Y (raw coordinates, after trim) — the nearest
           quiet row at or after Y is used, so the cut never lands on a
           card; the row actually used is printed
  strip=1  add a status strip above the UI in the app's own background
           colour, sampled from the capture, so the frame's punch-hole
           sits on plain ground and not on the app's header
  ratio=R  make every crop in a context the SAME height: H = width × R.
           The cut is the last quiet row at or above H and the image is
           padded to H with the app's own ground, so frames sized alike
           show alike and the holder's edge always lands on plain ground.
  pad=bottom  in ratio mode, take the padding colour from the rows just
           above the cut instead of the top rows — for a screen whose top
           is a photo (the result screen) and whose ground is below it
  width=W  output width (default 640)

The frame itself is CSS (.dev-frame in assets/css/site.css): one frame
style for dark and light sections, and the image carries the screen only.
tools/frame_screen.py (the baked frame) remains for the other pages.
"""
import sys
from PIL import Image


def is_quiet(px, im, y, x_frac=(0.08, 0.92), thresh=0.985):
    x0, x1 = int(im.width * x_frac[0]), int(im.width * x_frac[1])
    cols = {}
    for x in range(x0, x1, 2):
        r, g, b = px[x, y]
        k = (r >> 3, g >> 3, b >> 3)
        cols[k] = cols.get(k, 0) + 1
    return max(cols.values()) / ((x1 - x0) // 2) >= thresh


def quiet_row(im, target, span=400, direction=1):
    """First row at/after target (direction 1) or at/before it (-1) where
    ≥98.5% of the screen width is one colour (bucketed)."""
    px = im.convert("RGB").load()
    rows = range(target, min(im.height, target + span)) if direction > 0 else range(min(target, im.height - 1), max(-1, target - span), -1)
    for y in rows:
        if is_quiet(px, im, y):
            return y
    return target


def main():
    args = [a for a in sys.argv[1:] if "=" not in a]
    opts = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    src, out = args
    im = Image.open(src).convert("RGB")
    trim = int(opts.get("trim", 0))
    im = im.crop((0, trim, im.width, im.height))
    top = int(opts.get("top", 0))
    if top:
        top = quiet_row(im, top)
    if "ratio" in opts:
        H = round(im.width * float(opts["ratio"]))
        cut = top + H
        used = quiet_row(im, min(cut, im.height - 1), direction=-1)
        src_rows = (used - 4, used) if opts.get("pad") == "bottom" else (top, top + 4)
        bg = im.crop((0, src_rows[0], im.width, src_rows[1])).resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        crop = im.crop((0, top, im.width, used))
        padded = Image.new("RGB", (im.width, H), bg)
        padded.paste(crop, (0, 0))
        im = padded
    else:
        cut = int(opts["cut"]) if "cut" in opts else im.height
        used = quiet_row(im, cut) if "cut" in opts else cut
        im = im.crop((0, top, im.width, used))
    if opts.get("strip", "1") == "1":
        st = round(im.width * 0.082)
        bg = im.crop((0, 0, im.width, 4)).resize((1, 1), Image.LANCZOS).getpixel((0, 0))
        canvas = Image.new("RGB", (im.width, im.height + st), bg)
        canvas.paste(im, (0, st))
        im = canvas
    # never upscale: a frame is never shown above the capture's own pixels,
    # so the output is at most the source width
    w = min(int(opts.get("width", 640)), im.width)
    if w != im.width:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(out, "WEBP", quality=82, method=6)
    print("%-44s %dx%d  rows %d-%d (asked %s-%d)  ratio %.2f" % (out, im.width, im.height, top, used, opts.get("top", 0), cut, im.height / im.width))


if __name__ == "__main__":
    main()
