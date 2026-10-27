// The contact form must still submit: fill it, intercept the request to
// Web3Forms (never sent for real), check the payload and that the success
// banner appears; then check the honeypot path sends nothing.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const browser = await chromium.launch(); let fails = 0;
for (const path of ['/contact/', '/en/contact/']) {
  const page = await browser.newPage(); let posted = null;
  await page.route('https://api.web3forms.com/submit', async route => { posted = JSON.parse(route.request().postData() || '{}'); await route.fulfill({ status: 200, contentType: 'application/json', body: '{"success":true}' }); });
  await page.goto(base + path, { waitUntil: 'load' });
  await page.fill('#cfName', 'Prueba'); await page.fill('#cfEmail', 'prueba@example.com'); await page.fill('#cfMessage', 'Mensaje de prueba del checker, diez palabras o más para pasar.');
  await page.waitForTimeout(4200); // the time gate
  await page.click('#cfSubmit'); await page.waitForTimeout(600);
  const ok = await page.$eval('#cfOk', e => e.classList.contains('show') && e.textContent.trim().length > 0).catch(() => false);
  if (!posted) { fails++; console.log('FAIL', path, 'no request reached Web3Forms'); }
  else { for (const k of ['access_key', 'name', 'email', 'message', 'subject']) if (!posted[k]) { fails++; console.log('FAIL', path, 'payload missing', k); } if ('botcheck' in posted || 'botcheck_text' in posted) { fails++; console.log('FAIL', path, 'honeypot fields leaked into the payload'); } }
  if (!ok) { fails++; console.log('FAIL', path, 'success banner not shown'); }
  // honeypot: a filled decoy must send nothing and still show the quiet success
  posted = null; await page.reload({ waitUntil: 'load' });
  await page.fill('#cfName', 'Bot'); await page.fill('#cfEmail', 'bot@example.com'); await page.fill('#cfMessage', 'Spam spam spam spam spam spam spam spam spam.');
  await page.evaluate(() => { document.querySelector('input[name="botcheck_text"]').value = 'filled'; }); await page.waitForTimeout(4200); await page.click('#cfSubmit'); await page.waitForTimeout(400);
  if (posted) { fails++; console.log('FAIL', path, 'honeypot submission was sent'); }
  await page.close();
}
await browser.close(); console.log(fails ? `contact form: ${fails} problem(s)` : 'contact form: OK, both languages, honeypot blocks'); process.exit(fails ? 1 : 0);
