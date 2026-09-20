# STATE (rewritten 00:21 IST 20 Sep) -- COMMANDS read: [0]..[7]; STOP: none
phase: CHECKPOINT 3 = C3 main download RUNNING (detached, started 00:19 IST). Old-era 321 ledgered old_spa_shell with no requests; user decision [6]: never retry them. Every file: 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026).
job: google-jd/c3_download.py (round-robin across description-capture years 2026/2025/2024/2023 and themes; chunks of 25 via wayback_google_details.fetch_details; guard 60-120 s, 40/h; exits at next posting if STOP exists or COMMANDS.md mtime changes; handles Throttled (60 min pause) and Offline (10 min wait)). Log: c3_download.log; counters: c3_progress.json; requests: requests.jsonl.
resume (safe any time; idempotent): cd ../no-github-remote/web-scrap && nohup .venv/bin/python3 ./tracks/gate/career-mapping/google-jd/c3_download.py >> ./tracks/gate/career-mapping/google-jd/c3_download.log 2>&1 &
check first whether it is running: pgrep -f c3_download.py
start: stored 22 (pilot), ledgered 326 (321 old_spa_shell + 5 search fallback), requestable remaining 535 (2025:270, 2024:134, 2026:109, 2023:22 by description-capture year). ~13-14 h.
while running: no other work, no extra requests, no C4 design. Heartbeat every 30 min with counts (c3_progress.json).
at the end of the main run: (a) per-year x theme coverage table by DESCRIPTION-CAPTURE year with reasons for missing; (b) latest-capture fetch for postings whose new-format captures span >= 6 months (edit tracking, same guard); (c) the 21-title front-page 'Qualifications:' snippets as a labelled anecdotal appendix (no trend claims, 2019-2023); then write CHECKPOINT 3 and wait for the parent.
last archive.org request: see requests.jsonl (job running).
