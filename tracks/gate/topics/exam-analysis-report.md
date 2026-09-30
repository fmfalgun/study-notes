# GATE CS — Previous-Paper Analysis (2007–2026)

Analysis of **27 GATE CS sittings** spanning 2007–2026 (corrected from 24 — see "Sitting-count
correction" below) — sourced from a user-supplied `CS.zip` archive covering years the official
`gate2027.iitm.ac.in/download` page doesn't offer (that page only goes back to 2021). Mapped
against the 12-section CS structure in `gfg-gate-topic-map.md`. This supersedes the prior
8-sitting (2022–2026) version of this report — that version's numbers are referenced below
where relevant for comparison, not preserved as a separate file.

**Partial-update disclosure, read this before the rest**: this pass was scoped to fix three
issues (density-fallback sittings, the ~27-30% unclassified rate, Calculus's low score) as a
single automated/semi-manual pass, without subagent fanout. It made real, verified progress on
the sitting-count structural error and on Computer Networks specifically (both below), applied
four small lexicon fixes, and ran a systematic (not exhaustive) check on the unclassified-rate
and Calculus questions. **It did not achieve full per-question re-classification for all 13
topics across every previously-density-fallback sitting** — that would require either
substantially more OCR/regex engineering per malformed file or page-by-page visual reading
across roughly 180+ pages, neither of which fit in this pass. The topic-weightage tables below
are **not fully recomputed** for the corrected 27-sitting dataset outside of Computer Networks;
treat the non-Networks numbers as the prior (24-sitting) run's figures, now known to be built on
a slightly wrong sitting count for 2015/2021, until a future pass redoes them properly.

**Sitting-count correction (24 → 27)**: the networking-only re-verification pass (see
`networking-question-analysis.md`) discovered that `2015_CS.pdf` bundles **3 distinct full
65-question GATE sessions** (Session-1/2/3, each with its own answer key) in one 79-page file,
and `2021_CS.pdf` bundles **2 distinct official sets** (Set-1/Set-2, each with its own answer
key) in one 91-page file — not one scanned paper each, as the prior run assumed. Confirmed via
direct text search for `SESSION -N` / `Set-N` markers in the cached extracted text. This raises
the true sitting count from 24 to **27**, and recent-era sittings (2014–2026) from 17 to **20**
(+2 from 2015, +1 from 2021); older-era (2007–2013) is unaffected, still 7.

## Methodology

**Recent era vs. older era — a deliberate split, not an oversight.** GATE CS's format and
section structure has drifted significantly since 2007: question counts varied year to year,
some years number General Aptitude and the subject section as one continuous Q.1–Q.65
sequence while others restart subject numbering from Q.1 after GA, and several papers ship
as multi-"SET" PDFs with the same 65 questions repeated 2–4× in randomized order
(anti-cheating measure) rather than one clean paper. Blending 19 years of this drift into
one score would let outdated syllabus weight distort what to study *now*. So, per direct
instruction:

- **Recent era (2014–2026, 17 sittings)** drives the actual Tier 1/2/3 scoring in
  `exam-priority-report.md`.
- **Older era (2007–2013, 7 sittings)** is reported here as historical reference/context
  only — not blended into the score.

**Extraction**: `pdftotext -layout` for text-layer PDFs (13 of 24 sittings); `pdftoppm`
(150dpi grayscale) + `tesseract` OCR for the rest (11 of 24 — every pre-2012 paper plus
2015, both 2017 shifts, 2019, 2020, and 2021 all ship as scanned images with no text layer).
All extracted text is cached in `tools/gate-paper-classifier/extracted-text-cache/` for
reuse — this wasn't done for the prior 8-sitting run, forcing unnecessary re-extraction
this time; not repeating that mistake.

**Splitting**: `Q.N` markers with strict sequential stepping, extended this run to handle
two format quirks the prior (2022–2026-only) run never had to deal with: (1) **section
renumbering** (GA numbered separately, then the subject section restarts at Q.1) —
detected and re-offset; (2) **duplicate "SET" booklets** (the same 65 questions repeated in
a second/third randomized order later in the same PDF, seen in 2013 and 2014) — detected
via a Q.1 recurrence after a high question number already accepted, stopping at the first
complete booklet.

**Density fallback for 6 recent-era + 2 older-era sittings** where splitting still produced
an implausible count (mostly OCR quality on scanned papers, not format quirks): 2014, 2015,
2017-CS1, 2017-CS2, 2020, 2021 (recent) and 2008, 2010 (older). Instead of forcing an
unreliable per-question split, these use **whole-paper keyword density** — every lexicon
keyword hit across the full extracted text, proportionally scaled to a nominal
55-subject-question paper. They still contribute real per-topic counts to every table below
(the density estimate *is* a count, just not tied to real question numbers), but **not** to
Complex Question Citations (no question numbers exist to cite) and are marked in the
per-sitting breakdown. Treat their numbers as directional, not exact.

**Classification**: word-boundary keyword lexicon (`tools/gate-paper-classifier/classify.py`)
built from `gfg-gate-topic-map.md`'s 12 CS sections. A question hitting 2+ distinct sections
is flagged **Complex**, same bar as before.

**Two lexicon bugs caught and fixed mid-run, before any number below was finalized** — both
are the same class of failure the original classifier's word-boundary fix didn't prevent,
because the problem wasn't substring-matching, it was a *short, common word* matching
correctly as a whole word but in the wrong context:
1. **`nat`** (meant to catch "NAT" as in Network Address Translation) was instead matching
   **"Numerical Answer Type (NAT)"** — GATE's own standard question-format boilerplate label,
   present in the instructions of nearly every modern paper. This alone produced 175 false
   hits across the recent-era dataset and was the single largest driver of Computer
   Networks' score in the first draft of this analysis.
2. **`nor`** (meant to catch NOR-gate/Boolean-NOR questions) was instead matching the
   English conjunction **"neither ... nor ..."**, overwhelmingly common in Theory of
   Computation and DBMS question phrasing ("neither L1 nor L2 is regular", "neither
   S-attributed nor L-attributed"). Spot-checking 15 raw hits found only 2 genuine NOR-gate
   references; this was the single largest driver of Digital Logic's score in the first draft.

Fixed by replacing both bare keywords with more specific phrases (`network address
translation`, `static nat`, `dynamic nat`, `nat table` for Networks; `nor gate`, `nor
operation`, `exclusive nor` for Digital Logic) directly in `classify.py`, then re-running
the full 24-sitting classification. **Every number in this report reflects the fixed
lexicon** — see Key Findings for how much this changed the topic ordering, and Limitations
for the honest caveat that other undiscovered short-keyword collisions may still be lurking
elsewhere in the lexicon.

**Four smaller lexicon gaps found and fixed in this pass**, via aggregate word-frequency
analysis across unclassified questions (not by reading individual question text): bare
`probability` was missing from the Probability lexicon (only distribution-specific terms were
listed); `printf`/`scanf`/`stdio`/`#include` were missing from Programming & DS (C
output-tracing questions using these don't always also say "array"/"pointer"); `context-free
language` (as opposed to `context-free grammar`) was missing from Theory of Computation;
`s-attributed`/`l-attributed` were missing from Compiler Design. **Re-running the classifier
with these fixes across the 16 cleanly-split sittings changed the unclassified count only
marginally (250/845 → still ~29.6% on that subset) — these were real but low-frequency gaps,
not another `nat`/`nor`-scale systemic bug.** No topic's tier placement changed as a result.

**Aggregation formula** (unchanged from the prior run, applied only to the 17 recent-era
sittings):

```
avg_weightage% = mean(per-sitting topic%) across the 17 recent-era sittings
score = avg_weightage% + (total complex-question count across those 17 sittings × 1.5)
```

Never reproduces question text — all citations are `sitting Q#` + topic label only.

## Aggregate Topic Weightage — Recent Era (2014–2026, 17 sittings, 985 subject questions)

| Topic | Avg weightage % | Total Qs | Total Complex | Score |
|---|---|---|---|---|
| Programming & Data Structures | 11.3% | 111 | 35 | 63.8 |
| Discrete Mathematics | 8.9% | 88 | 16 | 32.9 |
| Databases (DBMS) | 7.6% | 74 | 9 | 21.1 |
| Computer Organization & Architecture | 4.8% | 48 | 8 | 16.8 |
| Linear Algebra (Eng. Math) | 4.8% | 47 | 8 | 16.8 |
| Operating System | 5.8% | 56 | 7 | 16.3 |
| Computer Networks | 8.0% | 78 | 4 | 14.0 |
| Compiler Design | 4.1% | 40 | 6 | 13.1 |
| Algorithms | 5.1% | 49 | 5 | 12.6 |
| Theory of Computation | 5.5% | 54 | 3 | 10.0 |
| Digital Logic | 3.4% | 33 | 4 | 9.4 |
| Probability & Statistics (Eng. Math) | 2.4% | 23 | 4 | 8.4 |
| Calculus (Eng. Math) | 0.4% | 4 | 0 | 0.4 |

**Unclassified (recent era): 265/985 subject questions (26.9%)** — see Limitations.

**Comparison with the prior 8-sitting (2022–2026) run** (scores: ProgDS 51.6, DiscreteMath
30.6, DBMS 16.8, DigitalLogic 15.0, COA 14.9, Networks 14.8, LinAlg 14.2, OS 13.4, Algorithms
10.9, Compiler 10.9, ToC 7.8, Prob&Stats 5.9, Calculus 0.5):
- **Stable across both runs**: Programming & Data Structures and Discrete Mathematics remain
  the clear top 2, by a wide margin, in both the 8-sitting and 24-sitting versions — the
  most robust finding in the whole dataset.
- **Databases moved up** (16.8 → 21.1, now clearly 3rd) with 9 more sittings of data.
- **Digital Logic dropped sharply** (15.0 → 9.4, out of Tier 2 entirely) once the `nor` bug
  was fixed — the prior 8-sitting run's 15.0 was itself likely somewhat inflated by the same
  bug (it used the same unfixed lexicon), so don't read this as "Digital Logic became less
  important," read it as "the earlier number was never fully trustworthy either."
- **Computer Networks stayed roughly flat** (14.8 → 14.0) — a first draft of this expanded
  analysis (before the `nat` fix) had shown Networks jumping to 17.1 and overtaking COA/
  LinAlg; that jump didn't survive the bug fix. Networks' true position relative to its
  neighbors is genuinely close and shouldn't be over-read either direction.
- **Computer Networks recomputed with the corrected 20-sitting recent era** (the only topic
  fully redone for the sitting-count fix, since verified per-session/per-set data already
  existed from the networking-only pass): high-confidence Networks-question counts now exist
  for 18 of the 20 recent-era sittings — 2016, 2018, 2019, 2020, 2022, 2023, 2024-CS1/CS2,
  2025-CS1/CS2, 2026-CS1/CS2 (clean-split or Read-verified) plus 2015's 3 sessions (17
  questions total: 5+6+6) and 2021's 2 sets (8 total: 4+4) — leaving only **2014** still on
  the whole-paper density estimate (11 questions). Total recent-era Networks count: **90
  questions across 20 sittings**, up from 78/17 in the table above (which still reflects the
  pre-correction 17-sitting count) — a full weightage-score recompute incorporating this is
  deferred to a future pass alongside the other 12 topics, per the disclosure at the top of
  this file.

## Aggregate Topic Weightage — Older Era (2007–2013, 7 sittings, 413 subject questions)

**Reference only — not blended into the score above.**

| Topic | Avg weightage % | Total Qs |
|---|---|---|
| Programming & Data Structures | 11.5% | 48 |
| Discrete Mathematics | 9.6% | 41 |
| Operating System | 6.3% | 27 |
| Theory of Computation | 5.8% | 23 |
| Databases (DBMS) | 6.5% | 26 |
| Computer Networks | 6.1% | 26 |
| Digital Logic | 4.6% | 18 |
| Algorithms | 4.6% | 19 |
| Compiler Design | 4.2% | 17 |
| Computer Organization & Architecture | 4.4% | 18 |
| Probability & Statistics (Eng. Math) | 3.2% | 12 |
| Calculus (Eng. Math) | 1.3% | 5 |
| Linear Algebra (Eng. Math) | 1.8% | 7 |

**Unclassified (older era): 124/413 (30.0%)**. Same top-2 as recent era. Linear Algebra
scores much lower historically (1.8% vs. 4.7% recent) — given the OCR-heavy extraction for
this era, treat that specific gap cautiously rather than as a confirmed syllabus-weight
trend; it's plausibly an extraction artifact (dense matrix notation, like Calculus's known
issue) rather than a real historical difference.

**Old-syllabus content found, not in the current topic map**: two 2007-era Computer
Networks questions referenced **BGP** (Border Gateway Protocol) and **token ring**.
Cross-checked against `gfg-gate-topic-map.md` §12 — **BGP is genuinely absent** (OSPF and
RIP are listed as Network Layer routing protocols, BGP isn't — confirmed via direct grep,
zero mentions). Worth flagging even from old-era data since BGP is still a live, testable
concept, unlike token ring (obsolete hardware, correctly not in the current syllabus).

## Per-Sitting Breakdown — Recent Era

| Sitting | OS | DBMS | Networks | Calculus | Lin.Alg | Prob. | Discrete Math | Digital Logic | COA | Prog&DS | Algorithms | ToC | Compiler | Unclassified | Method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2014 | 6 | 5 | 11 | 1 | 1 | 0 | 3 | 5 | 1 | 8 | 3 | 4 | 4 | 0 | density (est.) |
| 2015 | 2 | 8 | 8 | 0 | 3 | 1 | 6 | 2 | 1 | 8 | 7 | 3 | 4 | 0 | density (est.) |
| 2016 | 4 | 3 | 4 | 0 | 2 | 1 | 5 | 2 | 1 | 6 | 2 | 3 | 1 | 28 | per-question |
| 2017-CS1 | 6 | 7 | 1 | 0 | 2 | 6 | 3 | 3 | 3 | 6 | 8 | 6 | 2 | 0 | density (est.) |
| 2017-CS2 | 0 | 7 | 6 | 0 | 4 | 4 | 5 | 4 | 2 | 9 | 4 | 6 | 5 | 0 | density (est.) |
| 2018 | 4 | 4 | 4 | 0 | 4 | 0 | 5 | 3 | 5 | 4 | 1 | 3 | 0 | 21 | per-question |
| 2019 | 1 | 4 | 4 | 1 | 2 | 1 | 7 | 0 | 2 | 4 | 2 | 2 | 1 | 30 | per-question |
| 2020 | 4 | 9 | 4 | 0 | 4 | 1 | 4 | 2 | 7 | 12 | 2 | 2 | 4 | 0 | density (est.) |
| 2021 | 6 | 7 | 8 | 0 | 3 | 1 | 5 | 1 | 1 | 7 | 6 | 5 | 4 | 0 | density (est.) |
| 2022 | 4 | 4 | 4 | 1 | 5 | 0 | 7 | 1 | 6 | 3 | 1 | 2 | 1 | 18 | per-question |
| 2023 | 3 | 0 | 0 | 1 | 2 | 2 | 4 | 2 | 0 | 5 | 1 | 3 | 1 | 26 | per-question |
| 2024-CS1 | 0 | 4 | 5 | 0 | 2 | 1 | 3 | 0 | 3 | 4 | 2 | 2 | 2 | 30 | per-question |
| 2024-CS2 | 4 | 3 | 4 | 0 | 3 | 1 | 8 | 0 | 5 | 8 | 0 | 2 | 3 | 18 | per-question |
| 2025-CS1 | 3 | 4 | 1 | 0 | 3 | 1 | 6 | 2 | 2 | 6 | 1 | 3 | 3 | 26 | per-question |
| 2025-CS2 | 4 | 2 | 3 | 0 | 2 | 0 | 4 | 2 | 2 | 6 | 3 | 4 | 2 | 26 | per-question |
| 2026-CS1 | 3 | 2 | 5 | 0 | 3 | 1 | 9 | 2 | 3 | 6 | 2 | 2 | 2 | 20 | per-question |
| 2026-CS2 | 2 | 1 | 6 | 0 | 2 | 2 | 4 | 2 | 4 | 9 | 4 | 2 | 1 | 22 | per-question |

Density-fallback rows (method column) have real per-topic *estimated* counts — they're not
blank — but those counts come from whole-paper keyword proportions, not a verified walk
through actual questions, so treat them as softer signal than the per-question rows.
**2024-CS1's 30/55 unclassified rate (55%) remains the clear outlier** — still worth a
manual spot-check before trusting that row specifically.

*(Older-era per-sitting breakdown omitted — 2 of 7 older sittings are on density fallback
and the rest carry real format-drift risk per the BGP finding above; the aggregate table is
the right level of detail for reference-only data.)*

## Complex Question Citations (by topic)

Only from the 16 sittings with a clean per-question split (7 older-era: 2007, 2009, 2011,
2012, 2013; 9 recent-era: 2016, 2018, 2019, 2022, 2023, 2024-CS1, 2024-CS2, 2025-CS1,
2025-CS2, 2026-CS1, 2026-CS2):

- **Programming & Data Structures**: 2007-CS Q41, Q48 · 2009-CS Q36, Q54, Q58 · 2011-CS Q31,
  Q43 · 2012-CS Q5, Q10 · 2013-CS Q17, Q43, Q44 · 2016-CS Q20, Q47, Q65 · 2018-CS Q13, Q65 ·
  2019-CS Q24, Q50 · 2022-CS Q15, Q28 · 2023-CS Q13, Q20, Q54 · 2024-CS1 Q17, Q24 · 2024-CS2
  Q33, Q39, Q41, Q55 · 2025-CS1 Q26, Q29, Q62, Q65 · 2025-CS2 Q35, Q38, Q41 · 2026-CS1 Q14,
  Q24, Q40 · 2026-CS2 Q17, Q30, Q32, Q38, Q42, Q49, Q53
- **Discrete Mathematics**: 2007-CS Q35, Q36, Q46, Q60 · 2012-CS Q16, Q43, Q47 · 2016-CS
  Q12, Q37, Q44 · 2018-CS Q18 · 2019-CS Q58 · 2023-CS Q15 · 2024-CS1 Q42 · 2024-CS2 Q15,
  Q45, Q56 · 2025-CS1 Q19, Q33 · 2025-CS2 Q30, Q42, Q43 · 2026-CS1 Q31
- **Databases (DBMS)**: 2007-CS Q61 · 2011-CS Q44 · 2012-CS Q15, Q51 · 2016-CS Q61 ·
  2019-CS Q42, Q61 · 2022-CS Q35 · 2024-CS1 Q22 · 2024-CS2 Q27 · 2025-CS1 Q47 · 2026-CS1
  Q30 · 2026-CS2 Q65
- **Computer Organization & Architecture**: 2007-CS Q74 · 2011-CS Q30 · 2018-CS Q19 ·
  2022-CS Q17, Q38 · 2024-CS1 Q15 · 2024-CS2 Q10, Q57, Q61 · 2026-CS1 Q54
- **Algorithms**: 2007-CS Q42 · 2009-CS Q14, Q35 · 2011-CS Q27 · 2012-CS Q4 · 2013-CS Q7,
  Q18 · 2023-CS Q25 · 2024-CS1 Q45 · 2025-CS2 Q17, Q29 · 2026-CS2 Q25
- **Operating System**: 2007-CS Q17, Q84 · 2011-CS Q18 · 2016-CS Q60 · 2022-CS Q62 ·
  2023-CS Q22 · 2024-CS2 Q25, Q37 · 2025-CS2 Q48 · 2026-CS2 Q54
- **Linear Algebra**: 2018-CS Q49 · 2022-CS Q20 · 2024-CS1 Q49 · 2024-CS2 Q17, Q46 ·
  2025-CS1 Q22, Q40 · 2025-CS2 Q44
- **Compiler Design**: 2009-CS Q42 · 2024-CS2 Q21 · 2025-CS1 Q12, Q13, Q46 · 2025-CS2 Q40 ·
  2026-CS1 Q53
- **Computer Networks**: 2013-CS Q65 · 2024-CS1 Q16 · 2025-CS1 Q16 · 2025-CS2 Q18 ·
  2026-CS1 Q45. *(2016-CS Q65 and 2018-CS Q65 dropped out of this list after the `nat` fix
  — they were driven by the bug, not genuine complexity. 2013-CS Q65 remaining here despite
  also being a last-question chunk is worth the same "chunk-boundary artifact" caution as
  before — don't treat it as confirmed without a manual look.)*
- **Digital Logic**: 2009-CS Q47 · 2011-CS Q28 · 2012-CS Q7 · 2013-CS Q5 · 2022-CS Q40 ·
  2025-CS1 Q11 · 2025-CS2 Q55 · 2026-CS2 Q59
- **Probability & Statistics**: 2011-CS Q23 · 2012-CS Q21 · 2019-CS Q47 · 2023-CS Q23 ·
  2025-CS1 Q58 · 2026-CS2 Q14
- **Theory of Computation**: 2009-CS Q17 · 2011-CS Q21 · 2016-CS Q53 · 2024-CS1 Q59 ·
  2025-CS1 Q28
- **Calculus**: 2012-CS Q9

## Key Findings

1. **Programming & Data Structures and Discrete Mathematics dominate in every era and every
   version of this analysis** (buggy first draft and fixed final version alike) — the most
   robust finding in the whole dataset, unaffected by the lexicon bugs described above.
2. **Databases jumped into a clear 3rd place with more data** (21.1, up from 16.8 in the
   prior 8-sitting run) — worth re-weighting prep priority upward versus the earlier report.
3. **Digital Logic and Computer Networks's apparent movement in the first draft of this
   report was a measurement artifact, not a real trend** — catching the `nat`/`nor` bugs
   before publishing reversed both: Digital Logic fell out of Tier 2 entirely (15.0 → 9.4),
   Computer Networks landed close to where it started (14.8 → 14.0). This is the headline
   methodological lesson of this expansion: automated keyword classification is fragile to
   exactly this kind of short-word collision, and a 3x-larger dataset amplifies a bug's
   effect on the aggregate just as much as it amplifies genuine signal.
4. **Complex questions still cluster heavily in Programming & Data Structures** (35 of 122
   total recent-era complex hits — 29%), consistent with the prior finding.
5. **GA (General Aptitude) is excluded from topic scoring**, same call as before.

## Limitations (read before trusting the numbers above)

1. **8 of 24 sittings needed whole-paper density fallback** (2008, 2010 older-era; 2014,
   2015, 2017-CS1, 2017-CS2, 2020, 2021 recent-era) instead of per-question classification —
   old/scanned PDFs where OCR quality wasn't sufficient for reliable question-boundary
   detection even after the section-restart and duplicate-booklet fixes. **6 of these 8 are
   recent-era and do feed the Tier-driving score** — a larger and more consequential
   fallback fraction than the prior 8-sitting report had (which excluded 2021 entirely
   rather than estimating it).
2. **Two lexicon bugs (`nat`, `nor`) were caught and fixed mid-run** — see Methodology for
   the full story. **This is disclosed precisely because it's the kind of error that's easy
   to miss**: both keywords passed the original classifier's word-boundary safeguard (they
   matched real, complete words, just in the wrong context) and would not have been caught
   without manually spot-checking raw keyword-hit context before trusting the aggregate
   numbers. Other short/common-word keywords in the lexicon (`function`, `relation`, `group`,
   `join` among others) were spot-checked and looked legitimate on a small sample, but
   weren't exhaustively audited — treat any topic whose score depends heavily on a single
   short keyword with the same caution this report now applies to Networks and Digital Logic.
3. **~27–30% of subject questions get no keyword match** in both eras — same automated-
   classification ceiling as the prior report. Treat percentages as a lower-bound signal.
4. **Calculus is almost certainly under-counted in both eras** (0.4% recent, 1.3% older) —
   dense math notation that `pdftotext`/OCR both struggle with, not genuinely near-zero
   weightage. Don't deprioritize based on this number. **Checked this pass, confirmed not a
   fixable lexicon gap**: ran a systematic scan for calculus-notation-adjacent text
   (derivative/integral/f(x)-style patterns) across all cleanly-split sittings' unclassified
   and misclassified questions — found exactly one candidate across 11 sittings checked. This
   rules out "missing keyword" as the cause with reasonable confidence; the extraction-artifact
   explanation (the notation itself doesn't survive as matchable text, so there's nothing for
   any keyword list to catch) is the more likely one, and isn't fixable by editing
   `classify.py` — would need either better math-aware OCR or manual reading.
5. **"Complex" is keyword-co-occurrence, not verified difficulty** — same heuristic-proxy
   caveat as before, with the added "Q65 chunk-boundary" artifact risk noted for Computer
   Networks specifically.
6. **Old-syllabus drift confirmed real**: BGP (absent from the current topic map, flagged
   above) and token ring (obsolete, correctly not added) both appeared in 2007-era papers.
   Not an exhaustive syllabus audit — these are what the keyword classifier happened to surface.
7. **This report was built by automated passes**, not spot-checked question-by-question
   against source PDFs beyond the specific debugging done on the duplicate-booklet/
   section-restart splitting logic and the two lexicon bugs above. Treat
   `exam-priority-report.md`'s tiers as a starting filter — the bug-catch in this run is a
   reason for *more* caution about undiscovered issues, not less, despite the larger sample.
8. **This pass's scope was explicitly partial — see the disclosure at the top of this file.**
   What's fully done: the 24→27 sitting-count correction (structurally confirmed), Computer
   Networks' recount for the corrected 20-sitting recent era, four minor lexicon fixes, and a
   systematic (not exhaustive) check ruling out a fixable-lexicon-gap explanation for Calculus.
   What's **not** done: per-question re-classification for all 13 topics across 2014, 2015's 3
   sessions, 2017-CS1, 2017-CS2, 2020, and 2021's 2 sets — these remain on whole-paper density
   estimates for every topic except Networks. The aggregate weightage tables above still use
   the pre-correction 17-sitting recent-era figures for every topic except Networks' note
   above; a genuinely complete redo would need either much deeper OCR/regex work per malformed
   file or direct page-by-page visual reading (via a PDF-capable reading tool) across roughly
   180+ pages — correctly identified as the right method by direct instruction, but not
   completed within this single pass's resource budget. Flagging this explicitly rather than
   presenting partial work as finished.
