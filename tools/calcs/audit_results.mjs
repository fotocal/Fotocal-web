// Calculator result audit (calc-results-responsive, Nov 2026).
//   node tools/calcs/audit_results.mjs <outDir> [--shots]
// Fills every calculator (ES + EN) through its URL parameters, opens the
// result and measures it at phone, tablet and laptop widths, with normal,
// largest and smallest inputs and with text at 200 %. Prints one line per
// problem; with --shots also saves a picture of each result to <outDir>.
// Needs the local server: python3 -m http.server 8765 --bind 127.0.0.1
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const out = process.argv[2] || "docs/calc-audit/before";
const shots = process.argv.includes("--shots");
const BASE = "http://127.0.0.1:8765";
export const CALCS = ["calorias-diarias", "deficit-calorico", "imc", "proteinas", "macros", "agua", "tmb", "peso-saludable"];
const SHORT = { "calorias-diarias": "tdee", "deficit-calorico": "deficit", imc: "bmi", proteinas: "protein", macros: "macros", agua: "water", tmb: "bmr", "peso-saludable": "ideal" };
const Q = {
  es: { normal: "sexo=mujer&edad=35&altura=165&peso=70&actividad=light&objetivo=perder&ritmo=0.5&meta=62&grasa=25&reparto=balanced&kcal=2150",
        max: "sexo=hombre&edad=18&altura=230&peso=250&actividad=hard&objetivo=musculo&ritmo=0.75&meta=240&grasa=3&reparto=high_protein&kcal=6000",
        min: "sexo=mujer&edad=90&altura=130&peso=35&actividad=sedentary&objetivo=perder&ritmo=0.25&meta=35&grasa=60&reparto=keto&kcal=1000" },
  en: { normal: "sex=woman&age=35&height=165&weight=70&activity=light&goal=lose&pace=0.5&target=62&bodyfat=25&split=balanced&kcal=2150",
        max: "sex=man&age=18&height=230&weight=250&activity=hard&goal=build_muscle&pace=0.75&target=240&bodyfat=3&split=high_protein&kcal=6000",
        min: "sex=woman&age=90&height=130&weight=35&activity=sedentary&goal=lose&pace=0.25&target=35&bodyfat=60&split=keto&kcal=1000" } };
const WIDTHS = [360, 390, 430, 768, 1280, 1440];

// runs in the page: every measurable problem inside the calculator
function measure() {
  const P = [], vw = document.documentElement.clientWidth;
  if (document.documentElement.scrollWidth > vw + 1) P.push("page scrolls sideways (" + document.documentElement.scrollWidth + " > " + vw + ")");
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none"; };
  const name = e => (e.className && typeof e.className === "string" ? "." + e.className.split(" ")[0] : e.tagName.toLowerCase());
  const txt = e => (e.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40);
  const lines = e => { const s = getComputedStyle(e); const lh = parseFloat(s.lineHeight) || parseFloat(s.fontSize) * 1.2; return Math.round(e.getBoundingClientRect().height / lh); };
  document.querySelectorAll(".calc-lang .calc-tool *, .calc-lang .calc-text table, .calc-quick *").forEach(e => {
    if (!vis(e)) return;
    const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    if (r.right > vw + 1 || r.left < -1) P.push("outside the screen: " + name(e) + " «" + txt(e) + "»");
    if (e.children.length === 0 && e.scrollWidth > e.clientWidth + 1 && s.overflow !== "visible" && s.display !== "inline") P.push("text cut off in its box: " + name(e) + " «" + txt(e) + "»");
    const fs = parseFloat(s.fontSize);
    if (e.children.length === 0 && txt(e) && fs < 12) P.push("tiny text " + fs + "px: " + name(e) + " «" + txt(e) + "»");
  });
  // numbers must stay on one line, with their unit
  document.querySelectorAll(".calc-out .calc-main b, .calc-out .calc-row b, .calc-out .calc-macro b").forEach(e => {
    if (vis(e) && e.getClientRects().length > 1 && lines(e) > 1) P.push("number wraps onto " + lines(e) + " lines: «" + txt(e) + "»");
    if (vis(e) && e.getClientRects().length > 1) { const rs = [...e.getClientRects()]; if (new Set(rs.map(r => Math.round(r.top))).size > 1) P.push("number broken across lines: «" + txt(e) + "»"); }
  });
  // a label squeezed into a sliver next to its number
  document.querySelectorAll(".calc-out .calc-row").forEach(e => {
    if (!vis(e)) return; const lab = e.querySelector("span"); if (!lab) return;
    const n = lines(lab); if (n >= 4) P.push("label squeezed into " + n + " lines: «" + txt(lab) + "»");
  });
  // cards on top of each other
  const cards = [...document.querySelectorAll(".calc-out .calc-main, .calc-out .calc-rows, .calc-out .calc-macros, .calc-out .calc-share, .calc-out .dl-card, .calc-out .calc-warn")].filter(vis);
  for (let i = 1; i < cards.length; i++) { const a = cards[i - 1].getBoundingClientRect(), b = cards[i].getBoundingClientRect(); if (b.top < a.bottom - 2 && b.left < a.right && a.left < b.right) P.push("blocks overlap: " + name(cards[i - 1]) + " and " + name(cards[i])); }
  // tap targets
  document.querySelectorAll(".calc-lang .calc-tool button, .calc-lang .calc-tool a.btn, .calc-lang .calc-tool select, .calc-lang .calc-tool input:not([type=radio]):not([type=hidden]), .calc-lang .calc-tool label.calc-pill, .calc-lang .calc-tool summary").forEach(e => {
    if (vis(e) && e.getBoundingClientRect().height < 43.5) P.push("tap target " + Math.round(e.getBoundingClientRect().height) + "px high: " + name(e) + " «" + txt(e) + "»");
  });
  document.querySelectorAll(".calc-lang .calc-text .dp-table-wrap").forEach(w => { const t = w.querySelector("table"); if (t && t.scrollWidth > w.clientWidth + 1 && getComputedStyle(w).overflowX === "visible") P.push("table wider than the screen, no scroll area"); });
  const o = document.querySelector(".calc-lang .calc-out"); const r = o ? o.getBoundingClientRect() : null;
  return { P: [...new Set(P)], outW: r ? Math.round(r.width) : 0, vw, state: o ? o.dataset.state : "none" };
}

const browser = await chromium.launch();
if (shots) fs.mkdirSync(out, { recursive: true });
const problems = {};
async function run(lang, slug, w, variant, zoom, scheme) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, colorScheme: scheme || "light", locale: lang === "es" ? "es-ES" : "en-GB" });
  const p = await ctx.newPage();
  await p.addInitScript(l => { try { localStorage.setItem("fotocal-lang", l); } catch (e) {} }, lang);
  await p.goto(BASE + (lang === "en" ? "/en" : "") + "/calculadoras/" + slug + "/?" + Q[lang][variant], { waitUntil: "load" });
  if (zoom) await p.addStyleTag({ content: "html{font-size:200% !important}" });
  // the floating download bar is site chrome that covers part of every picture
  await p.addStyleTag({ content: ".calc-sticky{display:none !important}" });
  await p.waitForTimeout(350);
  const m = await p.evaluate(measure);
  const tag = SHORT[slug] + "-" + lang + "-" + w + (variant !== "normal" ? "-" + variant : "") + (zoom ? "-zoom200" : "") + (scheme === "dark" ? "-dark" : "");
  if (m.state !== "ok" && m.state !== "done" && m.state === "empty") m.P.push("the result did not open (state " + m.state + ")");
  if (m.P.length) problems[tag] = m.P;
  if (shots) { const el = await p.$(".calc-lang .calc-tool"); if (el) await el.screenshot({ path: out + "/" + tag + ".png" }); }
  await ctx.close();
}
for (const lang of ["es", "en"]) for (const slug of CALCS) {
  for (const w of WIDTHS) await run(lang, slug, w, "normal");
  for (const w of [360, 1280]) { await run(lang, slug, w, "max"); await run(lang, slug, w, "min"); }
  await run(lang, slug, 390, "normal", true);
  await run(lang, slug, 390, "normal", false, "dark");
}
await browser.close();
const keys = Object.keys(problems).sort();
for (const k of keys) for (const x of problems[k]) console.log(k + ": " + x);
console.log(keys.length ? keys.length + " view(s) with problems" : "calculator results: OK");
if (shots) fs.writeFileSync(out + "/problems.txt", keys.map(k => problems[k].map(x => k + ": " + x).join("\n")).join("\n") + "\n");
