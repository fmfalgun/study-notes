# Practical `/proc` survey — local machine

Companion to `link-02-notes.md` (the `proc(5)` doc study). Same doc gave the theory; this is a
hands-on, read-only walk of `/proc` on the actual machine these notes are being written on
(Arch-family, zen kernel). No destructive commands were run — only `ls`, `cat`, `stat`, `readlink`
against `/proc` itself.

Sources for field meanings: `proc(5)`/`proc_pid_status(5)`/`proc_pid_fd(5)` (man7.org), already
cited in `link-02-notes.md`.

---

## Filesystem identity

**Claim**: `/proc` mounts as its own filesystem type, separate from the root filesystem, with
zero-sized blocks/inodes (because there's no backing storage — it's synthesized on read).

**Simple explanation**: `stat -f` on a real filesystem shows block/inode counts. On `/proc` those
come back all zero — confirming there's no disk allocation behind it, matching the "kernel data
structures exposed as files" claim from `proc(5)`.

**Observed**:
```
$ stat -f /proc
  File: "/proc"
    ID: 1800000000 Namelen: 255     Type: proc
Blocks: Total: 0  Free: 0  Available: 0
Inodes: Total: 0  Free: 0

$ grep " /proc " /proc/mounts
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
```
No `hidepid=` option present in the mount line, and `grep -o 'hidepid=[0-9]'` against
`/proc/mounts` matches nothing (exit status 1) — this system runs the default `hidepid=0`
(anyone can list/read any PID's `/proc` dir, subject to normal per-file permission checks).

## Top-level layout: numeric PID dirs + system-wide files

**Claim**: `/proc` mixes two kinds of entries at the top level — one directory per running PID
(numeric name), plus several dozen system-wide files/dirs that aren't tied to any single process.

**Simple explanation**: this matches the man page's "process info" vs "system info" split
exactly. The numeric dirs come and go as processes start/exit; the system-wide entries are
comparatively static.

**Observed**: ~380 numeric PID directories present at time of writing (`ls -d /proc/[0-9]* | wc
-l`), each `dr-xr-xr-x`. Non-numeric top-level entries seen: `acpi/`, `asound/`, `bootconfig`,
`buddyinfo`, `bus/`, `cgroups`, `cmdline`, `config.gz`, `consoles`, `cpuinfo`, `crypto`,
`devices`, `diskstats`, `dma`, `driver/`, `dynamic_debug/`, `execdomains`, `fb`, `filesystems`,
`fs/`, `interrupts`, `iomem`, `ioports`, `irq/`, `kallsyms`, `kcore`, `keys`, `key-users`, `kmsg`,
`kpagecgroup`, `kpagecount`, `kpageflags`, `loadavg`, `locks`, `meminfo`, `misc`, `modules`,
`mounts` (symlink to `self/mounts`), `mtrr`, `net` (symlink to `self/net`), `pagetypeinfo`,
`partitions`, `pressure/`, `schedstat`, `scsi/`, `self` (magic symlink), `slabinfo`, `softirqs`,
`stat`, `swaps`, `sys/`, `sysrq-trigger`, `sysvipc/`, `thread-self` (magic symlink),
`timer_list`, `tty/`, `uptime`, `version`, `vmallocinfo`, `vmstat`, `zoneinfo`.

A handful of these are notably locked down even to their owner unless root: `kcore`, `kmsg`,
`kpagecgroup`, `kpagecount`, `kpageflags`, `pagetypeinfo`, `slabinfo`, `timer_list`, `vmallocinfo`
are all `-r--------` (root-read-only) — these expose raw kernel memory layout / internal
allocator state, which is why they're restricted even though most of `/proc` is world-readable.
`sysrq-trigger` is `--w-------` — write-only, root-only, because writing to it triggers kernel
magic-SysRq actions.

## `/proc/self` — process ownership

**Claim** (per `proc_pid(5)`, already summarized in link-02): files under a process's own
`/proc/pid/` are owned by that process's effective UID/GID, not root, as long as the process is
"dumpable."

**Simple explanation**: your own shell session's `/proc` entry should be owned by you, not root —
confirmed directly.

**Observed**:
```
$ ls -ld /proc/self
lrwxrwxrwx 1 root root 0 ... /proc/self -> <pid>

$ ls -ld /proc/<own-pid>
dr-xr-xr-x 9 <local user> <local user> 0 ... /proc/<own-pid>
```
The `self` symlink itself is always shown as `root:root` — that's a property of the magic symlink
object, not the target directory. The target directory it resolves to is owned by the local user.

By contrast, `/proc/1` (PID 1, a root-owned process) stays `dr-xr-xr-x root root`, and attempting
to read a privileged file inside it as an unprivileged user is denied outright:
```
$ cat /proc/1/environ
cat: /proc/1/environ: Permission denied
```
This lines up with `proc_pid(5)`: baseline directory listing of another user's PID dir is often
still visible (`hidepid=0` here), but individual sensitive files inside it (`environ`, `maps`,
etc.) still enforce their own per-file permission bits, which deny cross-user reads regardless of
`hidepid`.

## `/proc/pid/status` — selected fields

**Claim** (per `proc_pid_status(5)`): `Seccomp` reports the process's seccomp mode (0 = disabled,
1 = strict, 2 = filter-mode/BPF); `NoNewPrivs` reports the `no_new_privs` bit, which — once set —
blocks the process (and its descendants) from gaining privileges via `execve()` of a setuid/
setgid binary or file capabilities.

**Simple explanation**: these two fields are the standard way to check, from outside a process,
whether it's running under a sandboxing/hardening posture (`no_new_privs` is the mechanism that
makes seccomp+bwrap-style sandboxes reliable — a sandboxed process literally cannot re-elevate
even by execing a setuid binary).

**Observed**: an ordinary interactive shell/utility process on this machine shows
`Seccomp: 0` and `NoNewPrivs: 0` — no sandboxing applied, as expected for a normal login shell.

## `/proc/pid/fd/` — open file descriptors as symlinks

**Claim** (per `proc_pid_fd(5)`): one entry per open file descriptor, named by descriptor number,
each a symlink to what the descriptor actually points at — a real file, a `pipe:[inode]`,
`socket:[inode]`, or similar; access is gated by a ptrace-style read check, so only the owning
user (or root) can list another process's `fd/` contents.

**Simple explanation**: this is the mechanism `lsof`/`ss` effectively build on — `/proc/pid/fd/`
is a live, walkable map of everything a process currently has open, described by *what kind* of
object each descriptor is rather than needing a separate syscall per descriptor.

**Observed** (own shell/utility process, structure only — descriptor targets genericized):
```
$ ls -la /proc/self/fd
dr-x------ 2 <user> <user>  4 ... .
dr-xr-xr-x 9 <user> <user>  0 ... ..
lr-x------ 1 <user> <user> 64 ... 0 -> /dev/null
l-wx------ 1 <user> <user> 64 ... 1 -> <a regular file under the session's temp dir>
l-wx------ 1 <user> <user> 64 ... 2 -> <a regular file under the session's temp dir>
lr-x------ 1 <user> <user> 64 ... 3 -> /proc/<child-pid>/fd
```
Note the directory itself is `dr-x------` — even the owning user can only *list* their own `fd/`
directory (mode 0500-equivalent read+execute, no write), consistent with the ptrace-mode-read
gate `proc_pid_fd(5)` describes.

## `/proc/pid/maps` — memory mappings

**Claim**: each line describes one contiguous virtual memory region — address range, permission
bits (`r`/`w`/`x`/`p`-private or `s`-shared), file offset, device, inode, and backing file path
(blank for anonymous mappings like the heap).

**Observed** (structure, path of the utility binary itself is not sensitive):
```
5594fe0a3000-5594fe0a5000 r--p 00000000 00:23 3336990   /usr/bin/head
5594fe0a5000-5594fe0ad000 r-xp 00002000 00:23 3336990   /usr/bin/head
559536637000-559536658000 rw-p 00000000 00:00 0         [heap]
7f0a72000000-7f0a72024000 r--p 00000000 00:23 4205730   /usr/lib/libc.so.6
```
Matches the man page exactly: the same backing file (`/usr/bin/head`) appears multiple times with
different permission bits because the loader maps its read-only, executable, and read-write
segments as separate regions; the heap shows device `00:00` / inode `0` because it's anonymous
memory, not backed by a file.

## `/proc/pid/task/` — thread subdirectories

**Claim**: `/proc/pid/task/` has one entry per thread; a single-threaded process shows exactly
one entry, matching its own PID.

**Observed**: `ls /proc/self/task/` for an ordinary single-threaded shell utility returned exactly
one numeric entry.

## `/proc/net` and `/proc/sys` — system-wide subtrees

**Claim**: `/proc/net/` exposes networking state as a flat set of pseudo-files (routing, protocol
stats, per-interface counters); `/proc/sys/` exposes tunable kernel parameters, organized into
subdirectories by subsystem.

**Observed**: `/proc/net/` on this machine includes `arp`, `dev`, `dev_mcast`, `dev_snmp6`,
`fib_trie`, `fib_triestat`, `icmp`, `icmp6`, `if_inet6`, `igmp`, `igmp6`, `ip_mr_cache`, plus
Bluetooth-related entries (`bnep`, `hci`) — no live connection data or addresses reproduced here.
`/proc/sys/` top level: `abi`, `debug`, `dev`, `fs`, `kernel`, `net`, `user`, `vm` — matches the
standard subsystem grouping from `proc_sys(5)`.

## `/proc/version`

**Claim**: a single-line file with the running kernel's version string, build toolchain, and
build timestamp — non-identifying, safe to record verbatim (it says nothing about *this*
machine's identity beyond "runs this distro's kernel build").

**Observed**: kernel is a `zen`-flavored build (Arch-family `linux-zen` package), version series
`7.1.x` — consistent with a rolling-release desktop/dev machine rather than an LTS server kernel.

## Summary — what surprised me relative to the plain doc

1. The `self`/`thread-self` magic symlinks themselves always report `root:root` ownership even
   though the directory they resolve to is user-owned — the doc doesn't call this distinction out
   explicitly, but it makes sense once you think of the symlink object as living in a shared,
   kernel-managed namespace rather than per-process space.
2. `hidepid` defaults to unset (`=0`) here, meaning directory-listing-level privacy between users
   isn't the actual defense on this box — the real enforcement point turned out to be per-file
   permission bits inside each `/proc/pid/` dir (confirmed via the `Permission denied` on another
   user's `environ`), which is a second, independent layer beneath `hidepid`.
3. A meaningful chunk of top-level `/proc` (`kcore`, `slabinfo`, `pagetypeinfo`, `vmallocinfo`,
   `timer_list`, `kpage*`) is root-only by default — the doc's "most files read-only, some
   writable" framing undersells how many are *also* root-only-readable, not just read-only.
