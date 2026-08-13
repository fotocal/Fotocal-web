/* ═══════════════════════════════════════════════════════════════
   FOTOCAL — legal pages behaviour
   • builds a sticky table-of-contents with smooth-scroll anchors and
     scroll-spy highlighting
   • language switcher: two links to the same page in the other tree

   These pages used to hold both languages at once and swap them at
   runtime from a localStorage key. They are now rendered one language
   per URL like the rest of the site (Spanish at /privacy-policy/,
   English at /en/privacy-policy/), so there is nothing left to swap —
   and the runtime swap was actively harmful here, because it also
   rewrote <html lang> and told crawlers the Spanish page was English.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var FLAGS = {
    en: '<svg class="lang-flag-svg" viewBox="0 0 60 30" aria-hidden="true">' +
          '<rect width="60" height="30" fill="#012169"/>' +
          '<path d="M0 0 60 30M60 0 0 30" stroke="#fff" stroke-width="6"/>' +
          '<path d="M0 0 60 30M60 0 0 30" stroke="#C8102E" stroke-width="3.5"/>' +
          '<rect x="25" width="10" height="30" fill="#fff"/>' +
          '<rect y="10" width="60" height="10" fill="#fff"/>' +
          '<rect x="27" width="6" height="30" fill="#C8102E"/>' +
          '<rect y="12" width="60" height="6" fill="#C8102E"/></svg>',
    es: '<svg class="lang-flag-svg" viewBox="0 0 60 40" aria-hidden="true">' +
          '<rect width="60" height="40" fill="#AA151B"/>' +
          '<rect y="10" width="60" height="20" fill="#F1BF00"/></svg>'
  };
  var CODES = { en: "EN", es: "ES" };
  var TOC_LABEL = { en: "On this page", es: "En esta página" };

  var lang = (document.documentElement.lang === "en") ? "en" : "es";

  /* The same page in the other tree. /en/terms/ <-> /terms/ */
  function counterpart(to) {
    var p = location.pathname;
    var bare = p.indexOf("/en/") === 0 ? p.slice(3) : (p === "/en" ? "/" : p);
    return (to === "en" ? "/en" + bare : bare) + location.hash;
  }

  /* ── Restructure into TOC + content layout (no HTML change needed) ── */
  var card = document.querySelector(".legal-card") || document.querySelector(".legal-content");
  var toc = null;
  if (card) {
    var container = card.closest(".container");
    if (container) container.classList.remove("container-narrow");
    var layout = document.createElement("div");
    layout.className = "legal-layout";
    toc = document.createElement("aside");
    toc.className = "legal-toc";
    toc.innerHTML = '<div class="legal-toc-title"></div><nav aria-label="Table of contents"></nav>';
    card.parentNode.insertBefore(layout, card);
    layout.appendChild(toc);
    layout.appendChild(card);
    card.classList.add("legal-content");
  }

  var spyObserver = null;

  function buildTOC() {
    if (!toc || !card) return;
    var nav = toc.querySelector("nav");
    var title = toc.querySelector(".legal-toc-title");
    title.textContent = TOC_LABEL[lang] || TOC_LABEL.en;
    nav.innerHTML = "";
    if (spyObserver) { spyObserver.disconnect(); spyObserver = null; }

    /* One language per page now, so the headings in the card ARE the
       headings — there is no hidden second copy to filter out. */
    var heads = card.querySelectorAll("h2");
    var links = [];
    heads.forEach(function (h, i) {
      var id = "sec-" + (i + 1);
      h.id = id;
      var a = document.createElement("a");
      a.href = "#" + id;
      a.textContent = h.textContent.replace(/^\s*\d+\.\s*/, "");
      nav.appendChild(a);
      links.push(a);
    });

    /* Scroll-spy: highlight the section currently in view. */
    if ("IntersectionObserver" in window && heads.length) {
      var byId = {};
      links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
      spyObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            links.forEach(function (a) { a.classList.remove("active"); });
            var active = byId[en.target.id];
            if (active) active.classList.add("active");
          }
        });
      }, { rootMargin: "-20% 0px -70% 0px", threshold: 0 });
      heads.forEach(function (h) { spyObserver.observe(h); });
    }
  }

  /* Landing on a tree is itself a choice, so keep the shared preference in
     step — it is what the rest of the site reads to decide where to send a
     returning visitor. It never overrides the URL. */
  try { localStorage.setItem("fotocal-lang", lang); } catch (e) {}
  buildTOC();

  /* ── Language switcher ──
     Real links, matching the main site's: they show a URL on hover, work
     with the handlers dead, and a crawler can follow them. */
  var host = document.getElementById("langToggle");
  if (host) {
    var sel = document.createElement("div");
    sel.className = "lang-select";
    sel.id = "langSelect";
    sel.innerHTML =
      '<button class="lang-current" id="langCurrent" type="button" aria-haspopup="listbox" ' +
        'aria-expanded="false" aria-label="Change language / Cambiar idioma">' +
        '<span class="lang-flag">' + (FLAGS[lang] || "") + '</span>' +
        '<span class="lang-code">' + CODES[lang] + '</span>' +
        '<svg class="lang-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
          'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
          '<path d="M6 9l6 6 6-6"/></svg>' +
      '</button>' +
      '<ul class="lang-menu" id="langMenu" role="listbox">' +
        '<li role="none"><a class="lang-item" role="option" href="' + counterpart("es") + '" ' +
            'hreflang="es" lang="es" data-lang="es" aria-selected="' + (lang === "es") + '">' +
          '<span class="lang-flag">' + FLAGS.es + '</span><span class="lang-name">Español</span></a></li>' +
        '<li role="none"><a class="lang-item" role="option" href="' + counterpart("en") + '" ' +
            'hreflang="en" lang="en" data-lang="en" aria-selected="' + (lang === "en") + '">' +
          '<span class="lang-flag">' + FLAGS.en + '</span><span class="lang-name">English</span></a></li>' +
      '</ul>';
    host.replaceWith(sel);

    var current = sel.querySelector("#langCurrent");
    var menu = sel.querySelector("#langMenu");
    var close = function () { sel.classList.remove("open"); current.setAttribute("aria-expanded", "false"); };
    var open = function () { sel.classList.add("open"); current.setAttribute("aria-expanded", "true"); };
    current.addEventListener("click", function (e) {
      e.stopPropagation();
      if (sel.classList.contains("open")) close(); else open();
    });
    menu.querySelectorAll(".lang-item").forEach(function (a) {
      /* Store the choice before the navigation, not after — after never runs. */
      a.addEventListener("click", function () {
        try { localStorage.setItem("fotocal-lang", a.getAttribute("data-lang")); } catch (e) {}
      });
      a.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { close(); current.focus(); }
      });
    });
    document.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }

})();
