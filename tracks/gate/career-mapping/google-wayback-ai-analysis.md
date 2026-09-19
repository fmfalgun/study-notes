# Google AI roles, 2019–2026: what changed and what stayed

Companion to `google-wayback-analysis.md` (the cybersecurity write-up) and built the same way: Wayback Machine's archive of Google's individual job-posting pages — **18,188 distinct postings** (URL = job ID + title slug; capture date = it was live then), of which **1,385 are AI/ML by the strict rule**.

> **Supersedes the earlier AI figures, for AI only.** The AI columns in `google-wayback-job-trends.json` and the AI sentences in `google-wayback-analysis.md` used a broader keyword rule (it counted data-scientist analytics titles and Google's "Quantum AI" org, and missed titles spelled "Aiml"). Those AI figures are superseded by this file. **The cybersecurity numbers are unaffected.** `google-wayback-job-trends.json` is deliberately left unchanged as the record of the earlier rule.

## Plain-language summary

1. **The 2024 jump is mostly a change in wording plus AI-labelled roles, not more roles called "machine learning".** Titles containing the phrase "machine learning" fell from 53%–66% of AI titles (2020–2023) to 5% in 2026, while the acronym "AI" rose from about a quarter to 55%. Counting every ML spelling together (machine learning / ML / Aiml), ML-family titles roughly doubled their share of *all* postings in 2024 (2.9% → 5.5%) and then held (4.0%, 4.1%), while titles that say AI/GenAI/Gemini *without* an ML word grew from 1.2% (2023) to 7.8% (2026). So most growth after 2023 is AI/GenAI-labelled titles. **What the data cannot say:** whether those are existing ML roles retitled or new roles — nothing here links an old posting to a new one.
2. **Level:** AI/ML titles were 1.9%–4.2% of observed postings in 2019–2023, 11.1% in 2024, 9.8% in 2025 and 12.4% in 2026 (to Sep). A step up in 2024, then roughly flat. (Yearly archived counts swing from 269 to 6,824, so only shares are compared.)
3. **Data-science analytics is a separate, growing thing:** 0.7%–1.1% of postings in 2020–2023, 2.2%, 2.1%, then 4.2% in 2026. It is Ads/product analytics, not AI, and is kept out of the headline.
4. **Supported lead (not a finding): AI as a team label on non-AI work.** The share of AI-titled postings whose function is unrelated to AI expertise (marketing, UX/design, ops/escalations, policy…) is about 8% in 2025 (rule 9.8%) against about 3.7% pooled 2021–2024. One judge, who also wrote the rule, checked it; see the section below for what would upgrade it.
5. **AI × security appears only from 2025:** none before 2025; 18 postings in 2025 (17 after removing a false positive) and 5 in 2026 (to Sep), about 5.3% and 4.2% of that year's security postings.

## What this data can and cannot tell you — read before the numbers

- **Not every Google job.** Only postings Wayback archived.
- **Counts are not comparable across years; shares are.** Archived postings per year swing from 269 (2019) to 6,824 (2025) with Wayback's crawl activity. Every share below shows its denominator. Shares cancel crawl intensity to a first approximation, not perfectly — the 2025 dip may be partly broader archive coverage (observed postings ×2.8 vs AI postings ×2.4); that is inference and cannot be checked here.
- **Small years are noisy.** 2019 (5) and 2020 (19) have fewer than 30 AI postings (marked `*`); 2026 is partial (to Sep).
- **Titles, not skills.** Titles come from URL slugs; they show role types, not required skills.
- **Keyword classification, one judge.** Every precision/recall figure below comes from a single sample judged by the classifier's own author, unblinded.
- **Every cause given below (product launches, renames, reorganisations) is inference**, not something the data proves.

Files this is based on: `google-wayback-ai-roles-by-year.md` (every AI posting by year and family), `google-wayback-ai-trends.json` (all tables + per-posting flags + the hand-check), `scraper-data/google-careers-job-urls.cdx.json` (raw URL list), code `plugins/job_search/wayback_google_ai.py` (op `google_wayback_ai_trends`, rules version `google-ai-rules/v2 (2026-09-19)`).

## Headline: AI/ML share of observed postings (strict CORE)

|  | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| observed postings (denominator) | 269 | 572 | 2,326 | 4,276 | 2,371 | 2,469 | 6,824 | 1,925 |
| strict CORE postings (n) | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| **strict CORE share** | 1.9% | 3.3% | 2.5% | 3.0% | 4.2% | 11.1% | 9.8% | 12.4% |

`*` = n<30, noisy.

### Sensitivity: how much do the definitions matter?

| share of observed postings | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| (a) strict CORE — headline | 1.9% | 3.3% | 2.5% | 3.0% | 4.2% | 11.1% | 9.8% | 12.4% |
| (b) strict CORE + DeepMind-titled | 1.9% | 3.3% | 2.5% | 3.0% | 4.2% | 11.1% | 9.8% | 13.8% |
| (c) strict CORE + AI-adjacent | 4.8% | 4.7% | 4.0% | 4.4% | 4.9% | 13.8% | 10.7% | 14.3% |
| data-science-only (separate layer) | 1.9% | 0.7% | 1.1% | 0.8% | 0.7% | 2.2% | 2.1% | 4.2% |
| memo: earlier broader rule | 4.1% | 3.8% | 4.2% | 3.9% | 4.8% | 12.1% | 9.8% | 15.0% |

2026 with and without DeepMind: 12.4% (239/1925) vs 13.8% (266/1925). Counts behind the separate lines — AI-adjacent: 2019 8, 2020 8, 2021 35, 2022 60, 2023 17, 2024 65, 2025 56, 2026 37; data-science-only: 2019 5, 2020 4, 2021 25, 2022 36, 2023 17, 2024 54, 2025 142, 2026 80.

**DeepMind — one definition per number.** A = titles containing "DeepMind": **34**. B = A not AI by other words ("DeepMind-only"): **27**. The other 7 are already in the headline by other words. (The earlier broader rule tagged 5 of the 34; 29 it did not.) All 34 were first captured March–September 2026 (03/2026: 1, 04/2026: 6, 06/2026: 3, 07/2026: 19, 08/2026: 4, 09/2026: 1); none earlier. About half were archived through URLs carrying a `?company=DeepMind` listing filter. The earliest front-page snapshot that mentions DeepMind is 2026-07-02, and none of 25 old-layout snapshots (Jun 2021–Jun 2023) lists DeepMind in its organisation filter; for Jul 2023–Jun 2026 the filter list is not visible in the captures. **All 34 appear only in 2026; the cause is not verifiable from this data** (a change in what Wayback archived is one possibility). DeepMind is excluded from the headline and reported on its own.

## Reconciliation: earlier broader rule → strict CORE

The 2025 share is 9.8% under both rules **only because large changes offset each other** — not because the classifier did not change.

| postings per year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| earlier broader rule | 11 | 22 | 97 | 166 | 114 | 298 | 666 | 289 |
| − data-scientist analytics | 5 | 4 | 25 | 36 | 17 | 54 | 142 | 80 |
| − "Quantum AI" org name | 1 | 1 | 16 | 8 | 4 | 5 | 15 | 31 |
| − other | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| + Aiml / GenAI / MLOps spellings | 0 | 1 | 1 | 3 | 4 | 28 | 138 | 52 |
| + TPU / Vertex / Gemma / NotebookLM | 0 | 0 | 0 | 2 | 1 | 6 | 19 | 6 |
| + agentic | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 3 |
| + other (natural language processing) | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 0 |
| **= strict CORE** | 5 | 19 | 58 | 130 | 99 | 275 | 671 | 239 |
| identity holds | yes | yes | yes | yes | yes | yes | yes | yes |

2025: 666 − 157 removed + 162 added = 671. Exact overlap of the two rules (no sampling): the earlier rule tags 1524, strict CORE 1385, both 1119 → the earlier rule's recall against strict CORE is 80.8%, its precision 73.4%.

## Wording versus size (the lead finding)

| AI-titled postings only | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| ML-family (machine learning / ML / Aiml / MLOps), % of AI postings | 100% | 58% | 62% | 71% | 69% | 49% | 41% | 33% |
| AI/GenAI/Gemini **without** an ML-family word, % of AI postings | 0% | 37% | 36% | 22% | 29% | 43% | 55% | 63% |
| ML-family, % of **all observed** postings | 1.9% | 1.9% | 1.5% | 2.2% | 2.9% | 5.5% | 4.0% | 4.1% |
| AI/GenAI-only, % of **all observed** postings | 0.0% | 1.2% | 0.9% | 0.7% | 1.2% | 4.8% | 5.4% | 7.8% |
| (counts: ML-family / AI-only) | 5 / 0 | 11 / 7 | 36 / 21 | 92 / 29 | 68 / 29 | 136 / 119 | 272 / 367 | 79 / 150 |

Reading it: as a share of AI titles, ML-family words fall (58–71% in 2020–2023 → 33% in 2026) — but as a share of *all* postings they rose in 2024 and then held around 4%. The growth after 2023 is mostly titles labelled AI/GenAI without an ML word. **Not supported:** that ML roles were "retitled" — that would need the same role tracked across years, which this data cannot do.

### Vocabulary: share of each year's AI postings whose title contains the term

| term | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| n (AI postings) | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| machine learning | 100% | 53% | 60% | 66% | 58% | 36% | 17% | 5% | 2019 |
| AI (acronym) | 0% | 26% | 28% | 23% | 34% | 38% | 50% | 55% | 2020 |
| Aiml spelling | 0% | 5% | 2% | 2% | 4% | 9% | 20% | 20% | 2020 |
| generative / GenAI | 0% | 0% | 0% | 0% | 4% | 12% | 16% | 13% | 2023 |
| Gemini | 0% | 0% | 0% | 0% | 0% | 7% | 5% | 3% | 2024 |
| agent / agentic | 0% | 0% | 0% | 1% | 0% | 0% | 3% | 5% | 2022 |
| Vertex | 0% | 0% | 0% | 0% | 0% | 0% | 1% | 2% | 2025 |
| LLM / language model | 0% | 0% | 0% | 1% | 1% | 1% | 1% | 1% | 2022 |
| TPU / tensor | 0% | 0% | 0% | 3% | 4% | 3% | 3% | 3% | 2022 |
| responsible AI / AI safety | 0% | 0% | 2% | 4% | 0% | 1% | 2% | 1% | 2021 |

The last column is the first year the term appears in the *archive* — not necessarily its first year at Google (archive coverage varies). Note: "LLM / language model" is rare in titles (about 1% from 2022) — an earlier draft of this analysis understated it because of a matching bug that missed capitalised "Large Language Models"; this table is the corrected version.

### Data-driven comparison (AI postings first captured ≤2023, n=277, vs ≥2024, n=1108); location, spoken-language and level words dropped; ≥12 uses

- **Rising:** aiml (18% vs 3%), generative (9% vs 1%), genai (6% vs 0%), data (6% vs 2%), gemini (6% vs 0%), applied (5% vs 2%), analyst (3% vs 1%), security (2% vs 0%), systems (2% vs 0%), safety (3% vs 1%), agent (2% vs 0%), architect (3% vs 1%), innovation (1% vs 0%), manager (15% vs 12%), field (2% vs 1%), quality (1% vs 0%), ads (3% vs 2%), engineering (5% vs 3%), trust (2% vs 1%), sector (1% vs 0%), partner (1% vs 0%), product (6% vs 5%), compute (1% vs 0%), sales (4% vs 3%)
- **Falling:** machine (17% vs 63%), learning (18% vs 63%), industry (0% vs 6%), solutions (4% vs 10%), conversational (1% vs 4%), research (10% vs 18%), platform (2% vs 5%), professional (1% vs 3%), artificial (1% vs 4%), software (43% vs 51%), engineer (55% vs 63%), health (2% vs 4%)

Reading it (inference): generative/GenAI/Gemini/agent vocabulary arrives from 2023; the "Cloud AI and Industry Solutions" team-name words ("industry", "solutions", "conversational") fade; "research" falls; "data", "analyst", "safety", "trust" rise.

## Role families (mutually exclusive, first match wins)

Order: 1 ai_safety_responsible > 2 sales_consulting_gtm > 3 product_program_mgmt > 4 business_functions > 5 research > 6 infra_hardware > 7 ml_ai_engineering > 8 management_other > 9 other_functions.

| share of that year's AI postings | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| n (AI postings) | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| ai_safety_responsible | 0% | 0% | 3% | 5% | 1% | 1% | 3% | 3% |
| sales_consulting_gtm | 20% | 21% | 22% | 7% | 18% | 12% | 16% | 15% |
| product_program_mgmt | 0% | 0% | 9% | 8% | 7% | 7% | 8% | 8% |
| business_functions | 0% | 0% | 9% | 3% | 7% | 4% | 10% | 7% |
| research | 0% | 26% | 12% | 7% | 4% | 15% | 3% | 6% |
| infra_hardware | 0% | 0% | 0% | 9% | 21% | 8% | 10% | 15% |
| ml_ai_engineering | 80% | 47% | 43% | 55% | 39% | 49% | 47% | 44% |
| management_other | 0% | 0% | 2% | 4% | 2% | 4% | 2% | 2% |
| other_functions | 0% | 5% | 0% | 2% | 0% | 0% | 0% | 1% |
| sum | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

- **Constant:** ML/AI engineering is the largest family every year (2021 43%, 2022 55%, 2023 39%, 2024 49%, 2025 47%, 2026 44%); sales/consulting/go-to-market 7–22%; product/program management 7–9% since 2021; AI safety/responsible AI small (≤5%).
- **Moved:** infrastructure & hardware 2021 0%, 2022 9%, 2023 21%, 2024 8%, 2025 10%, 2026 15% (bouncy; 2023 n=99); research is noisy (26% in 2020 on n=19, 15% in 2024, 3% in 2025).

Families are heuristics (about 1 wrong in 24 in a spot check); the "business functions" family was split out of a mixed management bucket after review.

## AI as a team label on non-AI work — a supported lead, not a finding

**What is claimed:** a growing share of AI-titled postings are functions unrelated to AI expertise (marketing, UX/design, ops/support/escalations, policy/government affairs, HR/finance, generic front-end/full-stack engineering) where "AI" is only the team or product name. One rule was applied to every year (so 2025 is compared on the same basis as the rest).

| share of AI postings | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| n (AI postings) | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| rule: domain-only postings (k) | 0 | 0 | 2 | 5 | 3 | 15 | 66 | 17 |
| rule: share | 0.0% | 0.0% | 3.4% | 3.8% | 3.0% | 5.5% | 9.8% | 7.1% |
| hand-corrected estimate | 0.0% | 0.0% | 3.0% | 2.1% | 1.9% | 5.2% | 8.4% | 5.7% |

2025 hand-corrected ≈ 8.4% (95% Wilson interval 6.5–10.7%) against ≈ 3.7% pooled over 2021–2024 (n=562; 2.5–5.6%). The intervals do not overlap; 2026 (≈5.7%) overlaps both.

**Checks it survived:** one rule on all years; a hand check of 118 titles (all 40 borderline, 18 other domain calls, 60 "work" calls); a baseline showing that domain-function words among *all* observed postings did not rise in 2025 (2019 16%, 2020 15%, 2021 19%, 2022 17%, 2023 12%, 2024 12%, 2025 14%, 2026 11%), so it is not simply broader archive coverage of non-technical roles.
**What the hand check found:** of 40 borderline titles the rule wrongly called 10 "domain" (e.g. "Android AI Core", "Chrome Web AI Platform", "Group Product Manager, Compliance and Policy, Generative AI"); of 18 other domain calls, 3 were wrong (one was a regex bug: "Tele*communications*" matched "communications"); of 60 "work" calls, none was a clear domain miss and 2 were ambiguous. The hand-corrected row applies those corrections (exact for the borderline group; the non-borderline group scaled by its 2-in-17 error rate).

**Composition (rule, uncorrected)** — 2025 (n=66): marketing / brand 12, UX / design 12, ops / support / escalations 10, generic front-end / full-stack / mobile / web engineering 9, policy / government affairs 8, finance / people / recruiting 5, comms / writing 5, legal / counsel 3, strategy 2. 2021–2024 (n=23): generic front-end / full-stack / mobile / web engineering 6, comms / writing 5, UX / design 4, marketing / brand 4, policy / government affairs 3, finance / people / recruiting 1. 2026 (n=17): UX / design 7, marketing / brand 4, finance / people / recruiting 2, comms / writing 2, ops / support / escalations 1, policy / government affairs 1. The 2025 excess is marketing/brand, UX/design and ops/support/escalations (the last had none in 2021–2024).

**Why only a *supported lead*:** the checker is one judge who also wrote the rule, unblinded. The direction survives the hand check and the uniform-rule comparison; the size is uncertain (rule 9.8% vs corrected ≈8.4% for 2025). **What would upgrade it:** an independent reader classifying the same 40 borderline titles (Appendix A) and a fresh random sample of ~100 AI titles from 2021–2024 and 2025. Cause (AI becoming a product-wide theme, so non-AI functions were hired under AI team names) is inference; also unresolved is whether Google hired more of these roles or Wayback archived more of them.

## AI × cybersecurity

| postings | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| AI postings that are also security-tagged — raw | 0 | 0 | 0 | 0 | 0 | 0 | 18 | 5 |
| — cleaned (false positive removed) | 0 | 0 | 0 | 0 | 0 | 0 | 17 | 5 |
| AI postings (n) | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| cleaned, % of AI postings | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.5% | 2.1% |
| security-tagged postings (n) | 8 | 16 | 74 | 202 | 142 | 142 | 322 | 118 |
| cleaned, % of security postings | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 5.3% | 4.2% |

Raw 23 postings, cleaned 22. Footnote: the one excluded false positive is "Aiml Engineer National Security Public Sector" — "security" there means *national* security. Counts under 10 are noisy (2026: 5). Titles: AI Information Security Engineer; AI Information Security Engineer; AI Security Engineer; Distinguished Security Engineer Cyber And AI Cloud Security; Group Product Manager AI Agent Security And Authorization; Security Engineer AI Agent Security; Security Engineer AI Agent Security; Security Engineer AI Agent Security; Security Engineer AI Protection; Senior AI Threat Intelligence Integrator; Senior Security Engineer AI Systems Security; Senior Security Engineer AI Systems Security; Senior Security Engineer Agentic Red Team Deepmind; Senior Software Engineer AI Security Agents; Software Engineer III AI Agent Security Core; Software Engineer III AI Agent Security Core Systems; Software Engineer III Cloud AI Security And Compliance; Software Engineer Threat Infrastructure And Detection AI Security; Software Engineering Manager Core AI Security Agents; Staff Security Engineer AI Vulnerability Research; Staff Security Engineer AI Vulnerability Research; Staff Security Engineer AI Vulnerability Research. The shares of security postings (about 5–6% in 2025, 4% in 2026) agree with the cybersecurity analysis's AI-in-security-titles figures.

## Data science (analytics) — separate layer

| share of observed postings | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| data-science-only postings (k) | 5 | 4 | 25 | 36 | 17 | 54 | 142 | 80 |
| share | 1.9% | 0.7% | 1.1% | 0.8% | 0.7% | 2.2% | 2.1% | 4.2% |
| 95% interval | 0.8–4.3% | 0.3–1.8% | 0.7–1.6% | 0.6–1.2% | 0.4–1.1% | 1.7–2.8% | 1.8–2.4% | 3.4–5.1% |

This is Ads/product analytics, not AI. It rises from 0.7–1.1% (2020–2023) to 4.2% in 2026 (2026 does not overlap 2025). Cause unknown. 2019 (k=5) and 2020 (k=4) are noisy.

## Quality of the classifier

Every figure here is from **one sample, judged by the classifier's own author, unblinded.**

- **Precision** (100 matched titles, stratified by year): raw 94 of 100 judged AI-as-work (6 domain-only, 0 outright false matches); **year-weighted strict precision 86.3% ± 9.9**. The gap between 94 and 86: sampling gave roughly equal titles per year, but the 2025 stratum is 45% of all AI postings and held 5 of the 6 domain-only titles, so population weighting lowers precision. Counting domain-only titles as correct, precision is ≈100% (no outright false match in 100, i.e. below about 3–4%).
- **Recall** of the strict rules: 100 weak-signal and 150 remainder titles among the unmatched; missed ≈14 (95% interval 2–75) clear plus ≈82 (interval 38–171) if ambiguous titles count; 0 of 150 remainder titles positive (rule-of-three upper bound 309). Residual recall 94.4–99.0% central; conservative floor 74.3% (loose, from the small remainder sample).
- Not countable from titles and excluded: generic "Research Scientist, Google Research" (~157), Google Assistant roles (~63), ranking/recommendation/personalization, perception/robotics, translate/speech.

## What changed / what stayed

**Changed:** a step up in AI share in 2024 (4.2% → 11.1%); wording moved from "machine learning" to "AI"/"Aiml"/GenAI (generative/GenAI 0% to 2022, 4% in 2023, 12% in 2024; Gemini 7% in 2024; agentic/agent from 2022, 5% in 2026; Vertex only from 2025); AI × security titles from 2025; analytics titles rising; a supported lead that AI became a team label for non-AI functions in 2025.
**Stayed:** ML/AI engineering is the largest family every year; sales/consulting/go-to-market is a steady 7–22% of AI titles; product/program management 7–9%; AI safety small.

## What the data cannot say — and the sensible next step

Titles cannot show skills, seniority mix or whether roles were retitled rather than created. Skills need job descriptions: the live crawler (`google-live/`) covers currently-active security roles; descriptions for AI roles would need one extra page load per role, which has not been requested. A second, independent reader for the classifier (Appendix A) is the cheapest way to firm up the team-label lead.

## Appendix A — the 40 borderline titles and the hand-check verdict for each

"Rule" = the rule called it AI-as-domain. "Verdict" = my reading, single judge, unblinded. Please check them yourself.

| # | first captured | title | rule | my verdict |
|---|---|---|---|---|
| 1 | 2025 | Android Studio Engineer AI Benchmark Tooling | domain | **work** (rule wrong) |
| 2 | 2024 | Staff Software Developer Front End Applied AI | domain | domain (agree) |
| 3 | 2025 | Product Policy Specialist Generative AI | domain | domain (agree) |
| 4 | 2024 | Software Engineer Fullstack Conversational AI Learnx | domain | domain (marginal) |
| 5 | 2025 | Operations Manager GENAI Trust And Safety Youtube | domain | domain (agree) |
| 6 | 2025 | Vendor Operations Manager GENAI | domain | domain (agree) |
| 7 | 2025 | Aiml Research Practice Principal Executive Recruiting | domain | domain (agree) |
| 8 | 2026 | Product Marketing Manager Retail Ads Agentic Commerce | domain | domain (agree) |
| 9 | 2025 | Senior Staff UX Design Manager GENAI Creation Youtube | domain | domain (agree) |
| 10 | 2025 | Senior Policy Specialist Product And Generative AI Solutions | domain | domain (agree) |
| 11 | 2024 | UX Designer Core Machine Learning | domain | domain (agree) |
| 12 | 2023 | Business And Marketing Data Scientist Applied Machine Learning | domain | **work** (rule wrong) |
| 13 | 2023 | Senior Product Marketing Manager Generative AI Youtube | domain | domain (agree) |
| 14 | 2025 | Data Center Operations Manager Machine Learning Travel | domain | **work** (rule wrong) |
| 15 | 2025 | UX Lead Youtube GENAI Lab | domain | domain (agree) |
| 16 | 2025 | Senior Software Engineer Front End Google Cloud AI | domain | domain (agree) |
| 17 | 2024 | Generative AI Product Marketing Manager Search Marketing | domain | domain (agree) |
| 18 | 2025 | Escalations Analyst Search And Generative AI | domain | domain (agree) |
| 19 | 2025 | Senior Technical Program Manager Marketing Engineering Aiml | domain | domain (marginal) |
| 20 | 2025 | Software Developer III Gemini Code Assist Full Stack | domain | domain (marginal) |
| 21 | 2025 | Product Policy Lead Generative AI | domain | domain (agree) |
| 22 | 2026 | Interaction Designer Android AI Experiences | domain | domain (agree) |
| 23 | 2025 | Escalations Analyst Trust And Safety Search GENAI | domain | domain (agree) |
| 24 | 2024 | Software Developer III Front End Google Cloud AI | domain | domain (agree) |
| 25 | 2022 | Business And Marketing Data Scientist Applied Machine Learning | domain | **work** (rule wrong) |
| 26 | 2026 | Internal Communications Manager GENAI And Chief AI Architect | domain | domain (agree) |
| 27 | 2025 | GENAI Vendor Operations Manager | domain | domain (agree) |
| 28 | 2025 | Staff Software Engineer Gemini Enterprise Mobile& | domain | domain (marginal) |
| 29 | 2022 | Technical Program Manager Finance Machine Learning | domain | **work** (rule wrong) |
| 30 | 2024 | Senior Software Engineer Full Stack Google Cloud AI | domain | domain (agree) |
| 31 | 2025 | Product Policy Lead GENAI | domain | domain (agree) |
| 32 | 2024 | Software Engineer III Full Stack Google Cloud AI | domain | domain (agree) |
| 33 | 2022 | Software Engineer III Front End Google Cloud Platform AI And Industry Solutions | domain | domain (agree) |
| 34 | 2024 | Architecture Technical Writer Aiml | domain | domain (agree) |
| 35 | 2025 | Software Engineer Chrome Web AI Platform | domain | **work** (rule wrong) |
| 36 | 2026 | Program Manager Aiml Finance Data And Analytics | domain | **work** (rule wrong) |
| 37 | 2025 | Software Engineer Android AI Core | domain | **work** (rule wrong) |
| 38 | 2025 | Staff Software Engineer Front End Gemini Cloud Assist | domain | domain (agree) |
| 39 | 2026 | Business And Marketing Data Scientist Applied Machine Learning | domain | **work** (rule wrong) |
| 40 | 2025 | Group Product Manager Compliance And Policy Generative AI | domain | **work** (rule wrong) |

## Appendix B — how to reproduce

`plugins/job_search/wayback_google_ai.py`, op `google_wayback_ai_trends(domain, data_repo_path)` (analyze kind, no network, ~2 s) regenerates every table in this file except the hand-check block, the precision/recall samples and the data-driven token comparison (`google-ai/c4_generate.py`). Rules version `google-ai-rules/v2 (2026-09-19)`; tests in `tests/test_google_wayback_ai.py` (41). Registration in `plugins/job_search/__init__.py` is left to the maintainer (`google-ai/PLUGIN_NOTES.md`).

## Checkpoint 5 addendum — cross-checks and what remains unknown

*(Appended after the main analysis; the sections above are unchanged apart from two edits: the title now says 2019–2026 because the archive holds no AI posting before 2019, and a typo "7%%" became "7%".)*

### Direction cross-check against the archived front-page snapshots

The front-page snapshots are a separate, much smaller source: 79 parseable Wayback snapshots of Google's careers search page (5 more captures were unparseable), each showing 18–20 listings that the site chose to display (a **small, relevance-sorted sample**, not the whole board; the same listing can appear in several snapshots, so these are not independent postings and the intervals below are optimistic). The strict CORE rule (same `classify_ai_title`) was applied to those listing titles. Only the *direction* is compared, not the level.

| year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| snapshots | 3 | 8 | 12 | 12 | 12 | 12 | 11 | 9 |
| listings (denominator) | 60 | 160 | 240 | 240 | 231 | 240 | 220 | 179 |
| strict-CORE listings (k) | 1 | 4 | 2 | 7 | 16 | 29 | 23 | 28 |
| front-page share | 1.7% | 2.5% | 0.8% | 2.9% | 6.9% | 12.1% | 10.5% | 15.6% |
| Wilson 95% interval (optimistic) | 0.3–8.9 | 1.0–6.3 | 0.2–3.0 | 1.4–5.9 | 4.3–11.0 | 8.5–16.8 | 7.1–15.2 | 11.0–21.7 |
| posting-list share (main table) | 1.9% | 3.3% | 2.5% | 3.0% | 4.2% | 11.1% | 9.8% | 12.4% |

Reading it: **the shape agrees** — low (about 1–3%) through 2022, higher from 2023, a clear step by 2024 (12.1%), no further rise in 2025 (10.5%, intervals overlap 2024), and the highest value in 2026 (15.6%). Two differences: the front page already shows 6.9% in 2023 (posting list 4.2%; the intervals just overlap), so on the front page the rise looks more gradual, and its 2026 level (15.6%) is above the posting list's (12.4%) though inside its interval. Small years (2019, 2020) have k < 5 listings and mean nothing. Levels are not expected to match: the front page shows what Google ranked first, not what was live. Both sources are limited to what Wayback archived, so agreement in shape is corroboration of direction, not independent proof.

### Cross-check against the cybersecurity analysis (AI × security)

- The posting-list crossover here (strict CORE title that also carries the security tag) is 0 before 2025, 18 in 2025 (17 after removing one false positive, "Aiml Engineer, National Security, Public Sector") and 5 in 2026 — i.e. 17 of 322 security-tagged postings (5.3%) in 2025 and 5 of 118 (4.2%) in 2026 (small n, noisy). As a share of strict CORE postings: 18/671 (2.7%) and 5/239 (2.1%) raw.
- `google-wayback-analysis.md` reports AI in security titles as 0% in every year to 2024, then 6% (2025) and 4% (2026) by its broader rule; after the parent's edit it quotes the same 17/322 and 5/118. The two analyses agree on timing (nothing before 2025) and on size (roughly 4–6% of security postings).
- The front-page sample gives no crossover listing in any year (0 of 220 in 2025, 0 of 179 in 2026); with only 7 (2025) and 10 (2026) security-tagged listings, 0 is what a ~5% rate would produce (expected about 0.4 and 0.5), so it neither supports nor contradicts the posting result.

### What this data cannot say, and the next step

- **Skills.** Titles show role types, not skills; knowing whether "AI Engineer" work changed needs job descriptions.
- **Hiring versus archive density.** Archived postings per year swing from 269 to 6,824. Shares partly cancel that, but "more AI roles hired" cannot be separated from "Wayback captured more AI-related pages" (or the reverse) from this data.
- **Renamed versus new.** A title change is not a new job; the renaming finding is about wording.
- **Next step.** The job-description worker (per the parent) is already recovering descriptions for postings archived from mid-2023; joining those to the AI flags in `google-wayback-ai-trends.json` (by `job_id`) is the sensible way to test skills and the "AI as team label" lead. This replaces the earlier note above that descriptions "have not been requested". An independent second reader of Appendix A remains the cheapest upgrade for the lead.

