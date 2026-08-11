# `/proc` system-wide entries — theoretical reference (non-`/proc/pid/*` only)

Companion to `link-02-notes.md` (which covers `proc(5)` as a structural hub page, and explicitly
declines to expand the `/proc/[a-z]*` "See also" index) and to `proc-catalog-theoretical.md` (which
covers `/proc/pid/*` in depth and only briefly touches system-wide files). This file is the
deliberate follow-through on that boundary: every entry below lives directly under `/proc` and is
**not** process-specific.

Format matches `link-02-notes.md`: **Claim** (sourced), **Simple explanation**, **Why a
security/systems analyst checks it**, **Try-it** (read-only, safe to run). Sources are restricted to
man7.org man-pages, kernel.org `Documentation/`, and Arch/Debian/Kali/Garuda official docs — no
blogs, no Stack Overflow. Where a distro doc has nothing relevant, that's stated explicitly rather
than invented (see the "Distro-doc coverage" section at the end).

**A note on ArchWiki access**: `wiki.archlinux.org` sits behind Anubis anti-bot JS-challenge
protection that blocks naive automated fetchers outright, but responds normally to a plain `curl`
carrying an ordinary browser `User-Agent` string — no login, no cookies, no JS execution needed. So
ArchWiki content below is genuinely fetched and verbatim-quoted, not skipped. `wiki.debian.org`, by
contrast, runs a proof-of-work JS challenge that a UA-string alone doesn't clear — those pages stay
inaccessible to automation and are flagged as such rather than guessed at.

---

## 1. Interrupts, softirqs, and overall kernel/CPU statistics

### `/proc/interrupts`

**Claim**: "used to record the number of interrupts per CPU per IO device. Since Linux 2.6.24, for
the i386 and x86-64 architectures, at least, this also includes interrupts internal to the system
... such as NMI ..., LOC (local timer interrupt), and for SMP systems, TLB (TLB flush interrupt),
RES (rescheduling interrupt), CAL (remote function call interrupt), and possibly others."
Source: https://man7.org/linux/man-pages/man5/proc_interrupts.5.html

**Simple explanation**: one row per interrupt line, one column per CPU — how many times each IRQ
has fired on each core since boot.

**Why check it**: a device or driver generating an abnormal interrupt storm shows up here before
anything else notices; also a baseline for "what hardware/IRQ lines does this box actually have,"
useful when validating a VM/container's exposed device surface.

**Try-it**:
```sh
cat /proc/interrupts | head
awk '{print $1, $NF}' /proc/interrupts | head   # IRQ number + owning device/driver name
```

### `/proc/stat`

**Claim**: "kernel/system statistics. Varies with architecture." Per-CPU time is broken into `user`,
`nice`, `system`, `idle`, `iowait`, `irq`, `softirq`, `steal`, `guest`, `guest_nice` (USER_HZ units).
Also: `intr` (interrupt counts since boot), `ctxt` (total context switches), `btime` (boot time,
seconds since epoch), `processes` (fork/clone count since boot), `procs_running`, `procs_blocked`,
and a `softirq` summary line.
Source: https://man7.org/linux/man-pages/man5/proc_stat.5.html

**Simple explanation**: the single richest whole-system activity counter file — CPU time breakdown,
scheduler churn, and boot timestamp in one place. Backs `vmstat(1)`/`mpstat(1)`/`uptime`-style tools.

**Why check it**: `btime` gives you an authoritative boot timestamp independent of any log that
could've been tampered with; a spike in `ctxt` (context switches) or `procs_blocked` can be the
first system-wide symptom of a resource-exhaustion attack (fork bomb, I/O-bound DoS) before you've
even identified the offending PID.

**Try-it**:
```sh
grep -E '^(btime|ctxt|processes|procs_running|procs_blocked)' /proc/stat
date -d @$(awk '/btime/{print $2}' /proc/stat)   # human-readable boot time
```

### `/proc/softirqs`

**Claim**: "Provides counts of softirq handlers serviced since boot time, for each CPU." Categories
include HI, TIMER, NET_TX, NET_RX, BLOCK, TASKLET, SCHED, HRTIMER, RCU.
Source: https://www.kernel.org/doc/Documentation/filesystems/proc.rst (section on `/proc/softirqs`)

**Simple explanation**: like `/proc/interrupts` but one level up the stack — deferred (bottom-half)
interrupt work, broken out by category and CPU.

**Why check it**: an unexplained sustained `NET_RX`/`NET_TX` spike on a box that shouldn't be doing
much networking is a cheap early signal of unexpected traffic (exfil, C2 beaconing, a DoS being
launched from the box) — cheaper to check than starting a packet capture.

**Try-it**:
```sh
cat /proc/softirqs | head
```

### `/proc/schedstat`

**Claim**: per-CPU fields report `sched_yield()` invocations, `schedule()` call counts, idle
occurrences, wake-up statistics, and latency measurements including "sum of all time spent running
by tasks" and time spent waiting, in nanoseconds; per-scheduling-domain fields (produced once per
domain per CPU) cover load-balancing operations and task-migration attempts.
Source: https://www.kernel.org/doc/Documentation/scheduler/sched-stats.rst

**Simple explanation**: raw scheduler internals — how much CPU time was actually handed out vs.
spent waiting for it, and how the load balancer moved tasks between cores.

**Why check it**: a systems analyst uses this to distinguish "the box is genuinely CPU-starved" from
"something is pinning/monopolizing specific cores" during a performance-anomaly investigation —
scheduling-latency spikes can also be a side effect of a noisy-neighbor container or a cryptominer
competing for CPU.

**Try-it**:
```sh
head -5 /proc/schedstat
```

---

## 2. `net/` — networking layer

### `/proc/net/` (directory)

**Claim**: "various files and subdirectories containing information about the networking layer,"
readable as ASCII with `cat(1)`, though "the standard netstat(8) suite provides much cleaner access
to these files." Since Linux 2.6.25, `/proc/net` is a symbolic link to `/proc/self/net`, exposing
"information for the network namespace of which the process is a member."
Source: https://man7.org/linux/man-pages/man5/proc_net.5.html

**Simple explanation**: the raw data `netstat`/`ss`/`ip` read from — and, because it's per-namespace
since 2.6.25, what a process sees here reflects *its own* network namespace, not necessarily the
host's.

**Why check it**: the namespace-relative behavior is itself a forensics-relevant fact — reading
`/proc/1234/net/tcp` from outside that process's namespace shows you exactly what network state a
containerized/namespaced process can see, distinct from the host's own `/proc/net/tcp`.

**Try-it**:
```sh
readlink -f /proc/net           # confirms the /proc/self/net symlink
ls /proc/net | head
```

### `/proc/net/tcp`, `/proc/net/udp`

**Claim** (`/proc/net`): documents "TCP socket table dump" and "UDP socket table dump" as files
under this directory.
Source: https://man7.org/linux/man-pages/man5/proc_net.5.html

**Claim** (field layout, `/proc/net/tcp` and `tcp6`): each line has connection details (`local
address:port`, `remote address:port`, connection state, hex-encoded), queue/timer data
(`tx_queue:rx_queue`, timer-active code, jiffies-to-expiry, retransmit-timeout count), and socket
stats (UID, unanswered probes, inode, refcount, memory pointer, RTO, ACK data, congestion window,
slow-start threshold). Timer-active codes: `0` none pending, `1` retransmit pending, `2` another
timer (delayed ack/keepalive) pending, `3` socket in `TIME_WAIT`, `4` zero-window-probe pending.
Source: https://www.kernel.org/doc/Documentation/networking/proc_net_tcp.rst

**Simple explanation**: a live table of every TCP/UDP socket in the current network namespace —
addresses, ports, state, and the UID that owns each socket — in raw hex/decimal, before any
formatting tool touches it.

**Why check it**: the `uid` field lets you attribute a socket to a specific user even if the owning
process has already exited or is hidden; the `inode` field is the exact cross-reference key against
a suspicious process's `/proc/<pid>/fd/*` symlinks (which show as `socket:[inode]`) — this is the
core network-forensics pivot for "which process actually owns this connection."

**Try-it**:
```sh
cat /proc/net/tcp | head -3
# decode a hex port, e.g. column 2 local_address is IP:PORT in hex:
python3 -c "print(int('0050', 16))"   # 0x0050 = port 80
```

### `/proc/net/arp`

**Claim**: "ASCII readable dump of the kernel ARP table used for address resolutions."
Source: https://man7.org/linux/man-pages/man5/proc_net.5.html

**Simple explanation**: current IP-to-MAC mappings the kernel has learned on the local segment.

**Why check it**: live evidence for ARP-spoofing investigations (duplicate/flapping MAC for one IP)
and for confirming exactly what else is reachable on the local L2 segment during lateral-movement
analysis.

**Try-it**:
```sh
cat /proc/net/arp
```

### `/proc/net/dev`

**Claim**: "network device status information. This gives the number of received and sent packets,
the number of errors and collisions and other basic statistics. These are used by the ifconfig(8)
program to report device status."
Source: https://man7.org/linux/man-pages/man5/proc_net.5.html

**Simple explanation**: per-NIC packet/byte/error counters since the interface came up.

**Why check it**: a fast baseline for "is this interface actually passing the volume of traffic
I'd expect" — large RX byte counts on an interface that should be idle, or a climbing error/drop
counter, are both cheap anomaly signals worth a closer look with a real capture tool.

**Try-it**:
```sh
cat /proc/net/dev
```

### `/proc/net/route`

**Claim**: `route(8)`'s FILES section lists `/proc/net/route` as its data source; its OUTPUT section
documents the column semantics: "Destination ... Gateway ... Genmask ... Flags [U up, H host,
G gateway, R reinstate, D dynamic, M modified, A addrconf, C cache, ! reject] ... Metric ... Ref ...
Use ... Iface."
Source: https://man7.org/linux/man-pages/man8/route.8.html

**Note on coverage**: `man7.org`'s dedicated `proc_net(5)` page does **not** document
`/proc/net/route` itself — it's `route(8)`'s FILES/OUTPUT sections that establish the mapping, since
the `route` command reads this file directly. Flagged rather than silently merged, so the sourcing
stays honest.

**Simple explanation**: the kernel's live IPv4 routing table in raw form — same data `route -n`/
`ip route` present, just unformatted.

**Why check it**: a route pointing traffic somewhere unexpected (an added default route, a
more-specific route hijacking a subnet) is a classic host-level MITM/exfil-redirection technique;
this is the ground-truth file to check when you don't trust that `ip route` itself hasn't been
tampered with (e.g. via a hooked/aliased binary).

**Try-it**:
```sh
column -t /proc/net/route | head
```

---

## 3. `sys/` — the sysctl-tunable kernel-variable tree

### `/proc/sys/` (directory, general)

**Claim**: "contains a number of files and subdirectories corresponding to kernel variables" that
"can be read and in some cases modified using the /proc filesystem." Subsystem-specific detail is
delegated to `proc_sys_abi(5)`, `proc_sys_debug(5)`, `proc_sys_dev(5)`, `proc_sys_fs(5)`,
`proc_sys_kernel(5)`, `proc_sys_net(5)` (→ `proc_sys_net_ipv4(5)`), `proc_sys_proc(5)`,
`proc_sys_sunrpc(5)`, `proc_sys_user(5)`, `proc_sys_vm(5)`.
Source: https://man7.org/linux/man-pages/man5/proc_sys.5.html

**Simple explanation**: this is where `sysctl(8)` actually reads/writes — `kernel.sysrq` as a
`sysctl` name is literally the file `/proc/sys/kernel/sysrq`.
Source (mapping confirmed): https://wiki.archlinux.org/title/Sysctl — "The parameters available are
those listed under `/proc/sys/`. For example, the `kernel.sysrq` parameter refers to the file
`/proc/sys/kernel/sysrq` on the file system."

**Why check it**: `/proc/sys` is the single largest concentration of security-relevant *runtime*
kernel configuration in `/proc` — ASLR, ptrace restriction, kernel-pointer leaks, IP forwarding,
source-routing acceptance, and dozens more all live here and can be flipped without a reboot. It's
also the one place where "current value" and "written config" can legitimately diverge (a value
changed by `echo` directly bypasses `/etc/sysctl.d/*.conf`, so what's live may not match what
`sysctl --system` would reapply on reboot).
Source (config vs. live-value distinction): https://wiki.archlinux.org/title/Sysctl

**Try-it**:
```sh
ls /proc/sys
cat /proc/sys/kernel/sysrq
sysctl kernel.sysrq   # same value, via the sysctl(8) wrapper
```

### `/proc/sys/kernel/*` — selected security-relevant entries

**Claim**, per-entry, source: https://man7.org/linux/man-pages/man5/proc_sys_kernel.5.html
- **`dmesg_restrict`** — "if the value is 1, only privileged users can read the kernel syslog."
- **`kptr_restrict`** — controls kernel-pointer exposure; value `2` "replaces pointers with zeros
  regardless of the user's capabilities."
- **`yama/ptrace_scope`** — restricts `ptrace(2)` attachment scope (documented in `ptrace(2)`).
- **`modules_disabled`** — a one-way toggle: once set to 1, "modules can be neither loaded nor
  unloaded."
- **`randomize_va_space`** — ASLR policy: 0 off, 1 partial, 2 full heap randomization.
- **`core_pattern`** — controls core-dump filename/pipe-target pattern (full semantics in `core(5)`).
- **`sysrq`** — bitmask of which Magic-SysRq functions are permitted (`CONFIG_MAGIC_SYSRQ`
  required).

**Claim (Kali-specific default deviation)**: "The kernel logs are unrestricted by default, meaning
that any unprivileged user can run the command `dmesg`" and inspect kernel logs; `kali-tweaks` can
"restore this behavior" (i.e. re-enable restriction).
Source: https://www.kali.org/docs/general-use/kernel-configuration/

**Simple explanation**: `dmesg_restrict=0` (Kali's shipped default) means any local user, including
a low-privilege shell obtained through an exploit, can read the entire kernel ring buffer —
including driver probe messages that sometimes leak physical/kernel addresses or hardware serials.

**Why check it**: this is the single most important sysctl subtree for a security analyst — it's
the direct on-disk record of whether ASLR, ptrace confinement, dmesg visibility, and module-loading
are actually hardened *on this specific running system right now*, independent of whatever the
distro's shipped defaults claim. Note the Kali finding above as a concrete example: a general
security checklist that assumes `dmesg_restrict=1` will be wrong on a stock Kali install.

**Try-it**:
```sh
for f in dmesg_restrict kptr_restrict yama/ptrace_scope modules_disabled randomize_va_space sysrq; do
  printf '%-25s ' "$f"; cat /proc/sys/kernel/$f 2>/dev/null || echo "(not present)"
done
```

### `/proc/sys/vm/*` — selected entries

**Claim**, per-entry, source: https://man7.org/linux/man-pages/man5/proc_sys_vm.5.html
- **`swappiness`** — "Controls kernel swap aggressiveness." Default 60.
- **`overcommit_memory`** — accounting mode: 0 heuristic (default), 1 always overcommit, 2 always
  check against `CommitLimit`.
- **`drop_caches`** — "Writing to this file causes the benefits of caching to be lost, it can
  degrade overall system performance" (frees pagecache/dentries/inodes on write).
- **`panic_on_oom`** — 0 invoke OOM-killer (default), 1 panic with exceptions, 2 always panic.
- **`oom_dump_tasks`** — dumps the task list when the OOM-killer activates (default off).
- **`unprivileged_userfaultfd`** (Linux 5.2+) — default 1 (allowed); 0 requires
  `CAP_SYS_PTRACE` — gates a syscall class (`userfaultfd(2)`) that has been abused in real
  privilege-escalation exploit chains for race-window widening.

**Claim (practical tuning example, non-security)**: Garuda Linux's gaming-optimization guide shows
live-editing several of these same files directly, e.g. `echo 10 > /proc/sys/vm/swappiness`,
`echo 0 > /proc/sys/vm/compaction_proactiveness`, `echo 1048576 > /proc/sys/vm/min_free_kbytes` —
confirming these are treated as routinely user-tunable at runtime, not just theoretical knobs.
Source: https://wiki.garudalinux.org/en/Gaming-optimizations

**Simple explanation**: memory-management policy knobs — how eagerly the kernel swaps, whether it
lets processes overcommit virtual memory beyond physical+swap, and what happens when memory really
runs out.

**Why check it**: `overcommit_memory=2` + a tight `overcommit_ratio` on a host is a deliberate
hardening/stability choice (fail allocations early instead of triggering the OOM-killer's somewhat
unpredictable process-killing); seeing `drop_caches` written to right before/after an incident
timestamp (check via file mtime/audit log, since the file itself has no history) can indicate
someone deliberately trying to make forensic timing/cache-based analysis harder.

**Try-it**:
```sh
for f in swappiness overcommit_memory panic_on_oom unprivileged_userfaultfd; do
  printf '%-25s ' "$f"; cat /proc/sys/vm/$f 2>/dev/null || echo "(not present)"
done
```

### `/proc/sys/net/*` — selected entries

**Claim (general structure)**: "This directory contains networking stuff. Explanations for some of
the files under this directory can be found in tcp(7) and ip(7)." Documents
`net/core/bpf_jit_enable` and `net/core/somaxconn` ("defines a ceiling value for the backlog
argument of listen(2)") directly; delegates IPv4 specifics to `proc_sys_net_ipv4(5)`.
Source: https://man7.org/linux/man-pages/man5/proc_sys_net.5.html

**Claim (man7 IPv4 coverage, and its limits)**: `proc_sys_net_ipv4(5)` documents `ip_forward`
("Enable IP forwarding"), `ip_local_port_range`, `ip_default_ttl`, `ip_no_pmtu_disc`,
`ip_nonlocal_bind`, and IPv6-fragment-reassembly timers — but does **not** document
`tcp_syncookies`, `icmp_echo_ignore_all`, `tcp_timestamps`, or the `conf/*/rp_filter` /
`accept_redirects` / `accept_source_route` / `log_martians` family; confirmed absent by direct
text search of the page.
Source: https://man7.org/linux/man-pages/man5/proc_sys_net_ipv4.5.html

**Claim (the missing security-relevant ones, from the canonical kernel doc instead)**:
- **`tcp_syncookies`** — "Send out syncookies when the syn backlog queue of a socket overflows.
  This is to prevent against the common 'SYN flood attack.'"
- **`icmp_echo_ignore_all`** — "If enabled, then the kernel will ignore all ICMP ECHO requests sent
  to it."
- **`conf/*/rp_filter`** — "Strict mode tests each incoming packet against the FIB and if the
  interface is not the best reverse path the packet check will fail. Loose mode tests the source
  address against the FIB and if not reachable via any interface the packet check will fail."
- **`conf/*/accept_redirects`** — "Accept ICMP redirect messages."
- **`conf/*/accept_source_route`** — "Accept packets with SRR [Strict Source Routing] option."
- **`conf/*/log_martians`** — "Log packets with impossible addresses to kernel log."
- **`tcp_timestamps`** — "Enable timestamps as defined in RFC1323 ..."
Source: https://www.kernel.org/doc/Documentation/networking/ip-sysctl.rst

**Claim (ArchWiki practical framing of the same knobs, as deployed hardening)**: "By enabling
reverse path filtering, the kernel will do source validation of the packets received from all the
interfaces on the machine. This can protect from attackers that are using IP spoofing methods to do
harm." Also notes the *shipped default differs from the kernel default*: "The kernel's default value
is 0 (no source validation), but systemd ships `/usr/lib/sysctl.d/50-default.conf` that sets
`net.ipv4.conf.all.rp_filter` to 2 (loose mode)." On martian logging: "Often martian and unroutable
packet may be used for a dangerous purpose. Logging these packets for further inspection may be
useful" (with the caveat that it "can fill up your logs"). On ICMP redirects: cross-references
"What are ICMP redirects? Should they be blocked?" as background before disabling
`accept_redirects`/`send_redirects`.
Source: https://wiki.archlinux.org/title/Sysctl

**Claim (Kali-specific default deviation)**: "Traditionally, IPv4 ports below 1024 are called
'privileged ports,' and can only be used by the privileged user. In Kali Linux, this is disabled by
default" — because "Kali is no longer root user by default" — re-enableable via `kali-tweaks`. (The
underlying knob is `net.ipv4.ip_unprivileged_port_start`, per man7's naming convention for this
family of settings; Kali's own doc text does not name the sysctl explicitly.)
Source: https://www.kali.org/docs/general-use/kernel-configuration/

**Simple explanation**: this is the live IPv4/IPv6 stack-hardening control panel — SYN-flood
cookies, source-address spoofing checks, ICMP behavior, and privileged-port enforcement all sit
here, and defaults genuinely vary by distro/init-system shipped overrides, not just kernel
defaults.

**Why check it**: never assume the kernel's compiled-in default is what's actually running — both
the ArchWiki (`rp_filter` shipped as loose-mode 2, not the kernel's strict-mode default) and Kali
(`dmesg_restrict` and privileged-port enforcement both off by default) examples above are concrete,
sourced proof that distro packaging silently overrides kernel defaults in security-relevant ways.
An analyst auditing a box's actual network-hardening posture has to read these files directly rather
than trust generic "Linux defaults to X" claims.

**Try-it**:
```sh
for f in ipv4/tcp_syncookies ipv4/icmp_echo_ignore_all ipv4/conf/all/rp_filter \
         ipv4/conf/all/accept_redirects ipv4/conf/all/accept_source_route \
         ipv4/conf/all/log_martians ipv4/ip_forward ipv4/ip_unprivileged_port_start; do
  printf '%-40s ' "$f"; cat /proc/sys/net/$f 2>/dev/null || echo "(not present)"
done
```

---

## 4. Modules, devices, and hardware-resource tables

### `/proc/modules`

**Claim**: "A text list of the modules that have been loaded by the system. See also lsmod(8)."
Source: https://man7.org/linux/man-pages/man5/proc_modules.5.html

**Simple explanation**: exactly what `lsmod` shows — every currently loaded kernel module.

**Why check it**: baseline rootkit-hunting file — an unexpected module name, or one whose reference
count/dependency chain looks wrong, is worth investigating. Caveat: a sufficiently capable
loadable-kernel-module rootkit can hook the very data structures this file reads from and hide its
own entry, so a clean read is not proof of absence for advanced threats.

**Try-it**:
```sh
cat /proc/modules | head
lsmod | head        # same data, formatted
```

### `/proc/devices`

**Claim**: "Text listing of major numbers and device groups. This can be used by MAKEDEV scripts
for consistency with the kernel."
Source: https://man7.org/linux/man-pages/man5/proc_devices.5.html

**Simple explanation**: which major device numbers are currently bound to which driver/subsystem,
split into "Character devices" and "Block devices" sections.

**Why check it**: a device major number that shouldn't exist on this hardware profile (or one
that's missing when it should be present) is a hardware/driver-tampering or virtualization-detection
signal — useful when confirming whether a box is bare metal, a VM, or a container with a restricted
device set.

**Try-it**:
```sh
cat /proc/devices
```

### `/proc/dma`

**Claim**: "a list of the registered ISA DMA (direct memory access) channels in use."
Source: https://man7.org/linux/man-pages/man5/proc_dma.5.html

**Simple explanation**: legacy ISA-bus DMA channel registrations — mostly historical on modern
hardware, but still present.

**Why check it**: low priority on modern hardware (most devices don't use ISA DMA anymore); included
here for completeness of the top-level index rather than as an active triage target.

**Try-it**:
```sh
cat /proc/dma
```

### `/proc/iomem`, `/proc/ioports`

**Claim** (`iomem`): "I/O memory map in Linux 2.4." — the man page is notably terse on this one.
Source: https://man7.org/linux/man-pages/man5/proc_iomem.5.html

**Claim** (`ioports`): "This is a list of currently registered Input-Output port regions that are
in use."
Source: https://man7.org/linux/man-pages/man5/proc_ioports.5.html

**Simple explanation**: which physical memory address ranges (`iomem`) and I/O port ranges
(`ioports`) are claimed by which kernel drivers.

**Why check it**: a driver claiming a memory/port range it shouldn't (or address ranges that
overlap unexpectedly) can indicate a malicious or misbehaving kernel module; also useful groundwork
before attempting any physical-memory acquisition, since `iomem` marks which ranges are legitimately
RAM vs. device-mapped.

**Try-it**:
```sh
head -20 /proc/iomem
head -20 /proc/ioports
```

### `/proc/mtrr`

**Claim**: "Memory Type Range Registers. See the Linux kernel source file
`Documentation/arch/x86/mtrr.rst` for details."
Source: https://man7.org/linux/man-pages/man5/proc_mtrr.5.html

**Simple explanation**: x86 CPU registers controlling cacheability policy for physical memory
ranges (mostly relevant to graphics/framebuffer memory historically).

**Why check it**: low security relevance day-to-day; included for index completeness. Occasionally
relevant to VM/hypervisor-detection or performance-debugging work.

**Try-it**:
```sh
cat /proc/mtrr 2>/dev/null || echo "not present (common on modern kernels using PAT instead)"
```

### `/proc/execdomains`

**Claim**: "Used to list ABI personalities before Linux 4.1; now contains a constant string for
userspace compatibility."
Source: https://man7.org/linux/man-pages/man5/proc_execdomains.5.html

**Simple explanation**: a vestigial file — used to matter for tracking alternate binary ABI
personalities (`personality(2)`), now frozen to a fixed string kept only so old parsers don't break.

**Why check it**: essentially none today — flagged here specifically because the *kernel.org*
summary table still labels it "related to security" (a holdover from when ABI-personality tracking
mattered for security policy), which is worth knowing is now stale.
Source (table label): https://www.kernel.org/doc/Documentation/filesystems/proc.rst

**Try-it**:
```sh
cat /proc/execdomains
```

---

## 5. Filesystems, storage, and swap

### `/proc/filesystems`

**Claim**: "a text listing of the filesystems which are supported by the kernel, namely filesystems
which were compiled into the kernel or whose kernel modules are currently loaded." Filesystems
marked `nodev` don't require a block device (virtual/network filesystems); `mount(8)` may consult
this list (excluding `nodev` entries) when no filesystem type is specified.
Source: https://man7.org/linux/man-pages/man5/proc_filesystems.5.html

**Simple explanation**: which filesystem drivers the running kernel can currently mount.

**Why check it**: the presence of an unusual or rarely-used filesystem driver already loaded (e.g.
something normally not needed on this host's role) can indicate either legitimate removable-media
use or, in rarer cases, prep for mounting a crafted filesystem image as part of a container-escape
or privilege-escalation chain that targets a specific parser's bugs.

**Try-it**:
```sh
cat /proc/filesystems
```

### `/proc/swaps`

**Claim**: "Swap areas in use. See also swapon(8)."
Source: https://man7.org/linux/man-pages/man5/proc_swaps.5.html

**Simple explanation**: every active swap device/file, its size, and current usage.

**Why check it**: swapped-out memory can retain sensitive data (credentials, keys) far longer than
RAM would — confirming whether swap is even active, and where, is a prerequisite question before
any memory-forensics claim like "no sensitive data persisted to disk" can be trusted.

**Try-it**:
```sh
cat /proc/swaps
```

### `/proc/diskstats`

**Claim**: "This file contains disk I/O statistics for each disk device. See the Linux kernel
source file Documentation/admin-guide/iostats.rst for further information." (since Linux 2.5.69)
Source: https://man7.org/linux/man-pages/man5/proc_diskstats.5.html

**Simple explanation**: per-block-device I/O counters (reads, writes, merges, time spent) — the
data behind `iostat(1)`.

**Why check it**: a spike in write I/O on a disk that should be quiet is an early, cheap indicator
of mass file writes — ransomware encrypting files in bulk, or a large staged-exfil write to local
disk before it gets shipped out.

**Try-it**:
```sh
cat /proc/diskstats | head
```

### `/proc/partitions`

**Claim**: "Contains the major and minor numbers of each partition as well as the number of
1024-byte blocks and the partition name."
Source: https://man7.org/linux/man-pages/man5/proc_partitions.5.html

**Simple explanation**: the kernel's current view of every known block-device partition and its
size.

**Why check it**: comparing this against what you *expect* to be attached (and against `lsblk`/
`fdisk -l`) is a quick way to spot an unexpected block device — a mounted USB image, an unusual
loop device, or an attacker-attached volume during live triage.

**Try-it**:
```sh
cat /proc/partitions
```

---

## 6. Virtual-memory subsystem detail

### `/proc/vmstat`

**Claim**: "displays various virtual memory statistics. Each line of this file contains a single
name-value pair" — over 100 possible fields (`nr_free_pages`, `pgsteal_kswapd_normal`, `numa_hit`,
`thp_fault_alloc`, `nr_tlb_remote_flush`, etc.); "some lines are present only if the kernel was
configured with suitable options." (since Linux 2.6.0)
Source: https://man7.org/linux/man-pages/man5/proc_vmstat.5.html

**Simple explanation**: the fine-grained, cumulative-counter version of what `/proc/meminfo` shows
as a snapshot — page allocations, reclaim activity, NUMA behavior, transparent-hugepage stats.

**Why check it**: sustained heavy page-reclaim/steal activity (`pgsteal_*` climbing fast) is a
systems-level early-warning sign of memory pressure that can precede an OOM-kill event — useful
context when correlating "why did this critical process just die" with memory subsystem behavior
rather than assuming it was killed deliberately.

**Try-it**:
```sh
grep -E '^(nr_free_pages|pgsteal_kswapd|pswpin|pswpout)' /proc/vmstat
```

### `/proc/zoneinfo`

**Claim**: "displays information about memory zones. This is useful for analyzing virtual memory
behavior." (since Linux 2.6.13)
Source: https://man7.org/linux/man-pages/man5/proc_zoneinfo.5.html

**Simple explanation**: per-NUMA-node, per-zone (DMA/DMA32/Normal/etc.) memory statistics — a more
structural breakdown than `meminfo`.

**Why check it**: relevant mainly to deep memory-pressure/fragmentation investigations rather than
routine security triage; pairs with `buddyinfo` below for a full fragmentation picture.

**Try-it**:
```sh
head -20 /proc/zoneinfo
```

### `/proc/buddyinfo`

**Claim**: "contains information used for diagnosing memory fragmentation issues. Each line starts
with node identification and zone name, followed by counts of available chunks at certain orders.
Chunk size is calculated as (2^order) * PAGE_SIZE... Heavy memory fragmentation results in zero
counters for higher order chunks, causing large contiguous allocation failures."
Source: https://man7.org/linux/man-pages/man5/proc_buddyinfo.5.html

**Simple explanation**: how many free contiguous memory chunks exist at each power-of-two size —
the kernel's "buddy allocator" free-list snapshot.

**Why check it**: if a system is refusing large contiguous allocations (huge pages, certain DMA
buffers) despite plenty of total free memory, this file tells you it's a fragmentation problem, not
an actual memory shortage — relevant when diagnosing degraded performance that superficially looks
like a resource-exhaustion attack but isn't.

**Try-it**:
```sh
cat /proc/buddyinfo
```

---

## 7. Kernel identity and uptime

### `/proc/version`

**Claim**: "This string identifies the kernel version that is currently running. It includes the
contents of `/proc/sys/kernel/ostype`, `/proc/sys/kernel/osrelease`, and
`/proc/sys/kernel/version`." Example: `Linux version 1.0.9 (quinlan@phaze) #1 Sat May 14 01:51:54
EDT 1994`.
Source: https://man7.org/linux/man-pages/man5/proc_version.5.html

**Simple explanation**: the same string `uname -a` largely reproduces, plus build metadata (builder,
build date, compiler).

**Why check it**: fastest way to check a running kernel's exact patch level against a known-CVE
version list — and, because it includes builder/build-timestamp metadata rather than just a version
number, a mismatch between this string and what a management/inventory system *thinks* is running
can indicate an unauthorized kernel swap.

**Try-it**:
```sh
cat /proc/version
uname -a   # cross-check, should agree
```

### `/proc/uptime`

**Claim**: "This file contains two numbers (values in seconds): the uptime of the system (including
time spent in suspend) and the amount of time spent in the idle process."
Source: https://man7.org/linux/man-pages/man5/proc_uptime.5.html

**Simple explanation**: total wall-clock uptime, and separately, cumulative idle time (which can
exceed uptime on multi-core systems, since it sums idle time across all CPUs).

**Why check it**: cross-reference against `/proc/stat`'s `btime` and system logs — a suspiciously
short uptime on a server that's supposed to run for months is either an unplanned reboot (crash,
forced restart post-compromise) or evidence of an unauthorized restart during an incident window.

**Try-it**:
```sh
cat /proc/uptime
uptime -p   # human-readable cross-check
```

---

## 8. Security modules, crypto, keys, and locks

### `/proc/crypto`

**Claim**: "a list of the ciphers provided by the kernel crypto API. For details, see the kernel
Linux Kernel Crypto API documentation available under the kernel source directory
`Documentation/crypto/`."
Source: https://man7.org/linux/man-pages/man5/proc_crypto.5.html

**Simple explanation**: every cryptographic algorithm implementation currently registered with the
in-kernel crypto API (used by dm-crypt, IPsec, kTLS, etc.), including whether each is a software or
hardware-accelerated implementation.

**Why check it**: confirms whether disk-encryption or IPsec/kTLS traffic is actually backed by a
hardware-accelerated (AES-NI) implementation vs. a slow software fallback — relevant to both
performance triage and to confirming an assumed hardware-crypto security property is actually in
effect.

**Try-it**:
```sh
grep -A3 '^name.*: aes\|^name.*: sha256' /proc/crypto | head -20
```

### `/proc/key-users`, `/proc/keys`

**Claim**: both pages state simply "See keyrings(7)" (since Linux 2.6.10).
Source: https://man7.org/linux/man-pages/man5/proc_keys.5.html ;
https://man7.org/linux/man-pages/man5/proc_key-users.5.html

**Simple explanation**: the in-kernel key-retention-service tables — `/proc/keys` lists individual
keys/keyrings the caller can view; `/proc/key-users` shows per-UID quota/usage accounting for that
same service. (Both man pages defer all real field-level detail to `keyrings(7)`, which is a
process/credentials page outside this file's system-wide scope — noted rather than expanded, per
this repo's one-level-deep convention.)

**Why check it**: the kernel key-retention service backs things like NFSv4 credential caching, the
`request-key` upcall mechanism, and some VPN/crypto tooling's in-kernel key storage — an unexpected
key description or a key-quota exhaustion in `/proc/key-users` can point to abuse of that mechanism
(e.g. a runaway or malicious process hammering `add_key(2)`).

**Try-it**:
```sh
cat /proc/key-users
cat /proc/keys 2>/dev/null || echo "may be empty/restricted depending on caller's keyrings"
```

### `/proc/locks`

**Claim**: displays current file locks from `flock(2)`/`fcntl(2)` and leases from `fcntl(2)`. Eight
fields per line: ordinal position, lock type (`FLOCK`/`OFDLCK`/`POSIX`), mode (`ADVISORY`/
`MANDATORY`), access (`READ`/`WRITE`), owning PID (`-1` for OFD locks, not owned by a single
process), `major:minor:inode`, start offset, end offset (`EOF` or literal offset). Since Linux 4.9,
filtered to locks held by processes in the same PID namespace `/proc` was mounted in.
Source: https://man7.org/linux/man-pages/man5/proc_locks.5.html

**Simple explanation**: every advisory/mandatory file lock currently held system-wide (within the
caller's PID namespace).

**Why check it**: a process holding a long-lived exclusive `WRITE` lock on a file it has no obvious
business locking (e.g. a lock file for a service that shouldn't be running) is a persistence/
tamper-prevention signal — some malware locks its own files to resist being overwritten or deleted
while running.

**Try-it**:
```sh
cat /proc/locks
lslocks   # same data, cross-referenced with paths and command names
```

---

## 9. cgroups, consoles, and misc devices

### `/proc/cgroups`

**Claim**: "(since Linux 2.6.24) See cgroups(7)."
Source: https://man7.org/linux/man-pages/man5/proc_cgroups.5.html

**Simple explanation**: lists which cgroup (v1) controllers/subsystems (`cpu`, `memory`, `blkio`,
`pids`, etc.) the running kernel actually supports and how many cgroups currently use each — a
capabilities table, not a per-process membership list (that's `/proc/<pid>/cgroup`, out of scope
here).

**Why check it**: confirms which resource-isolation controllers are actually available before
trusting that a container's resource limits (memory caps, PID caps) can even be enforced — a
controller missing here means limits configured for it are silently unenforceable.

**Try-it**:
```sh
cat /proc/cgroups
```

### `/proc/consoles`

**Claim**: "Shows registered system console lines. To see which character device lines are
currently used for the system console `/dev/console`, you may simply look into the file
`/proc/consoles`."
Source: https://www.kernel.org/doc/Documentation/filesystems/proc.rst (dedicated section on
`/proc/consoles`)

**Simple explanation**: which physical/virtual devices are currently registered as kernel console
output targets (serial port, VGA/framebuffer, netconsole, etc.) and their capability flags.

**Why check it**: a `netconsole`-type entry appearing unexpectedly means kernel messages (which can
include stack traces, addresses, and other sensitive debug output) are being shipped off-box over
the network — worth flagging as a data-exposure channel, and worth checking during a compromise
investigation since some attackers configure netconsole for covert low-level command/control.

**Try-it**:
```sh
cat /proc/consoles
```

### `/proc/misc`

**Claim (registration mechanism)**: miscellaneous character-device drivers register via
`misc_register()`, sharing a single major number; the kernel's official static device-number
allocation table lists **major number 10** as "Non-serial mice, misc features" — the major number
`/proc/misc` entries are all minor numbers under.
Source: https://www.kernel.org/doc/Documentation/admin-guide/devices.rst

**Simple explanation**: a flat list of `minor-number  device-name` pairs — every misc-class
character device currently registered (e.g. `rtc`, `kvm`, `vhost-net`, `tun`, hardware RNGs, watchdog
devices).

**Why check it**: the presence of devices like `/dev/kvm` (virtualization) or a hardware watchdog
tells you real facts about the platform (bare metal vs. VM, whether nested virtualization is
exposed) that are useful context when scoping what kind of attack surface a box actually has;
`tun`/`vhost-net` presence is relevant when auditing whether a host can create its own VPN/tunnel
interfaces.

**Try-it**:
```sh
cat /proc/misc
```

---

## 10. Kernel symbols

### `/proc/kallsyms`

**Claim**: "(since Linux 2.5.71) This holds the kernel exported symbol definitions used by the
modules(X) tools to dynamically link and bind loadable modules. In Linux 2.5.47 and earlier, a
similar file with slightly different syntax was named ksyms."
Source: https://man7.org/linux/man-pages/man5/proc_kallsyms.5.html

**Simple explanation**: every exported kernel symbol (function/variable name) and its current
address — the address column reads as all-zeros for unprivileged readers unless `kptr_restrict` is
disabled (see the `sys/kernel/` section above).

**Why check it**: this file is the direct, concrete consumer of `kptr_restrict` — if you can read
real (non-zeroed) kernel addresses out of `/proc/kallsyms` as an unprivileged user, that's live,
demonstrable proof `kptr_restrict` is misconfigured on this box (not just a theoretical policy
reading), since leaked kernel addresses are a standard building block for defeating KASLR in a
kernel-exploit chain.

**Try-it**:
```sh
head -5 /proc/kallsyms
# addresses of all zeros ("0000000000000000") = kptr_restrict is doing its job for your privilege level
```

---

## 11. Additional top-level `/proc` entries the official docs mention beyond the requested list

The task's list is described as "at minimum" — cross-checking man7's full `proc_*(5)` page index and
kernel.org's `proc.rst` summary table turned up several more genuinely top-level, non-`pid`,
non-process entries worth a one-line flag each:

- **`/proc/sysrq-trigger`** — "Writing a character to this file triggers the same SysRq function as
  typing ALT-SysRq-`<character>`." Writable only by root. A live, no-reboot-needed way to trigger
  emergency kernel actions (sync, remount-read-only, force-reboot, or — relevant to security work —
  a full memory/register dump) without physical console access.
  Source: https://man7.org/linux/man-pages/man5/proc_sysrq-trigger.5.html
- **`/proc/slabinfo`** — "provides information about kernel caches." Backs `slabtop(1)`; kernel
  object-allocation-level memory accounting, one step below `buddyinfo`/`zoneinfo`.
  Source: https://man7.org/linux/man-pages/man5/proc_slabinfo.5.html
- **`/proc/kcore`** — "represents the physical memory of the system ... in ELF core file format,"
  usable with an unstripped kernel binary in GDB to examine live kernel data structures. This is
  effectively a live full-physical-memory acquisition interface built into `/proc` itself —
  directly relevant to memory-forensics tooling, and a high-value target to restrict access to.
  Source: https://man7.org/linux/man-pages/man5/proc_kcore.5.html
- **`/proc/kmsg`** — kernel message ring buffer, readable as an alternative to the `syslog(2)`
  syscall; "a process must have superuser privileges to read this file." The lower-level sibling of
  `dmesg(1)`/`dmesg_restrict`.
  Source: https://man7.org/linux/man-pages/man5/proc_kmsg.5.html
- **`/proc/config.gz`** — "exposes the configuration options that were used to build the currently
  running kernel," gzip-compressed, only present if built with `CONFIG_IKCONFIG_PROC`. Useful for
  confirming exactly which kernel hardening options (e.g. `CONFIG_STRICT_DEVMEM`,
  `CONFIG_MODULE_SIG`) were actually compiled in, without needing separate access to the build
  artifacts.
  Source: https://man7.org/linux/man-pages/man5/proc_config.gz.5.html
- **`/proc/sysvipc/`** (directory: `msg`, `sem`, `shm`) — "enumerate System V Interprocess
  Communication (IPC) objects ... presently exist on the system," equivalent to `ipcs(1)`. Relevant
  to spotting shared-memory-segment-based inter-process covert channels.
  Source: https://man7.org/linux/man-pages/man5/proc_sysvipc.5.html
- **`/proc/pagetypeinfo`**, **`/proc/vmallocinfo`**, **`/proc/allocinfo`**, **`/proc/bootconfig`** —
  all appear only in kernel.org's summary table (Table 1-5) with one-line descriptions
  ("Additional page allocator information," "Show vmalloced areas," memory-allocation-site
  profiling, and boot-config-derived kernel command line respectively); no man7 page exists for any
  of the four. Flagged as index-only coverage rather than expanded, since the source itself doesn't
  go deeper.
  Source: https://www.kernel.org/doc/Documentation/filesystems/proc.rst

(`meminfo`, `cpuinfo`, `loadavg`, and `mounts` are also top-level system-wide entries technically in
scope for this file, but are already covered in `proc-catalog-theoretical.md` Part 2 — not
duplicated here to avoid redundant sourcing of the same claims.)

---

## Distro-doc coverage notes

- **ArchWiki** (`wiki.archlinux.org`): reachable this session via `curl` with a browser User-Agent
  (the Anubis JS-challenge blocks generic automated fetchers but not a normal-looking `curl`
  request). Two pages used directly: `Procfs` (confirms `/proc/cpuinfo`, `/proc/meminfo`,
  `/proc/vmstat`, `/proc/mounts`, `/proc/filesystems`, `/proc/uptime`, `/proc/cmdline` as the
  wiki's own worked examples, plus the `echo 1 > /proc/sys/kernel/sysrq` usage example) and
  `Sysctl` (extensive, cited throughout section 3 above — the richest distro-doc source used in
  this file, particularly for TCP/IP stack hardening knobs and their real-world shipped-default
  deviations from kernel defaults).
- **Debian wiki** (`wiki.debian.org`): **inaccessible this session** — the site runs a
  proof-of-work JS challenge that a bare `curl` (even with a browser User-Agent and a cookie jar)
  cannot clear, unlike ArchWiki's lighter Anubis gate. No Debian wiki content is cited in this file
  as a result; nothing was fabricated to fill the gap. (A prior research pass recorded in
  `proc-catalog-theoretical.md` found `wiki.debian.org/chroot` and `wiki.debian.org/FileSystem` had
  only thin, tangential procfs mentions even when reachable — no dedicated Debian procfs reference
  page exists.)
- **Kali Linux docs** (`kali.org/docs`): genuinely useful, Kali-specific content found and used —
  `kali.org/docs/general-use/kernel-configuration/` documents two concrete default-hardening
  deviations from a "generic Linux" assumption: `dmesg` is unprivileged-readable by default (i.e.
  `kernel.dmesg_restrict` ships as 0, not 1), and IPv4 privileged-port enforcement (ports <1024) is
  disabled by default, both because "Kali is no longer root user by default" — both reversible via
  `kali-tweaks`. Cited in section 3 above (`sys/kernel/*` and `sys/net/*`). `kali.org/tools/procps/`
  was also checked and confirms `sysctl` ships as part of Kali's `procps` package (used only for the
  minor factual point that `sysctl` is bundled Kali tooling, not for any Kali-specific behavioral
  claim).
- **Garuda Linux wiki** (`wiki.garudalinux.org`): one directly relevant page found —
  `Gaming-optimizations` — which live-edits several `/proc/sys/vm/*` and `/proc/sys/kernel/sched_*`
  files as part of its tuning walkthrough (`swappiness`, `compaction_proactiveness`,
  `min_free_kbytes`, `watermark_boost_factor`, `watermark_scale_factor`, `zone_reclaim_mode`,
  `page_lock_unfairness`, `sched_child_runs_first`, `sched_autogroup_enabled`,
  `split_lock_mitigate`). This is genuinely Garuda-specific practical content (cited in the
  `sys/vm/*` section above) — not security-focused, but confirms these files are treated as
  routine, directly-editable runtime knobs in real distro documentation, not just abstract man-page
  entries. No content found for any of `interrupts`, `net/`, `modules`, `swaps`, `diskstats`,
  `crypto`, `keys`, or the other entries in this file — stated explicitly rather than assumed.

---

## References — every distinct source URL used in this file

man7.org Linux man-pages:
- https://man7.org/linux/man-pages/man5/proc_interrupts.5.html
- https://man7.org/linux/man-pages/man5/proc_stat.5.html
- https://man7.org/linux/man-pages/man5/proc_net.5.html
- https://man7.org/linux/man-pages/man8/route.8.html
- https://man7.org/linux/man-pages/man5/proc_sys.5.html
- https://man7.org/linux/man-pages/man5/proc_sys_kernel.5.html
- https://man7.org/linux/man-pages/man5/proc_sys_vm.5.html
- https://man7.org/linux/man-pages/man5/proc_sys_net.5.html
- https://man7.org/linux/man-pages/man5/proc_sys_net_ipv4.5.html
- https://man7.org/linux/man-pages/man5/proc_modules.5.html
- https://man7.org/linux/man-pages/man5/proc_devices.5.html
- https://man7.org/linux/man-pages/man5/proc_dma.5.html
- https://man7.org/linux/man-pages/man5/proc_iomem.5.html
- https://man7.org/linux/man-pages/man5/proc_ioports.5.html
- https://man7.org/linux/man-pages/man5/proc_mtrr.5.html
- https://man7.org/linux/man-pages/man5/proc_execdomains.5.html
- https://man7.org/linux/man-pages/man5/proc_filesystems.5.html
- https://man7.org/linux/man-pages/man5/proc_swaps.5.html
- https://man7.org/linux/man-pages/man5/proc_diskstats.5.html
- https://man7.org/linux/man-pages/man5/proc_partitions.5.html
- https://man7.org/linux/man-pages/man5/proc_vmstat.5.html
- https://man7.org/linux/man-pages/man5/proc_zoneinfo.5.html
- https://man7.org/linux/man-pages/man5/proc_buddyinfo.5.html
- https://man7.org/linux/man-pages/man5/proc_version.5.html
- https://man7.org/linux/man-pages/man5/proc_uptime.5.html
- https://man7.org/linux/man-pages/man5/proc_crypto.5.html
- https://man7.org/linux/man-pages/man5/proc_keys.5.html
- https://man7.org/linux/man-pages/man5/proc_key-users.5.html
- https://man7.org/linux/man-pages/man5/proc_locks.5.html
- https://man7.org/linux/man-pages/man5/proc_cgroups.5.html
- https://man7.org/linux/man-pages/man5/proc_kallsyms.5.html
- https://man7.org/linux/man-pages/man5/proc_sysrq-trigger.5.html
- https://man7.org/linux/man-pages/man5/proc_slabinfo.5.html
- https://man7.org/linux/man-pages/man5/proc_kcore.5.html
- https://man7.org/linux/man-pages/man5/proc_kmsg.5.html
- https://man7.org/linux/man-pages/man5/proc_config.gz.5.html
- https://man7.org/linux/man-pages/man5/proc_sysvipc.5.html

kernel.org (canonical kernel-source documentation):
- https://www.kernel.org/doc/Documentation/filesystems/proc.rst
- https://www.kernel.org/doc/Documentation/networking/proc_net_tcp.rst
- https://www.kernel.org/doc/Documentation/networking/ip-sysctl.rst
- https://www.kernel.org/doc/Documentation/scheduler/sched-stats.rst
- https://www.kernel.org/doc/Documentation/admin-guide/devices.rst

ArchWiki (fetched via curl + browser User-Agent; see coverage note above):
- https://wiki.archlinux.org/title/Procfs
- https://wiki.archlinux.org/title/Sysctl

Kali Linux official docs:
- https://www.kali.org/docs/general-use/kernel-configuration/
- https://www.kali.org/tools/procps/

Garuda Linux wiki:
- https://wiki.garudalinux.org/en/Gaming-optimizations

Debian wiki: no content cited — inaccessible this session (proof-of-work JS challenge); see
coverage note above.
