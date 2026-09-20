# Checkpoint 3 tables (scratch). Denominators next to every share; `*` = n<30 (noisy). Postings count toward every year they were captured.

## A. DeepMind — one definition per number
- A = titles containing "DeepMind" (any rule): **34**. Used for sensitivity (b) in C2.
- B = A not in strict CORE by other words ("DeepMind-only"): **27**. This was the "27" in C2.
- A in strict CORE by other words: 7 (A − B).
- C = A not tagged by the OLD published rule: **29**. This was the "29" in C1.
- A tagged by the old rule: 5 (A − C).
- Window: all 34 first captured Mar–Sep 2026 (Mar 1, Apr 6, Jun 3, Jul 19, Aug 4, Sep 1); none earlier. Cause not verifiable (see CHECKPOINT 2).
Going forward: "DeepMind-titled" = A (34); "DeepMind-only" = B (27).

## B. Reconciliation old published rule -> strict CORE (postings per year; identity checked equal in every year)
| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| old published rule | 11 | 22 | 97 | 166 | 114 | 298 | 666 | 289 |
| − data-scientist (analytics) | 5 | 4 | 25 | 36 | 17 | 54 | 142 | 80 |
| − "Quantum AI" org name | 1 | 1 | 16 | 8 | 4 | 5 | 15 | 31 |
| − other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| + Aiml/GenAI/MLOps spelling | 0 | 1 | 1 | 3 | 4 | 28 | 138 | 52 |
| + TPU/Vertex/Gemma/NotebookLM | 0 | 0 | 0 | 2 | 1 | 6 | 19 | 6 |
| + agentic | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 3 |
| + other (natural language processing) | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 0 |
| **= new strict CORE** | 5 | 19 | 58 | 130 | 99 | 275 | 671 | 239 |
2025: 666 − 157 removed + 162 added = 671. The near-identical share (9.8% both) is offsetting changes of ~160 postings each way, NOT "the classifier did not change".

## C. Families (mutually exclusive; first match wins; each year sums to 100%)
Order: 1 ai_safety_responsible > 2 sales_consulting_gtm > 3 product_program_mgmt > 4 business_functions > 5 research > 6 infra_hardware > 7 ml_ai_engineering > 8 management_other > 9 other_functions
| share of CORE | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| n (CORE) | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| ai_safety_responsible | 0% | 0% | 3% | 5% | 1% | 1% | 3% | 3% |
| sales_consulting_gtm | 20% | 21% | 22% | 7% | 18% | 12% | 16% | 15% |
| product_program_mgmt | 0% | 0% | 9% | 8% | 7% | 7% | 8% | 8% |
| business_functions | 0% | 0% | 9% | 3% | 7% | 4% | 10% | 7% |
| research | 0% | 26% | 12% | 7% | 4% | 15% | 3% | 6% |
| infra_hardware | 0% | 0% | 0% | 9% | 21% | 8% | 10% | 15% |
| ml_ai_engineering | 80% | 47% | 43% | 55% | 39% | 49% | 47% | 44% |
| management_other | 0% | 0% | 2% | 4% | 2% | 4% | 2% | 2% |
| other_functions | 0% | 5% | 0% | 2% | 0% | 0% | 0% | 1% |
Changes vs C2: "business_functions" split out of management_other (also "ai principles" added to family 1; "performance" no longer sends ML engineers to infra).

## D. AI-as-domain (one rule, all years; rule v2 = regex bug fixed)
| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| n CORE | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| rule v2 domain-only k | 0 | 0 | 2 | 5 | 3 | 15 | 66 | 17 |
| rule v2 share | 0.0% | 0.0% | 3.4% | 3.8% | 3.0% | 5.5% | 9.8% | 7.1% |
| hand-corrected share (est.) | 0.0% | 0.0% | 3.0% | 2.1% | 1.9% | 5.2% | 8.4% | 5.7% |
| corrected range (non-borderline error 0-30%) | - | - | 2-3% | 2-2% | 2-2% | 5-5% | 7-9% | 5-6% |
Pooled 2021-24 corrected 3.7% (n=562) vs 2025 8.4% (~56/671; Wilson 6.5-10.7%) — non-overlapping. 2026 5.7% overlaps both.
Baseline (domain-function words among ALL observed postings): 2019 16% | 2020 15% | 2021 19% | 2022 17% | 2023 12% | 2024 12% | 2025 14% | 2026 11% — did NOT rise in 2025, so the 2025 rise is not simply broader archive coverage of non-technical roles (by this measure).
Composition of rule-v2 domain-only titles: 2025 (n=66): marketing/brand 12, UX/design 12, ops/support/escalations 10 (0 in 2021-24), generic front-end/full-stack/mobile/web engineering 9, policy/gov affairs 8, finance/people/recruiting 5, comms/writing 5, legal/counsel 3, strategy 2. 2021-24 (n=23): front-end etc 6, comms/writing 5, UX/design 4, marketing/brand 4, policy 3, finance 1. 2026 (n=17): UX/design 7, marketing 4, finance/people 2, comms 2, ops 1, policy 1.
Hand-check (single judge = rule's author, unblinded): 118 titles. All 40 borderline: 30 correctly domain, 10 wrongly domain (should be work). 18 other domain calls: 15 right, 3 wrong (1 = regex bug "Tele-communications", fixed). 60 "work" calls: 0 clear domain misses, 2 ambiguous (AI only a team label). Missed-domain upper bound among work calls 6% (clear) - 11% (incl. ambiguous), 95%.

## E. Vocabulary — share of that year's CORE postings whose title contains the term (n CORE as above)
| term | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | first year archived |
|---|---|---|---|---|---|---|---|---|---|
| machine learning | 100% | 53% | 60% | 66% | 58% | 36% | 17% | 5% | 2019 |
| AI (acronym) | 0% | 26% | 28% | 23% | 34% | 38% | 50% | 55% | 2020 |
| Aiml spelling | 0% | 5% | 2% | 2% | 4% | 9% | 20% | 20% | 2020 |
| generative / GenAI | 0% | 0% | 0% | 0% | 4% | 12% | 16% | 13% | 2023 |
| Gemini | 0% | 0% | 0% | 0% | 0% | 7% | 5% | 3% | 2024 |
| agent / agentic | 0% | 0% | 0% | 1% | 0% | 0% | 3% | 5% | 2022 |
| Vertex | 0% | 0% | 0% | 0% | 0% | 0% | 1% | 2% | 2025 |
| LLM / language model | 0% | 0% | 0% | 0% | 0% | 0% | 1% | 0% | 2025 |
| TPU / tensor | 0% | 0% | 0% | 3% | 4% | 3% | 3% | 3% | 2022 |
| responsible AI / AI safety | 0% | 0% | 2% | 4% | 0% | 1% | 2% | 1% | 2021 |
"First year archived" is not "first year at Google": archive coverage varies.
Naming vs size (CORE titles only):
| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| ML-family (machine learning / ML / Aiml / MLOps), % of CORE | 100% | 58% | 62% | 71% | 69% | 49% | 41% | 33% |
| AI/GenAI/Gemini WITHOUT an ML-family word, % of CORE | 0% | 37% | 36% | 22% | 29% | 43% | 55% | 63% |
| ML-family, % of ALL observed postings | 1.9% | 1.9% | 1.5% | 2.2% | 2.9% | 5.5% | 4.0% | 4.1% |
| AI/GenAI-only, % of ALL observed postings | 0.0% | 1.2% | 0.9% | 0.7% | 1.2% | 4.8% | 5.4% | 7.8% |
=> "machine learning" falls as a share of AI titles, but ML-family titles hold ~4-5.5% of all postings since 2024; the growth since 2024 is mostly AI/GenAI-labelled titles.
Data-driven token comparison (CORE titles first captured <=2023, n=277, vs >=2024, n=1,108; location/language/level tokens dropped; >=12 uses): RISING aiml 18% vs 3%, generative 9% vs 1%, genai 6% vs 0%, data 6% vs 2%, gemini 6% vs 0%, applied 5% vs 2%, analyst 3% vs 1%, safety 3% vs 1%, agent 2% vs 0%, security 2% vs 0%, trust 2% vs 1%, architect 3% vs 1%. FALLING machine/learning 63% vs 17-18%, industry 6% vs 0%, solutions 10% vs 4%, conversational 4% vs 1%, research 18% vs 10%, platform 5% vs 2%, professional 3% vs 1%, artificial 4% vs 1%, health 4% vs 2%.

## F. AI x cybersecurity crossover (strict CORE AND classify_title "cybersecurity")
| | 2019-2024 | 2025 | 2026 |
|---|---|---|---|
| crossover postings k | 0 each year | 18 | 5* |
| % of that year's CORE | 0% | 2.7% (n=671) | 2.1% (n=239) |
| security-tagged postings (n) | 8/16/74/202/142/142 | 322 | 118 |
| % of security-tagged | 0% | 5.6% | 4.2% |
Hand-check of all 23 titles: 22 genuine (AI agent security, AI vulnerability research, AI systems security, AI threat intelligence, agentic red team, AI protection); 1 false ("Aiml Engineer, National Security, Public Sector"; "security" = national security). k<10 flagged (2026: 5).

## G. Data-science-only (analytics; NOT AI) — share of observed postings, 95% Wilson interval
2019 1.9% (5/269; 0.8-4.3%)* | 2020 0.7% (4/572; 0.3-1.8%)* | 2021 1.1% (25/2326; 0.7-1.6%) | 2022 0.8% (36/4276; 0.6-1.2%) | 2023 0.7% (17/2371; 0.4-1.1%) | 2024 2.2% (54/2469; 1.7-2.8%) | 2025 2.1% (142/6824; 1.8-2.4%) | 2026 4.2% (80/1925; 3.4-5.1%). 2026 does not overlap 2025.

## H. Precision statement (must accompany every precision figure)
Single sample, judged by the classifier's own author, unblinded. Raw 94/100 titles judged AI-as-work; year-weighted strict precision 86.3% +/-9.9 (lenient, counting domain-only titles as correct, ~100%; no outright false match in 100). The gap: sampling gave roughly equal titles per year, but the 2025 stratum is 45% of all CORE postings and held 5 of the 6 domain-only titles (5 of 17 sampled), so weighting by population lowers precision.
