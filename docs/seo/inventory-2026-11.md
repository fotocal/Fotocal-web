# Page inventory (MASTER PROMPT v3, PART 0), 9 November 2026

Counted in the build output (`tools/build_site.py`, commit after b7e776a) and compared with `sitemap.xml`. No content was changed.

| Page type | ES | EN | In sitemap (ES / EN) | Noindex (ES + EN) |
|---|---|---|---|---|
| Home | 1 | 1 | 1 / 1 | 0 |
| Features (scan-food, scan-barcode, voice-logging, weight-loss, nutrition-diet, lifestyle-mindset, hub) | 7 | 7 | 7 / 7 | 2 (`/features/recipe/`, hidden feature) |
| AI page (`/ai/`) | 1 | 1 | 1 / 1 | 0 |
| Calculators | 8 | 8 | 8 / 8 | 0 |
| Calculator hub | 1 | 1 | 1 / 1 | 0 |
| Dish pages `/calorias/<dish>/` | **58** | **58** | 58 / 58 | 0 |
| `/calorias/` hub + `tabla-de-calorias` | 2 | 2 | 2 / 2 | 0 |
| Blog posts | 62 | 62 | 62 / 62 | 4 (2 old redirect stubs per language) |
| Blog index + series hubs | 4 | 4 | 4 / 4 | 12 (6 thin series hubs per language) |
| Guías | 1 | 1 | 1 / 1 | 0 |
| Comparativa (hub + 3 vs-pages) | 4 | 4 | 4 / 4 | 0 |
| Metodología | 1 | 1 | 1 / 1 | 0 |
| Widget (+ `/embed/` iframes) | 1 | 1 | 1 / 1 | 4 (embeds, noindex by design) |
| About, contact, FAQ, subscription | 4 | 4 | 4 / 4 | 0 |
| Legal (privacy, terms, account deletion) | 3 | 3 | 3 / 3 | 0 |
| **Total indexable** | **158** | **158** | **316** | 22 |

## Findings

- **The sitemap and the build match exactly:** 316 indexable pages, 316 sitemap URLs. No page is missing from the sitemap, and the sitemap lists no page that isn't built. `tools/check_site.py` fails the build if that ever changes.
- **There are 58 dish pages per language, not 218.** The live sitemap of 9 Nov morning showed 60 `/calorias/` URLs per language: 58 dishes, plus the hub, plus `tabla-de-calorias`, i.e. 59 dish-looking URLs plus the table. The hub's "58 platos" is correct; it counts only dish pages.
- **The "218" is the food table.** `/calorias/tabla-de-calorias/` lists the app's **218 foods and dishes** in one table (one row each, 222 table rows including headers). Those 218 are not separate pages.
- **Room to grow:** 134 more app foods have figures that could become dish pages. The weekly routine adds 2–3 a week from `dish-priority.txt` while indexing catches up.
- **Search Console (owner's numbers, Nov 2026):** 130 indexed + 90 not indexed = 220 pages known to Google, out of 316 submitted. About 96 pages are not yet discovered. Most of those are the newest: the EN twins, comparison pages and dish pages from 7–9 Nov.
- **The not-indexed reasons are unknown** until the export below arrives. Possible causes on our side:
  - the 22 noindex pages, which are deliberate;
  - "Discovered – currently not indexed" on new pages, which is normal for a young site and fixed by internal links and time;
  - Spanish/English twins Google treats as alternates.

## Exports needed (the owner's assistant, 10 minutes)

Put the files in `docs/seo/gsc/2026-11/` (upload steps: `docs/seo/ASSISTANT.md`, task M1).

1. **Performance:** Search Console → Rendimiento → Resultados de búsqueda → date **Últimos 3 meses** → Exportar → CSV. One zip, with `Consultas.csv`, `Páginas.csv` and others.
2. **Indexing reasons:** Search Console → Indexación → Páginas → "Por qué no se indexan las páginas". Open **each reason** in the table, then Exportar → CSV. Name each file after the reason, e.g. `descubierta-no-indexada.csv`.
3. **Generative AI performance report, if the menu shows it** (under Rendimiento): Exportar → CSV.

Until these arrive, the rollout uses the default order in section C (PART 3 = calculators batch 1).
