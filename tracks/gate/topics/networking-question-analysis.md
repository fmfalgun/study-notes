# GATE Computer Networks — Full Question-History Analysis (CS 2007–2026, DA 2024–2026)

Dedicated deep-dive on networking questions specifically, built from every previous-year paper
currently on disk — **27 real CS sittings** (2007–2026; several years turned out to bundle more
than one official paper per PDF — see the sitting-count correction below) and all 3 DA sittings
that have ever existed (2024–2026). This is a companion to, not a replacement for,
`exam-priority-report.md`'s Computer Networks section — that section uses primary-topic-per-question
classification for apples-to-apples scoring against the other 11 CS subjects; this file uses a
broader "any networking mention" lexicon built specifically to surface every networking-adjacent
question, including secondary references. Expect this file's counts to run higher than the priority
report's for the same years — that's by design, not an error.

Built by two parallel forks (2007–2017 slice, 2018–2026 slice), a manual DA pass, and a follow-up
direct-PDF-read verification pass that replaced every low-confidence OCR estimate with an exact
count. Source data: `tools/gate-paper-classifier/networking-findings-{2007-2017,2018-2026}.{json,md}`.

**Sitting-count correction**: the original "24 CS sittings" framing undercounted the real paper
count by 3. Two files turned out to bundle multiple official sittings into one PDF: **2015 is
three full sessions** (Session-1/2/3, 65 questions each, each with its own answer-key table), not
one paper, and **2021 is two full sets** (Set-1, Set-2), each with its own answer key — the prior
"91-page scanned merge" framing treated it as a single hard-to-parse sitting. The true count is
27 (2007–2014 singly = 8, 2015 ×3, 2016 singly = 1, 2017 ×2, 2018 singly = 1, 2019 singly = 1,
2020 singly = 1, 2021 ×2, 2022 singly = 1, 2023 singly = 1, 2024 ×2, 2025 ×2, 2026 ×2 = 27).

**Copyright note**: no verbatim question text anywhere below — only topic/sub-cluster paraphrases
and question numbers, same convention as the rest of this track.

---

## Combined per-sitting count, all 24 CS + 3 DA sittings

| Year | Shift | Networking Qs | Confidence | Extraction method |
|---|---|---|---|---|
| 2007 | — | 6 | high | OCR |
| 2008 | — | 3 | high | OCR |
| 2009 | — | 2 | high | OCR |
| 2010 | — | 3 | high | OCR |
| 2011 | — | 3 | high | OCR |
| 2012 | — | 9 | high | pdftotext |
| 2013 | — | 7 | high | pdftotext *(source PDF had the paper repeated ~4×; deduplicated)* |
| 2014 | — | 7 | high | pdftotext |
| 2015 | Session-1 | 5 | high | direct PDF read |
| 2015 | Session-2 | 6 | high | direct PDF read |
| 2015 | Session-3 | 6 | high | direct PDF read |
| 2016 | — | 6 | high | pdftotext |
| 2017 | CS1 | 3 | high | direct PDF read |
| 2017 | CS2 | 5 | high | direct PDF read |
| 2018 | — | 5 | high | pdftotext |
| 2019 | — | 4 | high | direct PDF read |
| 2020 | — | 4 | high | direct PDF read |
| 2021 | Set-1 | 4 | high | direct PDF read |
| 2021 | Set-2 | 4 | high | direct PDF read |
| 2022 | — | 6 | high | pdftotext |
| 2023 | — | 5 | high | pdftotext |
| 2024 | CS1 | 5 | high | pdftotext |
| 2024 | CS2 | 7 | high | pdftotext |
| 2025 | CS1 | 5 | high | pdftotext |
| 2025 | CS2 | 5 | high | pdftotext |
| 2026 | CS1 | 5 | high | pdftotext |
| 2026 | CS2 | 4 | high | pdftotext |
| **2024** | DA | **0** | high | pdftotext *(only "network" hits are ML terms — Bayesian/Neural Network — not real networking)* |
| **2025** | DA | **0** | high | pdftotext |
| **2026** | DA | **0** | high | pdftotext |

**CS total: 134 networking questions across 27 sittings, every sitting now high-confidence.**
No estimates remain — every year that originally needed OCR-based density estimation (2015,
2017×2, 2019, 2020, 2021×2) was re-verified via direct page-by-page PDF reading, which also
corrected the sitting count upward (2015 and 2021 both turned out to be multi-paper bundles).
**DA total: 0 across all 3 sittings that have ever existed** — expected, DA's syllabus has no
Computer Networks section at all.

## Most-hit sub-clusters (CS, across all years with reliable per-question data)

**Transport Layer dominates**, consistently: TCP/TCP-segment-structure questions (header fields,
port numbers, segment-size numericals) recur in almost every single year 2007–2026 — this is the
single most-tested networking sub-cluster across the entire 20-year history, not just recent years.

Behind that: **Network Layer routing** (distance-vector vs. link-state, every other year roughly),
**IP addressing/subnetting/CIDR numericals**, and **Data Link Layer ARQ/sliding-window numericals**
(clustered in specific years — 2009, 2014 — rather than every year). Ethernet and HTTP show up with
real but lower frequency, consistent with `exam-priority-report.md`'s existing "most-hit: TCP, IP
addressing/subnetting, HTTP, Ethernet" finding from the smaller 8-sitting sample — the fuller
24-sitting history confirms that ranking rather than changing it.

## Topic-map gap found

**BGP** (2007 Q70) doesn't map to any current sub-cluster in `gfg-gate-topic-map.md` §12's Network
Layer list — OSPF and RIP are there, BGP isn't. This is the only genuine current-topic-map gap found
across all 24 CS sittings; it appeared exactly once, in the oldest paper on file, and never
recurred in any sitting since (including all of 2014–2026). Given that pattern, this reads as
low-priority — worth a one-line addition to the topic map if you want completeness, but not
something the 19-year question history suggests is worth deep prep time.

*(Token ring — 2007 Q68, 2014 Q55 — was also flagged during extraction but is obsolete syllabus
content GATE stopped testing; not a real gap, not added anywhere.)*

## Limitations (read before trusting the numbers above)

1. **(Resolved)** Originally, 13 of the then-assumed 24 sittings needed OCR and several of those
   (2015, 2017×2, 2019, 2020, 2021×2) only produced density-based estimates, not verified
   per-question counts. A follow-up pass re-extracted all of these via direct, page-by-page PDF
   reading (multimodal, no OCR) instead — every sitting in the table above is now high-confidence
   with real question-number citations. 2020 was the most deceptive of the original OCR failures:
   `pdftotext` returned plausible-looking output that was actually just question numbers and
   option labels, with the real question content rasterized as images.
2. **The two forks' lexicons differ slightly in strictness** — the 2018–2026 fork explicitly caught
   and fixed a bad first draft (generic substrings like `lan`, `syn`, bare `switch` were matching
   unrelated English words and non-networking questions — an Operating-System "context switch"
   question and pure graph-theory MST questions were false positives before the fix). The
   2007–2017 fork's lexicon was built independently; both were manually spot-checked against
   source text but weren't cross-validated against each other question-by-question.
3. **Automated keyword classification, not question-by-question human reading**, same caveat as
   every other analysis report in this track. A keyword hit could occasionally land on a
   distractor answer choice rather than the question's actual subject. The direct-read
   verification pass (item 1) mitigates this for the years it covered, but the originally-clean
   `pdftotext` years (2012–2014, 2016, 2018, 2022–2026) were not re-verified by direct read.
4. **Old-syllabus drift**: GATE CS's Computer Networks content has narrowed since 2007 (BGP, token
   ring above are the clearest examples) — a handful of other pre-2014 questions may reference
   concepts no longer on the current syllabus; not exhaustively audited against a historical
   syllabus document.
5. This file's "any mention" lexicon is deliberately broader than `exam-priority-report.md`'s
   primary-topic-per-question classification — the two files' Computer Networks numbers for the
   same years (e.g. 42 here vs. 32 there for 2022–2026) will not match, and that gap is expected,
   not a discrepancy to resolve.
6. **Minor question-number uncertainty for 2019/2020**: unlike 2015/2017/2021 (read with careful
   per-question Q-label tracking), the 2019/2020 direct-read pass was done in larger page batches
   without cross-checking every printed `Q.<N>` label against a running count — question numbers
   for these two years carry a small (±1) risk of being off, though the *topics found* and total
   *counts* are solid.
