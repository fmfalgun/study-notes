# Book Review: "Calculus Made Easy" (33283-pdf.pdf) — Fit for ISRO Prep

Evaluation of `33283-pdf.pdf` — **"Calculus Made Easy" by Silvanus Thompson** (1910/1914, Project Gutenberg #33283) — as a reference for ISRO SC Computer Science prep and the BLE/ZigBee/HackRF work.

## Verdict

Legitimate, well-regarded, very approachable introduction to differential and integral calculus. Its scope is **narrow: pure single-variable Calculus only** — no Linear Algebra, Discrete Math, Probability, or Graph Theory. Good fit for one slice of Math prep, not the whole thing.

## Fit check against syllabus Calculus items

| Syllabus Calculus item | Covered? |
|---|---|
| Limits, continuity, differentiability | ✅ Ch I–III |
| Maxima and minima | ✅ Ch XI (explicit chapter) |
| **Mean Value Theorem** (Lagrange's/Rolle's/Cauchy's) | ❌ **Not covered at all** — this book never formalizes MVT. Use the GFG links in `math-crossover-analysis.md` for this. |
| Integration | ✅ Ch XVII–XX |
| Multivariable/triple integrals (needed for Q75-style questions) | ❌ Book only reaches Partial Differentiation (Ch XVI) and basic area-finding — no formal multiple-integral treatment |

It also happens to cover exactly the calculus mechanics used in the BLE/ZigBee/FM docs: differentiating phase to get frequency, integrating frequency to get phase, differentiating sin/cos, and exponential growth/decay (AGC, DC-blocker time constants).

## Pages/sections to study, ranked

### High priority — directly maps to syllabus + reinforces the RF docs

| Chapter | Pages | Why |
|---|---|---|
| I–III: Preliminary Terrors, Degrees of Smallness, Relative Growings | 1–16 | Builds the core `d`/`∫` intuition — same notation as `dφ/dt` and `∫m(t)dt` in the BLE/FM docs |
| XI: Maxima and Minima | 91–108 | Explicit syllabus topic |
| XV: How to deal with Sines and Cosines | 162–171 | Directly used in every phase/frequency derivation in the ZigBee/BLE/FM papers |
| XIV: True Compound Interest and Law of Organic Growth | 131–161 | Exponential functions — same math as AGC convergence and DC-blocker decay (`α^n`, time constants) |
| XVII–XVIII: Integration, Integrating as Reverse of Differentiating | 180–203 | Explicit syllabus topic, core integration technique |

### Medium priority — solid foundation, builds general fluency

| Chapter | Pages | Why |
|---|---|---|
| IV–VI: Simplest Cases, Constants, Sums/Products/Quotients | 17–47 | Differentiation rules (product/quotient rule shows up in filter derivations) |
| VIII: When Time Varies | 52–65 | Related-rates — functions of time, same framing as signal processing |
| XIX–XX: Finding Areas by Integrating, Dodges/Pitfalls | 204–231 | Integration applications; partial bridge toward Q75-style area/volume reasoning (though not true triple integrals) |
| Table of Standard Forms | 249–251 | Quick-reference cheat sheet — worth bookmarking regardless |

### Lower priority / optional

| Chapter | Pages | Why |
|---|---|---|
| VII, XII, XIII: Successive Differentiation, Curvature, Other Dodges | 48–51, 109–130 | Not directly tested, general fluency only |
| XVI: Partial Differentiation | 172–179 | Not in syllabus explicitly, but a conceptual stepping-stone toward multivariable calculus |
| XXI: Finding Some Solutions | 232–248 | Worked examples, optional practice |

## Bottom line

Use this book for **Ch I, III, XI, XIV, XV, XVII–XVIII** as the core calculus pass — a fast, intuitive way to lock down exactly the differentiation/integration skills the RF docs already exercise. It does **not replace** the Mean Value Theorem or multivariable-integral study needed for the full syllabus — keep using the GFG links from `math-crossover-analysis.md` for those. Calculus was only 1 of 9 Math questions in the sample paper analyzed (`exam-analysis-report.md`) — Linear Algebra, Discrete Math, and Graph Theory still need their own separate resources, none of which this book touches.
