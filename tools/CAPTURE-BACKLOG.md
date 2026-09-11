# Capture backlog — swap-when-available

Raw captures live in tools/captures/<sitting>/ (committed, always).
Framing is CSS (.dev-frame); tools/screen_crop.py makes the screen image,
with the crop row recorded in the commit.

## After sitting 3 (2026-09-11) — retakes still to come
All: light theme, the phone's own screenshot, 1080x2400, untouched, one
file per scroll position. Same state in both languages.
  1. Voice result — SPANISH and ENGLISH, three foods the app recognises
     cleanly. The sitting-3 pair is not published: "Afel" (a
     misrecognised apple) on both screens. He says exactly «Dos huevos y
     tostada con aguacate» / "Two eggs and toast with avocado" — the
     sentence the card quotes — so screen and copy match.
     Slots: home page voice card (Spanish), /features/ voice tile (Spanish).
  2. Result screen lower half — ENGLISH, the first three scroll positions
     ("Informe completo": quality score, sugar impact, satiety, NOVA,
     nutrient radar, micronutrients), to pair with Spanish
     tools/captures/s3/food-detail-lower-es-1..3.jpg.
     Slot: /features/scan-food/ "what you get" tile (src marks it).
  3. Ingredient sheet — ENGLISH, to pair with
     tools/captures/s3/ingredient-edit-es.jpg. No slot yet; a pair would
     let the "fix the amounts" step show the sheet itself.
  5. Barcode scanner screen — ENGLISH, to pair with
     tools/captures/s4/barcode-scanner-es.png (the Activia kéfir bottle,
     barcode inside the frame). Slot: /features/scan-barcode/ step 1.
  4. A second, mixed restaurant-style dish — SPANISH and ENGLISH, result
     top only, scanned from the same photo via the gallery button.
     Slot: /features/scan-food/ "in practice" (src marks it).
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
