# 1. VPN Protocol Development — Notes

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 1.

## WireGuard protocol & cryptography spec

**Claim**: WireGuard is a two-message Noise_IK handshake (initiator→responder, responder→initiator)
that gives identity hiding, perfect forward secrecy, and resistance to key-compromise impersonation
and replay, using a fixed (non-negotiated) primitive suite: Curve25519 for DH, ChaCha20-Poly1305
(RFC 7539 AEAD) for symmetric encryption, BLAKE2s for hashing/keying, HKDF (RFC 5869) for key
derivation, SipHash24 for internal hashtable DoS-resistance. Each packet type has a fixed binary
layout — Type 1 (handshake init): sender index, unencrypted ephemeral pubkey, encrypted static
pubkey, encrypted timestamp, two MACs; Type 2 (handshake response): sender/receiver indices,
unencrypted ephemeral pubkey, encrypted empty payload, MACs; Type 4 (data): receiver index, 64-bit
counter (replay protection), encrypted payload. Under load, the responder can demand a cookie
(a MAC of the sender's IP keyed by a secret that rotates every 2 minutes) before doing expensive DH
math, which is the DoS mitigation. Keys rotate automatically: `REKEY_AFTER_TIME` triggers a fresh
handshake, `REKEY_AFTER_MESSAGES` forces one after enough traffic, and `REJECT_AFTER_TIME * 3` is
the hard ceiling after which stale keys are zeroed even with no new handshake.

**Simple explanation**: WireGuard deliberately removed the "choose your cipher suite" negotiation
step that TLS/IPsec have — everyone always uses the same, currently-strong primitives, which
shrinks the attack surface (no downgrade attacks) at the cost of needing a full protocol version
bump if a primitive is ever broken. The handshake is short (2 messages) because both sides already
know each other's public key ahead of time (this is the `IK` pattern from the Noise notes in
section 0) — no certificate authority, no negotiation, just "prove you hold the private key
matching the pubkey I already have for you."

**Try it**: Read the actual packet format tables on the page and cross-check the field ordering
against a local WireGuard install (if present) or the source. Check whether `wg` tooling is
available locally, and if so inspect a real config's public-key format (safe — reading your own
keys, not generating new secrets to leave lying around):
```fish
which wg wg-quick
```
```
# bash/sh:
which wg wg-quick
```
If not installed, note the install command for later without running it (Arch:
`sudo pacman -S wireguard-tools`; Debian: `sudo apt install wireguard-tools`) — this repo's
convention is coding/analysis, not standing up live tunnels, so installing/configuring an actual
interface is optional and out of scope for this exercise.

## WireGuard official whitepaper (PDF)

**Claim**: The whitepaper's core argument (verified locally via `pdftotext`, not a lossy web
summary) is that IPsec's *layering* — separating key exchange (IKEv2), transform/encryption
(xfrm), and interface administration into distinct subsystems — is "strictly correct" but is
exactly what makes it complex and error-prone to implement and deploy. WireGuard's design
collapses these into one thing: a virtual network interface (`wg0`) whose entire security model
is **Cryptokey Routing** — a single table mapping each peer's public key to the set of source IPs
it's allowed to use. On send, the destination IP looks up which peer's key to encrypt with; on
receive, after decryption the *source* IP must match the sending peer's allowed range in that same
table or the packet is dropped. This makes "is this packet authentically from peer X" a table
lookup instead of a separate authentication/firewall layer — outgoing/incoming authorization is
inherent to the crypto, not bolted on. A peer's UDP endpoint (IP:port) is optional in the table and
self-updates from the source address of the last correctly-authenticated packet, which is what
lets WireGuard clients roam across networks (e.g. wifi to mobile data) without a reconnect. The
whole reference implementation is claimed at under 4,000 lines of code specifically because of this
collapsed design, which the paper argues makes it more auditable than IPsec.

**Simple explanation**: Instead of "authenticate the peer, THEN separately decide via firewall
rules what traffic from them is allowed," WireGuard fuses both into one lookup table: know the
public key, and you inherently know what source IPs are legitimate for that key. It's the
"AllowedIPs" setting anyone who has written a WireGuard config file has seen — this paper is the
underlying reason that field exists and does double duty as both routing and access control.

**Try it**: Reconstruct a cryptokey routing table by hand for a 2-peer full-tunnel setup (client
routes 0.0.0.0/0 through a "server" peer) using the paper's own example format (see Configuration
2a in the paper — one peer table entry authorizing `0.0.0.0/0` as allowed source range). Then
inspect whether `wg-quick`'s config file syntax (if installed locally) maps 1:1 onto this table
concept:
```fish
man 8 wg-quick | grep -A3 "AllowedIPs"
```
```
# bash/sh:
man 8 wg-quick | grep -A3 "AllowedIPs"
```
verified locally: `AllowedIPs` in the actual `wg-quick(8)` man page is described exactly as this
paper's cryptokey-routing table column — confirming the paper's abstract concept and the shipped
tool's config field are the same mechanism.

## WireGuard project/source

**Claim**: WireGuard is not one codebase but a family of implementations across platforms sharing
the same wire protocol: `wireguard-linux` (in-tree kernel module, GPLv2, merged upstream since
Linux 5.6), `wireguard-tools` (the `wg`/`wg-quick` userspace CLI, verified installed locally),
`wireguard-go`, `wireguard-rs`, `wireguard-apple`, `wireguard-windows`/`wireguard-nt`,
`wireguard-android`, `wireguard-openbsd`, `wireguard-freebsd` — each a separate git repo under
`git.zx2c4.com`, licensed variously (kernel: GPLv2 to match Linux; userspace tools: MIT/BSD/Apache
2.0 mix depending on the repo). The homepage's positioning is explicitly comparative: "faster,
simpler, leaner...than IPsec," configuration modeled on SSH's public-key-exchange simplicity rather
than IPsec/IKEv2's negotiation complexity — directly continuing the whitepaper's Section 1
argument (link 2 above) about layering complexity being the root problem with IPsec.

**Simple explanation**: There's no single "WireGuard source tree" — cross-platform support means a
cluster of repos, one per OS/language, all implementing the same wire format from the protocol
spec (link 1) so they interoperate. A notable repo worth knowing about for section 5 later:
`wireguard-tamarin` — the Tamarin Prover formal models used to mechanically verify the handshake
(direct link forward to this file's Tamarin Prover entry in section 5).

**Try it**: List the actual repository family instead of trusting a summary, and pick one repo to
inspect structurally (read-only clone to scratch, per this file's repo conventions):
```fish
curl -sL https://www.wireguard.com/repositories/ | grep -oE 'href="[^"]*"' | grep -i git
```
```
# bash/sh:
curl -sL https://www.wireguard.com/repositories/ | grep -oE 'href="[^"]*"' | grep -i git
```
then shallow-clone the userspace tools repo (small, fast) to scratch and look at its layout:
```fish
git clone --depth 1 https://git.zx2c4.com/wireguard-tools /tmp/wg-tools-src ; and ls /tmp/wg-tools-src/src
```
```
# bash/sh:
git clone --depth 1 https://git.zx2c4.com/wireguard-tools /tmp/wg-tools-src && ls /tmp/wg-tools-src/src
```

## Mechanised cryptographic proof of the WireGuard handshake (Lipp, Blanchet, Bhargavan, EuroS&P 2019)

**Claim** (formal-verification paper — theorem/model, not literal text): This is a *computational*
(cryptographic-reduction) proof of WireGuard's Noise_IKpsk2 handshake using the CryptoVerif proof
assistant — distinct from and stronger than the earlier *symbolic* (Tamarin) analysis mentioned in
section 5, because computational proofs can rule out cryptanalytic attacks that symbolic models
assume away. The paper proves: correctness, message secrecy, forward secrecy, mutual
authentication, session uniqueness, resistance to key-compromise impersonation, resistance to
"identity mis-binding," and replay resistance — for the *entire* protocol including the transport
data messages, not just the handshake. Its two genuinely novel theoretical contributions (reusable
beyond WireGuard): (1) a new CryptoVerif model that accounts for the fact that Curve25519, as used
in WireGuard, has **no public-key validation** — points aren't checked to be valid/on-curve before
use, which most textbook DH security proofs assume away, so this is the first mechanised proof to
handle that realistic-but-sloppy real-world detail; (2) the finding that most WireGuard security
properties need only standard AEAD assumptions, but **identity hiding specifically requires a
stronger assumption** that ChaCha20-Poly1305 happens to satisfy but which isn't guaranteed for
every AEAD construction — i.e. if WireGuard swapped ciphers casually, identity hiding could
silently break even though confidentiality wouldn't.

**Simple explanation**: This paper is the mathematical proof that backs up WireGuard's marketing
claim of being simple-and-secure — rather than trusting "it looks clean so it's probably fine,"
these researchers built a machine-checked proof covering the real cryptographic details (including
the specific quirk that WireGuard skips a validation step other protocols do). The one caveat they
surface that a builder should remember: don't assume identity hiding survives a cipher swap just
because confidentiality does — that property rides on a stronger, cipher-specific assumption.

**Try it**: Read the paper's own framing of *why* a mechanised proof matters over a hand-written one
(the "manual proof would need to be carefully reviewed and adapted if WireGuard changed" argument)
and connect it to this file's section 5 Tamarin Prover entry — write a short comparison: what does
a *symbolic* prover (Tamarin) tell you that a *computational* prover (CryptoVerif, used here)
doesn't, and vice versa. Then locate and skim the actual "II. WireGuard" and "Noise IKpsk2" section
locally (WebFetch's markdown conversion loses the protocol diagrams; `pdftotext -layout` preserves
the message-flow figure text better). Use `set` to capture the mktemp'd path so it can be reused
across the following commands. **Environment note, verified on this machine**: `grep` in the
fish config here is a function aliased to `ugrep`, whose default regex dialect treats a *bare*
`|` as alternation (unlike GNU grep's BRE default, where `|` needs a backslash) — so `\|` silently
matches nothing under fish's `grep`. Use `grep -E` with an unescaped `|` so the same pattern works
whether `grep` resolves to GNU grep or ugrep:
```fish
set proof_pdf (mktemp -t wg-proof.XXXX.pdf)
curl -sL -o $proof_pdf https://bblanche.gitlabpages.inria.fr/publications/LippBlanchetBhargavanEuroSP19.pdf
pdftotext -layout $proof_pdf - | grep -E -n "identity hiding requires|Curve25519" | head -10
rm -f $proof_pdf
```
```
# bash/sh:
proof_pdf=/tmp/wg-proof.pdf
curl -sL -o "$proof_pdf" https://bblanche.gitlabpages.inria.fr/publications/LippBlanchetBhargavanEuroSP19.pdf
pdftotext -layout "$proof_pdf" - | grep -E -n "identity hiding requires|Curve25519" | head -10
rm -f "$proof_pdf"
```

## strongSwan (production IPsec/IKEv2 implementation, source)

**Claim**: strongSwan is a production, widely-deployed open-source IPsec VPN implementation
supporting both IKEv1 (legacy) and IKEv2 (current), built around a modular **plugin architecture**
rather than a monolithic daemon — verified locally by cloning: the core IKE/IPsec daemon is
`charon` (in `src/libcharon`), and `src/libcharon/plugins/` contains **65 separate plugin
directories** (confirmed by directory listing), covering EAP authentication variants
(`eap-aka`, `eap-tls`, `eap-mschapv2`, ...), certificate/credential handling, kernel IPsec
backends, and operational concerns (DHCP, connection tracking marks, certificate expiry). Modern
configuration goes through `swanctl` + the `vici` (Versatile IKE Configuration Interface) protocol,
superseding the older `stroke`/`ipsec` command interface. This is architecturally the opposite of
WireGuard's philosophy (link 1-3 above): where WireGuard collapsed everything into one small,
fixed-primitive kernel module, strongSwan stays flexible and standards-compliant by making almost
everything a swappable plugin — the tradeoff the WireGuard whitepaper explicitly critiques as
"complexity" versus what IPsec deployments need for interoperability (RADIUS/EAP integration,
smartcard/TPM support, legacy IKEv1 clients, etc).

**Simple explanation**: If WireGuard is "one opinionated, minimal way to do a VPN," strongSwan is
"an extensible framework that can be configured to speak whatever IPsec variant a given enterprise
network already requires" — the plugin count alone (65) is a proxy for how much more configuration
surface (and thus complexity) a production IPsec deployment carries compared to a WireGuard
deployment.

**Try it**: Shallow-clone and inspect the real repo structure rather than trusting a GitHub summary
page (verified working, clone completes in seconds):
```fish
git clone --depth 1 https://github.com/strongswan/strongswan /tmp/strongswan-src
ls /tmp/strongswan-src/src
ls /tmp/strongswan-src/src/libcharon/plugins | wc -l
```
```
# bash/sh:
git clone --depth 1 https://github.com/strongswan/strongswan /tmp/strongswan-src
ls /tmp/strongswan-src/src
ls /tmp/strongswan-src/src/libcharon/plugins | wc -l
```
then clean up (do not leave the clone in the repo):
```fish
rm -rf /tmp/strongswan-src
```

## strongSwan project docs

**Claim**: Beyond the source repo (previous link), strongswan.org documents the operational
feature set that justifies the plugin-heavy architecture: RFC 7296 (IKEv2, matches section 1's own
spec link below) with IPv6 and message fragmentation, **MOBIKE** (mobility — a peer can change its
IP/interface mid-session and the tunnel survives, the IPsec-world analogue of WireGuard's
roaming-via-endpoint-rediscovery from the whitepaper notes above), a wide authentication matrix
(EAP methods, X.509 certs, PSK, smartcard/TPM), **post-quantum key exchange (ML-KEM)** and modern
curves (Ed25519) alongside legacy algorithm support, NAT traversal (UDP encapsulation, port
floating), and Trusted Network Connect (TNC) — a network-access-control standard for checking a
connecting device's health/posture before admitting it, which has no WireGuard equivalent at all.
It runs across Linux 2.6 through 6.x kernels plus Android/FreeBSD/macOS/iOS/Windows ports.

**Simple explanation**: This page answers "why does strongSwan need 65 plugins?" concretely — each
highlighted feature (MOBIKE, TNC, post-quantum KEX, multiple EAP methods) is a real enterprise
requirement that WireGuard deliberately doesn't try to solve, because IPsec/IKEv2 has to
interoperate with decades of existing enterprise infrastructure (RADIUS servers, smartcards,
network-access-control policies) while WireGuard only has to interoperate with itself.

**Try it**: Cross-reference one specific feature against the actual IKEv2 RFC covered later in this
section (link 7, RFC 7296) — find where MOBIKE is referenced in the RFC text itself:
```fish
curl -sL https://www.rfc-editor.org/rfc/rfc7296 | grep -E -i -n "mobike|mobility" | head -10
```
```
# bash/sh:
curl -sL https://www.rfc-editor.org/rfc/rfc7296 | grep -E -i -n "mobike|mobility" | head -10
```

## IKEv2 protocol spec (RFC 7296)

**Claim**: The rendered HTML at `rfc-editor.org/rfc/rfc7296` is heavy with CSS/JS chrome that
drowns the actual normative text; the same document is available as clean plain text at
`rfc-editor.org/rfc/rfc7296.txt` (verified: `HTTP 200`, `content-type: text/plain`), which is the
better source to grep/read directly — same convention as this repo's man7.org and FHS work
preferring the authoritative plain source over a lossy render. IKEv2's structure (confirmed from
the real ToC and Section 1.1 body text) is request/response **exchanges**, not free-form messages:
`IKE_SA_INIT` negotiates security parameters, exchanges nonces and Diffie-Hellman values;
`IKE_AUTH` transmits identities, proves possession of the corresponding secrets, and sets up the
first Child SA (an ESP/AH security association carried inside the authenticated IKE SA);
`CREATE_CHILD_SA` creates additional/rekeyed Child SAs; `INFORMATIONAL` deletes SAs, reports
errors, or does liveness checks. In the common case that's 2 exchanges / 4 messages to fully
establish a tunnel — contrast with WireGuard's 2-message total handshake (link 1 above). Critically,
IKEv2 **negotiates** cipher suites (algorithms are proposed and matched in a mix-and-match fashion)
rather than fixing them, which is exactly the "complexity/flexibility" tradeoff the WireGuard
whitepaper (link 2) argues against and the "negotiation enables downgrade attacks" theme that
recurs in section 4 (offensive concepts — real-world IKEv1 auth-bypass).

**Simple explanation**: Where WireGuard is "one handshake, always," IKEv2 is "negotiate first (what
algorithms, what identities), then prove who you are, then set up the actual data-protection SA" —
more steps and more configurability, which is why strongSwan (links 5-6) needs 65 plugins to cover
the negotiation space IKEv2 allows.

**Try it**: Fetch the plain-text RFC (not the JS-heavy HTML render) and confirm the four exchange
types and their ordering constraint (`IKE_SA_INIT` and `IKE_AUTH` MUST complete before any
`CREATE_CHILD_SA`/`INFORMATIONAL` exchange) directly from the normative text:
```fish
curl -sL https://www.rfc-editor.org/rfc/rfc7296.txt -o (mktemp -t rfc7296.XXXX.txt)
```
```
# bash/sh:
curl -sL https://www.rfc-editor.org/rfc/rfc7296.txt -o /tmp/rfc7296.txt
```
then grep the exchange-type names and read the surrounding paragraph (Section 1, around line 300 in
the fetched file as of the October 2014 revision):
```fish
grep -n "IKE_SA_INIT|IKE_AUTH|CREATE_CHILD_SA|INFORMATIONAL" -E /tmp/rfc7296.txt | head -10
```

## OpenVPN community resources (WireGuard mesh-VPN guide, OpenVPN blog)

**Claim**: This OpenVPN-authored post makes an important architectural point that the WireGuard
protocol spec itself (link 1) doesn't emphasize: WireGuard has **no concept of a user, directory,
SSO, or MFA built in** — it deliberately only solves "encrypted tunnel between two known public
keys," leaving identity/key-distribution/access-policy entirely to external tooling. This connects
to a second distinction the post draws: **mesh** VPN topology (direct point-to-point encrypted
tunnels between every pair of peers who need to talk) vs. **hub-and-spoke** (all traffic routes
through a central gateway) — and within mesh designs, separating the **control plane**
(coordinating who has which key, and what policy applies) from the **data plane** (the actual
encrypted peer-to-peer traffic). WireGuard is *only* a data-plane primitive; a real mesh product
(the post's own example: OpenVPN's CloudConnexa, which notably does NOT use WireGuard at all, using
OpenVPN protocol instead) has to build the control plane itself.

**Simple explanation**: WireGuard is a brick, not a house — an extremely good encrypted-tunnel
brick, but someone still has to build identity management, key distribution, and mesh topology
coordination around it before it's a deployable product for an organization with actual users.
This is the same "engineering vs. primitives" theme as section 0's Cryptography Engineering entry,
applied concretely: the primitive (WireGuard's handshake) being provably secure doesn't mean a
*product* built from it is automatically secure or even functional without solving identity/control
plane separately.

**Try it**: Write a short design note (no code) sketching what a minimal control plane for a
WireGuard mesh would need to do: (1) generate/distribute each peer's static keypair, (2) tell every
peer every other peer's current public key + endpoint, (3) handle a peer leaving/being revoked. Then
check the actual `wg` config format to see how brittle *manual* key distribution is without such a
control plane — verified locally: `AllowedIPs`/`PublicKey`/`Endpoint` are all static text a human
must edit per peer:
```fish
man 8 wg-quick | grep -B2 -A8 "^CONFIGURATION"
```
```
# bash/sh:
man 8 wg-quick | grep -B2 -A8 "^CONFIGURATION"
```

## WireGuard vs IPsec vs OpenVPN architecture comparison

**Claim**: This comparison ties together everything covered earlier in this section into a single
practical decision table. Performance: WireGuard is reported ~20% lower latency / ~15% higher
throughput than IPsec, attributed directly to the small, fixed-primitive, connectionless design
covered in links 1-3 (no negotiation overhead, small codebase = less processing per packet).
Security posture: WireGuard's minimal codebase makes external audit tractable (ties to the
whitepaper's <4000-LOC claim and the mechanised-proof paper, links 2 and 4); IPsec's support for
legacy/negotiable algorithms is a double-edged sword — broad compatibility but larger
misconfiguration/downgrade surface (foreshadows section 4's real-world IKEv1 auth-bypass entry).
Operational behavior: WireGuard's connectionless design (no explicit session teardown/handshake
state machine to get "stuck" in) enables the roaming behavior from the whitepaper's Cryptokey
Routing / endpoint-rediscovery mechanism; IPsec's more stateful connection model can hang on brief
network interruptions. Compatibility: IPsec has broader *native* OS support (built into
Windows/iOS/Android's OS-level VPN frameworks) vs. WireGuard needing a userspace app on mobile —
directly the identity/deployment gap the OpenVPN blog post (link 8) raised. Net recommendation
given: WireGuard for performance-sensitive/peer-to-peer/remote-access use cases; IPsec where
regulatory compliance or legacy-hardware interoperability is the hard requirement.

**Simple explanation**: This is the "so which one do I actually build/deploy" summary — WireGuard
wins on speed/simplicity/auditability, IPsec wins on broad native OS support and mature
standards-track compliance credentials. Neither is universally "better"; the choice tracks directly
back to which tradeoff (this section's links 1-7) matters more for a given deployment.

**Try it**: Build your own one-page comparison table from what's now been verified locally in this
section, rather than trusting a third-party blog's numbers blindly — fill in a table with rows
{Handshake message count, Fixed vs negotiated ciphersuite, Reference impl LOC/plugin count, Native
mobile OS support, Roaming mechanism} and columns {WireGuard, IPsec/strongSwan}, using only what
was verified in links 1-7 of this notes file (2 vs 4 messages; fixed vs negotiated; <4000 LOC vs 65
plugins; app vs OS-native; cryptokey-routing vs MOBIKE). This produces a locally-grounded version of
the same comparison the zenarmor article makes, cross-checked against primary sources instead of
taken on faith.
