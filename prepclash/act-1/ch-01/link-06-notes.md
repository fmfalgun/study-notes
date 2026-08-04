# Link 6 — Notes: FHS 3.0 Chapter 3 — The Root Filesystem

Source: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch03.html (index page — real content in
`ch03s02.html` through `ch03s18.html`, all fetched via `curl`; no local man-page equivalent for
FHS).

Same usrmerge caveat as links 4-5: `/bin`, `/sbin` → `/usr/bin`; `/lib` → `/usr/lib` on this
machine. Confirmed again below per-section where it changes what a claim actually means here.

---

## 3.2. Requirements — the 14 mandatory root-level entries

**Claim**: `bin`, `boot`, `dev`, `etc`, `lib`, `media`, `mnt`, `opt`, `run`, `sbin`, `srv`, `tmp`,
`usr`, `var` (or symlinks) required directly under `/`.

**Try it**:
```sh
for d in bin boot dev etc lib media mnt opt run sbin srv tmp usr var; do
  echo -n "/$d -> "; readlink -f /$d 2>&1
done
```
**Real-world gap to flag**: if `/media` came back missing on your system, that's real — modern
desktop auto-mount daemons (`udisks2`/`gvfs`) commonly mount removable media under
`/run/media/<user>/...` instead, bypassing `/media` entirely. Worth noting as exactly the kind of
practical drift the standard can't force distros to avoid.

## 3.3. Specific Options — the 3 conditional root-level entries

**Claim**: `home`, `lib<qual>`, `root` required only if that subsystem is installed.

**Try it**:
```sh
for d in home lib32 lib64 root; do echo -n "/$d -> "; readlink -f /$d 2>&1; done
```

## 3.4. `/bin` — Essential user command binaries

**Claim**: commands needed even with no other filesystem mounted (e.g. single-user mode), or used
indirectly by scripts. **Requirement**: no subdirectories; ~28 named commands required
(`cat`,`chgrp`,`chmod`,`chown`,`cp`,`date`,`dd`,`df`,`dmesg`,`echo`,`false`,`hostname`,`kill`,
`ln`,`login`,`ls`,`mkdir`,`mknod`,`more`,`mount`,`mv`,`ps`,`pwd`,`rm`,`rmdir`,`sed`,`sh`,`stty`,
`su`,`sync`,`true`,`umount`,`uname`); if `/bin/sh` isn't itself POSIX-compliant, it must link to
the real POSIX shell; `[` and `test` must be in `/bin` or `/usr/bin`. Optional (if subsystem
installed): `csh`,`ed`,`tar`,`cpio`,`gzip`,`gunzip`,`zcat`,`netstat`,`ping` — rationale: these
exist specifically to make system *restoration* from the root partition possible.

**Try it**:
```sh
find /bin -maxdepth 1 -type d | grep -v '^/bin$'          # must be empty
for c in cat chgrp chmod chown cp date dd df dmesg echo false hostname kill ln login ls mkdir \
         mknod more mount mv ps pwd rm rmdir sed sh stty su sync true umount uname; do
  which $c >/dev/null 2>&1 || echo "MISSING: $c"
done
readlink -f /bin/sh              # confirm it resolves to a real POSIX shell
which "[" test
for c in csh ed tar cpio gzip gunzip zcat netstat ping; do which $c >/dev/null 2>&1 || echo "absent (optional): $c"; done
```

## 3.5. `/boot` — Static files of the boot loader

**Claim**: everything needed for boot except config not needed at boot time (→ `/etc`) and the
map installer; may include saved MBR/sector maps. Boot-arranging programs → `/sbin`. Kernel must
be in `/` or `/boot`.

**Try it**:
```sh
ls /boot | grep -iE 'vmlinu'
ls /boot | head -10
```

## 3.6. `/dev` — Device files

**Claim**: location of special/device files. If devices might need manual creation, `/dev` must
contain a `MAKEDEV` command (plus optional `MAKEDEV.local`) capable of creating any device that
could exist on the system.

**Try it**:
```sh
ls -la /dev/MAKEDEV /dev/MAKEDEV.local 2>&1
```
**Real-world note**: expect this missing on any modern system — `MAKEDEV` is a relic of
statically-populated `/dev`; `devtmpfs` + `udev`/`eudev` auto-populate `/dev` from the kernel now,
making manual device-node creation essentially obsolete.

## 3.7. `/etc` — Host-specific system configuration

**Claim**: configuration files only — **must contain no binaries** (native ELF executables;
human-readable executable *scripts* are explicitly fine, e.g. init scripts). Required: `etc/opt`.
Optional dirs: `X11`, `sgml`, `xml`. ~30 optional named config files listed (`fstab`, `passwd`,
`hosts`, `resolv.conf`, `inittab`, `motd`, `services`, `shells`, etc.) — `mtab` is explicitly
grandfathered in as an exception to the "static" rule (historically dynamic; on some Linux systems
it's a symlink to `/proc/mounts` instead, which sidesteps the exception entirely).
`/etc/opt/<subdir>` holds host-specific config for the matching `/opt/<subdir>` package, no
imposed internal structure. `/etc/X11` holds X11 host-specific config (`xorg.conf`, `Xmodmap`) —
exists specifically so X can be configured even with `/usr` mounted read-only.

**Try it**:
```sh
find /etc -maxdepth 1 -type f -perm -u+x 2>/dev/null | xargs -r file | grep -v text
                                                    # look for actual ELF binaries directly in /etc (should be none)
ls -ld /etc/opt /etc/X11 /etc/sgml /etc/xml 2>&1
ls /etc/fstab /etc/passwd /etc/hosts /etc/resolv.conf /etc/shells 2>&1
readlink -f /etc/mtab 2>&1                         # common modern form: symlink to /proc/self/mounts or /proc/mounts
```

## 3.8. `/home` — User home directories (optional)

**Claim**: site-specific, no program should hardcode a home-directory location — query it (e.g.
via `getpwent`/`getpwnam`, not by parsing `/etc/passwd` directly, since accounts may come from
NIS/LDAP). Small systems: flat `/home/<user>`; large/NFS-shared systems may subdivide
(`/home/staff`, `/home/guests`). Per-app config files are "dot files"/"dot directories". Distros
may layer XDG Base Directory-spec hierarchies underneath home directories.

**Try it**:
```sh
ls -ld /home; ls /home
getent passwd $USER 2>/dev/null; or getent passwd (whoami)   # fish
echo $XDG_CONFIG_HOME $XDG_DATA_HOME $XDG_CACHE_HOME          # XDG dirs layered under $HOME, per the notes
ls -la ~ | grep '^d\.' | head -5    # dot-directories in your own home
```
bash/sh: `getent passwd $USER` for the getent line.

## 3.9. `/lib` — Essential shared libraries and kernel modules

**Claim**: only shared libs needed to boot and run `/bin`+`/sbin` binaries — libraries needed
*only* by `/usr` binaries must NOT be here. At least one `libc.so.*` and one `ld*` (loader)
required. If a C preprocessor is installed, `/lib/cpp` must reference it (historical). Optional:
`modules` (loadable kernel modules).

**Try it**:
```sh
ls -la /lib/libc.so* 2>&1 | head -3
readlink -f /lib/cpp 2>&1
ls -ld /lib/modules 2>&1
ls /lib/modules 2>/dev/null       # one subdir per installed kernel version
```

## 3.10. `/lib<qual>` — Alternate format essential shared libraries (optional)

**Claim**: same content rules as `/lib` for an alternate binary format (commonly 32/64-bit
coexistence — `/lib32`/`/lib64`, with `/lib` symlinked to whichever is primary), except
`<qual>/cpp` isn't required.

**Try it**:
```sh
readlink -f /lib32 /lib64
ls -ld /lib32 2>&1
```

## 3.11. `/media` — Mount point for removable media

**Claim**: subdirectories here are mount points for removable media (floppy/cdrom/zip — dated
examples, concept generalizes to any removable media). Rationale explicitly rejects the older
`/cdrom`/`/mnt`/`/mnt/cdrom` conventions to avoid root-directory sprawl. Optional named
subdirs: `floppy`,`cdrom`,`cdrecorder`,`zip`. Multiple devices of one type: append a digit
(`cdrom0`, `cdrom1`), but the unqualified name must still exist too.

**Try it**:
```sh
ls -ld /media 2>&1
ls /media 2>/dev/null
ls /run/media/$USER 2>&1; or ls /run/media/(whoami) 2>&1   # the actual modern auto-mount location
```
bash/sh: `ls /run/media/$USER 2>&1` for the last line.

## 3.12. `/mnt` — Mount point for a temporarily mounted filesystem

**Claim**: for the *administrator's* ad hoc temporary mounts — content is a local matter, must not
affect how any program runs. Installers must **never** use `/mnt` — they need their own temp dir.

**Simple explanation**: `/media` = removable consumer media (semi-permanent, semi-automatic);
`/mnt` = "I, the admin, am mounting something by hand right now for a specific task." Different
purposes despite looking similar.

**Try it**:
```sh
ls -ld /mnt
ls /mnt 2>/dev/null
```

## 3.13. `/opt` — Add-on application software packages

**Claim**: static package files go in `/opt/<package>` or `/opt/<provider>` (provider = LANANA-
registered name). `/opt/{bin,doc,include,info,lib,man}` are reserved for the *local admin*, not
packages (packages may offer front-end files for the admin to link in, but must work without
them). User-invoked programs → `/opt/<package>/bin`; man pages →
`/opt/<package>/share/man` (same substructure as `/usr/share/man`). Variable data → `/var/opt`;
host config → `/etc/opt`. No other package files allowed outside `/opt`+`/var/opt`+`/etc/opt`
except where the filesystem forces a fixed location (e.g. lock files in `/var/lock`, devices in
`/dev`).

**Try it**:
```sh
ls -ld /opt
ls /opt 2>/dev/null
ls -ld /etc/opt/* /var/opt/* 2>/dev/null   # matching /etc/opt and /var/opt entries for anything under /opt
```
**Real-world note**: package names actually found under `/opt` on a typical desktop (browser
vendor bundles, proprietary drivers) rarely follow strict LANANA registration — a good example of
a "must" that's aspirational in practice, not enforced by anything technical.

## 3.14. `/root` — Home directory for the root user (optional)

**Claim**: recommended default, not mandated exact path; if root's home isn't on the root
partition, it must default to `/` if unreachable. Recommendation (not requirement): don't clutter
it with app subdirectories/mail — forward admin-role mail elsewhere instead.

**Try it**:
```sh
ls -ld /root
sudo -n getent passwd root 2>/dev/null | cut -d: -f6   # root's actual configured home dir field
```

## 3.15. `/run` — Run-time variable data

**Claim**: boot-since data, must be cleared at boot start. Historically `/var/run`'s job;
`/var/run` still works for back-compat but new code should target `/run` directly. PID files:
`<program-name>.pid`, content = ASCII decimal PID + newline, readers should tolerate whitespace/
leading zeros/no-trailing-newline. Transient Unix-domain sockets also belong here. Security note:
`/run` itself should not be world-writable; per-user subdirs only writable by their owner.

**Try it**:
```sh
ls -ld /run /var/run
readlink -f /var/run              # confirm the back-compat symlink into /run
findmnt /run                      # confirm it's typically its own tmpfs — cleared on every boot by construction
ls /run/*.pid 2>/dev/null | head -3
cat /run/*.pid 2>/dev/null | head -1 | xxd | head -1   # eyeball: decimal digits + trailing newline byte (0a)
stat -c '%A' /run                 # confirm not world-writable
```

## 3.16. `/sbin` — System binaries

**Claim**: boot/restore/recover/repair-critical admin binaries (beyond `/bin`) go in `/sbin`
specifically — `/usr/sbin` is for admin programs only needed once `/usr` is confirmed mounted;
`/usr/local/sbin` for locally-installed admin tools. The `/bin`-vs-`/sbin` split is explicitly
**not** a security boundary (rationale explicitly disclaims that) — it's "does an ordinary user
ever run this directly," full stop. **Requirement**: no subdirectories; `shutdown` required.
Optional: `fastboot`,`fasthalt`,`fdisk`,`fsck`,`fsck.*`,`getty`,`halt`,`ifconfig`,`init`,`mkfs`,
`mkfs.*`,`mkswap`,`reboot`,`route`,`swapon`,`swapoff`,`update`.

**Try it**:
```sh
find /sbin -maxdepth 1 -type d | grep -v '^/sbin$'
which shutdown
for c in fdisk fsck halt ifconfig init mkswap reboot route swapon swapoff; do which $c 2>&1; done
stat -c '%A %U' /sbin/shutdown 2>/dev/null; or stat -c '%A %U' (which shutdown)
```
bash/sh: `stat -c '%A %U' "$(which shutdown)"` for the last line.

## 3.17. `/srv` — Data for services provided by this system

**Claim**: site-specific data *served by* this system (as opposed to `/var/lib`, for data whose
internal structure isn't exposed to consumers, or a user's home dir, for single-user-relevant
data). Internal naming under `/srv` is deliberately unspecified — common patterns: by-protocol
(`ftp`,`rsync`,`www`,`cvs`) or by-context (`/srv/physics/www`). Programs must never assume a
specific `/srv` layout exists. `/srv` itself should always exist on an FHS-compliant system even
if empty. Distros must not silently delete admin-placed files here.

**Try it**:
```sh
ls -ld /srv
ls /srv 2>/dev/null
```

## 3.18. `/tmp` — Temporary files

**Claim**: available for any program needing temp files; programs must **not** assume anything
in `/tmp` survives between invocations. FHS doesn't mandate clearing on boot (out of scope, admin
decision) but recommends it based on historical common practice.

**Try it**:
```sh
ls -ld /tmp
findmnt /tmp                     # common modern implementation choice: tmpfs (RAM-backed, cleared every boot)
stat -c '%A' /tmp                # sticky bit (t) expected — prevents users deleting each other's temp files
```
