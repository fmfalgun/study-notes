# Link 9 — Exercise: `ps(1)`

Fish primary; bash/sh forms called out where they differ. All read-only observation of live system
state, except the `kill -STOP`/`-CONT`/`-KILL` step which only touches a `sleep` you spawn
yourself.

---

### 1. Default selection vs. "everything," in both grammars

```sh
ps
ps -e | wc -l
ps ax | wc -l
```
Confirm the first command's much smaller output matches the "your EUID, your terminal" default
from the notes, and that `-e`/`ax` give the same (or very close) total count despite different
option grammars.

### 2. The `-aux` vs. `aux` trap, on this actual machine

```sh
ps aux 2>&1 | head -1
ps -aux 2>&1 | head -1
getent passwd x 2>&1
```
The third command checks whether a user literally named `x` exists on this system. Explain,
using the notes' description of the ambiguity, exactly what `ps -aux` is technically asking for
versus what most people mean when they type it — and why the two commands' output likely matched
anyway on this machine specifically.

### 3. Process selection by list — PID, command name, and real vs. effective user

```fish
ps -p $fish_pid
```
bash/sh: `ps -p $$`.
```sh
ps -C bash 2>&1
ps -U $USER -u $USER u | head -5
```

### 4. Custom columns — build one from scratch, then rename and widen

```sh
ps -eo pid,ppid,user,stat,%cpu,%mem,comm --sort=-%cpu | head -8
ps -eo pid,ruser=RealUser,comm=Command --sort=-pid | head -5
ps -eo pid,wchan:20,comm | head -5
```
For the third command, pick one process whose `WCHAN` isn't `-` and look up what that kernel
function name suggests the process is currently blocked waiting on.

### 5. `-f`/`-F`/`-l`/`j` — compare the same processes across four format presets

```sh
ps -p 1 -f
ps -p 1 -F
ps -p 1 -l
ps -p 1 j
```
List which columns appear in `-F` but not `-f`, and which appear in `-l` but not `-f` — cross-
reference against the notes' per-option column lists to confirm your answer without guessing.

### 6. Process tree

```sh
ps -e --forest | head -15
ps axjf | head -15
```
Find your own shell's PID in the tree output and trace its ancestor chain up to PID 1.

### 7. Thread display

```fish
ps -eLf | head -5
ps -T -p $fish_pid
```
bash/sh: `ps -T -p $$`.
```sh
ps -eo pid,nlwp,comm | awk '$2 > 1' | sort -k2 -rn | head -5
```
The last command lists every process on the system with more than one thread, most-threaded
first. Pick the top one and explain why a program like that would plausibly need many threads.

### 8. Process state codes — force a real state transition and observe it

```fish
sleep 60 &
set BPID $last_pid
ps -o pid,stat -p $BPID
kill -STOP $BPID
ps -o pid,stat -p $BPID
kill -CONT $BPID
ps -o pid,stat -p $BPID
kill -KILL $BPID
```
bash/sh: `BPID=$!` in place of `set BPID $last_pid`.

Also survey the whole system's state distribution:
```sh
ps -eo stat --no-headers | cut -c1 | sort | uniq -c | sort -rn
```
Identify at least one process in `S` state and explain what it's most likely waiting on, and
check whether anything is in `D` state (uninterruptible sleep) — if so, that's usually I/O-bound;
if not, explain why `D` is normally rare to observe on a healthy desktop system.

### 9. Signal masks via `ps`, cross-checked against `/proc` directly (ties back to link 3)

```sh
ps -eo pid,blocked,caught,ignored,comm | head -5
grep -E '^Sig(Blk|Cgt|Ign):' /proc/self/status
```
Confirm the second command's three hex values correspond conceptually to the `blocked`/`caught`/
`ignored` columns you'd see for your own shell's PID in the first command's style of output (run
`ps -o pid,blocked,caught,ignored,comm -p` your own PID directly to compare exactly).

### 10. CPU%/memory caveats, made concrete

```sh
ps -eo pid,%cpu | awk 'NR>1{s+=$2} END{print "sum of %CPU:", s}'
ps -eo rss,comm --sort=-rss | head -5
```
Explain why the `%CPU` sum from the first command is not a reliable "total system CPU load"
figure, per the NOTES section's own caveat — what would you use instead to get real system-wide
CPU utilization?

### 11. `PS_FORMAT` and format-listing introspection

```sh
env PS_FORMAT="pid,comm" ps -e | head -5
ps L | wc -l
ps L | head -20
```
Compare the `PS_FORMAT`-driven output against an equivalent `ps -eo pid,comm` — confirm they
produce the same columns via two different mechanisms.

### 12. Self-check

1. Explain, precisely, the difference between what `-a` and `x` each do to the *selection* set —
   not just "they show more processes," but the specific restriction each one lifts.
2. Why does the notes file connect `ps`'s `euser`/`ruser` format specifiers back to link 1
   (`credentials(7)`) instead of treating them as `ps`-specific concepts?
3. Give one concrete reason `SIZE`/`RSS` numbers from `ps` should not be trusted as an exact
   memory-accounting figure, per the NOTES caveats.
4. What's the actual mechanical relationship between a process showing `STAT` of `T` in `ps` and
   the `SIGSTOP`/`SIGCONT` material from link 3 — is `T` itself a signal, or something else?
