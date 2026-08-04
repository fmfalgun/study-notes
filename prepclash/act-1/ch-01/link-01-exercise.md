# Link 1 — Exercise: `credentials(7)`

Run these on your own machine (Arch and/or Debian), in order. Every command here is read-only or
touches only processes you spawn yourself — nothing destructive, nothing needs root except where
explicitly noted as optional.

Commands are written for **fish** (this machine's default interactive shell) — see the
shell-compatibility note in `../../README.md` if you're running these from a plain bash/sh
session instead (mainly: `$$`→`$fish_pid`, `$!`→`$last_pid`, `$(cmd)`→`(cmd)`).

**Tooling needed** (skip installs if already present):
- `pstree` — Arch: `sudo pacman -S psmisc` · Debian: `sudo apt install psmisc`
- `getpcaps` / `capsh` — Arch: `sudo pacman -S libcap` · Debian: `sudo apt install libcap2-bin`

---

### 1. Identity of your current shell

```fish
echo "PID=$fish_pid PPID="(ps -o ppid= -p $fish_pid | string trim)
ps -o pid,ppid,pgid,sid,tty,stat,cmd -p $fish_pid
id
```
bash/sh:
```bash
echo "PID=$$ PPID=$PPID"
ps -o pid,ppid,pgid,sid,tty,stat,cmd -p $$
id
```
Confirm you can map every column in the `ps` output back to a term from the notes (PID, PPID,
PGID, SID).

### 2. `execve` preserves PID/PPID — only the program image changes

```fish
bash -c 'echo "before exec: PID=$$"; exec sh -c "echo after exec: PID=$$"'
```
Single-quoted, so it's handed to `bash -c` literally regardless of your login shell. Same PID
printed both times, even though the running program changed from `bash` to `sh`.

### 3. Process groups and job control

```fish
sleep 100 &
set BPID $last_pid
ps -o pid,ppid,pgid,sid,stat,cmd -p $BPID
kill $BPID          # clean up
```
bash/sh:
```bash
sleep 100 &
BPID=$!
ps -o pid,ppid,pgid,sid,stat,cmd -p $BPID
kill $BPID
```
Confirm PID == PGID for this backgrounded `sleep` (it's its own group leader, since it's the only
process in that pipeline).

```fish
ls | wc -l &
wait
ps -o pid,pgid,cmd -p (jobs -p)    # jobs -p may be empty by now if it already finished — that's fine,
                                   # rerun and check `jobs -l` immediately after backgrounding instead
```
bash/sh: same, but capture the pgid via `jobs -l` before it finishes (no `$(jobs -p)`-style
one-liner needed here — `ps -o pid,pgid,cmd` immediately after backgrounding is enough).
Two processes (`ls`, `wc`) sharing one PGID is the "a pipeline is one job" claim from the notes.

### 4. Foreground/background terminal signaling

```fish
cat &          # backgrounds a process that wants to read the terminal
jobs -l        # note it's already Stopped — that's SIGTTIN from the notes, delivered automatically
kill (jobs -p) # clean up the stopped job
```
bash/sh:
```bash
cat &
jobs -l
kill %1        # or: kill $!
```

### 5. The four UID/GID columns

```sh
grep -E '^(Uid|Gid|Groups):' /proc/self/status
```
Identify which of the four numbers on the `Uid:`/`Gid:` line is real, effective, saved-set, and
filesystem (order: real, effective, saved-set, filesystem — per the notes). On a normal login
shell they'll all be identical; that's expected, not a bug.

### 6. Find a real setuid binary and reason about what it does

```sh
ls -l /usr/bin/passwd
stat -c '%A %U:%G %n' /usr/bin/passwd
```
Identify the `s` in the permission string (owner execute position). Explain out loud: when you run
`passwd` as a normal user, what does its *effective* UID become during execution, and why does it
need that to edit `/etc/shadow`?

### 7. Capabilities tied to your current process

```fish
getpcaps $fish_pid
capsh --print
```
bash/sh: `getpcaps $$` (rest identical).
Confirm your normal-user shell has an empty (or near-empty) permitted/effective capability set —
this is the practical evidence for "capabilities are gated by UID 0, and get stripped when UID
goes nonzero" from the notes.

### 8. Cross-check against `/proc/self/status`'s capability fields directly

```sh
grep -E '^Cap(Inh|Prm|Eff|Bnd|Amb):' /proc/self/status
```
These are hex bitmasks — `capsh --decode=<hexvalue>` (same package as above) translates one back
into capability names if you want to double check `capsh --print`'s output matches.

### 9. (Optional, root only, read-only) Compare capability sets before/after privilege drop

```sh
sudo bash -c 'echo "as root:"; capsh --print | head -6; setpriv --reuid 1000 --regid 1000 --clear-groups -- capsh --print | head -6'
```
Replace `1000` with your own UID if different (`id -u`). Watch the permitted/effective capability
sets collapse to empty the moment the UID leaves 0 — this is the exact rule from the notes
("effective UID 0 → nonzero clears the effective capability set... all all-zero → all-nonzero
clears permitted+effective+ambient").

### 10. Self-check

Without re-reading the notes, explain out loud:
1. Why does a setuid-root binary need the *saved* UID, not just real+effective?
2. Why is `setresuid` preferred over `setuid`/`seteuid` for writing careful privilege-drop code?
3. What's the practical difference between "effective UID" and "filesystem UID" on Linux?
