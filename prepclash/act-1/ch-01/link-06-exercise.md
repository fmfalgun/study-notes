# Link 6 — Exercise: FHS 3.0 Chapter 3 — The Root Filesystem

Fish primary; bash/sh forms called out where they differ. All read-only — this is the biggest
chapter (17 sub-sections), so work through it in order rather than skipping around.

---

### 1. The full required + optional root-level inventory in one pass

```sh
for d in bin boot dev etc lib media mnt opt run sbin srv tmp usr var; do
  echo -n "/$d -> "; readlink -f /$d 2>&1
done
for d in home lib32 lib64 root; do echo -n "/$d -> "; readlink -f /$d 2>&1; done
```
Build a two-column list from the output: "exists as expected" vs. "missing/unexpected" (e.g.
`/media`). For each gap, form a hypothesis before moving on — you'll test some of them directly in
later steps (`/media` in step 8).

### 2. `/bin` — every required command, checked programmatically, not by eye

```sh
find /bin -maxdepth 1 -type d | grep -v '^/bin$'
for c in cat chgrp chmod chown cp date dd df dmesg echo false hostname kill ln login ls mkdir \
         mknod more mount mv ps pwd rm rmdir sed sh stty su sync true umount uname; do
  which $c >/dev/null 2>&1 || echo "MISSING: $c"
done
readlink -f /bin/sh
which "[" test
```
A clean run prints *nothing* from the `for` loop — that's success, not the script doing nothing.
Confirm `/bin/sh` really does resolve to a real POSIX-compatible shell binary, not a broken link.

### 3. `/boot` and the kernel-location rule

```sh
ls /boot | grep -iE 'vmlinu'
file /boot/vmlinuz-* 2>/dev/null | head -1
```
Confirm the kernel lives in `/boot`, not `/` — consistent with 3.5's "kernel must be in `/` or
`/boot`" (either is compliant; `/boot` is what you'll find on virtually every modern system).

### 4. `/dev` — `MAKEDEV` (expect absent) and confirm *why* that's fine

```sh
ls -la /dev/MAKEDEV /dev/MAKEDEV.local 2>&1
cat /proc/mounts | grep ' /dev '
```
`/dev` mounted as `devtmpfs` is the modern replacement mechanism — explain in one sentence why a
kernel-populated `devtmpfs` makes a manual `MAKEDEV` script largely unnecessary.

### 5. `/etc` — no-binaries rule, required/optional structure, and the `mtab` exception

```sh
find /etc -maxdepth 1 -type f -perm -u+x 2>/dev/null | xargs -r file | grep -v text
ls -ld /etc/opt /etc/X11 /etc/sgml /etc/xml 2>&1
ls /etc/fstab /etc/passwd /etc/hosts /etc/resolv.conf /etc/shells 2>&1
readlink -f /etc/mtab 2>&1
```
The first command should print nothing (no real ELF binaries directly under `/etc`). Confirm
`/etc/mtab`'s actual form on this system and connect it back to the notes' point about the
`/proc/mounts` symlink sidestepping the "must be static" exception entirely.

### 6. `/home` — query, don't hardcode

```sh
ls -ld /home; ls /home
```
```fish
getent passwd (whoami)
echo $XDG_CONFIG_HOME $XDG_DATA_HOME $XDG_CACHE_HOME
```
bash/sh: `getent passwd $USER`.
```sh
ls -la ~ | grep '^d\.' | head -5
```
Pick two dot-directories from the last command's output and identify which application each
belongs to.

### 7. `/lib` and `/lib<qual>` together

```sh
ls -la /lib/libc.so* 2>&1 | head -3
readlink -f /lib/cpp 2>&1
ls -ld /lib/modules 2>&1
ls /lib/modules 2>/dev/null
readlink -f /lib32 /lib64
```
Confirm: does `uname -r`'s output match one of the subdirectory names under `/lib/modules`?

### 8. `/media` vs `/mnt` vs the real auto-mount location — resolve step 1's gap

```sh
ls -ld /media /mnt
```
```fish
ls /run/media/(whoami) 2>&1
```
bash/sh: `ls /run/media/$USER 2>&1`.

Plug in a USB drive (or skip this physical step and just reason about it) — where would it
actually mount on this machine, `/media/...` or `/run/media/.../...`? Explain the practical
difference in purpose between `/media` (removable-media mount points) and `/mnt` (admin's ad hoc
temporary mounts) even though both are just "places to mount something."

### 9. `/opt` — inventory what's actually installed, and its `/etc/opt`+`/var/opt` counterparts

```sh
ls -ld /opt; ls /opt 2>/dev/null
ls -ld /etc/opt/* /var/opt/* 2>/dev/null
```
Pick one entry under `/opt` and check whether it has a matching `/etc/opt/<name>` and/or
`/var/opt/<name>` — most won't, which is itself informative about how loosely this convention is
actually followed in practice.

### 10. `/root`

```sh
ls -ld /root
sudo -n getent passwd root 2>/dev/null | cut -d: -f6
```
(Second line needs passwordless sudo — skip gracefully if unavailable, that's expected on most
personal machines.)

### 11. `/run` — PID file format, live

```sh
ls -ld /run /var/run
readlink -f /var/run
findmnt /run
ls /run/*.pid 2>/dev/null
```
For any `.pid` file you can actually read, inspect its raw bytes and confirm the format the notes
describe (ASCII decimal PID, then a single newline byte, nothing else):
```sh
cat /run/some-example.pid | xxd
```
(replace `some-example.pid` with a real filename from the `ls` above — if none are readable as a
normal user, explain why that's expected given `/run`'s security note about not being
world-writable/readable for sensitive entries).

### 12. `/sbin` — no-subdirectories, required + optional commands

```sh
find /sbin -maxdepth 1 -type d | grep -v '^/sbin$'
which shutdown
for c in fdisk fsck halt ifconfig init mkswap reboot route swapon swapoff; do which $c 2>&1; done
```
Of the optional list, which are present vs. absent on this machine, and can you guess why (e.g.
`ifconfig`/`route` are legacy `net-tools`, commonly replaced by `ip` on modern distros — check
`which ip` too)?

### 13. `/srv`

```sh
ls -ld /srv
ls /srv 2>/dev/null
```
Confirm it exists (required, even if empty) — this is a good example of "the directory itself is
mandatory; its contents are not."

### 14. `/tmp` — implementation choice vs. spec requirement

```sh
ls -ld /tmp
findmnt /tmp
stat -c '%A' /tmp
```
The sticky bit (`t` in the permission string) isn't something FHS itself mandates in this
chapter — where do you think that convention actually comes from? (Hint: think about what
`/tmp`'s world-writability combined with multi-user access would mean *without* it.)

### 15. Self-check

1. State, in your own words, the actual purpose-based distinction FHS draws between `/opt`,
   `/usr/local`, and `/srv` — three different "extra software/data" locations that are easy to
   conflate.
2. Why does the standard explicitly forbid installer programs from using `/mnt`?
3. Name the two directories in this chapter whose defining property is "must contain **no**
   subdirectories," and explain what real operational problem that rule prevents.
4. `/run` supersedes `/var/run` for new code, but `/var/run` still has to work. What's the
   mechanism on this machine that makes both paths resolve to the same data?
