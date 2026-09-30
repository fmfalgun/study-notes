# GATE DA — Previous-Paper Analysis (2024–2026)

Analysis of all 3 official GATE DA (Data Science and Artificial Intelligence) sittings that
have ever existed — 2024, 2025, 2026 (DA is a new GATE paper; there is no 2021–2023 DA
data) — downloaded from `gate2027.iitm.ac.in/download`, mapped against DA's syllabus
sections in `gfg-gate-topic-map.md` (§1–5/9/11 shared with CS, §13 Machine Learning and §14
Artificial Intelligence DA-only).

## Methodology

Identical pipeline to `exam-analysis-report.md` (CS) — see that file for full detail on
extraction/splitting/classification/scoring. Same lexicon, same word-boundary matching, same
"2+ section hits = Complex" bar, same aggregation formula:

```
avg_weightage% = mean(per-sitting topic%) across all 3 sittings
score = avg_weightage% + (total complex-question count across all 3 sittings × 1.5)
```

**Sample-size caveat specific to DA**: 3 sittings (165 subject questions total) is a much
thinner dataset than CS's 8 sittings (440 questions) — DA simply hasn't existed long enough
to have more. Every number below should be read with wider error bars than the CS report's
equivalent numbers.

## Aggregate Topic Weightage (3 sittings, 165 subject questions)

| Topic | Avg weightage % | Total Qs | Total Complex | Score |
|---|---|---|---|---|
| Probability & Statistics (Eng. Math) | 15.2% | 25 | 10 | 30.2 |
| Databases (DBMS) | 11.5% | 19 | 11 | 28.0 |
| Programming & Data Structures | 13.9% | 23 | 6 | 22.9 |
| Discrete Mathematics | 10.3% | 17 | 8 | 22.3 |
| Machine Learning | 9.1% | 15 | 4 | 15.1 |
| Linear Algebra (Eng. Math) | 9.7% | 16 | 1 | 11.2 |
| Algorithms | 3.0% | 5 | 2 | 6.0 |
| Calculus (Eng. Math) | 1.2% | 2 | 1 | 2.7 |
| Artificial Intelligence | 2.4% | 4 | 0 | 2.4 |

**Unclassified: 39/165 subject questions (23.6%)** — lower than CS's 29.3%, but still
substantial; see Limitations.

*No Digital Logic, Computer Organization, Operating System, Theory of Computation, or
Compiler Design rows — those aren't on the DA syllabus at all, consistent with
`gfg-gate-topic-map.md`.*

## Per-Sitting Breakdown

| Sitting | DBMS | ML | AI | Calculus | Lin.Alg | Probability | Discrete Math | Prog&DS | Algorithms | Unclassified |
|---|---|---|---|---|---|---|---|---|---|---|
| 2024-DA | 3 | 4 | 1 | 1 | 5 | 7 | 7 | 8 | 3 | 16 |
| 2025-DA | 7 | 3 | 1 | 1 | 6 | 12 | 7 | 7 | 1 | 10 |
| 2026-DA | 9 | 8 | 2 | 0 | 5 | 6 | 3 | 8 | 1 | 13 |

DBMS and ML both trend upward year over year (3→7→9 and 4→3→8 respectively) — too short a
series to call a trend with confidence, but worth watching if a 2027 paper analysis is added
later.

## Complex Question Citations (by topic)

- **Probability & Statistics**: 2024-DA Q57, Q64 · 2025-DA Q19, Q35, Q39, Q40, Q41, Q60 ·
  2026-DA Q28, Q54
- **Databases (DBMS)**: 2024-DA Q55 · 2025-DA Q16, Q33, Q46, Q56, Q57 · 2026-DA Q26, Q42,
  Q51, Q60, Q61
- **Discrete Mathematics**: 2024-DA Q41 · 2025-DA Q22, Q42, Q43, Q44, Q48 · 2026-DA Q29, Q32
- **Programming & Data Structures**: 2024-DA Q40 · 2025-DA Q18, Q27 · 2026-DA Q15, Q31, Q39
- **Machine Learning**: 2024-DA Q18 · 2026-DA Q23, Q37, Q55
- **Algorithms**: 2024-DA Q44 · 2026-DA Q40
- **Linear Algebra**: 2024-DA Q22
- **Calculus**: 2025-DA Q51

*No Complex citations for Artificial Intelligence — its 4 detected questions all hit exactly
one lexicon section each. Given AI's very low overall detection (2.4%), this likely reflects
classifier under-reach (see Limitations) rather than AI questions genuinely being simple.*

## Key Findings

1. **Probability & Statistics is DA's single highest-weighted topic** (15.2%, plus the
   highest complex-question count at 10) — makes sense given DA's syllabus explicitly adds
   hypothesis testing/z-test/t-test/chi-squared/CLT on top of CS's baseline probability
   content.
2. **Databases (DBMS) scores far higher for DA (11.5%) than for CS (4.8%)** — consistent with
   DA's syllabus explicitly weighting data warehouse/dimensional modelling content that CS's
   syllabus doesn't test as heavily.
3. **Machine Learning (9.1%) and Artificial Intelligence (2.4%) are both real syllabus
   sections with disproportionately low detected weightage relative to Probability/DBMS** —
   see Limitations before concluding they're actually low-priority.
4. **GA (Q1–10, 10/65 = 15.4% of every sitting) is excluded from topic scoring**, same
   treatment as the CS report.

## Limitations (read before trusting the numbers above)

1. **Only 3 sittings exist** — DA launched in 2024, so this is the entire historical dataset,
   not a sample of a larger one. Wider variance is expected; don't over-index on small
   differences between adjacent tiers.
2. **23.6% of subject questions got no keyword match** — same automated-classification
   caveat as the CS report; treat percentages as a lower-bound signal.
3. **Artificial Intelligence's 2.4% is very likely under-counted.** AI questions
   (search-tree traces, minimax game trees, Bayesian network diagrams) are often
   diagram-heavy with the actual reasoning shown in a figure `pdftotext` can't extract —
   the keyword lexicon has very little text to match against for exactly the DA-specific §14
   content added to `gfg-gate-topic-map.md`. Do not deprioritize AI based on this number.
4. **Machine Learning's 9.1% may also be under-counted** for the same figure-heavy reason
   (confusion matrices, decision boundaries, clustering diagrams) — the true weightage is
   plausibly higher than shown here.
5. Same "Complex = 2+ section keyword hits, not verified difficulty" caveat as the CS report
   applies here.
6. This report was built by a single automated pass, not spot-checked question-by-question.
   `exam-priority-report-da.md`'s tiers are a **starting filter**, more so than usual given
   both the automation-noise layer and the thin 3-sitting sample.
