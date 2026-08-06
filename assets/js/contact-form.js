/* ═══════════════════════════════════════════════════════════════
   FOTOCAL — contact form (Web3Forms)

   The site is static, so there is no backend to post to. Web3Forms
   receives the submission and forwards it to the support inbox, which it
   stores server-side: only the public access key is present in the page,
   so the address cannot be scraped from the HTML.

   Submission is AJAX so the sender never leaves the page — a redirect to
   a third-party thank-you screen is exactly the moment people doubt the
   message went anywhere.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var form = document.getElementById("contactForm");
  if (!form) return;

  var btn = document.getElementById("cfSubmit");
  var ok  = document.getElementById("cfOk");
  var bad = document.getElementById("cfBad");

  /* Copy from the shared dictionary so the form speaks the chosen
     language. main.js owns the switch; this only reads it. */
  function t(key, fallback) {
    var D = window.FOTOCAL_I18N || {};
    var lang = "en";
    try {
      var saved = localStorage.getItem("fotocal-lang");
      if (saved === "es" || saved === "en") lang = saved;
    } catch (e) {}
    var v = (D[lang] && D[lang][key]);
    if (v == null) v = (D.en && D.en[key]);
    return v != null ? v : fallback;
  }

  function show(el, msg) {
    el.textContent = msg;
    el.classList.add("show");
  }
  function hide() {
    ok.classList.remove("show");
    bad.classList.remove("show");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    hide();

    /* Reveal validation styling only once a send has been attempted, so
       the form is not covered in red the moment it renders. */
    form.classList.add("was-validated");
    if (!form.checkValidity()) {
      var first = form.querySelector(":invalid");
      if (first) first.focus();
      return;
    }

    /* A filled honeypot means a bot. Show the normal success message
       rather than an error — telling a bot it failed just invites a
       retry, and a human will never see this branch. */
    if (form.botcheck && form.botcheck.value) {
      show(ok, t("cf.ok", "Thanks! We'll reply within 24 hours — please check your email."));
      form.reset();
      form.classList.remove("was-validated");
      return;
    }

    var data = Object.fromEntries(new FormData(form).entries());
    delete data.botcheck;

    btn.disabled = true;
    var label = btn.textContent;
    btn.textContent = t("cf.sending", "Sending…");

    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json().then(function (j) { return { r: r, j: j }; }); })
      .then(function (res) {
        if (res.r.ok && res.j.success) {
          show(ok, t("cf.ok", "Thanks! We'll reply within 24 hours — please check your email."));
          form.reset();
          form.classList.remove("was-validated");
          ok.scrollIntoView({ block: "nearest", behavior: "smooth" });
        } else {
          show(bad, t("cf.fail", "Sorry — that did not send. Please try again in a moment."));
        }
      })
      .catch(function () {
        show(bad, t("cf.fail", "Sorry — that did not send. Please try again in a moment."));
      })
      .finally(function () {
        btn.disabled = false;
        btn.textContent = label;
      });
  });

  /* Typing again clears a stale result banner. */
  form.addEventListener("input", hide);
})();
