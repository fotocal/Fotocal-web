// The eight calculators must give the app's answers, in both languages, and
// behave as a tool a first-time visitor understands (lang-ux, 2026-11).
//
// Every expected number below is worked out by hand from the app's code
// (fotocal/Fotocal src/logic/plan.ts, src/lib/water.ts), written out here
// independently of assets/js/calc.js. One deliberate difference from the
// app: the site ROUNDS the calorie target where the app floors it (at most
// 1 kcal), so maintenance − target always equals the deficit shown.
//
//   python3 -m http.server 8765 --bind 127.0.0.1   (from the repo root)
//   node tools/check_calcs.mjs
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36';
const browser = await chromium.launch();
const ctx = await browser.newContext({ userAgent: UA, locale: 'es-ES' });
await ctx.addInitScript(() => { try { localStorage.setItem('fotocal-lang', document.documentElement.lang || 'es'); } catch (e) {} });
const page = await ctx.newPage();
let fails = 0, n = 0;
const bad = (m) => { fails++; console.log('FAIL ' + m); };

const es = (x, d = 0) => { const [i, f] = Number(x).toFixed(d).split('.'); return i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (f ? ',' + f : ''); };
const en = (x, d = 0) => { const [i, f] = Number(x).toFixed(d).split('.'); return i.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (f ? '.' + f : ''); };
const R = '.calc-page .calc-out';
const out = async (key) => (await page.textContent(`${R} [data-out="${key}"]`)).trim();
const want = async (key, value, label) => { n++; const got = await out(key); if (got !== value) bad(`${label}: ${key} shows ${got}, expected ${value}`); };
async function fill(fields) {
  for (const [k, v] of Object.entries(fields)) {
    if (k === 'sex') await page.click(`.calc-page .calc-seg input[value="${v}"] + label`);
    else if (await page.$(`.calc-page select[name="${k}"]`)) await page.selectOption(`.calc-page select[name="${k}"]`, String(v));
    else await page.fill(`.calc-page input[name="${k}"]`, String(v));
  }
}
async function open(path, fields = {}) {
  await page.goto(base + path);
  await page.evaluate(() => localStorage.removeItem('fc_calc'));
  await page.goto(base + path);
  await fill(fields);
  await page.click('.calc-page .calc-go');
  await page.waitForTimeout(60);
}
const state = () => page.getAttribute(R, 'data-state');

// 0. a first visit: empty inputs, no result, nothing that looks like yours
for (const slug of ['calorias-diarias', 'deficit-calorico', 'imc', 'proteinas', 'macros', 'agua', 'tmb', 'peso-saludable']) {
  for (const pre of ['', '/en']) {
    await page.goto(`${base}${pre}/calculadoras/${slug}/`); await page.evaluate(() => localStorage.removeItem('fc_calc')); await page.reload();
    n++;
    const vals = await page.$$eval('.calc-page input[type=text]', els => els.map(e => e.value).filter(Boolean));
    if (vals.length) bad(`${pre}/${slug}: inputs not empty on a first visit (${vals})`);
    if ((await state()) !== 'empty') bad(`${pre}/${slug}: result shown before any input`);
    if (!(await page.isVisible('.calc-page .calc-go'))) bad(`${pre}/${slug}: no visible Calcular button`);
  }
}

// 0b. Calcular with nothing filled: a message under each field, no result
await page.goto(base + '/calculadoras/calorias-diarias/'); await page.click('.calc-page .calc-go'); await page.waitForTimeout(60);
n++; const errs = await page.$$eval('.calc-page .calc-err:not([hidden])', e => e.map(x => x.textContent.trim()));
if (errs.length < 5 || !errs.includes('Introduce un peso entre 35 y 250 kg.')) bad('empty submit: messages ' + JSON.stringify(errs));
if ((await state()) !== 'empty') bad('empty submit: a result appeared');

// 1. calorías diarias — woman 40 y, 165 cm, 70 kg, "moving all day" (1.55)
await open('/calculadoras/calorias-diarias/', { sex: 'f', age: 40, height: 165, weight: 70, activity: 'active' });
let bmr = 10 * 70 + 6.25 * 165 - 5 * 40 - 161, tdee = bmr * 1.55;           // 1370.25, 2123.89
await want('main', es(Math.round(tdee)), 'tdee maintenance');
await want('bmr', es(Math.round(bmr)), 'tdee BMR');
await want('lose50', es(Math.round(tdee - Math.min(550, tdee * 0.25))), 'tdee lose 0.5 (25 % cap)');
await want('lose25', es(Math.round(tdee - 275)), 'tdee lose 0.25');
await want('gain25', es(Math.round(tdee + 275)), 'tdee gain 0.25');
await want('bridge', es(Math.round(tdee)), 'download card headline');
n++; if ((await state()) !== 'ready') bad('tdee: result not shown after Calcular');

// 1b. a wrong value after a result: message shown, old result dimmed, never left looking current
await page.fill('.calc-page input[name="weight"]', '400'); await page.waitForTimeout(60);
n++; if ((await state()) !== 'invalid') bad('invalid weight did not dim the result');
if (await page.isHidden('.calc-page [data-err-for="weight"]')) bad('invalid weight shows no message');
await page.fill('.calc-page input[name="weight"]', '70'); await page.waitForTimeout(60);
if ((await state()) !== 'ready') bad('fixed weight did not bring the result back');

// 2. déficit — man 35 y, 178 cm, 90 kg, light (1.375), to 80 kg at 0.75 kg/week
await open('/calculadoras/deficit-calorico/', { sex: 'm', age: 35, height: 178, weight: 90, activity: 'light', target: 80, pace: '0.75' });
bmr = 10 * 90 + 6.25 * 178 - 5 * 35 + 5; tdee = bmr * 1.375;                // 1842.5, 2533.44
let kcal = Math.round(tdee - Math.min(0.75 * 7700 / 7, tdee * 0.25));       // 825 vs 633.4 -> capped
await want('main', es(kcal), 'deficit target');
await want('tdee', es(Math.round(tdee)), 'deficit maintenance');
await want('deficit', es(Math.round(tdee) - kcal), 'deficit = maintenance − target');
const kgWeek = (Math.round(tdee) - kcal) * 7 / 7700;
await want('kgweek', es(kgWeek, 2), 'deficit kg/week');
await want('weeks', es(Math.ceil(10 / kgWeek)), 'deficit weeks');
n++; if (await page.isHidden(`${R} [data-warn="capped"]`)) bad('deficit: the 25 % cap note is not shown');

// 2b. the floor — woman 60 y, 150 cm, 50 kg, sitting, to 45 kg at 0.75: target under 1,200
await open('/calculadoras/deficit-calorico/', { sex: 'f', age: 60, height: 150, weight: 50, activity: 'sedentary', target: 45, pace: '0.75' });
await want('main', es(1200), 'deficit floor');
n++; if (await page.isHidden(`${R} [data-warn="floor"]`)) bad('deficit: the 1,200 kcal floor note is not shown');

// 3. IMC — 170 cm, 80 kg -> 27.7, overweight, 53–72 kg
await open('/calculadoras/imc/', { height: 170, weight: 80 });
await want('main', es(80 / 1.7 / 1.7, 1), 'BMI value');
await want('lo', es(Math.round(18.5 * 1.7 * 1.7)), 'BMI range low');
await want('hi', es(Math.round(24.9 * 1.7 * 1.7)), 'BMI range high');
n++; const cat = (await page.textContent(`${R} .calc-cat span:not([hidden])`)).trim(); if (cat !== 'Sobrepeso') bad('BMI category: ' + cat);

// 4. proteínas — 80 kg, 175 cm, lose: BMI 26.1 -> reference 25 × 1.75² = 76.56 kg, × 2.0
await open('/calculadoras/proteinas/', { height: 175, weight: 80, goal: 'lose' });
await want('main', es(Math.round(2.0 * 25 * 1.75 * 1.75)), 'protein grams');
await want('efsa', es(Math.round(0.83 * 80)), 'protein recommended minimum');

// 5. macros — woman 35, 170 cm, 70 kg, light, maintain, own 2,000 kcal; pace hidden for "maintain"
await open('/calculadoras/macros/', { sex: 'f', age: 35, height: 170, weight: 70, activity: 'light', goal: 'maintain', kcal: 2000 });
let p = Math.round(1.6 * 70), f = Math.round(0.275 * 2000 / 9), c = Math.round((2000 - 4 * p - 9 * f) / 4);   // 112, 61, 251
await want('p', es(p), 'macros protein'); await want('f', es(f), 'macros fat'); await want('c', es(c), 'macros carbs');
await want('main', es(2000), 'macros kcal');
n++; if (await page.isVisible('.calc-page select[name="pace"]')) bad('macros: pace shown although the goal is "maintain"');
await page.selectOption('.calc-page select[name="goal"]', 'lose');
if (!(await page.isVisible('.calc-page select[name="pace"]'))) bad('macros: pace hidden although the goal is "lose"');

// 6. agua — man 35, 178 cm, 85 kg, moving all day, maintain: kcal × 1.25 × 0.8
await open('/calculadoras/agua/', { sex: 'm', age: 35, height: 178, weight: 85, activity: 'active', goal: 'maintain' });
tdee = (10 * 85 + 6.25 * 178 - 5 * 35 + 5) * 1.55; let ml = Math.round(Math.max(Math.min(Math.round(tdee) * 1.25 * 0.8, 4000), 2000));
await want('ml', es(ml), 'water ml');
await want('glasses', es(Math.ceil(ml / 250)), 'water glasses');
await open('/calculadoras/agua/', { sex: 'f', age: 70, height: 150, weight: 45, activity: 'sedentary', goal: 'lose' });
await want('ml', es(1600), 'water EFSA floor');

// 7. TMB — man 35, 178, 85: the body-fat row hidden; with 20 % fat, Katch-McArdle 370 + 21.6 × 68
await open('/calculadoras/tmb/', { sex: 'm', age: 35, height: 178, weight: 85 });
await want('main', es(Math.round(10 * 85 + 6.25 * 178 - 5 * 35 + 5)), 'BMR Mifflin');
n++; if (await page.isVisible(`${R} [data-out="katch"]`)) bad('TMB: body-fat row shown with no body fat');
await page.fill('.calc-page input[name="bf"]', '20'); await page.waitForTimeout(60);
await want('main', es(Math.round(370 + 21.6 * 68)), 'BMR Katch-McArdle');
if (!(await page.isVisible(`${R} [data-out="katch"]`))) bad('TMB: body-fat row hidden with body fat');

// 8. peso saludable — 180 cm: 60–81 kg; 170 cm and 80 kg: about 8 kg above (80 − 24.9 × 1.7² = 8.04)
await open('/calculadoras/peso-saludable/', { height: 180 });
await want('main', es(Math.round(18.5 * 1.8 * 1.8)) + '–' + es(Math.round(24.9 * 1.8 * 1.8)), 'healthy range');
await open('/calculadoras/peso-saludable/', { height: 170, weight: 80 });
await want('gap', es(Math.round(80 - 24.9 * 1.7 * 1.7)), 'healthy gap from the exact limit');

// 9. URL parameters fill the form and show the result; English formats in English
await page.goto(base + '/en/calculadoras/calorias-diarias/?sex=m&age=35&height=178&weight=85&activity=active');
await page.waitForTimeout(80);
await want('main', en(Math.round((10 * 85 + 6.25 * 178 - 5 * 35 + 5) * 1.55)), 'EN url params + format');
await page.goto(base + '/calculadoras/imc/?peso=80&altura=175');
await page.waitForTimeout(80);
await want('main', es(80 / 1.75 / 1.75, 1), 'ES url params (peso, altura)');

// 10. Calcular writes shareable parameters into the address bar
await open('/calculadoras/imc/', { height: 160, weight: 60 });
n++; const q = new URL(page.url()).searchParams; if (q.get('altura') !== '160' || q.get('peso') !== '60') bad('share URL: ' + page.url());

// 11. the hub's quick BMI tool
await page.goto(base + '/calculadoras/'); await page.fill('.calc-quick input[name="height"]', '170'); await page.fill('.calc-quick input[name="weight"]', '80');
await page.click('.calc-quick .calc-go'); await page.waitForTimeout(60);
n++; const quick = (await page.textContent('.calc-quick [data-out="main"]')).trim(); if (quick !== es(80 / 1.7 / 1.7, 1)) bad('hub quick BMI shows ' + quick);

await browser.close();
console.log(fails ? `calculators: ${fails} problem(s) in ${n} checks` : `calculators: OK, 8 calculators × 2 languages, ${n} checks`);
process.exit(fails ? 1 : 0);
