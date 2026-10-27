// The four calculators must give the right answers. Each case is computed
// here with the published formulas (Mifflin-St Jeor, 7,700 kcal per kg,
// 4/4/9 kcal per gram) and compared with what the page shows.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const tick = async (sel) => page.$eval(sel, e => { e.checked = true; e.dispatchEvent(new Event('change', { bubbles: true })); e.dispatchEvent(new Event('input', { bubbles: true })); });
const fmt = (x, d = 0) => { const s = Number(x).toFixed(d); const [i, f] = s.split('.'); return i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (f ? ',' + f : ''); };
const mifflin = (sex, age, h, w) => 10 * w + 6.25 * h - 5 * age + (sex === 'm' ? 5 : -161);
const browser = await chromium.launch(); const page = await browser.newPage(); let fails = 0;
const expect = async (id, want, label) => { const got = (await page.textContent('#' + id)).trim(); if (got !== want) { fails++; console.log(`FAIL ${label}: #${id} shows ${got}, expected ${want}`); } };
// 1. calorías diarias: woman 40 y, 165 cm, 70 kg, activity 1.55
await page.goto(base + '/calculadoras/calorias-diarias/'); await page.evaluate(() => localStorage.clear());
await tick('#sex-f'); await page.fill('#age', '40'); await page.fill('#height', '165'); await page.fill('#weight', '70'); await page.selectOption('#activity', '1.55'); await page.dispatchEvent('#weight', 'input'); await page.waitForTimeout(200);
let bmr = mifflin('f', 40, 165, 70), tdee = bmr * 1.55;
await expect('r-bmr', fmt(bmr), 'tdee page BMR'); await expect('r-tdee', fmt(tdee), 'tdee page TDEE'); await expect('r-lose50', fmt(tdee - 550), 'tdee page -550');
// 2. déficit: man 35 y, 178 cm, 90 kg, activity 1.375, goal 10 kg, rate 0.75 %/week
await page.goto(base + '/calculadoras/deficit-calorico/'); await page.evaluate(() => localStorage.clear());
await tick('#sex-m'); await page.fill('#age', '35'); await page.fill('#height', '178'); await page.fill('#weight', '90'); await page.selectOption('#activity', '1.375'); await page.fill('#goal', '10');
const rateVals = await page.$$eval('input[name="rate"]', els => els.map(e => e.value)); const rate = rateVals.includes('0.75') ? '0.75' : rateVals[1] || rateVals[0];
await tick(`input[name="rate"][value="${rate}"]`); await page.dispatchEvent('#goal', 'input'); await page.waitForTimeout(200);
bmr = mifflin('m', 35, 178, 90); tdee = bmr * 1.375; const weekly = 90 * parseFloat(rate) / 100, deficit = weekly * 7700 / 7;
await expect('r-tdee', fmt(tdee), 'deficit TDEE'); await expect('r-deficit', fmt(deficit), 'deficit kcal/day'); await expect('r-target', fmt(tdee - deficit), 'deficit target'); await expect('r-weekly', fmt(weekly, 2), 'deficit kg/week'); await expect('r-weeks', fmt(10 / weekly, 0), 'deficit weeks');
// 3. IMC: 170 cm, 80 kg -> 27.7 sobrepeso
await page.goto(base + '/calculadoras/imc/'); await page.evaluate(() => localStorage.clear());
await page.fill('#height', '170'); await page.fill('#weight', '80'); await page.dispatchEvent('#weight', 'input'); await page.waitForTimeout(200);
await expect('r-bmi', fmt(80 / 1.7 / 1.7, 1), 'IMC value'); await expect('r-cat', 'Sobrepeso', 'IMC category'); await expect('r-lo', fmt(18.5 * 1.7 * 1.7, 1), 'IMC low'); await expect('r-hi', fmt(24.9 * 1.7 * 1.7, 1), 'IMC high');
// 4. macros: 2000 kcal, 70 kg, protein g/kg from the select, fat % from the select
await page.goto(base + '/calculadoras/macros/'); await page.evaluate(() => localStorage.clear());
await page.fill('#kcal', '2000'); await page.fill('#weight', '70');
const gkg = parseFloat(await page.$eval('select[name="protein"]', e => e.value)), fatPct = parseFloat(await page.$eval('select[name="fat"]', e => e.value));
await page.dispatchEvent('#weight', 'input'); await page.waitForTimeout(200);
const pG = 70 * gkg, pK = pG * 4, fK = 2000 * fatPct / 100, fG = fK / 9, cK = 2000 - pK - fK;
await expect('r-p', fmt(pG), 'macros protein g'); await expect('r-f', fmt(fG), 'macros fat g'); await expect('r-c', fmt(cK / 4), 'macros carbs g'); await expect('r-ck', fmt(cK), 'macros carbs kcal');
await browser.close(); console.log(fails ? `calculators: ${fails} wrong answer(s)` : 'calculators: OK, 4 calculators, 16 values'); process.exit(fails ? 1 : 0);
