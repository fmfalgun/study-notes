# Execution Roadmap — Distribution-Fitting Toolkit (ProOne)

The step-by-step build order for `proone/plan.md`, scoped by `proone/scope.md`. Read
`steps-proone.md` first if you haven't touched the underlying math yet — this doc assumes that
reading is done and focuses on what to actually build, in order.

## 0. Real-time telemetry source — decided

Live deployment (`../proone/scope.md` § Input) needed a real data source per distribution instead
of synthetic batches. Decided in favor of **stdlib-only, direct `/proc` reads** (implemented in
`proone/script/telemetry_source.py`) over `psutil`, specifically because ProOne's installed
packages were unverified at the time (`../../proone-utilities.md` was still a stub) — reading
`/proc` directly needs nothing installed at all, which was the whole point of making this resilient
to "just transfer the folder and run it."

| Distribution | Metric | Source |
|---|---|---|
| Normal | aggregate CPU busy % per interval | `/proc/stat`'s `cpu` line, delta between two ticks |
| Poisson | interrupt count per interval | `/proc/interrupts`, summed across all IRQs/CPUs, delta between two ticks |
| Binomial | count of busy cores per interval (n = core count) | `/proc/stat`'s `cpuN` lines, same busy/idle delta logic per core |

`psutil`, `mpstat`/`sar` remain documented as alternatives in `../../garuda-utilities.md` if a
future topic prefers them, but this topic doesn't use them.

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
- Run via `python3 ../proone/script/run_validate.py` (or `python3 run_validate.py` from inside
  `script/`) — works from any working directory, no `-m` module invocation needed

## 4. Build the API

- `POST /fit` → `{params, log_likelihood}`
- `GET /pdf`, `GET /cdf` → value
- Add request logging (timestamp, distribution, sample size, result) to a flat file

## 5. Local smoke test

- Run the service, hit each endpoint manually, confirm logging writes correctly

## 6. Deploy on the ProOne — done, `sampling_daemon.py` + `run_daemon.py`

- Transfer the `proone/script/` folder to ProOne (contains everything: `distributions/`,
  `telemetry_source.py`, `sampling_daemon.py`, `run_daemon.py`) — no install step needed, stdlib
  only.
- Start it: `python3 run_daemon.py` (default 60s interval) or `python3 run_daemon.py --interval N`.
  To survive a closed terminal: `nohup python3 run_daemon.py > /dev/null 2>&1 &`.
- Resilience is a self-restarting loop *inside* `sampling_daemon.py` — no systemd unit, per
  `../proone/scope.md` § Both phases. `kill <pid>` (SIGTERM) or Ctrl+C (SIGINT) both trigger a clean
  shutdown.
- Every 10 samples (`BASELINE_BATCH_COUNT` in `sampling_daemon.py`) forms one batch: the first batch
  becomes the baseline, every batch after that is compared against it and flagged in
  `results/anomalies.jsonl` if any parameter drifts beyond 3 SE.
- All output lives in `script/results/` — `samples.jsonl`, `baseline.json`, `anomalies.jsonl`,
  `errors.log` — inside the transferred folder itself, per `../proone/scope.md` § Output.
- Verified locally (25s run, 1s interval): baseline established after batch 1, batch 2 correctly
  flagged a real Poisson drift, clean SIGTERM shutdown, zero uncaught errors.
- Let it run 1–2 weeks, accumulating the logs above.
- **Watch it live**: `python3 run_monitor.py`, in a separate terminal, any time — polls
  `results/status.json` every 1s and renders a btop-style dashboard (curses, stdlib only). Fully
  decoupled from the daemon: attach/detach whenever, works whether the daemon is foreground or
  backgrounded, closing the monitor never affects the running daemon. Flags the daemon as `STALE`
  if `status.json` hasn't updated in 3+ intervals.

## 7. Analyze results at the end

- Correctness (validation phase only): max abs error vs SciPy, broken down by n
- Baseline stability (live-deployment phase): read `results/anomalies.jsonl` for the rate/pattern of
  flagged batches vs the 3-SE self-baseline threshold (`../proone/scope.md` § Test) — expect a
  higher-than-3-SE-implies rate early on since real telemetry isn't i.i.d.
  (`../doc/steps-proone.md` Tier 6), settling as the baseline window matures
- Performance: fit/query latency vs n (once the service layer in step 4 exists)
- Reliability: `results/errors.log` entry count and `results/samples.jsonl` gap-checking over the
  full window
- Write up findings as a new doc in `../doc/` once the deployment window closes
- Phase 2 (deferred, not this iteration): revisit validating the math against real data directly
