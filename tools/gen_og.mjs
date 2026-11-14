// Share cards (Open Graph images): one per page and language, 1200×630 JPEG,
// in assets/og/, plus a square 1080×1080 card for the two home pages.
//
// Every card is drawn from the page's own data, so it cannot drift:
//   · dish pages   tools/dishes/og.json (written by tools/gen_dishes.py):
//                  name, kcal per serving, grams, macros
//   · other pages  the BUILT page: og:title, the kicker/category, the H1
// Colours are the site's tokens (assets/css/site.css is loaded into the card
// and only var(--…) is used below); fonts are the site's two typefaces.
// No price and no offer ever appears on a card: it would go stale.
//
// tools/build_site.py points og:image at the card when it exists, adds its
// alt text (assets/og/alts.json, written here) and a version from the file's
// hash, so run:  build → this → build.  Start the server first:
//   python3 -m http.server 8765   (from the repository root)
//   node tools/gen_og.mjs [id-filter]     e.g. node tools/gen_og.mjs home-
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';
const ROOT = new URL('..', import.meta.url).pathname.replace(/\/$/, '');
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const only = process.argv[2] || '';
const MAX_BYTES = 300 * 1024;
const walk = (d, out = []) => { for (const f of readdirSync(d)) { const p = join(d, f); if (statSync(p).isDirectory()) { if (!['src', 'tools', 'assets', 'docs', '.git', 'node_modules'].includes(f)) walk(p, out); } else if (f === 'index.html') out.push(p); } return out; };
const pages = walk(ROOT).map(p => relative(ROOT, p));
mkdirSync(join(ROOT, 'assets', 'og'), { recursive: true });
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const text = h => h.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&#x27;|&rsquo;/g, '’').replace(/\s+/g, ' ').trim();
const meta = (html, prop) => text((html.match(new RegExp(`<meta property="${prop}" content="([^"]*)"`)) || [, ''])[1]);
const OG = JSON.parse(readFileSync(join(ROOT, 'tools', 'dishes', 'og.json'), 'utf8'));
const num = (x, lang) => { const s = String(Math.round(x * 10) / 10); const [i, f] = s.split('.'); const g = i.replace(/\B(?=(\d{3})+(?!\d))/g, lang === 'es' ? '.' : ','); return f ? g + (lang === 'es' ? ',' : '.') + f : g; };

// ── words ────────────────────────────────────────────────────────────
const T = {
  es: { home1: 'Haz una foto.', home2: 'Fotocal cuenta las calorías.', homeSub: 'Contador de calorías con IA · Android', perServing: 'kcal por ración', protein: 'Proteínas', carbs: 'Hidratos', fat: 'Grasas',
        dishKick: 'Calorías', calcKick: 'Calculadora gratis', calcLine: 'Tu resultado en 30 segundos · Sin registro', hub1: 'Calorías de la comida española', hubSub: n => `${n} platos · por ración y por 100 g`,
        table1: 'Tabla de calorías', tableSub: n => `${n} alimentos y platos · para consultar o imprimir`, calcHub1: 'Calculadoras de nutrición', calcHubSub: '8 calculadoras gratis · sin registro', blog: 'Blog', blogHub1: 'El blog de Fotocal', blogHubSub: 'Calorías, hábitos y comida de verdad' },
  en: { home1: 'Snap a photo.', home2: 'Fotocal counts the calories.', homeSub: 'AI calorie counter · Android', perServing: 'kcal per serving', protein: 'Protein', carbs: 'Carbs', fat: 'Fat',
        dishKick: 'Calories', calcKick: 'Free calculator', calcLine: 'Your result in 30 seconds · No sign-up', hub1: 'Calories in Spanish food', hubSub: n => `${n} dishes · per serving and per 100 g`,
        table1: 'Food calorie chart', tableSub: n => `${n} foods and dishes · to look up or print`, calcHub1: 'Nutrition calculators', calcHubSub: '8 free calculators · no sign-up', blog: 'Blog', blogHub1: 'The Fotocal blog', blogHubSub: 'Calories, habits and real food' },
};
const CALC = {
  'calorias-diarias': { es: 'Calorías diarias', en: 'Daily calories', icon: 'M12 3c1 3-2 4-2 7a2 2 0 0 0 4 0c0-1 0-2-1-3 3 1 5 4 5 7a6 6 0 0 1-12 0c0-5 4-7 6-11z' },
  'deficit-calorico': { es: 'Déficit calórico', en: 'Calorie deficit', icon: 'M4 6l6 6 4-4 6 7M20 10v5h-5' },
  'imc': { es: 'IMC', en: 'BMI', icon: 'M4 16a8 8 0 0 1 16 0M12 16l4-6M4 16h16' },
  'proteinas': { es: 'Proteínas al día', en: 'Protein per day', icon: 'M12 4c-4 0-6 4-6 8s2.5 8 6 8 6-4 6-8-2-8-6-8zM12 10a3 3 0 1 0 0 6 3 3 0 0 0 0-6z' },
  'macros': { es: 'Macros y calorías', en: 'Macros and calories', icon: 'M12 3v9l7.5 4.5A9 9 0 1 1 12 3zM12 3a9 9 0 0 1 9 9h-9z' },
  'agua': { es: 'Agua al día', en: 'Water per day', icon: 'M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z' },
  'tmb': { es: 'Metabolismo basal (TMB)', en: 'Basal metabolic rate (BMR)', icon: 'M3 12h4l2-5 4 10 2-5h6' },
  'peso-saludable': { es: 'Peso ideal según altura', en: 'Ideal weight by height', icon: 'M5 20h14M7 20V8l5-4 5 4v12M10 12h4M10 16h4' },
};
// a food tone per dish group, from the site's own macro and glow tokens
const TONE = { platos: 'var(--coral)', tapas: 'var(--macro-carbs)', desayuno: 'var(--macro-carbs)', basicos: 'var(--macro-protein)', bebidas: 'var(--pink)' };

// ── shared pieces ────────────────────────────────────────────────────
const CSS = `
  *{box-sizing:border-box} html,body{margin:0;padding:0}
  body{width:var(--W);height:var(--H);overflow:hidden;position:relative;font-family:var(--font-body);-webkit-font-smoothing:antialiased;background:var(--dark);color:var(--on-dark)}
  .cream{background:var(--macro-carbs-bg);color:var(--ink)}
  .glow{position:absolute;border-radius:50%;filter:blur(90px);pointer-events:none}
  .brand{position:absolute;left:64px;top:52px;display:flex;align-items:center;gap:16px;font-family:var(--font-display);font-weight:600;font-size:38px;letter-spacing:-.01em}
  .brand img{width:60px;height:60px}
  .url{position:absolute;left:64px;bottom:50px;font-size:26px;font-weight:600;opacity:.82}
  .kick{font-size:25px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral)}
  .cream .kick{color:var(--brand-text)}
  h1{margin:0;font-family:var(--font-display);font-weight:600;letter-spacing:-.02em;line-height:1.04}
  .grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
  .pill{display:inline-flex;align-items:center;gap:10px;padding:12px 22px;border-radius:999px;font-size:26px;font-weight:700}
  .bar{position:absolute;left:0;right:0;bottom:0;height:14px;background:var(--grad)}
`;
const logo = `<div class="brand"><img src="${base}/assets/img/logo-96.png" alt=""><span>Fotocal</span></div>`;
const doc = (lang, cls, inner, W = 1200, H = 630) => `<!doctype html><html lang="${lang}"><head><meta charset="utf-8">
<link rel="stylesheet" href="${base}/assets/css/fonts.css"><link rel="stylesheet" href="${base}/assets/css/site.css">
<style>:root{--W:${W}px;--H:${H}px}${CSS}</style></head><body class="${cls}">${inner}</body></html>`;
const fit = (s, sizes) => { for (const [max, px] of sizes) if (s.length <= max) return px; return sizes[sizes.length - 1][1]; };

// ── templates ────────────────────────────────────────────────────────
function home(lang, square) {
  const t = T[lang], shot = `${base}/assets/img/screens/app-scan-700-${lang}.webp`;
  if (square) return doc(lang, '', `
    <div class="glow" style="width:700px;height:700px;left:-200px;top:-220px;background:var(--glow-coral)"></div>
    <div class="glow" style="width:700px;height:700px;right:-240px;bottom:-200px;background:var(--glow-pink)"></div>
    ${logo}
    <h1 style="position:absolute;left:64px;right:64px;top:170px;font-size:84px">${esc(t.home1)}<br><span class="grad">${esc(t.home2)}</span></h1>
    <div style="position:absolute;left:50%;top:470px;width:470px;transform:translateX(-50%);border-radius:44px 44px 0 0;overflow:hidden;border:10px solid var(--frame);border-bottom:0;box-shadow:var(--shadow-lift)"><img src="${shot}" style="display:block;width:100%"></div>
    <div class="bar"></div>`, 1080, 1080);
  return doc(lang, '', `
    <div class="glow" style="width:640px;height:640px;left:-220px;top:-260px;background:var(--glow-coral)"></div>
    <div class="glow" style="width:620px;height:620px;right:60px;bottom:-320px;background:var(--glow-pink)"></div>
    ${logo}
    <div style="position:absolute;left:64px;top:176px;width:650px">
      <h1 style="font-size:${lang === 'es' ? 76 : 78}px">${esc(t.home1)}<br><span class="grad">${esc(t.home2)}</span></h1>
      <p style="margin:30px 0 0;font-size:30px;font-weight:600;color:var(--on-dark-soft)">${esc(t.homeSub)}</p>
    </div>
    <div class="url">getfotocal.com</div>
    <div style="position:absolute;right:92px;top:46px;width:330px;border-radius:40px;overflow:hidden;border:9px solid var(--frame);box-shadow:var(--shadow-lift);transform:rotate(3deg)"><img src="${shot}" style="display:block;width:100%"></div>
    <div class="bar"></div>`);
}

function dish(lang, d) {
  const t = T[lang], name = d[lang], tone = TONE[d.group] || 'var(--coral)';
  const size = fit(name, [[14, 86], [22, 72], [32, 58], [99, 48]]);
  const chip = (label, v, c, bg) => `<span class="pill" style="background:${bg};color:${c}">${esc(label)} <b style="font-weight:800">${num(v, lang)} g</b></span>`;
  return doc(lang, 'cream', `
    <div class="glow" style="width:620px;height:620px;right:-140px;top:-220px;background:${tone};opacity:.34"></div>
    <div class="glow" style="width:520px;height:520px;right:180px;bottom:-330px;background:var(--pink);opacity:.20"></div>
    ${logo}
    <div style="position:absolute;left:64px;top:150px;width:640px">
      <div class="kick">${esc(t.dishKick)}</div>
      <h1 style="margin-top:14px;font-size:${size}px">${esc(name)}</h1>
      ${lang === 'en' && d.en_sub ? `<p style="margin:14px 0 0;font-size:32px;font-weight:600;color:var(--text-soft)">${esc(d.en_sub)}</p>` : ''}
    </div>
    <div style="position:absolute;left:64px;bottom:112px;display:flex;gap:12px;flex-wrap:wrap;width:760px">
      ${chip(t.protein, d.p, 'var(--macro-protein-text)', 'var(--macro-protein-bg)')}${chip(t.carbs, d.c, 'var(--macro-carbs-text)', 'var(--surface)')}${chip(t.fat, d.f, 'var(--macro-fats-text)', 'var(--macro-fats-bg)')}
    </div>
    <div class="url">getfotocal.com</div>
    <div style="position:absolute;right:56px;top:128px;width:400px;height:400px;border-radius:50%;background:var(--surface);box-shadow:var(--shadow-lift);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
      <div class="grad" style="font-family:var(--font-display);font-weight:600;font-size:${d.kcal >= 1000 ? 136 : 168}px;line-height:.95;letter-spacing:-.03em;padding:0 8px">${num(d.kcal, lang)}</div>
      <div style="margin-top:8px;font-size:30px;font-weight:700;color:var(--ink)">${esc(t.perServing)}</div>
      <div style="margin-top:4px;font-size:25px;font-weight:600;color:var(--muted)">${esc(d['serving_' + lang])} · ${num(d.g, lang)} g</div>
    </div>
    <div class="bar"></div>`);
}

function calc(lang, c) {
  const t = T[lang], name = c[lang];
  return doc(lang, '', `
    <div class="glow" style="width:640px;height:640px;right:-160px;top:-240px;background:var(--glow-coral)"></div>
    <div class="glow" style="width:560px;height:560px;left:-220px;bottom:-320px;background:var(--glow-pink)"></div>
    ${logo}
    <div style="position:absolute;left:64px;top:186px;width:700px">
      <div class="kick">${esc(t.calcKick)}</div>
      <h1 style="margin-top:16px;font-size:${fit(name, [[16, 92], [24, 76], [99, 62]])}px">${esc(name)}</h1>
      <p style="margin:28px 0 0;font-size:30px;font-weight:600;color:var(--on-dark-soft)">${esc(t.calcLine)}</p>
    </div>
    <div class="url">getfotocal.com</div>
    <div style="position:absolute;right:78px;top:150px;width:330px;height:330px;border-radius:84px;background:var(--grad);box-shadow:var(--shadow-lift);display:grid;place-items:center;transform:rotate(-5deg)">
      <svg viewBox="0 0 24 24" width="190" height="190" fill="none" stroke="var(--on-brand)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="${c.icon}"/></svg>
    </div>
    <div class="bar"></div>`);
}

function post(lang, kicker, title) {
  return doc(lang, '', `
    <div class="glow" style="width:700px;height:700px;right:-260px;top:-300px;background:var(--glow-coral)"></div>
    <div class="glow" style="width:620px;height:620px;left:240px;bottom:-420px;background:var(--glow-pink)"></div>
    <div style="position:absolute;right:-90px;bottom:-110px;width:500px;height:500px;border-radius:50%;overflow:hidden;border:10px solid var(--frame);box-shadow:var(--shadow-lift)"><img src="${base}/assets/img/screens/scan-plate-900.webp" style="width:100%;height:100%;object-fit:cover"></div>
    ${logo}
    <div style="position:absolute;left:64px;top:150px;bottom:110px;width:${title.length > 44 ? 820 : 780}px;display:flex;flex-direction:column;justify-content:center">
      <span class="pill" style="align-self:flex-start;background:var(--grad);color:var(--on-brand);font-size:23px;letter-spacing:.08em;text-transform:uppercase;padding:9px 20px">${esc(kicker)}</span>
      <h1 style="margin-top:26px;font-size:${fit(title, [[30, 88], [44, 76], [60, 64], [999, 54]])}px">${esc(title)}</h1>
    </div>
    <div class="url">getfotocal.com</div>
    <div class="bar"></div>`);
}

function hub(lang, title, sub, kicker) {
  return doc(lang, 'cream', `
    <div class="glow" style="width:640px;height:640px;right:-180px;top:-240px;background:var(--coral);opacity:.32"></div>
    <div class="glow" style="width:520px;height:520px;left:-200px;bottom:-330px;background:var(--pink);opacity:.18"></div>
    <div style="position:absolute;right:-60px;top:70px;width:500px;height:500px;border-radius:50%;overflow:hidden;border:12px solid var(--surface);box-shadow:var(--shadow-lift)"><img src="${base}/assets/img/screens/scan-plate-900.webp" style="width:100%;height:100%;object-fit:cover"></div>
    ${logo}
    <div style="position:absolute;left:64px;top:176px;width:690px">
      <div class="kick">${esc(kicker)}</div>
      <h1 style="margin-top:14px;font-size:${fit(title, [[18, 86], [28, 72], [99, 60]])}px">${esc(title)}</h1>
      <p style="margin:26px 0 0;font-size:30px;font-weight:700;color:var(--text-soft)">${esc(sub)}</p>
    </div>
    <div class="url">getfotocal.com</div>
    <div class="bar"></div>`);
}

// ── which card for which page ────────────────────────────────────────
// "gratis"/"free" never goes on an image: on this site the word must sit next
// to the free plan's limits, and an image has no room for them.
const clean = s => s.replace(/\s*\((?:gratis|free)\)/gi, '').replace(/,?\s+(?:gratis|free)\b(?=[:.,]|$)/gi, '').replace(/\b(?:gratis|free)\s+/gi, '').replace(/\s{2,}/g, ' ').trim().replace(/^./, c => c.toUpperCase());
function card(rel, html, lang) {
  const t = T[lang], bare = rel.replace(/^en\//, '').replace(/index\.html$/, '');
  const ogTitle = clean((meta(html, 'og:title') || text((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [, 'Fotocal'])[1])).replace(/\s+[—|]\s+Fotocal$/, ''));
  let m;
  if (bare === '') return { html: home(lang), alt: `${t.home1} ${t.home2}`, square: home(lang, true) };
  if ((m = bare.match(/^calorias\/([^/]+)\/$/)) && OG.dishes[m[1]]) {
    const d = OG.dishes[m[1]];
    return { html: dish(lang, d), alt: `${d[lang]}: ${num(d.kcal, lang)} ${t.perServing} (${num(d.g, lang)} g)` };
  }
  if (bare === 'calorias/') return { html: hub(lang, t.hub1, t.hubSub(OG.n_ready), 'Fotocal'), alt: `${t.hub1}: ${t.hubSub(OG.n_ready)}` };
  if (bare === 'calorias/tabla-de-calorias/') return { html: hub(lang, t.table1, t.tableSub(OG.n_hand), t.dishKick), alt: `${t.table1}: ${t.tableSub(OG.n_hand)}` };
  if (bare === 'calculadoras/') return { html: hub(lang, t.calcHub1, t.calcHubSub, 'Fotocal'), alt: `${t.calcHub1}: ${t.calcHubSub}` };
  if ((m = bare.match(/^calculadoras\/([^/]+)\/$/)) && CALC[m[1]]) return { html: calc(lang, CALC[m[1]]), alt: `${t.calcKick}: ${CALC[m[1]][lang]}. ${t.calcLine}` };
  if (bare === 'blog/') return { html: hub(lang, t.blogHub1, t.blogHubSub, t.blog), alt: `${t.blogHub1}: ${t.blogHubSub}` };
  // the post's category is the last breadcrumb (…/blog/?cat=…); other pages use their first kicker
  let kicker = text((html.match(/<a href="[^"]*\?cat=[^"]*">([^<]+)<\/a>\s*<\/nav>/) || html.match(/class="kicker[^"]*"[^>]*>([\s\S]*?)<\//) || [, ''])[1]);
  if (!kicker || kicker.length > 34) kicker = bare.startsWith('blog/') ? t.blog : 'Fotocal';
  return { html: post(lang, kicker, ogTitle), alt: `${ogTitle} · Fotocal` };
}

// ── render ───────────────────────────────────────────────────────────
const browser = await chromium.launch();
const ctx = await browser.newContext({ deviceScaleFactor: 1 });
const page = await ctx.newPage();
let current = '';
await page.route(base + '/__og', r => r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: current }));   // same origin as the fonts
async function shoot(html, file, W, H) {
  current = html;
  await page.setViewportSize({ width: W, height: H });
  await page.goto(base + '/__og', { waitUntil: 'load' });
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  let q = 86, buf;
  do { buf = await page.screenshot({ type: 'jpeg', quality: q, clip: { x: 0, y: 0, width: W, height: H } }); q -= 6; } while (buf.length > MAX_BYTES && q > 50);
  writeFileSync(join(ROOT, 'assets', 'og', file), buf);
  return buf.length;
}
const altsFile = join(ROOT, 'assets', 'og', 'alts.json');
const alts = only && existsSync(altsFile) ? JSON.parse(readFileSync(altsFile, 'utf8')) : {};
let n = 0, skipped = 0, biggest = 0;
for (const rel of pages) {
  const html = readFileSync(join(ROOT, rel), 'utf8');
  if (/content="noindex/.test(html)) { skipped++; continue; }
  const lang = rel.startsWith('en/') ? 'en' : 'es';
  const bare = rel.replace(/^en\//, '');
  const id = (bare === 'index.html' ? 'home' : bare.replace(/\/index\.html$/, '').replace(/\//g, '-')) + '-' + lang;
  if (only && !id.includes(only)) continue;
  const c = card(rel, html, lang);
  biggest = Math.max(biggest, await shoot(c.html, id + '.jpg', 1200, 630));
  if (c.square) await shoot(c.square, id + '-square.jpg', 1080, 1080);
  alts[id] = c.alt; n++;
}
await browser.close();
writeFileSync(altsFile, JSON.stringify(Object.fromEntries(Object.entries(alts).sort()), null, 1) + '\n');
console.log(`og cards: ${n} written, ${skipped} noindex pages skipped, largest ${Math.round(biggest / 1024)} KB`);
