# Link 7 — Exercise: FHS 3.0 Chapter 5 — The `/var` Hierarchy

Fish primary; bash/sh forms called out where they differ. All read-only.

---

### 1. Required + optional `/var` entries, and the reserved names

```sh
for d in cache lib local lock log opt run spool tmp; do
  echo -n "/var/$d -> "; readlink -f /var/$d 2>&1
done
for d in backups cron msgs preserve; do ls -ld /var/$d 2>&1; done
for d in account crash games mail yp; do echo -n "/var/$d -> "; readlink -f /var/$d 2>&1; done
```
Confirm all 4 reserved names are absent (expected — nothing on this machine should be using them
for anything other than their historically-reserved purpose).

### 2. `/var/cache` — inventory and disk usage

```sh
ls /var/cache 2>&1
du -sh /var/cache/* 2>/dev/null | sort -rh | head -5
ls -ld /var/cache/man 2>&1
```
Pick the largest cache directory from the `du` output and explain, from its name alone, why
deleting its contents would cost you *time* (recomputation) but not real *data loss* — that's the
defining property of everything under `/var/cache` per the notes.

### 3. `/var/games` vs `/usr/share/games` — variable vs. static split

```sh
ls -ld /var/games /usr/share/games 2>&1
```

### 4. `/var/lib` — the required subdirectory and real package state

```sh
ls -ld /var/lib/misc
ls /var/lib | head -15
ls -ld /var/lib/color /var/lib/hwclock 2>&1
```
Pick 3 subdirectory names from the `ls /var/lib` output and, from the name alone, guess which
installed package/subsystem owns each — then verify with your package manager (`pacman -Qo
/var/lib/<name>` on Arch, `dpkg -S /var/lib/<name>` on Debian, adjusting for directories vs files
as needed).

### 5. `/var/lock` — confirm it's tmpfs-backed (cleared every boot, by design)

```sh
readlink -f /var/lock
findmnt (readlink -f /var/lock) 2>&1
ls /var/lock 2>&1
```
bash/sh: `findmnt $(readlink -f /var/lock) 2>&1`.

### 6. `/var/log` — required files, and the journald reality check

```sh
ls -la /var/log/lastlog /var/log/wtmp /var/log/messages 2>&1
journalctl --disk-usage 2>/dev/null
last -n 3 2>/dev/null
```
If `/var/log/messages` is missing but `journalctl` works and has real data, explain in one
sentence what replaced plain-text syslog on this machine, and why FHS's text (which assumes
`syslogd`) is still technically satisfiable even so (hint: is a `messages` file *required*, or
required *if that subsystem is installed*?).

### 7. `/var/mail` — trace the symlink chain

```sh
ls -ld /var/mail
readlink -f /var/mail
ls -la /var/spool/mail 2>&1
```
Confirm `/var/mail` really does resolve into `/var/spool/mail` on this machine (or wherever it
actually points) — this is 5.11's back-compat note made concrete: the *logical* location moved,
but the *physical* one didn't have to.

### 8. `/var/opt` cross-referenced against `/opt` (link 6)

```sh
ls /var/opt 2>&1
ls /opt 2>/dev/null
```
For every entry under `/opt`, check whether a matching `/var/opt/<name>` exists. Report the ratio
— this tells you how much variable state those particular packages actually generate.

### 9. `/var/run` → `/run`

```sh
readlink -f /var/run
ls -la /var/run/utmp 2>&1
who 2>/dev/null
```

### 10. `/var/spool` — what's actually queued right now

```sh
ls /var/spool 2>&1
ls -ld /var/spool/lpd /var/spool/mqueue /var/spool/news /var/spool/rwho /var/spool/uucp 2>&1
```

### 11. `/tmp` vs `/var/tmp` — the mechanism behind "survives a reboot," not just the rule

```sh
findmnt /tmp
findmnt /var/tmp
stat -c '%A' /tmp /var/tmp
```
Compare the `FSTYPE` column between the two `findmnt` outputs. State explicitly: which one is
RAM-backed, which is disk-backed, and why that alone — independent of any FHS text — is what
actually determines whether their contents survive a reboot.

### 12. `/var/yp` — confirm NIS isn't in use (expected on virtually any modern machine)

```sh
ls -ld /var/yp /var/nis 2>&1
which ypbind ypserv 2>&1
```

### 13. Self-check

1. `/var/cache`, `/var/lib`, and `/var/spool` all hold "data an application generates while
   running," yet FHS gives them three separate top-level directories. State the one-sentence
   distinguishing purpose of each.
2. Why was `/var/mail`'s *logical* location changed from `/var/spool/mail`, while explicitly
   *not* requiring the physical spool to move?
3. Give the exact byte-for-byte format FHS mandates for a `/var/lock/LCK..*` file's contents, for
   a hypothetical process with PID `42`.
4. Explain, using only what you observed in step 11 (not what the spec says), why `/tmp` is safe
   to lose on reboot but `/var/tmp` deliberately is not.
