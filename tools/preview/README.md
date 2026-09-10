# Preview deployment — https://fotocal.github.io/

The `web-redesign` branch is published, read-only and unindexed, at
https://fotocal.github.io/ (Spanish) and https://fotocal.github.io/en/
(English), so it can be scrolled and tapped on a real phone before
anything reaches main.

How it works
- The repository `fotocal/fotocal.github.io` holds one workflow
  (`preview.yml` here is the reference copy). Every 10 minutes it checks
  out this repository's `web-redesign` branch, renders both trees, runs
  `prepare.sh`, and deploys the result to that repository's GitHub Pages.
  It skips the deploy when the branch has not moved. It can also be run
  on demand from the Actions tab.
- `prepare.sh` is what makes it a preview and not a second live site:
  CNAME removed (so it can never claim getfotocal.com), sitemap removed,
  robots.txt = Disallow: /, and a noindex/nofollow meta on every page.
  It refuses to produce output if any of those is missing.
- The live site is untouched: its workflow runs only on pushes to `main`
  of this repository, and the preview never writes to this repository.
- Which commit is live on the preview: https://fotocal.github.io/.preview-sha

Why a user site and not a subpath or a host
- The site is built with root-relative URLs (/assets/…, /en/…), so it has
  to be served from a domain root. A project site would be a subpath. A
  user site (`<login>.github.io`) is served at the root, needs no DNS, no
  secrets and no third-party account, and costs nothing.
