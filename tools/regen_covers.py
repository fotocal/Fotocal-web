#!/usr/bin/env python3
"""Regenerate every blog cover, preserving each post's glyph/palette pair.

Reads the pairing back out of the existing SVGs is not possible (they carry
no metadata), so the mapping lives here. Edit it when you add a post.
Run from the repository root:  python3 tools/regen_covers.py
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_covers import cover_svg  # noqa: E402

MAP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog_covers.json")

def main():
    if not os.path.exists(MAP_FILE):
        sys.exit(f"missing {MAP_FILE} — it maps slug -> (category, glyph, palette)")
    mapping = json.load(open(MAP_FILE, encoding="utf-8"))
    total = 0
    for slug, m in mapping.items():
        path = os.path.join("assets", "img", "blog", f"{slug}.svg")
        open(path, "w", encoding="utf-8").write(
            cover_svg(slug, m["category"], glyph=m["glyph"], pal=m["pal"]))
        total += os.path.getsize(path)
    print(f"regenerated {len(mapping)} covers, {total // 1024} KB total")

if __name__ == "__main__":
    main()
