// BEFORE | AFTER strips of the header pictures saved by audit_header_zoom.mjs.
import { createRequire } from "module";
import fs from "fs";
import path from "path";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const dir = path.resolve("docs/header-audit"), out = path.join(dir, "compare");
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();
for (const kind of ["390-zoom200", "390-zoom200-scrolled", "390", "390-scrolled"]) {
  const names = fs.readdirSync(path.join(dir, "after")).filter(f => f.endsWith("-" + kind + ".png") && /^[a-z-]+-390/.test(f) && f.replace(/^[a-z-]+?-(390.*)\.png$/, "$1") === kind);
  const img = (d, f) => "data:image/png;base64," + fs.readFileSync(path.join(dir, d, f)).toString("base64");
  const rows = names.map(f => `<tr><td style="padding:6px 14px 6px 0;font:600 15px system-ui">${f.split("-390")[0]}</td><td><img src="${img("before", f)}" style="border:1px solid #c00;display:block;margin:6px"></td><td><img src="${img("after", f)}" style="border:1px solid #0a7a3d;display:block;margin:6px"></td></tr>`).join("");
  await page.setContent(`<body style="margin:0;background:#fff"><table id="x" style="border-collapse:collapse;padding:16px"><tr><th></th><th style="font:700 17px system-ui;color:#b00020">BEFORE · ${kind}</th><th style="font:700 17px system-ui;color:#0a7a3d">AFTER · ${kind}</th></tr>${rows}</table></body>`);
  await page.waitForFunction(() => [...document.images].every(i => i.complete));
  await (await page.$("#x")).screenshot({ path: path.join(out, `header-${kind}-before-after.png`) });
}
await browser.close();
console.log("done");
