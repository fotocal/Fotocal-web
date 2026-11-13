// Builds one BEFORE | AFTER picture per calculator, language and width from
// the pictures saved by audit_results.mjs.
//   node tools/calcs/audit_compare.mjs            (reads docs/calc-audit/before and /after)
import { createRequire } from "module";
import fs from "fs";
import path from "path";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const dir = path.resolve("docs/calc-audit"), out = path.join(dir, "compare");
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
let n = 0;
for (const s of ["tdee", "deficit", "bmi", "protein", "macros", "water", "bmr", "ideal"]) for (const lang of ["es", "en"]) for (const w of [390, 1280]) {
  const f = `${s}-${lang}-${w}.png`;
  if (!fs.existsSync(path.join(dir, "before", f)) || !fs.existsSync(path.join(dir, "after", f))) continue;
  const img = d => "data:image/png;base64," + fs.readFileSync(path.join(dir, d, f)).toString("base64");
  const col = w === 390 ? "" : "flex-direction:column;";
  await page.setContent(`<body style="margin:0;background:#fff;font:600 18px system-ui,sans-serif"><div id="x" style="display:inline-flex;${col}gap:24px;padding:20px;align-items:flex-start">
    <div><p style="margin:0 0 8px;color:#b00020">BEFORE · ${s} · ${lang.toUpperCase()} · ${w}px</p><img src="${img("before")}" style="border:1px solid #ccc;display:block"></div>
    <div><p style="margin:0 0 8px;color:#0a7a3d">AFTER · ${s} · ${lang.toUpperCase()} · ${w}px</p><img src="${img("after")}" style="border:1px solid #ccc;display:block"></div></div></body>`);
  await page.waitForFunction(() => [...document.images].every(i => i.complete));
  await (await page.$("#x")).screenshot({ path: path.join(out, `${s}-${lang}-${w}-before-after.png`) });
  n++;
}
await browser.close();
console.log(n + " side-by-side pictures in docs/calc-audit/compare/");
