#!/usr/bin/env bash
# Turn a checkout of the web-redesign branch into the PREVIEW site.
#
#     bash tools/preview/prepare.sh <checkout-dir> <out-dir> <sha>
#
# Run by the workflow in the fotocal/fotocal.github.io repository (a copy
# of that workflow lives next to this file). What it changes, and why:
#
#   CNAME          removed. Left in, the preview repo would claim
#                  getfotocal.com and GitHub would have two sites fighting
#                  over the live domain. This line is the one that protects
#                  the live site.
#   sitemap.xml    removed — nothing to submit.
#   robots.txt     replaced with Disallow: / for every agent.
#   every .html    gets <meta name="robots" content="noindex, nofollow">
#                  as the first thing in <head>, so a stray link cannot get
#                  a half-finished page into Google.
#   src/ tools/ .github/   not copied — build inputs, raw captures and
#                  workflows are not part of any site.
#   .preview-sha   the commit the preview was built from, so the scheduler
#                  can skip a rebuild when nothing changed, and so anyone
#                  can check which commit they are looking at.
set -euo pipefail
src="$1"; out="$2"; sha="$3"
rm -rf "$out"; mkdir -p "$out"
# copy the rendered site, nothing else
(cd "$src" && tar --exclude=./.git --exclude=./.github --exclude=./src --exclude=./tools \
                  --exclude=./CNAME --exclude=./sitemap.xml --exclude=./deploy-trigger.txt \
                  -cf - .) | (cd "$out" && tar -xf -)
printf 'User-agent: *\nDisallow: /\n' > "$out/robots.txt"
printf '%s\n' "$sha" > "$out/.preview-sha"
touch "$out/.nojekyll"
n=0; miss=0
while IFS= read -r -d '' f; do
  if grep -q '<head>' "$f"; then
    sed -i '0,/<head>/s//<head>\n  <meta name="robots" content="noindex, nofollow">/' "$f"
    n=$((n+1))
  else
    miss=$((miss+1)); echo "no <head> in $f" >&2
  fi
done < <(find "$out" -name '*.html' -print0)
[ "$miss" -eq 0 ] || { echo "prepare: $miss page(s) without <head>" >&2; exit 1; }
[ ! -e "$out/CNAME" ] || { echo "prepare: CNAME survived" >&2; exit 1; }
[ ! -e "$out/sitemap.xml" ] || { echo "prepare: sitemap survived" >&2; exit 1; }
[ ! -d "$out/src" ] && [ ! -d "$out/tools" ] || { echo "prepare: build inputs survived" >&2; exit 1; }
# every page must carry the noindex, verified on the files as written
bad=$(grep -L 'name="robots" content="noindex, nofollow"' $(find "$out" -name '*.html') | wc -l)
[ "$bad" -eq 0 ] || { echo "prepare: $bad page(s) without noindex" >&2; exit 1; }
echo "prepare: $n pages, noindex on all, CNAME and sitemap dropped, robots disallow, sha $sha"
