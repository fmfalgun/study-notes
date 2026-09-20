# Checkpoint 1 — can we get the job descriptions, and how?

Worker: JD worker. Sources: 12-posting probe (24 fetches) + 6 alternative-capture fetches + local
data measurements. All archive.org requests: single thread, 6–12 s apart, every one HTTP 200 in
1–6 s, no throttle signs. (This is 30 fetches, more than the "~12" in the brief: each probe posting
was tried on two paths, then 6 extra fetches settled the old-era question.)

## Headline

**Job descriptions are recoverable for the new site format only (captures from mid-2023 on).
For postings that exist only as old-site captures they are not recoverable from Wayback over HTTP.**
That is 562 of 883 security postings (64%); 321 (36%) have no reachable description.

## Per era

| Era | Probe result | What the archived page contains |
|---|---|---|
| **Old site, 2019-09 → 2023-05** (`careers.google.com/jobs/results/<id>-<slug>/`) | **0 / 7** first-capture, **0 / 6** alternative captures | An empty single-page-app shell: 5–10 KB raw, 14–75 chars of text. Only the title exists (2022+ also a one-line meta tag "Apply for <title> via Google Careers"; earlier a generic "Careers at Google…" line). Raw and playback are equally empty. |
| **New site, 2024-03 → 2026-09** (`google.com/about/careers/applications/jobs/results/<id>-<slug>`) | **5 / 5** | Full description in the HTML: *About the job*, *Responsibilities*, *Minimum qualifications*, *Preferred qualifications* all present. ~1.04–1.16 MB decoded. |
| 2023-07 → 2023-12 (migration window) | not probed | To be included in the C2 pilot. |

**The description is in the raw archived HTML, not only in the rendered page.** Cheapest path that
works: `GET https://web.archive.org/web/<timestamp>id_/<url>` → **gunzip** → parse. 2–6 s per fetch.
Playback (`/web/<timestamp>/<url>`) also works but adds Wayback's toolbar text and is slightly larger;
no reason to prefer it.

**Correction of my own first reading.** My first probe reported "raw has no description" for the new
era. That was wrong: Wayback replays the original `Content-Encoding`, so the raw body is
gzip-compressed and my code did not decode it (it looked like binary garbage; `Accept-Encoding: identity`
does not prevent it). After decompressing, raw works. The capability must decode gzip/deflate (and
brotli if the module is available; it is not in the venv, so a `br` body would need the fallback).

## Alternatives for the old era — all checked

| Source | Result |
|---|---|
| Archived jobs API JSON (`careers.google.com/api/jobs/jobs-v1/jobs/get/…`) | 21 such URLs exist; **1** of the 883 security IDs is among them. Not viable. |
| Other captures of the same old-era posting (last capture of 6 postings with 3–6 captures) | 0 / 6 — all shells. |
| Search-API JSON recorded inside the old front-page snapshot captures | None present (0 job objects). |
| The old front-page snapshots' "Qualifications:" snippets | 21 unique security titles, median 335 chars, **minimum qualifications only**; matches by title to 10 of the 321 old-only postings. Anecdotal at best. |
| Browser (Selenium) fallback | Not used (needs parent direction). Expected useless: the SPA would call the job-detail API, which is not archived (1/883). |

## Coverage reality (measured locally, no network)

| First-seen year | Security postings | Have ≥1 new-era capture (description reachable) | Old-era only |
|---|---|---|---|
| 2019 | 8 | 3 | 5 |
| 2020 | 14 | 2 | 12 |
| 2021 | 70 | 6 (9%) | 64 |
| 2022 | 168 | 9 (5%) | 159 |
| 2023 | 115 | 34 (30%) | 81 |
| 2024 | 131 | 131 | 0 |
| 2025 | 265 | 265 | 0 |
| 2026 | 112 | 112 | 0 |
| **Total** | **883** | **562 (64%)** | **321 (36%)** |

Old-era-only by theme: security_engineering 127, sales_and_consulting 60, threat_intel_and_response 56,
other_security 55, physical_corporate_security 23.

**Consequence that matters for the analysis.** A posting first seen in 2021 whose description we can
read is readable only because it was captured *again* after mid-2023, so the text reflects a 2023+
capture, not 2021. By the year of the description's own capture, the 562 reachable postings are:
**2023: 36, 2024: 137, 2025: 276, 2026: 113.** Description-based findings therefore describe roughly
**mid-2023 → 2026**. 2019–2022 cannot be characterised from descriptions (20 reachable postings out of
260 first seen in those years, and even those carry later text).

## Proposed design (nothing implemented yet)

1. **Generic capability — `scraper_core/wayback.py` (additive only).**
   - `fetch_archived_page(timestamp, url, *, raw=True, timeout=60)` → `{ok, status, final_url, content_encoding, bytes, secs, body}` with `body` already decoded (gzip/deflate; brotli if installed, else a clear `unsupported_encoding:br` result). Builds the `id_` or playback URL. 404/403 are definitive (no retry).
   - `ArchiveFetcher(min_gap=6, max_gap=12, backoff_start=60, backoff_max=900, max_consecutive_failures=5)` with `.fetch(timestamp, url)`: jittered spacing, retry/backoff on refusal/timeout/429/503, raises `Throttled` after 5 consecutive failures. This is the reusable piece for any future "get the archived text of page X" task; the gzip lesson goes in its docstring.
   - No-network tests in `tests/test_wayback_fetch.py`: gzip/deflate/identity decoding, unsupported encoding, URL building, definitive 404, backoff schedule, spacing, `Throttled`.
2. **Google-specific — `plugins/job_search/wayback_google_details.py` (new).** `parse_job_detail(html)` → `{title, sections: {about, responsibilities, minimum_qualifications, preferred_qualifications}}` (exact DOM/markup to be read in C2); `pick_captures(captures)` (see 3); resumable fetch orchestrator; ops `google_wayback_fetch_details` (scrape, long timeout) and `google_wayback_details_coverage` (analyze). Registration lines go in `PLUGIN_NOTES.md`; I do not touch `__init__.py`.
3. **Which capture.** Earliest capture with host `www.google.com/about/careers` and timestamp ≥ 2023-07-01 (closest to the posting's original text). If it yields no sections, try the next new-era capture (max 3 tries). Postings with no new-era capture are **not requested at all** and are written to a ledger with reason `old_spa_shell`, so a later run never retries them.
4. **Storage (scraper-data).** Do **not** store the raw ~1 MB HTML (883 postings ≈ 0.9 GB; it is re-fetchable in ~3 s). Store parsed sections plus capture metadata (timestamp, URL, fetch seconds, source size/hash) as one `details`-kind capture per **description-capture year** (4 files: 2023–2026), saved every 25 postings (~23 commits for the whole run, each rewriting one ≤~1.5 MB file), skipping ids already present on restart; one extra `details` capture holds the ledger of unavailable postings and failures.
5. **Time.** 562 postings × (≈9 s spacing + ≈3 s fetch) ≈ **1.9 h**, ≈2.5 h allowing retries. Old-era: zero requests.

## Questions for the parent

See the CHECKPOINT 1 block in `progress.md`.
