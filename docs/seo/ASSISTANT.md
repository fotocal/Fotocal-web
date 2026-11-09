# SEO browser tasks for the owner's assistant

Claude runs the SEO plan for getfotocal.com. Every Monday it publishes a blog post and new dish pages, refreshes an older page and confirms the deploy. On the first Monday of each month it also writes a short report. Claude has no browser logins, so a few steps need a person in the owner's Chrome. This file lists all of them. You never need to edit the website itself.

Everything happens in the owner's Chrome, signed in to the Fotocal Google account (the one that owns the Play listing and Search Console).

**Three rules**
1. Copy texts exactly as written in the files. Don't add numbers, ratings, download counts, reviews or awards.
2. If a form asks for something the files don't give (a phone number, a founding date, a tax ID), leave it empty or ask the owner. Never guess.
3. Log everything you do the same day (see "How to log a result" at the end). Claude reads the logs every Monday.

---

## Once, this week

| # | Task | Where | Time |
|---|---|---|---|
| O1 | **Resubmit the sitemap.** Open https://search.google.com/search-console → property `getfotocal.com` → left menu **Sitemaps** → in "Add a new sitemap" type `sitemap.xml` → **Submit**. If it is already listed, click it and check the status says "Success". | Search Console | 2 min |
| O2 | **Add the site to Bing.** Open https://www.bing.com/webmasters → sign in with the same Google account → **Import from Google Search Console** → allow → select getfotocal.com → Import. | Bing Webmaster Tools | 5 min |
| O3 | **Social profiles.** Check each profile in the table "Social profile checklist" at the end of `docs/seo/backlinks/directories.md` has https://getfotocal.com/ in its website or bio field, and tick the boxes. | Instagram, TikTok, YouTube, Facebook | 15 min |

## Every week

| # | Task | File to use | Time |
|---|---|---|---|
| W1 | **Two directory listings**, in the order given in "Step by step, in this order". | `docs/seo/backlinks/directories.md` | 30 min |
| W2 | **Every second Tuesday: one Web 2.0 article**, on the date in the schedule. Follow that platform's file from top to bottom: title, body, tags, the two links, and the posting steps at the end. | `docs/seo/backlinks/web20/README.md` (schedule), then `web20/<platform>.md` | 1 hour |

**Web 2.0 order:**

| # | Date | Platform | File |
|---|---|---|---|
| 1 | Tue 17 Nov 2026 | Blogger | `web20/blogger.md` |
| 2 | Tue 1 Dec 2026 | WordPress.com | `web20/wordpress.md` |
| 3 | Tue 15 Dec 2026 | Medium | `web20/medium.md` |
| 4 | Tue 12 Jan 2027 | LinkedIn | `web20/linkedin.md` |
| 5 | Tue 26 Jan 2027 | Tumblr | `web20/tumblr.md` |
| 6 | Tue 9 Feb 2027 | Dev.to | `web20/devto.md`. **Before posting, the owner must read it and confirm every sentence is true**: it tells the story of building the app in his own voice. |

**How to copy an article without losing its formatting:**
1. Open the file on github.com. GitHub shows it formatted, with headings, bold text and links.
2. Select from the line after **▼ ARTICLE START** down to the line before **▲ ARTICLE END**, and copy.
3. Paste into the platform's normal editor (not an HTML or Markdown box). Headings, bold text and links come across.
4. Dev.to is the only exception: it wants Markdown. Click **Raw** at the top of the file on GitHub, copy the same part, and paste it.
5. Before publishing, click both getfotocal.com links in the editor and check they open the right page.

**Every time you post, also add the "read also" line** that the platform file gives you, linking to the previous article. Its live URL is in `tracker.csv`.

## First Monday of every month, before 09:00 Madrid time

Claude's monthly review runs that morning and reads what you upload. If the files aren't there yet, it reports "no data this month" and keeps the previous priorities.

| # | Task | Time |
|---|---|---|
| M1 | **Search Console export** (steps below). | 10 min |
| M2 | **AI visibility check** (steps below). | 60–90 min |
| M3 | **Resubmit the sitemap** (as O1). It only takes a click, and new pages get found faster. | 2 min |

### M1 · Search Console export
1. https://search.google.com/search-console → getfotocal.com → **Performance → Search results**.
2. Date: **Last 28 days**. Search type: **Web**. Tick **Total clicks**, **Total impressions**, **Average CTR** and **Average position**.
3. Top right, **Export → Download CSV**. You get a .zip. Unzip it: there are files such as `Queries.csv`, `Pages.csv`, `Countries.csv`, `Devices.csv` and `Dates.csv`.
4. Left menu **Pages** (under Indexing). Note two numbers: **Indexed** and **Not indexed**.
5. Upload to GitHub:
   1. Open https://github.com/fotocal/Fotocal-web/tree/main/docs/seo/gsc.
   2. Click **Add file → Upload files**.
   3. Drag in the CSV files.
   4. In the box above the file list, the folder name is part of the path. Type the month first, e.g. `2026-12/`, so the files land in `docs/seo/gsc/2026-12/`.
   5. Click **Commit changes**.
6. Same folder: **Add file → Create new file**. Name it `2026-12/indexing.txt`. Write two lines, e.g. `indexed: 280` and `not indexed: 30`, then **Commit changes**.

### M2 · AI visibility check
1. Open `docs/seo/ai-visibility.md`. It has 20 questions and the exact protocol: fresh chat, Spanish, no follow-ups.
2. Ask each question in ChatGPT, Gemini and Perplexity.
3. Record the answers. On GitHub, open `docs/seo/ai-checks/TEMPLATE.csv`, click **Raw**, and copy the contents. Then go to `docs/seo/ai-checks/` → **Add file → Create new file**, name it `2026-12.csv`, paste, and fill in one row per question and assistant:
   - **mentioned:** `yes` or `no`
   - **cited_url:** the getfotocal.com address, if one is shown
   - **competitors:** the other apps it names
   - **number_given:** the calorie figure it gives
4. **Commit changes.**

---

## How to log a result

`docs/seo/backlinks/tracker.csv` is the list of every link target. To update it:
1. Open the file on github.com.
2. Click the **pencil** (Edit).
3. Find the row for the site. Change its `status` column to one of `submitted`, `live`, `draft`, `rejected` or `not found`.
4. If it is live, replace its `url` with the address of the listing or article.
5. Change `date` to today, e.g. `2026-11-17`.
6. **Commit changes** at the top right, with a short message such as "tracker: AlternativeTo submitted".

The columns are `date,site,url,anchor,dofollow,indexed,status,notes`. Leave `dofollow` and `indexed` as `unknown`; Claude checks them.

Add a new row for any link not already in the list, such as a Web 2.0 article. Copy the format of the rows above it, and don't put commas inside a field.

## Files you will use

| File | For |
|---|---|
| `docs/seo/ASSISTANT.md` | this list |
| `docs/seo/backlinks/directories.md` | directory listings: steps and the texts to paste |
| `docs/seo/backlinks/web20/README.md` | Web 2.0 rules and schedule |
| `docs/seo/backlinks/web20/blogger.md`, `wordpress.md`, `medium.md`, `linkedin.md`, `tumblr.md`, `devto.md` | the six articles: title, body, tags, links and posting steps |
| `docs/seo/backlinks/tracker.csv` | the log of every link |
| `docs/seo/ai-visibility.md` + `docs/seo/ai-checks/TEMPLATE.csv` | the monthly AI check |
| `docs/seo/gsc/` | where the monthly Search Console export goes |

**Not for you**, unless the owner asks: `outreach.md` and `mentions.md`. These emails go out in the owner's name, and he should send them himself or approve each one first.
