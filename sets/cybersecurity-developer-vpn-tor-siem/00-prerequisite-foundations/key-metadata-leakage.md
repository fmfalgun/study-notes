# 0. Prerequisite Foundations — What Generated Keys Leak Beyond the Secret

Companion to `key-generation.md`. Two separate harm categories from pushing generated key
material to git: **direct compromise** (the key itself is a working credential) and
**information disclosure** (the key/commit *metadata* reveals things about you and your system,
independent of whether the crypto itself holds). This file details the second category, which is
easy to underrate because "it's just a public key, that's supposed to be shareable."

## 1. Direct compromise (baseline, for contrast)

Git is content-addressed and permanent by design — deleting a key in a later commit does not
remove the blob from `.git/objects`, from any clone, or from any fork. Automated scanners crawl
public pushes in real time looking for private-key headers (see `../someday-checklist.md` for the
exact terminology — "secrets sprawl" / "secret scanning" — and the empirical numbers). This is
the obvious risk; the table below is about the *less obvious* one.

## 2. Information disclosure — what each key type reveals

| Key type | What leaks | Why / evidence |
|---|---|---|
| **GPG** | Real name + email, permanently, if a real UID is used | The UID is baked into the public key packet. Once it touches a keyserver, it is **unremovable** — SKS-network keyservers are append-only by design |
| **SSH** | Username + hostname, *by default* | `ssh-keygen`'s default comment (when `-C` is omitted) is `user@host` — on this machine that would be `fmf@vajrangi`. Public `.pub` files scraped from repos are a direct source for username wordlists used in credential-stuffing / SSH brute-force targeting |
| **X.509 cert / CSR** | Internal hostnames, org names, network naming conventions | `-subj "/CN=..."` (or a real CSR's full Subject DN: Country/Org/OU/email) is reconnaissance value — it reveals internal domain scheme before an attacker has touched the network |
| **Git commit wrapping any key** | Real identity + provable creation time | Commits in this repo carry `falgun@garuda` / `fmfalgunmarothia@gmail.com` and a timestamp on every commit — pushing a key ties a cryptographic secret to a real identity and a provable time-of-creation, strictly worse than an anonymous leak |
| **Any key's cryptographic parameters** | Toolchain/platform fingerprint | Curve choice, KDF iteration defaults, and PRNG behavior can fingerprint which library/version/OS generated the key — see the Debian case study for what happens when that fingerprint points at a *broken* toolchain |

## 3. Why "it's just the public half" isn't a safe assumption

Public keys are *supposed* to be shareable — that's the entire point of public-key crypto. The
risk here isn't the public key breaking confidentiality on its own; it's that the metadata
riding along with it (comment fields, UIDs, Subject DNs, commit authorship) leaks recon-grade
information about you and your infrastructure that has nothing to do with the cryptography, and
that a real key was ever generated on this machine at all — every generation command in
`key-generation.md` was written with this in mind (throwaway UIDs, explicit `-C` overrides,
`generated-keys/` gitignored entirely rather than trusting per-file judgment calls).

See also: `secret-scraping-economy.md`, `case-study-debian-weak-keys.md`,
`../someday-checklist.md`.
