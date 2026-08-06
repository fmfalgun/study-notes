# 0. Prerequisite Foundations — Key Generation Commands

Companion to `exercise.md`. Generates one real sample of every key type covered in section 0's
tooling analysis into `generated-keys/` (gitignored — never commit real key material) for
hands-on study.

## Command groups

Each group below covers one key type: **(a)** install command, given for both Arch (`pacman`) and
Debian/Ubuntu (`apt`) for portability reference, then **(b)** the generation command itself, given
in `fish` (this machine's shell) and plain `bash`/`sh` for reference. Run the setup block once,
then each group's generate block from inside `generated-keys/`.

### Setup — cd into the output directory and tighten the umask

```
cd ~/Projects/study-notes/sets/cybersecurity-developer-vpn-tor-siem/00-prerequisite-foundations/generated-keys
umask 077
```

`umask 077` is not optional — verified empirically (see below) that two of this file's commands
create their output file at mode `644` (world-readable) under this machine's default umask
(`022`), not `600`: `openssl rand -out` and `wg genkey | tee`. The other tools (`openssl genpkey`/
`ecparam`/`req`, `ssh-keygen`, `gpg`, `age-keygen`) already `chmod 600` their own private-key
output internally regardless of umask — but running `umask 077` once, up front, protects the two
gaps *and* removes the need to individually verify every future tool's internal behavior before
trusting it. This closes the exposure window at creation time rather than fixing permissions
after the fact with a follow-up `chmod`, which leaves a real (if brief) window where another local
account could read the file between its creation and the `chmod`.

`generated-keys/` itself has also been set to `700` (not just `750`/`755`) — a `644` key file
inside a `755` directory is still protected file-by-file, but the directory listing itself (just
the *filenames*, e.g. seeing that `wg-private.key` exists) is metadata another local account
shouldn't need either.

### 1. Symmetric key (AES-256)

```fish
# arch:   sudo pacman -S openssl
# debian: sudo apt install openssl
```
```fish
openssl rand -out aes256.key 32
```
```
# bash/sh: (same command, portable)
openssl rand -out aes256.key 32
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `32` (positional) | byte count | determines key entropy — 32 bytes = 256 bits, the strength claim of "AES-256" |
| `-out <file>` | output destination | **confirmed empirically**: `openssl rand -out` does *not* self-protect its output — it lands at your raw default umask (`644` under this machine's `022`), unlike `genpkey`/`ecparam`/`req` which do `chmod 600` internally. This is exactly why the Setup step now runs `umask 077` first (Exercise 1's adversary model) |

### 2. RSA keypair

```fish
# arch:   sudo pacman -S openssl
# debian: sudo apt install openssl
```
```fish
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out rsa2048.pem
openssl pkey -in rsa2048.pem -pubout -out rsa2048.pub
```
```
# bash/sh: (same command, portable)
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out rsa2048.pem
openssl pkey -in rsa2048.pem -pubout -out rsa2048.pub
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `-algorithm RSA` | selects the public-key family | the single most consequential choice — everything downstream depends on it |
| `-pkeyopt rsa_keygen_bits:2048` | key size in bits | security margin: 2048 ≈ 112-bit security (today's floor), use 3072/4096 for headroom |
| `-pubout` | emit only the public key | without it, `openssl pkey` re-emits the *private* key — easy accidental leak |
| `-out` / `-in` | output / input file paths | `-out` here is sensitive private material; `-in` just reads it back to derive the pubkey |

### 3. ECDSA keypair (P-256)

```fish
# arch:   sudo pacman -S openssl
# debian: sudo apt install openssl
```
```fish
openssl ecparam -name prime256v1 -genkey -noout -out ecdsa-p256.pem
openssl ec -in ecdsa-p256.pem -pubout -out ecdsa-p256.pub
```
```
# bash/sh: (same command, portable)
openssl ecparam -name prime256v1 -genkey -noout -out ecdsa-p256.pem
openssl ec -in ecdsa-p256.pem -pubout -out ecdsa-p256.pub
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `-name prime256v1` | curve selection | determines security level (~128-bit); NIST curve — widely supported but its constants have drawn historical scrutiny vs. Curve25519's verifiably-random generation |
| `-genkey` | actually generate a keypair | without it `ecparam` only prints domain parameters, no key |
| `-noout` | suppress printing curve params | keeps the output file to just the key |
| `-pubout` | emit only the public key | same leak risk as the RSA case above |
| `-out` / `-in` | file paths | as above |

### 4. Ed25519 / X25519 keypair (openssl)

```fish
# arch:   sudo pacman -S openssl
# debian: sudo apt install openssl
```
```fish
openssl genpkey -algorithm ed25519 -out ed25519.pem
openssl genpkey -algorithm x25519 -out x25519.pem
```
```
# bash/sh: (same command, portable)
openssl genpkey -algorithm ed25519 -out ed25519.pem
openssl genpkey -algorithm x25519 -out x25519.pem
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `-algorithm ed25519` vs `-algorithm x25519` | signing vs. key-exchange curve | **not interchangeable** — ed25519 (EdDSA) signs/authenticates, x25519 does Diffie-Hellman; picking the wrong one for your use case is a real design bug, not a style choice |
| `-out` | output file | private key material |

### 5. SSH keypair (ed25519)

```fish
# arch:   sudo pacman -S openssh
# debian: sudo apt install openssh-client
```
```fish
ssh-keygen -t ed25519 -f ssh_study_ed25519 -N "" -C "study-key"
```
```
# bash/sh: (same command, portable)
ssh-keygen -t ed25519 -f ssh_study_ed25519 -N "" -C "study-key"
```
Always pass `-f <path>` explicitly (as above) — never run `ssh-keygen` bare, or it defaults to
prompting toward the real `~/.ssh/id_ed25519`.

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `-t ed25519` | key type/algorithm | modern SSH default: smaller, faster, avoids the weak-randomness concerns of some legacy curves |
| `-N ""` | passphrase (empty = none) | **security-critical**: an unencrypted private key relies entirely on filesystem permissions for protection — exactly the adversary model from Exercise 1 |
| `-f <path>` | output path | must always be explicit — prevents accidentally clobbering your real `~/.ssh/id_ed25519` |
| `-C "comment"` | cosmetic label in the pubkey | shows up in `authorized_keys`/logs — minor audit/attribution value, no security weight |



### 6. GPG/PGP keypair

```fish
# arch:   sudo pacman -S gnupg
# debian: sudo apt install gnupg
```
```fish
gpg --homedir . --quick-generate-key "Study Key <study@example.local>" ed25519 sign 1y
```
```
# bash/sh: (same command, portable)
gpg --homedir . --quick-generate-key "Study Key <study@example.local>" ed25519 sign 1y
```
`--homedir .` keeps this study key in a throwaway keyring inside `generated-keys/`, isolated
from your real `~/.gnupg`.

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `--homedir .` | isolates the keyring | prevents polluting your real trust store/keyring with a throwaway study key |
| `ed25519` (positional) | algorithm | modern default over RSA for new GPG keys |
| `sign` (positional) | capability restriction | least-privilege: this key can only sign, not decrypt — narrows blast radius if it leaks |
| `1y` (positional) | expiration | bounds exposure of a lost/compromised key and forces periodic rotation — a real-world best practice, not just a study artifact |



### 7. X.509 self-signed certificate + key

```fish
# arch:   sudo pacman -S openssl
# debian: sudo apt install openssl
```
```fish
openssl req -x509 -newkey ed25519 -keyout tls-cert.key -out tls-cert.pem -days 365 -nodes -subj "/CN=study.local"
```
```
# bash/sh: (same command, portable)
openssl req -x509 -newkey ed25519 -keyout tls-cert.key -out tls-cert.pem -days 365 -nodes -subj "/CN=study.local"
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `-nodes` | "no DES" — do NOT encrypt the private key | security-critical: same tradeoff as `ssh-keygen -N ""`, relies on filesystem perms instead |
| `-subj "/CN=..."` | subject identity embedded in the cert | in real deployments this **must** match the hostname clients connect to, or TLS validation fails/is spoofable |
| `-x509` | emit a self-signed cert directly | skips the "submit CSR to a CA" step — fine for study/testing, never for production trust |
| `-newkey ed25519` | algorithm for the freshly generated key | same weight as the RSA/ECDSA algorithm choices above |
| `-days 365` | certificate validity window | shorter = smaller exposure window if compromised, forces rotation |
| `-keyout` / `-out` | private key / cert output paths | `-keyout` is sensitive, `-out` (the cert) is meant to be shared |

### 8. WireGuard keypair

```fish
# arch:   sudo pacman -S wireguard-tools
# debian: sudo apt install wireguard-tools
```
```fish
wg genkey | tee wg-private.key | wg pubkey > wg-public.key
```
```
# bash/sh: (same command, portable)
wg genkey | tee wg-private.key | wg pubkey > wg-public.key
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `wg genkey` | generate a random Curve25519 private key to stdout | no flags — output streams straight through the pipe, never touching a temp file, minimizing exposure window |
| `tee wg-private.key` | write to disk *and* forward down the pipe | **confirmed empirically**: `tee` has no key-aware permission logic of its own, so this file lands at your raw default umask (`644` under this machine's `022`) — the same gap as `openssl rand -out` above, and why the Setup step now runs `umask 077` first (same Exercise 1 concern) |
| `wg pubkey` | derive the public key from stdin | one-way derivation; the output is safe to share/commit |
| `>` | redirect derived pubkey to file | this file is public material, no protection needed |

### 9. KDF-derived key (PBKDF2)

```fish
# arch:   sudo pacman -S openssl
# debian: sudo apt install openssl
```
```fish
openssl kdf -keylen 32 -kdfopt digest:SHA2-256 -kdfopt pass:studypassword -kdfopt salt:0102030405060708 -kdfopt iter:600000 PBKDF2
```
```
# bash/sh: (same command, portable)
openssl kdf -keylen 32 -kdfopt digest:SHA2-256 -kdfopt pass:studypassword -kdfopt salt:0102030405060708 -kdfopt iter:600000 PBKDF2
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `PBKDF2` (positional) | KDF algorithm choice | weakest of the modern options against GPU/ASIC attacks — it isn't memory-hard, unlike scrypt/Argon2; a teaching point, not just a label |
| `-kdfopt iter:600000` | iteration count | **the primary security lever for PBKDF2** — directly trades attacker cost vs. your own latency; 600k matches current OWASP baseline for SHA-256 |
| `-kdfopt salt:...` | salt value | must be random and unique per key in real use — reusing it defeats rainbow-table resistance; hardcoded here only for reproducible study output |
| `-kdfopt pass:...` | input password/secret | hardcoded here only for the exercise — **never** put a real password on a command line, it leaks via shell history and `/proc/<pid>/cmdline` |
| `-kdfopt digest:SHA2-256` | underlying hash function | secondary to iteration count, but still affects output strength |
| `-keylen 32` | output key length in bytes | determines final derived-key size (32 bytes = 256 bits) |

### 10. age keypair (X25519)

```fish
# arch:   sudo pacman -S age
# debian: sudo apt install age
```
```fish
age-keygen -o age-key.txt
```
```
# bash/sh: (same command, portable)
age-keygen -o age-key.txt
```

**Flags** (ordered by security relevance):

| Flag | Meaning | Why it matters |
|---|---|---|
| `-o age-key.txt` | output file path | contains the private key **and** the public key (as a comment) in one plaintext file — no separate passphrase protection by default; pipe through `age -p` to encrypt the identity file at rest if that matters for your use case |
