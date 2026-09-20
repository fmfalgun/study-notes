# C3 coverage of security-posting descriptions (Wayback)

**Scope note (applies to every table):** postings are only those Wayback archived (883 security postings, first-seen 2019-2026). 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026). Description-capture year = the year of the archived capture the text was parsed from (not the year the posting was first seen). Themes: physical_corporate_security is NOT cybersecurity and must be analysed separately. n<30 flagged weak (W).

## Table 1. Description-capture year x theme (denominator = 883 postings)

| theme | postings | 2023 | 2024 | 2025 | 2026 | described total | no description | described % |
|---|---|---|---|---|---|---|---|---|
| other_security | 142 | 4 W | 20 W | 15 W | 13 W | 52 | 90 | 36.6% |
| physical_corporate_security | 50 | 0 | 8 W | 11 W | 3 W | 22 | 28 | 44.0% |
| sales_and_consulting | 151 | 3 W | 15 W | 30 | 14 W | 62 | 89 | 41.1% |
| security_engineering | 326 | 10 W | 32 | 71 | 42 | 155 | 171 | 47.5% |
| threat_intel_and_response | 214 | 9 W | 25 W | 67 | 17 W | 118 | 96 | 55.1% |
| ALL | 883 | 26 W | 100 | 194 | 89 | 409 | 474 | 46.3% |

W = n<30 (weak: treat any share from that cell as anecdotal). The 4 year columns count each posting once, under the year of the capture whose text was stored.

## Table 2. Why a posting has NO description, by theme (denominator per row = postings in that theme)

| theme | no description | old_spa_shell | search_fallback_page | http_404 | parse_failed |
|---|---|---|---|---|---|
| other_security | 90 | 55 | 32 | 0 | 3 |
| physical_corporate_security | 28 | 23 | 5 | 0 | 0 |
| sales_and_consulting | 89 | 60 | 26 | 2 | 1 |
| security_engineering | 171 | 127 | 43 | 0 | 1 |
| threat_intel_and_response | 96 | 56 | 36 | 3 | 1 |
| ALL | 474 | 321 | 142 | 5 | 6 |

Reasons: old_spa_shell = the posting was archived only in Google's OLD site format (<=2023-05), whose pages are empty single-page-app shells (0/18 retried pairs held any description, see retry_experiment_result.md); the 321 were never requested again. search_fallback_page = the archived URL returned Google's 'Jobs search' results page (the posting was gone at capture time; it lists OTHER jobs). http_404 = the archive returned 404 for the tried captures. parse_failed = a page came back but no description section parsed (6 postings).

## Table 3. First-seen year x outcome (denominator = postings first seen that year)

| first-seen year | postings | described | described % | old_spa_shell | search_fallback | 404 | parse_failed |
|---|---|---|---|---|---|---|---|
| 2019 | 8 W | 0 | 0% | 5 | 3 | 0 | 0 |
| 2020 | 14 W | 0 | 0% | 12 | 2 | 0 | 0 |
| 2021 | 70 | 0 | 0% | 64 | 6 | 0 | 0 |
| 2022 | 168 | 0 | 0% | 159 | 9 | 0 | 0 |
| 2023 | 115 | 26 | 23% | 81 | 5 | 0 | 3 |
| 2024 | 131 | 100 | 76% | 0 | 29 | 0 | 2 |
| 2025 | 265 | 194 | 73% | 0 | 65 | 5 | 1 |
| 2026 | 112 | 89 | 79% | 0 | 23 | 0 | 0 |
| ALL | 883 | 409 | 46% | 321 | 142 | 5 | 6 |

Read: a 2019-2022 posting is described only if it was captured again after mid-2023, and then the text is the 2023+ text (not the wording at the time it was first seen).

## Table 4. Description-capture year x first-seen year (described postings only; shows how much 2023+ text belongs to older postings)

| first-seen year | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|
| 2019 | 0 | 0 | 0 | 0 | 0 |
| 2020 | 0 | 0 | 0 | 0 | 0 |
| 2021 | 0 | 0 | 0 | 0 | 0 |
| 2022 | 0 | 0 | 0 | 0 | 0 |
| 2023 | 26 | 0 | 0 | 0 | 26 |
| 2024 | 0 | 100 | 0 | 0 | 100 |
| 2025 | 0 | 0 | 194 | 0 | 194 |
| 2026 | 0 | 0 | 0 | 89 | 89 |

## Edit-tracking candidate count (offline)

- Postings with new-format captures spanning >=182 days (earliest to latest new-format capture), ANY outcome: 47 of 883.
- Of the 409 described postings, ones with a later new-format capture than the stored text: 261; with the latest capture >=182 days after the stored capture (a request is needed for each): **34**.
- By theme (>=182d): {'sales_and_consulting': 10, 'other_security': 7, 'threat_intel_and_response': 9, 'security_engineering': 7, 'physical_corporate_security': 1}
- By stored-text year (>=182d): {'2023': 5, '2024': 28, '2025': 1}
