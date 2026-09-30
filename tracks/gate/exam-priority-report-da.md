# GATE DA Exam Priority Report — Highest-Priority Links by Tier

Extends `topics/exam-analysis-report-da.md`. Same approach as the CS priority report: lists
the **actual highest-priority links per topic**, filtered from `topics/gfg-gate-topic-map.md`,
based on which sub-clusters the 3 analyzed DA sittings (2024–2026 — the entire history of the
DA paper) actually hit. Everything not listed here still exists in
`topics/gfg-gate-topic-map.md`, just lower priority.

## Methodology

Same formula as the CS report:

```
score = avg_weightage% (mean of per-sitting %, out of 55 subject questions) + (total complex-question count × 1.5)
```

**Read this report more cautiously than the CS one.** Two compounding limitations apply here
specifically (see `topics/exam-analysis-report-da.md` for detail):

1. Only 3 sittings (165 questions) exist at all — DA is a new paper, this isn't a sample of a
   bigger dataset, it's the whole population so far.
2. Machine Learning and Artificial Intelligence — DA's two most distinctive sections, the
   ones GATE CS doesn't test — are specifically likely under-counted, since their questions
   tend to be diagram-heavy (confusion matrices, decision boundaries, search trees, Bayesian
   network diagrams) in ways plain-text extraction loses. **Don't read their low tier
   placement below as "these don't matter" — read Limitations in the analysis report first.**

---

## Tier 1 — Critical (score ≥ 25)

### 1. Probability & Statistics (score 30.2 — highest weightage AND highest complex count, 10)

Most-hit: random variables, variance/mean/expectation — classic distribution-parameter
questions dominate over the DA-specific hypothesis-testing additions.

[Random Variable](https://www.geeksforgeeks.org/random-variable/) ·
[Variance](https://www.geeksforgeeks.org/maths/variance/) ·
[Mean](https://www.geeksforgeeks.org/maths/what-is-mean/) ·
[Conditional Probability](https://www.geeksforgeeks.org/maths/conditional-probability/) ·
[Bayes's Formula](https://www.geeksforgeeks.org/maths/bayes-theorem/) ·
[Central Limit Theorem](https://www.geeksforgeeks.org/maths/central-limit-theorem/) ·
[Understanding Hypothesis Testing](https://www.geeksforgeeks.org/data-science/understanding-hypothesis-testing/)

### 2. Databases (DBMS) (score 28.0 — second-highest complex count, 11)

Most-hit: SQL queries/joins, primary keys, relational algebra, OLAP — noticeably more
SQL-query-execution-flavored than CS's DBMS questions, which lean concurrency/transactions.

[Introduction to SQL](https://www.geeksforgeeks.org/dbms/structured-query-language/) ·
[Joins](https://www.geeksforgeeks.org/sql/sql-join-set-1-inner-left-right-and-full-joins/) ·
[Keys (Candidate/Super/Primary/Alternate/Foreign)](https://www.geeksforgeeks.org/dbms/types-of-keys-in-relational-model-candidate-super-primary-alternate-and-foreign/)
· [Relational Algebra Overview](https://www.geeksforgeeks.org/dbms/introduction-of-relational-algebra-in-dbms/)
· [Solving Relational Algebra Problems for GATE](https://www.geeksforgeeks.org/dbms/how-to-solve-relational-algebra-problems-for-gate/)
· [OLTP vs OLAP](https://www.geeksforgeeks.org/dbms/differences-between-operational-database-systems-and-data-warehouse/)

---

## Tier 2 — Important (score 10–25)

### 3. Programming & Data Structures (score 22.9)

Most-hit: arrays and Python syntax tied at the top (8 hits each) — unlike CS, actual Python
language mechanics get tested directly here, not just DS structures.

[Array Notes for GATE](https://www.geeksforgeeks.org/dsa/array-notes-for-gate-exam/) ·
[Introduction to Python](https://www.geeksforgeeks.org/python/introduction-to-python/) ·
[Python Data Types](https://www.geeksforgeeks.org/python/python-data-types/) ·
[Python OOP Concepts](https://www.geeksforgeeks.org/python/python-oops-concepts/) ·
[Trees Notes for GATE](https://www.geeksforgeeks.org/dsa/trees-notes-for-gate-exam/) ·
[Hashing Notes for GATE](https://www.geeksforgeeks.org/dsa/hashing-notes-for-gate-exam/)

### 4. Discrete Mathematics (score 22.3)

Most-hit: functions overwhelmingly (16 hits vs. 1 for relations) — narrower than CS's
function+relation split.

[Classes of Functions](https://www.geeksforgeeks.org/maths/functions/) ·
[Types of Functions](https://www.geeksforgeeks.org/maths/types-of-functions/) ·
[Inverse Functions](https://www.geeksforgeeks.org/maths/inverse-functions/) ·
[Composition of Functions](https://www.geeksforgeeks.org/maths/composition-of-functions/)

### 5. Machine Learning (score 15.1 — likely under-counted, see caveat above)

Most-hit: clustering, regression variants (ridge/logistic named specifically), SVM, PCA.

[Clustering Algorithms](https://www.geeksforgeeks.org/machine-learning/different-types-clustering-algorithm/)
· [K-Means/K-Medoid](https://www.geeksforgeeks.org/machine-learning/ml-k-medoids-clustering-with-example/)
· [Regression in Machine Learning](https://www.geeksforgeeks.org/machine-learning/regression-in-machine-learning/)
· [Ridge Regression](https://www.geeksforgeeks.org/machine-learning/what-is-ridge-regression/) ·
[Logistic Regression](https://www.geeksforgeeks.org/machine-learning/understanding-logistic-regression/)
· [Support Vector Machine](https://www.geeksforgeeks.org/machine-learning/support-vector-machine-algorithm/)
· [Principal Component Analysis](https://www.geeksforgeeks.org/data-analysis/principal-component-analysis-pca/)

### 6. Linear Algebra (score 11.2)

Most-hit: matrix operations/determinants — eigenvalues present but less frequent than in the
raw syllabus emphasis; the DA-specific SVD/projection-matrix additions to
`gfg-gate-topic-map.md` got zero direct hits in this 3-sitting sample (too small a sample to
conclude they're untested).

[Matrix Operations](https://www.geeksforgeeks.org/maths/matrix-operations/) ·
[Determinants](https://www.geeksforgeeks.org/maths/what-is-determinant-of-a-matrix/) ·
[Eigenvalues and Eigenvectors](https://www.geeksforgeeks.org/engineering-mathematics/eigen-values/)
· [Rank of a Matrix](https://www.geeksforgeeks.org/maths/rank-of-matrix/) ·
[Null Space and Nullity](https://www.geeksforgeeks.org/machine-learning/null-space-and-nullity-of-a-matrix/)

---

## Tier 3 — Lower priority (score < 10)

### 7. Algorithms (score 6.0 — all detected hits are graph traversal)

[Graph Algorithms Notes for GATE](https://www.geeksforgeeks.org/dsa/graph-based-algorithms-for-gate-exam/)
(BFS/DFS, topological sort)

### 8. Calculus (score 2.7 — only 2 hits across all 3 sittings; likely under-counted for the
same notation-loss reason flagged in the CS report)

[Limits](https://www.geeksforgeeks.org/maths/limits/) ·
[Absolute Minima and Maxima](https://www.geeksforgeeks.org/maths/absolute-minima-and-maxima/)

### 9. Artificial Intelligence (score 2.4 — lowest score, but see the under-counting caveat
at the top of this file before treating it as skippable)

[Adversarial Search Algorithms](https://www.geeksforgeeks.org/artificial-intelligence/adversarial-search-algorithms/)
· [Exact Inference in Bayesian Networks](https://www.geeksforgeeks.org/artificial-intelligence/exact-inference-in-bayesian-networks/)
· [Approximate Inference in Bayesian Networks](https://www.geeksforgeeks.org/artificial-intelligence/approximate-inference-in-bayesian-networks/)

---

## Recommended completion order

1. **Tier 1** — Probability & Statistics → Databases
2. **Tier 2** — Programming & Data Structures → Discrete Mathematics → Machine Learning →
   Linear Algebra
3. **Tier 3** — Algorithms → Calculus → Artificial Intelligence — but don't actually leave AI
   for last given the under-counting caveat; treat it as at least Tier-2 priority in practice
4. Once every link above is done, fall back to the full, unfiltered §13/§14 lists in
   `topics/gfg-gate-topic-map.md`
