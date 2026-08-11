# `/proc` Ground-Reality Report — docs vs. two live systems

Companion to `link-02-notes.md` (the `proc(5)` doc study) and the three catalogs it spawned:
`proc-catalog-theoretical.md` (documentation-only, 40 cited sources), `proc-catalog-practical-local.md`
(this machine, Arch-family/zen kernel), `proc-catalog-practical-kali.md` (a personal Kali lab VM,
inspected read-only over SSH). This file reconciles the three: for each area, does what the official
docs claim actually hold up on two real, independently-built Linux boxes?

**Method**: no new commands were run to produce this file — it's a synthesis of the other three
documents only. Same sanitization rule as the practical reports applies throughout (no real IP,
password, hostname, or username, even indirectly quoted).

---

## 1. Filesystem identity

**Match.** Both live systems confirm the doc's core claim exactly: `proc` filesystem type,
zero-sized blocks/inodes (`stat -f /proc` shows `Blocks: Total: 0`), mounted `rw,nosuid,nodev,
noexec,relatime` with no `hidepid=` option present in either mount line. This is the one area with
zero daylight between theory and practice on either box — unsurprising, since it's a structural
guarantee of how procfs is implemented, not a configurable policy.

## 2. Top-level layout: numeric PID dirs + system-wide files

**Match, with a system-specific difference underneath.** Both systems show the same two-tier shape
(numeric PID dirs + several dozen system-wide entries) and, notably, the *same* root-only-readable
cluster: `kcore`, `kmsg`, `kpagecgroup`, `kpagecount`, `kpageflags`, `pagetypeinfo`, `slabinfo`,
`timer_list`, `vmallocinfo` are `-r--------` on both, and `sysrq-trigger` is `--w-------` (write-only,
root-only) on both. That consistency across two unrelated kernel builds is a meaningful confirmation
that this restricted cluster is a stable, intentional kernel-wide policy — not a distro quirk.

**System-specific difference**: the local machine has `bootconfig`, `config.gz`, and `scsi/` at the
top level; the Kali VM has none of the three. Per the practical-kali report this is a kernel-build/
boot-time configuration difference, not a security posture difference:
- `config.gz` requires `CONFIG_IKCONFIG_PROC` compiled in.
- `bootconfig` requires the kernel command line to actually carry an extended boot-config blob.
- `scsi/` reflects whether the kernel registered a legacy SCSI HBA handler — expected to be absent on
  a VM presenting virtio/NVMe-style block devices instead.

None of these three differences change what an analyst should assume is *always* there — they're a
concrete example of the doc's "system-wide files" being real but non-guaranteed at the individual-file
level, something the theoretical catalog documents each file's existence but doesn't flag as
conditional.

## 3. Per-process file ownership and the `self`/`thread-self` symlinks

**Partial/nuance — a detail the docs don't emphasize.** The docs (`proc_pid(5)`, folded into
link-02) correctly state that `/proc/pid/*` files are owned by the process's effective UID/GID
(barring the dumpable exception). Both live systems confirm this for the *target* directory. But
both also independently surfaced the same nuance neither `proc(5)` nor `proc_pid(5)` calls out
explicitly: the `self`/`thread-self` **magic symlink objects themselves** always report as
`root:root`, regardless of who owns the process they resolve to. This is a property of the symlink
living in procfs's shared kernel-managed namespace, distinct from the target directory's ownership —
confirmed identically on both the local machine and the Kali VM, so it's not a fluke of one system.

## 4. `hidepid` hardening

**Not observed / environment-dependent.** This is the clearest gap between documentation and
practice in this set of reports. The theoretical catalog documents `hidepid=0/1/2/4` (`off`/
`noaccess`/`invisible`/`ptraceable`) and `subset=pid` in detail, citing both man7.org and kernel.org.
Neither live system has `hidepid=` set at all — both show the bare default (`hidepid=0`, "everyone
can list/read any PID's `/proc` dir, subject to normal per-file permission checks"). So every claim
about `hidepid=1/2/4` behavior in this repo is **documented-only**, not practically confirmed by
either box. Neither system is configured as a hardened shared/multi-user host or a `subset=pid`
container, so that whole mount-hardening layer remains theoretical here.

## 5. The real access-control layer that *was* observed: per-file permissions

**Partial/nuance — arguably the most important correction to the docs' framing.** With `hidepid=0`
on both systems, the docs might suggest cross-user `/proc` visibility is wide open. Both live systems
show this isn't true in practice: `/proc/1` (PID 1, root-owned) stays listable (`dr-xr-xr-x root
root`), but reading a privileged file inside it as an unprivileged user (`cat /proc/1/environ`) is
denied outright on **both** systems, identically. This confirms a two-layer model that the docs state
separately (per-file permission bits exist) but don't connect explicitly: with `hidepid` unset,
directory-listing-level privacy isn't the actual defense on either box — the real enforcement point
is per-file permission bits inside each `/proc/pid/` dir, which is a layer independent of and beneath
`hidepid`. An analyst should not assume "no hidepid configured" means "no cross-user protection" —
the per-file gate is present by default regardless.

## 6. `Seccomp` / `NoNewPrivs` status fields

**Match.** Both systems show ordinary interactive/utility processes with `Seccomp: 0` and
`NoNewPrivs: 0` — no sandboxing applied, exactly what the docs predict for an unsandboxed login
shell or plain command. This is a low-information match (neither box happened to run anything
sandboxed at inspection time) but it does confirm the fields read as documented, with no surprises
in format or default value.

## 7. `/proc/pid/fd/` structure and access gate

**Match, plus a real-world nuance about what fds actually look like.** Both systems confirm the
`proc_pid_fd(5)` access model exactly: the `fd/` directory itself is `dr-x------` — even the owning
user gets list+read only, no write, consistent with the ptrace-mode-read gate. Both show the same
symlink shape: fd 0/1/2 for stdio, plus an extra fd pointing at a child process's own `fd/` directory
(a shell-pipeline artifact) on both boxes.

**System-specific-but-expected difference**: locally, fds 1/2 point at real regular files (session
log files); over the Kali SSH session, fds 0/1/2 all point at anonymous `pipe:[inode]` objects. This
isn't a system difference so much as an execution-context difference (local interactive shell vs.
remote SSH-executed command with stdio wired through pipes to the SSH channel) — but it's a good
concrete illustration that `proc_pid_fd(5)`'s claim ("fd symlinks describe whatever kind of object
the descriptor is — file, pipe, or socket") isn't just a hypothetical enumeration; the *same*
descriptor slot (fd 1) is a different underlying kernel object type depending purely on how the
process was launched. A tool that assumes "fd 1 is always a regular file or tty" will be wrong for
any pipelined/remote-executed process.

## 8. `/proc/pid/maps`

**Match.** Both systems show the identical structural pattern the docs describe: the same backing
binary appearing as multiple mapping lines with different permission bits (`r--p`/`r-xp`/`rw-p`) for
its separate ELF segments, and the heap as anonymous `00:00`/inode `0`. No deviation between systems
in pattern — only addresses differ (expected, ASLR), which neither report reproduced since raw
addresses aren't useful as identifying data anyway.

## 9. `/proc/pid/task/` — thread subdirectories

**Match (limited demonstration).** Both live surveys only exercised the single-threaded case
(ordinary shell/utility processes show exactly one `task/` entry matching their own PID), which
matches the doc's claim for that case. Neither practical report demonstrates the multithreaded case
(`link-02-notes.md`'s own "Try it" section has a python3 threading snippet for that, but the two
practical catalogs didn't run it) — so the *multi-entry* thread behavior remains confirmed only by
the docs and the separate link-02 exercise, not by these two system surveys specifically.

## 10. `/proc/net/` and `/proc/sys/` subtrees

**Match at `/proc/net/`; system-specific difference at `/proc/sys/`.** `/proc/net/` top-level entries
matched closely between the two systems (`arp`, `dev`, `dev_mcast`, `dev_snmp6`, `fib_trie`,
`fib_triestat`, `icmp`, `icmp6`, `if_inet6`, `igmp`, `igmp6`, plus Bluetooth entries) — consistent
with the doc's claim that this is a stable, network-namespace-scoped pseudo-file set.

`/proc/sys/` differs: the Kali VM additionally exposes `crypto` and `sunrpc` subtrees that the local
machine doesn't have. Per the practical-kali report, `sunrpc`'s presence implies NFS/RPC client
kernel support is compiled into the VM's kernel, which the local machine's build apparently doesn't
expose the same way — again a kernel-config difference, not a hardening or security-relevant one.
This directly illustrates the theoretical catalog's `proc_sys(5)` claim that `/proc/sys/` subdirectory
membership depends on which subsystems the running kernel actually has compiled in — the docs state
this structurally, but only the two-system comparison actually shows it happening.

## 11. `/proc/version`

**Match (as a non-identifying field), with confirmed system-specific content.** Both systems confirm
the doc's claim that this file is safe to record verbatim — it says nothing about the specific
machine beyond kernel flavor/build. Content differs as expected: local shows an Arch-family
`linux-zen` build (7.1.x series); Kali shows a Debian/Kali-branded kernel with `+kali` suffix and
distinct GCC/binutils versions — confirming these are genuinely separate distro/kernel builds, not
two configurations of the same base image, which is exactly the kind of signal an analyst would use
`/proc/version` for.

## 12. Mount-time hardening (`subset=pid`) and other documented-only areas

**Not observed / environment-dependent.** Beyond `hidepid` (section 4), `subset=pid` container
hardening is entirely undemonstrated — neither system is a container using this option, so nothing
in either practical report confirms or contradicts the theoretical catalog's claim that it hides
`meminfo`/`net/`/`sys/` etc. from a sandboxed process. Likewise, several per-process files the
theoretical catalog documents in depth (`smaps`, `mem`, `syscall`, `wchan`, `auxv`, `attr/`, `ns/`,
`cgroup`, `mountinfo`, `coredump_filter`) were not exercised by either live survey — their existence
and permission model are documented-only in this repo's current state, not yet practically confirmed.

---

## Practical takeaways for a security analyst

**Reliably present, safe to build tooling around** (confirmed identically on two independent
kernel builds):
- The `-r--------` root-only cluster (`kcore`, `kmsg`, `kpage*`, `pagetypeinfo`, `slabinfo`,
  `timer_list`, `vmallocinfo`) and write-only `sysrq-trigger` — a stable kernel-wide policy, not a
  distro choice. Don't expect to read these as a normal user on any mainline-derived kernel.
- The per-file permission gate inside `/proc/pid/*` (e.g. `environ` denied cross-user even with
  `hidepid=0`). This is the layer that's actually doing access control on a default/unhardened box —
  don't assume "no `hidepid` configured" means "no protection between users."
- `fd/` directory access mode (`dr-x------`, owner-only list+read) and the fact that fd targets can
  be files, pipes, *or* sockets depending purely on how the process was launched — a tool that
  hardcodes an assumption about what fd 0/1/2 point to will misclassify pipelined or remotely-executed
  processes.
- `maps` segment-per-permission structure and the `self`/`thread-self` symlink-vs-target ownership
  split (symlink object always `root:root`, target directory user-owned) — both confirmed identical
  across systems, so safe to hardcode into parsing logic.

**Theoretical / config-dependent — don't assume, verify per-target first**:
- `hidepid=1/2/4` and `subset=pid` behavior: fully documented, zero practical confirmation in this
  repo. Before relying on either as a defense you're auditing, or an obstacle you expect to hit,
  check `/proc/mounts` or `/proc/self/mountinfo` on the actual target — this survey's own two boxes
  both turned out to run the wide-open default.
- Presence of specific top-level files/subtrees (`bootconfig`, `config.gz`, `scsi/`, `/proc/sys/
  crypto`, `/proc/sys/sunrpc`) is kernel-build-and-boot-config-dependent, confirmed by direct
  A/B difference between two real systems. Don't write a tool that assumes a fixed top-level
  `/proc` file inventory across all Linux hosts — enumerate what's actually there.
- Multithreaded `task/` behavior, `smaps`/`mem`/`syscall`/`wchan`/`auxv`/`ns/`/`attr/`/`cgroup`/
  `mountinfo` — documented in detail but not exercised on either live box in this repo yet; treat as
  "should work as documented" rather than "confirmed working" until actually tested.

**Real gotchas the official docs don't call out, but two live systems both revealed**:
- The `self`/`thread-self` magic-symlink-object-vs-target ownership split (section 3) — easy to
  misread `ls -ld /proc/self` as "proof `/proc/self` is root-controlled" when it's really just the
  symlink pointer; the actual target directory is user-owned.
- `hidepid=0` (the common default) does *not* mean "no privacy between users" in practice — the
  per-file permission layer beneath it is what's actually enforcing the boundary, and both docs
  catalogs discuss `hidepid` and per-file permissions as separate topics without connecting them as
  a two-layer defense-in-depth pair the way the live systems make obvious.
- `/proc/modules` (and similar "just read the file" rootkit-hunting checks) is trustworthy only
  against unsophisticated threats — a capable LKM rootkit can hook the backing kernel structures and
  simply omit its own entry, so a clean read is evidence of absence only for the low end of the
  threat model, a caveat the theoretical catalog flags as its own analytical note rather than
  something drawn from official docs.

---

## Sanitization check

Re-read both practical source files in full for this synthesis. No real IP address, hostname,
password, or username was present in either — both were already fully genericized (placeholders like
`<local user>`, `<lab VM user>`, `<pid>`, `<child-pid>`, `<inode>` throughout; the Kali report
explicitly states IP/hostname/credentials were omitted at authoring time and only notes password-auth
was used via `expect`, with no actual password value present). Nothing needed to be flagged or
excluded when writing this file, and nothing sensitive was carried forward into it.
