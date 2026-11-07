// The eight calculators must give the app's answers, in both languages.
//
// Every expected number below is worked out by hand from the app's code
// (fotocal/Fotocal src/logic/plan.ts, src/lib/water.ts), written out here
// independently of assets/js/calc.js, and compared with what the page shows
// after typing the inputs. Also checked: the pre-rendered result equals what
// the script computes on load (so nothing changes on first paint), URL
// parameters fill the form, and the English pages use English number format.
//
//   python3 -m http.server 8765 --bind 127.0.0.1   (from the repo root)
//   node tools/check_calcs.mjs
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const browser = await chromium.launch();
const page = await browser.newPage();
let fails = 0, n = 0;

const es = (x, d = 0) => { const [i, f] = Number(x).toFixed(d).split('.'); return i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (f ? ',' + f : ''); };
const en = (x, d = 0) => { const [i, f] = Number(x).toFixed(d).split('.'); return i.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (f ? '.' + f : ''); };
const out = async (key) => (await page.textContent(`.calc-out [data-out="${key}"]`)).trim();
const want = async (key, value, label) => { n++; const got = await out(key); if (got !== value) { fails++; console.log(`FAIL ${label}: ${key} shows ${got}, expected ${value}`); } };
async function open(path, fields = {}) {
  await page.goto(base + path);
  await page.evaluate(() => localStorage.clear());
  await page.goto(base + path);
  for (const [k, v] of Object.entries(fields)) {
    if (k === 'sex') await page.check(`.calc input[name="sex"][value="${v}"]`);
    else if (await page.$(`.calc select[name="${k}"]`)) await page.selectOption(`.calc select[name="${k}"]`, String(v));
    else await page.fill(`.calc input[name="${k}"]`, String(v));
  }
  await page.dispatchEvent('form.calc', 'input');
  await page.waitForTimeout(80);
}

// 0. first paint = script result, every page and language
for (const slug of ['calorias-diarias', 'deficit-calorico', 'imc', 'proteinas', 'macros', 'agua', 'tmb', 'peso-saludable']) {
  for (const pre of ['', '/en']) {
    const r = await fetch(`${base}${pre}/calculadoras/${slug}/`); const html = await r.text();
    const stat = html.match(/<b data-out="main">([^<]*)<\/b>/)[1];
    await page.goto(`${base}${pre}/calculadoras/${slug}/`); await page.evaluate(() => localStorage.clear()); await page.reload();
    n++; const live = await out('main'); if (live !== stat) { fails++; console.log(`FAIL ${pre}/${slug}: pre-rendered ${stat}, script ${live}`); }
  }
}

// 1. calorías diarias — woman 40 y, 165 cm, 70 kg, "moving all day" (1.55)
await open('/calculadoras/calorias-diarias/', { sex: 'f', age: 40, height: 165, weight: 70, activity: 'active' });
let bmr = 10 * 70 + 6.25 * 165 - 5 * 40 - 161, tdee = bmr * 1.55;           // 1370.25, 2123.89
await want('main', es(Math.round(tdee)), 'tdee maintenance');
await want('bmr', es(Math.round(bmr)), 'tdee BMR');
await want('lose50', es(Math.round(Math.floor(tdee - Math.min(550, tdee * 0.25)))), 'tdee lose 0.5');   // 550 < 531? no: cap 25 %
await want('lose25', es(Math.floor(tdee - 275)), 'tdee lose 0.25');
await want('gain25', es(Math.round(tdee + 275)), 'tdee gain 0.25');

// 2. déficit — man 35 y, 178 cm, 90 kg, light (1.375), to 80 kg at 0.75 kg/week
await open('/calculadoras/deficit-calorico/', { sex: 'm', age: 35, height: 178, weight: 90, activity: 'light', target: 80, pace: '0.75' });
bmr = 10 * 90 + 6.25 * 178 - 5 * 35 + 5; tdee = bmr * 1.375;                // 1842.5, 2533.44
let deficit = Math.min(0.75 * 7700 / 7, tdee * 0.25);                        // 825 vs 633.4 -> capped
let kcal = Math.floor(tdee - deficit);
await want('main', es(kcal), 'deficit target');
await want('tdee', es(Math.round(tdee)), 'deficit maintenance');
const kgWeek = (tdee - kcal) * 7 / 7700;
await want('kgweek', es(kgWeek, 2), 'deficit kg/week');
await want('weeks', es(Math.ceil(10 / kgWeek)), 'deficit weeks');
n++; if (await page.isHidden('[data-warn="capped"]')) { fails++; console.log('FAIL deficit: the 25 % cap warning is not shown'); }

// 2b. the floor — woman 60 y, 150 cm, 50 kg, sitting, to 45 kg at 0.75: target under 1,200
await open('/calculadoras/deficit-calorico/', { sex: 'f', age: 60, height: 150, weight: 50, activity: 'sedentary', target: 45, pace: '0.75' });
await want('main', es(1200), 'deficit floor');
n++; if (await page.isHidden('[data-warn="floor"]')) { fails++; console.log('FAIL deficit: the 1,200 kcal floor warning is not shown'); }

// 3. IMC — 170 cm, 80 kg -> 27.7, overweight, 53–72 kg
await open('/calculadoras/imc/', { height: 170, weight: 80 });
await want('main', es(80 / 1.7 / 1.7, 1), 'BMI value');
await want('lo', es(Math.round(18.5 * 1.7 * 1.7)), 'BMI range low');
await want('hi', es(Math.round(24.9 * 1.7 * 1.7)), 'BMI range high');
n++; const cat = (await page.textContent('.calc-cat span:not([hidden])')).trim(); if (cat !== 'Sobrepeso') { fails++; console.log('FAIL BMI category: ' + cat); }

// 4. proteínas — 80 kg, 175 cm, lose: BMI 26.1 -> reference 25 × 1.75² = 76.56 kg, × 2.0
await open('/calculadoras/proteinas/', { height: 175, weight: 80, goal: 'lose' });
await want('main', es(Math.round(2.0 * 25 * 1.75 * 1.75)), 'protein grams');
await want('efsa', es(Math.round(0.83 * 80)), 'protein EFSA minimum');

// 5. macros — woman 35, 170 cm, 70 kg, light, maintain, own 2,000 kcal
await open('/calculadoras/macros/', { sex: 'f', age: 35, height: 170, weight: 70, activity: 'light', goal: 'maintain', kcal: 2000 });
let p = Math.round(1.6 * 70 * 4 / 4), f = Math.round(0.275 * 2000 / 9), c = Math.round((2000 - 4 * p - 9 * f) / 4);   // 112, 61, 251
await want('p', es(p), 'macros protein'); await want('f', es(f), 'macros fat'); await want('c', es(c), 'macros carbs');
await want('main', es(2000), 'macros kcal');

// 6. agua — man 35, 178 cm, 85 kg, moving all day, maintain: kcal × 1.25 × 0.8
await open('/calculadoras/agua/', { sex: 'm', age: 35, height: 178, weight: 85, activity: 'active', goal: 'maintain' });
tdee = (10 * 85 + 6.25 * 178 - 5 * 35 + 5) * 1.55; let ml = Math.round(Math.max(Math.min(Math.round(tdee) * 1.25 * 0.8, 4000), 2000));
await want('ml', es(ml), 'water ml');
await want('glasses', es(Math.ceil(ml / 250)), 'water glasses');
// 6b. the EFSA floor: woman 70 y, 150 cm, 45 kg, sitting, losing -> 1,600 ml
await open('/calculadoras/agua/', { sex: 'f', age: 70, height: 150, weight: 45, activity: 'sedentary', goal: 'lose' });
await want('ml', es(1600), 'water EFSA floor');

// 7. TMB — man 35, 178, 85, then with 20 % body fat (Katch-McArdle 370 + 21.6 × 68)
await open('/calculadoras/tmb/', { sex: 'm', age: 35, height: 178, weight: 85 });
await want('main', es(Math.round(10 * 85 + 6.25 * 178 - 5 * 35 + 5)), 'BMR Mifflin');
await page.fill('.calc input[name="bf"]', '20'); await page.dispatchEvent('form.calc', 'input'); await page.waitForTimeout(80);
await want('main', es(Math.round(370 + 21.6 * 68)), 'BMR Katch-McArdle');

// 8. peso saludable — 180 cm: 60–81 kg
await open('/calculadoras/peso-saludable/', { height: 180, weight: '' });
await want('main', es(Math.round(18.5 * 1.8 * 1.8)) + '–' + es(Math.round(24.9 * 1.8 * 1.8)), 'healthy range');

// 9. URL parameters fill the form, and English formats numbers in English
await page.goto(base + '/en/calculadoras/calorias-diarias/?sex=m&age=35&height=178&weight=85&activity=active');
await page.waitForTimeout(80);
await want('main', en(Math.round((10 * 85 + 6.25 * 178 - 5 * 35 + 5) * 1.55)), 'EN url params + format');
await page.goto(base + '/calculadoras/imc/?peso=80&altura=175');
await page.waitForTimeout(80);
await want('main', es(80 / 1.75 / 1.75, 1), 'ES url params (peso, altura)');

// 10. typing updates the address bar with shareable parameters
await open('/calculadoras/imc/', { height: 160, weight: 60 });
n++; const q = new URL(page.url()).searchParams; if (q.get('altura') !== '160' || q.get('peso') !== '60') { fails++; console.log('FAIL share URL: ' + page.url()); }

await browser.close();
console.log(fails ? `calculators: ${fails} wrong answer(s) of ${n}` : `calculators: OK, 8 calculators × 2 languages, ${n} values`);
process.exit(fails ? 1 : 0);
