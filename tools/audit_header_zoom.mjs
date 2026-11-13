// Header at 200 % text on a phone: measures sideways scroll on a sample of
// pages and (with an output folder) saves a picture of the top of each.
//   node tools/audit_header_zoom.mjs [outDir]      needs the local server on :8765
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const BASE = process.env.SITE_BASE || "http://127.0.0.1:8765";
const out = process.argv[2];
const PAGES = { home: "/", "home-en": "/en/", calc: "/calculadoras/imc/?altura=165&peso=70", "calc-hub": "/calculadoras/", dish: "/calorias/paella-valenciana/", "dish-hub": "/calorias/", blog: "/blog/", post: "/blog/app-contar-calorias-gratis/", compare: "/comparativa/", contact: "/contact/", features: "/features/", "blog-en": "/en/blog/" };
if (out) fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
let fails = 0;
for (const [name, u] of Object.entries(PAGES)) for (const [w, zoom, scrolled] of [[390, 2, 0], [390, 2, 1], [360, 2, 0], [390, 1, 0], [390, 1, 1]]) {
  const p = await browser.newPage({ viewport: { width: w, height: 800 } });
  const res = await p.goto(BASE + u, { waitUntil: "load" });
  if (!res || !res.ok()) { await p.close(); if (zoom === 2 && w === 390 && !scrolled) console.log("skip " + u + " (not found)"); continue; }
  if (zoom === 2) await p.addStyleTag({ content: "html{font-size:200% !important}" });
  if (scrolled) { await p.evaluate(() => window.scrollTo(0, 1400)); }
  await p.waitForTimeout(600);
  const [sw, cw] = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
  const tag = `${name}-${w}${zoom === 2 ? "-zoom200" : ""}${scrolled ? "-scrolled" : ""}`;
  if (sw > cw) { fails++; console.log(`FAIL ${tag}: scrolls sideways (${sw} > ${cw})`); }
  if (out) await p.screenshot({ path: `${out}/${tag}.png`, clip: { x: 0, y: 0, width: Math.max(sw, cw), height: 260 } });
  await p.close();
}
await browser.close();
console.log(fails ? `header: ${fails} view(s) scroll sideways` : "header: OK, no sideways scroll at 200 % text or normal text");
process.exit(fails ? 1 : 0);
