# Execution Roadmap — Distribution-Fitting Toolkit (ProOne)

The step-by-step build order for `proone/plan.md`, scoped by `proone/scope.md`. Read
`steps-proone.md` first if you haven't touched the underlying math yet — this doc assumes that
reading is done and focuses on what to actually build, in order.

## 0. Decide the real-time telemetry source (pending brainstorm)

Live deployment (`../proone/scope.md` § Input) needs a real data source per distribution instead of
synthetic batches. Candidates, checked so far only on `garuda` (see `../../garuda-utilities.md` for
full detail — `proone` itself still needs its own check via `../../proone-utilities.md`'s
verification command before picking a final source there):

| Distribution | Candidate metric | Candidate source | Confirmed on garuda? |
|---|---|---|---|
| Normal | CPU%, memory%, network throughput, temperature | `psutil` (cpu_percent, virtual_memory, net_io_counters) or raw `/proc/stat`, `/proc/meminfo`, `/proc/net/dev` | yes (`psutil` v7.2.2 present) |
| Poisson | process spawns/sec, interrupts/sec, packets/sec | `/proc/interrupts` deltas, `psutil.pids()` count deltas, or `journalctl` event counts (e.g. auth failures) | yes (`/proc/interrupts`, `journalctl` present) |
| Binomial | per-core busy/idle at a sampled instant (n cores = n trials) | `psutil.cpu_percent(percpu=True)` thresholded, or raw per-cpu lines in `/proc/stat` | yes (`psutil` present) |

Not yet decided: exact metric per distribution, and the install-vs-skip call on `mpstat`/`sar`
(`sysstat` package, missing on garuda, would give per-core breakdown without `psutil`). Brainstorm
and lock this in before step 1's `script/service/api.py` needs a concrete source to call.

## 1. Scaffold the code layout

Creates `proone/script/` for the first time, per the on-demand convention in `../../README.md`.

- `script/distributions/normal.py`, `binomial.py`, `poisson.py` — each exposing `pdf`/`pmf`, `cdf`,
  `fit(data) -> params`
- `script/distributions/validate.py` — grid-based comparison against
  `scipy.stats.norm`/`binom`/`poisson`
- `script/service/api.py` — the HTTP API

## 2. Implement the three distributions

- Normal: closed-form `pdf`/`cdf`, MLE `fit` (μ̂ = mean, σ̂² = biased variance, 1/n)
- Binomial: closed-form `pmf`/`cdf`, MLE `fit` (p̂ = successes / (n × trials))
- Poisson: closed-form `pmf`/`cdf`, MLE `fit` (λ̂ = mean)

## 3. Validate against SciPy

- PDF/CDF value comparison on a point grid, tolerance ~`1e-9`
- Fitted-parameter recovery on synthetic data from known ground truth, looser tolerance for small n
- This must pass before moving to the service layer

## 4. Build the API

- `POST /fit` → `{params, log_likelihood}`
- `GET /pdf`, `GET /cdf` → value
- Add request logging (timestamp, distribution, sample size, result) to a flat file

## 5. Local smoke test

- Run the service, hit each endpoint manually, confirm logging writes correctly

## 6. Deploy on the ProOne

- Run as an always-on local process (systemd user service or equivalent — not yet decided, pick
  when we get here)
- Feed it the real telemetry source decided in step 0, at a sampling interval the service reads as a
  runtime-configurable option (env var / CLI flag / config value) — not hardcoded, per
  `../proone/scope.md` § Input.
- Let it run 1–2 weeks, accumulating the request log

## 7. Analyze results at the end

- Correctness (validation phase only): max abs error vs SciPy, broken down by n
- Baseline stability (live-deployment phase): rate of out-of-band fits vs the 3-SE self-baseline
  threshold (`../proone/scope.md` § Test)
- Performance: fit/query latency vs n
- Reliability: uptime, crashes, log completeness
- Write up findings as a new doc in `../doc/` once the deployment window closes
- Phase 2 (deferred, not this iteration): revisit validating the math against real data directly
