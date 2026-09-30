# gate-paper-classifier/

Automated pipeline that turned the downloaded GATE CS/DA previous-year question papers into
`tracks/gate/topics/exam-analysis-report*.md` + `tracks/gate/exam-priority-report*.md`. Kept
here so a future paper (e.g. 2027's, once it exists) can be folded in without rebuilding the
pipeline from scratch.

## Files

- `classify.py` — per-paper pipeline: strips `Q.N – Q.M Carry ... marks Each` range headers,
  splits the paper into individual questions via strict sequential `Q.N` stepping, then
  classifies each subject question against a keyword lexicon (built from
  `tracks/gate/topics/gfg-gate-topic-map.md`'s 14 section/sub-cluster names) using
  word-boundary regex matching. A question hitting 2+ distinct topic sections is flagged
  `complex`. CLI: `python3 classify.py <extracted.txt> <ga_count> <total_questions>` — e.g.
  `python3 classify.py cs_2026_CS1_QP.txt 10 65`. Prints a JSON array to stdout (one object
  per question: `q`, `section`, `hits` (keyword list, not question text), `complex`).
- `aggregate.py` — reads a `classified/*.json` directory, computes per-topic avg weightage %
  and total complex count across all sittings, applies the scoring formula
  (`avg_weightage% + total_complex × 1.5`), prints a plain-text ranked table. Expects
  `classified/cs_*.json` and `classified/da_*.json` naming.
- `report_data.py` — same aggregation as `aggregate.py` but emits ready-to-paste Markdown
  tables (aggregate weightage table, per-sitting breakdown table, complex-question citation
  lists) plus proper sitting labels (`2026-CS1`, `2024-DA`, etc.) instead of raw filenames.
  This is what actually generated the tables in the two `exam-analysis-report*.md` files.

## Full pipeline (what was actually run)

```bash
# 1. Extract each question paper PDF to plain text
pdftotext -layout cs/2026/CS1_QP.pdf cs_2026_CS1_QP.txt
# (repeat per sitting; scanned/no-text-layer PDFs need pdftoppm + tesseract OCR instead —
#  see the "2021 CS" limitation note in exam-analysis-report.md for why that attempt was
#  abandoned rather than trusted)

# 2. Classify each sitting
mkdir classified
python3 classify.py cs_2026_CS1_QP.txt 10 65 > classified/cs_2026_CS1_QP.json
# (repeat per sitting, matching the classified/{cs,da}_*.json naming aggregate.py expects)

# 3. Aggregate + generate report tables
python3 aggregate.py        # quick sanity-check table
python3 report_data.py      # full Markdown tables, paste into the analysis report
```

## Known limitations (carry these forward if reusing this on a new paper)

- **~25–30% of questions get no keyword match** ("unclassified") — this is a fast automated
  pass, not a manually-read one. Expand `LEXICON` in `classify.py` if a future paper's topic
  mix drifts and the miss rate climbs noticeably.
- **Diagram-heavy questions under-count** — anything where the actual content is in a figure
  (search trees, K-maps as images, circuit diagrams) has little text for the lexicon to match
  against. This hit GATE DA's Machine Learning/AI sections hardest.
- **Dense math notation gets dropped by `pdftotext`** — Calculus scored suspiciously low in
  both CS and DA analyses for this reason, not because it's actually untested.
- **`complex` is a keyword-co-occurrence heuristic, not verified difficulty** — a question
  hitting 2+ lexicon sections might genuinely combine concepts, or might just contain two
  generic terms coincidentally.
- If a paper's `Q.N – Q.M Carry ... marks Each` range headers use different wording than
  `"Carry ONE/TWO marks Each"`, update the `RANGE_HEADER` regex in `classify.py` — it's a
  fairly literal pattern match, not general parsing.
