# GATE CS Exam Priority Report — Highest-Priority Links by Tier

Extends `topics/exam-analysis-report.md`. Rather than just ranking topics, this lists the
**actual highest-priority links per topic**, filtered down from the full lists in
`topics/gfg-gate-topic-map.md`, based on which specific sub-clusters the 27 analyzed
sittings (2007–2026, corrected from 24 — see `topics/exam-analysis-report.md`'s top-of-file
disclosure) actually hit most often. Everything not listed here still exists in
`topics/gfg-gate-topic-map.md` — it's just lower priority, not deleted.

This supersedes the prior 8-sitting (2022–2026) version of this report. **Tier placements
and scores below are carried over from the 24-sitting run** (not the corrected 27-sitting
one) for every topic except the sitting-count note on Computer Networks — a full recompute
for the corrected sitting count is a deferred follow-up, not completed in the pass that fixed
the sitting-count error itself. See `topics/exam-analysis-report.md`'s disclosure for exactly
what was and wasn't finished.

## Methodology

Topics are grouped into tiers by score, computed across the **17 recent-era (2014–2026)
sittings only** — the 7 older-era (2007–2013) sittings are analyzed in
`topics/exam-analysis-report.md` as historical reference but deliberately excluded from
this score, since 19 years of GATE CS format/syllabus drift would otherwise distort what to
study *now*:

```
score = avg_weightage% (mean of per-sitting %, out of ~55 subject questions) + (total complex-question count × 1.5)
```

**This is automated-classification data, not a manually-read paper like ISRO's equivalent
report.** Two things make this run's numbers worth extra caution even relative to the prior
8-sitting version: (1) the ~27% unclassified rate carries over unchanged, and (2) **two
lexicon bugs were caught and fixed mid-run** — `nat` was matching GATE's own "Numerical
Answer Type (NAT)" boilerplate instead of Network-Address-Translation content, and `nor` was
matching the English phrase "neither...nor" instead of NOR-gate content. Both were fixed
before these numbers were finalized (see `topics/exam-analysis-report.md`'s Methodology for
the full story), and fixing them **significantly changed Computer Networks and Digital
Logic's tier placement** relative to an unpublished first draft — Digital Logic fell out of
Tier 2 entirely once fixed. Treat tier placement as a starting filter, and treat Digital
Logic and Computer Networks specifically as topics where the underlying signal was noisier
than most. The full link sets remain in `topics/gfg-gate-topic-map.md` for once these
priority links are done.

**6 of the 17 recent-era sittings (2014, 2015, 2017-CS1, 2017-CS2, 2020, 2021) are
whole-paper keyword-density estimates, not verified per-question splits** — old/scanned
PDFs where OCR didn't support reliable question-boundary detection. See the analysis
report's Limitations before treating any single topic's score as precise.

---

## Tier 1 — Critical (score ≥ 25)

### 1. Programming & Data Structures (score 63.8 — highest weightage AND highest complex-question count, 35 complex hits)

Most-hit sub-clusters: arrays, stacks, pointers, heaps, queues, structs, binary trees/BSTs
— in that order of frequency, consistent with the prior 8-sitting run.

[Array Notes for GATE](https://www.geeksforgeeks.org/dsa/array-notes-for-gate-exam/) ·
[Stack Notes for GATE](https://www.geeksforgeeks.org/dsa/stack-notes-for-gate-exam/) ·
[Pointers](https://www.geeksforgeeks.org/c/c-pointers/) ·
[Binary Heap Notes for GATE](https://www.geeksforgeeks.org/dsa/binary-heap-notes-for-gate-exam/)
· [Queue Notes for GATE](https://www.geeksforgeeks.org/dsa/queue-notes-for-gate-exam/) ·
[Enum/Struct/Union](https://www.geeksforgeeks.org/cpp/structures-unions-and-enumerations-in-cpp/)
· [Trees Notes for GATE (BST, AVL)](https://www.geeksforgeeks.org/dsa/trees-notes-for-gate-exam/)
· [Linked List Notes for GATE](https://www.geeksforgeeks.org/dsa/linked-list-notes-for-gate-exam/)
· [Recursion Notes for GATE](https://www.geeksforgeeks.org/dsa/recursion-notes-for-gate-exam/)

### 2. Discrete Mathematics (score 32.9 — second-highest complex-question count, 16)

Most-hit sub-clusters: functions and relations dominate heavily, same as before, followed
by groups/algebraic structures.

[Classes of Functions](https://www.geeksforgeeks.org/maths/functions/) ·
[Types of Functions](https://www.geeksforgeeks.org/maths/types-of-functions/) ·
[Inverse Functions](https://www.geeksforgeeks.org/maths/inverse-functions/) ·
[Composition of Functions](https://www.geeksforgeeks.org/maths/composition-of-functions/) ·
[Relations and Types](https://www.geeksforgeeks.org/maths/relation-in-maths/) ·
[Equivalence Relations](https://www.geeksforgeeks.org/maths/equivalence-relations/) ·
[Groups](https://www.geeksforgeeks.org/engineering-mathematics/groups-discrete-mathematics/)
· [Partial Orders and Lattices](https://www.geeksforgeeks.org/engineering-mathematics/partial-orders-lattices/)

---

## Tier 2 — Important (score 10–25)

### 3. Databases (DBMS) (score 21.1)

Most-hit: SQL queries/joins, transactions, schedules — concurrency-control-heavy, same
pattern as the prior run, now with a clearer lead over the next tier.

[Introduction to SQL](https://www.geeksforgeeks.org/dbms/structured-query-language/) ·
[Joins](https://www.geeksforgeeks.org/sql/sql-join-set-1-inner-left-right-and-full-joins/) ·
[Transaction Isolation Levels](https://www.geeksforgeeks.org/dbms/transaction-isolation-levels-dbms/)
· [Types of Schedules](https://www.geeksforgeeks.org/dbms/types-of-schedules-in-dbms/) ·
[Conflict Serializability](https://www.geeksforgeeks.org/dbms/conflict-serializability-in-dbms/)
· [Keys (Candidate/Super/Primary/Alternate/Foreign)](https://www.geeksforgeeks.org/dbms/types-of-keys-in-relational-model-candidate-super-primary-alternate-and-foreign/)
· [Lossy/Lossless Decomposition](https://www.geeksforgeeks.org/dbms/lossless-decomposition-in-dbms/)
· [Functional Dependency & Attribute Closure](https://www.geeksforgeeks.org/dbms/functional-dependency-and-attribute-closure/)

### 4. Computer Organization & Architecture (score 16.8)

Most-hit: cache (by far the single most-hit COA keyword, 156 hits — genuinely dominant,
not a lexicon artifact like Networks/Digital Logic were), TLB, interrupts, DMA.

[Cache Memory](https://www.geeksforgeeks.org/computer-science-fundamentals/cache-memory/) ·
[Cache Organization](https://www.geeksforgeeks.org/computer-organization-architecture/cache-organization-set-1-introduction/)
· [CPU Cache vs TLB](https://www.geeksforgeeks.org/computer-organization-architecture/whats-difference-between-cpu-cache-and-tlb/)
· [Interrupt & DMA Mode](https://www.geeksforgeeks.org/computer-organization-architecture/io-interface-interrupt-dma-mode/)
· [DMA Controller](https://www.geeksforgeeks.org/computer-organization-architecture/direct-memory-access-dma-controller-in-computer-architecture/)
· [Instruction Formats (0/1/2/3-address)](https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-instruction-formats-zero-one-two-three-address-instruction/)

### 5. Linear Algebra (Eng. Math) (score 16.8 — tied with COA)

Most-hit: matrix operations/determinants dominate heavily over eigenvalues/LU decomposition.

[Matrix Operations](https://www.geeksforgeeks.org/maths/matrix-operations/) ·
[Determinants](https://www.geeksforgeeks.org/maths/what-is-determinant-of-a-matrix/) ·
[Properties of Determinants](https://www.geeksforgeeks.org/engineering-mathematics/properties-of-determinants-of-matrices/)
· [Eigenvalues and Eigenvectors](https://www.geeksforgeeks.org/engineering-mathematics/eigen-values/)
· [System of Linear Equations](https://www.geeksforgeeks.org/engineering-mathematics/system-linear-equations/)
· [LU Decomposition](https://www.geeksforgeeks.org/engineering-mathematics/l-u-decomposition-system-linear-equations/)

### 6. Operating System (score 16.3)

Most-hit: deadlock (top keyword), paging/page-tables, page replacement, semaphores.

[Deadlock Introduction](https://www.geeksforgeeks.org/operating-systems/introduction-of-deadlock-in-operating-system/)
· [Banker's Algorithm](https://www.geeksforgeeks.org/operating-systems/bankers-algorithm-in-operating-system-2/)
· [Paging](https://www.geeksforgeeks.org/operating-systems/paging-in-operating-system/) ·
[Page Table Entries](https://www.geeksforgeeks.org/operating-systems/page-table-entries-in-page-table/)
· [Page Replacement Algorithms](https://www.geeksforgeeks.org/operating-systems/page-replacement-algorithms-in-operating-systems/)
· [Semaphores](https://www.geeksforgeeks.org/operating-systems/semaphores-in-process-synchronization/)
· [Critical Section](https://www.geeksforgeeks.org/operating-systems/critical-section-in-synchronization/)

### 7. Computer Networks (score 14.0 as shown — not yet recomputed for the corrected sitting count, see below)

Most-hit (post-bug-fix): TCP (still the top genuine keyword, 80 hits), HTTP, DNS, OSPF,
subnetting, IP addressing, MAC address, UDP.

**Sitting-count correction note**: `topics/exam-analysis-report.md` now has verified
Networks-question counts across the corrected 20-sitting recent era (90 total, vs. 78/17
above) — 2015 turned out to be 3 sessions and 2021 turned out to be 2 sets, not 1 each. The
score above (14.0) still reflects the pre-correction 17-sitting count; a recomputed score
using the 20-sitting figure is a deferred follow-up. Directionally, more data at a similar
per-sitting rate (90/20=4.5 avg vs. 78/17=4.6 avg) suggests the corrected score will land
very close to 14.0, not meaningfully different — but treat that as an estimate, not a
verified recomputation.

[TCP Services & Segment Structure](https://www.geeksforgeeks.org/computer-networks/services-and-segment-structure-in-tcp/)
· [TCP Congestion Control](https://www.geeksforgeeks.org/computer-networks/tcp-congestion-control/)
· [TCP 3-Way Handshake](https://www.geeksforgeeks.org/computer-networks/tcp-3-way-handshake-process/)
· [Classful IP Addressing](https://www.geeksforgeeks.org/computer-networks/introduction-of-classful-ip-addressing/)
· [Subnetting](https://www.geeksforgeeks.org/computer-networks/introduction-to-subnetting/) ·
[OSPF Fundamentals](https://www.geeksforgeeks.org/computer-networks/open-shortest-path-first-ospf-protocol-fundamentals/)
· [DNS](https://www.geeksforgeeks.org/computer-networks/domain-name-system-dns-in-application-layer/)
· [MAC Address](https://www.geeksforgeeks.org/computer-networks/mac-address-in-computer-network/)

### 8. Compiler Design (score 13.1)

Most-hit: parsing/parsers (SLR and LALR both named directly), symbol tables.

[Introduction to Syntax Analysis](https://www.geeksforgeeks.org/compiler-design/introduction-to-syntax-analysis-in-compiler-design/)
· [SLR/CLR/LALR Parsers](https://www.geeksforgeeks.org/compiler-design/slr-clr-and-lalr-parsers-set-3/)
· [Shift-Reduce Parsers](https://www.geeksforgeeks.org/compiler-design/bottom-up-or-shift-reduce-parsers-set-2/)
· [Symbol Table](https://www.geeksforgeeks.org/compiler-design/symbol-table-compiler/) ·
[Lexical Analysis](https://www.geeksforgeeks.org/compiler-design/introduction-of-lexical-analysis/)

### 9. Algorithms (score 12.6)

Most-hit: binary search (top keyword), time complexity, BFS/DFS/graph traversal, MST.

[Searching/Sorting Notes for GATE](https://www.geeksforgeeks.org/dsa/searching-and-sorting-algorithm-notes-for-gate-exam/)
· [Asymptotic Analysis Notes for GATE](https://www.geeksforgeeks.org/dsa/asymptotic-analysis-of-algorithms-notes-for-gate-exam/)
· [Graph Algorithms Notes for GATE](https://www.geeksforgeeks.org/dsa/graph-based-algorithms-for-gate-exam/)
· [Prim's MST](https://www.geeksforgeeks.org/dsa/prims-minimum-spanning-tree-mst-greedy-algo-5/)
· [Recurrence Relations (Master Theorem)](https://www.geeksforgeeks.org/dsa/recurrence-relations-notes-for-gate-exam/)

### 10. Theory of Computation (score 10.0 — right at the Tier 2/3 boundary)

Most-hit: DFA design, recursively-enumerable languages, Turing machines, context-free
grammars — all closely bunched, no single dominant sub-cluster.

[Designing DFA Set 1](https://www.geeksforgeeks.org/theory-of-computation/designing-deterministic-finite-automata-set-1/)
· [Recursive/Recursively Enumerable Languages](https://www.geeksforgeeks.org/theory-of-computation/recursive-and-recursive-enumerable-languages-in-toc/)
· [Introduction to Turing Machine](https://www.geeksforgeeks.org/theory-of-computation/turing-machine-in-toc/)
· [What is Context-Free Grammar?](https://www.geeksforgeeks.org/theory-of-computation/what-is-context-free-grammar/)
· [Regular Expressions/Grammar/Languages](https://www.geeksforgeeks.org/theory-of-computation/regular-expressions-regular-grammar-and-regular-languages/)

---

## Tier 3 — Lower priority (score < 10)

### 11. Digital Logic (score 9.4 — dropped out of Tier 2 after the `nor` bug fix; see Methodology)

Most-hit (post-fix, genuine signal): counters, multiplexers, flip-flops, decoders/adders —
none individually dominant the way cache dominates COA or arrays dominate ProgDS. **This
topic's score moved more than any other when the lexicon bug was fixed (20.5 → 9.4 in the
unpublished first draft) — treat its exact rank with real caution, but the underlying
sub-clusters below are still legitimate GATE content worth knowing regardless of tier.**

[Counters (Ripple/Ring/Johnson)](https://www.geeksforgeeks.org/digital-logic/counters-in-digital-logic/)
· [Multiplexers](https://www.geeksforgeeks.org/digital-logic/multiplexers-in-digital-logic/) ·
[Flip-Flops (SR/JK/D/T)](https://www.geeksforgeeks.org/digital-logic/flip-flop-types-their-conversion-and-applications/)
· [Encoders & Decoders](https://www.geeksforgeeks.org/digital-logic/encoders-and-decoders-in-digital-logic/)
· [K-Map](https://www.geeksforgeeks.org/digital-logic/introduction-of-k-map-karnaugh-map/) ·
[Minimization of Boolean Functions](https://www.geeksforgeeks.org/digital-logic/minimization-of-boolean-functions/)

### 12. Probability & Statistics (Eng. Math) (score 8.4)

[Random Variable](https://www.geeksforgeeks.org/random-variable/) ·
[Conditional Probability](https://www.geeksforgeeks.org/maths/conditional-probability/) ·
[Mean, Median and Mode](https://www.geeksforgeeks.org/mean-median-and-mode/) ·
[Bayes's Formula](https://www.geeksforgeeks.org/maths/bayes-theorem/)

---

## Wildcard — likely under-counted, don't fully deprioritize

**Calculus** (score 0.4, only 4 hits across 985 recent-era questions, same story in the
older-era reference data). Per `topics/exam-analysis-report.md`'s Limitations, this is
almost certainly a text-extraction artifact — dense math notation `pdftotext`/OCR both drop
— not genuine near-zero weightage. Unlike Networks/Digital Logic, this under-count was
*not* traced to a specific fixable lexicon bug; it's a structural limitation of extracting
text from typeset mathematical notation. Keep:
[Limits](https://www.geeksforgeeks.org/maths/limits/) ·
[Lagrange's MVT](https://www.geeksforgeeks.org/engineering-mathematics/lagranges-mean-value-theorem/)
· [Application of Derivative](https://www.geeksforgeeks.org/maths/application-of-derivatives/)
in your rotation despite the low score.

---

## Recommended completion order

1. **Tier 1** — Programming & Data Structures → Discrete Mathematics
2. **Tier 2** — Databases → Computer Organization & Architecture → Linear Algebra →
   Operating System → Computer Networks → Compiler Design → Algorithms → Theory of
   Computation
3. **Tier 3** — Digital Logic → Probability & Statistics *(don't skip Digital Logic despite
   the tier drop — see the caution above; its sub-clusters are still real GATE content)*
4. **Wildcard** — Calculus (don't skip despite the low score — see above)

Once every priority link above is done, fall back to the full, unfiltered lists in
`topics/gfg-gate-topic-map.md` for the same topics, in the same order.
