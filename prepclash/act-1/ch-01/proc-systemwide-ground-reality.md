# `/proc` system-wide entries — theory vs. ground reality

Synthesis of three companion files: `proc-systemwide-theoretical.md` (sourced claims from man7,
kernel.org, and distro docs), `proc-systemwide-practical-local.md` (hands-on survey, local Garuda/
`zen`-kernel desktop, unprivileged user), and `proc-systemwide-practical-kali.md` (same survey, remote
Kali lab VM over SSH, unprivileged user). Goal: for every entry/logical group in the theoretical file,
classify what the practical surveys actually confirmed.

## Classification legend

- **match** — practical observation on one or both systems confirms the theoretical claim as stated,
  no meaningful gap.
- **partial-nuance** — theory was broadly right, but practice surfaced a real-world detail, edge case,
  or interaction the theoretical file didn't fully spell out (or got the framing slightly off).
- **system-specific-difference** — structure/claim held on both systems, but *values or content*
  diverged in an explainable, informative way (kernel build, distro, hardware, VM vs. bare metal).
- **documented-but-not-observed** — theoretical file makes a claim (sometimes a security-critical one)
  that neither practical survey actually exercised/verified with a real value.

---

## 1. Interrupts, softirqs, CPU/scheduler statistics

| Entry | Classification | Note |
|---|---|---|
| `/proc/interrupts` | match + system-specific-difference | Structure/claim confirmed on both. Kali VM's `i8042` IRQ count was ~10x the local machine's — plausible VM keyboard-controller emulation artifact, not a theory gap. |
| `/proc/stat` | match | Confirmed on both, no surprises. |
| `/proc/softirqs` | match | Confirmed on both; both systems independently showed `NET_RX` pinned to one CPU (Wi-Fi NIC without RSS/multi-queue steering) — a real-world illustration of the theoretical "cheap anomaly signal" framing, not a contradiction of it. |
| `/proc/schedstat` | match | Confirmed on both, both idle at survey time so counters were mostly zero — consistent with theory's description, no dynamic/attack scenario was actually exercised. |

## 2. `net/` — networking layer

| Entry | Classification | Note |
|---|---|---|
| `/proc/net` (symlink-to-self/net claim) | documented-but-not-observed | Neither practical file ran `readlink -f /proc/net` to confirm the Linux-2.6.25+ symlink/namespace behavior specifically — net/* contents were read directly, but this particular structural claim wasn't re-verified. |
| `/proc/net/tcp`, `/proc/net/udp` | match | Hex-encoded local/remote address:port, state, UID fields all confirmed present on both systems. |
| `/proc/net/arp` | match | Confirmed present, same field layout, on both. |
| `/proc/net/dev` | match + partial-nuance | Confirmed on both; local survey added a genuinely new observation not in theory — counters visibly change between two `cat` calls a second apart even at idle, a live-data caveat worth stating explicitly for analysts diffing snapshots. |
| `/proc/net/route` | match | Confirmed present on both (claimed via the `net/{tcp,udp,arp,dev,route}` bundle), no worked example shown but presence/format not contradicted. |

## 3. `sys/` — sysctl tree

| Entry | Classification | Note |
|---|---|---|
| `/proc/sys/` (directory, general) | partial-nuance | Never explicitly `ls`'d in either practical file, but `kernel/*`, `vm/*`, `net/*` subtrees were sampled directly, confirming the tree exists and is populated as claimed. |
| `/proc/sys/kernel/{dmesg_restrict, yama/ptrace_scope, modules_disabled, randomize_va_space, core_pattern, sysrq}` | **documented-but-not-observed** | None of these named security-relevant entries were read with real values in either practical survey. Notably, the theoretical file's headline Kali-specific claim (`dmesg_restrict` ships as 0/unrestricted on Kali) was **never actually checked** on the real Kali lab VM — a genuine theory/practice gap worth closing before relying on that claim operationally. |
| `/proc/sys/kernel/kptr_restrict` | partial-nuance | Indirectly observed via the `kallsyms` entry (value `0` on the local box) — see section 10 below for the nuance practice added about *how* it actually gates kallsyms. |
| `/proc/sys/vm/{swappiness, overcommit_memory}` | match + system-specific-difference | Both explicitly read on both systems. `swappiness`: 133 (local, `zen`-patched) vs. 60 (Kali, vanilla default) — direct empirical confirmation that the local box's high value is a kernel-patch artifact, exactly as the theoretical file's Garuda-tuning citation implied. `overcommit_memory`: 0 on both. |
| `/proc/sys/vm/{drop_caches, panic_on_oom, oom_dump_tasks, unprivileged_userfaultfd}` | documented-but-not-observed | Named in theory, not individually read with values in either practical survey. |
| `/proc/sys/net/*` (tree existence: `core/ipv4/ipv6/mptcp/netfilter/unix`) | match | Tree presence confirmed on both. |
| `/proc/sys/net/*` named hardening knobs (`tcp_syncookies`, `rp_filter`, `accept_redirects`, `accept_source_route`, `log_martians`, `tcp_timestamps`, `ip_unprivileged_port_start`) | **documented-but-not-observed** | Theory's second Kali-specific claim (unprivileged ports <1024 by default) also went unverified in practice — same gap pattern as `dmesg_restrict` above. |
| AppArmor sysctls under `kernel/*` | system-specific-difference (practice-only finding) | Kali survey found `apparmor_display_secid_mode` / `apparmor_restrict_unprivileged_unconfined` present, absent on the local Arch-derivative box — a real, practically-discovered LSM-availability delta the theoretical file doesn't mention at all (it predates/doesn't cover AppArmor specifics). |

## 4. Modules, devices, hardware-resource tables

| Entry | Classification | Note |
|---|---|---|
| `/proc/modules` | match + system-specific-difference | Confirmed both (177 local vs. 189 Kali); Kali's extra modules (`xt_conntrack`, `xt_MASQUERADE`, `bridge`, `stp`, `llc`) trace to Docker's netfilter/bridge setup — a concrete, theory-consistent "unexpected module → investigate why" scenario, resolved benignly. |
| `/proc/devices` | match + system-specific-difference | Best real-world confirmation of the theoretical "Why check it" claim about VM/bare-metal fingerprinting: local box shows Nvidia + `cpu/msr`/`cpu/cpuid` device classes, Kali VM lacks both and shows `spi`/`ptp`/`pps`/`cxl` instead. |
| `/proc/dma` | match | Identical single-line vestigial content (`4: cascade`) on both — confirms theory's "low priority on modern hardware" framing. |
| `/proc/iomem`, `/proc/ioports` | partial-nuance | Confirmed present on both, but both practical files independently found unprivileged readers get all-zero address ranges (resource *names* only) — a real, consistent behavior across two distros/kernels that the theoretical file doesn't mention at all (it only describes tree structure/purpose, not this access-control detail). Flagged in both practical files as "not spelled out" in the man pages checked. |
| `/proc/mtrr` | partial-nuance | Theoretical file's try-it script hedges with "not present (common on modern kernels using PAT instead)." Practice found the opposite shape on both systems: the file **is** present but returns `Operation not permitted` for an unprivileged reader — a real permission denial, not absence. Worth correcting in the theory file if revised. |
| `/proc/execdomains` | match | Identical vestigial single-line content on both, consistent with theory's "essentially none today" framing. |

## 5. Filesystems, storage, swap

| Entry | Classification | Note |
|---|---|---|
| `/proc/filesystems` | match + system-specific-difference | Confirmed both; Kali adds `overlay` and `rpc_pipefs` (Docker container storage), local doesn't have those loaded — exactly the kind of "unusual driver present" signal theory calls out, resolved benignly by the Docker explanation. |
| `/proc/swaps` | match + system-specific-difference | Confirmed both; local uses swapfile+`zram` dual-tier, Kali uses a dedicated swap partition — two valid provisioning choices, structure identical. |
| `/proc/diskstats` | match | Confirmed both, no structural delta. |
| `/proc/partitions` | match + system-specific-difference | Confirmed both; Kali's 6-partition layout vs. local's 2-partition layout reflects installer defaults, not a `/proc` behavior difference. |

## 6. Virtual-memory subsystem detail

| Entry | Classification | Note |
|---|---|---|
| `/proc/vmstat` | match | Confirmed both, no structural delta. |
| `/proc/zoneinfo` | match | Confirmed both, no structural delta. |
| `/proc/buddyinfo` | match | Confirmed both, no structural delta. |

## 7. Kernel identity and uptime

| Entry | Classification | Note |
|---|---|---|
| `/proc/version` | match | Confirmed both; correctly distinguished two genuinely different kernel builds (Arch `zen` vs. Debian-toolchain Kali-patched), exactly the "unauthorized kernel swap" detection use case theory describes. |
| `/proc/uptime` | match | Confirmed both, values differ only because runtimes differ — not a `/proc` behavior difference. |

## 8. Security modules, crypto, keys, locks

| Entry | Classification | Note |
|---|---|---|
| `/proc/crypto` | match + system-specific-difference | Strong real-world confirmation of theory's "confirms hardware-accelerated crypto" claim: local (bare metal) selects an AVX-512 AES driver at priority 550; Kali VM guest selects AVX2 at priority 350 — the registry visibly adapting to the CPU feature set each kernel can actually see. |
| `/proc/key-users`, `/proc/keys` | match | Confirmed both, confidentiality boundary (own UID's keys only) held on both, consistent with theory. |
| `/proc/locks` | match | Confirmed both (57 vs. 51 active locks), same format, no structural delta. |

## 9. cgroups, consoles, misc devices

| Entry | Classification | Note |
|---|---|---|
| `/proc/cgroups` | match + system-specific-difference | Confirmed both; Kali's slightly older kernel (7.0.12) lacks the `dmem` controller row present on local's 7.1.5 — a clean kernel-version-dependent delta, both otherwise identical (cgroup v2 unified, hierarchy 0 everywhere). |
| `/proc/consoles` | match | Confirmed both, only cosmetic major:minor numbering differs. |
| `/proc/misc` | match + system-specific-difference | Second-best VM/bare-metal fingerprint in the survey: local (VirtualBox *host*) shows `vboxdrv`/`vboxdrvu`/`vboxnetctl`; Kali (a VM *guest*) lacks those and has a narrower driver set overall — directly confirms theory's stated use case ("bare metal vs. VM... context"). |

## 10. Kernel symbols

| Entry | Classification | Note |
|---|---|---|
| `/proc/kallsyms` | partial-nuance | Confirmed present, world-readable, and zeroed-for-unprivileged on both systems — but practice surfaced a real mechanism theory doesn't state: `kallsyms` specifically gates real addresses on `CAP_SYSLOG`, *independent of* the `kptr_restrict` sysctl's numeric value (which read `0`, the "permissive" setting, on the local box, yet addresses were still zeroed). Worth folding back into the theoretical file as a correction/refinement. |

## 11. Additional top-level entries (sysrq-trigger, slabinfo, kcore, kmsg, config.gz, sysvipc/, pagetypeinfo, vmallocinfo, allocinfo, bootconfig)

**documented-but-not-observed — all of them.** None of the ten entries flagged as "additional top-level entries the official docs mention" in the theoretical file's section 11 were exercised in either practical survey. This includes `/proc/kcore` (live physical-memory acquisition interface) and `/proc/config.gz` (build-time hardening-flag confirmation) — both high-value for an analyst and both untested in practice so far.

(`meminfo`, `cpuinfo`, `loadavg`, `mounts` are explicitly out of scope for all three source files, per the theoretical file's own note — not scored here.)

---

## Gotcha for analysts doing live remote `/proc` inspection over SSH

During the practical survey's SSH session against the remote Kali lab VM, the returned data stream
contained a fake system-reminder-style text injection — content formatted to look like a legitimate
meta-instruction, claiming a `/proc` file had been "modified" and directing the agent conducting the
survey not to tell the user about it. It was correctly identified as untrusted payload embedded in
remote output and disregarded as a control signal; it is reported here instead of being acted on.

**Takeaway**: anything read back over an SSH session — command output, file contents, terminal
text — is *data*, never *control input*, no matter how authoritative-looking or how closely it mimics
an system/tool-level instruction format. A compromised or malicious remote host (or a MITM'd session)
can inject text designed to look like a trusted directive. Automated tooling (including LLM-driven
tooling) doing live remote `/proc` inspection must treat 100% of remote output as untrusted and inert,
and any embedded "instruction-shaped" text as itself a finding to flag, not a command to follow. This
applies equally to a human analyst manually reviewing SSH session output before acting on it.

---

## Practical takeaways for a security analyst

**Reliable across any Linux box** (presence, format, and field semantics held on both a bare-metal
Arch-derivative desktop and a Debian-family Kali VM guest — safe to build tooling/parsers against
without distro-specific branching): `/proc/stat`, `/proc/uptime`, `/proc/version`, `/proc/interrupts`,
`/proc/softirqs`, `/proc/schedstat`, `/proc/modules`, `/proc/filesystems`, `/proc/swaps`,
`/proc/diskstats`, `/proc/partitions`, `/proc/vmstat`, `/proc/zoneinfo`, `/proc/buddyinfo`,
`/proc/cgroups`, `/proc/consoles`, `/proc/execdomains`, `/proc/dma`, `/proc/locks`,
`/proc/key-users`/`/proc/keys`, `/proc/net/{tcp,udp,arp,dev,route}`. Values will differ machine to
machine; the *shape* and where to look will not.

**Kernel-config / hardening-posture dependent** (same file exists everywhere, but the live value
depends on which kernel patches, LSM, or packages are in play — never assume a value from one box
generalizes): `/proc/sys/vm/swappiness` (60 vanilla vs. 133 on a `zen`-patched kernel), AppArmor-
specific entries under `/proc/sys/kernel/*` (present only where AppArmor is compiled in and active —
Debian/Kali-family, not Arch by default), `/proc/sys/kernel/kptr_restrict` interacting with
`/proc/kallsyms`'s separate `CAP_SYSLOG` gate, `/proc/iomem`/`/proc/ioports` address-zeroing for
unprivileged readers, `/proc/mtrr`'s root-only permission gate, `/proc/cgroups`'s exact controller set
(kernel-version-dependent — `dmem` appeared only on the newer kernel here). The specific hardening
knobs this survey flagged but never actually verified with real values —
`dmesg_restrict`, `yama/ptrace_scope`, `modules_disabled`, `randomize_va_space`, `sysrq`,
`tcp_syncookies`, `rp_filter`, `accept_redirects`, `accept_source_route`, `log_martians`,
`ip_unprivileged_port_start` — belong in this same bucket by nature, but as a documented gap: don't
treat this survey as having confirmed Kali's shipped defaults for any of them; re-check directly.

**VM vs. bare-metal dependent** (the file is universal, but its *content* is one of the more reliable
signals for distinguishing guest from host — genuinely useful for scoping attack surface or spotting a
box that claims to be bare metal but isn't): `/proc/devices` (Nvidia/`cpu/msr`/`cpu/cpuid` present only
on bare metal with a real GPU; `spi`/`ptp`/`pps`/`cxl` seen only on the VM guest here), `/proc/misc`
(VirtualBox host drivers `vboxdrv`/`vboxdrvu`/`vboxnetctl` present only on the bare-metal
*hypervisor host*, absent on the VM guest), `/proc/crypto` (AES driver and priority tracks the CPU
instruction set the kernel can actually see — AVX-512 bare metal vs. AVX2-only VM guest), and to a
lesser extent `/proc/interrupts` (VM guest keyboard-controller emulation showing a much higher `i8042`
count than bare metal).

---

## Sanitization check

Both source practical files were already written with this repo's public-GitHub sanitization
discipline applied at authoring time: `proc-systemwide-practical-local.md` uses `<port>`/`<uid>`/
`<inode>`/`<ip>`/`<mac>`/`<iface>` placeholders throughout its worked examples and a generic build-tag
placeholder in the `/proc/version` excerpt; `proc-systemwide-practical-kali.md` carries an explicit
closing "Sanitization note" stating the remote VM's real IP, SSH credentials, and hostname/username
were used only to establish the session and were deliberately never recorded, with MAC/ARP/IP values
in examples likewise generalized to placeholders. Re-reading all three source files in full for this
comparison, nothing sensitive (no real IPs, credentials, hostnames, usernames, or raw MAC addresses)
was found that needed flagging or was carried forward into this file — the existing sanitization holds
up under review, and this file only aggregates already-sanitized claims from the three sources.
