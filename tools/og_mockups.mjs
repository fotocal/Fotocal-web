// Pictures for the owner (v3): each new card as a large single image, as it
// appears in WhatsApp and Instagram DM at phone size, and one comparison of
// the old live home card, the rejected direction B and the new card.
// The chat frames are drawings of each app's light-mode link preview, not
// screenshots of the apps.   node tools/og_mockups.mjs   (server on :8765)
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { readFileSync, mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
const ROOT = new URL('..', import.meta.url).pathname.replace(/\/$/, '');
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const out = join(ROOT, 'docs/og-previews/v3'); mkdirSync(out, { recursive: true });
const PAGES = { home: '', dish: 'calorias/patatas-bravas/', calculator: 'calculadoras/calorias-diarias/', blog: 'blog/hydration-and-weight/', hub: 'calorias/tabla-de-calorias/' };
const unesc = s => s.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const og = (h, p) => unesc((h.match(new RegExp(`<meta property="${p}" content="([^"]*)"`)) || [, ''])[1]);
function read(lang, path) {
  const h = readFileSync(join(ROOT, lang === 'en' ? 'en' : '', path, 'index.html'), 'utf8');
  const file = og(h, 'og:image').replace('https://getfotocal.com/', '').split('?')[0];
  return { title: og(h, 'og:title'), desc: og(h, 'og:description'), file, img: `${base}/${file}?${Date.now()}`, url: 'getfotocal.com/' + (lang === 'en' ? 'en/' : '') + path };
}
const clamp = n => `display:-webkit-box;-webkit-line-clamp:${n};-webkit-box-orient:vertical;overflow:hidden`;
const wa = p => `<div><p>WhatsApp</p><div class="ph" style="background:#EFEAE2"><div style="margin-left:auto;width:300px;background:#D9FDD3;border-radius:10px;padding:4px"><div style="background:#CFF2C8;border-radius:7px;overflow:hidden"><img src="${p.img}" style="width:100%;display:block"><div style="padding:7px 9px 8px"><div style="font-weight:600;font-size:14px;${clamp(2)}">${esc(p.title)}</div><div style="font-size:12.5px;color:#54656F;${clamp(2)}">${esc(p.desc)}</div><div style="font-size:12px;color:#54656F">getfotocal.com</div></div></div><div style="padding:6px;font-size:14px;color:#027EB5">https://${esc(p.url)}</div></div></div></div>`;
const ig = p => `<div><p>Instagram DM</p><div class="ph" style="background:#fff"><div style="margin-left:auto;width:270px;border-radius:18px;overflow:hidden;background:#EFEFEF"><img src="${p.img}" style="width:100%;display:block"><div style="padding:9px 12px 11px"><div style="font-weight:600;font-size:14px;${clamp(2)}">${esc(p.title)}</div><div style="font-size:12px;color:#737373">getfotocal.com</div></div></div></div></div>`;
const CSS = `body{margin:0;background:#E4E1DC;font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#111B21}section{padding:20px 26px 8px}h2{font:800 24px system-ui;margin:0 0 10px}
  .r{display:flex;gap:26px;align-items:flex-start}p{font:600 14px system-ui;color:#555;margin:0 0 6px}img{display:block}.ph{width:350px;height:340px;border-radius:26px;border:7px solid #222;padding:14px 12px;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden}`;
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
const settle = () => page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
for (const lang of ['es', 'en']) {
  let html = '';
  for (const [k, path] of Object.entries(PAGES)) {
    const p = read(lang, path);
    copyFileSync(join(ROOT, p.file), join(out, `card-${k}-${lang}.jpg`));
    html += `<section><h2>${k} · ${lang.toUpperCase()} · ${esc(p.url)}</h2><div class="r"><div><p>Card (1200×630)</p><img src="${p.img}" style="width:760px;border-radius:6px"></div><div><p>Thumbnail, 300 px</p><img src="${p.img}" style="width:300px"></div>${wa(p)}${ig(p)}</div></section>`;
  }
  await page.setViewportSize({ width: 1930, height: 1000 });
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>${CSS}</style>${html}`, { waitUntil: 'load' }); await settle();
  await page.screenshot({ path: join(out, `apps-all-${lang}.png`), fullPage: true });
  if (existsSync(join(ROOT, `assets/og/home-${lang}-square.jpg`))) copyFileSync(join(ROOT, `assets/og/home-${lang}-square.jpg`), join(out, `card-home-${lang}-square.jpg`));
}
// home: the old live card, the rejected B, the new card
const cmp = [['Old card (live today)', `${base}/docs/og-previews/before/home-es.jpg`, '#b00020'], ['Rejected direction B', `${base}/docs/og-previews/v2/home-B.jpg`, '#b06000'], ['New v3', read('es', '').img, '#0a7a3d']];
await page.setViewportSize({ width: 1960, height: 700 });
await page.setContent(`<!doctype html><meta charset="utf-8"><style>${CSS}.c{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;padding:24px}.c img{width:100%;border:1px solid #ccc}.c p{font:800 18px system-ui}</style><div class="c">${cmp.map(([t, u, c]) => `<div><p style="color:${c}">${t}</p><img src="${u}"><p style="margin-top:14px;color:#555;font:600 14px system-ui">At thumbnail size (300 px)</p><img src="${u}" style="width:300px"></div>`).join('')}</div>`, { waitUntil: 'load' }); await settle();
await page.screenshot({ path: join(out, 'home-old-vs-B-vs-v3.png'), fullPage: true });
await browser.close();
console.log('v3 pictures written to ' + out);
