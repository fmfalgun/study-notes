# Tool Reference — ssh-keygen

Deep-dive companion to `key-generation.md`'s SSH keypair section (§5), which only exercises
`ssh-keygen -t ed25519 -f <path> -N "" -C "study-key"`. This file covers the full `ssh-keygen(1)`
surface — every generation, conversion, inspection, certificate, moduli, revocation, and signing
flag — so the earlier file's single invocation can be understood in its full context.

## Scope

`ssh-keygen` is inherently a key-lifecycle tool (generate → inspect → convert → rotate → revoke),
unlike `openssl`/`gpg` in this same documentation batch, so there's no hard exclusion boundary
here — the whole man page is covered. Depth is prioritized as follows, per the task that produced
this file:

1. **Key generation** (`-t`, `-b`, `-f`, `-N`, `-C`, `-o`, `-a`, all six `-t` key types, `-A` batch
   host-key generation) — deepest coverage, most relevant to day-to-day use.
2. **Format conversion / inspection** (`-y`, `-p`, `-l`/`-E`, `-e`/`-i`/`-m`, `-B`) — second
   priority, still covered with full flag tables and gotchas.
3. **`known_hosts` file operations** (`-R`, `-F`, `-H`) — covered for completeness, but lighter
   depth. These are more accurately **SSH client hygiene** than key *generation* — they mutate a
   trust-store file, not a key — and are included here because they live in the same binary and
   man page, not because they belong to the generation workflow proper.

Below priority 3, the man page also documents **certificates** (CA-signing), **DH-GEX moduli
generation**, **key revocation lists (KRLs)**, and **SSH signatures** (`ssh-keygen -Y ...`, a
general-purpose signing tool riding on SSH keys). These are covered fully (every flag/option is
enumerated — nothing skipped for brevity) but with terser notes than priorities 1–2, reflecting
that a cybersecurity developer reaches for them far less often than plain key generation.

## Index

- [Key Types and the `-t` Flag](#key-types-and-the--t-flag)
- [Key Generation Flags](#key-generation-flags)
- [Batch Host-Key Generation (`-A`)](#batch-host-key-generation--a)
- [FIDO/Security-Key-Backed Keys](#fidosecurity-key-backed-keys)
- [Format Conversion and Inspection](#format-conversion-and-inspection)
- [`known_hosts` File Operations](#known_hosts-file-operations)
- [Certificates (CA-Signed Keys)](#certificates-ca-signed-keys)
- [Moduli Generation (DH-GEX)](#moduli-generation-dh-gex)
- [Key Revocation Lists (KRLs)](#key-revocation-lists-krls)
- [SSH Signatures (`-Y`) and Allowed Signers](#ssh-signatures--y-and-allowed-signers)
- [Global / Miscellaneous Flags](#global--miscellaneous-flags)
- [Use Cases](#use-cases)
- [References](#references)

## Key Types and the `-t` Flag

`ssh-keygen -t <type>` selects the key algorithm. Run with no arguments at all, `ssh-keygen`
defaults to generating an **Ed25519** key (and will interactively prompt for
`~/.ssh/id_ed25519` — see the `-f` gotcha below).

| `-t` value | Algorithm | Default/allowed size (`-b`) | Notes |
|---|---|---|---|
| `ed25519` | EdDSA over Curve25519 | fixed; `-b` ignored | the default when `-t` is omitted; modern recommendation for new keys — small, fast, deterministic signatures, no weak-randomness footgun |
| `rsa` | RSA | min 1024, default **3072**, no fixed upper bound (subject to practical limits) | 3072 is "generally considered sufficient" per the man page; the `key-generation.md` openssl example used 2048 as a security *floor* — `ssh-keygen`'s own default is already above that floor |
| `ecdsa` | ECDSA over NIST curves | `-b` selects **one of 256, 384, or 521** — any other value fails outright | inherits the NIST-curve provenance concerns noted in `key-generation.md`'s openssl ECDSA section |
| `ecdsa-sk` | ECDSA, FIDO/U2F-hardware-backed | fixed; `-b` ignored | private key material never leaves the authenticator; see [FIDO section](#fidosecurity-key-backed-keys) |
| `ed25519-sk` | Ed25519, FIDO2-hardware-backed | fixed; `-b` ignored | same hardware-backed model as `ecdsa-sk`, modern curve |
| `mldsa44-ed25519` | **Experimental** composite post-quantum: ML-DSA-44 + Ed25519 hybrid | fixed; `-b` ignored | added in **OpenSSH 10.4** (2026-07-06) — brand new at the time of writing; verify support before relying on it in any script targeting older hosts (see [References](#references)) |

**Gotcha — `dsa` is gone.** Older documentation and scripts reference `-t dsa`. DSA support was
fully **removed** from OpenSSH in version **10.0** (2025-04-09), completing a deprecation that
began in 2015 (DSA disabled by default in `sshd`). It does not appear in this machine's `-t` list
at all. Debian bookworm (stable, OpenSSH 9.2p1) still lists `dsa` as an accepted `-t` value in its
man page — if working across a fleet that mixes Debian stable with anything OpenSSH ≥10.0, do not
assume `-t dsa` behaves the same everywhere, and don't use it regardless (it's weak and obsolete).

**Real-machine grounding:** this machine (Arch/Garuda, `openssh 10.4p1-3`) matches
`man.archlinux.org`'s ssh-keygen(1) page exactly, including `mldsa44-ed25519`. Debian **testing**
(10.3p1, as of this writing) supports every type except `mldsa44-ed25519` — it's one release
behind. Debian **stable** (bookworm, 9.2p1) is further behind still: it has `ecdsa-sk`/`ed25519-sk`
but predates the 10.0 DSA removal, so `dsa` is still present (deprecated, not gone). Expect
`mldsa44-ed25519` to be unavailable on essentially any non-bleeding-edge system for some time.

## Key Generation Flags

Full flag/option table for the default (key-generation) invocation mode of `ssh-keygen`:

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-t <type>` | key algorithm | see [table above](#key-types-and-the--t-flag); omitting it defaults to `ed25519` |
| `-b bits` | key size in bits | meaning depends on `-t` — see table above; ignored outright for fixed-size types |
| `-f filename` | private key output path (public key written to `filename.pub`) | **always pass this explicitly.** Without it, `ssh-keygen` interactively prompts with a default of `~/.ssh/id_<type>` — confirmed by direct test on this machine: a bare invocation printed `Enter file in which to save the key (~/.ssh/id_ed25519):` and would silently overwrite an existing real key if confirmed. This is exactly the risk `key-generation.md` calls out. |
| `-N new_passphrase` | sets the passphrase on the new key | `-N ""` = no passphrase (security-critical: private key protection then rests entirely on filesystem permissions — same adversary model as Exercise 1). Host keys generated by `-A` are *always* given an empty passphrase, by design — an unattended `sshd` can't prompt for one at boot. |
| `-C comment` | sets the comment embedded in the public key / private key metadata | **security-relevant default to flag explicitly:** if omitted, the comment is auto-set to `user@host` — i.e. your local username and hostname get baked into the `.pub` file and will propagate into every `authorized_keys` file the key is added to, and into server auth logs. Minor but real information leak (username/hostname enumeration). Always pass `-C` explicitly with a non-identifying label, exactly as `key-generation.md` does (`"study-key"`). |
| `-c` | *change* (not set) the comment on an **existing** key pair | prompts for the private key file, its passphrase (if any), and the new comment. Distinct from `-C`, which only applies during generation (or with `-c`/`-p`). |
| `-a rounds` | KDF (bcrypt_pbkdf) rounds used when encrypting the private key at rest | default **16**. Higher = slower passphrase verification but stronger resistance to offline brute-force if the encrypted key file is stolen. Only matters if the key has a passphrase (`-N` non-empty) — an unencrypted key has no KDF to strengthen. |
| `-Z cipher` | cipher used to encrypt the OpenSSH-format private key file | default **`aes256-ctr`**. Full list of available ciphers via `ssh -Q cipher`. Only relevant for OpenSSH-format keys with a passphrase set. |
| `-m key_format` | output format for the private key | default is OpenSSH's own format (bcrypt-KDF-protected, since OpenSSH 7.8, 2018-08). Set `-m PEM` to write the older PEM format instead (legacy interop; weaker at-rest protection, no embedded comment). Also governs `-i`/`-e`/`-p` — see [conversion section](#format-conversion-and-inspection). |
| `-o` | *(historical)* force new-format private key | **No longer a documented flag as of OpenSSH 10.4p1** — it does not appear in this machine's man page options list at all. Historically (pre-7.8) the new bcrypt-KDF OpenSSH private-key format was opt-in via `-o`; OpenSSH 7.8 made that format the unconditional default (opt back out to legacy PEM via `-m PEM` instead). If encountering `-o` in an old script, it is now a no-op left over from that transition — treat any reliance on it as legacy and prefer explicit `-m` if a specific format is required. |
| `-q` | silence normal output | suppresses the progress/summary messages; errors still surface |
| `-w provider` | path to an alternate FIDO middleware library | overrides the built-in USB HID support when generating `-sk` keys; see [FIDO section](#fidosecurity-key-backed-keys) |
| `-A` | batch-generate all default host key types | see [dedicated section](#batch-host-key-generation--a) below |

**Method — generating a standard user key** (mirrors `key-generation.md` exactly, generalized):

```fish
ssh-keygen -t ed25519 -f <path> -N "" -C "<label>"
```

Swap `-t ed25519` for any other supported type; add `-a <rounds>` if hardening KDF rounds for a
passphrase-protected key; add `-Z <cipher>` to pin a specific at-rest cipher.

## Batch Host-Key Generation (`-A`)

`ssh-keygen -A` generates host keys of **all default key types** (per the man page on this
machine: rsa, ecdsa, mldsa44-ed25519, and ed25519 — the exact "default" set tracks whatever the
installed OpenSSH version considers current) for any type that doesn't already have a key file
present. This is what `/etc/rc`-style init scripts and package post-install hooks use to provision
a fresh host's SSH identity.

| Flag combination | Behavior |
|---|---|
| `-A` alone | generates missing host keys at their default system paths (`/etc/ssh/ssh_host_<type>_key`), default bit sizes, default (empty) comment, **empty passphrase always** (a daemon can't prompt at boot) |
| `-A` with `-f <prefix>` | the `-f` argument is used as a path *prefix* rather than the literal default system path — useful for generating a throwaway host-key set into a scratch directory instead of `/etc/ssh/` |
| `-A` with `-a <rounds>` | applies the given KDF rounds to any keys `-A` generates (moot given the empty passphrase, but accepted) |

**Concerning fact:** `-A` will skip any key type whose file already exists — it never silently
overwrites. Re-running it after a partial provisioning failure is safe.

## FIDO/Security-Key-Backed Keys

`-t ecdsa-sk` and `-t ed25519-sk` generate keys where the private key material is split: a "key
handle" lives in the on-disk private key file, and a per-device secret lives inside the hardware
authenticator (YubiKey, etc.) and can never be exported. The two combine at authentication time.
Authenticators generally require a physical touch/tap to authorize each use.

These types accept extra generation-time options via `-O key=value` (repeatable):

| `-O` option | Meaning | Notes |
|---|---|---|
| `application` | overrides the default FIDO application/origin string `ssh:` | must still begin with `ssh:`; useful for host- or domain-specific resident keys |
| `challenge=path` | supplies a challenge string for out-of-band enrollment protocols | random challenge used by default if omitted |
| `device` | pins a specific `fido(4)` device rather than letting middleware auto-select | useful with multiple authenticators attached |
| `no-touch-required` | generates a key that does not require a touch event per signature | **`sshd` refuses such signatures by default** unless explicitly overridden via an `authorized_keys` option — weakens the "something you have + do" model back toward "something you have" |
| `resident` | stores the key handle **on** the authenticator itself, not just on disk | portable across machines via `ssh-add` (see `-K` below); typically requires a PIN set on the authenticator; **increases blast radius if the authenticator itself is stolen**, since both halves then live on one device |
| `user` | associates a username with a resident key | overrides the empty default; useful when generating multiple resident keys for the same `application` |
| `verify-required` | requires user verification (PIN or biometric) per signature, not just presence | not all authenticators support this |
| `write-attestation=path` | records the attestation data returned during generation | discarded by default; the man page flags this data as "potentially sensitive" — treat the written file accordingly |

| Related flag | Meaning |
|---|---|
| `-K` | downloads **resident** keys off an attached FIDO authenticator, writing private/public key files to the current directory. If multiple authenticators are attached, keys come from whichever is touched first. |
| `-w provider` | path to alternate FIDO middleware library (default: built-in USB HID support) |
| `SSH_SK_PROVIDER` (environment variable) | same override as `-w`, applied when *loading* (not generating) `-sk` keys |

## Format Conversion and Inspection

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-y` | read a private OpenSSH-format key file, print the corresponding **public** key to stdout | use when a `.pub` file has been lost but the private key survives |
| `-p` | change the passphrase of an existing private key (does **not** generate a new key) | prompts for the key file, old passphrase, and new passphrase (twice); combine with `-N`/`-P` to script it non-interactively, and with `-m PEM` to simultaneously convert format while rotating passphrase |
| `-P passphrase` | supplies the **old** passphrase (paired with `-p`) | avoid on real shared machines — command-line arguments leak via shell history and `/proc/<pid>/cmdline`, same caution `key-generation.md` gives for `openssl kdf`'s `pass:` option |
| `-l` | show the fingerprint of a specified public (or private) key file | combine with `-v` for an ASCII-art visual fingerprint; combine with `-E` to pick the hash algorithm |
| `-E fingerprint_hash` | hash algorithm for fingerprint display: `md5` or `sha256` | default is `sha256`; `md5` fingerprints are the older/shorter style still seen in some legacy documentation and server banners |
| `-B` | show the **bubblebabble** digest of a key file | a different, pronounceable-word-based encoding of the key digest — historically used for reading a fingerprint aloud over a low-bandwidth voice channel (e.g. a phone call) as an out-of-band verification method |
| `-e` | export: read a private or public OpenSSH key, print a public key in another format to stdout | default export format is `RFC4716`; format selectable via `-m` |
| `-i` | import: read an unencrypted private (or public) key in a foreign format, print an OpenSSH-compatible key to stdout | default import format is `RFC4716`; this is the counterpart to `-e` |
| `-m key_format` | selects the format used by `-i`, `-e`, and `-p` | valid values: `RFC4716` (RFC 4716/SSH2 public or private key), `PKCS8` (public or private key), `PEM` (public key only, or legacy private-key output at generation time) |
| `-L` | print the contents of one or more **certificates** | see [Certificates](#certificates-ca-signed-keys) |
| `-r hostname` | print the SSHFP DNS resource record for a given public key file, named for `hostname` | pair with `-g` for the generic DNS record format; pair with `-O hashalg=sha1\|sha256` to pick the SSHFP hash algorithm (default: prints both) |
| `-g` | use generic DNS record format when printing SSHFP records via `-r` | only meaningful alongside `-r` |

**Method — extracting a fingerprint before trusting a key:**

```fish
ssh-keygen -l -E sha256 -f <path-to-pubkey-or-privkey>
```

**Method — converting a foreign-format key into OpenSSH's native format:**

```fish
ssh-keygen -i -m PEM -f <foreign-key-file> > converted_key
```

## `known_hosts` File Operations

As stated in [Scope](#scope), these are SSH-client-hygiene operations on a *trust store* file, not
key generation — included for completeness, lighter depth intentionally.

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-F hostname` or `-F [hostname]:port` | search a `known_hosts` file for entries matching `hostname` (optionally with port), listing any found | defaults to the user's real `known_hosts` unless `-f <file>` overrides the target — be deliberate with `-f` on a shared/study machine to avoid touching the real file |
| `-H` | hash an entire `known_hosts` file in place — replaces all plaintext hostnames/addresses with hashed representations | the **original file is preserved with a `.old` suffix**, not destroyed; safe to run on a file that already mixes hashed and unhashed entries — it leaves existing hashed entries untouched. Purpose: if the file leaks, an attacker can't read off which hosts you connect to. |
| `-R hostname` or `-R [hostname]:port` | remove all keys belonging to the given host from a `known_hosts` file | the standard fix after rebuilding a server or rotating its host key and hitting SSH's "REMOTE HOST IDENTIFICATION HAS CHANGED" warning — clears the stale entry so a fresh connection can re-trust-on-first-use |

`-F` combined with `-H` prints found entries in hashed form; `-F` combined with `-l` shows the
fingerprint of found keys rather than the raw key material.

## Certificates (CA-Signed Keys)

OpenSSH certificates are a distinct, simpler format from X.509 (`ssl(8)`) certificates — a public
key plus identity/principal information plus certificate options, all signed by a CA key. Clients/
servers configured to trust the CA key then trust any certificate it signs, instead of needing to
individually trust every user/host key.

| Flag | Meaning |
|---|---|
| `-s ca_key` | sign (certify) a public key using the given CA private key, producing a certificate |
| `-I certificate_identity` | a free-text key identifier embedded in the cert, logged by the server on use, and usable for revocation |
| `-n principals` | comma-separated list of usernames (user cert) or hostnames (host cert, wildcards allowed) the certificate is valid for |
| `-h` | signs a **host** certificate instead of a user certificate |
| `-V validity_interval` | start:end validity window — see time-format table below; default (unset) is Unix epoch to the distant future |
| `-z serial_number` | embeds a serial number distinguishing this cert from others signed by the same CA; prefix with `+` to auto-increment across multiple certs signed in one command; default `0` |
| `-U` | indicates the CA key is hosted in a running `ssh-agent(1)` rather than a plain file |
| `-D pkcs11_provider` | indicates the CA key resides on a PKCS#11 hardware token; the CA is then identified by its public half |

`-V`'s time syntax (start and end separated by `:`):

| Form | Meaning |
|---|---|
| `always` (start only) | no specified start — valid from the epoch |
| `forever` (end only) | no specified end |
| `YYYYMMDD` / `YYYYMMDDHHMM[SS]` | absolute date/time in the **system** time zone |
| same with trailing `Z` | absolute date/time in **UTC** |
| `-<interval>` (start) / `+<interval>` (end) | relative to "now", using `sshd_config(5)`'s TIME FORMATS interval syntax (e.g. `52w1d` = 52 weeks 1 day) |
| `0x<hex>` | raw seconds-since-epoch in hex |

Example intervals straight from the man page: `+52w1d` (now → +52w1d), `-4w:+4w` (4 weeks ago →
4 weeks ahead), `-1d:20110101` (yesterday → a fixed date), `-1m:forever` (a minute ago → never
expiring).

Certificate **options** (set via `-O`, user certs only — host certs currently accept none):

| Option | Meaning |
|---|---|
| `clear` | clears the default permission set, so options can be added individually from a blank slate |
| `critical:name[=contents]` | arbitrary critical option — an unrecognizing server/client **refuses** the certificate |
| `extension:name[=contents]` | arbitrary extension — an unrecognizing server/client just ignores it |
| `force-command=command` | forces execution of `command` regardless of what the user requests |
| `no-agent-forwarding`, `no-port-forwarding`, `no-pty`, `no-user-rc`, `no-x11-forwarding` | disable each named feature (all are *permitted by default* otherwise) |
| `permit-agent-forwarding`, `permit-port-forwarding`, `permit-pty`, `permit-user-rc`, `permit-X11-forwarding` | explicitly (re-)allow each feature |
| `no-touch-required` | (FIDO `-sk` keys only) don't require touch presence per signature |
| `source-address=address_list` | restricts which source CIDR ranges may present this certificate |
| `verify-required` | (FIDO `-sk` keys only) requires PIN/biometric verification per signature |

**Method — issuing a user certificate:**

```fish
ssh-keygen -s /path/to/ca_key -I some-id -n someuser /path/to/user_key.pub
```

Output lands at `/path/to/user_key-cert.pub`. Host certificates are the same shape with `-h` added
and hostnames (wildcards allowed) in `-n`.

## Moduli Generation (DH-GEX)

A two-step process for producing custom Diffie-Hellman Group Exchange parameters for
`/etc/ssh/moduli` (format documented in `moduli(5)`): first generate fast-but-memory-intensive
candidates, then screen them with a slow, CPU-intensive primality/suitability test.

| Flag | Meaning |
|---|---|
| `-M generate` | generates candidate primes to an output file |
| `-M screen` | screens candidates (from stdin or `-f <file>`) for suitability as safe (Sophie Germain) primes with acceptable generators |

`-O` suboptions for moduli generation/screening:

| Option | Meaning |
|---|---|
| `bits=number` | desired candidate prime length, used with `-M generate` |
| `start=hex-value` | overrides the (otherwise random) starting point for candidate search |
| `lines=number` | stop screening after this many input lines |
| `start-line=line-number` | start screening at a given line number |
| `checkpoint=filename` | records the last-processed line so a restarted screening job can resume |
| `generator=value` | requests a specific DH generator (`2`, `3`, or `5`) rather than automatic selection |

Screening defaults to 100 primality tests per candidate unless overridden by `generator=`/related
options. Example from the man page:

```
ssh-keygen -M generate -O bits=2048 moduli-2048.candidates
ssh-keygen -M screen -f moduli-2048.candidates moduli-2048
```

## Key Revocation Lists (KRLs)

KRLs are compact binary files (as little as one bit per certificate, if revoked by serial number)
listing revoked keys/certificates.

| Flag | Meaning |
|---|---|
| `-k` | generate a new KRL at the path given by `-f`, from one or more input files (KRL-spec lines or plain public keys, one per line) |
| `-u` | (with `-k`) merge into an **existing** KRL instead of overwriting it |
| `-Q` | test whether given keys are revoked by a KRL; add `-l` to also print the KRL's contents; exits non-zero if any key is revoked (or on error) |
| `-s ca_public` | (in KRL mode) the CA public key used to revoke certs directly by key ID/serial number, without needing the full certificate |
| `-z version_number` | (in KRL mode; distinct meaning from the certificate `-z`) sets the KRL's version number |

KRL-specification directives (one per line, `directive: value`):

| Directive | Meaning |
|---|---|
| `serial: serial_number[-serial_number]` | revokes one cert serial, or an inclusive range; requires `-s` on the command line |
| `id: key_id` | revokes by certificate key-ID string; requires `-s` |
| `key: public_key` | revokes the specific key outright (a certificate here is revoked as a plain public key) |
| `sha1: public_key` | revokes by the key's SHA1 hash |
| `sha256: public_key` | revokes by SHA256 hash — **not supported by OpenSSH before 7.9** |
| `hash: fingerprint` | revokes by a SHA256 fingerprint as produced by `sshd` auth logs or `ssh-keygen -l` — **not supported before 7.9** |

## SSH Signatures (`-Y`) and Allowed Signers

A general-purpose file/message signing facility riding on ordinary SSH keys — an alternative to
GPG for signing arbitrary data (e.g. git commit signing, release-artifact signing).

| Flag | Meaning |
|---|---|
| `-Y sign` | sign file(s) on the command line (or stdin if none given) with the key from `-f`; output is `<file>.sig` per input file, or stdout for stdin input. Requires `-n <namespace>`. |
| `-Y verify` | verify a signature: needs `-s <signature_file>`, `-I <signer_identity>`, `-n <namespace>`, `-f <allowed_signers_file>`; optionally `-r <revocation_file>` (a KRL or a one-per-line pubkey list). Zero exit status on success. |
| `-Y check-novalidate` | checks a signature's *structure* only (not whether it comes from an authorized signer) — needs `-n <namespace>` and `-s <signature_file>`, message on stdin |
| `-Y find-principals` | given a signature (`-s`) and allowed-signers file (`-f`), prints the matching principal(s) |
| `-Y match-principals` | given an identity (`-I`) and allowed-signers file (`-f`), prints matching principals |

`-n <namespace>` is mandatory for signing/verification and exists specifically to prevent
signature confusion across different domains of use — e.g. a signature meant for `file` signing
should not validate as an `email` signature. Convention for custom namespaces:
`NAMESPACE@YOUR.DOMAIN`.

`-O` suboptions specific to `-Y` operations:

| Option | Meaning |
|---|---|
| `hashalg=algorithm` | `sha256` or `sha512` (default) — hash used on the message before signing |
| `print-pubkey` | after successful verification, also print the full public key to stdout |
| `verify-time=timestamp` | validate as of a given time instead of "now" (`YYYYMMDD[Z]` or `YYYYMMDDHHMM[SS][Z]`) |

**Allowed signers file** (used as `-f` for `-Y verify`/`find-principals`/`match-principals`):
one entry per line, space-separated fields: `principals options keytype base64-key`. Blank lines
and `#`-prefixed lines are comments.

| Field/option | Meaning |
|---|---|
| `principals` | pattern-list of `USER@DOMAIN` identities accepted for signing (comma-separated) |
| `cert-authority` | marks this key as a trusted CA for signatures made by certs it signed |
| `namespaces=namespace-list` | restricts this key to only the listed signature namespaces |
| `valid-after=timestamp` / `valid-before=timestamp` | bounds the key's acceptance window |

Example straight from the man page:

```
# Comments allowed at start of line
user1@example.com,user2@example.com ssh-rsa AAAAX1...
# A certificate authority, trusted for all principals in a domain.
*@example.com cert-authority ssh-ed25519 AAAB4...
# A key that is accepted only for file signing.
user2@example.com namespaces="file" ssh-ed25519 AAA41...
```

## Global / Miscellaneous Flags

| Flag | Meaning |
|---|---|
| `-q` | silences normal progress/summary output (errors still print) |
| `-v` | verbose/debug output; repeatable up to `-vvv` (max verbosity 3) — primarily useful debugging moduli generation |
| `-D pkcs11` | outside certificate/KRL contexts, downloads public keys from a PKCS#11 token directly |

**Environment variable:**

| Variable | Meaning |
|---|---|
| `SSH_SK_PROVIDER` | path to the FIDO middleware library used when *loading* `-sk` keys (the load-time counterpart to generation-time `-w`) |

**Default file locations** (never used automatically by `ssh-keygen` itself — offered only as
interactive defaults; `ssh(1)` is what actually reads them at connection time):

```
~/.ssh/id_ecdsa            ~/.ssh/id_ecdsa.pub
~/.ssh/id_ecdsa_sk         ~/.ssh/id_ecdsa_sk.pub
~/.ssh/id_ed25519          ~/.ssh/id_ed25519.pub
~/.ssh/id_ed25519_sk       ~/.ssh/id_ed25519_sk.pub
~/.ssh/id_mldsa44-ed25519  ~/.ssh/id_mldsa44-ed25519.pub
~/.ssh/id_rsa              ~/.ssh/id_rsa.pub
/etc/ssh/moduli            # DH-GEX groups, format in moduli(5)
```

This is precisely the default-path mechanism `key-generation.md` warns about: any bare
`ssh-keygen` invocation without `-f` targets one of these real paths.

## Use Cases

- Generating a brand-new SSH keypair for a personal workstation so it can authenticate to a remote
  server with public-key auth instead of a password.
- Rotating the passphrase on an existing private key, using `ssh-keygen -p`, without regenerating
  the underlying key material or needing to redistribute the public key anywhere.
- Checking a server's host-key fingerprint out of band (over a phone call, a trusted chat channel,
  or a hardware console) before accepting it into `known_hosts`, using `ssh-keygen -l -E sha256`.
- Extracting a public key from a private key file, using `ssh-keygen -y`, when the corresponding
  `.pub` file has been lost or was never generated in the first place.
- Converting a key exported from a commercial SSH client, or an old-style PEM private key, into
  OpenSSH's native private key format so it works cleanly with a modern `ssh`/`sshd`.
- Batch-generating a fresh set of host keys during initial provisioning of a new server or a
  container/VM image, using `ssh-keygen -A`.
- Removing a stale or now-untrusted host entry from `~/.ssh/known_hosts`, using `ssh-keygen -R`,
  after a server has been rebuilt or its host key rotated and the client is warning about identity
  mismatch.
- Hashing an entire `known_hosts` file with `ssh-keygen -H` so that a stolen laptop's `known_hosts`
  doesn't reveal which hosts and addresses its owner regularly connects to.
- Generating a FIDO2/U2F hardware-security-key-backed SSH key (`-t ed25519-sk` or `-t ecdsa-sk`) so
  that private key material never leaves the physical token, even if the host machine is
  compromised.
- Issuing a short-lived, CA-signed SSH certificate for a user or a host as part of a
  certificate-based SSH authentication rollout, using `ssh-keygen -s`, instead of distributing raw
  public keys to every server's `authorized_keys`.
- Checking whether a specific key or certificate has already been revoked by an organization's Key
  Revocation List before deciding to trust it, using `ssh-keygen -Q`.
- Cryptographically signing an arbitrary file (a release artifact, a document, a git object) with
  an existing SSH key and later verifying that signature, using `ssh-keygen -Y sign` and
  `-Y verify`, as a GPG alternative that reuses keys already in daily SSH use.
- Generating custom Diffie-Hellman moduli for `/etc/ssh/moduli` on a hardened server that wants to
  avoid relying solely on the vendor-shipped, widely-shared DH group set.
- Displaying a key's bubblebabble digest, using `ssh-keygen -B`, as a more human-pronounceable
  alternative to a raw hex fingerprint for verbal out-of-band key verification.
- Downloading the public keys resident on a PKCS#11 hardware token, using `ssh-keygen -D`, to use
  as an SSH identity backed by that token.
- Changing the embedded comment on an existing key pair with `ssh-keygen -c`, e.g. to correct a
  key that was generated with the leaky default `user@host` comment without deliberately setting
  `-C`.

## References

- `ssh-keygen(1)` — local manual page, this machine (Arch/Garuda, `openssh 10.4p1-3`), read via
  `man ssh-keygen`. Verified structurally identical to the Arch Linux web-hosted copy below.
- [man.archlinux.org/man/ssh-keygen.1](https://man.archlinux.org/man/ssh-keygen.1) — cross-checked;
  confirms this machine's local page (OpenSSH 10.4p1-3, includes `mldsa44-ed25519`, RSA default
  3072 bits, `-a` default 16 rounds).
- [manpages.debian.org — bookworm (stable), openssh-client](https://manpages.debian.org/bookworm/openssh-client/ssh-keygen.1.en.html) —
  cross-checked; OpenSSH 9.2p1, still lists `dsa` as a `-t` value (pre-10.0 removal), no
  `mldsa44-ed25519`.
- [manpages.debian.org — testing, openssh-client](https://manpages.debian.org/testing/openssh-client/ssh-keygen.1.en.html) —
  cross-checked; OpenSSH 10.3p1, has `ecdsa-sk`/`ed25519-sk`, no `mldsa44-ed25519` (one release
  behind this machine).
- [openssh.org/releasenotes.html](https://www.openssh.org/releasenotes.html) — cross-checked for
  the `mldsa44-ed25519` addition (OpenSSH 10.4, 2026-07-06) and the DSA removal (OpenSSH 10.0,
  2025-04-09). Note: `www.openssh.com/releasenotes.html` redirects here (`.com` → `.org`).
- [openssh.org/txt/release-7.8](https://www.openssh.org/txt/release-7.8) — cross-checked for the
  origin of the `-o`/new-private-key-format transition: OpenSSH 7.8 made the OpenSSH-native
  private key format the default (`ssh-keygen(1): write OpenSSH format private keys by default
  instead of using OpenSSL's PEM format`), with `-m PEM` retained as the opt-out.
- RFC 4716, *The Secure Shell (SSH) Public Key File Format* (2006) — referenced by the man page for
  the `-e`/`-i` default export/import format.
