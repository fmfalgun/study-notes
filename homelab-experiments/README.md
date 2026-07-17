# Homelab Experiments

Independent research/learning projects run across four machines, one task per machine at a time.
This folder is where the actual scripts, analysis, and results live once a topic is picked —
`isroprep/` above it is your ISRO/GATE exam-prep material, kept separate. These experiments still
count toward exam prep indirectly: most of the CS-Eng/Cybersecurity/DS-AI foundations below overlap
with the syllabus topics in `../topics/`.

## The four machines

| Key | Machine | Field | Menu file |
|---|---|---|---|
| `rpi5` | Raspberry Pi 5 (BCM2712, 8GB RAM, ARM64) | CS-Engineering (top priority) | `rpi5-cs-eng.md` |
| `probook` | HP ProBook 445 G11 (Ryzen 5 7535U, 16GB, Kali, portable) | Cybersecurity — build & analysis only | `probook-cybersec.md` |
| `proone` | HP ProOne 440 G9 (i7-14700, 16GB, no dGPU, Kali, always-on desktop) | DS/AI — classical/CPU | `proone-dsai.md` |
| `garuda` | Main daily-driver (Ryzen 7 7445HS, RTX 4050) | GPU overflow only — no field of its own | `garuda-gpu.md` |

Field priority order (strict): **CS-Engineering > Cybersecurity > DS/AI**. `garuda-gpu.md` is not a
4th field — it only holds ideas pulled from the other three when a task genuinely needs a discrete
GPU (mostly deep learning; a couple of crypto/DB entries too). If a category doesn't need a GPU
(e.g. Databases in general), it has no entry there.

Categories are shared across all four files and match `../topics/gfg-isro-topic-map.md`'s 11-topic
structure (Mathematics, Computer Organization & Architecture, Programming Languages, DSA, Theory of
Computation, Operating Systems, Databases, Computer Networks, Image/Vision, AI/ML, Cyber Security).
A category can appear in more than one file when its ideas naturally split by compute tier — e.g.
Databases appears in all three CPU-only files, simplest tier on the Pi, heaviest (distributed) on
the ProOne — see the tier notes inline in each file.

**Cybersecurity scope**: coding/analysis, not hacking. Cryptography & math, digital forensics,
blockchain, and malware-analysis *fundamentals* (binary formats, packers, disassembly) — never
scanning, exploiting, or otherwise targeting a real device/node on any network. Every target in
`probook-cybersec.md` is self-generated or a public dataset used for static reference.

Every idea in every file carries exactly one reference link — a GeeksforGeeks article, a starred
GitHub repo, or a link already present in `../topics/gfg-isro-topic-map.md` /
`../topics/gfg-gate-topic-map.md`.

## Prefer real-time system data over synthetic where it fits

When writing `plan.md`/`scope.md` for a topic, don't default to synthetic/generated data just
because it's easiest to reason about. Be creative about pulling in real, live signals from the
target device itself — `/proc`, `psutil`, `journalctl`, `vmstat`, `ss`, `sensors`, systemd services,
package-manager logs, whatever Linux utility on that specific machine actually maps to what the
topic needs. The point is to learn from real telemetry, not to stay comfortable with one tool (e.g.
don't reach for `btop` reflexively — pick whatever source fits the topic's actual metric).

Synthetic/known-ground-truth data still has its place — anywhere a topic needs to check "did the
implementation compute the right answer," a known ground truth is often the only way to verify
that, and should stay separate from real-data usage rather than being replaced by it.

**Utilities inventory**: each device has a `<device-key>-utilities.md` file at this directory's
root (`rpi5-utilities.md`, `probook-utilities.md`, `proone-utilities.md`, `garuda-utilities.md`),
tracking what real-time data sources/CLI tools/libraries are actually confirmed present on that
machine, what's confirmed missing, and the check command to re-verify. Before proposing a data
source for a new topic, check that device's file first — only investigate what's still unknown or
look for a better alternative, don't re-discover from scratch every time. Update the file whenever
a topic's work turns up something new about that machine's available tooling.

## Workflow: picking and scoping a task

This is a four-step funnel, from "here's everything we could do" down to "here's the exact plan
for one task on one machine":

1. **Pick a machine.** Decide which of the four you're pointing at right now.
2. **Pick a category.** The AI lists that machine's categories (from its menu file's `## ` headers).
3. **Pick a topic.** The AI lists every topic bullet inside that category. Pick one.
4. **Get the detailed plan.** Once a specific topic is selected, the AI takes that topic's title,
   description, and reference link, researches the reference link (and searches further as needed),
   and — combined with this README and whatever you add in the moment — writes the four documents
   described below (not in this file). That detailed-plan step happens *after* selection, one task at
   a time — never in bulk ahead of time.

### Directory layout for a task-plan and its code

Every topic that gets a detailed plan lives in its own directory, nested by topic then device —
never as a flat file directly under `homelab-experiments/`:

```
homelab-experiments/<topic-slug>/<device-key>/plan.md       # what & why
homelab-experiments/<topic-slug>/<device-key>/scope.md      # in/out boundary
homelab-experiments/<topic-slug>/doc/steps-<device-key>.md  # what to read
homelab-experiments/<topic-slug>/doc/roadmap-<device-key>.md # what to build, in order
homelab-experiments/<topic-slug>/<device-key>/script/       # code only — created on demand
```

- `<topic-slug>` names the experiment topic itself (e.g. `distribution-fitting-toolkit`), not the
  device.
- `<device-key>` is one of `rpi5` / `probook` / `proone` / `garuda`, matching the machine keys in
  `select.py`.

**All four docs — `plan.md`, `scope.md`, `steps-<device-key>.md`, `roadmap-<device-key>.md` — get
created together, as soon as a topic+device is selected from `select.py`'s output.** They are not
staggered or created ad hoc later; this is the standard output of step 4 above, every time. Only
`script/` stays on-demand — created the first time there's an actual code file to put in it.

Each of the four has one job, and **no two of them may restate the same information**. If a fact
already lives in one file, every other file references it by relative link instead of repeating it —
this is a hard rule, not a style preference, because these docs drift out of sync silently otherwise.

| File | Job | Answers |
|---|---|---|
| `plan.md` | The full narrative: what's being built, why, hardware fit, implementation sketch, deployment, end-of-run analysis. | "What is this experiment, in full?" |
| `scope.md` | A sharpened boundary pulled from `plan.md`: in scope / explicitly out of scope, plus the concrete contract `plan.md` only gestures at loosely — **Input**, **Output**, **Database/dataset** (what it reads/writes, or "none"), **Timespan** (build phase vs. deployment/running duration), and **Test/pass-threshold** (the concrete criteria the script's output must clear, derived from theory where possible rather than an arbitrary number). | "Where exactly is the line, and what does pass/fail actually mean?" |
| `doc/steps-<device-key>.md` | A tiered reading list, built by walking the plan's reference link (and its sub-links) outward, assuming zero prior knowledge. Same tiering style as `../topics/math-crossover-analysis.md` and the topic maps in `../topics/`. | "What do I need to read first?" |
| `doc/roadmap-<device-key>.md` | The concrete build sequence (scaffold → implement → validate → deploy → analyze), assuming the reading in `steps-<device-key>.md` is done. | "What do I build, in what order?" |

- `plan.md` and `scope.md` sit directly under `<device-key>/`, as siblings of `script/` — not nested
  in a `markdown/` subfolder.
- `steps-<device-key>.md` and `roadmap-<device-key>.md` live in `doc/`, a sibling of the device
  directories at the `<topic-slug>/` level (not nested inside a device directory) — this is where
  they're shared if the topic is later scoped for more than one device.
- `script/` is reserved strictly for that experiment's actual code — nothing else goes there.
- If the same topic is later run on a second machine, it gets its own `<topic-slug>/<device-key>/`
  directory (with its own `plan.md`/`scope.md`) alongside the first, plus its own
  `doc/steps-<device-key>.md` / `doc/roadmap-<device-key>.md` — the topic directory can hold multiple
  device subdirectories plus the shared `doc/`.

### Claude Code session convention

Every Claude Code chat working on a task here must be run with `homelab-experiments/` (this
directory) as the working directory — never `isroprep/` root or anywhere else.

Rename each such session (`/rename`) to:

```
task<task-number>-<topic-slug>-<device-key>
```

e.g. `task1-distribution-fitting-toolkit-proone` for the session working the
`distribution-fitting-toolkit` topic on `proone`. `<topic-slug>` and `<device-key>` match the
directory layout above.

### Using `select.py` for steps 1-3

`select.py` (in this folder) mechanizes the machine → category → topic walk so you don't have to
read full markdown files by hand. It reads the four menu files directly, so it's always in sync
with them.

Interactive:
```
python3 select.py
```
Walks you through numbered menus for machine, then category, then topic, and prints the selected
topic's full block (title, description, reference link) at the end.

Non-interactive (useful for an AI session, or to jump straight to a known topic):
```
python3 select.py --machine probook --category "Blockchain" --topic "Minimal Blockchain"
```
Machine/category/topic arguments match by case-insensitive substring, so partial names work.

Dump the entire tree (all four machines, all categories, all topics) in one shot:
```
python3 select.py --list
```

Once `select.py` prints the selected block, hand that output plus this README to the AI and say
which machine/topic you picked — that's steps 1-4 combined, and step 4 (the detailed task-plan
markdown) is what the AI produces from there.

## What's done so far

One topic has its full four-doc set: `distribution-fitting-toolkit` on `proone`
(`proone/plan.md`, `proone/scope.md`, `doc/steps-proone.md`, `doc/roadmap-proone.md`). Use it as the
reference example — including how the four avoid repeating each other — when creating the next one.
