# Raw captures — committed, always

Every raw screenshot the founder sends is committed here BEFORE it is
framed, next to the framed version it produces. The sitting-1 home pair
was lost with a scratchpad wipe and would have needed a retake; that must
not be possible again. A re-frame (new width, new cut row, new frame
style) must never need the founder to touch his phone.

Layout and naming

    tools/captures/<sitting>/<screen>-<lang>.<ext>

    tools/captures/s1/home-es.png        raw, as received (never edited)
    tools/captures/s1/home-en.png
    tools/captures/s2/camera-plate-es.png
    tools/captures/s2/plate.jpg           the plate photo, full resolution

<lang> is es or en — the same suffix convention check 9 in
tools/check_site.py enforces on the framed assets, so a raw file and its
framed output always pair by name. A file with no language (a food photo)
carries none.

Framed outputs go to assets/img/… via tools/frame_screen.py, with the
exact command recorded in the commit message, e.g.

    python3 tools/frame_screen.py tools/captures/s1/home-es.png \
            assets/img/screens/home-hero-es.webp cut=1648 width=1200

Nothing in this directory is linked from the site.

Sitting 3 (2026-09-11) — tools/captures/s3/. The founder cannot label
files, so the names here are our reading of each capture (screen,
language, scroll position), confirmed with the intermediary before any
of them is cropped. Both batches committed as received.

Sitting 4 (2026-09-12) — tools/captures/s4/, the barcode set. The Red
Bull pair sent with it is pixel-identical to s2/barcode-{es,en}.jpg and
is not duplicated here. Files named DO-NOT-PUBLISH are kept as evidence
for tools/APP-BUGS.md (item 0) and must never reach the site: the swaps
list in both languages and the English kéfir result.
