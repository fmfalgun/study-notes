# 1. VPN Protocol Development — Exercises

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 1.

## 1. WireGuard protocol spec — inspect the tooling and key format locally

1. Check whether `wireguard-tools` is already installed (verified present on this machine):
   ```fish
   which wg wg-quick
   ```
   ```
   # bash/sh:
   which wg wg-quick
   ```
2. Generate a throwaway keypair in the scratchpad only (never in the repo, never used for a real
   tunnel) to inspect WireGuard's key encoding, then delete it immediately:
   ```fish
   wg genkey | tee (mktemp -t wg-priv.XXXX) | wg pubkey
   ```
   ```
   # bash/sh:
   wg genkey | tee /tmp/wg-priv.txt | wg pubkey
   ```
   Note the format: both keys are 32 bytes, base64-encoded (44 chars incl. padding `=`) — this is
   the `encrypted static key` field described in the handshake message layout.
3. Clean up the throwaway private key file immediately (it must never be committed or left around):
   ```fish
   rm -f /tmp/wg-priv*
   ```
4. Write down, from the notes, the 3 packet types (init/response/data) and one field each type has
   that the others don't — this is the same drill as reading a binary protocol spec before writing
   a parser for it.
5. (Optional, no install needed) Read `man 8 wg` if installed, to compare the CLI surface against
   the protocol spec's terminology (`AllowedIPs`, `Endpoint`, `PersistentKeepalive`):
   ```fish
   man 8 wg
   ```

## 2. WireGuard whitepaper — reconstruct a cryptokey routing table

1. Download the whitepaper PDF and confirm `pdftotext` extracts it cleanly (WebFetch alone
   struggles with this PDF's layout for tables — verify locally instead):
   ```fish
   curl -sL -o (mktemp -t wireguard.XXXX.pdf) https://www.wireguard.com/papers/wireguard.pdf
   ```
   ```
   # bash/sh:
   curl -sL -o /tmp/wireguard.pdf https://www.wireguard.com/papers/wireguard.pdf
   ```
2. Extract Section 2 (Cryptokey Routing) specifically:
   ```fish
   pdftotext -layout /tmp/wireguard.pdf - | sed -n '/^2     Cryptokey Routing/,/^2.1    Endpoints/p'
   ```
3. By hand (paper/text editor), draw a 2-column cryptokey routing table for a scenario: your
   laptop (peer A) routes ALL traffic (`0.0.0.0/0`) through a home-server peer (peer B); peer B
   only allows peer A's tunnel IP (`10.10.10.2/32`) as its `AllowedIPs`. Write both peers' table
   rows exactly like the paper's Configuration 1a/2a examples.
4. Confirm the same concept is in the real `wg-quick` man page (not just the paper):
   ```fish
   man 8 wg-quick | grep -A5 "AllowedIPs"
   ```
5. Clean up:
   ```fish
   rm -f /tmp/wireguard*.pdf
   ```

## 3. WireGuard project/source — survey the repo family and inspect one

1. List every repository the project links to (confirms the "cross-platform, many repos" claim
   instead of assuming a single source tree):
   ```fish
   curl -sL https://www.wireguard.com/repositories/ | grep -oE 'href="[^"]*"' | grep -i git
   ```
   ```
   # bash/sh:
   curl -sL https://www.wireguard.com/repositories/ | grep -oE 'href="[^"]*"' | grep -i git
   ```
2. Shallow-clone the small userspace-tools repo to scratch (verified ~instant, read-only):
   ```fish
   git clone --depth 1 https://git.zx2c4.com/wireguard-tools /tmp/wg-tools-src
   ```
   ```
   # bash/sh:
   git clone --depth 1 https://git.zx2c4.com/wireguard-tools /tmp/wg-tools-src
   ```
3. List its `src/` directory and identify which files correspond to notes-file concepts already
   covered: `curve25519.c` (DH), `genkey.c` (the `wg genkey` command used in exercise 1), `config.c`
   (parses the `AllowedIPs`/cryptokey-routing table from exercise 2):
   ```fish
   ls /tmp/wg-tools-src/src
   ```
4. Note the `fuzz/` directory's existence for later cross-reference with section 5 (AFL++
   fuzzing link) — don't run it, just confirm it exists as evidence WireGuard's own maintainers
   fuzz their parser:
   ```fish
   ls /tmp/wg-tools-src/src/fuzz
   ```
5. Clean up the clone (must not be committed to this repo):
   ```fish
   rm -rf /tmp/wg-tools-src
   ```

## 4. Mechanised proof paper — compare symbolic vs computational verification claims

1. Download the paper PDF and confirm `pdftotext -layout` preserves the protocol-diagram text
   better than a web-fetch summary would:
   ```fish
   set proof_pdf (mktemp -t wg-proof.XXXX.pdf)
   curl -sL -o $proof_pdf https://bblanche.gitlabpages.inria.fr/publications/LippBlanchetBhargavanEuroSP19.pdf
   ```
   ```
   # bash/sh:
   proof_pdf=/tmp/wg-proof.pdf
   curl -sL -o "$proof_pdf" https://bblanche.gitlabpages.inria.fr/publications/LippBlanchetBhargavanEuroSP19.pdf
   ```
2. **Environment note, verified on this machine**: `grep` under fish resolves to a `ugrep` alias
   whose default regex dialect treats bare `|` as alternation (GNU grep's BRE default needs `\|`
   instead) — always use `grep -E` with an unescaped `|` so the pattern is portable across both:
   ```fish
   pdftotext -layout $proof_pdf - | grep -E -n "identity hiding requires|Curve25519" | head -10
   ```
   ```
   # bash/sh:
   pdftotext -layout "$proof_pdf" - | grep -E -n "identity hiding requires|Curve25519" | head -10
   ```
3. Read the two lines the search surfaces around "identity hiding requires a stronger assumption"
   (paper page 2, right column) and write one sentence explaining what that means for a builder:
   if you swap WireGuard's AEAD cipher for a different one, which security property is most at
   risk of silently breaking even if confidentiality still holds?
4. Write a short (3-5 sentence) comparison of symbolic (Tamarin, see section 5) vs computational
   (CryptoVerif, this paper) verification: what can a computational proof rule out that a symbolic
   one cannot?
5. Clean up:
   ```fish
   rm -f $proof_pdf
   ```
   ```
   # bash/sh:
   rm -f "$proof_pdf"
   ```

## 5. strongSwan source — count and categorize the plugin architecture

1. Shallow-clone the repo (verified: completes in well under a minute):
   ```fish
   git clone --depth 1 https://github.com/strongswan/strongswan /tmp/strongswan-src
   ```
   ```
   # bash/sh:
   git clone --depth 1 https://github.com/strongswan/strongswan /tmp/strongswan-src
   ```
2. Count the plugins and list the top-level `src/` daemons/tools (verified: 65 plugins on this
   clone; the exact count may drift slightly as the project evolves — re-run to confirm current):
   ```fish
   ls /tmp/strongswan-src/src/libcharon/plugins | wc -l
   ls /tmp/strongswan-src/src
   ```
3. Group the plugin names by rough category just from their names (EAP variants, kernel backends,
   credential/cert handling, operational/monitoring) — this is the same "read the source layout
   before the source itself" skill used for the WireGuard-tools clone in exercise 3.
4. Compare directory-count-as-complexity-proxy against WireGuard: WireGuard's entire `wg-tools`
   `src/` (from exercise 3) has roughly a dozen files total; strongSwan's plugin directory alone has
   65. Write one sentence on what real-world requirement (protocol version support, enterprise
   auth backends, hardware token integration) justifies that gap.
5. Clean up (must not be committed):
   ```fish
   rm -rf /tmp/strongswan-src
   ```

## 6. strongSwan project docs — trace one feature (MOBIKE) into the actual RFC

1. From the strongswan.org feature list, pick MOBIKE (IKEv2 Mobility and Multihoming) — the
   feature that lets a mobile client keep its VPN tunnel alive across a network change.
2. Confirm it's a real RFC-level concept, not just a strongSwan marketing term, by grepping the
   actual RFC 7296 text (verified working; note the `-E` + unescaped `|` per the environment note
   from exercise 4 above):
   ```fish
   curl -sL https://www.rfc-editor.org/rfc/rfc7296 | grep -E -i -n "mobike|mobility" | head -10
   ```
   ```
   # bash/sh:
   curl -sL https://www.rfc-editor.org/rfc/rfc7296 | grep -E -i -n "mobike|mobility" | head -10
   ```
3. Note that RFC 7296 references MOBIKE as a *separate* RFC (RFC 4555) rather than defining it
   inline — write down that distinction (core IKEv2 spec vs. an extension RFC) since it matters for
   correctly scoping "what IKEv2 requires" vs "what a specific deployment adds."
4. Compare conceptually to WireGuard's roaming mechanism (from the whitepaper notes above): WireGuard
   achieves similar behavior "for free" from cryptokey routing + endpoint auto-update, with no
   separate protocol extension needed. Write 2-3 sentences on the architectural reason IPsec needed
   a dedicated extension RFC for this while WireGuard didn't.

## 7. RFC 7296 (IKEv2) — fetch the clean plain-text spec and map the 4 exchange types

1. Fetch the plain-text version specifically — verified cleaner than the JS-heavy HTML render at
   `rfc-editor.org/rfc/rfc7296`:
   ```fish
   curl -sL https://www.rfc-editor.org/rfc/rfc7296.txt -o (mktemp -t rfc7296.XXXX.txt)
   ```
   ```
   # bash/sh:
   curl -sL https://www.rfc-editor.org/rfc/rfc7296.txt -o /tmp/rfc7296.txt
   ```
2. Locate all four exchange types and their table-of-contents entries:
   ```fish
   grep -n "IKE_SA_INIT|IKE_AUTH|CREATE_CHILD_SA|INFORMATIONAL" -E /tmp/rfc7296.txt | head -10
   ```
   ```
   # bash/sh:
   grep -nE "IKE_SA_INIT|IKE_AUTH|CREATE_CHILD_SA|INFORMATIONAL" /tmp/rfc7296.txt | head -10
   ```
3. Read Section 1 body text (around line ~295-335 in the October 2014 revision) describing the
   ordering constraint: `IKE_SA_INIT` and `IKE_AUTH` MUST complete before any `CREATE_CHILD_SA` or
   `INFORMATIONAL` exchange. Draw a 4-message sequence diagram by hand for the common case (1
   `IKE_SA_INIT` request/response + 1 `IKE_AUTH` request/response = tunnel established).
4. Count total messages for that common case (4) and compare to WireGuard's handshake (2, from
   link 1's notes) — write one sentence on what extra round trip IKEv2 spends and why (negotiation
   of algorithm suites happens in `IKE_SA_INIT` before authentication can even start).
5. Clean up:
   ```fish
   rm -f /tmp/rfc7296.txt
   ```

## 8. OpenVPN blog (WireGuard mesh guide) — design a minimal control plane on paper

1. Without code, write a short design note answering: for a 4-peer WireGuard mesh (all peers talk
   directly to each other), what are the minimum three responsibilities a control plane needs to
   handle? (keypair generation/distribution; propagating each peer's current public key + endpoint
   to all others; handling peer revocation/removal.)
2. Confirm how manual/brittle the *data plane only* config format is without such a control plane —
   read the real config section of the man page:
   ```fish
   man 8 wg-quick | grep -B2 -A8 "^CONFIGURATION"
   ```
   ```
   # bash/sh:
   man 8 wg-quick | grep -B2 -A8 "^CONFIGURATION"
   ```
3. Sketch (in prose, one paragraph) what breaks at 4 peers vs. at 40 peers if key/endpoint
   distribution is done by hand-editing each peer's config file — this is the concrete case for why
   "mesh" WireGuard deployments in practice always pair it with an external coordinator (e.g.
   Headscale/Tailscale-style control planes), even though WireGuard itself has no opinion on this.
4. Cross-reference against Cryptokey Routing (link 2's notes above): note explicitly that
   `AllowedIPs` propagation *is* the control-plane problem in miniature — every peer's routing
   table entry for every other peer has to be correct and current, which is exactly what a control
   plane automates away.

## 9. WireGuard vs IPsec vs OpenVPN — build a locally-grounded comparison table

1. Without re-reading the zenarmor article, build a table from memory of what this section's own
   exercises already verified:

   | Dimension | WireGuard | IPsec/strongSwan |
   |---|---|---|
   | Handshake messages | ? | ? |
   | Ciphersuite negotiation | ? | ? |
   | Reference impl size (LOC / plugin count) | ? | ? |
   | Native mobile OS support | ? | ? |
   | Roaming mechanism | ? | ? |

2. Fill in each cell using ONLY facts already verified earlier in this file's notes (link 1: 2
   handshake messages; link 2: fixed, non-negotiated primitives, <4000 LOC; link 5: 65 strongSwan
   plugins; link 6: OS-native IPsec support vs WireGuard needing an app; link 1 whitepaper: cryptokey
   routing/endpoint rediscovery vs link 6: MOBIKE extension RFC).
3. Compare your filled table against the zenarmor article's own claims (20% lower latency, 15%
   higher throughput for WireGuard) — note that these are the *only* cells in the table that require
   trusting a third-party benchmark rather than something independently verified in this file's
   earlier exercises; flag that distinction explicitly.
4. Write one sentence recommending WireGuard vs IPsec for two different scenarios: (a) a
   performance-sensitive point-to-point link between two servers you control, (b) a scenario
   requiring native VPN support on unmanaged/BYOD mobile devices without installing a third-party
   app.
