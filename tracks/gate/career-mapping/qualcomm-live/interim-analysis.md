# Qualcomm India, security roles: interim analysis (collected 10-11 Oct 2026)

Source: `scraper-data/careers.qualcomm.com-live-security-roles.live.json` (state of `qualcomm_live_security_roles`, plugin commits `0f3c4b4`, `f61c6be` in web-scrap). Every number below was counted from that file.
**Status: INCOMPLETE.** The walk was halted twice by HTTP 429. A patient driver (`run_crawl_patient.py`) resumes it automatically; re-run this analysis when it finishes.

## What was collected
- 122 distinct roles, all India, all on-site (Bangalore 73, Hyderabad 39, Chennai 10, Noida 5 by listed location).
- Search terms done: cybersecurity (8 matches), threat (4), vulnerability (4), penetration (1), red team (3), fuzzing (3), cryptography (6), malware (0), reverse engineering (0). `security`: 12 of 58 pages (580 matches on the board). `exploit`: not started.
- Search is relevance-ranked over the whole posting text, so a match means the word is somewhere in the posting, not in the title.

## Headline
- **Only 10 of 122 roles have a security word in the title.** The other 112 are body-text hits (Linux kernel, firmware, camera, DSP, CPU design, and so on).
- Of the 10: hardware security 5, GRC/IT/compliance 3, software security engineering 1, offensive 1, threat/response 0.
- **Offensive/red-team (title level): 1 role.** "Engineer - AI Agentic Fuzzing & Linux Security" (Software Engineering, Hyderabad); matched security, threat, vulnerability, fuzzing.
- **Software security engineering: 1 role.** "Senior Lead Engineer - Android OS System Security" (Software Engineering, Hyderabad).
- The 5 hardware roles: 2 RTL design (Security), 2 Hardware Security Architect (Bangalore, Chennai), 1 pre/post-silicon validation (SoC security).
- The 3 GRC/IT roles: Manager Compliance; FOSS Compliance Engineer; Sr Manager SAP Basis & Security.

## Roles that need a description read (security content behind generic titles)
Narrow terms hit these roles although the title says nothing about security: they are the likeliest hidden software-security roles.
| Role id | Title | Narrow terms hit |
|---|---|---|
| 446715560343 | Engineer staff (Software Eng., Hyderabad) | penetration, vulnerability, threat, cryptography |
| 446720951362 | Engineer, Senior Staff (Software Eng., Hyderabad) | vulnerability, cryptography |
| 446720988930 | Lead Engineer-Senior-Python/C++, CI-CD/Devops... (Hyderabad) | vulnerability, fuzzing |
| 446715899384 | R&D Engineer, XR AI Software and Systems (Bangalore) | cryptography |
| 446718913864 | ADAS/AD Safety Software Infra Architect Staff (Bangalore) | cybersecurity |
| 446720156834 | Telematics Platform Senior Engineer (Bangalore) | cybersecurity |
| 446721024772 | Flex Solution Principal Engineer - Customer Program | cybersecurity |
| 446721164776 | Engineer, Senior_CE (Software Applications, Hyderabad) | cybersecurity |

"red team" matched 3 PMIC Systems Validation roles (hardware); likely an unrelated phrase, to be confirmed from the text.

## What this says (and does not say)
- Qualcomm's India security demand, by title, is mostly **hardware (silicon/SoC)** and a few compliance/IT roles; **dedicated red-team or pentest roles were not seen** in the pages collected.
- The only offensive-flavoured role is a **fuzzing / Linux security** engineering role, which is the closest fit to a computer-science red-team direction.
- This is India-only, one day, and 12 of 58 `security` pages. Deeper pages and global locations may add roles. No claim is made about hiring volume or trend.
- Title tags are a keyword heuristic (`classify_role`); descriptions are not yet downloaded, so skills/tools/certifications are not analysed.

## Next
1. Let the patient driver finish `security` pages 13-58 and `exploit` (about 8 requests per attempt, backing off after each 429).
2. Re-run this analysis on the complete data.
3. Download descriptions for the non-hardware tagged roles plus the 8 generic-title roles above; build the skills/tools checklist.
4. Optionally repeat with a global location filter for red-team roles.
