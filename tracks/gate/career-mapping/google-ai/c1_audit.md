# Checkpoint 1 — AI classifier audit (scratch notes, not a deliverable)

Data: 18,188 distinct postings (cdx capture). Current rule (`classify_title` "ai") tags 1,524.

## False positives in the current tag
- 355 (23.3%) contain "data scien*" -> Ads/product analytics, not AI/ML. Move to a separate layer.
- 76 (5.0%) contain "Quantum AI" -> Google's quantum-computing lab (qubits, error correction). Not AI/ML. 31 of them in 2026, 17 in 2021.
- Sample of 40 non-DS tagged titles: 37 fine, 2 clear FP (Quantum AI), 1 borderline (Quantum error correction + "Applied ML").
- Domain-only mentions (e.g. UX Research Manager, "Search Discover AI") are tagged but are not AI/ML work; they land in the "other functions" family, not dropped.

## False negatives (missed by the current rule)
- 213 postings spell it "Aiml" (slug of "AI/ML" loses the slash): 2019-2023 total 9; 2024: 25; 2025: 135 (2.0% of 2025); 2026: 51. Biggest gap, and it hits 2025 hardest.
- 45 TPU / Tensor Processing Units / Vertex / Gemma / NotebookLM (AI hardware & platform names).
- 10 agentic / autonomous agents / agent platform.
- 29 "DeepMind" titles -- ALL in 2026 (none earlier). See QUESTION 1.
- Not countable from titles (excluded, count only): generic "Research Scientist/Engineer, Google Research" ~157; "Google Assistant" product roles 63; ranking/recommendation/personalization 19; perception/robotics 14; translate/speech/machine translation ~29.

## Estimated quality
- Current rule vs strict CORE AI/ML: ~72% of tagged postings are core (rest = 23% analytics + 5% Quantum AI).
- Non-DS, non-quantum tags: ~93% precise in the 40-title sample (small sample; +-8pp).
- Recall of current rule for core: ~79% (1,093 of ~1,385 postings core under the proposed rules).

## Proposal (see c1_rules_draft.py)
CORE = title (after removing "Quantum AI" and "data scien*") matches: machine/deep/reinforcement learning, artificial intelligence, computer vision, neural, language model(s), generative, gemini/gemma/notebooklm/bard, natural language, agentic / agent platform, tensor processing / TPU / vertex, aiml/genai/mlops spellings, or AI/ML/LLM/NLP/GenAI acronyms.
DATA-SCIENCE = "data scien*" titles without a core word (separate layer). DS titles WITH a core word count as core too (25).
Families (first match): ai_safety_responsible, sales_consulting_gtm, product_program_mgmt, research, infra_hardware, ml_ai_engineering, management_other, other_functions.
Draft result: CORE 1,385 postings; DS-only 330. Families over core: ml_ai_engineering 670, sales_consulting_gtm 202, infra_hardware 176, product_program_mgmt 108, research 96, management_other 65, ai_safety_responsible 35, other_functions 33.
Known family flaw to fix in C2: "performance" keyword sends ML engineers to infra_hardware; drop it. Family spot-check: ~1 wrong in ~24.

## Draft CORE share of observed postings (vs current rule)
year      2019 2020 2021 2022 2023 2024 2025 2026
observed   269  572 2326 4276 2371 2469 6824 1925
current    4.1  3.8  4.2  3.9  4.8 12.1  9.8 15.0
CORE draft 1.9  3.3  2.5  3.0  4.2 11.1  9.8 12.4
DS-only    1.9  0.7  1.1  0.8  0.7  2.2  2.1  4.2
Shape holds (low until 2023, jump 2024, no further rise 2025, higher 2026); levels are lower than published for 2019-2023 and 2026. 2025 observed postings rose 2.8x vs 2024 -- if the extra coverage is broad rather than AI-specific it dilutes the 2025 share; cannot be resolved from this data.
