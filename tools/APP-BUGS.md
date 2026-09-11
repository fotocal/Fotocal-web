# App bugs observed during website work — for the next app batch

Logged here so they survive the website sessions. These are APP defects,
not website work. Do not fix from this repo; do not chase during Part 3.

## 0 · THE HEALTH SCORE FALLS BACK TO "74 · GOOD" — highest priority
Observed 2026-09-12 in the barcode captures (tools/captures/s4/, the
files marked DO-NOT-PUBLISH). Every product whose data is missing scores
exactly 74/100 "Good" / "Bueno":
  · "Try these instead" for Red Bull Sugarfree (24/100 Bad) lists, as
    healthier swaps, all at 74/100 Good: Mountain dew, Pepsi Max zero a
    la lima, Cherryade Can (Barr), Cocacola original taste, Coca-Cola
    Zero Zero, Coca Zéro, Pepsi-cola (diet) 330ml max … nine in all,
    identical in the Spanish list ("Cámbialo por · 9", 74/100 Bueno).
  · The English "kéfir" (Activia) result: Sugar "No data", Salt
    "No data" — and still 74/100 Good.
A real score would not put Coca-Cola original taste and a kéfir on the
same number. The Spanish "Kéfir natural" (Hacendado) result, whose rows
ARE filled (36 kcal, 0.0 g sugar, 0.00 g salt, 0 additives), also lands
on 74/100 — which suggests the mechanism: a missing value is scored as
if it were zero, so any product with gaps gets the best-case negatives
and the same 74 as a product that genuinely has none. The list of swaps
is then built from that number, which is how a full-sugar cola becomes
a recommended swap for a sugar-free drink. Until fixed: no product with
missing rows should carry a score, and no product should be offered as
a swap on a score it did not earn.
Separate oddity in the same capture: the English Activia kéfir is
flagged "Not suitable for you: contains Gluten / coeliac, Dairy /
lactose". Kéfir contains no gluten; the allergen mapping is wrong.
Also still present: the English Red Bull result keeps the Spanish line
"Ajustado por: alto en calorías" (sitting-2 item 1).
Website consequence: the barcode page's "swaps" section is built with
no capture and describes what the feature does, not how good the
suggestions are.

## 0b · ENGLISH STRINGS INSIDE THE SPANISH UI — second
Observed 2026-09-11, app language Spanish, Baked Chicken Bowl result and
its ingredient sheet. Spain is the primary market; a Spanish user reads
these on the screen the whole product is built around:
  · Result, "Calidad nutricional" chips:  "+ High in protein and fiber."
                                          "· Moderate sodium content."
  · Result, row summary:                  "Rico en Vitamin C"
  · Result, "Radar de nutrientes" rows:   "Vitamin C", "Potassium",
                                          "Vitamin A", "Magnesium"
  · Result, "Micronutrientes" rows:       "Potassium", "Vitamin C",
                                          "Iron", "Calcium"
  · Result top (sitting 2), chip:         "High protein"
  · Ingredient sheet, "Reemplazar por…":  "Turkey", "Tofu"
  · Barcode result, ENGLISH UI, the reverse: "Ajustado por: alto en calorías"
The nutrient names look like untranslated keys from the nutrition data
layer; the chips and replacements look like AI output that is not told
the app language (same family as items 1 and 2 below).

## 1 · Scan → Coach Kal handoff generates its question in English
Observed 2026-08-31, app language Spanish. Tapping through from a scan
composes the question bubble in English even though the whole app UI and
Kal's reply are Spanish. The reply language is right, so detection is
fine — consistent with a missing/untranslated i18n key on the prompt
template. (The Spanish website capture needed the question typed by hand.)

## 2 · Kal's Spanish replies get the calorie arithmetic wrong
Observed 2026-08-31. Identical data, both languages, chicken bowl of
905 kcal against 663 kcal remaining:
  · English reply: "it will put you over, leaving you with -242 kcal" — correct.
  · Spanish reply: "905 kcal … encaja bien con tus 663 kcal restantes" — wrong;
    905 > 663 by 242.
A second, softer Spanish sample called the 2 075 kcal daily GOAL "tus
calorías restantes" (it was the goal, not the remainder). Two Spanish
samples wrong, two English samples right — not proof of a pattern, but
enough to investigate, and Spain is the primary market. Suspect the
Spanish system/prompt template around the numeric context, not the model's
maths per se, since English gets it right from the same data.


## Seen in the sitting-2 captures (2026-09-10)
1. Barcode result, ENGLISH UI: the adjustment line is in Spanish —
   "Ajustado por: alto en calorías" under the 24/100 score (Red Bull
   sugar free). Untranslated string.
2. Menu scan, SPANISH UI: the recommendation banner and every dish note
   are in English ("Menú Plato is the best option based on the remaining
   macros.", "High in fat which exceeds the remaining macros.") while the
   buttons are translated ("Registrar plato"). The AI-generated strings
   are not following the app language.
3. Food detail, SPANISH UI: the "High protein" chip is in English.
4. Weekly report → Your goal: Start 80.0 kg · Now 110.0 kg · Goal 90.0 kg
   renders "100% done" and "20.0 kg to go" at the same time. The progress
   maths breaks when the current weight is past the start in the wrong
   direction. (Capture kept out of the website for this reason.)
5. Coach Kal's "calories remaining" (652 kcal) is goal − eaten, ignoring
   the 539 kcal burned that the home screen counts (1.191 left). Not
   wrong, but the two numbers disagree on the same day; worth one rule.

## Seen in the sitting-3 captures (2026-09-11)
5. (Detailed at the top, item 0.) Result screen, SPANISH UI, "Informe completo": the quality chips are
   in English ("+ High in protein and fiber.", "· Moderate sodium
   content."), and every nutrient name in "Radar de nutrientes" and
   "Micronutrientes" is English (Vitamin C, Potassium, Magnesium, Iron,
   Calcium; "Rico en Vitamin C"). Same family as bug 2 and 3.
6. Ingredient sheet, SPANISH UI: the "Reemplazar por…" suggestions are
   English ("Turkey", "Tofu").
7. Voice result, both languages: "apple" came back as "Afel" — the same
   misrecognition in the Spanish and the English run of the same three
   items (Cola, Afel, Malta). Shows in the capture that will go on the
   site; a retake with clearer foods would avoid publishing it.
8. Weekly report "Nutrición" table, SPANISH: row labels break mid-word
   ("Proteín a", "Carboh idratos") and a "PARTE EST" badge (partly
   estimated?) takes the label's width. The English table wraps
   "Carboh ydrates" the same way.
