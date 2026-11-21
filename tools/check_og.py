#!/usr/bin/env python3
"""Share previews: every indexable page must carry og:title, og:description
and og:image; the image must exist, be 1200x630 (or the 1080x1080 square
second card), match its declared size, be under 300 KB, and carry alt text;
twitter:card must be summary_large_image.

    python3 tools/check_og.py        (after tools/build_site.py)"""
import glob, html as H, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://getfotocal.com/"
MAX = 300 * 1024
SIZES = {(1200, 630), (1080, 1080)}


def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def main():
    fails, pages, images = [], 0, set()
    for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT)
        if rel.split(os.sep)[0] in ("src", "docs", "tools", "node_modules"):
            continue
        h = open(f, encoding="utf-8").read()
        if re.search(r'<meta name="robots" content="noindex', h):
            continue
        pages += 1
        get = lambda k, a="property": [H.unescape(x) for x in re.findall(r'<meta %s="%s" content="([^"]*)"' % (a, re.escape(k)), h)]
        for k in ("og:title", "og:description", "og:image", "og:site_name", "og:locale"):
            if not get(k) or not get(k)[0].strip():
                fails.append("%s: no %s" % (rel, k))
        if get("twitter:card", "name") != ["summary_large_image"]:
            fails.append("%s: twitter:card is not summary_large_image" % rel)
        imgs, ws, hs, alts = get("og:image"), get("og:image:width"), get("og:image:height"), get("og:image:alt")
        if len(alts) < len(imgs) or any(not a.strip() for a in alts):
            fails.append("%s: og:image without og:image:alt" % rel)
        for n, url in enumerate(imgs):
            if not url.startswith(SITE):
                fails.append("%s: og:image is not an absolute https URL on the site: %s" % (rel, url))
                continue
            path = os.path.join(ROOT, url[len(SITE):].split("?")[0])
            if not os.path.isfile(path):
                fails.append("%s: og:image file missing: %s" % (rel, url))
                continue
            size = jpeg_size(path) if path.endswith(".jpg") else None
            declared = (int(ws[n]), int(hs[n])) if n < len(ws) and n < len(hs) else None
            if size not in SIZES:
                fails.append("%s: og:image is %s, want 1200x630 or 1080x1080" % (rel, size))
            elif declared != size:
                fails.append("%s: og:image declared %s but the file is %s" % (rel, declared, size))
            if os.path.getsize(path) > MAX:
                fails.append("%s: og:image is %d KB, over 300 KB" % (rel, os.path.getsize(path) // 1024))
            images.add(path)
    for x in fails[:40]:
        print("FAIL " + x)
    if fails:
        print("share previews: %d problem(s)" % len(fails))
        sys.exit(1)
    print("share previews: OK, %d pages, %d images, all present, right size, under 300 KB, with alt text" % (pages, len(images)))


if __name__ == "__main__":
    main()
