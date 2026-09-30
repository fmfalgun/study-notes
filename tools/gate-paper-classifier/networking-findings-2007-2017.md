# GATE CS Networking Questions — 2007–2017 (fork slice)

Covers 12 papers: 2007–2016 (one paper/year) + 2017 (CS1 + CS2, two shifts). Companion to
`networking-findings-2007-2017.json` (per-question records) — this file is the narrative summary.
A second fork covers 2018–2026 on a disjoint file set.

## Method

`pdftotext` first; OCR (`pdftoppm` + `tesseract`, 150dpi grayscale) for files that extracted near-empty
(2007–2011, 2015, 2017 CS1/CS2 all needed OCR — see Limitations). Classified against the Computer
Networks sub-clusters in `gfg-gate-topic-map.md` §12 using a keyword lexicon extending
`tools/gate-paper-classifier/classify.py`'s approach. For years with clean `Q.<N>` markers surviving
extraction (2007–2014, 2016), each of the paper's questions was isolated and checked once for
networking keywords — giving an exact per-question count.

**Update — 2015 and 2017 (CS1/CS2) re-verified via direct PDF read**: the initial OCR pass on these
three lost question-number markers and only produced density-based estimates (flagged low-confidence).
A follow-up pass read these files directly page-by-page (multimodal PDF reading, no OCR) and produced
exact, verified per-question counts — now high-confidence, same as the rest of this file. This also
surfaced an important correction: **the "2015" PDF is not one paper, it's three full GATE sessions
bundled into a single 79-page file** (Session-1, Session-2, Session-3, 65 questions each, confirmed by
each session's own answer-key table). The original 12-sitting count for this file's date range
therefore undercounts the true number of sittings — it's 14 (2007–2014 singly, 2015 ×3, 2016 singly,
2017 ×2), not 12.

**Copyright note**: no verbatim question text is reproduced anywhere in this file or the JSON —
only topic/sub-cluster paraphrases and question numbers, same convention as `exam-analysis-report.md`.

## Per-year networking question count

| Year | Shift | Networking Qs | Confidence | Notes |
|---|---|---|---|---|
| 2007 | — | 6 | high | Q19, Q34, Q46, Q52, Q68, Q70 |
| 2008 | — | 3 | high | Q14, Q17, Q59 |
| 2009 | — | 2 | high | Q47, Q55 |
| 2010 | — | 3 | high | Q17, Q47, Q50 |
| 2011 | — | 3 | high | Q30, Q50, Q61 |
| 2012 | — | 9 | high | Q3, Q10, Q22, Q34, Q44, Q45, Q47, Q48, Q49 |
| 2013 | — | 7 | high | Q5, Q12, Q16, Q36, Q37, Q47, Q49 |
| 2014 | — | 7 | high | Q20, Q23, Q24, Q27, Q28, Q45, Q55 |
| 2015 | Session-1 | 5 | high | Q23, Q26, Q27, Q36, Q39 |
| 2015 | Session-2 | 6 | high | Q33, Q34, Q35, Q36, Q37, Q38 |
| 2015 | Session-3 | 6 | high | Q18, Q19, Q35, Q46, Q47, Q56 |
| 2016 | — | 6 | high | Q19, Q24, Q30, Q41, Q53, Q54 |
| 2017 | CS1 | 3 | high | Q14, Q32, Q45 |
| 2017 | CS2 | 5 | high | Q9, Q18, Q20, Q34, Q35 |

**Total: 71 networking questions across 14 sittings, all high-confidence** (2007–2014 singly = 46
across 8 sittings; 2015 ×3 sessions = 17 across 3 sittings; 2016 = 6; 2017 ×2 shifts = 8 — average
~5.1/sitting). Every year in this file is now high-confidence — the low-confidence OCR estimates for
2015/2017 have been superseded by the direct-read re-verification above.

## Sub-cluster frequency (all years, 2007–2017)

Most-hit: **TCP / TCP segment structure** (appears in the plurality of questions — TCP header
fields, port numbers, segment-size numericals recur almost every year), **Transport Layer general**
(multiplexing, sockets), **Network Layer routing** (distance vector vs link state — every other
year), **Data Link Layer ARQ/sliding-window numericals** (2009, 2014, and now confirmed recurring
across all three 2015 sessions and both 2017 shifts too).

Seen only once or twice, worth noting: **BGP** (2007 Q70) and **token ring** (2007 Q68, 2014 Q55)
— neither is in the current topic map's Network/Data-Link Layer sub-clusters. BGP is genuinely
absent from `gfg-gate-topic-map.md` §12's Network Layer list (OSPF and RIP are there, BGP isn't).
Token ring is obsolete-syllabus content GATE stopped testing years ago — don't add it to the topic
map, it's a historical artifact, not a current gap.

## Limitations

0. **Superseded**: the original low-confidence estimates for 2015 and 2017 (CS1/CS2) have been
   replaced with verified per-question counts (see the Method section's "Update" note) — the
   remaining limitations below describe the extraction process, not a confidence caveat on those
   three years anymore.
1. **8 of 14 real sittings needed OCR or direct-read verification** (2007–2011, all 3 of 2015's
   sessions, 2017 CS1, 2017 CS2) — their PDFs are scanned images with no usable text layer via direct
   `pdftotext`. Quality varies; treat all OCR'd
   years' counts as somewhat less reliable than the 4 papers (2012, 2013, 2014, 2016) that extracted
   cleanly via `pdftotext` directly.
2. **(Resolved)** 2015 and both 2017 shifts originally lost Q-number markers during OCR, forcing
   density-based estimates. Superseded by the direct-read verification pass — see item 0.
3. **2013's source PDF contains the exam repeated ~4 times** (multiple question-booklet sets, same
   65 questions in different order/lettering) — handled by classifying only the first occurrence of
   each `Q.<N>`, but flagging here in case the same pattern affects other years' true/apparent
   question totals.
4. **Old-syllabus drift**: GATE CS's Computer Networks syllabus has narrowed since 2007 (BGP, token
   ring seen above are the clearest examples). A handful of other older questions may reference
   concepts the current syllabus doesn't test — flagged individually in the JSON's `note` field
   where noticed, but this wasn't exhaustively audited against a historical syllabus.
5. **Keyword lexicon, not manual reading** — same caveat as the original `exam-analysis-report.md`:
   automated classification, not question-by-question human verification. A "TCP" keyword hit could
   occasionally be a distractor option mentioning TCP in a question that's actually about something
   else (e.g., a general networking-devices question that lists TCP as one wrong answer choice).
