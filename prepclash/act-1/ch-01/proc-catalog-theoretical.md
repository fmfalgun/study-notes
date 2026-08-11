# `/proc` Reference Catalog — patterns for security/forensics triage

Companion to `link-02-notes.md` (which covers `proc(5)` as a structural hub page). This file goes
the other direction: it expands the "intentionally not expanded" `/proc/[a-z]*` and `/proc/pid/*`
indexes from that page, but filtered and annotated specifically for **live incident-response /
process-triage use** — not exhaustive coverage of every field on every page.

**Scope boundary**: every entry below is sourced from one of the official documentation sets
listed in the task — man7.org Linux man-pages, kernel.org's canonical `proc.rst`, Arch/Debian/
Kali/Garuda official docs where they actually have relevant content. No blogs, no Stack Overflow,
no tutorials. Each claim below is followed by a `[source: ...]` tag; the References section at the
bottom lists every distinct URL used.

This is a **documentation research artifact** — no live commands were run and no real filesystem
was touched while producing it (unlike `link-02-notes.md`'s "Try it" blocks).

---

## Part 1 — Per-process files (`/proc/<pid>/*`)

Each entry: what it exposes, then why a security analyst would check it during triage.

### Identity / command line

**`cmdline`** — null-byte-separated argv strings the process "wants you to see." A process can
rewrite its own argv after `execve(2)`, override the backing memory region, or use `prctl(2)`
`PR_SET_MM_ARG_START` to redirect where this file reads from — so it is **not a reliable audit
trail**, only a self-reported one. Empty for zombie processes.
[source: https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html]
- *Analyst use*: first thing to check for a suspicious PID, but cross-check against `exe`, `maps`,
  and `auxv` rather than trusting it alone — process-hollowing / argv-spoofing malware specifically
  targets this file's self-reported nature.

**`comm`** — the command name (≤16 chars, silently truncated), a superset of `prctl(2)`
`PR_SET_NAME`/`PR_GET_NAME`. Writable by the process (or any thread in its group) — so, like
`cmdline`, it's spoofable self-reported data, not ground truth.
[source: https://man7.org/linux/man-pages/man5/proc_pid_comm.5.html]
- *Analyst use*: quick label, but never authoritative — malware renaming itself to `[kworker/…]`
  to blend in with kernel threads is a classic trick this field enables.

**`exe`** — symlink to the executable's on-disk path. If the backing file has been unlinked, the
link resolves with `" (deleted)"` appended to the original path.
[source: https://man7.org/linux/man-pages/man5/proc_pid_exe.5.html]
- *Analyst use*: the single highest-value fileless/self-deleting-malware indicator in `/proc` — a
  running process whose `exe` shows `(deleted)` has no backing file left on disk to inspect
  normally; you must recover the binary bytes from `/proc/<pid>/exe` itself (or `mem`) before the
  process exits. Requires `PTRACE_MODE_READ_FSCREDS` to read/dereference; unavailable once the main
  thread of a multithreaded process has terminated.

**`cwd`** — symlink to the process's current working directory.
[source: https://man7.org/linux/man-pages/man5/proc_pid_cwd.5.html]
- *Analyst use*: reveals where a process was launched from / is currently rooted in, useful for
  correlating with dropped files or a working directory full of staged exfil data.

**`root`** — symlink to the process's root directory, reflecting any `chroot(2)` applied to it. The
man page's own worked example shows how `/proc/<pid>/root/etc` from outside a namespace can reveal
an empty tmpfs rather than the host's real `/etc`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_root.5.html]
- *Analyst use*: detects chroot/jail confinement and — combined with `ns/mnt` — helps tell whether
  a process is running inside a container's filesystem view vs. the host's. Same
  `PTRACE_MODE_READ_FSCREDS` and multithreaded-main-thread-exit caveats as `cwd`/`exe`.

### Status, resource, and scheduling state

**`status`** — human-readable status/memory summary. Forensically relevant fields: `State`
(running/sleeping/disk-sleep/stopped/tracing-stop/zombie/dead), `PPid`, `TracerPid` (nonzero means
something is currently `ptrace`-attached — e.g. a debugger, or a sandbox/EDR hook, or a malicious
process attached to steal memory), `Uid`/`Gid` (all four of real/effective/saved-set/filesystem —
divergence between these is a privilege-transition signal), `VmPeak`/`VmSize`/`VmRSS`, `Threads`,
signal masks `SigBlk`/`SigIgn`/`SigCgt` (a process ignoring/blocking `SIGKILL`-adjacent signals or
catching unusual signals is worth a second look), the capability sets `CapInh`/`CapPrm`/`CapEff`/
`CapBnd`/`CapAmb` (this is the `capabilities(7)` and `credentials(7)` link from earlier chapters —
an unprivileged-looking process with a nonzero `CapEff` is a red flag), `Seccomp` mode, and
`Cpus_allowed`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_status.5.html]
- *Analyst use*: the single richest "at a glance" file for a suspicious PID — state, parentage,
  privilege, and capability posture in one read.

**`stat`** — the machine-parsable sibling of `status`, source for `ps(1)`. Fields include `pid`,
`comm` (also 16-char-truncated here), single-letter `state`, `ppid`, `pgrp`, `session`, `tty_nr`,
kernel `flags`, `utime`/`stime` (CPU time in clock ticks), `starttime` (time since boot — lets you
compute exact process age/start timestamp), `priority`, `nice`, `num_threads`. Some fields are
gated `[PT]` (ptrace-permission-dependent) and read as 0 if permission is denied.
[source: https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html]
- *Analyst use*: `starttime` is the reliable way to timestamp when a process actually began (versus
  trusting a log line); scripting-friendly for bulk triage across many PIDs.

**`statm`** — memory usage in pages: `size` (≈`VmSize`), `resident` (≈`VmRSS`), `shared`
(file-backed resident pages), `text`, `lib` (unused, always 0 since Linux 2.6), `data`, `dt`
(unused, always 0 since Linux 2.6). Doc notes some values are inaccurate due to kernel
optimizations; recommends `smaps`/`smaps_rollup` for precision.
[source: https://man7.org/linux/man-pages/man5/proc_pid_statm.5.html]
- *Analyst use*: cheap/fast memory footprint check; use `smaps` instead when you actually need
  trustworthy numbers for e.g. detecting an anomalously large heap from an injected payload.

**`io`** — per-process I/O counters since Linux 2.6.20: `rchar`/`wchar` (bytes through
read/write-family syscalls), `syscr`/`syscw` (syscall counts, including `sendfile`,
`copy_file_range`, and I/O-shaped `ioctl`s), `read_bytes`/`write_bytes` (actual storage-layer I/O),
`cancelled_write_bytes` (writeback saved by truncation). Requires `PTRACE_MODE_READ_FSCREDS`;
counters are not atomic on systems where 64-bit ops can tear.
[source: https://man7.org/linux/man-pages/man5/proc_pid_io.5.html]
- *Analyst use*: a process with huge `wchar`/`write_bytes` and no obvious reason (e.g. a shell
  process) suggests exfiltration or ransomware-style mass file writes in progress.

**`limits`** — soft/hard `getrlimit(2)`-equivalent resource limits table (readable by all users
since Linux 2.6.36).
[source: https://man7.org/linux/man-pages/man5/proc_pid_limits.5.html]
- *Analyst use*: unusually high `RLIMIT_NOFILE`/`RLIMIT_NPROC` on an otherwise ordinary process can
  indicate prep for a fork-bomb or fd-exhaustion-style attack, or a service intentionally configured
  to survive resource pressure.

**`oom_score`** — the kernel's current OOM-killer-selection ranking; higher means more likely to be
killed under memory pressure. Reflects any adjustment applied via `oom_score_adj`/`oom_adj`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html]
- *Analyst use*: a process with `oom_score_adj` deliberately set to `-1000` (OOM-immune) is
  suspicious persistence behavior — malware protecting itself from being reaped under memory
  pressure.

**`wchan`** — symbolic kernel function name where a sleeping/blocked process currently sits.
Requires `PTRACE_MODE_READ_FSCREDS`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_wchan.5.html]

**`syscall`** — while blocked in a syscall: syscall number, argument registers, stack pointer, and
program counter. Shows `-1` for the syscall number if blocked outside a syscall, or the literal
string `"running"` if actively executing. Requires `CONFIG_HAVE_ARCH_TRACEHOOK` and ptrace
permission.
[source: https://man7.org/linux/man-pages/man5/proc_pid_syscall.5.html]
- *Analyst use*: `wchan`+`syscall` together let you snapshot exactly what a hung or suspicious
  process is doing at the kernel level without attaching a full debugger.

**`auxv`** — the ELF auxiliary vector passed by the interpreter at `exec` time, as ID/value pairs
terminated by a zero pair; same data `getauxval(3)` exposes programmatically. Requires
`PTRACE_MODE_READ_FSCREDS`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_auxv.5.html]
- *Analyst use*: can reveal the real interpreter/base-address info even when `cmdline`/`comm` have
  been spoofed, since it's kernel-populated at exec rather than process-controlled.

**`coredump_filter`** — bitmask controlling which memory segment types are included if the process
core-dumps; full semantics documented in `core(5)`, not this page itself.
[source: https://man7.org/linux/man-pages/man5/proc_pid_coredump_filter.5.html]
- *Analyst use*: if you plan to force a core dump of a live suspicious process for offline memory
  forensics, check/adjust this first so anonymous and file-backed mappings you need aren't excluded.

### Memory mapping / raw memory access

**`maps`** — one line per mapped memory region: address range, `perms` (r/w/x, plus s=shared or
p=private-copy-on-write), file `offset`, `dev` (major:minor), `inode` (0 = no backing inode),
`pathname`. Special pathnames: `[heap]`, `[stack]`, `[stack:tid]` (per-thread stacks, Linux
3.4–4.4 only), `[vdso]`, `[anon:name]` (named private anonymous mapping, Linux 5.17+),
`[anon_shmem:name]` (Linux 6.2+). Blank pathname = anonymous `mmap()`. File-backed mappings show
`" (deleted)"` if the backing file was removed.
[source: https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html]
- *Analyst use*: the primary tool for spotting **injected code** — an executable (`x` permission)
  anonymous mapping with no backing file, or a mapping whose pathname shows `(deleted)`, is a
  strong indicator of process injection or a self-deleting payload still resident in memory.

**`smaps`** — per-mapping expansion of `maps` (since Linux 2.6.14) adding `Size`, `Rss`, `Pss`
(proportional share), `Shared_Clean`/`Shared_Dirty`/`Private_Clean`/`Private_Dirty`, `Referenced`,
`Anonymous`, `Swap`, `KernelPageSize`, `MMUPageSize`, `Locked`, `ProtectionKey` (x86, Linux 4.9+),
and `VmFlags` (kernel-attribute flags like `rd`, `ex`, `io`).
[source: https://man7.org/linux/man-pages/man5/proc_pid_smaps.5.html]
- *Analyst use*: `Pss`/`Rss` per-mapping is the accurate way to size an anonymous executable region
  you've flagged from `maps`; `VmFlags` containing both writable and executable attributes on the
  same region (W+X) is a classic injected-shellcode signature that a security-hardened process
  shouldn't normally have.

**`mem`** — the process's raw memory image itself, accessed via `open(2)`/`lseek(2)`/`read(2)` (seek
to an offset from `maps`, then read). Gated by `PTRACE_MODE_ATTACH_FSCREDS` — the same privilege
level required to attach a debugger, so generally only the owner or root.
[source: https://man7.org/linux/man-pages/man5/proc_pid_mem.5.html]
- *Analyst use*: this is how you actually dump the bytes of a flagged anonymous/injected mapping
  found via `maps`/`smaps`, or recover a `(deleted)` executable's code before the process exits —
  the last-resort memory-acquisition primitive `/proc` offers without a separate tool.

### File descriptors and I/O objects

**`fd/`** — one symlink per open file descriptor, named by fd number. Regular files/directories
resolve to their real path (with `(deleted)` suffix if unlinked, per general `/proc` symlink
behavior). Pipes and sockets appear as pseudo-paths `type:[inode]` (e.g. `socket:[2248868]`),
cross-referenceable against `/proc/net/*`. Descriptors without a backing inode (from `bpf()`,
`epoll_create()`, `eventfd()`, `inotify_init()`) show as `anon_inode:file-type`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html]
- *Analyst use*: enumerate exactly what files/sockets/pipes a suspicious process currently holds
  open — including deleted files still held open (a common log-tampering / anti-forensics pattern:
  a process deletes a file from the directory tree but keeps its fd open, so the data is still
  recoverable via `/proc/<pid>/fd/<n>` until the process exits).

**`fdinfo/`** — per-fd metadata: universal `pos` (file offset), `flags` (octal, includes
`O_CLOEXEC`), `mnt_id` (Linux 3.15+); plus type-specific detail — `eventfd` counter value,
`epoll` monitored-fd list with event masks, `signalfd` accepted-signal mask, `inotify` watch
descriptors (inode/device/event mask/handle), `fanotify` mark info, `timerfd` clock/expiration/
interval. Only the owning process can read these.
[source: https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html]
- *Analyst use*: the `inotify`/`fanotify` entries can reveal a process that's watching specific
  files or directories for changes — relevant when investigating something that reacts to file
  drops (e.g. a loader watching a staging directory).

### Threads, security context, namespaces, cgroups

**`task/`** — one subdirectory per thread (named by `tid`), containing the same file set as
`/proc/pid/` itself. Shared attributes (e.g. `cwd`) read identically across threads; per-thread
attributes can differ. Unavailable once the main thread has exited via `pthread_exit()`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_task.5.html]
- *Analyst use*: multithreaded malware can have a worker thread doing the malicious work while the
  main thread looks benign — `task/<tid>/status` per-thread lets you catch that.

**`attr/`** — LSM (SELinux/AppArmor/Smack) security-attribute API. Key file `current` — the
process's active security context/label (writable since Linux 2.6.11, subject to policy). Related:
`exec` (context for next `execve`), `fscreate` (context for newly created files), `keycreate`,
`socketcreate`, `prev` (context before the last `execve`).
[source: https://man7.org/linux/man-pages/man5/proc_pid_attr.5.html]
- *Analyst use*: `attr/current` tells you the MAC label a process is actually confined under — an
  unexpectedly unconfined/permissive label on a process that should be sandboxed (e.g. a
  container's expected AppArmor profile missing) is a containment-failure indicator.

**`ns/`** — subdirectory of symlinks, one per namespace type supporting `setns(2)` (mnt, net, pid,
user, uts, ipc, cgroup, time), since Linux 3.0. The page itself is sparse on individual namespace
semantics, deferring to `namespaces(7)`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_ns.5.html]
- *Analyst use*: comparing `ns/*` symlink targets (they encode an inode number) across processes is
  the standard way to tell whether two processes share a namespace or are isolated from each other
  — e.g. confirming a process actually lives inside a specific container's namespaces rather than
  having escaped to the host's.

**`cgroup`** — the process's control-group memberships (since Linux 2.6.24); page defers detail to
`cgroups(7)`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_cgroup.5.html]
- *Analyst use*: identifies which container/pod a process actually belongs to on a shared host —
  useful when a suspicious PID needs to be attributed to a specific workload.

**`mountinfo`** — per-namespace mount table with 11 fields per entry: mount ID, parent ID, root
path (the real backing location), mount point (visible path), and propagation tags
(shared/master/unbindable), since Linux 2.6.26.
[source: https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html]
- *Analyst use*: reveals the actual filesystem boundaries a (possibly containerized) process can
  reach, including bind mounts that might unexpectedly expose host paths inside a container.

**`environ`** — the initial environment set at `execve(2)` time, null-separated. Does **not**
reflect later `putenv()`/direct-`environ`-manipulation changes, and the backing memory location can
be moved via `prctl(2)` `PR_SET_MM_ENV_START`. Requires `PTRACE_MODE_READ_FSCREDS`.
[source: https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html]
- *Analyst use*: often the fastest way to spot `LD_PRELOAD`, proxy variables, or credential material
  passed via env vars to a suspicious process — but remember it's a startup snapshot, not live state.

---

## Part 2 — System-wide files (`/proc/*`)

**`meminfo`** — system memory statistics: `MemTotal`, `MemFree`, `MemAvailable` (Linux 3.14+,
estimate of memory available for new apps without swapping), `Buffers`, `Cached` (page cache),
`SwapTotal`/`SwapFree`, plus `Active`/`Inactive`/`Dirty`/`Writeback`/`Slab`/`KernelStack`, etc.
Backs `free(1)`.
[source: https://man7.org/linux/man-pages/man5/proc_meminfo.5.html]
- *Analyst use*: baseline system memory-pressure check when triaging whether OOM-kill activity or
  swap thrashing is part of an incident's symptom set.

**`cpuinfo`** — architecture-dependent CPU/system info per logical processor (`processor` index,
`bogomips`, etc., varying by arch); backs `lscpu(1)`.
[source: https://man7.org/linux/man-pages/man5/proc_cpuinfo.5.html]

**`loadavg`** — five fields: 1/5/15-minute load averages (runnable + uninterruptible-disk-wait
jobs, same as `uptime`); a field with format `runnable/total` kernel scheduling entities; and the
PID of the most recently created process on the system.
[source: https://man7.org/linux/man-pages/man5/proc_loadavg.5.html]
- *Analyst use*: the last field (most-recently-created PID) is a cheap, race-prone but sometimes
  useful signal for "something just spawned" during live monitoring.

**`modules`** — text list of currently loaded kernel modules; backs `lsmod(8)`.
[source: https://man7.org/linux/man-pages/man5/proc_modules.5.html]
- *Analyst use*: baseline rootkit-hunting file — compare against an expected module list. Caveat
  (my own analytical note, not from the source): sufficiently capable LKM rootkits can hook the
  kernel structures backing this file and hide their own entry, so a clean `/proc/modules` read is
  evidence of absence only for less sophisticated threats — cross-check with `unhide`-style
  proc-vs-syscall comparison techniques (see Kali section below) or offline/out-of-band inspection.

**`mounts`** — since Linux 2.4.19, a symlink to `/proc/self/mounts`; shows the calling process's
mount namespace view in `fstab(5)` format. Pollable via `select`/`poll`/`epoll_wait` since Linux
2.6.15 for real-time mount/unmount change notification.
[source: https://man7.org/linux/man-pages/man5/proc_mounts.5.html]

**`net/`** — networking-layer info, reflecting the calling process's network namespace since Linux
2.6.25.
[source: https://man7.org/linux/man-pages/man5/proc_net.5.html]
- **`net/tcp`**, **`net/udp`** — kernel socket tables: `local_address`/`rem_address` (address:port,
  hex-encoded), `St` (internal socket state code), `uid` (effective UID of the socket's creator),
  tx/rx queue sizes. [source: https://man7.org/linux/man-pages/man5/proc_net.5.html]
  - *Analyst use*: correlate a `socket:[inode]` seen under a suspicious process's `fd/` against
    these tables to identify exactly what remote address/port that process is talking to, and which
    UID owns the socket — core network-forensics pivot.
- **`net/arp`** — ASCII dump of the kernel ARP table: IP, hardware type, flags, MAC address,
  device. [source: https://man7.org/linux/man-pages/man5/proc_net.5.html]
  - *Analyst use*: live IP-to-MAC mapping, useful for spotting ARP-spoofing artifacts or confirming
    what's actually on the local segment.
- **`net/dev`** — per-interface device statistics (packet counts, errors, collisions).
  [source: https://man7.org/linux/man-pages/man5/proc_net.5.html]
  - Note: the man7 `proc_net(5)` page does **not** document `/proc/net/route` contents — I could not
    find that as a separately documented field set on this page, so it's omitted here rather than
    guessed at.

**`sys/`** — root of the sysctl-tunable kernel-variable tree (present since Linux 1.3.57); readable/
writable through `/proc` itself (the `sysctl(2)` syscall route is deprecated). Values may be
strings (NUL/newline-terminated), decimal or `0x`-prefixed hex numbers, or space/tab/newline-
separated multi-value fields. Subdirectories include `sys/kernel`, `sys/net` (with `sys/net/ipv4`
etc.), `sys/vm`, `sys/fs`, plus `abi`/`debug`/`dev`/`user`.
[source: https://man7.org/linux/man-pages/man5/proc_sys.5.html]

**`sys/kernel/`** — selected entries relevant to security triage:
[source: https://man7.org/linux/man-pages/man5/proc_sys_kernel.5.html]
  - `dmesg_restrict` — gates unprivileged reads of the kernel log (0 = unrestricted, 1 =
    privileged-only). A value of 0 on a hardened system is itself a finding.
  - `kptr_restrict` — controls whether kernel pointers are exposed via `/proc` (0–2); relevant
    because leaked kernel addresses aid exploitation.
  - `yama/ptrace_scope` — restricts which processes may `ptrace` which others; a weakened setting
    (0) widens the attack surface for credential/memory theft via `ptrace`.
  - `modules_disabled` — one-way switch that, once set, prevents further module loading; checking
    this tells you whether module-loading is currently possible at all as an attack vector.
  - `randomize_va_space` — ASLR policy (0 off / 1 partial / 2 full); 0 on a running system is a
    hardening regression worth flagging.
  - `core_pattern` — controls core-dump handling, including piping dumps to a program; a
    `core_pattern` rewritten to pipe into an attacker-controlled script is a known
    privilege-escalation/persistence technique.
  - `pid_max`, `threads-max`, `sysrq`, `panic`/`panic_on_oops`, `ctrl-alt-del`, `shmmax`/`shmall`/
    `shmmni` — general system-behavior tunables, lower triage priority but relevant to
    fork-bomb/resource-exhaustion scenarios.

---

## Part 3 — Mount-time hardening options

**`hidepid=<mode>`** (since Linux 3.3; man7 documents modes as numbers, kernel.org's `proc.rst`
additionally documents symbolic aliases):
- `hidepid=0` / `off` (default) — classic/traditional mode: everyone can access all `/proc/<pid>/`
  directories and their contents.
  [source: https://man7.org/linux/man-pages/man5/proc.5.html;
  https://www.kernel.org/doc/html/latest/filesystems/proc.html]
- `hidepid=1` / `noaccess` — users cannot access files/subdirectories inside *other* users'
  `/proc/<pid>/` (the directory itself stays visible/listable, but sensitive files like `cmdline`,
  `status`, and — per kernel.org's more detailed wording — `sched*` are blocked).
  [source: https://man7.org/linux/man-pages/man5/proc.5.html;
  https://www.kernel.org/doc/html/latest/filesystems/proc.html]
- `hidepid=2` / `invisible` — as mode 1, but other users' `/proc/<pid>/` directories become fully
  invisible (not just content-blocked) — hides PID existence from directory listings entirely.
  [source: https://man7.org/linux/man-pages/man5/proc.5.html;
  https://www.kernel.org/doc/html/latest/filesystems/proc.html]
- `hidepid=4` / `ptraceable` — documented only in the kernel.org `proc.rst` text (not present in the
  man7 `proc(5)` page's enumeration): "procfs should only contain `/proc/<pid>/` directories that
  the caller can ptrace." This is a stricter/newer mode than the man7 page's 0/1/2 set.
  [source: https://www.kernel.org/doc/html/latest/filesystems/proc.html]
- `gid=<gid>` — a group exempted from `hidepid` restrictions (cleaner than sudoers hacks for tools
  that legitimately need cross-user process visibility, e.g. monitoring agents).
  [source: https://man7.org/linux/man-pages/man5/proc.5.html]

**`subset=pid`** (since Linux 5.8) — hides all top-level `/proc` files/directories not related to
tasks; a container-hardening option so a sandboxed process only sees task-related `/proc` content,
not full system telemetry (`meminfo`, `net/`, `sys/`, etc. become unavailable).
[source: https://man7.org/linux/man-pages/man5/proc.5.html;
https://www.kernel.org/doc/html/latest/filesystems/proc.html]

**Analyst relevance**: when triaging a container or shared multi-user host, checking the actual
mount options in effect (`/proc/mounts` or `/proc/self/mountinfo`) for `hidepid`/`subset=pid` tells
you *up front* how much `/proc` visibility you or a compromised process actually has — a process
running under `subset=pid` genuinely cannot see `/proc/net/tcp` etc. even if it wanted to, which
changes what you should expect to find (and what an attacker inside that container could have seen).

---

## Distro-doc coverage notes (per task's caveat instructions)

- **Arch Wiki** (`wiki.archlinux.org/title/Procfs`): could not be fetched — the live page is behind
  Anubis anti-bot protection and returned an access-denied challenge page to automated fetches, both
  directly and via a second retry. I did **not** fabricate Arch Wiki content to fill this gap.
  As a partial substitute, Arch's own official man-page mirror was checked instead:
  `man.archlinux.org/man/procfs.5.en` — this is a straight mirror of the same upstream
  `man7.org` `proc(5)` text (via the `core/man-pages` package), with no Arch-specific supplementary
  content (no `ProcSubset=`/systemd-unit guidance, no distro-specific hardening notes). So it adds
  no claims beyond what's already cited from man7.org above.
  [source: https://man.archlinux.org/man/procfs.5.en]
- **Debian wiki**: no dedicated procfs/`\proc` reference page exists. Two tangentially relevant
  pages were checked:
  - `wiki.debian.org/chroot` — gives the literal mount command for bind-mounting `/proc` into a
    chroot (`mount -t proc proc "${chrootFolder}/proc"`) and notes `binfmt_misc` (a `/proc` child
    filesystem) isn't worth binding in a chroot; no security-specific commentary beyond that.
    [source: https://wiki.debian.org/chroot]
  - `wiki.debian.org/FileSystem` — lists procfs-related kernel config flags
    (`CONFIG_PROC_FS`, `CONFIG_PROC_KCORE`, `CONFIG_PROC_SYSCTL`, `CONFIG_PROC_PAGE_MONITOR`) with
    no explanatory text. [source: https://wiki.debian.org/FileSystem]
  Neither page constitutes a procfs reference in its own right; both are cited only for the specific
  narrow facts above.
- **Kali Linux official docs** (`www.kali.org/docs`): **no dedicated `/proc`-specific forensics
  content exists.** The Kali Linux Forensics Mode doc page does not mention `/proc` at all.
  [source: https://www.kali.org/docs/general-use/kali-linux-forensics-mode/]
  The closest relevant material is a **tool** page, not a docs page: `kali.org/tools/unhide/`
  describes the `unhide` utility's detection techniques, two of which are explicitly `/proc`-based —
  "Compare /proc vs /bin/ps output" and "Compare info gathered from /bin/ps with info gathered by
  walking thru the procfs" — used to catch rootkit-hidden processes by exploiting exactly the kind
  of `/proc`-vs-`ps` discrepancy noted under `modules` above. [source:
  https://www.kali.org/tools/unhide/] This is included because it's genuine official Kali content
  that directly bears on `/proc`-based forensics, even though it documents a tool rather than the
  filesystem itself.
- **Garuda Linux wiki** (`wiki.garudalinux.org`): **no procfs/`/proc` content found at all**, dedicated
  or otherwise, in a site search. The wiki's stated purpose is to supplement the Arch Wiki with
  Garuda-specific material only, and procfs is not Garuda-specific, so this absence is expected
  rather than a search failure. Nothing was invented to fill this gap.

---

## References — every distinct official source URL used

man7.org Linux man-pages:
- https://man7.org/linux/man-pages/man5/proc.5.html
- https://man7.org/linux/man-pages/man5/proc_pid.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_status.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_statm.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_io.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_limits.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_wchan.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_syscall.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_auxv.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_coredump_filter.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_smaps.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_mem.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_task.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_attr.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_ns.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_cgroup.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_mountinfo.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_comm.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_exe.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_cwd.5.html
- https://man7.org/linux/man-pages/man5/proc_pid_root.5.html
- https://man7.org/linux/man-pages/man5/proc_meminfo.5.html
- https://man7.org/linux/man-pages/man5/proc_cpuinfo.5.html
- https://man7.org/linux/man-pages/man5/proc_loadavg.5.html
- https://man7.org/linux/man-pages/man5/proc_modules.5.html
- https://man7.org/linux/man-pages/man5/proc_mounts.5.html
- https://man7.org/linux/man-pages/man5/proc_net.5.html
- https://man7.org/linux/man-pages/man5/proc_sys.5.html
- https://man7.org/linux/man-pages/man5/proc_sys_kernel.5.html

kernel.org (canonical kernel-source documentation):
- https://www.kernel.org/doc/html/latest/filesystems/proc.html

Arch Linux official (man-page mirror only; see coverage note above — Arch Wiki itself was
inaccessible):
- https://man.archlinux.org/man/procfs.5.en

Debian wiki (thin/tangential content only; see coverage note above):
- https://wiki.debian.org/chroot
- https://wiki.debian.org/FileSystem

Kali Linux official (tool doc, not a procfs reference; see coverage note above):
- https://www.kali.org/docs/general-use/kali-linux-forensics-mode/ (checked, confirmed no `/proc` content)
- https://www.kali.org/tools/unhide/

Garuda Linux wiki: no usable source found (see coverage note above; nothing to cite).
