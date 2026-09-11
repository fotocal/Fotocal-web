# App bugs observed during website work — for the next app batch

Logged here so they survive the website sessions. These are APP defects,
not website work. Do not fix from this repo; do not chase during Part 3.

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
5. Result screen, SPANISH UI, "Informe completo": the quality chips are
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
