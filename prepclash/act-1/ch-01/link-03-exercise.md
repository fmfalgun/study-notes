# Link 3 — Exercise: `signal(7)`

Fish primary; bash/sh forms called out where they differ. All commands spawn/signal only your own
processes — nothing destructive.

---

### 1. Disposition basics: catch, ignore, default

```fish
function on_usr1 --on-signal USR1
    echo "caught SIGUSR1"
end
kill -USR1 $fish_pid
```
bash/sh:
```bash
trap 'echo caught SIGUSR1' USR1
kill -USR1 $$
```

### 2. Sending signals to a real spawned process

```fish
sleep 60 &
set BPID $last_pid
kill -TERM $BPID
```
bash/sh: `sleep 60 & BPID=$!; kill -TERM $BPID`.

### 3. `pause(2)` — must catch the waking signal, or the default action wins

```sh
timeout 3 python3 -c "
import signal
signal.signal(signal.SIGALRM, lambda s, f: None)
signal.alarm(1)
print('pausing...')
signal.pause()
print('woken by a signal')
"
```
Remove the `signal.signal(...)` line and rerun — explain why the process now just dies silently
instead of printing the second line (tie this back to `SIGALRM`'s default disposition from the
standard-signals table).

### 4. Synchronous signal acceptance

```sh
python3 -c "
import signal, os
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])
os.kill(os.getpid(), signal.SIGUSR1)
info = signal.sigwaitinfo([signal.SIGUSR1])
print('synchronously accepted signal', info.si_signo, 'from PID', info.si_pid)
"
```

### 5. `/proc` fields for mask/pending/caught/ignored

```sh
grep -E '^Sig(Blk|Cgt|Ign|Pnd)|^ShdPnd' /proc/self/status
```
Run this in a shell where you've set a trap/event handler (step 1) vs. a fresh shell with none —
compare the `SigCgt` hex value between the two and confirm it changed.

### 6. Standard signals table, live

```sh
kill -l
kill -l SEGV; kill -l KILL; kill -l TERM
uname -m
```

### 7. Standard signals do NOT queue — prove it

```sh
python3 -c "
import signal, os
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])
for _ in range(5): os.kill(os.getpid(), signal.SIGUSR1)
count = 0
while signal.sigtimedwait([signal.SIGUSR1], 0.2) is not None:
    count += 1
print('drained', count, 'of 5 sent -- standard signals collapse into one pending instance')
"
```

### 8. Real-time signals DO queue, AND deliver low-numbered-first — prove both

```sh
python3 -c "
import signal, os
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGRTMIN])
for _ in range(3): os.kill(os.getpid(), signal.SIGRTMIN)
count = 0
while signal.sigtimedwait([signal.SIGRTMIN], 0.2) is not None:
    count += 1
print('drained', count, 'of 3 sent -- real-time signals queue individually')
"
python3 -c "
import signal, os, time
received = []
def h(s, f): received.append(s)
signal.signal(signal.SIGRTMIN, h); signal.signal(signal.SIGRTMIN + 1, h)
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGRTMIN, signal.SIGRTMIN + 1])
os.kill(os.getpid(), signal.SIGRTMIN + 1)    # higher-numbered sent FIRST
os.kill(os.getpid(), signal.SIGRTMIN)        # lower-numbered sent SECOND
signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGRTMIN, signal.SIGRTMIN + 1])
time.sleep(0.1)
print('delivery order:', received, '-- low-numbered wins despite being sent second')
"
```
Run step 7's version again but with the signals *not* pre-blocked (drop the `pthread_sigmask`
calls) — the count comes out different. Explain why, in terms of "simultaneously pending" vs.
"delivered and handled before the next send even happens."

### 9. `time.sleep()` vs. real `sleep(3)` — a stdlib abstraction gotcha

```sh
timeout 8 python3 -c "
import signal, time
signal.signal(signal.SIGALRM, lambda s, f: None)
signal.alarm(1)
start = time.monotonic()
time.sleep(5)
print('elapsed:', round(time.monotonic() - start, 1), 's')
"
```
The man page says `sleep(3)` is never restarted and returns the remaining seconds early. Your
measured elapsed time here is ~5s, not ~1s. Explain the discrepancy (hint: PEP 475, and the
difference between a C library function and a Python stdlib wrapper around it).

### 10. Hardware-exception signals — trigger one for real (safely, in a subprocess)

```sh
python3 -c "
import subprocess, signal
r = subprocess.run(['python3', '-c', 'import ctypes; ctypes.string_at(0)'])
sig = -r.returncode if r.returncode < 0 else None
print('child died from signal', sig, '=', signal.Signals(sig).name if sig else 'n/a')
"
```
This dereferences a null pointer in a throwaway subprocess (safe — it only crashes that child).
Confirm which signal fired (should be `SIGSEGV` on this architecture) and connect it back to the
BUGS section's point about the hardware-exception-to-signal mapping being architecture-dependent
and not always the "logical" choice.

### 11. Self-check

1. Why does `execve(2)` reset *handled* signal dispositions to default but leave *ignored* ones
   alone?
2. Name the one property that makes real-time signals fundamentally different from standard
   signals in a way that actually matters for application design (not just "they queue").
3. What's the practical difference between catching a signal with a handler vs. accepting it
   synchronously via `sigwaitinfo`/`signalfd`, and when would you prefer the latter?
4. Why is `SIGKILL` special-cased at the kernel level instead of just being "a signal whose
   default action is Term, that everyone agrees not to catch by convention"?
