# Link 3 — Notes: `signal(7)` — overview of signals

Source: https://man7.org/linux/man-pages/man7/signal.7.html
Local equivalent: `man 7 signal`

One-level-deep reference pulled in: `signal-safety(7)` (NOTES section explicitly delegates "what's
safe to call inside a handler" here — real detail, not a name-drop).

---

## Signal dispositions

**Claim**: every signal has a current disposition controlling what happens on delivery — default
actions: **Term** (terminate), **Ign** (ignore), **Core** (terminate + dump core), **Stop**
(stop the process), **Cont** (continue if stopped). Changed via `sigaction(2)` or `signal(2)`
(latter less portable for handler installation). A process can: run the default action, ignore the
signal, or catch it with a handler. Handlers run on the normal stack by default, or an alternate
one via `sigaltstack(2)`. Disposition is per-**process** (same across all threads). `fork(2)`
copies dispositions; `execve(2)` resets *handled* signals to default but leaves *ignored* signals
ignored.

**Simple explanation**: "ignored" survives `exec` because it's a deliberate choice about the
signal itself; "handled" doesn't survive because the handler function's code no longer exists once
`exec` replaces the program image.

**Try it** (fish):
```fish
trap 2>&1 | head -3   # fish has no `trap` builtin the bash way -- see the function-based form below
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

## Sending a signal

**Claim**: `raise(3)` (to caller's own thread), `kill(2)` (to a PID/process-group/everyone),
`pidfd_send_signal(2)` (to a process identified by a PID file descriptor — avoids PID-reuse races),
`killpg(3)` (to a whole process group), `pthread_kill(3)` (to a specific POSIX thread in the same
process), `tgkill(2)` (to a specific thread in a specific process — what `pthread_kill(3)` is
built on), `sigqueue(3)` (real-time signal + accompanying data).

**Try it** (fish):
```fish
sleep 60 &
set BPID $last_pid
kill -TERM $BPID
```
bash/sh: `sleep 60 & BPID=$!; kill -TERM $BPID`.

## Waiting for a signal to be caught

**Claim**: `pause(2)` (suspend until any signal is caught), `sigsuspend(2)` (atomically swap the
signal mask and suspend until an unmasked signal is caught).

**Try it**:
```sh
timeout 3 python3 -c "
import signal
signal.signal(signal.SIGALRM, lambda s, f: None)   # must catch it -- SIGALRM's default action is Term
signal.alarm(1)
print('pausing...')
signal.pause()
print('woken by a signal')
"
```

## Synchronously accepting a signal

**Claim**: two mechanisms to *synchronously* accept a signal instead of catching it
asynchronously via a handler: `sigwaitinfo(2)`/`sigtimedwait(2)`/`sigwait(3)` (block until one of
a specified set arrives, return info about it), or `signalfd(2)` (get a file descriptor you can
`read(2)` — each read blocks until a matching signal arrives, returns a struct describing it).

**Simple explanation**: `signalfd` turns "a signal happened" into an ordinary readable file
descriptor — lets you `select`/`poll`/`epoll` on signals alongside sockets and other I/O in one
event loop, instead of juggling async handlers.

**Try it** (the `sigwaitinfo`/`sigtimedwait` half — Python's stdlib doesn't expose `signalfd(2)`
directly, unlike the syscalls above, so that half is `man 2 signalfd`-only, no runnable snippet):
```sh
python3 -c "
import signal, os
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])
os.kill(os.getpid(), signal.SIGUSR1)
info = signal.sigwaitinfo([signal.SIGUSR1])
print('synchronously accepted signal', info.si_signo, 'from PID', info.si_pid)
"
man 2 signalfd | head -20
```

## Signal mask and pending signals

**Claim**: a signal can be **blocked** (deferred until unblocked); between generation and delivery
it's **pending**. Each *thread* has its own independent mask (`pthread_sigmask(3)`; single-threaded
programs can use `sigprocmask(2)`). Mask is inherited across `fork(2)`, preserved across
`execve(2)`. A signal may be **process-directed** (targets the process as a whole — e.g. sent via
`kill(2)`/`sigqueue(3)`, or kernel-generated for non-hardware reasons) or **thread-directed**
(targets one specific thread — e.g. `SIGSEGV`/`SIGFPE` from a hardware exception in that thread's
own code, or sent via `tgkill(2)`/`pthread_kill(3)`). A process-directed signal goes to any one
thread that doesn't currently have it blocked (kernel picks arbitrarily if several qualify).
`sigpending(2)` returns the union of process-pending and thread-pending sets. `fork(2)` starts a
child with an empty pending set.

**Try it**:
```sh
grep -E '^Sig(Blk|Cgt|Ign|Pnd)|^ShdPnd' /proc/self/status
```
`SigBlk`/`SigCgt`/`SigIgn`/`SigPnd`/`ShdPnd` are exactly this section made visible — see the NOTES
point below for what each hex field means.

## Execution of signal handlers

**Claim**: on every kernel→user transition, the kernel checks for a pending, unblocked signal with
a handler installed. If found: (1) prep — remove signal from pending set, install the alternate
stack if `SA_ONSTACK` was used, save context (program counter, registers, mask, alt-stack
settings) onto a stack frame (accessible via `ucontext_t` if `SA_SIGINFO` was used); mask the
signals named in `sa_mask` plus (unless `SA_NODEFER`) the signal itself, for the handler's
duration; (2) build the handler's stack frame, point PC at the handler, arrange return-address to
land in the **signal trampoline**; (3) hand control to the handler; (4) on handler return, control
passes to the trampoline; (5) trampoline calls `sigreturn(2)`, which restores everything saved in
step 1 and resumes the interrupted code. If the handler never returns normally (`siglongjmp(3)`,
or it `execve(2)`s a new program), step 5 never runs — so restoring the signal mask afterward
becomes the *programmer's* responsibility. The kernel treats handler execution as ordinary
user-space code — nesting depth is limited only by the user-space stack.

**Simple explanation**: this is the mechanical answer to "how does a signal handler actually
interrupt my program and then let it continue as if nothing happened" — the kernel is essentially
doing a manual context-switch onto your handler and back, using your own stack as scratch space.

**Try it**:
```sh
man 2 sigreturn 2>&1 | head -15   # the syscall this whole mechanism hinges on
```

## Standard signals — the table

**Claim** (each row = one point; Action column per FHS-style claim, per the man page):
`SIGABRT`(Core), `SIGALRM`(Term), `SIGBUS`(Core), `SIGCHLD`(Ign), `SIGCONT`(Cont), `SIGFPE`(Core),
`SIGHUP`(Term), `SIGILL`(Core), `SIGINT`(Term), `SIGIO`/`SIGPOLL`(Term), `SIGKILL`(Term, **cannot
be caught, blocked, or ignored**), `SIGPIPE`(Term), `SIGPROF`(Term), `SIGPWR`(Term),
`SIGQUIT`(Core), `SIGSEGV`(Core), `SIGSTOP`(Stop, **cannot be caught, blocked, or ignored**),
`SIGTSTP`(Stop), `SIGSYS`(Core), `SIGTERM`(Term), `SIGTRAP`(Core), `SIGTTIN`/`SIGTTOU`(Stop),
`SIGURG`(Ign), `SIGUSR1`/`SIGUSR2`(Term), `SIGVTALRM`(Term), `SIGXCPU`/`SIGXFSZ`(Core),
`SIGWINCH`(Ign). Up to Linux 2.2, `SIGSYS`/`SIGXCPU`/`SIGXFSZ`/(non-SPARC/MIPS)`SIGBUS` terminated
*without* a core dump; Linux 2.4+ conforms to POSIX.1-2001 and dumps core for these.

**Try it**:
```sh
kill -l                          # the full name/number table on this machine, live
man 7 signal | grep -A2 '^     SIGSEGV'
```

## Queueing and delivery semantics for standard signals

**Claim**: if multiple *standard* signals are pending, delivery order is **unspecified**.
Standard signals do **not** queue — multiple instances of the same signal while blocked collapse
into one pending instance; the `siginfo_t` recorded is from the *first* instance, not overwritten
by later ones.

**Try it**:
```sh
python3 -c "
import signal, os, time
count = [0]
def h(s, f): count[0] += 1
signal.signal(signal.SIGUSR1, h)
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])
for _ in range(5):
    os.kill(os.getpid(), signal.SIGUSR1)   # send 5 instances while blocked
signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGUSR1])
time.sleep(0.1)
print('handler ran', count[0], 'time(s) despite 5 sends -- standard signals do not queue')
"
```

## Signal numbering for standard signals

**Claim**: numeric values differ by architecture — the table's 4 columns are x86/ARM/most-others,
Alpha/SPARC, MIPS, PARISC. `SIGRTMIN`/`SIGRTMAX` bound the real-time range separately (next
point). `SIGUNUSED` (synonym for `SIGSYS`) was removed from glibc 2.26 onward on every arch.

**Try it**:
```sh
kill -l SEGV; kill -l KILL; kill -l TERM   # numeric value on THIS architecture specifically
uname -m
```

## Real-time signals

**Claim**: since Linux 2.2 (POSIX.1b). Range: `SIGRTMIN`..`SIGRTMAX`, kernel supports 33
(numbered 32-64), but glibc's NPTL reserves 2 (LinuxThreads reserved 3) for its own internal use,
adjusting the effective `SIGRTMIN` to 34 or 35 — **never hardcode real-time signal numbers, always
use `SIGRTMIN+n`** with a runtime check against `SIGRTMAX`. No predefined meaning — fully
application-defined. Default action if unhandled: terminate. Distinguishing properties vs.
standard signals: (1) **do** queue — multiple instances all get delivered; (2) `sigqueue(3)` can
attach a value (int or pointer), retrievable via `siginfo_t.si_value` in an `SA_SIGINFO` handler,
plus `si_pid`/`si_uid` of the sender; (3) **guaranteed delivery order** — same-type instances in
send order, different types low-numbered-first. If both standard and real-time signals are
pending, POSIX leaves priority unspecified; Linux prioritizes standard signals. Queue-depth limit:
historically `/proc/sys/kernel/rtsig-max`/`rtsig-nr` (≤ Linux 2.6.7), replaced by the
`RLIMIT_SIGPENDING` per-user resource limit (Linux 2.6.8+). Old vs. new syscalls (32-bit → 64-bit
`sigset_t` widening): `sigaction`→`rt_sigaction`, `sigpending`→`rt_sigpending`,
`sigprocmask`→`rt_sigprocmask`, `sigreturn`→`rt_sigreturn`, `sigsuspend`→`rt_sigsuspend`,
`sigtimedwait`→`rt_sigtimedwait`.

**Try it**:
```sh
python3 -c "import signal; print('SIGRTMIN =', signal.SIGRTMIN, ' SIGRTMAX =', signal.SIGRTMAX)"
```
Confirm real-time queueing (all 3 delivered, unlike standard signals above) — this needs
`sigtimedwait` draining the queue one at a time rather than an async handler counting a flag: an
async Python handler only sets a per-signal-number flag and can visibly coalesce multiple pending
same-number real-time signals into a single Python-level callback, which would make the queueing
claim look false even though the kernel queued all 3 correctly:
```sh
python3 -c "
import signal, os
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGRTMIN])
for _ in range(3): os.kill(os.getpid(), signal.SIGRTMIN)
count = 0
while signal.sigtimedwait([signal.SIGRTMIN], 0.2) is not None:
    count += 1
print('drained', count, 'queued real-time signal(s) for 3 sends')
"
python3 -c "
import signal, os
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])
for _ in range(3): os.kill(os.getpid(), signal.SIGUSR1)
count = 0
while signal.sigtimedwait([signal.SIGUSR1], 0.2) is not None:
    count += 1
print('drained', count, 'queued standard signal(s) for 3 sends -- contrast with the real-time count above')
"
```
Confirm low-numbered-first ordering when two different real-time signals are simultaneously
pending:
```sh
python3 -c "
import signal, os, time
received = []
def h(s, f): received.append(s)
signal.signal(signal.SIGRTMIN, h); signal.signal(signal.SIGRTMIN + 1, h)
signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGRTMIN, signal.SIGRTMIN + 1])
os.kill(os.getpid(), signal.SIGRTMIN + 1)   # send higher-numbered first
os.kill(os.getpid(), signal.SIGRTMIN)       # then lower-numbered, while both still pending
signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGRTMIN, signal.SIGRTMIN + 1])
time.sleep(0.1)
print('delivery order:', received, '-- expect [SIGRTMIN, SIGRTMIN+1] despite send order')
"
```
**Caveat learned while verifying this**: sending both signals back-to-back *without* blocking
first often delivers each one immediately as it's sent (no real race), which can make it look like
send-order determines delivery-order. Blocking both first, so they're genuinely simultaneously
pending before either is handled, is what actually exercises the ordering guarantee.

## Interruption of system calls/library functions by signal handlers

**Claim**: if a handler fires while a blocking call is in progress, either the call auto-restarts
after the handler returns (if `SA_RESTART` was set), or it fails with `EINTR`. Auto-restartable
(with `SA_RESTART`): `read`/`readv`/`write`/`writev`/`ioctl` on "slow" devices (terminal/pipe/
socket — NOT local disk, which is never signal-interrupted), `open(2)` if it can block (e.g. a
FIFO), the `wait*` family, socket calls (unless a timeout is set), file-locking calls, POSIX
message-queue calls, `futex(2)` `FUTEX_WAIT`/`FUTEX_WAIT_BITSET`, `getrandom(2)`, POSIX semaphore
waits, `inotify(7)` reads (Linux 3.8+). **Never** restarted regardless of `SA_RESTART` (always
`EINTR` on interruption): socket calls *with* a timeout set, the signal-waiting calls themselves
(`pause`/`sigsuspend`/`sigtimedwait`/`sigwaitinfo`), `epoll`/`poll`/`select`/`pselect` family,
System V IPC calls, sleep calls (`nanosleep`/`clock_nanosleep`/`usleep`), `io_getevents(2)`.
`sleep(3)` specifically: never restarted, but returns success with the remaining seconds instead
of an error.

**Try it** (Python's own `time.sleep()` isn't a good demo for this specific point — since PEP 475,
CPython auto-retries `time.sleep()` across an `EINTR` all the way to the originally requested
duration, verified below; this masks the raw C `sleep(3)` "returns early with remaining time"
behavior the man page describes, so read the man text directly instead for this one):
```sh
timeout 8 python3 -c "
import signal, time
signal.signal(signal.SIGALRM, lambda s, f: None)
signal.alarm(1)
start = time.monotonic()
time.sleep(5)
print('elapsed:', round(time.monotonic() - start, 1), 's -- CPython restarted through the interruption to the full 5s')
"
man 7 signal | grep -B2 -A3 'never restarted after'
```

**Claim**: even with *no* signal handler installed, certain blocking interfaces can fail with
`EINTR` after being stopped (a stop signal) and later resumed (`SIGCONT`) — not sanctioned by
POSIX.1, Linux-specific behavior. Affected: timeout-set socket calls, `epoll_wait`/`epoll_pwait`,
`semop`/`semtimedop`, `sigtimedwait`/`sigwaitinfo` (plus some now-historical cases: pre-3.8
inotify reads, pre-2.6.22 futex/semaphore waits, pre-2.4 `nanosleep`).

**Try it**:
```sh
man 7 signal | grep -B2 -A10 'even in the absence of signal handlers'
```

## NOTES — async-signal-safety and `/proc` fields (one level deep: `signal-safety(7)`)

**Claim**: an async-signal-safe function is safe to call from inside a handler; most nonreentrant
functions are not. Classic example: `stdio` functions maintain a static buffer + position state —
if a handler interrupts a `printf(3)` mid-update and itself calls `printf(3)`, the second call
corrupts shared state. Two fixes: (a) handler calls only async-signal-safe functions and is itself
reentrant w.r.t. globals, or (b) block signals in the main program around unsafe operations —
POSIX.1 mandates a specific set of functions be async-signal-safe (`write`, `_exit`, `kill`,
`signal`, and similar low-level, non-buffering calls are the classic safe set; `malloc`/`printf`/
most of libc's higher-level surface is *not* safe).

Also: `/proc/pid/task/tid/status` fields `SigBlk`/`SigCgt`/`SigIgn` (blocking/catching/ignoring —
identical across all threads of a process) and `SigPnd`/`ShdPnd` (thread-pending vs.
process-pending) — the `/proc/pid/status` fields you already checked above are the *main thread's*
view of the same data.

**Try it**:
```sh
grep -E '^Sig(Blk|Cgt|Ign|Pnd)|^ShdPnd' /proc/self/status   # main-thread view
python3 -c "
import signal
print('SIGKILL blockable in mask?', signal.SIGKILL in signal.valid_signals())  # it's 'valid' but the kernel silently ignores attempts to block/catch/ignore it
"
```

## BUGS — hardware-exception signal mapping is architecture-dependent and not always sensible

**Claim**: six signals can arise from a hardware exception (`SIGBUS`, `SIGEMT`, `SIGFPE`,
`SIGILL`, `SIGSEGV`, `SIGTRAP`) — *which* one fires for a given exception is undocumented and
inconsistent across architectures (an invalid access might be `SIGSEGV` on one arch, `SIGBUS` on
another). Concrete x86 example: the `int` instruction with an argument other than 3 or 128
produces `SIGSEGV`, even though `SIGILL` would make more logical sense, purely because of how the
CPU reports that specific fault to the kernel.

**Simple explanation**: don't write portable code that pattern-matches on *which* signal a crash
produced to diagnose *why* it crashed — the mapping itself is a documented gray area, not a
reliable signal (pun intended).
