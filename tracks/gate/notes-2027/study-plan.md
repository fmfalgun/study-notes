# GATE 2027: weekend plan and today's checklist

Written Sun 22 Nov 2026. Exam window starts 6 Feb 2027. I don't know your paper's exact date, so the last weekend (30–31 Jan) is the last full study day.
Assumes about 6–8 hours per weekend day-block and 30–45 minutes on weekdays. Adjust if your real hours differ.

## How the files map to your study loop (one subject)
1. **Index table (C, N, P, E, R1, R2):** tick as you go. C = concept read, N = notes made, P = PYQs done, E = error log written, R1 / R2 = revision rounds.
2. **Concept:** use the Ref link, then the Hbk chapter range where one exists (the Handbook has no Maths, ML or AI chapters).
3. **Formulas and worked examples** in the same file: re-derive each example once without looking.
4. **PYQs:** your GKP book (2000–2021) by topic, then GATE 2022–2026 papers. Log wrong answers in the E column and the *Notes* section.
5. **R1 after 7–10 days, R2 in the last two weeks.**

Which files cover what: Maths (`linear-algebra`, `probability-statistics`, `calculus`, `discrete-maths`); core CS (`programming-ds`, `algorithms`, `databases`, `digital-logic`, `computer-organization`, `theory-of-computation`, `compiler-design`, `operating-systems`, `computer-networks`); DA only (`machine-learning`, `artificial-intelligence`); common (`general-aptitude`); 2027 syllabus check (`cn-2027-check`).

## Why this order
- Maths is your weakest high-weight block (about 14 marks a year in GKP's analysis) and is mostly shared between CS and DA, so it goes first, before the 27 Dec CS-vs-DA decision.
- After the decision the plan splits. Strong subjects (Programming/DS, Algorithms, DBMS, Digital Logic, Networks) only get timed PYQ and revision slots, not full study weekends.
- General Aptitude (15 marks) is a weekday drip so it doesn't use weekend time.

## Weekend map

| Wk | Dates | CS path | DA path (if you switch) |
|---|---|---|---|
| 1 | 22 Nov (today) | Linear Algebra | same |
| 2 | 28–29 Nov | Probability & Statistics | same |
| 3 | 5–6 Dec | Calculus | Calculus and optimization |
| 4 | 12–13 Dec | Discrete Maths | Machine Learning part 1 |
| 5 | 19–20 Dec | Operating Systems | Machine Learning part 2 |
| 6 | 26–27 Dec | Theory of Computation; **decide CS vs DA on 27 Dec** | Artificial Intelligence |
| 7 | 2–3 Jan | Computer Organization + Digital Logic | Programming/DS, DBMS and warehousing |
| 8 | 9–10 Jan | Compiler Design + Networks (2027 scope) | Probability and Linear Algebra revision |
| 9 | 16–17 Jan | Programming/DS + Algorithms + DBMS: timed PYQs and gap fixes | Algorithms and timed PYQs |
| 10 | 23–24 Jan | Two full mocks, error analysis | same |
| 11 | 30–31 Jan | Weak-topic fixes, formula sheets, R2 of Maths | same |

**1–5 Feb:** weekday light revision only: formulas, error log, rest. No new topics.

## Weekday routine (30–45 min)
- 15 min GA (one topic from `general-aptitude.md` per day).
- 20–30 min: PYQs from last weekend's subject, or R1 of an earlier file. Write errors into the file.

## Honest caveats
- Weeks 5–8 are heavy for the CS path (OS, TOC, COA/DL, CD, CN in four weekends). If you fall behind, drop Compiler Design's back-end topics first (code generation / optimization), then low-frequency TOC theory, not the numerical topics.
- NPTEL links, per-topic Handbook pages and GATE 2022–2026 question data are still to add. Slot them in while studying.
- Dates assume you study every listed weekend. Move a week only by swapping subjects, not by deleting a revision round.

---

# Today: Sun 22 Nov, Linear Algebra (file: `linear-algebra.md`)

Rows 7–10 are DA-only: **skip them today** (do them only if you end up in DA).

| Time | Block | Checklist |
|---|---|---|
| 09:30–11:00 | Matrix types, determinant, inverse (rows 1–2) | ☐ Read §1–2 formulas ☐ Open the LMN link, skim ☐ Re-solve worked examples E1–E2 without looking ☐ Note 3 properties you forget most (e.g. det(kA) = kⁿ det A) |
| 11:15–12:45 | Rank and linear systems (rows 3–4) | ☐ Row echelon form by hand on two matrices ☐ Write the consistency table: unique / infinite / none ☐ Redo the systems example ☐ Tick C and N for rows 1–4 |
| 12:45–14:00 | Break | ☐ Eat, rest, no screens |
| 14:00–15:45 | Eigenvalues and Cayley-Hamilton (row 5) | ☐ Sum = trace, product = det ☐ Eigenvalues of Aᵀ, A², A⁻¹, A + kI, triangular, idempotent, orthogonal ☐ Find eigenvectors for one 2×2 and one 3×3 ☐ Verify Cayley-Hamilton once |
| 16:00–17:00 | LU decomposition (row 6) | ☐ Do one 3×3 LU by hand ☐ Solve LUx = b by forward then back substitution |
| 17:15–18:30 | PYQs | ☐ Take the Linear Algebra / matrices questions from GKP (Engineering Maths) ☐ Time each at about 2 min ☐ Log every wrong one in the E column and the file's Notes ☐ Tick P for rows 1–6 |
| 18:30–18:45 | Close | ☐ Update the index ticks ☐ Write tomorrow's 20-min weekday task: matrices PYQs, plus 15 min GA |

**Today's pass criteria:** rows 1–6 have C, N and P ticked; the error log has an entry for every miss; you can state the 5 eigenvalue shortcuts from memory.
