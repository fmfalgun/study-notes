# prepclash/

Study log for material worked through on [prepclash](https://fmfalgun.github.io/prepclash/),
organized to mirror its own act → chapter structure.

## Layout

```
prepclash/act-<N>/ch-<NN>/link-<NN>-notes.md      # notes from working through that link
prepclash/act-<N>/ch-<NN>/link-<NN>-exercise.md   # the testing/exercise done for that link
```

- `act-<N>` — act number, unpadded (`act-1`, `act-2`, ...).
- `ch-<NN>` — chapter number within the act, zero-padded (`ch-01`, `ch-02`, ...).
- `link-<NN>-*` — one notes/exercise pair per link within a chapter, zero-padded
  (`link-01-notes.md` / `link-01-exercise.md`, `link-02-notes.md` / `link-02-exercise.md`, ...).

Every link gets exactly two files: `-notes.md` (what was learned) and `-exercise.md` (the
testing/practice done against it). No other file types at the link level — if a chapter needs
shared context beyond its individual links, that goes in a `ch-<NN>/README.md` instead of
overloading a link's own pair.

## Convention for man7.org-sourced links

Applies to any link under `man7.org/linux/man-pages/` (man5/man7/etc.) — not just the first batch.

**Source of truth**: prefer the local `man <section> <page>` output when it structurally matches
the linked page (verify section headings once — the man-pages project sometimes reorganizes a
page, e.g. `proc(5)` is now a short hub page instead of the old monolithic version, so don't
assume local == linked without checking). Fall back to fetching the URL directly if they diverge.

**Notes granularity**: one point per paragraph, and one point per table row — not literal
line-by-line (man page text-wrapping is arbitrary, not semantic). Each point gets: **Claim**
(paraphrase of the doc), **Simple explanation** (plain language), **Try it** (commands).

**One-level-deep references**: when the doc explicitly delegates real explanatory detail to
another man page (a sentence pointing there *for the actual content*, not just a name-drop), pull
that page's relevant section into the same notes file. A bare "See also" bibliography-style list
of many sibling pages is *not* expanded — each of those stays a future `link-NN` of its own if
wanted later. State the boundary explicitly at the top of the notes file whenever a doc has this
kind of index (e.g. `proc(5)`'s ~55-entry `/proc/[a-z]*` list).

**Exercises**: ordered, runnable command sequences inspired by the notes + source doc, meant to be
pasted into a real terminal on this machine. Read-only/non-destructive by default; anything
needing root or touching live system state is marked "(Optional, root, ...)" and left reversible.

**Shell compatibility — verify every command actually runs here before writing it down.** The
default interactive shell on this machine is **fish**, not bash/POSIX sh — fish does not support
`$$`, `$!`, `$(cmd)`, or `VAR=value` the POSIX way, and a command written assuming POSIX syntax
will error out when pasted directly into a fish prompt. Rules:
- Own PID: fish `$fish_pid` (not `$$`).
- PID of the last backgrounded job: fish `$last_pid` (not `$!`).
- Command substitution: fish `(cmd)` (not `$(cmd)`).
- Variable assignment: fish `set VAR value` (not `VAR=value`).
- For anything multi-step (spawn a background process, capture its PID, run several commands
  against it), prefer wrapping the whole sequence in `bash -c '...'` — single-quoted at the fish
  level so it's passed through literally — over hand-translating each POSIX construct. This also
  makes the block portable to a plain bash/sh login shell (e.g. Debian) without edits.
- Give the fish-native form as the primary command, and **keep the bash/sh form alongside it too**
  (as a separate labeled block, or an inline "bash/sh: ..." note for a one-line swap) — don't
  strip the POSIX form out. Every command block should make it unambiguous which shell it's
  written for.

**Tooling differences**: call out Arch (`pacman -S ...`) vs Debian (`apt install ...`) package
names inline, the first time an exercise uses a tool that isn't part of a base install.

## Convention for refspecs.linuxfoundation.org / FHS-sourced links

Applies to FHS (Filesystem Hierarchy Standard) links and any other Linux Foundation refspec —
same underlying philosophy as the man7.org convention above, with source-type-specific
adjustments below.

**Source of truth**: no local man-page equivalent exists for FHS — the standard web-fetch tool
also can't reach `refspecs.linuxfoundation.org` (domain-verification block), so content is pulled
directly with `curl` and HTML-tag-stripped for reading. This is slower than the man7 workflow but
gives the same verbatim-text fidelity, which matters more here than for prose man pages since FHS
is normative ("must"/"should"/"may" carry real weight).

**Index pages vs. real content — check before assuming a given link *is* the content.** FHS
chapter pages (`ch03.html`, `ch04.html`, `ch05.html`, ...) are thin table-of-contents pages; the
actual per-directory text lives in numbered sub-pages (`ch03s02.html`, `ch03s03.html`, ...,
discoverable by grepping the index page's HTML for `href="ch0Xs\d+\.html"`). Always check for this
pattern before writing a notes file — treating a bare index page as "the whole link" produces a
nearly content-free file.

**Granularity — one notes/exercise pair per top-level link given, not per sub-page.** Even though
the real content is spread across many sub-pages, all of them fold into *one* `link-NN-notes.md` /
`link-NN-exercise.md` pair for that top-level chapter link — same pattern as `proc(5)`'s Overview
section folding many `/proc/*` entries into one file under the man7 convention. Within that one
file, give **every** sub-page its own `**Claim**`/**Simple explanation**/**Try it** point — no
skipping entries for brevity, and every claim gets a validation command, even in a long chapter
(FHS chapter 3 alone covers 17 sub-pages in one notes file). Work through sub-pages in order,
adding one section at a time, rather than trying to summarize the whole chapter in one pass.

**Real-machine grounding matters more here than for man7 links**, because FHS is old enough that
several of its assumptions no longer hold on a modern distro — check and call out explicitly where
they diverge:
- **usrmerge**: on this machine `/bin`, `/sbin`, `/usr/sbin` are all symlinks to `/usr/bin`, and
  `/lib` → `/usr/lib`. FHS predates this and describes them as physically separate. State this
  once prominently per notes file, then flag it again at each specific point it changes the
  answer (e.g. the `/bin`-vs-`/sbin` essential/non-essential split).
- **glibc-conditional text**: some FHS requirements are explicitly scoped to non-glibc systems —
  don't apply them unconditionally to a glibc-based distro (verify with `ldd --version`) without
  reading the actual conditional wording first.
- **Superseded mechanisms**: `MAKEDEV` (replaced by `devtmpfs`/`udev`), `/media` (often replaced in
  practice by `/run/media/<user>/...` from desktop auto-mount daemons), plain-text
  `/var/log/messages` (often replaced by `journalctl`/systemd-journald), LILO config (replaced by
  GRUB/systemd-boot) — expect these absent on a modern system and explain *why* that's the
  expected, compliant state rather than a defect.
- When a real observed value ties directly back to *why* a rule exists (e.g. `/tmp` on `tmpfs` vs
  `/var/tmp` on real disk — the actual mechanism behind "survives a reboot," not just the rule
  saying so), call that connection out explicitly.

**Chapter/act placement**: unless told otherwise, a new batch of links continues in the
*existing* chapter directory as the next `link-NN` — don't assume a new source domain means a new
`ch-NN`. Confirm with whoever's directing the work if it's ambiguous.

