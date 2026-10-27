#!/usr/bin/env python3
"""AVIF siblings for every WebP screenshot under assets/img (not the SVG blog
covers). tools/build_site.py wraps an <img> in <picture> with an AVIF
<source> only when every candidate in its srcset has a sibling here, so a
partial run is safe. Quality 60 / speed 4 measured at 55–70 % of the WebP
size on these UI captures with no visible loss at display size."""
import glob, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
done = skipped = 0
for src in sorted(glob.glob(os.path.join(ROOT, "assets", "img", "**", "*.webp"), recursive=True)):
    dst = src[:-5] + ".avif"
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        skipped += 1; continue
    im = Image.open(src)
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") and "A" in im.getbands() else im.convert("RGB")
    im.save(dst, "AVIF", quality=60, speed=4)
    done += 1
print("avif: %d written, %d up to date" % (done, skipped))
