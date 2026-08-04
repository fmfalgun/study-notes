# Link 4 — Exercise: FHS 3.0 Chapter 6 — Operating System Specific Annex (Linux)

Fish primary (this machine's shell); bash/sh forms called out where they differ. All read-only —
nothing here modifies system state.

---

### 1. Confirm the usrmerge reality before anything else

```sh
for d in /bin /sbin /usr/sbin /lib; do echo -n "$d -> "; readlink -f "$d"; done
```
Note every target — this single fact reframes every `/bin`-vs-`/sbin` claim in FHS chapter 6 for
this specific machine. Keep this output in mind for steps 3, 7, and 9.

### 2. `/` — kernel naming convention

```sh
ls -la / | grep -i vmlinu
ls -la /boot | grep -i vmlinu
file /boot/vmlinuz-* 2>/dev/null | head -1
```
Confirm the kernel isn't actually in `/` on this machine (expected — it moved to `/boot` on
essentially every modern distro) and that its name still follows the `vmlinuz` convention FHS
recommends.

### 3. `/bin` — `setserial`

```sh
which setserial 2>&1
readlink -f /bin
```
Explain out loud: given step 1's usrmerge result, what does "`setserial` should be in `/bin`"
actually cash out to as a real filesystem path on this machine?

### 4. `/dev` — the three required devices, tested for real behavior (not just existence)

```fish
ls -la /dev/null /dev/zero /dev/tty
stat -c '%A %F' /dev/null /dev/zero /dev/tty

echo "discarded" > /dev/null
echo "write to /dev/null exit status: $status"     # fish; bash/sh: $?

head -c 5 /dev/zero | xxd                          # confirm 5 zero bytes, nothing else

cat < /dev/null
echo "cat read from /dev/null and exited immediately (EOF), no hang"
```
For `/dev/tty`, confirm it reaches your terminal even when stdout is redirected elsewhere:
```sh
echo "you should see this on-screen, not in the file" > /dev/tty > /tmp/fhs-ex4-discard.txt
rm -f /tmp/fhs-ex4-discard.txt
```

### 5. `/etc` — `lilo.conf` (expected absent)

```sh
ls -la /etc/lilo.conf 2>&1
bootctl status 2>/dev/null | head -3
```
Confirm your actual bootloader (`bootctl` for systemd-boot, or check `/etc/default/grub` for
GRUB) — name it, and explain why LILO's config file is a dead reference on this machine.

### 6. `/proc` — cross-reference to link 2

```sh
grep " /proc " /proc/mounts
cat /proc/loadavg
```
This is deliberately the same check as link 2's exercise step 1 — confirms this FHS point and
`proc(5)` describe the same real thing from two different documents.

### 7. `/sys` and `/sbin` static-binary rationale together

```sh
grep " /sys " /proc/mounts
ls /sys/class/ | head -5
ls /sys/block/

readlink -f /sbin
which ldconfig sln kbdrate 2>&1
```
```fish
file (which sln) 2>/dev/null
ldd (which sln) 2>&1
```
bash/sh: use `$(which sln)` in place of `(which sln)` in both lines above.

Confirm `sln` really is statically linked (`ldd` should refuse to report dynamic dependencies —
that's the whole point of it being a disaster-recovery tool).

### 8. `/usr/include` — glibc-vs-not-glibc conditional

```sh
ldd --version | head -1
ls -ld /usr/include/asm /usr/include/linux 2>&1
```
```fish
gcc --version 2>&1 | head -1; or cc --version 2>&1 | head -1
```
bash/sh: `gcc --version 2>&1 | head -1 || cc --version 2>&1 | head -1`

Confirm: are `/usr/include/asm`/`/usr/include/linux` real directories or symlinks on this
machine? Given the `ldd --version` output (glibc or not), does FHS's symlink requirement even
apply here? State the reasoning, not just the observation.

### 9. `/usr/src` — kernel source location, by distro

Arch:
```sh
ls -ld /usr/src 2>&1
ls /usr/src/ 2>&1 | head
pacman -Qi linux-headers 2>/dev/null | grep -E '^(Name|Version)'
```
Debian:
```sh
ls -ld /usr/src 2>&1
ls /usr/src/ 2>&1 | head
dpkg -l "linux-headers-$(uname -r)" 2>/dev/null | tail -1
```

### 10. `/var/spool/cron` — optional, presence-dependent

```sh
ls -ld /var/spool/cron 2>&1
ls -ld /var/spool 2>&1
systemctl list-timers 2>/dev/null | head -5
which cron crontab atd 2>&1
```
If `/var/spool/cron` doesn't exist, confirm *why* per the notes (optional, only appears once
cron/at are installed and used) rather than treating it as something broken.

### 11. Self-check

1. Name three FHS-6.1 claims on this page that don't hold literally on this specific machine, and
   explain the real-world reason for each (usrmerge, glibc, or "this convention is obsolete").
2. Why does the rationale for `/usr/src/linux/include/` explicitly *not* want kernel headers
   mixed into `/usr/include`?
3. What's the practical difference in purpose between `/proc` and `/sys`, even though both are
   virtual/pseudo filesystems exposing kernel state?
