/* FOTOCAL — the eight calculators (/calculadoras/ and /en/calculadoras/).

   Everything runs in the page: nothing is sent anywhere and there is no
   account. Body data (sex, age, height, weight, activity) is kept in
   localStorage under one key so the next calculator opens prefilled; a
   browser that blocks storage simply starts from the defaults.

   THE FORMULAS ARE THE APP'S (fotocal/Fotocal: src/logic/plan.ts,
   src/lib/water.ts, src/logic/safetyFloor.ts), so the site and the app give
   the same number for the same person:
     BMR      Mifflin-St Jeor 1990: 10·kg + 6.25·cm − 5·age + 5 (man) / − 161 (woman)
              Katch-McArdle when body fat is given: 370 + 21.6 · lean kg
     TDEE     BMR × 1.2 / 1.375 / 1.465 / 1.55 / 1.725 (five day-to-day levels)
     Lose     deficit = pace kg × 7,700 ÷ 7, at most 25 % of TDEE; floor() ;
              never below 1,200 kcal (women) / 1,500 kcal (men)
     Gain     surplus = pace kg × 7,700 ÷ 7, at most 825 kcal; muscle = TDEE × 1.1
     Protein  2.0 g/kg (lose, muscle) or 1.6 g/kg (maintain, gain) on the
              weight at BMI 25 when BMI > 25, else on the real weight
     Fat      25 % (lose, muscle) / 27.5 % (maintain, gain) of kcal; carbs the rest
     Water    kcal target × 1.0–1.5 ml (by activity) × 0.8 (drinks share),
              at most 4,000 ml, at least the EFSA adequate intake × 0.8
     BMI      kg / m², WHO adult bands; healthy weight = BMI 18.5–24.9

   The pure part (CALC) also runs under Node: tools/gen_calcs.py renders each
   page's default result with it, and tools/check_calcs.mjs checks it against
   numbers worked out by hand from the app's code. */
(function () {
  "use strict";

  /* ─── pure arithmetic, the app's constants ─────────────────────────── */
  var FACTOR = { sedentary: 1.2, light: 1.375, standing: 1.465, active: 1.55, hard: 1.725 };
  var WATER_RATIO = { sedentary: 1.0, light: 1.1, standing: 1.1, active: 1.25, hard: 1.5 };
  var PROTEIN_G_PER_KG = { lose: 2.0, maintain: 1.6, gain: 1.6, build_muscle: 2.0 };
  var FAT_PCT = { lose: 0.25, maintain: 0.275, gain: 0.275, build_muscle: 0.25 };
  var FLOOR = { m: 1500, f: 1200 };
  var KCAL_PER_KG = 7700;

  function mifflin(sex, age, h, w) { return 10 * w + 6.25 * h - 5 * age + (sex === "m" ? 5 : -161); }
  function katch(w, bf) { return 370 + 21.6 * w * (1 - bf / 100); }
  function saneBf(v) { return v != null && isFinite(v) && v >= 3 && v <= 60 ? v : null; }
  function bmiOf(h, w) { var m = h / 100; return w / (m * m); }

  /* calculatePlan() without the app-only inputs (target date, GLP-1, pins).
     target 0 = "no target weight", which keeps the chosen goal as it is. */
  function plan(i) {
    var bf = saneBf(i.bf);
    var bmr = bf != null ? katch(i.weight, bf) : mifflin(i.sex, i.age, i.height, i.weight);
    var tdee = bmr * (FACTOR[i.activity] || FACTOR.light);
    var goal = i.goal || "maintain";
    if (i.target > 0) {
      var diff = i.target - i.weight;
      goal = Math.abs(diff) < 0.5 ? "maintain" : diff < 0 ? "lose" : (goal === "build_muscle" ? "build_muscle" : "gain");
    }
    var kgToGo = i.target > 0 ? Math.abs(i.weight - i.target) : Infinity;
    var pace = Math.min(i.pace || 0.5, kgToGo / 2);
    var paceKcal = pace * KCAL_PER_KG / 7;
    var daily, capped = false;
    if (goal === "lose") {
      var d = Math.min(paceKcal, tdee * 0.25);
      capped = d < paceKcal;
      daily = Math.floor(tdee - d);
    } else if (goal === "build_muscle") daily = tdee * 1.1;
    else if (goal === "gain") daily = Math.round(tdee + Math.min(paceKcal, 825));
    else daily = tdee;
    var floor = FLOOR[i.sex] || 1200;
    var floored = daily < floor;
    var kcal = Math.round(Math.max(daily, floor));
    var mk = i.kcal > 0 ? Math.round(i.kcal) : kcal;
    var m = macros({ goal: goal, height: i.height, weight: i.weight, split: i.split }, mk);
    /* applyMacroPins() with no pins: carbs are re-derived from the ROUNDED
       protein and fat grams, so the three always add back up to the kcal */
    m.carbs = Math.round((mk - 4 * m.protein - 9 * m.fat) / 4);
    if (m.carbs < 0) { m.carbs = 0; m.kcal = 4 * m.protein + 9 * m.fat; if (!(i.kcal > 0)) kcal = m.kcal; }
    return { bmr: bmr, tdee: tdee, goal: goal, raw: daily, kcal: kcal, floor: floor, floored: floored, capped: capped,
             pace: pace, kgToGo: kgToGo, protein: m.protein, carbs: m.carbs, fat: m.fat, refKg: m.refKg, gPerKg: m.gPerKg,
             macroKcal: m.kcal, fatDropped: m.fatDropped, bmrKatch: bf != null };
  }

  function macros(i, kcal) {
    var hm = i.height / 100;
    var bmi = i.weight / (hm * hm);
    var refKg = bmi > 25 ? 25 * hm * hm : i.weight;
    var split = i.split || "balanced";
    var g = PROTEIN_G_PER_KG[i.goal] || 1.6;
    if (split === "high_protein") g = Math.max(g, 2.2);
    if (split === "keto") g = Math.min(g, 1.8);
    var pK = g * refKg * 4, fK, cK, dropped = false;
    if (split === "low_carb" || split === "keto") {
      cK = (split === "keto" ? 0.10 : 0.25) * kcal;
      fK = kcal - pK - cK;
      if (fK < 0.2 * kcal) { fK = 0.2 * kcal; pK = Math.max(0, kcal - cK - fK); dropped = true; }
    } else {
      fK = (FAT_PCT[i.goal] || 0.275) * kcal;
      cK = kcal - pK - fK;
      if (cK < 0) {
        fK = 0.2 * kcal; cK = kcal - pK - fK; dropped = true;
        if (cK < 0) { pK = kcal * 0.4; cK = kcal - pK - fK; }
      }
    }
    return { kcal: kcal, protein: Math.round(pK / 4), carbs: Math.round(cK / 4), fat: Math.round(fK / 9),
             refKg: refKg, gPerKg: g, fatDropped: dropped };
  }

  function water(i, kcal) {
    var ai = i.age > 0 && i.age < 14 ? null : (i.sex === "m" ? 2500 : 2000);   /* adults only on the site */
    var floor = Math.round((ai || 2000) * 0.8);
    var base = kcal * (WATER_RATIO[i.activity] || WATER_RATIO.light) * 0.8;
    var capped = Math.min(base, 4000);
    return { ml: Math.round(Math.max(capped, floor)), floor: floor, base: base, atFloor: capped < floor, atCap: base > 4000,
             ratio: WATER_RATIO[i.activity] || WATER_RATIO.light };
  }

  function healthy(h) { var h2 = Math.pow(h / 100, 2); return { min: Math.round(18.5 * h2), max: Math.round(24.9 * h2) }; }

  function bmiBand(b) {
    return b < 18.5 ? 0 : b < 25 ? 1 : b < 30 ? 2 : b < 35 ? 3 : b < 40 ? 4 : 5;
  }

  /* ─── formatting ─── */
  function fmt(x, lang, dec) {
    if (x == null || !isFinite(x)) return "—";
    var s = Number(x).toFixed(dec || 0), p = s.split(".");
    var th = lang === "en" ? "," : ".", dp = lang === "en" ? "." : ",";
    /* Spanish keeps the thousands dot in four-digit numbers (1.200 kcal),
       as the app and the rest of the site print them. */
    p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, th);
    return p.join(dp);
  }

  /* ─── one compute per calculator: inputs -> { out: {key: text}, warn: [keys], bars, band } ─── */
  var KINDS = {
    tdee: function (i, L) {
      var p = plan(i);
      var lose = function (kg) { var r = plan(merge(i, { goal: "lose", pace: kg, target: 0 })); return r; };
      var l25 = lose(0.25), l50 = lose(0.5), g25 = plan(merge(i, { goal: "gain", pace: 0.25, target: 0 }));
      var mt = Math.round(p.tdee);
      return { main: mt, out: { main: fmt(mt, L), bmr: fmt(Math.round(p.bmr), L), lose25: fmt(l25.kcal, L), lose50: fmt(l50.kcal, L),
               gain25: fmt(g25.kcal, L), floor: fmt(p.floor, L), bridge: fmt(mt, L) },
               warn: l50.floored ? ["floor"] : [] };
    },
    deficit: function (i, L) {
      var p = plan(merge(i, { goal: "lose" }));
      var warn = [];
      if (!(i.target > 0) || i.target >= i.weight - 0.4) warn.push("notlose");
      var deficit = Math.max(0, p.tdee - p.kcal);
      var kgWeek = deficit * 7 / KCAL_PER_KG;
      var pct = kgWeek / i.weight * 100;
      var weeks = kgWeek > 0 && p.kgToGo < Infinity ? p.kgToGo / kgWeek : null;
      if (p.floored) warn.push("floor");
      if (pct > 1) warn.push("fast");
      if (p.capped && !p.floored) warn.push("capped");
      if (i.target > 0 && bmiOf(i.height, i.target) < 18.5) warn.push("lowbmi");
      return { main: p.kcal, out: { main: fmt(p.kcal, L), tdee: fmt(Math.round(p.tdee), L), deficit: fmt(Math.round(deficit), L),
               kgweek: fmt(kgWeek, L, 2), pct: fmt(pct, L, 2), weeks: weeks ? fmt(Math.ceil(weeks), L) : "—",
               months: weeks ? fmt(weeks / 4.345, L, 1) : "—", floor: fmt(p.floor, L), bridge: fmt(p.kcal, L),
               hmin: fmt(healthy(i.height).min, L) }, warn: warn };
    },
    bmi: function (i, L) {
      var b = bmiOf(i.height, i.weight), hw = healthy(i.height);
      return { main: Math.round(b * 10) / 10, band: bmiBand(b), out: { main: fmt(b, L, 1), lo: fmt(hw.min, L), hi: fmt(hw.max, L) },
               cat: bmiBand(b), warn: [] };
    },
    protein: function (i, L) {
      var m = macros({ goal: i.goal, height: i.height, weight: i.weight }, 2000);
      var g = Math.round(m.gPerKg * m.refKg);
      return { main: g, out: { main: fmt(g, L), gkg: fmt(m.gPerKg, L, 1), ref: fmt(m.refKg, L, 1),
               lo: fmt(Math.round(1.2 * m.refKg), L), hi: fmt(Math.round(2.0 * m.refKg), L),
               efsa: fmt(Math.round(0.83 * i.weight), L), meal3: fmt(Math.round(g / 3), L), meal4: fmt(Math.round(g / 4), L),
               bridge: fmt(g, L) }, warn: m.refKg < i.weight - 0.05 ? ["ref"] : [] };
    },
    macros: function (i, L) {
      var p = plan(i);
      var k = p.macroKcal, pk = p.protein * 4, ck = p.carbs * 4, fk = p.fat * 9, tot = pk + ck + fk || 1;
      var warn = [];
      if (p.floored && !(i.kcal > 0)) warn.push("floor");
      if (p.fatDropped) warn.push("dropped");
      return { main: k, out: { main: fmt(k, L), p: fmt(p.protein, L), c: fmt(p.carbs, L), f: fmt(p.fat, L),
               pk: fmt(pk, L), ck: fmt(ck, L), fk: fmt(fk, L),
               pp: fmt(pk / tot * 100, L), cp: fmt(ck / tot * 100, L), fp: fmt(fk / tot * 100, L),
               tdee: fmt(Math.round(p.tdee), L), floor: fmt(p.floor, L), bridge: fmt(k, L) },
               bars: { p: pk / tot * 100, c: ck / tot * 100, f: fk / tot * 100 }, warn: warn };
    },
    water: function (i, L) {
      var p = plan(i), w = water(i, p.kcal);
      var warn = [];
      if (w.atFloor) warn.push("floor");
      if (w.atCap) warn.push("cap");
      return { main: w.ml, out: { main: fmt(w.ml / 1000, L, 1), ml: fmt(w.ml, L), glasses: fmt(Math.max(1, Math.ceil(w.ml / 250 - 1e-6)), L),
               kcal: fmt(p.kcal, L), ratio: fmt(w.ratio, L, Math.round(w.ratio * 100) % 10 ? 2 : 1), wfloor: fmt(w.floor, L), bridge: fmt(w.ml / 1000, L, 1) }, warn: warn };
    },
    bmr: function (i, L) {
      var mf = mifflin(i.sex, i.age, i.height, i.weight), bf = saneBf(i.bf);
      var b = bf != null ? katch(i.weight, bf) : mf;
      var o = { main: fmt(Math.round(b), L), mifflin: fmt(Math.round(mf), L), katch: bf != null ? fmt(Math.round(katch(i.weight, bf)), L) : "—",
                bridge: fmt(Math.round(b * FACTOR.light), L) };
      for (var k in FACTOR) o["t_" + k] = fmt(Math.round(b * FACTOR[k]), L);
      return { main: Math.round(b), out: o, warn: bf != null ? ["katch"] : [] };
    },
    healthy: function (i, L) {
      var hw = healthy(i.height), b = i.weight > 0 ? bmiOf(i.height, i.weight) : null;
      var warn = [], gap = 0;
      if (b != null) {
        if (i.weight < hw.min) { warn.push("under"); gap = hw.min - i.weight; }
        else if (i.weight > hw.max) { warn.push("over"); gap = i.weight - hw.max; }
        else warn.push("inside");
      }
      return { main: hw.min + "-" + hw.max, out: { main: fmt(hw.min, L) + "–" + fmt(hw.max, L), lo: fmt(hw.min, L), hi: fmt(hw.max, L),
               bmi: b != null ? fmt(b, L, 1) : "—", gap: fmt(gap, L, 1), mid: fmt(Math.round(22 * Math.pow(i.height / 100, 2)), L) }, warn: warn };
    }
  };

  function merge(a, b) { var o = {}, k; for (k in a) o[k] = a[k]; for (k in b) o[k] = b[k]; return o; }

  /* the inputs each kind needs, with the defaults the pages are rendered with */
  var DEFAULTS = { sex: "f", age: 35, height: 165, weight: 70, activity: "light", goal: "lose", pace: 0.5,
                   target: 63, bf: null, split: "balanced", kcal: null };
  /* a different starting goal where it reads better: water and protein for
     someone keeping their weight is the common question */
  var KIND_DEFAULTS = { water: { goal: "maintain" }, protein: { goal: "maintain" } };
  var NEEDS = {
    tdee: ["sex", "age", "height", "weight", "activity"],
    deficit: ["sex", "age", "height", "weight", "activity", "target", "pace"],
    bmi: ["height", "weight"],
    protein: ["height", "weight", "goal"],
    macros: ["sex", "age", "height", "weight", "activity", "goal", "pace", "split", "kcal"],
    water: ["sex", "age", "height", "weight", "activity", "goal"],
    bmr: ["sex", "age", "height", "weight", "bf"],
    healthy: ["height", "weight"]
  };
  var RANGE = { age: [18, 90], height: [130, 230], weight: [35, 250], target: [35, 250], bf: [3, 60], kcal: [1000, 6000] };
  var CHOICES = { sex: ["f", "m"], activity: ["sedentary", "light", "standing", "active", "hard"],
                  goal: ["lose", "maintain", "gain", "build_muscle"], pace: ["0.25", "0.5", "0.75"],
                  split: ["balanced", "high_protein", "low_carb", "keto"] };
  /* URL parameter names per page language; both sets are read on every page */
  var PARAM = {
    es: { sex: "sexo", age: "edad", height: "altura", weight: "peso", activity: "actividad", goal: "objetivo",
          pace: "ritmo", target: "meta", bf: "grasa", split: "reparto", kcal: "kcal" },
    en: { sex: "sex", age: "age", height: "height", weight: "weight", activity: "activity", goal: "goal",
          pace: "pace", target: "target", bf: "bodyfat", split: "split", kcal: "kcal" }
  };
  var VALUE_ALIAS = { mujer: "f", hombre: "m", woman: "f", man: "m", female: "f", male: "m",
                      perder: "lose", mantener: "maintain", ganar: "gain", musculo: "build_muscle", "músculo": "build_muscle" };

  function clean(key, v) {
    if (v == null || v === "") return null;
    v = String(v).trim().toLowerCase();
    if (VALUE_ALIAS[v]) v = VALUE_ALIAS[v];
    if (CHOICES[key]) {
      if (key === "pace") { var n0 = parseFloat(v.replace(",", ".")); v = isFinite(n0) ? String(n0) : v; }
      return CHOICES[key].indexOf(v) >= 0 ? (key === "pace" ? parseFloat(v) : v) : null;
    }
    var n = parseFloat(v.replace(",", "."));
    var r = RANGE[key];
    return isFinite(n) && (!r || (n >= r[0] && n <= r[1])) ? n : null;
  }

  function compute(kind, input, lang) {
    var i = merge(DEFAULTS, KIND_DEFAULTS[kind] || {});
    for (var k in input) if (input[k] != null) i[k] = input[k];
    if (NEEDS[kind].indexOf("target") < 0) i.target = 0;
    if (NEEDS[kind].indexOf("pace") < 0) i.pace = 0.5;
    if (NEEDS[kind].indexOf("kcal") < 0) i.kcal = null;
    if (NEEDS[kind].indexOf("goal") < 0 && kind !== "deficit") i.goal = "maintain";
    if (NEEDS[kind].indexOf("split") < 0) i.split = "balanced";
    if (NEEDS[kind].indexOf("bf") < 0) i.bf = null;
    return KINDS[kind](i, lang || "es");
  }

  var CALC = { FACTOR: FACTOR, WATER_RATIO: WATER_RATIO, PROTEIN_G_PER_KG: PROTEIN_G_PER_KG, FAT_PCT: FAT_PCT, FLOOR: FLOOR,
               mifflin: mifflin, katch: katch, plan: plan, macros: macros, water: water, healthy: healthy, bmiOf: bmiOf,
               bmiBand: bmiBand, fmt: fmt, compute: compute, DEFAULTS: DEFAULTS, KIND_DEFAULTS: KIND_DEFAULTS, NEEDS: NEEDS, PARAM: PARAM, clean: clean };

  if (typeof module !== "undefined" && module.exports) { module.exports = CALC; return; }
  if (typeof document === "undefined") return;

  /* ─── the page ─────────────────────────────────────────────────────── */
  var KEY = "fc_calc";
  var SHARED = ["sex", "age", "height", "weight", "activity"];
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { /* storage blocked */ } }

  function fromUrl() {
    var q = {}, s = location.search.replace(/^\?/, "").split("&");
    s.forEach(function (kv) {
      if (!kv) return;
      var p = kv.split("="), name = decodeURIComponent(p[0] || "").toLowerCase(), val = decodeURIComponent((p[1] || "").replace(/\+/g, " "));
      ["es", "en"].forEach(function (l) { for (var k in PARAM[l]) if (PARAM[l][k] === name) q[k] = val; });
    });
    return q;
  }

  function field(form, key) { return form.elements[key]; }

  function setField(form, key, v) {
    var el = field(form, key);
    if (!el || v == null) return;
    if (el.length && el[0] && el[0].type === "radio") {
      for (var j = 0; j < el.length; j++) el[j].checked = el[j].value === String(v);
    } else if (el.tagName === "SELECT") {
      var sv = String(v);
      for (var o = 0; o < el.options.length; o++) if (parseFloat(el.options[o].value) === parseFloat(sv) || el.options[o].value === sv) el.value = el.options[o].value;
    } else {
      el.value = String(v).replace(".", el.getAttribute("data-dec") === "," ? "," : ".");
    }
  }

  function readField(form, key) {
    var el = field(form, key);
    if (!el) return null;
    var v = (el.length && el[0] && el[0].type === "radio")
      ? (form.querySelector('input[name="' + key + '"]:checked') || {}).value
      : el.value;
    return clean(key, v);
  }

  function init(form) {
    var kind = form.getAttribute("data-calc");
    var lang = document.documentElement.lang === "en" ? "en" : "es";
    var needs = NEEDS[kind];
    var stored = load(), url = fromUrl();
    needs.forEach(function (k) {
      var v = url[k] != null ? clean(k, url[k]) : null;
      if (v == null && SHARED.indexOf(k) >= 0) v = clean(k, stored[k]);
      if (v != null) setField(form, k, v);
    });
    var out = document.querySelector('[data-calc-out="' + kind + '"]');
    var share = document.querySelector("[data-calc-share]");

    function run(userChange) {
      var input = {}, bad = false;
      needs.forEach(function (k) {
        var el = field(form, k);
        var v = readField(form, k);
        var optional = k === "bf" || k === "kcal" || (k === "weight" && kind === "healthy");
        var raw = el && !(el.length && el[0] && el[0].type === "radio") ? String(el.value).trim() : "x";
        if (v == null && !(optional && raw === "")) { bad = true; if (el && el.setAttribute && raw !== "") el.setAttribute("aria-invalid", "true"); }
        else if (el && el.removeAttribute) el.removeAttribute("aria-invalid");
        input[k] = v;
      });
      if (kind === "healthy" && input.weight == null) input.weight = 0;
      if (bad) { out.setAttribute("data-stale", ""); return; }
      out.removeAttribute("data-stale");
      var r = compute(kind, input, lang);
      Object.keys(r.out).forEach(function (k) {
        var els = out.querySelectorAll('[data-out="' + k + '"]');
        for (var j = 0; j < els.length; j++) els[j].textContent = r.out[k];
      });
      var ws = document.querySelectorAll("[data-warn]");
      for (var j = 0; j < ws.length; j++) ws[j].hidden = r.warn.indexOf(ws[j].getAttribute("data-warn")) < 0;
      if (r.bars) ["p", "c", "f"].forEach(function (k) {
        var b = out.querySelector('[data-bar="' + k + '"]'); if (b) b.style.width = r.bars[k].toFixed(1) + "%";
      });
      if (r.cat != null) {
        var cats = out.querySelectorAll("[data-cat]");
        for (var c = 0; c < cats.length; c++) cats[c].hidden = String(r.cat) !== cats[c].getAttribute("data-cat");
        var rows = document.querySelectorAll("[data-bmi-band]");
        for (var rr = 0; rr < rows.length; rr++) rows[rr].classList.toggle("is-this", String(r.cat) === rows[rr].getAttribute("data-bmi-band"));
      }
      if (userChange) {
        var s = load();
        SHARED.forEach(function (k) { if (input[k] != null) s[k] = input[k]; });
        save(s);
        /* a shareable address for exactly these inputs, without a reload */
        var parts = [];
        needs.forEach(function (k) { if (input[k] != null && !(kind === "healthy" && k === "weight" && !input[k])) parts.push(PARAM[lang][k] + "=" + encodeURIComponent(input[k])); });
        try { history.replaceState(null, "", location.pathname + "?" + parts.join("&") + location.hash); } catch (e) { /* file:// */ }
      }
    }
    form.addEventListener("input", function () { run(true); });
    form.addEventListener("change", function () { run(true); });
    form.addEventListener("submit", function (e) { e.preventDefault(); run(true); });
    run(false);

    if (share) share.addEventListener("click", function () {
      run(true);
      var done = function () { share.setAttribute("data-copied", ""); setTimeout(function () { share.removeAttribute("data-copied"); }, 2200); };
      try { navigator.clipboard.writeText(location.href).then(done, done); } catch (e) { done(); }
    });
  }

  /* Phones: a slim download bar once the result card has scrolled away, so it
     never sits over the inputs. Fixed position, so it moves nothing. */
  function stickyBar() {
    var bar = document.querySelector(".calc-sticky"), card = document.querySelector(".calc-out");
    if (!bar || !card || !("IntersectionObserver" in window)) return;
    var seen = false;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) seen = true;
        bar.classList.toggle("is-on", seen && !e.isIntersecting && e.boundingClientRect.top < 0);
      });
    }).observe(card);
  }

  function boot() {
    var forms = document.querySelectorAll("form[data-calc]");
    for (var i = 0; i < forms.length; i++) init(forms[i]);
    stickyBar();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
