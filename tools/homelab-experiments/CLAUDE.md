# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is not a software project — it's a set of markdown **menus** of independent research/learning
project ideas, run one at a time across four physical machines in the user's homelab, plus a small
Python helper (`select.py`) to browse them. There is no build, lint, or test suite; the only "code"
is `select.py` itself.

This folder is scoped to *experiments* — the actual scripts/analysis/results once a topic is picked.
It lives under `tools/` in the repo root; two levels up (`../../`) holds the ISRO/GATE exam-prep
material (`../../tracks/isro/topics/gfg-isro-topic-map.md`, `../../tracks/gate/topics/gfg-gate-topic-map.md`)
which every experiment idea here traces back to by design.

## Running select.py

```
python3 select.py                    # interactive machine -> category -> topic walk
python3 select.py --list              # dump the full machine/category/topic tree
python3 select.py --machine probook --category "Blockchain" --topic "Minimal Blockchain"
```

Machine/category/topic args match by case-insensitive substring. `select.py` parses the four menu
files directly (via the `## ` category headers and `- **Title** — description` topic bullets), so it
always stays in sync with them — never hardcode menu content into the script.

## Structure and invariants

- **Four menu files, one per machine**, each with its own fixed field and priority:
  - `rpi5-cs-eng.md` — Raspberry Pi 5, CS-Engineering (top priority)
  - `probook-cybersec.md` — HP ProBook 445 G11, Cybersecurity (2nd priority, build/analysis only —
    never scanning, exploiting, or targeting a real device/node on any network)
  - `proone-dsai.md` — HP ProOne 440 G9, DS/AI classical/CPU (3rd priority)
  - `garuda-gpu.md` — main daily-driver, GPU overflow only (not a field of its own — only holds
    ideas pulled from the other three that genuinely need a discrete GPU)
- Field priority order is strict: CS-Engineering > Cybersecurity > DS/AI.
- Categories are shared across files and mirror the 11-topic structure in
  `../../tracks/isro/topics/gfg-isro-topic-map.md`. The same category can appear in multiple files
  when a topic naturally splits by compute tier (e.g. Databases: Tier 1 on the Pi, Tier 2 on the
  ProBook, Tier 3 on the ProOne) — tier notes are inline in each file's section headers.
- Every topic bullet carries **exactly one** reference link (a GFG article, a starred GitHub repo, or
  a link already present in the two topic-map files under `../../tracks/{isro,gate}/topics/`).
  Preserve this when adding/editing topics.
- Topic bullet format `select.py` depends on: `- **Title** — description text`. Category headers must
  be `## Category Name`. Breaking either format breaks the parser.

## Workflow when the user is picking/scoping a task

This is a four-step funnel:

1. **Pick a machine** (one of the four above).
2. **Pick a category** within that machine's menu file.
3. **Pick a topic** within that category — use `select.py` to surface the exact block (title,
   description, reference link) rather than re-reading the whole markdown file by hand.
4. **Write the detailed task-plan.** Once a topic is selected, research its reference link (and
   beyond, as needed) and write a **new, separate markdown file** (not one of the four menu files)
   covering: what's being built, why, how it's scoped to that machine's hardware, how it'll be
   deployed and for how long, and what gets analyzed at the end. Only do this *after* a topic is
   explicitly chosen — never generate task plans in bulk ahead of time.

No detailed task-plan markdowns exist yet as of this writing — only the four menus, `README.md`, and
`select.py`. Ideas generally run as dev → deploy (days to 1–2 weeks) → analyze cycles, not one-shot
scripts; deploy usually means a bounded background run on the target machine, not a permanent service
(garuda-gpu.md ideas in particular run as bounded multi-day training/benchmark jobs since that machine
is the user's daily driver).
