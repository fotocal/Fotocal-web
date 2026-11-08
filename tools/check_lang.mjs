// The language switcher must work on every kind of page, desktop and phone,
// and take the visitor to the SAME page in the other language (found dead
// site-wide on 07-11-2026: the handlers were bound to an element that the
// pre-rendered nav no longer had).
//
//   python3 -m http.server 8765 --bind 127.0.0.1   (from the repo root)
//   node tools/check_lang.mjs
import { chromium, devices } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36';
const PAGES = ['/', '/features/scan-food/', '/blog/', '/blog/how-much-protein-per-day/', '/calculadoras/', '/calculadoras/imc/',
               '/calorias/', '/calorias/paella-valenciana/', '/calorias/tabla-de-calorias/', '/privacy-policy/', '/subscription/', '/faq/'];
const twin = (p) => p.startsWith('/en/') ? p.slice(3) : '/en' + p;
const b = await chromium.launch();
let fails = 0, n = 0;
const bad = (m) => { fails++; console.log('FAIL ' + m); };

// desktop: open, Escape, outside click, then follow the other language
const d = await b.newContext({ viewport: { width: 1280, height: 860 }, userAgent: UA });
await d.addInitScript(() => { try { localStorage.setItem('fotocal-lang', document.documentElement.lang || 'es'); } catch (e) {} });
const p = await d.newPage();
for (const path of [...PAGES, ...PAGES.map(twin)]) {
  n++;
  await p.goto(base + path);
  const cur = p.locator('#langCurrent');
  await cur.click();
  if (!(await p.locator('#langSelect.open').count()) || (await cur.getAttribute('aria-expanded')) !== 'true') { bad(`${path}: menu does not open`); continue; }
  await p.keyboard.press('Escape');
  if (await p.locator('#langSelect.open').count()) bad(`${path}: Escape does not close`);
  await cur.click(); await p.mouse.click(5, 600);
  if (await p.locator('#langSelect.open').count()) bad(`${path}: outside click does not close`);
  await cur.click();
  const other = path.startsWith('/en/') ? 'es' : 'en';
  await Promise.all([p.waitForNavigation(), p.click(`#langMenu .lang-item[data-lang="${other}"]`)]);
  const got = new URL(p.url()).pathname, want = twin(path) === '/en/' && path === '/' ? '/en/' : twin(path);
  if (got !== want) bad(`${path}: switcher went to ${got}, expected ${want}`);
  const stored = await p.evaluate(() => localStorage.getItem('fotocal-lang'));
  if (stored !== other) bad(`${path}: stored ${stored}, expected ${other}`);
}
await d.close();

// phone: ES / EN in the ☰ menu
const m = await b.newContext({ ...devices['Pixel 7'], userAgent: UA });
await m.addInitScript(() => { try { localStorage.setItem('fotocal-lang', document.documentElement.lang || 'es'); } catch (e) {} });
const q = await m.newPage();
for (const path of PAGES) {
  n++;
  await q.goto(base + path);
  await q.click('#navBurger');
  await q.waitForTimeout(350);
  const link = q.locator('.nav-mobile .m-lang-item[data-lang="en"]');
  if (!(await link.isVisible())) { bad(`${path}: no visible EN in the phone menu`); continue; }
  await Promise.all([q.waitForNavigation(), link.click()]);
  const got = new URL(q.url()).pathname;
  if (got !== twin(path)) bad(`${path}: phone menu went to ${got}, expected ${twin(path)}`);
}
await m.close();
await b.close();
console.log(fails ? `language switcher: ${fails} problem(s) of ${n}` : `language switcher: OK, ${n} checks (desktop both trees, phone menu)`);
process.exit(fails ? 1 : 0);
