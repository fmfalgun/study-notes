# 1. VPN (Normal) — Notes

## VPN concepts overview (Wikipedia)

**Claim**: A VPN is an overlay network — it uses tunneling (encapsulating one packet inside
another) plus encryption to extend a "private" trust boundary across a public/untrusted network.
Two deployment shapes cover almost all real use: remote-access (one host tunnels into a network,
e.g. an employee's laptop) and site-to-site (two gateways tunnel two whole networks together,
e.g. office-to-datacenter). Major tunneling protocols, in order of age: IPsec (1996, often
hardware-accelerated, works at the network layer), TLS/SSL-based (1999, e.g. OpenVPN uses this),
OpenVPN (2001), WireGuard (2015, deliberately minimal/modern). Critically: a VPN gives you
confidentiality + integrity (via MACs) from your ISP/local network's view, but it does **not**
give you anonymity — the VPN provider (and anyone downstream of the VPN exit) still sees your
real traffic and can correlate you to it, and connection metadata (that a tunnel exists, when,
to where) is still visible to your ISP even if the payload isn't.

**Simple explanation**: A VPN is a locked, opaque tube from your device to some other point on
the internet — anyone watching the wire between you and that point sees only the tube, not
what's inside it. But whoever is standing at the *far end* of the tube (the VPN provider) sees
your traffic in the clear, same as your ISP would without a VPN. "VPN = anonymous" is a common
misconception this article explicitly warns against.

**Try it**: Inspect this machine's own default routing/tunnel-free path, then reason about what a
VPN would change. No VPN client needed to observe the baseline.
```fish
# see current default route and interface — no tunnel present
ip route show default
# confirm no vpn/tunnel interfaces exist right now (tun*/wg*/ppp* naming conventions)
ip -brief link show
```
bash/sh: identical syntax.
Applied exercise: draw a diagram of remote-access vs site-to-site VPN topology, labeling exactly
where encryption starts/ends in each, and mark the one segment in each diagram where traffic is
still in cleartext relative to the *destination* server (the VPN-provider-to-destination hop for
a commercial VPN, or LAN segments behind either gateway for site-to-site).

## WireGuard protocol & cryptography

**Claim**: WireGuard's handshake is Noise_IK from the Noise Protocol Framework — a 2-message
(1 round-trip) handshake, much simpler than IPsec/IKEv2's multi-message negotiation, because it
hard-codes one specific cipher suite instead of negotiating options: Curve25519 for ECDH key
exchange, ChaCha20-Poly1305 as the AEAD cipher, BLAKE2s for hashing, SipHash24 for internal
hashtable lookups (DoS-resistance, not cryptographic security per se), and HKDF for key
derivation. The handshake gives forward secrecy (an ephemeral key pair is generated per
handshake) and identity hiding (the initiator's static public key is itself encrypted in message
1, so a passive observer can't identify who is connecting without already knowing who to look
for). Keys auto-rotate: a new handshake happens on a timer (REKEY_AFTER_TIME) or after a message
count threshold (REKEY_AFTER_MESSAGES), independent of whether the session is idle, bounding the
damage of any one session key's compromise.

**Simple explanation**: Where older VPN protocols are "negotiate everything" (which cipher? which
hash? which key size?), WireGuard is "there is exactly one modern, vetted answer" — this is why
its entire codebase is a few thousand lines versus OpenVPN/IPsec's tens of thousands, and why
that's considered a *security* feature, not just a simplicity one (less code, less negotiable
surface area, less to get wrong).

**Try it**: Generate a real WireGuard keypair locally (no network setup needed — this alone
demonstrates the Curve25519 key generation step of the protocol).
```fish
wg genkey > /tmp/wgtest_priv.key
cat /tmp/wgtest_priv.key | wg pubkey > /tmp/wgtest_pub.key
cat /tmp/wgtest_priv.key   # base64 32-byte Curve25519 private scalar
cat /tmp/wgtest_pub.key    # corresponding public point
rm /tmp/wgtest_priv.key /tmp/wgtest_pub.key
```
bash/sh: identical (`wg` CLI syntax is shell-independent); note the tool itself warns
`Warning: writing to world accessible file. Consider setting the umask to 077` — a real reminder
that private key material needs restrictive file permissions even in a throwaway test.
Arch: `wireguard-tools` package provides `wg`/`wg-quick` (already installed here). Debian:
`apt install wireguard-tools`.

## WireGuard project home

**Claim**: The project's own positioning (beyond the crypto detail in the previous link) is
about auditability and operational simplicity as security properties. It explicitly aims to be
"comprehensively reviewable by a single individual" — a direct contrast with IPsec/OpenVPN
codebases too large for one person to fully audit. Its most distinctive mechanism not covered by
the protocol page is **Cryptokey Routing**: each peer's WireGuard public key is bound to a list
of `AllowedIPs` — source/destination IP ranges that key is permitted to send/receive for. This
single table does double duty as both the routing table AND the access-control/authentication
mechanism (if a packet's source IP doesn't match the sending peer's AllowedIPs, it's dropped) —
conceptually similar to how SSH binds authorized actions to a public key in `authorized_keys`.
It runs as an in-kernel module on Linux (confirmed present on this machine) for performance, and
as a userspace implementation elsewhere (Windows/macOS/BSD/iOS/Android), and is licensed GPLv2
for the kernel module.

**Simple explanation**: A WireGuard config isn't "here's my routing table" and separately "here's
my access control list" — it's one list where a peer's public key IS its identity and its
`AllowedIPs` entry IS the rule for both "where do I send packets meant for this peer" and "which
packets from this peer do I actually trust." Fewer moving parts to misconfigure.

**Try it**: Confirm the kernel module is present and inspect the Cryptokey Routing config syntax
(without bringing up a real interface).
```fish
# confirm in-kernel WireGuard is available on this machine
modinfo wireguard | head -5

# no interfaces currently up (expected — nothing configured)
wg show

# write a throwaway config to see AllowedIPs/Cryptokey Routing syntax (never applied — just inspecting)
set -l demo_peer_pub (wg genkey | wg pubkey)
printf "[Interface]\nPrivateKey = <redacted>\nAddress = 10.10.10.1/24\n\n[Peer]\nPublicKey = %s\nAllowedIPs = 10.10.10.2/32\n" $demo_peer_pub
```
bash/sh: `demo_peer_pub=$(wg genkey | wg pubkey)` replaces the `set -l` line; the rest is
identical. Arch: kernel module ships in-tree since Linux 5.6 (confirmed via `modinfo` above,
no extra package needed here). Debian (older kernels): `apt install wireguard-dkms` if the
in-kernel module isn't present.

## OpenVPN fundamentals & community resources — "WireGuard Mesh VPN Guide" (OpenVPN blog)

**Claim** (note: the linked page's actual content is a mesh-vs-hub-and-spoke architecture guide,
not a general OpenVPN protocol tutorial — captured accurately here rather than force-fit to the
list's label): it draws a topology distinction orthogonal to protocol choice. **Hub-and-spoke**
(the traditional VPN/OpenVPN-server model): every peer connects to one central concentrator;
peer-to-peer traffic detours through that hub even if the peers are on the same LAN. **Mesh**:
peers connect directly to each other over encrypted tunnels; a lightweight control-plane server
only handles key distribution and policy, not the actual traffic. It notes WireGuard-the-protocol
deliberately has no opinion on identity, directory services, or config distribution — that's
explicitly out of scope for the protocol itself, so any real mesh product (e.g. Tailscale,
OpenVPN CloudConnexa) has to build an identity/SSO/ACL layer on top. Mesh's practical cost is NAT
traversal: two devices behind separate NATs/CGNAT can't just dial each other, so mesh systems use
STUN/ICE/UDP hole-punching to try direct paths, falling back to a relay server (with a real
performance hit) when a firewall blocks the direct route. Every mesh endpoint also needs its own
running agent — devices that can't run one (printers, IoT, legacy boxes) can't join the mesh
directly.

**Simple explanation**: Hub-and-spoke is like every phone call in a company going through a
receptionist, even calls between two people sitting next to each other. Mesh is everyone having
each other's direct number — faster, but now you need a phone book (control plane) and some calls
still can't connect directly (bad phone reception = strict NAT), so they fall back through the
receptionist anyway.

**Try it**: This is a topology/architecture concept, not a single tool invocation — the concrete
exercise is diagramming and reasoning about the tradeoff, informed by real WireGuard config
syntax already demonstrated in the previous entry.
1. Diagram hub-and-spoke: 4 laptops, each with a `[Peer]` block pointing only at a central
   server's public key/AllowedIPs. Mark the path packet-A-to-B takes.
2. Diagram mesh: same 4 laptops, each with 3 `[Peer]` blocks (one per other laptop). Mark the
   path packet-A-to-B takes and note it's now direct.
3. Identify, in the mesh diagram, which single component (the control-plane/coordination server)
   is doing strictly less work than the hub-and-spoke central server, and explain why that's the
   performance/scalability win despite mesh needing more total tunnel configs.

## IPsec / IKEv2 concepts (RFC 7296)

**Claim** (verified via `curl` on the RFC's official `.txt` release — the HTML page at
`rfc-editor.org/rfc/rfc7296` is a JS-rendered app that doesn't yield readable text via WebFetch or
plain tag-stripping, so the canonical plaintext export was used instead, same convention as this
repo's GNU-manual notes): RFC 7296 defines IKEv2, the key-exchange protocol that establishes the
shared cryptographic state IPsec itself needs (IPsec/ESP/AH do the actual packet
encryption/authentication; IKE negotiates and rotates the keys/algorithms for that). Every IKE
message is a request/response pair called an "exchange." There are exactly 4 exchange types,
and they're strictly ordered: **IKE_SA_INIT** (negotiate crypto algorithms, exchange nonces and
Diffie-Hellman values — this is unauthenticated) must complete first, then **IKE_AUTH**
(transmit identities, prove each side actually knows the claimed secret, and set up the first
"Child SA" for real traffic) must complete, and only after both of those may **CREATE_CHILD_SA**
(add more Child SAs, or rekey an existing IKE/Child SA) and **INFORMATIONAL** (delete an SA,
report errors, or serve as a liveness check via an empty request) exchanges happen, in any order,
any number of times. The IKE SA itself is the "control channel"; Child SAs are the actual
data-protecting SAs (mapping to ESP/AH) — separating control-channel setup from data-channel setup
is the key structural idea. The common case is 2 exchanges / 4 messages total to get the first
tunnel up.

**Simple explanation**: IKEv2 is IPsec's separate "let's agree on a secret and prove who we are"
handshake protocol, distinct from the encryption that later protects your actual traffic. Step 1
(IKE_SA_INIT) is like exchanging Diffie-Hellman values in the open ("here's my half of the math
problem") — anyone can see this, no identity proven yet. Step 2 (IKE_AUTH) is now encrypted with
keys derived from step 1, and is where each side proves "I really am who I claim to be" and
agrees what traffic gets protected (the Child SA). Everything after that (rekeying, adding more
protected traffic classes, tearing down) reuses the already-authenticated channel.

**Try it**: This is a protocol spec, not a runnable tool by itself (strongSwan, the next link,
provides the actual implementation) — the applied exercise is tracing the exchange structure
directly from the RFC text.
```fish
curl -sL https://www.rfc-editor.org/rfc/rfc7296.txt -o /tmp/rfc7296.txt
grep -n "^1\.\|IKE_SA_INIT\|IKE_AUTH\|CREATE_CHILD_SA\|INFORMATIONAL" /tmp/rfc7296.txt | head -20
rm /tmp/rfc7296.txt
```
bash/sh: identical (curl/grep syntax doesn't depend on shell).
Applied exercise: from the grep output plus Section 1.2 ("The Initial Exchanges"), diagram the
4-message handshake (IKE_SA_INIT request/response, IKE_AUTH request/response) as a sequence
diagram, labeling exactly which message pair is unauthenticated and which is encrypted+authenticated.

## strongSwan (real-world IPsec deployment/config)

**Claim**: strongSwan is a real, widely-deployed open-source implementation of exactly the RFC
7296 protocol just studied (plus legacy IKEv1). Confirmed installed on this machine (version
6.0.7) — its architecture splits into a background daemon (`charon`) that actually speaks
IKE/manages Security Associations, and CLI tools (`swanctl`, plus legacy `ipsec`) that talk to
that daemon over a local control socket (`vici`) to load configuration and trigger
connect/disconnect. Configuration lives in `swanctl.conf`, organized into `connections` (peer
definitions: local/remote addresses, IKE version, auth method), `secrets` (PSKs/certs), and
`pools` (virtual IP address ranges for remote-access clients) sections — directly mapping onto
the IKE SA / Child SA / authentication concepts from RFC 7296. It advertises modern features
beyond the base RFC: MOBIKE (RFC 4555, lets a mobile client keep its IKE SA alive across a
network/IP change — e.g. wifi to cellular handoff), EAP-based auth methods for enterprise
2FA/RADIUS integration, and (notably, ahead of most VPN tooling) post-quantum ML-KEM key exchange
support.

**Simple explanation**: If RFC 7296 is the rulebook, strongSwan is a real referee that actually
plays the game — `charon` is the daemon doing the IKE handshakes, `swanctl` is the tool an admin
uses to say "here are the peers I want to trust and how," and the config file's structure
(`connections`/`secrets`/`pools`) is IKE's abstract IKE-SA/Child-SA/authentication concepts made
concrete and administrable.

**Try it**: Inspect the real, installed strongSwan toolchain and its config schema via local man
pages (config file itself is root-only 0640, appropriately, since it can contain PSKs — so the
exercise is reading tool output + docs, not the live secrets).
```fish
ipsec version
swanctl --version
# daemon isn't running (expected — no service configured), confirms client/daemon split:
swanctl --version --daemon
# config file schema, straight from the installed strongSwan package's own man pages:
man 5 swanctl.conf | head -60
```
bash/sh: identical (no shell-specific syntax used).
Arch: `pacman -S strongswan` (already installed here). Debian: `apt install strongswan
strongswan-swanctl`.

## WireGuard vs IPsec vs OpenVPN comparison (Zenarmor)

**Claim** (note: the fetched article content is weighted toward an IPsec-vs-WireGuard comparison
specifically, with OpenVPN mentioned only in passing — captured as actually returned): the
article's comparison collapses to one root cause repeated in earlier links — WireGuard's small,
fixed-cipher-suite, UDP-only design — and traces its downstream effects. Performance: WireGuard
benchmarks ~20% lower latency / ~15% higher throughput than IPsec in the article's cited tests,
attributed to simpler per-packet processing. Auditability: IPsec implementations like Openswan
exceed 100,000 lines of code across languages, vs. WireGuard's minimal codebase (already observed
directly in this study set — WireGuard's own site claims single-person-reviewable). Crypto
agility is framed as a tradeoff, not a pure downside: IPsec's negotiable suites (including legacy
RSA/PSK) are *why* it remains necessary for regulatory/legacy-compatibility scenarios that must
interoperate with old gear, while WireGuard's fixed modern suite removes an entire class of
misconfiguration risk but can't talk to anything that doesn't also speak WireGuard. Roaming:
WireGuard has no formal "connection" state tied to an IP (it's just "does this packet decrypt
correctly with this peer's key"), so a client changing IP (wifi to cellular) doesn't need a
protocol-level re-handshake the way a connection-oriented tunnel might.

**Simple explanation**: IPsec is the flexible-but-heavy option you're stuck with when talking to
older/regulated infrastructure that requires it; WireGuard is the fast, simple, modern option
when you control both ends and don't need legacy interop. Neither is "just better" — the
comparison is really "how much do you need negotiability/legacy support vs. simplicity/speed."

**Try it**: Concretely observe two of the article's claims already verifiable with tools
confirmed present on this machine — WireGuard's UDP-only transport, and the "no formal connection
state" roaming design — by reading the installed docs rather than a live comparison benchmark
(no real WireGuard tunnel is configured here to benchmark against).
```fish
# WireGuard is UDP-only by design — confirm via its own man page (no TCP option exists)
man 8 wg-quick | grep -i -A2 "ListenPort"

# IPsec/IKE negotiates over UDP 500/4500 but the protocol itself supports multiple transforms —
# see the cipher-suite negotiation surface directly in the RFC 7296 text pulled in link 5
grep -n "Transform Type" /tmp/rfc7296.txt 2>/dev/null || echo "(re-fetch rfc7296.txt from link 5 if needed)"
```
bash/sh: identical.
Applied exercise: build a 3-column comparison table (WireGuard / IPsec+IKEv2 / OpenVPN) covering
codebase size, cipher agility, typical use case, and NAT/roaming behavior, using facts gathered
across links 2, 3, 5, 6, and this one.

## VPN internals: protocols, leaks, kill switches

**Claim**: A VPN client works by intercepting packets at the OS network-stack level before
routing, encrypting them, and re-wrapping them addressed to the VPN server, which unwraps and
forwards to the real destination — from the destination's point of view all traffic appears to
originate from the VPN server's IP. The article's real contribution over earlier links is the
**leak taxonomy**: (1) DNS leaks — if the OS's system DNS resolver isn't repointed at the VPN's
resolver, plaintext DNS queries go out via the normal (non-tunneled) network path even while
other traffic is tunneled, letting the ISP see every hostname resolved; (2) WebRTC leaks — browser
WebRTC uses STUN directly from the browser's own network stack (bypassing the OS-level VPN
routing entirely in some configurations) and can leak the real IP to any website using WebRTC;
(3) IPv6 leaks — many VPN clients only capture/tunnel IPv4 traffic, so if the network also hands
out a routable IPv6 address, that IPv6 path stays completely outside the tunnel. A kill switch
is a firewall rule set (not a VPN protocol feature) that blocks all non-VPN-interface traffic so
that if the tunnel drops, nothing leaks out unprotected instead of silently falling back to the
normal route — but the article flags a real 2025 finding that there's a brief timing gap between
tunnel failure and firewall-rule activation where some traffic can still escape.

**Simple explanation**: A VPN tunnel only protects what actually goes *through* it. DNS queries,
WebRTC's own direct connections, and IPv6 traffic are three separate paths off your machine that
a naively-configured VPN client can simply forget to route into the tunnel — each looks like "the
VPN is on" while quietly leaking exactly the data you thought was hidden. A kill switch is the
safety net for when the tunnel itself fails, not for these routing gaps.

**Try it**: Inspect this machine's actual DNS and IPv6 exposure (no VPN active here, so this shows
the *baseline* an actual VPN client would need to override), plus read (not apply) a kill-switch
firewall-rule pattern.
```fish
# DNS leak surface: what resolver would plaintext DNS actually go to right now?
cat /etc/resolv.conf

# IPv6 leak surface: does this machine even have a routable global IPv6 address to leak?
ip -6 addr show scope global
# (empty output on this machine = no global IPv6 currently assigned, so no IPv6-leak surface
# exists right now — but this is exactly the kind of check a VPN client needs to make dynamically)
```
bash/sh: identical.
```fish
# (Optional, root, read-only) inspect a kill-switch-style DROP-by-default nftables pattern —
# NOT applied here, just the rule shape you'd review in a real client's firewall config:
# table inet killswitch {
#   chain output {
#     type filter hook output priority 0; policy drop;
#     oifname "wg0" accept
#     oifname "lo" accept
#     ip daddr <vpn-server-ip> accept
#   }
# }
sudo nft list ruleset | head -20   # read current live ruleset, if any (requires root)
```
Arch/Debian: `nft`/`iptables` both ship in base install on most distros; confirmed present here.

## DNS leaks (Wikipedia)

**Claim**: A DNS leak is defined as DNS requests reaching the ISP's (or another untrusted)
resolver despite a VPN being active. The article's specific named cause is split-tunnel
configurations plus OS-level "smart" multi-homed resolution (its concrete example: Windows 8's
Smart Multi-Homed Named Resolution, which fires DNS queries across *every* available network
interface simultaneously "for speed," so even with a VPN's tunnel interface up, the query also
races out the physical NIC's default resolver and whichever answers first wins) — this
generalizes the DNS-leak point already made more briefly in the previous link. Mitigations
listed: encrypt DNS itself (DoH/DoT, so even a "leaked" query isn't plaintext to the ISP),
choose a VPN client that explicitly forces all DNS through the tunnel interface, manually pin
the DNS server on the network adapter to the VPN's resolver, or use a client (Tor Browser is the
named example) that handles name resolution entirely inside its own protected path rather than
delegating to the OS resolver at all.

**Simple explanation**: The VPN might correctly encrypt your web traffic while your computer,
trying to be "smart" about speed, quietly still asks the question "what's the IP for
example.com?" to your regular ISP-assigned DNS server over the open network — same failure mode
as the DNS-leak point in the previous link, described here with the concrete Windows mechanism
that causes it.

**Try it**: Demonstrate the core mechanism DNS-leak-test websites use — special debug DNS records
that reveal which resolver actually answered a query — directly against different resolvers from
this machine.
```fish
# Google's debug record: reveals what IP/subnet Google's resolver sees you querying from
dig +short TXT o-o.myaddr.l.google.com @8.8.8.8

# OpenDNS's debug record queried directly against OpenDNS — reveals your real public IP as seen
# by that specific resolver
dig +short myip.opendns.com @resolver1.opendns.com

# now the SAME query through this machine's normal system resolver (not pinned to OpenDNS) —
# verified result on this machine: returns nothing, because myip.opendns.com only resolves
# meaningfully when the query actually lands on OpenDNS's own infrastructure
dig +short myip.opendns.com
```
bash/sh: identical. This is exactly dnsleaktest.com's underlying method generalized: a real DNS
leak test checks *which* resolvers respond to your queries while a VPN is active — if an
unexpected resolver (e.g. your ISP's, instead of the VPN provider's) answers, that's the leak.
