# ChaCha20-Poly1305 — Sequence Diagram

An AEAD (Authenticated Encryption with Associated Data) construction: an
ARX stream cipher (ChaCha20) for confidentiality, composed with a
polynomial one-time MAC over `GF(2^130 − 5)` (Poly1305) for authenticity,
per RFC 8439. This is the sole symmetric cipher WireGuard uses — both the
handshake messages and every transport data packet are encrypted with it.

**AEAD, defined:** a single operation giving both confidentiality
(encryption) and authenticity/integrity (a tag proving the data was not
tampered with). Decryption is refused outright if the tag doesn't verify —
the receiver never processes unauthenticated plaintext.

## Layman version

```
  SENDER
  ------
  scramble the message using the shared secret code
  also compute a short "proof" stamp over the scrambled message
        |
        |==== send: scrambled message + proof stamp ====>
        |
  RECEIVER
  --------
  recompute the proof stamp independently
  stamp doesn't match  -> reject, throw it away, never unscramble
  stamp matches        -> unscramble using the shared secret code
```

## Precise mathematical / cryptographic version

```
ChaCha20 internal state: 4x4 matrix of 32-bit words
  row0     = 4 fixed constants ("expa nd 3-2-byte k")
  row1-2   = 256-bit key (8 words)
  row3     = 32-bit block counter + 96-bit nonce (3 words)

Quarter-round(a,b,c,d)  — ARX: Add, Rotate, XOR:
  a += b;  d ^= a;  d <<<= 16
  c += d;  b ^= c;  b <<<= 12
  a += b;  d ^= a;  d <<<= 8
  c += d;  b ^= c;  b <<<= 7

20 rounds total = 10 "double rounds" (1 column round + 1 diagonal round
each), each round running 4 quarter-rounds in parallel over the state.

  ENCRYPT SIDE
  ------------
  poly1305_key (r, s) = first 32 bytes of ChaCha20_block(key, counter=0, nonce)
  keystream            = ChaCha20_block(key, counter=1,2,3..., nonce), serialized
  ciphertext            = plaintext XOR keystream

  mac_input = AAD || pad16(AAD) || ciphertext || pad16(ciphertext)
              || len(AAD) as u64-LE || len(ciphertext) as u64-LE

  tag = Poly1305(r, s, mac_input)
      = ( mac_input blocks treated as coefficients, evaluated as a
          polynomial at the point r, mod (2^130 − 5) ) + s, mod 2^128,
        truncated to 128 bits

        |==== send: nonce, AAD, ciphertext, tag ====>

  DECRYPT SIDE
  ------------
  recompute poly1305_key(r,s) from (key, nonce) — same derivation
  recompute tag' from (r, s, mac_input)
  tag' != tag  -> reject (constant-time compare; no decryption occurs)
  tag' == tag  -> keystream = ChaCha20_block(key, counter=1,2,...)
                  plaintext = ciphertext XOR keystream
```

## In WireGuard's handshake and transport

Every AEAD call in the handshake uses a **one-time key** derived fresh via
HKDF (see `diagram-hkdf.md`), so `nonce = 0` is safe there — the key is
never reused, so nonce-reuse (ChaCha20-Poly1305's one real footgun) can't
happen. Transport data packets instead reuse one session key across many
packets, so there the nonce is an incrementing 64-bit counter instead.
