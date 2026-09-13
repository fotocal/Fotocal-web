#!/usr/bin/env python3
"""
Render tools/premium_features.json — the one place the site says what Premium
includes — into the spots that read it:

  · src/subscription/index.html, twice, between source-only markers:
      <!--# premium:list -->  …  <!--# /premium:list -->      the nine lines above the plan cards
      <!--# premium:detail --> … <!--# /premium:detail -->    the nine lines with a sentence each
  · assets/js/i18n-pages.js, in BOTH language blocks, between
      /* premium:generated */ … /* /premium:generated */     sub.pl1..9 and sub.plb1..9

    python3 tools/premium_list.py          write
    python3 tools/premium_list.py --check  exit 1 if anything is stale, or if the
                                           titles differ from the app's array
Then run tools/build_site.py as usual. check_site.py runs --check itself.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "premium_features.json")
PAGE = os.path.join(ROOT, "src", "subscription", "index.html")
I18N = os.path.join(ROOT, "assets", "js", "i18n-pages.js")
L_OPEN, L_CLOSE = "<!--# premium:list -->", "<!--# /premium:list -->"
D_OPEN, D_CLOSE = "<!--# premium:detail -->", "<!--# /premium:detail -->"
J_OPEN, J_CLOSE = "/* premium:generated */", "/* /premium:generated */"


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _between(src, open_m, close_m, body, label):
    a, b = src.find(open_m), src.find(close_m)
    if a < 0 or b < 0 or b < a:
        raise SystemExit("%s: markers %s / %s missing" % (label, open_m, close_m))
    return src[: a + len(open_m)] + "\n" + body + "\n" + src[b - len(src[:b]) + b:][0:0] + src[b:] if False else src[: a + len(open_m)] + "\n" + body + "\n              " + src[b:]


def render_page(page, data):
    feats = data["features"]
    lst = "\n".join('              <li data-i18n="sub.pl%d">%s</li>' % (i + 1, esc(f["title"]["en"])) for i, f in enumerate(feats))
    det = "\n".join('            <li><b data-i18n="sub.pl%d">%s</b><span data-i18n="sub.plb%d">%s</span></li>'
                    % (i + 1, esc(f["title"]["en"]), i + 1, esc(f["body"]["en"])) for i, f in enumerate(feats))
    page = re.sub(re.escape(L_OPEN) + r".*?" + re.escape(L_CLOSE), lambda m: L_OPEN + "\n" + lst + "\n              " + L_CLOSE, page, count=1, flags=re.S)
    page = re.sub(re.escape(D_OPEN) + r".*?" + re.escape(D_CLOSE), lambda m: D_OPEN + "\n" + det + "\n            " + D_CLOSE, page, count=1, flags=re.S)
    return page


def render_i18n(src, data):
    feats = data["features"]
    def block(lang):
        lines = []
        for i, f in enumerate(feats):
            lines.append('      "sub.pl%d": %s,' % (i + 1, json.dumps(f["title"][lang], ensure_ascii=False)))
        for i, f in enumerate(feats):
            lines.append('      "sub.plb%d": %s,' % (i + 1, json.dumps(f["body"][lang], ensure_ascii=False)))
        return "\n".join(lines)
    parts = re.split(r"(" + re.escape(J_OPEN) + r".*?" + re.escape(J_CLOSE) + r")", src, flags=re.S)
    gens = [p for p in parts if p.startswith(J_OPEN)]
    if len(gens) != 2:
        raise SystemExit("i18n-pages.js: expected two %s blocks (en, es), found %d" % (J_OPEN, len(gens)))
    langs = iter(["en", "es"])
    out = []
    for p in parts:
        if p.startswith(J_OPEN):
            out.append(J_OPEN + "\n" + block(next(langs)) + "\n      " + J_CLOSE)
        else:
            out.append(p)
    return "".join(out)


def app_titles(data):
    """The FEATURES array in the app checkout, when it is on disk; else None."""
    src = data.get("app_source") or {}
    path = os.path.join(src.get("local_checkout", ""), src.get("file", ""))
    if not (src.get("local_checkout") and os.path.exists(path)):
        return None
    ts = open(path, encoding="utf-8").read()
    i = ts.find("const %s: Array" % src.get("symbol", "FEATURES"))
    if i < 0:
        return None
    blk = ts[i: ts.index("];", i)]
    rows = re.findall(r"\{ es: '((?:[^'\\]|\\.)*)', en: '((?:[^'\\]|\\.)*)' \}", blk)
    return [{"es": es.replace("\\'", "'"), "en": en.replace("\\'", "'")} for es, en in rows]


def check(data):
    problems = []
    page = open(PAGE, encoding="utf-8").read()
    if render_page(page, data) != page:
        problems.append("src/subscription/index.html: Premium lists are out of date with tools/premium_features.json — run tools/premium_list.py")
    i18n = open(I18N, encoding="utf-8").read()
    if render_i18n(i18n, data) != i18n:
        problems.append("assets/js/i18n-pages.js: sub.pl*/sub.plb* are out of date with tools/premium_features.json — run tools/premium_list.py")
    app = app_titles(data)
    if app is not None:
        ours = [{"es": f["title"]["es"], "en": f["title"]["en"]} for f in data["features"]]
        if app != ours:
            problems.append("tools/premium_features.json: titles differ from the app's %s array (%s) — the app changed, or the site did; make them identical"
                            % (data["app_source"]["symbol"], data["app_source"]["file"]))
    return problems


if __name__ == "__main__":
    data = load()
    if "--check" in sys.argv:
        probs = check(data)
        for p in probs:
            print(p)
        sys.exit(1 if probs else 0)
    page = open(PAGE, encoding="utf-8").read()
    open(PAGE, "w", encoding="utf-8").write(render_page(page, data))
    i18n = open(I18N, encoding="utf-8").read()
    open(I18N, "w", encoding="utf-8").write(render_i18n(i18n, data))
    app = app_titles(data)
    print("rendered %d lines; app checkout %s" % (len(data["features"]), "matches" if app == [{"es": f["title"]["es"], "en": f["title"]["en"]} for f in data["features"]] else ("NOT on disk" if app is None else "DIFFERS")))
