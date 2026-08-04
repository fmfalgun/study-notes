"""Binomial distribution: PMF, CDF, and closed-form MLE fitting — no scipy in this file.

See ../../doc/steps-proone.md Tier 2 for the underlying theory.
"""

import math


def pmf(k: int, n: int, p: float) -> float:
    """P(X=k) = C(n,k) * p^k * (1-p)^(n-k). math.comb is exact-integer (stdlib), no
    factorial-overflow risk the way a naive n!/(k!(n-k)!) implementation would have for large n.
    """
    return math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))


def cdf(k: int, n: int, p: float) -> float:
    """P(X<=k) = sum of the PMF from 0 to k. No closed form shorter than this sum exists for
    Binomial CDF in general (it's expressible via the regularized incomplete beta function, but
    that's scipy's job, not ours — direct summation is the from-scratch equivalent).
    """
    return sum(pmf(i, n, p) for i in range(0, k + 1))


def fit(data: list[int], n: int) -> dict[str, float]:
    """MLE for p, given each element of `data` is the observed success count from one Binomial(n,p)
    trial-block. p_hat = (total successes) / (n * number of blocks) — the sample proportion of
    successes across every coin-flip actually observed, which is exactly what maximizing the
    Binomial likelihood reduces to.
    """
    total_successes = sum(data)
    total_trials = n * len(data)
    return {"p": total_successes / total_trials}
