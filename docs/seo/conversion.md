# Conversion: from a visit to an install

## UTM tags, by page type

Every Google Play link on the site carries `utm_source=web`. The `utm_medium` says what kind of page sent the visitor, so Play Console → Store listing acquisition shows which pages convert.

| utm_medium | Where | utm_campaign |
|---|---|---|
| `tool` | download card under a calculator result | the calculator slug, e.g. `calorias-diarias`; `<slug>-sticky` for the phone bar; `hub` for the calculator hub |
| `dish` | download card on a dish page and the dish hub | the dish slug (`-en` for English pages); `hub` |
| `compare` | the comparison pages | `vs-myfitnesspal`, `vs-yazio`, `vs-cal-ai` |
| `home`, `features`, `blog`, `subscription`, `about`, `ai`, `faq`, `guias`, `metodologia`, … | every other Play link (header, footer, phone bar, hero buttons), tagged by the build | the page path and language, e.g. `features-scan-food-es` |

Tags are added by `tools/build_site.py` (`tag_play_links`). Links that already carry tags keep them.

## Two copy variants to test (A/B ready)

Test one thing at a time, for at least 4 weeks or 1,000 visits per variant, and compare installs per visit by `utm_campaign`. The site has no A/B tool, so run them one after the other and compare equal periods. Avoid holidays and launches.

### Home hero

- **A (current):**
  - Title: "Una foto. Toda tu nutrición, al instante."
  - Text: "Haz una foto de tu comida y ten las calorías, los macros y una puntuación de salud en segundos. Gratis, sin tarjeta: 2 escaneos con IA al día, código de barras y Coach Kal sin límite."
- **B (Spanish-food angle):**
  - Title: "Cuenta las calorías de tu tortilla con una foto."
  - Text: "Fotocal conoce la comida española con raciones reales: haz una foto y tendrás las calorías y los macros en segundos. Gratis, sin tarjeta: 2 escaneos con IA al día, 1 registro por voz al día, código de barras y Coach Kal sin límite."

### Download card button

- **A (current):** "Descárgala gratis", with the line "Gratis · sin tarjeta · Android".
- **B (outcome first):** "Pruébala con tu próxima comida", with the line "Gratis · sin tarjeta · Android".

Whichever variant runs, all four free-plan limits stay on the same screen as the word "gratis".

## Header button on phones

A small "App" pill with the Google Play mark sits next to the menu button on screens under 1,024 px. It is one tap to the store, without covering anything. It is hidden on desktop, where the menu already has room.
