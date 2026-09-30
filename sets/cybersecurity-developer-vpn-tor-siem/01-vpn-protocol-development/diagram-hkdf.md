# HKDF (HMAC-BLAKE2s) — Sequence Diagram

HMAC-based key derivation, per the Noise Protocol Framework's
`HKDF(chaining_key, input, num_outputs)` definition, which WireGuard uses
verbatim with the hash slot filled by **BLAKE2s**. Its job: take raw,
not-safe-to-use-directly material (like a DH output) and derive clean,
independent symmetric keys from it.

## Layman version

```
raw shared secret (not safe to use directly)
        |
        v
   [ key-strengthening blender ]
        |
        v
one or more clean, independent, ready-to-use keys
```

## Precise mathematical / cryptographic version

```
Underlying hash: BLAKE2s (32-byte / 256-bit digest)

HMAC-BLAKE2s(key, data) — standard HMAC construction (RFC 2104),
instantiated with BLAKE2s as the hash H:
  HMAC(key, data) = H( (key' XOR opad) || H( (key' XOR ipad) || data ) )
  (key' = key, zero-padded/hashed down to BLAKE2s's block size)

  input_key_material (e.g. a raw X25519 DH output)
  chaining_key        (running state, carried through the whole handshake)
        |
        v
  temp_key = HMAC-BLAKE2s(chaining_key, input_key_material)
        |
        v
  output1 = HMAC-BLAKE2s(temp_key, 0x01)
        |
        v
  output2 = HMAC-BLAKE2s(temp_key, output1 || 0x02)
        |
        v
  output3 = HMAC-BLAKE2s(temp_key, output2 || 0x03)   <- only if 3 outputs requested
        |
        v
  new_chaining_key = output1
  derived_key(s)    = output2 (and output3, when a step needs two keys —
                                e.g. the final transport-key derivation,
                                which produces separate send/receive keys)
```

This is a fixed 2-or-3-output construction defined directly in the Noise
spec — not the general variable-length HKDF from RFC 5869, though it's
built from the same Extract-then-Expand-via-HMAC idea.

## In WireGuard's handshake

Every `DH(...)` result (see `diagram-x25519-diffie-hellman.md`) is fed
through this exact HKDF before it's ever used to key ChaCha20-Poly1305
(see `diagram-chacha20-poly1305.md`). The `chaining_key` accumulates state
across the whole handshake, which is what cryptographically binds the
final transport keys to every DH operation that came before them.
