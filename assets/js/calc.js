/* FOTOCAL — the four Spanish calculators (/calculadoras/, PART 47).
   Everything runs in the page: nothing is sent anywhere and there is no
   account. The body data (sex, age, height, weight, activity) is kept in
   localStorage under one key so the next calculator opens prefilled; a
   browser that blocks storage simply starts empty.

   Formulas, stated once here and in the page text:
     TMB  Mifflin-St Jeor (1990): 10·kg + 6,25·cm − 5·años + 5 (hombre) / − 161 (mujer)
     Gasto diario = TMB × factor de actividad (1,2 · 1,375 · 1,55 · 1,725 · 1,9)
     Déficit diario ≈ (peso × ritmo semanal en %) × 7.700 kcal/kg ÷ 7  (aproximación)
     IMC = kg / m²  (rangos OMS adultos)
     Macros: proteína en g/kg, grasa como % de las calorías, hidratos el resto (4/4/9 kcal/g) */
(function () {
  "use strict";
  var KEY = "fc_calc";
  var ACT = { 1.2: 1.2, 1.375: 1.375, 1.55: 1.55, 1.725: 1.725, 1.9: 1.9 };

  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { /* storage blocked */ } }
  function fmt(x, dec) {
    if (x == null || isNaN(x)) return "—";
    var s = Number(x).toFixed(dec || 0);
    var parts = s.split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return parts.join(",");
  }
  function num(el) { var v = parseFloat(String(el.value).replace(",", ".")); return isNaN(v) ? null : v; }
  function inRange(v, lo, hi) { return v != null && v >= lo && v <= hi; }
  function mifflin(sex, age, h, w) { return 10 * w + 6.25 * h - 5 * age + (sex === "m" ? 5 : -161); }
  function floorFor(sex) { return sex === "m" ? 1500 : 1200; }

  /* Reads the shared body fields of a form; null when any is missing or out of range. */
  function body(form) {
    var sexEl = form.querySelector('input[name="sex"]:checked');
    var sex = sexEl ? sexEl.value : null;
    var age = num(form.elements.age), h = num(form.elements.height), w = num(form.elements.weight);
    var act = form.elements.activity ? parseFloat(form.elements.activity.value) : null;
    if (!sex || !inRange(age, 18, 90) || !inRange(h, 130, 230) || !inRange(w, 35, 250)) return null;
    if (form.elements.activity && !ACT[act]) return null;
    save({ sex: sex, age: age, height: h, weight: w, activity: act || load().activity });
    return { sex: sex, age: age, height: h, weight: w, activity: act, bmr: mifflin(sex, age, h, w) };
  }
  function prefill(form) {
    var d = load();
    ["age", "height", "weight"].forEach(function (k) { if (form.elements[k] && d[k] != null && !form.elements[k].value) form.elements[k].value = d[k]; });
    if (d.sex) { var r = form.querySelector('input[name="sex"][value="' + d.sex + '"]'); if (r) r.checked = true; }
    if (form.elements.activity && d.activity) form.elements.activity.value = String(d.activity);
  }
  function set(id, text) { var el = document.getElementById(id); if (el) el.textContent = text; }
  function show(id, on) { var el = document.getElementById(id); if (el) el.hidden = !on; }

  /* ── calorías diarias ── */
  function tdeeCalc(form) {
    var b = body(form);
    show("out", !!b);
    if (!b) return;
    var tdee = b.bmr * b.activity;
    set("r-tdee", fmt(tdee));
    set("r-bmr", fmt(b.bmr));
    set("r-lose25", fmt(tdee - 275));
    set("r-lose50", fmt(tdee - 550));
    set("r-gain", fmt(tdee + 275));
    var fl = floorFor(b.sex);
    var low = tdee - 550 < fl;
    show("w-floor", low);
    if (low) set("w-floor-n", fmt(fl));
  }

  /* ── déficit calórico ── */
  function deficitCalc(form) {
    var b = body(form);
    var goal = num(form.elements.goal);
    var rateEl = form.querySelector('input[name="rate"]:checked');
    var rate = rateEl ? parseFloat(rateEl.value) : null;
    var ok = b && rate && inRange(goal, 0.5, 100);
    show("out", !!ok);
    if (!ok) return;
    var tdee = b.bmr * b.activity;
    var weeklyKg = b.weight * rate / 100;           // kg a perder por semana al ritmo elegido
    var deficit = weeklyKg * 7700 / 7;              // kcal/día, con 7.700 kcal por kg como aproximación
    var target = tdee - deficit;
    var fl = floorFor(b.sex);
    var weeks = goal / weeklyKg;
    set("r-tdee", fmt(tdee));
    set("r-deficit", fmt(deficit));
    set("r-target", fmt(target));
    set("r-weekly", fmt(weeklyKg, 2));
    set("r-weeks", fmt(weeks, 0));
    set("r-months", fmt(weeks / 4.33, 1));
    show("w-bmr", target < b.bmr);
    show("w-floor", target < fl);
    if (target < fl) set("w-floor-n", fmt(fl));
  }

  /* ── IMC ── */
  function bmiCalc(form) {
    var h = num(form.elements.height), w = num(form.elements.weight);
    var ok = inRange(h, 130, 230) && inRange(w, 35, 250);
    show("out", ok);
    if (!ok) return;
    var d = load(); d.height = h; d.weight = w; save(d);
    var m = h / 100, bmi = w / (m * m);
    var cat = bmi < 18.5 ? "Bajo peso" : bmi < 25 ? "Peso normal" : bmi < 30 ? "Sobrepeso" :
              bmi < 35 ? "Obesidad grado I" : bmi < 40 ? "Obesidad grado II" : "Obesidad grado III";
    set("r-bmi", fmt(bmi, 1));
    set("r-cat", cat);
    set("r-lo", fmt(18.5 * m * m, 1));
    set("r-hi", fmt(24.9 * m * m, 1));
    var rows = document.querySelectorAll("[data-bmi-row]");
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i].getAttribute("data-bmi-row").split("-");
      rows[i].classList.toggle("is-this", bmi >= parseFloat(r[0]) && bmi < parseFloat(r[1]));
    }
  }

  /* ── macros ── */
  function macroCalc(form) {
    var kcal = num(form.elements.kcal), w = num(form.elements.weight);
    var gkg = parseFloat(form.elements.protein.value), fatPct = parseFloat(form.elements.fat.value);
    var ok = inRange(kcal, 800, 6000) && inRange(w, 35, 250) && gkg > 0 && fatPct > 0;
    show("out", ok);
    if (!ok) return;
    var d = load(); d.weight = w; save(d);
    var pG = w * gkg, pK = pG * 4;
    var fK = kcal * fatPct / 100, fG = fK / 9;
    var cK = kcal - pK - fK, cG = cK / 4;
    set("r-p", fmt(pG)); set("r-pk", fmt(pK)); set("r-pp", fmt(pK / kcal * 100));
    set("r-f", fmt(fG)); set("r-fk", fmt(fK)); set("r-fp", fmt(fK / kcal * 100));
    set("r-c", fmt(Math.max(0, cG))); set("r-ck", fmt(Math.max(0, cK))); set("r-cp", fmt(Math.max(0, cK / kcal * 100)));
    show("w-carbs", cG < 50);
  }
  /* The macros page can take the maintenance from the daily-calories page. */
  function macroPrefill(form) {
    var d = load();
    if (form.elements.weight && d.weight && !form.elements.weight.value) form.elements.weight.value = d.weight;
    if (form.elements.kcal && !form.elements.kcal.value && d.sex && d.age && d.height && d.weight && d.activity) {
      form.elements.kcal.value = Math.round(mifflin(d.sex, d.age, d.height, d.weight) * d.activity);
      show("note-prefill", true);
    }
  }

  var CALCS = { tdee: tdeeCalc, deficit: deficitCalc, bmi: bmiCalc, macros: macroCalc };
  var form = document.querySelector("form[data-calc]");
  if (!form) return;
  var kind = form.getAttribute("data-calc");
  var run = CALCS[kind];
  if (!run) return;
  if (kind === "macros") macroPrefill(form); else prefill(form);
  form.addEventListener("submit", function (e) { e.preventDefault(); run(form); });
  form.addEventListener("input", function () { run(form); });
  form.addEventListener("change", function () { run(form); });
  run(form);
})();
