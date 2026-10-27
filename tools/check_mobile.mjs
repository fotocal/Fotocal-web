// Mobile layout pins: no horizontal scroll, nothing wider than the viewport,
// no tap target under 24×24 CSS px, on one page of every template, at 360 px.
// Needs the built site served locally: python3 -m http.server 8765
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const base = process.env.SITE_BASE || 'http://127.0.0.1:8765';
const SAMPLE = ['/', '/en/', '/features/', '/features/scan-food/', '/en/features/weight-loss/', '/subscription/', '/ai/', '/faq/', '/contact/', '/about/', '/privacy-policy/', '/terms/', '/account-deletion/',
  '/blog/', '/en/blog/', '/blog/how-fast-should-you-lose-weight/', '/blog/calorias-menu-del-dia/', '/blog/series/calories/', '/calorias/', '/calorias/tortilla-de-patatas/', '/calorias/tabla-de-calorias/', '/calculadoras/', '/calculadoras/deficit-calorico/', '/calculadoras/imc/', '/404.html'];
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 360, height: 740 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
let fails = 0;
for (const path of SAMPLE) {
  const page = await ctx.newPage();
  await page.goto(base + path, { waitUntil: 'load' }); await page.waitForTimeout(400);
  const r = await page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const out = { scrollW: document.documentElement.scrollWidth, vw, wide: [], small: [] };
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') continue;
      const b = el.getBoundingClientRect(); if (!b.width) continue;
      if (b.right > vw + 1 && cs.overflowX !== 'hidden' && cs.overflowX !== 'auto' && cs.overflowX !== 'scroll' && !el.closest('[style*="overflow"], .log-track, table, pre, .table-wrap, .lang-menu, .nav-mobile')) out.wide.push(el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : '') + ' right=' + Math.round(b.right));
    }
    for (const el of document.querySelectorAll('a, button, summary, input:not([type=hidden]), select, textarea')) {
      const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const b = el.getBoundingClientRect(); if (!b.width || !b.height) continue;
      if (b.top > window.innerHeight * 6) continue;
      if (b.right < 0 || b.left > vw || el.closest('[aria-hidden="true"]')) continue; // off-screen or hidden on purpose (honeypot decoy)
      const inlineText = cs.display.startsWith('inline') && !el.matches('button, input, select, textarea, summary') && el.closest('p, li, td, th, dd, figcaption, small, .post-lead, .section-sub, .hub-why, blockquote');
      const hiddenCtl = el.matches('input, select, textarea') && (b.width <= 2 || cs.opacity === '0' || cs.clipPath !== 'none' || cs.clip !== 'auto');
      if (!inlineText && !hiddenCtl && (b.width < 24 || b.height < 24) && !el.closest('.nav-mobile, .lang-menu')) out.small.push((el.tagName.toLowerCase()) + '.' + String(el.className).split(' ')[0] + ' ' + Math.round(b.width) + 'x' + Math.round(b.height) + ' "' + (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 25) + '"');
    }
    return out;
  });
  const bad = [];
  if (r.scrollW > r.vw + 1) bad.push(`horizontal scroll: page ${r.scrollW}px wide in a ${r.vw}px viewport`);
  if (r.scrollW > r.vw + 1 && r.wide.length) bad.push('overflowing: ' + [...new Set(r.wide)].slice(0, 5).join(', '));
  if (r.small.length) bad.push('tap targets under 24px: ' + [...new Set(r.small)].slice(0, 6).join(' | '));
  if (bad.length) { fails++; console.log('FAIL', path, '\n   ' + bad.join('\n   ')); }
  await page.close();
}
await browser.close();
console.log(fails ? `mobile: ${fails} page(s) with problems` : `mobile: OK, ${SAMPLE.length} pages at 360px`);
process.exit(fails ? 1 : 0);
