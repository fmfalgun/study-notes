# Tool Reference — age-keygen

Companion deep-reference to `key-generation.md` §10 (age keypair). `age-keygen` is the
key-generation half of [`age`](https://github.com/FiloSottile/age) — a simple, modern,
X25519-based file-encryption tool positioned as an alternative to `gpg` for straightforward
"encrypt this file to this recipient" use cases, without gpg's keyring/web-of-trust machinery.
`age-keygen` itself does nothing but produce and inspect key material; encryption/decryption is a
separate binary, `age`.

## Scope

`age-keygen` is a small, single-purpose tool, so the whole man page is in scope — no exclusions
needed. Every documented flag (`-o`/`--output`, `-y`, `-pq`, `--version`) is covered in full below,
along with the identity-file format it produces and the Bech32 encoding underlying both key types.

One deliberate boundary: the separate `age` / `age -d` encryption/decryption tool — which
*consumes* the identity file `age-keygen` produces — is **not** covered in flag-by-flag depth here,
since it's a usage-adjacent tool, not the generation tool this file documents. The
[How the Output Is Consumed](#how-the-output-is-consumed) section below covers `age -r`, `age -R`,
and `age -d -i` only briefly, as necessary context for the [Use Cases](#use-cases) section to make
sense — the same way `key-generation.md`'s GPG entry generates a signing key without going into
`gpg --encrypt` depth.

## Index

- [Flags and Options](#flags-and-options)
- [The Identity File Format](#the-identity-file-format)
- [Bech32 Encoding](#bech32-encoding)
- [Protecting the Identity File at Rest](#protecting-the-identity-file-at-rest)
- [How the Output Is Consumed](#how-the-output-is-consumed)
- [Real-Machine Grounding: Arch vs. Debian](#real-machine-grounding-arch-vs-debian)
- [Use Cases](#use-cases)
- [References](#references)

## Flags and Options

`age-keygen` has two synopsis forms:

```
age-keygen [-pq] [-o OUTPUT]
age-keygen -y [-o OUTPUT] [INPUT]
```

The first form generates a fresh key pair; the second (`-y`) converts an existing identity file
into its corresponding recipient(s). These modes are mutually exclusive in practice — `-y` changes
what `INPUT`/`OUTPUT` mean rather than combining with generation.

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-o`, `--output=OUTPUT` | Write the identity (or, in `-y` mode, the derived recipient) to `OUTPUT` instead of standard output. | **If `OUTPUT` already exists, it is not overwritten** — the command errors out (`failed to open output file ... file exists`) rather than clobbering an existing key. Verified on this machine: re-running `age-keygen -o key.txt` against an existing `key.txt` exits 1 with that exact message. |
| `-y` | Read an identity file from `INPUT` (or standard input if `INPUT` is omitted) and print the corresponding recipient(s) to standard output, one per line, with no comments. | This is the "re-derive/re-display the public key" flag called out in `key-generation.md`'s flag table — use it any time you have the private identity file but lost or need to re-share the public key. Works whether or not the original file still has its `# public key:` comment line. |
| `-pq` | Generate a post-quantum hybrid ML-KEM-768 + X25519 key pair instead of a plain X25519 one. | New in age **1.3.0** (December 2025) — see [Real-Machine Grounding](#real-machine-grounding-arch-vs-debian) below for why this matters on older installs. The man page itself notes "In the future, this might become the default," i.e. it is opt-in for now, not yet the baseline. Produces a much longer public key (observed locally: ~1,900+ characters vs. ~62 for plain X25519) and a secret key with an `AGE-SECRET-KEY-PQ-1...` prefix instead of `AGE-SECRET-KEY-1...`. |
| `--version` | Print the version and exit. | Plain informational flag; confirmed locally as `age-keygen --version` → `1.3.1`. |

**No output-destination behavior when not writing to a file**: if `-o` is omitted and standard
output is *not* a terminal (e.g. it's piped or redirected), `age-keygen` prints the identity to
standard output as usual but sends the `Public key: ...` confirmation line to **standard error**
instead of interleaving it with the identity on stdout. This is a deliberate design choice so that
`age-keygen | some-pipe` doesn't accidentally capture the human-readable status line as part of the
key material.

**No `-p`/passphrase flag on `age-keygen` itself.** Passphrase protection is not a generation-time
option of this tool — it's applied afterward by piping the resulting file through the separate
`age -p` command (see [Protecting the Identity File at Rest](#protecting-the-identity-file-at-rest)
below). Don't confuse this with `age`'s own `-p`/`--passphrase` flag, which belongs to the
encryption tool, not `age-keygen`.

**No `-q` (quiet) flag.** The synopsis line `[-pq]` is easy to misread as two combinable short
flags (`-p` and `-q`, in the getopt-bundling style common to other CLI tools); it is in fact one
single flag, `-pq`, meaning "post-quantum." Confirmed against both `man age-keygen` and
`age-keygen -h` — both list `-pq` as one entry with one description, and there is no separate `-p`
or `-q` flag documented anywhere in the man page, help text, or `age-keygen`'s own error output.

## The Identity File Format

Running `age-keygen -o age-key.txt` (as in `key-generation.md`) produces a small plaintext file
with exactly three lines. Verified locally by generating a throwaway key in a scratch directory:

```
# created: 2026-08-05T13:16:02+05:30
# public key: age1wrmpanzx48kcvzn0zu3qgfqgpckq6ep3fhtfdmmlkzl8zddzff0s95ef23
AGE-SECRET-KEY-10PPPCX3PY8Y0PNKGGA3LFZ9GL3FRP6J5946RRUGE8NL6XF5Z8Q5QAZPJ8E
```

One point per line, since each carries distinct meaning:

- **Line 1 (`# created: ...`)** is a comment (age treats any line starting with `#` as a comment,
  ignored by parsers) recording an RFC 3339 timestamp of generation time. Purely informational —
  no cryptographic role.
- **Line 2 (`# public key: ...`)** is also a comment, but a load-bearing one in practice: it's the
  human-convenient copy of the public key, present purely so a human (or script grepping for the
  `# public key:` prefix) can read off the recipient value without re-deriving it via `age-keygen
  -y`. Deleting this line does not affect the key's function — the private key on line 3 fully
  determines the public key, which is why `-y` can always re-derive it.
- **Line 3 (`AGE-SECRET-KEY-1...`)** is the actual secret key — the only line age's own tooling
  strictly requires. This is the X25519 private key value, Bech32-encoded (see next section).

**Concerning fact, called out explicitly**: this file is **plaintext by default**. There is no
passphrase, no OS keychain integration, and no encryption applied by `age-keygen` itself — the
entire security of the private key rests on filesystem permissions (and whatever encrypts the disk
underneath it). This is the exact same adversary-model gap `key-generation.md`'s flag table already
flags for this entry, and it's the same category of risk as `ssh-keygen -N ""` or `openssl ...
-nodes` elsewhere in that file's key list.

One mitigation `age-keygen` *does* apply automatically, verified locally: the output file is
created with mode `0600` (owner read/write only) regardless of the process umask — tested here
with `umask` reporting `0022` and the resulting file still showing `-rw-------`. This is stricter
than several of the other tools in `key-generation.md` (e.g. `openssl ... -out aes256.key`, which
lands at the umask default and needs a manual `chmod 600`), but it is *not* a substitute for actual
passphrase encryption — anyone with read access to the file (root, a backup snapshot, another
process running as the same user) can read the key straight off disk.

## Bech32 Encoding

Both key values use [Bech32](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki)
encoding (per the age specification at age-encryption.org, which redirects to the formal spec on
[C2SP](https://github.com/C2SP/C2SP/blob/main/age.md)) — the same checksummed encoding scheme
Bitcoin's BIP173 defines for addresses, minus BIP173's data-length limit (age's payloads are longer
than a Bitcoin address's).

- **Public keys / recipients** use the human-readable prefix (HRP) `age`, giving the familiar
  `age1...` form (e.g. `age1wrmpanzx48kcvzn0zu3qgfqgpckq6ep3fhtfdmmlkzl8zddzff0s95ef23`).
  Post-quantum recipients use HRP `age1pq` instead (`age1pq1...`).
- **Secret keys / identities** use HRP `AGE-SECRET-KEY-`, giving `AGE-SECRET-KEY-1...`.
  Post-quantum identities use `AGE-SECRET-KEY-PQ-1...`.
- **Case rule**: per the Bech32 spec, a Bech32 string must be *all* uppercase or *all* lowercase —
  never mixed — and the checksum is always computed over the lowercase form regardless of which
  case is displayed. This is exactly why age's convention displays public keys lowercase
  (`age1...`) and secret keys uppercase (`AGE-SECRET-KEY-1...`): it's a visual convention layered
  on top of the same underlying encoding, chosen so the two key types are unmistakable at a glance
  (and so accidentally pasting a secret key where a public key is expected is visually obvious).
- **Checksum**: Bech32's built-in checksum means a single mistyped or corrupted character in either
  key value will (with high probability) be caught as invalid rather than silently accepted —
  useful when a key is transcribed by hand or read aloud, though in practice these values are long
  enough that copy-paste is the realistic path.

## Protecting the Identity File at Rest

Since `age-keygen` has no passphrase option of its own, protecting the generated identity file
means encrypting it *after the fact* with the separate `age` tool's own passphrase mode:

```fish
age -p -o age-key.txt.age age-key.txt
```

This produces a passphrase-encrypted copy of the identity file. Practical notes, gathered from
testing this locally:

- `age -p` prompts interactively for the passphrase via the controlling terminal (`/dev/tty`) — it
  cannot read the passphrase from a plain piped stdin in a non-interactive context (confirmed
  locally: piping a passphrase via `echo ... | age -p ...` inside a non-terminal context fails with
  `could not read passphrase: standard input is not a terminal, and /dev/tty is not available`).
  Scripting this requires either an actual pty or a tool built for that (e.g. `expect`), not a bare
  pipe.
- Once encrypted this way, the resulting `.age` file can itself be used directly as an identity
  file for `age -d -i age-key.txt.age ...` — `age`'s own `--help` text confirms "Passphrase
  encrypted age files can be used as identity files," so this doesn't require a separate decrypt
  step before use.
- The original plaintext `age-key.txt` should then be securely deleted (e.g. `shred`) once the
  encrypted copy is verified to work — otherwise the passphrase protection is moot.

## How the Output Is Consumed

(Brief per [Scope](#scope) — full `age` flag depth belongs in a separate `age` reference, not this
file.) The public key `age-keygen` prints or writes is meant to be handed to the `age` encryption
tool as a **recipient**:

```fish
# encrypt to one recipient given directly
age -r age1wrmpanzx48kcvzn0zu3qgfqgpckq6ep3fhtfdmmlkzl8zddzff0s95ef23 -o secret.age file.txt

# encrypt to every recipient listed in a file (one per line, '#' comments allowed)
age -R recipients.txt -o secret.age file.txt

# decrypt using the matching identity file
age -d -i age-key.txt -o file.txt secret.age
```

Verified end-to-end locally: a public key derived from a freshly generated identity (`age-keygen -y
sample-key.txt`) successfully encrypted a test string via `age -r <pubkey>`, and the matching
identity file decrypted it back via `age -d -i sample-key.txt` to the original plaintext. `-r` can
be repeated for multiple recipients (multi-recipient encryption — any one of the listed identities
can decrypt); `-R` does the file-list equivalent, useful when the recipient set is large or
maintained separately from the command line; `-i` for decryption can likewise be repeated, and
`age` silently ignores identity files that don't match the ciphertext, trying each in turn.

## Real-Machine Grounding: Arch vs. Debian

This machine runs Arch/Garuda with `age` **1.3.1** installed (`pacman -Qi age`: built December 2025,
depends only on `glibc`, 11.49 MiB installed). Cross-checked against
`man.archlinux.org/man/age-keygen.1`, which matches the locally installed man page exactly
(same December 2025 date, same flag set) — no divergence between local and upstream-mirrored Arch
docs.

Debian is a real divergence risk here, at two levels:

1. **Whether `age` is packaged at all.** Per `manpages.debian.org` and the upstream README's
   install table: `age` is available via plain `apt install age` on **Debian 12 (Bookworm) and
   later**, and on Ubuntu 22.04+. On **Debian 11 (Bullseye)**, it is *not* in the default repos and
   requires enabling `bullseye-backports` first. Anyone following `key-generation.md`'s
   `sudo apt install age` line on an older Debian install (Bullseye or earlier) will hit a
   package-not-found error unless they've added backports — this is the concrete gotcha the task
   flagged as likely, and it's confirmed real.
2. **Which version, and therefore which flags.** Debian's package versions lag noticeably behind
   upstream: Debian testing/unstable carry `age` 1.3.1 (current), but Debian **trixie** (the next
   stable at time of writing) carries **1.2.1** — a version that predates `-pq` entirely.
   Per upstream's own release notes, the post-quantum hybrid ML-KEM-768 + X25519 support (`-pq`,
   the `age1pq...`/`AGE-SECRET-KEY-PQ-1...` key forms, and `age-inspect(1)`) shipped in **age
   1.3.0**, released December 27, 2025. Anyone on a stable Debian install with an older packaged
   `age` will find `-pq` simply doesn't exist yet — `age-keygen -pq` will fail as an unrecognized
   flag rather than doing anything post-quantum-related. The plain `-o`/`-y`/`--version` behavior
   documented above, by contrast, has been stable across these versions and is safe to rely on
   regardless of which Debian release is in play.

## Use Cases

- A developer generates a fresh X25519 identity with `age-keygen -o age-key.txt` to encrypt
  personal files (backups, config with secrets, notes) for their own later decryption, replacing an
  ad hoc `gpg` or `openssl` workflow with a simpler single-purpose tool.
- A team sets up a shared encryption scheme where each member runs `age-keygen` once to produce
  their own personal identity, then publishes only the public key (via `age-keygen -y` on their own
  identity file, or by reading the `# public key:` comment) into a shared `recipients.txt` so
  anyone can encrypt a file to the whole team with a single `age -R recipients.txt` call.
- Someone who kept an old identity file but lost track of the matching public key runs
  `age-keygen -y old-key.txt` to re-derive and re-share the recipient value, without needing to
  regenerate (and thereby invalidate) the keypair.
- A user protects a freshly generated identity file at rest by immediately piping it through
  `age -p -o age-key.txt.age age-key.txt`, then deleting the plaintext original, so a stolen laptop
  or leaked backup doesn't hand over the raw private key.
- A CI/CD pipeline or automated backup script generates (or is provisioned with) an `age` identity
  ahead of time specifically so encryption/decryption in the pipeline can use `age -r`/`age -d -i`
  without any interactive passphrase prompt, trading the passphrase-at-rest protection above for
  automation convenience — a deliberate tradeoff that should be paired with strict filesystem
  permissions and, ideally, a dedicated non-personal key.
- A security-conscious user evaluates or adopts the post-quantum hybrid mode (`age-keygen -pq`) for
  identities meant to protect data with a long confidentiality shelf-life, accepting the much larger
  key size as the tradeoff for resistance to a future large-scale quantum adversary — while knowing
  this requires age 1.3.0+, so it isn't yet available on every Debian install by default (see
  [Real-Machine Grounding](#real-machine-grounding-arch-vs-debian)).
- Someone auditing or documenting a key management workflow inspects an existing identity file's
  three lines (`# created:`, `# public key:`, `AGE-SECRET-KEY-1...`) to confirm generation date and
  confirm which public key it corresponds to, without needing to run any tool at all — the file is
  self-describing plaintext.

## References

- `age-keygen(1)` — local man page, Arch package `age` 1.3.1 (`man age-keygen`; verified structurally
  identical to the upstream-mirrored copy below).
- `age-keygen -h` / `age --help` — local help output, same package/version, used to cross-check the
  man page (both agree; no divergence found).
- Arch Linux man page mirror: [man.archlinux.org/man/age-keygen.1](https://man.archlinux.org/man/age-keygen.1)
  — fetched and confirmed to match the local man page (same December 2025 date, same flags).
- Debian man page mirror (unstable/testing suite): [manpages.debian.org/unstable/age/age-keygen.1.en.html](https://manpages.debian.org/unstable/age/age-keygen.1.en.html)
  — used to confirm Debian's packaged version lag (1.2.1 on trixie vs. 1.3.1 upstream/Arch) and to
  cross-check the flag table; content otherwise matches.
- Official `age` project: [github.com/FiloSottile/age](https://github.com/FiloSottile/age)
  (README, install table, release notes) — used for OS/distro packaging status and the 1.3.0
  changelog entry introducing `-pq`.
- Formal age encryption format specification: [github.com/C2SP/C2SP/blob/main/age.md](https://github.com/C2SP/C2SP/blob/main/age.md)
  (canonically served from `age-encryption.org/v1`, which redirects there) — used for the Bech32
  encoding details (HRPs, case rule, checksum, BIP173 basis).
- [BIP173 (Bech32)](https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki) — the base
  encoding spec age's key format builds on, referenced by the C2SP spec above.
- Local hands-on verification (this session): generated a scratch X25519 identity and a scratch
  `-pq` identity in a temp directory (not committed, not under this repo's `generated-keys/`),
  confirmed file permissions (`0600` despite `umask 0022`), confirmed no-overwrite behavior on
  `-o`, confirmed `-y` round-trips correctly, and confirmed a full `age -r` / `age -d -i`
  encrypt-decrypt round trip against the generated key. All scratch files were deleted afterward.
