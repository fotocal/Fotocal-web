// Google AI features eligibility audit (GEO round, 22-11-2026).
// For every URL in sitemap.xml (served locally on :8765): returns 200, robots
// meta allows indexing and snippets, no nosnippet / max-snippet:0 /
// data-nosnippet on the main content, and the main text is already in the
// HTML without JavaScript (JS-off text >= 90% of JS-on text).
//   node tools/seo/ai_eligibility.mjs   → docs/seo/geo-google/eligibility.csv
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
const ROOT = new URL('../..', import.meta.url).pathname;
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const urls = [...readFileSync(ROOT + 'sitemap.xml', 'utf8').matchAll(/<loc>https:\/\/getfotocal\.com\/([^<]*)<\/loc>/g)].map(m => m[1]);
const b = await chromium.launch();
const on = await (await b.newContext()).newPage();
const off = await (await b.newContext({ javaScriptEnabled: false })).newPage();
const txt = p => p.evaluate(() => { const m = document.querySelector('main') || document.body; return m.innerText.replace(/\s+/g, ' ').trim().length; });
const rows = [['url', 'status', 'robots', 'nosnippet', 'data_nosnippet_in_main', 'text_js_on', 'text_js_off', 'ratio', 'ok']];
let bad = 0;
for (const u of urls) {
  const r = await off.goto(`${base}/${u}`, { waitUntil: 'load' });
  const status = r.status();
  const robots = await off.evaluate(() => [...document.querySelectorAll('meta[name=robots],meta[name=googlebot]')].map(m => m.content).join('|'));
  const nosnip = /nosnippet|max-snippet:\s*0|noindex/i.test(robots);
  const dns = await off.evaluate(() => !!(document.querySelector('main') || document.body).querySelector('[data-nosnippet]'));
  const tOff = await txt(off);
  await on.goto(`${base}/${u}`, { waitUntil: 'load' });
  const tOn = await txt(on);
  const ratio = tOn ? +(tOff / tOn).toFixed(2) : 0;
  const ok = status === 200 && !nosnip && !dns && ratio >= 0.9;
  if (!ok) bad++;
  rows.push([u || '/', status, robots, nosnip, dns, tOn, tOff, ratio, ok]);
}
await b.close();
mkdirSync(ROOT + 'docs/seo/geo-google', { recursive: true });
writeFileSync(ROOT + 'docs/seo/geo-google/eligibility.csv', rows.map(r => r.join(',')).join('\n') + '\n');
console.log(`${urls.length} URLs, ${bad} not eligible`);
for (const r of rows.slice(1)) if (!r[8]) console.log('  FAIL', r.join(' '));
process.exit(bad ? 1 : 0);
