# Capture backlog — swap-when-available

Raw captures live in tools/captures/<sitting>/ (committed, always).
Framing is CSS (.dev-frame); tools/screen_crop.py makes the screen image,
with the crop row recorded in the commit.

## Still missing after sitting 2 (home page)
  · Voice logging — SPANISH (assets/img/screens/log-voice-es.webp)
    What to send: the voice result screen ("Esto es lo que he entendido"
    / the list of recognised foods with calories and macros — the same
    screen as tools/captures/s2/voice-en.jpg), app in Spanish, light
    theme, phone screenshot as it comes: 1080x2400, PNG or JPG, nothing
    cropped or marked. Ideally say exactly «Dos huevos y tostada con
    aguacate», the sentence the card quotes, so screen and copy match.
    Until then the Spanish card shows its own utterance instead of a
    phone — src/index.html marks the single place the capture drops in
    and the exact crop command. The English card is real. The barcode
    pair is complete. Nothing else is needed for the home page.

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
