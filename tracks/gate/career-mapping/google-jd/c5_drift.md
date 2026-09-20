# C5 drift: wording changes 2024 -> 2025 -> 2026 (description-capture years)

**Scope and limits.** Postings are only those Wayback archived; each year's postings are the ones archived with a new-format page in that year, so the years are NOT random samples of Google's security roles and their theme mix differs. 2019-2022 postings are title-based only (no recoverable descriptions); descriptions start mid-2023. **2023 (n = 26) is weak and is NOT compared.** Text is a snapshot at capture date; causes are inference and none is claimed. Term counts are phrase matching (heuristic); regex rows are documented regexes (c4_years.py).

**Rule (entry [10]).** A group is compared only if it has n>=30 in EVERY year of the comparison. A difference is listed only if it is >= 10 percentage points AND the posting count behind the higher share is >= 8 (my reading of '>= 8 postings'; counts are printed so any other reading can be applied). Shares are with denominators. Many terms are tested (counts below), so some listed differences will arise by chance; treat the list as candidates to read, not as proven change.

### Group sizes and theme mix

| year | ALL | security_engineering | threat_intel_and_response | sales_and_consulting | other_security | physical_corporate_security |
|---|---|---|---|---|---|---|
| 2024 | 100 | 32 | 25 W | 15 W | 20 W | 8 W |
| 2025 | 194 | 71 | 67 | 30 | 15 W | 11 W |
| 2026 | 89 | 42 | 17 W | 14 W | 13 W | 3 W |

Groups compared: **ALL** (n = 100, 194, 89) and **security_engineering** (n = 32, 71, 42). **threat_intel_and_response is NOT compared** (n = 25, 67, 17; 2024 and 2026 are below 30, W); only 2025 has n>=30 for it. sales_and_consulting (n = 15, 30, 14) is also below 30 in 2024 and 2026. Because the theme mix changes (the ALL level mixes different proportions of engineering, threat and sales roles), an ALL-level difference may reflect the archive's mix rather than a change in wording; the security_engineering comparison is the like-for-like one.

## Group: ALL (n = 2024: 100, 2025: 194, 2026: 89; distinct-text postings 2024: 98, 2025: 183, 2026: 84)

Terms x sections tested (a term must reach >=5 postings in some year): 2343. Listed (>=10 pp and >=8 postings in at least one pair): 127; shown: top 45 by size of difference.

| term | section | 2024 (n=100) | 2025 (n=194) | 2026 (n=89) | flagged pairs: change in pp [same on distinct-text postings] |
|---|---|---|---|---|---|
| security | responsibilities | 60/100 (60%) | 118/194 (61%) | 76/89 (85%) | 2025->2026: +25 [+24]; 2024->2026: +25 [+26] |
| secure | any | 10/100 (10%) | 30/194 (15%) | 30/89 (34%) | 2025->2026: +18 [+15]; 2024->2026: +24 [+21] |
| secure | responsibilities | 7/100 (7%) | 22/194 (11%) | 26/89 (29%) | 2025->2026: +18 [+15]; 2024->2026: +22 [+20] |
| security engineering | any | 12/100 (12%) | 35/194 (18%) | 30/89 (34%) | 2025->2026: +16 [+15]; 2024->2026: +22 [+19] |
| infrastructure | preferred | 9/100 (9%) | 12/194 (6%) | 24/89 (27%) | 2025->2026: +21 [+20]; 2024->2026: +18 [+16] |
| engineering | any | 45/100 (45%) | 79/194 (41%) | 54/89 (61%) | 2025->2026: +20 [+20]; 2024->2026: +16 [+15] |
| security assessments | any | 13/100 (13%) | 30/194 (15%) | 29/89 (33%) | 2025->2026: +17 [+13]; 2024->2026: +20 [+16] |
| protocols | required | 16/100 (16%) | 19/194 (10%) | 26/89 (29%) | 2025->2026: +19 [+16]; 2024->2026: +13 [+10] |
| vulnerabilities | any | 19/100 (19%) | 51/194 (26%) | 34/89 (38%) | 2025->2026: +12 [+12]; 2024->2026: +19 [+19] |
| ai | any | 4/100 (4%) | 19/194 (10%) | 20/89 (22%) | 2025->2026: +13 [+15]; 2024->2026: +18 [+20] |
| security engineering | required | 11/100 (11%) | 27/194 (14%) | 26/89 (29%) | 2025->2026: +15 [+14]; 2024->2026: +18 [+16] |
| protocols | any | 30/100 (30%) | 35/194 (18%) | 32/89 (36%) | 2024->2025: -12 [-11]; 2025->2026: +18 [+14] |
| infrastructure | any | 25/100 (25%) | 51/194 (26%) | 38/89 (43%) | 2025->2026: +16 [+17]; 2024->2026: +18 [+16] |
| reports | any | 30/100 (30%) | 47/194 (24%) | 11/89 (12%) | 2025->2026: -12 [-14]; 2024->2026: -18 [-17] |
| risk | preferred | 9/100 (9%) | 22/194 (11%) | 23/89 (26%) | 2025->2026: +15 [+15]; 2024->2026: +17 [+18] |
| coding | any | 17/100 (17%) | 37/194 (19%) | 30/89 (34%) | 2025->2026: +15 [+12]; 2024->2026: +17 [+15] |
| engineering | required | 29/100 (29%) | 44/194 (23%) | 35/89 (39%) | 2025->2026: +17 [+16]; 2024->2026: +10 [+10] |
| security protocols | required | 10/100 (10%) | 16/194 (8%) | 22/89 (25%) | 2025->2026: +16 [+14]; 2024->2026: +15 [+12] |
| security protocols | any | 12/100 (12%) | 23/194 (12%) | 25/89 (28%) | 2025->2026: +16 [+14]; 2024->2026: +16 [+14] |
| computer | any | 13/100 (13%) | 26/194 (13%) | 26/89 (29%) | 2025->2026: +16 [+13]; 2024->2026: +16 [+14] |
| network security | required | 17/100 (17%) | 21/194 (11%) | 24/89 (27%) | 2025->2026: +16 [+12] |
| findings | any | 15/100 (15%) | 40/194 (21%) | 4/89 (4%) | 2025->2026: -16 [-16]; 2024->2026: -11 [-10] |
| ai | responsibilities | 2/100 (2%) | 18/194 (9%) | 16/89 (18%) | 2024->2026: +16 [+17] |
| platforms | preferred | 10/100 (10%) | 34/194 (18%) | 23/89 (26%) | 2024->2026: +16 [+15] |
| reports | responsibilities | 27/100 (27%) | 43/194 (22%) | 10/89 (11%) | 2025->2026: -11 [-13]; 2024->2026: -16 [-15] |
| security assessments | required | 9/100 (9%) | 22/194 (11%) | 22/89 (25%) | 2025->2026: +13 [+9]; 2024->2026: +16 [+12] |
| remediation | any | 6/100 (6%) | 11/194 (6%) | 19/89 (21%) | 2025->2026: +16 [+15]; 2024->2026: +15 [+15] |
| general purpose languages | any | 13/100 (13%) | 20/194 (10%) | 23/89 (26%) | 2025->2026: +16 [+13]; 2024->2026: +13 [+11] |
| general purpose languages | required | 13/100 (13%) | 20/194 (10%) | 23/89 (26%) | 2025->2026: +16 [+13]; 2024->2026: +13 [+11] |
| risk | any | 35/100 (35%) | 66/194 (34%) | 44/89 (49%) | 2025->2026: +15 [+15]; 2024->2026: +14 [+13] |
| computer | required | 11/100 (11%) | 16/194 (8%) | 21/89 (24%) | 2025->2026: +15 [+13]; 2024->2026: +13 [+10] |
| audiences | any | 22/100 (22%) | 41/194 (21%) | 6/89 (7%) | 2025->2026: -14 [-15]; 2024->2026: -15 [-15] |
| access | any | 14/100 (14%) | 36/194 (19%) | 26/89 (29%) | 2025->2026: +11 [+12]; 2024->2026: +15 [+15] |
| controls | preferred | 18/100 (18%) | 23/194 (12%) | 24/89 (27%) | 2025->2026: +15 [+14] |
| security | required | 57/100 (57%) | 116/194 (60%) | 64/89 (72%) | 2025->2026: +12 [+11]; 2024->2026: +15 [+12] |
| information security | preferred | 16/100 (16%) | 17/194 (9%) | 1/89 (1%) | 2024->2026: -15 [-14] |
| problems | any | 26/100 (26%) | 27/194 (14%) | 10/89 (11%) | 2024->2025: -12 [-11]; 2024->2026: -15 [-14] |
| industry | any | 27/100 (27%) | 49/194 (25%) | 11/89 (12%) | 2025->2026: -13 [-13]; 2024->2026: -15 [-13] |
| agentic | any | 0/100 (0%) | 2/194 (1%) | 13/89 (15%) | 2025->2026: +14 [+14]; 2024->2026: +15 [+15] |
| engineering | preferred | 13/100 (13%) | 22/194 (11%) | 23/89 (26%) | 2025->2026: +15 [+13]; 2024->2026: +13 [+12] |
| programming languages | any | 13/100 (13%) | 53/194 (27%) | 13/89 (15%) | 2024->2025: +14 [+12]; 2025->2026: -13 [-10] |
| vulnerabilities | responsibilities | 14/100 (14%) | 35/194 (18%) | 25/89 (28%) | 2025->2026: +10 [+11]; 2024->2026: +14 [+14] |
| coding | required | 15/100 (15%) | 25/194 (13%) | 24/89 (27%) | 2025->2026: +14 [+12]; 2024->2026: +12 [+10] |
| assessments | any | 30/100 (30%) | 66/194 (34%) | 39/89 (44%) | 2024->2026: +14 [+11] |
| cycle | any | 1/100 (1%) | 8/194 (4%) | 13/89 (15%) | 2025->2026: +10 [+12]; 2024->2026: +14 [+14] |

**Regex metrics, ALL** (documented regexes; * = meets both thresholds in at least one pair)

| metric | 2024 (n=100) | 2025 (n=194) | 2026 (n=89) | flagged pairs (pp) |
|---|---|---|---|---|---|
| 'bachelor' in required | 91/100 (91%) | 190/194 (98%) | 84/89 (94%) | - |
| master/masters/PhD/doctorate/doctoral wording in preferred | 25/100 (25%) | 45/194 (23%) | 18/89 (20%) | - |
| same wording in required | 0/100 (0%) | 3/194 (2%) | 3/89 (3%) | - |
| the phrase 'advanced degree' in preferred (often 'or N years of experience with an advanced degree') | 0/100 (0%) | 3/194 (2%) | 1/89 (1%) | - |
| 'certification' in preferred * | 28/100 (28%) | 47/194 (24%) | 14/89 (16%) | 2024->2026: -12 |
| 'certification' in required | 3/100 (3%) | 5/194 (3%) | 2/89 (2%) | - |
| 'clearance' in required * | 7/100 (7%) | 27/194 (14%) | 3/89 (3%) | 2025->2026: -11 |
| 'travel' in required | 6/100 (6%) | 28/194 (14%) | 8/89 (9%) | - |
| 'python' in required * | 14/100 (14%) | 36/194 (19%) | 6/89 (7%) | 2025->2026: -12 |
| 'c++' in required * | 13/100 (13%) | 37/194 (19%) | 8/89 (9%) | 2025->2026: -10 |
| 'java' (word) in required | 12/100 (12%) | 24/194 (12%) | 7/89 (8%) | - |
| 'software development' in required * | 15/100 (15%) | 48/194 (25%) | 12/89 (13%) | 2025->2026: -11 |
| 'programming language' in required * | 12/100 (12%) | 44/194 (23%) | 9/89 (10%) | 2024->2025: +11; 2025->2026: -13 |
| 'network forensics' in required | 8/100 (8%) | 18/194 (9%) | 1/89 (1%) | - |
| 'incident response' in required | 12/100 (12%) | 23/194 (12%) | 12/89 (13%) | - |
| 'incident response' in preferred | 11/100 (11%) | 30/194 (15%) | 13/89 (15%) | - |
| 'malware' in required | 13/100 (13%) | 21/194 (11%) | 6/89 (7%) | - |
| 'cloud' (word) in required | 24/100 (24%) | 31/194 (16%) | 16/89 (18%) | - |
| 'cybersecurity'/'cyber security' in required | 30/100 (30%) | 62/194 (32%) | 27/89 (30%) | - |
| 'threat intelligence' in preferred | 8/100 (8%) | 19/194 (10%) | 4/89 (4%) | - |
| software-engineer template: required has 'software development' AND ('programming language' OR 'data structures') | 10/100 (10%) | 36/194 (19%) | 9/89 (10%) | - |
| security-engineer template: required has 'security assessments' AND 'security protocols' * | 8/100 (8%) | 13/194 (7%) | 20/89 (22%) | 2025->2026: +16; 2024->2026: +14 |
| 'machine learning' or 'artificial intelligence' or 'AI' (word) in any section * | 6/100 (6%) | 26/194 (13%) | 26/89 (29%) | 2025->2026: +16; 2024->2026: +23 |

**Stayed the same, ALL** (term in >=20% of postings in at least one year, any section, and highest minus lowest share across the three years < 5 pp; top 25)

| term | 2024 | 2025 | 2026 |
|---|---|---|---|
| response | 40/100 (40%) | 75/194 (39%) | 38/89 (43%) |
| customer | 33/100 (33%) | 67/194 (35%) | 31/89 (35%) |
| operations | 31/100 (31%) | 59/194 (30%) | 26/89 (29%) |
| client | 28/100 (28%) | 56/194 (29%) | 25/89 (28%) |
| python | 26/100 (26%) | 53/194 (27%) | 22/89 (25%) |
| detection | 27/100 (27%) | 51/194 (26%) | 24/89 (27%) |
| program | 23/100 (23%) | 48/194 (25%) | 23/89 (26%) |
| leadership | 23/100 (23%) | 50/194 (26%) | 20/89 (22%) |
| intelligence | 25/100 (25%) | 43/194 (22%) | 19/89 (21%) |
| executive | 24/100 (24%) | 46/194 (24%) | 22/89 (25%) |
| managing | 24/100 (24%) | 39/194 (20%) | 21/89 (24%) |
| sources | 19/100 (19%) | 46/194 (24%) | 19/89 (21%) |
| standards | 20/100 (20%) | 43/194 (22%) | 16/89 (18%) |
| cyber | 17/100 (17%) | 39/194 (20%) | 19/89 (21%) |
| travel | 17/100 (17%) | 39/194 (20%) | 14/89 (16%) |
| security controls | 20/100 (20%) | 30/194 (15%) | 17/89 (19%) |

## Group: security_engineering (n = 2024: 32, 2025: 71, 2026: 42; distinct-text postings 2024: 31, 2025: 65, 2026: 38)

Terms x sections tested (a term must reach >=5 postings in some year): 677. Listed (>=10 pp and >=8 postings in at least one pair): 256; shown: top 45 by size of difference.

| term | section | 2024 (n=32) | 2025 (n=71) | 2026 (n=42) | flagged pairs: change in pp [same on distinct-text postings] |
|---|---|---|---|---|---|
| security | responsibilities | 14/32 (44%) | 39/71 (55%) | 38/42 (90%) | 2024->2025: +11 [+13]; 2025->2026: +36 [+34]; 2024->2026: +47 [+47] |
| security | preferred | 14/32 (44%) | 43/71 (61%) | 34/42 (81%) | 2024->2025: +17 [+13]; 2025->2026: +20 [+20]; 2024->2026: +37 [+34] |
| risk | any | 5/32 (16%) | 20/71 (28%) | 22/42 (52%) | 2024->2025: +13 [+13]; 2025->2026: +24 [+21]; 2024->2026: +37 [+34] |
| secure | any | 5/32 (16%) | 19/71 (27%) | 22/42 (52%) | 2024->2025: +11 [+13]; 2025->2026: +26 [+18]; 2024->2026: +37 [+31] |
| ai | any | 0/32 (0%) | 8/71 (11%) | 15/42 (36%) | 2024->2025: +11 [+12]; 2025->2026: +24 [+27]; 2024->2026: +36 [+39] |
| security | any | 21/32 (66%) | 62/71 (87%) | 42/42 (100%) | 2024->2025: +22 [+18]; 2025->2026: +13 [+14]; 2024->2026: +34 [+32] |
| security engineering | any | 6/32 (19%) | 20/71 (28%) | 22/42 (52%) | 2025->2026: +24 [+24]; 2024->2026: +34 [+31] |
| secure | responsibilities | 3/32 (9%) | 13/71 (18%) | 18/42 (43%) | 2025->2026: +25 [+19]; 2024->2026: +33 [+30] |
| programming languages | any | 10/32 (31%) | 35/71 (49%) | 7/42 (17%) | 2024->2025: +18 [+15]; 2025->2026: -33 [-29]; 2024->2026: -15 [-14] |
| security engineering | required | 5/32 (16%) | 14/71 (20%) | 20/42 (48%) | 2025->2026: +28 [+27]; 2024->2026: +32 [+31] |
| network security | required | 6/32 (19%) | 10/71 (14%) | 19/42 (45%) | 2025->2026: +31 [+27]; 2024->2026: +26 [+23] |
| programming | required | 10/32 (31%) | 35/71 (49%) | 8/42 (19%) | 2024->2025: +18 [+15]; 2025->2026: -30 [-27]; 2024->2026: -12 [-11] |
| software development | required | 11/32 (34%) | 35/71 (49%) | 8/42 (19%) | 2024->2025: +15 [+11]; 2025->2026: -30 [-25]; 2024->2026: -15 [-14] |
| programming | any | 13/32 (41%) | 40/71 (56%) | 11/42 (26%) | 2024->2025: +16 [+12]; 2025->2026: -30 [-28]; 2024->2026: -14 [-16] |
| access | any | 2/32 (6%) | 19/71 (27%) | 15/42 (36%) | 2024->2025: +21 [+17]; 2024->2026: +29 [+30] |
| research | any | 2/32 (6%) | 14/71 (20%) | 15/42 (36%) | 2024->2025: +13 [+12]; 2025->2026: +16 [+18]; 2024->2026: +29 [+30] |
| research | responsibilities | 2/32 (6%) | 9/71 (13%) | 15/42 (36%) | 2025->2026: +23 [+23]; 2024->2026: +29 [+30] |
| network security | any | 6/32 (19%) | 13/71 (18%) | 20/42 (48%) | 2025->2026: +29 [+25]; 2024->2026: +29 [+25] |
| coding | any | 9/32 (28%) | 29/71 (41%) | 24/42 (57%) | 2024->2025: +13 [+14]; 2025->2026: +16 [+15]; 2024->2026: +29 [+29] |
| ai | responsibilities | 0/32 (0%) | 7/71 (10%) | 12/42 (29%) | 2025->2026: +19 [+21]; 2024->2026: +29 [+32] |
| software | required | 16/32 (50%) | 38/71 (54%) | 11/42 (26%) | 2025->2026: -27 [-22]; 2024->2026: -24 [-23] |
| python | required | 11/32 (34%) | 23/71 (32%) | 3/42 (7%) | 2025->2026: -25 [-26]; 2024->2026: -27 [-28] |
| assessments | required | 5/32 (16%) | 12/71 (17%) | 18/42 (43%) | 2025->2026: +26 [+21]; 2024->2026: +27 [+23] |
| security assessments | required | 5/32 (16%) | 12/71 (17%) | 18/42 (43%) | 2025->2026: +26 [+21]; 2024->2026: +27 [+23] |
| infrastructure | preferred | 2/32 (6%) | 9/71 (13%) | 14/42 (33%) | 2025->2026: +21 [+18]; 2024->2026: +27 [+22] |
| programming languages | required | 10/32 (31%) | 31/71 (44%) | 7/42 (17%) | 2024->2025: +12 [+9]; 2025->2026: -27 [-23]; 2024->2026: -15 [-14] |
| protocols | required | 7/32 (22%) | 13/71 (18%) | 19/42 (45%) | 2025->2026: +27 [+22]; 2024->2026: +23 [+20] |
| general purpose languages | any | 6/32 (19%) | 15/71 (21%) | 19/42 (45%) | 2025->2026: +24 [+23]; 2024->2026: +26 [+25] |
| general purpose languages | required | 6/32 (19%) | 15/71 (21%) | 19/42 (45%) | 2025->2026: +24 [+23]; 2024->2026: +26 [+25] |
| threat | required | 6/32 (19%) | 16/71 (23%) | 19/42 (45%) | 2025->2026: +23 [+17]; 2024->2026: +26 [+23] |
| vulnerabilities | any | 6/32 (19%) | 24/71 (34%) | 19/42 (45%) | 2024->2025: +15 [+14]; 2025->2026: +11 [+11]; 2024->2026: +26 [+25] |
| security assessments | any | 8/32 (25%) | 17/71 (24%) | 21/42 (50%) | 2025->2026: +26 [+21]; 2024->2026: +25 [+22] |
| security | required | 17/32 (53%) | 45/71 (63%) | 33/42 (79%) | 2024->2025: +10 [+7]; 2025->2026: +15 [+15]; 2024->2026: +25 [+21] |
| c++ | any | 10/32 (31%) | 28/71 (39%) | 6/42 (14%) | 2025->2026: -25 [-24]; 2024->2026: -17 [-16] |
| computer | required | 6/32 (19%) | 11/71 (15%) | 17/42 (40%) | 2025->2026: +25 [+23]; 2024->2026: +22 [+20] |
| security protocols | required | 5/32 (16%) | 11/71 (15%) | 17/42 (40%) | 2025->2026: +25 [+23]; 2024->2026: +25 [+23] |
| threat modeling | required | 5/32 (16%) | 13/71 (18%) | 17/42 (40%) | 2025->2026: +22 [+17]; 2024->2026: +25 [+21] |
| computer | any | 6/32 (19%) | 16/71 (23%) | 18/42 (43%) | 2025->2026: +20 [+17]; 2024->2026: +24 [+23] |
| security protocols | any | 6/32 (19%) | 14/71 (20%) | 18/42 (43%) | 2025->2026: +23 [+21]; 2024->2026: +24 [+23] |
| risk | responsibilities | 3/32 (9%) | 15/71 (21%) | 14/42 (33%) | 2024->2025: +12 [+12]; 2025->2026: +12 [+10]; 2024->2026: +24 [+22] |
| java | any | 13/32 (41%) | 21/71 (30%) | 7/42 (17%) | 2024->2025: -11 [-14]; 2025->2026: -13 [-9]; 2024->2026: -24 [-24] |
| threat | any | 14/32 (44%) | 27/71 (38%) | 26/42 (62%) | 2025->2026: +24 [+16]; 2024->2026: +18 [+16] |
| ai | preferred | 0/32 (0%) | 4/71 (6%) | 10/42 (24%) | 2025->2026: +18 [+20]; 2024->2026: +24 [+26] |
| platforms | preferred | 0/32 (0%) | 10/71 (14%) | 10/42 (24%) | 2024->2025: +14 [+15]; 2024->2026: +24 [+21] |
| software development | any | 13/32 (41%) | 37/71 (52%) | 12/42 (29%) | 2024->2025: +11 [+7]; 2025->2026: -24 [-18]; 2024->2026: -12 [-10] |

**Regex metrics, security_engineering** (documented regexes; * = meets both thresholds in at least one pair)

| metric | 2024 (n=32) | 2025 (n=71) | 2026 (n=42) | flagged pairs (pp) |
|---|---|---|---|---|---|
| 'bachelor' in required | 30/32 (94%) | 71/71 (100%) | 40/42 (95%) | - |
| master/masters/PhD/doctorate/doctoral wording in preferred * | 12/32 (38%) | 34/71 (48%) | 11/42 (26%) | 2024->2025: +10; 2025->2026: -22; 2024->2026: -11 |
| same wording in required | 0/32 (0%) | 1/71 (1%) | 2/42 (5%) | - |
| the phrase 'advanced degree' in preferred (often 'or N years of experience with an advanced degree') | 0/32 (0%) | 0/71 (0%) | 0/42 (0%) | - |
| 'certification' in preferred | 1/32 (3%) | 6/71 (8%) | 0/42 (0%) | - |
| 'certification' in required | 1/32 (3%) | 1/71 (1%) | 0/42 (0%) | - |
| 'clearance' in required | 1/32 (3%) | 5/71 (7%) | 1/42 (2%) | - |
| 'travel' in required | 1/32 (3%) | 4/71 (6%) | 1/42 (2%) | - |
| 'python' in required * | 11/32 (34%) | 23/71 (32%) | 3/42 (7%) | 2025->2026: -25; 2024->2026: -27 |
| 'c++' in required * | 11/32 (34%) | 25/71 (35%) | 6/42 (14%) | 2025->2026: -21; 2024->2026: -20 |
| 'java' (word) in required * | 10/32 (31%) | 17/71 (24%) | 5/42 (12%) | 2025->2026: -12; 2024->2026: -19 |
| 'software development' in required * | 12/32 (38%) | 35/71 (49%) | 8/42 (19%) | 2024->2025: +12; 2025->2026: -30; 2024->2026: -18 |
| 'programming language' in required * | 10/32 (31%) | 31/71 (44%) | 7/42 (17%) | 2024->2025: +12; 2025->2026: -27; 2024->2026: -15 |
| 'network forensics' in required | 1/32 (3%) | 0/71 (0%) | 0/42 (0%) | - |
| 'incident response' in required | 2/32 (6%) | 1/71 (1%) | 2/42 (5%) | - |
| 'incident response' in preferred | 2/32 (6%) | 4/71 (6%) | 3/42 (7%) | - |
| 'malware' in required | 3/32 (9%) | 1/71 (1%) | 0/42 (0%) | - |
| 'cloud' (word) in required | 5/32 (16%) | 4/71 (6%) | 4/42 (10%) | - |
| 'cybersecurity'/'cyber security' in required | 1/32 (3%) | 4/71 (6%) | 5/42 (12%) | - |
| 'threat intelligence' in preferred | 0/32 (0%) | 1/71 (1%) | 0/42 (0%) | - |
| software-engineer template: required has 'software development' AND ('programming language' OR 'data structures') * | 10/32 (31%) | 29/71 (41%) | 7/42 (17%) | 2025->2026: -24; 2024->2026: -15 |
| security-engineer template: required has 'security assessments' AND 'security protocols' * | 5/32 (16%) | 9/71 (13%) | 16/42 (38%) | 2025->2026: +25; 2024->2026: +22 |
| 'machine learning' or 'artificial intelligence' or 'AI' (word) in any section * | 2/32 (6%) | 12/71 (17%) | 18/42 (43%) | 2024->2025: +11; 2025->2026: +26; 2024->2026: +37 |

**Stayed the same, security_engineering** (term in >=20% of postings in at least one year, any section, and highest minus lowest share across the three years < 5 pp; top 25)

| term | 2024 | 2025 | 2026 |
|---|---|---|---|
| developing | 14/32 (44%) | 28/71 (39%) | 17/42 (40%) |
| engineers | 9/32 (28%) | 22/71 (31%) | 11/42 (26%) |
| improve | 6/32 (19%) | 16/71 (23%) | 8/42 (19%) |
| large scale | 7/32 (22%) | 12/71 (17%) | 8/42 (19%) |

## Reading of the tables (hand-written after reading the postings behind the flagged terms; no causal claims)

Every figure below is copied from the tables above (shares with denominators; the bracket in a table row is the same change measured on distinct-text postings). "Candidate" = passes >=10 pp and >=8 postings; nothing is a proven change, and no cause is claimed. Groups compared: ALL (n = 100, 194, 89) and security_engineering (n = 32, 71, 42) only. threat_intel_and_response (n = 25, 67, 17), sales_and_consulting (n = 15, 30, 14), other_security and physical_corporate_security are below 30 in 2024 and/or 2026 and are NOT compared; 2023 (n = 26) is weak and not compared; 2019-2022 postings are title-based only. The archive's theme mix changes by year (security_engineering is 32% of the 2024 postings, 37% of 2025, 47% of 2026), so ALL-level differences partly reflect which postings were archived; the security_engineering comparison is the like-for-like one.

**1. AI wording rises, most clearly in security_engineering (candidate, survives the distinct-text check).** 'machine learning' / 'artificial intelligence' / 'AI' / 'LLM' anywhere in the text: ALL 6/100 (6%), 26/194 (13%), 26/89 (29%); security_engineering 2/32 (6%), 12/71 (17%), 18/42 (43%) [regex]. The word 'agentic' (any section, phrase-term): ALL 0/100, 2/194, 13/89. In the 2026 postings it appears as a skill asked for and as a thing to secure: "Experience designing and building LLM-based agentic workflows, frameworks, or automation tools specifically targeted at vulnerability research and remediation" (109866904700494534, security_engineering); "Build high-fidelity prototypes simulating agentic AI to test privacy and security concepts in real-world scenarios" (143876826572169926, security_engineering).

**2. In security_engineering, the requirement wording swings with which requirement template a posting uses (candidate; the pattern is consistent with a template-mix change, which I did not test against other explanations).** Software-engineer template (required has 'software development' and 'programming language' or 'data structures'): security_engineering 10/32 (31%), 29/71 (41%), 7/42 (17%); security-engineer template (required has 'security assessments' and 'security protocols'): 5/32 (16%), 9/71 (13%), 16/42 (38%) [regex; ALL: software-engineer template 10/100, 36/194, 9/89, security-engineer template 8/100, 13/194, 20/89]. Terms that move with the templates in security_engineering: programming languages / software development / python / c++ / java in REQUIRED rise 2024 -> 2025 and fall 2025 -> 2026 (e.g. python required 11/32, 23/71, 3/42; software development required 12/32, 35/71, 8/42 [regex]); 'security engineering', 'network security', protocols, security assessments, 'general purpose languages' and threat modeling in required rise 2025 -> 2026 (e.g. 'security engineering' required 14/71 -> 20/42, 'network security' required 10/71 -> 19/42). Template examples: "5 years of experience with software development in one or more programming languages, and with data structures/algorithms." (78793268778672838, security_engineering); "5 years of experience with security assessments or security design reviews or threat modeling." (95289251511313094, security_engineering).

**3. Master/PhD wording in preferred (security_engineering) follows the same pattern (candidate).** 12/32 (38%), 34/71 (48%), 11/42 (26%) [regex]. The software-engineer template's preferred list carries it: "Master's degree or PhD in Computer Science or related technical fields." (96435610394206918, security_engineering). Consistent with note 2, not tested separately. At the ALL level it is 25/100 (25%), 45/194 (23%), 18/89 (20%): no difference reaches 10 pp.

**4. 'security' in the responsibilities section rises (candidate, cause not isolated).** ALL 60/100 (60%), 118/194 (61%), 76/89 (85%); security_engineering 14/32 (44%), 39/71 (55%), 38/42 (90%) [phrase-term]. In 2026 the term 'security' is in more than 90% of all postings and is dropped by the boilerplate rule (in 2024 and 2025 it was not). I did not test whether this is wording or the mix of postings.

**5. Threat-intelligence reporting vocabulary falls at the ALL level (candidate, confounded by mix).** 'reports' any-section 30/100, 47/194, 11/89; 'audiences' 22/100, 41/194, 6/89; 'findings' 15/100, 40/194, 4/89 [phrase-term]. threat_intel_and_response is 25% of the 2024 postings, 35% of 2025 and 19% of 2026, and that theme cannot be compared by itself (n < 30 in 2024 and 2026), so composition and wording cannot be separated.

**6. Other ALL-level candidates:** 'certification' in preferred 28/100 (28%), 47/194 (24%), 14/89 (16%) (2024 -> 2026 -12 pp); 'clearance' in required 7/100, 27/194, 3/89 (2025 -> 2026 -11 pp); phrase 'programming languages' any-section 13/100, 53/194, 13/89.

**7. What stayed the same (all within 5 pp across the three years, ALL level):** 'response' 40/100, 75/194, 38/89; 'customer' 33/100, 67/194, 31/89; 'operations' 31/100, 59/194, 26/89; 'client' 28/100, 56/194, 25/89; 'detection' 27/100, 51/194, 24/89; 'leadership' 23/100, 50/194, 20/89; 'executive' 24/100, 46/194, 22/89; 'cybersecurity' in required 30/100, 62/194, 27/89 [regex]; 'incident response' in required 12/100, 23/194, 12/89 [regex]; 'bachelor' in required 91/100, 190/194, 84/89 (all within 10 pp); master/PhD in preferred at ALL level (note 3). In security_engineering the stable terms are few ('developing', 'engineers', 'improve', 'large scale').

**8. Duplicates and templates.** Distinct (required + responsibilities) texts: 98 of 100 (2024), 183 of 194 (2025), 84 of 89 (2026), so exact repeats are few and the bracketed distinct-text changes in the tables are close to the plain ones. The stronger template effect is note 2: near-identical requirement blocks reused across different roles.

**9. Theme mislabels.** Reading found questionable theme labels: 2024 (3 of 13 read: a customer-support engineer and an ICS/OT security engineer, and a detection-style analyst); 2025 (1 of 15); 2026 (2 of 12: an operational-technology operations role labelled sales_and_consulting and a UX engineer labelled security_engineering). Theme-level tables inherit these title-based labels; the samples are too small to give a mislabel rate.

**10. Multiple comparisons.** 2343 (ALL) and 677 (security_engineering) term-by-section combinations were tested, so a share of the listed differences can be chance; the consistent, template-explained and quote-supported items above (1-3) are the ones worth carrying forward, 4-6 are candidates only.

