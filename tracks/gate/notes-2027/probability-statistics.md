# Probability and Statistics — GATE 2027 (CS + DA)

**Syllabus basis:** CS: probability, conditional probability, Bayes, random variables, mean/median/mode/SD, uniform, normal, exponential, Poisson, binomial. DA adds: joint/marginal/conditional distributions, covariance and correlation, CLT, confidence intervals, hypothesis testing (z, t, chi-square).
Items marked **[DA]** are DA-only.
**Hbk** column: the Arihant Handbook has no Maths chapter, so it is "—".
**Links:** only GFG / Harvard URLs returned by search are used. NPTEL links are still unverified, so search "NPTEL Probability and Statistics" and add one under *My links*.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Counting, basic probability, axioms | — | [Stat 110 syllabus / lectures](https://stat110.hsites.harvard.edu/youtube) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Conditional probability, independence, Bayes | — | [LMN Prob & Stats](https://www.geeksforgeeks.org/maths/last-minute-notes-lmns-probability-and-statistics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Random variables, PMF, PDF, CDF | — | [PDF](https://www.geeksforgeeks.org/engineering-mathematics/probability-density-function/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Expectation, variance, moments, MGF | — | [MGF](https://www.geeksforgeeks.org/engineering-mathematics/moment-generating-functions/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Binomial and Poisson | — | [Poisson](https://www.geeksforgeeks.org/maths/poisson-distribution/) · [Bin vs Poisson](https://www.geeksforgeeks.org/maths/difference-between-binomial-and-poisson-distribution/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Uniform and exponential | — | [Continuous distributions](https://www.geeksforgeeks.org/maths/continuous-probability-distributions/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Normal distribution, z-scores | — | [Prob Distribution quiz](https://www.geeksforgeeks.org/quizzes/probability-distribution-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Mean, median, mode, SD, descriptive stats | — | [Variance](https://www.geeksforgeeks.org/maths/variance/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Joint distributions, covariance, correlation **[DA]** | — | [Joint PMF](https://www.geeksforgeeks.org/maths/joint-probability-mass-function/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Chebyshev, CLT **[DA]** | — | [CLT](https://www.geeksforgeeks.org/maths/central-limit-theorem/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Confidence intervals and hypothesis tests **[DA]** | — | [Statistics cheat sheet](https://www.geeksforgeeks.org/data-science/statistics-cheatsheet/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [GFG GATE DA Prob & Stats short-notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251006153002183900/Probability---Stats-GATE-DA-short-notes_compressed.pdf), [Stat 110 syllabus](https://stat110.hsites.harvard.edu/resource/syllabus) (free book: probabilitybook.net).

**My links:** (NPTEL / textbook, add here)

---

## 1–2. Probability basics
- P(A∪B) = P(A) + P(B) − P(A∩B). P(Aᶜ) = 1 − P(A).
- P(A|B) = P(A∩B)/P(B).
- Independent: P(A∩B) = P(A)P(B).
- Total probability: P(B) = Σ P(B|Aᵢ)P(Aᵢ).
- Bayes: P(Aᵢ|B) = P(B|Aᵢ)P(Aᵢ) / Σⱼ P(B|Aⱼ)P(Aⱼ).

## 3–4. Random variables
- Discrete: Σ p(x) = 1. Continuous: ∫ f(x)dx = 1 and f = dF/dx.
- E[X] = Σ x p(x), or ∫ x f(x) dx.
- Var X = E[X²] − (E[X])². Var(aX + b) = a² Var X. E[aX + b] = aE[X] + b.
- E[X + Y] = E[X] + E[Y] always. Var(X + Y) = Var X + Var Y only if independent (more generally, plus 2Cov).
- MGF: M(t) = E[e^{tX}]. The n-th moment is the n-th derivative at t = 0.

## 5–7. Distributions
| Distribution | PMF / PDF | Mean | Variance |
|---|---|---|---|
| Bernoulli(p) | pˣ(1−p)¹⁻ˣ | p | p(1−p) |
| Binomial(n,p) | C(n,k)pᵏ(1−p)ⁿ⁻ᵏ | np | np(1−p) |
| Poisson(λ) | e⁻λ λᵏ/k! | λ | λ |
| Uniform(a,b) | 1/(b−a) | (a+b)/2 | (b−a)²/12 |
| Exponential(λ) | λe^{−λx}, x ≥ 0 | 1/λ | 1/λ² |
| Normal(μ,σ²) | bell curve | μ | σ² |

- Poisson is the limit of Binomial for large n, small p, with λ = np.
- Exponential is memoryless: P(X > s+t | X > s) = P(X > t). P(X > x) = e^{−λx}.
- Normal: Z = (X − μ)/σ. About 68 / 95 / 99.7 % lie within 1 / 2 / 3 σ.
- Discrete uniform on {a..b}: mean (a+b)/2, variance ((b−a+1)² − 1)/12.

## 8. Descriptive statistics
Mean, median (middle value), mode (most frequent). Population variance divides by n, sample variance by n − 1.

## 9–11. [DA]
- Cov(X,Y) = E[XY] − E[X]E[Y]. ρ = Cov/(σₓσᵧ), with −1 ≤ ρ ≤ 1. Independent implies Cov = 0, but not the converse.
- Chebyshev: P(|X − μ| ≥ kσ) ≤ 1/k².
- CLT: X̄ ≈ N(μ, σ²/n) for large n. Standard error = σ/√n.
- z-test: z = (X̄ − μ)/(σ/√n). t-test: t = (X̄ − μ)/(s/√n). Confidence interval: X̄ ± z·σ/√n.

---

## Worked examples (all recomputed in code)

**E1: Bayes.** Prevalence 1%, sensitivity 90%, false-positive rate 5%. P(disease | positive) = 0.01·0.9 / (0.01·0.9 + 0.99·0.05) = 0.009 / 0.0585 = **0.1538**. Most positives are false positives.

**E2: Binomial.** n = 10, p = 0.3. P(X = 3) = C(10,3)(0.3)³(0.7)⁷ = **0.2668**.

**E3: Poisson.** λ = 2. P(X ≥ 1) = 1 − e⁻² = **0.8647**. P(X = 0) = 0.1353.

**E4: Exponential.** λ = 0.5. Mean = 2 and variance = 4. P(X > 3) = e^{−1.5} = **0.2231**. By memorylessness this is also P(X > 5 | X > 2).

**E5: Uniform.** X ~ U[0,25]. Mean = 12.5. Variance = 25²/12 = **52.083**.

**E6: Normal.** X ~ N(30, 5²). P(26 ≤ X ≤ 34) = P(−0.8 ≤ Z ≤ 0.8) = 2Φ(0.8) − 1 = **0.5763**. This matches the GFG quiz's table value A(0.8) = 0.2881, doubled.

**E7: Expectation.** Max of two fair dice: E = 161/36 = **4.472**. Variance of one fair die: 35/12 = **2.917**.

**E8 [DA]: CLT.** σ = 12, n = 36 gives standard error 12/6 = **2**.

---

## Notes / flags
- Past-paper analysis is not included, as agreed. Add GATE 2022–2026 data here while studying.
- The GFG LMN page lists exponential "mean 1/λ, variance 1/λ²" directly under its Poisson section. Don't confuse the two: Poisson has mean = variance = λ.
