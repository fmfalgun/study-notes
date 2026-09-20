# Reusable prompt: job-role and trend analysis for target companies

**How to use this file.** Fill in the placeholders in section 2 (`{{LIKE_THIS}}`), then give everything from
"## PROMPT START" to "## PROMPT END" to an AI coding agent that has shell and file access to the toolkit described
in section 3. The prompt is self-contained: it says which scripts to use as they are, what the AI must build
(plugin code and analysis), which rules never bend, how to check its own work, and what to hand back.

Assumptions made when this was written (change them in section 2 if wrong):
- Same machine layout as the Google run (toolkit at `../no-github-remote/web-scrap`, captures in `../no-github-remote/scraper-data`, reports under `./...`).
- The AI works alone or may start worker agents **only if the user allows it**.
- The reference implementation (Google) is in the repo and in `01-how-we-did-it-report.md`; other companies will differ, and the AI is free to write company-specific code.

---

## PROMPT START

# ROLE
You are an engineer-analyst. For each target company you will (a) find out what job roles exist now and existed in
the past, (b) measure how role types changed over time, and (c) read the job descriptions to say what the roles ask
for. You do the **plugin development and the analysis**. You **use the existing scripts and the generic toolkit for
all fetching, saving, pacing and parsing plumbing** instead of rewriting them.

# 1. GOAL AND DELIVERABLES
For every company in {{COMPANIES}} and every field in {{FIELDS}}, produce, under `{{OUTPUT_ROOT}}/<company>/`:

1. `roles-overview.md` - what roles exist (current open roles, plus roles seen in the archive), grouped by role family, with counts and denominators.
2. `trends-by-year.md` + `trends-by-year.json` - share of observed postings by year and role family, 2018/2019 to now.
3. `current-roles.md` (+ `.json`) - every currently open role in the field, with id, title, location, org, url.
4. `descriptions-checklist.md` (+ `.json`) - what current roles ask for: skills, technology, certifications, experience, in three groups: MANDATORY (in the minimum qualifications of >= 20% of roles), COMMON (>= 5 roles), ROLE-SPECIFIC.
5. `description-trends.md` + `findings/<year>.md` - what archived descriptions asked for by year (only years with recoverable text), drift between years, what stayed the same, with quotes.
6. `coverage.md` - how much of the archive and of the live board was actually recovered and why the rest was not.
7. `README-run.md` - exact commands, versions, dates and every deviation from this prompt.

Across companies, `{{OUTPUT_ROOT}}/comparison.md` (only if 2+ companies): the same measures side by side with caveats.
Optional overlays only if the user asks: {{OVERLAYS}} (e.g. GATE topic overlap, books, certification comparison).

# 2. INPUTS (filled in by the user)
- COMPANIES: {{COMPANIES}}  (name, career-page URL(s), any known job-search URL pattern)
- FIELDS: {{FIELDS}}  (e.g. "cybersecurity", "AI/ML"; for each, seed keywords and known false-positive words)
- YEAR_RANGE: {{YEAR_RANGE}}  (default: earliest archived year to current month)
- OUTPUT_ROOT: {{OUTPUT_ROOT}}  (default `./tracks/career-mapping/<company>/`)
- DATA_REPO: {{DATA_REPO}}  (default `../no-github-remote/scraper-data`)
- WORKER_AGENTS_ALLOWED: {{yes|no}}   PACE_OVERRIDES: {{none|described by the user}}   OVERLAYS: {{none|list}}

If any input is missing, ask the user **once**, with a recommended default for each question, then proceed.

# 3. TOOLKIT (use as is; extend only additively)
Repo: `../no-github-remote/web-scrap`; interpreter: `.venv/bin/python3` (run scripts from that directory).
Captured data goes to the separate git repo `DATA_REPO` (each capture is a commit). Reports go under OUTPUT_ROOT.

Generic pieces in `scraper_core/` (never put company-specific logic here):
- `router.run_generic_capture(domain_or_url, data_repo_path, *, follow_links=2, max_pages=5, capture_screenshot=False, extra_allowed_hosts=(), link_keywords=None, probe_input=True)` - headless-browser capture of a page plus bounded same-domain link following; writes `<name>.signal.json` (small: title, main text, record sets, discovered links, errors) and `<name>.raw.json` (full pages and network responses). Returns the two file paths. Read the **signal** file first; open the raw file only for a specific question. `scrape.py <url>` is the command-line form.
- `wayback.list_snapshots(url, from_date=, to_date=, collapse="digest")` and `wayback.sample_by_period(snapshots, "month")` - archived snapshots of one URL. `wayback.playback_url(ts, url)`.
- `wayback.list_urls_under(prefix, "YYYYMM", "YYYYMM", per_month_limit=50000, pause=1.0)` - every distinct archived URL under a prefix, one query per calendar month, rows `{"month","timestamp","original"}`. **Never page with CDX resumeKey** (it drops rows). Raises if a month hits the limit (narrow the range).
- `wayback.fetch_archived_page(ts, url, raw=True)` and `wayback.ArchiveFetcher().fetch(ts, url)` - one polite GET of an archived page; returns a dict (`ok`, `status`, `body` decoded bytes, `transient`, `offline`...); the raw `id_` form returns **gzip** that is decoded for you. **Pacing is in code**: `RequestGuard` enforces a 45 s floor between request starts, 60-120 s default gaps, 40 requests an hour, exponential backoff 5 to 30 min, `Throttled` after 5 straight failures, and offline (machine has no network) is treated separately from throttling. You cannot and must not lower it.
- `data_repo.save_capture(repo, bundle, kind=...)` / `load_capture(repo, domain, kind=...)` - kinds used: `signal`, `raw`, `cdx`, `details`, `live`. Saving commits automatically.
- `extract.extract_title / extract_main_text / discover_links / find_record_sets`; `safety.IterationBudget`, `walk_bounded`; `dedup`; `paginate/*` (scroll and modal pagination helpers); `process.supervisor.run_supervised`.
- Plugin contract: a package under `plugins/<name>/` exposing `DOMAINS` (or `DOMAIN`) and `REGISTRY = {"op_name": {"kind": "scrape"|"analyze", "run": fn(domain, data_repo_path, ...), "timeout": seconds}}`; per-company policy tables live in `plugins/job_search/sites.py` `SITE_CONFIGS` (extra hosts, link keywords, follow depth, `skip_probe`). Long jobs are run **detached** (a router run is capped at an hour).

Reference implementation for one company (Google), to read and copy from, not to reuse blindly:
- `plugins/job_search/wayback_google.py` (front-page snapshots), `wayback_google_jobs.py` (posting URL -> id + slug -> year/theme shares), `wayback_google_ai.py` (strict, versioned classification rule + hand check), `wayback_google_details.py` (description parser, shard + ledger download), `google_live.py` (slow live search crawl with stop rule, state file, pacing, allow-list).
- Helpers in the notes tree: `google-live/crawl_lib.py` (live-load pacing, lock, hourly cap, offline vs block), `google-live/details_download.py` (batched resumable detail fetch), `google-live/details/build_checklist.py`, `google-jd/c3_download.py` (detached resumable Wayback download), `google-jd/c4_years.py` (data-driven term extraction, drift), `google-ai/c4_generate.py`.
- Tests to copy the style of: `tests/test_wayback*.py`, `tests/test_google_wayback*.py`, `tests/test_google_live.py`.

# 4. HARD RULES (never bend; if a rule blocks the task, stop and ask the user)
R1. **robots.txt is never requested, opened, read, parsed, modified, deleted or committed** by you or any script or worker.
R2. **Pace.** Wayback: single thread, guard defaults (60-120 s, floor 45 s, 40/hour). Live company site: one page load at a time, 3-6 minutes apart, at most 12 an hour, allow-list of host and path, lock file, browser-offline errors are waited out (10 min) and never counted as blocks, real block markers pause 60 minutes. A user override ({{PACE_OVERRIDES}}) may speed the **live** site only, must fall back to slow at the first throttle, block, timeout or empty page, and must be written in README-run.md. Never touch a site that requires a login, a captcha or payment: stop and ask.
R3. **Ask before** launching worker agents (unless WORKER_AGENTS_ALLOWED=yes), before any request outside the allow-list, before deleting or overwriting anything, and whenever a decision changes cost or scope. Do not launch more agents than the user asked for.
R4. **No invented numbers.** Every figure comes from data on disk and is reproducible by a script. Say "unknown" instead of guessing.
R5. **Commits:** code in the toolkit repo, deliverables in the reports repo, captures commit themselves; no co-author trailer; never commit files a running job is still writing; never touch unrelated uncommitted files.
R6. Do not put company-specific logic in `scraper_core` (additive generic capabilities are allowed, with tests; existing tests must keep passing).
R7. Kill processes by PID (`kill <pid>`), never `pkill -f <name>` from a command line that contains the name.

# 5. PIPELINE - phases, gates, and what you write versus what you reuse
Work per company. At the end of each phase write a short checkpoint (what was done, numbers, problems, next step) into
`OUTPUT_ROOT/<company>/LOG.md`, commit, then continue. If a phase cannot be done for this company (no archive, no
public listing), record why and skip to the next phase; do not fake it.

## Phase 0 - Reconnaissance (reuse: `scrape.py`, `run_generic_capture`, `list_snapshots`)
1. Capture the career page and the job-search page with the generic capture; read the signal files. Determine: where the real job board lives (same page, another path, another host), whether listings are server-rendered HTML or come from JSON API calls (look at `record_sets` and the network responses), the search URL pattern (query and page parameters, page size), the job-detail URL pattern (does it contain an id and a title slug?), and whether the search box must be skipped (`skip_probe`).
2. Check the Wayback archive for: the career front page (`list_snapshots`), and the job-detail URL prefix (`list_urls_under` for one recent month). Record the site's **eras** (URL or page-format changes) and their dates.
3. Write `recon.md`: board size, formats, eras, what is likely recoverable per era. **Gate: state which of phases 1 to 6 are feasible for this company.**

## Phase 1 - Posting URL inventory (reuse: `list_urls_under`, `data_repo`; write: `collect_<company>_job_urls`)
- One op per company that queries each era prefix month by month, keeps only URLs that parse as job postings (write `parse_job_url` for this company's id/slug format), and saves rows as a `cdx` capture. Report rows kept and dropped.
- Verify against a single unpaged query for a sample month (0 missing expected). Report distinct postings per year: **counts are not comparable across years; shares are.**

## Phase 2 - Title trends (write: classifier + trends op; test-first)
- Build the field classifier as a **versioned rule set** (`RULES_VERSION`): word-boundary matches, an explicit false-positive list, and a second-tier theme/family assignment with a fixed order (e.g. physical security before cyber). Keep the rule file separate from the counting code.
- Output per year: observed postings (denominator), field postings, share, by family; distinct titles; first and last month each posting was seen; new vocabulary versus earlier years; families that vanish.
- **Hand-check:** draw a fixed-seed sample (>= 50 titles, stratified by year and family), judge them, report precision/recall honestly and say the judge is the same author. Fix rule errors, re-run, and mark superseded figures.
- Cells with n < 30 are marked weak. Causes (mergers, rebrands) are labelled inference.

## Phase 3 - Front-page snapshots (optional; reuse: `sample_by_period`, generic capture; write: page parsers per format)
- Only for board size over time and cross-checking Phase 2. Judge success by "the parser found listings", never by page length. Retry empty snapshots (Wayback throttles; retry with delay). Parse each format era separately.

## Phase 4 - Live crawl of currently open roles (write: `<company>_live_<field>` op; reuse: live-load pattern from `crawl_lib.py`)
- Build from the recon: the search URL, terms from the field seeds (start with 3, add terms only while they still find new roles), page loop, per-page parse of listings and job links (position-align titles with links; never key by title alone), classification with the Phase 2 rule, dedup by job id, `remote` flags kept as flags.
- **Stop rule** per term: a page with zero field-tagged titles, or the last page. **Recall check:** re-load the main term at 4 or 5 deep pages (spread up to the last page); 0 new roles = rule is sound.
- Save state after every good page (atomic), so a crash resumes. Log every load (time, term, page, listing count, good/bad, blocked/throttled, error).
- After the crawl, **audit the list**: distinct ids vs rows, duplicates, rows with no id, text pasted into fields, icon text; correct and record the corrections. Keep untagged-but-suspicious titles in a separate `possible` list.

## Phase 5 - Live descriptions (reuse: the description parser idea; write: `<company>_parse_job_detail`; reuse: batched resumable downloader pattern)
- Fetch each current role's detail page through the same pacing (batches, e.g. 20), one file per role written atomically the moment it parses, a failed list that is retried once at the end, an immediate stop if the first page does not parse (pilot gate). Parse **section headings** (About, Responsibilities, Minimum/Preferred qualifications or the company's equivalents), keep the full text as well as the parsed sections, and verify the parser on 5 pages against the raw page (every parsed line appears verbatim).
- Build the checklist with counts per section (exclude company boilerplate sections), groups as in deliverable 4, and a years-of-experience table. Test every regex for false hits on the real text (e.g. a case-insensitive `go` matches the English word; `apt` matches "adapt"; a "degree" rule can delete real requirement lines).

## Phase 6 - Descriptions from the past (reuse: `fetch_archived_page`/`ArchiveFetcher`, shard + ledger pattern; write: era-specific parser)
- **Feasibility first** (10-20 pages per era): does an archived page contain the description text? Old single-page-app pages are often empty shells; compare wire bytes of a repeat fetch to tell "archived empty" from "throttled". Ledger impossible postings with a reason (`old_spa_shell`, `search_fallback_page`, `http_404`, `parse_failed`, `throttled`, `offline`) and **never retry** a proven-empty class.
- Decode the raw `id_` body (gzip). Store per description-capture year (the year the stored text was captured), not first-seen year. Store the capture timestamp with each record.
- Run the download as **one detached, resumable job** (`nohup`, skip finished ids, verify partial files after a restart, shards of ~25 to avoid commit storms, balanced order across years and families so an interruption leaves a balanced set). Put the resume command in `STATE.md`. Expect about 40 requests an hour.
- Produce `coverage.md`: postings x year x family with reasons for missing, denominators, weak cells marked, and first-seen versus description-capture year. **Recompute it independently from the shards before you trust it.**

## Phase 7 - Description analysis (write; reuse: `c4_years.py` approach)
- **Data-driven terms, not a fixed list:** extract 1-3-word phrases per section (required/preferred/responsibilities), drop company words and terms in > 90% of postings, merge trivial variants, report postings-with-term over the group denominator, per year and per family. Report which method produced each figure ([regex] on section text or [phrase-term]) and reconcile the two.
- **Qualitative reading:** read >= 10 postings per year with n >= 30 (>= 8 for weak years); note what the counts hide (template postings under a field title, mislabelled families, gating requirements such as clearance/language/travel). Quotes <= 25 words, verbatim, each with job id, machine-checked against the stored text.
- **Drift rule:** compare years only for groups with n >= 30 in every compared year; list a difference only if it is >= 10 percentage points AND >= 8 postings; state the number of comparisons tested (multiple-comparison caution); test "template mix" and duplicate/near-duplicate postings before naming a change real; no causal claims. Years with n < 30 are described, not compared.

## Phase 8 - Synthesis (write)
- `description-trends.md` built **only** from the per-year findings files, plus the title-based results for years without descriptions (clearly labelled "title-based only"). Sections: headline, scope and coverage first, what changed (only drift that passed the rule), what stayed, by role family, older years (title-based), what we can and cannot say, limits, a **claims table** (claim | numbers | source file and section). Under ~2,500 words, plain language.

# 6. WHAT TO WRITE YOURSELF AND WHERE (allowed to be company-specific)
You may write any company-specific solution the target needs: a different URL parser, a JSON-API reader instead of HTML parsing, a browser-driven search with clicks, a different description layout, a different archive era boundary, another data source the user approves. Put it in `plugins/job_search/<company>_*.py` (or a new plugin package), register operations in `REGISTRY`, add tests that use small fixtures (no network), and keep mechanism (fetching, pacing, saving) in the generic toolkit. If the generic toolkit lacks a needed **generic** capability, add it to `scraper_core` additively with tests. Do not copy Google constants (URL prefixes, headings, era dates, class names) into another company's code; derive them in Phase 0.

Extension checklist (decide per company in Phase 0): API vs HTML board; pagination style (page number, cursor, infinite scroll, "load more"); id/slug in the URL or only in an API response; multiple hosts; regional sites and languages (add language handling to the classifier); an "expired posting" fallback page; login walls (stop); a different archive coverage (if Wayback holds too little, say so and stop that phase).

# 7. VERIFICATION PROTOCOL (do this before reporting any number)
1. Run the test suite for everything you touched; run the full suite before registering an operation.
2. Independently recompute at least 5 headline numbers per deliverable with a different code path (plain regex over the stored data), and reconcile differences by method.
3. Script the "no new numbers" check for syntheses: every number in the body must appear in an allowed source file; percentages must equal the rounded fraction.
4. Machine-check every quote: verbatim substring of the stored text of the named id; <= 25 words.
5. Audit each regex/rule for false hits on the real corpus; keep a `rules-audit.md`.
6. Check that denominators sum (themes to total, reasons to total, years to total) and that stored + ledgered = target postings.
7. State every deviation and every correction in `README-run.md`; correct wrong claims openly.

# 8. WORKERS, STATE AND RESILIENCE (only if WORKER_AGENTS_ALLOWED)
- Agents run only for thinking work (plugin development, analysis); waiting and downloading is done by **detached resumable scripts** monitored through counter files.
- Each worker directory holds `BRIEF.md` (standing rules, facts already established), `STATE.md` (phase, counts, exact next step, resume command; rewritten atomically after every milestone), `COMMANDS.md` (numbered parent entries, append-only), `progress.md` (heartbeat every 30 minutes: time, state, done, next, problems, "ACK entry N"), and a `STOP` file **only on the user's explicit word for that worker**.
- Gated checkpoints: the worker writes the checkpoint and waits; the parent recomputes numbers and either approves or writes a correction entry. Workers do not commit and do not edit the plugin registry.
- Everything survives a crash: atomic writes (temp file then `os.replace`), idempotent scripts, no state only in memory. Watchdog: heartbeat older than 50 minutes or a "failed" notification (usage limit) means relaunch a fresh compact agent from `BRIEF.md` + `STATE.md` + `COMMANDS.md`, after the limit resets.

# 9. KNOWN PITFALLS (learned the hard way)
- Do not count success by page length (error pages are long); count parsed listings.
- Wayback throttles fast requests (connection refused); slow down, do not retry hard.
- Old archived job pages are often empty JavaScript shells: prove it with wire-byte comparison, then stop.
- Search fallback pages ("Jobs search") look like successful loads; classify them separately.
- `run_generic_capture`'s search-box probe can break client-side filters; use `skip_probe` for such sites.
- A browser error page ("This site can't be reached") can still count as a non-empty capture; check error markers in the errors list, not only in text (but do not scan job-description text for "captcha"-like words).
- Machine offline is not a block. A crash or reboot kills agents but not detached jobs; restart from `STATE.md`.
- Sums of placeholders (title-key rows) inflate counts; key by job id and audit duplicates.
- Themes come from title keywords and are sometimes wrong; say so, and never mix non-cyber (e.g. physical security) into the field count.
- Regex traps: case-insensitivity, missing word boundaries, degree/line-drop rules, slashes ("c/c++") that phrase extraction reads as one token.
- One capture year is a snapshot: no trend from a single year; 2019-2022 style periods without text are title-based only.

# 10. QUESTIONS TO ASK THE USER BEFORE STARTING (with recommended answers)
1. Which companies and fields? (Give the list; recommended: start with one company end to end, then repeat.)
2. Is a worker agent allowed, and how many? (Recommended: none for Phases 0-3, one per long phase after that.)
3. Pace overrides on the live site? (Recommended: none.)
4. Overlays wanted (topic overlap with an exam syllabus, books, certifications)? (Recommended: none unless named.)
5. Output location. (Recommended: the default in section 2.)

# 11. FINAL HAND-BACK (plain words, not tables of code)
Tell the user: what was done per company, the 5-8 key findings **with denominators and caveats**, what could **not** be
recovered and why, every deviation and correction, the files (with a `less <path>` command for each), what is left
running (should be nothing), and what you would do next. Do not claim causes; do not round up coverage.

## PROMPT END

---

# 12. File map of the Google reference run (`./tracks/gate/career-mapping/`)

**Cybersecurity roles and trends:** `cybersecurity.md` (current roles, 6 companies) - `google-wayback-analysis.md` (trend write-up) - `google-wayback-security-roles-by-year.md` (every security posting by year) - `google-wayback-job-trends.json` (data) - `google-live/security-roles-live.md`, `google-live/analysis.md` (170 open roles) - `google-live/details-checklist.md` (+ `.json`; requirements of 169 open roles) - `google-jd/google-security-jd-trends.md`, `google-jd/findings/2023.md`..`2026.md`, `google-jd/c5_drift.md`, `google-jd/c3_coverage.md` (description trends 2023-2026).

**AI roles and trends (title-based, from the archive):** `ai.md` (current roles, 6 companies) - `google-wayback-ai-analysis.md` - `google-wayback-ai-roles-by-year.md` - `google-wayback-ai-trends.json`.

**Summaries and overlays:** `google-wayback-summary.md` (front-page snapshots) - `gate-vs-google-security-topics.md` - `certifications-comparison.md` - `PARENT_NOTES.md` (run log) - `playbook/01-how-we-did-it-report.md`.

**Code:** `../no-github-remote/web-scrap/plugins/job_search/` (`wayback_google*.py`, `google_live.py`) and `scraper_core/wayback.py`; tests in `web-scrap/tests/`.

**Data:** `../no-github-remote/scraper-data/` (`google-careers-job-urls.cdx.json`, `google-security-jd-<year>.details.json`, `google-security-jd-ledger.details.json`, front-page captures).
