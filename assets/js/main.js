/* ══════════════════════════════════════════════════════════════
   FOTOCAL — page interactions
   Load order matters: i18n.js -> layout.js -> main.js
   (i18n.js holds the nav/footer strings, layout.js injects the chrome
   already translated, and this file wires up the interactions.)

   Page copy is NOT translated here. It is baked into the HTML by
   tools/build_site.py — see that file for the two-tree architecture.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

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

  /* ═══════════ Language ═══════════
     The site is now two rendered trees — Spanish at the root, English under
     /en/ — so the language of a page is decided by its URL, not by a
     setting. Nothing is translated at runtime any more: the text is already
     in the HTML, which is the whole point (Google can only index what it is
     served).

     What is left here is the switcher. It navigates to the same page in the
     other tree and remembers the choice, so a returning visitor who picked
     English lands on English. The preference never overrides the URL — a
     shared link always opens in the language it names. */
  var PAGE_LANG = (document.documentElement.lang === "en") ? "en" : "es";

  /* The same page in the other tree. /en/foo/ <-> /foo/ */
  function counterpart(lang) {
    var p = location.pathname;
    var bare = p.indexOf("/en/") === 0 ? p.slice(3) : (p === "/en" ? "/" : p);
    return (lang === "en" ? "/en" + bare : bare) + location.search + location.hash;
  }

  function remember(lang) {
    try { localStorage.setItem("fotocal-lang", lang); } catch (e) {}
  }
  /* Landing on a tree is itself a choice — keep the preference in step so
     the root-level redirect below never fights the URL the visitor used. */
  remember(PAGE_LANG);

  /* ═══════════ Language switcher ═══════════
     Built as real links, so it works without the click handlers, shows a
     proper URL on hover, and is followable by a crawler. */
  var langHost = document.getElementById("langToggle");
  if (langHost) {
    var sel = document.createElement("div");
    sel.className = "lang-select";
    sel.id = "langSelect";
    sel.innerHTML =
      '<button class="lang-current" id="langCurrent" type="button" aria-haspopup="listbox" ' +
        'aria-expanded="false" aria-label="Change language / Cambiar idioma">' +
        '<span class="lang-flag">' + (FOTOCAL_FLAGS[PAGE_LANG] || "") + '</span>' +
        '<span class="lang-code">' + (LANG_CODES[PAGE_LANG] || PAGE_LANG.toUpperCase()) + '</span>' +
        '<svg class="lang-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
          'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
          '<path d="M6 9l6 6 6-6"/></svg>' +
      '</button>' +
      '<ul class="lang-menu" id="langMenu" role="listbox">' +
        '<li role="none"><a class="lang-item" role="option" href="' + counterpart("es") + '" ' +
            'hreflang="es" lang="es" data-lang="es" aria-selected="' + (PAGE_LANG === "es") + '">' +
          '<span class="lang-flag">' + FOTOCAL_FLAGS.es + '</span>' +
          '<span class="lang-name">Español</span></a></li>' +
        '<li role="none"><a class="lang-item" role="option" href="' + counterpart("en") + '" ' +
            'hreflang="en" lang="en" data-lang="en" aria-selected="' + (PAGE_LANG === "en") + '">' +
          '<span class="lang-flag">' + FOTOCAL_FLAGS.en + '</span>' +
          '<span class="lang-name">English</span></a></li>' +
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

    menu.querySelectorAll(".lang-item").forEach(function (a) {
      /* Store the choice before the navigation, not after — after never runs. */
      a.addEventListener("click", function () { remember(a.getAttribute("data-lang")); });
      a.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { closeMenu(); current.focus(); }
      });
    });

    document.addEventListener("click", closeMenu);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMenu(); });
  }

  /* ═══════════ Scroll reveal ═══════════ */
  var revealEls = document.querySelectorAll(".reveal");
  /* Siblings arrive in sequence: each .reveal that has no delay of its
     own gets one from its position among the .reveal children of the
     same parent — 90ms apart, capped so a long row never waits on the
     last card. Runs once per element: the observer unobserves on entry. */
  revealEls.forEach(function (el) {
    if (el.style.getPropertyValue("--rd")) return;
    var i = 0, n = el;
    while ((n = n.previousElementSibling)) { if (n.classList.contains("reveal")) i++; }
    if (i) el.style.setProperty("--rd", Math.min(i * 90, 450) + "ms");
  });
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

  /* ═══════════ FAQ — one open at a time, and it slides ═══════════
     The FAQ is native <details>/<summary> and stays that way: it is what
     makes the answers readable to a crawler, operable from the keyboard
     and announced by a screen reader. A browser opens and closes it in a
     single frame, though — there was nothing easing, so there was nothing
     CSS could smooth. The height is animated AROUND the element instead:

       opening — set open=true first (a closed <details> has no height to
                 measure), then animate the element's own height from its
                 closed height up to the full one;
       closing — cancel the default, which would snap it shut, animate
                 back down, and only then set open=false.

     Both directions share a duration and a curve, and the + turns into the
     × on the same clock — from .is-open, not [open], because [open] stays
     true for the whole of the closing animation.

     One at a time is kept from the old version, but the panel being
     displaced now slides shut instead of vanishing mid-gesture, so the two
     read as one movement rather than a fight.

     Interruption is the normal case on a phone: a second tap mid-flight
     re-targets from the CURRENT height instead of restarting, and the old
     animation's handlers are detached before it is cancelled, so a panel
     can never be left half-open or stuck. Because it is the <details> box
     itself that grows, everything below moves with it and the page never
     jumps.

     prefers-reduced-motion: nothing is intercepted at all, so the browser's
     instant open/close is exactly what it was before. */
  var FAQ_MS = 260, FAQ_EASE = "cubic-bezier(.2,.8,.3,1)";
  var faqStill = window.matchMedia("(prefers-reduced-motion: reduce)");
  var faqCtrls = [];

  function faqCloseOthers(except, animate) {
    faqCtrls.forEach(function (c) {
      if (c.el === except || !c.el.open) return;
      if (animate) { c.close(); }
      else { c.el.open = false; c.el.classList.remove("is-open"); }
    });
  }

  function faqAccordion(el) {
    var summary = el.querySelector("summary");
    if (!summary) return;
    var anim = null, closing = false, expanding = false;
    var ctrl = { el: el, close: function () { if (!closing) shrink(); } };
    faqCtrls.push(ctrl);

    /* keeps the icon and the border honest when the browser does the
       toggling itself: reduced motion, no Web Animations, find-in-page. */
    el.addEventListener("toggle", function () {
      if (!anim) el.classList.toggle("is-open", el.open);
      if (el.open && !anim) faqCloseOthers(el, false);
    });

    summary.addEventListener("click", function (e) {
      if (faqStill.matches || !el.animate) return;
      e.preventDefault();
      if (closing || !el.open) { openIt(); }
      else if (expanding || el.open) { shrink(); }
    });

    function contentHeight() {
      var h = 0, n = summary.nextElementSibling;
      while (n) { h += n.offsetHeight; n = n.nextElementSibling; }
      return h;
    }
    /* The closed height is the summary PLUS the <details>'s own border and
       padding. Animating to the summary alone undershoots by exactly the
       border, and the panel snaps those last two pixels — small, but it is
       the kind of snap this whole change exists to remove. */
    function closedHeight() {
      var cs = getComputedStyle(el);
      return summary.offsetHeight
           + parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth)
           + parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
    }
    function run(from, to, willBeOpen) {
      el.style.overflow = "hidden";
      if (anim) { anim.onfinish = null; anim.cancel(); }   /* detach first: a
          stale handler would clear the flags of the animation replacing it */
      anim = el.animate({ height: [from + "px", to + "px"] },
                        { duration: FAQ_MS, easing: FAQ_EASE });
      anim.onfinish = function () {
        el.open = willBeOpen;
        el.classList.toggle("is-open", willBeOpen);
        anim = null; closing = false; expanding = false;
        el.style.height = "";
        el.style.overflow = "";
      };
    }
    function openIt() {
      faqCloseOthers(el, true);
      el.style.height = el.offsetHeight + "px";
      el.open = true;
      el.classList.add("is-open");
      requestAnimationFrame(function () {
        expanding = true; closing = false;
        run(el.offsetHeight, closedHeight() + contentHeight(), true);
      });
    }
    function shrink() {
      closing = true; expanding = false;
      el.classList.remove("is-open");
      run(el.offsetHeight, closedHeight(), false);
    }
  }
  document.querySelectorAll(".faq-item").forEach(faqAccordion);

  /* ═══════════ Hero parallax (home page only) ═══════════
     Gentle mouse-move parallax on the hero illustration and its
     floating chips. Each element declares its depth via data-par
     (positive = moves with the cursor, negative = against it).
     Pointer-fine + no-reduced-motion only, and rAF-throttled, so it
     costs nothing on phones and respects accessibility settings. */
  var heroStage = document.getElementById("heroStage");
  var finePointer = window.matchMedia("(pointer: fine)").matches;
  var noMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (heroStage && finePointer && !noMotion) {
    var parEls = heroStage.querySelectorAll("[data-par]");
    var pmx = 0, pmy = 0, raf = null;
    var paint = function () {
      raf = null;
      parEls.forEach(function (el) {
        var d = parseFloat(el.getAttribute("data-par")) || 0;
        el.style.transform = "translate3d(" + (pmx * d) + "px," + (pmy * d) + "px,0)";
      });
    };
    heroStage.addEventListener("mousemove", function (e) {
      var r = heroStage.getBoundingClientRect();
      pmx = ((e.clientX - r.left) / r.width - 0.5);   /* -0.5 .. 0.5 */
      pmy = ((e.clientY - r.top) / r.height - 0.5);
      if (!raf) raf = requestAnimationFrame(paint);
    });
    heroStage.addEventListener("mouseleave", function () {
      pmx = 0; pmy = 0;
      if (!raf) raf = requestAnimationFrame(paint);
    });
  }

  /* ═══════════ Blog category filter (listing page only) ═══════════
     Pure client-side: every card carries data-cat, chips carry
     data-filter. No pagination and no re-render — we just toggle
     `hidden`, so filtering is instant and the page stays one static
     document that GitHub Pages can serve straight from cache. */
  var blGrid = document.getElementById("blGrid");
  if (blGrid) {
    var chips = document.querySelectorAll(".bl-chip");
    var cards = blGrid.querySelectorAll(".bl-card");
    var countEl = document.getElementById("blCount");
    var emptyEl = document.getElementById("blEmpty");

    /* The featured article lives outside #blGrid so it can render large,
       but it is a post like any other: it carries data-cat, it counts
       toward the chip totals, and it hides when the filter excludes it.
       Leaving it out was why "All" said 53 against 54 articles, and why
       filtering by Mindset still showed a calorie-counting piece. */
    var featured = document.getElementById("blFeature");

    var applyFilter = function (want) {
      var shown = 0;
      if (featured) {
        var fMatch = want === "all" || featured.getAttribute("data-cat") === want;
        featured.hidden = !fMatch;
        if (fMatch) shown++;
      }
      cards.forEach(function (c) {
        var match = want === "all" || c.getAttribute("data-cat") === want;
        c.hidden = !match;
        if (match) shown++;
      });
      if (countEl) countEl.textContent = String(shown);
      if (emptyEl) emptyEl.hidden = shown !== 0;
      chips.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === want));
      });
    };

    chips.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var want = btn.getAttribute("data-filter");
        applyFilter(want);
        /* Reflect the choice in the URL so a filtered view is shareable
           and survives a refresh, without adding a history entry per click. */
        var url = want === "all" ? location.pathname
                                 : location.pathname + "?cat=" + encodeURIComponent(want);
        history.replaceState(null, "", url);
      });
    });

    /* Honour ?cat= on load. */
    var initial = new URLSearchParams(location.search).get("cat");
    if (initial && document.querySelector('.bl-chip[data-filter="' + CSS.escape(initial) + '"]')) {
      applyFilter(initial);
    }
  }

  /* ═══════════ Card spotlight (home page only) ═══════════
     The .log-card::before layer paints a radial highlight at
     --mx/--my; this just keeps those props under the cursor. */
  if (finePointer) {
    // Carousel prev/next (under 1100px the track scrolls; the buttons page
    // it one card at a time and disable at the ends). Arrow keys already
    // work because the track is focusable and scrolls natively.
    var track = document.querySelector(".log-track");
    if (track) {
      var prev = document.querySelector("[data-log-prev]"), next = document.querySelector("[data-log-next]");
      var step = function () { var c = track.querySelector(".log-card"); return c ? c.getBoundingClientRect().width + 16 : 300; };
      var sync = function () {
        if (!prev) return;
        prev.disabled = track.scrollLeft <= 2;
        next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
      };
      if (prev) {
        prev.addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: "smooth" }); });
        next.addEventListener("click", function () { track.scrollBy({ left: step(), behavior: "smooth" }); });
        track.addEventListener("scroll", sync, { passive: true });
        window.addEventListener("resize", sync);
        sync();
      }
    }
    document.querySelectorAll(".log-card").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--mx", (e.clientX - r.left) + "px");
        card.style.setProperty("--my", (e.clientY - r.top) + "px");
      });
    });
  }

  /* ═══════════ Image load-in ═══════════
     CSS starts lazy images at opacity 0 and this fades them in when the
     bytes land. Two details that matter:

       · `complete` is checked first. An image already in cache fires no
         load event, so without this it would sit invisible forever.
       · onerror marks it too. A 404 should show its alt text, which it
         cannot do at opacity 0.  */
  document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
    if (img.complete) { img.classList.add("is-loaded"); return; }
    img.addEventListener("load", function () { img.classList.add("is-loaded"); }, { once: true });
    img.addEventListener("error", function () { img.classList.add("is-loaded"); }, { once: true });
  });

  /* ═══════════ Reading progress ═══════════
     Long-form pages only. On a short page the bar is already part-filled
     when you arrive, which reads as a stuck loader rather than progress.
     2.2 screens is the threshold where it starts being informative. */
  var doc = document.documentElement;
  var article = document.querySelector(".art-body, .legal-body, .prose");
  if (article && doc.scrollHeight > window.innerHeight * 2.2) {
    var bar = document.createElement("div");
    bar.className = "read-bar";
    bar.setAttribute("aria-hidden", "true");   /* decorative; the page is the content */
    var fill = document.createElement("span");
    bar.appendChild(fill);
    document.body.appendChild(bar);

    var ticking = false;
    var draw = function () {
      var max = doc.scrollHeight - window.innerHeight;
      var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      fill.style.width = Math.min(100, Math.max(0, pct)) + "%";
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(draw);
    }, { passive: true });
    window.addEventListener("resize", draw, { passive: true });
    draw();
  }

})();
