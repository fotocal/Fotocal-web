#!/usr/bin/env python3
"""Minified bundles for the stylesheets and scripts, in assets/dist/.

Why: every page loaded three to six render-blocking stylesheets and three
scripts, none minified (Lighthouse, 27-10-2026). One stylesheet per page and
one script per page, minified, is fewer round trips on a slow phone.
tools/build_site.py swaps the individual references for the bundle whose
name matches the page's set of stylesheets, and only if the bundle file
exists, so a stale or missing bundle degrades to the old behaviour, never to
a broken page. Run this whenever anything in assets/css or assets/js changes,
before tools/build_site.py. Minification uses esbuild through npx when it is
reachable; otherwise the bundle is the plain concatenation."""
import os, subprocess, sys, shutil, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, "assets", "css"); JS = os.path.join(ROOT, "assets", "js"); DIST = os.path.join(ROOT, "assets", "dist")
# fonts.css is inlined into the page by the build, never bundled
COMBOS = [("site", "home", "features", "blog", "tools"), ("site", "home", "features", "blog"),
          ("site", "home", "features"), ("site", "home"), ("site", "sections"), ("site",)]
JSB = {"js-core": ["i18n", "layout", "main"], "js-calc": ["calc"], "js-contact-form": ["contact-form"]}
os.makedirs(DIST, exist_ok=True)

def minify(text, kind):
    try:
        with tempfile.NamedTemporaryFile("w", suffix="." + kind, delete=False, encoding="utf-8") as f:
            f.write(text); src = f.name
        r = subprocess.run(["npx", "--yes", "esbuild@0.24.2", src, "--minify", "--target=es2017", "--log-level=error"],
                           capture_output=True, text=True, timeout=180)
        os.unlink(src)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout, True
        sys.stderr.write("esbuild failed for %s: %s\n" % (kind, r.stderr[:200]))
    except Exception as e:
        sys.stderr.write("esbuild unavailable: %s\n" % e)
    return text, False

written = []
for combo in COMBOS:
    text = "\n".join(open(os.path.join(CSS, n + ".css"), encoding="utf-8").read() for n in combo)
    out, ok = minify(text, "css")
    name = "css-" + "-".join(combo) + ".css"
    open(os.path.join(DIST, name), "w", encoding="utf-8").write(out)
    written.append((name, len(text), len(out), ok))
for name, parts in JSB.items():
    text = "\n;\n".join(open(os.path.join(JS, n + ".js"), encoding="utf-8").read() for n in parts)
    out, ok = minify(text, "js")
    open(os.path.join(DIST, name + ".js"), "w", encoding="utf-8").write(out)
    written.append((name + ".js", len(text), len(out), ok))
for name, a, b, ok in written:
    print("%-44s %7d -> %7d bytes %s" % (name, a, b, "minified" if ok else "NOT minified"))
