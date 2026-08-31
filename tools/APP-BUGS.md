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
