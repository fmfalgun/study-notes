# WireGuard Full Handshake — Sequence Diagram (Noise_IK, exact math)

The complete two-message Noise_IK handshake as WireGuard actually runs it,
wiring together the three primitives documented separately in this folder:
`diagram-x25519-diffie-hellman.md` (the `DH(...)` steps),
`diagram-hkdf.md` (the `KDF(...)` steps, HMAC-BLAKE2s), and
`diagram-chacha20-poly1305.md` (the `AEAD(...)` steps). This file only
shows how they're wired together, not their internals — see those files
for that.

## Symbols

```
I, R              = Initiator, Responder
I_s_priv, I_s_pub = Initiator's static (permanent) X25519 keypair
R_s_priv, R_s_pub = Responder's static keypair — R_s_pub already known
                     to I beforehand (the "IK" in Noise_IK)
I_e_priv, I_e_pub = Initiator's ephemeral (one-handshake-only) keypair
R_e_priv, R_e_pub = Responder's ephemeral keypair
DH(priv, pub)     = X25519 scalar multiplication -> shared secret
KDF1(C, input)    = HKDF, 1 output -> new chaining key C
KDF2(C, input)    = HKDF, 2 outputs -> new chaining key C, key k
KDF3(C, input)    = HKDF, 3 outputs -> new chaining key C, key tau, key k
AEAD(k, n, plaintext, aad) = ChaCha20-Poly1305 encrypt
Hash(...)         = BLAKE2s
C                 = chaining key (running state, starts from a fixed
                     protocol-name constant, mixed at every step)
H                 = transcript hash (running state, authenticates
                     everything sent/received so far as AAD)
Q                 = pre-shared symmetric key (optional; 32 zero bytes if
                     the user hasn't configured one — a hedge against a
                     future break of X25519/ECDLP, e.g. by a quantum
                     computer, since Q is a plain symmetric secret with
                     no discrete-log structure to attack)
```

## Message 1: Handshake Initiation (I -> R)

```
I generates ephemeral keypair: I_e_priv, I_e_pub

H = Hash(H || I_e_pub)
C = KDF1(C, I_e_pub)

secret1 = DH(I_e_priv, R_s_pub)
C, k1   = KDF2(C, secret1)
enc_static = AEAD(k1, nonce=0, I_s_pub, aad=H)
H = Hash(H || enc_static)

secret2 = DH(I_s_priv, R_s_pub)
C, k2   = KDF2(C, secret2)
enc_timestamp = AEAD(k2, nonce=0, TAI64N_now, aad=H)
H = Hash(H || enc_timestamp)

mac1 = MAC( Hash(LABEL_MAC1 || R_s_pub), msg_so_far )
mac2 = MAC( cookie, msg_so_far )   -- all-zero unless R is under load
                                       and issued a cookie reply earlier

  I                                                          R
  |==== MSG1: I_e_pub, enc_static, enc_timestamp, mac1, mac2 ====>
```

`mac1` is keyed off `Hash(R_s_pub)` — it doesn't authenticate I's
identity, only proves I actually knows R's real static public key before
R does any expensive DH work. This is WireGuard's DoS defense: cheap MAC
check first, expensive elliptic-curve math only if that passes.

## R processes Message 1

```
secret1' = DH(R_s_priv, I_e_pub)          -- equals secret1 (ECDH property)
C, k1    = KDF2(C, secret1')
I_s_pub  = AEAD_decrypt(k1, nonce=0, enc_static, aad=H)   -- reveals I's identity
H = Hash(H || enc_static)

secret2' = DH(R_s_priv, I_s_pub)          -- equals secret2
C, k2    = KDF2(C, secret2')
timestamp = AEAD_decrypt(k2, nonce=0, enc_timestamp, aad=H)
H = Hash(H || enc_timestamp)

reject if timestamp <= last-seen timestamp for this peer (replay defense)
```

## Message 2: Handshake Response (R -> I)

```
R generates ephemeral keypair: R_e_priv, R_e_pub

H = Hash(H || R_e_pub)
C = KDF1(C, R_e_pub)

secret3 = DH(R_e_priv, I_e_pub)
C = KDF1(C, secret3)

secret4 = DH(R_e_priv, I_s_pub)
C = KDF1(C, secret4)

C, tau, k3 = KDF3(C, Q)          -- Q = pre-shared key (zero if unset)
H = Hash(H || tau)

enc_empty = AEAD(k3, nonce=0, plaintext="", aad=H)   -- pure key-confirmation,
                                                          no real payload
H = Hash(H || enc_empty)

mac1 = MAC( Hash(LABEL_MAC1 || I_s_pub), msg_so_far )
mac2 = MAC( cookie, msg_so_far )   -- all-zero unless I is under load

  R                                                          I
  <==== MSG2: R_e_pub, enc_empty, mac1, mac2 ====================|
```

## I processes Message 2

```
secret3' = DH(I_e_priv, R_e_pub)          -- equals secret3
C = KDF1(C, secret3')

secret4' = DH(I_s_priv, R_e_pub)          -- equals secret4
C = KDF1(C, secret4')

C, tau, k3 = KDF3(C, Q)
H = Hash(H || tau)

verify enc_empty decrypts under k3 (aad=H)   -- proves R knows the chain,
                                                 i.e. is the real R
H = Hash(H || enc_empty)
```

## Final transport key derivation (both sides, independently)

```
(Ta, Tb) = KDF2(C, empty_input)

I sets:  send_key = Ta,  recv_key = Tb
R sets:  send_key = Tb,  recv_key = Ta

-> I's send_key == R's recv_key, and vice versa: cross-matched,
   confirming the entire chain of DH steps landed identically on both
   sides, without either side ever transmitting a symmetric key.
```

From here, all data packets are `AEAD(send_key, nonce=incrementing_counter, plaintext, aad=receiver_index)` — see `diagram-chacha20-poly1305.md` for that primitive's internals.

## Why this is secure (tying back to the individual primitive notes)

- **Mutual authentication:** `secret1`/`secret2` (msg1) and `secret3`/`secret4`
  (msg2) each mix one static key from every party in some combination, so
  the final chaining key `C` could only be reproduced by someone holding
  both `I_s_priv` and `R_s_priv`'s legitimate counterpart knowledge — an
  impersonator with only one side's keys gets a different (rejected) `C`.
- **Forward secrecy:** every DH step also involves at least one ephemeral
  key (`I_e_priv`/`R_e_priv`), which is discarded immediately after the
  handshake. Recovering a static private key later can't reconstruct a
  destroyed ephemeral one, so past transport keys stay safe.
- **Transcript binding:** `H` accumulates every message exchanged so far
  and is passed as AAD into every `AEAD(...)` call — tampering with any
  earlier field breaks every later authentication check.
