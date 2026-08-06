# -*- coding: utf-8 -*-
"""Generate one unique, on-brand SVG cover per blog post.

Design system (matches assets/css/site.css tokens):
  · cream base #FDF9F0 with a warm gradient wash
  · accent family: pink #E91E63 -> orange #FF7A3D, plus supporting
    green #17B26A, gold #E8A50C, sky #38BDF8
  · one line-art food/health glyph, large, plus soft blobs + dots
Uniqueness = glyph x palette x geometry x accent-dot layout, seeded
from the post slug, so a given post always renders the same cover.
"""
import os, re, hashlib, html

OUT = "assets/img/blog"
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 675

# ── warm palettes (from the live design tokens) ──
PALETTES = [
    ("#FFE9D6", "#FFD3B0", "#E9633F", "#B23A1E"),   # peach
    ("#FDE4EC", "#F9C9DC", "#E91E63", "#A81348"),   # pink
    ("#FFF0D2", "#FCE0A8", "#E8A50C", "#A9760A"),   # gold
    ("#E5F6EC", "#C8EBD8", "#17B26A", "#0D7A48"),   # green
    ("#FFEBDD", "#FFD8BC", "#FF7A3D", "#C4501D"),   # orange
    ("#E9F1FB", "#CFE0F5", "#3B82C4", "#255A8E"),   # cool blue
    ("#F3EAFB", "#E2D0F6", "#7C3AED", "#54219F"),   # violet
]

# ── line-art glyphs: 24x24 viewBox paths, drawn with stroke ──
GLYPHS = {
 "apple":     "M12 7c-3 0-5 2-5 5.5S9 21 12 21s5-4 5-8.5S15 7 12 7zM12 7c0-2 1-3.5 3-4",
 "leaf":      "M20 4C10 4 4 9 4 16c0 2 1 4 1 4s8-1 12-5c3-3 3-11 3-11zM6 20C9 15 13 11 18 8",
 "drop":      "M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z",
 "flame":     "M12 3s4 4.5 4 8a4 4 0 0 1-8 0c0-1.5.6-2.8 1.2-3.8M12 21a6 6 0 0 0 6-6c0-2-1-3.5-2-5M12 21a6 6 0 0 1-6-6c0-1 .3-2 .8-3",
 "chart":     "M3 3v18h18M8 16v-5M13 16V8M18 16v-9",
 "trend":     "M3 17l6-6 4 4 8-8M14 7h7v7",
 "heart":     "M20.8 6.6a5.5 5.5 0 0 0-7.8 0L12 7.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 23.2l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.8z",
 "clock":     "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3.5 3.5",
 "scale":     "M4 8h16M12 8V5M6 8l-2.5 7a4 4 0 0 0 8 0L9 8M18 8l-2.5 7a4 4 0 0 0 8 0L21 8M9 21h6",
 "cutlery":   "M7 3v8a2 2 0 0 0 4 0V3M9 11v10M17 3c-1.5 1.5-2 3-2 5v3h3V3zM18 11v10",
 "cup":       "M5 8h11v7a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V8zM16 10h2a2.5 2.5 0 0 1 0 5h-2M7 4c0-1 .8-1.5.8-2.5M11 4c0-1 .8-1.5.8-2.5",
 "fish":      "M3 12c3-4 7-6 11-6 3 0 5 2 6 4-1 4-5 8-10 8-3 0-5-2-7-6zM21 10l0 4M8 11h.01",
 "egg":       "M12 3c-4 0-7 6-7 11a7 7 0 0 0 14 0c0-5-3-11-7-11z",
 "grain":     "M12 21V8M12 8c0-3 2-5 5-5 0 3-2 5-5 5zM12 8C12 5 10 3 7 3c0 3 2 5 5 5zM12 14c0-3 2-5 5-5 0 3-2 5-5 5zM12 14c0-3-2-5-5-5 0 3 2 5 5 5z",
 "carrot":    "M9 12l3-7 3 7M4 20c3-1 9-3 12-8M4 20l6-2M4 20l2-6",
 "broccoli":  "M12 21v-7M8 14a4 4 0 0 1-1-7.7A4 4 0 0 1 14 4a4 4 0 0 1 4 4 4 4 0 0 1-2 6z",
 "moon":      "M20 14a8.5 8.5 0 0 1-10.5-11A8.5 8.5 0 1 0 20 14z",
 "brain":     "M12 5.5A3.5 3.5 0 0 0 5.6 3.6 3 3 0 0 0 3.6 8.7 3.2 3.2 0 0 0 4.4 14 3 3 0 0 0 8 18.6a3 3 0 0 0 4 1.9zM12 5.5a3.5 3.5 0 0 1 6.4-1.9 3 3 0 0 1 2 5.1 3.2 3.2 0 0 1-.8 5.3A3 3 0 0 1 16 18.6a3 3 0 0 1-4 1.9zM12 5.5v15",
 "dumbbell":  "M6 8v8M4 10v4M18 8v8M20 10v4M6 12h12",
 "barcode":   "M4 6v12M8 6v12M12 6v12M16 6v12M20 6v12",
 "camera":    "M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h3l2-3h6l2 3h3a2 2 0 0 1 2 2zM12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
 "basket":    "M4 9h16l-1.5 10.5A2 2 0 0 1 16.5 21h-9A2 2 0 0 1 5.5 19.5zM9 9L11 3M15 9L13 3M10 13v4M14 13v4",
 "plate":     "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10z",
 "sprout":    "M12 21v-8M12 13c0-3-2-5-5-5-1 0-2 .3-2 .3C5 11 8 13 12 13zM12 13c0-4 3-7 6-7 .7 0 1 .2 1 .2C19 10 16 13 12 13z",
 "avocado":   "M12 2.5c-3.6 0-5.6 3.4-5.6 6.8 0 1.7-1.4 2.7-1.4 5.2C5 18.4 8.1 21.5 12 21.5s7-3.1 7-7c0-2.5-1.4-3.5-1.4-5.2 0-3.4-2-6.8-5.6-6.8zM12 11.5a3 3 0 1 0 0 6 3 3 0 0 0 0-6z",
 "bread":     "M4 10a4 4 0 0 1 4-4h8a4 4 0 0 1 0 8v5a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-9",
 "berry":     "M4 8.5 9.5 5.5 15 8.5 9.5 11.5ZM4 8.5v6l5.5 3v-6M15 8.5v6l-5.5 3M13.5 15.5 18 13l4.5 2.5L18 18ZM13.5 15.5v3.2L18 21.2M22.5 15.5v3.2L18 21.2",
 "milk":      "M9 3h6v3l2 4v9a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2v-9l2-4zM7 12h10",
 "target":    "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 13.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z",
 "shield":    "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
 "star":      "M12 3l2.6 5.6 6 .8-4.4 4.3 1.1 6.1L12 17l-5.3 2.8 1.1-6.1L3.4 9.4l6-.8z",
 "bottle":    "M10 2h4v3.5l2 3V20a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2V8.5l2-3zM8 13h8",
 "list":      "M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01",
 "sun":       "M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4",
 "bowl":      "M3 11h18a9 9 0 0 1-18 0zM8 7c0-1.5 1-2 1-3M12 6c0-1.5 1-2 1-3M16 7c0-1.5 1-2 1-3",
}
GK = sorted(GLYPHS)

def seeded(slug):
    h = hashlib.md5(slug.encode("utf-8")).hexdigest()
    return [int(h[i:i+4], 16) for i in range(0, 32, 4)]

def cover_svg(slug, category, glyph=None, pal=None):
    s = seeded(slug)
    g = glyph or GK[s[0] % len(GK)]
    p1, p2, acc, deep = PALETTES[(pal if pal is not None else s[1]) % len(PALETTES)]
    geo = s[2] % 4
    rot = (s[3] % 14) - 7
    bx, by = 60 + s[4] % 90, 40 + s[5] % 70
    gid = "g" + hashlib.md5(slug.encode()).hexdigest()[:6]

    # background geometry variants — keeps every cover visually distinct
    if geo == 0:
        deco = (f'<circle cx="{980+s[6]%80}" cy="{110+s[7]%60}" r="230" fill="{acc}" opacity=".10"/>'
                f'<circle cx="{170}" cy="{600}" r="180" fill="{deep}" opacity=".07"/>')
    elif geo == 1:
        deco = (f'<path d="M0 {430+s[6]%70} C 300 {330+s[7]%60} 720 {560} 1200 {400}' 
                f' L1200 675 L0 675 Z" fill="{acc}" opacity=".12"/>'
                f'<circle cx="{1040}" cy="{140}" r="150" fill="{deep}" opacity=".07"/>')
    elif geo == 2:
        deco = ''.join(
            f'<circle cx="{110+i*152}" cy="{80+((i*67)%110)}" r="{26+((i*23)%30)}" fill="{acc}" opacity=".13"/>'
            for i in range(8))
        deco += f'<circle cx="200" cy="590" r="210" fill="{deep}" opacity=".06"/>'
    else:
        deco = (f'<rect x="-60" y="{380+s[6]%60}" width="1320" height="420" rx="120" fill="{acc}" opacity=".11"'
                f' transform="rotate(-6 600 500)"/>'
                f'<circle cx="{1010}" cy="{130}" r="170" fill="{deep}" opacity=".07"/>')

    # small floating accent dots, unique arrangement per slug
    dots = ''.join(
        f'<circle cx="{90+((s[(i%8)]*(i+3))%1020)}" cy="{70+((s[(i+2)%8]*(i+5))%520)}" '
        f'r="{4+((s[(i+1)%8])%7)}" fill="{deep}" opacity=".{14+(i%3)}"/>'
        for i in range(7))

    label = html.escape(category.upper())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{html.escape(category)}"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p1}"/><stop offset="1" stop-color="{p2}"/></linearGradient><radialGradient id="{gid}h" cx=".3" cy=".2" r=".9"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs><rect width="{W}" height="{H}" fill="url(#{gid})"/>{deco}<rect width="{W}" height="{H}" fill="url(#{gid}h)"/>{dots}<circle cx="{bx+430}" cy="{by+240}" r="150" fill="#FFFFFF" opacity=".34"/><g transform="translate({bx+430},{by+240}) rotate({rot}) scale(15)"><g transform="translate(-12,-12)" fill="none" stroke="{deep}" stroke-opacity=".92" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"><path d="{GLYPHS[g]}"/></g></g></svg>'''
