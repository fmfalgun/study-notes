# 1. VPN (Normal) — Exercises

## 1. VPN concepts overview

1. Run `ip route show default` and `ip -brief link show` on this machine. Confirm there is no
   active VPN/tunnel interface (look for absence of `tun*`, `wg*`, `ppp*`, `tap*` names).
2. Draw the remote-access VPN topology: laptop -> encrypted tunnel -> corporate gateway ->
   internal resource. Mark which segment(s) are encrypted and which are not.
3. Draw the site-to-site VPN topology: LAN A -> gateway A -> encrypted tunnel -> gateway B -> LAN
   B. Mark which segment(s) are encrypted and which are not (hint: traffic inside each LAN,
   before/after the gateway, is not covered by the VPN tunnel itself).
4. Write 3 sentences explaining why "I used a VPN so I'm anonymous" is wrong, specifically
   distinguishing confidentiality (what a VPN provides) from anonymity (what it does not).
5. List the 4 tunneling protocols named in the article in chronological order and one
   distinguishing fact about each (hardware acceleration, layer, age, design philosophy).

## 2. WireGuard protocol & cryptography

1. Generate a WireGuard keypair:
   ```fish
   wg genkey > /tmp/wgtest_priv.key
   cat /tmp/wgtest_priv.key | wg pubkey > /tmp/wgtest_pub.key
   cat /tmp/wgtest_priv.key
   cat /tmp/wgtest_pub.key
   rm /tmp/wgtest_priv.key /tmp/wgtest_pub.key
   ```
   (Arch: `sudo pacman -S wireguard-tools` if `wg` is missing. Debian: `sudo apt install
   wireguard-tools`.)
2. Note the umask warning WireGuard prints. Explain in 1-2 sentences why a private key file with
   world-readable permissions (mode 644) is a real security problem, and what `umask 077` before
   key generation would change.
3. List, in order, the 5 cryptographic primitives WireGuard hard-codes (key exchange, AEAD
   cipher, hash, keyed hash for hashtables, KDF) and match each to the one job it does.
4. Explain in 3-4 sentences why hard-coding one cipher suite (vs. IPsec/TLS-style negotiation of
   multiple supported suites) is considered a security advantage, not just a simplicity one —
   specifically mention downgrade attacks as the class of problem this design avoids entirely.
5. Explain what "identity hiding" means in the Noise_IK handshake (which message encrypts the
   initiator's static public key, and why a passive network observer capturing the handshake
   can't extract it without already knowing the responder's public key to test against).

## 3. WireGuard project home (Cryptokey Routing)

1. Confirm the kernel module and CLI are present:
   ```fish
   modinfo wireguard | head -5
   wg show
   ```
   (`wg show` prints nothing if no interfaces are configured — that's the expected/correct state
   here, not an error.)
2. Generate a throwaway config snippet showing Cryptokey Routing syntax (does not create or
   activate any interface):
   ```fish
   set -l demo_peer_pub (wg genkey | wg pubkey)
   printf "[Interface]\nPrivateKey = <redacted>\nAddress = 10.10.10.1/24\n\n[Peer]\nPublicKey = %s\nAllowedIPs = 10.10.10.2/32\n" $demo_peer_pub
   ```
   bash/sh: `demo_peer_pub=$(wg genkey | wg pubkey)` then the same `printf` line.
3. In the output config, identify: which line is the routing decision, and which line is the
   authentication decision. Explain in 2-3 sentences why they're the same line in WireGuard
   (Cryptokey Routing) but two separate mechanisms in a traditional router + VPN setup.
4. Write 2-3 sentences on what "comprehensively reviewable by a single individual" means as a
   security design goal, and why a smaller trusted computing base (TCB) reduces risk independent
   of how strong the underlying crypto primitives are.
5. List the platforms WireGuard supports (Linux in-kernel vs. userspace elsewhere) and explain in
   1-2 sentences why an in-kernel implementation is typically faster than a userspace one for a
   VPN data path.

## 4. OpenVPN fundamentals / mesh vs hub-and-spoke

1. Diagram (ASCII or description) a hub-and-spoke VPN with 4 endpoints, all connecting to one
   central server. Trace the path a packet from endpoint A to endpoint B takes.
2. Diagram the same 4 endpoints as a full mesh (each peer has a direct tunnel to every other
   peer). Trace the same A-to-B path and note it no longer passes through a central relay.
3. Count the number of tunnel configs needed in each topology for N=4 endpoints, then generalize
   the formula for hub-and-spoke (N tunnels) vs full mesh (N*(N-1)/2 tunnels). At what N does
   mesh's config count start to look impractical to manage by hand?
4. Write 2-3 sentences on why WireGuard-the-protocol has no built-in concept of "user identity"
   or "which peers should be allowed to mesh with which" — and why that's a deliberate design
   choice (small TCB) rather than an oversight, pushed instead onto tools like Tailscale/
   CloudConnexa/Headscale.
5. Explain NAT traversal fallback in 2-3 sentences: what STUN/ICE/hole-punching try to achieve,
   and why a mesh product must still support falling back to a relay server for some peer pairs
   (e.g. both sides behind symmetric/carrier-grade NAT).

## 5. IPsec / IKEv2 concepts (RFC 7296)

1. Fetch the RFC's plaintext export and locate the exchange types:
   ```fish
   curl -sL https://www.rfc-editor.org/rfc/rfc7296.txt -o /tmp/rfc7296.txt
   grep -n "^1\.\|IKE_SA_INIT\|IKE_AUTH\|CREATE_CHILD_SA\|INFORMATIONAL" /tmp/rfc7296.txt | head -20
   ```
   bash/sh: identical.
2. Read Section 1 ("Introduction") and Section 1.2 ("The Initial Exchanges") in the downloaded
   text (`grep -n "^1.2" /tmp/rfc7296.txt` to find the line number, then read from there). Draw a
   sequence diagram of the 4-message handshake: IKE_SA_INIT request, IKE_SA_INIT response,
   IKE_AUTH request, IKE_AUTH response.
3. Label on your diagram exactly where encryption starts (hint: IKE_AUTH messages are protected
   using keys derived from the IKE_SA_INIT exchange — find the sentence that states this).
4. Explain in 2-3 sentences the difference between an "IKE SA" and a "Child SA," and why
   separating control-channel negotiation from data-channel (traffic-protecting) SAs is a useful
   design.
5. Explain in 1-2 sentences what an INFORMATIONAL exchange with no payloads is used for (hint:
   search `grep -n "check for liveness" /tmp/rfc7296.txt`), then clean up: `rm /tmp/rfc7296.txt`.

## 6. strongSwan (real-world IPsec deployment/config)

1. Check the installed version and confirm the daemon/CLI split:
   ```fish
   ipsec version
   swanctl --version
   swanctl --version --daemon
   ```
   Note: the daemon call fails with a "No such file or directory" vici-socket error if `charon`
   isn't running as a service — that failure itself demonstrates the client/daemon architecture
   (swanctl is just a thin client; without the daemon running there's nothing to talk to).
2. Read the config schema directly from the installed man page:
   ```fish
   man 5 swanctl.conf
   ```
   bash/sh: identical.
3. From the man page, find and note the purpose of these three top-level sections:
   `connections`, `secrets`, `pools`. Map each one to a concept from RFC 7296 studied in the
   previous link (link 5) — e.g. which section configures what becomes an IKE SA / Child SA.
4. Find the `connections.<conn>.version` setting in the man page and explain what value `0`
   (the default) means for interoperability between IKEv1-only and IKEv2-only peers.
5. Write 2-3 sentences on why `/etc/swanctl/swanctl.conf` being mode 0640 root-owned (verify with
   `ls -la /etc/swanctl/swanctl.conf`) is the correct security posture for a file that can contain
   pre-shared keys, even on a single-user machine.

## 7. WireGuard vs IPsec vs OpenVPN comparison

1. Confirm WireGuard is UDP-only by design (no TCP option exists in its config schema):
   ```fish
   man 8 wg-quick | grep -i -A2 "ListenPort"
   ```
   bash/sh: identical. Note there is no `Protocol = tcp|udp` style option anywhere in the config —
   UDP is not configurable because it's architecturally the only choice.
2. Build a comparison table with columns: Protocol | Approx. codebase size | Cipher agility
   (fixed vs. negotiable) | Typical use case | NAT/roaming behavior — one row each for WireGuard,
   IPsec+IKEv2, OpenVPN. Populate it using facts already gathered in links 2 (WireGuard protocol),
   3 (WireGuard home), 5 (RFC 7296), and 6 (strongSwan) of this section, plus this link's article.
3. Write 3-4 sentences arguing the case FOR choosing IPsec/IKEv2 over WireGuard in a regulated
   enterprise environment (hint: legacy hardware VPN concentrators, FIPS-validated cipher
   requirements, existing PKI investment).
4. Write 3-4 sentences arguing the case FOR choosing WireGuard over IPsec for a homelab/personal
   mesh setup (hint: auditability, roaming across wifi/cellular, config simplicity).
5. Explain in 2 sentences why "which VPN protocol is best" is the wrong framing per this
   comparison — what's the right framing instead?

## 8. VPN internals: protocols, leaks, kill switches

1. Check this machine's current DNS resolver and global IPv6 exposure (baseline, no VPN active):
   ```fish
   cat /etc/resolv.conf
   ip -6 addr show scope global
   ```
   bash/sh: identical. Record what each command shows (this machine currently resolves via the
   local NetworkManager-assigned nameserver and has no global IPv6 address).
2. For each of the 3 leak types (DNS, WebRTC, IPv6), write one sentence on the specific
   misconfiguration or missing step that causes it, distinct for each type.
3. Read (do not apply) the nftables kill-switch pattern sketch in notes.md — explain in 2-3
   sentences what `policy drop` on the `output` chain accomplishes, and why the `oifname "wg0"
   accept` / `oifname "lo" accept` lines are both necessary (what breaks if either is missing?).
4. (Optional, root, read-only) Inspect any currently active firewall rules on this machine:
   `sudo nft list ruleset`. This is read-only and does not modify anything.
5. Write 2-3 sentences on the "timing gap" problem the article raises: why can a kill switch that
   correctly blocks traffic *after* activation still leak a small amount of traffic *during* the
   failure-to-activation window, and what would close that gap (hint: fail-closed default policy
   set up *before* the tunnel ever starts, not reactively after a drop is detected).

## 9. DNS leaks

1. Run the three debug-record queries and record the output of each:
   ```fish
   dig +short TXT o-o.myaddr.l.google.com @8.8.8.8
   dig +short myip.opendns.com @resolver1.opendns.com
   dig +short myip.opendns.com
   ```
   bash/sh: identical. Verified on this machine: the first two return real IP/subnet info, the
   third (unpinned system resolver) returns nothing.
2. Explain in 2-3 sentences why the third query's empty result is expected rather than a bug —
   what does `myip.opendns.com` require to resolve meaningfully (hint: which resolver has to
   actually receive the query)?
3. Explain in 3-4 sentences how a real DNS-leak-testing site (e.g. dnsleaktest.com) generalizes
   this same debug-record technique to detect a live VPN leak: what does the site's page load do
   under the hood, and what would "seeing your ISP's resolver in the results while a VPN is
   active" mean?
4. Look up Windows 8's "Smart Multi-Homed Named Resolution" behavior described in the article and
   explain in 2-3 sentences the specific race condition it creates (multiple interfaces queried
   simultaneously, fastest answer wins) and why that defeats a VPN's DNS protection even when the
   VPN tunnel itself is healthy.
5. List the 4 mitigations the article names (encrypted DNS, VPN-forced DNS routing, manually
   pinned adapter DNS, app-level resolution like Tor Browser) and rank them from
   "most robust / hardest to misconfigure" to "least robust / easiest to accidentally bypass," with
   one sentence justifying the ranking.
