// Pictures of the GEO round additions, phone (Pixel 7) and laptop (1366 px):
// each «Datos de Fotocal» box and one app screen inside a calculator.
//   node tools/seo/geo_shots.mjs  → docs/seo/geo-google/shots/
import { chromium, devices } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const OUT = new URL('../../docs/seo/geo-google/shots/', import.meta.url).pathname;
const SHOTS = [['hub-oil-es', 'calorias/', '.datos-box'], ['hub-oil-en', 'en/calorias/', '.datos-box'],
  ['count-portion-es', 'blog/how-to-count-calories-accurately/', '.datos-box'], ['foods-400-es', 'blog/best-foods-for-weight-loss/', '.datos-box'],
  ['imc-screen-es', 'calculadoras/imc/', '.app-shot'], ['scanfood-faq-es', 'features/scan-food/', '.faq-more']];
const b = await chromium.launch();
for (const [dev, opts] of [['phone', { ...devices['Pixel 7'], locale: 'es-ES' }], ['laptop', { viewport: { width: 1366, height: 900 }, locale: 'es-ES' }]]) {
  const p = await (await b.newContext(opts)).newPage();
  for (const [name, url, sel] of SHOTS) {
    await p.goto(`${base}/${url}`, { waitUntil: 'load' });
    await p.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important}' });
    await p.addStyleTag({ content: sel + '{outline:12px solid #fff;outline-offset:0}' }); const el = p.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(300);
    await el.screenshot({ path: `${OUT}${name}-${dev}.png` });
  }
}
await b.close(); console.log('pictures in ' + OUT);
