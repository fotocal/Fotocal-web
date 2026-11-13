// Calculator result pages must never scroll sideways, and their numbers must
// never break across lines. Opens every calculator (ES + EN) with its result
// showing, at a phone (360 px) and a laptop (1280 px), with ordinary and with
// the largest inputs. Run through tools/check_calc_layout.py, which starts
// the local server for it; or directly with SITE_BASE set.
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const BASE = process.env.SITE_BASE || "http://127.0.0.1:8765";
const CALCS = ["calorias-diarias", "deficit-calorico", "imc", "proteinas", "macros", "agua", "tmb", "peso-saludable"];
const Q = {
  es: ["sexo=mujer&edad=35&altura=165&peso=70&actividad=light&objetivo=perder&ritmo=0.5&meta=62&grasa=25&reparto=balanced&kcal=2150",
       "sexo=hombre&edad=18&altura=230&peso=250&actividad=hard&objetivo=musculo&ritmo=0.75&meta=240&grasa=3&reparto=high_protein&kcal=6000"],
  en: ["sex=woman&age=35&height=165&weight=70&activity=light&goal=lose&pace=0.5&target=62&bodyfat=25&split=balanced&kcal=2150",
       "sex=man&age=18&height=230&weight=250&activity=hard&goal=build_muscle&pace=0.75&target=240&bodyfat=3&split=high_protein&kcal=6000"] };
const browser = await chromium.launch();
let fails = 0, n = 0;
for (const w of [360, 1280]) for (const lang of ["es", "en"]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, locale: lang === "es" ? "es-ES" : "en-GB" });
  await ctx.addInitScript(l => { try { localStorage.setItem("fotocal-lang", l); } catch (e) {} }, lang);
  const p = await ctx.newPage();
  const pre = lang === "en" ? "/en" : "";
  const urls = [];
  for (const c of CALCS) for (const q of Q[lang]) urls.push(pre + "/calculadoras/" + c + "/?" + q);
  urls.push(pre + "/calculadoras/");
  for (const u of urls) {
    await p.goto(BASE + u, { waitUntil: "load" }); if (u.includes("?")) await p.waitForSelector('.calc-out[data-state="ready"]', { timeout: 5000 }).catch(() => {});
    await p.waitForTimeout(150);
    const r = await p.evaluate(() => {
      const d = document.documentElement, P = [];
      if (d.scrollWidth > d.clientWidth) P.push("scrolls sideways (" + d.scrollWidth + " > " + d.clientWidth + ")");
      const o = document.querySelector(".calc-lang .calc-out") || document.querySelector(".calc-out");
      if (document.querySelector(".calc-tool") && (!o || o.dataset.state !== "ready")) P.push("the result did not open");
      document.querySelectorAll(".calc-out .calc-main b, .calc-out .calc-row b, .calc-out .calc-macro b").forEach(e => {
        if (!e.getClientRects().length) return;
        if (new Set([...e.getClientRects()].map(x => Math.round(x.top))).size > 1) P.push("number broken across lines: " + e.textContent.trim());
        const b = e.getBoundingClientRect(); if (b.right > d.clientWidth + 1) P.push("number runs off the screen: " + e.textContent.trim());
      });
      return P;
    });
    n++; for (const m of r) { fails++; console.log("FAIL " + w + "px " + u.split("?")[0] + (u.includes("230") ? " (largest inputs)" : "") + ": " + m); }
  }
  await ctx.close();
}
await browser.close();
console.log(fails ? `calculator layout: ${fails} problem(s) in ${n} views` : `calculator layout: OK, ${n} result views at 360 and 1280 px, no sideways scroll`);
process.exit(fails ? 1 : 0);
