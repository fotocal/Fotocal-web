#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The next dish pages to write, in keyword priority order (weekly routine).

    python3 tools/seo/dish_queue.py            # the next 10 candidates
    python3 tools/seo/dish_queue.py --mark     # set target_status=existing in
                                               # keywords.csv for every dish
                                               # page that now exists

A candidate is a row of docs/seo/keywords.csv with family=dish and
target_status=new whose slug is in the app. Foods whose recipe composes
(figures() has composed=True: a full ingredient breakdown from USDA/CIQUAL
rows) come first; foods with only the app's reference figure ("hand", the
same kind as /calorias/croquetas-de-jamon/) come after them at the same
priority, and their page says so. Foods not in the app are skipped. When the keyword rows run out, the remaining composed app recipes
follow in app order, so the queue never runs dry before ~150 pages.

Order: priority (1 first), composed before hand, then difficulty (low,
medium, high), then the order of the CSV.
"""
import csv, io, json, os, sys, contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    import gen_dishes as G  # noqa: E402

CSV = os.path.join(ROOT, "docs", "seo", "keywords.csv")
DIFF = {"low": 0, "medium": 1, "high": 2}


def slug_of(url):
    return url.rstrip("/").split("/")[-1]


HAND = {h["id"] for h in G.APP["hand"]}


def composed(slug):
    if slug not in G.APP["recipes"]:
        return False
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return G.figures(slug)["composed"]


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    have = {d["slug"] for d in G.DISHES}
    if "--mark" in sys.argv:
        n = 0
        for r in rows:
            if r["family"] == "dish" and r["target_status"] == "new" and slug_of(r["target_url"]) in have:
                r["target_status"] = "existing"
                n += 1
        with open(CSV, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print("marked %d keyword rows as existing" % n)
        return
    seen, out = set(), []
    cands = []
    for i, r in enumerate(rows):
        s = slug_of(r["target_url"])
        if r["family"] != "dish" or s in have:
            continue
        kind = 0 if composed(s) else (1 if s in HAND else None)
        if kind is not None:
            cands.append(((r["priority"], kind, DIFF.get(r["difficulty"], 3), i), s, r))
    for _, s, r in sorted(cands, key=lambda t: t[0]):
        if s in seen:
            continue
        seen.add(s)
        out.append((s, "p%s %s%s" % (r["priority"], r["difficulty"], "" if composed(s) else " hand"), r["keyword"]))
    for s in G.APP["recipes"]:
        if s not in have and s not in seen and composed(s):
            seen.add(s)
            out.append((s, "app only", "calorías " + s.replace("-", " ")))
    print("%d dish pages live; %d candidates with app figures" % (len(have), len(out)))
    for s, why, kw in out[:int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10]:
        print("  %-34s %-12s %s" % (s, why, kw))


if __name__ == "__main__":
    main()
