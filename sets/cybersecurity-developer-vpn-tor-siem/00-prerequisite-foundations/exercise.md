# 0. Prerequisite Foundations — Exercises

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 0.

## 1. Cryptography Engineering — threat-model exercise

1. Pick a concrete component: "a VPN client daemon that stores its WireGuard private key at
   `/etc/wireguard/private.key`".
2. Write down, in your own words: (a) who the realistic adversaries are (local unprivileged user,
   malware with user-level access, someone who steals the laptop, a malicious update), (b) what
   each adversary can actually do to the key file given typical Unix permissions, (c) the blast
   radius if the key leaks (can traffic be decrypted retroactively? can the attacker impersonate
   the client going forward?).
3. Verify your assumption about default permissions on this machine:
   ```fish
   umask
   ```
   ```
   # bash/sh:
   umask
   ```
4. Propose one concrete mitigation per adversary (e.g. `0600` permissions + dedicated non-root
   service user; disk encryption for the "stolen laptop" case; signed updates for the "malicious
   update" case) and note which of those WireGuard/strongSwan actually implement by default —
   revisit this once section 1's links are done.

## 2. A Graduate Course in Applied Cryptography — locate & read Chapter 21 (AKE)

1. Download the book PDF (large — ~9 MB; do this once and keep the copy in scratch, not the repo):
   ```fish
   curl -sL -o (mktemp -t cryptobook.XXXX.pdf) https://toc.cryptobook.us/book.pdf
   ```
   ```
   # bash/sh:
   curl -sL -o /tmp/cryptobook.pdf https://toc.cryptobook.us/book.pdf
   ```
2. Extract just the table of contents (first ~20 pages) instead of the whole book, and confirm
   `pdftotext` is available:
   ```fish
   which pdftotext
   pdftotext -f 1 -l 20 /tmp/cryptobook.pdf - | grep -n "Authenticated Key Exchange"
   ```
   (install if missing — Arch: `sudo pacman -S poppler`; Debian: `sudo apt install poppler-utils`)
3. Read the Chapter 21 section list (Identification and AKE; one-sided AKE; AKE with preshared
   keys; password-AKE) and write one sentence per subsection naming which VPN/Tor protocol from
   this file's later sections matches it (e.g. "AKE with preshared keys" → IKEv2 PSK auth mode from
   section 1; "one-sided AKE" → TLS's server-only-authenticated handshake pattern, contrast with
   WireGuard's mutual Noise_IK).
4. Extract and read the actual Chapter 21 pages (857 onward) for the Diffie-Hellman-based AKE
   construction:
   ```fish
   pdftotext -f 857 -l 880 /tmp/cryptobook.pdf - | less
   ```
5. Clean up the scratch copy when done (it is not part of the repo and should not be committed):
   ```fish
   rm -f /tmp/cryptobook*.pdf
   ```

## 3. OWASP Secure Coding Practices — checklist walkthrough

1. Download the actual checklist PDF (the HTML landing page doesn't render the checklist body):
   ```fish
   curl -sL -o (mktemp -t owasp-scp.XXXX.pdf) "https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/assets/docs/OWASP_SCP_Quick_Reference_Guide_v21.pdf"
   ```
   ```
   # bash/sh:
   curl -sL -o /tmp/owasp-scp.pdf "https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/assets/docs/OWASP_SCP_Quick_Reference_Guide_v21.pdf"
   ```
2. Confirm all 14 checklist category headings are present and note their line numbers:
   ```fish
   pdftotext -layout /tmp/owasp-scp.pdf - | grep -n "^[A-Z][a-zA-Z ]*:$"
   ```
3. Extract just the two categories most relevant to VPN/Tor/SIEM development:
   ```fish
   pdftotext -layout /tmp/owasp-scp.pdf - | sed -n '/^Cryptographic Practices:/,/^Error Handling and Logging:/p'
   ```
4. For each of the ~10 cryptographic-practices checklist items, mark which ones a VPN protocol
   implementation (section 1) already satisfies "for free" by using a vetted library (e.g.
   libsodium/noise-c) vs. which ones are still the *implementer's* responsibility (e.g. key storage
   permissions, key rotation policy) — this distinction is exactly the boundary explored in the
   Cryptography Engineering exercise above.
5. Clean up:
   ```fish
   rm -f /tmp/owasp-scp*.pdf
   ```

## 4. Noise Protocol Framework — decode a handshake name by hand

1. Without re-reading the Wikipedia page, write down from memory what each letter means in a Noise
   pattern name: `N`, `K`, `X`, `I` (first letter = initiator's static-key status, second letter =
   responder's static-key status).
2. Decode `Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s` (WireGuard's handshake) piece by piece:
   - `IK` → what does the initiator send and when? What does the responder already know?
   - `psk2` → what extra ingredient gets mixed in, and at which message?
   - `25519` / `ChaChaPoly` / `BLAKE2s` → name the three primitive categories (DH, AEAD cipher,
     hash) each token belongs to.
3. Compare against a hypothetical `Noise_XX_25519_ChaChaPoly_BLAKE2s`: which pattern needs more
   round trips, and which one leaks a static public key to a passive network observer sooner?
4. Cross-check your answers against the actual Noise Protocol spec's pattern table when you reach
   it (revisit this file's answer once section 1, link 1 — the WireGuard protocol page — is done)
   and correct anything that was wrong.

