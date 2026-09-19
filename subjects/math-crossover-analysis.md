# Math Topic Crossover — ISRO Syllabus vs. BLE/ZigBee/HackRF Work

Cross-analysis of mathematics appearing in `../../Downloads/intern/` (ble_receiver_complete_guide.md, zigbee.pdf, FM FINAL UPDATED (1).pdf, hackrf_configuration.md) against the ISRO SC syllabus Math section and the previous-attempt exam analysis (`exam-analysis-report.md`). GATE CS topic structure sourced from GeeksforGeeks GATE CS Notes and GATE CSE Syllabus pages.

## Math actually present in the 4 docs

| Concept | Where it shows up |
|---|---|
| Complex exponentials, Euler's identity (`cos(2πft) = ½(e^jωt + e^-jωt)`) | ZigBee O-QPSK waveform, BLE quadrature demod, phase representation everywhere |
| Differentiation (rate of change of phase → frequency) | BLE quadrature demodulator: `f(t) = (1/2π)·dφ/dt` |
| Integration (message signal → phase) | FM modulation `s(t)=A·cos(2πf_ct + 2πk_f∫m(t)dt)`; ZigBee phase `φ(t)=2πΔf∫m(τ)dτ` |
| Gaussian/Normal distribution, AWGN, Q-function, BER | BLE: `BER = Q(√(2Eb/N0))`; ZigBee/FM: thermal noise `N0=kBTB`, Rayleigh/Rician fading |
| Binomial coefficients / combinatorics | BLE Access Address correlator: false-detection prob `Σ C(32,k)/2^32`, missed-detection via `C(32,k)·p^k·(1-p)^(32-k)` |
| Recurrence relations / difference equations | DC blocker `y[n]=x[n]-x[n-1]+α·y[n-1]`, AGC update `g[n+1]=g[n](1+μ·e[n])`, Mueller-Muller timing loop |
| Boolean/XOR operations, modular arithmetic (GF(2)) | Hamming-distance correlation `ρ[n]=Σ b[n+k]⊕a[k]`, CRC-16/24 polynomial division mod 2, LFSR whitening |
| Logarithms (dB math) | Gain stacking, Friis path loss, SNR, processing gain — everywhere |
| **Matrices/determinants/eigenvalues** | **Not used anywhere in these 4 docs** |
| **Graph theory** | **Not used anywhere in these 4 docs** |

## Dual-benefit ranking (exam + daily RF work)

| Tier | GATE Topic | RF Docs Usage | ISRO Exam Qs | Verdict |
|---|---|---|---|---|
| **1 (High)** | **Probability & Statistics** (Normal/Gaussian, Binomial, Random Variables, Mean/Variance/SD) | AWGN, BER/Q-function, Rayleigh/Rician fading, thermal noise | Q87 + general Math weightage | Study this first — reinforces both immediately |
| **1 (High)** | **Calculus** (Differentiation, Integration, Limits/Continuity) | Instantaneous frequency (derivative), FM/GFSK phase (integral), sampling/Nyquist reasoning | Q75 + general Math weightage | Second priority — same reason |
| **1 (High)** | **Discrete Math — Combinatorics** (counting, binomial coefficients) | Hamming-distance error probability calc in BLE correlator | Q16, Q17, Q32 (confirmed gaps) | Directly patches the Math gap identified earlier |
| **2 (Medium)** | **Discrete Math — Groups/Modular Arithmetic** (GF(2) fields) | CRC-16/24 polynomial division, LFSR whitening | Syllabus lists "Monoids, Groups" explicitly | Good conceptual tie-in, lower direct question yield |
| **2 (Medium)** | **Boolean Algebra/Propositional Logic** (XOR, logic ops) | Access-address correlation via XOR | Q15-style logic questions | Some overlap, but exam tests formal propositional forms (p→(p∧q)) which the docs don't really exercise |
| **3 (None)** | **Linear Algebra** (matrices, determinants, eigenvalues) | Absent | Q73, Q74 | Needs pure dedicated study — no reinforcement from work |
| **3 (None)** | **Graph Theory** (Euler's formula, coloring, connectivity) | Absent | Q59, Q60 | Needs pure dedicated study — no reinforcement from work |

## What to study (with links)

### Tier 1 — fold into weekday BLE/ZigBee/HackRF reading (same math, dual purpose)

**Probability:**
- [Random Variable](https://www.geeksforgeeks.org/random-variable/)
- [Normal Distribution](https://www.geeksforgeeks.org/maths/normal-distribution/)
- [Binomial Distribution](https://www.geeksforgeeks.org/maths/binomial-distribution/)
- [Mean, Variance, and Standard Deviation](https://www.geeksforgeeks.org/maths/what-is-mean/)
- [Conditional Probability](https://www.geeksforgeeks.org/maths/conditional-probability/)
- [Bayes's Formula for Conditional Probability](https://www.geeksforgeeks.org/maths/bayes-theorem/)

**Calculus:**
- [Limits, Continuity and Differentiability](https://www.geeksforgeeks.org/maths/limits/)
- [Application of Derivative](https://www.geeksforgeeks.org/maths/application-of-derivatives/)
- [Indefinite Integrals](https://www.geeksforgeeks.org/maths/indefinite-integrals/)
- [Euler's Formula](https://www.geeksforgeeks.org/maths/eulers-formula/) — explains the complex-exponential identity used throughout the BLE/ZigBee docs

**Combinatorics:**
- [Combinatorics Basics](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-combinatorics-basics/)
- [Binomial Coefficients](https://www.geeksforgeeks.org/maths/coefficient-in-binomial-expansion/)
- [Generalized PnC Set 1](https://www.geeksforgeeks.org/engineering-mathematics/generalized-pnc-set-1/) / [Set 2](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-generalized-pnc-set-2/)
- [Pigeonhole Principle](https://www.geeksforgeeks.org/engineering-mathematics/discrete-mathematics-the-pigeonhole-principle/) — this set directly resolves Q16/Q17/Q32-style questions

### Tier 2 — quick pass, good conceptual payoff

- [Groups](https://www.geeksforgeeks.org/engineering-mathematics/groups-discrete-mathematics/)
- [Modular Addition](https://www.geeksforgeeks.org/engineering-mathematics/modular-addition/)
- [Modular Multiplication](https://www.geeksforgeeks.org/dsa/modular-multiplication/) — read these, then re-read the CRC/LFSR sections in the ZigBee/BLE docs; it should click as "this *is* GF(2) arithmetic"
- [Introduction to Propositional Logic](https://www.geeksforgeeks.org/engineering-mathematics/proposition-logic/)
- [Propositional Equivalence](https://www.geeksforgeeks.org/engineering-mathematics/mathematical-logic-propositional-equivalences/) — patches Q15-style questions

### Tier 3 — needs dedicated video time (no reinforcement from BLE/ZigBee/HackRF work)

**Linear Algebra:**
- [Introduction to Matrix](https://www.geeksforgeeks.org/maths/introduction-to-matrices/)
- [Determinants](https://www.geeksforgeeks.org/maths/what-is-determinant-of-a-matrix/)
- [Eigenvalues and Eigenvectors](https://www.geeksforgeeks.org/engineering-mathematics/eigen-values/)
- [System of Linear Equations](https://www.geeksforgeeks.org/engineering-mathematics/system-linear-equations/)

**Graph Theory:**
- [Graph Theory Basics](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-graph-theory-basics/)
- [Planar Graphs and Graph Coloring](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-planar-graphs-graph-coloring/)
- [Euler and Hamiltonian Paths](https://www.geeksforgeeks.org/engineering-mathematics/euler-hamiltonian-paths/)
- [Graph Theory Practice Questions](https://www.geeksforgeeks.org/engineering-mathematics/graph-theory-practice-questions/)

## Practical suggestion for the 10-day plan

Put **Probability & Statistics + Calculus + Combinatorics first** in every weekday math session, since they get reinforced naturally while re-reading the BLE/ZigBee/HackRF docs at work — genuine dual-purpose study time. Push **Linear Algebra and Graph Theory** to the back of each session (or a dedicated slot) since those get zero passive reinforcement from the actual work and need focused video time on their own.

This ordering is now applied starting Day 3 (Mon Jul 13) — see `exam-prep-schedule.md` for the day-by-day breakdown (Days 1-2 were missed) and `2026-07-13-daily-plan.md` for today's session in depth.
