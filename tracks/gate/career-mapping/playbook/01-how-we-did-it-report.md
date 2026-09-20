# How we analysed Google's cybersecurity and AI job roles, 2018/2019 to 2026

A full account of what was done, in what order, with which tools, what went wrong, and how each result was checked.
Written 21 Sep 2026 from the working notes (`../PARENT_NOTES.md`) and the finished deliverables. The companion file
`02-reusable-prompt.md` turns this into a prompt that repeats the operation for other companies.

**Honesty rules that governed everything** (they are also the reason the numbers can be trusted):
- A count is only compared across years as a **share with its denominator**; a cell with **n < 30 is "weak"**.
- **Titles are not skills.** Anything about skills needs job descriptions.
- Keyword classification is a **heuristic**; causes (acquisitions, rebrands) are **inference**, never findings.
- Only what the **archive contains** can be analysed (Wayback Machine holds a sample, not every posting).
- Every important number was **recomputed independently** before it was reported.

---

## 1. What was asked, and what came out

| Question | Answer produced | Main file |
|---|---|---|
| Which cybersecurity job roles exist at big tech firms, and what do they ask for? | Current-role lists for 6 companies each for cyber and AI, with stack, certifications, skills, GATE overlap, project ideas | `../cybersecurity.md`, `../ai.md` |
| How did Google's cybersecurity roles change 2018-2026? | 883 security-tagged postings from 18,188 archived posting pages, by year and role family | `../google-wayback-analysis.md`, `../google-wayback-security-roles-by-year.md`, `../google-wayback-job-trends.json` |
| Same question for AI roles | 1,385 AI/ML postings by a strict rule, verified against a hand-checked sample | `../google-wayback-ai-analysis.md`, `../google-wayback-ai-roles-by-year.md`, `../google-wayback-ai-trends.json` |
| Which security roles are open on Google's site today? | 170 distinct roles found on 19 Sep 2026 (board of 3,338 jobs) | `../google-live/security-roles-live.md`, `../google-live/analysis.md` |
| What do those roles ask for (skills, technology, certifications, experience)? | Descriptions of 169 live roles and a counted checklist | `../google-live/details-checklist.md` |
| What did descriptions say in past years? | 409 of the 883 archived security postings recovered as full descriptions (2023 to 2026) and analysed | `../google-jd/google-security-jd-trends.md`, `../google-jd/findings/2023.md` to `2026.md` |
| How does it map to GATE and to books we own? | Topic-by-topic comparison | `../gate-vs-google-security-topics.md` |
| Which certifications are worth it? | GIAC/SANS, OffSec, CISSP, CCSP compared on cost, ROI, field | `../certifications-comparison.md` |

**Not done (be aware):** AI roles have **no description-level analysis** and no live crawl; the AI Google analysis is title-based (Wayback posting URLs). Current AI roles for other companies are only in `../ai.md`.

---

## 2. The toolkit (what already existed and what we added)

Location: `../no-github-remote/web-scrap` (Python, venv at `.venv`). Captured data is kept in a **separate git repo**
`../no-github-remote/scraper-data` (every capture is a commit). Notes and reports live in
`./tracks/gate/career-mapping/`.

### Design rule: mechanism in `scraper_core`, policy in a plugin
`scraper_core` is generic and must stay generic. Site-specific knowledge goes in a plugin (`plugins/job_search/`).

| Layer | Piece | What it does |
|---|---|---|
| Generic (`scraper_core/`) | `router.run_generic_capture(url, data_repo, follow_links, max_pages, capture_screenshot, extra_allowed_hosts, link_keywords, probe_input)` | Real headless browser (Selenium) capture of a page and up to N followed links; writes a small `signal` file and a full `raw` file |
| | `capture_site`, `dom_capture`, `network_capture`, `extract` | Page HTML, JSON API responses, main text, record sets, link discovery |
| | `data_repo.save_capture(repo, bundle, kind)` / `load_capture(...)` | Atomic-ish save plus git commit; `kind` gives separate files (`signal`, `raw`, `cdx`, `details`, `live`) |
| | `wayback.py` | Wayback CDX queries (`list_snapshots`, `list_urls_under` month-by-month), playback URLs, archived-page fetch with gzip decoding, `ArchiveFetcher` (polite fetcher), `RequestGuard` (pacing in code) |
| | `safety.py`, `dedup.py`, `registry.py` | Loop limits, dedup, plugin discovery |
| Plugin (`plugins/job_search/`) | `sites.py` `SITE_CONFIGS` | Per-company policy: extra hosts, link keywords, follow depth, whether to skip the search-box probe |
| | `run.py` `find_openings` | Current-openings capture for a configured company |
| | `wayback_google.py` | Parses the 84 monthly front-page snapshots (two page formats) |
| | `wayback_google_jobs.py` | Posting URLs -> job id + title slug -> year-by-year security shares |
| | `wayback_google_ai.py` | Strict AI classification with a versioned rule set |
| | `wayback_google_details.py` | Parse description pages; resumable download into shards + ledger |
| | `google_live.py` | Slow live search crawl (currently **written and tested but not registered**, awaiting your review) |
| Helpers kept in the notes tree | `google-live/crawl_lib.py`, `details_download.py`, `build_checklist.py`; `google-jd/c3_download.py`, `c4_years.py`; `google-ai/c4_generate.py` | Worker scripts (pacing, batching, analysis) |

Operations are registered in `plugins/job_search/__init__.py` as `REGISTRY[name] = {"kind": "scrape"|"analyze", "run": fn, "timeout": s}`.
Run one from a script with the venv: `from plugins.job_search import REGISTRY; REGISTRY["google_wayback_job_trends"]["run"]("google.com", DATA_REPO)`.

---

## 3. The pipeline, step by step

Each step lists the input, what was done, the output and how it was verified.

### Step 0. Current roles across companies (first pass)
- Captured the career pages of ~30 product companies with the generic capture (`follow_links=2`, `max_pages=5`), then read the small `signal` files instead of the huge `raw` files (a token-saving split introduced for this).
- Result: title lists for cybersecurity and AI, consolidated into `cybersecurity.md` (Google, Anthropic, Cloudflare, Snowflake, SAP, Adobe) and `ai.md` (Google, Anthropic, Meta, SAP, Adobe, Palo Alto Networks). Companies whose crawl was blocked or polluted by the search-box probe are listed as "no usable data".
- Lesson: a page you are pointed at can be a hub; the real board lives one click away or on another host (Apple: `jobs.apple.com`). That is why link-following and per-site policy exist.

### Step 1. Wayback front-page snapshots (84 monthly)
- Listed snapshots with the CDX API, sampled one per month (Nov 2018 - Sep 2026), captured each archived front page, parsed the ~20 job cards.
- Result: only **79 of 84** parseable. The first "76 good" claim was wrong (character length counted Chrome error pages); success is now "the parser found listings".
- What this dataset is good for: board size over time. What it is **not**: "all roles" (20 relevance-ranked cards per page).

### Step 2. Full inventory of archived posting URLs
- The user rejected "first 20 listings per snapshot", so we listed **every posting URL Wayback holds** under the two site eras: `careers.google.com/jobs/results/` (to Jun 2023) and `google.com/about/careers/applications/jobs/results/` (Jul 2023 on), one CDX query per calendar month (`list_urls_under`).
- Each URL carries `<18-digit job id>-<title slug>`; the capture month proves the posting was live then.
- Result: **36,847 rows -> 18,188 distinct postings**; postings per year swing from 269 (2019) to 6,824 (2025) with Wayback's crawling, which is why only shares are compared.
- Verification: CDX `resumeKey` paging silently dropped rows (190 vs 193), so month windows are used; a full-range check found 0 missing and 1 extra (a case variant).

### Step 3. Cybersecurity title analysis (2019-2026)
- Classification: keyword rule on the title (security, cyber, threat, incident response, vulnerability, malware, forensics, cryptography ...), then a theme: physical/corporate security first (so "Data Center Security Manager" is not counted as cyber), then threat/response, sales/consulting, engineering, other.
- Result: **883 security-tagged postings**, 690 distinct titles; share of observed postings rose from ~3% (2019-2021) to ~5-6% (2023-2026); Cloud-titled roles 0-18% -> 30-44%; Mandiant 0% -> 8% (2023) -> 24% (2024); go-to-market roles 0-12% -> 22-27%.
- Verification: shares recomputed with denominators (269, 572, 2,326, 4,276, 2,371, 2,469, 6,824, 1,925 for 2019-2026).

### Step 4. AI title analysis, with a second, stricter rule
- A first broad keyword rule over-counted (data-science analytics titles, "Quantum AI") and missed spellings such as "Aiml". A worker (Worker B) rebuilt the classification as a **strict, versioned rule** (`RULES_VERSION`) with a documented false-positive check.
- Result: **1,385 AI/ML postings**; share 1.9%-4.2% in 2019-2023, 11.1% (2024), 9.8% (2025), 12.4% (2026). The title wording moved from "machine learning" (53-66% of AI titles) to "AI" (55%). AI inside security titles appears only from 2025.
- Verification: I re-ran the operation and compared to the saved trends and the hand-checked sample; one false positive was removed (18 -> 17 AI x security postings in 2025); the earlier broader numbers were marked "superseded for AI only".
- Bug found and fixed: a classifier test had encoded a gap ("Large Language Models" not counted as AI).

### Step 5. Live crawl of currently open security roles (Google)
- Slow live crawl of Google's careers search (`?q=<term>&page=<n>`, 20 listings per page), one page load every 3-6 minutes, at most 12 an hour, one at a time, allow-list of URL host/path, a lock file, and pause states (offline vs block).
- Terms: security, cybersecurity, threat, incident response, vulnerability, malware, red team, penetration testing, detection, cryptography (83 loads in total).
- Stop rule: a term stops at a page with zero security-tagged titles or the last page; a **deep-page recall check** re-loaded `security` at pages 20, 35, 50, 65, 71: 0 tagged, 0 new roles. The word "security" alone found 162 of the 170 roles, so the plugin default is now the 3 terms security, cybersecurity, threat.
- Result: **170 distinct roles** (165 Google, 4 DeepMind, 1 YouTube), 4 more "possible" (Mandiant titles with no security keyword); themes: engineering 58, threat/response 41, sales/consulting 34, other 31, physical 6.
- Errors caught: a false "blocked" pause was actually the machine being offline; "178 roles" counted title-key placeholder rows and was corrected to 170 after re-verification.

### Step 6. Live job descriptions and the checklist
- The detail page of each of the 169 live roles with an id was loaded (batched, resumable, atomic per-role files) and parsed by the same description parser used for Wayback pages (About / Responsibilities / Minimum / Preferred qualifications).
- Pace: first slow (3-6 min), then a user-approved fast mode (about 45 s) that falls back to slow on the first throttle or empty page. Three odd events (a Chrome certificate error, two timeouts) were all local/network; each failed role was retried and stored.
- `build_checklist.py` counts items by section (excluding the "About" boilerplate) and groups them: MANDATORY (in the minimum qualifications of >= 20% of roles), COMMON (>= 5 roles), ROLE-SPECIFIC. Errors found and fixed: a case-insensitive `Go` matched the English word "go", and `apt` matched "adapt".
- Result: coding is the most common technical minimum (68 of 169 roles); certifications are almost never required (2 of 169), and are preferred mostly in incident-response and red-team (Mandiant) roles.

### Step 7. Descriptions from the past (Wayback, security only)
- Feasibility first: only **562 of 883** postings could yield text. Old-format pages (to mid-2023) are archived as **empty single-page-app shells**; a controlled retry (same URL and timestamp) returned identical bytes, so it is not throttling and the 321 old-only postings were ledgered `old_spa_shell` and never retried. 2019-2022 therefore stay **title-based only**.
- The pacing guard was put **in code** (45 s floor that a caller cannot lower, 60-120 s default, 40 an hour, offline vs throttle classification) before any request, because an earlier run of the worker had broken the agreed cool-down.
- Download: one detached, resumable job, round-robin across years and themes, shards of 25 plus a ledger. About 20 hours with two Wayback throttle pauses handled automatically.
- Result: **409 stored** (2023: 26, 2024: 100, 2025: 194, 2026: 89 by capture year), **474 ledgered** (old shells 321, Google's "Jobs search" fallback page 142, 404 5, unparseable 6). Coverage tables recomputed from the shards and matched exactly.
- Edit tracking: 34 later captures were fetched; 32 were already gone and 2 unchanged, so nothing can be said about edits. Each description is "the text at its capture date".

### Step 8. Description analysis 2023-2026 and the synthesis
- Pilot on 2025 (n=194): terms extracted **from the text itself** (1-3-word phrases per section, boilerplate removed, variants merged), by theme with denominators; 15 postings read in full; quotes (<= 25 words) machine-checked as verbatim.
- My review found a flaw: the rule "drop lines with the word degree" also removed real requirement lines ("... or 1 year of experience with an advanced degree"), undercounting Python and C++; the rule was narrowed and all years re-run with one script (`c4_years.py`).
- Drift rule: compare years only where a group has n >= 30 in each; report a difference only if it is >= 10 percentage points and >= 8 postings. Only "all postings" and "security_engineering" qualify.
- Final synthesis was built only from the findings files, each claim traced in a claims table, and I verified it by script (all 98 fractions found in sources, all percentages correct, 9 quotes verbatim, capture-date ranges checked).

### Step 9. Overlays (specific to this user, optional for reuse)
- GATE topics vs Google's requirements vs the books on disk (`../gate-vs-google-security-topics.md`); certification comparison with cost and ROI (`../certifications-comparison.md`).

---

## 4. How the work was organised

- **Parent session** designs, reviews and commits; **worker agents** did analysis and plugin development (A: live crawl, B: AI, C: descriptions). Every worker had `BRIEF.md` (standing orders), `STATE.md` (where it is, how to resume), `COMMANDS.md` (numbered parent directions), `progress.md` (heartbeats), and an optional `STOP` file only on the user's explicit word.
- **Gated checkpoints:** a worker finishes a checkpoint, writes it, waits; the parent recomputes numbers, spot-checks quotes, and either approves or sends a correction.
- **Resilience:** long jobs are **detached, resumable scripts** (they survive agent death, usage limits and reboots); every result is written atomically the moment it is produced; a machine crash and three usage-limit stops cost nothing but time.
- **Quota rule:** an agent runs only when there is thinking work; waiting is done by scripts and cheap file checks.
- **Commits:** code in the `web-scrap` repo; deliverables in `study-notes`; captures commit themselves in `scraper-data`; no co-author trailer.

## 5. Rules the user set (kept as hard rules in the prompt)

1. `robots.txt` is never requested, opened, read, changed or committed by anyone.
2. The slowest sensible pace: Wayback single thread, 60-120 s apart (floor 45 s, 40 an hour); the live site 3-6 minutes between loads (later relaxed by the user for one job with automatic fallback).
3. A worker is stopped only by the user's explicit "complete" for that worker.
4. Ask before launching subagents; do not launch more than asked.
5. No outside data beyond what the toolkit and archive give; no invented numbers.

## 6. Mistakes we made and how they were caught (read before repeating)

| Mistake | How it was caught | Fix |
|---|---|---|
| "76 of 84 snapshots good" (counted error pages) | Re-check by parsed listings | 79 of 84; success = parser found listings |
| CDX `resumeKey` paging dropped rows | Compared to one unpaged query | Month windows |
| First analysis used only the first ~20 listings per snapshot | User challenge | Full posting-URL inventory |
| Broad AI rule over-counted | Hand check | Strict versioned rule |
| Live crawler paused as "blocked" | Error text showed the machine was offline | Offline = wait, never a block |
| "178 roles" (placeholders counted) | Worker flagged it; I re-verified | 170 |
| Worker broke an agreed cool-down | Its own heartbeats never mentioned the order | Pace enforced in code |
| Retry "different" verdicts (measurement artifact) | Compared wire bytes | Identical: shells, not throttling |
| `Go` and `apt` regex matches | Independent recompute | Case-sensitive / word-boundary patterns |
| Degree-line rule removed real requirements | My independent recompute differed | Narrower rule, all years re-run |
| `pkill -f name` killed my own shell | Exit code 144 | Kill by PID |
| Reading paths in a book list were wrong (`/hardisk` vs `/Projects/hardisk`) | Existence check | Path fix in the report |

## 7. What is Google-specific and what is reusable

| Reusable as is | Copy and adapt per company |
|---|---|
| `scraper_core` (capture, data repo, Wayback client, pacing guard, extract, safety) | URL prefixes and eras for posting pages |
| The pipeline order and gates | The slug/id format and title parser (`parse_job_url`) |
| Denominator/weak-cell/verification rules | Description page format and the section headings |
| Shard + ledger + detached resumable download pattern | Live search URL pattern, listing selectors, stop rule |
| Term-extraction and drift analysis method | Keyword rules for the target field (security, AI, others) |
| Worker/checkpoint protocol | Anything that depends on how that company's site renders |

## 8. Reproduce the Google results

```
cd ../no-github-remote/web-scrap
.venv/bin/python3 -m pytest tests/test_wayback.py tests/test_wayback_fetch.py tests/test_google_wayback*.py tests/test_google_live.py -q
# analyses that read data already captured (no network; verified to run on 21 Sep 2026):
.venv/bin/python3 - <<'EOF'
from pathlib import Path
from plugins.job_search import REGISTRY
D = Path("../scraper-data")
print(REGISTRY["google_wayback_job_trends"]["run"]("google.com", D)["total_postings"])   # 18188
print(REGISTRY["google_wayback_ai_trends"]["run"]("google.com", D)["rules_version"])
EOF
.venv/bin/python3 ./tracks/gate/career-mapping/google-jd/c4_years.py all      # description analysis, offline (regenerates google-jd files)
.venv/bin/python3 ./tracks/gate/career-mapping/google-live/details/build_checklist.py
```

## 9. Where everything is

See the file map at the end of `02-reusable-prompt.md` (section 12) and the run log in `../PARENT_NOTES.md`.
