# Calculus — GATE 2027 (CS + DA)

**Syllabus basis:** CS: limits, continuity and differentiability, maxima and minima, mean value theorem, integration. DA adds: partial derivatives, Taylor series, Hessian-based optimisation, multivariable maxima/minima, and the usual calculus-for-ML topics.
Items marked **[DA]** are DA-only.
**Hbk** column: the Arihant Handbook has no Maths chapter, so it is "—".
**Links:** only GFG / MIT OCW URLs returned by search are used. NPTEL links are still unverified, so search "NPTEL Calculus" and add one under *My links*.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Limits, continuity, differentiability | — | [MIT 18.01SC](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Mean value theorems (Rolle, Lagrange, Cauchy) | — | [Rolle and Lagrange](https://www.geeksforgeeks.org/maths/rolles-theorem-and-lagranges-mean-value-theorem/) · [LMVT](https://www.geeksforgeeks.org/engineering-mathematics/lagranges-mean-value-theorem/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Maxima and minima (single variable) | — | [Maxima and Minima](https://www.geeksforgeeks.org/application-of-derivative-maxima-and-minima-mathematics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Integration (definite, improper, properties) | — | [LMN Calculus](https://www.geeksforgeeks.org/engineering-mathematics/calculus-notes-for-gate-cse-and-da/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Sequences and series, convergence | — | [Sequences and Series](https://www.geeksforgeeks.org/maths/sequences-and-series/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Taylor and Maclaurin series **[DA]** | — | [Taylor Series](https://www.geeksforgeeks.org/engineering-mathematics/taylor-series/) · [Taylor Theorem](https://www.geeksforgeeks.org/engineering-mathematics/taylor-theorem/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Partial derivatives, Hessian, saddle points **[DA]** | — | [LMN Engg Maths](https://www.geeksforgeeks.org/engineering-mathematics/last-minute-notes-engineering-mathematics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [Calculus cheat sheet](https://www.geeksforgeeks.org/maths/calculus-cheat-sheet/), [MIT 18.01SC syllabus](https://www.ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/syllabus).

**My links:** (NPTEL / textbook, add here)

---

## 1. Limits and continuity
- lim sin x / x = 1 as x → 0. lim (1 − cos x)/x² = 1/2. lim (eˣ − 1)/x = 1. lim (1 + 1/n)ⁿ = e.
- L'Hôpital applies to 0/0 or ∞/∞: lim f/g = lim f′/g′.
- f is continuous at a if lim f(x) = f(a). Differentiable implies continuous, but not the converse (|x| at 0).

## 2. Mean value theorems
- Rolle: f continuous on [a,b], differentiable on (a,b), f(a) = f(b). Then some c has f′(c) = 0.
- Lagrange: f′(c) = (f(b) − f(a))/(b − a) for some c in (a,b).
- Cauchy: f′(c)/g′(c) = (f(b) − f(a))/(g(b) − g(a)).

## 3. Maxima and minima
- Critical points: f′(x) = 0 or f′ undefined.
- Second-derivative test: f″ > 0 gives a local minimum, f″ < 0 a local maximum. If f″ = 0 the test is inconclusive.
- On a closed interval, compare the critical points and the endpoints.

## 4. Integration
- ∫ₐᵇ f dx = F(b) − F(a). ∫ₐᵇ f = ∫ₐᶜ f + ∫꜀ᵇ f.
- For even f: ∫₋ₐᵃ f = 2∫₀ᵃ f. For odd f: ∫₋ₐᵃ f = 0.
- Integration by parts: ∫u dv = uv − ∫v du.
- ∫₀^∞ e^{−x} dx = 1. ∫₀^π sin x dx = 2.
- Improper integral ∫₁^∞ 1/xᵖ dx converges iff p > 1.

## 5. Series
- Geometric: Σ rⁿ = 1/(1 − r) for |r| < 1.
- p-series Σ 1/nᵖ converges iff p > 1. Ratio test: converges if limit of |aₙ₊₁/aₙ| < 1.

## 6. [DA] Taylor and Maclaurin
f(x) = Σ f⁽ⁿ⁾(a)(x − a)ⁿ / n!. Maclaurin is the case a = 0.
- eˣ = 1 + x + x²/2! + x³/3! + …
- sin x = x − x³/3! + x⁵/5! − …
- cos x = 1 − x²/2! + x⁴/4! − …

## 7. [DA] Multivariable optimisation
- Critical point: ∇f = 0.
- Hessian H. With D = f_xx f_yy − f_xy²: D > 0 and f_xx > 0 means local min. D > 0 and f_xx < 0 means local max. D < 0 means saddle. D = 0 is inconclusive.

---

## Worked examples (all recomputed in code)

**E1: limit.** lim sin t / t = **1** as t → 0.

**E2: Lagrange.** f = x² on [1,3]. The secant slope is (9 − 1)/2 = 4. f′(c) = 2c = 4, so **c = 2**, which lies in (1,3).

**E3: Max/min.** f = x³ − 3x. f′ = 3x² − 3 = 0 gives x = ±1. f″ = 6x: at x = −1, f″ = −6 (**local max**). At x = 1, f″ = 6 (**local min**).

**E4: Integrals.** ∫₀^π sin x dx = **2**. ∫ x eˣ dx = **(x − 1)eˣ + C**. ∫₀^∞ e^{−x} dx = **1**.

**E5: Taylor.** eˣ at x = 0.1 using terms up to x³: 1 + 0.1 + 0.005 + 0.000167 = **1.105167**. The exact value is 1.105171, so the error is about 4 × 10⁻⁶ (the next term is x⁴/24 ≈ 4.2 × 10⁻⁶).

**E6 [DA]: Saddle point.** f = x³ + y³ − 3xy. Critical points: (0,0) and (1,1). At (0,0), D = −9 < 0, so it is a **saddle**. At (1,1), D = 27 > 0 and f_xx = 6 > 0, so it is a **local minimum**.

---

## Notes / flags
- Past-paper analysis is not included, as agreed. Add GATE 2022–2026 data here while studying.
- The Hessian rule is written in terms of D (the determinant), which is how the GFG LMN page gives it (as H).
