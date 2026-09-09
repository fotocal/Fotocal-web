# Capture backlog — swap-when-available

Re-captures worth taking when the moment is right. None of these blocks a
section; each is a straight swap through tools/frame_screen.py when the
new pair (ES + EN, same state) arrives. REMIND THE USER when relevant.

## P1 home screen (hero) — two cosmetic upgrades in one re-capture
  · Clear the red "19" notification badge first: an unread count reads as
    a neglected app on the most-seen pixels of the site.
  · Take it on a streak longer than "1 día" — an app that sells habit
    formation deserves a streak with some days on it. Needs a week of
    real use; do not fake it, do not edit pixels.
  2026-09-09: re-captured on the redesigned app — badge cleared (done),
  streak still "1 día". When the founder has a streak worth showing, ask
  for a fresh P1 pair and swap home-hero-es/en.webp. Current captures
  dated 2026-09-09.

## Hero — the P1 home pair again, at full resolution
  The phone now renders at up to 560 CSS px (1120 device px on a 2x
  screen) and the framed file is 840px wide, so the screen is upscaled
  ~1.3x on desktop. The raw sitting-1 captures were lost with the
  scratchpad; the founder still has them. Re-send the same ES + EN pair
  and re-run tools/frame_screen.py with width=1200 cut=<same row>.

## Device frames everywhere (owner's rule)
  Every app screen on the site sits in the device frame — the baked one
  from tools/frame_screen.py or the CSS .cam-frame, never a bare cropped
  rectangle. Sections still on bare or stale imagery, and the pair each
  needs (ES + EN, same state):
    · Three Steps step 2 — the scan RESULT screen (calories, macros,
      health score) — sitting 2
    · Log it your way (section 4) — photo-scan result, barcode result,
      menu scan, voice logging — sittings 2, 4, 5, 6
    · Coach Kal band — the chat, new design, correct maths — sitting 3
    · More than calories (section 5) — food detail with micronutrients
      and the health score — sitting 4
    · Habits (section 6) — water, steps, reminders — sitting 8
    · Progress — weight chart and the weekly share card — sitting 7
    · Subscription page — paywall and Settings → Subscription — sitting 9
    · Feature pages — each feature's key screen, same sittings

## Three Steps — the camera-with-plate frame (SITTING 2, blocks nothing but is the point of the section)
  The section is composed around the app's camera pointed at a plate.
  Until sitting 2 lands, the CSS phone frame (.cam-frame, src/index.html
  "HOW IT WORKS") holds the plate photo itself — no app UI is drawn over
  it, nothing is faked, and the section copy no longer claims "real
  screens" until they are. When the pair arrives:
    · ES + EN captures of the camera/analysing state on the SAME plate,
      saved as assets/img/steps/camera-plate-es.webp / -en.webp (raw
      capture, no baked frame — the CSS frame does that here), swapped
      into <div class="cam-screen"><img …> with data-i18n-src.
    · a plate photo of that same meal at ≥ 2000px on the long side for
      the full-bleed panel (.how-plate): step1-meal.webp is 880px wide
      and is being shown at up to ~1000 CSS px on desktop, so it is
      visibly soft on a 2x screen. Then restore "These are real screens
      from the app." to how.sub in both languages.

## Subscription page mini cards (menu scanner, unlimited voice)
  Placeholder illustrations (feat-menu.webp, feat-voice.webp) until the
  real captures from sittings 5 and 6 land — owner's call to keep them.

## /ai/ social-share image
  og:image on /ai/ still points at the retired coach-kal illustration —
  kept on the server only for this. A purpose-built 1200x630 OG card
  should replace it (a tall chat screenshot crops badly as a share card).
