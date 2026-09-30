# A1.1 — Toy Diffie-Hellman: Why It Works

Companion note to
[`a1_1_toy_dh.py`](./a1_1_toy_dh.py). Explains why Alice and Bob's
independently computed secrets come out equal, using the actual run
output from that script.

## Layman version

Both sides end up doing the exact same multiplication, just in a
different order. Alice raises Bob's public number to *her* private
number; Bob raises Alice's public number to *his*. But "raise to a
power, then raise that to another power" is the same as "multiply the
two powers together" — and multiplication doesn't care what order you
do it in. So both sides land on the same result without ever telling
each other their private number.

## Precise version, with the script's actual run values

Run values: `p = 11`, `g = 2`, `a = 5` (Alice's private number),
`b = 7` (Bob's private number).

- Alice's public value: `A = g^a mod p = 2^5 mod 11 = 32 mod 11 = 10`
- Bob's public value: `B = g^b mod p = 2^7 mod 11 = 128 mod 11 = 7`

These match the script's printed output (`alice pubKey: 10`,
`Bob pubKey: 7`).

Now the shared-secret step — this is the algebraic identity that makes
DH work:

```
Alice computes:  B^a mod p  =  (g^b)^a mod p  =  g^(b*a) mod p
Bob computes:    A^b mod p  =  (g^a)^b mod p  =  g^(a*b) mod p
```

`(g^b)^a` and `(g^a)^b` are both just `g` raised to the product of the
two exponents — `g^(ab)`. Since ordinary integer multiplication
commutes (`a*b = b*a`), it doesn't matter which exponent gets applied
first; modular exponentiation preserves that identity
(`(g^x)^y mod p = g^(xy) mod p`, always — this is a basic law of
exponents, and it still holds when you reduce mod `p` at each step).
So both sides are computing the same number,
`g^(a*b) mod p = 2^35 mod 11 = 10`, just by two different paths — which
matches the script's `True` result.

## Why this is *not* secure at this size (and why real DH needs huge numbers)

Computing `g^a mod p` forward is cheap. But going backward — given `A`
and knowing `g, p`, recovering `a` — is the **discrete logarithm
problem**, and for a large prime `p` (hundreds of digits) there's no
known efficient way to do it. Here, with `p = 11`, an attacker could
just brute-force all 10 possible exponents in a millisecond and recover
`a = 5` instantly by trial. The security only shows up once `p` gets
astronomically large — which is exactly why WireGuard uses X25519
(elliptic-curve DH) instead of this classic mod-`p` version: same
algebraic idea, but the discrete-log problem on an elliptic curve stays
hard even with much shorter keys (32 bytes vs. thousands of bits for
classic DH at equivalent security). See
[`diagram-x25519-diffie-hellman.md`](../cybersecurity-developer-vpn-tor-siem/01-vpn-protocol-development/diagram-x25519-diffie-hellman.md)
for the elliptic-curve version of this same idea.
