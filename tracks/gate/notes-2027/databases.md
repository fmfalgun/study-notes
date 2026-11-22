# Databases (DBMS) — GATE 2027 (CS + DA)

**Syllabus basis (CS):** ER-model; relational model (relational algebra, tuple calculus, SQL); integrity constraints; normal forms; file organization; indexing (B and B+ trees); transactions and concurrency control. DA's database block is similar in structure; confirm against the official DA PDF.
**Hbk** column: the Arihant Handbook DBMS chapter is pp. 117–181. Per-topic pages are not mapped yet. Marked `117–181*`; fill exact pages as you read.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
Strength: you said you know DB very well, so this file is built for quick revision.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ER model, weak entities, keys | 117–181* | [LMN DBMS](https://www.geeksforgeeks.org/dbms/last-minute-notes-dbms/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Relational model, integrity constraints, keys | 117–181* | [GATE CS Notes index](https://www.geeksforgeeks.org/gate/gate-cs-notes-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Relational algebra | 117–181* | [RA vs RC](https://www.geeksforgeeks.org/dbms/difference-between-relational-algebra-and-relational-calculus/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Tuple relational calculus | 117–181* | [GATE 2007 RA/TRC set](https://www.geeksforgeeks.org/dbms/database-management-systems-set-11/) · [GATE CS 2017 TRC](https://www.geeksforgeeks.org/gate-gate-cs-2017-set-1-question-36/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | SQL (joins, aggregates, nested queries) | 117–181* | [DBMS for GATE](https://www.geeksforgeeks.org/dbms/databases-dbms-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Functional dependencies, closure, keys | 117–181* | [DBMS Set 1 (FD example)](https://www.geeksforgeeks.org/database-management-system-set-1/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Normal forms (1NF to BCNF), decomposition | 117–181* | [Normalization](https://www.geeksforgeeks.org/dbms/introduction-of-database-normalization/) · [Normal-form PYQ quiz](https://www.geeksforgeeks.org/quizzes/decomposition-gate-cs-pyq-quiz/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | File organization, indexing | 117–181* | [GFG DBMS syllabus PDF](https://media.geeksforgeeks.org/courses/syllabus/bf4e4a2a2a3b0d2c9e6805afb7af7a3a.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | B and B+ trees | 117–181* | [DBMS PYQ 2010–2025](https://www.geeksforgeeks.org/quizzes/gatedbms-pyq-2010-to-2025/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Transactions, ACID, schedules, serializability | 117–181* | [Concurrency control](https://alphagtest.geeksforgeeks.org/concurrency-control-in-dbms/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Recoverability, locking (2PL), timestamps, deadlock | 117–181* | [DBMS Set 5](https://geeksforgeeks.org/database-management-systems-set-5) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [DBMS GATE PYQs by topic](https://www.geeksforgeeks.org/dbms/database-management-system-gate-questions/).

**My links:** (NPTEL / textbook, add here)

---

## 1–2. ER and relational model
- Entity set, attribute types (simple, composite, multivalued, derived), weak entity (needs an identifying owner and a partial key).
- Converting ER to tables: one table per strong entity; many-to-many relationships become their own table; one-to-many puts a foreign key on the "many" side.
- Super key ⊇ candidate key. Primary key is one chosen candidate key. Foreign key references a candidate key.
- Integrity: entity (primary key not null), referential (foreign key must match or be null), domain.

## 3–4. Relational algebra and calculus
- σ select, π project (removes duplicates), ⋈ join, × product, ∪, ∩, −, ρ rename, ÷ division.
- Cross product of R (m tuples) and S (n tuples): m·n. Union: between max(m, n) and m + n. Intersection: between 0 and min(m, n). Difference R − S: between 0 and m.
- Natural join on a common key: at most the size of the referencing relation. With no matching attributes it behaves like a cross product.
- Division R ÷ S gives tuples of R's extra attributes that pair with every tuple of S ("for all" queries).
- Tuple calculus is non-procedural. "For all" is ∀, "there exists" is ∃. Queries with ∀ over an empty set are true (check NULL-handling in 2017-style questions).

## 5. SQL
- WHERE filters rows before grouping; HAVING filters groups. Aggregates ignore NULLs, except COUNT(*).
- Comparisons with NULL give unknown, so `x = NULL` never selects rows; use `IS NULL`.
- Joins: inner keeps matches; left/right/full outer keep unmatched rows with NULLs.
- `IN` / `EXISTS` / `ANY` / `ALL` and correlated subqueries are usual GATE targets.

## 6. Functional dependencies
- Armstrong's axioms: reflexivity, augmentation, transitivity. Derived: union, decomposition, pseudo-transitivity.
- Attribute closure X⁺: repeatedly add the right side of any FD whose left side is inside the set. X is a super key if X⁺ = all attributes.
- Number of super keys: if the only candidate key has k attributes out of n, there are 2^(n−k) super keys.
- Canonical cover: remove extraneous attributes, then redundant FDs. Two FD sets are equivalent if each is implied by the other.

## 7. Normal forms
- 1NF: atomic values. 2NF: no partial dependency of a non-prime attribute on part of a key. 3NF: for every FD X → A, X is a super key or A is prime. BCNF: for every non-trivial FD X → Y, X is a super key.
- BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF. A relation with only two attributes is always in BCNF. If all attributes are prime, it is in 3NF (not necessarily BCNF).
- Lossless decomposition of R into R1, R2: R1 ∩ R2 must be a super key of R1 or of R2. BCNF decompositions are lossless but may not preserve dependencies; 3NF always has a lossless, dependency-preserving decomposition.

## 8–9. Indexing, B and B+ trees
- Dense index: one entry per record. Sparse: one per block. Primary index is on the sorted key; clustering index on a sorted non-key; secondary index on an unsorted field (must be dense).
- B+ tree of order p (internal node: up to p pointers and p−1 keys). Fit p by: p·P + (p−1)·K ≤ block size.
- Non-root internal node: at least ⌈p/2⌉ pointers, so ⌈p/2⌉ − 1 keys. Root: at least 2 pointers (if not a leaf).
- B+ tree keeps all data pointers in linked leaves, so range scans are fast; B-tree stores data in internal nodes too.
- Tree height h search costs about h + 1 block accesses.

## 10–11. Transactions and concurrency
- ACID: Atomicity, Consistency, Isolation, Durability.
- Conflict: two operations on the same item, different transactions, at least one write. Conflict serializable iff the precedence graph is acyclic. Conflict serializable implies view serializable (not conversely).
- Dirty read, non-repeatable read, phantom, lost update.
- Recoverable: a transaction commits only after every transaction it read from has committed. Cascadeless: reads only committed data. Strict: also no overwriting of uncommitted data. Strict ⊂ cascadeless ⊂ recoverable.
- 2PL (growing, then shrinking) guarantees conflict serializability but not deadlock-freedom, nor cascadeless unless strict 2PL. Timestamp ordering: serializable and deadlock-free, but may cause cascading rollbacks.
- Deadlock detection: wait-for graph cycle.

---

## Worked examples (all recomputed in code)

**E1: attribute closure and keys.** R(A,B,C,D) with AB → C, C → D, D → A. (AB)⁺ = {A,B,C,D}. Candidate keys: **AB, BC, BD**. Every attribute is prime. Every FD has a prime right side, so R is in **3NF**. But C → D has a left side (C) that is not a super key, so R is **not in BCNF**.

**E2: super keys.** R(A,B,C,D) where A is the only candidate key. Super keys are every set containing A: 2³ = **8**.

**E3: B+ tree order.** Block 1024 B, key 10 B, block pointer 6 B. Largest p with 6p + 10(p−1) ≤ 1024 is **p = 64**. So an internal node holds at most **63 keys**, and a non-root internal node holds at least ⌈64/2⌉ − 1 = **31 keys**. For leaves with a 6 B record pointer per key, (q−1)(10+6) + 6 ≤ 1024 also gives q = 64, so **63 keys** per leaf.

**E4: serializability.** Schedule r1(A) w1(A) r2(A) w2(A) r1(B) w1(B) r2(B) w2(B): the only edge is T1 → T2 (no cycle), so it is **conflict serializable** (equivalent to T1 then T2). Schedule r1(A) w2(A) w1(A): edges T1 → T2 and T2 → T1 form a cycle, so it is **not** conflict serializable.

**E5: relational algebra sizes.** R has 100 tuples, S has 200: R × S has **20000** tuples.

---

## Notes / flags
- The GFG normal-forms table words 3NF as "no transitive dependency of a non-prime attribute on a candidate key". That is equivalent to the "super key or prime" form in section 7; use whichever you solve faster.
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying.
- Handbook check: I haven't confirmed whether the Handbook has a separate file-organization section. Look for it near the indexing pages when you read.
