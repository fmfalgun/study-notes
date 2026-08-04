"""Poisson distribution: PMF, CDF, and closed-form MLE fitting — no scipy in this file.

See ../../doc/steps-proone.md Tier 3 for the underlying theory.
"""

import math


def pmf(k: int, lam: float) -> float:
    """P(X=k) = exp(-lambda) * lambda^k / k!."""
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def cdf(k: int, lam: float) -> float:
    """P(X<=k) = sum of the PMF from 0 to k — same reasoning as binomial.cdf: no shorter
    closed form belongs in from-scratch code (the real one routes through the incomplete gamma
    function, which is scipy's job).
    """
    return sum(pmf(i, lam) for i in range(0, k + 1))


def fit(data: list[int]) -> dict[str, float]:
    """MLE for lambda: lambda_hat = sample mean. For Poisson, the mean and the rate parameter
    are the same quantity, so this is both "the obvious estimator" and the actual MLE — no
    coincidence, it falls straight out of setting d/d(lambda) of the log-likelihood to zero.
    """
    lam_hat = sum(data) / len(data)
    return {"lam": lam_hat}
