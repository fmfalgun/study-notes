# ISRO Exam Priority Report — Highest-Priority Links by Tier

Extends `exam-analysis-report.md`. Rather than just ranking topics, this lists the **actual highest-priority links per subject**, filtered down from the full lists in `gfg-isro-topic-map.md`, based on which specific sub-areas the previous paper's questions (and its Complex-question cluster) actually hit. Everything not listed here still exists in `gfg-isro-topic-map.md` — it's just lower priority, not deleted.

## Methodology

Topics are grouped into tiers by:
```
score = weightage% (share of Part A, 80 Qs) + (complex-question count × 1.5)
```
Within each topic, sub-section links are filtered to what the prior paper's question-mix and Complex-question cluster (Banker's algorithm, IPSec/Hamming/TCP math, triple integral, planar graphs, concurrency/isolation, etc. — per `exam-analysis-report.md`) actually points to. One exam's data — treat as a starting filter, not a ceiling; the full link sets remain in `gfg-isro-topic-map.md` for once these priority links are done.

**Role-difference caveat**: the previous paper was for a different role/posting than the one being prepped for now — same core 11-topic syllabus, but "shadow topics" (Software Engineering, Big Data, Compiler Design, Cloud/Virtualization) are more likely an artifact of that role's paper-setter. Kept separate below, not blended into the tiers.

---

## Tier 1 — Critical

### 1. Mathematics (score 17.3 — highest weightage, 4 Complex Qs: permutations, planar graphs, triple integral)

Syllabus names 4 sub-parts (Discrete Mathematics, Linear Algebra, Calculus, Probability & Statistics) — priority links per part:

**Discrete Mathematics — Combinatorics** *(Q16, Q17, Q32 — confirmed gap)*: [Combinatorics Basics](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-combinatorics-basics/) · [Binomial Coefficients](https://www.geeksforgeeks.org/maths/coefficient-in-binomial-expansion/) · [Generalized PnC Set 1](https://www.geeksforgeeks.org/engineering-mathematics/generalized-pnc-set-1/) · [Pigeonhole Principle](https://www.geeksforgeeks.org/engineering-mathematics/discrete-mathematics-the-pigeonhole-principle/)

**Discrete Mathematics — Graphs** *(Q59, Q60 — "planar graphs" is the named Complex-question type)*: [Graph Theory Basics](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-graph-theory-basics/) · [Planar Graphs and Coloring](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-planar-graphs-graph-coloring/) · [Graph Isomorphisms and Connectivity](https://www.geeksforgeeks.org/engineering-mathematics/graph-isomorphisms-connectivity/) · [Matching in Graph Theory](https://www.geeksforgeeks.org/engineering-mathematics/matching-graph-theory/) · [Euler and Hamiltonian Paths](https://www.geeksforgeeks.org/engineering-mathematics/euler-hamiltonian-paths/)

**Linear Algebra** *(Q73, Q74 — confirmed zero notes coverage per `math-crossover-analysis.md`)*: [Introduction to Matrix](https://www.geeksforgeeks.org/maths/introduction-to-matrices/) · [Determinants](https://www.geeksforgeeks.org/maths/what-is-determinant-of-a-matrix/) · [Eigenvalues and Eigenvectors](https://www.geeksforgeeks.org/engineering-mathematics/eigen-values/) · [System of Linear Equations](https://www.geeksforgeeks.org/engineering-mathematics/system-linear-equations/) · [LU Decomposition](https://www.geeksforgeeks.org/engineering-mathematics/l-u-decomposition-system-linear-equations/)

**Calculus** *(Q75 — the "triple integral" Complex question; mean value theorem and integration are named syllabus items)*: [Limits](https://www.geeksforgeeks.org/maths/limits/) · [Continuity](https://www.geeksforgeeks.org/maths/continuity-of-functions/) · [Differentiability](https://www.geeksforgeeks.org/maths/differentiability-of-a-function-class-12-maths/) · [Lagrange's MVT](https://www.geeksforgeeks.org/engineering-mathematics/lagranges-mean-value-theorem/) · [Absolute Minima and Maxima](https://www.geeksforgeeks.org/maths/absolute-minima-and-maxima/) · [Indefinite Integrals](https://www.geeksforgeeks.org/maths/indefinite-integrals/)

**Probability & Statistics** *(Q87)*: [Random Variable](https://www.geeksforgeeks.org/random-variable/) · [Normal Distribution](https://www.geeksforgeeks.org/maths/normal-distribution/) · [Binomial Distribution](https://www.geeksforgeeks.org/maths/binomial-distribution/) · [Mean, Median and Mode](https://www.geeksforgeeks.org/mean-median-and-mode/) · [Conditional Probability](https://www.geeksforgeeks.org/maths/conditional-probability/) · [Bayes's Formula](https://www.geeksforgeeks.org/maths/bayes-theorem/)

---

### 2. Operating System (score 14.5 — 3 Complex Qs: Banker's algorithm, page replacement)

**Deadlock** *(Q55/Q56 Complex — "Banker's algorithm" named directly)*: [Deadlock Introduction](https://www.geeksforgeeks.org/operating-systems/introduction-of-deadlock-in-operating-system/) · [Banker's Algorithm](https://www.geeksforgeeks.org/operating-systems/bankers-algorithm-in-operating-system-2/) · [Safety Algorithm](https://www.geeksforgeeks.org/operating-systems/program-bankers-algorithm-set-1-safety-algorithm/) · [Resource Allocation Graph](https://www.geeksforgeeks.org/operating-systems/resource-allocation-graph-rag-in-operating-system/)

**Virtual Memory & Paging** *(Q55/Q56 Complex — "page replacement" named directly)*: [Virtual Memory](https://www.geeksforgeeks.org/operating-systems/virtual-memory-in-operating-system/) · [Page Replacement Algorithms](https://www.geeksforgeeks.org/operating-systems/page-replacement-algorithms-in-operating-systems/) · [Paging](https://www.geeksforgeeks.org/operating-systems/paging-in-operating-system/) · [Demand Paging](https://www.geeksforgeeks.org/operating-systems/what-is-demand-paging-in-operating-system/)

**CPU Scheduling & Synchronization** *(Q18, Q33, Q34, Q53, Q54, Q76 — remaining Easy/Medium spread)*: [CPU Scheduling](https://www.geeksforgeeks.org/operating-systems/cpu-scheduling-in-operating-systems/) · [Process Synchronization](https://www.geeksforgeeks.org/operating-systems/introduction-of-process-synchronization/) · [Semaphores](https://www.geeksforgeeks.org/operating-systems/semaphores-in-process-synchronization/) · [Mutex vs Semaphore](https://www.geeksforgeeks.org/operating-systems/mutex-vs-semaphore/)

---

### 3. Computer Networks (score 13.25 — 3 Complex Qs: IPSec, Hamming code, TCP window math)

**Data Link Layer** *(Q46/Q47 Complex — "Hamming code" named directly)*: [Hamming Code](https://www.geeksforgeeks.org/computer-networks/hamming-code-in-computer-network/) · [Framing](https://www.geeksforgeeks.org/computer-networks/framing-in-data-link-layer/) · [Sliding Window Protocol](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocol-set-1/) · [Multiple Access Protocols](https://www.geeksforgeeks.org/computer-networks/multiple-access-protocols-in-computer-network/)

**Transport Layer** *(Q71 Complex — "TCP window math")*: [TCP 3-Way Handshake](https://www.geeksforgeeks.org/computer-networks/tcp-3-way-handshake-process/) · [TCP Congestion Control](https://www.geeksforgeeks.org/computer-networks/tcp-congestion-control/) · [Flow Control in Data Link Layer](https://www.geeksforgeeks.org/computer-networks/flow-control-in-data-link-layer/)

**Network Layer** *(Q9, Q28, Q40, Q70 — Medium spread; "IPSec" was named in methodology but has no dedicated GFG page in `gfg-isro-topic-map.md` yet — flagged, needs separate lookup)*: [IP Addressing (Classful/Classless)](https://www.geeksforgeeks.org/computer-networks/introduction-of-classful-ip-addressing/) · [Classless Inter-Domain Routing (CIDR)](https://www.geeksforgeeks.org/computer-networks/classless-inter-domain-routing-cidr/) · [Subnetting/Supernetting](https://www.geeksforgeeks.org/computer-networks/introduction-to-subnetting/) · [NAT](https://www.geeksforgeeks.org/computer-networks/network-address-translation-nat/) · [Routing Algorithms](https://www.geeksforgeeks.org/computer-networks/classification-of-routing-algorithms/)

---

### 4. Databases (score 10.25 — 1 Complex Q: concurrency/isolation)

**Transactions & Concurrency** *(Q72 Complex — "concurrency/isolation" named directly)*: [Concurrency Control](https://www.geeksforgeeks.org/dbms/concurrency-control-in-dbms/) · [ACID Properties](https://www.geeksforgeeks.org/dbms/acid-properties-in-dbms/) · [Conflict Serializability](https://www.geeksforgeeks.org/dbms/conflict-serializability-in-dbms/) · [Two Phase Locking](https://www.geeksforgeeks.org/dbms/two-phase-locking-protocol/)

**SQL & Relational Basics** *(Q10, Q11, Q29, Q30, Q48, Q49 — remaining Easy/Medium spread)*: [Introduction to SQL](https://www.geeksforgeeks.org/dbms/structured-query-language/) · [Joins](https://www.geeksforgeeks.org/sql/sql-join-set-1-inner-left-right-and-full-joins/) · [Database Normalization](https://www.geeksforgeeks.org/dbms/introduction-of-database-normalization/) · [Keys](https://www.geeksforgeeks.org/dbms/types-of-keys-in-relational-model-candidate-super-primary-alternate-and-foreign/)

---

### 5. Cyber Security (score 10.0 — no Complex Qs, but 10% weightage; zero GATE/GFG coverage, so this list already **is** the filtered set)

**Cryptography (Classical → RSA/Diffie-Hellman)**: [sobolevn/awesome-cryptography](https://github.com/sobolevn/awesome-cryptography)

**Network Security — Firewalls, IDS/IPS**: [OISF/suricata](https://github.com/OISF/suricata) (read docs/README for concepts, not the C source)

**OWASP Top 10**: [swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

**Incident Response**: [The-Art-of-Hacking/h4cker — `cybersecurity-domains/defensive-security`](https://github.com/The-Art-of-Hacking/h4cker/tree/master/cybersecurity-domains/defensive-security)

*(Full secondary list — `pFarb/awesome-crypto-papers`, `infoslack/awesome-web-hacking`, `brootware/awesome-cyber-security-university` — still in `gfg-isro-topic-map.md` §11 if the above four leave gaps.)*

---

## Tier 2 — Important

### 6. Computer Organization & Architecture (score 8.75 — all Easy/Medium, spread across the whole topic)

*(Q12, Q13, Q14, Q31, Q50, Q51, Q52 — no single sub-area dominates, so priority = the classic GATE-heavy clusters)*: [Machine Instructions](https://www.geeksforgeeks.org/computer-organization-architecture/machine-instructions/) · [Addressing Modes](https://www.geeksforgeeks.org/computer-organization-architecture/addressing-modes/) · [Cache Memory](https://www.geeksforgeeks.org/computer-science-fundamentals/cache-memory/) · [Cache Organization](https://www.geeksforgeeks.org/computer-organization-architecture/cache-organization-set-1-introduction/) · [Pipelining Set 1](https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-and-architecture-pipelining-set-1-execution-stages-and-throughput/) · [Pipelining Set 2 (Hazards)](https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-and-architecture-pipelining-set-2-dependencies-and-data-hazard/)

### 7. Theory of Computation (score 7.5 — all Medium, evenly spread)

*(Q7, Q8, Q35, Q36, Q58, Q65 — no Complex, no Easy, consistent Medium across FA/Grammar/TM)*: [Introduction to Finite Automata](https://www.geeksforgeeks.org/theory-of-computation/introduction-of-finite-automata/) · [Regular Expressions/Grammar/Languages](https://www.geeksforgeeks.org/theory-of-computation/regular-expressions-regular-grammar-and-regular-languages/) · [What is Context-Free Grammar?](https://www.geeksforgeeks.org/theory-of-computation/what-is-context-free-grammar/) · [Pumping Lemma](https://www.geeksforgeeks.org/theory-of-computation/pumping-lemma-in-theory-of-computation/) · [Introduction to Turing Machine](https://www.geeksforgeeks.org/theory-of-computation/turing-machine-in-toc/) · [Decidability](https://www.geeksforgeeks.org/theory-of-computation/decidability-and-undecidability-in-toc/)

### 8. Data Structures & Algorithms (score 6.25 — mostly Easy)

*(Q1, Q21, Q22, Q37, Q38 — all Easy/Medium, no Complex)*: [Array Notes for GATE](https://www.geeksforgeeks.org/dsa/array-notes-for-gate-exam/) · [Stack Notes for GATE](https://www.geeksforgeeks.org/dsa/stack-notes-for-gate-exam/) · [Linked List Notes for GATE](https://www.geeksforgeeks.org/dsa/linked-list-notes-for-gate-exam/) · [Searching/Sorting Notes for GATE](https://www.geeksforgeeks.org/dsa/searching-and-sorting-algorithm-notes-for-gate-exam/)

### 9. AI and Machine Learning (score 6.25 — all Easy)

*(Q4, Q5, Q62, Q63, Q64 — all Easy, definitional level; same priority pick already flagged in `gfg-isro-topic-map.md` §10)*: [Linear Regression](https://www.geeksforgeeks.org/machine-learning/linear-regression-python-implementation/) · [Logistic Regression](https://www.geeksforgeeks.org/machine-learning/understanding-logistic-regression/) · [K-Nearest Neighbor](https://www.geeksforgeeks.org/machine-learning/k-nearest-neighbours/) · [Naive Bayes Classifier](https://www.geeksforgeeks.org/machine-learning/naive-bayes-classifiers/) · [K-Means/K-Medoid](https://www.geeksforgeeks.org/machine-learning/ml-k-medoids-clustering-with-example/) · [BFS](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/) · [DFS](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/) · [A* Search](https://www.geeksforgeeks.org/dsa/a-search-algorithm/)

---

## Tier 3 — Lower priority / wildcard

### 10. Programming Language (score 1.25 — only 1/95 questions ever)

*(Q27 Medium only)*: [Introduction to C](https://www.geeksforgeeks.org/c/getting-started-with-c/) · [Pointers](https://www.geeksforgeeks.org/c/c-pointers/) · [Introduction to Python](https://www.geeksforgeeks.org/python/introduction-to-python/) · [Python Functions](https://www.geeksforgeeks.org/python/python-functions/)

### 11. Image and Vision Processing (score 0 — zero Qs, but explicit page-1 syllabus item — a wildcard, not a true zero)

No GFG/GATE coverage exists (gap, per `gfg-isro-topic-map.md` §9). Do not front-load time here; if time allows, look up a general (non-GATE) image-processing source directly rather than pulling from these two topic-map files.

---

## Shadow Topics — kept separate (role-difference artifact, not core syllabus)

Absent from the official syllabus PDF; per the role-difference caveat, secondary to all 11 ranked topics above.

**Software Engineering** *(8.75%, 1 Complex Q — biggest shadow topic)*: [Software Engineering Tutorial (hub)](https://www.geeksforgeeks.org/software-engineering/software-engineering/) · [SDLC — What is it and its phases](https://www.geeksforgeeks.org/software-engineering/what-is-sdlc-model-and-its-phases/) · [Agile SDLC](https://www.geeksforgeeks.org/software-engineering/agile-sdlc-software-development-life-cycle/)

**Big Data** *(6.25%, all Easy)*: [Hadoop Tutorial](https://www.geeksforgeeks.org/big-data/hadoop-tutorial/) · [HDFS Introduction](https://www.geeksforgeeks.org/big-data/introduction-to-hadoop-distributed-file-systemhdfs/) · [MapReduce in Hadoop](https://www.geeksforgeeks.org/big-data/map-reduce-in-hadoop/)

**Compiler Design** *(3.75%, all Easy)*: see `gfg-isro-topic-map.md` Bonus section.

**Cloud Computing / Virtualization** *(2.5%, smallest shadow topic)*: [Cloud Computing Tutorial](https://www.geeksforgeeks.org/cloud-computing-tutorial/) · [Virtualization in Cloud Computing and Types](https://www.geeksforgeeks.org/cloud-computing/virtualization-cloud-computing-types/)

---

## Recommended completion order

1. **Tier 1** — Mathematics → OS → Computer Networks → Databases → Cyber Security
2. **Tier 2** — CO&A → Theory of Computation → DSA → AI/ML
3. **Tier 3** — Programming Language → Image/Vision Processing
4. **Shadow topics** — Software Engineering → Big Data → Compiler Design → Cloud/Virtualization

Once every priority link above is done, fall back to the full, unfiltered lists in `gfg-isro-topic-map.md` for the same topics, in the same order.
