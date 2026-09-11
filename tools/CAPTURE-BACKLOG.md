# Capture backlog — swap-when-available

Raw captures live in tools/captures/<sitting>/ (committed, always).
Framing is CSS (.dev-frame); tools/screen_crop.py makes the screen image,
with the crop row recorded in the commit.

## Still to come (updated 2026-09-12)
All: light theme, the phone's own screenshot, untouched, one file per
scroll position. Same state in both languages unless it says otherwise.

  1. DONE (sitting 5). The voice result pair and the listening state
     arrived in both languages and are on the site: the home card, the
     hub tile and /features/voice-logging/ steps 2 and 4.
  1b. Voice tab screen — SPANISH and ENGLISH, with NO sheet open: the
     Scan / Barcode / Voice tabs, the microphone button and the recent
     list. Every capture so far has a sheet over it, dimming that screen,
     and a greyed-out UI reads as disabled. Slot: /features/voice-logging/
     step 1 (src marks it). Careful: the recent list must not show the
     misheard "Cafea +3" row — log something over it first, or scroll.
  2. Result screen lower half — ENGLISH, the first three scroll positions
     ("Informe completo": quality score, sugar impact, satiety, NOVA,
     nutrient radar, micronutrients), to pair with Spanish
     tools/captures/s3/food-detail-lower-es-1..3.jpg.
     Slot: /features/scan-food/ "what you get" tile (src marks it).
  3. Ingredient sheet — ENGLISH, to pair with
     tools/captures/s3/ingredient-edit-es.jpg. No slot yet; a pair would
     let the "fix the amounts" step show the sheet itself.
  4. A second, mixed restaurant-style dish — SPANISH and ENGLISH, result
     top only, scanned from the same photo via the gallery button.
     Slot: /features/scan-food/ "in practice" (src marks it).
  5. A scored barcode result in ENGLISH whose rows are filled — a product
     the database actually knows, so no row reads "No data". To pair with
     tools/captures/s4/barcode-kefir-es.jpg.
     Slot: /features/scan-barcode/ "the score" (src marks it). Until it
     arrives the English tile is composed from the page's own words. The
     English Activia kéfir result must NOT be used for this: see
     tools/APP-BUGS.md item 0.
  6. The amount bar and the meal picker on a barcode result — SPANISH and
     ENGLISH. The amount control lives in a fixed bar at the very bottom
     of the result, so it needs the result scrolled to its end (or the
     sheet, if tapping it opens one).
     Slots: /features/scan-barcode/ steps 3 and 4 (src marks both).
  7. BLOCKED, do not capture yet: the alternatives list under a result.
     The list the app builds today is wrong (tools/APP-BUGS.md item 0),
     so nothing goes in that slot until the score is fixed.

Received and in use from sitting 4: the barcode scanner in both
languages, the Spanish Kéfir natural result, the bottle photograph.
Received and in use from sitting 3: weekly report top (both languages,
different weeks — accepted), result lower half positions 4 and 5 (both
languages), Spanish positions 1–3 and the Spanish ingredient sheet
(committed, waiting for their English twins).

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
