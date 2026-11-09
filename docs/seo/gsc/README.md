# Search Console exports

One folder per month, uploaded by the owner's assistant on the first Monday (`docs/seo/ASSISTANT.md`, task M1):

    docs/seo/gsc/2026-12/Queries.csv
    docs/seo/gsc/2026-12/Pages.csv
    docs/seo/gsc/2026-12/indexing.txt   (two lines: "indexed: N" and "not indexed: N")

The monthly routine reads the newest folder, then fills in `kpis.md` and writes `monthly-report.md`. Nothing here is published on the website: the deploy drops `docs/`.
