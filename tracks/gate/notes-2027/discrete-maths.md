# Discrete Mathematics — GATE 2027 (CS; DA does not include it)

**Syllabus basis (CS):** propositional and first-order logic; sets, relations, functions, partial orders and lattices; monoids and groups; graphs (connectivity, matching, colouring); combinatorics (counting, recurrence relations, generating functions).
**Hbk** column: the Arihant Handbook has no Maths chapter, so it is "—".
**Links:** only GFG URLs returned by search are used. NPTEL links are still unverified, so search "NPTEL Discrete Mathematics" and add one under *My links*.
Discrete maths is shared with DA only in small parts (basic logic and counting), so it is mainly a CS-path subject.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Propositional logic, equivalences, inference | — | [Logic notes](https://www.geeksforgeeks.org/digital-logic/gate-notes-propositional-and-first-order-logic-discrete-mathematics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | First-order logic, quantifiers, negation | — | [Propositional and FOL (GQ)](https://www.geeksforgeeks.org/propositional-and-first-order-logic-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Sets and relations, equivalence classes | — | [Types of relations](https://www.geeksforgeeks.org/maths/types-of-relation-in-maths/) · [Equivalence](https://www.geeksforgeeks.org/maths/equivalence-relations/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Counting equivalence relations (Bell numbers) | — | [Number of equivalence relations](https://www.geeksforgeeks.org/engineering-mathematics/number-possible-equivalence-relations-finite-set/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Functions (one-one, onto, counting) | — | [LMN Discrete Maths](https://www.geeksforgeeks.org/maths/last-minute-notes-discrete-mathematics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Posets, Hasse diagrams, elements of a poset | — | [Hasse](https://www.geeksforgeeks.org/engineering-mathematics/discrete-mathematics-hasse-diagrams/) · [Elements of POSET](https://www.geeksforgeeks.org/engineering-mathematics/elements-of-poset/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Lattices | — | [Partial Orders and Lattices](https://www.geeksforgeeks.org/engineering-mathematics/partial-orders-lattices/) · [Set 2](https://www.geeksforgeeks.org/engineering-mathematics/partial-orders-and-lattices-set-2-mathematics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Semigroup, monoid, group, abelian group, subgroups | — | [Group theory](https://www.geeksforgeeks.org/engineering-mathematics/groups-discrete-mathematics/) · [GATE notes](https://www.geeksforgeeks.org/group-theory-notes-for-gate-exams/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Graph basics, isomorphism, connectivity | — | [Isomorphism and connectivity](https://www.geeksforgeeks.org/mathematics-graph-isomorphisms-connectivity/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Matching, independent sets, covering | — | [Independent sets, covering, matching](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-independent-sets-covering-and-matching/) · [Matching](https://www.geeksforgeeks.org/mathematics-matching-graph-theory/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Planar graphs and colouring | — | [Planar and colouring](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-planar-graphs-graph-coloring/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | Counting: inclusion-exclusion, pigeonhole, derangements | — | [PIE](https://www.geeksforgeeks.org/maths/principle-of-inclusion-and-exclusion/) · [Pigeonhole](https://www.geeksforgeeks.org/discrete-mathematics-the-pigeonhole-principle/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 13 | Recurrence relations | — | [Types of recurrences](https://www.geeksforgeeks.org/engineering-mathematics/discrete-mathematics-types-of-recurrence-relations-set-2/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 14 | Generating functions | — | [Generating functions](https://www.geeksforgeeks.org/engineering-mathematics/discrete-maths-generating-functions-introduction-prerequisites/) · [Set 2](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-generating-functions-set-2/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [GFG Discrete Maths for GATE CSE](https://www.geeksforgeeks.org/maths/discrete-mathematics-for-gate-cse-exam/), [Discrete Maths short-notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251006150112476506/Discrete-Maths_compressed.pdf), [GATE CS notes index (graph theory list)](https://www.geeksforgeeks.org/gate/gate-cs-notes-gq/).

**My links:** (NPTEL / textbook, add here)

---

## 1. Propositional logic
- p → q ≡ ¬p ∨ q ≡ ¬q → ¬p (contrapositive). The converse q → p is not equivalent.
- p ↔ q ≡ (p → q) ∧ (q → p).
- De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q. ¬(p ∨ q) ≡ ¬p ∧ ¬q.
- Tautology is always true; contradiction is always false.
- Modus ponens: p, p → q ⊢ q. Resolution: (p ∨ q), (¬p ∨ r) ⊢ (q ∨ r).

## 2. First-order logic
- ¬∀x P(x) ≡ ∃x ¬P(x). ¬∃x P(x) ≡ ∀x ¬P(x).
- ∀x (P ∧ Q) ≡ ∀x P ∧ ∀x Q. ∃x (P ∨ Q) ≡ ∃x P ∨ ∃x Q.
- ∃x (P ∧ Q) → ∃x P ∧ ∃x Q holds, but the converse does not.
- ∀x (P → Q) → (∀x P → ∀x Q) holds, but the converse does not.
- Translate "all A are B" as ∀x (A(x) → B(x)). Translate "some A is B" as ∃x (A(x) ∧ B(x)).

## 3–5. Sets, relations, functions
- |A| = n gives 2ⁿ subsets, 2^{n²} relations on A, and 2^{mn} relations from A to B (|B| = m).
- Reflexive, symmetric, antisymmetric, transitive. Equivalence = reflexive + symmetric + transitive. Partial order = reflexive + antisymmetric + transitive.
- An equivalence relation partitions the set. The number of equivalence relations on an n-set is the Bell number Bₙ: 1, 2, 5, 15, 52, 203, …
- Functions A → B with |A| = m, |B| = n: total nᵐ. One-one: n!/(n−m)! (for m ≤ n). Onto: Σᵢ (−1)ⁱ C(n,i)(n−i)ᵐ. Bijections (m = n): n!.

## 6–7. Posets and lattices
- Hasse diagram: draw only covering relations (no reflexive or transitive edges).
- Maximal / minimal elements, greatest / least element, upper / lower bounds, lub (join) and glb (meet).
- Lattice: every pair has a lub and a glb. Examples: divisors of n under divisibility (meet = gcd, join = lcm); the power set under ⊆.
- Bounded lattice has a top and a bottom. Distributive and complemented lattices; Boolean lattice = distributive + complemented (e.g., power set).
- A finite lattice is always bounded.

## 8. Algebraic structures
- Semigroup: closure + associativity. Monoid: + identity. Group: + inverses. Abelian group: + commutativity.
- Lagrange: the order of a subgroup divides the order of the group. The order of an element divides the order of the group.
- Z_n under + is a cyclic group. Z_n* (units, elements coprime to n) under × has φ(n) elements.
- Group of prime order is cyclic. If |G| = 2, every element is its own inverse.

## 9–11. Graphs
- Handshake: Σ deg = 2e, so the number of odd-degree vertices is even.
- Kₙ has n(n−1)/2 edges. Spanning trees of Kₙ: nⁿ⁻² (Cayley). A tree on n vertices has n − 1 edges.
- Connectivity: κ(G) ≤ λ(G) ≤ δ(G).
- Euler circuit exists iff the graph is connected and all degrees are even. Euler path iff exactly 0 or 2 vertices have odd degree.
- Matching: edges with no common vertex. Vertex cover + independent set = n (α₀ + β₀ = n). Hall's theorem for bipartite graphs.
- Planar: V − E + F = 2 (connected). E ≤ 3V − 6 for V ≥ 3. E ≤ 2V − 4 if no triangles. K₅ and K₃,₃ are non-planar.
- Colouring: χ(G) ≤ Δ + 1. Planar graphs are 4-colourable. Bipartite iff 2-colourable iff no odd cycle. χ(Kₙ) = n.

## 12. Counting
- |A ∪ B| = |A| + |B| − |A ∩ B|, extended by alternating signs.
- Pigeonhole: N objects in k boxes gives some box with ≥ ⌈N/k⌉.
- Derangements: Dₙ = n! Σ (−1)ᵏ/k!. Values: D₄ = 9, D₅ = 44.
- Stars and bars: non-negative solutions of x₁ + … + x_k = n number C(n+k−1, k−1).

## 13–14. Recurrences and generating functions
- Linear homogeneous with constant coefficients: the characteristic equation gives the roots, and the solution is a sum of cᵢ rⁱⁿ. Repeated root r gives (c₁ + c₂n)rⁿ.
- Generating function: G(x) = Σ aₙxⁿ. 1/(1 − x) generates 1, 1, 1, … and 1/(1 − x)² generates 1, 2, 3, … .
- Divide-and-conquer recurrences are covered in the Algorithms file (Master theorem).

---

## Worked examples (all recomputed in code)

**E1: Hasse diagram of divisors of 12.** Elements 1, 2, 3, 4, 6, 12. Covering pairs: 1–2, 1–3, 2–4, 2–6, 3–6, 4–12, 6–12. Every pair has gcd and lcm inside the set, so it is a **lattice**.

**E2: Relations.** On a 3-element set there are 2⁹ = **512** relations. On a 4-element set the number of equivalence relations is B₄ = **15**.

**E3: Onto functions.** From a 4-set to a 3-set: 3⁴ − 3·2⁴ + 3·1⁴ = 81 − 48 + 3 = **36**. A brute-force count of all 81 functions gives the same 36.

**E4: Inclusion-exclusion.** Integers from 1 to 100 divisible by 2 or 5: 50 + 20 − 10 = **60**.

**E5: Recurrence.** aₙ = 5aₙ₋₁ − 6aₙ₋₂ with a₀ = 1, a₁ = −2. Characteristic equation r² − 5r + 6 = 0 gives r = 2, 3. Solution aₙ = 5·2ⁿ − 4·3ⁿ. The sequence is 1, −2, −16, −68, −244, … and the closed form matches.

**E6: Derangements.** D₄ = 24(1 − 1 + 1/2 − 1/6 + 1/24) = **9**.

**E7: Groups.** Z₁₂* = {1, 5, 7, 11}, order φ(12) = 4. In Z₇* the element 3 has order **6**, so 3 generates the group (Z₇* is cyclic of order 6).

**E8: Graphs.** K₅ has 10 edges. A planar graph on 6 vertices has at most 3·6 − 6 = **12** edges. K₄ has 4² = **16** spanning trees. A triangle needs 3 colours, with 3·2·1 = **6** proper 3-colourings.

---

## Notes / flags
- Past-paper analysis is not included, as agreed. Add GATE 2022–2026 data here while studying.
- Some GFG pages in this list are old (dated 2018–2020 content) but cover standard results; the dated ones are fine for theorems, not for syllabus scoping.
- Generating-function questions are rare in recent papers, but I haven't verified that against papers, so treat it as a guess until you add PYQ data.
