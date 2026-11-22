# Digital Logic — GATE 2027 (CS + DA)

**2027 syllabus change (CS):** Digital Logic was reworded, nothing removed. It now names minimization by algebraic technique, Karnaugh map and tabular method, and design of combinational and sequential circuits, alongside Boolean algebra and number representation / computer arithmetic (fixed and floating point). I took this from several secondary summaries that compared the 2026 and 2027 PDFs (GATENotes, GateGuide, ProSyllabus, IAE Academy). I could not open the official PDF directly, so check the Digital Logic block in it once.
**Hbk** column: the Handbook's "Switching Theory and Computer Architecture" chapter is pp. 353–404 and covers both Digital Logic and COA. Per-topic pages are not mapped. Marked `353–404*`.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
Strength: you said Digital Logic is strong. This file is for revision plus the new 2027 wording (tabular method, design problems).

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Boolean algebra, laws, duality, functional completeness | 353–404* | [Boolean algebra](https://www.geeksforgeeks.org/digital-logic/boolean-algebra/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Logic gates, NAND/NOR realizations | 353–404* | [Digital Logic for GATE](https://www.geeksforgeeks.org/digital-logic/digital-logic-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | SOP/POS, minterms, canonical forms | 353–404* | [LMN Digital Electronics](https://www.geeksforgeeks.org/digital-logic/lmn-digital-electronics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Minimization: algebraic, K-map, don't cares | 353–404* | [K-Map intro](https://www.geeksforgeeks.org/introduction-of-k-map-karnaugh-map/) · [Minimization](https://origin.geeksforgeeks.org/minimization-of-boolean-functions) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Minimization: tabular (Quine-McCluskey) **new wording in 2027** | 353–404* | [Digital Logic for GATE (QM section)](https://www.geeksforgeeks.org/digital-logic/digital-logic-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Combinational design: adders, subtractors, comparators | 353–404* | [Construction of combinational circuits](https://www.geeksforgeeks.org/construction-of-combinational-circuits/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | MUX, DEMUX, decoder, encoder, implementing functions | 353–404* | [GFG course syllabus PDF (MUX/decoder topics)](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20230302142337/GATE-PDF-1.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Latches and flip-flops, conversions | 353–404* | [GATE CS Notes index (sequential)](https://www.geeksforgeeks.org/gate/gate-cs-notes-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Counters (ripple, ring, Johnson, custom sequence) | 353–404* | [Counters](https://www.geeksforgeeks.org/digital-logic/counters-in-digital-logic/) · [Design a counter](https://www.geeksforgeeks.org/design-counter-given-sequence/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Synchronous sequential design, state tables, sequence detectors | 353–404* | [Sequential PYQs 2026](https://www.geeksforgeeks.org/quizzes/gate-digital-logic-pyq-2026-module-2sequential-circuits/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Number systems, complements, fixed point, overflow | 353–404* | [Number representation](https://www.geeksforgeeks.org/number-representation-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | Floating point (IEEE 754) | 353–404* | [Number-system PYQs 2010–2025](https://www.geeksforgeeks.org/quizzes/gate-digital-logic-number-circuit-pyq-2010-to-2025/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [Digital Logic PYQs 2010–2025](https://www.geeksforgeeks.org/quizzes/gate-digital-logic-pyq-2010-to2025/), [BCD to 7-segment (K-map practice)](https://www.geeksforgeeks.org/digital-logic/bcd-to-7-segment-decoder/).

**My links:** (NPTEL / textbook, add here)

---

## 1–3. Boolean algebra
- Laws: identity, null, idempotent, complement, absorption (A + AB = A), consensus (AB + A'C + BC = AB + A'C), De Morgan.
- Dual: swap AND/OR and 0/1. Self-dual function: f(x₁..xₙ) = ¬f(¬x₁..¬xₙ). Number of self-dual functions of n variables: 2^(2^(n−1)).
- Number of Boolean functions of n variables: 2^(2ⁿ).
- NAND and NOR are universal. XOR from NAND needs 4 gates. Sets like {AND, NOT} and {OR, NOT} are functionally complete; {AND, OR} is not.
- Π M(i) lists the zeros of the function; Σ m(i) lists the ones. They are complementary index sets.

## 4–5. Minimization
- K-map cells follow Gray order. Groups are powers of 2, as large as possible, wrapping at the edges. A group of 2ᵏ cells removes k variables.
- Prime implicant: a largest group. Essential prime implicant: covers a minterm no other prime implicant covers. Include all essential ones first, then cover the rest minimally.
- Don't cares: treat as 1 only where they enlarge a group.
- Quine-McCluskey (tabular): group minterms by number of 1s, merge pairs differing in one bit, repeat to get prime implicants, then use a prime-implicant chart to choose a minimal cover.

## 6–7. Combinational circuits
- Half adder: S = A⊕B, C = AB. Full adder: S = A⊕B⊕Cin, Cout = AB + Cin(A⊕B).
- Ripple-carry delay grows with n. Carry-lookahead: Gᵢ = AᵢBᵢ, Pᵢ = Aᵢ⊕Bᵢ, Cᵢ₊₁ = Gᵢ + PᵢCᵢ.
- 2ⁿ:1 MUX has n select lines. A 2ⁿ:1 MUX can implement any function of n + 1 variables (with one variable on data inputs). An 8:1 MUX built from 2:1 MUXes needs 7.
- n-to-2ⁿ decoder generates minterms; any function of n variables = OR of selected decoder outputs.
- BCD addition: if the 4-bit sum exceeds 9 (or carries out), add 0110.

## 8–10. Sequential circuits
- Characteristic equations: SR: Q⁺ = S + R'Q (SR = 0). JK: Q⁺ = JQ' + K'Q. D: Q⁺ = D. T: Q⁺ = T⊕Q.
- JK with J = K = T gives a T flip-flop. JK with K = J' gives a D flip-flop.
- Counters: n flip-flops give modulus up to 2ⁿ; a mod-N counter needs ⌈log₂ N⌉ flip-flops. Ring counter: n states with n flip-flops. Johnson (twisted ring): 2n states with n flip-flops.
- Ripple (asynchronous) counter: each stage clocked by the previous output, so the delay adds up; max clock frequency is limited by the total propagation delay.
- Design steps: state diagram, state table, flip-flop excitation table, simplify inputs by K-map, draw circuit.
- Mealy output depends on state and input; Moore output depends on state only.

## 11–12. Number representation
- n-bit two's complement range: −2ⁿ⁻¹ to 2ⁿ⁻¹ − 1. One's complement: −(2ⁿ⁻¹ − 1) to 2ⁿ⁻¹ − 1 (two zeros). Sign-magnitude: same range as one's complement.
- Overflow in addition: the carry into the sign bit differs from the carry out of it; equivalently, two operands of the same sign give a result of the opposite sign.
- IEEE 754 single precision: 1 sign bit, 8 exponent bits (bias 127), 23 fraction bits; value = (−1)ˢ × 1.f × 2^(e−127). Double: 1, 11 (bias 1023), 52.
- Special cases: exponent all 0s = zero or denormal; exponent all 1s = infinity or NaN.
- Gray code: g = b ⊕ (b >> 1); adjacent values differ in one bit.

---

## Worked examples (all recomputed in code)

**E1: K-map.** Π(1,2,3) over A,B,C is the same as Σ(0,4,5,6,7). Minimal SOP: **A + B'C'**.

**E2: NAND realization of XOR.** Four NAND gates: n1 = NAND(a,b), then NAND(NAND(a,n1), NAND(b,n1)). Truth table output 0, 1, 1, 0.

**E3: Counting functions.** With n = 3 there are 2⁸ = **256** Boolean functions. Brute force confirms **16** self-dual functions, matching 2^(2^(n−1)) = 2⁴.

**E4: Overflow (8-bit two's complement).** 100 + 50 = 150 exceeds 127, and the 8-bit result reads as −106: **overflow**. −100 + −50 gives +106: **overflow**. 100 + (−50) = 50: **no overflow**.

**E5: IEEE 754 single.** 0.5 → **0x3F000000**. −6.25 → **0xC0C80000**. 10.75 → **0x412C0000**.

**E6: Gray code.** Binary 110 (6) → Gray **101**. The 3-bit sequence is 000, 001, 011, 010, 110, 111, 101, 100.

**E7: Counters.** Mod-10 counter needs **4** flip-flops. A 4-bit ripple counter has modulus **16**.

**E8: Flip-flop conversion.** A JK flip-flop with J = K = T satisfies Q⁺ = Q ⊕ T for all inputs, so it behaves as a T flip-flop (verified over all four input pairs).

**E9: BCD.** 7 + 8 gives 1111 in binary (15 > 9), so add 0110: result **0001 0101** (15 in BCD).

---

## Notes / flags
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying. GFG has a Digital Logic PYQ set for 2026 (listed above), which may help since it is the latest paper.
- The GFG "Digital Logic for GATE" page labels its syllabus box as "Computer Networks, as per GATE CSE 2025". That is a typo on their page; the listed items are the Digital Logic ones.
- I haven't checked how often earlier papers asked Quine-McCluskey questions. The 2027 wording names the tabular method, so keep it on your must-know list.
