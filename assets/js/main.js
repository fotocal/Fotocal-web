/* ═══════════════════════════════════════════════════════════════
   FOTOCAL — page interactions
   Load order matters: i18n.js -> layout.js -> main.js
   (layout.js injects the nav/footer; this file then translates them.)
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var DICT = window.FOTOCAL_I18N || {};
  var DEFAULT_LANG = "en";   /* English is the default. */

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

    document.querySelectorAll(".lang-opt").forEach(function (el) {
      el.classList.toggle("active", el.getAttribute("data-lang") === next);
    });

    try { localStorage.setItem("fotocal-lang", next); } catch (e) {}
  }

  /* Always run: the injected nav/footer ship with empty text nodes that
     only the dictionary fills, so this is what makes the page readable —
     and it guarantees a single source of truth for every string. */
  applyLang(lang);

  var toggle = document.getElementById("langToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      applyLang(lang === "en" ? "es" : "en");
    });
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
