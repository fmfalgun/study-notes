# Link 2 — Notes: `proc(5)` — process/system information pseudo-filesystem

Source: https://man7.org/linux/man-pages/man5/proc.5.html
Local equivalent: `man 5 proc`

**Scope boundary (important)**: current `proc(5)` is a short hub/overview page — the old
monolithic version that documented every single `/proc/pid/status` field etc. in one giant page
has been split across ~55+ separate man pages (`proc_pid_status(5)`, `proc_pid_maps(5)`, ...).
Per the one-level-deep rule: this link folds in the *structural* pages `proc(5)` explicitly
delegates real content to for its own overview claims (`proc_pid(5)` / `proc_self(5)`, and
`proc_pid_task(5)` / `proc_tid(5)` / `proc_thread-self(5)` — these three names are aliases for one
underlying page each on this system). It does **not** expand into the ~55-entry "See also" index
of individual `/proc/[a-z]*` system-file pages, or the further ~45-entry index of individual
`/proc/pid/*` file pages inside `proc_pid(5)` — those are each just a bibliography-style pointer,
not delegated detail, and each deserves its own future `link-NN` if/when you want it.

---

## What the proc filesystem is

**Claim**: a pseudo-filesystem exposing kernel data structures as files, normally mounted at
`/proc`, usually auto-mounted; most files read-only, some writable (lets you change kernel
variables through them).

**Simple explanation**: `/proc` isn't real files on disk — reading them asks the kernel a
question live, in real time, formatted as text.

**Try it**:
```sh
grep " /proc " /proc/mounts        # confirm the mount and its options
mount -t proc                      # same info via `mount`
stat -f /proc                      # filesystem type should show 0x9fa0 (PROC_SUPER_MAGIC)
ls -la /proc | head                # numeric dirs = PIDs, plus system-wide files/dirs
```

## Mount options

**Claim** (`hidepid=n`, since Linux 3.3): controls who can see inside `/proc/pid` directories.
- `hidepid=0` (default): everyone can access all `/proc/pid` dirs.
- `hidepid=1`: users can't access files/subdirs inside *other* users' `/proc/pid` dirs (the
  directories stay visible, but sensitive files like `cmdline`/`status` are blocked) — hides
  whether a specific program is running.
- `hidepid=2`: as 1, but other users' `/proc/pid` directories become fully invisible — hides PID
  existence itself from directory listing (though `kill -0 $PID` can still probe existence).
- `gid=gid`: a group exempted from `hidepid` restrictions, cleaner than sudoers hacks.

**Claim** (`subset=pid`, since Linux 5.8): mount option that hides all top-level `/proc` files/
dirs unrelated to tasks — a hardening option for containers that only need process info, not
full system telemetry exposed.

**Simple explanation**: `hidepid` is a real, deployed hardening control — shared/multi-user
systems (student labs, shared servers) commonly set `hidepid=2` so users can't snoop on what
processes other users are running.

**Try it**:
```sh
grep " /proc " /proc/mounts | grep -o 'hidepid=[0-9]'   # check current hidepid setting (often absent = 0)
man 5 proc | grep -A3 'hidepid=n'                        # re-read the option text locally
# Changing this requires a remount and root — read-only demo, don't actually remount your live /proc:
# sudo mount -o remount,hidepid=2 /proc
```

## Overview — the four structural entry points

**Claim**: `/proc/pid/` (see `proc_pid(5)`), `/proc/tid/` (see `proc_tid(5)`), `/proc/self`
(magic symlink to your own `/proc/pid`, see `proc_self(5)`), `/proc/thread-self` (magic symlink to
your own thread's `/proc/self/task/tid`, see `proc_thread-self(5)`). `/proc/pid` dirs are visible
when listing `/proc`; `/proc/tid` dirs are not (but are still usable by exact path).

**Try it**:
```sh
readlink -f /proc/self             # resolves to your PID right now
readlink -f /proc/thread-self      # resolves to your PID's main-thread task dir
ls -d /proc/[0-9]* | wc -l         # count of visible /proc/pid dirs
ls /proc/self/task/                # your thread ID(s) — one entry for a single-threaded shell
```

## `proc_pid(5)` — one level deep: ownership and the "dumpable" attribute

**Claim**: files inside `/proc/pid/` are normally owned by the process's effective UID/GID.
Exception: if the process's **dumpable** attribute isn't `1`, ownership is forced to `root:root`
(or the namespace's root, since Linux 4.11, inside containers). Dumpable can change via
`prctl(2)` `PR_SET_DUMPABLE`, or reset automatically per `/proc/sys/fs/suid_dumpable` rules
(triggered by UID/GID changes — this is exactly the credentials.7 connection from link 1).
Resetting dumpable to 1 reverts ownership back to the process's effective UID/GID.

**Simple explanation**: "dumpable" originally meant "is this process allowed to core-dump."
The kernel repurposed it as a security gate: a process that changed privilege (e.g. a setuid
binary) gets its `/proc/pid/*` files locked to root ownership so an unprivileged user can't read
its memory maps, environment, etc. through `/proc` after it dropped privilege.

**Try it** (fish — this machine's default shell; see the shell-compatibility note in
`../../README.md` for the bash/POSIX forms of `$fish_pid`/`(cmd)` used below):
```fish
grep -i dumpable /usr/include/linux/prctl.h 2>/dev/null; or echo "PR_SET_DUMPABLE not in local headers, that's fine"
prlimit --pid $fish_pid 2>/dev/null | head -1  # sanity check prlimit works, unrelated but same neighborhood

python3 -c "
import ctypes
libc = ctypes.CDLL('libc.so.6')
PR_GET_DUMPABLE = 3
print('dumpable:', libc.prctl(PR_GET_DUMPABLE, 0, 0, 0, 0))   # 1 = dumpable, this shell's normal state
"

ls -ld /proc/$fish_pid               # owned by you, since your shell is dumpable=1
```
bash/sh:
```bash
grep -i dumpable /usr/include/linux/prctl.h 2>/dev/null || echo "PR_SET_DUMPABLE not in local headers, that's fine"
prlimit --pid $$ 2>/dev/null | head -1

python3 -c "
import ctypes
libc = ctypes.CDLL('libc.so.6')
PR_GET_DUMPABLE = 3
print('dumpable:', libc.prctl(PR_GET_DUMPABLE, 0, 0, 0, 0))
"

ls -ld /proc/$$
```

## `proc_pid_task(5)` — one level deep: thread subdirectories

**Claim**: `/proc/pid/task/` has one subdir per thread (named by `tid`, see `gettid(2)`); shared
attributes (e.g. `cwd`) are identical across all `task/tid/*` files, per-thread attributes (e.g.
some `status` fields) can differ. `/proc/tid/` (for non-leader threads) mirrors the same content
but isn't visible in a plain `/proc` directory listing — only reachable by exact path.
`/proc/thread-self/` (since Linux 3.17) is a magic symlink to the calling thread's own
`task/tid` entry.

**Try it**:
```sh
ls /proc/self/task/                       # thread IDs for this shell (just 1, for a plain shell)
cat /proc/self/task/*/status | grep -m1 -E '^(Pid|Tgid):'

python3 -c "
import threading, os, time
def worker():
    print('worker tid:', os.listdir(f'/proc/self/task'))
    time.sleep(1)
t = threading.Thread(target=worker)
t.start()
print('main pid:', os.getpid())
t.join()
"
# run the python3 snippet above, then re-check /proc/self/task/ WHILE it's sleeping in another terminal:
# fish:        ls /proc/(pgrep -f 'python3 -c')/task/
# bash/sh:     ls /proc/$(pgrep -f 'python3 -c')/task/
# -- should show 2 entries while the thread is alive
```

## The `tr '\000' '\n'` note

**Claim**: many `/proc` files (environment, command line) use internal null-byte-separated
fields, not newlines — pipe through `tr '\000' '\n'` to make them human-readable.

**Try it**:
```sh
cat /proc/self/cmdline | tr '\000' '\n'; echo
cat /proc/self/environ | tr '\000' '\n' | head -5
# without tr, this prints one unreadable run-on line:
cat /proc/self/cmdline; echo
```

## The `/proc/[a-z]*` system-wide index (intentionally not expanded here)

**Claim**: dozens of other top-level `/proc` entries expose system-wide info (`proc_meminfo(5)`,
`proc_cpuinfo(5)`, `proc_loadavg(5)`, `proc_interrupts(5)`, `proc_net(5)`, `proc_sys(5)`, etc.) —
listed in the doc as a bare "See also" index, no per-entry detail on the page itself.

**Try it** (a taste, without treating this as the full topic — each of these could become its own
future link):
```sh
head -5 /proc/meminfo
cat /proc/loadavg
head -1 /proc/cpuinfo
```

---

## Session findings — hands-on gotchas from running this exercise

Practical discoveries made while actually running the exercise commands, worth keeping for future
reference (mostly tooling-specific consequences of the "`/proc/self` resolves to whoever's
currently reading it" claim above, not new claims about `proc(5)` itself).

1. **`/proc/self` inside a glob is a trap once a *different* process opens the expanded path** —
   the shell expands `/proc/self/task/*` using its own view of `self` (so it lists its own
   threads), but the literal word `self` survives into the resulting path text unresolved. A
   second, separate process (e.g. a pager) that later opens those exact paths gets *its own*
   `self`, not the shell's — producing "No such file or directory" for paths that look perfectly
   valid. Fix: substitute a real, fixed PID (`$fish_pid`) before globbing, so there's nothing left
   for a later process to misinterpret.
2. **The same trap breaks an "inode of `/proc/self` should match `/proc/<shell's own pid>`" check
   when run through an external command** — `ls` is a separate process from the shell, so
   `/proc/self` inside that one `ls` invocation resolves to `ls`'s own PID, not the shell's;
   expect two genuinely *different* inode numbers, not matching ones (see the corrected comment in
   the exercise file).
3. **`/proc/self` is safe and consistent *within* one process's own threads**, unlike the two
   points above — a background thread inside the *same* process reading `/proc/self/task/` still
   sees that whole process's full thread list correctly, because `self` means "the process," not
   "this specific thread." The failure mode above is strictly a cross-*process* issue, not a
   cross-thread one.
4. **A pager/viewer can render some `/proc` files fine and silently print nothing for others** —
   smaller files (`loadavg`, `cmdline`, `environ`) rendered correctly through the same tool and
   style flags that produced empty output for `/proc/meminfo`. Suspected cause: such tools may
   trust the file's *reported* size for buffering decisions, and procfs files report `0` bytes
   regardless of actual content — `cat` remains the reliable fallback for `/proc` content when a
   fancier viewer goes silent.
5. **A themed shell prompt's red/error indicator can reflect the *previous* command's exit status,
   not the one about to run** — a `grep`/pattern-match that legitimately finds zero matches exits
   non-zero (normal, expected behavior for "not found"), and that status can display as an error
   marker one line later, looking like the *next* typed command failed when it didn't.
6. **`head -l` vs `head -1`** — lowercase L and the digit one are easy to mistype and look near-
   identical in many fonts; `-l` isn't a valid `head` flag and errors immediately. A typo, not a
   conceptual mistake.
7. **`hidepid=2` remount concretely and sharply reduces the visible `/proc` directory-entry count**
   for a normal (non-root) listing compared to `hidepid=0` — dropped to roughly a quarter of the
   entries in this run, then fully restored after remounting back to `hidepid=0`. Confirms the
   notes' claim with a real before/after count, not just the option's description.
