# Link 7 — Notes: FHS 3.0 Chapter 5 — The `/var` Hierarchy

Source: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch05.html (index page — real content in
`ch05s02.html` through `ch05s16.html`, all fetched via `curl`; no local man-page equivalent).

---

## 5.2. Requirements — the 9 mandatory `/var` entries, plus 4 reserved names

**Claim**: `cache`, `lib`, `local`, `lock`, `log`, `opt`, `run`, `spool`, `tmp` required. Reserved
(must never be repurposed by a new application, for historical/local-practice reasons):
`/var/backups`, `/var/cron`, `/var/msgs`, `/var/preserve`.

**Try it**:
```sh
for d in cache lib local lock log opt run spool tmp; do
  echo -n "/var/$d -> "; readlink -f /var/$d 2>&1
done
for d in backups cron msgs preserve; do ls -ld /var/$d 2>&1; done   # reserved names — expect absent
```

## 5.3. Specific Options — the 5 conditional entries

**Claim**: `account`, `crash`, `games`, `mail`, `yp` — each only if that subsystem is installed.

**Try it**:
```sh
for d in account crash games mail yp; do echo -n "/var/$d -> "; readlink -f /var/$d 2>&1; done
```

## 5.4. `/var/account` — Process accounting logs (optional)

**Claim**: active process-accounting log + composite usage data, as consumed by `lastcomm`/`sa`.

**Try it**:
```sh
ls -ld /var/account 2>&1
which lastcomm sa 2>&1     # part of the (often not installed) acct/psacct package
```

## 5.5. `/var/cache` — Application cache data

**Claim**: regeneratable, locally-computed cache data — unlike `/var/spool`, deleting it loses no
real work, just recomputation time. Must survive reboots and between app invocations; expiry
policy is app/admin-defined; the app must always tolerate the cache being manually wiped (e.g.
under disk pressure). Optional named subdirs: `fonts` (dynamically generated, e.g. by
`mktexpk`), `man` (formatted man-page cache — specifically for read-only `/usr` setups; sites with
writable `/usr` may skip this and format in place instead), `www` (proxy/cache data),
`<package>`.

**Try it**:
```sh
ls /var/cache 2>&1
ls -ld /var/cache/fonts /var/cache/man /var/cache/www 2>&1
du -sh /var/cache/* 2>/dev/null | sort -rh | head -5   # biggest cache consumers on this machine
```

## 5.6. `/var/crash` — System crash dumps (optional)

**Claim**: holds system crash dumps. At the time FHS 3.0 was written, Linux itself didn't support
this (other FHS-compliant OSes might).

**Try it**:
```sh
ls -ld /var/crash 2>&1
which kdump kdumpctl 2>&1     # the modern Linux mechanism this concept maps onto, if installed
```

## 5.7. `/var/games` — Variable game data (optional)

**Claim**: *variable* game data (scores, saves) only — static game data (help text, levels) stays
in `/usr/share/games`. Given its own top-level hierarchy (rather than nesting under `/var/lib`, as
in FHS 1.2) specifically so backup/permission/disk-usage policy can differ, and to match
traditional BSD placement.

**Try it**:
```sh
ls -ld /var/games 2>&1
ls -ld /usr/share/games 2>&1
```

## 5.8. `/var/lib` — Variable state information

**Claim**: per-host state that programs modify while running — must remain valid across a reboot,
must **not** be something a user needs to hand-edit for configuration, and its internal file
layout must not be something regular users rely on (if the structure itself needs exposing →
that's `/srv`'s job instead, not `/var/lib`'s). Every app must use its own subdirectory; the one
required subdirectory is `misc` (state files not warranting their own subdir). Optional named
subdirs: `<editor>` (crash-recovery files, e.g. `emacs`/`vi`-clone lock/backup state),
`<pkgtool>`, `<package>`, `color` (dynamically-installed ICC profiles, same layout rules as
`/usr/share/color`), `hwclock` (holds `adjtime` — moved here from `/etc/adjtime` in FHS 2.1
specifically because `hwclock` itself writes it, which doesn't belong under `/etc`).

**Try it**:
```sh
ls -ld /var/lib/misc                                    # required
ls /var/lib | head -15                                  # the <package>-named subdirs in practice
ls -ld /var/lib/color /var/lib/hwclock 2>&1              # optional — likely absent unless those subsystems are used
cat /var/lib/hwclock/adjtime 2>/dev/null; or echo "no adjtime file (RTC handled without it, e.g. NTP-only)"
```
bash/sh: `cat /var/lib/hwclock/adjtime 2>/dev/null || echo "no adjtime file"`.

## 5.9. `/var/lock` — Lock files

**Claim**: shared-resource lock files (device locks especially — historically in
`/usr/spool/locks` or `/usr/spool/uucp`) now live here. Naming: `LCK..<devicebasename>` (e.g.
`LCK..ttyS0` for `/dev/ttyS0`). Format: HDB UUCP lock format — PID as a **10-byte, space-padded
ASCII decimal number** plus trailing newline (so PID 1230 → 6 spaces + "1230" + newline, 11 bytes
total). Lock files must be world-readable.

**Try it**:
```sh
readlink -f /var/lock             # on this machine: symlinked into /run/lock (tmpfs — cleared every boot, by design)
ls /var/lock 2>&1
```

## 5.10. `/var/log` — Log files and directories

**Claim**: general log destination. Required files (if the subsystem exists): `lastlog` (per-user
last-login record), `messages` (syslogd system messages), `wtmp` (full login/logout history).

**Try it**:
```sh
ls -la /var/log/lastlog /var/log/wtmp /var/log/messages 2>&1
which journalctl 2>&1
journalctl --disk-usage 2>/dev/null   # the systemd-journald replacement for plain-text /var/log/messages
last -n 3 2>/dev/null                 # reads wtmp directly
lastlog -u $USER 2>/dev/null; or lastlog -u (whoami) 2>/dev/null
```
bash/sh: `lastlog -u $USER` for the last line.

**Real-world note**: `/var/log/messages` commonly doesn't exist on a systemd-journald-only
system — `journalctl` reads structured binary logs instead, another example of FHS text
predating a now-dominant subsystem.

## 5.11. `/var/mail` — User mailbox files (optional)

**Claim**: mail spool must be reachable via `/var/mail`, one file per user named exactly
`<username>`, in standard Unix mailbox format. Moved here (from the older `/var/spool/mail`)
specifically for cross-distro/cross-host interoperability — `/var/mail` may be a symlink to the
real location, no requirement to physically relocate existing spools.

**Try it**:
```sh
ls -ld /var/mail 2>&1
readlink -f /var/mail
ls -la /var/spool/mail 2>&1
```

## 5.12. `/var/opt` — Variable data for `/opt`

**Claim**: variable data for an `/opt/<subdir>` package goes in `/var/opt/<subdir>` (unless a
specific file is superseded by something in `/etc`); no imposed internal structure.

**Try it**:
```sh
ls /var/opt 2>&1
ls /opt 2>/dev/null   # cross-reference against link 6's /opt inventory — matching entries?
```

## 5.13. `/var/run` — Run-time variable data

**Claim**: superseded by `/run` (link 6, 3.15) — this directory exists purely for backward
compatibility with software still targeting the old spec. All of `/run`'s requirements apply here
too; implementing `/var/run` as a symlink to `/run` is explicitly valid. `utmp` (who's currently
logged in) specifically still lives under this name. Programs should pick *one* of `/run` or
`/var/run` and stick to it — mixing both in the same program is what the standard is trying to
prevent confusion about.

**Try it**:
```sh
readlink -f /var/run              # expect: resolves straight to /run
ls -la /var/run/utmp 2>&1
who 2>/dev/null                   # reads utmp directly — confirms it's live data, not a stale artifact
```

## 5.14. `/var/spool` — Application spool data

**Claim**: data awaiting future processing (often deleted once processed) — this is the key
distinction from `/var/cache` (5.5): spool data represents *unfinished work*, cache data is purely
*disposable/regeneratable*. Optional named subdirs: `lpd` (print queue; `lpd.lock` goes directly
here, per-printer locks in each printer's own spool subdir), `mqueue` (outgoing mail queue),
`news`, `rwho` (per FHS: historically `/var/rwho` on some BSDs, but re-homed here since it fits
"spooled data" better), `uucp`. UUCP lock files specifically go in `/var/lock`, not here, despite
`uucp` having its own spool subdir.

**Try it**:
```sh
ls /var/spool 2>&1
ls -ld /var/spool/lpd /var/spool/mqueue /var/spool/news /var/spool/rwho /var/spool/uucp 2>&1
```

## 5.15. `/var/tmp` — Temporary files preserved between system reboots

**Claim**: like `/tmp`, but explicitly **must not** be cleared at boot — more persistent than
`/tmp`, though still eligible for site-specific eventual cleanup (recommended less aggressively
than `/tmp`).

**Try it**:
```sh
findmnt /var/tmp                  # compare its filesystem type against /tmp's (link 6, step 14)
ls -ld /var/tmp
stat -c '%A' /var/tmp             # sticky bit expected here too, same multi-user-safety reasoning as /tmp
```
**Real-world confirmation**: if `/tmp` came back as `tmpfs` (link 6) and `/var/tmp` comes back as
a real on-disk filesystem here, that's not a coincidence — it's the literal mechanism that makes
`/var/tmp` survive a reboot while `/tmp` doesn't: RAM-backed vs. disk-backed storage.

## 5.16. `/var/yp` — NIS database files (optional)

**Claim**: variable data for NIS (Network Information Service, formerly "Sun Yellow Pages").
Explicitly distinct from Sun NIS+, which uses `/var/nis` instead — don't conflate the two.

**Try it**:
```sh
ls -ld /var/yp /var/nis 2>&1
which ypbind ypserv 2>&1     # absent = NIS not in use, expected on virtually any modern desktop/laptop
```
