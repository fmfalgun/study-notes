# WireGuard + Python — Plan 2: Math/Crypto Deep-Dive

**Status: locked until Plan 1 is complete.** This is Phase 2. It does not
start until every module in
[`wireguard-python-learning-plan.md`](./wireguard-python-learning-plan.md)
(Plan 1) is checked off and the "Definition of proficient" bar there is
met. Plan 1 gets you *operationally* fluent in WireGuard + Python. This
plan goes one level deeper into the actual math/crypto foundations behind
the primitives Plan 1 treats as black boxes.

Origin: this list was generated while building the sequence diagrams for
Module A1 (Noise_IK handshake) — see
`cybersecurity-developer-vpn-tor-siem/01-vpn-protocol-development/diagram-x25519-diffie-hellman.md`,
`diagram-chacha20-poly1305.md`, `diagram-hkdf.md`, and
`diagram-wireguard-full-handshake.md`. Each topic below is a concept those
diagrams used but didn't derive from scratch.

Same living-checklist convention as Plan 1: a box is checked only once its
artifact is actually produced, not once the concept is merely explained.

---

## Group 1 — Algebra / number theory foundations

- [ ] **Modular arithmetic & finite fields `GF(p)`.**
  Artifact: hand-compute a small modular exponentiation and a small
  modular inverse without a calculator library (only `%` allowed).

- [ ] **Groups, generators, the discrete logarithm problem (classical,
  mod-p).**
  Artifact: given a small prime `p` and generator `g`, brute-force find a
  discrete log by hand, then explain why this becomes infeasible at
  cryptographic sizes.

## Group 2 — Elliptic curve cryptography

- [ ] **Elliptic curve basics: Weierstrass vs. Montgomery form.**
  Artifact: plot/derive a few points on a small toy curve by hand and
  verify they satisfy the curve equation.

- [ ] **Point addition / point doubling / scalar multiplication.**
  Artifact: implement toy point-addition and scalar multiplication in
  Python over a tiny curve (not Curve25519-scale), verify against
  hand-worked values.

- [ ] **Elliptic Curve Discrete Logarithm Problem (ECDLP).**
  Artifact: explain, unaided, why ECDLP is believed harder per-bit than
  classical DLP (why Curve25519 gets away with 256-bit keys where
  classical DH needs 2048+ bit primes for comparable security).

## Group 3 — Key exchange

- [ ] **Classical Diffie-Hellman (mod-p), end to end.**
  Artifact: run a full toy DH exchange by hand with small numbers, arrive
  at a matching shared secret from both "sides."

- [ ] **ECDH as DH generalized to elliptic curves.**
  Artifact: explain unaided how `X25519(k, u)` maps onto the point-scalar-
  multiplication artifact from Group 2.

## Group 4 — Symmetric cipher design

- [ ] **Stream ciphers vs. block ciphers.**
  Artifact: explain unaided why WireGuard picked a stream cipher
  (ChaCha20) over a block cipher (AES) for this use case.

- [ ] **ARX construction (Add-Rotate-XOR).**
  Artifact: hand-trace one ChaCha20 quarter-round by hand on small
  (e.g. 8-bit toy) words.

- [ ] **Keystream generation + XOR encryption mechanic.**
  Artifact: implement a minimal toy stream cipher in Python (any simple
  PRNG as keystream source) and demonstrate encrypt/decrypt round-trip.

## Group 5 — Hashing and MACs

- [ ] **Cryptographic hash function properties** (preimage resistance,
  second-preimage resistance, collision resistance).
  Artifact: explain unaided why each property matters specifically for
  BLAKE2s's role in the handshake's transcript hash `H`.

- [ ] **MACs in general** — the problem they solve, independent of any
  specific construction.
  Artifact: explain unaided why a hash function alone (without a key)
  cannot serve as a MAC.

- [ ] **Universal hashing / polynomial evaluation MACs (Poly1305's
  actual mechanism).**
  Artifact: hand-compute a tiny toy polynomial-evaluation MAC over a
  small modulus, matching the shape of `diagram-chacha20-poly1305.md`'s
  tag computation.

## Group 6 — Key derivation

- [ ] **HMAC construction, from first principles.**
  Artifact: hand-trace the inner/outer hash structure of HMAC on paper
  for a toy hash function.

- [ ] **Extract-then-Expand KDF paradigm.**
  Artifact: explain unaided why raw DH output isn't safe to use directly
  as a cipher key, and what Extract vs. Expand each contribute.

## Group 7 — Protocol-level concepts

- [ ] **AEAD as a composed primitive** — why encrypt+authenticate is
  bundled rather than done as two separate steps.
  Artifact: construct a concrete attack scenario that breaks under
  encrypt-then-MAC-separately-with-different-keys but not under AEAD.

- [ ] **Nonce/IV reuse consequences.**
  Artifact: demonstrate (toy example, e.g. two-time-pad on a stream
  cipher) what a reused nonce actually leaks.

- [ ] **Forward secrecy.**
  Artifact: explain unaided, using the ephemeral-key artifact from Group
  2/3, why compromising a static key later can't decrypt past sessions.

- [ ] **Replay attacks and defenses.**
  Artifact: explain unaided why WireGuard's TAI64N timestamp check in
  msg1 is sufficient to block a captured-and-replayed handshake message.

- [ ] **DoS-resistant handshake design (cookies, cheap-check-before-
  expensive-math).**
  Artifact: explain unaided why `mac1` is checked before any DH
  computation happens, and what class of attack that ordering defeats.

---

## Definition of "Plan 2 complete"

Every box above checked, each verified by its stated artifact — same bar
as Plan 1, just aimed at the underlying math instead of the operational
tooling.
