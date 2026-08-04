# Link 9 — Notes: `ps(1)` — report a snapshot of the current processes

Source: https://man7.org/linux/man-pages/man1/ps.1.html
Local equivalent: `man 1 ps` (verified structurally identical: same 23 section headings, in the
same order, confirmed by diffing headings against a fetched structural summary of the web page).

**Why this link exists separately from the coreutils link**: `ps` is not GNU coreutils — it's part
of `procps-ng`. Confirmed by grepping the downloaded coreutils manual (zero matches) and checking
GNU's own package index (link 8's notes). This is the correct home for it: the man7.org convention.

**Scope note (this page is unusually large — ~2,100 lines / ~28,000 words)**: `STANDARD FORMAT
SPECIFIERS` alone lists 100+ output-column keywords, and `AIX FORMAT DESCRIPTORS`/
`OBSOLETE SORT KEYS` add legacy variants on top of that. Per the same "index vs. real content"
judgment used for `proc(5)`'s `/proc/[a-z]*` list and the coreutils manual: the ~15 most
practically useful format specifiers get their own explanation + command below; the rest are
genuinely just a lookup table (`man 1 ps`, `ps L` lists them all live) — not expanded point by
point here, since doing so would mean transcribing the entire STANDARDS FORMAT SPECIFIERS table
verbatim. Same treatment for `AIX FORMAT DESCRIPTORS` and `OBSOLETE SORT KEYS` (both explicitly
legacy/deprecated per the page's own text) — summarized, not exhaustively itemized.

---

## NAME / SYNOPSIS / DESCRIPTION

**Claim**: `ps [option...]` — snapshot of active processes (for a *live-updating* view, the page
itself says to use `top` instead). Three option grammars coexist and can be freely mixed (with
possible conflicts): **Unix options** (grouped, dash-prefixed, e.g. `-ef`), **BSD options**
(grouped, no dash, e.g. `aux`), **GNU long options** (double-dash, e.g. `--sort`). Default
selection (no options): processes with your effective UID, on your terminal, showing
PID/TTY/TIME/CMD, unsorted. BSD-style options change two things at once: they add STAT to the
default display and switch CMD→full args, *and* they widen selection to all your processes across
every terminal — the page explicitly separates these two effects because they're easy to conflate.
Selection options are (mostly) **additive** — the default selection is discarded first, then
everything matching *any* given criterion is added back in.

**Simple explanation**: the "three grammars" thing is *the* source of `ps` confusion (`ps -aux` vs
`ps aux` is the classic mixup — see NOTES below). Treat Unix-with-dash and BSD-without-dash as two
genuinely different dialects that happen to share a binary, not two spellings of the same thing.

**Try it**:
```sh
ps                    # default: just your processes, your terminal
ps -e | head -5        # Unix-style: every process on the system
ps ax | head -5        # BSD-style: same intent, different grammar -- compare the header row to the line above
```

## EXAMPLES (the man page's own curated set — worth running as a group)

```sh
ps -ef | head -5                                    # every process, standard syntax
ps aux | head -5                                    # every process, BSD syntax
ps -ejH | head -8                                   # process tree, Unix syntax
ps axjf | head -8                                   # process tree, BSD syntax
ps -eLf | head -5                                   # thread info
ps -U root -u root u 2>/dev/null | head -5           # every process running as root, user format
ps -eo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchan:14,comm | head -5   # fully custom columns
ps -C sshd -o pid= 2>/dev/null                       # just the PID(s) of a named command
ps -q $fish_pid -o comm=                             # just the name of one specific PID
```
bash/sh: `ps -q $$ -o comm=` for the last line.

## SIMPLE PROCESS SELECTION

**Claim** (condensed — many of these are BSD-personality-specific toggles): `a` = lift the
"only yourself" restriction (show all-with-a-terminal); `x` = lift the "must have a tty"
restriction (show all-of-yours, even without a terminal); combining `a`+`x` (as in `ps aux`) =
genuinely everyone. Unix-style equivalents: `-A`/`-e` = all processes (identical to each other);
`-a` = all except session leaders and terminal-less processes; `-d` = all except session leaders;
`-N`/`--deselect` = negate the selection (identical to each other); `T` = processes on this
terminal; `r` = running-only filter; `g` = obsolete, only meaningful under the `sunos4`
personality.

**Simple explanation**: `-A`/`-e` is the "give me everything" you actually want 95% of the time —
the rest of this section is mostly historical/edge-case toggles.

**Try it**:
```sh
ps -A | wc -l          # total process count, Unix-style "everything"
ps -e | wc -l           # identical count -- confirms -A and -e really are the same option
ps -ax | wc -l 2>&1     # note: -ax mixes a dash with a BSD letter -- see NOTES for why this specific
                        # kind of mixing is flagged as a common mistake, even though it often "works"
ps r                    # running-only, BSD style
```

## PROCESS SELECTION BY LIST

**Claim**: accept a blank- or comma-separated list argument, usable multiple times (`ps -p "1 2"
-p 3,4` unions both). Bare `123` = `--pid 123`; `+123` = `--sid 123`; `-123` = select by PGID.
Named-list options (condensed, synonym groups): `-p`/`p`/`--pid` (PID list); `--ppid` (parent PID
list — children of); `-q`/`q`/`--quick-pid` (PID list, "quick mode": reads only those PIDs,
unsorted/unfiltered, no forest/sort allowed alongside it); `-s`/`--sid` (session ID);
`-t`/`t`/`--tty` (terminal — plain `-` selects processes with *no* terminal); `-C` (command name —
**not** the full command line; note the man page flags that older `procps`/kernel versions
truncated this to 15 characters, current ones don't); `-G`/`--Group` (real GID/name) vs.
`-g`/`--group` (session **or** effective GID, disambiguated by whether the list is numeric) vs.
`--group` alone (effective GID only); `-U`/`--User` (real UID/name) vs. `U`/`-u`/`--user`
(effective UID/name).

**Simple explanation**: the real/effective UID and GID distinction here is exactly what link 1
(`credentials(7)`) covered — `ps -U` asks "who created this process," `ps -u` asks "whose
permissions does this process currently run with." Same distinction, applied as a filter.

**Try it**:
```sh
ps -p $fish_pid
ps -C bash 2>&1                          # by executable name, not full command line
ps -U $USER -u $USER u | head -5          # real AND effective UID both matching yours
```
bash/sh: `ps -p $$` for the first line.

## OUTPUT FORMAT CONTROL

**Claim** (condensed — this section is almost entirely "preset bundles of `-o` columns," each
option is really just a named shortcut): `-f` (full format: adds UID/PPID/C/STIME/TTY/TIME/CMD,
prints full args); `-F` (extra-full, implies `-f`, adds SZ/RSS/PSR); `l`/`-l` (BSD/Unix long
format, adds priority/nice/memory/wait-channel columns); `j`/`-j` (job-control-oriented columns:
PGID/SID/TPGID); `-M`/`Z` (SELinux security context column, identical to each other); `s` (signal
format: pending/blocked/ignored/caught masks); `u` (user-oriented: %CPU/%MEM/VSZ/RSS/START/TIME);
`v` (virtual-memory format); `-y` (drop the F flags column, show RSS instead of ADDR — only valid
with `-l`). The real workhorse: **`o`/`-o`/`--format`** — fully custom column list from the
STANDARD FORMAT SPECIFIERS vocabulary, headers renameable (`-o pid,ruser=RealUser`), widths
explicitly settable (`-o wchan:14`), empty header suppresses the header row entirely (`-o pid=`).
`-O`/`O` = "`-o`, but preloaded with sensible default columns" (and `O` specifically is
*overloaded* — it heuristically decides whether you meant a format or a sort spec; use `-O` or
`--sort` explicitly if you care which).

**Try it**:
```sh
ps -ef | head -3
ps -eo pid,ppid,user,%cpu,%mem,stat,comm --sort=-%cpu | head -6   # busiest processes right now, custom columns
ps -eo pid,ruser=RealUser,comm=Command | head -3                  # renamed headers
ps -eo pid= -o comm= | head -3                                    # no header row at all (both columns headerless)
```

## OUTPUT MODIFIERS

**Claim** (condensed): `c` = true executable name instead of `args` (turns the `args` format
keyword effectively into `comm`); `-D`/`--date-format` = `strftime(3)`-style format for `lstart`
(≤24 chars to avoid column misalignment); `--delimiter` = single-char column separator override;
`e` = show environment after the command; `f`/`--forest`/`-H` = ASCII-art process tree; `h` =
header behavior is genuinely inconsistent across `ps` history (this version: no header unless BSD
personality, overridable via `--headers`/`--no-headers` regardless of personality); `k`/`--sort` =
multi-key sort spec `[+|-]key[,...]` using STANDARD FORMAT SPECIFIERS keywords (`+`=ascending,
default; `-`=descending); `n` = numeric WCHAN/USER/UID/GID instead of resolved names;
`S`/`--cumulative` = fold dead children's resource usage into the parent; `w`/`-w` = wide output
(repeat for unlimited); `--cols`/`--columns`/`--width`/`--lines`/`--rows` = explicit screen
dimension overrides (useful when output is piped/redirected and `ps` can't detect a real
terminal width).

**Try it**:
```sh
ps -eo pid,comm --sort=pid | head -5           # ascending sort (default direction)
ps -eo pid,comm --sort=-pid | head -5          # descending -- note the leading '-'
ps -e --forest | head -8                        # process tree
ps -eo pid,args -c | head -3                    # -c: args column collapses to bare executable name
ps -eo pid,comm,args --cols=200 | head -3       # explicit width override, useful when piping
```

## THREAD DISPLAY

**Claim**: `H` = show threads as if they were separate processes; `-L` = show threads, adding
LWP/NLWP columns; `m`/`-m` = show threads *after* their parent process (grouped display); `-T` =
show threads, adding SPID column.

**Try it**:
```sh
ps -eLf | head -5                    # LWP (thread ID) and NLWP (thread count) columns
ps -T -p $fish_pid       # thread view of your own shell
```
bash/sh: `ps -T -p $$`.

## OTHER INFORMATION

**Claim**: `--help section` (section ∈ simple/list/output/threads/misc/all, or first-letter
shorthand); `--info` (debugging info); `L` = list every recognized format specifier (this is the
live, authoritative version of the STANDARD FORMAT SPECIFIERS table this notes file summarizes);
`-V`/`V`/`--version` = procps-ng version.

**Try it**:
```sh
ps L | wc -l              # confirms the "100+ specifiers" scope claim directly, on this machine's ps version
ps --version | head -1
ps --help simple 2>&1 | head -5
```

## NOTES

**Claim**: this `ps` reads `/proc` directly (no special privilege needed — direct tie to link 2).
CPU% is lifetime-average, not instantaneous, and won't reliably sum to 100%. SIZE/RSS undercount
some kernel-side memory (page tables, kernel stack, `task_struct`) by roughly 20 KiB minimum,
always-resident. `<defunct>` = zombie process, not yet reaped by its parent (destroyed by `init`
if the parent itself exits first). Long usernames get truncated to column width. **`ps -aux` is
explicitly called out as a common mistake**: POSIX/Unix reads it as "`-a` (tty processes) `-u`
(user-format) `x` (no-tty-restriction-lift, but `x` here is being parsed as a *username* argument
to `-u`, not the BSD flag!)" — if no user named literally `x` exists, this `ps` charitably falls
back to assuming you meant `ps aux`, but the ambiguity is real.

**Try it**:
```sh
grep " /proc " /proc/mounts   # the mechanism this ps is built on, same as link 2
ps -eo pid,%cpu | awk 'NR>1{s+=$2} END{print "sum of %CPU column:", s, "-- rarely exactly 100"}'
ps -eo stat | grep -c Z        # zombie count right now (0 is normal/expected)
ps aux 2>&1 | head -1; ps -aux 2>&1 | head -1   # compare -- do they actually differ on this system?
```

## PROCESS FLAGS

**Claim**: the `F` column (flags format specifier) is a bitmask sum: `1` = forked but hasn't
`exec`'d yet, `4` = used superuser privileges at some point.

**Try it**:
```sh
ps -eo pid,f,comm | awk '$2 != 0' | head -5   # processes with a nonzero F value right now
```

## PROCESS STATE CODES

**Claim**: `D`=uninterruptible sleep (usually I/O), `I`=idle kernel thread, `R`=running/runnable,
`S`=interruptible sleep, `T`=stopped (job control), `t`=stopped (debugger trace), `W`=paging
(not valid since Linux 2.6 — effectively dead code today), `X`=dead (should never actually be
observed), `Z`=zombie. BSD-format additions: `<`=high-priority, `N`=low-priority (niced),
`L`=has locked pages, `s`=session leader, `l`=multithreaded (`CLONE_THREAD`/NPTL), `+`=foreground
process group.

**Simple explanation**: this is the exact same state machine as `signal(7)`'s `Stop`/`Cont`
disposition actions (link 3) — `T`/`t` here are what a process looks like from the *outside*
after receiving `SIGSTOP`/a stop signal; `SIGCONT` moves it back to `R`/`S`.

**Try it**:
```sh
ps -eo stat --no-headers | cut -c1 | sort | uniq -c | sort -rn   # census of every state on this machine right now
sleep 60 &
set BPID $last_pid
kill -STOP $BPID
ps -o pid,stat -p $BPID       # expect T
kill -CONT $BPID
ps -o pid,stat -p $BPID       # expect S again
kill -KILL $BPID
```
bash/sh: `BPID=$!` in place of `set BPID $last_pid`.

## OBSOLETE SORT KEYS / AIX FORMAT DESCRIPTORS (summarized, not itemized)

**Claim**: `OBSOLETE SORT KEYS` are single-letter sort keys used only by the legacy BSD `O`
sort syntax (`O[+|-]k1,...`) — the page explicitly says the modern `--sort`/`k` options use the
STANDARD FORMAT SPECIFIERS names instead, not these letters. `AIX FORMAT DESCRIPTORS` are an
alternate naming scheme for output columns, for AIX-compatibility. Neither is something to reach
for on a modern Linux system by choice — both exist purely for compatibility with older scripts.

**Try it** (confirm they're legacy without needing to memorize them):
```sh
man 1 ps | grep -A3 "OBSOLETE SORT KEYS"
man 1 ps | grep -A3 "AIX FORMAT DESCRIPTORS"
```

## STANDARD FORMAT SPECIFIERS (curated subset — ~15 of 100+, the practically essential ones)

**Claim + Try it, combined** (each keyword shown with its header, one-line meaning, and a live
column):
```sh
ps -eo pid,ppid,pgid,sid,tname,euser,ruser,stat,pcpu,pmem,vsz,rss,nice,pri,etime,wchan:20,comm | head -8
```
- `pid`/`ppid`/`pgid`/`sid` — process/parent/group/session IDs (link 1's `credentials(7)` concepts,
  visible live).
- `tname` (alias `tty`) — controlling terminal.
- `euser`/`ruser` — effective/real username (again: link 1's real-vs-effective distinction).
- `stat` — the process-state-code string covered above.
- `pcpu`/`pmem` (aliases `%cpu`/`%mem`) — CPU/memory percentage, per the NOTES caveats above.
- `vsz`/`rss` — virtual size / resident set size in KiB (the same undercounting caveat from NOTES
  applies to `rss`).
- `nice`/`pri` — scheduling niceness and kernel-computed priority.
- `etime` — elapsed wall-clock time since the process started (distinct from `time`/`cputime`,
  which is CPU time consumed, not wall-clock age).
- `wchan` — kernel function the process is sleeping in, if blocked (name truncates by default;
  widen with `wchan:20`-style explicit width, as used above).
- `comm`/`args`/`cmd` — executable name only / full command with args / alias for `args` — the
  exact distinction the `c` output-modifier flips between (Output Modifiers, above).
- `blocked`/`caught`/`ignored` — signal masks, direct tie to link 3 (`signal(7)`)'s
  `SigBlk`/`SigCgt`/`SigIgn` `/proc` fields — same data, different presentation.

**Try it** (the signal-mask tie-in specifically):
```sh
ps -eo pid,blocked,caught,ignored,comm | head -5
grep -E '^Sig(Blk|Cgt|Ign):' /proc/self/status   # same three values, /proc-native form, for your own shell
```

## PERSONALITY

**Claim**: `ps`'s option-parsing behavior can emulate ~20 historical Unix variants
(`bsd`/`sunos4`/`aix`/`hpux`/`irix`/`solaris2`/`tru64`/...), selected via `PS_PERSONALITY`/
`CMD_ENV`. The page's own recommendation: **`linux`** — everything else exists for compatibility
with scripts written against another system's `ps`.

**Try it**:
```sh
echo $CMD_ENV $PS_PERSONALITY   # almost certainly both empty -- confirms this machine uses the linux default
```

## ENVIRONMENT VARIABLES (the two actually worth knowing)

**Claim**: `PS_FORMAT` sets a default `-o`-style format (with `DefSysV`/`DefBSD` macros
available); `COLUMNS`/`LINES` override detected display width/height. The page's own advice:
setting most of the other listed variables (`POSIXLY_CORRECT`, `UNIX95`, etc.) is "a bad idea."

**Try it**:
```sh
env PS_FORMAT="pid,comm" ps -e | head -5   # override the default format for one invocation only
```

## BUGS / SEE ALSO

**Claim**: `bsdstart`/`start` always show English month abbreviations regardless of locale;
`lstart`/`stime` respect locale but can then overflow their column width. Related pages:
`pgrep(1)`, `pstree(1)`, `top(1)`, `strftime(3)`, `proc(5)` (link 2), `capabilities(7)` (pulled
into link 1 already).

**Try it**:
```sh
which pgrep pstree top 2>&1
```
