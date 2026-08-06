# 0. Prerequisite Foundations — Exercises

## 1. Networking basics (OSI/TCP-IP, routing, NAT, DNS)

1. Run `ip -4 addr show` and identify: your host's link-layer interface name, its internet-layer
   (IP) address, and the subnet mask (CIDR suffix).
2. Run `ip route show` and identify the default gateway — this is the internet-layer device your
   traffic goes through to leave the local link.
3. Run `traceroute -m 5 -w 1 8.8.8.8` (fish and bash/sh: identical syntax) and, for each hop
   shown, write one sentence explaining which layers that intermediate router actually processes
   (hint: routers terminate through the internet layer, not transport/application).
4. Run `dig +short A wikipedia.org` and then `dig +short AAAA wikipedia.org`. Explain in 2-3
   sentences why DNS resolution is considered an application-layer concern even though the actual
   query travels over UDP (transport layer) and IP (internet layer).
5. Draw (text or ASCII diagram is fine) the 4-layer TCP/IP stack next to the 7-layer OSI stack,
   labeling which OSI layers get merged into TCP/IP's single "application" layer.

## 2. Applied cryptography fundamentals (Cryptography Engineering)

1. Run the OpenSSL round-trip:
   ```fish
   openssl enc -aes-256-cbc -pbkdf2 -in /etc/hostname -out /tmp/test.enc -pass pass:demo123
   openssl enc -d -aes-256-cbc -pbkdf2 -in /tmp/test.enc -pass pass:demo123
   rm /tmp/test.enc
   ```
2. Modify one byte of `/tmp/test.enc` before decrypting (e.g. `printf '\x00' | dd of=/tmp/test.enc bs=1 seek=10 count=1 conv=notrunc`) and re-run the decrypt step. Verified result on this machine:
   OpenSSL prints `bad decrypt` / a padding error rather than garbage output. Write 2-3 sentences
   on why this is *not* the same as real integrity protection: it's PKCS7 padding validation
   catching a corrupted final block by luck (CBC chaining propagates the corruption forward),
   not a deliberate authentication tag — tamper a middle byte in a longer multi-block file instead
   and you'd often get garbled-but-padding-valid plaintext with zero error. This unreliable
   padding-based signal is exactly the weakness padding-oracle attacks exploit; a proper MAC/AEAD
   tag would catch tampering 100% of the time, unconditionally.
3. Note: `openssl enc -aes-256-gcm ...` errors with `AEAD ciphers not supported` on this machine's
   OpenSSL — the simple `enc` subcommand doesn't expose AEAD's authentication tag handling, which
   is itself a small illustration of AEAD being more than "just a cipher mode swap." Instead,
   compare against a tool that *does* do authenticated symmetric encryption end-to-end: `gpg`.
   ```fish
   echo "test data for gpg" > /tmp/plain.txt
   gpg --batch --yes --passphrase demo123 -c -o /tmp/test.gpg /tmp/plain.txt
   gpg --batch --yes --passphrase demo123 -d /tmp/test.gpg
   # tamper one byte, then try to decrypt again
   printf '\xff' | dd of=/tmp/test.gpg bs=1 seek=20 count=1 conv=notrunc
   gpg --batch --yes --passphrase demo123 -d /tmp/test.gpg
   rm /tmp/test.gpg /tmp/plain.txt
   ```
   Verified result: tampering reliably produces `gpg: decryption failed: Bad session key` — unlike
   the CBC case in step 2, this failure is deterministic, not padding-position luck.
4. Write a short (5-8 sentence) threat model for "a password manager stores a master-password-
   encrypted vault file on disk" — list at least 3 non-algorithmic failure points the book's
   systems-perspective would flag (e.g. key derivation, memory zeroing, backup copies, clipboard
   exposure) that pure "AES is secure" reasoning would miss.

## 3. Free graduate-level applied crypto book (Boneh & Shoup)

1. Download the book and extract it to text locally (WebFetch renders this PDF unreliably —
   `pdftotext` is the reliable local path, same convention as this repo's man7.org/FHS notes):
   ```fish
   curl -sL -o cryptobook.pdf https://toc.cryptobook.us/book.pdf
   pdftotext cryptobook.pdf cryptobook.txt
   grep -n "Definition of semantic security" cryptobook.txt
   ```
   bash/sh: identical (curl/pdftotext/grep syntax doesn't depend on shell).
2. Open the surrounding text at that line and copy out the formal definition of semantic security
   for a computational cipher. Rewrite it as a plain-English attacker/challenger game (3-5
   sentences) — no jargon, no formulas.
3. Find and read the "one time pad is malleable" subsection (search `grep -n "malleable"
   cryptobook.txt`). Explain in 2-3 sentences why an attacker who can flip bits of a one-time-pad
   ciphertext (without knowing the key) can make predictable changes to the plaintext — and why
   this matters even though the one-time pad has *perfect secrecy*.
4. Read section 2.4 "A fun application: anonymous routing" and write 3-4 sentences connecting it
   to how Tor (studied in section 2 of this set) layers encryption for onion routing.
