# Checkpoint 3 narrative draft — Google AI roles, what changed and what stayed (DRAFT; not a deliverable)
Every claim carries its counts. Causes are marked *inference*. Caveats that apply to all of it: postings are only what Wayback archived; yearly archived counts swing (269 -> 6,824) so shares of observed postings are used; 2019/2020 have n<30 CORE postings and are noisy; 2026 is partial; titles show role TYPES not skills; classification is a keyword heuristic judged by a single unblinded judge (its author).

## What changed
1. **A step up in 2024, then a plateau.** Strict CORE share of observed postings: 2-4% in 2019-2023 (1.9/3.3/2.5/3.0/4.2%), 11.1% in 2024 (275/2,469), 9.8% in 2025 (671/6,824), 12.4% in 2026 to Sept (239/1,925). The 2025 dip is not distinguishable from archive coverage broadening (2025 observed postings x2.8, CORE postings x2.4) — *inference*, unverifiable. The old published rule's 2025 value (9.8%) equals the new one only through offsetting changes of ~160 postings each way.
2. **The words changed more than the work.** "machine learning" in AI titles: 53-66% (2020-23) -> 36% (2024) -> 17% (2025) -> 5% (2026). "AI" acronym: 26-34% -> 38% -> 50% -> 55%; "Aiml" spelling 2-4% -> 9% -> 20%. But ML-family titles (any spelling) stay ~4-5.5% of ALL postings since 2024 (5.5/4.0/4.1%) while AI/GenAI-labelled titles without an ML word grow 1.2% (2023) -> 4.8% -> 5.4% -> 7.8%. So the post-2023 growth is mostly AI/GenAI-labelled roles, not more "machine learning" roles.
3. **GenAI vocabulary arrives in 2023.** generative/GenAI: 0% to 2022, 4% (2023), 12% (2024), 16% (2025), 13% (2026). Gemini 7% (2024), 5%, 3%. Agentic/agent: 1% (2022) -> 3% (2025) -> 5% (2026). Vertex only from 2025 (1-2%). LLM/"language model" is almost absent from titles (max 1%). (First appearance in the archive is not first appearance at Google.)
4. **Team names fade.** "Industry" (from "Cloud AI and Industry Solutions") 6% of early CORE titles -> 0%; "conversational" 4% -> 1%; "research" 18% -> 10%. Rising tokens: data (2% -> 6%), analyst, safety, trust, agent, security.
5. **Infrastructure/hardware grew.** 0% (2021) -> 9% (2022) -> 21% (2023, n=99) -> 8% -> 10% -> 15% (2026). Bouncy.

## AI spreading beyond engineering — FINDING (moderate confidence on direction; magnitude approximate)
The share of CORE postings where AI is only a team/product label on an unrelated function rose to about 8% in 2025 (rule 9.8% = 66/671; hand-corrected ~8.4%, 7-9%) from ~3.7% pooled 2021-24 (n=562); Wilson intervals do not overlap. 2026 (5.7%) overlaps both. It survived: one rule on all years; 118 hand-checked titles (10/40 borderline were wrong and corrected); a baseline showing domain-function words among ALL postings did not rise in 2025 (14% vs 11-19%). 2025's excess is marketing/brand (12), UX/design (12), ops/support/escalations (10, vs 0 in 2021-24), front-end/full-stack (9), policy/gov affairs (8). *Inference:* AI became a product-wide theme, so non-AI functions were hired under AI team names. Not shown: whether Google hired more of these, or Wayback archived more of them.

## What stayed constant
- ML/AI engineering is the largest family every year with adequate n: 43/55/39/49/47/44% (2021-2026).
- Sales/consulting/go-to-market 7-22% (12-16% in 2024-26); product/program management 7-9% every year since 2021; AI safety/responsible AI small (<=5%).

## AI x cybersecurity
Zero crossover titles before 2025. 18 postings in 2025 (2.7% of CORE, 5.6% of 322 security-tagged), 5 in 2026 (2.1%, 4.2% of 118; k<10 noisy). 22 of 23 titles are genuine (AI agent security, AI vulnerability research, AI systems security, AI threat intelligence, agentic red team); 1 is "national security". Matches the cybersecurity analysis (AI enters security titles in 2025).

## Data science (analytics, not AI) — separate
0.7-1.1% of observed postings 2020-2023, 2.2% (2024), 2.1% (2025), 4.2% (2026; 3.4-5.1%, non-overlapping with 2025). It is Ads/product analytics. Cause unknown.

## Quality of the classifier
Single sample, single judge (the rule's author), unblinded. Precision raw 94/100, year-weighted strict 86.3% +/-9.9 (gap: the 2025 stratum is 45% of CORE and held 5 of the 6 domain-only titles). Residual recall 94-99% central, floor ~74% (loose bound). Exact: published rule vs new CORE recall 80.8%, precision 73.4%.
