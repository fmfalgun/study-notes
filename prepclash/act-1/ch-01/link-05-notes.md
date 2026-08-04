# Link 5 — Notes: FHS 3.0 Chapter 4 — The `/usr` Hierarchy

Source: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch04.html (index page — real content lives
in `ch04s02.html` through `ch04s12.html`, all fetched and read directly via `curl`; no local
man-page equivalent exists for FHS).

Same usrmerge caveat as link 4 applies throughout: on this machine `/bin`, `/sbin`, `/usr/sbin`
are all the same directory (`/usr/bin`) via symlinks, and `/lib` = `/usr/lib`. FHS chapter 4
predates usrmerge and describes `/usr/bin` and `/usr/sbin` as if they were meaningfully separate
from `/bin`/`/sbin` in *purpose* even where the physical directories later got merged.

---

## 4.2. Requirements — the five mandatory `/usr` subdirectories

**Claim**: `/usr/bin`, `/usr/lib`, `/usr/local`, `/usr/sbin`, `/usr/share` (or symlinks to them)
are required.

**Try it**:
```sh
for d in bin lib local sbin share; do echo -n "/usr/$d -> "; readlink -f /usr/$d 2>&1; done
```

## 4.3. Specific Options — optional dirs, and legacy `/var` compatibility symlinks

**Claim**: `/usr/games`, `/usr/include`, `/usr/libexec`, `/usr/lib<qual>`, `/usr/src` are optional
(X11 gets a historical exception). Legacy symlinks `/usr/spool → /var/spool`,
`/usr/tmp → /var/tmp`, `/usr/spool/locks → /var/lock` **may** exist for backward compatibility,
and may be removed once no longer needed.

**Simple explanation**: this is FHS explicitly permitting its own obsolescence — these symlinks
existed because very old software still hardcoded `/usr/spool`/`/usr/tmp` paths from before the
`/var` hierarchy existed; a modern system has no reason to carry them.

**Try it**:
```sh
ls -ld /usr/spool /usr/tmp /usr/spool/locks 2>&1
```
Expect "No such file or directory" on a modern system — that's the *correct*, up-to-date state
per the standard's own text, not a violation of it.

## 4.4. `/usr/bin` — Most user commands

**Claim**: the primary directory of executable commands. **Requirement**: no subdirectories
allowed in `/usr/bin`. Specific optional files (if the subsystem is installed): `perl`, `python`,
`tclsh`, `wish`, `expect` — rationale: standardizing interpreter paths makes `#!/path` script
shebangs portable across systems.

**Try it**:
```sh
find /usr/bin -maxdepth 1 -type d | grep -v '^/usr/bin$'   # look for subdirectories (should be none per spec)
for c in perl python tclsh wish expect; do which $c 2>&1; done
file (which perl python 2>/dev/null)   # confirm these are real interpreter binaries, not stubs
grep -rl '^#!/usr/bin/perl' /usr/bin/*.pl 2>/dev/null | head -1 | xargs -r head -1
                                        # find one real script on the system whose shebang points
                                        # at exactly the standardized /usr/bin/perl this section requires
```
bash/sh: replace `file (which perl python 2>/dev/null)` with `file $(which perl python 2>/dev/null)`.

**Real-world check**: if `find` above turned up subdirectories (Arch's Perl packaging does add
`core_perl`/`vendor_perl`/`site_perl` under `/usr/bin` in some configurations) — that's a live
example of a distro trading strict FHS compliance for a packaging convenience, worth noting rather
than treating as "the spec must be wrong."

## 4.5. `/usr/include` — Standard include files

**Claim**: general-use C include files go here. Optional subdirectory: `bsd` (BSD compatibility
headers), if that subsystem is installed.

**Try it**:
```sh
ls -ld /usr/include/bsd 2>&1
ls /usr/include | wc -l           # rough sense of how many headers a typical desktop install carries
```

## 4.6. `/usr/lib` — Libraries for programming and packages

**Claim**: object files and libraries; may include internal (not user-facing) binaries; an
application using a subdirectory must keep all its architecture-dependent data inside that one
subdirectory. Historical special case: `/usr/lib/sendmail` must be a symlink to the system's
sendmail-compatible MTA command if one exists (modern placement default: `/usr/sbin/sendmail`).
X11 host-specific config must live in `/etc/X11`, never `/usr/lib/X11`.

**Try it**:
```sh
ls -la /usr/lib/sendmail /usr/sbin/sendmail 2>&1   # absent = no local MTA installed, expected on a desktop
ls /usr/lib | wc -l
ls -ld /usr/lib/perl5 2>&1        # example of the "single app subdirectory" pattern in practice
```

## 4.7. `/usr/libexec` — Binaries run by other programs (optional)

**Claim**: holds internal binaries not meant to be run directly by users/scripts. An app that uses
`/usr/libexec` for this must *not* also stash internal binaries in `/usr/lib` — pick one
convention per application. Rationale: older FHS versions didn't support `/usr/libexec` at all
(despite it being standard elsewhere, e.g. GNU Coding Standards), so `/usr/lib` became the
historical workaround; both are now acceptable.

**Try it**:
```sh
ls -ld /usr/libexec 2>&1
ls /usr/libexec 2>/dev/null | head -10
```

## 4.8. `/usr/lib<qual>` — Alternate format libraries (optional)

**Claim**: same role as `/usr/lib` but for an alternate binary format (e.g. 32-bit libs on a
64-bit system) — `<qual>` is a placeholder, not literal text. The `sendmail`/`X11` symlink
requirements from 4.6 don't apply to this alternate variant.

**Try it**:
```sh
ls -ld /usr/lib32 /usr/lib64 2>&1   # <qual> instantiated as 32/64 on most real distros
readlink -f /usr/lib64 2>&1          # on many 64-bit-primary distros this is itself a symlink to /usr/lib
```

## 4.9. `/usr/local` — Local hierarchy

**Claim**: for system-administrator-installed local software, safe from being overwritten by
system package updates. Required subdirs (or symlinks): `bin`, `etc`, `games`, `include`, `lib`,
`man`, `sbin`, `share`, `src`. `/usr/local/etc` may symlink to `/etc/local` (but `/usr/etc` is
never allowed — `/usr`-installed programs must use `/etc` directly, not a `/usr/etc`). If
`/usr/share/color` exists, `/usr/local/share/color` must exist too, governed the same way.
Rationale: keeps admin-installed software from being clobbered by a distro upgrade, without
needing to backup all of `/usr`.

**Try it**:
```sh
for d in bin etc games include lib man sbin share src; do
  echo -n "/usr/local/$d -> "; readlink -f /usr/local/$d 2>&1
done
ls -ld /usr/etc 2>&1     # must NOT exist per spec — confirm
ls /usr/local/bin /usr/local/share 2>&1 | head    # anything you've personally installed shows up here
```

## 4.10. `/usr/sbin` — Non-essential standard system binaries

**Claim**: non-essential sysadmin-only binaries. Anything required for system repair/recovery/
mounting `/usr` must instead be in `/sbin` (not `/usr/sbin`) — the essential-vs-non-essential
split is the whole reason `/sbin` and `/usr/sbin` exist as *separate concepts* (even though on
this usrmerged machine they're now the same physical directory). **Requirement**: no
subdirectories.

**Try it**:
```sh
find /usr/sbin -maxdepth 1 -type d | grep -v '^/usr/sbin$'   # should be none
readlink -f /sbin /usr/sbin   # confirm: same physical target on this machine (usrmerge)
```

## 4.11. `/usr/share` — Architecture-independent data

**Claim**: read-only, architecture-independent data (shareable across e.g. i386/Alpha/PPC builds
of the same OS release, not across different OSes or releases). Required subdirs: `man`, `misc`.
Optional (if subsystem installed): `color`, `dict`, `doc`, `games`, `info`, `locale`, `nls`, `ppd`,
`sgml`, `terminfo`, `tmac`, `xml`, `zoneinfo`. Game *data* here must be static — anything
modifiable (scores, logs) belongs in `/var/games` instead.

**Try it**:
```sh
ls -ld /usr/share/man /usr/share/misc          # required — should exist
for d in color dict doc games info locale nls ppd sgml terminfo tmac xml zoneinfo; do
  echo -n "/usr/share/$d -> "; ls -ld /usr/share/$d 2>&1 | awk '{print $NF}'
done
```

### 4.11's own sub-structure worth calling out individually

- **`/usr/share/man`**: the big one. `<mandir>/<locale>/man<section>/<arch>`. Sections 1-8 are
  standardized (1=user programs, 2=syscalls, 3=library calls, 4=special files/`/dev`, 5=file
  formats, 6=games, 7=misc/troff macros, 8=sysadmin). `<locale>` follows POSIX's
  `<language>[_<territory>][.<character-set>]` (e.g. `en_GB.10646`, `ja_JP.sjis`).
  ```sh
  ls /usr/share/man                      # locale subdirectories — real evidence of the <locale> scheme
  ls /usr/share/man/man1 2>/dev/null | wc -l   # if pages live unqualified, no multi-locale setup here
  man --path 2>/dev/null | tr ':' '\n' | head  # confirm your actual man search path matches this hierarchy
  ```
- **`/usr/share/misc`**: single-file, no-subdirectory-needed data. Optional: `ascii`, `termcap`,
  `termcap.db`.
  ```sh
  ls -la /usr/share/misc 2>&1
  ```
- **`/usr/share/dict`**: word lists (traditionally just `words`, American or British spelling).
  ```sh
  ls -ld /usr/share/dict 2>&1; ls /usr/share/dict 2>/dev/null
  ```
- **`/usr/share/color`**: ICC color profiles, only under an `icc` subdirectory — top level must
  hold *no files directly*.
  ```sh
  ls -la /usr/share/color 2>&1
  ```
- **`/usr/share/zoneinfo`**: timezone database.
  ```sh
  ls /usr/share/zoneinfo | head -5
  timedatectl show -p Timezone --value 2>/dev/null   # confirm your system actually reads from this hierarchy
  readlink -f /etc/localtime                          # /etc/localtime is normally a symlink INTO this tree
  ```

## 4.12. `/usr/src` — Source code (optional)

**Claim**: source may be placed here for *reference only* — the spec explicitly discourages
building software directly inside this hierarchy.

**Try it**:
```sh
ls -ld /usr/src 2>&1
ls /usr/src 2>&1 | head        # on this machine: DKMS-style kernel-module source trees, not raw kernel source
```
