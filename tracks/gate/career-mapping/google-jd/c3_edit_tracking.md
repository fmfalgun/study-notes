# C3 edit tracking: did stored job-description text change later? (Wayback)

Written by the parent (Worker C's agent hit the account usage limit before writing it); numbers are from `c3_edit_results.jsonl`, produced by `c3_edit_track.py`.
**Scope note:** postings are only those Wayback archived. 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026).

## What was tested

- Of the 409 described postings, **261** have a later new-format capture than the capture whose text we stored.
- Only those whose latest capture is **at least 182 days** after the stored one were fetched: **34 postings** (gap 193-589 days; stored-text year 2023: 5, 2024: 28, 2025: 1; themes: sales/consulting 10, threat/response 9, other 7, security engineering 7, physical 1). One request each, through the default guard (45 s floor, about 40 an hour).
- The stored text was compared section by section (about, responsibilities, minimum and preferred qualifications), line by line.

## Result

| Outcome | Postings | Meaning |
|---|---|---|
| `search_fallback_page` | **32** of 34 | The latest capture is Google's generic "Jobs search" page, not the posting: the posting had already been taken down by then |
| `compared` | **2** of 34 | Latest capture is the real posting page |
| of those 2: text changed | **0** | All four sections identical (gaps of 335 and 193 days; 1 posting other_security, 1 threat/response) |
| fetch_failed / parse_failed | 0 | |

## What this does and does not show

- **No edit was observed, but only 2 postings could be compared.** That is far too few to say postings are rarely edited; it says nothing about the other 407.
- The result that *is* solid: **for 32 of 34 postings, the latest archived copy shows the posting was already gone**. That is a fact about how long postings stay live (they are often removed within months of the stored capture), and it means later-capture comparison is not a workable way to track edits with this archive.
- So each stored description should be read as **the text at its capture date** (matching its first-seen year for every one of the 409: coverage Table 4), not as a text that was checked for later edits.
- One manual diagnostic request (a HEAD to web.archive.org at about 22:31 on 20 Sep, outside the guard, 302 in 13.9 s) was made by the agent and disclosed in `progress.md`; it is not in `requests.jsonl` except by that note.
