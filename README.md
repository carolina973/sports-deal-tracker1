# Sports Fund Deal Tracker

A public web dashboard that tracks sports / sports-tech **funds** and the **deals** they invest in,
plus a weekly digest of deals surfaced from sports-business **newsletters**. It's a single
self-contained web page (`public/index.html`) built from three JSON data files, hosted free on
**GitHub Pages**, and it refreshes itself once a week via a scheduled job.

> **Public-safe.** This repo is meant to be public. The fund data here has already had all
> firm-internal fields removed (no contact emails, no "warm relationship" flags, no Affinity
> contacts) — it contains only funds, deals, sectors and the newsletter tracker.

## What's here

```
sports-deal-tracker/
├── build.py                     # builds public/index.html from data/*.json (pure Python, no network)
├── weekly_update.py             # asks Claude to pull new deals from the newsletters -> data/deals.json
├── data/  funds.json · deals.json · newsletters.json
├── public/index.html            # the built dashboard (what GitHub Pages serves)
├── .github/workflows/
│   ├── pages.yml                # builds + publishes to GitHub Pages on every push
│   └── weekly-update.yml         # Mondays: pull new deals -> rebuild -> commit (which republishes)
├── requirements.txt
└── GO-LIVE-RUNBOOK.md / .docx    # the full click-by-click setup + handover guide
```

## Run it locally

```bash
pip install -r requirements.txt
python build.py            # regenerates public/index.html from the data files
open public/index.html
```

## Make it live + auto-updating

Follow **GO-LIVE-RUNBOOK** (also included as a Word doc). In short: push this to a **public** GitHub
repo, turn on **GitHub Pages** (Settings → Pages → Source: *GitHub Actions*), and add an
`ANTHROPIC_API_KEY` secret for the weekly pull. That's it — you get a public URL and it updates itself
every Monday.

## Everyday edits (no coding)

Edit the JSON in `data/` and push — the site rebuilds and republishes automatically. To change the
tracked newsletters, edit `SOURCES` in `weekly_update.py`. To change the schedule, edit the `cron` in
`.github/workflows/weekly-update.yml`.
