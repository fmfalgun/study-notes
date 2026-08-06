# 0. Prerequisite Foundations — Notes

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 0.

## Cryptography Engineering (Ferguson, Schneier, Kohno)

**Claim**: Knowing cryptographic algorithms (AES, RSA, SHA-2, ...) is not the same skill as
building a secure system with them. The book's thesis is that most real-world crypto failures
happen at the *engineering* layer — key management, protocol composition, side channels, error
handling, interfacing with people/hardware/policy — not in the math of the primitives themselves.
It teaches "thinking like a cryptographer": adversarial reasoning about how a design will actually
be attacked, applied to concrete protocols rather than abstract theorems.

**Simple explanation**: A cipher can be mathematically unbreakable and the system built around it
can still be trivially broken — e.g. a perfect AES implementation with a hardcoded key, no
authentication, or a buffer overflow in the parser that decrypts the ciphertext. This book is about
the "everything around the algorithm" that's usually where things actually go wrong: choosing
between competing designs, managing keys and their lifecycle, and building things so a single
mistake doesn't cascade into total compromise.

**Try it**: Since VPN protocol dev (WireGuard/IPsec) and Tor dev are exactly this "engineering
around primitives" problem, pick one core habit from the book — threat-model a design before
coding it — and apply it now: write a one-paragraph threat model for "a VPN client that stores its
private key on disk" (who's the adversary, what can they do, what's the blast radius of a key
leak). This is the same exercise style used later in section 1 (WireGuard) and section 4
(client-side VPN vulnerabilities), so keep the note for cross-reference.

## A Graduate Course in Applied Cryptography (Boneh & Shoup)

**Claim**: Cryptography is "brittle" — a single spec or implementation error can silently destroy
security that unit testing will never catch, so instead of testing your way to confidence you must
argue security via formal definitions and reduction proofs against plausible hardness assumptions.
The book (free, ~900+ pages, v0.6 as of Jan 2023) is structured in three parts: Part I — symmetric
crypto (stream ciphers, block ciphers, message integrity, authenticated encryption); Part II —
public-key crypto (public-key encryption, digital signatures, elliptic curves, post-quantum
lattices); Part III — protocols (identification, zero-knowledge, **Authenticated Key Exchange
(Ch. 21)**, threshold crypto, secure multi-party computation). Chapter 21 (AKE) is the direct
theoretical basis for how VPN/Tor handshakes are analyzed: it covers Diffie-Hellman-based AKE,
one-sided authentication, preshared-key AKE, and password-AKE — the exact taxonomy WireGuard's
Noise handshake and IKEv2 fall into.

**Simple explanation**: This is the rigorous companion to Cryptography Engineering above — where
that book teaches "how not to shoot yourself in the foot building a system," this one teaches "how
to prove, mathematically, that a specific construction (e.g. a key-exchange protocol) actually
achieves the security property you claim it does." Each chapter defines a security goal precisely
(e.g. "an eavesdropper who watches N key exchanges learns nothing about the resulting session
keys"), then proves a construction meets it, with real-world case studies of what breaks when it
doesn't (e.g. two-time-pad reuse, RC4 cryptanalysis, DVD CSS).

**Try it**: Read the Part III intro and Chapter 21 (Authenticated Key Exchange) section headers —
they map directly onto WireGuard's Noise_IK handshake and IKEv2's SA negotiation covered in
section 1. Fetch the PDF locally and confirm the chapter location instead of trusting a web
summary (WebFetch cannot parse this PDF's binary stream, so `curl` + `pdftotext` is the reliable
path here):
```fish
curl -sL -o (mktemp -t cryptobook.XXXX.pdf) https://toc.cryptobook.us/book.pdf
```
```
# bash/sh:
curl -sL -o /tmp/cryptobook.pdf https://toc.cryptobook.us/book.pdf
```
then extract just the contents pages with `pdftotext -f 1 -l 20 <file> -` and grep for
`"Authenticated Key Exchange"` to confirm the chapter/page number before reading it — verified
locally: Chapter 21, starting page 857, covers "Identification and AKE", "One-sided authenticated
key exchange", "AKE with preshared keys", and "Password authenticated key exchange", which is the
formal-proof backbone for the handshakes studied in section 1.

## OWASP Secure Coding Practices — Quick Reference Guide

**Claim**: Secure software is cheaper to build securely up front than to patch after a breach, and
most common vulnerabilities can be mitigated by a technology-agnostic checklist applied
consistently across the SDLC — the guide does not teach *how* to implement each practice (that
requires the developer's own security knowledge), only *what* must be checked before code ships.
Verified locally from the actual v2.1 PDF (not just the landing page), the checklist has exactly
14 categories: Input Validation, Output Encoding, Authentication and Password Management, Session
Management, Access Control, Cryptographic Practices, Error Handling and Logging, Data Protection,
Communication Security, System Configuration, Database Security, File Management, Memory
Management, and General Coding Practices.

**Simple explanation**: It's a pre-flight checklist, not a tutorial — like a pilot's checklist
that says "verify flaps" without teaching aerodynamics. For a VPN/Tor/SIEM developer, the most
directly relevant categories are Cryptographic Practices (don't roll your own crypto, use vetted
libraries, protect keys) and Communication Security (validate certs, use TLS correctly, don't trust
unauthenticated data on the wire) — both come up constantly in sections 1 and 2 of this file.

**Try it**: Download the actual PDF (the landing page alone doesn't show the checklist body) and
read the Cryptographic Practices and Communication Security sections specifically, since those are
the two most load-bearing for this file's later VPN/Tor/SIEM sections:
```fish
curl -sL -o (mktemp -t owasp-scp.XXXX.pdf) "https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/assets/docs/OWASP_SCP_Quick_Reference_Guide_v21.pdf"
```
```
# bash/sh:
curl -sL -o /tmp/owasp-scp.pdf "https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/assets/docs/OWASP_SCP_Quick_Reference_Guide_v21.pdf"
```
then `pdftotext -layout <file> - | less` and jump to the "Cryptographic Practices:" and
"Communication Security:" headings (page 9-10 in the v2.1 PDF).

## Noise Protocol Framework

**Claim**: Instead of building a bespoke authenticated-key-exchange (AKE) handshake from scratch
(mixing signatures + DH ad hoc), Noise is a *framework* for composing DH-only handshakes out of a
small vocabulary of message patterns. A handshake pattern is named by up to two letters describing
what each side knows about the other's static public key *before* the handshake starts: `N` = no
static key involved, `K` = static key already known to the peer out-of-band, `X` = static key is
transmitted (and thus encrypted/authenticated) during the handshake, `I` = static key is
transmitted immediately in the first message (trades identity-hiding for fewer round trips). A
full protocol name chains pattern + DH function + cipher + hash, e.g.
`Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s` — this exact string is WireGuard's handshake, decoded as:
pattern `IK` (initiator sends its static key immediately; responder's static key is already known
to the initiator — i.e. WireGuard peers pre-share public keys out of band, so this is mutual
authentication in effectively one round trip), `psk2` (an optional pre-shared symmetric key mixed
in at message 2 for post-quantum-ish defense-in-depth), Curve25519 for DH, ChaCha20-Poly1305 for
AEAD, BLAKE2s for hashing.

**Simple explanation**: Think of Noise as a set of LEGO instructions for "how to shake hands
securely," where the instructions vary based on what each side already knows about the other
before they even start talking (nothing, a known public key, or "I'll show you mine during the
handshake"). WireGuard picked one specific, fixed instruction set (`IK` + these exact primitives)
rather than negotiating cipher suites at runtime like TLS does — that's a deliberate simplicity
choice covered again in section 1's WireGuard spec link.

**Try it**: Decode the WireGuard handshake name against the pattern-letter rules above without
looking it up again — write out, in your own words, what "IK" implies about round-trip count and
identity-hiding compared to Noise's `XX` pattern (where both sides transmit their static key
*during* the handshake instead of one side knowing it in advance), then verify your answer holds
up when you read the actual WireGuard protocol page in section 1 (link 1). This is a paper-only
exercise — no toolchain needed at this stage.

