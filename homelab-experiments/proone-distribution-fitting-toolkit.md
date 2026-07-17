# Task Plan: Distribution-Fitting Toolkit

**Machine**: HP ProOne 440 G9 (i7-14700, 28 threads @ 5.4GHz, 16GB RAM, no dGPU, always-on desktop)
**Category**: Mathematics (Probability, Statistics & Linear Algebra — ML foundations)
**Reference**: [Probability Distribution](https://www.geeksforgeeks.org/maths/probability-distribution/) (GFG index — points to the individual Normal/Binomial/Poisson articles for formulas)

## What we're building

A small Python library + long-running local service that:

1. Implements PDF/PMF and CDF from scratch (no `scipy.stats` in the compute path) for three
   distributions: **Normal**, **Binomial**, **Poisson**.
2. Implements MLE-based parameter fitting from scratch for each — all three have closed-form MLEs,
   so this is direct estimator code, not numerical optimization:
   - Normal: μ̂ = sample mean, σ̂² = biased sample variance (1/n, matching MLE derivation, not 1/(n-1))
   - Binomial (n fixed/known): p̂ = (sum of successes) / (n × num_trials_observed)
   - Poisson: λ̂ = sample mean
3. Validates every PDF/CDF value and every fitted parameter against `scipy.stats` (`norm`, `binom`,
   `poisson`) on the same inputs, with a tolerance check.
4. Exposes fitting/querying over a minimal local HTTP API so other experiments on this machine (e.g.
   a future Bayesian/Naive-Bayes classifier, or K-Means convergence logging) can call it instead of
   reimplementing distribution math.

## Why

This is foundational math for everything else planned in `proone-dsai.md`'s AI/ML sections (Naive
Bayes, PCA, clustering all lean on distributional assumptions or MLE-style estimation). Building it
from scratch and validating against SciPy is the point — the deliverable is *understanding*, not a
wrapper around SciPy. Framing it as a small persistent service (rather than a one-off script) matches
ProOne's role per `README.md`/`proone-dsai.md`: it's the always-on machine best suited to run as a
continuous service other tasks can depend on.

## Hardware scoping

Closed-form MLE for these three distributions is O(n) over the sample — trivial compute, no need for
the ProOne's 28 threads for the math itself. The hardware fit here is about **uptime and concurrency
of the service**, not raw throughput:

- Run the API as a lightweight always-on local process (no GPU needed, matches this file's scope).
- Use the thread/process headroom only if concurrent fit requests from multiple other experiments
  need to be served without blocking each other (a simple thread pool is enough; do not over-engineer
  parallelism for O(n) closed-form math).
- 16GB RAM is far more than the toolkit needs (largest samples will be synthetic datasets in the
  low-to-mid millions of points at most) — no memory-tiering or streaming-fit logic is warranted.

## Implementation plan

- `distributions/normal.py`, `binomial.py`, `poisson.py` — each with `pdf`/`pmf`, `cdf`, and `fit(data) -> params`.
- `distributions/validate.py` — property-based-style checks against `scipy.stats` equivalents:
  compare PDF/CDF at a grid of points, compare fitted params on synthetic data drawn from known
  ground-truth parameters, assert error below a tolerance (e.g. `1e-9` for closed-form PDF/CDF,
  looser for MLE recovery on small-n samples where estimator variance itself is the source of error,
  not a bug).
- `service/api.py` — minimal HTTP API (stdlib `http.server` or a very small framework):
  - `POST /fit` — `{distribution, data[]}` → `{params, log_likelihood}`
  - `GET /pdf`, `GET /cdf` — `{distribution, params, x}` → value
  - No auth/multi-tenant concerns — this is a localhost-only service for the user's own experiments.
- Logging: every fit/query request logged with timestamp, distribution, sample size, and result, to a
  flat file — this log is the raw material for the end-of-run analysis.

## Deployment

Run the service continuously on the ProOne for **1–2 weeks**. During that window:
- Feed it synthetic batches (known ground-truth Normal/Binomial/Poisson samples at varying sample
  sizes: n = 10, 100, 1000, 10000, 100000) on a daily cron-style loop to build up a log of
  fit-accuracy-vs-n over time, rather than a single one-shot validation run.
- If/when another experiment on this machine needs distribution fitting, point it at this service
  instead of reimplementing — that's the intended integration point.

## What gets analyzed at the end

- **Correctness**: max absolute error between from-scratch and SciPy PDF/CDF values; max absolute
  parameter error between fitted and ground-truth params, broken down by sample size, to show
  estimator variance shrinking as n grows (the expected MLE consistency result).
- **Performance**: fit/query latency vs sample size, to confirm the O(n) closed-form implementation
  scales linearly and the service stays responsive under the logged request load.
- **Service reliability**: uptime over the 1–2 week deployment, any crashes/restarts, request log
  completeness.
- Write-up appended to this file (or a `results/` subsection) summarizing the above once the
  deployment window closes.
