/* ═══════════════════════════════════════════════════════════════
   FOTOCAL — legal pages behaviour
   • language dropdown (EN / ES) shared with the main site via the
     "fotocal-lang" localStorage key
   • builds a sticky table-of-contents from the visible language block
     with smooth-scroll anchors and scroll-spy highlighting
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

  var saved = null;
  try { saved = localStorage.getItem("fotocal-lang"); } catch (e) {}
  var lang = (saved === "en" || saved === "es") ? saved : "en";

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

    var block = card.querySelector('[data-lang-block].visible');
    if (!block) return;
    var heads = block.querySelectorAll("h2");
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

  function showLang(next) {
    lang = (next === "es") ? "es" : "en";
    document.documentElement.lang = lang;
    document.querySelectorAll("[data-lang-block]").forEach(function (b) {
      b.classList.toggle("visible", b.getAttribute("data-lang-block") === lang);
    });
    /* dropdown state */
    var trig = document.getElementById("langCurrent");
    if (trig) {
      var tf = trig.querySelector("[data-lang-flag]");
      var tc = trig.querySelector("[data-lang-code]");
      if (tf) tf.innerHTML = FLAGS[lang] || "";
      if (tc) tc.textContent = CODES[lang];
    }
    document.querySelectorAll(".lang-item").forEach(function (el) {
      el.setAttribute("aria-selected", el.getAttribute("data-lang") === lang ? "true" : "false");
    });
    try { localStorage.setItem("fotocal-lang", lang); } catch (e) {}
    buildTOC();
  }

  /* ── Build the language dropdown (replaces the old EN/ES toggle) ── */
  var host = document.getElementById("langToggle");
  if (host) {
    var sel = document.createElement("div");
    sel.className = "lang-select";
    sel.id = "langSelect";
    sel.innerHTML =
      '<button class="lang-current" id="langCurrent" type="button" aria-haspopup="listbox" ' +
        'aria-expanded="false" aria-label="Change language / Cambiar idioma">' +
        '<span class="lang-flag" data-lang-flag></span>' +
        '<span class="lang-code" data-lang-code>EN</span>' +
        '<svg class="lang-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
          'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
          '<path d="M6 9l6 6 6-6"/></svg>' +
      '</button>' +
      '<ul class="lang-menu" id="langMenu" role="listbox">' +
        '<li class="lang-item" role="option" data-lang="en" tabindex="0">' +
          '<span class="lang-flag">' + FLAGS.en + '</span><span class="lang-name">English</span></li>' +
        '<li class="lang-item" role="option" data-lang="es" tabindex="0">' +
          '<span class="lang-flag">' + FLAGS.es + '</span><span class="lang-name">Español</span></li>' +
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
    menu.querySelectorAll(".lang-item").forEach(function (li) {
      var pick = function () { showLang(li.getAttribute("data-lang")); close(); current.focus(); };
      li.addEventListener("click", function (e) { e.stopPropagation(); pick(); });
      li.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); }
        else if (e.key === "Escape") { close(); current.focus(); }
      });
    });
    document.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }

  showLang(lang);
})();
