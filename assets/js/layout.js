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
  /* The four official Fotocal accounts. These are the only social links on
     the site; every one opens in a new tab. */
  var FB_URL     = "https://www.facebook.com/share/1HbMUZSBJ6/";
  var IG_URL     = "https://www.instagram.com/getfotocal";
  var YT_URL     = "https://youtube.com/@getfotocal";
  var TIKTOK_URL = "https://www.tiktok.com/@getfotocal.com";

  var u = function (p) { return BASE + p; };

  /* ── Nav model — single source of truth ──
     Three shapes are supported:
       href only                 -> plain link
       children only             -> button that opens a panel
       href AND children (split) -> the label is a real link, and a
                                    separate caret button opens the panel

     Features is the split kind on purpose. It has its own overview page
     that people ask for by name, so clicking the word must go there —
     but it now also fronts four dedicated pages, and burying those
     behind a page visit would hide them. A label-that-navigates plus a
     caret-that-discloses is the only arrangement that serves both, and
     it keeps the caret a real button with its own aria-expanded. */
  var NAV = [
    { id: "home",         key: "nav.home",         href: u("") },
    { id: "features",     key: "nav.features",     href: u("features/"), children: [
        { key: "nav.allFeatures",  href: u("features/") },
        { key: "nav.scanFood",     href: u("features/scan-food/") },
        { key: "nav.scanBarcode",  href: u("features/scan-barcode/") },
        { key: "nav.voiceLogging", href: u("features/voice-logging/") },
        { key: "nav.recipe",       href: u("features/recipe/") }
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
    return '<a class="nav-logo" href="' + href + '" aria-label="Fotocal — home">' +
      '<img class="logo-mark is-tile" src="' + u("assets/img/logo.png") + '" alt="" width="32" height="32">' +
      '<span>Fotocal</span></a>';
  }

  /* ── Build navbar ── */
  function navHTML() {
    var desktop = "", mobile = "";

    NAV.forEach(function (item) {
      /* data-page marks the SECTION, not the page. On /features/scan-food/
         it is still "features", so it must NOT become aria-current="page" —
         that would claim the visitor is on the overview when they are not.
         The section gets a class here; the exact page is resolved from the
         real URL in markCurrent() after injection. */
      var sec  = item.id === PAGE ? " has-section" : "";

      if (!item.children) {
        desktop += '<li class="nav-item' + sec + '"><a class="nav-link" href="' + item.href +
                   '" data-i18n="' + item.key + '"></a></li>';
        mobile  += '<li class="m-item' + sec + '"><a class="m-link" href="' + item.href +
                   '" data-i18n="' + item.key + '"></a></li>';
        return;
      }

      var pid = "nav-panel-" + item.id;
      var mid = "m-panel-" + item.id;

      var links = item.children.map(function (c) {
        return '<li><a href="' + c.href + '" data-i18n="' + c.key + '"></a></li>';
      }).join("");

      var caretBtn = function (cls, id) {
        return '<button class="' + cls + '" type="button" aria-expanded="false" ' +
               'aria-haspopup="true" aria-controls="' + id + '" ' +
               'data-i18n-aria="nav.moreIn">' + CARET + '</button>';
      };

      /* Split: label navigates, caret discloses. */
      if (item.href) {
        desktop += '<li class="nav-item nav-split' + sec + '" data-dropdown>' +
          '<a class="nav-link" href="' + item.href + '" data-i18n="' + item.key + '"></a>' +
          caretBtn("nav-caret-btn", pid) +
          '<ul class="nav-panel" id="' + pid + '">' + links + '</ul>' +
          '</li>';

        mobile += '<li class="m-item m-split' + sec + '" data-dropdown>' +
          '<div class="m-split-row">' +
            '<a class="m-link" href="' + item.href + '" data-i18n="' + item.key + '"></a>' +
            caretBtn("m-caret-btn", mid) +
          '</div>' +
          '<div class="m-panel" id="' + mid + '"><div class="m-panel-inner"><ul>' + links + '</ul></div></div>' +
          '</li>';
        return;
      }

      desktop += '<li class="nav-item' + sec + '" data-dropdown>' +
        '<button class="nav-link" type="button" aria-expanded="false" aria-haspopup="true" ' +
          'aria-controls="' + pid + '">' +
          '<span data-i18n="' + item.key + '"></span>' + CARET +
        '</button>' +
        '<ul class="nav-panel" id="' + pid + '">' + links + '</ul>' +
        '</li>';

      mobile += '<li class="m-item' + sec + '" data-dropdown>' +
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
            /* Solid brand glyphs so each platform is recognisable at 18px.
               rel="noopener noreferrer" on every one: noopener severs the
               window.opener link, noreferrer withholds the referrer. */
            '<div class="footer-social">' +
              '<a href="' + FB_URL + '" target="_blank" rel="noopener noreferrer" aria-label="Fotocal on Facebook">' +
                '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
                '<path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg></a>' +
              '<a href="' + IG_URL + '" target="_blank" rel="noopener noreferrer" aria-label="Fotocal on Instagram">' +
                '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
                '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07zM12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63c-.79.3-1.46.72-2.13 1.38C1.35 2.68.93 3.35.63 4.14.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.3.79.72 1.46 1.38 2.13.67.66 1.34 1.08 2.13 1.38.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56.79-.3 1.46-.72 2.13-1.38.66-.67 1.08-1.34 1.38-2.13.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91-.3-.79-.72-1.46-1.38-2.13C21.32 1.35 20.65.93 19.86.63 19.1.33 18.22.13 16.95.07 15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 100 12.32 6.16 6.16 0 000-12.32zM12 16a4 4 0 110-8 4 4 0 010 8zm7.85-10.4a1.44 1.44 0 11-2.88 0 1.44 1.44 0 012.88 0z"/></svg></a>' +
              '<a href="' + YT_URL + '" target="_blank" rel="noopener noreferrer" aria-label="Fotocal on YouTube">' +
                '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
                '<path d="M23.5 6.19a3.02 3.02 0 00-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 00.5 6.19C0 8.07 0 12 0 12s0 3.93.5 5.81a3.02 3.02 0 002.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 002.12-2.14C24 15.93 24 12 24 12s0-3.93-.5-5.81zM9.55 15.57V8.43L15.82 12l-6.27 3.57z"/></svg></a>' +
              '<a href="' + TIKTOK_URL + '" target="_blank" rel="noopener noreferrer" aria-label="Fotocal on TikTok">' +
                '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
                '<path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a>' +
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
            '<a href="' + u("features/") + '" data-i18n="nav.allFeatures"></a>' +
            '<a href="' + u("features/scan-food/") + '" data-i18n="nav.scanFood"></a>' +
            '<a href="' + u("features/scan-barcode/") + '" data-i18n="nav.scanBarcode"></a>' +
            '<a href="' + u("features/voice-logging/") + '" data-i18n="nav.voiceLogging"></a>' +
            '<a href="' + u("features/recipe/") + '" data-i18n="nav.recipe"></a>' +
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

  /* ═══════════ "You are here" ═══════════
     Resolved from the real URL rather than from data-page, because
     data-page only names the section. Without this the open Features
     panel was five identical white rows with no way to tell which one you
     were already reading.

       exact URL match  -> aria-current="page"  (loud: accent + marker)
       section match    -> .has-section         (quiet: just weight)  */
  function normPath(p) {
    try { p = decodeURI(p); } catch (e) {}
    p = p.replace(/index\.html?$/i, "");
    /* Add the trailing slash to directory URLs only. "/404.html" is a file
       and must not become "/404.html/". */
    if (!/\.[a-z0-9]+$/i.test(p) && !/\/$/.test(p)) p += "/";
    return p;
  }

  function markCurrent() {
    var here = normPath(location.pathname);
    var nav = document.getElementById("site-nav");
    if (!nav) return;

    nav.querySelectorAll("a[href]").forEach(function (a) {
      if (a.classList.contains("nav-logo")) return;   /* the logo is not a nav item */
      var url;
      try { url = new URL(a.getAttribute("href"), location.href); } catch (e) { return; }
      if (url.origin !== location.origin) return;     /* Play Store, socials */
      if (normPath(url.pathname) !== here) return;

      a.setAttribute("aria-current", "page");

      /* Light up the parent item too, so a hit inside a closed panel is
         still visible from the collapsed bar. */
      var item = a.closest(".nav-item, .m-item");
      if (item) item.classList.add("has-section");

      /* And open the mobile accordion it lives in — arriving at the drawer
         already showing where you are beats making you hunt for it. */
      var mPanel = a.closest(".m-panel");
      if (mPanel) {
        var mItem = mPanel.closest(".m-item");
        if (mItem) {
          mItem.classList.add("open");
          var mBtn = mItem.querySelector("button");
          if (mBtn) mBtn.setAttribute("aria-expanded", "true");
        }
      }
    });
  }
  markCurrent();

  /* ═══════════ Dropdowns ═══════════
     DESKTOP: opens on hover, with intent delays (see HOVER_IN/HOVER_OUT).
     TOUCH:   hover never fires, so the caret button is the only way in.
     KEYBOARD: unaffected by either — ArrowDown/Up/Escape below.

     An earlier version of this file was click-only and carried a warning
     against adding hover, because a naive mouseenter fights the click
     handler: hover opens the panel, then the click that follows toggles it
     straight back shut. Two things make hover safe here:

       1. mouseenter OPENS (force = true); it never toggles. Only the
          button toggles, so the two cannot cancel each other out.
       2. It is gated on (hover: hover) and (pointer: fine), so a touch
          device — where a tap synthesises a mouseenter immediately before
          the click — never runs it at all.  */

  /* Tuned by hand: 90ms is short enough that a deliberate hover feels
     instant, long enough that a mouse crossing the bar does not trip it.
     260ms out is generous on purpose — closing early is far more annoying
     than closing late. */
  var HOVER_IN = 90;
  var HOVER_OUT = 260;
  var hoverCapable = window.matchMedia("(hover: hover) and (pointer: fine)");

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

  /* Only the links INSIDE the disclosed panel are arrow-key targets. On a
     split item the label is itself an <a>, and a bare item.querySelectorAll("a")
     would make it links[0] — ArrowDown would then "enter the menu" by landing
     back on the thing you just pressed the caret next to. */
  function panelLinks(item) {
    return [].slice.call(item.querySelectorAll(".nav-panel a, .m-panel a"));
  }

  document.querySelectorAll("[data-dropdown]").forEach(function (item) {
    var btn = item.querySelector("button");
    if (!btn) return;

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      toggle(item);
    });

    /* Keyboard: Down opens and moves into the panel; Esc closes.
       stopPropagation matters: without it this event also bubbles to the
       item-level handler below, which would see focus already on link[0]
       and advance to link[1] — silently skipping the first entry. */
    btn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        e.stopPropagation();
        toggle(item, true);
        var first = panelLinks(item)[0];
        if (first) first.focus();
      } else if (e.key === "Escape") {
        toggle(item, false);
      }
    });

    item.addEventListener("keydown", function (e) {
      var links = panelLinks(item);
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

    /* Close when focus leaves the whole item (keyboard tab-out) — unless
       the pointer is still resting on it, in which case the menu is open
       on purpose and yanking it away would be the bug. */
    item.addEventListener("focusout", function () {
      setTimeout(function () {
        if (item.contains(document.activeElement)) return;
        if (item.matches(":hover")) return;
        toggle(item, false);
      }, 0);
    });

    /* ── Hover to open (fine pointers only) ──
       HOVER_IN is intent: without it, dragging the mouse across the bar on
       the way to something else pops every menu open in turn.
       HOVER_OUT is grace: the panel sits 8px below the label, so a pointer
       travelling into it is briefly over neither. The delay covers that
       crossing, and the re-check on expiry means an early mouseleave never
       closes a menu the pointer has already arrived in. */
    if (hoverCapable.matches && item.closest(".nav-links")) {
      var inT = 0, outT = 0;
      var clear = function () { clearTimeout(inT); clearTimeout(outT); };

      item.addEventListener("mouseenter", function () {
        if (!hoverCapable.matches) return;
        clear();
        inT = setTimeout(function () { toggle(item, true); }, HOVER_IN);
      });

      item.addEventListener("mouseleave", function () {
        if (!hoverCapable.matches) return;
        clear();
        outT = setTimeout(function () {
          /* Keep it open if the pointer came back, or if the keyboard is
             in there — closing under an focused link would strand focus. */
          if (item.matches(":hover")) return;
          if (item.contains(document.activeElement)) return;
          toggle(item, false);
        }, HOVER_OUT);
      });

      /* A click on a panel link navigates; kill any pending open so the
         menu does not flash back up during the page transition. */
      item.addEventListener("click", clear);
    }
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

  /* Slot labels live in the dictionary, so they exist in EN *and* ES.
     data-label is only a hard fallback if the key is ever missing. */
  function slotLabel(slot) {
    var D = window.FOTOCAL_I18N || {};
    var key = slot.getAttribute("data-label-key");
    var lang = "en";
    try {
      var saved = localStorage.getItem("fotocal-lang");
      if (saved === "es" || saved === "en") lang = saved;
    } catch (e) {}
    var v = (D[lang] && D[lang][key]) || (D.en && D.en[key]);
    return v || slot.getAttribute("data-label") || "";
  }

  document.querySelectorAll(".screen-slot").forEach(function (slot) {
    var src = slot.getAttribute("data-src");
    var key = slot.getAttribute("data-label-key");
    var label = slotLabel(slot);

    /* Paint the placeholder immediately. */
    slot.innerHTML =
      '<div class="slot-icon">' + CAMERA + '</div>' +
      '<div class="slot-label"' + (key ? ' data-i18n="' + key + '"' : '') + '>' + label + '</div>' +
      '<div class="slot-note" data-i18n="slot.pending"></div>' +
      '<div class="slot-path">' + (src || "").replace(BASE, "") + '</div>';

    if (!src) return;
    var img = new Image();
    img.onload = function () {
      var el = document.createElement("img");
      el.src = src;
      el.alt = label;
      /* Explicit intrinsic size: the frame is aspect-ratio locked, so this
         just keeps the browser from ever reflowing around the image. */
      el.setAttribute("width", slot.getAttribute("data-w") || "540");
      el.setAttribute("height", slot.getAttribute("data-h") || "1152");
      el.decoding = "async";
      if (slot.hasAttribute("data-eager")) {
        el.loading = "eager";
        el.setAttribute("fetchpriority", "high");
      } else {
        el.loading = "lazy";
      }
      slot.replaceWith(el);
    };
    img.src = src;
  });
})();
