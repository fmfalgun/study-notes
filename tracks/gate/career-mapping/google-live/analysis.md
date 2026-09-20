# Google's currently open security roles (live crawl, 19 Sep 2026)

Every number here was **recomputed by the parent session** from the crawl files (`pages.jsonl`,
`phase2_state.json`, `deepcheck.json`, `security-roles-live.json`) and, for the comparison, from
`../google-wayback-job-trends.json`. Where the worker's own summary differed, the recomputed
figure is used and the difference is noted.

## Headline

- **170 distinct security-tagged roles** were open on Google's careers site on 19 Sep 2026
  (165 Google, 4 DeepMind, 1 YouTube), found among a board of **3,338 jobs** (all openings, seen on the
  first page of the pilot load). Security-tagged = 5.1% of the board (170 / 3,338).
- 1 of the 170 has no job ID on the page (`id_missing`) and is kept by title + location.
- Themes (title keyword heuristic): security engineering 58, threat/intel/response 41, sales and
  consulting 34, other security 31, physical/corporate security 6.
- 31 roles are flagged remote-eligible (an icon on the listing, not a promise from Google).
- This is a **snapshot of one day** (a stock of open roles), not hiring volume and not a trend.

## What was crawled

83 page loads between 2026-09-19 12:24 and 21:56 UTC (17:54 to 03:26 IST):

| Kind | Loads |
|---|---|
| Landing page | 1 (good) |
| Pilot results page (no search term) | 1 (good) |
| Search-term pages | 81: **76 good**, 5 not good |

(The worker reported "78 good search pages"; 78 counts the landing and pilot loads as well. 76 is the
number of good *search-term* pages.)

The 5 not-good loads: four retries of `threat` page 4 (a browser session error at 13:15, then three
"internet disconnected" errors between 14:55 and 15:27 while the machine was offline) and one empty
`cryptography` page 3 (21:18) that was retried successfully. None was a block or throttle: the
`blocked` and `throttled` fields are empty on every load. An earlier automatic "PAUSED_BLOCKED" was a
false alarm caused by the offline errors and was fixed (offline now means wait, never count as a block).

## Per-term results

Search terms ran in this order. "New roles" is the number of roles first found by that term, **after the
duplicate correction** (the worker's table said security 164 / cybersecurity 10 / threat 4 = 178; the
corrected list is 162 / 6 / 2 = 170 because 8 rows were title-keyed duplicates of real-ID rows).

| Term | Pages | Board jobs matching | Tagged titles seen | New roles | Roles it hits (any order) |
|---|---|---|---|---|---|
| security | 13 | 1,409 | 165 | 162 | 162 |
| cybersecurity | 10 | 235 | 105 | 6 | 101 |
| threat | 9 | 163 | 100 | 2 | 98 |
| incident response | 6 | 721 | 57 | 0 | 54 |
| vulnerability | 3 | 49 | 34 | 0 | 31 |
| malware | 3 | 59 | 27 | 0 | 27 |
| red team | 2 | 33 | 16 | 0 | 15 |
| penetration testing | 10 | 182 | 62 | 0 | 58 |
| detection | 11 | 851 | 63 | 0 | 61 |
| cryptography | 4 | 950 | 17 | 0 | 15 |

Reading it: one word, "security", finds 162 of 170 (95%). Seven terms after the first three found
nothing new, so the shorter 3-term walk (security, cybersecurity, threat) is now the plugin default.
The "roles it hits" column is bigger than "new roles" because most roles match several terms
(33 match one term, 137 match two to eight).

## Was the crawl deep enough?

The stop rule for each term was "a page with zero security-tagged titles" or "last page". As a check
against a badly ordered result list, `security` was re-loaded at pages 20, 35, 50, 65 and 71 (71 is the
last page): 0 tagged titles on each, 0 new roles. Recall by this test: no sign of missed roles deeper in the list.

**Known blind spot:** the tagger only sees titles. 4 titles that look security-related but carry no security
keyword are kept apart as "possible" (all four are Mandiant consulting roles: a Senior Strategic AppSec Consultant, a
Detection and SOAR Engineer, a Consulting Leader, and a Senior Project Manager).
They are **not** in the 170. If they count, the total is 174.

## Live roles vs the Wayback 2026 archive (titles only)

| | Live crawl, 19 Sep | Wayback, 2026 to Sep |
|---|---|---|
| Distinct security-tagged titles | 160 (from 170 roles) | 111 (from 118 postings) |
| Titles in both (exact, punctuation ignored) | 14 | 14 |
| Cloud in the title | 69 of 170 = 40.6% | 36 of 118 = 30.5% |
| Mandiant in the title | 32 of 170 = 18.8% | 21 of 118 = 17.8% |

- Only **14 titles match exactly** (the worker's report said 15; 14 is what the normalized comparison gives).
  Language suffixes such as "(Japanese, English)" make many live titles look different from their archived
  form; ignoring parentheses does not add matches (still 14).
- Mandiant share is stable (about 18%) and Cloud share is higher live than in the archive. Both are
  consistent with the Wayback finding that security sits inside Google Cloud and Mandiant.
- 14 live titles contain AI, ML or agent words (8.2% of 170). That uses a broader word list than the
  strict rule in `google-wayback-ai-analysis.md` (4.2% for 2026), so **do not compare the two figures.**

**Caveats.** The live list is what is open now; the archive is what Wayback happened to capture across
months. Similar shares do not prove the same hiring, and a different share may reflect either. Titles
say nothing about skills. Causes stay inference.

## Pace record (kept honest)

The crawl was meant to be slow. It was slow but **not uniformly as slow as later rules require**:

- Gaps between loads: minimum 59 s, median 252 s; 27 of 82 gaps were under 180 s. The crawler's 180 to 360 s gap
  rule is what the plugin now enforces; the early `security` pages ran at 63 to 171 s, i.e. faster than that rule.
- The busiest hour was 20 loads (12:00 UTC hour, which began at 12:24), above the later 12 loads/hour cap.
- The longest gap was about 2 hours (offline period and machine reboot).
- No block, captcha or throttle was recorded on any load; no robots.txt request was made.

## Incidents

| When (UTC) | What | Effect |
|---|---|---|
| 13:15 | Browser "invalid session id" on threat page 4 | Retried; nothing lost |
| 14:55 to 15:27 | Machine offline (three loads failed) | Misread as a block first; fixed |
| ~17:10 | Machine crash and reboot | Crawl resumed from saved state |
| Various | Two agent usage-limit stops | Detached scripts kept running; state on disk |
| 21:18 | Cryptography page 3 empty | Retried once, good |

## Corrections applied to the role list (commit `6dfe94c`)

Earlier claim of "178 distinct roles" was wrong: it counted title-key placeholders. Eight duplicate rows
removed, description text trimmed out of 4 DeepMind locations, and icon-font text "laptop_windowsRemote
eligible" moved from 32 locations into the `remote_eligible` flag.
