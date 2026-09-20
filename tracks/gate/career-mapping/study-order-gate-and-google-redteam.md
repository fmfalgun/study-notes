# Study order: GATE 2027 and Google red-team / cybersecurity roles

Written 21 Sep 2026 from files we already saved (list at the end). No new research and no web lookups.

## What this plan assumes

- **Person:** the profile in `profile-fit-google.md` (M.Tech Cyber Security, wireless/IoT security, Python/Go/C++, Kerberos and Zero Trust, GATE 2023 CSE rank 3547; about 1 year of experience).
- **Goal:** rank high in **GATE CSE 2027** and become a credible candidate for **Google red-team / offensive-security roles** (the "threat intel and response" family, mostly Mandiant consulting, plus "Security Research").
- **Exam date:** **not in our files.** GATE is normally held in early February (general knowledge, please confirm). From 21 Sep 2026 that is about **19 weeks**; the week numbers below use that and must be shifted if the date differs.
- The ordering rules (prerequisites, what compounds with daily practice) are **my judgement**; the weights, counts and gaps come from the saved files.

## The two kinds of subject

| Kind | What it is | How to study it |
|---|---|---|
| **A. Strict-order theory** | A finite syllabus with a prerequisite chain (a later subject needs an earlier one). | Finish one, in order, then only revise. Do not run two of them in parallel. |
| **B. Consistency tracks** | Skills that improve with daily repetition and never "finish". | A fixed small dose **every day**, on top of A, from day 1 to the exam. |
| **C. Red-team hands-on** | Practical offensive skills that GATE never tests. | A fixed weekly block, ordered by what Google's red-team roles ask for. |

## Track A. Strict-order theory (finish each, then revise)

Order follows prerequisites first, then GATE weight. "Score" is the GATE priority score from `exam-priority-report.md` (average weightage plus 1.5 x complex questions over 8 sittings). "Google" is how many of the 169 live security roles need the topic (`gate-vs-google-security-topics.md`); "red team" refers to the 11 non-physical red-team/offensive/security-research roles in the stored descriptions.

| # | Subject | Why at this position | GATE (score) | Google / red-team link | Your status (profile) | Finish by |
|---|---|---|---|---|---|---|
| A1 | **C programming semantics: pointers, memory, arrays, recursion** (the "PDS core") | Everything below (COA, OS, compilers, exploit basics) assumes it | Tier 1 (51.6, highest of all) | C/C++ in 35 roles (25 as a minimum); memory corruption is the base of exploit work | C++ 3/5, "no substantial C/C++ project shown" | Week 3 |
| A2 | **Discrete mathematics**: logic, sets, relations, combinatorics, graphs, number theory | Feeds algorithms, theory of computation, DBMS relations, cryptography | Tier 1 (30.6) | Cryptography in 17 roles (14 as preferred) | Crypto applied 4/5; GATE-style problems not shown | Week 4 |
| A3 | **Digital logic** | Needed before COA | Tier 2 (15.0) | Hardware/firmware in 29 roles | Lab hardware 2/5 | Week 5 |
| A4 | **Computer organization and architecture** (CPU, assembly view, memory hierarchy, pipelining, I/O) | Needed before OS memory management; it is the assembly-level view for reverse engineering | Tier 2 (14.9) | Assembly / RE / exploit dev appear in 29 roles; a red-team "Security Research" role asks 5 years of reverse engineering | not shown | Week 7 |
| A5 | **Operating systems** (processes, threads, synchronization, deadlock, paging, files) | Needs A1 and A4 | Tier 2 (13.4) | OS/kernel/Linux internals in 21 roles; privilege escalation and sandbox escapes rely on it | Linux daily use 4/5 (theory not shown) | Week 9 |
| A6 | **Databases** (relational model, SQL, normalization, transactions, indexing) | Needs A2 | Tier 2 (16.8, the top Tier 2 score) | SQL in 17 roles; SQL injection is core web pentest | SQLite 3/5 | Week 11 |
| A7 | **Computer networks** (layers, IP/subnetting, TCP, routing, application protocols) | Quick for you; do it after the heavier subjects and keep it for numericals | Tier 2 (14.8) | Network security is in 56 roles (40 as a minimum) and in 10 of 11 red-team roles | **4/5, your strongest area** | Week 12 |
| A8 | **Theory of computation** | Prerequisite of compilers (regex, grammars) | Tier 3 (7.8) | Almost no Google demand (1 role) | not shown | Week 13 |
| A9 | **Compiler design** | Needs A8 and A1; also program analysis | Tier 2 (10.9) | 7 roles; useful for reverse engineering | not shown | Week 14 |

**Why the network subject is late even though it matches best:** you are already strong there, so it needs a short GATE-numericals pass, while A1-A6 have the biggest gap between your profile and their weight.

## Track B. Consistency (every day, from week 1 to the exam)

| Item | Why it is a "daily" skill | Evidence in our files | Daily dose (suggested) |
|---|---|---|---|
| **DSA and coding problems** in Python and C++ (arrays, heaps, trees, lists, stacks, recursion, then DP/graphs) | Improves only with repetition; it is the top GATE topic and Google's most common technical minimum | PDS score 51.6 and Algorithms 10.9; "coding experience in a general-purpose language" is a minimum in 68 of 169 roles; DSA named in 20 (4 as a minimum) | about 1.5 h, always |
| **Mathematics**: linear algebra, probability and statistics, calculus | Skill of doing many problems; not a syllabus you finish | Linear algebra score 14.2, probability 5.9; calculus flagged as a "wildcard" (count is probably an extraction artifact) | about 1 h |
| **PYQs and timed mocks** (GATE previous papers) | Speed and accuracy compound | previous-year analysis for 8 sittings in `topics/exam-analysis-report.md` (2021 unprocessed) | one timed section per week, full mock every 2-3 weeks from week 12 |
| **Aptitude** (GATE General Aptitude section) | Practice-based | listed as section 1 of the topic map | 20 min |
| **Security design and technical writing** (threat models, short reports) | Improves by writing regularly | "security design reviews" in 45 roles; "technical writing" in the Security Research minimum; "communication/presenting" in 96 roles | 20 min, 3 times a week |

If the time is short, cut the other tracks before you cut Track B.

## Track C. Red-team hands-on (weekly block, in this order)

What the stored descriptions say for the **11 non-physical red-team, offensive and security-research roles**:
- **Years:** 4 ask 3 years, 6 ask 5 years, 1 asks 8. So the realistic entry point is the four 3-year Mandiant offensive-consultant roles, or another 2-3 year security role first.
- **Named in most:** network security (10 of 11), scripting/coding (10), red-team or pentest experience (9 as a minimum), web-application security (9), cloud (9, usually as one item in a list of test types), OSCP-family certificate (9 as preferred, 0 as a minimum), tool development in Python, Go, C# or C/C++ (preferred).
- **Not the main ask:** reverse engineering and exploit development (3 and 2 of 11): only the Security Research roles (5 years of reverse engineering, published research).

| # | Skill | Why in this order | Gap from the profile | Books/paths on disk (from the books report) |
|---|---|---|---|---|
| C1 | **Web application pentest** (7 phases, OWASP classes, Burp-type work) | Named in 9 of 11; you already have a 7-phase study | appsec 2/5 | Web Application Hacker's Handbook 2nd Ed; Mastering Modern Web Penetration Testing; SANS SEC542 day PDFs |
| C2 | **Network and Active Directory attacks** | 10 of 11; builds on your strong networking and Kerberos | AD not shown | Penetration Testing (Weidman); Attacking Network Protocols; Nmap Cookbook; Hands-On Penetration Testing on Windows; Pro PowerShell DSC |
| C3 | **Cloud security attack and defence** (one GCP project: IAM, logging, misconfigurations) | Named in 9 of 11 and the biggest gap on your profile | cloud 1/5 | none of the listed books is a cloud book; use official cloud documentation (not in our files) |
| C4 | **Tool development** (Python, Go, C; small scanners, C2-style utilities) | Preferred in the Mandiant red-team roles; reuses your coding | Python 4/5, Go 3/5, C++ 3/5 | Black Hat Python; Black Hat Go; Gray Hat Python |
| C5 | **One offensive certification: OSCP** | 9 of 11 prefer an OSCP-family cert; cheapest hands-on proof (about $1,749-2,749) | none | `certifications-comparison.md` |
| C6 | **Reverse engineering and exploit development** | Only for Security Research roles; needs A1, A4, A5 first, so it naturally comes last | RE 1/5 | Hacking: The Art of Exploitation; Reverse Engineering for Beginners; Shellcoder's Handbook |

## The schedule (assuming about 19 weeks to the exam; adjust to the real date)

| Phase | Weeks | Track A (one at a time) | Track B (daily) | Track C (one block a week) |
|---|---|---|---|---|
| 1 | 1-4 | A1 C/pointers, A2 discrete maths | DSA, maths (linear algebra), aptitude | C1 web pentest |
| 2 | 5-9 | A3 digital logic, A4 COA, A5 OS | DSA (trees, graphs), maths (probability) | C1 finish, C2 AD/network |
| 3 | 10-14 | A6 databases, A7 networks, A8 TOC, A9 compilers | DSA (DP), timed sections | C2, start C3 cloud project |
| 4 | 15-19 | **Revision only**, weakest topics first (from mock results) | full mocks every 2-3 weeks, PYQs | one small block, keep C3 alive |
| After the exam | | (done) | keep DSA daily | C4 tools -> C5 OSCP -> C6 reverse engineering |

Milestones to check yourself: a timed mock score per section after phase 2 and 3; a written web-pentest report by week 9; a GCP mini-project by week 14; OSCP booked after the exam.

## Why this order gives the best result for both goals

1. **Overlap first.** The subjects that appear in both lists (C/DSA, discrete maths/crypto, COA, OS, networks, DBMS) are studied before the GATE-only ones (theory of computation, probability, calculus).
2. **Prerequisites are respected:** C -> COA -> OS -> (compilers, RE), discrete maths -> DBMS and algorithms, TOC -> compilers.
3. **Daily practice never stops** (Track B), because coding and maths are where marks and Google's coding round are won and lost.
4. **Red-team work runs in small weekly blocks from week 1**, because experience (5+ years in most roles) and cloud are the real gates for Google; the heavy OSCP and reverse-engineering effort waits until the exam is over.
5. **Skills you already have get the shortest slots** (networks, cryptography, Python); the biggest gaps in the profile with the highest weight get the earliest slots.

## What our files cannot tell us (so check before you commit to it)

- The **GATE 2027 date** and how many hours a day are available.
- Your **current score level per subject** (a diagnostic mock would replace my guess about which subjects need more time).
- **Google's interview content**: the job descriptions show requirements, not interview questions.
- Whether the **AI roles** matter as a second target: we never analysed AI job descriptions.
- Prices, exam formats and salary claims in the certification file come from web summaries checked on 20 Sep 2026.

## Files this is based on (all under `./tracks/gate/`)

`exam-priority-report.md`, `topics/gfg-gate-topic-map.md`, `topics/exam-analysis-report.md` - `career-mapping/gate-vs-google-security-topics.md`, `career-mapping/profile-fit-google.md`, `career-mapping/google-live/details-checklist.md` and `google-live/details/roles/*.json` (red-team subset counted from these) - `career-mapping/certifications-comparison.md` - `career-mapping/cybersecurity.md` (project ideas per subject).
