/* Fotocal — landing page interactions */
(function () {
  "use strict";

  /* ── Language toggle ── */
  var DICT = window.FOTOCAL_I18N || {};
  var saved = null;
  try { saved = localStorage.getItem("fotocal-lang"); } catch (e) {}
  var lang = saved === "en" || saved === "es" ? saved : "es";

  function applyLang(next) {
    lang = next;
    var dict = DICT[next] || {};
    document.documentElement.lang = next;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (dict[key] != null) el.textContent = dict[key];
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-html");
      if (dict[key] != null) el.innerHTML = dict[key];
    });
    document.querySelectorAll(".lang-opt").forEach(function (el) {
      el.classList.toggle("active", el.getAttribute("data-lang") === next);
    });
    try { localStorage.setItem("fotocal-lang", next); } catch (e) {}
  }

  var toggle = document.getElementById("langToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      applyLang(lang === "es" ? "en" : "es");
    });
  }
  if (lang !== "es") applyLang(lang);

  /* ── Navbar scroll state ── */
  var nav = document.getElementById("nav");
  var onScroll = function () {
    if (nav) nav.classList.toggle("scrolled", window.scrollY > 30);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ── Mobile menu ── */
  var burger = document.getElementById("navBurger");
  var links = document.getElementById("navLinks");
  if (burger && links) {
    burger.addEventListener("click", function () {
      links.classList.toggle("open");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { links.classList.remove("open"); });
    });
  }

  /* ── Scroll reveal ── */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ── Calorie ring animation (hero phone) ── */
  var ring = document.getElementById("calRing");
  if (ring && "IntersectionObserver" in window) {
    var circumference = 2 * Math.PI * 52; // r = 52
    var progress = 1284 / 1900;
    var ringIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          requestAnimationFrame(function () {
            ring.style.strokeDashoffset = String(circumference * (1 - progress));
          });
          ringIO.unobserve(ring);
        }
      });
    }, { threshold: 0.4 });
    ringIO.observe(ring);
  } else if (ring) {
    ring.style.strokeDashoffset = "105";
  }

  /* ── FAQ: close others when one opens ── */
  var faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (item.open) {
        faqItems.forEach(function (other) {
          if (other !== item) other.open = false;
        });
      }
    });
  });
})();
