#!/usr/bin/env python3
"""Snapshot the app's Spanish dish figures into tools/dishes/app-data.json.

    python3 tools/dishes/sync_from_app.py /path/to/fotocal-app-clone

WHY. The dish pages under /calorias/ publish ONE figure per dish: the one
the app itself shows. The app's rule (src/lib/dishComposition.ts) is: a
dish has a hand-entered serving (src/data/spanishFoods.ts,
SPANISH_FOODS_HAND) and, where one exists, a standard recipe of rows from
the food table (src/data/spanishFoodRecipes.json → src/data/foodTable.json,
USDA FoodData Central / CIQUAL 2025). The recipe's composition replaces the
hand figures ONLY when its energy agrees with the hand energy within 25 %;
otherwise the hand figures stand. This script copies exactly what those
rules need — the hand list, the recipes, the food rows they use, the
retention table — plus the app commit, so tools/gen_dishes.py can apply
the same arithmetic and every published number is traceable to the app
at a known commit. Nothing is estimated here and nothing is typed in."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "app-data.json")


def parse_hand(ts):
    start = ts.index("export const SPANISH_FOODS_HAND")
    end = ts.index("];", start)
    body = ts[start:end]
    out = []
    for block in re.findall(r"\{(.*?)\n  \}", body, re.S):
        def f(key, conv=str):
            m = re.search(r"\b%s:\s*(\"[^\"]*\"|'[^']*'|[-\d.]+)" % key, block)
            if not m:
                return None
            v = m.group(1).strip("\"'")
            return conv(v)
        sec = re.search(r"secondarySlots:\s*\[([^\]]*)\]", block)
        out.append({
            "id": f("id"), "name_es": f("name_es"), "name_en": f("name_en"),
            "primarySlot": f("primarySlot"),
            "secondarySlots": re.findall(r"'([a-z]+)'", sec.group(1)) if sec else [],
            "servingLabel": f("servingLabel"), "servingGrams": f("servingGrams", float),
            "region": f("region"), "kcal": f("kcal", float),
            "carbs_g": f("carbs_g", float), "protein_g": f("protein_g", float), "fat_g": f("fat_g", float),
        })
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    app = sys.argv[1]
    ts = open(os.path.join(app, "src/data/spanishFoods.ts"), encoding="utf-8").read()
    hand = parse_hand(ts)
    recipes = json.load(open(os.path.join(app, "src/data/spanishFoodRecipes.json"), encoding="utf-8"))["recipes"]
    table = json.load(open(os.path.join(app, "src/data/foodTable.json"), encoding="utf-8"))
    foods = {f["id"]: f for f in table["foods"]}
    used = sorted({l["foodId"] for r in recipes.values() for l in r})
    missing = [u for u in used if u not in foods]
    if missing:
        sys.exit("recipes name food rows the table does not have: %s" % missing)
    commit = subprocess.check_output(["git", "-C", app, "rev-parse", "--short", "HEAD"], text=True).strip()
    date = subprocess.check_output(["git", "-C", app, "log", "-1", "--format=%cs"], text=True).strip()
    snap = {
        "_source": {
            "repo": "fotocal/Fotocal", "commit": commit, "commit_date": date,
            "files": ["src/data/spanishFoods.ts", "src/data/spanishFoodRecipes.json",
                      "src/data/foodTable.json", "src/lib/dishComposition.ts", "src/lib/foodCompose.ts"],
            "rule": "composition replaces hand figures only when |kcal_composed - kcal_hand| / kcal_hand <= 0.25",
            "tolerance": 0.25,
        },
        "hand": hand,
        "recipes": recipes,
        "foods": {u: foods[u] for u in used},
        "retention": table.get("retention", {}),
        "cook_yield": {   # src/lib/foodCompose.ts COOK_YIELD, copied verbatim
            "veg": {"boiled": 0.95, "stewed": 0.9, "sauteed": 0.8, "grilled": 0.8, "baked": 0.75, "fried": 0.7},
            "fruit": {"boiled": 0.95, "stewed": 0.95, "baked": 0.85, "grilled": 0.85},
            "fish": {"boiled": 0.85, "stewed": 0.85, "sauteed": 0.8, "grilled": 0.75, "baked": 0.8, "fried": 0.75},
            "egg": {"boiled": 1, "stewed": 1, "sauteed": 0.9, "fried": 0.9, "baked": 0.9},
            "cereal": {"boiled": 2.5, "stewed": 2.5},
        },
    }
    json.dump(snap, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%d hand dishes, %d recipes, %d food rows -> %s (app %s, %s)"
          % (len(hand), len(recipes), len(used), os.path.relpath(OUT), commit, date))


if __name__ == "__main__":
    main()
