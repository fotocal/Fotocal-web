# Capture backlog — swap-when-available

Raw captures live in tools/captures/<sitting>/ (committed, always).
Framing is CSS (.dev-frame); tools/screen_crop.py makes the screen image,
with the crop row recorded in the commit.

## Still missing after sitting 2 (home page and features hub)
  · Voice logging — SPANISH (assets/img/screens/log-voice-es.webp)
    What to send: the voice result screen ("Esto es lo que he entendido"
    / the list of recognised foods with calories and macros — the same
    screen as tools/captures/s2/voice-en.jpg), app in Spanish, light
    theme, phone screenshot as it comes: 1080x2400, PNG or JPG, nothing
    cropped or marked. Ideally say exactly «Dos huevos y tostada con
    aguacate», the sentence the card quotes, so screen and copy match.
    Until then the Spanish card (home page, and the same tile on
    /features/) shows its own utterance instead of a phone —
    src/index.html and src/features/index.html each mark the single
    place the capture drops in. The English card is real.
  · Weekly report — SPANISH AND ENGLISH pair
    (assets/img/screens/weekly-report-{600,900}-{es,en}.webp)
    What to send: the weekly report's summary view (the week's calories
    and macros day by day), app in Spanish and again in English, light
    theme, 1080x2400, untouched. The two English weekly captures from
    sitting 2 are not used: one shows the progress-maths bug noted in
    tools/APP-BUGS.md and neither has a Spanish twin. Until then the
    weekly tile on /features/ shows the feature's mark and what the
    report tells you — src/features/index.html marks where it drops in.
  Nothing else is needed for the home page or the features hub.

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
