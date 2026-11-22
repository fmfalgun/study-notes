# Artificial Intelligence — GATE 2027 (DA only; not in the CS paper)

**Syllabus basis (DA):** search (informed, uninformed, adversarial); logic (propositional, predicate); reasoning under uncertainty (conditional independence, Bayesian network representation, exact inference by variable elimination, approximate inference by sampling). Lists are from GFG pages, not the official PDF.
**Hbk** column: the Arihant Handbook has **no AI chapter**.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
Small section, so one weekend is likely enough. Only needed if you choose DA.

## Checklist (index)

| # | Topic | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|
| 1 | Uninformed search: BFS, DFS, UCS, depth-limited, IDDFS | [AI for GATE 2027](https://www.geeksforgeeks.org/artificial-intelligence/artificial-intelligence-for-gate-2025/) · [Search algorithms in AI](https://www.geeksforgeeks.org/machine-learning/search-algorithms-in-ai/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Informed search: greedy best-first, A*, heuristics (admissible, consistent) | [Informed search](https://www.geeksforgeeks.org/artificial-intelligence/informed-search-algorithms-in-artificial-intelligence/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Adversarial search: minimax, alpha-beta pruning | [AI for GATE 2027](https://www.geeksforgeeks.org/artificial-intelligence/artificial-intelligence-for-gate-2025/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Propositional logic, entailment, CNF / resolution | [AI short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174609550592/AI-Short-Notes_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Predicate logic and quantifiers | [AI for GATE 2027](https://www.geeksforgeeks.org/artificial-intelligence/artificial-intelligence-for-gate-2025/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Conditional independence, Bayesian networks | [AI short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174609550592/AI-Short-Notes_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Exact inference: variable elimination; approximate: sampling | [AI short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174609550592/AI-Short-Notes_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [GATE DA notes (2027 syllabus)](https://www.geeksforgeeks.org/gate/gate-da-notes-according-to-gate-2025-syllabus/), [GATE DA subject-wise tips](https://www.geeksforgeeks.org/gate/gate-da-subject-wise-preparation-tips/) (suggests Russell & Norvig for practice).

**My links:** (NPTEL / textbook, add here)

---

## 1. Uninformed search
b = branching factor, d = depth of the shallowest goal, m = max depth.
| Algorithm | Complete | Optimal | Time | Space |
|---|---|---|---|---|
| BFS | yes | yes (unit step costs) | O(bᵈ) | O(bᵈ) |
| UCS | yes (positive costs) | yes | O(b^(1+⌊C*/ε⌋)) | same |
| DFS | no (infinite / cyclic) | no | O(bᵐ) | O(bm) |
| Depth-limited (limit l) | no | no | O(bˡ) | O(bl) |
| IDDFS | yes | yes (unit costs) | O(bᵈ) | O(bd) |

## 2. Informed search
- Greedy: expand lowest h(n); not optimal, not complete in general.
- A*: expand lowest f(n) = g(n) + h(n). Optimal if h is admissible (h ≤ true cost) for tree search; for graph search h should be consistent (h(n) ≤ c(n, n′) + h(n′)). Consistent ⇒ admissible.
- If h = 0, A* behaves like UCS.

## 3. Adversarial search
- Minimax: MAX picks the largest child value, MIN the smallest. Time O(bᵐ).
- Alpha-beta gives the same root value as minimax; pruning depends on move ordering. Best case about O(b^(m/2)).

## 4–5. Logic
- Entailment KB ⊨ α: α true in every model of KB. Check by truth table (2ⁿ rows) or resolution.
- Valid: true in all models; satisfiable: true in at least one.
- Quantifiers: ¬∀x P ≡ ∃x ¬P. ∀x∃y differs from ∃y∀x.

## 6–7. Bayesian networks
- Joint = ∏ P(Xᵢ | Parents(Xᵢ)). With n Boolean variables the full joint needs 2ⁿ − 1 numbers; the network needs Σ 2^(#parents).
- Conditional independence: use d-separation (chain and common cause blocked when the middle node is observed; collider opens when the collider or a descendant is observed).
- Variable elimination: write the factors, sum out hidden variables in an order, normalize.
- Sampling: prior, rejection, likelihood weighting, Gibbs (MCMC).

---

## Worked examples (all recomputed in code)

**E1: A* vs UCS.** Graph S→A (1), S→B (4), A→B (2), A→G (12), B→G (5), with h(S) = 7, h(A) = 6, h(B) = 4, h(G) = 0. Both A* and UCS return S–A–B–G with cost **8**. (h is admissible here.)

**E2: Alpha-beta.** MAX over three MIN nodes with leaves (3, 5), (6, 9), (1, 2). Minimax value = **6**. Left to right, alpha-beta visits **5** of the 6 leaves: in the third branch, after seeing 1 it prunes the leaf 2, since 1 ≤ 6 already.

**E3: Variable elimination.** Network A → B, A → C with P(A) = 0.3, P(B|A) = 0.9, P(B|¬A) = 0.2, P(C|A) = 0.8, P(C|¬A) = 0.1. Query P(A | B, C): unnormalised 0.216 (A true) and 0.014 (A false), so P(A | B, C) = **0.939**.

**E4: Entailment.** (p → q) ∧ (q → r) ⊨ (p → r): all 8 rows of the truth table check out, so **yes** (hypothetical syllogism).

**E5: Parameter count.** 5 Boolean variables: full joint 2⁵ − 1 = **31** numbers. A chain X₁ → X₂ → … → X₅ needs 1 + 2 + 2 + 2 + 2 = **9**.

---

## Notes / flags
- Your uploaded `ai-ml.md` covers BFS, DFS and A*. It has no UCS / IDDFS, adversarial search, logic or Bayesian networks; rows 3 to 7 are the gaps.
- Optimality conditions for A* differ for tree and graph search; GATE questions usually say admissible or consistent explicitly.
- Past-paper analysis is not included. Add GATE DA 2024–2026 data while studying.
