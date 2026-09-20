# Google security job descriptions, 2024 description-capture year (findings/2024.md)

**Scope and limits, read first.** Postings are only those Wayback archived; this is not a census of Google's roles. 2019-2022 postings are title-based only (no recoverable descriptions); descriptions cover postings archived from mid-2023 (capture years 2023-2026). This file covers the **2024** capture year: **100** postings (security_engineering 32, threat_intel_and_response 25 W, other_security 20 W, sales_and_consulting 15 W, physical_corporate_security 8 W). W = n<30 (weak). **Only security_engineering (n=32) and the all-postings level are above the weak threshold; every other theme figure below is anecdotal.** physical_corporate_security is NOT cybersecurity. Text is the page at its capture date, not when the role opened. Every count is "postings containing it / postings in the group" and is tagged **[regex]** (documented regex on the raw section text, identical for every year) or **[phrase-term]** (data-driven phrase extraction, see c5_method.md). Causes are inference.

## Headline
1. **Degree wording.** 'Bachelor' in the required section: [[re:bachelor_req]]. Master/masters/PhD/doctorate/doctoral wording in the preferred section: [[re:adv_pref]] overall, [[re:adv_pref|security_engineering]] in security_engineering.
2. **Security engineering asks for programming, in about a third of postings.** Required text in security_engineering: python [[re:python_req|security_engineering]], c++ [[re:cpp_req|security_engineering]], java [[re:java_req|security_engineering]], software development [[re:swdev_req|security_engineering]]. Two requirement templates recur there: the generic software-engineer template [[re:swe_tpl_req|security_engineering]] and the security-engineer template (security assessments / design reviews / threat modeling plus security protocols) [[re:sec_tpl_req|security_engineering]].
3. **Threat/response and sales cells are weak (n<30), anecdotal only.** threat_intel_and_response W: network forensics required [[re:netforensics_req|threat_intel_and_response]], incident response required [[re:ir_req|threat_intel_and_response]], certification preferred [[re:cert_pref|threat_intel_and_response]]. sales_and_consulting W: cybersecurity required [[re:cybersec_req|sales_and_consulting]], cloud required [[re:cloud_req|sales_and_consulting]].
4. **Certifications** in the preferred section overall [[re:cert_pref]], in the required section [[re:cert_req]].
5. **Experience levels.** Highest "N years" figure in required: 5-6 years [[yrs:5-6]], 7 or more [[yrs:7-99]], 1-2 [[yrs:1-2]].
6. **Gating requirements:** 'clearance' in required [[re:clearance_req]]; 'travel' in required [[re:travel_req]].
7. **AI wording is rare in 2024:** 'machine learning' / 'artificial intelligence' / 'AI' / 'LLM' anywhere in the text [[re:ai_ml_any]].

## What is asked / preferred / done, security_engineering (n=32, phrase-terms)
Required: software [[software|minimum_qualifications|security_engineering]], software development [[software development|minimum_qualifications|security_engineering]], python [[python|minimum_qualifications|security_engineering]], java [[java|minimum_qualifications|security_engineering]]. Preferred: protocols [[protocols|preferred_qualifications|security_engineering]], cloud [[cloud|preferred_qualifications|security_engineering]]. Done: product [[product|responsibilities|security_engineering]], code [[code|responsibilities|security_engineering]], write [[write|responsibilities|security_engineering]]. Other themes: see the weak-theme table in c5_terms_2024.md (counts only, n<30).

## Reading notes (evidence quotes, verbatim, <=25 words, machine-checked)
- Seniority is expressed by scaling one template: the security-engineer requirement reads "5 years" in a senior posting and "10 years" in a tech-lead one: "10 years of experience with security assessments or security design reviews or threat modeling." (97575005541278406, security_engineering).
- Some security-labelled roles are support or program roles: "Work as part of a team of engineers/consultants that globally ensure 24 hour customer support." (133807659284341446, security_engineering).
- Gating: "Active US Government Top Secret/Sensitive Compartmentalized Information (TS/SCI) security clearance with polygraph." (128513480771674822, threat_intel_and_response).

## Tables (generated; see c5_terms_2024.md for all tables)

{{REGEX}}

{{RECON}}

{{YEARS}}

{{DISTINCTIVE}}

{{TOP40}}
