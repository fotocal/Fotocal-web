# Capture backlog — swap-when-available

Raw captures live in tools/captures/<sitting>/ (committed, always).
Framing is CSS (.dev-frame); tools/screen_crop.py makes the screen image,
with the crop row recorded in the commit.

## Sitting 3 — one list, everything still missing (2026-09-11)
All: light theme, the phone's own screenshot, 1080x2400, untouched, one
file per scroll position (no stitched long captures). Same state in both
languages where a pair is asked for.

  1. Voice result — SPANISH only (log-voice-es.webp). The screen after
     speaking: the list of recognised foods with calories and macros
     (the same screen as tools/captures/s2/voice-en.jpg). Say exactly
     «Dos huevos y tostada con aguacate» — the sentence the card quotes.
     Used by: home page bento card, /features/ capture tile.
  2. Weekly report summary — SPANISH and ENGLISH. The report's summary
     view: the week's calories and macros day by day. (The sitting-2
     English weekly captures are unused: one shows the progress-maths
     bug in tools/APP-BUGS.md, neither has a Spanish twin.)
     Used by: /features/ weekly tile.
  3. Result screen, LOWER HALF — SPANISH and ENGLISH. The same Baked
     Chicken Bowl result, scrolled past the fibre/sugar/sat-fat/sodium
     row: whatever the app shows there — micronutrients, NOVA level,
     glycemic load, allergens, the coach summary and the swap. One
     screenshot per scroll position until the end of the screen. If any
     of these lives on a separate screen, capture that screen instead
     and say which one. Used by: /features/scan-food/ "what you get".
  4. Portion adjustment — SPANISH and ENGLISH. The control the app shows
     for changing the amount after a scan (the ≈ 450 g), mid-adjustment
     if it is a slider. If a "split between people" option exists, one
     capture with it visible; if it does not, say so — the page text
     claims it and will be corrected.
  5. Ingredient editing — SPANISH and ENGLISH. The screen after tapping
     a detected ingredient row (e.g. Pollo 150 g): where it can be
     changed, re-weighed or removed.
  6. A second, mixed dish — SPANISH and ENGLISH, result screen top only.
     A restaurant-style plate with no obvious portions (paella, curry,
     tapas), scanned from the same photo via the gallery button in each
     language. Used by: /features/scan-food/ "in practice".
  Optional, only if it exists as a distinct screen: the "analysing"
  moment between the camera and the result, Spanish and English.

## Optional, same states as the English ones already taken
  · Home pair in the SAME header state: the English home shows the
    "Save 58%" pill, the Spanish one "Invitar". Cosmetic; swap only if
    a matching pair is easy.

## Subscription page mini cards (menu scanner, unlimited voice)
  Placeholder illustrations (feat-menu.webp, feat-voice.webp) until the
  page is redone — the real menu and voice crops now exist in
  assets/img/screens/ and can be reused there.

## /ai/ social-share image
  og:image on /ai/ still points at the retired coach-kal illustration —
  kept on the server only for this. A purpose-built 1200x630 OG card
  should replace it.
