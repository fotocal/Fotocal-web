// Full-page pictures of the /colabora/ draft, ES and EN, phone and laptop.
import { chromium, devices } from '/opt/node-tools/node_modules/playwright/index.mjs';
const OUT = new URL('../../docs/partners/shots/', import.meta.url).pathname;
const b = await chromium.launch();
for (const [dev, opts] of [['phone', { ...devices['Pixel 7'] }], ['laptop', { viewport: { width: 1366, height: 900 } }]])
  for (const [lang, url] of [['es', 'colabora/'], ['en', 'en/colabora/']]) {
    const p = await (await b.newContext({ ...opts, locale: lang === 'es' ? 'es-ES' : 'en-GB' })).newPage();
    await p.goto(`http://127.0.0.1:8765/${url}`, { waitUntil: 'load' });
    await p.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important}' });
    await p.evaluate(async () => { for (const i of document.images) { i.loading = 'eager'; } await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
    await p.waitForTimeout(500);
    await p.screenshot({ path: `${OUT}colabora-${lang}-${dev}.png`, fullPage: true });
  }
await b.close(); console.log('ok');
