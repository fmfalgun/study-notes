# Scope — Distribution-Fitting Toolkit (ProOne)

Boundary only — see `plan.md` for the full narrative (what's built, why, hardware fit,
implementation sketch, deployment, analysis). Nothing below restates anything from there.

## In scope

- Exactly three distributions: **Normal, Binomial, Poisson** — PDF/PMF, CDF, and closed-form MLE
  `fit()` for each (see `plan.md` § What we're building).
- Validation of all of the above against `scipy.stats` (see `plan.md` § Implementation plan).
- A minimal localhost-only HTTP API wrapping the fitting/querying (see `plan.md` § Implementation
  plan).

## Explicitly out of scope

- No numerical/iterative optimization — all three MLEs are closed-form.
- No distributions beyond Normal/Binomial/Poisson (no Geometric, no Uniform, etc.).
- No GPU, no other machines involved — see `plan.md` § Hardware scoping for why ProOne specifically.
- No authentication or production-hardening on the API — localhost-only, single user.
- **Phase 2, deferred**: validating the distribution math directly against real-world data (with no
  known ground truth to check against) is a future iteration, not built in this one.

## Input

- `POST /fit` — `{distribution: "normal" | "binomial" | "poisson", data: number[]}`
- `GET /pdf`, `GET /cdf` — `{distribution, params, x}`
- **Validation-phase input** (unchanged, Phase 1): synthetic data only, drawn in-process from known
  ground-truth parameters. Sample sizes: n ∈ {10, 100, 1000, 10000, 100000}, swept across all three
  distributions.
- **Live-deployment input** (Phase 1, real data): real system telemetry — exact metric-to-source
  mapping pending brainstorm (see `../doc/roadmap-proone.md`; candidate sources in
  `../../garuda-utilities.md`). Sampling interval is decided dynamically by the service/script at
  runtime, not fixed in advance.

## Output

- `POST /fit` → `{params: {...}, log_likelihood: number}`
- `GET /pdf`, `GET /cdf` → `{value: number}`
- Per-request line in the flat-file log: timestamp, distribution, sample size, result.
- End of the deployment window: a results write-up (see `plan.md` § What gets analyzed at the end).

## Database / dataset

**No persistent database, either phase.** Validation (Phase 1) generates every sample in-process
from known ground-truth parameters — no external dataset. Live deployment (Phase 1, real data) reads
real-time system telemetry directly from the OS at sample time — nothing is ingested from a stored
dataset there either. The only durable artifact in both cases is the flat-file request log.

## Timespan

- Build phase (scaffold → validate against SciPy → smoke test): no fixed duration, gated on tests
  passing, not on a calendar date.
- Deployment/running phase: **1–2 weeks continuous**, sampling real telemetry at a dynamically
  configured interval — no longer a fixed daily batch (see `plan.md` § Deployment).

## Test / pass-threshold for the script's output

**Validation phase (Phase 1, synthetic — has a known ground truth to check against):**

- **PDF/CDF correctness** (closed-form, exact formulas — no approximation involved): max absolute
  error vs the matching `scipy.stats` function must be **≤ 1e-9** at every point on the validation
  grid. Any larger gap is a bug, not expected numerical noise.
- **MLE parameter recovery** (this *is* expected to have noise — it's a statistical estimate from a
  finite sample, not a deterministic formula check): fitted parameter must fall within **3 asymptotic
  standard errors** of the true parameter, where the standard error is the theoretical one for that
  estimator at that sample size (e.g. σ/√n for the Normal mean, √(p(1-p)/n) for Binomial p̂, √(λ/n)
  for Poisson λ̂). This ties the pass/fail bound to statistical theory instead of an arbitrary flat
  tolerance, and is expected to still occasionally fail by chance (~0.3% of runs under the 3-SE bound)
  — a single failure isn't a bug, a *systematic* one across many runs at the same n is.

**Live-deployment phase (Phase 1, real telemetry — no ground truth exists to check against):**

- **Baseline stability**: the fitted parameter from each new telemetry batch must fall within 3 of
  *its own rolling baseline's* standard errors — same statistical logic as above, but checked
  against the toolkit's own prior estimate instead of an external known truth, since none exists for
  real data. A systematic run of out-of-band fits signals either a real anomaly in the telemetry or a
  fitting bug — distinguishing the two is a Phase 2 concern (see § Explicitly out of scope).

**Both phases:**

- **Service reliability**: zero unplanned restarts and zero gaps in the request log over the full
  1–2 week deployment window count as passing; any crash or log gap gets investigated, not silently
  waived.
