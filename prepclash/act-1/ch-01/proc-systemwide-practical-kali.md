# Practical survey — system-wide `/proc` entries (remote Kali lab VM)

Sources: `man 5 proc` and the individual `proc_*(5)` pages (man7.org), `kernel.org/doc/html/latest/filesystems/proc.html`, `kernel.org/doc/Documentation/admin-guide/sysctl/kernel.rst`, `kali.org/docs`.
Method: hands-on, read-only inspection as an unprivileged (non-root) user over one non-interactive SSH session to the remote Kali lab VM (an authorized personal lab machine on the local network) — no passwordless sudo available, so all reads are the plain-user view, same as the companion local-machine survey (`proc-systemwide-practical-local.md`). SSH connectivity confirmed working; connection details (address, credentials) intentionally not recorded here — see the "Sanitization" note at the end.

**Scope note**: same ~30-entry system-wide `/proc` list as the local survey, structured to make cross-system deltas easy to spot rather than repeating identical explanations. Where behavior matched the local machine exactly, this file says so briefly and points at the companion file for the "why."

---

## `/proc/interrupts` and `/proc/softirqs`

**Claim**: both present, same shape as local (per-CPU columns, `IR-IO-APIC` chip type). Kali's `wlan0` interface shows the same single-CPU skew for `NET_RX` softirqs seen on the local machine's Wi-Fi NIC (one CPU absorbing the bulk of RX softirq load) — a VM-nested Wi-Fi passthrough/bridge setup, consistent with no multi-queue RX steering for that path.

**Simple explanation**: same mechanism as the local file — see that file's entries for detail. Notable delta: this VM's `IRQ 1` (`i8042`, keyboard controller) count (414) is an order of magnitude higher than the local machine's (16) — plausible given this is a VM guest where keyboard-controller emulation/virtio input events register differently.

## `/proc/net/{tcp,udp,arp,dev,route}`

**Claim**: all five present, world-readable, same format as local. `net/dev` shows this VM has more interfaces than the local machine: `lo`, `eth0` (unused), `wlan0` (active), plus `docker0` and a `br-<hash>` bridge — confirming Docker is installed and has created its default bridge network on this box, even though no containers were observed running traffic at survey time.

**Simple explanation**: Kali images commonly ship or get Docker installed for containerized tool use; the bridge/docker0 interfaces existing with zero traffic just means Docker's daemon is present and initialized, not that anything is actively using it.

**Example** (sanitized, structure only):
```
=== net/dev ===
 face |bytes    packets errs drop ...
     lo:  <n>      <n>    0    0
   eth0:    0        0    0    0
  wlan0: <n>      <n>    0  <n>
docker0:    0        0    0    0
br-<hash>:  0        0    0    0
```

## `/proc/sys/kernel/*`, `/proc/sys/vm/*`, `/proc/sys/net/*`

**Claim**: same trees, same general population. One notable extra `kernel/*` entry not present on the local machine's list: `apparmor_display_secid_mode` and `apparmor_restrict_unprivileged_unconfined` — confirms AppArmor's LSM hooks are compiled in and exposing tunables here, whereas the local (Arch-derivative) machine's `kernel/*` sample didn't show AppArmor-specific entries (Arch-family distros typically ship AppArmor as opt-in, not default-enabled). `vm.swappiness` = 60 here (the kernel's vanilla stock default) vs. 133 on the local machine's `zen`-patched kernel — direct confirmation that the local box's high swappiness is a kernel-patch artifact, not a general Linux default. `vm.overcommit_memory` = 0 on both.

**Simple explanation**: this is the clearest same-list-different-values delta in the whole survey — same sysctl tree shape on both systems, but the actual tunable values (and which LSM-specific knobs exist) trace directly back to each distro's kernel config and default choices (Debian/Kali ships AppArmor enabled by default; this Arch-derivative machine's `zen` kernel patches swap heuristics).

## `/proc/modules`, `/proc/filesystems`, `/proc/swaps`

**Claim**: all present. `modules`: 189 loaded here vs. 177 locally — comparable order of magnitude; Kali's list is headed by `xt_conntrack`/`xt_MASQUERADE`/`bridge`/`stp`/`llc`, i.e. netfilter NAT and bridging modules, consistent with the Docker bridge networking seen in `net/dev` above. `filesystems`: same core pseudo-filesystem set, plus `rpc_pipefs` and `overlay` present here (overlay = Docker/container storage driver; not seen in the local machine's sampled list) and `virtiofs` present on both (host/guest sharing for the VM). `swaps`: this VM uses a single dedicated swap **partition** (`/dev/nvme0n1p6`, priority -1) rather than the local machine's swapfile+`zram` dual setup — a more traditional/textbook layout, no compressed-RAM swap tier here.

**Simple explanation**: `modules` and `filesystems` deltas both trace back to the same fact — this VM runs Docker, which pulls in `overlay` (container-layer filesystem) and netfilter NAT/bridge modules that a non-container desktop wouldn't normally have loaded. The `swaps` delta (partition vs. file+zram) reflects two different, equally valid provisioning choices — VM images are commonly given a fixed swap partition at install time rather than a tunable swapfile.

## `/proc/version`

**Claim**: present. Kernel is `7.0.12+kali-amd64`, Kali-patched, built by Debian's toolchain (`gcc-15`), Kali build tag (`Kali 7.0.12-2kali1`, 2026-06-18) — vs. the local machine's `7.1.5-zen1-2-zen`, Arch build. Confirms these are two genuinely distinct kernel builds/distros, not a shared image.

**Simple explanation**: same file, same purpose as local — the string itself is the most direct "which distro/kernel am I actually on" signal in all of `/proc`.

## `/proc/uptime`, `/proc/diskstats`, `/proc/partitions`

**Claim**: all present, same shape as local. `uptime`: this VM's reported uptime (~96876s, ~26.9h) happened to be roughly 10x the local machine's (~10018s, ~2.8h) at survey time — not a structural difference, just each system's actual runtime. `partitions`: this VM has six partitions on its virtual NVMe disk (EFI, and separate `p2`-`p6` including a dedicated swap partition) vs. the local machine's simpler two-partition (`p1` EFI + `p2` everything-else) layout — a more granular, traditional partition scheme, likely from a standard Kali installer default rather than a single-big-partition Arch install.

**Simple explanation**: both files behave identically to their local-machine counterparts; the values differ only because these are two different disks/histories, not because of any distro-level formatting difference in the `/proc` files themselves.

## `/proc/vmstat`, `/proc/zoneinfo`, `/proc/buddyinfo`, `/proc/cgroups`

**Claim**: all present, identical structure to local. `cgroups`: same 12-13 legacy v1 controller rows, all at hierarchy `0` (cgroup v2 unified hierarchy in use here too, same as local) — this VM's list omits the local machine's `dmem` controller row, likely a kernel-version/config difference (newer kernels have added `dmem` for device-memory cgroup accounting; this VM's slightly older 7.0.12 kernel doesn't yet expose it here vs. local's 7.1.5).

**Simple explanation**: no structural surprises — the memory-accounting internals `/proc` exposes are the same shape regardless of distro; only the live numbers and (for `cgroups`) the exact controller set (kernel-version-dependent) differ.

## `/proc/consoles`

**Claim**: present, same single-`tty0` shape as local, minor:major differs (`4:7` here vs. `4:2` locally) — cosmetic, reflects each VM/host's console device numbering, not a meaningful difference.

## `/proc/crypto`

**Claim**: present, same stanza format. First entries also AES/CCM-related but the driver string differs (`ctr-aes-vaes-avx2` here vs. `-avx512` on the local machine) — this VM's virtual CPU exposes AVX2 but not AVX-512 to the guest, so the kernel's crypto API selects the best available implementation for the hardware it can actually see. Priority values differ too (350 here vs. 550 locally) — consistent with a different (lower-tier, VM-visible) CPU feature set changing which implementation ranks best.

**Simple explanation**: same subsystem, but this is a clean, concrete illustration of `/proc/crypto`'s stated purpose — the registry reflects genuinely different available CPU instruction sets between a bare-metal host and its VM guest.

## `/proc/devices`

**Claim**: present, same two-section structure. Notably different character-device set: this VM lacks the local machine's Nvidia-driver entries (`nvidia`, `nvidia-modeset`, `nvidia-uvm`, etc. — expected, VM guest with no dedicated GPU passthrough) and lacks `cpu/msr`/`cpu/cpuid` character devices seen locally (MSR/CPUID device nodes are often unavailable inside VMs since raw MSR access isn't safely virtualizable). Kali's list instead shows `spi`, `ptp`, `pps`, `cxl` device classes not seen locally. Block devices section is minimal on both (`blkext` only) — modern kernels register actual block devices dynamically elsewhere.

**Simple explanation**: `/proc/devices` is a direct, readable fingerprint of "what hardware/subsystems does this specific kernel build think it has" — the Nvidia/MSR absence here is the clearest hardware-vs-VM tell in the whole survey.

## `/proc/dma`, `/proc/execdomains`

**Claim**: both present, identical single-line content to local (`4: cascade` for `dma`; `0-0 Linux [kernel]` for `execdomains`). No delta — both are legacy/vestigial files whose content doesn't vary meaningfully across modern x86_64 Linux systems.

## `/proc/iomem`, `/proc/ioports`

**Claim**: both present, same tree structure as local. Same zeroed-address behavior for this non-root, non-`CAP_SYSLOG` user — every range read back as `00000000-00000000`, only resource names visible (`System RAM`, `Reserved`, `PCI Bus 0000:00`, `System ROM`, `ACPI Non-volatile Storage`, `ACPI Tables`, ...).

**Simple explanation**: identical behavior to the local machine — see that file's entry for the caveat about this not being explicitly spelled out in the man pages checked. Consistent behavior across two different distros/kernel builds is itself useful confirmation this is a general kernel behavior, not a distro-specific patch.

## `/proc/kallsyms`

**Claim**: present, world-readable, same `0000000000000000` zeroed-address behavior as local for this non-root reader.

**Simple explanation**: same `CAP_SYSLOG`-gated behavior as local — see that file's entry. Consistent across both systems.

## `/proc/key-users`, `/proc/keys`

**Claim**: both present, same format. This VM's `key-users` UID list is shorter/different (fewer UIDs registered keys at survey time) — a function of what's actually logged in/running, not a structural difference.

## `/proc/locks`

**Claim**: present, 51 active locks here vs. 57 locally — comparable scale. Same POSIX/FLOCK-advisory format; on this VM the bulk of POSIX locks trace to one PID (likely a browser or IDE-class process, mirroring the local machine's pattern), plus several `FLOCK` locks scattered across a handful of other PIDs.

**Simple explanation**: no structural delta — file-locking activity just reflects each machine's actual running processes at the moment of the snapshot.

## `/proc/misc`

**Claim**: present. Overlapping core set with local (`kvm`, `rfkill`, `autofs`, `watchdog`, `fuse`, `hpet`, `userfaultfd`, `snapshot`, `hw_random`, `vga_arbiter`, `udmabuf`, `cpu_dma_latency`, `psaux`), but this VM's list lacks the local machine's VirtualBox-host entries (`vboxdrv`/`vboxdrvu`/`vboxnetctl`) and `nvram`/`btrfs-control`/`cpu_wakeup_latency`/`ntsync` — consistent with this being a VM *guest* (no VirtualBox host modules to load) with a narrower module set than the local bare-metal desktop.

**Simple explanation**: another hardware/virtualization-context fingerprint, same idea as `/proc/devices` above.

## `/proc/mtrr`

**Claim**: present as a path, `cat` returns `Operation not permitted` for this unprivileged user — identical behavior to local.

**Simple explanation**: same root-only gating as local; MTRR being permission-restricted rather than absent held true on both a bare-metal desktop and a VM guest.

## `/proc/schedstat`

**Claim**: present, same `version 17` format as local, same near-all-zero domain counters (idle system at survey time).

## `/proc/stat`

**Claim**: present, same per-CPU jiffy-counter format as local. No structural delta observed.

---

## Overall cross-system takeaways

1. **Structure was identical everywhere it mattered.** Every one of the ~30 entries that existed on the local machine also existed on the Kali VM, in the same format, with the same permission class (world-readable, or root-only for `mtrr`, or zeroed-for-non-privileged for `iomem`/`ioports`/`kallsyms`). `/proc`'s system-wide file *shape* is not distro-specific.
2. **Values differed for three distinct, explainable reasons**: (a) genuinely different hardware/virtualization context (Nvidia/MSR devices, VirtualBox-host misc drivers, AVX-512-vs-AVX2 crypto drivers — all local-machine-only, since it's bare metal with an Nvidia GPU vs. a VM guest), (b) different distro/kernel defaults (`vm.swappiness` 133 vs. 60, AppArmor sysctls present only on the Debian-family box), (c) different live workload (uptime, lock counts, interface traffic — just what each machine happened to be doing).
3. Nothing was found present-but-empty or unexpectedly root-only-readable on one system and not the other; the `mtrr` permission denial and the `iomem`/`ioports`/`kallsyms` address-zeroing behaved identically on both.

## Sanitization note

Per this repo's public-GitHub handling rule, the remote system's real IP address, SSH credentials, and hostname/username were used only to establish the one authorized SSH session and are deliberately not recorded anywhere in this file (or the local-machine companion file) — it's referred to throughout only as "the remote Kali lab VM." Raw MAC addresses, ARP table IPs, and other host-identifying values observed during the survey were likewise generalized to placeholders (`<mac>`, `<ip>`, `<n>`) rather than pasted verbatim.
