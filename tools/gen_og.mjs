// One share card per page and language, 1200×630 JPEG, in assets/og/.
// Reads the BUILT pages (H1, kicker, the kcal figure on dish pages), renders
// a card with the site's own fonts through the local server, and writes
// assets/og/<id>-<lang>.jpg. tools/build_site.py points og:image at the card
// when it exists, so run: build → this → build. Start the server first:
//   python3 -m http.server 8765   (from the repository root)
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';
const ROOT = new URL('..', import.meta.url).pathname.replace(/\/$/, '');
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const walk = (d, out = []) => { for (const f of readdirSync(d)) { const p = join(d, f); if (statSync(p).isDirectory()) { if (!['src', 'tools', 'assets', '.git', 'node_modules'].includes(f)) walk(p, out); } else if (f === 'index.html') out.push(p); } return out; };
const pages = walk(ROOT).map(p => relative(ROOT, p));
mkdirSync(join(ROOT, 'assets', 'og'), { recursive: true });
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const text = h => h.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#39;|&rsquo;/g, '’').replace(/\s+/g, ' ').trim();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
let n = 0, skipped = 0;
for (const rel of pages) {
  const html = readFileSync(join(ROOT, rel), 'utf8');
  if (/content="noindex/.test(html)) { skipped++; continue; }
  const lang = rel.startsWith('en/') ? 'en' : 'es';
  const bare = rel.replace(/^en\//, '');
  const id = (bare === 'index.html' ? 'home' : bare.replace(/\/index\.html$/, '').replace(/\//g, '-')) + '-' + lang;
  const h1 = text((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [, 'Fotocal'])[1]);
  let kicker = text((html.match(/class="(?:kicker|log-tag)[^"]*"[^>]*>([\s\S]*?)<\//) || [, ''])[1]);
  const kcal = html.match(/content="[^"]*?\((\d+ g)\) tiene (\d[\d.]*) kcal/);
  const sub = kcal ? `${kcal[2]} kcal · ${lang === 'es' ? 'ración de' : 'serving of'} ${kcal[1]}` : (lang === 'es' ? 'Contador de calorías con foto · Android' : 'Photo calorie counter · Android');
  if (!kicker) kicker = rel.startsWith('blog/') || rel.startsWith('en/blog/') ? 'Blog' : rel.startsWith('calorias/') ? 'Calorías de platos españoles' : rel.startsWith('calculadoras/') ? 'Calculadoras' : 'Fotocal';
  const size = h1.length > 110 ? 50 : h1.length > 70 ? 58 : 68;
  await page.setContent(`<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><link rel="stylesheet" href="${base}/assets/css/fonts.css"><style>
  html,body{margin:0;width:1200px;height:630px;background:#fff;font-family:'Instrument Sans',system-ui,sans-serif;color:#1B2340}
  .bar{position:absolute;left:0;top:0;bottom:0;width:22px;background:linear-gradient(180deg,#FF8A3D,#F2306B)}
  .wrap{position:absolute;left:86px;right:72px;top:64px;bottom:60px;display:flex;flex-direction:column}
  .brand{display:flex;align-items:center;gap:16px;font-weight:600;font-size:30px;letter-spacing:-.01em}
  .brand img{width:52px;height:52px;border-radius:14px}
  .kick{margin-top:46px;font-size:22px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#D91C5C}
  h1{margin:18px 0 0;font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:${size}px;line-height:1.08;letter-spacing:-.015em;max-height:${size*1.08*3}px;overflow:hidden}
  .foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:24px;color:#626983}
  .foot b{color:#1B2340;font-weight:600}
  </style></head><body><div class="bar"></div><div class="wrap">
  <div class="brand"><img src="${base}/assets/img/logo-96.png" alt=""><span>Fotocal</span></div>
  <div class="kick">${esc(kicker)}</div><h1>${esc(h1)}</h1>
  <div class="foot"><span><b>getfotocal.com</b></span><span>${esc(sub)}</span></div></div></body></html>`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const buf = await page.screenshot({ type: 'jpeg', quality: 80, clip: { x: 0, y: 0, width: 1200, height: 630 } });
  writeFileSync(join(ROOT, 'assets', 'og', id + '.jpg'), buf); n++;
}
await browser.close();
console.log(`og cards: ${n} written, ${skipped} noindex pages skipped`);
