# Link 8 — Exercise: GNU Coreutils — `chown` and `chmod`

Fish primary; bash/sh forms called out where they differ. Everything here operates on throwaway
files under `/tmp` — nothing touches real system files or permissions.

---

### 1. `chown`'s four colon-variants, one at a time

```fish
touch /tmp/ex8-chown.txt
chown $USER /tmp/ex8-chown.txt
stat -c '%U:%G' /tmp/ex8-chown.txt
chown $USER: /tmp/ex8-chown.txt          # owner + "owner's login group"
stat -c '%U:%G' /tmp/ex8-chown.txt
chown :$USER /tmp/ex8-chown.txt          # group only -- same effect as chgrp
stat -c '%U:%G' /tmp/ex8-chown.txt
rm /tmp/ex8-chown.txt
```
For each command, state out loud which of the four `NEW-OWNER` forms from the notes you just used,
before checking the `stat` output confirms it.

### 2. The numeric-ID disambiguation (`+`) — confirm the syntax works, and hunt for the actual risk

```fish
touch /tmp/ex8-numeric.txt
chown "+"(id -u) /tmp/ex8-numeric.txt
stat -c '%u' /tmp/ex8-numeric.txt
rm /tmp/ex8-numeric.txt
getent passwd | awk -F: '$3 ~ /^[0-9]+$/ && $1 ~ /^[0-9]+$/ {print}'
```
bash/sh: `chown "+$(id -u)" /tmp/ex8-numeric.txt`.

If the `getent` line found nothing (expected on most systems), explain in one sentence why the
`+` prefix is still worth using defensively in scripts, even when you're confident no such
username currently exists.

### 3. `chown --from` — the narrowed-but-not-eliminated TOCTOU gap

```fish
touch /tmp/ex8-from.txt
chown --from=root $USER /tmp/ex8-from.txt 2>&1     # should be a no-op / report nothing changed --
                                                     # current owner is you, not root
chown -c --from=$USER $USER /tmp/ex8-from.txt        # -c: should report a change only if owner truly differs
rm /tmp/ex8-from.txt
```
Explain, in your own words, why `--from` narrows the race window between checking a file's owner
and changing it, but doesn't close it completely.

### 4. `chmod` symbolic vs. numeric vs. operator-numeric — three ways to reach the same state

```fish
touch /tmp/ex8-chmod.txt
chmod u=rw,g=rw,o=r /tmp/ex8-chmod.txt
stat -c '%a %A' /tmp/ex8-chmod.txt
chmod 000 /tmp/ex8-chmod.txt
stat -c '%a %A' /tmp/ex8-chmod.txt
chmod 664 /tmp/ex8-chmod.txt
stat -c '%a %A' /tmp/ex8-chmod.txt
chmod =0 /tmp/ex8-chmod.txt
chmod +660 /tmp/ex8-chmod.txt
chmod +4 /tmp/ex8-chmod.txt
stat -c '%a %A' /tmp/ex8-chmod.txt        # should land back on 664 via three incremental operator-numeric steps
rm /tmp/ex8-chmod.txt
```

### 5. Decode a numeric mode by hand before checking your work

Without running anything yet, work out what `stat` will report for `chmod 640` and for
`chmod 2755` on a fresh file, using the 27.3 bit table from the notes. Then check:
```fish
touch /tmp/ex8-decode.txt
chmod 640 /tmp/ex8-decode.txt
stat -c '%a %A' /tmp/ex8-decode.txt
chmod 2755 /tmp/ex8-decode.txt
stat -c '%a %A' /tmp/ex8-decode.txt
rm /tmp/ex8-decode.txt
```

### 6. The `chmod 755` vs. `chmod =755` setuid/setgid preservation difference — on a directory

```fish
mkdir -p /tmp/ex8-setgid-dir
chmod g+s /tmp/ex8-setgid-dir
stat -c '%a %A' /tmp/ex8-setgid-dir
chmod 755 /tmp/ex8-setgid-dir
stat -c '%a %A' /tmp/ex8-setgid-dir       # setgid still present?
chmod g+s /tmp/ex8-setgid-dir
chmod =755 /tmp/ex8-setgid-dir
stat -c '%a %A' /tmp/ex8-setgid-dir       # setgid still present?
rmdir /tmp/ex8-setgid-dir
```
State which of the two `chmod` invocations cleared the setgid bit and which preserved it — and
confirm it matches what the notes claimed, not just what seems intuitive.

### 7. `chmod`'s symlink behavior — command-line target vs. recursion

```fish
mkdir -p /tmp/ex8-symlink-demo
touch /tmp/ex8-symlink-demo/real-file.txt
ln -s real-file.txt /tmp/ex8-symlink-demo/link-to-file
chmod 600 /tmp/ex8-symlink-demo/link-to-file    # named directly on the command line
stat -c '%a %n' /tmp/ex8-symlink-demo/real-file.txt /tmp/ex8-symlink-demo/link-to-file
rm -rf /tmp/ex8-symlink-demo
```
Confirm: did the permission change land on the symlink itself, or on `real-file.txt`? Connect this
back to the notes' claim about `chmod` and symlinks named directly vs. encountered during
recursion.

### 8. `--reference` for both commands together

```fish
touch /tmp/ex8-ref-source.txt /tmp/ex8-ref-target.txt
chmod 640 /tmp/ex8-ref-source.txt
chown $USER: /tmp/ex8-ref-source.txt
chmod --reference=/tmp/ex8-ref-source.txt /tmp/ex8-ref-target.txt
chown --reference=/tmp/ex8-ref-source.txt /tmp/ex8-ref-target.txt
stat -c '%a %U:%G' /tmp/ex8-ref-source.txt /tmp/ex8-ref-target.txt   # both lines should now match
rm /tmp/ex8-ref-source.txt /tmp/ex8-ref-target.txt
```

### 9. Self-check

1. Given numeric mode `6750`, name every permission and special bit it sets, without looking back
   at the notes' table.
2. Why does a plain numeric `chmod` mode "set absolutely" rather than "add to what's already
   there," while symbolic `+`/`-` and operator-numeric `+`/`-` don't have that limitation?
3. What's the actual security reasoning behind the `+`-prefix numeric-ID syntax for `chown` —
   not "it's faster," but the concrete attack/mistake it prevents?
4. Why does `chmod` refuse to touch a symlink's own permissions on most systems, even when you
   explicitly ask via `-h`/`--no-dereference`, unless the underlying OS provides `lchmod`-style
   support (name the syscall gap from the notes)?
