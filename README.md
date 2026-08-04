# study-notes

Notes, topic maps, and prep tracking for every exam/work track currently being studied for,
plus the tools built to support them.

## Layout

- **[`subjects/`](subjects/)** — shared, track-agnostic CS-fundamentals notes (Mathematics, OS,
  Networks, Databases, DSA, Computer Organization, Theory of Computation, Programming Languages,
  Cyber Security, AI/ML). Written once, used by every track below that overlaps with it.
- **[`tracks/`](tracks/)** — one directory per exam/work track (currently `gate/`, `isro/`,
  `anthropic-fellows/`), each with its own topic maps, priority/progress tracking, and status.
- **`tools/`** — code, not notes: `bluff.py` (a curses activity monitor themed on the subjects
  above), `practice/` (a SQLite-backed practice-question tool), and `homelab-experiments/` (an
  independent menu of homelab research projects that trace back to the subjects/tracks material
  by design — see its own `CLAUDE.md`).

See each subdirectory's own README for specifics.
