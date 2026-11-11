// The tables in tools/calcs/extra.py are worked out in Python; this compares
// those ports with assets/js/calc.js, the code the calculators really run.
//   node tools/calcs/check_extra.mjs
import { createRequire } from "module";
import { execFileSync } from "child_process";
const require = createRequire(import.meta.url);
const C = require("../../assets/js/calc.js");
const py = `
import sys, json; sys.path.insert(0, "tools")
from calcs import extra as E
out = {"plan": [], "water": []}
for g in ("lose", "maintain", "build_muscle"):
    for kg in (50, 70, 95):
        out["plan"].append(["f", 35, 165, kg, "light", g, E.plan("f", 35, 165, kg, "light", g)])
for sex, cm in (("f", 165), ("m", 178)):
    for kg in range(50, 110, 10):
        out["water"].append([sex, cm, kg, E.water_ml(sex, 35, cm, kg, "light")])
print(json.dumps(out))`;
const got = JSON.parse(execFileSync("python3", ["-c", py], { encoding: "utf8" }));
let bad = 0;
for (const [sex, age, height, weight, activity, goal, p] of got.plan) {
  const r = C.plan({ sex, age, height, weight, activity, goal, pace: 0.5, target: 0, split: "balanced" });
  for (const k of ["kcal", "protein", "fat", "carbs"]) if (r[k] !== p[k]) { bad++; console.log("plan", goal, weight, k, "py", p[k], "js", r[k]); }
}
for (const [sex, height, weight, ml] of got.water) {
  const i = { sex, age: 35, height, weight, activity: "light", goal: "maintain", pace: 0.5, target: 0, split: "balanced" };
  const w = C.water(i, C.plan(i).kcal).ml;
  if (w !== ml) { bad++; console.log("water", sex, weight, "py", ml, "js", w); }
}
console.log(bad ? bad + " mismatch(es)" : "calculator tables: OK, " + (got.plan.length * 4 + got.water.length) + " values match calc.js");
process.exit(bad ? 1 : 0);
