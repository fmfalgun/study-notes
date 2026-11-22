# Compiler Design — GATE 2027 (CS only; DA does not include it)

**Syllabus basis (CS):** lexical analysis; parsing; syntax-directed translation; runtime environments; intermediate code generation; local optimization; data flow analyses (constant propagation, liveness analysis, common sub-expression elimination). This section is unchanged for 2027.
**Hbk** column: the Arihant Handbook CD chapter is pp. 273–299. Per-topic pages are not mapped. Marked `273–299*`. **Check:** from the contents photos, the Handbook showed no separate code-generation or optimization sections. I couldn't tell whether runtime environments and intermediate code are covered either, so rows 8 to 11 are marked `check`. You may need GFG or a textbook for them.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
This is one of your weak subjects (about 5.3 marks per year in GKP's 2011–2021 analysis).

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Phases of a compiler, tokens, lexical analysis | 273–299* | [Introduction to compilers](https://www.geeksforgeeks.org/compiler-design/introduction-to-compilers/) · [CD short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251006150112515643/CD_ShortNotes2025-_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Grammars: ambiguity, left recursion, left factoring | 273–299* | [CD for GATE (index)](https://www.geeksforgeeks.org/compiler-design/compiler-design-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | FIRST and FOLLOW | 273–299* | [CD for GATE (index)](https://www.geeksforgeeks.org/compiler-design/compiler-design-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Top-down parsing: recursive descent, LL(1) | 273–299* | [Types of parsers](https://www.geeksforgeeks.org/compiler-design/types-of-parsers-in-compiler-design/) · [Compiler theory Set 1](https://www.geeksforgeeks.org/compilers-set-1/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Bottom-up parsing: shift-reduce, operator precedence | 273–299* | [LMN Compiler Design](https://www.geeksforgeeks.org/compiler-design/last-minute-notes-compiler-design-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | LR(0), SLR(1), CLR(1), LALR(1): tables and conflicts | 273–299* | [SLR, CLR and LALR](https://www.geeksforgeeks.org/compiler-design/slr-clr-and-lalr-parsers-set-3/) · [LALR with examples](https://www.geeksforgeeks.org/compiler-design/lalr-parser-with-examples/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Syntax-directed translation: S- and L-attributed | 273–299* | [SDT](https://www.geeksforgeeks.org/compiler-design/syntax-directed-translation-in-compiler-design/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Runtime environments: activation records, stack and heap, parameter passing | 273–299* **check** | [GATE CS Notes index (runtime)](https://www.geeksforgeeks.org/gate/gate-cs-notes-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Intermediate code: three-address code, basic blocks, CFG | 273–299* **check** | [Intermediate representations (CD for GATE)](https://www.geeksforgeeks.org/compiler-design/compiler-design-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Local optimization (peephole, algebraic) | 273–299* **check** | [LMN Compiler Design (optimization)](https://alphagtest.geeksforgeeks.org/last-minute-notes-compiler-design-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Data flow analysis: constant propagation, liveness, CSE | 273–299* **check** | [CD for GATE (data flow)](https://www.geeksforgeeks.org/compiler-design/compiler-design-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [CD PYQ quiz 2010–2025](https://www.geeksforgeeks.org/quizzes/gatecompiler-design-pyq-2010-to-2025/), [CD GATE questions page](https://www.geeksforgeeks.org/compiler-design-gate-questions/).

**My links:** (NPTEL / textbook, add here)

---

## 1. Phases
Lexical analysis → syntax analysis → semantic analysis → intermediate code generation → code optimization → code generation, with the symbol table and error handler used throughout.
- The lexer turns characters into tokens (using a DFA). Counting tokens: keywords, identifiers, constants, strings, operators and punctuation each count as one token; whitespace and comments do not.
- Longest-match rule picks the longest valid lexeme; ties go to the earlier rule.

## 2–4. Grammars and top-down parsing
- Left recursion A → Aα | β becomes A → βA′, A′ → αA′ | ε. Left factoring removes a common prefix.
- FIRST(X): terminals that can begin strings derived from X (ε if X can vanish). FOLLOW(A): terminals that can appear right after A in some derivation ($ is in FOLLOW of the start symbol).
- LL(1): for A → α | β, FIRST(α) ∩ FIRST(β) = ∅; if ε ∈ FIRST(α) then FIRST(β) ∩ FOLLOW(A) = ∅. A left-recursive or ambiguous grammar is never LL(1).
- Table entry M[A, a]: use A → α for each a in FIRST(α); if ε ∈ FIRST(α), also for each a in FOLLOW(A).

## 5–6. Bottom-up parsing
- LR parser: left-to-right scan, rightmost derivation in reverse. Handle pruning.
- LR(0) items, closure and goto build the DFA of states. SLR(1) uses FOLLOW sets for reductions; CLR(1) uses LR(1) items with exact lookaheads; LALR(1) merges CLR states with identical cores.
- Power: LR(0) ⊂ SLR(1) ⊂ LALR(1) ⊂ CLR(1). LL(1) ⊂ LALR(1) ⊂ CLR(1). Number of states: LR(0) = SLR = LALR ≤ CLR.
- Conflicts: shift-reduce and reduce-reduce. LALR can introduce reduce-reduce conflicts (never shift-reduce conflicts) that CLR avoids.
- Operator precedence parsers work on operator grammars with no ε-productions and no two adjacent non-terminals.

## 7. Syntax-directed translation
- Synthesized attribute: computed from children. Inherited: from parent or left siblings.
- S-attributed: only synthesized attributes, evaluated bottom-up during LR parsing. L-attributed: inherited attributes depend only on the parent and left siblings; evaluated in one left-to-right depth-first pass.
- Every S-attributed definition is L-attributed.

## 8. Runtime environments
- Activation record: return address, parameters, locals, saved registers, control and access links. Stack allocation for procedure calls; heap for dynamic data.
- Parameter passing: by value (copy in), by reference (alias), by copy-restore (copy in, copy out at return), by name (textual substitution, re-evaluated each use).

## 9. Intermediate code and basic blocks
- Three-address code: at most one operator on the right (t1 = a + b). Represented as quadruples, triples or indirect triples.
- Leaders: the first instruction; any jump target; any instruction after a jump. A basic block runs from one leader to just before the next.
- Control flow graph: basic blocks as nodes, edges for possible control flow.

## 10–11. Optimization and data flow
- Local: constant folding, algebraic simplification, strength reduction (x·2 → x + x), dead-code elimination, common sub-expression elimination (within a block), peephole.
- Liveness (backward analysis): a variable is live if it may be used before being redefined. live-in(B) = use(B) ∪ (live-out(B) − def(B)); live-out(B) = ∪ live-in(successors).
- Reaching definitions (forward): out(B) = gen(B) ∪ (in(B) − kill(B)); in(B) = ∪ out(predecessors).
- Constant propagation replaces a variable by its known constant value; available expressions supports global CSE.

---

## Worked examples (all recomputed in code)

**E1: FIRST and FOLLOW.** Grammar E → TE′, E′ → +TE′ | ε, T → FT′, T′ → *FT′ | ε, F → (E) | id.
FIRST(E) = FIRST(T) = FIRST(F) = { ( , id }. FIRST(E′) = { +, ε }. FIRST(T′) = { *, ε }.
FOLLOW(E) = FOLLOW(E′) = { $, ) }. FOLLOW(T) = FOLLOW(T′) = { +, $, ) }. FOLLOW(F) = { *, +, $, ) }.
Every production pair satisfies the LL(1) condition, so this grammar is **LL(1)**.

**E2: State counts.** Grammar S′ → S, S → AA, A → aA | b. LR(0) / SLR: **7** states. CLR(1): **10** states. LALR(1): **7** states (merging CLR states with equal cores).

**E3: Leaders.** Code: 1: i = 0; 2: t1 = i * 4; 3: if i < 10 goto 6; 4: i = i + 1; 5: goto 2; 6: x = t1; 7: return. Leaders: 1, 2, 4, 6 → blocks {1}, {2, 3}, {4, 5}, {6, 7}.

**E4: Parameter passing.** Procedure p(a, b) { a = a + 1; b = b * 2 } called as p(x, x) with x = 2.
By value: x stays **2**. By reference: a and b alias x, so x = (2 + 1) × 2 = **6**. By copy-restore: a and b are separate copies; a = 3, b = 4; copy-back order a then b leaves x = **4** (the result depends on the copy-back order).

**E5: Token count.** `printf("i = %d, &i = %x", i, &i);` has **10** tokens: printf, (, the string, comma, i, comma, &, i, ), ;.

**E6: SDT value.** For 2 + 3 * 4 with E → E + T {E.val = E1.val + T.val}, T → T * F {T.val = T1.val × F.val}, the parse tree (with * binding tighter) gives **14**.

---

## Notes / flags
- Handbook gaps: see the **check** rows. I only have the contents-page photos, so confirm by flipping through pp. 273–299.
- You have no uploaded Compiler Design notes, so this file is built from scratch.
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying.
