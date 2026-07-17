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

## Workflow: picking and scoping a task

This is a four-step funnel, from "here's everything we could do" down to "here's the exact plan
for one task on one machine":

1. **Pick a machine.** Decide which of the four you're pointing at right now.
2. **Pick a category.** The AI lists that machine's categories (from its menu file's `## ` headers).
3. **Pick a topic.** The AI lists every topic bullet inside that category. Pick one.
4. **Get the detailed plan.** Once a specific topic is selected, the AI takes that topic's title,
   description, and reference link, researches the reference link (and searches further as needed),
   and — combined with this README and whatever you add in the moment — writes a **new, separate
   task-plan markdown** (not in this file) covering: what we're building, why, how it's scoped for
   this machine's hardware, how it'll be deployed and for how long, and what we're analyzing at the
   end. That detailed plan is created *after* selection, one task at a time — never in bulk ahead of
   time.

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

## What's *not* done yet

No detailed task-plan markdowns exist yet — only the four menus, this README, and `select.py`.
The first one gets created the first time you actually walk through the workflow above and land on
a topic to commit to.
