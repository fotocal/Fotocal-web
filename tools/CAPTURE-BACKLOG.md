# Capture backlog — swap-when-available

Raw captures live in tools/captures/<sitting>/ (committed, always).
Framing is CSS (.dev-frame); tools/screen_crop.py makes the screen image,
with the crop row recorded in the commit.

## Still to come (updated 2026-09-12)
All: light theme, the phone's own screenshot, untouched, one file per
scroll position. Same state in both languages unless it says otherwise.

  1. Voice result — SPANISH and ENGLISH, three foods the app recognises
     cleanly. The sitting-3 pair is not published: "Afel" (a
     misrecognised apple) on both screens. He says exactly «Dos huevos y
     tostada con aguacate» / "Two eggs and toast with avocado" — the
     sentence the card quotes — so screen and copy match.
     Slots: home page voice card (Spanish), /features/ voice tile
     (Spanish), /features/voice-logging/ step 4 (Spanish; the English
     one there is the clean sitting-2 capture and can stay).
  1b. Voice tab screen — SPANISH and ENGLISH, the sheet NOT open: the
     Scan / Barcode / Voice tabs, the microphone button and "Recently by
     voice". Every voice capture so far has the result sheet over it,
     dimming the screen behind. Slot: /features/voice-logging/ step 1.
  1c. The listening state — SPANISH and ENGLISH, IF the app shows one
     (a waveform, "listening…", anything between tapping the mic and the
     result). If there is no such screen, say so and the slot stays as
     it is.
  1d. Two things the page CLAIMS and no capture backs. Whichever answer
     comes back, the copy follows it:
       · the transcript. /features/voice-logging/ says twice that you
         see what it heard, written out. The result sheet shows only
         "Esto entendí" and the food cards. If a transcript is shown
         anywhere, capture it; if it is not shown, the claim comes out.
       · editing an item. The FAQ says a detected food can be edited and
         re-weighed. The cards carry a heart and a bin and no chevron.
         If tapping a card opens an editor, capture it (both languages);
         if nothing happens, the claim comes out.
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
