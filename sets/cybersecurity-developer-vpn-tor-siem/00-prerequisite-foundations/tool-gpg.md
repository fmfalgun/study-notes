# Tool Reference — gpg (GnuPG)

Companion to `key-generation.md`, which uses `gpg --homedir . --quick-generate-key "Study Key
<study@example.local>" ed25519 sign 1y` to generate a throwaway keypair for hands-on study. This
file goes deep on the key-generation and key-management corner of `gpg` that command lives in.

## Scope

`gpg` (the OpenPGP part of GnuPG) is a large multi-purpose tool: encryption/decryption, digital
signatures on arbitrary data and files, keyserver operations, trust-database/web-of-trust
management, smartcard/token support, dirmngr network configuration, and more, on top of key
generation and management. This file documents **only key generation and key management** —
the area `key-generation.md`'s exercise actually touches — in full depth. Specifically in scope:

- **Key generation**: `--quick-generate-key`, `--full-generate-key`/`--generate-key`, `--batch`
  mode and its parameter-file syntax (`Key-Type`, `Key-Length`, `Subkey-Type`, `Name-Real`,
  `Name-Email`, `Expire-Date`, etc.).
- **Key inventory/inspection**: `--list-keys`, `--list-secret-keys`, `--fingerprint`,
  `--with-colons` (machine-readable listing).
- **Key export/import**: `--export`, `--export-secret-keys`, `--import`.
- **Key lifecycle editing**: `--edit-key` (the `expire`, `addkey`, `adduid`, `deluid`, `key <N>`,
  `save` sub-commands specifically), `--delete-keys`/`--delete-secret-keys`.
- **Isolation flags for safe study use**: `--homedir`, `--no-default-keyring`.

Explicitly **out of scope** — named here only as a one-line pointer, no flag tables, because this
file supports a key-*generation* study exercise, not a full GnuPG reference:

- Operational crypto use of an already-generated key: `--encrypt`, `--decrypt`, `--sign`,
  `--verify`.
- Keyserver operations: `--send-keys`, `--recv-keys`, `--search-keys`, `--keyserver`.
- Trust-database / web-of-trust internals: the `--edit-key` `trust` sub-command,
  `--update-trustdb`, `--trust-model`.
- Smartcard/token operations: `--card-edit`, `--card-status`.
- `dirmngr` configuration (the network-fetch daemon gpg delegates keyserver/CRL lookups to).

## Index

- [Key generation](#key-generation)
  - [Quick generation — `--quick-generate-key`](#quick-generation-------quick-generate-key)
  - [Full and default generation — `--generate-key` / `--full-generate-key`](#full-and-default-generation-------generate-key----full-generate-key)
  - [Batch/unattended generation — `--batch`](#batchunattended-generation-------batch)
    - [The batch parameter-file format](#the-batch-parameter-file-format)
- [Key inspection and listing](#key-inspection-and-listing)
- [Key export and import](#key-export-and-import)
- [Key lifecycle editing](#key-lifecycle-editing)
  - [`--edit-key` sub-commands](#--edit-key-sub-commands)
  - [Quick (non-interactive) lifecycle commands](#quick-non-interactive-lifecycle-commands)
  - [Deletion and revocation](#deletion-and-revocation)
- [Isolation flags](#isolation-flags)
- [Use Cases](#use-cases)
- [References](#references)

## Key generation

### Quick generation — `--quick-generate-key`

The command `key-generation.md` actually runs. It generates a standard key with one user ID
directly, without the interactive prompt sequence of `--generate-key`.

| Flag / argument | Meaning | Notes/gotchas |
|---|---|---|
| `--quick-generate-key user-id [algo [usage [expire]]]` (alias `--quick-gen-key`) | generate a key non-interactively | if `algo`/`usage` are omitted, gpg still shows a confirmation prompt unless run under `--batch`; if either is given, no prompts are shown at all |
| `user-id` (required) | the identity string, e.g. `"Study Key <study@example.local>"` | key creation is **canceled** if this exact user ID already exists in the keyring, unless `--yes` is given |
| `algo` (positional) | key algorithm | e.g. `ed25519`, `cv25519`, `rsa3072`, `rsa4096`, `dsa`; special values `default`, `future-default` (alias for the algorithm likely to become default in a future gpg), and `card` (derive the key from an inserted smartcard's keys) |
| `usage` (positional) | capability restriction (least-privilege) | comma/space-delimited list from `sign`, `encr` (or `encrypt`), `auth`; also accepts `cert` for a certify-only primary key. Default (if omitted but `algo`/`expire` given) is certify+sign. Combinable, e.g. `sign,auth` |
| `expire` (positional) | expiration date | ISO `YYYY-MM-DD` or `YYYYMMDDThhmmss`; relative `seconds=N`, `Nd`, `Nw`, `Nm`, `Ny`; `-` or omitted = a reasonable default interval (not "never"); `never`/`none` = no expiration |
| `--yes` | assume yes / skip the "already exists" cancel | needed for non-interactive re-runs against the same user-id |
| `--batch` | suppress the "Continue?" confirmation entirely | see [Batch/unattended generation](#batchunattended-generation-------batch) below for the combination with passphrase options |
| `--pinentry-mode loopback` + one of `--passphrase`/`--passphrase-fd`/`--passphrase-file` | supply a passphrase without an interactive Pinentry popup | only honored when `--batch` is also given (since GnuPG 2.0) and `--pinentry-mode loopback` is set (since 2.1); use `--passphrase ''` for an unprotected key |

Related quick commands that operate on an *existing* key rather than creating one:
`--quick-set-expire fpr expire [*|subfprs]` (change expiry of the primary key, or of all/named
subkeys with the `*`/fingerprint-list forms), and `--quick-add-key fpr [algo [usage [expire]]]`
(add a subkey to an existing primary key — same `algo`/`usage`/`expire` grammar as above; with no
arguments it defaults to adding an encryption subkey).

### Full and default generation — `--generate-key` / `--full-generate-key`

| Flag | Meaning | Notes/gotchas |
|---|---|---|
| `--generate-key` (alias `--gen-key`) | generate a new keypair using current default parameters | the "standard" command; **also writes a revocation certificate** to `openpgp-revocs.d/` under the GnuPG home directory as a side effect — relevant to what ends up in a throwaway `--homedir` |
| `--full-generate-key` (alias `--full-gen-key`) | generate a new keypair with dialogs for *all* options (algorithm, size, expiry, UID fields) | an extended, fully interactive version of `--generate-key`; this is also the command whose manual section documents batch-mode key generation, below |

Both differ from `--quick-generate-key` in that they are dialog-driven by default; use `--batch`
(next section) to drive either non-interactively via a parameter file.

### Batch/unattended generation — `--batch`

| Flag | Meaning | Notes/gotchas |
|---|---|---|
| `--batch` | enable batch mode: never ask, disallow interactive commands | if a filename is given on the command line, gpg may still read STDIN in some cases (e.g. detached-signature detection) — redirect STDIN to `/dev/null` if that's not wanted. GnuPG recommends pairing this with `--status-fd` and `--with-colons` for any unattended/scripted use, and says **not** to put `--batch` in an options file |
| `--no-batch` | explicitly disable batch mode | reverses `--batch` |
| `--yes` | assume yes on most (non-batch-blocking) questions | should not be used in an option file |
| `--no` | assume no on most questions | should not be used in an option file |
| `--status-fd n` | emit machine-parseable status lines to file descriptor `n` | the recommended pairing with `--batch`; not detailed further here (out of scope — general scripting interface, not key-management specific) |

`--generate-key` combined with `--batch` reads a **key parameter file** — either from STDIN or as
a filename argument — and is described by GnuPG itself as "the most flexible way of generating
keys, but also the most complex one," recommending the quick-generate interface above unless that
flexibility is actually needed. This is the mechanism for scripted/bulk key generation, e.g.
generating many test keys non-interactively.

#### The batch parameter-file format

A distinct mini-syntax, separate from gpg's normal command-line flag grammar. Format rules: plain
text, line length limited to roughly 1000 characters, UTF-8 for non-ASCII, blank lines and
leading/trailing whitespace ignored, a line starting with `#` is a comment. **Control statements**
start with `%`; **parameters** are `Keyword: value` (colon-separated, arguments space-separated
after the colon). `Key-Type` must be the first parameter of a block, though control statements may
appear anywhere. A key block commits (key generation actually happens) at end-of-file, at the next
`Key-Type` line, or at an explicit `%commit`.

**Control statements:**

| Statement | Meaning | Notes/gotchas |
|---|---|---|
| `%echo text` | print `text` as a diagnostic | cosmetic only |
| `%dry-run` | suppress actual key generation | useful to syntax-check a batch file before committing |
| `%commit` | perform the key generation now | an implicit commit also happens at the next `Key-Type` line or end of file |
| `%pubring filename` | write the key to `filename` instead of the default/command-line keyring | must be set before the first commit; GnuPG's own manual recommends the [ephemeral-homedir pattern](#isolation-flags) instead as the more robust way to contain side effects |
| `%secring filename` | (legacy) secret-keyring target | no-op since GnuPG 2.1 — secret keys are always stored under `private-keys-v1.d/` in the home directory now |
| `%ask-passphrase` / `%no-ask-passphrase` | (legacy) toggle passphrase prompting | no-op since GnuPG 2.1 |
| `%no-protection` | create the key with no passphrase protection at all | GnuPG's own docs say this is "mainly intended for regression tests" — exactly the batch-generate-many-test-keys use case, but a real conscious choice to weigh even for study/test keys |
| `%transient-key` | use a faster, less secure RNG | only takes effect combined with `%no-protection`; intended for short-lived keys that don't need full cryptographic strength |

**General parameters** (all `Keyword: value`, one point per row):

| Parameter | Meaning | Notes/gotchas |
|---|---|---|
| `Key-Type: algo` | primary key algorithm | **required**, must be first in the block; algorithm must be signing-capable; `algo` is an OpenPGP algorithm number or name string; special value `default` picks the default key type, in which case `Key-Usage` should not be given and `Subkey-Type: default` should also be used |
| `Key-Length: nbits` | requested key size in bits | default comes from `gpg --gpgconf-list`; ignored for ECC keys |
| `Key-Curve: curve` | elliptic curve for the primary key | required for ECC key types, ignored otherwise |
| `Key-Grip: hexstring` | reuse an already-existing key (by keygrip) | used to generate a CSR/certificate for a key that already exists; makes `Key-Length` irrelevant |
| `Key-Usage: usage-list` | capability flags for the primary key | space/comma-delimited from `encrypt`, `sign`, `auth`; OpenPGP always forces the `cert` flag on for primary keys regardless of this list; if omitted and `Key-Type` isn't `default`, all usages the algorithm allows are granted — if `Key-Type` *is* `default` and this is omitted, usage defaults to `sign` only |
| `Subkey-Type: algo` | generates a secondary key (subkey) | only **one** subkey can be specified this way per block |
| `Subkey-Length: nbits` | subkey size in bits | same default-lookup behavior as `Key-Length` |
| `Subkey-Curve: curve` | subkey elliptic curve | analogous to `Key-Curve` |
| `Subkey-Usage: usage-list` | subkey capability flags | analogous to `Key-Usage` |
| `Passphrase: string` | passphrase for the secret key | default (if omitted) is to prompt via Pinentry — a batch script needs this set (or `%no-protection`) to be truly non-interactive |
| `Name-Real: name` | the "real name" portion of the UID | combines with `Name-Comment`/`Name-Email` — a UID is only created if at least one of the three is given; UTF-8 |
| `Name-Comment: comment` | the parenthetical comment portion of the UID | see above |
| `Name-Email: email` | the email portion of the UID | see above |
| `Expire-Date: iso-date\|(number[d\|w\|m\|y])` | expiration for the key (and its subkey) | ISO format (`20000815T145012`) or a relative count of days/weeks/months/years from creation; `seconds=N` also accepted; **no letter suffix means days**; GnuPG stores this as an absolute internal timestamp, and the last representable year is 2105 |
| `Creation-Date: iso-date` | override the key's creation timestamp | affects the fingerprint calculation since creation time is part of it; date or full timestamp, treated as UTC; `seconds=N` (Unix epoch) also accepted; defaults to "now" |
| `Preferences: string` | cipher/hash/compression preference string | same syntax as the `setpref` sub-command of `--edit-key` |
| `Revoker: algo:fpr [sensitive]` | register a designated revoker at creation time | `algo` is the revoker's public-key algorithm number (e.g. RSA=1, DSA=17); `sensitive` withholds this from default exports; only v4/v5 keys support this |
| `Keyserver: string` | preferred-keyserver URL to embed | out-of-scope territory (keyserver ops) but the parameter itself lives in this list |
| `Handle: string` | a caller-supplied tag (≤100 chars, no spaces) | surfaces in the `KEY_CREATED`/`KEY_NOT_CREATED` status lines — useful to correlate a batch script's own record of "which block generated which key" during bulk generation |

**Note on `User-Id`**: the official GnuPG web manual (gnupg.org) documents an additional
`User-Id: string` parameter — a single pre-composed UID string as an alternative to the
`Name-Real`/`Name-Comment`/`Name-Email` triad — that is **not present in the local `man gpg`
text** on this machine (gnupg 2.4.9). This is exactly the man-page-vs-manual divergence the
sourcing convention anticipates; treat the web manual as authoritative for this one parameter.

Minimal example, using an ephemeral home directory (see [Isolation
flags](#isolation-flags)) so nothing touches a real keyring:

```
export GNUPGHOME="$(mktemp -d)"
cat >batch-params <<EOF
%echo Generating a default key
Key-Type: default
Subkey-Type: default
Name-Real: Joe Tester
Name-Comment: with stupid passphrase
Name-Email: joe@foo.bar
Expire-Date: 0
Passphrase: abc
%commit
%echo done
EOF
gpg --batch --generate-key batch-params
```

`Expire-Date: 0` means "no expiration" in this positional context (distinct from the `never`/
`none` keyword form accepted by `--quick-generate-key`'s positional `expire` argument).

## Key inspection and listing

| Flag | Meaning | Notes/gotchas |
|---|---|---|
| `--list-keys` (`-k`), `--list-public-keys` | list public keys (all, or the given names) | **never parse this output in scripts** — GnuPG explicitly documents it as human-oriented and subject to format changes; use `--with-colons` instead for anything programmatic |
| `--list-secret-keys` (`-K`) | list secret keys | a `#` after the `sec`/`ssb` tag means that key/subkey is present in the listing but not actually usable (e.g. taken offline via `--export-secret-subkeys`); a `>` means the key material lives on a smartcard, not in the local keyring |
| `--check-signatures` (`--check-sigs`) | like `--list-keys`, but also verifies and lists key signatures | for performance reasons, a signing key's own revocation status is *not* checked; signatures whose public key isn't locally available are silently omitted (use `--list-sigs` to still see their key IDs) |
| `--fingerprint` | list keys with their fingerprint on an extra line | same base output as `--list-keys`; **given twice**, also prints fingerprints of all subkeys |
| `--with-fingerprint` | same fingerprint info, layered onto another command's output | e.g. combine with `--list-keys` without switching commands |
| `--with-subkey-fingerprint` | force subkey fingerprints even without doubling `--with-fingerprint` | pairs well with `--keyid-format none` for compact output |
| `--with-colons` | machine-readable, colon-delimited listing | the stable, scriptable format; always UTF-8 regardless of `--display-charset`; format is specified in GnuPG's `doc/DETAILS` file, not the man page itself |
| `--with-keygrip` | include the keygrip in listings | implicitly on for secret keys when `--with-colons` is used |
| `--with-secret` | flag whether a secret key is present, in a `--list-keys --with-colons` public-key listing | useful to check secret-key presence without switching to `--list-secret-keys` |
| `--keyid-format {none\|short\|0xshort\|long\|0xlong}` | controls how key IDs are rendered in listings | long/`0xlong` are the only forms that avoid short-keyid collision ambiguity; ignored once `--with-colons` is used |
| `--show-keys` | print info about OpenPGP keys given as *input* (e.g. a key file), not ones already in a local keyring | same rendering as `--list-keys`, meant to be combined with `--with-colons` for automated processing |
| `--locate-keys` | resolve key arguments the same way gpg would when picking a key for encryption | public keys only; useful to preview what gpg *would* select |

## Key export and import

| Flag | Meaning | Notes/gotchas |
|---|---|---|
| `--export` | export public keys (all, or named) from the configured keyrings | written to STDOUT, or to the file given by `--output`/`-o`; combine with `--armor`/`-a` to get ASCII-armored (mail/paste-friendly) text instead of raw binary OpenPGP |
| `--export-secret-keys` | export secret keys instead of public | often combined with `--armor` for a paper-backup-style export, though GnuPG itself notes the external `paperkey` tool does a better job of actual paper backups; exporting a secret key over an insecure channel is a direct compromise risk |
| `--export-secret-subkeys` | like `--export-secret-keys`, but renders the primary key's secret part **useless** in the exported copy | a GNU extension to OpenPGP — other implementations may not import such a key correctly. Intended workflow: keep the primary key's real secret material on one (offline) machine, and export only a signing subkey to a day-to-day machine |
| `--armor` (`-a`) | ASCII-armor the output | default output is raw binary OpenPGP; armor is what makes a key pasteable into a text field or email |
| `--output file` (`-o file`) | write to `file` instead of STDOUT | `-` explicitly means STDOUT |
| `--export-ssh-key` | export a subkey in OpenSSH `authorized_keys`-compatible public-key format | exports the newest subkey with the authentication capability by default; a specific subkey/primary key can be forced with a fingerprint suffixed `!` |
| `--import` (`--fast-import`) | import/merge keys into the keyring | `--fast-import` is currently just a synonym; `--import-options merge-only` restricts this to merging new signatures/UIDs/subkeys onto keys that already exist, without inserting brand-new keys |

## Key lifecycle editing

### `--edit-key` sub-commands

`--edit-key name` opens an interactive menu for essentially all key-management tasks. Selection
state matters: `uid n` toggles selection of user-ID index `n` (`*` selects all, `0` deselects
all), and `key n` toggles selection of subkey index/key-ID `n` the same way — most sub-commands
below act on whatever is currently selected, or on the primary key if nothing is selected.

| Sub-command | Meaning | Notes/gotchas |
|---|---|---|
| `adduid` | create an additional user ID | |
| `deluid` | delete a user ID | **local-only** — it does not retract a UID that has already reached a keyserver, since keyservers are append-only; use `revuid` for a UID that's already public (see `key-metadata-leakage.md` in this repo for why a real UID is effectively permanent once published) |
| `revuid` | revoke a user ID | the correct operation for a UID that may already be public, as opposed to `deluid` |
| `primary` | flag the currently selected UID as primary | removes the primary flag from all other UIDs of the same kind (regular vs. photo) |
| `addkey` | add a subkey to the currently open key | interactive equivalent of `--quick-add-key` |
| `delkey` | remove a subkey | only deletes the **public** part locally; same "can't retract from a keyserver" caveat as `deluid` — use `revkey` if the subkey may already be public |
| `revkey` | revoke a subkey | |
| `expire` | change expiration time | acts on the selected subkey if one is selected, otherwise on the primary key |
| `change-usage` | change the capability flags (Certify/Sign/Authenticate/Encrypt) of the primary key or a subkey | allowed combinations depend on the key's algorithm — not every algorithm supports every usage flag |
| `passwd` | change the secret key's passphrase | shortcut also available directly as `--change-passphrase`/`--passwd` |
| `disable` / `enable` | disable or enable the whole key | a disabled key is normally unusable for encryption |
| `clean` | strip non-usable signatures/UIDs (revoked, expired, non-validating, superseded, or from keys not present locally) | reduces key size/clutter without changing what's cryptographically valid |
| `minimize` | remove all signatures from every UID except the most recent self-signature | most aggressive size-reduction option |
| `cross-certify` | add cross-certification signatures to signing subkeys that lack them | protects against a specific attack on signing subkeys; all newly generated keys already get this, so mainly useful to bring an old key up to date |
| `save` | write all changes to the keyring and exit | **required** to persist anything done in the session — `quit` discards changes instead |
| `quit` | exit without saving | |
| `trust` | (out of scope — web-of-trust) | changes ownertrust immediately, no `save` needed for this one specifically |

### Quick (non-interactive) lifecycle commands

The unattended equivalents of the `--edit-key` sub-commands above, for scripting:

| Flag | Meaning | Notes/gotchas |
|---|---|---|
| `--quick-set-expire fpr expire [*\|subfprs]` | set expiry on the primary key, or (with `*`/a fingerprint list) on subkeys | non-interactive equivalent of `--edit-key`'s `expire` |
| `--quick-add-key fpr [algo [usage [expire]]]` | add a subkey | non-interactive equivalent of `addkey`; same `algo`/`usage`/`expire` grammar as `--quick-generate-key` |
| `--quick-add-uid user-id new-user-id` | add a UID verbatim | unlike interactive `adduid`, applies **no form validation** — only leading/trailing whitespace is trimmed |
| `--quick-revoke-uid user-id user-id-to-revoke` | revoke a UID | cannot revoke the *last* remaining UID on a key; always uses the reason "User ID is no longer valid" — use interactive `revuid` for a custom reason/text |
| `--quick-set-primary-uid user-id primary-user-id` | set the primary UID flag | non-interactive equivalent of `primary` |
| `--change-passphrase user-id` (alias `--passwd`) | change the secret key's passphrase | combine with `--dry-run` to only *verify* the current passphrase without changing it |

### Deletion and revocation

| Flag | Meaning | Notes/gotchas |
|---|---|---|
| `--delete-keys name` | remove a key from the public keyring | in batch mode, either `--yes` is required or the key must be identified by fingerprint — a deliberate safeguard against deleting multiple ambiguously-matched keys by accident. A `!`-suffixed subkey fingerprint deletes only that subkey; a `!`-suffixed primary-key fingerprint deletes the whole key |
| `--delete-secret-keys name` | remove a key from the secret keyring | in batch mode must be specified by fingerprint; `--yes` avoids a gpg-agent confirmation prompt |
| `--delete-secret-and-public-key name` | delete secret key first (if present), then the public key | in batch mode must be specified by fingerprint |
| `--generate-revocation name` (alias `--gen-revoke`) | create a revocation certificate for the whole key | this only **creates** the certificate — it doesn't revoke anything by itself. Actually revoking requires `--import`-ing the certificate back into the same keyring, then republishing (export/send) the now-revoked key |
| `--generate-designated-revocation name` (alias `--desig-revoke`) | create a revocation certificate that lets someone *else* (a pre-registered designated revoker) revoke this key | requires the keyholder to have set up a `Revoker:` entry (batch format) or `addrevoker` (`--edit-key`) in advance |

The deletion vs. revocation distinction matters for the same reason UIDs are effectively permanent
once published (see `key-metadata-leakage.md`): `--delete-keys`/`deluid`/`delkey` only ever affect
the *local* keyring copy. If a key or UID has already reached a keyserver or another party's
keyring, deleting your local copy does nothing to that copy — revocation is the only mechanism
that actually communicates "don't trust this anymore" to anyone who already has the key.

## Isolation flags

The flags that make a throwaway study keyring possible without touching the real
`~/.gnupg` — the mechanism `key-generation.md`'s `--homedir .` relies on.

| Flag | Meaning | Notes/gotchas |
|---|---|---|
| `--homedir dir` | set the GnuPG home directory (keyring, trustdb, config, agent socket) | defaults to `~/.gnupg`; only recognized when given **on the command line** (not inside a config file); overrides the `GNUPGHOME` environment variable when both are set |
| `GNUPGHOME` (environment variable) | same effect as `--homedir`, set via the environment instead of a flag | GnuPG's own manual recommends this (or `--homedir`) as *the* preferred way to create an "ephemeral home directory" — generate a `mktemp -d` directory, point `GNUPGHOME`/`--homedir` at it, do the work, then delete the directory when done. This is the general pattern `key-generation.md`'s `--homedir .` is a specific instance of |
| `--no-default-keyring` | don't add the default keyring to the keyring list | **gotcha**: gpg still needs *some* keyring for most operations — if this is used without also supplying `--keyring`, GnuPG falls back to using the default keyring anyway. It does not, by itself, guarantee isolation |
| `--keyring file` | add `file` to the list of keyrings used | additive by default — combine with `--no-default-keyring` to use *only* the specified keyring; a bare filename (no slash) resolves relative to the GnuPG home directory |
| `--no-keyring` | use no keyring at all | overrides every other keyring-selecting option; stricter than `--no-default-keyring` |
| `--primary-keyring file` | designate which keyring newly imported keys land in | a variant of `--keyring` |
| `--secret-keyring file` | (obsolete, ignored) | secret keys have lived under `private-keys-v1.d/` in the home directory since GnuPG 2.1 — this flag is a no-op leftover from the pre-2.1 keyring-file model |

**Why isolation matters for a study exercise**: a real `~/.gnupg` accumulates trust decisions,
ownertrust values, and an agent that may already be caching passphrases for real keys. Generating
a throwaway key without `--homedir`/`GNUPGHOME` pointed elsewhere risks (a) polluting that real
trust store with study artifacts, and (b) accidentally interacting with real secret key material
via a shared `gpg-agent` socket. A related gotcha worth knowing even inside an isolated homedir:
by default GnuPG sets a **newly created key's ownertrust to `ultimate`** automatically
(`--no-auto-trust-new-key` is the flag that disables this) — harmless in a disposable homedir, but
the kind of default that would matter immediately if the same command were ever run against a real
keyring.

## Use Cases

- Generating a signing-only key for code-signing or commit-signing use, via
  `--quick-generate-key <uid> ed25519 sign` to enforce least-privilege at creation time rather than
  restricting capabilities after the fact.
- Generating a key with multiple capabilities spread across subkeys (a certify-only primary key
  plus separate sign, encrypt, and authenticate subkeys), so that the highest-value key (the
  certify-capable primary) can be kept offline while day-to-day subkeys stay on a working machine.
- Batch-generating many keys non-interactively for test fixtures or CI, using `--batch
  --generate-key` with a parameter file (and `%no-protection` where a passphrase would only get in
  the way of automated testing).
- Listing and auditing what keys currently exist in a keyring, including which ones have usable
  vs. expired/revoked/offline secret material, before trusting or reusing any of them.
- Exporting a public key (optionally `--armor`-ed) to hand to a colleague or attach to a commit, so
  others can verify signatures made with the corresponding secret key.
- Exporting and securely backing up a private key, understanding that the export itself is
  sensitive material and that `--export-secret-subkeys` exists specifically to avoid moving the
  most sensitive (primary) secret material off an offline machine.
- Setting or extending a key's expiration date (`--quick-set-expire` or `--edit-key`'s `expire`) to
  enforce periodic rotation rather than letting a key remain valid indefinitely.
- Revoking a compromised or retired key with a pre-generated or freshly created revocation
  certificate, and understanding that revocation — not local deletion — is what actually
  communicates "stop trusting this" to anyone who already holds a copy.
- Adding a new user ID to an existing key (e.g. a new email address) without generating a whole new
  keypair, via `adduid`/`--quick-add-uid`.
- Deleting a locally unwanted key or secret key from a personal keyring, while understanding that
  `--delete-keys`/`deluid`/`delkey` only ever affect the local copy, never anything already
  published elsewhere.
- Generating a key inside an isolated, throwaway `--homedir`/`GNUPGHOME` specifically to study or
  test gpg's behavior without risking any interaction with a real keyring, trust database, or
  running `gpg-agent`.
- Inspecting a key's machine-readable listing (`--list-keys --with-colons`) as the stable interface
  to build tooling or scripts against, instead of parsing the human-oriented default listing.

## References

- `gpg(1)` — local man page, GnuPG 2.4.9, as installed on this machine (Arch/Garuda,
  `pacman -S gnupg`). Primary source for this file; consulted in full for every in-scope section
  (`How to manage your keys`, the full `OPTIONS` list, and the `Unattended key generation`
  subsection).
- GnuPG official manual, gnupg.org — "Unattended GPG key generation"
  (`https://www.gnupg.org/documentation/manuals/gnupg/Unattended-GPG-key-generation.html`),
  consulted as the secondary source for the batch parameter-file format per this repo's
  gnu.org-sourced-link convention. It matches the local man page's coverage almost exactly, with
  one addition: a `User-Id: string` batch parameter not present in the local `man gpg` text —
  called out explicitly above where it's documented.
- `https://man.archlinux.org/man/gpg.1` — cross-referenced; documents GnuPG 2.4, no divergence
  found from the local man page in the key-generation/key-management sections.
- `https://manpages.debian.org/testing/gnupg/gpg.1.en.html` — cross-referenced; Debian
  testing/unstable currently ship gpg 2.4.9-4/2.4.9-5 (trixie: 2.4.7-21), i.e. version parity with
  this machine's 2.4.9 at the time of writing. No functional divergence found in the key-generation
  or key-management sections; Debian *stable* branches can lag on the 2.2.x series in general, so
  re-check this page if working against an older Debian install.
