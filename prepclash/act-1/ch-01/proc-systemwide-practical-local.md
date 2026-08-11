# Practical survey — system-wide `/proc` entries (local machine)

Sources: `man 5 proc` and the individual `proc_*(5)` pages (man7.org), `kernel.org/doc/html/latest/filesystems/proc.html`, `kernel.org/doc/Documentation/admin-guide/sysctl/kernel.rst`.
Method: hands-on, read-only inspection as an unprivileged (non-root) user on this local machine — an Arch-derivative (Garuda) desktop running a `zen` kernel. Companion file `proc-systemwide-practical-kali.md` covers the same list on the remote Kali lab VM for cross-system comparison.

**Scope note**: this is a breadth-first survey of ~30 system-wide (non-`pid`) `/proc` entries listed in `proc(5)`'s "See also" index — the entries `link-02-notes.md` explicitly declined to expand into. Each item below is what was actually observed, not a re-statement of the man page.

---

## `/proc/interrupts`

**Claim**: one row per IRQ line, one column per CPU, showing interrupt counts serviced by each CPU, plus the IRQ chip type (`IR-IO-APIC`) and driver name. Present, world-readable, non-empty.

**Simple explanation**: a live tally of "how many times has each CPU handled interrupt N," useful for spotting an IRQ pinned to one CPU (a sign of bad `irqbalance` config or a driver quirk) or dead hardware.

**Example** (shape, values illustrative):
```
            CPU0       CPU1       ...
   0:        132          0    IR-IO-APIC    2-edge      timer
   1:          0          0    IR-IO-APIC    1-edge      i8042
```

## `/proc/net/{tcp,udp,arp,dev,route}`

**Claim**: all five present, world-readable (no `hidepid`-style gating observed on `net/*`). `tcp`/`udp` list one row per socket with hex-encoded local/remote address:port, state, and owning UID; `arp` lists the neighbor cache (IP, hardware type, flags, MAC, device); `dev` gives per-interface RX/TX byte/packet/error counters; `route` gives the kernel routing table in hex.

**Simple explanation**: this is the pre-`ss`/`ip` era view of networking state — still what those modern tools read under the hood. Addresses are little-endian hex (`0100007F` = `127.0.0.1`), which is the single most confusing thing about reading these files raw.

**Example** (sanitized — real local addresses/interfaces/MACs omitted, placeholders used):
```
=== net/tcp ===
sl  local_address rem_address st tx_queue rx_queue ... uid inode
 0: 0100007F:<port> 00000000:0000 0A ... <uid> <inode>

=== net/arp ===
IP address     HW type  Flags  HW address          Device
<ip>           0x1      0x2    <mac>               <iface>

=== net/dev ===
 face |bytes    packets errs drop ...
   lo:   <n>       <n>    0    0
<iface>: <n>       <n>    0  <n>
```
Note: `/proc/net/dev` counters are live and change between successive reads even at idle — a background process (e.g. a browser tab) generates traffic between two `cat` calls a second apart.

## `/proc/sys/kernel/*`, `/proc/sys/vm/*`, `/proc/sys/net/*` (representative sample)

**Claim**: all three trees present and populated (dozens to 100+ tunables each). Sampled entries: `kernel/{ostype,osrelease,hostname,pid_max,panic,...}`, `vm/{swappiness,overcommit_memory,dirty_ratio,drop_caches,...}`, `net/{core,ipv4,ipv6,mptcp,netfilter,unix}`. Most files are `-rw-r--r--` root:root but world-readable; a few (`osrelease`, `ostype`) are `-r--r--r--` (read-only even to root via this interface — changed only by the kernel itself). `vm.swappiness` = 133 here (unusually high — see note), `vm.overcommit_memory` = 0 (heuristic overcommit).

**Simple explanation**: `/proc/sys` is the live control-panel — same values `sysctl -a` reads/writes, one file per tunable, `cat` to read, `echo > file` (as root) to write for the current boot only. `swappiness` above 100 is possible on kernels with modified swap heuristics (this machine runs `zen`, which patches default swappiness upward to favor `zram`); vanilla kernels cap it at 100.

**Example**:
```sh
cat /proc/sys/vm/swappiness            # 133 (zen-patched default, favors zram)
cat /proc/sys/vm/overcommit_memory     # 0 = heuristic overcommit
ls -la /proc/sys/kernel/osrelease      # -r--r--r-- root root — read-only even to root
```

## `/proc/modules`

**Claim**: present, one line per loaded kernel module: name, size in bytes, use count, list of dependent modules, load state (`Live`/`Loading`/`Unloading`), and kernel address (zeroed here — see `kallsyms` below). 177 modules loaded on this system at survey time.

**Simple explanation**: this is what `lsmod` formats for humans; `modules` is the raw source.

## `/proc/filesystems`

**Claim**: present, two columns — a `nodev` marker (pseudo/virtual filesystems needing no block device) and the filesystem type name. ~30 entries: `sysfs`, `tmpfs`, `proc`, `cgroup2`, `ext4`, `btrfs`, `vfat`, `fuse`, `overlay`-class entries, etc.

**Simple explanation**: the list of filesystem types the running kernel currently knows how to mount (built-in + currently-loaded modules) — `mount -t <fstype>` only works for types appearing here.

## `/proc/swaps`

**Claim**: present, header + one row per active swap area: filename, type (`file`/`partition`), size, used (KB), priority. This system has two: a swapfile (`/swap/swapfile`, priority -1) and a `zram0` block device (priority 100, near-zero used).

**Simple explanation**: higher priority is preferred first — here `zram` (compressed RAM-backed swap, very fast) is drained before the on-disk swapfile.

## `/proc/version`

**Claim**: present, single line: kernel version string, build user/host, compiler/linker versions, build flags, build timestamp.

**Simple explanation**: `uname -a` sources most of its output from here.

**Example** (distro build tag only, not this machine's real hostname):
```
Linux version <ver>-zen<n>-<n>-zen (<builder>@archlinux) (gcc ...) #1 ZEN SMP PREEMPT_DYNAMIC <date>
```

## `/proc/uptime`

**Claim**: present, two space-separated floats: total seconds since boot, and total "idle" seconds summed across all CPUs (so on a multi-core box the second number can exceed the first).

**Simple explanation**: what `uptime`(1) parses; the idle figure is a cumulative CPU-seconds count, not wall-clock idle time.

## `/proc/diskstats` and `/proc/partitions`

**Claim**: both present. `diskstats`: one row per block device/partition with 17-20 space-separated counters (major, minor, name, reads completed, reads merged, sectors read, ms spent reading, ... — the full field list is in the kernel's `Documentation/admin-guide/iostat.rst`). `partitions`: simpler four-column table (major, minor, block count, name) — what `lsblk`/lsblk-less tools like lightweight installers read directly.

**Simple explanation**: `iostat` and friends parse `diskstats`; `partitions` is the minimal "what block devices exist" listing, both readable by any user (block-level statistics aren't considered sensitive, unlike file contents).

## `/proc/vmstat`, `/proc/zoneinfo`, `/proc/buddyinfo`

**Claim**: all present. `vmstat`: flat `key value` list, hundreds of counters (`nr_free_pages`, `nr_zone_active_anon`, `workingset_refault_file`, ...). `zoneinfo`: per-NUMA-node, per-zone (`DMA`/`DMA32`/`Normal`) breakdown of the same class of counters plus watermarks. `buddyinfo`: one row per zone showing free-page-block counts by order (2^order pages) — the raw view of the kernel's buddy allocator's free lists.

**Simple explanation**: three views of the same subsystem at increasing granularity — `vmstat` is the systemwide summary, `zoneinfo` breaks it down per memory zone, `buddyinfo` shows fragmentation directly (a `buddyinfo` row heavy on order-0/1 and empty at high orders means memory is fragmented, harder to satisfy large contiguous allocations like hugepages).

## `/proc/cgroups`

**Claim**: present, header + one row per cgroup v1 controller (`cpu`, `cpuacct`, `blkio`, `devices`, `freezer`, `net_cls`, `perf_event`, `net_prio`, `hugetlb`, `pids`, `rdma`, `misc`, `dmem` here — 13 total), with hierarchy ID, cgroup count, enabled flag.

**Simple explanation**: this file only enumerates the legacy cgroup v1 controllers; a pure-cgroup-v2 (unified hierarchy) system still shows this file for compatibility, with `hierarchy` staying `0` for controllers that have moved to v2 — that's the case here (all rows show hierarchy `0`).

## `/proc/consoles`

**Claim**: present, one line here: `tty0 -WU (EC p ) 4:2` — device name, operations flags (write/unblanked/enabled), major:minor.

**Simple explanation**: lists registered kernel consoles (where kernel messages/`printk` output can go) — `tty0` here means the current virtual terminal is the active console.

## `/proc/crypto`

**Claim**: present, large (dozens of stanzas), one block per registered crypto algorithm/implementation: `name`, `driver`, backing `module`, `priority` (implementation selection order — higher wins), `refcnt`, `selftest` result, `type` (`aead`/`skcipher`/`shash`/...), block/IV sizes.

**Simple explanation**: the kernel's crypto API registry — every AES/SHA/etc. implementation available in-kernel (used by dm-crypt, IPsec, kTLS, etc.), including which one wins when multiple implementations of the same algorithm exist (e.g. an AES-NI-accelerated one outranking a generic C one). First entry observed here (`ccm(aes)`) shows a VAES/AVX-512-accelerated driver, confirming hardware AES acceleration is in use.

## `/proc/devices`

**Claim**: present, two sections (`Character devices:`, `Block devices:`), each a `major_number name` table.

**Simple explanation**: the major-number-to-driver-name registry `mknod` and the kernel's device layer rely on; this is what `ls -la /dev` major numbers resolve against.

## `/proc/dma`

**Claim**: present but nearly empty — a single line, `4: cascade`, on this modern (2026) laptop hardware.

**Simple explanation**: legacy ISA-style DMA channel registry from the PC/AT era; the "cascade" entry is a historical artifact (channel 4 cascades the two legacy 8237 DMA controllers together) — modern devices use scatter-gather/bus-mastering DMA that never registers here, so this file being nearly empty is expected on current hardware, not a fault.

## `/proc/execdomains`

**Claim**: present, one line: `0-0 Linux [kernel]`.

**Simple explanation**: historical hook for Linux's personality/ABI-emulation layer (running non-Linux binary personalities, e.g. old iBCS2/SVR4 support); on a modern kernel only the native `Linux` personality is registered — this file is effectively vestigial today.

## `/proc/iomem` and `/proc/ioports`

**Claim**: both present, tree-structured (indented) listings of physical memory address ranges / I/O port ranges and the resource name claiming each. As an unprivileged user, every address range read back as `00000000-00000000` — only the resource *names* (`System RAM`, `Reserved`, `PCI Bus 0000:00`, `System ROM`, `ACPI Non-volatile Storage`, keyboard/DMA/RTC port names, ...) were visible; the actual addresses were zeroed.

**Simple explanation**: this looks like the same address-hiding family as `kptr_restrict` (see `kallsyms` below) — recent kernels avoid handing unprivileged users a physical memory map, since that map is exactly what you'd want before attempting a `/dev/mem`-based exploit or defeating KASLR. This specific address-zeroing behavior for `iomem`/`ioports` wasn't spelled out in the man7.org `proc_iomem(5)`/`proc(5)` pages or the kernel.org filesystems/proc.html doc checked — noted here as directly observed behavior, not a documented guarantee.

**Example** (as actually observed, non-root):
```
00000000-00000000 : Reserved
00000000-00000000 : System RAM
  00000000-00000000 : PCI Bus 0000:00
  00000000-00000000 : System ROM
```

## `/proc/kallsyms`

**Claim**: present, world-readable (`-r--r--r--`), one line per kernel symbol: address, type letter (`T`=text/global, `t`=text/local, etc.), symbol name. As an unprivileged user every address read back as `0000000000000000` despite `/proc/sys/kernel/kptr_restrict` reading `0` (the default, "hash %p addresses" setting) on this system.

**Simple explanation**: `kptr_restrict` (documented in `kernel.org/doc/Documentation/admin-guide/sysctl/kernel.rst`) is the general sysctl governing `%pK`-format kernel pointer exposure (0=hashed, 1=zeroed unless `CAP_SYSLOG`+matching UID, 2=always zeroed) — but `kallsyms` specifically gates on `CAP_SYSLOG` for showing real values regardless of the sysctl's numeric value, so a non-`CAP_SYSLOG` reader sees zeros here even at the "permissive" setting 0. This is why `nm`-style kernel address leaks aren't just a `sudo cat` away on a stock desktop.

## `/proc/key-users` and `/proc/keys`

**Claim**: both present. `key-users`: one row per UID that owns kernel keys, with key counts and quota usage (`used total/max_keys used/max_bytes`). `keys`: one row per key visible to the caller — serial (hex), flags, expiry, permission bits, owning UID/GID, type (`keyring`), description.

**Simple explanation**: the kernel keyring subsystem (used for kernel-held credentials — keyutils, some VPN/Kerberos/NFS auth material, systemd's credential store) — a normal user only sees their *own* session/UID keyrings here, not other users' keys, which is the expected confidentiality boundary (no `hidepid`-equivalent needed; the keyring subsystem enforces this itself).

**Example** (sanitized):
```
=== key-users ===
    0:   <n> <used>/<used> <n>/<max> <n>/<max>
 <uid>:     1 1/1 1/200 9/20000

=== keys ===
<serial> I--Q---   <n> perm <perm>  <uid>  <uid> keyring   _ses: 1
```

## `/proc/locks`

**Claim**: present, one row per active file lock system-wide (POSIX advisory, `FLOCK` advisory, etc.): lock ID, type, mode (`READ`/`WRITE`), owning PID, `major:minor:inode` of the locked file, byte range (`start end` or `EOF`). 57 active locks observed at survey time, mostly held by one browser-class process's PID, plus a handful of others (lockfiles, single-instance app locks).

**Simple explanation**: what `lslocks`(8) parses; visible system-wide to any user (lock metadata — which PID locked which inode — isn't file *content*, so it isn't gated).

## `/proc/misc`

**Claim**: present, `minor_number name` pairs for drivers registered under the shared major-10 "misc" character device class: `rfkill`, `psaux`, `device-mapper`, `watchdog`, VirtualBox's `vboxdrv`/`vboxdrvu`/`vboxnetctl` (confirms VirtualBox host modules loaded), `kvm`, `uinput`, `btrfs-control`, `hw_random`, `fuse`, `nvram`, `hpet`, `userfaultfd`.

**Simple explanation**: `/dev/misc/*`-style devices that don't warrant their own major number all share major 10 and are told apart by minor number — this file is the lookup table.

## `/proc/mtrr`

**Claim**: present as a path, but `cat /proc/mtrr` returns `Operation not permitted` (exit 1) for an unprivileged user — a real permission denial, not an empty/absent file.

**Simple explanation**: Memory Type Range Registers configure CPU cache behavior (write-combining, uncacheable) for physical address ranges — a hardware-level setting significant enough that reading the live register state is root-only.

## `/proc/schedstat`

**Claim**: present, per-CPU scheduler statistics (`version 17` format here) plus per-`domain` (SMT/MC scheduling-domain) load-balancing counters, mostly zero on an idle desktop system.

**Simple explanation**: raw counters for the CFS/EEVDF scheduler's internal accounting — what tools like `perf sched` or custom scheduler-latency dashboards would consume; not something a human reads directly.

## `/proc/softirqs`

**Claim**: present, same shape as `/proc/interrupts` (one row per softirq type, one column per CPU): `HI`, `TIMER`, `NET_TX`, `NET_RX`, `BLOCK`, `IRQ_POLL`, `TASKLET`, `SCHED`, `HRTIMER`, `RCU`. `NET_RX` on this system is heavily skewed to one CPU (>11 million vs. tens/hundreds on others) — consistent with a single CPU handling the Wi-Fi NIC's softirq load (no RSS/multi-queue spreading for this device).

**Simple explanation**: softirqs are the deferred, lower-priority half of interrupt handling (the hardirq does minimal work and schedules a softirq to finish the job) — this file is `/proc/interrupts`'s counterpart for that deferred layer.

## `/proc/stat`

**Claim**: present, kernel/system-wide statistics since boot: aggregate `cpu` line plus one `cpuN` line per logical CPU (user/nice/system/idle/iowait/irq/softirq/steal/guest/guest_nice jiffy counts), plus (further down, not shown in this excerpt) `intr`, `ctxt`, `btime`, `processes`, `procs_running`, `procs_blocked`.

**Simple explanation**: this is the single file `top`, `vmstat`, and `mpstat` all read for CPU utilization — the per-jiffy counters here are what gets diffed over an interval to compute the percentages those tools display.
