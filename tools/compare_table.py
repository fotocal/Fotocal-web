#!/usr/bin/env python3
"""
Render tools/compare_data.json — the one place competitor facts live —
into the two spots the site reads them from:

  · the <tbody> of the comparison table in src/index.html, between the
    source-only markers  <!--# compare:generated -->  /  <!--# /compare:generated -->
  · the dated footnote "cmp.note" (en + es) in assets/js/i18n.js

    python3 tools/compare_table.py          write both
    python3 tools/compare_table.py --check  exit 1 if either is stale

Then run tools/build_site.py as usual. check_site.py runs --check itself
and warns when checked_on is older than 90 days.
"""
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "compare_data.json")
PAGE = os.path.join(ROOT, "src", "index.html")
I18N = os.path.join(ROOT, "assets", "js", "i18n.js")
OPEN, CLOSE = "<!--# compare:generated -->", "<!--# /compare:generated -->"
STALE_DAYS = 90

TIER = {"premium": "cmp.premium", "pro": "cmp.pro", "gfit": "cmp.gfit"}
MONTHS_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def date_text(iso, lang):
    d = datetime.date.fromisoformat(iso)
    if lang == "es":
        return "%d de %s de %d" % (d.day, MONTHS_ES[d.month - 1], d.year)
    return d.strftime("%-d %B %Y")


def cell(label, value, us=False):
    attrs = ' data-label="%s"' % label + (' class="c-us"' if us else "")
    if value is None:
        inner = ('<span class="na" aria-hidden="true">—</span>'
                 '<span class="sr-only" data-i18n="cmp.na">Not stated on the maker\'s site</span>')
    elif value == "yes":
        inner = '<span class="yes">✓</span>'
    elif value in TIER:
        inner = '<span class="part" data-i18n="%s">%s</span>' % (TIER[value], {"premium": "Premium", "pro": "Pro", "gfit": "Google Fit"}[value])
    else:
        inner = '<span class="price">%s</span>' % value
    return "<td%s>%s</td>" % (attrs, inner)


def tbody(data):
    lines = []
    for row in data["rows"]:
        price = row["key"] == "cmp.r12"
        tr = '<tr class="compare-price">' if price else "<tr>"
        tds = cell("Fotocal", row["fotocal"], us=True)
        for col in data["columns"]:
            tds += cell(col, row["cells"][col])
        lines.append('              %s<th data-i18n="%s"></th>%s</tr>' % (tr, row["key"], tds))
    return "\n".join(lines)


def render_page(src, data):
    a, b = src.index(OPEN) + len(OPEN), src.index(CLOSE)
    return src[:a] + "\n" + tbody(data) + "\n              " + src[b:]


def render_i18n(src, data):
    for lang in ("en", "es"):
        note = data["note"][lang].replace("{date}", date_text(data["checked_on"], lang))
        pat = re.compile(r'("cmp\.note": ")([^"]*)(")')
        # the en block comes first in the file, then es: replace the nth
        hits = list(pat.finditer(src))
        assert len(hits) == 2, "expected two cmp.note keys, found %d" % len(hits)
        m = hits[0 if lang == "en" else 1]
        src = src[:m.start(2)] + json.dumps(note, ensure_ascii=False)[1:-1] + src[m.end(2):]
    return src


def main():
    data = load()
    page = open(PAGE, encoding="utf-8").read()
    i18n = open(I18N, encoding="utf-8").read()
    new_page, new_i18n = render_page(page, data), render_i18n(i18n, data)
    stale = [p for p, old, new in ((PAGE, page, new_page), (I18N, i18n, new_i18n)) if old != new]
    if "--check" in sys.argv:
        age = (datetime.date.today() - datetime.date.fromisoformat(data["checked_on"])).days
        if stale:
            print("stale: %s — run tools/compare_table.py" % ", ".join(os.path.relpath(p, ROOT) for p in stale))
            sys.exit(1)
        print("compare table in sync; competitor data checked %d day(s) ago" % age)
        sys.exit(2 if age > STALE_DAYS else 0)
    for p, new in ((PAGE, new_page), (I18N, new_i18n)):
        with open(p, "w", encoding="utf-8") as f:
            f.write(new)
    print("wrote %s and %s (checked_on %s)" % (os.path.relpath(PAGE, ROOT), os.path.relpath(I18N, ROOT), data["checked_on"]))


if __name__ == "__main__":
    main()
