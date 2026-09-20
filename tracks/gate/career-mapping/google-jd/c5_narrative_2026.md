# Google security job descriptions, 2026 description-capture year (findings/2026.md)

**Scope and limits, read first.** Postings are only those Wayback archived; this is not a census of Google's roles. 2019-2022 postings are title-based only (no recoverable descriptions); descriptions cover postings archived from mid-2023 (capture years 2023-2026). This file covers the **2026** capture year (captures to Aug 2026): **89** postings (security_engineering 42, threat_intel_and_response 17 W, sales_and_consulting 14 W, other_security 13 W, physical_corporate_security 3 W). W = n<30 (weak). **Only security_engineering (n=42) and the all-postings level are above the weak threshold; every other theme figure is anecdotal.** physical_corporate_security (n=3) is NOT cybersecurity and is not summarised. Text is the page at its capture date. Every count is "postings containing it / postings in the group" and is tagged **[regex]** (documented regex, identical for every year) or **[phrase-term]** (data-driven phrase extraction, see c5_method.md). Causes are inference. The boilerplate rule dropped the term 'security' in 2026 (it is in more than 90% of the 89 postings; see the last table of c5_terms_2026.md).

## Headline
1. **Degree wording.** 'Bachelor' in required: [[re:bachelor_req]]. Master/masters/PhD/doctorate/doctoral wording in preferred: [[re:adv_pref]] overall, [[re:adv_pref|security_engineering]] in security_engineering.
2. **AI wording is much more common than in 2024/2025.** 'machine learning' / 'artificial intelligence' / 'AI' / 'LLM' anywhere in the text: [[re:ai_ml_any]] overall and [[re:ai_ml_any|security_engineering]] in security_engineering. The word 'agentic' (any section) appears in [[agentic|any]] postings. It appears both as a skill asked for (building agentic workflows for security) and as something to secure. Wording shift within the posting archive only; no claim about Google's hiring volume.
3. **The security_engineering requirements in 2026 lean to the security-engineer template, not the generic software-engineer template.** Security-engineer template (security assessments + security protocols in required): [[re:sec_tpl_req|security_engineering]]; software-engineer template: [[re:swe_tpl_req|security_engineering]]. Correspondingly, python is required in [[re:python_req|security_engineering]] and c++ in [[re:cpp_req|security_engineering]] of security_engineering postings, and 'general purpose languages' (the template wording for coding) appears in the required text of [[general purpose languages|minimum_qualifications|security_engineering]] of them.
4. **Certifications** in preferred overall [[re:cert_pref]]; in required [[re:cert_req]].
5. **Experience levels.** Highest "N years" figure in required: 5-6 years [[yrs:5-6]], 7 or more [[yrs:7-99]], 1-2 [[yrs:1-2]].
6. **Gating requirements:** 'clearance' in required [[re:clearance_req]]; 'travel' in required [[re:travel_req]].
7. **Weak cells (n<30, anecdotal):** threat_intel_and_response W: incident response required [[re:ir_req|threat_intel_and_response]]; sales_and_consulting W: cybersecurity required [[re:cybersec_req|sales_and_consulting]].

## What is asked / preferred / done, security_engineering (n=42, phrase-terms)
Required: security engineering [[security engineering|minimum_qualifications|security_engineering]], network security [[network security|minimum_qualifications|security_engineering]], protocols [[protocols|minimum_qualifications|security_engineering]], assessments [[assessments|minimum_qualifications|security_engineering]]. Preferred: cloud [[cloud|preferred_qualifications|security_engineering]], infrastructure [[infrastructure|preferred_qualifications|security_engineering]], ai [[ai|preferred_qualifications|security_engineering]]. Done: secure [[secure|responsibilities|security_engineering]], research [[research|responsibilities|security_engineering]], vulnerability [[vulnerability|responsibilities|security_engineering]], ai [[ai|responsibilities|security_engineering]].

## Reading notes (evidence quotes, verbatim, <=25 words, machine-checked)
- AI as a skill: "Experience designing and building LLM-based agentic workflows, frameworks, or automation tools specifically targeted at vulnerability research and remediation" (109866904700494534, security_engineering); even a program-management posting asks "Experience using AI and seek opportunities to use AI/ML technologies to lead improvements across programs." (73986696906973894, other_security).
- The same incident-response responsibilities sentence appears in more than one 2026 posting (also in a 2023 one, see findings/2023.md): "Conduct host forensics, network forensics, log analysis, and malware triage in support of incident response investigations" (79030552585216710, threat_intel_and_response).
- Gating: "Ability to communicate in English and German fluently to support local stakeholders." (91252549188756166, physical_corporate_security); "Must possess an active Top Secret security clearance." (95624077397369542, threat_intel_and_response).

## Tables (generated; see c5_terms_2026.md for all tables)

{{REGEX}}

{{RECON}}

{{YEARS}}

{{DISTINCTIVE}}

{{TOP40}}
