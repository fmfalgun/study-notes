# Link 2 — Exercise: `proc(5)`

All read-only inspection of your own processes plus one optional root-only remount check
(explicitly marked, don't run it unless you're fine with touching your live `/proc` mount).

Commands are written for **fish** (this machine's default interactive shell) — see the
shell-compatibility note in `../../README.md` if running from bash/sh instead (`$$`→`$fish_pid`).

---

### 1. Confirm the mount itself

```sh
grep " /proc " /proc/mounts
mount -t proc
stat -f /proc
```
Identify the mount options currently active (compare against the `hidepid=`/`subset=pid` options
from the notes — most desktop systems run with neither set, i.e. `hidepid=0` default).

### 2. `/proc/self` vs `/proc/$fish_pid` vs `/proc/<literal PID>`

```fish
echo $fish_pid
readlink -f /proc/self
ls -di /proc/self /proc/$fish_pid | awk '{print $1}'   # expect DIFFERENT inode numbers -- see below
```
bash/sh:
```bash
echo $$
readlink -f /proc/self
ls -di /proc/self /proc/$$ | awk '{print $1}'
```
Confirms `/proc/self` is a magic symlink that always resolves to *whoever's reading it* — not a
fixed target. **Correction**: because `ls` is itself a separate process from your shell, `/proc/self`
inside that one `ls` invocation resolves to `ls`'s own PID, not your shell's — so the two inode
numbers you get back are expected to be *different*, not the same. If you want a same-process
comparison instead, you'd need something that reads both paths from within the shell itself (no
external command in between).

### 3. Threads: `/proc/self/task/`

```sh
ls /proc/self/task/
```

Then run this in one terminal and, **while it's still sleeping**, check its task dir from another
terminal (or a second pane):
```sh
python3 -c "
import threading, os, time
def worker():
    time.sleep(8)
t = threading.Thread(target=worker)
t.start()
print('pid:', os.getpid())
t.join()
"
```
```sh
# in the second terminal, within the 8-second window:
ls /proc/<printed-pid>/task/
```
You should see **two** entries (main thread + worker thread) while it's running — this is the
`proc_pid_task(5)` claim made concrete.

### 4. The dumpable attribute

```sh
python3 -c "
import ctypes
libc = ctypes.CDLL('libc.so.6')
PR_GET_DUMPABLE = 3
print('dumpable:', libc.prctl(PR_GET_DUMPABLE, 0, 0, 0, 0))
"
ls -ld /proc/$fish_pid
```
bash/sh: same python3 block, then `ls -ld /proc/$$`.
`1` = dumpable (normal state for your own shell) — confirms why `/proc/$fish_pid` is owned by you,
not root.

### 5. Null-byte-separated files

```sh
cat /proc/self/cmdline; echo               # unreadable run-on line
cat /proc/self/cmdline | tr '\000' '\n'; echo   # readable, one arg per line
cat /proc/self/environ | tr '\000' '\n' | wc -l  # count of env vars
```

### 6. A taste of the system-wide files (not the deep dive — just confirm they're live data)

```sh
cat /proc/loadavg
head -3 /proc/meminfo
grep MHz /proc/cpuinfo | head -1
```
Run `uptime` and `free -h` right after, and confirm the numbers roughly match what you just read
raw from `/proc` — this is the "everything ps/free/uptime use is just parsed /proc text" point.

### 7. (Optional, root, changes live mount state — read the notes' hidepid explanation first)

```sh
sudo mount -o remount,hidepid=2 /proc
ls -la /proc | grep -c '^d'          # compare pid-dir count as non-root vs before
sudo mount -o remount,hidepid=0 /proc   # put it back
```

### 8. Self-check

1. What's the practical difference between `/proc/pid` and `/proc/tid` visibility when listing
   `/proc`?
2. Why would a shared university/lab server want `hidepid=2`?
3. Why does `cat /proc/self/cmdline` look broken without `tr '\000' '\n'`?

**Answers given, with corrections**:

1. Given answer: "pid is for process id and tid is for thread id." Correct definition, but misses
   the actual question — *visibility*, not naming. `/proc/<pid>` dirs **show up** in `ls /proc`;
   `/proc/<tid>` dirs (non-leader threads) do **not** show up in a listing, but still work by exact
   path — hidden from browsing, not actually inaccessible.
2. Given answer: "to separate resources n maintain confidentiality/access-control." Right instinct,
   slightly off reasoning — it's not resource separation (that's cgroups/quotas' job).
   `hidepid=2` specifically **hides one user's running processes from other users** on the same
   box: without it, any user can read everyone else's `cmdline`/`environ` (which can leak
   passwords typed as arguments) and even just see *that* a given program is running — a real
   privacy leak on a shared, mutually-untrusting-users server.
3. Given answer: "coz it is one line with trailing \000 which represent new line." The mechanism is
   backwards — `\000` does **not** represent a newline. It's the opposite: an *invisible,
   non-printing* control character. The terminal renders it as nothing at all — no space, no
   break — so the separate arguments just get jammed together with zero visible separation.
   `tr '\000' '\n'` works by *replacing* each invisible null with an actual, visible newline; it's
   a substitution of one separator for a different (visible) one, not decoding something that
   already "represents" a newline.
