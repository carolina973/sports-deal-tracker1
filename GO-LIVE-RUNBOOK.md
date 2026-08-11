# Sports Deal Tracker — Setup & Handover Guide

**For colleagues.** This guide lets you take this code and turn it into a **live public web page that
updates itself every week** — and keep it running over time. No prior experience assumed; where it
matters it says exactly what to click. About 20 minutes.

You'll use two accounts: **GitHub** (stores the code and hosts the free public page) and **Anthropic**
(the AI that does the weekly deal research; a few cents to a few dollars a week).

> **This is the public version.** The data has already had all firm-internal fields removed (no contact
> emails, no "warm relationship" flags). It's safe to publish. Anyone with the link — and search
> engines — can view the page; that's intended.

---

## 1. Get the files

You have a folder called **`sports-deal-tracker`** (unzip `sports-deal-tracker.zip` if you haven't).
It holds the code, the data, the built page, and this guide. Keep it handy.

## 2. Part A — Put the code on GitHub (public)

Easiest without a command line is **GitHub Desktop**; the terminal option follows.

**A1 — GitHub Desktop**

1. Install from **desktop.github.com**, open it, and sign in (click **Authorize** in the browser; make
   a free GitHub account first at github.com if needed).
2. Top menu **File → Add local repository… → Choose…**, pick the **sports-deal-tracker** folder, **Open**.
3. If prompted that it isn't a Git repo, click **create a repository**, then **Create repository**.
4. Bottom-left **Summary** box: type `Initial import` → click **Commit to main**.
5. Click **Publish repository** (top). In the pop-up, **UNtick "Keep this code private"** (you want it
   public), then click **Publish repository**. ✅ Your code is on GitHub, public.

**A2 — Terminal**

1. On github.com: **+ → New repository** → name `sports-deal-tracker` → choose **Public** → **Create
   repository** (don't initialize).
2. From inside the folder:
   ```
   git init
   git add .
   git commit -m "Initial import"
   git branch -M main
   git remote add origin https://github.com/<your-username>/sports-deal-tracker.git
   git push -u origin main
   ```

## 3. Part B — Turn on GitHub Pages (this creates the public link)

1. In your repo on github.com, click the **Settings** tab.
2. Left sidebar → **Pages**.
3. Under **Build and deployment → Source**, open the dropdown and choose **GitHub Actions**. (That's the
   only change — the workflow already included in the repo does the rest.)
4. Go to the **Actions** tab. You'll see **Deploy to GitHub Pages** run automatically (or click it →
   **Run workflow** to start it). Wait for the green tick.
5. Back in **Settings → Pages**, your live address appears at the top, like
   `https://<your-username>.github.io/sports-deal-tracker/`. **That's your public link.** Open it.

## 4. Part C — Turn on the weekly auto-update

1. Get an API key at **console.anthropic.com** → create an account → **Settings → Billing** (add a card,
   set a small monthly cap, e.g. $20) → **API keys → Create key** → **Copy** it.
2. In the GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**.
   Name: `ANTHROPIC_API_KEY`, value: paste the key → **Add secret**.
3. Done. The weekly job runs **every Monday**: it pulls new deals, rebuilds the page, and the push
   republishes it. To run it now: **Actions → Weekly deal-tracker update → Run workflow**.

## 5. Part D — Verify (5 min)

1. Trigger the weekly workflow (Part C step 3) → it goes green and ends with "Weekly update complete…".
2. A new commit appears on `main`; **Deploy to GitHub Pages** then runs and republishes.
3. Open your Pages link — the dashboard shows the current date.

That's it — live, public, and self-updating every Monday.

---

## 6. Handover (when the person who set it up leaves)

Only two things need to move; both are quick.

1. **The repo** → repo **Settings → General → Transfer ownership** to a colleague or the org's GitHub
   organization. (Or just add another person as an admin under **Settings → Collaborators**.)
2. **The API key** (the must-do) → a colleague creates their own key on their Anthropic account (with
   billing + a spend cap), updates the `ANTHROPIC_API_KEY` secret (Part C step 2), and the departing
   person revokes the old key. If skipped, the weekly refresh stops when that account closes — the live
   page keeps working and can still be updated by hand; it just won't self-refresh.

Then re-run Part D to confirm it still works.

## 7. Everyday use (no coding)

- **Add/fix a deal or fund:** edit the file in the `data/` folder (`funds.json`, `deals.json`), save,
  and push (GitHub Desktop: commit → **Push origin**). The site rebuilds and republishes automatically.
- **Add or drop a newsletter:** edit the `SOURCES` list in `weekly_update.py`.
- **Change the weekly day/time:** edit the `cron` line in `.github/workflows/weekly-update.yml`.
- **Pause auto-updates:** repo → Actions → the workflow → **Disable workflow**.

## 8. If something goes wrong

- **Weekly job failed at "Pull new deals…":** the `ANTHROPIC_API_KEY` is missing/expired or the Anthropic
  account is out of credit. Fix it and re-run.
- **Job ran but added 0 deals:** normal on a quiet week — it only adds new, verifiable deals.
- **Page didn't change:** Actions tab → check the latest **Deploy to GitHub Pages** run; re-run if it failed.
- **Lost the URL:** it's in **Settings → Pages**.
