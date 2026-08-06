# -*- coding: utf-8 -*-
"""Inject Spanish article content into the blog post pages.

Each post ends up carrying both languages, each wrapped in a
[data-lang-block] element. assets/js/main.js shows the one matching the
chosen language and hides the other, so the existing top-right language
switch flips the whole article — title, lead and body — on one URL.
"""
import glob, importlib, os, re, sys

SCR = "/tmp/claude-0/-home-user-Fotocal-web/4b27db02-dd75-547a-bff9-04baf58fa359/scratchpad/es"
sys.path.insert(0, SCR)

ES = {}
for mod in sorted(os.path.splitext(f)[0] for f in os.listdir(SCR) if f.startswith("b") and f.endswith(".py")):
    m = importlib.import_module(mod)
    ES.update(m.ES)
print(f"translations loaded: {len(ES)}")

done, skipped = 0, []
for path in sorted(glob.glob("blog/*/index.html")):
    slug = path.split("/")[1]
    if slug not in ES:
        skipped.append(slug)
        continue
    s = open(path, encoding="utf-8").read()
    es = ES[slug]

    # Idempotent: strip any previously injected Spanish before re-injecting.
    s = re.sub(r'\n?\s*<h1 class="art-title reveal" data-lang-block="es".*?</h1>', "", s, flags=re.S)
    s = re.sub(r'\n?\s*<p class="art-lead reveal" data-lang-block="es".*?</p>', "", s, flags=re.S)
    s = re.sub(r'\n?\s*<div class="art-body reveal" data-lang-block="es".*?\n      </div>', "", s, flags=re.S)
    # Strip ONLY the markers this script adds. A blanket strip would also
    # remove the en/es markers the page generator writes (dates, card titles),
    # leaving the English copy permanently visible in Spanish mode.
    s = s.replace('<h1 class="art-title reveal" data-lang-block="en">', '<h1 class="art-title reveal">')
    s = s.replace('<p class="art-lead reveal" data-lang-block="en">', '<p class="art-lead reveal">')
    s = s.replace('<div class="art-body reveal" data-lang-block="en">', '<div class="art-body reveal">')

    # Title
    s = re.sub(r'(<h1 class="art-title reveal")(>)(.*?)(</h1>)',
               lambda m: (f'{m.group(1)} data-lang-block="en"{m.group(2)}{m.group(3)}{m.group(4)}'
                          f'\n        <h1 class="art-title reveal" data-lang-block="es" hidden>{es["title"]}</h1>'),
               s, count=1, flags=re.S)
    # Lead
    s = re.sub(r'(<p class="art-lead reveal")(>)(.*?)(</p>)',
               lambda m: (f'{m.group(1)} data-lang-block="en"{m.group(2)}{m.group(3)}{m.group(4)}'
                          f'\n        <p class="art-lead reveal" data-lang-block="es" hidden>{es["lead"]}</p>'),
               s, count=1, flags=re.S)
    # Body
    s = re.sub(r'(<div class="art-body reveal">)(.*?)(\n      </div>)',
               lambda m: (f'<div class="art-body reveal" data-lang-block="en">{m.group(2)}{m.group(3)}'
                          f'\n      <div class="art-body reveal" data-lang-block="es" hidden>\n{es["body"]}\n      </div>'),
               s, count=1, flags=re.S)

    open(path, "w", encoding="utf-8").write(s)
    done += 1

print(f"injected: {done} | still English-only: {len(skipped)}")
if skipped:
    print("pending:", " ".join(skipped))
