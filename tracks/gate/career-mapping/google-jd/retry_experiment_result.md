# Retry experiment (COMMANDS [2]-4, [4], [5]) -- the archived old-era pages are shells; not throttling

Run 2026-09-19 23:03-23:29 IST at the guarded pace. 18 URL+timestamp pairs (7 first-capture pairs and 6 alternative-capture pairs from C1, plus 5 never tried) + ONE re-request of the 404 pair (the one extra request allowed by entry [5]). Raw bodies: retry_raw/; data: retry_experiment_results.json, retry_experiment_404_recheck.json.

Like-for-like measure = WIRE BYTES (compressed size as served). C1's decoded/character counts were affected by the gzip misread (C1 measured undecoded bytes as characters), so differences in those columns are a measurement change, not a content change; they are not used for any verdict. C1 stored no hashes (its raw pages were deleted), so equality is judged on wire size; today's sha256 values are in the results JSON for future comparisons.

| # | kind | capture ts | C1 wire bytes | now wire bytes | verdict (wire) | text chars, whole document / inside <body>, same extractor for all | description headings |
|---|---|---|---|---|---|---|---|
| 1 | c1_first_capture | 20190919050245 | 5020 | 5020 | identical | 14 / 0 | none |
| 2 | c1_first_capture | 20200803131344 | 2332 | 2332 | identical | 35 / 0 | none |
| 3 | c1_first_capture | 20211022223242 | 9101 | 9101 | identical | 278 / 0 | none |
| 4 | c1_first_capture | 20221121170318 | 10016 | 10016 | identical | 318 / 0 | none |
| 5 | c1_first_capture | 20220215125433 | 9217 | 9217 | identical | 290 / 0 | none |
| 6 | c1_first_capture | 20230327185950 | 9864 | HTTP 404 (re-check 23:28:56: 200, 9864) | identical on re-check; first run = transient 404 anomaly | 310 / 0 | none |
| 7 | c1_first_capture | 20230522201744 | 3383 | 3383 | identical | 311 / 0 | none |
| 8 | c1_alt_last_capture | 20211214210916 | not recorded (C1 kept decoded length 9272) | 9272 | decoded length identical = C1's; wire not comparable | 301 / 0 | none |
| 9 | c1_alt_last_capture | 20230311151108 | not recorded (C1 kept decoded length 9839) | 9839 | decoded length identical = C1's; wire not comparable | 305 / 0 | none |
| 10 | c1_alt_last_capture | 20230123002816 | not recorded (C1 kept decoded length 9765) | 3416 | decoded length identical = C1's; wire not comparable | 278 / 0 | none |
| 11 | c1_alt_last_capture | 20230603140437 | not recorded (C1 kept decoded length 9618) | 9618 | decoded length identical = C1's; wire not comparable | 278 / 0 | none |
| 12 | c1_alt_last_capture | 20220120042123 | not recorded (C1 kept decoded length 9257) | 9257 | decoded length identical = C1's; wire not comparable | 298 / 0 | none |
| 13 | c1_alt_last_capture | 20230321072248 | not recorded (C1 kept decoded length 9648) | 9648 | decoded length identical = C1's; wire not comparable | 278 / 0 | none |
| 14 | new_untried | 20190303095023 | - | 5555 | new capture, never tried | 14 / 0 | none |
| 15 | new_untried | 20201110043835 | - | 8082 | new capture, never tried | 278 / 0 | none |
| 16 | new_untried | 20210222230816 | - | 2810 | new capture, never tried | 278 / 0 | none |
| 17 | new_untried | 20221201210326 | - | 3438 | new capture, never tried | 295 / 0 | none |
| 18 | new_untried | 20220630192058 | - | 3217 | new capture, never tried | 324 / 0 | none |

Reading (no over-claim):
- 7 same-pair re-fetches of C1's first captures: 6/7 returned the identical wire size at once (5020, 2332, 9101, 10016, 9217, 3383). The 7th (20230327185950) returned HTTP 404 on the first attempt, where C1 got 200/9864 B, and 200 with 9864 B again on the single allowed re-check 45 s after the previous request: a transient archive anomaly, logged as such, not evidence of throttling (a 404 is a definitive-looking answer, not a refusal/429).
- 6 alternative-capture pairs: C1 recorded only decoded length; today's decoded length is identical for all 6 (wire size not comparable).
- With ONE extractor over all 18 pages: 14-324 characters of text in the whole document (title/meta/noscript boilerplate), 0 inside <body>; none contains 'About the job', 'Minimum qualifications', 'Preferred qualifications' or 'Responsibilities'. 0 of 18 (0 of the 5 untried captures either) contain a description => old-era postings are archived as empty single-page-app shells.
- Recovered old-era descriptions: 0 (0 in each of 2019-2023). NOT throttling: the same bytes come back.
- Per entry [5]: the 321 old-only postings are NOT being retried; no old-era request will be made unless the parent writes it in COMMANDS.md.
