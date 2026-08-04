# Reading Steps — Distribution-Fitting Toolkit (ProOne)

`plan.md`'s reference link ([Probability Distribution](https://www.geeksforgeeks.org/maths/probability-distribution/))
is a hub/index page, not an article — it doesn't itself contain any PDF/PMF/CDF formulas or MLE
content. This doc goes through that page's actual links, plus a separate search for Maximum
Likelihood Estimation (which the hub page doesn't cover at all), and orders everything into a
reading path assuming **zero prior knowledge** of probability distributions or MLE — same approach
as `../../../../subjects/math-crossover-analysis.md` and the tiering used in `../../../../tracks/gate/topics/gfg-gate-topic-map.md` /
`../../../../tracks/isro/topics/gfg-isro-topic-map.md`.

Only links that actually feed the toolkit's scope (Normal, Binomial, Poisson — PDF/PMF, CDF, MLE
`fit`) are placed in the required tiers. Everything else on the hub page is listed at the bottom as
skippable, with the reason it doesn't apply here.

## Tier 1 — Foundations (read first, in this order)

Needed before any of the three distributions make sense — what a random variable is, and what
PDF/PMF/CDF even mean.

1. [Introduction to Probability Distribution](https://www.geeksforgeeks.org/maths/introduction-to-probability-distribution/)
2. [Random Variable](https://www.geeksforgeeks.org/engineering-mathematics/random-variable/)
3. [Discrete Random Variable](https://www.geeksforgeeks.org/maths/discrete-random-variable/)
4. [Probability Distribution Function](https://www.geeksforgeeks.org/maths/probability-distribution-function/)
5. [Probability Mass Function (PMF)](https://www.geeksforgeeks.org/maths/probability-mass-function/) — this *is* the `pmf()` we implement for Binomial/Poisson
6. [Probability Density Function (PDF)](https://www.geeksforgeeks.org/maths/probability-density-function-meaning-formula-and-graph/) — this *is* the `pdf()` we implement for Normal
7. [Expected Value and Variance](https://www.geeksforgeeks.org/maths/expected-value-and-variance/) — the μ/σ² and λ our `fit()` functions estimate are just this

## Tier 2 — Binomial (needed for `distributions/binomial.py`)

8. [Discrete Probability Distribution](https://www.geeksforgeeks.org/maths/discrete-probability-distribution/) — general framing before the specific discrete distributions
9. [Bernoulli Trials and Binomial Distribution](https://www.geeksforgeeks.org/maths/bernoulli-trials-binomial-distribution/)
10. [Binomial Distribution](https://www.geeksforgeeks.org/maths/binomial-distribution/) — the PMF/CDF formulas to implement
11. [Binomial Mean and Standard Deviation](https://www.geeksforgeeks.org/maths/binomial-mean-and-standard-deviation-probability-class-12-maths/) — where p̂ = mean/n (our MLE) comes from
12. [Variance of Binomial Distribution](https://www.geeksforgeeks.org/maths/variance-of-binomial-distribution/)

## Tier 3 — Poisson (needed for `distributions/poisson.py`)

13. [Poisson Distribution](https://www.geeksforgeeks.org/maths/poisson-distribution/) — PMF/CDF formulas, and where λ̂ = sample mean (our MLE) comes from
14. [Binomial vs Poisson Distribution](https://www.geeksforgeeks.org/maths/difference-between-binomial-and-poisson-distribution/) — useful once both are read, ties the two together (when Poisson approximates Binomial)

## Tier 4 — Normal (needed for `distributions/normal.py`)

15. [Continuous Probability Distributions](https://www.geeksforgeeks.org/maths/continuous-probability-distributions/) — general framing before Normal specifically
16. [Normal Distribution](https://www.geeksforgeeks.org/maths/normal-distribution/) — the PDF/CDF formulas to implement
17. [Standard Normal Distribution](https://www.geeksforgeeks.org/maths/standard-normal-distribution/)
18. [Z-Score Table](https://www.geeksforgeeks.org/maths/z-score-table/) — needed to sanity-check CDF values by hand while validating against SciPy
19. [How to Calculate Probability Using Mean and Variance](https://www.geeksforgeeks.org/maths/how-to-calculate-probability-in-a-normal-distribution-given-the-mean-and-variance/)
20. [How to Find Probability Between Two Z-Scores](https://www.geeksforgeeks.org/maths/how-to-find-probability-between-two-z-scores/)

## Tier 5 — Maximum Likelihood Estimation (needed for every `fit()` — not on the hub page at all)

The reference link's hub page has no MLE content whatsoever, so these came from a separate search.
This is the actual math behind why μ̂ = mean, λ̂ = mean, p̂ = mean/n are *the* MLEs, not just
"the obvious formula":

21. [Likelihood Function](https://www.geeksforgeeks.org/data-science/likelihood-function/)
22. [Log Likelihood](https://www.geeksforgeeks.org/data-science/log-likelihood/) — why we maximize log-likelihood instead of likelihood directly
23. [Probability Density Estimation & Maximum Likelihood Estimation](https://www.geeksforgeeks.org/machine-learning/probability-density-estimation-maximum-likelihood-estimation/) — the general MLE procedure
24. [Maximum Likelihood Estimation of Gaussian Parameters](https://www.geeksforgeeks.org/machine-learning/maximum-likelihood-estimation-of-gaussian-parameters/) — the actual derivation of Normal's μ̂/σ̂², worked example to check your own derivation against

## Tier 6 — Why real telemetry is a different beast than synthetic data (needed once live deployment starts)

Every MLE formula in Tier 2–5 assumes the sample is i.i.d. — independent, identically distributed
draws from one fixed distribution. Synthetic ground-truth batches satisfy this by construction; real
system telemetry (CPU%, event counts, etc.) usually doesn't — it drifts over time and consecutive
samples are autocorrelated (high CPU now makes high CPU a second later more likely). This is *why*
`scope.md`'s live-deployment test criterion checks against a *rolling* self-baseline instead of a
single fixed ground truth — the underlying distribution is allowed to drift.

25. [Stochastic Process](https://www.geeksforgeeks.org/engineering-mathematics/stochastic-process/) — the general framing telemetry actually fits, vs. the fixed-distribution assumption used so far
26. [How to Check if Time Series Data is Stationary with Python?](https://www.geeksforgeeks.org/python/how-to-check-if-time-series-data-is-stationary-with-python/) — practical check for whether a telemetry stream still behaves close enough to i.i.d. for the existing `fit()` code to be meaningful

## Skip for now (on the hub page, but out of scope for this toolkit)

- [Geometric Distribution](https://www.geeksforgeeks.org/maths/geometric-distribution/) / [Geometric Distribution Formula](https://www.geeksforgeeks.org/maths/geometric-distribution-formula/) — toolkit doesn't implement Geometric
- [Uniform Distribution Formula](https://www.geeksforgeeks.org/maths/uniform-distribution-formula/) — not implemented
- [Normal vs Non-Normal Distribution](https://www.geeksforgeeks.org/maths/normal-vs-non-normal-distribution/), [Coefficient of Skewness](https://www.geeksforgeeks.org/maths/coefficient-of-skewness/), [Positively](https://www.geeksforgeeks.org/maths/positively-skewed-distribution/)/[Negatively Skewed](https://www.geeksforgeeks.org/maths/negatively-skewed-distribution/) — descriptive-stats detail not needed to implement PDF/CDF/MLE
- [Continuous vs Discrete Uniform Distribution](https://www.geeksforgeeks.org/maths/difference-between-continuous-and-discrete-uniform-distribution/) — Uniform isn't in scope
- [Point Estimation](https://www.geeksforgeeks.org/maths/point-estimation/) — broader context around MLE, nice-to-have but not required to implement the three `fit()`s
- Practice-problem sets ([Random Variables](https://www.geeksforgeeks.org/maths/random-variables-practice-problems/), [Binomial](https://www.geeksforgeeks.org/maths/binomial-distribution-practice-problems/), [Poisson](https://www.geeksforgeeks.org/maths/poisson-distribution-practice-problems/)) and [Last Minute Notes](https://www.geeksforgeeks.org/maths/last-minute-notes-lmns-probability-and-statistics/) — revision material, come back to these after implementation if you want extra confidence, not required to start
