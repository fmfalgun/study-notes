# Theory of Computation — Notes

---
## Introduction of Finite Automata — Notes

**1. Formal definition (5-tuple)**
`{ Q, Σ, q, F, δ }` — a finite automaton is a tuple where:
- `Q`: finite set of states
- `Σ`: set of input symbols
- `q`: initial state
- `F`: set of final states
- `δ`: transition function
*For a DFA specifically: `δ : Q × Σ → Q` (exactly one resulting state).*

**2. DFA vs NFA**
- DFA: "for each input symbol, the machine transitions to one and only one state"; "DFA does not allow any null transitions."
- NFA: "It can transition to multiple states for the same input"; "It allows null (ϵ) moves."

**3. Worked example — DFA accepting strings ending in 'a'**
`Σ = {a, b}`, `Q = {q0, q1}`, `F = {q1}`
```
Transition table:
        a       b
q0  ->  q1      q0
q1  ->  q1      q0
```
"if the string ends in 'a', the machine reaches state q1, which is an accepting state."

**4. Worked example — NFA accepting strings ending in 'a'**
Same `Σ`, `Q`, `F` as above.
```
Transition table:
        a           b
q0  ->  {q0,q1}     q0
q1  ->  φ           φ
```
"if any transition leads to an accepting state, the string is accepted." (Note: NFA branches on 'a' from q0 into two simultaneous states, then any branch reaching q1 on end-of-string accepts.)

**Priority for your prep:** High — the 5-tuple definition and DFA-vs-NFA distinction are near-certain MCQ material; memorize the transition table format above since ISRO tends to ask "which string is accepted/rejected by this DFA" style questions.

---
## Regular Expressions, Regular Grammar and Regular Languages — Notes

**5. Regular expression — recursive definition**
A regular expression represents a regular language by these rules (as stated on page):
1. `ϵ` is a regular expression representing the language `{ϵ}` (the empty string).
2. Any symbol `a` from alphabet `Σ` is a regular expression, representing the language `{a}`.
3. Union `(a + b)` is a regular expression if `a` and `b` are regular expressions, representing the language `{a, b}`.
4. Concatenation `(ab)` is a regular expression if `a` and `b` are regular expressions.
5. Kleene star `(a*)` is a regular expression, meaning zero or more occurrences of `a`.

**6. Worked example — regex patterns**
- `ab*` generates: `{a, ab, abb, abbb, abbbb, ...}`
- `[aeiou]*[bcdfghjklmnpqrstvwxyz]*` generates: `{ε, a, aou, aiou, b, abcd, ...}`

**7. Regular grammar**
Components: Terminals (e.g. `a, b`), Non-terminals (e.g. `S, A`), Production rules transforming non-terminals into terminals or other non-terminals.
- Right-linear grammar example (verbatim from page): `S -> aS | bS | ε`
- Left-linear grammar form: `A -> Ba` or `A -> a`

**8. Regular languages**
"Regular languages are the class of languages that can be represented using finite automata, regular expressions, or regular grammar." Closed under union, intersection, concatenation, Kleene closure, and complement.

**9. Chomsky hierarchy**
Not covered on this page — no worked example / levels given here (see CFG notes below for where the hierarchy actually appears via context-free grammar).

**Priority for your prep:** High — regex-to-language pattern matching (`ab*`, character-class regex) is a classic ISRO objective-question style; know the right-linear grammar form `S -> aS | bS | ε` cold since it maps directly to a DFA/NFA.

---
## What is Context-Free Grammar? — Notes

**10. Formal 4-tuple definition**
`G = (V, T, P, S)` where:
- `V`: finite set of variables (non-terminals / syntactic categories)
- `T`: finite set of terminals — symbols that form strings of the language
- `P`: set of production rules representing the recursive definition of the language
- `S`: start symbol representing the language being defined

**11. Production rule notation**
`G -> (V∪T)*`, where `G ∊ V`. "The left-hand side can only be a Variable, it cannot be a terminal. But on the right-hand side ... it can be a Variable or Terminal or both combination."

**12. Worked example — arithmetic expressions grammar**
```
E → int
E → E Op E
E → (E)
Op → +
Op → -
Op → *
Op → /
```
Example derivation (verbatim): `E ⇒ E Op E ⇒ E Op int ⇒ int Op int ⇒ int / int`

**13. Worked example — palindromes**
`S → ε | a | b | aSa | bSb`

**14. Worked example — balanced parentheses**
`S → ε | (S) | SS`

**Priority for your prep:** Very high — CFG 4-tuple and derivation notation appear constantly; the palindrome grammar `S → ε | a | b | aSa | bSb` and balanced-parens grammar `S → ε | (S) | SS` are exactly the kind of "give the grammar for language X" question ISRO asks.

---
## Pumping Lemma in Theory of Computation — Notes

**15. Formal lemma statement**
"for any regular language L, there exists an integer n such that any string `x ∈ L` with length `|x| ≥ n` can be divided into `x = uvw`, where `u, v, w ∈ Σ*`, satisfying the following conditions:
```
|uv| ≤ n
|v| ≥ 1
For all i ≥ 0, u vⁱ w ∈ L
```"

**16. Worked example — proving `L = {0ⁿ1ⁿ | n ≥ 0}` is NOT regular (proof by contradiction)**
"If (1) and (2) hold then `x = 0ⁿ1ⁿ = uvw` with `|uv| ≤ n` and `|v| ≥ 1`. So, `u = 0ᵃ, v = 0ᵇ, w = 0ᶜ1ⁿ` where: `a + b ≤ n, b ≥ 1, c ≥ 0, a + b + c = n`. But, then (3) fails for `i = 0`: `uv⁰w = uw = 0^(a+c)1ⁿ ∉ L`, since `a + c ≠ n`."
This contradiction (pumping down to `i=0` produces a string with unequal 0s and 1s) shows `L` cannot be regular.

**Priority for your prep:** Very high — pumping lemma proofs (`0ⁿ1ⁿ` style) are a guaranteed descriptive/objective question. Memorize the exact `u=0ᵃ, v=0ᵇ, w=0ᶜ1ⁿ` decomposition and the `i=0` contradiction step — this is the standard template you reuse for other non-regular languages (e.g. `a^n b^n c^n`, `ww`).

---
## Turing Machine in TOC — Notes

**17. Formal definition (7 components)**
A Turing Machine is defined by: "A finite set of states (Q). An input alphabet (Σ). A tape alphabet (Γ) that includes Σ. A transition function (δ). A start state (q0). A blank symbol (B). A set of final states (F)."

**18. Worked example — TM for `L = {0ⁿ1ⁿ | n ≥ 1}`**
```
Q = {q0, q1, q2, q3}   (q0 is the initial state)
Γ = {0, 1, X, Y, B}    (B = blank; X marks a processed 0, Y marks a processed 1)
Σ = {0, 1}
F = {q3}
```
The page traces execution on input `0011`: the machine processes each symbol through sequential transitions (matching an unmarked `0` with an unmarked `1`, marking each as it goes), ultimately reaching accept state `q3` with the head pointing at a blank once all `0`s and `1`s are paired off.

**Priority for your prep:** High — the 7-tuple TM definition (note it has 7 components, not 5 like FA) is a common "how many tuples" trap question; the `0ⁿ1ⁿ` TM (mark-and-match via `X`/`Y`) is the standard worked example to reproduce for descriptive answers.

---
## Decidability and Undecidability in TOC — Notes

**19. Definitions**
- Decidable: "A decision problem P is said to be decidable if there exists an algorithm (or Turing Machine) that always halts and correctly determines the answer for every input."
- Undecidable: "A decision problem P is said to be undecidable if there is no algorithm or computational procedure that can correctly determine the answer for every possible input."

**20. Named decidable examples (from page)**
1. Acceptance problem for DFA — "Given a DFA and an input string, determine whether the DFA accepts the string."
2. Emptiness problem for DFA — "Given a DFA, determine whether it accepts at least one string."
3. Equivalence problem for DFA — "Given two DFAs, determine whether both accept the same language."

**21. Named undecidable examples (from page)**
1. The Halting Problem — "Given a program and an input, determine whether the program will halt or run forever."
2. State Entry Problem — "Given a Turing Machine M and an input string w, determine whether a specific state Q is ever reached during the computation."

**Priority for your prep:** High — ISRO loves a "which of the following is decidable/undecidable" MCQ; memorize that DFA acceptance/emptiness/equivalence are all decidable, while Halting Problem and TM state-reachability are undecidable. Note the asymmetry: decidability results for DFA don't carry over to Turing Machines in general.

---
## Overall Priority for Your Prep

1. **CFG production rules + derivations** and **Pumping Lemma proof template** — highest yield, both MCQ and descriptive.
2. **Finite Automata 5-tuple + DFA/NFA transition tables** — frequent, easy marks if the table format is memorized exactly.
3. **Turing Machine 7-tuple** — watch the tuple-count trap versus FA's 5-tuple.
4. **Decidable vs undecidable problem lists** — memorize the specific named examples (DFA acceptance/emptiness/equivalence = decidable; Halting Problem = undecidable) rather than reasoning from first principles under time pressure.
5. **Regular expressions / regular grammar** — lower marginal yield alone, but underpins FA and pumping-lemma questions, so review after the above.

*Note: the Regular Expressions/Grammar/Languages page did not cover the Chomsky hierarchy explicitly — flagged as a gap; if ISRO questions reference Chomsky hierarchy levels (Type 0–3), supplement from another source since it was not present on the fetched GFG page.*
