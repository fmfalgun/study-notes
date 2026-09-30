# X25519 / Diffie-Hellman — Sequence Diagram

Elliptic-curve Diffie-Hellman (ECDH), instantiated on the Montgomery curve
`Curve25519: y² = x³ + 486662x² + x` over the prime field `GF(2²⁵⁵ − 19)`,
per RFC 7748. This is the sole key-agreement primitive WireGuard uses —
every DH operation in the Noise_IK handshake is an X25519 call.

## Layman version

Two people each pick a permanent secret (their real identity) and a
one-time secret (a throwaway mask for this session). Each publishes the
"public" half of whichever secret is relevant. Combining *my* private half
with *your* public half lands on the exact same number as combining *your*
private half with *my* public half — a shared secret that only the two of
you can compute, even though an eavesdropper saw both public halves.

```
   PERSON A                                          PERSON B
   --------                                          --------
   pick private secret (random)                      pick private secret (random)
   compute public value from it                      compute public value from it
        |                                                  |
        |============ send public value ================> |
        | <=========== send public value ================= |
        |                                                  |
   combine(my private, their public)                combine(my private, their public)
        |                                                  |
        \\_________________ SAME VALUE _________________/
```

## Precise mathematical / cryptographic version

```
Curve:            Curve25519 (Montgomery form)
Field:            GF(2^255 − 19)
Base point:       u-coordinate u = 9   (standardized, public, fixed)

Scalar clamping (RFC 7748 §5) — applied to every 32-byte random private
scalar k before use:
  - clear bits 0, 1, 2 of byte 0
  - clear bit 7 of byte 31
  - set   bit 6 of byte 31
  (forces k into the curve's prime-order subgroup; defeats small-subgroup
   and invalid-curve attacks)

Function: X25519(k, u) -> u-coordinate of the point reached by scalar-
          multiplying the point at u-coordinate u by scalar k.

  PARTY A                                          PARTY B
  --------                                        --------
  a_priv = clamp(random 32 bytes)                 b_priv = clamp(random 32 bytes)
  a_pub  = X25519(a_priv, 9)                       b_pub  = X25519(b_priv, 9)
        |                                                |
        |============= send a_pub (32 bytes) ==========> |
        | <============ send b_pub (32 bytes) =========== |
        |                                                |
  secret = X25519(a_priv, b_pub)                  secret = X25519(b_priv, a_pub)
        |                                                |
        \\_____________ EQUAL, by associativity of scalar
                         multiplication on the curve:
                         (a_priv · b_priv) · BasePoint
                         = (b_priv · a_priv) · BasePoint
```

Only `a_pub` and `b_pub` ever cross the wire. `a_priv`/`b_priv` never leave
their owner. An eavesdropper who sees both public values still cannot
compute `secret` — that intractability is the elliptic-curve discrete
logarithm problem (ECDLP), the hard problem X25519 relies on.

## In WireGuard's handshake

Every `DH(...)` step in the Noise_IK handshake (static-ephemeral,
static-static, ephemeral-ephemeral combinations) is exactly this function
call, just with different key pairs plugged in for `k` and `u` each time.
See `diagram-hkdf.md` for what happens to the raw `secret` output next —
it is never used directly as an encryption key.
