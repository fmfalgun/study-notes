# Link 1 — Notes: `credentials(7)` — process identifiers

Source: https://man7.org/linux/man-pages/man7/credentials.7.html
Local equivalent: `man 7 credentials`

One-level-deep reference pulled in: `capabilities(7)` → "Effect of user ID changes on
capabilities" section only (the one paragraph credentials(7) explicitly points at for real
detail — not the full capabilities page, which is its own huge topic).

---

## Process ID (PID)

**Claim**: every process gets a unique nonnegative integer ID on creation via `fork(2)`;
obtained with `getpid(2)`; used by `kill`, `ptrace`, `setpriority`, `setpgid`, `setsid`,
`sigqueue`, `waitpid`; preserved across `execve(2)`.

**Simple explanation**: the PID is the process's name tag. "Preserved across execve" means
replacing a process's code (e.g. a shell `exec`-ing into another program) does *not* give it a
new PID — same process, new program image.

**Try it** (fish — this machine's default shell; `$$`/`$!` are bash/POSIX-only and will error in
fish, see the shell-compatibility note in `../../README.md`):
```fish
echo $fish_pid                       # PID of your current shell
ps -o pid,cmd -p $fish_pid
bash -c 'echo $$; exec sleep 5'      # single-quoted -> passed to bash literally, works from fish too
                                      # watch the PID stay the same even though the program changed
```

## Parent process ID (PPID)

**Claim**: identifies the process that `fork(2)`-created this one; obtained with `getppid(2)`;
also preserved across `execve(2)`.

**Simple explanation**: every process (except the very first) has a parent. If the parent dies
first, the child gets re-parented (usually to PID 1 / your session's subreaper).

**Try it** (fish has no `$PPID` variable — read it back via `ps` instead; bash/sh keep `$PPID`
directly, shown alongside):
```fish
ps -o ppid= -p $fish_pid | string trim   # your shell's parent PID
ps -o pid,ppid,cmd -p $fish_pid
pstree -p $fish_pid      # visualize the parent chain (install: Arch `pacman -S psmisc`, Debian `apt install psmisc`)
```
```bash
echo $PPID                     # bash/sh: just a builtin variable, no ps needed
ps -o pid,ppid,cmd -p $$
pstree -p $$
```

## Process group ID and session ID

**Claim**: every process has a session ID (`getsid(2)`) and process group ID (`getpgrp(2)`); a
process group ("job") shares a process group ID, created by the shell per command/pipeline; a
session is a collection of process groups sharing a session ID, created via `setsid(2)`; the
process whose PID equals its PGID is the group leader; sessions have one controlling terminal;
at most one job is the foreground job — background jobs reading from the terminal get `SIGTTIN`,
writing (if `TOSTOP` is set) gets `SIGTTOU`; Ctrl-C-style keys signal the foreground job.

**Simple explanation**: this is the machinery behind shell job control. `ls | wc` — both
processes share one process group, so Ctrl-C kills both at once. A session is everything tied to
one terminal login; closing the terminal can signal the whole session.

**Try it** (fish):
```fish
ls | wc -l &                      # backgrounds a pipeline (one process group)
ps -o pid,ppid,pgid,sid,tty,stat,cmd

sleep 60 &
set BPID $last_pid                # fish: PID of the job you just backgrounded
ps -o pid,pgid,sid -p $BPID       # PGID here equals BPID -> sleep is its own group leader
kill $BPID

# background job trying to read the terminal gets SIGTTIN and stops:
cat &
jobs -l                           # note the Stopped state
kill (jobs -p)                    # fish command substitution: (...) not $(...)
```
Same sequence in bash/sh:
```bash
ls | wc -l &
ps -o pid,ppid,pgid,sid,tty,stat,cmd

sleep 60 &
BPID=$!                           # bash: PID of the job you just backgrounded
ps -o pid,pgid,sid -p $BPID
kill $BPID

cat &
jobs -l
kill %1                           # or: kill $!
```

## User and group identifiers

**Claim**: each process has several distinct UID/GID pairs, all `uid_t`/`gid_t`:
- **Real UID/GID** — who owns the process (`getuid(2)`/`getgid(2)`).
- **Effective UID/GID** — used for permission checks on shared resources (message queues, shared
  memory, semaphores); on Linux, *file* access uses the filesystem IDs below instead
  (`geteuid(2)`/`getegid(2)`).
- **Saved set-user-ID/set-group-ID** — a stashed copy of the effective ID at `execve(2)` time, so
  a setuid program can drop privilege and re-acquire it later via `seteuid`/`setreuid`/`setresuid`
  (`getresuid(2)`/`getresgid(2)`).
- **Filesystem UID/GID** (Linux-only) — actually governs file-access permission checks; normally
  tracks the effective ID automatically, can be split off with `setfsuid(2)`/`setfsgid(2)`.
- **Supplementary group IDs** — extra groups for file/resource permission checks
  (`getgroups(2)`); max count via `sysconf(_SC_NGROUPS_MAX)`.

Real/supplementary IDs are preserved across `execve(2)`; effective/saved may change (setuid-bit
programs). User IDs also gate: sending signals (`kill(2)`), scheduling params, resource-limit
checks, inotify instance limits.

**Simple explanation**: "real" is who you logged in as. "Effective" is who the kernel is
currently treating you as for most permission checks (this is what changes when a setuid binary
runs). "Saved" is a bookmark so a privileged program can safely drop and later reclaim privilege
without needing to be root again. "Filesystem" is a Linux-specific extra layer, rarely touched
directly, that's what *actually* gates file access (in practice it just mirrors effective).

**Try it**:
```sh
id                                 # real uid/gid + supplementary groups
id -u; id -g; id -G                # just the numbers
grep -E '^(Uid|Gid|Groups):' /proc/self/status   # shows real/effective/saved/fs, all 4 columns
                                    # (order for Uid/Gid line is: real, effective, saved-set, filesystem)

ls -l /usr/bin/passwd              # find a setuid-root binary: the 's' in owner-exec bit
stat -c '%A %U' /usr/bin/passwd

python3 -c "import os; print('real', os.getuid(), 'eff', os.geteuid())"
```

## Modifying process user and group IDs

**Claim**: APIs and exactly what each touches:
- `setuid(2)`/`setgid(2)` — real (and possibly effective+saved).
- `seteuid(2)`/`setegid(2)` — effective only.
- `setfsuid(2)`/`setfsgid(2)` — filesystem only.
- `setreuid(2)`/`setregid(2)` — real and effective (and possibly saved).
- `setresuid(2)`/`setresgid(2)` — real, effective, and saved, all explicitly.
- `setgroups(2)` — supplementary group list.

Effective-ID changes auto-propagate to the filesystem ID, and can flip the process's "dumpable"
attribute (see `prctl(2)`, and `proc(5)` — covered in link 2). Changes to UID/GID **can change
the process's capabilities** (next point).

**Simple explanation**: `setresuid` is the precise, unambiguous one to reach for if you're writing
privilege-drop code — it sets all three IDs explicitly instead of relying on implicit rules.

**Try it**:
```sh
man 2 setresuid | head -30       # read the actual syscall contract
python3 -c "
import os
print('before:', os.getresuid())
# only root can actually change to an arbitrary uid — this just reads, doesn't change, if not root
"
sudo -n true 2>/dev/null && echo "passwordless sudo available" || echo "no passwordless sudo (expected on a normal box)"
```

## Effect of user-ID changes on capabilities (from `capabilities(7)`, one level deep)

**Claim**: when a thread's real/effective/saved/filesystem UID changes via `setuid`/`setresuid`/
etc., the kernel adjusts capability sets to preserve traditional 0-vs-nonzero-UID semantics:
- If real/effective/saved were **all previously 0** and the change makes **all of them nonzero**,
  every capability is cleared from the permitted, effective, and ambient sets.
- Effective UID 0 → nonzero: effective capability set cleared.
- Effective UID nonzero → 0: permitted set copied into effective set.
- Filesystem UID 0 → nonzero: specific effective capabilities cleared (`CAP_CHOWN`,
  `CAP_DAC_OVERRIDE`, `CAP_DAC_READ_SEARCH`, `CAP_FOWNER`, `CAP_FSETID`, `CAP_LINUX_IMMUTABLE`,
  `CAP_MAC_OVERRIDE`, `CAP_MKNOD`); filesystem UID nonzero → 0 re-enables those that are in the
  permitted set.
- `SECBIT_KEEP_CAPS` securebit exists specifically to prevent the permitted set from being wiped
  when a thread drops all its UIDs to 0→nonzero on purpose while still wanting to keep them.

**Simple explanation**: "root" isn't really one flag — it's UID 0 plus a bag of capabilities, and
the kernel silently adjusts that capability bag whenever your UID crosses the 0/nonzero boundary.
This is *why* dropping privileges by just calling `setuid(nonroot)` is safe by default: the
capabilities go away with the UID change, not just the UID number.

**Try it** (fish; bash/sh: swap `$fish_pid` for `$$`):
```fish
getpcaps $fish_pid                # your shell's current capability set (usually near-empty as a normal user)
capsh --print                    # fuller picture: current/bounding/ambient sets, securebits
                                  # install if missing: Arch `pacman -S libcap`, Debian `apt install libcap2-bin`

# as root, compare before/after dropping to a normal user (read-only demo, don't actually run destructively):
man 7 capabilities | grep -A5 "Effect of user ID changes"
```

## `/proc/pid/status` connection

**Claim**: various fields in `/proc/pid/status` expose these credentials directly; see `proc(5)`
(link 2).

**Try it**:
```sh
grep -E '^(Uid|Gid|Groups|CapInh|CapPrm|CapEff|CapBnd|CapAmb):' /proc/self/status
```

## Threads share credentials (mostly)

**Claim**: POSIX requires credentials be shared across all threads in a process; at the kernel
level Linux actually keeps **separate** per-thread credentials, and glibc's NPTL threading
implementation does extra work to propagate any `setuid`/`setresuid`-style change to every thread
so POSIX semantics hold in practice. See `nptl(7)` for detail (not expanded here — out of scope
for this link, would need its own link entry).

**Simple explanation**: don't assume changing UID in one thread of a multithreaded program is
instantly safe/atomic across all threads at the kernel level — it's glibc doing the syncing work,
not the kernel itself.
