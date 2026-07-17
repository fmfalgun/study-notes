"""Resilient telemetry-sampling daemon.

Every `interval` seconds: samples real /proc-based telemetry, accumulates it into batches, fits
Normal/Poisson/Binomial to each completed batch, and flags any batch whose fitted parameter
drifts more than SE_MULTIPLE standard errors from the established baseline — see ../scope.md
§ Test (live-deployment phase) for why the threshold is a standard-error multiple rather than a
flat number, and ../../doc/roadmap-proone.md Step 0 for why these particular /proc sources map
to these particular distributions (CPU busy% -> Normal, interrupts/interval -> Poisson, per-core
busy count -> Binomial).

Resilience: every iteration's work is wrapped in try/except so one bad reading, a transient
/proc read failure, or any other single-iteration error never kills the process — it's logged to
errors.log and the loop continues. This is the entire reason this file exists separately from a
plain script: the loop body assumes it WILL occasionally fail and is built to keep going anyway.

Live view: this process only ever writes files, never a live display (it's meant to run
detached, e.g. under nohup, with no terminal to draw to). status.json is overwritten atomically
every tick specifically so a separate, decoupled run_monitor.py can poll it and render a live
dashboard whenever you want to attach one — see that file.
"""

import json
import math
import os
import signal
import time
import traceback
from pathlib import Path

from distributions import binomial, normal, poisson
from telemetry_source import busy_fraction, read_cpu_lines, read_interrupts_total

# All results live inside this file's own directory, not wherever the process happens to be
# launched from — this is what makes "transfer the folder, run it" produce results in that same
# folder regardless of cwd.
RESULTS_DIR = Path(__file__).parent / "results"
SAMPLES_LOG = RESULTS_DIR / "samples.jsonl"
ANOMALIES_LOG = RESULTS_DIR / "anomalies.jsonl"
ERRORS_LOG = RESULTS_DIR / "errors.log"
BASELINE_FILE = RESULTS_DIR / "baseline.json"
STATUS_FILE = RESULTS_DIR / "status.json"

DEFAULT_INTERVAL_SECONDS = 60
BASELINE_BATCH_COUNT = 10  # samples per batch — both the baseline batch and every batch after it
SE_MULTIPLE = 3  # see ../scope.md § Test


class Sampler:
    """Holds the previous /proc snapshot so each tick can compute a delta against it."""

    def __init__(self) -> None:
        self.prev_cpu_lines: dict[str, list[int]] | None = None
        self.prev_interrupts: int | None = None

    def sample(self) -> dict | None:
        """Return one tick's readings, or None on the very first call — there's no previous
        snapshot yet to delta against, so the first tick only warms up the sampler.
        """
        cpu_lines = read_cpu_lines()
        interrupts_total = read_interrupts_total()

        if self.prev_cpu_lines is None:
            self.prev_cpu_lines, self.prev_interrupts = cpu_lines, interrupts_total
            return None

        aggregate_busy_pct = busy_fraction(self.prev_cpu_lines["cpu"], cpu_lines["cpu"]) * 100.0

        core_keys = sorted(k for k in cpu_lines if k != "cpu")
        busy_cores = sum(
            1 for k in core_keys
            if busy_fraction(self.prev_cpu_lines[k], cpu_lines[k]) > 0.5
        )

        interrupts_delta = interrupts_total - self.prev_interrupts

        self.prev_cpu_lines, self.prev_interrupts = cpu_lines, interrupts_total

        return {
            "timestamp": time.time(),
            "cpu_busy_pct": aggregate_busy_pct,
            "busy_cores": busy_cores,
            "n_cores": len(core_keys),
            "interrupts_delta": interrupts_delta,
        }


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(record) + "\n")


def write_status(status: dict) -> None:
    """Atomic write (write-then-rename) so run_monitor.py never reads a half-written file —
    os.replace is atomic on POSIX, unlike a plain write to STATUS_FILE directly.
    """
    tmp_path = STATUS_FILE.with_name(STATUS_FILE.name + ".tmp")
    tmp_path.write_text(json.dumps(status))
    os.replace(tmp_path, STATUS_FILE)


def fit_batch(samples: list[dict]) -> dict:
    """Fit all three distributions on one batch of samples."""
    cpu_values = [s["cpu_busy_pct"] for s in samples]
    interrupt_values = [s["interrupts_delta"] for s in samples]
    busy_core_values = [s["busy_cores"] for s in samples]
    n_cores = samples[0]["n_cores"]

    return {
        "normal": normal.fit(cpu_values),
        "poisson": poisson.fit(interrupt_values),
        "binomial": binomial.fit(busy_core_values, n_cores),
        "n_cores": n_cores,
        "batch_size": len(samples),
    }


def standard_errors(fit: dict) -> dict:
    """Theoretical standard error of each fitted parameter at this batch size — see
    ../doc/steps-proone.md Tier 5/6 for why these are the right formulas to use here.
    """
    n = fit["batch_size"]
    normal_se = fit["normal"]["sigma"] / math.sqrt(n)
    poisson_se = math.sqrt(fit["poisson"]["lam"] / n)
    p = fit["binomial"]["p"]
    total_trials = fit["n_cores"] * n
    binomial_se = math.sqrt(p * (1 - p) / total_trials) if 0 < p < 1 else 0.0
    return {"normal": normal_se, "poisson": poisson_se, "binomial": binomial_se}


def check_drift(baseline_fit: dict, batch_fit: dict, batch_se: dict) -> list[str]:
    """Which fitted parameters (if any) drifted beyond SE_MULTIPLE standard errors from the
    baseline. Empty list means everything's stable.
    """
    drifted = []
    if abs(batch_fit["normal"]["mu"] - baseline_fit["normal"]["mu"]) > SE_MULTIPLE * batch_se["normal"]:
        drifted.append("normal")
    if abs(batch_fit["poisson"]["lam"] - baseline_fit["poisson"]["lam"]) > SE_MULTIPLE * batch_se["poisson"]:
        drifted.append("poisson")
    if abs(batch_fit["binomial"]["p"] - baseline_fit["binomial"]["p"]) > SE_MULTIPLE * batch_se["binomial"]:
        drifted.append("binomial")
    return drifted


def log_error(context: str, exc: BaseException) -> None:
    with ERRORS_LOG.open("a") as f:
        f.write(f"{time.time()} [{context}] {exc!r}\n{traceback.format_exc()}\n")


_shutdown_requested = False


def _handle_signal(signum, frame) -> None:
    global _shutdown_requested
    _shutdown_requested = True


def run(interval_seconds: float) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    sampler = Sampler()
    current_batch: list[dict] = []
    baseline_fit = json.loads(BASELINE_FILE.read_text()) if BASELINE_FILE.exists() else None

    started_at = time.time()
    counters = {"total_samples": 0, "total_batches": 0, "total_anomalies": 0, "total_errors": 0}
    last_sample: dict | None = None
    last_batch_fit: dict | None = None
    last_drift: list[str] | None = None

    print(f"Starting telemetry daemon: interval={interval_seconds}s, results -> {RESULTS_DIR}")

    while not _shutdown_requested:
        try:
            record = sampler.sample()
            if record is not None:
                counters["total_samples"] += 1
                last_sample = record
                append_jsonl(SAMPLES_LOG, record)
                current_batch.append(record)

                if len(current_batch) >= BASELINE_BATCH_COUNT:
                    counters["total_batches"] += 1
                    batch_fit = fit_batch(current_batch)
                    last_batch_fit = batch_fit
                    if baseline_fit is None:
                        baseline_fit = batch_fit
                        BASELINE_FILE.write_text(json.dumps(baseline_fit))
                        last_drift = []
                    else:
                        batch_se = standard_errors(batch_fit)
                        drifted = check_drift(baseline_fit, batch_fit, batch_se)
                        last_drift = drifted
                        if drifted:
                            counters["total_anomalies"] += 1
                            append_jsonl(ANOMALIES_LOG, {
                                "timestamp": time.time(),
                                "drifted_metrics": drifted,
                                "batch_fit": batch_fit,
                                "baseline_fit": baseline_fit,
                            })
                    current_batch = []
        except Exception as exc:  # the resilience boundary — must never propagate out of the loop
            counters["total_errors"] += 1
            log_error("sample_loop", exc)

        # Written every tick (not just every batch) so a monitor polling this file always has
        # fresh liveness info, even between batch completions.
        write_status({
            "pid": os.getpid(),
            "started_at": started_at,
            "last_tick_at": time.time(),
            "interval_seconds": interval_seconds,
            "batch_size": BASELINE_BATCH_COUNT,
            "batch_progress": len(current_batch),
            "counters": counters,
            "last_sample": last_sample,
            "baseline_fit": baseline_fit,
            "last_batch_fit": last_batch_fit,
            "last_drift": last_drift,
        })

        # Sleep in 1s slices so a shutdown signal is noticed promptly even with a long interval,
        # instead of blocking for the full interval on a single time.sleep() call.
        for _ in range(int(interval_seconds)):
            if _shutdown_requested:
                break
            time.sleep(1)

    print("Shutdown requested, exiting cleanly.")


if __name__ == "__main__":
    run(DEFAULT_INTERVAL_SECONDS)
