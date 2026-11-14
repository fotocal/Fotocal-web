// Pictures for the owner: how a shared link will look in five apps, drawn
// from the BUILT page's own og: tags and card. Approximations of each app's
// light-mode link preview, not screenshots of the apps.
//   node tools/og_mockups.mjs [outDir]      needs the local server on :8765
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { readFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
const ROOT = new URL('..', import.meta.url).pathname.replace(/\/$/, '');
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const out = join(ROOT, process.argv[2] || 'docs/og-previews');
mkdirSync(out, { recursive: true });
const PAGES = { home: '', dish: 'calorias/patatas-bravas/', calculator: 'calculadoras/calorias-diarias/', blog: 'blog/hydration-and-weight/' };
const unesc = s => s.replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const og = (h, p) => unesc((h.match(new RegExp(`<meta property="${p}" content="([^"]*)"`)) || [, ''])[1]);
function read(lang, path) {
  const h = readFileSync(join(ROOT, lang === 'en' ? 'en' : '', path, 'index.html'), 'utf8');
  const img = og(h, 'og:image').replace('https://getfotocal.com', base);
  return { title: og(h, 'og:title'), desc: og(h, 'og:description'), img, url: 'getfotocal.com/' + (lang === 'en' ? 'en/' : '') + path };
}
const L = { es: { msg: 'Mira esto 👇', time: '10:24' }, en: { msg: 'Have a look 👇', time: '10:24' } };
const phone = (app, bg, inner) => `<div class="ph"><div class="app">${app}</div><div class="scr" style="background:${bg}">${inner}</div></div>`;
const clamp = n => `display:-webkit-box;-webkit-line-clamp:${n};-webkit-box-orient:vertical;overflow:hidden`;
function apps(p, lang) {
  const m = L[lang];
  return [
    phone('WhatsApp', '#EFEAE2', `<div style="margin-left:auto;width:300px;background:#D9FDD3;border-radius:10px;padding:4px;box-shadow:0 1px .5px rgba(0,0,0,.13)">
      <div style="background:#CFF2C8;border-radius:7px;overflow:hidden"><img src="${p.img}" style="width:100%;display:block">
      <div style="padding:7px 9px 8px"><div style="font-weight:600;font-size:14px;${clamp(2)}">${esc(p.title)}</div><div style="font-size:12.5px;color:#54656F;margin-top:2px;${clamp(2)}">${esc(p.desc)}</div><div style="font-size:12px;color:#54656F;margin-top:3px">getfotocal.com</div></div></div>
      <div style="padding:6px 6px 2px;font-size:14px;color:#027EB5">https://${esc(p.url)}</div><div style="padding:0 6px 4px;font-size:14px">${m.msg}</div><div style="text-align:right;font-size:11px;color:#667781;padding:0 6px 2px">${m.time} ✓✓</div></div>`),
    phone('Instagram DM', '#FFFFFF', `<div style="margin-left:auto;width:270px"><div style="border-radius:18px;overflow:hidden;background:#EFEFEF"><img src="${p.img}" style="width:100%;display:block">
      <div style="padding:9px 12px 11px"><div style="font-weight:600;font-size:14px;${clamp(2)}">${esc(p.title)}</div><div style="font-size:12px;color:#737373;margin-top:3px">getfotocal.com</div></div></div>
      <div style="margin-top:6px;margin-left:auto;width:max-content;background:#3797F0;color:#fff;border-radius:18px;padding:8px 13px;font-size:14px">${m.msg}</div></div>`),
    phone('X', '#FFFFFF', `<div style="display:flex;gap:10px"><div style="width:38px;height:38px;border-radius:50%;background:#CFD9DE;flex:none"></div><div style="flex:1">
      <div style="font-size:14px"><b>Fotocal</b> <span style="color:#536471">@fotocal · 2 h</span></div><div style="font-size:14px;margin:2px 0 8px">${m.msg} ${esc(p.url)}</div>
      <div style="position:relative;border-radius:16px;overflow:hidden;border:1px solid #CFD9DE"><img src="${p.img}" style="width:100%;display:block">
      <div style="position:absolute;left:10px;bottom:10px;background:rgba(0,0,0,.77);color:#fff;font-size:12.5px;border-radius:4px;padding:1px 6px;max-width:85%;${clamp(1)}">${esc(p.title)}</div></div>
      <div style="font-size:12.5px;color:#536471;margin-top:4px">From getfotocal.com</div></div></div>`),
    phone('Facebook', '#FFFFFF', `<div style="font-size:14px;margin-bottom:8px"><b>Fotocal</b><div style="color:#65676B;font-size:12px">2 h · 🌐</div></div><div style="font-size:14px;margin-bottom:8px">${m.msg}</div>
      <div style="margin:0 -14px;background:#F0F2F5"><img src="${p.img}" style="width:100%;display:block"><div style="padding:9px 14px 11px">
      <div style="font-size:12px;color:#65676B;text-transform:uppercase">getfotocal.com</div><div style="font-weight:600;font-size:15px;margin-top:2px;${clamp(2)}">${esc(p.title)}</div><div style="font-size:13px;color:#65676B;margin-top:2px;${clamp(1)}">${esc(p.desc)}</div></div></div>`),
    phone('Telegram', '#C6D9B3', `<div style="margin-left:auto;width:300px;background:#EFFEDD;border-radius:12px;padding:7px 9px 5px;box-shadow:0 1px 2px rgba(0,0,0,.12)">
      <div style="font-size:14px;color:#168ACD">https://${esc(p.url)}</div><div style="margin-top:5px;border-left:3px solid #4FAE4E;padding:1px 0 2px 8px">
      <div style="font-size:13.5px;font-weight:600;color:#4FAE4E">Fotocal</div><div style="font-size:13.5px;font-weight:600;${clamp(2)}">${esc(p.title)}</div><div style="font-size:13px;margin-top:1px;${clamp(3)}">${esc(p.desc)}</div>
      <img src="${p.img}" style="width:100%;display:block;border-radius:6px;margin-top:6px"></div><div style="text-align:right;font-size:11px;color:#5FAA4E">${m.time} ✓✓</div></div>`),
  ].join('');
}
const CSS = `body{margin:0;background:#E9E6E1;font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#111B21}
  .row{display:flex;gap:22px;padding:26px;align-items:flex-start}.ph{width:360px;flex:none}.app{font:700 17px system-ui;margin:0 0 8px 4px;color:#333}
  .scr{height:620px;border-radius:30px;border:8px solid #222;padding:18px 14px;box-sizing:border-box;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end}
  h2{font:700 22px system-ui;margin:22px 26px 0;color:#222}`;
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
for (const lang of ['es', 'en']) for (const [k, path] of Object.entries(PAGES)) {
  const p = read(lang, path);
  await page.setViewportSize({ width: 1950, height: 760 });
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>${CSS}</style><h2>${k} · ${lang.toUpperCase()} · ${esc(p.url)}</h2><div class="row">${apps(p, lang)}</div>`, { waitUntil: 'load' });
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  await page.screenshot({ path: join(out, `apps-${k}-${lang}.png`), fullPage: true });
}
// home: before and after, as the full card and as a ~300 px chat thumbnail
const b = `${base}/docs/og-previews/before/home-es.jpg`, a = read('es', '').img;
await page.setViewportSize({ width: 1300, height: 900 });
await page.setContent(`<!doctype html><meta charset="utf-8"><style>${CSS} .c{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:24px} img{width:100%;display:block;border:1px solid #ccc} .s{width:300px} p{font:700 18px system-ui;margin:0 0 8px}</style>
  <div class="c"><div><p style="color:#b00020">BEFORE · home · ES</p><img src="${b}"></div><div><p style="color:#0a7a3d">AFTER · home · ES</p><img src="${a}"></div>
  <div><p style="color:#b00020">BEFORE at thumbnail size (300 px)</p><img class="s" src="${b}"></div><div><p style="color:#0a7a3d">AFTER at thumbnail size (300 px)</p><img class="s" src="${a}"></div></div>`, { waitUntil: 'load' });
await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
await page.screenshot({ path: join(out, 'home-before-after.png'), fullPage: true });
await browser.close();
console.log('mock-ups written to ' + out);
