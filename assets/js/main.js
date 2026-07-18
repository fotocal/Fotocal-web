/* ══════════════════════════════════════════════════════════════
   FOTOCAL — page interactions
   Load order matters: i18n.js -> layout.js -> main.js
   (layout.js injects the nav/footer; this file then translates them.)
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var DICT = window.FOTOCAL_I18N || {};
  var DEFAULT_LANG = "en";   /* English is the default. */

  /* Inline flag artwork — SVG, not emoji, so flags render identically on
     every OS (Windows in particular does not draw flag emoji). */
  var FOTOCAL_FLAGS = {
    en: '<svg class="lang-flag-svg" viewBox="0 0 60 30" aria-hidden="true">' +
          '<rect width="60" height="30" fill="#012169"/>' +
          '<path d="M0 0 60 30M60 0 0 30" stroke="#fff" stroke-width="6"/>' +
          '<path d="M0 0 60 30M60 0 0 30" stroke="#C8102E" stroke-width="3.5"/>' +
          '<rect x="25" width="10" height="30" fill="#fff"/>' +
          '<rect y="10" width="60" height="10" fill="#fff"/>' +
          '<rect x="27" width="6" height="30" fill="#C8102E"/>' +
          '<rect y="12" width="60" height="6" fill="#C8102E"/>' +
        '</svg>',
    es: '<svg class="lang-flag-svg" viewBox="0 0 60 40" aria-hidden="true">' +
          '<rect width="60" height="40" fill="#AA151B"/>' +
          '<rect y="10" width="60" height="20" fill="#F1BF00"/>' +
        '</svg>'
  };
  var LANG_CODES = { en: "EN", es: "ES" };

  /* ═══════════ Language ═══════════ */
  var saved = null;
  try { saved = localStorage.getItem("fotocal-lang"); } catch (e) {}
  var lang = (saved === "en" || saved === "es") ? saved : DEFAULT_LANG;

  function applyLang(next) {
    if (!DICT[next]) next = DEFAULT_LANG;
    lang = next;

    var dict = DICT[next];
    var fallback = DICT[DEFAULT_LANG] || {};

    document.documentElement.lang = next;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var k = el.getAttribute("data-i18n");
      var v = dict[k];
      if (v == null) v = fallback[k];        /* never leave a string blank */
      if (v != null) el.textContent = v;
    });

    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-html");
      var v = dict[k];
      if (v == null) v = fallback[k];
      if (v != null) el.innerHTML = v;
    });

    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-aria");
      var v = dict[k] != null ? dict[k] : fallback[k];
      if (v != null) el.setAttribute("aria-label", v);
    });

    /* Reflect the choice in the language dropdown (trigger + option ticks). */
    var trig = document.getElementById("langCurrent");
    if (trig) {
      var tf = trig.querySelector("[data-lang-flag]");
      var tc = trig.querySelector("[data-lang-code]");
      if (tf) tf.innerHTML = FOTOCAL_FLAGS[next] || "";
      if (tc) tc.textContent = LANG_CODES[next] || next.toUpperCase();
    }
    document.querySelectorAll(".lang-item").forEach(function (el) {
      el.setAttribute("aria-selected", el.getAttribute("data-lang") === next ? "true" : "false");
    });

    try { localStorage.setItem("fotocal-lang", next); } catch (e) {}
  }

  /* Always run: the injected nav/footer ship with empty text nodes that
     only the dictionary fills, so this is what makes the page readable. */
  applyLang(lang);

  /* ═══════════ Language dropdown ═══════════
     Replaces the old EN/ES flip-toggle. One click on the trigger opens a
     proper menu; picking a language sets it explicitly and persists it, so
     there is no accidental flipping. */
  var langHost = document.getElementById("langToggle");
  if (langHost) {
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
          '<span class="lang-flag">' + FOTOCAL_FLAGS.en + '</span>' +
          '<span class="lang-name">English</span></li>' +
        '<li class="lang-item" role="option" data-lang="es" tabindex="0">' +
          '<span class="lang-flag">' + FOTOCAL_FLAGS.es + '</span>' +
          '<span class="lang-name">Español</span></li>' +
      '</ul>';
    langHost.replaceWith(sel);

    var current = sel.querySelector("#langCurrent");
    var menu = sel.querySelector("#langMenu");

    var closeMenu = function () {
      sel.classList.remove("open");
      current.setAttribute("aria-expanded", "false");
    };
    var openMenu = function () {
      sel.classList.add("open");
      current.setAttribute("aria-expanded", "true");
    };

    current.addEventListener("click", function (e) {
      e.stopPropagation();
      if (sel.classList.contains("open")) closeMenu(); else openMenu();
    });

    menu.querySelectorAll(".lang-item").forEach(function (li) {
      var pick = function () { applyLang(li.getAttribute("data-lang")); closeMenu(); current.focus(); };
      li.addEventListener("click", function (e) { e.stopPropagation(); pick(); });
      li.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); }
        else if (e.key === "Escape") { closeMenu(); current.focus(); }
      });
    });

    document.addEventListener("click", closeMenu);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });

    /* Paint the trigger now that the dropdown exists. */
    applyLang(lang);
  }

  /* ═══════════ Scroll reveal ═══════════ */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -5% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ═══════════ FAQ — one open at a time ═══════════ */
  var faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      faqItems.forEach(function (other) {
        if (other !== item) other.open = false;
      });
    });
  });
})();
