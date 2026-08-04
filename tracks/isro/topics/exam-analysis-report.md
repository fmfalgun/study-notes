# ISRO SC Computer Science Engineering — Previous Attempt Paper Analysis

Analysis of `isro-prev-attempt-1/` (Set C, 95 questions captured) mapped against the official syllabus (`Syllabus for Post Code 07 and 08_SciEngr SC_Computer Science Engineering.pdf`).

## Overview

- **Part A (Domain-specific, Q1–80)** maps to the 11 syllabus topics — but several questions came from topics not in the official syllabus PDF (flagged below).
- **Part B (Q81–95, 15 questions)** is a General Aptitude/Reasoning section — not covered by the CS syllabus at all, separate prep track needed.

## Part A: Topic-wise Weightage (out of 80)

| Syllabus Topic | Count | % | Easy | Medium | Complex |
|---|---|---|---|---|---|
| Mathematics (Discrete/Linear Algebra/Calculus incl. Graph theory Q59,60) | 9 | 11.3% | 1 | 4 | 4 |
| Operating System | 8 | 10.0% | 4 | 1 | 3 |
| Cyber Security | 8 | 10.0% | 6 | 2 | 0 |
| Computer Organization & Architecture | 7 | 8.75% | 1 | 6 | 0 |
| Databases | 7 | 8.75% | 3 | 3 | 1 |
| Computer Networks | 7 | 8.75% | 0 | 4 | 3 |
| Theory of Computation | 6 | 7.5% | 0 | 6 | 0 |
| Data Structures & Algorithms | 5 | 6.25% | 3 | 2 | 0 |
| AI and Machine Learning | 5 | 6.25% | 5 | 0 | 0 |
| Programming Language (C/Python, incl. C++) | 1 | 1.25% | 0 | 1 | 0 |
| Image and Vision Processing | 0 | 0% | – | – | – |
| **Subtotal (syllabus topics)** | **63** | **78.75%** | | | |

### Topics that appeared but are NOT in the official syllabus

| Extra Topic | Count | % | Easy | Medium | Complex |
|---|---|---|---|---|---|
| Software Engineering (SDLC, risk mgmt, testing, CMM, function points) | 7 | 8.75% | 5 | 1 | 1 |
| Big Data (Hadoop, HDFS, Flink, NoSQL storage) | 5 | 6.25% | 5 | 0 | 0 |
| Compiler Design (lexer, parser, yacc, JVM) | 3 | 3.75% | 3 | 0 | 0 |
| Cloud Computing / Virtualization (hypervisors, elasticity) | 2 | 2.5% | 1 | 1 | 0 |
| **Subtotal (non-syllabus)** | **17** | **21.25%** | | | |

**Key finding:** Image/Vision Processing (syllabus item 9) got zero questions in this paper, while Software Engineering — completely absent from the syllabus — got 7 questions (as much as OS or Cyber Security). Big Data and Compiler Design also appear despite no syllabus mention. Worth prepping these as "shadow topics."

## Part B: Aptitude/Reasoning (Q81–95, 15 questions)

| Sub-type | Count | Easy | Medium |
|---|---|---|---|
| Quantitative/Numerical (ratios, calendar, volume, linear eq.) | 5 | 4 | 1 |
| Verbal Reasoning (syllogisms) | 4 | 0 | 4 |
| Non-verbal Reasoning (pattern/figure/mirror) | 4 | 0 | 4 |
| Data Interpretation (Venn diagram) | 1 | 0 | 1 |
| Numerical Series | 1 | 0 | 1 |

No "complex" items in this section — it's designed to be quick, moderate-difficulty filler (1 mark each mostly, a few 2-mark ones).

## Overall Difficulty Distribution (all 95 questions)

| Difficulty | Count | % |
|---|---|---|
| Easy | 42 | 44% |
| Medium | 42 | 44% |
| Complex | 11 | 12% |

Complex questions cluster almost entirely in Operating Systems (Banker's algorithm, page replacement), Networks (IPSec, Hamming code, TCP window), Databases (concurrency/isolation), Mathematics (permutations, planar graphs, triple integral), and Software Engineering (function point calc).

## Question-wise Table

| Q | Topic | Diff | Q | Topic | Diff | Q | Topic | Diff | Q | Topic | Diff |
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|DSA|E|25|BigData*|E|49|DB|M|73|Math|M|
|2|CyberSec|M|26|BigData*|E|50|CO&A|M|74|Math|E|
|3|CyberSec|E|27|Prog|M|51|CO&A|E|75|Math|C|
|4|AI/ML|E|28|Networks|M|52|CO&A|M|76|OS|M|
|5|AI/ML|E|29|DB|E|53|OS|E|77|SE*|E|
|6|Cloud*|E|30|DB|E|54|OS|E|78|SE*|E|
|7|ToC|M|31|CO&A|M|55|OS|C|79|SE*|E|
|8|ToC|M|32|Math|C|56|OS|C|80|SE*|E|
|9|Networks|M|33|OS|E|57|SE*|C|81|Quant|E|
|10|DB|E|34|OS|M|58|ToC|M|82|Verbal|M|
|11|DB|M|35|ToC|M|59|Math|C|83|NonVerbal|M|
|12|CO&A|E|36|ToC|M|60|Math|M|84|NonVerbal|M|
|13|CO&A|M|37|DSA|M|61|CyberSec|E|85|NonVerbal|M|
|14|CO&A|M|38|DSA|E|62|AI/ML|E|86|Quant|E|
|15|Math|M|39|CyberSec|E|63|AI/ML|E|87|Math/Stats|E|
|16|Math|C|40|Networks|M|64|AI/ML|E|88|Verbal|M|
|17|Math|M|41|CyberSec|E|65|ToC|M|89|Quant|E|
|18|OS|M|42|CyberSec|E|66|Compiler*|E|90|Quant|M|
|19|SE*|E|43|BigData*|E|67|Compiler*|E|91|Verbal|M|
|20|SE*|M|44|BigData*|E|68|Compiler*|E|92|NonVerbal|M|
|21|DSA|E|45|BigData*|E|69|CyberSec|M|93|DI|M|
|22|DSA|E|46|Networks|C|70|Networks|M|94|Verbal|M|
|23|CyberSec|E|47|Networks|C|71|Networks|C|95|NumSeries|M|
|24|Cloud/Virt*|M|48|DB|M|72|DB|C| | | |

*(E=Easy, M=Medium, C=Complex; \* = topic not in official syllabus)*

## Prep Takeaways

1. **Highest weightage**: Math, OS, Cyber Security, CO&A, Databases, Networks — all roughly 9–10% each. These six form the backbone (~55% of Part A).
2. **Don't skip "shadow topics"**: SE + Big Data + Compiler Design + Cloud/Virtualization together are **21% of Part A** — bigger than any single syllabus topic except Math. Since the syllabus doesn't mention them, candidates who stick strictly to the syllabus will lose ~1/5th of the marks.
3. **Image/Vision Processing** had zero questions here — lowest priority if time-constrained (but don't fully skip, one paper isn't a guarantee).
4. **Complex questions are concentrated**: if you want to save time, master OS (Banker's/paging), Networks (IPSec/Hamming/TCP math), and DB (isolation/deadlocks) numerically — that's where most "complex" marks live.
5. **Part B aptitude** is all Easy/Medium — high ROI, quick section to lock down separately (calendar tricks, syllogism rules, mirror-image patterns, Venn diagrams).
