// Renders the JS-built navigation and footer once per language and saves the
// HTML, so tools/build_site.py can inline it into every page: crawlers and
// no-JS visitors then see the same links as everyone else. Run against the
// local server of the built site:  python3 -m http.server 8765  then
// node tools/render_chrome.mjs
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { writeFileSync } from 'node:fs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const browser = await chromium.launch();
const page = await browser.newPage();
for (const [lang, path] of [['es', '/'], ['en', '/en/']]) {
  await page.goto(base + path, { waitUntil: 'load' });
  await page.waitForSelector('#site-nav .nav');
  const out = await page.evaluate((origin) => {
    const abs = (root) => {
      root.querySelectorAll('a[href]').forEach(a => {
        const h = a.getAttribute('href');
        if (h.startsWith('#') || h.startsWith('mailto:')) return;
        const u = new URL(h, location.href);
        a.setAttribute('href', u.origin === origin ? u.pathname + u.search + u.hash : u.href);
      });
      root.querySelectorAll('img[src]').forEach(i => { i.setAttribute('src', new URL(i.getAttribute('src'), location.href).pathname); if (i.getAttribute('srcset')) i.setAttribute('srcset', i.getAttribute('srcset').split(',').map(p => { const [u, d] = p.trim().split(/\s+/); return new URL(u, location.href).pathname + (d ? ' ' + d : ''); }).join(', ')); });
      root.querySelectorAll('.has-section, .is-current, [aria-current]').forEach(e => { e.classList.remove('has-section', 'is-current'); e.removeAttribute('aria-current'); });
      return root.innerHTML;
    };
    return { nav: abs(document.getElementById('site-nav').cloneNode(true)), footer: abs(document.getElementById('site-footer').cloneNode(true)) };
  }, new URL(base).origin);
  writeFileSync(`tools/chrome/nav-${lang}.html`, out.nav);
  writeFileSync(`tools/chrome/footer-${lang}.html`, out.footer);
  console.log(lang, 'nav', out.nav.length, 'footer', out.footer.length, 'links', (out.nav.match(/<a /g)||[]).length + (out.footer.match(/<a /g)||[]).length);
}
await browser.close();
