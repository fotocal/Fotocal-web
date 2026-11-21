// Three design directions for the HOME share card (v2), for the owner to
// pick from: A food hero, B big phone, C bold type. Writes the cards and one
// comparison picture (card, 300 px thumbnail, square crop, WhatsApp,
// Instagram DM) to docs/og-previews/v2/.   Needs the local server on :8765.
// Card type: Plus Jakarta Sans ExtraBold (SIL OFL, tools/og/fonts/), used
// for the cards only; it is not shipped to the site.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
const ROOT = new URL('..', import.meta.url).pathname.replace(/\/$/, '');
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const out = join(ROOT, 'docs/og-previews/v2'); mkdirSync(out, { recursive: true });
const HEAD = `<meta charset="utf-8"><link rel="stylesheet" href="${base}/assets/css/site.css"><style>
@font-face{font-family:"PJS";font-weight:700;src:url(${base}/tools/og/fonts/plus-jakarta-sans-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"PJS";font-weight:800;src:url(${base}/tools/og/fonts/plus-jakarta-sans-latin-800-normal.woff2) format("woff2")}
*{box-sizing:border-box}html,body{margin:0}body{width:1200px;height:630px;overflow:hidden;position:relative;font-family:"PJS",system-ui,sans-serif;font-weight:800;background:var(--surface);color:var(--ink)}
.abs{position:absolute}.logo{display:flex;align-items:center;gap:14px;font-size:44px;letter-spacing:-.02em}.logo img{width:72px;height:72px}
h1{margin:0;font-weight:800;letter-spacing:-.035em;line-height:1.02}
.chip{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:10px 20px;font-size:26px;font-weight:800;white-space:nowrap}
.sticker{position:absolute;background:var(--surface);color:var(--ink);border-radius:26px;padding:14px 24px;font-size:34px;box-shadow:var(--shadow-lift);white-space:nowrap}
</style>`;
const LOGO = `${base}/assets/img/logo.png`, BOWL = `${base}/assets/img/screens/scan-plate-900.webp`, SHOT = `${base}/assets/img/screens/app-scan-1080-es.webp`;
const chips = `<span class="chip" style="background:var(--macro-protein-bg);color:var(--macro-protein-text)">Proteína 40 g</span><span class="chip" style="background:var(--macro-carbs-bg);color:var(--macro-carbs-text)">Hidratos 70 g</span><span class="chip" style="background:var(--macro-fats-bg);color:var(--macro-fats-text)">Grasa 20 g</span>`;
const CARDS = {
  A: `<img class="abs" src="${BOWL}" style="left:0;top:-330px;width:1200px;height:1200px;object-fit:cover">
    <div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(var(--ink-rgb),.78) 0%,rgba(var(--ink-rgb),.80) 34%,rgba(var(--ink-rgb),.42) 60%,rgba(var(--ink-rgb),0) 82%)"></div>
    <div class="abs logo" style="left:290px;top:40px;color:var(--on-dark)"><img src="${LOGO}"><span>Fotocal</span></div>
    <h1 class="abs" style="left:290px;top:150px;font-size:98px;color:var(--on-dark)">Una foto.<br><span style="color:var(--macro-carbs)">600 kcal.</span></h1>
    <div class="abs" style="left:290px;top:398px;width:640px;background:var(--surface);border-radius:32px;padding:22px 26px 24px;box-shadow:var(--shadow-lift)">
      <div style="font-size:34px;letter-spacing:-.02em">Tazón de pollo con arroz</div>
      <div style="display:flex;gap:10px;margin-top:14px">${chips}</div></div>`,
  B: `<div class="abs" style="inset:0;background:linear-gradient(105deg,var(--pink) 0%,var(--coral) 55%,var(--macro-carbs) 100%)"></div>
    <div class="abs" style="left:-140px;bottom:-200px;width:520px;height:520px;border-radius:50%;background:rgba(var(--white-rgb),.14)"></div>
    <div class="abs" style="right:-120px;top:-160px;width:460px;height:460px;border-radius:50%;background:rgba(var(--white-rgb),.18)"></div>
    <div class="abs logo" style="left:290px;top:46px;color:var(--on-brand)"><img src="${LOGO}" style="background:var(--surface);border-radius:20px;padding:6px"><span>Fotocal</span></div>
    <h1 class="abs" style="left:290px;top:180px;font-size:72px;color:var(--on-brand)">Una foto.<br>Todas las<br><span style="color:var(--ink)">calorías.</span></h1>
    <div class="abs" style="left:668px;top:44px;width:330px;height:700px;border-radius:46px;border:10px solid var(--ink);overflow:hidden;box-shadow:0 40px 80px -20px rgba(var(--ink-rgb),.55);transform:rotate(4deg);background:var(--surface)"><img src="${SHOT}" style="width:100%;display:block"></div>
    <div class="sticker" style="left:36px;top:468px;transform:rotate(-7deg)">40 g proteína</div>
    <div class="sticker" style="right:30px;top:300px;transform:rotate(6deg);background:var(--ink);color:var(--on-ink);font-size:40px">600 kcal</div>`,
  C: `<div class="abs" style="inset:0;background:var(--macro-carbs-bg)"></div>
    <div class="abs" style="right:-150px;top:-190px;width:620px;height:620px;border-radius:50%;background:var(--macro-carbs);opacity:.55"></div>
    <div class="abs" style="left:-170px;bottom:-230px;width:480px;height:480px;border-radius:50%;background:var(--coral);opacity:.9"></div>
    <div class="abs logo" style="left:288px;top:36px"><img src="${LOGO}" style="width:104px;height:104px"><span style="font-size:54px">Fotocal</span></div>
    <h1 class="abs" style="left:288px;top:172px;font-size:92px">Cuenta<br>calorías con<br><span style="background:linear-gradient(90deg,var(--coral),var(--pink));-webkit-background-clip:text;background-clip:text;color:transparent">una foto.</span></h1>
    <div class="abs" style="left:850px;top:214px;width:400px;height:400px;border-radius:50%;overflow:hidden;border:12px solid var(--surface);box-shadow:var(--shadow-lift)"><img src="${BOWL}" style="width:100%;height:100%;object-fit:cover"></div>
    <div class="sticker" style="left:740px;top:498px;transform:rotate(-6deg);background:var(--ink);color:var(--on-ink);font-size:42px">600 kcal</div>`,
};
const browser = await chromium.launch();
const ctx = await browser.newContext({ deviceScaleFactor: 1 });
const page = await ctx.newPage();
let current = '';
await page.route(base + '/__og', r => r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: current }));
const sizes = {};
for (const [k, inner] of Object.entries(CARDS)) {
  current = `<!doctype html><html lang="es"><head>${HEAD}</head><body>${inner}</body></html>`;
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.goto(base + '/__og', { waitUntil: 'load' });
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  const buf = await page.screenshot({ type: 'jpeg', quality: 86 });
  writeFileSync(join(out, `home-${k}.jpg`), buf); sizes[k] = Math.round(buf.length / 1024);
}
// the comparison picture
const NAME = { A: 'A · Food hero', B: 'B · Big phone', C: 'C · Bold type' };
const T = 'Contador de calorías gratis: con una foto, sin pesar nada', D = 'Haz una foto al plato y Fotocal cuenta calorías y macros en segundos.';
const clamp = n => `display:-webkit-box;-webkit-line-clamp:${n};-webkit-box-orient:vertical;overflow:hidden`;
const row = k => { const img = `${base}/docs/og-previews/v2/home-${k}.jpg?${Date.now()}`; return `<section><h2>${NAME[k]} <small>${sizes[k]} KB</small></h2><div class="r">
  <div><p>Card (1200×630)</p><img src="${img}" style="width:640px;border-radius:6px"></div>
  <div><p>Thumbnail, 300 px</p><img src="${img}" style="width:300px"><p style="margin-top:14px">Square crop</p><div style="width:150px;height:150px;overflow:hidden;border-radius:8px"><img src="${img}" style="height:150px;margin-left:-68px"></div></div>
  <div><p>WhatsApp</p><div class="ph" style="background:#EFEAE2"><div style="margin-left:auto;width:300px;background:#D9FDD3;border-radius:10px;padding:4px"><div style="background:#CFF2C8;border-radius:7px;overflow:hidden"><img src="${img}" style="width:100%;display:block"><div style="padding:7px 9px 8px"><div style="font-weight:600;font-size:14px;${clamp(2)}">${T}</div><div style="font-size:12.5px;color:#54656F;${clamp(2)}">${D}</div><div style="font-size:12px;color:#54656F">getfotocal.com</div></div></div><div style="padding:6px;font-size:14px;color:#027EB5">https://getfotocal.com/</div></div></div></div>
  <div><p>Instagram DM</p><div class="ph" style="background:#fff"><div style="margin-left:auto;width:270px;border-radius:18px;overflow:hidden;background:#EFEFEF"><img src="${img}" style="width:100%;display:block"><div style="padding:9px 12px 11px"><div style="font-weight:600;font-size:14px;${clamp(2)}">${T}</div><div style="font-size:12px;color:#737373">getfotocal.com</div></div></div></div></div>
  </div></section>`; };
await page.setViewportSize({ width: 1780, height: 1000 });
await page.setContent(`<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#E9E6E1;font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#111B21}section{padding:18px 26px 6px}h2{font:800 26px system-ui;margin:0 0 10px}h2 small{font:500 15px system-ui;color:#666}
  .r{display:flex;gap:26px;align-items:flex-start}p{font:600 14px system-ui;color:#555;margin:0 0 6px}img{display:block}.ph{width:350px;height:330px;border-radius:26px;border:7px solid #222;padding:14px 12px;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden}</style>${['A', 'B', 'C'].map(row).join('')}`, { waitUntil: 'load' });
await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
await page.screenshot({ path: join(out, 'home-directions-ABC.png'), fullPage: true });
await browser.close();
console.log('directions written:', JSON.stringify(sizes), 'KB');
