# Google security job descriptions, 2019-2026: what the text says and how it moved

**Scope, read first.** Built only from the findings files (`findings/2023.md` to `findings/2026.md`), `c5_drift.md`, `c5_method.md` and the title-based 2019-2022 results in `career-mapping/google-wayback-analysis.md`. No new analysis, no network use. Postings are only those Wayback archived, not a census of Google's roles. **2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026).** Every description is the page text at its capture date. W = n<30 (weak).

## 1. Headline

- Descriptions exist for 409 security postings (2023: 26 W, 2024: 100, 2025: 194, 2026: 89). Nothing about job descriptions can be said for 2019-2022; only titles exist there.
- Between 2024 and 2026 the clearest change in wording is AI: AI/ML/LLM wording appears in 6/100 postings (2024), 26/194 (2025) and 26/89 (2026); "agentic" goes 0/100, 2/194, 13/89.
- In security_engineering (the one theme large enough in every year) the requirement lists swing with which requirement template a posting uses: a generic software-engineer template (python, C++, "software development") peaks in 2025; a security-engineer template (security assessments, protocols, network security) is the most common in 2026. This is a pattern consistent with a template mix change; it was not tested against other explanations.
- A Bachelor's degree is in the required text of nearly all postings in every year; an advanced degree is a preference, not a requirement; core response, customer, operations and detection vocabulary is stable.
- Titles (2019-2026) show security roles moving into Google Cloud, a growing go-to-market share and Mandiant appearing in 2023. Titles are not skills, so these cannot be linked to the description findings beyond loose context.
- Small cells are weak, 2023 is only described, and no cause is claimed anywhere.

## 2. Scope and coverage

| Description-capture year | Postings with descriptions | security_engineering | threat_intel_and_response | sales_and_consulting | other_security | physical_corporate_security |
|---|---|---|---|---|---|---|
| 2023 (Jul-Dec) | 26 W | 10 W | 9 W | 3 W | 4 W | 0 |
| 2024 | 100 | 32 | 25 W | 15 W | 20 W | 8 W |
| 2025 | 194 | 71 | 67 | 30 | 15 W | 11 W |
| 2026 (to Sep) | 89 | 42 | 17 W | 14 W | 13 W | 3 W |

- The four counts sum to 409 postings, out of the 883 security-tagged postings in the title-based analysis.
- Only security_engineering and the all-postings level reach n>=30 in each of 2024, 2025 and 2026. threat_intel_and_response has n>=30 in 2025 only (67); sales_and_consulting (30) is at the threshold in 2025 only.
- physical_corporate_security is not cybersecurity and is kept separate.
- Themes are assigned from title keywords. Each year is the set of postings archived with a new-format page in that year, so years are not random samples and their theme mix differs: security_engineering is 32% of the 2024 postings, 37% of 2025 and 47% of 2026.
- Numbers are tagged in the source files as **[regex]** (documented regex on the raw section text, identical every year) or **[phrase-term]** (data-driven phrase extraction). Unless stated, counts below are regex or phrase-term counts as in those files.

## 3. What changed, 2024 to 2026

Rule (from `c5_drift.md`): a group is compared only if n>=30 in every year (ALL and security_engineering); a difference is listed only if it is at least 10 percentage points and at least 8 postings. 2023 is not compared. Items 1-3 are consistent, quote-supported and survive a distinct-text check; items 4-6 are candidates only.

**1. AI wording rises (candidate that survives the distinct-text check).** AI/ML/LLM wording anywhere: ALL 6/100 (6%), 26/194 (13%), 26/89 (29%); security_engineering 2/32 (6%), 12/71 (17%), 18/42 (43%). "Agentic" (any section): 0/100, 2/194, 13/89. It appears as a skill asked for and as a thing to secure:
- "Experience designing and building LLM-based agentic workflows, frameworks, or automation tools specifically targeted at vulnerability research and remediation" (109866904700494534, security_engineering).
- "Build high-fidelity prototypes simulating agentic AI to test privacy and security concepts in real-world scenarios" (143876826572169926, security_engineering); this one is a UX role carrying the security_engineering label.

This is a wording shift inside the archive only, not a claim about Google's hiring volume.

**2. Requirement-template mix in security_engineering (candidate; consistent with a template-mix change, not tested against other explanations).**

| security_engineering [regex] | 2024 (n=32) | 2025 (n=71) | 2026 (n=42) |
|---|---|---|---|
| software-engineer template | 10/32 (31%) | 29/71 (41%) | 7/42 (17%) |
| security-engineer template | 5/32 (16%) | 9/71 (13%) | 16/42 (38%) |
| python in required | 11/32 (34%) | 23/71 (32%) | 3/42 (7%) |
| c++ in required | 11/32 (34%) | 25/71 (35%) | 6/42 (14%) |
| software development in required | 12/32 (38%) | 35/71 (49%) | 8/42 (19%) |

Terms of the security-engineer template rise in 2026 (phrase-term): security engineering in required 5/32, 14/71, 20/42; network security in required 6/32, 10/71, 19/42. The two templates read: "5 years of experience with software development in one or more programming languages, and with data structures/algorithms." (78793268778672838, security_engineering) versus "5 years of experience with security assessments or security design reviews or threat modeling." (95289251511313094, security_engineering). Because the wording follows the template, python/C++ counts measure the template as much as a security skill. The template rows are my operational regex definitions, not Google's.

**3. Master/PhD wording in preferred (security_engineering) follows the same pattern.** 12/32 (38%), 34/71 (48%), 11/42 (26%) [regex]. At the ALL level it is 25/100 (25%), 45/194 (23%), 18/89 (20%), with no difference of 10 points.

**4. "security" in responsibilities rises (candidate, cause not isolated).** ALL 60/100 (60%), 118/194 (61%), 76/89 (85%); security_engineering 14/32 (44%), 39/71 (55%), 38/42 (90%) [phrase-term]. In 2026 the word is in over 90% of postings and is dropped by the boilerplate rule. Wording versus posting mix was not separated.

**5. Reporting vocabulary falls at the ALL level (candidate, confounded by theme mix).** "reports" 30/100, 47/194, 11/89; "audiences" 22/100, 41/194, 6/89; "findings" 15/100, 40/194, 4/89 [phrase-term]. threat_intel_and_response is 25% of the 2024 postings, 35% of 2025 and 19% of 2026 and cannot be compared by itself, so composition and wording are not separable.

**6. Other ALL-level candidates.** Certification in preferred 28/100 (28%), 47/194 (24%), 14/89 (16%); clearance in required 7/100, 27/194, 3/89 [regex].

## 4. What stayed the same

All within 5 points across 2024, 2025 and 2026 at the ALL level (`c5_drift.md`):
- Terms: "response" 40/100, 75/194, 38/89; "customer" 33/100, 67/194, 31/89; "operations" 31/100, 59/194, 26/89; "client" 28/100, 56/194, 25/89; "detection" 27/100, 51/194, 24/89; "leadership" 23/100, 50/194, 20/89; "executive" 24/100, 46/194, 22/89.
- Regex: cybersecurity in required 30/100, 62/194, 27/89; incident response in required 12/100, 23/194, 12/89.
- Bachelor in required 91/100, 190/194, 84/89 (within 10 points, not 5).
- In security_engineering the stable terms are few: "developing", "engineers", "improve", "large scale".
- Near-identical text is rare: distinct required-plus-responsibilities texts are 98 of 100 (2024), 183 of 194 (2025), 84 of 89 (2026).

## 5. By role family

**security_engineering (n=32, 71, 42; the only family comparable across years).** Asks for programming plus security design. 2024: software 16/32 required, python 11/32, java 10/32. 2025: software development 35/71, c++ 23/71 (phrase-term), python 23/71, design reviews 21/71 in responsibilities; advanced-degree wording in preferred 34/71 (48%). 2026: security engineering 20/42, network security 19/42, protocols 19/42 in required; AI 12/42 in responsibilities. Reading shows the family includes generic software roles, research-level roles (a distinguished-engineer posting cites publications at S&P, CCS, USENIX Security, NeurIPS, ICML) and roles that only carry the label. An internship states the degree being pursued. Cross-year changes are those in section 3.

**threat_intel_and_response (n=67 in 2025; 25 W, 17 W and 9 W elsewhere; no cross-year comparison).** 2025: network forensics 18/67 (27%), incident response 17/67 (25%), malware 15/67 (22%) in required; certification in preferred 23/67 (34%); reports in responsibilities 24/67 (36%); travel in required 15/67 (22%); master/PhD wording in preferred 5/67 (7%), against 34/71 in security_engineering. It is written by activity: "Conduct host forensics, network forensics, log analysis, and malware triage in support of incident response investigations." (78684822089671366, threat_intel_and_response). The same sentence appears in a 2023 posting and in 2026 postings, so this text is reused, not new. Some requirements gate who can apply: "United Kingdom Security Vetting Developed Vetting (DV) clearance." (86120617354371782, threat_intel_and_response). Title keywords sometimes put engineering roles here (an incident-response-titled internal-tool posting). Weak years, counts only: 2024 network forensics 6/25 W, incident response 5/25 W; 2026 incident response 5/17 W.

**sales_and_consulting (n=30 in 2025, the smallest non-weak cell; 15 W in 2024, 14 W in 2026, 3 W in 2023).** 2025: cybersecurity in required 20/30 (67%), cloud 14/30 (47%), 7 or more years of experience 13/30 (43%), the most senior group; certification in preferred 12/30 (40%). The text describes delivery and selling, not depth of security engineering: "Provide consultation and support for deployment and operations of Google SecOps in client environments." (130800037121663686, sales_and_consulting). A quota-carrying leadership posting reads as a sales role. No cross-year share is claimed.

**other_security (15 W in 2025) and physical_corporate_security (11 W in 2025).** Governance, SAP compliance, review-and-approve and program-management roles, and facility/guard-force security. "Experience working with vendors, suppliers and managing a contracted guard team." (98215481499886278, physical_corporate_security). Counts only; physical security is not cybersecurity.

**2023 (n=26 W, described only, no shares).** Requirement blocks were less standardised: "Experience in Code Reviews" (80182026012893894, security_engineering) appears as a bare skill line with no years or degree. 13/26 postings mention Bachelor in required, so degree counts are not comparable with later years. AI wording: 0/26.

## 6. 2019-2022 context (title-based only; source `google-wayback-analysis.md`)

For 2019-2022 there are no descriptions. From titles alone, on 883 security-tagged postings in 18,188 distinct postings:
- Security share of observed postings: 3.0% (2019, 8 of 269), 2.8% (2020), 3.2% (2021), 4.7% (2022), then 6.0% (2023), 5.8% (2024), 4.7% (2025), 6.1% (2026). 2019 and 2020 (8 and 16 postings) are noisy.
- Cloud-titled security roles: 0-18% in 2019-2021, 30% in 2022, 44% in 2023. Sales/consulting titles: 0-12% in 2019-2021, 22-27% from 2023. Mandiant: 0% until 2022, 8% in 2023, 24% in 2024.
- Threat/detection/response titles are present every year (16-38%); management titles 20-36% since 2020; offensive/vulnerability titles small (2-7% since 2021).
- AI in titles: 0% through 2024, 6% in 2025, 4% in 2026 (broad title rule). The source itself calls the causes (acquisition, rebrand) inference.

How this lines up: titles show AI words entering security titles in 2025, while description text shows AI/ML wording already in 6/100 postings in 2024 and 29% of 2026 postings, so wording in descriptions moves without a title change. The role families in the title analysis (Cloud, Mandiant, sales) and the description themes (security_engineering, threat_intel_and_response, sales_and_consulting) are defined differently and their shares must not be compared. What cannot be linked: what a 2019-2022 "Security Engineer" was asked to know, whether the python/C++ template existed before 2024, or whether requirements shifted at any point before mid-2023.

## 7. What we can and cannot say

**Can say (within the archive):**
- AI/ML and "agentic" wording is more common in 2026 descriptions than in 2024, at the ALL level and in security_engineering.
- Requirement wording in security_engineering follows the requirement template used, and the template mix differs across years.
- A Bachelor's is near-universal in required text; advanced degrees and certifications are mostly preferred; response, customer, operations and detection vocabulary is stable.
- Roles differ by family: forensics and malware in threat/response, cybersecurity and cloud in sales and consulting, programming in security_engineering.

**Cannot say:**
- Anything about skills in 2019-2022, or any 2019-2023 trend in descriptions.
- Anything about Google's hiring volume or what any requirement is for.
- Why any wording changed; template mix is an untested explanation, not a cause.
- Any cross-year change for threat_intel_and_response or sales_and_consulting, or any share for 2023.

## 8. Limits

- Wayback-only: postings are those archived, first mid-2023 onward for descriptions. Years are not random samples.
- Themes come from titles and some are wrong: 3 of 13 read in 2024, 1 of 15 in 2025, 2 of 12 in 2026 (for example an operational-technology operations role labelled sales_and_consulting). Samples are too small for a mislabel rate.
- Template and duplicate postings (see section 4) mean counts partly measure the template.
- Phrase matching and regexes are heuristics: a term absent from a posting may be asked for in other words; phrase extraction misses "c/c++" written without spaces (c++ 25/71 regex vs 23/71 phrase in 2025).
- Multiple comparisons: 2343 (ALL) and 677 (security_engineering) term-by-section combinations were tested, so some listed differences can be chance.
- Snapshot at capture date, not at first appearance. No causes are asserted.

**Optional context, separate dataset.** `google-live/details-checklist.md` describes a one-day snapshot of 169 live security roles with different regexes. Directionally, AI/ML wording is common in the live roles too; the shares are not compared with the archive figures here.

## 9. Claims table

| # | Claim | Numbers | Source file and section |
|---|---|---|---|
| 1 | Descriptions exist only for 2023-2026 captures | 26 W, 100, 194, 89; 883 postings | findings/2023-2026.md (scope); google-wayback-analysis.md |
| 2 | AI/ML/LLM wording rose 2024 to 2026 | ALL 6/100, 26/194, 26/89; security_engineering 2/32, 12/71, 18/42 | c5_drift.md, Reading of the tables item 1 |
| 3 | "Agentic" is new in 2026 | 0/100, 2/194, 13/89 | c5_drift.md item 1; findings/2026.md headline 2 |
| 4 | Template mix in security_engineering swings (candidate) | software template 10/32, 29/71, 7/42; security template 5/32, 9/71, 16/42 | c5_drift.md item 2 |
| 5 | Python and C++ in required follow the template | python 11/32, 23/71, 3/42; c++ 11/32, 25/71, 6/42 | c5_drift.md, security_engineering regex table |
| 6 | Network security and security engineering required rise 2025 to 2026 | 6/32, 10/71, 19/42; 5/32, 14/71, 20/42 | c5_drift.md, security_engineering table; item 2 |
| 7 | Master/PhD preferred in security_engineering (candidate) | 12/32, 34/71, 11/42; ALL 25/100, 45/194, 18/89 | c5_drift.md item 3 |
| 8 | "security" in responsibilities rises (candidate) | ALL 60/100, 118/194, 76/89; SE 14/32, 39/71, 38/42 | c5_drift.md item 4 |
| 9 | Reporting vocabulary falls, theme-mix confounded (candidate) | reports 30/100, 47/194, 11/89 | c5_drift.md item 5 |
| 10 | Stable vocabulary and requirements | response 40/100, 75/194, 38/89; bachelor 91/100, 190/194, 84/89 | c5_drift.md item 7 |
| 11 | Threat/response asks for forensics and malware (2025) | 18/67, 17/67, 15/67 | findings/2025.md headline 1 |
| 12 | Sales/consulting asks for cybersecurity and cloud (2025) | 20/30, 14/30, 13/30 | findings/2025.md headline 1 and 4 |
| 13 | Theme labels are partly wrong | 3 of 13, 1 of 15, 2 of 12 | c5_drift.md item 9; c5_method.md limits |
| 14 | Title-based security share and family shifts, 2019-2026 | 3.0% to 6.1%; cloud 44% (2023); sales 22-27%; Mandiant 8% to 24% | google-wayback-analysis.md, tables and What changed 1-3 |
| 15 | Multiple-comparison caution | 2343 and 677 tests | c5_drift.md item 10 |
| 16 | 2023 is described only | 26 W; AI wording 0/26 | findings/2023.md |
