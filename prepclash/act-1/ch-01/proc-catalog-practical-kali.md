# Practical `/proc` survey — Kali lab VM (remote)

Companion to `proc-catalog-practical-local.md` — same method, run against a personal Kali Linux
lab VM (owned/authorized by the note-taker) over a single non-interactive SSH session, purely
read-only `/proc` inspection. No files were modified, nothing was installed on the remote host,
no privilege escalation or scanning was attempted. IP address, hostname, and credentials used to
connect are intentionally omitted below — this repo is public.

Sources for field meanings: same man7.org pages as the local write-up
(`proc(5)`, `proc_pid_status(5)`, `proc_pid_fd(5)`).

---

## Filesystem identity

**Claim**: same `proc` filesystem type as any other Linux box — zero-sized blocks/inodes, no
`hidepid=` mount option set (default, open listing).

**Observed** (over SSH, non-interactive):
```
$ stat -f /proc
  File: "/proc"
    ID: 1800000000 Namelen: 255     Type: proc
Blocks: Total: 0  Free: 0  Available: 0

$ grep " /proc " /proc/mounts
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0

$ grep -o 'hidepid=[0-9]' /proc/mounts   # no match, exit 1 — hidepid=0 (default) here too
```

## Top-level layout

**Claim/Observed**: same general shape as the local machine — numeric PID dirs plus system-wide
files. ~339 numeric PID directories present at time of inspection.

Non-numeric top-level entries seen on the lab VM: `acpi/`, `asound/`, `buddyinfo`, `bus/`,
`cgroups`, `cmdline`, `consoles`, `cpuinfo`, `crypto`, `devices`, `diskstats`, `dma`, `driver/`,
`dynamic_debug/`, `execdomains`, `fb`, `filesystems`, `fs/`, `interrupts`, `iomem`, `ioports`,
`irq/`, `kallsyms`, `kcore`, `keys`, `key-users`, `kmsg`, `kpagecgroup`, `kpagecount`,
`kpageflags`, `loadavg`, `locks`, `meminfo`, `misc`, `modules`, `mounts` (symlink), `mtrr`, `net`
(symlink), `pagetypeinfo`, `partitions`, `pressure/`, `schedstat`, `self` (magic symlink),
`slabinfo`, `softirqs`, `stat`, `swaps`, `sys/`, `sysrq-trigger`, `sysvipc/`, `thread-self`
(magic symlink), `timer_list`, `tty/`, `uptime`, `version`, `vmallocinfo`, `vmstat`, `zoneinfo`.

**Notable difference from the local machine**: this listing is missing `bootconfig`, `config.gz`,
and `scsi/`, all three of which were present locally. `bootconfig` and `config.gz` are both
kernel-build-option-gated (`config.gz` requires `CONFIG_IKCONFIG_PROC`; `bootconfig` requires the
kernel command line to actually carry an extended boot-config blob) — their absence here just
means the lab VM's kernel/boot setup doesn't enable/populate them, not that anything is broken.
`scsi/` not appearing is consistent with the VM likely presenting virtio/NVMe-style block devices
rather than a legacy SCSI HBA the kernel registers a `/proc/scsi` handler for.

Same root-only-readable cluster as local (`kcore`, `slabinfo`, `pagetypeinfo`, `vmallocinfo`,
`timer_list`, `kpage*`) and same write-only `sysrq-trigger`.

## `/proc/self` — ownership

**Claim/Observed**: identical pattern to local — the `self` magic symlink itself shows as
`root:root`, but the PID directory it resolves to is owned by the connecting (lab VM's) user, not
root. PID 1 on the lab VM is `dr-xr-xr-x root root`, and reading a privileged file inside it as
the unprivileged lab user is denied:
```
$ cat /proc/1/environ
cat: /proc/1/environ: Permission denied
```
Same two-layer picture as local: `hidepid=0` so directories stay listable across users, but
per-file permission bits inside `/proc/pid/` still block cross-user reads of sensitive files.

## `/proc/pid/status` — selected fields

**Observed**: an ordinary command run over the SSH session shows `Seccomp: 0`, `NoNewPrivs: 0`,
`Threads: 1` — no sandboxing applied, single-threaded, exactly what's expected for a plain
shell-spawned utility process.

## `/proc/pid/fd/` — open descriptors

**Observed** (structure only, descriptor targets genericized — pipe/inode numbers are not
sensitive but are omitted here anyway to keep this purely structural):
```
dr-x------ 2 <lab VM user> <lab VM user>  4 ... .
dr-xr-xr-x 9 <lab VM user> <lab VM user>  0 ... ..
lr-x------ 1 <lab VM user> <lab VM user> 64 ... 0 -> pipe:[<inode>]
l-wx------ 1 <lab VM user> <lab VM user> 64 ... 1 -> pipe:[<inode>]
l-wx------ 1 <lab VM user> <lab VM user> 64 ... 2 -> pipe:[<inode>]
lr-x------ 1 <lab VM user> <lab VM user> 64 ... 3 -> /proc/<child-pid>/fd
```
Same shape as local: stdin/stdout/stderr as descriptors 0/1/2, an extra descriptor pointing at a
child process's own `fd/` directory (an artifact of how the remote shell pipeline was chained),
directory itself `dr-x------` (list+read only, no write, owner-only).

The difference worth flagging: locally, descriptors 1/2 pointed at real regular files (the
session's log files); over SSH, descriptors 0/1/2 all point at anonymous `pipe:[inode]` objects.
That's expected — an SSH-executed remote command has its stdio wired through pipes back to the
SSH channel rather than directly to a terminal or file, which is a good concrete illustration of
`proc_pid_fd(5)`'s claim that fd symlinks describe *whatever kind of object* the descriptor
actually is (file vs pipe vs socket), not just plain files.

## `/proc/pid/maps`

**Observed** (structure only): same layout as local — multiple mapping lines for the same backing
binary at different permission bits (`r--p`, `r-xp`, `rw-p`) reflecting separate ELF segments,
device/inode fields populated for file-backed regions. No addresses reproduced here since ASLR
makes them meaningless as identifying data anyway, but the *pattern* (segment-per-permission,
`[heap]` as anonymous `00:00`/inode `0`) matched the local observation exactly.

## `/proc/net` and `/proc/sys`

**Observed**: `/proc/net/` top-level entries matched the local machine closely (`arp`, `dev`,
`dev_mcast`, `dev_snmp6`, `fib_trie`, `fib_triestat`, `icmp`, `icmp6`, `if_inet6`, `igmp`, `igmp6`,
plus Bluetooth entries `bnep`/`hci`) — no addresses or connection tables reproduced here.

`/proc/sys/` top level: `abi`, `crypto`, `debug`, `dev`, `fs`, `kernel`, `net`, `sunrpc`, `user`,
`vm`. **Difference from local**: this lab VM has `crypto` and `sunrpc` subtrees under
`/proc/sys/` that weren't present (as `/proc/sys/` entries) on the local machine — `sunrpc` in
particular implies NFS/RPC client kernel support is compiled in on this kernel build, which the
local machine's kernel apparently doesn't expose the same way.

## `/proc/version`

**Observed**: the lab VM runs a Debian/Kali-branded kernel build (`+kali` suffix in the version
string, Kali's own package/build metadata, GCC/binutils versions distinct from the local
machine's). Confirms it's a genuinely separate distro/kernel build, not just a differently
configured copy of the same base system — non-identifying beyond "this is a Kali box."

## Mount count

**Observed**: `/proc/mounts` on the lab VM lists 28 active mounts at time of inspection —
recorded only as a count, not the actual mount table (which could reveal VM-specific disk
layout/paths).

## SSH connection note

Connection was made over a single non-interactive SSH session (password auth, `expect`-driven
since `sshpass` wasn't available locally and couldn't be installed without a sudo password — the
`expect` package was already present and used as a drop-in equivalent). No other network access,
port scans, or additional connections were made to the lab VM.

## Summary — differences from the local machine

1. **Kernel-config-gated top-level files differ**: local has `bootconfig`/`config.gz`/`scsi/`,
   the lab VM doesn't — a build-time/boot-time kernel configuration difference, not a
   security-relevant one.
2. **`/proc/sys/` subtree differs**: lab VM additionally exposes `crypto` and `sunrpc` — kernel
   config difference (RPC/NFS client support compiled in on the VM's kernel, differently on the
   local machine).
3. **Everything else — ownership model, `hidepid` default, root-only file cluster,
   `Seccomp`/`NoNewPrivs` defaults, `fd/`/`maps`/`task/` structure, permission-denied behavior on
   another user's `environ`** — was identical in pattern between the two systems, which is a
   reasonable confirmation that `/proc`'s core structure (as described in `proc(5)` and friends)
   is genuinely kernel-version/config-driven at the edges but architecturally stable across
   distros.
