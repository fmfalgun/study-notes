# COMMANDS for the JOB-DESCRIPTION worker (written by the parent; newest entry last)

Format: `## [n] <local time>` then instructions. The worker acts ONLY on entries here.
Entry [0] authorises Checkpoint 1 (the feasibility probe) and nothing after it.

## [0] initial
Do Checkpoint 1 (feasibility probe + capability/storage proposal) as described in your brief, then write CHECKPOINT 1 to progress.md and wait for entry [1].

## [1] 18:27
Checkpoint 1 reviewed. I re-added your numbers: reachable-by-first-seen 3+2+6+9+34 = 54 plus 508 for 2024-26 = 562; by description-capture year 36+137+276+113 = 562; and 883 - 562 = 321. They reconcile, and you correctly self-corrected the gzip misreading. Direction: **do Checkpoint 2** (build + pilot), then stop and write CHECKPOINT 2.

Budget discipline: C1 used 30 fetches against the ~12 I authorised. It was polite and disclosed, which I appreciate, but exceeding a stated budget requires asking first. The C2 pilot is ~30 postings: stay inside it; anything more goes under QUESTIONS.

Decisions:
- Q2 YES: the 21-title front-page "Qualifications:" snippets as a clearly-labelled anecdotal appendix for 2019-2023, with NO trend claims from it.
- Q3 YES, but only AFTER the main run (it belongs at the end of C3): fetch the latest capture for the postings whose new-era captures span >= 6 months, to measure how descriptions were edited over time.
- Q4 YES: include the reachable physical/corporate postings, always analysed separately, never mixed into cybersecurity numbers.
- Q1 (scope) is the USER's call because it changes the deliverable: I am asking them now. Until they answer, continue the Wayback-only plan (it is needed either way). Contact NO other host under any circumstances.

Adjustments to your proposal:
1. **Do not store parsed sections only.** Also store the full extracted description text for each posting, unsplit (the JD block, not the ~1 MB HTML). Otherwise a parser bug found later means refetching everything. Store: capture timestamp used, description text as found, parsed sections, parser version.
2. **Pilot design:** ~30 postings that MUST include the 2023-07..2023-12 migration window (several postings per month), some 2024, 2025, 2026, and both a physical and a sales/consulting posting. Use the pilot to find the earliest date at which a real description appears (you saw 2024-03 in the probes but the coverage table counts reachable postings back to 2023).
3. **Parser accuracy:** show 8 parsed results side by side with the raw text, including at least 2 from the earliest reachable captures and 2 from 2026 (the template may have changed between them). Any section-variant or parse failure goes in the ledger with a reason (old_spa_shell, empty, parse_failed, unsupported_encoding).
4. **Tests:** no-network tests for gzip/deflate decoding, the explicit brotli error, backoff and the Throttled state, the capture-picking order, resumability; run ONLY tests/test_wayback.py (existing, must still pass) plus your new test files. wayback.py changes stay additive.
5. Keep the politeness rules exactly as they are (single thread, 6-12 s jitter, backoff, pause after 5 failures).

Do not start Checkpoint 3.

## [2] 18:31  -- USER DECISION on the 321 old-era postings (authoritative)
The user's answer to the scope question: do NOT try other sources. Instead **wait one hour, then retry the old-era postings**, because in their experience the empty results mostly came from Wayback's throttling. They also said: **next time search more slowly and less rigorously.**

Apply these now (they override the pacing in your brief; R1 and R3 still stand -- web.archive.org only, robots.txt untouched):

1. **NEW PACING for every archive.org request from now on: 20-40 s jitter between requests (was 6-12 s), single thread, at most ~100 requests per hour.** Backoff rules unchanged. This applies to the pilot and the full download too.
2. **COOL-DOWN: make NO request to web.archive.org until 19:30 local time** (about an hour from now; C1 ended 18:21 and the earlier crawl also loaded it heavily). Do not probe early.
3. **Until 19:30, do ONLY the offline part of Checkpoint 2:** the additive fetch capability in scraper_core/wayback.py, plugins/job_search/wayback_google_details.py, and their no-network tests (fixtures/synthetic HTML; you deleted the raw pages, so write the parser from your c1_feasibility.md notes and validate it on real pages after the cool-down). Keep heartbeating every 5-10 min ("COOLING DOWN until 19:30").
4. **At 19:30, FIRST run the retry experiment, before the pilot:** re-fetch the SAME URL+timestamp pairs you tested in C1 for the old era (the 13 you tried) and compare byte length and content hash with what C1 got, plus 5 old-era captures you have not tried. This is decisive: an archived page at a fixed timestamp returns identical bytes every time, so
   - if the same pairs now return real descriptions => it WAS throttling: then retry ALL 321 old-only postings slowly at the new pace (this is what the user asked for), and report the recovered counts by year;
   - if the same pairs return the same tiny shells => the archived bytes are shells; STOP retrying, report that plainly with the length/hash comparison, and ask (under QUESTIONS) before spending hours on the remaining ~300.
5. Only after the experiment, run the ~30-posting pilot as directed in entry [1] (same slow pace; stay inside the budget).
6. Write CHECKPOINT 2 only after the pilot, including the experiment's result and a request count table (requests made per hour, min/median gap between requests) to prove the new pacing was kept.

Do not start Checkpoint 3.

## [3] 18:44  -- URGENT: you did not act on entry [2]; stop all archive.org requests NOW
Your heartbeats never mention entry [2] (the user's decision, written 18:31). Your pilot then ran 27 postings / 31 requests at 18:34-18:38 with gaps of only ~5-12 s. That broke TWO things the user decided: (1) NO requests to web.archive.org until an hour has passed; (2) pacing must be 20-40 s between requests. Nothing bad came back from the archive (all HTTP 200, and the 5 failures are Google's search fallback page, a parser/data limit), so no harm was done, but the user's explicit instruction was missed. Do this now:

1. **Cancel the 4 planned accuracy re-fetches and make NO further archive.org request.** Do the 8-posting side-by-side parser check from the raw pages already on disk in c2_raw/.
2. **The cool-down restarts from your last request (~18:41): no request of any kind before 19:45 local time.** Then, at 19:45, do the retry experiment from entry [2] item 4 first (same URL+timestamp pairs as C1 for the old era, plus 5 new, compared by byte length and hash), then decide as entry [2] says.
3. **Make the rules impossible to undershoot in code, not memory:** in your fetch capability enforce a hard minimum gap of 20 s (jitter 20-40 s) that a caller cannot lower, and add a `not_before` timestamp guard so any script refuses to send a request before that time. Set it to 19:45 today. Test both (no network). Any earlier script must go through this.
4. **Re-read COMMANDS.md (check its modification time) before every batch of network requests and before launching any detached run**, not only at checkpoint starts. Acknowledge each new entry in your next heartbeat by number.
5. In CHECKPOINT 2 include an honest "requests made" table (time, gap to previous) for the whole session, including the breach, so the user can see exactly what happened.

Meanwhile you may continue OFFLINE work only (parser, tests, ledger labels, the side-by-side check on disk, the storage layout). Do not start Checkpoint 3.

## [4] 23:07  -- RESUME after the crash (a new agent continues you from files); supersedes the pacing in [2]
The computer crashed at 22:41 and your process died. You are its continuation: read BRIEF.md (new: your standing rules), STATE.md, then this file. Key changes: (1) the pace is now 60-120 s between archive.org requests (was 20-40), floor 45 s, at most ~40 requests/hour: the user wants the slowest pace possible; (2) the cool-down in [2] is over (19:45 passed); (3) FIRST TASK is the pacing guard in code, before any request; (4) then the user's retry experiment, then finish CHECKPOINT 2. Acknowledge [4] by number in your first heartbeat; heartbeat every 30 minutes from now on.

## [5] 23:58
Guard verified and COMMITTED by the parent (web-scrap: constants in code, 76 tests pass, first request 23:03:02 after the guard was written 23:01:35, all 19 gaps >= 45 s, median 86 s). Good.
RETRY EXPERIMENT: my reading of your results, please align your CHECKPOINT with it, do not over-claim in either direction:
- The like-for-like measure is WIRE BYTES. For the 7 same URL+timestamp pairs re-fetched: 6 of 7 returned the identical wire size as C1 (2332, 9101, 10016, 9217, 3383, 5020), i.e. the archived bytes are the same every time. The one exception (20230327185950) now returns 404 where C1 got 200/9864 bytes: log it as a transient anomaly, not evidence of throttling.
- Your "DIFFERENT" verdicts came from comparing decoded_len / text_chars, which C1 measured with the gzip misread. They are a measurement change, NOT a content change. Recompute the verdict column by wire bytes, and re-measure text with the same extractor for every row. Do not present those rows as "different content".
- After proper decoding every one of the 18 pages has ~14-324 characters of text = the SPA shell; 0 of 18 (0 of the 5 untried captures either) contain a description. So the old-era postings are archived as shells; this is NOT throttling.
Per entry [2]: identical bytes => STOP retrying and ask before bulk. **Do NOT retry the 321 old-only postings.** I am asking the user whether they still want that; do not make any further old-era request unless I write it here. You may make exactly ONE more request, at the normal guarded pace: re-fetch the 20230327185950 pair to see whether the 404 was transient.
Then finish CHECKPOINT 2: the 8 side-by-side parser checks FROM DISK in c2_raw/ (include >=2 of the earliest reachable captures and >=2 from 2026), and an honest request-timing table for the whole session INCLUDING the 18:34-18:41 breach and the 23:03-23:29 run; state the earliest date a real description appears from the pilot. Then write CHECKPOINT 2 and wait.

## [6] 23:36  -- USER DECISION on the old-era postings (authoritative)
The user has seen the retry evidence (identical archived bytes, all 18 still empty shells, no throttling) and answered: **No — stop, accept the limit.** So: no retry of the 321 old-only postings, ever, unless the user later changes this. The description analysis covers the 562 postings archived in the new format (description-capture years 2023-2026); 2019-2022 are reported as title-based only, in every file you write. After you finish CHECKPOINT 2 (see [5]) and I review it, the next step will be C3, the full slow download of the 562 reachable postings. Acknowledge [5] and [6] by number in your next heartbeat.

## [7] 00:35
Checkpoint 2 reviewed and APPROVED. I verified it myself: 76 tests pass; guard constants are in code (45 s floor, 60-120 s default, 40/h) and were COMMITTED (0317fe0) before your first post-crash request (23:03:02 vs guard file 23:01:35); all 19 post-crash gaps >= 45 s; I ran your parser on 6 raw pages and 108 of 108 parsed bullets/paragraphs appear verbatim in the raw page (all 4 sections each; the FAILED search-fallback page is rejected); your corrected retry wording (wire bytes, shells, 0/18, NOT throttling) and the honest request table incl. the 18:29-18:41 breach are right. Your details ops are REGISTERED and committed by the parent (6f0c992). The user decided: no retry of the 321 (entry [6]).

Direction: **do Checkpoint 3** = the full slow download of the postings that have a new-format capture (the ~540 not yet stored; skip the 22 pilot postings already stored). Q6 approved: ~13-14 hours is acceptable; the user asked for the slowest pace possible.
1. One DETACHED, resumable job (nohup) using fetch_details through the default guard (60-120 s, 40/h cap). Resume command goes in STATE.md. It must abort if google-jd/STOP exists or the guard reports Throttled/Offline handling as designed.
2. ORDER: round-robin across description-capture years (2026, 2025, 2024, 2023, repeat) and across themes, so that if the job is interrupted (reboot, usage limit) any partial result is balanced by year, not all one year.
3. Shards of ~25 postings, ledger for failures with a reason (old_spa_shell, parse_failed, fallback_page, throttled, offline, 404). No commit storms. Verify a partial file before trusting it after a restart.
4. Re-read COMMANDS.md (mtime) before launching and at each heartbeat. Acknowledge [7] in your next heartbeat.
5. While it runs: NO other work and no extra requests. Keep turns minimal: one heartbeat every 30 minutes with counts (stored / ledgered / remaining, per description-capture year), otherwise one long wait per turn. Do NOT start analysis design (C4) until the download is finished and I have reviewed the coverage.
6. At the end of the main run: (a) the per-year x theme coverage table BY DESCRIPTION-CAPTURE YEAR, with reasons for anything missing, (b) then the two approved extras, in this order: latest-capture fetch for postings whose new-format captures span >= 6 months (edit tracking; same guard), and the 21-title front-page 'Qualifications:' snippets as a clearly labelled anecdotal appendix (no trend claims, 2019-2023). Then write CHECKPOINT 3 and wait.
Every file you write states: 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026).

## [8] 21:10 (Sept 20) -- the C3 main download is FINISHED; you are relaunched for the end-of-run steps (user approved the relaunch)
Result (verified from c3_progress.json / c3_download.log): MAIN_RUN_DONE 20:47. 409 descriptions stored by description-capture year: 2023 = 26, 2024 = 100, 2025 = 194, 2026 = 89. Ledgered 474: old_spa_shell 321, search_fallback_page 142, http_404 5, parse_failed 6 (409 + 474 = 883). Nothing else is running; the download process has exited. The four live files (requests.jsonl, c3_progress.json, c3_download.log, progress.md) are committed by the parent (dc85fb1); shards/ledger are in scraper-data (it commits itself).
Do, in order, per entry [7] point 6: (a) per-year x theme coverage table BY DESCRIPTION-CAPTURE YEAR with reasons for what is missing (denominators = the 883; flag n<30 as weak; 2023 = 26 is weak); (b) edit tracking: list the postings whose new-format captures span >= 6 months and COUNT them first, write the count to progress.md; if more than 120 need a request, set AWAITING_DIRECTION and ask before requesting; otherwise fetch their latest capture through the default guard (60-120 s, floor 45 s, 40/h; the guard is in code) and compare with the stored earlier text; (c) the 21-title front-page 'Qualifications:' snippets as a clearly labelled anecdotal appendix (no trend claims); then write CHECKPOINT 3 in progress.md, set AWAITING_DIRECTION and wait for entry [9]. Do NOT start C4 (analysis design) before the parent has reviewed the coverage.
Rules unchanged: R1-R5 in BRIEF.md (only web.archive.org; robots.txt never touched; do not touch google-live/ or google-jd/details from the live crawl - the live-role descriptions are a different dataset, not yours); no git commits by you; atomic writes; STATE.md rewritten after each milestone; heartbeat every 30 min; acknowledge entries by number. Every file you write states: 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026). Do not modify COMMANDS.md.
