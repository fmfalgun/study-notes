# Theory of Computation — GATE 2027 (CS only; DA does not include it)

**Syllabus basis (CS):** regular expressions and finite automata; context-free grammars and push-down automata; regular and context-free languages, pumping lemma; Turing machines and undecidability. This section is not among the three that changed for 2027 (only Digital Logic, COA and Networks were rewritten).
**Hbk** column: the Arihant Handbook TOC chapter is pp. 1–29. Per-topic pages are not mapped. Marked `1–29*`.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
This is one of your weak subjects, so the notes are more detailed than for the strong ones.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Alphabets, strings, languages, Chomsky hierarchy | 1–29* | [Intro to TOC](https://www.geeksforgeeks.org/theory-of-computation/introduction-of-theory-of-computation/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | DFA design and complement / product constructions | 1–29* | [TOC for GATE (index)](https://www.geeksforgeeks.org/theory-of-computation/theory-of-computation-toc-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | NFA, ε-NFA, NFA to DFA conversion | 1–29* | [LMN TOC](https://www.geeksforgeeks.org/lmn-toc/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | DFA minimization | 1–29* | [LMN TOC (minimization)](https://www.geeksforgeeks.org/lmn-toc/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Regular expressions, regular grammars, FA ↔ RE | 1–29* | [TOC short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806171405492570/TOC-SHORT-NOTES_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Mealy and Moore machines | 1–29* | [GATE CS Notes index](https://www.geeksforgeeks.org/gate/gate-cs-notes-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Closure properties of regular languages | 1–29* | [Closure properties](https://www.geeksforgeeks.org/theory-of-computation/closure-properties-of-regular-languages/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Pumping lemma (regular and CFL) | 1–29* | [Pumping lemma](https://www.geeksforgeeks.org/theory-of-computation/pumping-lemma-in-theory-of-computation/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | CFG, derivations, ambiguity, simplification, CNF / GNF | 1–29* | [LMN TOC (CFG)](https://alphagtest.geeksforgeeks.org/lmn-toc/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | PDA (DPDA vs NPDA), CFG ↔ PDA | 1–29* | [LMN TOC (PDA)](https://www.geeksforgeeks.org/lmn-toc/) · [PDA problems list](https://www.geeksforgeeks.org/undecidability-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | CFL properties and closure table | 1–29* | [CFL properties](https://www.geeksforgeeks.org/theory-of-computation/various-properties-of-context-free-languages-cfl/) · [Closure table](https://www.geeksforgeeks.org/theory-of-computation/closure-properties-table-in-toc/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | Turing machines, recursive vs RE languages | 1–29* | [LMN TOC (types of languages)](https://www.geeksforgeeks.org/theory-of-computation/lmn-toc/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 13 | Decidability, undecidability, reductions | 1–29* | [Undecidability and reducibility](https://www.geeksforgeeks.org/theory-of-computation/undecidability-and-reducibility-in-toc/) · [Undecidability PYQs](https://www.geeksforgeeks.org/quizzes/gate-toc-undecideability-pyq-2010-to2025/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [Context-free languages and PDA GATE set](https://www.geeksforgeeks.org/context-free-languages-and-push-down-automata-gq/).

**My links:** (NPTEL / textbook, add here)

---

## 1. Hierarchy
| Type | Grammar | Machine | Example |
|---|---|---|---|
| 3 Regular | A → aB / a | DFA / NFA | aⁿ |
| 2 Context-free | A → α | NPDA | aⁿbⁿ |
| 1 Context-sensitive | α → β, \|α\| ≤ \|β\| | LBA | aⁿbⁿcⁿ |
| 0 Recursively enumerable | unrestricted | Turing machine | halting-problem language |
Regular ⊂ DCFL ⊂ CFL ⊂ CSL ⊂ Recursive ⊂ RE.

## 2–4. Finite automata
- DFA: exactly one move per (state, symbol). NFA: zero or more. Both accept exactly the regular languages.
- NFA with n states gives a DFA with at most 2ⁿ states, and that bound can be tight (see E2).
- Complement of a DFA: flip final and non-final states (needs a complete DFA). Complementing an NFA this way does not work in general.
- Product construction: intersection and union of two DFAs with m and n states needs up to m·n states.
- Minimization: remove unreachable states, split final / non-final, refine by transitions until stable (Myhill-Nerode). The minimal DFA is unique up to renaming.
- Number of states of minimal DFA = number of Myhill-Nerode equivalence classes.
- A DFA for "n-th symbol from the end is 1" needs 2ⁿ states even though an NFA needs n + 1.

## 5–6. Regular expressions and machines
- Identities: (a*)* = a*, (a + b)* = (a*b*)*, ε + aa* = a*, (ab)*a = a(ba)*.
- Convert FA to RE by state elimination (or Arden's rule X = R + XS ⇒ X = RS*).
- Mealy output depends on state and input; Moore output depends on state only. A Moore machine has n + 1 output symbols for n input symbols; Mealy has n.

## 7. Regular closure
Closed under union, intersection, complement, concatenation, Kleene star, reversal, difference, homomorphism, inverse homomorphism, quotient. Finite languages are regular.

## 8. Pumping lemma
- Regular: if L is regular there is p with every w ∈ L, |w| ≥ p written w = xyz, |xy| ≤ p, |y| ≥ 1, xyⁱz ∈ L for all i ≥ 0. Use it only to prove non-regularity (it can't prove regularity).
- CFL: w = uvxyz with |vxy| ≤ p, |vy| ≥ 1, uvⁱxyⁱz ∈ L for all i ≥ 0.
- Non-regular: aⁿbⁿ, ww^R, aᵖ for prime p, aⁿ². Non-CFL: aⁿbⁿcⁿ, ww, aⁿ² (every CFL over a one-letter alphabet is regular, by Parikh's theorem, so a non-regular unary language is not a CFL).

## 9–11. CFG and PDA
- Ambiguous grammar has two parse trees (or two leftmost derivations) for some string. Inherently ambiguous CFLs exist (e.g., aⁱbʲcᵏ with i = j or j = k).
- Simplification order: remove ε-productions, unit productions, then useless symbols.
- CNF: every rule A → BC or A → a; a string of length n needs 2n − 1 derivation steps. GNF: A → aα.
- DPDA accepts a proper subset (DCFLs) of what an NPDA accepts. DCFLs are closed under complement, not under union or intersection.
- CFLs are closed under union, concatenation, star, reversal, homomorphism, intersection with a regular language. Not closed under intersection or complement.
- Decidable for CFLs: membership (CYK), emptiness, finiteness. Undecidable: equivalence, universality (is L(G) = Σ*?), ambiguity, inclusion.

## 12. Turing machines
- Recursive (decidable): a TM that halts on every input. RE: a TM halts on strings in the language, may loop otherwise.
- Recursive languages are closed under complement, union, intersection. RE languages are closed under union, intersection, concatenation, star, but not complement. L and L̄ both RE implies L recursive.
- Multi-tape and nondeterministic TMs are equivalent in power to a single-tape TM.

## 13. Undecidability
- Decidable: membership, emptiness and equivalence for regular languages; emptiness and membership for CFLs; emptiness of a DFA / NFA.
- Undecidable: halting problem, membership problem for TMs (A_TM), emptiness and equivalence for TMs, equivalence of CFGs, whether L(M) is regular (Rice's theorem: every non-trivial property of RE languages is undecidable).
- Reduction: if A reduces to B and B is decidable, then A is decidable; if A is undecidable then B is undecidable.

---

## Worked examples (all recomputed in code)

**E1: DFA minimization.** A 4-state DFA for "even number of 0s" in which two states are clones of the other two minimizes to **2** states.

**E2: Subset construction can blow up.** "n-th symbol from the end is 1": the minimal DFA has **8** states for n = 3 and **16** for n = 4 (2ⁿ), while an NFA needs only n + 1 states.

**E3: Product DFA.** Strings with an even number of a's AND a number of b's divisible by 3: minimal DFA has 2 × 3 = **6** states.

**E4: CYK.** Grammar S → AB | AC, C → SB, A → a, B → b (in CNF, generating aⁿbⁿ, n ≥ 1). aabb ∈ L (**yes**), aab ∉ L (**no**), aaabbb ∈ L (**yes**), abab ∉ L (**no**).

**E5: Why aⁿbⁿ is not regular (Myhill-Nerode).** The prefixes a⁰, a¹, …, a⁶ are pairwise distinguishable by suffix bᵏ. Checking suffixes b⁰ to b⁷ gives **7** distinct behaviours, so any DFA needs at least that many states, and that number grows with n.

---

## Notes / flags
- The uploaded `theory-of-computation.md` covers FA, regular expressions, CFG, pumping lemma, Turing machines and decidability. It has no PDA coverage, no DFA minimization, no closure tables and no CNF/GNF, which this file's checklist adds.
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying.
