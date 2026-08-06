# Tool Reference — openssl

Companion to `key-generation.md`. That file runs a curated set of `openssl` subcommands to
produce one real sample of each key type in section 0's tooling analysis; this file documents
those specific subcommands in depth — full flag coverage, defaults, and gotchas — as reference
material to read alongside (not instead of) the hands-on exercise.

## Scope

`openssl` is a general-purpose cryptography toolkit and CLI with dozens of subcommands covering
TLS handshake testing, certificate chain verification, PKCS#12 bundling, S/MIME, CA operations,
benchmarking, and more. Documenting all of it is a separate, much larger undertaking than what
`key-generation.md` needs. This file is scoped to **exactly the subcommands that file invokes, or
that sit one step away from them in the same key-generation workflow**:

- **`openssl rand`** — generates the raw random bytes used as the AES-256 symmetric key.
- **`openssl genpkey`** — generates RSA, Ed25519, and X25519 private keys.
- **`openssl pkey`** — derives/extracts a public key from a private key produced by `genpkey`.
- **`openssl ecparam`** — generates EC domain parameters and, with `-genkey`, the P-256 ECDSA
  private key itself (the EC equivalent of `genpkey`, used because P-256 keygen was exercised via
  the parameter-file-style tool rather than `genpkey -algorithm EC`).
- **`openssl ec`** — derives/extracts a public key from the EC private key `ecparam` produced (the
  EC-specific counterpart to `pkey`).
- **`openssl req -x509 ...`** — **self-signed certificate generation only.** Covered here purely
  as "turn a fresh key into a self-signed X.509 cert in one step." The much larger CSR-to-CA
  submission workflow that `req` primarily exists for (generating a CSR *without* `-x509`,
  submitting it to a CA, `openssl ca` signing it) is explicitly **not** covered.
- **`openssl kdf`** — derives a symmetric key from a password via PBKDF2.

**Explicitly out of scope — not documented here, and deliberately so:** `openssl enc` (symmetric
encryption/decryption of data, as opposed to key generation), `openssl dgst` (hashing/signing
arbitrary data), `openssl x509` (certificate inspection and verification — note this is distinct
from `req -x509`, which *creates* a cert; `x509` the subcommand *reads* one), `openssl pkcs12`
(bundling keys+certs into `.p12`/`.pfx` files), `openssl s_client` / `openssl s_server` (live TLS
connection testing), `openssl ca` (the actual CA-signing workflow that a real CSR would go
through), `openssl ts` (RFC 3161 timestamping), `openssl cms` / `openssl smime` (S/MIME message
encryption/signing), `openssl engine` (legacy hardware/engine integration, deprecated since
3.0 in favor of providers), `openssl speed` (benchmarking), `openssl verify` (chain verification),
`openssl crl` (certificate revocation lists), and any CSR-to-CA or TLS-connection-testing
workflow in general. If a future exercise needs any of those, they warrant their own reference
file — bolting them onto this one would blur the "what does `key-generation.md` actually run"
boundary this file exists to preserve.

## Index

- [`openssl rand`](#openssl-rand)
- [`openssl genpkey`](#openssl-genpkey)
- [`openssl pkey`](#openssl-pkey)
- [`openssl ecparam`](#openssl-ecparam)
- [`openssl ec`](#openssl-ec)
- [`openssl req` (self-signed certs only)](#openssl-req-self-signed-certs-only)
- [`openssl kdf`](#openssl-kdf)
- [Use Cases](#use-cases)
- [References](#references)

## `openssl rand`

Generates `num` pseudo-random bytes using a cryptographically secure pseudo-random number
generator (CSPRNG), via the `RAND_bytes(3)` function. `RAND_bytes(3)` provides a 256-bit security
level *provided* it successfully seeded itself from a trusted OS entropy source — if that seeding
fails, the command exits with a nonzero error code rather than silently falling back to weaker
randomness.

**Syntax:** `openssl rand [options] num[K|M|G|T]`

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `num` (positional, required) | number of random bytes to produce | may be suffixed `K`/`M`/`G`/`T` for KiB/MiB/GiB/TiB — these are **binary** multiples (K = 1024 bytes, not 1000) and the suffix letters are **case-sensitive** |
| `max` (in place of `num`) | request the maximum number of bytes the CSPRNG can produce per instantiation | currently capped at 2^61 bytes per NIST SP 800-90C |
| `-out file` | write output to `file` instead of stdout | stdout output is raw binary by default (not printable) unless `-base64`/`-hex` is also given |
| `-base64` | base64-encode the output | |
| `-hex` | hex-encode the output | |
| `-engine id` | use the named engine for random generation | **deprecated since OpenSSL 3.0** — providers replaced engines |
| `-rand files` | seed the RNG from the given file(s) at startup | legacy pre-1.1.1 mechanism; rarely needed on a modern OS with a trusted entropy source; if used, should be paired with `-writerand` |
| `-writerand file` | write 256 bytes of seed state to `file` on exit | pairs with `-rand`; using the same seed file more than once is generally an error |
| `-provider name`, `-provider-path path`, `-provparam [name:]key=value`, `-propquery propq` | provider-loading and property-query controls | see `provider(7)`/`property(7)`; not needed for ordinary use |
| `-help` | usage message | |

**Concerning facts / gotchas:**
- Without `-out`, raw binary bytes go straight to stdout — piping that to a terminal will print
  garbage; redirect to a file or pipe, or use `-base64`/`-hex` for a text-safe encoding.
- The byte count you request is *exactly* the entropy/key strength you get for a directly-used
  symmetric key — `rand -out aes256.key 32` gives 32 bytes = 256 bits, matching the "AES-256"
  claim only because 32 was chosen deliberately.
- A file written by `-out` lands at your process's default umask — it is not created with
  restrictive permissions automatically; `chmod 600` immediately if the output is sensitive key
  material.
- Failure to seed from a trusted OS entropy source is a hard error, not a silent downgrade — this
  is a safety property worth knowing about, not just a gotcha.

## `openssl genpkey`

The modern, unified command for generating a private key or key pair for essentially any public-
key algorithm OpenSSL supports (RSA, RSA-PSS, EC, X25519, X448, Ed25519, Ed448, DH/DHX, DSA,
ML-DSA, ML-KEM). The man page explicitly recommends `genpkey` over the older algorithm-specific
utilities (`genrsa`, `gendsa`, etc.) because it can also pick up engine/provider-supplied
algorithms.

**Syntax:** `openssl genpkey [options] -algorithm alg [-pkeyopt opt:value ...] -out filename`

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-algorithm alg` | selects the public-key algorithm (`RSA`, `RSA-PSS`, `EC`, `X25519`, `X448`, `ED25519`, `ED448`, `ML-DSA`, `ML-KEM`, and `DH`/`DSA`/`EC` for `-genparam`) | must precede any `-pkeyopt` options on the command line; mutually exclusive with `-paramfile` |
| `-pkeyopt opt:value` | sets an algorithm-specific option (see tables below) | exact supported set depends on algorithm and implementation; list them with `openssl genpkey -algorithm XXX -help` |
| `-paramfile file` | supply pre-generated parameters (from `-genparam`) instead of an algorithm name; the algorithm is inferred from the file | mutually exclusive with `-algorithm`; must precede `-pkeyopt` |
| `-genparam` | generate a parameter set instead of a key | must precede `-algorithm`/`-paramfile`/`-pkeyopt`; only DH, DSA, EC support parameter generation; `-outform` is ignored when this is set |
| `-out filename` | write the private key here | if omitted, key goes to stdout |
| `-outpubkey filename` | additionally write the public key here | if omitted, the public key is not written at all |
| `-outform DER\|PEM` | output encoding | default `PEM`; ignored when `-genparam` is used |
| `-cipher` | encrypt the output private key with the named cipher (e.g. `-aes-128-cbc`) | accepts any name `EVP_get_cipherbyname()` recognizes |
| `-pass arg` | password source for the output file encryption | see pass-phrase argument forms below (`pass:`, `env:`, `file:`, `fd:`, `stdin`) |
| `-text` | also print an unencrypted plaintext dump of the key/params alongside the encoded form | |
| `-verbose` / `-quiet` | show/suppress "status dots" during generation | mutually exclusive intents |
| `-rand files`, `-writerand file` | legacy RNG seed file options | see `openssl rand` above |
| `-engine id` | **deprecated since OpenSSL 3.0** | |
| `-config configfile` | alternate OpenSSL config file | |
| `-provider*` / `-propquery` | provider-loading controls | |
| `-help` | usage message | |

**RSA / RSA-PSS key-generation `-pkeyopt` values:**

| Option | Meaning | Default |
|---|---|---|
| `rsa_keygen_bits:numbits` | key size in bits | **2048** if unspecified |
| `rsa_keygen_primes:numprimes` | number of primes in the key | 2 |
| `rsa_keygen_pubexp:value` | public exponent (decimal, or hex with `0x` prefix) | 65537 |
| `rsa_pss_keygen_md:digest` (RSA-PSS only) | restricts the key to signing with this digest | unrestricted by default |
| `rsa_pss_keygen_mgf1_md:digest` (RSA-PSS only) | restricts the MGF1 digest | unrestricted by default |
| `rsa_pss_keygen_saltlen:len` (RSA-PSS only) | minimum salt length, once restricted | unrestricted by default |

**EC key/parameter-generation `-pkeyopt` values:**

| Option | Meaning | Default |
|---|---|---|
| `ec_paramgen_curve:curve` | curve to use (OpenSSL accepts NIST names like `P-256`, or SECG names like `prime256v1`/`secp384r1`) | none — must be specified |
| `ec_param_enc:encoding` | `named_curve` (OID reference) or `explicit` (parameters spelled out in full) | `named_curve` |

**ML-DSA / ML-KEM `-pkeyopt` values (OpenSSL ≥ 3.5 only):**

| Option | Meaning | Gotcha |
|---|---|---|
| `hexseed:seed` | derive the key deterministically from a 32-byte (ML-DSA) or 64-byte (ML-KEM) hex seed | if other users/processes can see this command's argv, the seed — and therefore the secret key — may leak; man page explicitly recommends avoiding this outside of tests |

**DH key-generation:** `-pkeyopt group:name` selects a named safe-prime/FFDHE group without
needing a separate `-paramfile`; valid names include `ffdhe2048`…`ffdhe8192`, `modp_1536`…
`modp_8192` (algorithm `DH`), and `dh_1024_160`/`dh_2048_224`/`dh_2048_256` (algorithm `DHX`).

Note: **no key-generation options exist for X25519, X448, Ed25519, or Ed448** — these curves have
a single fixed security level and encoding, so `-algorithm ed25519 -out key.pem` (or `x25519`) is
the entire invocation.

**Concerning facts / gotchas:**
- `rsa_keygen_bits` defaulting to 2048 means an `-algorithm RSA` invocation *without* an explicit
  `-pkeyopt rsa_keygen_bits:...` silently produces a 2048-bit key — fine as a current-day floor,
  but worth setting explicitly if you actually want 3072/4096.
- `-algorithm` and `-pkeyopt` ordering matters: `-algorithm` must come first on the command line,
  and it's mutually exclusive with `-paramfile`.
- ML-DSA and ML-KEM support was only added in OpenSSL 3.5 — see the Debian divergence note under
  `req` below; a system on an older 3.x branch will not recognize these algorithm names at all.
- `-cipher` on `genpkey` encrypts the *private key file itself*; without it (and without a
  `-pass`), the key is written unencrypted in PEM/DER — same filesystem-permissions-only
  protection model flagged for `-nodes`/`-noenc` elsewhere in this workflow.

## `openssl pkey`

Processes an existing public or private key: converts between PEM/DER/P12, strips or adds
passphrase-encryption, prints components, and — the operation `key-generation.md` actually uses
it for — derives/extracts just the public key from a private key file.

**Syntax:** `openssl pkey [options] -in filename [-pubout] -out filename`

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-in filename\|uri` | key to read (private, unless `-pubin` is given); defaults to stdin | if the input is encrypted and `-passin` isn't given, you're prompted interactively |
| `-inform DER\|PEM\|P12\|ENGINE` | input format | unspecified by default — OpenSSL 3.0+ auto-detects DER/PEM/P12 |
| `-passin arg` | password source for reading an encrypted input key | see pass-phrase argument forms |
| `-pubin` | treat `-in` as a **public** key rather than private | if the file actually contains a private key, its public part is used |
| `-out filename` | output destination; can equal `-in` (file is truncated then rewritten — not atomic) | defaults to stdout |
| `-outform DER\|PEM` | output format | default `PEM` |
| `-cipher` | encrypt the output PEM private key with the given cipher | DER output cannot be encrypted this way |
| `-passout arg` | password source for the output file's encryption | if a cipher is set but no `-passout`, you're prompted; if that prompt is interrupted, the output file is left untouched |
| `-traditional` | write the private key in the old algorithm-specific format instead of the PKCS#8 default | |
| `-pubout` | **restrict output to the public key only** | auto-set if the input was already a public key; **omit this by mistake and `pkey` re-emits the full private key** — the exact accidental-leak scenario `key-generation.md` flags for RSA/ECDSA pubkey extraction |
| `-noout` | suppress the encoded key output entirely | typically paired with `-text`/`-text_pub` for inspection-only runs |
| `-text` | print all key components (private + public) in plaintext, in addition to the encoded form | cannot combine with DER output |
| `-text_pub` | print only the public components in plaintext (even for a private key input) | same as `-pubout -text` combined |
| `-check` | validate consistency of a full key pair | |
| `-pubcheck` | validate correctness of a public key (or the public half of a pair) | |
| `-ec_conv_form arg` (EC keys only) | point encoding: `compressed` (default), `uncompressed`, `hybrid` | compressed form is disabled by default for *binary* curves for patent-history reasons, re-enabled only via a compile-time macro |
| `-ec_param_enc arg` (EC keys only) | `named_curve` (default) or `explicit` parameter encoding | RFC 3279's `implicitlyCA` alternative is not implemented |
| `-engine id` | **deprecated since 3.0** | |
| `-provider*` / `-propquery` | provider controls | |
| `-help` | usage message | |

**Concerning facts / gotchas:**
- The single most consequential flag here is `-pubout` — its absence is the difference between
  "extract a shareable public key" and "dump the private key back out," with identical-looking
  command output either way if you're not watching for it.
- `-out` allowed to equal `-in` is convenient but not crash-safe: "file I/O is not atomic" per the
  man page, so a failure mid-write can leave a truncated file.
- `pkey` is the generic, algorithm-agnostic successor to `openssl rsa`/`openssl dsa`/`openssl ec` —
  prefer it when scripting across mixed key types.

## `openssl ecparam`

Manipulates or generates EC *domain parameter* files, and — with `-genkey` — generates an actual
EC private key using those parameters in one step. OpenSSL cannot invent brand-new elliptic-curve
groups; this command only works from its list of already-implemented named curves.

**Syntax (parameter generation):** `openssl ecparam -name curvename -out file`
**Syntax (key generation):** `openssl ecparam -name curvename -genkey -noout -out file`

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-name arg` | select EC parameters by short curve name (e.g. `prime256v1`, `P-256` is *not* a valid `-name` value here — this command uses SECG-style short names, unlike `genpkey`'s `ec_paramgen_curve` which accepts NIST names too) | required for generation; see `-list_curves` for the full set |
| `-list_curves` | print all implemented curve names and exit | does not generate anything |
| `-genkey` | generate an EC **private key** using the given/loaded parameters | without this, the command only emits/manipulates the *parameters*, not a key — the single most important flag distinguishing "params file" from "actual key" |
| `-noout` | suppress printing the encoded parameters | almost always wanted alongside `-genkey`, otherwise the output file mixes parameter block and key material together |
| `-in filename` | read existing parameters from a file (instead of `-name`) | defaults to stdin |
| `-out filename` | output destination; can equal `-in` (truncated then rewritten, not atomic) | defaults to stdout |
| `-inform DER\|PEM`, `-outform DER\|PEM` | encodings; parameters are encoded as `EcpkParameters` per RFC 3279 | output default `PEM` |
| `-text` | print parameters in human-readable form | |
| `-check` | validate the EC parameters | |
| `-check_named` | validate that named-curve parameters match a real built-in curve | narrower than `-check` |
| `-conv_form arg` | point encoding: `compressed`, `uncompressed` (default), `hybrid` | same patent-era caveat on binary-curve `compressed` as `pkey`/`ec` |
| `-param_enc arg` | `named_curve` (default) or `explicit` | |
| `-no_seed` | omit the parameter-generation seed from the output `ECParameters` structure | |
| `-rand files`, `-writerand file` | legacy RNG seed options | |
| `-engine id` | **deprecated since 3.0** | |
| `-provider*` / `-propquery` | provider controls | |
| `-help` | usage message | |

**Concerning facts / gotchas:**
- Forgetting `-genkey` is the classic mistake: the command silently succeeds and just writes out
  parameters, producing a file that looks plausible but contains no actual key material.
- Forgetting `-noout` alongside `-genkey` writes the human-readable-ish encoded parameter block
  into the same output file as the key, which is usually not what you want when the file is meant
  to be "just the private key."
- The man page states plainly that `openssl genpkey` (and `openssl pkeyparam`) can do everything
  `ecparam` can, plus other key types — `ecparam` is kept mainly for EC-specific/legacy workflows
  and scripts that predate `genpkey`'s EC support.

## `openssl ec`

Processes an *existing* EC key (as produced by `ecparam -genkey`): converts formats, prints
components, and — the operation used in the key-generation workflow — extracts the public key.

**Syntax:** `openssl ec -in filename [-pubout] -out filename`

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-in filename\|uri` | key to read; defaults to stdin | encrypted input prompts for a passphrase if `-passin` isn't given |
| `-inform DER\|PEM\|P12\|ENGINE` | input format | unspecified by default |
| `-out filename` | output destination | **the man page explicitly says this "should not be the same as the input filename"** — unlike `pkey`/`ecparam`, which tolerate `-in == -out` |
| `-outform DER\|PEM` | output format; private keys are SEC1 or PKCS#8, public keys are `SubjectPublicKeyInfo` (RFC 3280) | default `PEM` |
| `-passin arg`, `-passout arg` | password sources for input/output | |
| `-des` \| `-des3` \| `-idea` | encrypt the *output* private key with the named cipher, prompting for a passphrase | **if none of these is given, the key is written in plain text** — the same bare-filesystem-permissions security model flagged elsewhere; these flags only apply to PEM output |
| `-text` | print public/private components and parameters in plaintext | |
| `-noout` | suppress the encoded key output | |
| `-param_out` | print the EC parameters | |
| `-pubin` | treat input as a public key | if it's actually a private key, its public part is used |
| `-pubout` | **output only the public key** | auto-set if the input was already public; omitting it re-emits the private key, same leak risk as `pkey -pubout` |
| `-conv_form arg` | point encoding: `compressed`, `uncompressed` (default), `hybrid` | |
| `-param_enc arg` | `named_curve` (default) or `explicit` | |
| `-no_public` | omit public-key components from private-key output | |
| `-check` | validate consistency of the EC private/public key | |
| `-engine id` | **deprecated since 3.0**; `-conv_form`/`-no_public` are additionally unsupported for engine-loaded keys since 3.0 | |
| `-provider*` / `-propquery` | provider controls | |
| `-help` | usage message | |

**Concerning facts / gotchas:**
- `openssl ec`'s private-key output format is SEC1 by default, *not* PKCS#8 — if you need PKCS#8
  specifically, the man page points at `openssl pkcs8` to convert (out of scope here, but worth
  knowing the gap exists).
- The "don't reuse `-in` as `-out`" warning here is stricter than the equivalent notes for
  `pkey`/`ecparam`, which merely note the truncate-then-write non-atomicity risk without telling
  you outright not to do it.
- Same as `pkey`: `openssl pkey` is the generic successor capable of everything `ec` does, plus
  non-EC key types — prefer it in new scripts, but `ec` remains relevant for its EC-specific
  flags like `-param_out`.

## `openssl req` (self-signed certs only)

`req` is primarily OpenSSL's PKCS#10 certificate-signing-request (CSR) tool. **This section
covers only its `-x509` mode**, which short-circuits the normal "create a CSR → submit to a CA →
CA signs it" flow and emits a self-signed X.509 certificate directly in one command — exactly
what `key-generation.md`'s sample 7 does. The full CSR/CA workflow (`req` without `-x509`,
`openssl ca`) is out of scope per this file's [Scope](#scope) section.

**Syntax:** `openssl req -x509 -newkey alg -keyout keyfile -out certfile [-days n] [-nodes|-noenc] [-subj "/CN=..."]`

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `-x509` | **emit a self-signed certificate instead of a CSR** | implies `-new` if `-in` isn't given; if `-in` *is* given, an existing CSR is converted to a cert instead of created from scratch; a large random serial number is used unless `-set_serial` is given |
| `-newkey arg` | generate a fresh private key to certify | forms: `[rsa:]nbits` (RSA of that bit size, or config/2048 default if bits omitted); `algname[:paramfile]` for any other algorithm (e.g. `ed25519`, `ec:paramfile`); implies `-new`/`-x509`-as-appropriate |
| `-pkeyopt opt:value` | algorithm options for the freshly generated key | same option namespace as `openssl genpkey` |
| `-key filename\|uri` | use an **existing** private key instead of generating one | overridden by `-CA` if that's also given; accepts PKCS#8 PEM |
| `-keyout filename` | where to write the newly generated (or re-read) private key | if omitted, falls back to the config file's `default_keyfile`, else stdout |
| `-out filename` | where to write the certificate | defaults to stdout |
| `-days n` | certificate validity window in days from today | **default is only 30 days** if omitted — `key-generation.md`'s explicit `-days 365` is a deliberate override, not incidental |
| `-not_before date`, `-not_after date` | explicit start/expiry timestamps (`YYMMDDHHMMSSZ` or `YYYYMMDDHHMMSSZ`, or the literal `today`) | only take effect with `-x509`; `-not_after` overrides `-days`; `-not_before` does **not** change how `-days` counts (always counted from today) |
| `-set_serial n` | explicit serial number (decimal, or hex with `0x` prefix) | default is a large random number |
| `-subj arg` | set the subject DN directly, bypassing interactive prompts | format `"/type0=value0/type1=value1/..."`; `+` instead of `/` forms multi-valued RDNs; a bare `/` yields an empty (NULL) DN |
| `-noenc` | write the private key **unencrypted** | current, non-deprecated spelling |
| `-nodes` | same effect as `-noenc` | **deprecated since OpenSSL 3.0** — `key-generation.md` uses this spelling; functionally identical but `-noenc` is the form to prefer in new work |
| `-cipher name` | cipher to encrypt the output private key with, if it's *not* left unencrypted | **default changed from 3DES to AES-256-CBC in OpenSSL 3.5** — see the Debian divergence note below |
| `-passout arg` | password source if the key is being encrypted | |
| `-newhdr` | add `NEW` to the PEM header/footer lines | needed by some legacy CAs/software (e.g. old Netscape cert server) |
| `-copy_extensions arg` | `none` (default) ignores extensions from an input CSR; `copy`/`copyall` carries them into the `-x509` output | only matters when `-in` supplies an existing CSR being converted to a cert |
| `-x509v1` | force an X.509 **version 1** certificate | implies `-x509`; if any extensions are also requested, version 3 is set anyway; default (since 3.2) is version 3 with key-identifier extensions included automatically |
| `-extensions section` / `-reqexts section` | override which config-file section supplies X.509 extensions | `-reqexts` is an alias of `-extensions` since 3.2 |
| `-addext ext` | add one extension as a `key=value` pair directly on the command line, repeatable | overrides a same-OID extension from the config file; the same key must not be given twice |
| `-digest` | override the signing digest | some algorithms ignore this entirely — DSA always signs with SHA1, Ed25519/Ed448 never use any digest |
| `-config filename`, `-section name` | alternate config file / section (`req` is the default section) | |
| `-utf8` | interpret field values as UTF-8 instead of ASCII | |
| `-batch` | non-interactive mode | no prompting for DN fields |
| `-verbose` / `-quiet` | more/fewer status messages during operation | `-quiet` suppresses key-generation progress dots too |
| `-CA filename\|uri`, `-CAkey filename\|uri` | sign using a separate "micro CA" cert/key pair rather than self-signing | **out of scope** for the pure self-signed use case this section documents — mentioned here only because it appears in the same flag surface |
| `-text`, `-pubkey`, `-noout`, `-verify`, `-modulus`, `-subject` | inspection/printing options for an existing request or cert | mostly relevant to the CSR-inspection workflow, out of scope, but harmless to combine with `-x509` output for a quick sanity check |
| `-reqopt option`, `-nameopt option` | customize `-text` print formatting | |
| `-sigopt nm:v`, `-vfyopt nm:v` | algorithm-specific options passed to the sign/verify operation | e.g. SM2's `distid:...` |
| `-rand files`, `-writerand file` | legacy RNG seed options | |
| `-engine id` | **deprecated since 3.0** | |
| `-keygen_engine id` | engine specifically for key generation | |
| `-provider*` / `-propquery` | provider controls | |
| `-help` | usage message | |

**Relevant config-file (`openssl.cnf`) keys** (the `[ req ]` section, or the section named by
`-section`): `default_bits` (default key size for `-new`/`-newkey` when no size is given — 2048 if
unset, 512-bit minimum accepted), `default_keyfile`, `default_md`, `encrypt_key` (`no` = same
effect as `-noenc`), `string_mask` (default `utf8only`, the RFC 5280/PKIX-recommended setting),
`distinguished_name` (points at the section defining DN prompts), `prompt` (`no` disables
interactive prompting and reads DN fields straight from the config file), `x509_extensions`
(extensions section used specifically in `-x509` mode).

**Concerning facts / gotchas:**
- **The 30-day default validity is easy to miss.** Anyone running `req -x509 -newkey ... -keyout
  ... -out ...` without `-days` gets a certificate that expires in a month — `key-generation.md`'s
  explicit `-days 365` is not cosmetic, it's overriding a genuinely short default.
- `-nodes` vs `-noenc`: identical behavior, but `-nodes` ("no DES") is a historical name that's
  been deprecated since OpenSSL 3.0. It still works and still appears constantly in tutorials
  (including `key-generation.md`), but `-noenc` is the form the project wants used going forward.
- `-subj`'s DN string format is easy to get subtly wrong: `/` separates RDNs, `+` inside one RDN
  makes it multi-valued, and a *lone* `/` produces an empty DN rather than an error — worth
  double-checking the rendered cert's subject after generation, not just trusting the string was
  parsed as intended.
- `-x509` without an explicit `-subj` falls back to interactive prompting (unless `-batch`/config
  `prompt=no` is set) — scripting this without `-subj` or `-batch` will hang waiting for terminal
  input.
- **Debian/Arch divergence:** this machine runs OpenSSL 3.6.3; Debian **bookworm** (current
  stable) ships OpenSSL **3.0.20**. Two concrete behavioral differences confirmed against Debian's
  own hosted man pages: (1) the private-key encryption cipher for `-cipher`/no-passphrase-given
  changed its default from 3DES to AES-256-CBC only in OpenSSL 3.5 — Debian bookworm's 3.0.x
  branch predates that change; (2) `ML-DSA`/`ML-KEM` as `-algorithm`/`-newkey` values were added
  in 3.5 and are simply unrecognized on bookworm. The `-nodes`→`-noenc` deprecation, `-x509v1`, and
  the general certificate-generation flags used in `key-generation.md` are present on both.

## `openssl kdf`

A single generic driver command for OpenSSL's key-derivation-function implementations —
`TLS1-PRF`, `HKDF`, `SSKDF`, `PBKDF2`, `SSHKDF`, `X942KDF-ASN1`, `X942KDF-CONCAT`, `X963KDF`, and
`SCRYPT` — all invoked through the same `-kdfopt nm:v` option-passing interface, with the specific
KDF selected as the final positional argument. `key-generation.md` uses it for `PBKDF2` only.

**Syntax:** `openssl kdf -keylen num [-kdfopt nm:v ...] [-digest|-cipher|-mac name] [-out file] [-binary] kdf_name`

| Flag | Meaning | Notes / gotchas |
|---|---|---|
| `kdf_name` (positional, required) | which KDF algorithm to run: `TLS1-PRF`, `HKDF`, `SSKDF`, `PBKDF2`, `SSHKDF`, `X942KDF-ASN1`, `X942KDF-CONCAT`, `X963KDF`, `SCRYPT` | availability depends on how this OpenSSL build was configured (per the man page's NOTES section) |
| `-keylen num` | output key length in bytes | **required** for every KDF |
| `-kdfopt nm:v` | pass a named parameter to the chosen KDF (repeatable) | see the common parameter names below; the full authoritative list is `PARAMETERS` in `EVP_KDF(3)` |
| `-digest name` | digest algorithm, where the KDF needs one | error to supply this for a KDF that doesn't use a digest; list available digests with `openssl list -digest-commands` |
| `-cipher name` | cipher algorithm, where the KDF needs one | error to supply for a KDF that doesn't use a cipher |
| `-mac name` | MAC algorithm, where the KDF needs one | error to supply for a KDF that doesn't use a MAC |
| `-out filename` | output destination | defaults to stdout |
| `-binary` | emit the derived key as raw binary | default is hex-encoded text |
| `-provider*` / `-propquery` | provider controls | |
| `-help` | usage message | |

**Common `-kdfopt` parameter names** (from `EVP_KDF(3)`, applicable across multiple KDFs):

| `-kdfopt` name | Meaning |
|---|---|
| `key:string` / `hexkey:string` | the secret key, as printable text or hex-encoded bytes respectively — required by most KDFs other than the password-based ones |
| `pass:string` / `hexpass:string` | the input password, as printable text or hex — **required for PBKDF2 and SCRYPT** |
| `salt:string` / `hexsalt:string` | the (non-secret) salt, as printable text or hex — required by several KDFs including PBKDF2 |
| `info:string` / `hexinfo:string` | context-binding "info"/"fixed info"/"other info" data (used by HKDF and similar) |
| `digest:string` | equivalent to `-digest` | 
| `cipher:string` | equivalent to `-cipher` |
| `mac:string` | equivalent to `-mac` |

**PBKDF2-specific parameters** (from `EVP_KDF-PBKDF2(7)`, algorithm `SP800-132`):

| Parameter | Meaning | Default |
|---|---|---|
| `pass` | the password (octet string) | required |
| `salt` | the salt (octet string) | required |
| `iter` | iteration count | **2048** if not set via `-kdfopt iter:N` |
| `digest` | underlying hash function | see `EVP_KDF(3)` general default |
| `pkcs5` | toggles SP800-132 compliance checking (iteration count ≥ 1000, salt length ≥ 128 bits, derived key length ≥ 112 bits) | default provider defaults this to mode `1` (checks **disabled**, for backwards compatibility); the FIPS provider defaults to mode `0` (checks **enabled**) |
| `fips-indicator` | read-only getter reporting whether the derivation was FIPS-approved | consumed by the FIPS provider only |

**Concerning facts / gotchas:**
- **PBKDF2's built-in default iteration count is 2048 — dramatically below current guidance.**
  OWASP's current baseline for PBKDF2-HMAC-SHA256 is roughly 600,000 iterations; leaving `iter`
  unset silently gets you a count that's over 250x weaker than that baseline. `key-generation.md`
  setting `-kdfopt iter:600000` explicitly is compensating for this default, not adding an
  optional hardening step.
  For SHA-1, and other digest choices, OWASP's current recommended counts differ again — the
  right number depends on the digest, so treat 600k as tied to SHA-256 specifically, not a
  universal constant.
- **`-kdfopt pass:...`/`-kdfopt salt:...` on the literal command line leak.** The pass-phrase-
  options man page states outright that the `pass:password` argument form "is visible to
  utilities (like `ps`) under Unix" — the same mechanism (`/proc/<pid>/cmdline`, `ps aux`, shell
  history) that makes `key-generation.md` call out never putting a real password there. Prefer
  `env:`, `file:`, `fd:`, or `stdin` sourcing for anything beyond a disposable study exercise.
- The default provider silently accepting weak PBKDF2 parameters (`pkcs5` mode `1`) unless you're
  specifically running under the FIPS provider is itself worth knowing — nothing in a default
  build stops you from generating a PBKDF2 key with a 1-iteration count or an empty salt.
- PBKDF2 (the algorithm choice itself, independent of its parameters) is not memory-hard, unlike
  `SCRYPT` (also available through this same `openssl kdf` interface) — a real design consideration
  when picking which `kdf_name` to reach for, separate from tuning `iter`.

## Use Cases

- Use `openssl rand` to generate a cryptographically secure symmetric key, a salt for a KDF, or
  test/nonce material when no other CSPRNG is conveniently available.
- Use `openssl rand -base64` or `-hex` to produce a random value in a text-safe form suitable for
  pasting into a config file, environment variable, or `.env` secret, rather than raw binary.
- Use `openssl genpkey -algorithm RSA` to generate an RSA key pair for legacy-compatible signing
  or key-exchange workflows where RSA is still required by an external system.
- Use `openssl genpkey -algorithm ED25519` to generate a modern, fast, small signing key when the
  consuming system supports EdDSA and RSA is not a hard requirement.
- Use `openssl genpkey -algorithm X25519` to generate a key-exchange (Diffie-Hellman) key pair,
  distinct from a signing key, for protocols that need confidentiality/key-agreement rather than
  authentication.
- Use `openssl genpkey -genparam` to pre-generate reusable DH/DSA/EC parameters once, then derive
  multiple keys from the same parameter set with `-paramfile`, avoiding repeated (and for DH,
  potentially slow) parameter generation.
- Use `openssl pkey -pubout` to extract just the public half of a private key you already hold,
  for distribution to a peer without exposing the private material.
- Use `openssl pkey -text -noout` to inspect a private or public key's raw numeric components for
  debugging or manual verification, without re-emitting the encoded key material.
- Use `openssl pkey -traditional` or `-outform DER` when an older tool or library expects a
  specific legacy key encoding rather than the modern PKCS#8/PEM default.
- Use `openssl ecparam -list_curves` to discover which named elliptic curves this OpenSSL build
  actually implements before picking one for key generation.
- Use `openssl ecparam -name <curve> -genkey -noout` to generate an EC private key directly from a
  named curve in one step, when you want the parameter-file-centric EC workflow rather than
  `genpkey -algorithm EC`.
- Use `openssl ecparam -check` to validate that a set of EC domain parameters (your own or a
  third party's) are well-formed before trusting keys generated from them.
- Use `openssl ec -pubout` to extract the public key from an EC private key produced by `ecparam`,
  mirroring what `pkey -pubout` does for RSA/Ed25519/X25519 keys.
- Use `openssl ec -text -noout` to print an EC key's curve, private scalar, and public point for
  manual inspection.
- Use `openssl req -x509 -newkey ... -nodes/-noenc` to produce a throwaway self-signed TLS
  certificate for local development or testing, when no real CA involvement is needed or wanted.
- Use `openssl req -x509 -days N` to control exactly how long a self-signed test certificate stays
  valid, since the tool's own default (30 days) is short enough to be surprising in practice.
- Use `openssl req -x509 -subj "/CN=..."` to set the certificate's subject non-interactively in a
  script or CI pipeline, avoiding the tool's default interactive DN-prompting behavior.
- Use `openssl kdf ... PBKDF2` to derive a symmetric encryption key from a human-chosen password
  and a stored salt, rather than using the password bytes directly as key material.
- Use `openssl kdf -kdfopt iter:N` to explicitly tune PBKDF2's iteration count to a current
  security baseline, since the algorithm's own built-in default is far too low for production use.
- Use `openssl kdf ... SCRYPT` (via the same command, though out of this file's worked examples)
  when memory-hardness against GPU/ASIC attackers matters more than PBKDF2's simplicity and
  ubiquity.

## References

Primary sources — local man pages, OpenSSL 3.6.3 (Arch/Garuda, confirmed via `openssl version -a`
and `man -w <page>` for each before reading):

- `openssl(1)` — general command overview; consulted for the shared "Random State Options" and
  "Provider Options" sections referenced by every subcommand above.
- `openssl-rand(1)`
- `openssl-genpkey(1)`
- `openssl-pkey(1)`
- `openssl-ecparam(1)`
- `openssl-ec(1)`
- `openssl-req(1)`
- `openssl-kdf(1)`
- `EVP_KDF-PBKDF2(7)` — PBKDF2-specific parameters (`iter`, `pkcs5`, defaults), delegated to from
  `openssl-kdf(1)`'s `-kdfopt` description; pulled in directly per this repo's one-level-deep
  reference convention.
- `openssl-format-options(1)` — `-inform`/`-outform`/`-keyform` semantics shared across the above.
- `openssl-passphrase-options(1)` — `-pass`/`-passin`/`-passout` argument forms (`pass:`, `env:`,
  `file:`, `fd:`, `stdin`) shared across the above, and the source of the "`ps`-visible" leak
  warning cited under `openssl kdf`.

Cross-referenced against Arch's own hosted copy and Debian's hosted man pages via `WebFetch` to
confirm version numbers and locate the Debian-vs-Arch divergences noted under `openssl req`:

- `https://man.archlinux.org/man/openssl-req.1` — confirmed Arch's current package is OpenSSL
  3.6.3-1, matching this machine's installed version exactly (same content, no divergence to
  reconcile for Arch itself).
- `https://manpages.debian.org/testing/openssl/openssl-req.1ssl.en.html` — Debian *testing* is
  also on 3.6.3-1, i.e. currently in sync with Arch.
- `https://manpages.debian.org/bookworm/openssl/openssl-req.1ssl.en.html` — Debian **stable**
  (bookworm) is on OpenSSL **3.0.16-1~deb12u1** (package metadata separately confirms
  3.0.20-1~deb12u2 as the current point release) — noticeably older than Arch, source of the
  3DES-vs-AES-256-CBC default-cipher divergence and the ML-DSA/ML-KEM availability gap noted
  above.
- `https://packages.debian.org/bookworm/openssl` — used to confirm the current bookworm point
  release version number.

No man page needed was missing locally; all seven in-scope subcommands plus the general
`openssl(1)` overview and the two delegated-to reference pages (`format-options`,
`passphrase-options`) were read directly from this machine's installed OpenSSL 3.6.3 man pages.
