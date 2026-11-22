// Page experience (GEO round 22-11-2026): on a phone, fixed bars (download
// bar, calculator result bar, top app bar) never cover more than 20% of the
// screen, and the end of the main content can still be scrolled clear of
// them. Also: exactly one H1.   node tools/seo/check_overlays.mjs
import { chromium, devices } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const PAGES = ['', 'calorias/', 'features/scan-food/', 'features/scan-barcode/', 'calculadoras/peso-saludable/', 'calculadoras/imc/',
  'calculadoras/deficit-calorico/', 'calculadoras/tmb/', 'calculadoras/calorias-diarias/', 'blog/how-to-count-calories-accurately/',
  'blog/best-foods-for-weight-loss/', 'calorias/paella-valenciana/', 'en/calorias/', 'en/calculadoras/imc/', 'en/blog/best-foods-for-weight-loss/'];
const b = await chromium.launch();
const ctxs = { es: await b.newContext({ ...devices['Pixel 7'], locale: 'es-ES' }), en: await b.newContext({ ...devices['Pixel 7'], locale: 'en-GB' }) };
const pes = await ctxs.es.newPage(), pen = await ctxs.en.newPage();
let bad = 0;
for (const u of PAGES) {
  const p = u.startsWith('en/') ? pen : pes;
  await p.goto(`${base}/${u}`, { waitUntil: 'load' });
  const r = await p.evaluate(async () => {
    const H = innerHeight, out = { h1: document.querySelectorAll('h1').length, maxCover: 0, hidden: false };
    for (let y = 0; y <= document.documentElement.scrollHeight; y += Math.round(H * 0.7)) {
      scrollTo(0, y); await new Promise(r => setTimeout(r, 120));
      let cover = 0;
      for (const el of document.querySelectorAll('body *')) {
        const cs = getComputedStyle(el);
        if (cs.position !== 'fixed' || cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
        const rc = el.getBoundingClientRect();
        const vis = Math.max(0, Math.min(rc.bottom, H) - Math.max(rc.top, 0));
        if (vis > 2 && rc.width > innerWidth * 0.6 && rc.height < H * 0.9) cover += vis;   // ignores the open menu sheet
      }
      out.maxCover = Math.max(out.maxCover, cover / H);
    }
    // end of main content: scroll so the last line of main sits at the bottom of the screen; no fixed bar may cover it
    const ps = [...document.querySelectorAll('main p, main li, main td')].filter(e => e.offsetParent && e.getClientRects().length && !e.closest('details:not([open])'));
    const last = ps[ps.length - 1];
    if (last) {
      last.scrollIntoView({ block: 'end' }); scrollBy(0, 0); await new Promise(r => setTimeout(r, 250));
      const lr = last.getBoundingClientRect();
      for (const el of document.querySelectorAll('body *')) {
        const cs = getComputedStyle(el);
        if (cs.position !== 'fixed' || cs.display === 'none' || cs.visibility === 'hidden') continue;
        const rc = el.getBoundingClientRect();
        if (rc.right <= 0 || rc.left >= innerWidth || rc.bottom <= 0 || rc.top >= H) continue;      // parked off screen
        if (rc.top < lr.bottom - 2 && rc.bottom > lr.top + 2 && rc.width > innerWidth * 0.6) {
          // covered now; is there room to scroll it clear?
          const room = document.documentElement.scrollHeight - (scrollY + H);
          if (room < (lr.bottom - rc.top)) out.hidden = (el.className || el.tagName) + '';
        }
      }
    }
    return out;
  });
  const ok = r.h1 === 1 && r.maxCover <= 0.2 && !r.hidden;
  if (!ok) bad++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${u || '/'}  h1=${r.h1}  max covered=${Math.round(r.maxCover * 100)}%  last text hidden=${r.hidden}`);
}
await b.close();
console.log(bad ? `${bad} page(s) fail` : 'OK, no overlay hides content');
process.exit(bad ? 1 : 0);
