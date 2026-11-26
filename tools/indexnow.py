#!/usr/bin/env python3
"""Tell IndexNow (Bing, Yandex, Seznam, Naver…) which pages changed in a push.

    python3 tools/indexnow.py <before-sha> <after-sha>

Run by .github/workflows/deploy.yml after the deploy. The key is the file
<key>.txt at the site root (IndexNow checks it is served there). Only pages
whose source changed are sent, both languages; a first push or a forced
history sends the sitemap's URLs instead. Never fails the deploy: IndexNow
is a hint, and an error here must not take the site down."""
import glob, json, os, re, subprocess, sys, time, urllib.error, urllib.request

# In the deploy job the script runs from a copy in /tmp (tools/ is not
# published), so the checkout is found through GITHUB_WORKSPACE.
ROOT = os.environ.get("GITHUB_WORKSPACE") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://getfotocal.com/"
HOST = "getfotocal.com"


def key():
    for f in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(f)[:-4]
        if re.fullmatch(r"[0-9a-f]{32}", name) and open(f).read().strip() == name:
            return name
    sys.exit("no IndexNow key file at the site root")


def sitemap_urls():
    return re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())


def changed_urls(before, after):
    try:
        out = subprocess.run(["git", "diff", "--name-only", before, after], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    except Exception:
        return None
    # A push that replaces the key file (26-11-2026) sends the whole sitemap,
    # so the new key is tested, and used, straight away.
    if any(re.fullmatch(r"[0-9a-f]{32}\.txt", f) for f in out):
        return None
    live = set(sitemap_urls())
    urls = set()
    for f in out:
        if f.startswith("src/") and f.endswith("index.html"):
            path = f[4:-len("index.html")]
            for u in (SITE + path, SITE + "en/" + path):
                if u in live:
                    urls.add(u)
    return sorted(urls)


def main():
    before, after = (sys.argv[1:3] + [None, None])[:2]
    urls = changed_urls(before, after) if before and not re.fullmatch(r"0+", before or "") else None
    if urls is None:
        urls = sitemap_urls()
    if not urls:
        print("IndexNow: no page changed")
        return
    k = key()
    # IndexNow answers 403 when it cannot read the key file. Right after a
    # deploy the CDN may not serve it yet (first run, 08-11-2026: 403 four
    # seconds after the deploy), so wait until the live site has it, then
    # send, and try once more a minute later if it is still refused.
    key_url = SITE + k + ".txt"
    for _ in range(18):                      # up to 3 minutes
        try:
            with urllib.request.urlopen(key_url + "?t=%d" % time.time(), timeout=15) as r:
                if r.status == 200 and r.read().decode().strip() == k:
                    break
        except Exception:
            pass
        time.sleep(10)
    else:
        print("IndexNow: the key file is not live yet; not sent (the deploy is unaffected)")
        return
    body = json.dumps({"host": HOST, "key": k, "keyLocation": key_url, "urlList": urls[:10000]}).encode()
    # 23-11-2026: two deploys in a row got 403 from api.indexnow.org with the
    # key file live. Try Bing's own endpoint too, and print the reply body,
    # which says why a key is refused.
    for attempt, endpoint in ((1, "https://api.indexnow.org/indexnow"), (2, "https://www.bing.com/indexnow")):
        req = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print("IndexNow: %d URL(s) sent to %s, HTTP %d" % (len(urls), endpoint, r.status))
                return
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300].replace("\n", " ")
            print("IndexNow: attempt %d (%s) not accepted (HTTP %d) %s" % (attempt, endpoint, e.code, detail))
        except Exception as e:
            print("IndexNow: attempt %d (%s) not accepted (%s)" % (attempt, endpoint, e))
        if attempt == 1:
            time.sleep(60)
    print("IndexNow: not sent; the deploy is unaffected")


if __name__ == "__main__":
    main()
