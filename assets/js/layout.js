/* ═══════════════════════════════════════════════════════════════
   FOTOCAL — shared layout: navbar + footer + screenshot slots
   ───────────────────────────────────────────────────────────────
   HOW THIS WORKS (read this before adding a new page)

   This is a no-build static site, so the nav and footer are defined
   ONCE here and injected by JS. A page only needs:

     <div id="site-nav"></div>          <- nav is injected here
     <main id="main"> ... </main>
     <div id="site-footer"></div>       <- footer is injected here

     <script src="assets/js/i18n.js"></script>
     <script src="assets/js/layout.js" data-page="home"></script>
     <script src="assets/js/main.js"></script>

   data-page marks the active nav item (home | features | blog |
   subscription | about). Use the SAME relative depth for the script
   src as the page's depth — BASE below is derived from this script's
   own URL, so nested pages (e.g. /features/weight-loss/) resolve all
   links correctly with no hard-coded absolute paths.

   WHY JS INCLUDE instead of duplicating markup in 8 files:
   the site already requires JS for the ES/EN toggle, so JS is a hard
   dependency regardless. One source of truth means a nav change is a
   one-file edit rather than an 8-file edit. Trade-off accepted: the
   nav is not in the initial HTML for crawlers, so every page ALSO
   carries real <a> links to key routes inside its own <main> content
   and in the page source, and each page has proper <title>/<meta>.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  document.documentElement.classList.remove("no-js");

  /* ── Resolve site base from this script's own src ──
     assets/js/layout.js  ->  strip 3 segments  ->  site root.
     Works on GitHub Pages (/Fotocal-web/) and at a domain root. */
  var me = document.currentScript ||
           (function () { var s = document.getElementsByTagName("script"); return s[s.length - 1]; })();
  var BASE = me.src.replace(/assets\/js\/layout\.js.*$/, "");
  var PAGE = me.getAttribute("data-page") || "";

  var PLAY_URL = "https://play.google.com/store/apps/details?id=com.fotokal.app";
  var IG_URL   = "https://www.instagram.com/fotocal_app?igsh=MWRvNGRkMXMwNmZicw==";
  /* Official support address — taken from the existing Google Play
     compliance pages (privacy-policy / terms / account-deletion).
     Do not change without changing those too. */
  var SUPPORT  = "esmarketstop@gmail.com";

  var u = function (p) { return BASE + p; };

  /* ── Nav model — single source of truth ── */
  var NAV = [
    { id: "home",         key: "nav.home",         href: u("") },
    { id: "features",     key: "nav.features",     children: [
        { key: "nav.weightLoss",   href: u("features/weight-loss/") },
        { key: "nav.nutrition",    href: u("features/nutrition-diet/") },
        { key: "nav.lifestyle",    href: u("features/lifestyle-mindset/") }
      ] },
    { id: "blog",         key: "nav.blog",         href: u("blog/") },
    { id: "subscription", key: "nav.subscription", href: u("subscription/") },
    { id: "about",        key: "nav.about",        children: [
        { key: "nav.aboutUs",   href: u("about/") },
        { key: "nav.contactUs", href: u("contact/") }
      ] }
  ];

  var CARET = '<svg class="nav-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';

  var PLAY_SVG = '<svg viewBox="0 0 32 34" class="play-badge-icon" aria-hidden="true">' +
    '<path d="M2.6 1.2C1.9 1.9 1.5 3 1.5 4.4v25.2c0 1.4.4 2.5 1.1 3.2l.2.2 14.1-14.1v-.6L2.8 1l-.2.2z" fill="#00D7FE"/>' +
    '<path d="M21.6 21.6l-4.7-4.7v-.6l4.7-4.7.1.1 5.6 3.2c1.6.9 1.6 2.4 0 3.3l-5.6 3.2-.1.2z" fill="#FFCE00"/>' +
    '<path d="M21.7 21.5L16.9 16.7 2.6 31 2.6 31c.5.6 1.4.6 2.4.1l16.7-9.6" fill="#FF3A44"/>' +
    '<path d="M21.7 12.1L5 2.5C4 1.9 3.1 2 2.6 2.6l14.3 14.1 4.8-4.6z" fill="#00F076"/></svg>';

  /* ── Logo ──
     NOTE: the official Fotocal app icon has not been added to the repo yet.
     When it lands at assets/img/logo.png this markup picks it up
     automatically — the <img> is tried first and the inline SVG below is
     only shown if that file 404s. Swapping the logo = dropping in one file. */
  function logoHTML(href) {
    return '<a class="nav-logo" href="' + href + '" aria-label="Fotocal — ' +
      'home">' +
      '<img class="logo-mark is-tile" src="' + u("assets/img/logo.png") + '" alt="" ' +
        'width="32" height="32" data-logo-img hidden>' +
      '<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true" data-logo-fallback>' +
        '<defs><linearGradient id="fcLogoG" x1="0" y1="0" x2="1" y2="1">' +
          '<stop offset="0" stop-color="#E91E63"/><stop offset="1" stop-color="#FF7A3D"/>' +
        '</linearGradient></defs>' +
        '<path d="M24 12c-7-5-16-1.5-16 9 0 9 7 19 13 19 1.6 0 2.2-.9 3-.9s1.4.9 3 .9c6 0 13-10 13-19 0-10.5-9-14-16-9z" fill="url(#fcLogoG)"/>' +
        '<path d="M24 12c0-5 3.5-8 8-8 0 5-3.5 8-8 8z" fill="#3FA37A"/>' +
        '<circle cx="24" cy="27" r="7.5" fill="none" stroke="#FDF9F0" stroke-width="2.6"/>' +
        '<circle cx="24" cy="27" r="2.6" fill="#FDF9F0"/>' +
      '</svg>' +
      '<span>Fotocal</span></a>';
  }

  /* ── Build navbar ── */
  function navHTML() {
    var desktop = "", mobile = "";

    NAV.forEach(function (item, i) {
      var active = item.id === PAGE;
      var cur = active ? ' aria-current="page"' : "";

      if (!item.children) {
        desktop += '<li class="nav-item"><a class="nav-link" href="' + item.href + '"' + cur +
                   ' data-i18n="' + item.key + '"></a></li>';
        mobile  += '<li class="m-item"><a class="m-link" href="' + item.href + '"' + cur +
                   ' data-i18n="' + item.key + '"></a></li>';
        return;
      }

      var pid = "nav-panel-" + item.id;
      var mid = "m-panel-" + item.id;

      var links = item.children.map(function (c) {
        return '<li><a href="' + c.href + '" data-i18n="' + c.key + '"></a></li>';
      }).join("");

      desktop += '<li class="nav-item" data-dropdown>' +
        '<button class="nav-link" type="button" aria-expanded="false" aria-haspopup="true" ' +
          'aria-controls="' + pid + '"' + (active ? ' aria-current="page"' : "") + '>' +
          '<span data-i18n="' + item.key + '"></span>' + CARET +
        '</button>' +
        '<ul class="nav-panel" id="' + pid + '">' + links + '</ul>' +
        '</li>';

      mobile += '<li class="m-item" data-dropdown>' +
        '<button class="m-link" type="button" aria-expanded="false" aria-controls="' + mid + '">' +
          '<span data-i18n="' + item.key + '"></span>' + CARET +
        '</button>' +
        '<div class="m-panel" id="' + mid + '"><div class="m-panel-inner"><ul>' + links + '</ul></div></div>' +
        '</li>';
    });

    return '' +
      '<a class="skip-link" href="#main" data-i18n="nav.skip"></a>' +
      '<div class="nav-wrap" id="navWrap">' +
        '<nav class="container nav" aria-label="Main">' +
          logoHTML(u("")) +
          '<ul class="nav-links">' + desktop + '</ul>' +
          '<div class="nav-actions">' +
            '<button class="lang-toggle" id="langToggle" type="button" ' +
              'aria-label="Change language / Cambiar idioma">' +
              '<span class="lang-opt" data-lang="en">EN</span>' +
              '<span class="lang-sep">/</span>' +
              '<span class="lang-opt" data-lang="es">ES</span>' +
            '</button>' +
            '<a class="btn btn-cta btn-sm btn-nav" href="' + PLAY_URL + '" target="_blank" rel="noopener" ' +
              'data-i18n="nav.cta"></a>' +
            '<button class="nav-burger" id="navBurger" type="button" aria-expanded="false" ' +
              'aria-controls="navMobile" aria-label="Menu">' +
              '<span></span><span></span><span></span>' +
            '</button>' +
          '</div>' +
        '</nav>' +
      '</div>' +
      '<div class="nav-mobile" id="navMobile">' +
        '<ul>' + mobile + '</ul>' +
        '<a class="play-badge" href="' + PLAY_URL + '" target="_blank" rel="noopener">' +
          PLAY_SVG +
          '<span class="play-badge-text"><small data-i18n="cta.badgeTop"></small><strong>Google Play</strong></span>' +
        '</a>' +
      '</div>';
  }

  /* ── Build footer ── */
  function footerHTML() {
    var year = new Date().getFullYear();
    return '' +
      '<footer class="footer">' +
        '<div class="container footer-grid">' +
          '<div class="footer-brand">' +
            logoHTML(u("")) +
            '<p data-i18n="footer.tag"></p>' +
            '<div class="footer-social">' +
              '<a href="' + IG_URL + '" target="_blank" rel="noopener" aria-label="Instagram">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">' +
                '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/>' +
                '<circle cx="17.3" cy="6.7" r="1.2" fill="currentColor" stroke="none"/></svg></a>' +
              '<a href="mailto:' + SUPPORT + '" aria-label="Email">' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">' +
                '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7l8.5 6 8.5-6"/></svg></a>' +
            '</div>' +
          '</div>' +
          '<div class="footer-col">' +
            '<h5 data-i18n="footer.product"></h5>' +
            '<a href="' + u("") + '" data-i18n="nav.home"></a>' +
            '<a href="' + u("subscription/") + '" data-i18n="nav.subscription"></a>' +
            '<a href="' + u("blog/") + '" data-i18n="nav.blog"></a>' +
            '<a href="' + PLAY_URL + '" target="_blank" rel="noopener">Google Play</a>' +
          '</div>' +
          '<div class="footer-col">' +
            '<h5 data-i18n="nav.features"></h5>' +
            '<a href="' + u("features/weight-loss/") + '" data-i18n="nav.weightLoss"></a>' +
            '<a href="' + u("features/nutrition-diet/") + '" data-i18n="nav.nutrition"></a>' +
            '<a href="' + u("features/lifestyle-mindset/") + '" data-i18n="nav.lifestyle"></a>' +
          '</div>' +
          '<div class="footer-col">' +
            '<h5 data-i18n="footer.company"></h5>' +
            '<a href="' + u("about/") + '" data-i18n="nav.aboutUs"></a>' +
            '<a href="' + u("contact/") + '" data-i18n="nav.contactUs"></a>' +
            '<a href="' + u("privacy-policy/") + '" data-i18n="footer.privacy"></a>' +
            '<a href="' + u("terms/") + '" data-i18n="footer.terms"></a>' +
            '<a href="' + u("account-deletion/") + '" data-i18n="footer.deletion"></a>' +
          '</div>' +
        '</div>' +
        '<div class="container footer-bottom">' +
          '<p>&copy; ' + year + ' Fotocal &middot; <span data-i18n="footer.rights"></span></p>' +
          '<p data-i18n="footer.made"></p>' +
        '</div>' +
      '</footer>';
  }

  /* ── Inject ── */
  var navMount = document.getElementById("site-nav");
  var footMount = document.getElementById("site-footer");
  if (navMount) navMount.innerHTML = navHTML();
  if (footMount) footMount.innerHTML = footerHTML();

  /* ── Logo: prefer the real PNG, fall back to inline SVG ── */
  (function () {
    document.querySelectorAll("[data-logo-img]").forEach(function (img) {
      var svg = img.parentNode.querySelector("[data-logo-fallback]");
      var probe = new Image();
      probe.onload = function () { img.hidden = false; if (svg) svg.remove(); };
      probe.onerror = function () { img.remove(); };
      probe.src = img.src;
    });
  })();

  /* ═══════════ Dropdowns — desktop (click) + mobile (accordion) ═══════════
     Click, not hover: matches the pattern used across this category, and is
     the only thing that works on touch. Hover-intent is added on top for
     pointer devices as a convenience, not as the primary mechanism. */

  function closeAll(except) {
    document.querySelectorAll("[data-dropdown].open").forEach(function (d) {
      if (d === except) return;
      d.classList.remove("open");
      var b = d.querySelector("button");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  }

  function toggle(item, force) {
    var btn = item.querySelector("button");
    var open = force != null ? force : !item.classList.contains("open");
    if (open) closeAll(item);
    item.classList.toggle("open", open);
    if (btn) btn.setAttribute("aria-expanded", String(open));
    return open;
  }

  document.querySelectorAll("[data-dropdown]").forEach(function (item) {
    var btn = item.querySelector("button");
    if (!btn) return;

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      toggle(item);
    });

    /* Keyboard: Down opens and moves into the panel; Esc closes. */
    btn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        toggle(item, true);
        var first = item.querySelector("a");
        if (first) first.focus();
      } else if (e.key === "Escape") {
        toggle(item, false);
      }
    });

    item.addEventListener("keydown", function (e) {
      var links = [].slice.call(item.querySelectorAll("a"));
      var i = links.indexOf(document.activeElement);
      if (e.key === "Escape") {
        e.preventDefault();
        toggle(item, false);
        btn.focus();
      } else if (e.key === "ArrowDown" && i > -1) {
        e.preventDefault();
        (links[i + 1] || links[0]).focus();
      } else if (e.key === "ArrowUp" && i > -1) {
        e.preventDefault();
        if (i === 0) { btn.focus(); } else { links[i - 1].focus(); }
      }
    });

    /* Close when focus leaves the whole item (keyboard tab-out). */
    item.addEventListener("focusout", function () {
      setTimeout(function () {
        if (!item.contains(document.activeElement)) toggle(item, false);
      }, 0);
    });

    /* NOTE: deliberately click-only — no hover-to-open.
       A hover handler here fights the click handler (hover opens the panel,
       then the click that follows immediately toggles it shut, so the menu
       looks broken on desktop). Click-only is also what every comparable
       app-marketing site in this category does, and it is the only thing
       that behaves correctly on touch. Do not add mouseenter/mouseleave. */
  });

  document.addEventListener("click", function () { closeAll(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeAll(); });

  /* ═══════════ Mobile drawer ═══════════ */
  var burger = document.getElementById("navBurger");
  var drawer = document.getElementById("navMobile");
  if (burger && drawer) {
    burger.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !drawer.classList.contains("open");
      drawer.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-locked", open);
      if (!open) closeAll();
    });
    drawer.addEventListener("click", function (e) { e.stopPropagation(); });
    drawer.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        drawer.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-locked");
      });
    });
    /* Close the drawer if the viewport grows into desktop layout. */
    window.matchMedia("(min-width: 900px)").addEventListener("change", function (ev) {
      if (ev.matches) {
        drawer.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-locked");
      }
    });
  }

  /* ═══════════ Navbar scrolled state ═══════════ */
  var navWrap = document.getElementById("navWrap");
  var onScroll = function () {
    if (navWrap) navWrap.classList.toggle("scrolled", window.scrollY > 8);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ═══════════ Screenshot slots ═══════════
     Every phone screen in the markup is a .screen-slot with data-src +
     data-label. We try to load data-src; if the real screenshot exists it
     replaces the placeholder, otherwise the labelled placeholder stays.
     => never a broken-image icon, and adding the PNG is the only step
        needed to go live with real screens. */
  var CAMERA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>';

  document.querySelectorAll(".screen-slot").forEach(function (slot) {
    var src = slot.getAttribute("data-src");
    var label = slot.getAttribute("data-label") || "";

    /* Paint the placeholder immediately. */
    slot.innerHTML =
      '<div class="slot-icon">' + CAMERA + '</div>' +
      '<div class="slot-label">' + label + '</div>' +
      '<div class="slot-note" data-i18n="slot.pending"></div>' +
      '<div class="slot-path">' + (src || "").replace(BASE, "") + '</div>';

    if (!src) return;
    var img = new Image();
    img.onload = function () {
      var el = document.createElement("img");
      el.src = src;
      el.alt = label;
      el.loading = "lazy";
      el.decoding = "async";
      slot.replaceWith(el);
    };
    img.src = src;
  });
})();
