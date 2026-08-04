# Link 5 — Exercise: FHS 3.0 Chapter 4 — The `/usr` Hierarchy

Fish primary; bash/sh forms called out where they differ. All read-only.

---

### 1. The five required subdirectories, and the usrmerge reality behind them

```sh
for d in bin lib local sbin share; do echo -n "/usr/$d -> "; readlink -f /usr/$d 2>&1; done
readlink -f /bin /sbin /usr/sbin /lib
```
Explain: given the second command's output, is `/usr/sbin` on this machine actually a distinct
directory from `/sbin`, or the same one? What does that mean for 4.10's "essential → `/sbin`,
non-essential → `/usr/sbin`" distinction in practice here?

### 2. Legacy compatibility symlinks — confirm they're correctly *absent*

```sh
ls -ld /usr/spool /usr/tmp /usr/spool/locks 2>&1
```
All three should be missing. Explain why that's the spec-compliant modern state, not a defect.

### 3. `/usr/bin` — no-subdirectories rule and interpreter standardization

```sh
find /usr/bin -maxdepth 1 -type d | grep -v '^/usr/bin$'
for c in perl python tclsh wish expect; do which $c 2>&1; done
```
```fish
file (which perl python 2>/dev/null)
```
bash/sh: `file $(which perl python 2>/dev/null)`
```sh
grep -rl '^#!/usr/bin/perl' /usr/bin/*.pl 2>/dev/null | head -1 | xargs -r head -1
```
If step 1's `find` returned any subdirectories, name them and explain what packaging convenience
is trading against strict spec compliance there.

### 4. `/usr/include`, `/usr/lib`, `/usr/libexec`, `/usr/lib<qual>` in one pass

```sh
ls -ld /usr/include/bsd 2>&1
ls -la /usr/lib/sendmail /usr/sbin/sendmail 2>&1
ls -ld /usr/libexec 2>&1
ls -ld /usr/lib32 /usr/lib64 2>&1
readlink -f /usr/lib64 2>&1
```
Identify which of these five checks came back "optional feature not installed" vs. "exists and
matches the spec."

### 5. `/usr/local` — every required subdirectory, plus the `/usr/etc` negative check

```sh
for d in bin etc games include lib man sbin share src; do
  echo -n "/usr/local/$d -> "; readlink -f /usr/local/$d 2>&1
done
ls -ld /usr/etc 2>&1                 # must NOT exist
ls /usr/local/bin /usr/local/share 2>&1 | head
```
`/usr/etc` not existing is a hard requirement, not an optional check — if it *did* exist on some
system, that would be a real FHS violation worth flagging, unlike most of the "optional, not
installed" results elsewhere in this exercise.

### 6. `/usr/sbin` — no-subdirectories rule

```sh
find /usr/sbin -maxdepth 1 -type d | grep -v '^/usr/sbin$'
```

### 7. `/usr/share` — required vs. optional subdirectories, all at once

```sh
ls -ld /usr/share/man /usr/share/misc
for d in color dict doc games info locale nls ppd sgml terminfo tmac xml zoneinfo; do
  echo -n "/usr/share/$d -> "; ls -ld /usr/share/$d 2>&1 | awk '{print $NF}'
done
```
Tally: how many of the 13 optional subdirectories are actually present on this machine? That
ratio is itself informative about how minimal/full this particular install is.

### 8. `/usr/share/man` — the locale/section structure, verified against the real man search path

```sh
ls /usr/share/man                        # locale-coded subdirectories, e.g. en, de_DE.88591-style
ls /usr/share/man/man1 2>/dev/null | wc -l
man --path 2>&1 | tr ':' '\n'
manpath 2>&1 | tr ':' '\n'
```
Pick any one locale directory you see and, using the notes' `<language>[_<territory>][.<charset>]`
breakdown, decode exactly what language/region/character-set it represents.

### 9. `/usr/share/zoneinfo` — trace the actual chain from your live system clock to this hierarchy

```sh
timedatectl show -p Timezone --value 2>&1
readlink -f /etc/localtime
ls /usr/share/zoneinfo | head -5
```
Confirm `/etc/localtime` really does resolve into `/usr/share/zoneinfo/...` — this is FHS's
"architecture-independent shareable data" claim made concrete for something you rely on every
time you check the system clock.

### 10. `/usr/src` — reference-only source, distro-specific

```sh
ls -ld /usr/src 2>&1
ls /usr/src 2>&1 | head
```
Given what's actually in there (or its absence), state whether this matches "reference-only
source code, not meant to be built in place" or looks like something else (e.g. DKMS trees).

### 11. Self-check

1. Explain the essential/non-essential split FHS draws between `/sbin` and `/usr/sbin` — and why
   that conceptual split still matters for boot/recovery reasoning even on a usrmerged system
   where they're the same physical directory.
2. Why does FHS explicitly forbid `/usr/etc`, requiring `/etc` directly instead?
3. Give one concrete example from this exercise of a directory that's "optional, and absent" vs.
   one that's "required, and present" — and explain how you'd tell the difference from the spec
   text alone before ever running a command.
