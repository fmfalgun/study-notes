"""Normal distribution: PDF, CDF, and closed-form MLE fitting — no scipy in this file.

See ../../doc/steps-proone.md Tier 4 for the underlying theory, and Tier 5 for why the MLE
formulas below are what they are (not just "the obvious formula").
"""

import math


def pdf(x: float, mu: float, sigma: float) -> float:
    """f(x) = 1/(sigma*sqrt(2*pi)) * exp(-(x-mu)^2 / (2*sigma^2))."""
    coefficient = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
    exponent = -((x - mu) ** 2) / (2.0 * sigma ** 2)
    return coefficient * math.exp(exponent)


def cdf(x: float, mu: float, sigma: float) -> float:
    """CDF via the standard-normal error function: Phi(z) = (1 + erf(z/sqrt(2))) / 2.

    math.erf is stdlib (no scipy needed) — this is the standard closed-form CDF for a Normal,
    not an approximation.
    """
    z = (x - mu) / (sigma * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


def fit(data: list[float]) -> dict[str, float]:
    """MLE for (mu, sigma): mu_hat = sample mean, sigma_hat^2 = *biased* variance (1/n, not
    1/(n-1)). The 1/n form is what maximizing the likelihood actually derives to — the 1/(n-1)
    "unbiased" version is a separate, different estimator, not what we want here.
    """
    n = len(data)
    mu_hat = sum(data) / n
    variance_hat = sum((x - mu_hat) ** 2 for x in data) / n
    return {"mu": mu_hat, "sigma": math.sqrt(variance_hat)}
