# Fotocal — Marketing Website

Static marketing site for **Fotocal**, the AI-powered calorie & health tracking app for Android ([Google Play](https://play.google.com/store/apps/details?id=com.fotokal.app)).

Live: https://getfotocal.com

## Two language trees

The site is published twice, one language per URL:

| Language | URL | Notes |
|---|---|---|
| Spanish | `https://getfotocal.com/…` | the default — the market is Spain |
| English | `https://getfotocal.com/en/…` | mirrors the Spanish tree exactly |

Every page exists in both, with reciprocal `hreflang` and `x-default`
pointing at Spanish. A first-time visitor lands on Spanish with no redirect;
the switcher navigates to the same page in the other tree and remembers the
choice, which is then honoured only when someone types the bare domain — a
shared link always opens in the language its URL names.

Spanish sits on the existing slugs rather than under `/es/` because GitHub
Pages cannot issue 301s. Moving it would have broken all 71 live URLs with
nothing but meta-refresh to cover them, and slug keywords matter far less
than the title, H1 and body, all of which are Spanish now.

## Building

`src/**/*.html` are the templates. They are bilingual: text is bound to
dictionary keys with `data-i18n`, and whole blocks that only exist in one
language are marked `data-lang-block`.

```
python3 tools/build_site.py     # src/ -> the two trees + sitemap.xml
python3 tools/check_site.py     # verify what was rendered
```

`build_site.py` resolves the i18n keys, picks the right language blocks,
sets `<html lang>`, title, description, Open Graph and Twitter tags, the
self-canonical and the hreflang triple, keeps internal links inside their
own tree, localises the JSON-LD, and writes `sitemap.xml`. It strips the
build attributes, so nothing is translated in the browser.

`check_site.py` fails the build on a dead link, a tree with a missing page,
a wrong `<html lang>`, a bad canonical or hreflang set, a surviving build
attribute, an unresolved `{{i18n:…}}` token, invalid JSON-LD, or a sitemap
that disagrees with what was rendered. Over-long titles are warnings.

The deploy workflow runs both, then drops `src/` and `tools/` from the
artifact so the templates are never published.

**Edit `src/`, never the rendered output** — the builder deletes and
rewrites the output directories on every run.

## Copy

Both dictionaries live in `assets/js/`:

* `i18n.js` — nav, footer, shared CTAs, and the handful of strings the
  contact form writes at runtime. Shipped to the browser.
* `i18n-pages.js` — page copy. Build input only; not shipped, because the
  text it holds is already baked into the HTML.

The two languages are kept at exact key parity.

## Pages

| Page | Path | Purpose |
|---|---|---|
| Landing | `/` | Marketing landing |
| Features | `/features/` | Overview, plus four dedicated feature pages |
| Subscription | `/subscription/` | Plans and pricing |
| Blog | `/blog/` | 54 articles |
| About / Contact | `/about/`, `/contact/` | |
| Privacy Policy | `/privacy-policy/` | Google Play compliance (health data, AI, GDPR) |
| Terms of Service | `/terms/` | Subscriptions, auto-renewal, free trial |
| Account Deletion | `/account-deletion/` | Google Play account-deletion requirement |

## Stack

Hand-written HTML/CSS/JS with a small Python renderer — no bundler, no
framework, no dependencies. Fonts: Fraunces + Instrument Sans.

## Deployment

GitHub Pages via `.github/workflows/deploy.yml`, on every push to `main`.
