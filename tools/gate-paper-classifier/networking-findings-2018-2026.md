# Networking-question findings — GATE CS 2018–2026 (fork slice)

Companion data file: `networking-findings-2018-2026.json`. Covers the 12 sittings in this
fork's slice: 2018, 2019, 2020, 2021, 2022, 2023 (single papers), 2024/2025/2026 (CS1+CS2
each). A second fork covers 2007–2017 separately.

## Method

`pdftotext -layout` for text-layer PDFs; `pdftoppm`+`tesseract` OCR fallback for image-only
ones (2019, 2020, 2021 all needed OCR — none of the three had a usable text layer). Questions
split on `Q.No. N` / `Q.N` / `QN` (format varies by year), then each question block matched
against a word-boundary-anchored keyword lexicon built from `gfg-gate-topic-map.md` §12's five
Computer Networks sub-clusters. Acronyms with real collision risk (LAN/MAN/WAN/SYN/ARP/RARP/
NAT/RIP/MAC/TCP/UDP/RTT/ICMP) are matched case-sensitively as whole words against the
*original*-case text, not the lowercased text — this was a deliberate second-pass fix after an
initial lexicon version wildly over-matched (see Limitations).

**Update — 2019, 2020, 2021 re-verified via direct PDF read**: the OCR pass on these three lost
reliability (2020 especially — `pdftotext` looked clean but only extracted question numbers/option
labels). A follow-up pass read these files directly page-by-page (multimodal PDF reading, no OCR)
and produced exact, verified per-question counts — now high-confidence. This also confirmed that
2021's source PDF is genuinely two full official sets (Set-1 and Set-2, 55 CS questions + 10 GA
each, each with its own answer-key table) merged into one 91-page file, not a single paper — the
prior "91-page scanned merge" framing undercounted it as one sitting instead of two.

## Per-sitting counts

| Sitting | Networking Qs | Confidence |
|---|---|---|
| 2018 | 5 | high (clean text layer) |
| 2019 | 4 | high (verified via direct PDF read) |
| 2020 | 4 | high (verified via direct PDF read) |
| 2021 Set-1 | 4 | high (verified via direct PDF read) |
| 2021 Set-2 | 4 | high (verified via direct PDF read) |
| 2022 | 6 | high |
| 2023 | 5 | high |
| 2024-CS1 | 5 | high |
| 2024-CS2 | 7 | high |
| 2025-CS1 | 5 | high |
| 2025-CS2 | 5 | high |
| 2026-CS1 | 5 | high |
| 2026-CS2 | 4 | high |
| **Total (this slice)** | **67** | — |

**Sitting count correction**: this slice actually covers **13 sittings, not 12** — 2021 is two full
sets (Set-1, Set-2), each with its own 55 CS + 10 GA questions and its own answer key, not one
91-page paper. The original framing undercounted it by one sitting.

**Sanity check**: the 2022–2026 subset (8 sittings) totals **42** here vs. **32** in the prior
full multi-subject classification run recorded in `topics/exam-analysis-report.md`. The 10-question
gap is expected, not a red flag: this run's lexicon is broader/more permissive (built specifically
to catch networking mentions, including ones where networking isn't necessarily the dominant
topic of the question — e.g. a question primarily about something else that references "TCP" or
"IP address" in passing). Both numbers should be read as "at least this many," not a precise count.

## Limitations

1. **First lexicon draft was badly broken** — generic short strings (`lan`, `man`, `syn`, bare
   `switch`, bare `spanning tree`) were matching unrelated content as raw substrings: `man`/`lan`
   inside ordinary English words, `syn` inside "synchronous"/"syntax", bare `switch` catching an
   Operating-System "context switch" question, bare `spanning tree` catching pure graph-theory
   MST/DFS questions (Discrete Math, not Computer Networks). Initial run returned 146 hits for the
   2022–2026 subset alone — obviously wrong against the 32-question baseline. Rewritten with
   word-boundary regex throughout and case-sensitive whole-word matching for the worst-offending
   acronyms; re-verified against source text for `router`, `sequence number`, `spanning tree
   protocol` hits by hand before trusting the v2 numbers above.
2. **(Resolved)** 2019, 2020, 2021 originally relied on OCR (2020's was especially deceptive —
   `pdftotext` returned "text" that was actually just question numbers and option labels, with
   the real question content rasterized). Superseded by the direct-read verification pass —
   see the Method section's "Update" note.
3. **(Resolved)** 2021 was previously the known-hard file (a prior full-subject classification
   attempt gave up on question-boundary detection for it entirely). The direct-read pass fixed
   this and additionally revealed it's two full sittings (Set-1 + Set-2), not one.
4. **Multi-cluster questions** (e.g. one question hitting both "IPv4" and "TCP" keywords) are
   listed with an array of sub-clusters rather than forced into one — this is intentional, not
   a bug, but means simple per-cluster counts across the JSON will double-count a few questions.
5. Not spot-checked against answer keys (this zip had no answer keys) — classification is by
   question topic only, correctness of the classification's "numerical vs conceptual" tag is a
   regex heuristic, not verified.
