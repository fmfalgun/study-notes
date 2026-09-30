# GATE Track — Study Files Log

Running record of every file generated or substantially modified during this track's buildout
(topic-map creation, previous-paper download/classification, priority-report generation,
Computer-Networks deep-dive, hands-on tooling reference). See `README.md` for what each
deliverable actually is; this file is just the index.

**Update rule:** every time a new file is generated or an existing one substantially reworked as
part of this track, add/update a row here in the same session, so a future session knows what
already exists before regenerating it.

## Log

| File (path relative to repo root) | What it is | Created | Last substantial revision |
|---|---|---|---|
| `tracks/gate/topics/gfg-gate-topic-map.md` | Source-of-truth GATE CS+DA study-link map (15 sections: 12 CS + 2 DA-only + 1 hands-on-tools), audited against official GATE 2027 syllabus PDFs, 3 dated audit-note passes | 2026-09-09 | 2026-09-30 (link-update fork: gap fills + practice links; manual §15 tools section added) |
| `tracks/gate/topics/prev-papers/cs/**` | 27 real CS previous-year question papers (2007–2026; 2015 = 3 sessions, 2021 = 2 sets, 2017/2024/2025/2026 = 2 shifts each) | 2026-09-09 (2021–2026 via official download) | 2026-09-29 (2007–2020 + full 2015/2021 supplement via user-provided CS.zip/DA.zip) |
| `tracks/gate/topics/prev-papers/da/**` | 3 real DA previous-year question papers (2024–2026, DA's entire paper history) | 2026-09-09 | — (DA.zip confirmed byte-identical, no changes) |
| `tools/gate-paper-classifier/classify.py` | Automated per-question topic classifier (keyword-lexicon based) against the topic-map's sub-clusters | 2026-09-09 | 2026-09-30 (NAT/NOR keyword-collision bug fix; 4 minor lexicon additions) |
| `tools/gate-paper-classifier/aggregate.py`, `report_data.py` | Supporting pipeline scripts (per-sitting aggregation, report-table generation) | 2026-09-09 | — |
| `tools/gate-paper-classifier/reclassify_multisession.py`, `sample_unclassified.py`, `wordfreq_unclassified.py`, `final_recompute.py` | Scratch scripts from the full-confidence rework pass — reusable starting point for a future complete pass, not cleaned up | 2026-09-30 | — |
| `tools/gate-paper-classifier/extracted-text-cache/*.txt` | Persisted raw extracted/OCR'd text per sitting (27 CS + 3 DA), so future re-runs don't need to re-extract/re-OCR | 2026-09-30 | — |
| `tools/gate-paper-classifier/networking-findings-2007-2017.{json,md}` | Networking-question findings, CS 2007–2017 slice | 2026-09-29 | 2026-09-30 (low-confidence years replaced with direct-PDF-read verified counts) |
| `tools/gate-paper-classifier/networking-findings-2018-2026.{json,md}` | Networking-question findings, CS 2018–2026 slice | 2026-09-29 | 2026-09-30 (same treatment) |
| `tracks/gate/topics/exam-analysis-report.md` | CS: per-sitting topic-weightage analysis, all 27 sittings, recent-era (2014–2026) vs. older-era (2007–2013) split | 2026-09-09 | 2026-09-30 (sitting-count correction 24→27; partial full-confidence rework — Computer Networks fully recomputed, 12 other topics for 6 sittings still on density estimates, disclosed explicitly in-file) |
| `tracks/gate/exam-priority-report.md` | CS: tiered, filtered priority links derived from the analysis report | 2026-09-09 | 2026-09-30 (same corrections as above) |
| `tracks/gate/topics/exam-analysis-report-da.md` | DA: per-sitting topic-weightage analysis, all 3 sittings | 2026-09-09 | — (independently re-verified from scratch, confirmed identical, left untouched) |
| `tracks/gate/exam-priority-report-da.md` | DA: tiered, filtered priority links | 2026-09-09 | — (same re-verification) |
| `tracks/gate/topics/networking-question-analysis.md` | Dedicated Computer-Networks deep-dive: every networking question across all 27 CS + 3 DA sittings, cited by year/shift + Q-number | 2026-09-29 | 2026-09-30 (sitting-count correction; all low-confidence years upgraded to verified via direct PDF read — 134 CS questions, zero estimates remaining) |
| `files/networking.md` | Standalone consolidated copy of everything Computer-Networks-related in this track (study links, hands-on tools, worked-formula notes, priority tier, full question-history, Google job-market findings) — static snapshot, not auto-synced | 2026-09-30 | — |
| `tracks/gate/README.md` | Track overview and file-by-file pointer | 2026-09-09 | 2026-09-30 |
| `tracks/gate/study-files-log.md` | This file — the log itself | 2026-09-30 | — |
