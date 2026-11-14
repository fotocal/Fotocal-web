// Share cards (Open Graph images), v3: one per page and language, 1200×630
// JPEG in assets/og/, plus a square 1080×1080 card for the two home pages.
//
// The look (owner's spec, Nov 2026): a warm off-white ground, near-black
// heavy type, grey small print and ONE accent, the brand orange. A short
// text block on the left, ONE real visual on the right: genuine app
// captures (tools/captures/) or a real phone-size screenshot of the page
// itself, in a plain upright phone frame that runs off the bottom edge.
// Nothing drawn: no stickers, pills, badges, shapes, tilts or emoji.
// No price, no offer and no "gratis"/"free" on any card.
//
// Every card is built from the page's own data, so it cannot drift:
//   · dish pages   tools/dishes/og.json (written by tools/gen_dishes.py)
//   · other pages  the BUILT page: og:title, its category, and for
//                  calculators, hubs and the table a live screenshot
// Type: Plus Jakarta Sans (SIL OFL, tools/og/fonts/), for the cards only.
//
// tools/build_site.py points og:image at the card, adds its alt text
// (assets/og/alts.json, written here) and a ?v= from the file's hash, so
// run:  build → this → build.  Start the server first:
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
// the one accent is the site's own orange token, read from the stylesheet
const ORANGE = (readFileSync(join(ROOT, 'assets', 'css', 'site.css'), 'utf8').match(/--coral:\s*(#[0-9A-Fa-f]{6})/) || [])[1];
if (!ORANGE) throw new Error('--coral not found in assets/css/site.css');
const [OR, OG_, OB] = [1, 3, 5].map(i => parseInt(ORANGE.slice(i, i + 2), 16));

// ── words ────────────────────────────────────────────────────────────
const T = {
  es: { home: ['Haz una foto.', 'Sabrás las', 'calorías.'], homeSq: ['Haz una foto.', 'Sabrás las ', 'calorías.'], homeSub: 'Contador de calorías con IA · Android', perServing: 'kcal por ración',
        macros: d => `Proteínas ${num(d.p, 'es')} g · Hidratos ${num(d.c, 'es')} g · Grasas ${num(d.f, 'es')} g`, calcLine: 'Resultado en 30 segundos · Sin registro',
        hub: 'Calorías de la comida española', hubSub: n => `${n} platos · por ración y por 100 g`, table: 'Tabla de calorías', tableSub: n => `${n} alimentos y platos españoles`,
        calcHub: 'Calculadoras de nutrición', calcHubSub: '8 calculadoras · Sin registro', blogHub: 'El blog de Fotocal', blogHubSub: 'Calorías, hábitos y comida de verdad', blogFoot: 'Blog de Fotocal', blog: 'Blog' },
  en: { home: ['Snap a photo.', 'Know the', 'calories.'], homeSq: ['Snap a photo.', 'Know the ', 'calories.'], homeSub: 'AI calorie counter · Android', perServing: 'kcal per serving',
        macros: d => `Protein ${num(d.p, 'en')} g · Carbs ${num(d.c, 'en')} g · Fat ${num(d.f, 'en')} g`, calcLine: 'Result in 30 seconds · No sign-up',
        hub: 'Calories in Spanish food', hubSub: n => `${n} dishes · per serving and per 100 g`, table: 'Food calorie chart', tableSub: n => `${n} Spanish foods and dishes`,
        calcHub: 'Nutrition calculators', calcHubSub: '8 calculators · No sign-up', blogHub: 'The Fotocal blog', blogHubSub: 'Calories, habits and real food', blogFoot: 'The Fotocal blog', blog: 'Blog' },
};
const CALC = {
  'calorias-diarias': { es: 'Calculadora de calorías diarias', en: 'Daily calorie calculator' },
  'deficit-calorico': { es: 'Calculadora de déficit calórico', en: 'Calorie deficit calculator' },
  'imc': { es: 'Calculadora de IMC', en: 'BMI calculator' },
  'proteinas': { es: 'Calculadora de proteínas', en: 'Protein calculator' },
  'macros': { es: 'Calculadora de macros', en: 'Macro calculator' },
  'agua': { es: '¿Cuánta agua beber al día?', en: 'How much water to drink a day' },
  'tmb': { es: 'Calculadora de metabolismo basal', en: 'BMR calculator' },
  'peso-saludable': { es: 'Peso ideal según tu altura', en: 'Ideal weight by height' },
};
const CALC_Q = { es: 'sexo=mujer&edad=35&altura=165&peso=70&actividad=light&objetivo=perder&ritmo=0.5&meta=62&grasa=25&reparto=balanced&kcal=2150',
                 en: 'sex=woman&age=35&height=165&weight=70&activity=light&goal=lose&pace=0.5&target=62&bodyfat=25&split=balanced&kcal=2150' };
// real app captures (tools/captures/): the full phone screens the site's own pictures were cut from
const cap = (name, lang) => `${base}/tools/captures/${name}-${existsSync(join(ROOT, 'tools', 'captures', `${name}-${lang}.jpg`)) ? lang : 'es'}.jpg`;
const CAP = { result: 's7/scan-result-top', home: 's7/home-calories', progress: 's7/progress-top', streak: 's7/streak', activity: 's7/home-activity-day', voice: 's7/voice-result', coach: 's2/coach' };
const BLOG_CAP = { calories: CAP.result, weightloss: CAP.progress, nutrition: CAP.home, eating: CAP.home, mindset: CAP.streak, movement: CAP.activity };

// ── shared pieces ────────────────────────────────────────────────────
const F = `${base}/tools/og/fonts/plus-jakarta-sans-latin-`;
const CSS = `
@font-face{font-family:"PJS";font-weight:500;src:url(${F}500-normal.woff2) format("woff2")}
@font-face{font-family:"PJS";font-weight:700;src:url(${F}700-normal.woff2) format("woff2")}
@font-face{font-family:"PJS";font-weight:800;src:url(${F}800-normal.woff2) format("woff2")}
:root{--bg:#FBF7F2;--tx:#1A1A1A;--gr:#6B6B6B;--or:${ORANGE}}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{overflow:hidden;position:relative;background:var(--bg);color:var(--tx);font-family:"PJS",system-ui,sans-serif;font-weight:800;-webkit-font-smoothing:antialiased}
.glow{position:absolute;inset:0;background:radial-gradient(circle at 80% 58%,rgba(${OR},${OG_},${OB},.10) 0%,rgba(${OR},${OG_},${OB},0) 46%)}
.col{position:absolute;left:80px;top:64px;bottom:64px;display:flex;flex-direction:column;justify-content:center}
.logo{display:flex;align-items:center;gap:16px;font-size:40px;letter-spacing:-.5px;line-height:1}
.logo img{width:64px;height:64px}.logo.s{font-size:32px;gap:12px}.logo.s img{width:48px;height:48px}
h1{margin:0;font-weight:800;line-height:1.05;letter-spacing:-1.5px}
h1 .l{display:block;white-space:nowrap}
.or{color:var(--or)}
.sub{margin:0;font-size:26px;font-weight:500;color:var(--gr);line-height:1.3;letter-spacing:0}
.lab{font-size:22px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--or);line-height:1.2}
.phone{position:absolute;width:300px;height:660px;border-radius:48px;border:9px solid var(--tx);background:var(--tx);overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.18)}
.phone img{display:block;width:100%;height:100%;object-fit:cover;object-position:top center;border-radius:39px}
`;
// shrink a heading until it fits its width and its line limit (runs in the card page)
const FIT = `<script>document.fonts.ready.then(()=>{for(const e of document.querySelectorAll('[data-fit]')){const [max,min,lines]=e.dataset.fit.split(',').map(Number);let s=max;const ok=()=>{e.style.fontSize=s+'px';const lh=parseFloat(getComputedStyle(e).lineHeight);return e.scrollWidth<=e.clientWidth+1&&e.getBoundingClientRect().height<=lines*lh+2};while(!ok()&&s>min)s-=2}document.body.dataset.ready='1'})</script>`;
const logo = small => `<div class="logo${small ? ' s' : ''}"><img src="${base}/assets/img/logo.png" alt=""><span>Fotocal</span></div>`;
const doc = (lang, inner, W = 1200, H = 630) => `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><style>${CSS}body{width:${W}px;height:${H}px}</style></head><body><div class="glow"></div>${inner}${FIT}</body></html>`;
const phone = (src, x, y, extra = '') => `<div class="phone" style="left:${x}px;top:${y}px;${extra}"><img src="${src}" alt=""></div>`;

// ── templates ────────────────────────────────────────────────────────
function home(lang, square) {
  const t = T[lang], front = cap(CAP.result, lang), back = cap(CAP.home, lang);
  if (square) return doc(lang, `
    <div style="position:absolute;left:64px;right:64px;top:84px;display:flex;flex-direction:column;align-items:center;text-align:center">
      ${logo()}
      <h1 style="margin-top:36px;font-size:84px"><span class="l">${esc(t.homeSq[0])}</span><span class="l">${esc(t.homeSq[1])}<span class="or">${esc(t.homeSq[2])}</span></span></h1>
      <p class="sub" style="margin-top:28px">${esc(t.homeSub)}</p>
    </div>
    ${phone(back, 560, 470, 'width:340px;height:760px')}${phone(front, 190, 520, 'width:340px;height:760px')}`, 1080, 1080);
  return doc(lang, `
    <div class="col" style="width:560px">
      ${logo()}
      <h1 style="margin-top:36px;font-size:80px"><span class="l">${esc(t.home[0])}</span><span class="l">${esc(t.home[1])}</span><span class="l or">${esc(t.home[2])}</span></h1>
      <p class="sub" style="margin-top:28px">${esc(t.homeSub)}</p>
    </div>
    ${phone(back, 884, 50)}${phone(front, 694, 90)}`);
}

function dish(lang, d, shot) {
  const t = T[lang], name = d[lang];
  return doc(lang, `
    <div class="col" style="width:620px">
      ${logo(true)}
      <h1 data-fit="84,56,2" style="margin-top:32px;font-size:84px">${esc(name)}</h1>
      <div style="margin-top:22px;display:flex;align-items:baseline;gap:16px;white-space:nowrap">
        <span class="or" style="font-size:96px;line-height:1;letter-spacing:-2px">${num(d.kcal, lang)}</span>
        <span style="font-size:28px;font-weight:500;color:var(--gr)">${esc(t.perServing)}</span>
      </div>
      <p class="sub" data-fit="24,18,1" style="margin-top:20px;font-size:24px;white-space:nowrap">${esc(t.macros(d))}</p>
    </div>
    ${phone(shot || cap(CAP.result, lang), 800, 80)}`);
}

function titled(lang, title, line, shot, sizes = '76,52,3') {
  return doc(lang, `
    <div class="col" style="width:620px">
      ${logo()}
      <h1 data-fit="${sizes}" style="margin-top:36px;font-size:76px">${esc(title)}</h1>
      <p class="sub" style="margin-top:28px">${esc(line)}</p>
    </div>
    ${phone(shot, 800, 80)}`);
}

function post(lang, label, title, foot, shot) {
  return doc(lang, `
    <div class="col" style="width:620px">
      ${logo()}
      <div class="lab" style="margin-top:36px">${esc(label)}</div>
      <h1 data-fit="72,60,3" style="margin-top:14px;font-size:72px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;padding-bottom:6px">${esc(title)}</h1>
      <p class="sub" style="margin-top:22px">${esc(foot)}</p>
    </div>
    ${phone(shot, 800, 80)}`);
}

// ── real phone-size screenshots of the site's own pages ──────────────
const browser = await chromium.launch();
const shots = new Map();
async function webShot(lang, path, sel) {
  const key = lang + path;
  if (shots.has(key)) return shots.get(key);
  const ctx = await browser.newContext({ viewport: { width: 390, height: 858 }, deviceScaleFactor: 2, locale: lang === 'es' ? 'es-ES' : 'en-GB' });
  const p = await ctx.newPage();
  await p.goto(base + (lang === 'en' ? '/en/' : '/') + path, { waitUntil: 'load' });
  await p.addStyleTag({ content: // no price or offer may reach a card, so the download card and offer lines are left out of the screenshot
    '.fc-topbar,.calc-sticky,.lang-hint,.dl-card,.offer-badge,.offer-keep,.price-note{display:none!important}.reveal{opacity:1!important;transform:none!important}html{scroll-behavior:auto!important}#site-nav{top:0!important}' });
  if (path.includes('?')) await p.waitForSelector('.calc-out[data-state="ready"]', { timeout: 5000 }).catch(() => {});
  if (sel) await p.evaluate(s => { const e = document.querySelector(s); if (e) window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 104); }, sel);
  await p.waitForTimeout(350);
  const buf = await p.screenshot({ type: 'jpeg', quality: 82 });
  await ctx.close();
  const uri = 'data:image/jpeg;base64,' + buf.toString('base64');
  shots.set(key, uri);
  return uri;
}

// ── which card for which page ────────────────────────────────────────
// "gratis"/"free" never goes on an image: on this site the word must sit next
// to the free plan's limits, and an image has no room for them.
const clean = s => s.replace(/\s*\((?:gratis|free)\)/gi, '').replace(/,?\s+(?:gratis|free)\b(?=[:.,]|$)/gi, '').replace(/\b(?:gratis|free)\s+/gi, '').replace(/\s{2,}/g, ' ').trim().replace(/^./, c => c.toUpperCase());
async function card(rel, html, lang) {
  const t = T[lang], bare = rel.replace(/^en\//, '').replace(/index\.html$/, '');
  const ogTitle = clean((meta(html, 'og:title') || text((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [, 'Fotocal'])[1])).replace(/\s+[—|]\s+Fotocal$/, ''));
  let m;
  if (bare === '') return { html: home(lang), alt: t.home.join(' '), square: home(lang, true) };
  if ((m = bare.match(/^calorias\/([^/]+)\/$/)) && OG.dishes[m[1]]) {
    const d = OG.dishes[m[1]];
    if (process.env.OG_DISH_PAGE) return { html: dish(lang, d, await webShot(lang, bare, '.dp-kpis')), alt: '' };
    return { html: dish(lang, d), alt: `${d[lang]}: ${num(d.kcal, lang)} ${t.perServing} (${num(d.g, lang)} g). ${t.macros(d)}` };
  }
  if (bare === 'calorias/') return { html: titled(lang, t.hub, t.hubSub(OG.n_ready), await webShot(lang, bare, '.dp-table-wrap')), alt: `${t.hub}: ${t.hubSub(OG.n_ready)}` };
  if (bare === 'calorias/tabla-de-calorias/') return { html: titled(lang, t.table, t.tableSub(OG.n_hand), await webShot(lang, bare, '.dp-table-wrap')), alt: `${t.table}: ${t.tableSub(OG.n_hand)}` };
  if (bare === 'calculadoras/') return { html: titled(lang, t.calcHub, t.calcHubSub, await webShot(lang, bare, '.calc-cards')), alt: `${t.calcHub}: ${t.calcHubSub}` };
  if ((m = bare.match(/^calculadoras\/([^/]+)\/$/)) && CALC[m[1]])
    return { html: titled(lang, CALC[m[1]][lang], t.calcLine, await webShot(lang, bare + '?' + CALC_Q[lang], '.calc-out')), alt: `${CALC[m[1]][lang]}. ${t.calcLine}` };
  if (bare === 'blog/') return { html: titled(lang, t.blogHub, t.blogHubSub, await webShot(lang, bare, '.habit-grid')), alt: `${t.blogHub}: ${t.blogHubSub}` };
  // posts: the category is the last breadcrumb (…/blog/?cat=<key>); other pages use their first kicker
  const cat = html.match(/<a href="[^"]*\?cat=([a-z]+)[^"]*">([^<]+)<\/a>\s*<\/nav>/);
  if (cat) return { html: post(lang, text(cat[2]), ogTitle, t.blogFoot, cap(BLOG_CAP[cat[1]] || CAP.home, lang)), alt: `${ogTitle} · ${t.blogFoot}` };
  let kicker = text((html.match(/class="kicker[^"]*"[^>]*>([\s\S]*?)<\//) || [, ''])[1]);
  if (!kicker || kicker.length > 34) kicker = 'Fotocal';
  const shot = /voice/.test(bare) ? CAP.voice : /barcode/.test(bare) ? CAP.home : /^ai\//.test(bare) ? CAP.coach : /scan-food|^features\/$/.test(bare) ? CAP.result : CAP.home;
  return { html: post(lang, kicker, ogTitle, t.homeSub, cap(shot, lang)), alt: `${ogTitle} · Fotocal` };
}

// ── render ───────────────────────────────────────────────────────────
const ctx = await browser.newContext({ deviceScaleFactor: 1 });
const page = await ctx.newPage();
let current = '';
await page.route(base + '/__og', r => r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: current }));   // same origin as the fonts
async function shoot(html, file, W, H) {
  current = html;
  await page.setViewportSize({ width: W, height: H });
  await page.goto(base + '/__og', { waitUntil: 'load' });
  await page.waitForFunction(() => document.body.dataset.ready === '1');
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  let q = 88, buf;
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
  const c = await card(rel, html, lang);
  biggest = Math.max(biggest, await shoot(c.html, id + '.jpg', 1200, 630));
  if (c.square) await shoot(c.square, id + '-square.jpg', 1080, 1080);
  alts[id] = c.alt; n++;
}
await browser.close();
writeFileSync(altsFile, JSON.stringify(Object.fromEntries(Object.entries(alts).sort()), null, 1) + '\n');
console.log(`og cards: ${n} written, ${skipped} noindex pages skipped, largest ${Math.round(biggest / 1024)} KB`);
