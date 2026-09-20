# Checkpoint 2 tables (scratch; C4 will turn these into deliverables)
Denominator rule: a posting counts toward every year it was captured (same as analyze_job_index / the cybersecurity tables). Shares = % of that year's observed postings.

| | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|---|---|---|---|
| observed postings | 269 | 572 | 2,326 | 4,276 | 2,371 | 2,469 | 6,824 | 1,925 |
| strict CORE count | 5* | 19* | 58 | 130 | 99 | 275 | 671 | 239 |
| **(a) strict CORE share** | 1.9% | 3.3% | 2.5% | 3.0% | 4.2% | 11.1% | 9.8% | 12.4% |
| (b) strict CORE + DeepMind | 1.9% | 3.3% | 2.5% | 3.0% | 4.2% | 11.1% | 9.8% | 13.8% |
| (c) strict CORE + AI-adjacent | 4.8% | 4.7% | 4.0% | 4.4% | 4.9% | 13.8% | 10.7% | 14.3% |
| data-science-only share (separate layer) | 1.9% | 0.7% | 1.1% | 0.8% | 0.7% | 2.2% | 2.1% | 4.2% |
| (memo) published broad rule | 4.1% | 3.8% | 4.2% | 3.9% | 4.8% | 12.1% | 9.8% | 15.0% |
Counts behind the separate lines: AI-adjacent 8/8/35/60/17/65/56/37; DS-only 5/4/25/36/17/54/142/80; DeepMind-only 27 (all 2026; 34 DeepMind-titled in total, 7 already CORE by other words). `*` = n<30, noisy.

Family shares: see c2_family_table.md.

## Sample method (all judged by the worker alone, no second rater)
- Precision: 100 matched titles, stratified by first-captured year (all 5 from 2019, ~12-17 per other year); two-level rubric Y (AI/ML is the substance of the role) / D (AI is only the team/product domain of an unrelated function) / N (false match). Result 94 Y, 6 D, 0 N raw; population-weighted: strict 86.3% +/-9.9, lenient (Y+D) ~100% (no outright false match in 100 => <~3-4%). 5 of the 6 D titles are 2025.
- Recall of the proposed rules (residual): unmatched pool split into W (weak signal words, 1,371 postings) and R (15,431 rest). W sample 100: 1 clear miss, 5 ambiguous. R sample 150: 0. Missed ~14 (CI 2-75) strict, ~82 (CI 38-171) incl. ambiguous; R upper bound 309 (rule of three). Recall central 94.4-99.0%; conservative floor 74.3%.
- Exact (no sampling): published rule vs new CORE: recall 80.8% (1,119/1,385), precision 73.4% (1,119/1,524). The earlier "~79%" was this comparison, estimated by class counts.
