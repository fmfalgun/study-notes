# Google careers page — Wayback Machine download summary

Companion to `cybersecurity.md` / `ai.md`. Records what was downloaded from the Wayback
Machine for Google's job listings, so it never needs fetching again. The trend findings are in
`google-wayback-analysis.md`.

> **Correction.** An earlier version of this file said "76 of 84 (90%) with real content".
> That was wrong: it judged by character count, which counted 5 Chrome "This site can't be
> reached" error pages (712 chars) and tiny JavaScript shells as good. The figures below judge by
> **parseable job listings**.

## Where the data lives

| What | Where |
|---|---|
| 84 monthly front-page snapshots: index | `google-wayback-results.json` (this folder) |
| Captured content per snapshot | `../no-github-remote/scraper-data/https___web.archive.org_web_<timestamp>_<url>.signal.json` (+ `.raw.json` full capture) |
| 18,188 archived individual job postings (URL list, 36,847 rows) | `../no-github-remote/scraper-data/google-careers-job-urls.cdx.json` |
| Parsed trends from those postings | `google-wayback-job-trends.json`, `google-wayback-security-roles-by-year.md` |
| Code | `web-scrap/scraper_core/wayback.py`, `plugins/job_search/wayback_google.py`, `plugins/job_search/wayback_google_jobs.py` |

`scraper-data` is a git repo: every capture is a commit.

## Two datasets, two purposes

1. **Front-page snapshots (84, monthly, Nov 2018 – Sep 2026).** Each holds only the first ~20
   relevance-sorted listings plus the board-wide "N jobs matched" total. Good for the size of
   the board over time; **not** for "all roles" (a small biased sample).
2. **Individual posting URLs (18,188 postings).** Every posting Wayback archived. This is the
   dataset the security analysis uses.

## Front-page snapshots: true coverage

- **79 of 84 have parseable listings.**
- **5 do not**, and cannot be recovered:
  - `20181115195622`, `20181201040552`, `20190106214641`, `20190403215323` — the 2018–Apr 2019
    pages are JavaScript shells; Wayback stored no rendered listings (4 retries each, all empty).
  - `20250602155633` — navigation rendered but no results (4 retries, all empty).
- Google moved its job board in mid-2023, so there are two page formats:
  `careers.google.com/jobs/results/` (to Jun 2023) and
  `google.com/about/careers/applications/jobs/results` (Jul 2023 on).

## What went wrong along the way (kept so it is not repeated)

1. **A cookie-consent "OK" click crashed whole captures** when another element intercepted it.
   Fixed: a failed dismiss-click is now logged and skipped (web-scrap commit `5e6d8c2`).
2. **Wayback throttles rapid requests** — back-to-back captures got `ERR_CONNECTION_REFUSED` in
   1–2 s. Fixed with a 5 s delay plus retry with backoff. Every one of the 8 snapshots that came
   back empty in the first pass recovered on retry, so those were throttling, not missing data.
3. **CDX `resumeKey` paging silently dropped rows** (190 URLs vs 193 from one query). The
   URL-listing function now queries one month at a time and was verified against the
   single-query ground truth with 0 missing (commit `d6f0925`).
4. **Judging success by character count was wrong** (see the correction at the top). The check
   now is "did the parser find listings".

## Code that exists now

- `scraper_core/wayback.py` — generic: list snapshots, list URLs under a prefix (month-windowed),
  build playback URLs.
- `plugins/job_search/wayback_google.py` — parses the two front-page formats; op
  `google_wayback_history`.
- `plugins/job_search/wayback_google_jobs.py` — parses posting URLs; ops
  `google_wayback_collect_job_urls` (network) and `google_wayback_job_trends` (analysis).
- A separate **live-site crawler** for currently-active security roles is being built in
  `google-live/` (slow, gentle by design).
