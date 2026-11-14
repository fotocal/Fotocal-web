# -*- coding: utf-8 -*-
"""English twins of the dish pages, the dish hub and the full table
(lang-ux round, 2026-11). Called by tools/gen_dishes.py.

Every number comes from gen_dishes.figures(), the same function the Spanish
page uses, so both languages always show the same figures. The words that
are not numbers live in tools/dishes/en.json: a short English gloss per dish
("Paella valenciana (Valencian paella)"), the hub groups, serving labels and
ingredient names. The Spanish pages carry long editorial prose per dish; the
English pages are built from the data (what a serving weighs, where the
energy comes from, what is in it, how it compares) with three questions
answered from the same figures."""
import json, os, re

import gen_dishes as G

EN = json.load(open(os.path.join(G.ROOT, "tools", "dishes", "en.json"), encoding="utf-8"))
SITE = G.SITE


def ne(x, dec=None):
    """English number: 1,650 and 8.3 (same rounding as gen_dishes.n)."""
    if x is None:
        return "—"
    if dec is None:
        dec = 0 if float(x).is_integer() or abs(x) >= 100 else 1
    return ("{:,.%df}" % dec).format(x)


def date_en(iso):
    y, m, d = iso.split("-")
    return "%d %s %s" % (int(d), ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][int(m) - 1], y)


def serving_en(label):
    return EN["serving"].get(label, label)


def gloss(d):
    return EN["gloss"][d["slug"]]


def display(d):
    """'Paella valenciana (Valencian paella)': the Spanish name people search
    for, then what it is. Just one name when the two are the same."""
    nm = EN.get("name", {}).get(d["slug"])
    if nm:      # English first: "Spanish omelette (tortilla de patatas)"
        return G.cap(nm["en"]) + (" (%s)" % d["name"] if nm["es"] else "")
    es, en = G.cap(d["name"]), gloss(d)
    return es if es.lower() == en.lower() else "%s (%s)" % (es, en)


SMALL = {"a", "an", "and", "at", "by", "con", "de", "del", "el", "en", "for", "in", "la", "las", "los", "of", "on", "or", "the", "to", "with", "y", "al", "cl", "ml"}


def title_case(s):
    """'Spanish omelette (tortilla de patatas)' -> 'Spanish Omelette (Tortilla de Patatas)'"""
    out = []
    for i, w in enumerate(s.split(" ")):
        core = w.strip("()")
        out.append(w if (i and core.lower() in SMALL) or core[:1].isdigit() else w.replace(core, core[:1].upper() + core[1:], 1))
    return " ".join(out)


def prose_name(d):
    """The name used inside sentences: the English one where people type an
    English name ("Spanish omelette"), the Spanish one where they do not
    ("gazpacho", "patatas bravas"); never the explanatory gloss."""
    nm = EN.get("name", {}).get(d["slug"])
    return re.sub(r"\s*\(.*?\)", "", nm["en"]) if nm else d["name"]


def kw_name(d):
    """The dish name of the page's English primary keyword: 'spanish omelette', 'gazpacho'."""
    nm = EN.get("name", {}).get(d["slug"])
    return (nm["en"] if nm else d["name"]).lower()


def app_name_en(app_id):
    v = G.HAND[app_id]
    return v.get("name_en") or v["name_es"]


METHOD = {"boiled": "boiled", "stewed": "stewed", "sauteed": "sautéed", "fried": "fried", "grilled": "grilled", "baked": "baked"}


def title_desc(d, fig):
    nm = EN.get("name", {}).get(d["slug"], {})
    full = title_case(display(d))
    short = title_case(nm["en"]) if nm else G.cap(d["name"])     # without the bracket
    title = nm.get("title")
    if not title:
        for cand in ("Calories in %s: per Serving & 100 g" % full, "Calories in %s: per Serving" % full, "Calories in %s" % full,
                     "Calories in %s: per Serving & 100 g" % short, "Calories in %s" % short):
            if len(cand) <= G.TITLE_MAX:
                title = cand
                break
    assert title and len(title) <= G.TITLE_MAX, (d["slug"], title)
    g = fig["serving_g"]
    base = "A serving of %s (%s g) has %s kcal, %s per 100 g: %s g protein, %s g carbs and %s g fat." % (
        prose_name(d), ne(g), ne(fig["kcal"]), ne(fig["per100"]), ne(fig["protein"]), ne(fig["carbs"]), ne(fig["fat"]))
    for tail in (" With the real serving and similar dishes.", " With the real serving.", " Spanish food data.", ""):
        if len(base + tail) <= 155:
            return title, base + tail
    return title, base[:154].rsplit(" ", 1)[0] + "."


def dish_aside_en(d):
    link = G.PLAY + "&utm_source=web&utm_medium=dish&utm_campaign=" + d["slug"] + "-en"
    return G.download_card("en", "Snap a photo of your %s and Fotocal works it out" % G.esc(prose_name(d)),
                           "Fotocal estimates the serving from a photo, with the figures on this page, and lets you fix each ingredient and its grams before saving.", link)


def dish(d, fig, ready_by_app):
    """(title, desc, json-ld blocks, <main> html) for /en/calorias/<slug>/."""
    g = fig["serving_g"]
    url = SITE + "calorias/%s/" % d["slug"]
    title, desc = title_desc(d, fig)
    name = display(d)
    gl = prose_name(d)
    sp = fig["split"]
    top = max((("protein", sp["p"]), ("carbs", sp["c"]), ("fat", sp["f"]), ("alcohol", sp.get("a", 0))), key=lambda x: x[1])
    faq = [
        ("How many calories are in %s?" % gl,
         "A serving of %s (%s, %s g) has %s kcal: %s g protein, %s g carbs and %s g fat. Per 100 g it is %s kcal." % (
             gl, serving_en(fig["serving_label"]), ne(g), ne(fig["kcal"]), ne(fig["protein"]), ne(fig["carbs"]), ne(fig["fat"]), ne(fig["per100"]))),
        ("Where do the calories in %s come from?" % gl,
         "Mostly from %s: about %d of every 100 kcal. The rest is %s." % (
             top[0], top[1], ", ".join("%s %d%%" % (k, v) for k, v in (("protein", sp["p"]), ("carbs", sp["c"]), ("fat", sp["f"]), ("alcohol", sp.get("a", 0))) if k != top[0] and v))),
        ("How many calories are in half a serving or a bigger one?" % (),
         "Half a serving (%s g) is about %s kcal; a serving and a half (%s g), about %s kcal. For any other amount, weigh it and multiply the grams by %s, then divide by 100." % (
             ne(round(g / 2)), ne(round(fig["kcal"] / 2)), ne(round(g * 1.5)), ne(round(fig["kcal"] * 1.5)), ne(fig["per100"]))),
    ]
    grp = EN["group_of"].get(d["slug"])
    peers = sorted(G.figures(x["app_id"])["per100"] for x in G.DISHES if x.get("status") == "ready" and EN["group_of"].get(x["slug"]) == grp)
    if len(peers) >= 5 and fig["per100"]:
        below = sum(1 for p in peers if p < fig["per100"])
        third = "lower" if below < len(peers) / 3.0 else ("higher" if below >= 2 * len(peers) / 3.0 else "middle")
        gname = EN["groups"][grp]["en"].lower()
        faq.append(("Is %s high in calories?" % gl,
                    "At %s kcal per 100 g it is in the %s third of the %d %s on this site, which run from %s to %s kcal per 100 g. A serving (%s g) is %s kcal." % (
                        ne(fig["per100"]), third, len(peers), gname, ne(peers[0]), ne(peers[-1]), ne(g), ne(fig["kcal"]))))
    crumbs = [("Home", SITE), ("Calories in Spanish food", SITE + "calorias/"), (G.cap(kw_name(d)) if d["slug"] in EN.get("name", {}) else G.cap(d["name"]), url)]
    ld = [
        G.ld_block({"@context": "https://schema.org", "@type": "Article", "headline": title.replace(" — Fotocal", ""), "description": desc,
                    "inLanguage": "en", "mainEntityOfPage": url, "url": url, "datePublished": d.get("published"), "dateModified": d.get("updated", d.get("published")),
                    "author": G.ORG, "publisher": G.ORG, "image": SITE + "assets/og-image.png", "about": {"@type": "Thing", "name": name}}),
        G.ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c[0], "item": c[1]} for i, c in enumerate(crumbs)]}),
        G.nutrition_ld(d, fig, url, name=name, lang="en", serving=serving_en(fig["serving_label"])),
        G.ld_block({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "en", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}),
    ]
    o = []
    o.append('\n<main id="main">\n  <article class="post dp">\n    <header class="post-head">\n      <div class="container-narrow">')
    o.append('        <nav class="post-crumbs reveal" aria-label="Breadcrumb"><a href="../../">Home</a><span class="sep" aria-hidden="true">/</span>'
             '<a href="../">Calories in Spanish food</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">%s</a></nav>' % G.esc(crumbs[-1][0]))
    o.append('        <h1 class="post-title reveal">Calories in %s</h1>' % G.esc(name))
    o.append('        <p class="post-lead reveal">A serving of %s (%s g) has %s kcal, %s kcal per 100 g: %s g protein, %s g carbs and %s g fat. Below: what a real serving weighs, where the calories come from and how it compares with similar dishes.</p>'
             % (G.esc(gl), ne(g), ne(fig["kcal"]), ne(fig["per100"]), ne(fig["protein"]), ne(fig["carbs"]), ne(fig["fat"])))
    upd = d.get("updated", d.get("published"))
    o.append('        <div class="post-meta reveal"><span>Updated <time datetime="%s">%s</time></span><span class="dot" aria-hidden="true">&middot;</span><span>By Fotocal, Madrid</span><span class="dot" aria-hidden="true">&middot;</span><a href="../../metodologia/">How we calculate</a></div>'
             % (upd, date_en(upd)))
    o.append('      </div>\n    </header>\n    <div class="container-narrow">')
    o.append('      <div class="answer-box reveal"><p><strong>Quick answer:</strong> %s has %s kcal per serving (%s g) and %s kcal per 100 g. '
             'A serving gives %s g protein, %s g carbs and %s g fat. Half a serving is about %s kcal; a serving and a half, about %s. '
             'Figures from the Fotocal database, built from USDA and CIQUAL.</p></div>'
             % (G.esc(name), ne(fig["kcal"]), ne(g), ne(fig["per100"]), ne(fig["protein"]), ne(fig["carbs"]), ne(fig["fat"]), ne(round(fig["kcal"] / 2)), ne(round(fig["kcal"] * 1.5))))
    o.append('      <div class="dp-kpis reveal">')
    sl = serving_en(fig["serving_label"])
    o.append('        <div class="dp-kpi dp-kpi-main"><b>%s<small>kcal</small></b><span>per serving (%s%s g)</span></div>' % (ne(fig["kcal"]), "" if sl == "1 serving" else G.esc(sl) + ", ", ne(g)))
    o.append('        <div class="dp-kpi"><b>%s<small>kcal</small></b><span>per 100 g</span></div>' % ne(fig["per100"]))
    o.append('        <div class="dp-kpi"><b>%s<small>g</small></b><span>protein per serving</span></div>' % ne(fig["protein"]))
    o.append('        <div class="dp-kpi"><b>%s<small>g</small></b><span>fat per serving</span></div>' % ne(fig["fat"]))
    o.append('      </div>')
    o.append('      <div class="post-body reveal">')
    o.append('      <h2 id="nutrition">Nutrition facts</h2>')
    o.append('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">&nbsp;</th><th scope="col">Per serving (%s g)</th><th scope="col">Per 100 g</th></tr></thead><tbody>' % ne(g))
    rows = [("Calories", fig["kcal"], fig["per100"], "kcal", True), ("Protein", fig["protein"], fig["per100_p"], "g", False),
            ("Carbohydrate", fig["carbs"], fig["per100_c"], "g", False)]
    if fig["sugar"] is not None:
        rows.append(("&nbsp;&nbsp;of which sugars", fig["sugar"], G.r1(fig["sugar"] / g * 100), "g", False))
    rows.append(("Fat", fig["fat"], fig["per100_f"], "g", False))
    if fig["satfat"] is not None:
        rows.append(("&nbsp;&nbsp;of which saturates", fig["satfat"], G.r1(fig["satfat"] / g * 100), "g", False))
    if fig["fiber"] is not None:
        rows.append(("Fibre", fig["fiber"], G.r1(fig["fiber"] / g * 100), "g", False))
    if fig["salt"] is not None:
        rows.append(("Salt", fig["salt"], G.r1(fig["salt"] / g * 100), "g", False))
    for lab, a, b, u, hl in rows:
        c = ' class="hl"' if hl else ""
        o.append('        <tr><th scope="row">%s</th><td%s>%s %s</td><td%s>%s %s</td></tr>' % (lab, c, ne(a), u, c, ne(b), u))
    o.append('      </tbody></table></div>')
    o.append('      <p class="dp-table-note">Average values. Your own plate can be above or below: the recipe, the oil and the size of the serving move the number more than any table. Sources are at the end of the page.</p>')
    o.append('      <h2 id="serving">How big is a real serving?</h2>')
    o.append('      <p>Fotocal counts %s as %s, %s g, the way it is usually served in Spain: %s kcal. Half of that is about %s kcal; a serving and a half, about %s.</p>'
             % (G.esc(gl), G.esc(serving_en(fig["serving_label"])), ne(g), ne(fig["kcal"]), ne(round(fig["kcal"] / 2)), ne(round(fig["kcal"] * 1.5))))
    o.append('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">Amount</th><th scope="col">Grams</th><th scope="col">kcal</th></tr></thead><tbody>')
    for lab, k in (("100 g", 100 / g), ("Half a serving", .5), ("One serving", 1), ("A serving and a half", 1.5)):
        o.append('        <tr%s><td>%s</td><td>%s g</td><td class="hl">%s</td></tr>' % (' class="is-this"' if k == 1 else "", lab, ne(round(g * k)), ne(round(fig["kcal"] * k))))
    o.append('      </tbody></table></div>')
    o.append('      <h2 id="energy">Where the calories come from</h2>')
    parts = [("p", "protein", sp["p"]), ("c", "carbs", sp["c"]), ("f", "fat", sp["f"])] + ([("a", "alcohol", sp["a"])] if sp.get("a") else [])
    o.append('      <p>Of every 100 kcal in %s, about %s.%s</p>' % (G.esc(gl), ", ".join("%d come from %s" % (v, w) for _, w, v in sorted(parts, key=lambda x: -x[2])),
             " Alcohol gives 7 kcal per gram and is not in the table above, because it is not protein, carbohydrate or fat." if sp.get("a") else ""))
    o.append('      <div class="dp-bar" role="img" aria-label="Energy split: %s">%s</div>' % (", ".join("%d%% %s" % (v, w) for _, w, v in parts), "".join('<span class="%s" style="width:%d%%"></span>' % (k, v) for k, _, v in parts)))
    o.append('      <div class="dp-legend">%s</div>' % "".join('<span class="%s"><i></i>%s %d%%</span>' % (k, w.capitalize(), v) for k, w, v in parts))
    if fig["composed"]:
        o.append('      <h2 id="ingredients">What is in a serving</h2>')
        o.append('      <p>The serving is built from these ingredients, gram by gram:</p><ul>')
        for s in fig["sources"]:
            o.append('        <li>%s g %s%s</li>' % (ne(s["grams"]), G.esc(EN["ingredient"].get(s["es"], s["es"])), (" (%s)" % METHOD.get(s["method"], s["method"])) if s.get("method") else ""))
        o.append('      </ul>')
    # comparison
    o.append('      <h2 id="compare">How it compares with similar dishes</h2>')
    o.append('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">Dish</th><th scope="col">Serving</th><th scope="col">kcal / serving</th><th scope="col">kcal / 100 g</th><th scope="col">Protein</th></tr></thead><tbody>')
    cmp_rows = [(d["app_id"], True)] + [(c, False) for c in d.get("compare", [])]
    for cid, is_this in cmp_rows:
        f2 = G.figures(cid)
        slug2 = ready_by_app.get(cid)
        label = name if is_this else app_name_en(cid)
        cell = ('<a href="../%s/">%s</a>' % (slug2, G.esc(label))) if (slug2 and not is_this) else G.esc(label)
        o.append('        <tr%s><td>%s</td><td>%s g</td><td class="hl">%s</td><td>%s</td><td>%s g</td></tr>'
                 % (' class="is-this"' if is_this else "", cell, ne(f2["serving_g"]), ne(f2["kcal"]), ne(f2["per100"]), ne(f2["protein"])))
    o.append('      </tbody></table></div>')
    o.append('      <p class="dp-table-note">All figures come from the same database, so they can be compared with each other.</p>')
    o.append('      <h2 id="faq">Frequently asked questions</h2>\n      <div class="faq-list">')
    for i, (q, a) in enumerate(faq):
        o.append('        <details class="faq-item"%s><summary><span>%s</span><i class="faq-plus" aria-hidden="true"></i></summary><p>%s</p></details>' % (" open" if i == 0 else "", G.esc(q), G.esc(a)))
    o.append('      </div>')
    o.append('      </div>')
    o.append(dish_aside_en(d))
    # sources
    o.append('      <section class="dp-src reveal" id="sources">\n        <h2>Where these figures come from</h2>')
    o.append('        <p>Public databases: <a href="https://fdc.nal.usda.gov/" target="_blank" rel="noopener">USDA FoodData Central</a> and <a href="https://ciqual.anses.fr/" target="_blank" rel="noopener">CIQUAL (ANSES)</a>. How they are added up and how the serving is set: <a href="../../metodologia/">our methodology</a>.</p>')
    if fig["composed"]:
        o.append('        <p>They are the figures the Fotocal app uses for this dish: a standard serving built from rows of public databases, added up gram by gram.</p><ul>')
        for s in fig["sources"]:
            o.append('          <li>%s g %s — %s, %s</li>' % (ne(s["grams"]), G.esc(EN["ingredient"].get(s["es"], s["es"])), G.esc(s["db"]), G.esc(s["ref"])))
        o.append('        </ul><p>Per 100 g is derived from the serving. App snapshot: commit %s (%s).</p>' % (G.APP["_source"]["commit"], G.APP["_source"]["commit_date"]))
    else:
        o.append('        <p>This is the reference figure the Fotocal app uses for a serving of %s (%s g); it has no ingredient breakdown yet, so fibre, sugars and salt are not shown. App snapshot: commit %s (%s).</p>'
                 % (G.esc(gl), ne(g), G.APP["_source"]["commit"], G.APP["_source"]["commit_date"]))
    o.append('        <p>General information about food, not medical or dietary advice.</p>\n      </section>')
    # related
    o.append('      <nav class="dp-related reveal" aria-label="Related pages">\n        <h2>Keep going</h2>\n        <div class="post-nav">')
    for dd in G.related(d):
        s2 = dd["slug"]
        o.append('          <a class="post-nav-item" href="../%s/"><small>Another dish</small><strong>Calories in %s</strong></a>' % (s2, G.esc(display(dd))))
    o.append('          <a class="post-nav-item" href="../"><small>Table</small><strong>Calories in Spanish dishes, per serving and per 100 g</strong></a>')
    o.append('          <a class="post-nav-item" href="../../calculadoras/calorias-diarias/"><small>Calculator</small><strong>Daily calorie calculator</strong></a>')
    o.append('        </div>\n      </nav>')
    o.append('    </div>\n  </article>\n</main>')
    return title, desc, "\n".join(ld), "\n".join(o)


def hub(ready):
    title = "Calories in Spanish Food: per Serving and per 100 g"
    desc = "Calories in Spanish food: %d dishes with the serving as it is really served, per 100 g, protein, carbs and fat, and the source of every figure." % len(ready)
    assert len(title) <= G.TITLE_MAX and len(desc) <= 155, (len(title), len(desc))
    url = SITE + "calorias/"
    items = [{"@type": "ListItem", "position": i + 1, "name": "Calories in " + display(d), "url": SITE + "calorias/%s/" % d["slug"]} for i, d in enumerate(ready)]
    ld = "\n".join([
        G.ld_block({"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "inLanguage": "en", "url": url, "publisher": G.ORG,
                    "mainEntity": {"@type": "ItemList", "itemListElement": items}}),
        G.ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE}, {"@type": "ListItem", "position": 2, "name": "Calories in Spanish food", "item": url}]}),
    ])
    o = ['\n<main id="main">\n  <article class="post dp dp-hub">\n    <header class="post-head">\n      <div class="container-narrow">',
         '        <nav class="post-crumbs reveal" aria-label="Breadcrumb"><a href="../">Home</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">Calories in Spanish dishes</a></nav>',
         '        <h1 class="post-title reveal">Calories in Spanish food, per serving and per 100 g</h1>',
         '        <p class="post-lead reveal">How many calories are in Spanish food? A table of what people really eat in Spain: the serving as it is served, its calories, and per 100 g so you can compare. Each dish has its own page with the protein, carbs and fat, what a serving weighs and how it compares.</p>',
         '      </div>\n    </header>\n    <div class="container-narrow">', '      <div class="post-body reveal">']
    o.append(G.hub_answer(ready, "en"))
    o.append(group_tables(ready, "en"))
    o.append('      <p class="dp-table-note">Serving: the one the Fotocal app uses for each dish, in grams as served. Figures come from public databases (USDA FoodData Central and CIQUAL 2025) added up ingredient by ingredient; each page says exactly which rows.</p>')
    o.append('      <h2>How to read the table</h2>')
    o.append('      <p>The serving column is the one that matters day to day: it is what you log if you eat the dish. Per 100 g is for comparing dishes and for working out a different amount: weigh what you have, multiply by the figure and divide by 100.</p>')
    def top_en(key, k=10):
        rows = sorted(((G.figures(d["app_id"]), d) for d in ready), key=lambda t: (t[0][key], t[1]["slug"]), reverse=True)[:k]
        out = ["      <ol>"]
        for f, d in rows:
            nm = '<a href="%s/">%s</a>' % (d["slug"], G.esc(display(d)))
            if key == "kcal":
                out.append("        <li>%s: %s kcal per serving of %s g (%s kcal per 100 g)</li>" % (nm, ne(f["kcal"]), ne(f["serving_g"]), ne(f["per100"])))
            else:
                out.append("        <li>%s: %s kcal per 100 g (%s kcal per serving of %s g)</li>" % (nm, ne(f["per100"]), ne(f["kcal"]), ne(f["serving_g"])))
        return "\n".join(out + ["      </ol>"])
    o.append('      <h2 id="most-calories">The 10 Spanish dishes with the most calories per serving</h2>')
    o.append('      <p>Of the %d dishes with their own page, these add up to the most as served. All sit around or above 500 kcal: they fit in a main meal, but it helps to know that is what they are.</p>' % len(ready))
    o.append(top_en("kcal"))
    o.append('      <h2 id="most-calories-100g">The 10 with the most calories per 100 g</h2>')
    o.append('      <p>Per 100 g the order changes: foods with a lot of fat and little water move up, and they are eaten in small servings.</p>')
    o.append(top_en("per100"))
    o.append('      <p>The whole app database, %d foods and dishes, is in the <a href="tabla-de-calorias/">full calorie table</a>. To work out how much you should eat, try the <a href="../calculadoras/">eight calculators</a>, starting with <a href="../calculadoras/calorias-diarias/">daily calories</a>.</p>' % len(G.HAND))
    o.append('      </div>')
    o.append(G.download_card("en", "Want the calories of your own plate, not the average?",
                             "Snap a photo and Fotocal counts the calories for you, with the figures on these pages.", G.PLAY + "&utm_source=web&utm_medium=dish&utm_campaign=hub-en"))
    o.append('      <p class="post-disclaimer reveal">General information about food, not medical or dietary advice.</p>')
    o.append('    </div>\n  </article>\n</main>')
    return title, desc, ld, "\n".join(o)


def group_tables(ready, lang):
    """The dish hub table, one table per group (Spanish dishes first, drinks
    last: 05-11-2026 Coca-Cola Zero topped an alphabetical list)."""
    fmt = ne if lang == "en" else G.n
    head = ("Dish", "Serving", "kcal / serving", "kcal / 100 g", "Protein", "Carbs", "Fat") if lang == "en" else \
           ("Plato", "Ración", "kcal / ración", "kcal / 100 g", "Prot.", "Hidr.", "Grasas")
    out = []
    for gk in EN["group_order"]:
        ds = [d for d in ready if EN["group_of"].get(d["slug"]) == gk]
        if not ds:
            continue
        ds.sort(key=lambda d: (display(d) if lang == "en" else d["name"]).lower())
        out.append('      <h2 id="g-%s">%s <small>(%d)</small></h2>' % (gk, EN["groups"][gk][lang], len(ds)))
        out.append('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr>%s</tr></thead><tbody>' % "".join('<th scope="col">%s</th>' % h for h in head))
        for d in ds:
            f = G.figures(d["app_id"])
            label = display(d) if lang == "en" else G.cap(d["name"])
            out.append('        <tr><td><a href="%s/">%s</a></td><td>%s g</td><td class="hl">%s</td><td>%s</td><td>%s g</td><td>%s g</td><td>%s g</td></tr>'
                       % (d["slug"], G.esc(label), fmt(f["serving_g"]), fmt(f["kcal"]), fmt(f["per100"]), fmt(f["protein"]), fmt(f["carbs"]), fmt(f["fat"])))
        out.append('      </tbody></table></div>')
    return "\n".join(out)


SLOTS_EN = {"desayuno": "Breakfasts", "comida": "Lunches", "merienda": "Afternoon snacks and bites", "cena": "Dinners"}


def table(ready_by_app):
    title = "Food calorie chart: Spanish foods and dishes"
    desc = ("Printable calorie table of the %d Spanish foods and dishes in the Fotocal app: serving, kcal per serving and per 100 g, protein, carbs and fat." % len(G.HAND))
    title += " — Fotocal"
    assert len(title) <= G.TITLE_MAX and len(desc) <= 155, (len(title), len(desc))
    url = SITE + "calorias/tabla-de-calorias/"
    ld = "\n".join([
        G.ld_block({"@context": "https://schema.org", "@type": "WebPage", "name": title.replace(" — Fotocal", ""), "description": desc, "inLanguage": "en", "url": url,
                    "dateModified": G.APP["_source"]["commit_date"], "publisher": G.ORG, "isPartOf": {"@type": "WebSite", "@id": SITE + "#site"}}),
        G.ld_block({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE}, {"@type": "ListItem", "position": 2, "name": "Calories in Spanish dishes", "item": SITE + "calorias/"},
            {"@type": "ListItem", "position": 3, "name": "Calorie table", "item": url}]}),
    ])
    o = ['\n<main id="main">\n  <article class="post dp dp-hub">\n    <header class="post-head">\n      <div class="container-narrow">',
         '        <nav class="post-crumbs reveal" aria-label="Breadcrumb"><a href="../../">Home</a><span class="sep" aria-hidden="true">/</span><a href="../">Calories in Spanish dishes</a><span class="sep" aria-hidden="true">/</span><a href="./" aria-current="page">Calorie table</a></nav>',
         '        <h1 class="post-title reveal">Food calorie chart of Spanish foods and dishes</h1>',
         '        <p class="post-lead reveal">The %d foods and dishes in the Fotocal database in one table, to look up or print: the serving as served, its calories, per 100 g to compare, and protein, carbs and fat. Grouped by the time of day the app suggests them.</p>' % len(G.HAND),
         '        <p class="tbl-print reveal"><button type="button" class="btn btn-ghost" onclick="window.print()">Print the table</button></p>',
         '      </div>\n    </header>\n    <div class="container-narrow">', '      <div class="post-body reveal">',
         '      <p>Each row is an entry in the app, with the serving the app uses; the ones with their own page are linked. Spanish name first, English after.</p>']
    for slot, label in G.SLOT_NAMES:
        rows = sorted([(k, v) for k, v in G.HAND.items() if v.get("primarySlot") == slot], key=lambda kv: kv[1]["name_es"].lower())
        if not rows:
            continue
        o.append('      <h2 id="%s">%s <small>(%d)</small></h2>' % (slot, SLOTS_EN[slot], len(rows)))
        o.append('      <div class="dp-table-wrap"><table class="dp-table"><thead><tr><th scope="col">Food or dish</th><th scope="col">Serving</th><th scope="col">kcal / serving</th><th scope="col">kcal / 100 g</th><th scope="col">Prot.</th><th scope="col">Carbs</th><th scope="col">Fat</th></tr></thead><tbody>')
        for k, v in rows:
            f = G.figures(k)
            nm = "%s (%s)" % (v["name_es"], v["name_en"]) if v.get("name_en") and v["name_en"].lower() != v["name_es"].lower() else v["name_es"]
            slug = ready_by_app.get(k)
            cell = ('<a href="../%s/">%s</a>' % (slug, G.esc(nm))) if slug else G.esc(nm)
            o.append('        <tr><td>%s</td><td>%s, %s g</td><td class="hl">%s</td><td>%s</td><td>%s g</td><td>%s g</td><td>%s g</td></tr>'
                     % (cell, G.esc(serving_en(f["serving_label"])), ne(f["serving_g"]), ne(f["kcal"]), ne(f["per100"]), ne(f["protein"]), ne(f["carbs"]), ne(f["fat"])))
        o.append('      </tbody></table></div>')
    o.append('      <h2 id="sources">Where the figures come from</h2>')
    o.append('      <p>They are the Fotocal app\'s: each entry is a serving set by the app, built from rows of public databases (USDA FoodData Central and CIQUAL 2025) added up gram by gram, or its reference figure where there is no recipe. App snapshot: commit %s (%s). General information about food, not medical or dietary advice.</p>' % (G.APP["_source"]["commit"], G.APP["_source"]["commit_date"]))
    o.append('      </div>')
    o.append('    </div>\n  </article>\n</main>')
    return title, desc, ld, "\n".join(o)
