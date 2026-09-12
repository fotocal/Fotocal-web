# Capture backlog — swap-when-available

Raw captures live in tools/captures/<sitting>/ (committed, always).
Framing is CSS (.dev-frame); tools/screen_crop.py makes the screen image,
with the crop row recorded in the commit.

## Still to come (updated 2026-09-11, after sitting 6)

Six sittings have happened. Everything the site states as fact is now
backed by a real screen or by the app's own code. What is left below is
cosmetic or blocked, and NONE of it is being chased — each slot is
composed from its own content and reads as finished, not as a hole.

  A. BLOCKED by an app bug, do not capture until it is fixed:
     · the alternatives list under a barcode result (APP-BUGS 0).
     · the weekly report's goal card (APP-BUGS 0a) — the Cuerpo tab's
       goal card is on the site instead and says the same thing.

  B. Would improve a slot that already works without it:
     · the micronutrient panel AS A FREE USER SEES IT — two readable,
       the rest under the unlock. Needs a free or signed-out account, so
       it cannot come from the owner's phone as it is.
       Slot: /features/nutrition-diet/ tile 4, composed today.
     · the pace screen (0.25 / 0.5 / 0.75 and the typed figure).
       /features/weight-loss/ step 1 now shows the goal card and carries
       the pace figures in the sentence, so this is no longer needed.
     · the Cuerpo tab's weight chart with a real trend across 30 days.
       The capture we have shows two points and a BMI category label, so
       /features/weight-loss/ step 4 stays composed.
     · where "Saber más" / "Learn more" leads, tapped from under an
       answer or from the cold chat header. Nothing on the site claims
       anything about it, so nothing is wrong without it.

  C. English twins of Spanish captures already in hand. Each one would
     let a tile stop being composed; none of them changes a claim:
     · the scan result's lower half, positions 1-3
     · the ingredient sheet
     · a scored barcode result whose rows are filled
     · the barcode amount bar and the meal picker
     · a second mixed restaurant dish, both languages

## Received and in use
  Sitting 6 (2026-09-11): the voice tab at full contrast, Mi salud, Coach
  Kal opened cold, a Coach Kal dinner reply, the Cuerpo tab, and the
  allergy reply. Six pairs. What could not be published from them is
  recorded in tools/captures/s6/README.md.
  Sitting 5: the voice result pair and the listening state.
  Sitting 4: the barcode scanner, the Spanish Kéfir result, the bottle.
  Sitting 3: the weekly report tops, the result lower half 4-5.
  Sitting 2: the home screens, the meal detail, the coach chat, the menu,
  the progress tab, the activity record.

## Optional, same states as the English ones already taken
  · Home pair in the SAME header state: the English home shows the
    "Save 58%" pill, the Spanish one "Invitar". Cosmetic; swap only if
    a matching pair is easy.

## Subscription page — done 2026-09-12, no placeholders left
  The page now uses nd-day, coach-chat and sf-analysis only. It has no
  menu-scanner crop on purpose: the only menu capture (log-menu-es) has
  English AI text inside the Spanish UI (APP-BUGS sitting-2 item 2). The
  Google Play purchase sheet for each plan, ES+EN, would be the one
  capture that shows the price exactly as the store charges it; the page
  states the list prices from src/lib/pricing.ts instead.

## /ai/ social-share image
  og:image on /ai/ now points at the shared site card (assets/og-image.png)
  and the retired coach-kal illustration is deleted. A purpose-built
  1200x630 card for this page would still be better than the shared one.
