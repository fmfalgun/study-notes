"""Validation harness: checks the from-scratch normal/binomial/poisson code against scipy.stats.

This is the ONLY file in this package allowed to import scipy — it's the answer key, never part
of the shipped compute path (see ../../plan.md § Implementation plan and ../../scope.md § In scope).

Two separate checks, matching ../../scope.md's Test section:
  1. PDF/PMF/CDF correctness — exact formulas, so scipy agreement should be near machine precision.
  2. MLE parameter recovery — a statistical estimate from a finite sample, so agreement is only
     expected within the estimator's own theoretical standard error, not exactly.
"""

import math

import numpy as np
from scipy import stats

from distributions import binomial, normal, poisson

# Tolerance for check 1 — see ../../scope.md § Test: "any larger gap is a bug, not expected
# numerical noise", because these are exact closed-form formulas, not approximations.
PDF_CDF_TOLERANCE = 1e-9

# How many standard errors away from the true parameter still counts as "recovered" for check 2.
# See ../../scope.md § Test for why this is derived from theory (asymptotic normality of the MLE)
# instead of being an arbitrary flat number.
MLE_RECOVERY_SE_MULTIPLE = 3

# Sample sizes swept during MLE recovery checks — matches ../../plan.md § Deployment's n values.
SAMPLE_SIZES = [10, 100, 1_000, 10_000, 100_000]

# Repeats per sample size for the recovery check. A single run is expected to occasionally land
# outside the 3-SE band by chance (~0.3% of the time under a correct implementation) — repeating
# and looking at the *pass rate* is what actually distinguishes "unlucky sample" from "bug",
# rather than treating one failure as damning or one pass as proof.
RECOVERY_TRIALS_PER_N = 200


def check_pdf_cdf() -> None:
    """Grid-compare from-scratch pdf/pmf/cdf against scipy.stats over a range of parameters."""
    max_diff = 0.0

    # Normal: sweep a few (mu, sigma) pairs and x values.
    for mu in (-5.0, 0.0, 5.0):
        for sigma in (0.5, 1.0, 3.0):
            for x in np.linspace(mu - 4 * sigma, mu + 4 * sigma, 25):
                x = float(x)
                max_diff = max(max_diff, abs(normal.pdf(x, mu, sigma) - stats.norm.pdf(x, mu, sigma)))
                max_diff = max(max_diff, abs(normal.cdf(x, mu, sigma) - stats.norm.cdf(x, mu, sigma)))

    # Binomial: sweep a few (n, p) pairs and every k in range.
    for n in (10, 50, 100):
        for p in (0.1, 0.5, 0.9):
            for k in range(0, n + 1):
                max_diff = max(max_diff, abs(binomial.pmf(k, n, p) - stats.binom.pmf(k, n, p)))
                max_diff = max(max_diff, abs(binomial.cdf(k, n, p) - stats.binom.cdf(k, n, p)))

    # Poisson: sweep a few lambda values and k in a range wide enough to cover the mass.
    for lam in (1.0, 5.0, 20.0):
        for k in range(0, int(lam * 5) + 10):
            max_diff = max(max_diff, abs(poisson.pmf(k, lam) - stats.poisson.pmf(k, lam)))
            max_diff = max(max_diff, abs(poisson.cdf(k, lam) - stats.poisson.cdf(k, lam)))

    status = "PASS" if max_diff <= PDF_CDF_TOLERANCE else "FAIL"
    print(f"[{status}] PDF/PMF/CDF vs scipy.stats — max abs diff = {max_diff:.2e} "
          f"(tolerance {PDF_CDF_TOLERANCE:.0e})")
    if status == "FAIL":
        raise AssertionError("PDF/PMF/CDF diverged from scipy.stats beyond tolerance — this is a bug.")


def check_mle_recovery() -> None:
    """For each distribution and sample size, fit synthetic ground-truth data many times and
    report what fraction of fits land within MLE_RECOVERY_SE_MULTIPLE standard errors of the
    true parameter — the pass-rate itself is the signal, not any single trial.
    """
    rng = np.random.default_rng(seed=0)

    print("\n[MLE recovery] fraction of trials within "
          f"{MLE_RECOVERY_SE_MULTIPLE} standard errors of the true parameter:")

    # Normal: true mu=10, sigma=2. SE of mu_hat is sigma/sqrt(n) (see ../../doc/steps-proone.md
    # Tier 5 for why this is the relevant standard error for the mean estimator).
    true_mu, true_sigma = 10.0, 2.0
    for n in SAMPLE_SIZES:
        hits = 0
        for _ in range(RECOVERY_TRIALS_PER_N):
            sample = rng.normal(true_mu, true_sigma, size=n).tolist()
            mu_hat = normal.fit(sample)["mu"]
            se = true_sigma / math.sqrt(n)
            if abs(mu_hat - true_mu) <= MLE_RECOVERY_SE_MULTIPLE * se:
                hits += 1
        print(f"  normal   n={n:>7}: {hits}/{RECOVERY_TRIALS_PER_N}")

    # Binomial: true n_trials=20, p=0.3. SE of p_hat is sqrt(p(1-p) / total_trials).
    true_n_trials, true_p = 20, 0.3
    for n_blocks in SAMPLE_SIZES:
        hits = 0
        for _ in range(RECOVERY_TRIALS_PER_N):
            sample = rng.binomial(true_n_trials, true_p, size=n_blocks).tolist()
            p_hat = binomial.fit(sample, true_n_trials)["p"]
            total_trials = true_n_trials * n_blocks
            se = math.sqrt(true_p * (1 - true_p) / total_trials)
            if abs(p_hat - true_p) <= MLE_RECOVERY_SE_MULTIPLE * se:
                hits += 1
        print(f"  binomial n={n_blocks:>7}: {hits}/{RECOVERY_TRIALS_PER_N}")

    # Poisson: true lambda=7. SE of lambda_hat is sqrt(lambda / n).
    true_lam = 7.0
    for n in SAMPLE_SIZES:
        hits = 0
        for _ in range(RECOVERY_TRIALS_PER_N):
            sample = rng.poisson(true_lam, size=n).tolist()
            lam_hat = poisson.fit(sample)["lam"]
            se = math.sqrt(true_lam / n)
            if abs(lam_hat - true_lam) <= MLE_RECOVERY_SE_MULTIPLE * se:
                hits += 1
        print(f"  poisson  n={n:>7}: {hits}/{RECOVERY_TRIALS_PER_N}")

    print("\nExpect roughly 99.7% under a correct implementation — a rate far below that across "
          "many n values (not just one unlucky sample size) signals a real bug, not chance.")


if __name__ == "__main__":
    check_pdf_cdf()
    check_mle_recovery()
