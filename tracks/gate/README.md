# GATE — Active

`topics/gfg-gate-topic-map.md` is the source of truth for this track: GATE's native section
structure, sourced from GeeksforGeeks GATE Corner/CS Notes — GATE CS's 12 sections plus GATE DA's
two DA-only sections (Machine Learning, Artificial Intelligence), audited against the literal text
of the official GATE 2027 syllabus PDFs (CS and DA) from `gate2027.iitm.ac.in`. It also has a
§15 "Hands-On Networking Lab Tools" section — practical Linux/networking tooling (not GFG study
links) for actually running the §12 Computer Networks concepts on a real box. See
`../isro/topics/gfg-isro-topic-map.md` for the same underlying content regrouped under the ISRO
syllabus's 11 topics — the two overlap heavily since both draw on `../../subjects/`.

- `topics/exam-analysis-report.md` — CS: per-sitting analysis across **27 real sittings**
  (2007–2026 — two years turned out to bundle multiple official papers per PDF: 2015 is 3
  sessions, 2021 is 2 sets, not 1 each as first assumed). Scoring uses only the 20 **recent-era**
  (2014–2026) sittings; the 7 **older-era** (2007–2013) sittings are reported as historical
  reference only, since 19 years of syllabus/format drift would otherwise distort what to study
  *now*. Computer Networks is the one topic fully recomputed for the corrected 27-sitting count;
  the other 12 topics for 6 specific sittings (2014, 2015, 2017-CS1, 2017-CS2, 2020, 2021) are
  still on whole-paper density estimates, not verified per-question splits — a full-confidence
  rework of those is a known, deferred follow-up (see the file's own disclosure at the top).
- `topics/exam-analysis-report-da.md` — DA: same analysis for all 3 sittings that have ever
  existed (2024–2026 — DA is a new paper). Independently re-verified against a from-scratch
  re-run; numbers confirmed identical.
- `topics/networking-question-analysis.md` — dedicated deep-dive on Computer Networks
  specifically: every networking question across all 27 CS sittings + 3 DA sittings, cited by
  year/shift + question number. Broader "any networking mention" lexicon than the priority
  report's primary-topic classification, so its counts run higher for the same years — by
  design. 134 CS networking questions found (all high-confidence, no OCR estimates remaining);
  0 for DA (no Computer Networks section in DA's syllabus).
- `exam-priority-report.md` — CS: highest-priority links per topic, filtered from
  `topics/gfg-gate-topic-map.md`, tiered by a score derived from the analysis report
  (`avg weightage% + total complex-question count × 1.5`, adapted from ISRO's single-paper
  formula for this multi-sitting dataset).
- `exam-priority-report-da.md` — same, for DA.
- `study-files-log.md` — running index of every file (report, script, data cache) generated or
  substantially modified during this track's buildout — check this first in a new session before
  regenerating something that already exists.

Both analysis reports were built by an automated per-question classification pipeline (kept
in `../../tools/gate-paper-classifier/` for reuse on future papers — includes a persisted
extracted-text cache so re-runs don't need to re-OCR anything), not a manual read like ISRO's
single-paper report — read each report's own Limitations section before trusting a specific
number. No progress tracker exists yet (unlike `../isro/`'s `progress-tracker.md`) — add one
once you start working through the priority links.

`../../files/networking.md` is a standalone consolidated copy of everything Computer-Networks
related in this track (study links, hands-on tools, worked-formula notes, priority tier, the
full question-history analysis, and the Google job-market findings) merged into one file for
convenience — the individual source files above remain authoritative; the consolidated file is
a static snapshot, not auto-synced.
