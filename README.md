# Fotocal — Marketing Website

Static marketing site for **Fotocal**, the AI-powered calorie & health tracking app for Android ([Google Play](https://play.google.com/store/apps/details?id=com.fotokal.app)).

## Pages

| Page | Path | Purpose |
|---|---|---|
| Landing | `/` | Marketing landing (ES default, EN toggle) |
| Privacy Policy | `/privacy-policy/` | Google Play compliance (health data, AI, GDPR) |
| Terms of Service | `/terms/` | Subscriptions, auto-renewal, free trial |
| Account Deletion | `/account-deletion/` | Google Play account-deletion requirement |

## Stack

Pure static HTML/CSS/JS — no build step. Fonts: Fraunces + Instrument Sans (Google Fonts).
Language toggle (ES/EN) persisted in `localStorage`.

## Deployment

Deployed to GitHub Pages via `.github/workflows/deploy.yml` on every push to `main`.

Live: https://fotocal.github.io/Fotocal-web/
