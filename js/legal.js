/* Fotocal — legal pages language toggle (shows ES or EN content block) */
(function () {
  "use strict";
  var saved = null;
  try { saved = localStorage.getItem("fotocal-lang"); } catch (e) {}
  var lang = saved === "en" || saved === "es" ? saved : "es";

  function apply(next) {
    lang = next;
    document.documentElement.lang = next;
    document.querySelectorAll("[data-lang-block]").forEach(function (el) {
      el.classList.toggle("visible", el.getAttribute("data-lang-block") === next);
    });
    document.querySelectorAll(".lang-opt").forEach(function (el) {
      el.classList.toggle("active", el.getAttribute("data-lang") === next);
    });
    try { localStorage.setItem("fotocal-lang", next); } catch (e) {}
  }

  var toggle = document.getElementById("langToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      apply(lang === "es" ? "en" : "es");
    });
  }
  apply(lang);
})();
