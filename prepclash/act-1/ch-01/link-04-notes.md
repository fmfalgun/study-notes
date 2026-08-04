# Link 4 — Notes: FHS 3.0 Chapter 6 — Operating System Specific Annex (Linux)

Source: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch06.html
No local man-page equivalent for FHS — fetched directly (this domain isn't reachable via the
standard web-fetch tool, so raw HTML was pulled with `curl` and stripped of tags).

**Structural note**: unlike ch03/ch04/ch05 (which are thin index pages linking out to a real
sub-page per directory), ch06 is short enough to be entirely on one page — all 10 subsections
below are `curl`-verified directly from `ch06.html`, no further fetching needed.

**One fact that changes almost every answer on this machine**: this system (Garuda Linux, Arch
based) is **fully usrmerged** — `/bin`, `/sbin`, and `/usr/sbin` are all symlinks to `/usr/bin`,
and `/lib` is a symlink to `/usr/lib`. FHS predates usrmerge and still talks about `/bin` and
`/sbin` as physically separate directories with their own contents. Every point below that
mentions `/bin`/`/sbin` gets a live "on this machine" callout for that reason — this is one of the
most common real gaps between the written standard and a modern distro.

```sh
for d in /bin /sbin /usr/sbin /lib; do echo -n "$d -> "; readlink -f "$d"; done
```

---

## 6.1. Linux (annex scope)

**Claim**: "This section is for additional requirements and recommendations that only apply to a
specific operating system. The material in this section should never conflict with the base
standard." This annex covers Linux specifically.

**Simple explanation**: the base FHS chapters (3/4/5) are OS-agnostic in principle; this chapter
is where Linux-specific reality (like `/proc`, `/sys`, kernel source conventions) gets bolted on.

## 6.1.1. `/` — Root directory

**Claim**: if the kernel is located in `/`, the recommended names are `vmlinux` or `vmlinuz`
(source: recent Linux kernel source packages at time of writing).

**Simple explanation**: `vmlinuz` = compressed kernel image; the trailing `z` is the convention
for "gzip-compressed." Most distros don't actually keep the kernel in `/` anymore — it moved to
`/boot`.

**Try it**:
```sh
ls -la / | grep -i vmlinu
ls -la /boot | grep -i vmlinu   # this is where you'll actually find it on most modern distros
file /boot/vmlinuz-* 2>/dev/null | head -1
```

## 6.1.2. `/bin` — Essential user command binaries

**Claim**: Linux systems that need it place `setserial` in `/bin` as an additional file beyond
the base FHS `/bin` list.

**Simple explanation**: `setserial` configures serial ports — a legacy tool, rarely needed on a
modern laptop/desktop with no real RS-232 hardware.

**Try it**:
```sh
which setserial 2>&1                     # may well be absent — that's expected on modern hardware
readlink -f /bin                          # on this machine: usrmerged, so /bin is really /usr/bin
ls -la /usr/bin/setserial 2>&1
```

## 6.1.3. `/dev` — Devices and special files

**Claim**: these three devices **must** exist under `/dev`:
- `/dev/null` — all writes discarded; reads return EOF immediately.
- `/dev/zero` — writes discarded; reads return as many zero bytes as requested.
- `/dev/tty` — synonym for the calling process's controlling terminal; behaves as if that actual
  terminal device were opened.

Rationale note: earlier FHS versions had stricter `/dev` requirements; other devices may exist,
may be symlinks into `/dev` or a subdirectory, and there's no requirement on major/minor numbers.

**Simple explanation**: these three are the most-relied-upon "fake" devices in all of Unix
scripting — `/dev/null` to discard output, `/dev/zero` to generate zero-filled data (disk wiping,
padding files), `/dev/tty` to always reach the user's terminal regardless of stdin/stdout
redirection.

**Try it**:
```sh
ls -la /dev/null /dev/zero /dev/tty
stat -c '%A %F major=%t minor=%T' /dev/null /dev/zero /dev/tty   # confirm "character special file"

echo "discarded" > /dev/null; echo "exit code: $status"          # fish: $status ; bash: $?
head -c 5 /dev/zero | xxd                                        # 5 zero bytes
cat < /dev/null; echo "read returned immediately (EOF)"

# /dev/tty always reaches your terminal even if stdout is redirected elsewhere:
echo "this goes to the terminal, not the file" > /dev/tty > /tmp/fhs-test-discard.txt
rm -f /tmp/fhs-test-discard.txt
```

## 6.1.4. `/etc` — Host-specific system configuration

**Claim**: Linux systems that need it place `lilo.conf` in `/etc` as an additional file.

**Simple explanation**: LILO (Linux Loader) is the predecessor to GRUB — almost nothing uses it
today, so this file legitimately won't exist on a modern system. Good example of FHS text that's
now historical rather than prescriptive.

**Try it**:
```sh
ls -la /etc/lilo.conf 2>&1        # expected: not found, on any modern GRUB/systemd-boot system
bootctl status 2>/dev/null | head -3 || cat /etc/default/grub 2>/dev/null | head -3
```

## 6.1.5. `/proc` — Kernel and process information virtual filesystem

**Claim**: `/proc` is "the de-facto standard Linux method for handling process and system
information," preferred over `/dev/kmem` and similar older methods, strongly encouraged for
process/kernel/memory info.

**Simple explanation**: you already did a deep dive on exactly this in link 2 (`proc(5)`) — this
FHS point is just the standards document formally blessing what you already explored hands-on.

**Try it**:
```sh
grep " /proc " /proc/mounts
cat /proc/loadavg
```

## 6.1.6. `/sbin` — Essential system binaries

**Claim**: filesystem-maintenance and boot-loader-management commands go in `/sbin`. Optional
static binaries: `ldconfig`, `sln` (static `ln`), `ssync` (static `sync`) — useful when dynamic
linking itself is broken (e.g. you deleted a critical shared library and need a statically-linked
tool to fix it without depending on the broken linker). Optional misc: `kbdrate` (fix unusable
keyboard repeat rate), `ctrlaltdel` (disable the kernel's default instant-reboot-on-Ctrl-Alt-Del
before mounting root read-write).

**Simple explanation**: the whole "keep static binaries around" idea is a disaster-recovery
pattern — if `/lib`'s dynamic libraries are broken, *every* dynamically-linked binary (including
`ls`, `ln`, `sync`) stops working; a statically-linked emergency tool has no such dependency.

**Try it** (fish; on this machine `/sbin` is a usrmerge symlink to `/usr/bin`, so these all live in
one merged directory rather than a separate `/sbin`):
```fish
readlink -f /sbin
which ldconfig sln kbdrate 2>&1
file (which sln) 2>/dev/null       # check if it's actually statically linked
ldd (which sln) 2>&1               # "not a dynamic executable" = static
```
bash/sh: replace `(which sln)` with `$(which sln)` on both lines, rest identical.

## 6.1.7. `/sys` — Kernel and system information virtual filesystem

**Claim**: `sysfs` exposes info about devices/drivers/kernel features; its structure is determined
by the specific kernel in use and otherwise unspecified (i.e. FHS deliberately does not pin down
`/sys`'s internal layout).

**Simple explanation**: `/proc` is process/system-stat-oriented; `/sys` is device/driver-model
oriented (this is where `udev` and kernel driver code publish structured device info). FHS
punting on `/sys`'s internal structure is honest — it genuinely varies by kernel version/config.

**Try it**:
```sh
grep " /sys " /proc/mounts
ls /sys/class/     # device classes exposed by currently loaded drivers — differs machine to machine
ls /sys/block/     # block devices, e.g. your actual disks
```

## 6.1.8. `/usr/include` — Header files included by C programs

**Claim**: `/usr/include/asm` → `/usr/src/linux/include/asm-<arch>` and `/usr/include/linux` →
`/usr/src/linux/include/linux` are **required symlinks**, but *only* if a C/C++ compiler is
installed **and** the system is not glibc-based.

**Simple explanation**: this is glibc-vs-not-glibc conditional text left over from an era with
real libc diversity on Linux. Virtually every mainstream desktop distro today (including this one)
is glibc-based, so this specific symlink requirement doesn't apply here — a good concrete example
of reading FHS's conditionals carefully instead of treating every "must" as universal.

**Try it**:
```sh
ldd --version | head -1                        # confirms glibc, and its version
ls -ld /usr/include/asm /usr/include/linux 2>&1 # these exist here as real directories/headers,
                                                 # not as the symlinks FHS describes for non-glibc systems
gcc --version 2>&1 | head -1; or cc --version 2>&1 | head -1
```

## 6.1.9. `/usr/src` — Source code

**Claim**: for glibc-based systems, FHS gives no specific guidance for this directory. For older
non-glibc systems: only the Linux kernel source belongs at a fixed location, `/usr/src/linux`
(may be a symlink to the actual kernel source tree); if a compiler is installed without the full
kernel source, the kernel's `asm-<arch>`/`linux` include dirs must still exist there. Rationale:
keeps kernel headers out of `/usr/include` so upgrading kernel versions doesn't silently break the
compiler's view of kernel headers.

**Simple explanation**: another "doesn't apply to modern glibc systems" point — today, kernel
headers for building modules come from a separate `linux-headers`-style package, not a
`/usr/src/linux` convention.

**Try it** — Arch:
```sh
ls -ld /usr/src 2>&1
ls /usr/src/ 2>&1 | head    # often empty or holds DKMS module sources on modern distros, not raw kernel source
pacman -Qi linux-headers 2>/dev/null | grep -E '^(Name|Version)'
```
Debian:
```sh
ls -ld /usr/src 2>&1
ls /usr/src/ 2>&1 | head
dpkg -l "linux-headers-$(uname -r)" 2>/dev/null | tail -1
```

## 6.1.10. `/var/spool/cron` — cron and at jobs

**Claim**: this directory holds variable data for the `cron` and `at` programs.

**Simple explanation**: per-user crontabs and pending `at` jobs live here on systems using
classic cron; note this is entirely optional — it only exists if cron/at are actually installed
and have been used at least once.

**Try it**:
```sh
ls -ld /var/spool/cron 2>&1    # not found here = no cron daemon installed, which is normal/expected
ls -ld /var/spool 2>&1         # the parent still exists as a general "spool" area
systemctl list-timers 2>/dev/null | head -5   # systemd-based distros often use timers instead of cron
which cron crontab atd 2>&1
```
