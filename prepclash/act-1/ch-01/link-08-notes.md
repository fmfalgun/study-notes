# Link 8 — Notes: GNU Coreutils Manual — `chown` and `chmod`

Source: https://www.gnu.org/software/coreutils/manual/ (landing page — actual manual is
`coreutils.html`/`coreutils.txt`, one of several official download formats linked from that page).

**Scope note**: the full manual is 31 chapters covering ~100 utilities — far beyond one link pair.
Per your direction, this link covers only `chown` (§13.1) and `chmod` (§13.3), plus two sections
they explicitly delegate real detail to (one level deep): §27 "File permissions" (chmod's MODE
syntax) and §2.4 "Disambiguating user names and IDs" (chown's `+42`-style numeric-ID syntax).
`chgrp`/`touch` (§13.2/§13.4, same chapter) and the rest of the manual are out of scope here.

**Source of truth**: downloaded the official plain-text release directly —
`curl -O https://www.gnu.org/software/coreutils/manual/coreutils.txt.gz` — rather than scraping
the HTML, since GNU publishes this as a first-class distributable format (alongside `.pdf`,
`.info.tar.gz`, `.texi.tar.gz`), and plain text avoids re-deriving structure from markup.

**On `ps`**: not covered by this manual — confirmed by grepping the downloaded text (zero matches)
and cross-checking the GNU software index. `ps` belongs to `procps-ng`, not GNU coreutils; it'll
get its own man7.org-style link later (`man 1 ps`) instead of being force-fit here.

---

## 13.1. `chown` — Change file owner and group

**Claim**: `chown [OPTION]... {NEW-OWNER | --reference=REF_FILE} FILE...`. `NEW-OWNER` syntax
(no embedded whitespace): `[OWNER][:[GROUP]]` —
- `OWNER` alone → owner changes, group untouched.
- `OWNER:GROUP` → both change.
- `OWNER:` → owner changes; group becomes OWNER's *login* group.
- `:GROUP` → only group changes (same effect as `chgrp`).
- `:` alone, or empty `NEW-OWNER` → nothing changes.

A leading `+` on a numeric ID forces integer interpretation, skipping the name-lookup step
entirely (see §2.4 below for *why* this matters — it's not just a performance shortcut).
`.` is accepted in place of `:` for old-script backward compatibility only — new scripts should
never use it. `chown` **may clear the setuid/setgid bits** as a side effect, depending on the
underlying `chown(2)` syscall's policy — not something `chown` itself fully controls.

**Simple explanation**: `chown` is really "set owner, optionally set group in the same call" —
the colon syntax is doing double duty, and the four colon-variants above are the actual API, not
just one form with optional pieces.

**Try it** (fish; all on throwaway files, nothing touches real system state):
```fish
touch /tmp/chown-demo.txt
chown $USER /tmp/chown-demo.txt              # owner only
chown $USER:$USER /tmp/chown-demo.txt        # owner + group
chown +(id -u):+(id -g) /tmp/chown-demo.txt  # numeric, name-lookup skipped
stat -c '%U:%G' /tmp/chown-demo.txt
rm /tmp/chown-demo.txt
```
bash/sh: `chown "+$(id -u):+$(id -g)" /tmp/chown-demo.txt` for the numeric line.

### `chown` options worth knowing

- `-c`/`--changes`: only report files whose ownership *actually* changed (quieter than `-v`).
- `-f`/`--silent`/`--quiet`: suppress error messages.
- `--from=OLD-OWNER`: only act if the file's *current* owner matches — the manual's own rationale
  is a real security point: without this, a `find -owner OLD -exec chown NEW {}` has a TOCTOU gap
  (the file's owner could change between `find`'s check and `chown`'s action); `--from` narrows
  that window, though the manual is explicit it doesn't eliminate it.
- `--dereference` (default when non-recursive) vs. `-h`/`--no-dereference` (act on the symlink
  itself, via `lchown(2)`): combining `--dereference` with `-R` recursion is flagged as a real
  security risk — an attacker can plant a symlink mid-traversal to redirect the operation.
- `--reference=REF_FILE`: copy REF_FILE's owner/group instead of naming one directly.
- `-R`/`--recursive`, with `-H`/`-L`/`-P` controlling symlink traversal depth during recursion.
- `--preserve-root` / `--no-preserve-root`: guard against `chown -R ... /` by accident.

**Try it**:
```fish
mkdir -p /tmp/chown-demo-dir
touch /tmp/chown-demo-dir/a.txt
chown -c $USER /tmp/chown-demo-dir/a.txt          # -c only prints if ownership truly changed
chown -c $USER /tmp/chown-demo-dir/a.txt          # run again -- no output, nothing changed this time
chown --reference=/tmp/chown-demo-dir/a.txt /tmp/chown-demo-dir
rm -rf /tmp/chown-demo-dir
```

## 2.4. Disambiguating user names and IDs (one level deep — `chown`'s `+` syntax)

**Claim**: POSIX requires `chown`/`chgrp`/`chroot`/`id` to try resolving a given string as a
*name* first, falling back to numeric ID only if that lookup fails. This is genuinely dangerous if
you intend a numeric ID that also happens to collide with an existing *user name* — `chown 42 F`
could silently resolve "42" as a username mapping to UID 1000, not literal UID 42. Prefixing with
`+` (`chown +42 F`) forces integer interpretation and skips the name lookup — also a minor
performance win (no database lookup), though the manual is clear the safety reason is the primary
motivation. Not portable to Solaris 10, but works on "most common Unix systems."

**Simple explanation**: this is the same class of bug as SQL injection, just for identity
resolution — an *ambiguous* input format lets attacker-controlled or accidental string content
change what a privileged command actually does. The `+` prefix is the disambiguating sigil.

**Try it**:
```sh
id -u          # your real numeric UID
touch /tmp/chown-id-demo.txt
chown "+$(id -u)" /tmp/chown-id-demo.txt   # forced-numeric form
stat -c '%u' /tmp/chown-id-demo.txt
rm /tmp/chown-id-demo.txt
getent passwd | awk -F: '$3 ~ /^[0-9]+$/ && $1 ~ /^[0-9]+$/ {print}' | head -3
                # hunt for any purely-numeric usernames on this system -- the exact ambiguity this section warns about
```

## 13.3. `chmod` — Change access permissions

**Claim**: `chmod [OPTION]... {MODE | --reference=REF_FILE} FILE...`. `chmod` does **not** change
a symlink's own permissions (most systems ignore them anyway / the syscall can't) — a symlink
named directly on the command line has its **target's** permissions changed instead; symlinks
encountered *during recursive traversal* are ignored entirely by default. Only the file's owner
(matching effective UID) or a privileged process may change its mode bits. A successful `chmod`
clears the setgid bit on a regular file if the file's group doesn't match the caller's effective
or supplementary group IDs (unless privileged) — an automatic safety clamp, not something you
opt into.

**Try it** (fish):
```fish
touch /tmp/chmod-demo.txt
chmod 644 /tmp/chmod-demo.txt
stat -c '%a %A' /tmp/chmod-demo.txt
chmod u+x /tmp/chmod-demo.txt
stat -c '%a %A' /tmp/chmod-demo.txt
chmod a=r,u+w /tmp/chmod-demo.txt
stat -c '%a %A' /tmp/chmod-demo.txt
rm /tmp/chmod-demo.txt
```

### `chmod` options worth knowing

Same `-c`/`--dereference`/`-h`/`--preserve-root`/`--reference`/`-R`/`-H`/`-L`/`-P` pattern as
`chown` above (consistent option vocabulary across the coreutils suite is itself worth noticing).
One `chmod`-specific subtlety: `chmod =755 DIR` (operator-numeric form) **clears** setuid/setgid
on a directory, while `chmod 755 DIR` (plain numeric) **preserves** them — a real, easy-to-miss
behavioral difference between two modes that look almost identical.

**Try it**:
```fish
mkdir -p /tmp/chmod-setgid-demo
chmod g+s /tmp/chmod-setgid-demo
stat -c '%a %A' /tmp/chmod-setgid-demo   # note the 's' in the group execute position
chmod 755 /tmp/chmod-setgid-demo
stat -c '%a %A' /tmp/chmod-setgid-demo   # setgid PRESERVED (plain numeric mode)
chmod g+s /tmp/chmod-setgid-demo
chmod =755 /tmp/chmod-setgid-demo
stat -c '%a %A' /tmp/chmod-setgid-demo   # setgid CLEARED (operator-numeric mode)
rmdir /tmp/chmod-setgid-demo
```

## 27.1–27.4. File permissions (one level deep — `chmod`'s MODE argument, in full)

**Claim** (27.1 — structure): every file has permission bits (read/write/execute, for owner/
group/other = 9 bits total) plus 3 special bits: **setuid** (execute → effective UID becomes the
file's owner), **setgid** (execute → effective GID becomes the file's group; on directories: new
files inherit the *directory's* group, and the setgid bit itself propagates to new subdirs),
**sticky/restricted-deletion** (on a directory: only the file's owner or the directory's owner may
delete/rename a file inside — the canonical `/tmp` pattern). Filesystem-specific attributes
(immutability via `chattr` on ext-family, `chflags` on FFS) sit *outside* the mode-bits system
entirely — a file can be unmodifiable regardless of what `chmod` says.

**Claim** (27.2 — symbolic modes): format `[ugoa...][-+=]PERMS...[,...]`. `USERS`: `u`=owner,
`g`=group, `o`=others, `a`=all (=`ugo`), letters combinable in any order. `OPERATION`: `+`=add,
`-`=remove, `=`=set-exactly (clearing anything not listed). `PERMS`: letters from `rwxXst` (or a
single `ugo` letter, to copy another category's current permission).

**Claim** (27.3 — numeric/octal modes): 4 octal digits, high to low: special bits
(`4000`=setuid, `2000`=setgid, `1000`=sticky), owner (`400`/`200`/`100` = r/w/x), group
(`40`/`20`/`10`), other (`4`/`2`/`1`). E.g. `4751` = `u=srwx,g=rx,o=x`; `664` = `ug=rw,o=r`.
Numeric modes are always octal without needing a leading `0`. **Limitation**: a plain numeric mode
sets bits *absolutely* — it can't say "add to whatever's already there" the way symbolic `+` can
(setuid/setgid-on-directories being the one documented exception).

**Claim** (27.4 — operator numeric modes, GNU extension): prefixing a numeric mode with
`-`/`+`/`=` gives it the same relative semantics as symbolic mode operators — e.g. `+440` adds
owner+group read, `-1` removes other's execute, `=600` clears everything except owner rw. This is
exactly the mechanism behind the `chmod 755` vs. `chmod =755` setuid/setgid distinction noted
above.

**Try it**:
```fish
# decode a numeric mode by hand, then verify against stat
chmod 4751 /tmp/chmod-numeric-demo 2>/dev/null; or touch /tmp/chmod-numeric-demo; and chmod 4751 /tmp/chmod-numeric-demo
stat -c '%a %A' /tmp/chmod-numeric-demo   # expect rwsr-x--x  (setuid 's' replacing owner's x)
chmod 664 /tmp/chmod-numeric-demo
stat -c '%a %A' /tmp/chmod-numeric-demo   # expect rw-rw-r--
rm /tmp/chmod-numeric-demo

# symbolic vs numeric producing the identical result
touch /tmp/chmod-equiv-demo
chmod u=rw,g=rw,o=r /tmp/chmod-equiv-demo
stat -c '%a' /tmp/chmod-equiv-demo        # should read 664
chmod 664 /tmp/chmod-equiv-demo
stat -c '%a' /tmp/chmod-equiv-demo        # unchanged -- confirms the two forms are equivalent here
rm /tmp/chmod-equiv-demo
```
bash/sh: replace the fish `or`/`and` conditional line with
`touch /tmp/chmod-numeric-demo && chmod 4751 /tmp/chmod-numeric-demo`.
