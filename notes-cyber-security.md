# Cyber Security — Notes

This subject has **zero GATE/GFG tutorial coverage** per `exam-priority-report.md` (Tier 1, item 5) — the source list is 4 GitHub reference repos (curated lists / real tool docs / defensive-security index), not step-by-step tutorial pages. Notes below are therefore synthesized from what those repos actually contain, clearly separated from standard security knowledge filled in where the repos themselves don't spell out exam-testable material (e.g. RSA/DH math, classical ciphers, NIST IR phase names).

---

## Cryptography (sobolevn/awesome-cryptography) — Notes

The repo's actual top-level structure is: **THEORY** (Algorithms → Symmetric/Asymmetric/Transform Encryption/Hash Functions, plus Articles/Books/Courses) → **TOOLS** → **FRAMEWORKS AND LIBS** (per-language) → **RESOURCES**. Only the "Algorithms" subsection is exam-relevant; the rest is tool/library listings for practitioners, not exam concepts.

**1. Symmetric Encryption** *(repo category, named algorithms listed)*
One key encrypts and decrypts. Repo lists: **3DES** (Triple DES), **AES** (Rijndael, current standard, block size 128 bits, key sizes 128/192/256), **Blowfish**.

**2. Classical ciphers** *(standard reference, not from repo — repo jumps straight to modern algorithms, but ISRO-level questions often start here)*
- **Caesar cipher**: shift each letter by a fixed `k`: `C = (P + k) mod 26`.
- **Vigenère cipher**: polyalphabetic shift using a repeating keyword.
- **Substitution cipher**: each symbol mapped to another symbol (mono-alphabetic).
- **Transposition cipher**: rearranges symbol order without changing the symbols (e.g. rail-fence).

**3. DES / 3DES** *(standard reference detail on repo-listed term)*
DES: 64-bit block, 56-bit effective key, 16 Feistel rounds — considered broken (small key space, brute-forceable). 3DES applies DES three times (encrypt-decrypt-encrypt with 2 or 3 keys) to extend effective key length.

**4. AES (Advanced Encryption Standard)** *(repo-listed)*
Symmetric block cipher, block size 128 bits, key sizes 128/192/256 bits, operates via SubBytes/ShiftRows/MixColumns/AddRoundKey rounds (10/12/14 rounds respectively). Replaced DES as the US federal standard (Rijndael algorithm).

**5. Asymmetric Encryption** *(repo category, named algorithms: DH, ECC, RSA)*
Uses a public/private key pair — what one key encrypts, only the paired key decrypts. Repo lists **DH (Diffie-Hellman Key Exchange)**, **ECC (Elliptic-Curve Cryptography)**, **RSA (Rivest–Shamir–Adleman)**.

**6. RSA — key generation and use** *(standard reference math filled in behind the repo-listed term; this IS testable)*
```
1. Choose two large primes p, q.
2. n = p * q                      (the modulus, public)
3. φ(n) = (p-1)(q-1)               (Euler's totient)
4. Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1   (public exponent)
5. Compute d = e^(-1) mod φ(n)      (private exponent, modular inverse of e)

Public key  = (e, n)
Private key = (d, n)

Encryption:  C = M^e mod n
Decryption:  M = C^d mod n
```
*Security rests on the difficulty of factoring `n` into `p` and `q` for large numbers.*

**7. Diffie–Hellman (DH) key exchange** *(standard reference math filled in behind the repo-listed term)*
```
Public parameters: prime p, generator g (primitive root mod p)

Alice picks private a  → sends A = g^a mod p
Bob picks private b    → sends B = g^b mod p

Shared secret: s = B^a mod p = A^b mod p = g^(ab) mod p
```
*Security rests on the difficulty of the discrete logarithm problem. Vulnerable to man-in-the-middle without authentication — this is the standard exam "why is DH not enough alone" point.*

**8. ECC (Elliptic-Curve Cryptography)** *(repo-listed)*
Achieves RSA-equivalent security with much smaller key sizes by using the algebraic structure of elliptic curves over finite fields; security based on the elliptic-curve discrete logarithm problem (ECDLP).

**9. Transform Encryption / Proxy Re-Encryption** *(repo-listed, niche category)*
A semi-trusted proxy can transform ciphertext encrypted under Alice's key into ciphertext decryptable by Bob's key, without the proxy ever seeing the plaintext.

**10. Hash Functions** *(repo category, named algorithms listed)*
One-way functions producing a fixed-size digest; repo lists **MD5** (128-bit, broken/collision-prone), **SHA1** (160-bit, broken/deprecated), **SHA2** (SHA-256, SHA-512 — current standard family), **SHA3** (Keccak-based, newest standard).

**11. Hash function properties** *(standard reference, not spelled out in repo but implied by the category)*
Pre-image resistance, second pre-image resistance, collision resistance, avalanche effect (small input change → large output change).

**12. Digital signatures** *(standard reference — not a repo section header, but the standard downstream use of asymmetric crypto + hashing an exam will test)*
Sign: hash the message, encrypt the hash with the sender's private key. Verify: decrypt the signature with the sender's public key and compare to a fresh hash of the message. Provides authentication + integrity + non-repudiation (not confidentiality).

**Priority for your prep**: RSA key-gen formula and DH exchange formula are the two genuinely numeric/testable items here — know them cold. Everything else (AES/DES/hash families/ECC) is definitional: know what each *is* and roughly why it's used, not internal round structure.

---

## Network Security / Firewalls / IDS-IPS (OISF/suricata) — Notes

**1. What Suricata is** *(repo-sourced, README's own description)*
Suricata is described in its own README as "a network IDS, IPS and NSM engine developed by the OISF and the Suricata community" — i.e. a real, open-source **network Intrusion Detection System, Intrusion Prevention System, and Network Security Monitoring engine** in one codebase (C core, Rust components).

**2. IDS vs IPS — the conceptual distinction** *(standard reference; repo confirms Suricata implements both modes but the README fetch didn't spell out the definitional contrast)*
- **IDS (Intrusion Detection System)**: passively monitors traffic (usually via a tap/mirror port), matches against rules/signatures, and **alerts** on suspicious activity. It does not sit inline and cannot itself block traffic.
- **IPS (Intrusion Prevention System)**: sits **inline** in the traffic path; on a rule match it can actively **drop/block** the packet or connection in real time, not just alert.
- Suricata can run in either mode depending on deployment (passive tap = IDS mode; inline = IPS mode) — same rule engine, different placement/action.

**3. Where IDS/IPS fits relative to firewalls** *(standard reference)*
- **Firewall**: enforces access-control rules based on IP/port/protocol (allow/deny) — coarse, header-level filtering, no deep inspection of payload content by default.
- **IDS/IPS**: inspects packet payloads against signatures/anomaly models — catches attacks that pass a firewall's header-level rules (e.g. a SQL injection string arriving on an allowed port 443/80 connection).
- Typical stack ordering: perimeter firewall → IDS/IPS (Suricata-class engine) → host-based defenses (antivirus/EDR) → application-layer controls.

**4. Signature-based detection / rule structure** *(standard reference — the fetched README linked out to a User Guide for rule syntax rather than including it inline)*
Generic Suricata/Snort-style rule shape:
```
action protocol src_ip src_port -> dst_ip dst_port (options)

Example:
alert tcp any any -> any 80 (msg:"Possible attack"; content:"malicious_string"; sid:1000001; rev:1;)
```
- **action**: alert / drop / pass / reject
- **protocol**: tcp, udp, icmp, http, tls, etc.
- **src/dst IP and port**, direction operator (`->` or `<>`)
- **options** in parentheses: `msg` (alert text), `content` (byte/string match), `sid` (rule ID), `rev` (revision) — this is signature-based detection: known attack patterns encoded as content matches.

**5. NSM (Network Security Monitoring)** *(repo-sourced term)*
Broader than alerting — logging metadata/flow records (Suricata produces "eve.json" style logs) for later analysis/threat hunting, not just real-time block/alert decisions.

**Priority for your prep**: the IDS-vs-IPS distinction (passive/alert vs inline/block) and "firewall = header filtering, IDS/IPS = payload/signature inspection" are the two likely one-liner definitional questions. Rule-syntax detail is lower yield — know that rules are signature-based (pattern match against known content), not the exact field order.

---

## OWASP Top 10 (cross-referenced against swisskyrepo/PayloadsAllTheThings) — Notes

The repo's actual top-level directory structure (fetched via the GitHub contents API, since the README itself is a landing page without a full inline TOC) organizes content by **vulnerability class** — confirmed categories include: SQL Injection, Command Injection, NoSQL Injection, LDAP/XPATH/SAML/XSLT/GraphQL Injection, XSS Injection, XXE Injection, SSRF, CSRF, Insecure Direct Object References, CORS Misconfiguration, Insecure Deserialization, JSON Web Token, OAuth Misconfiguration, Race Condition, Business Logic Errors, Directory/Path Traversal, Open Redirect, Dependency Confusion, Mass Assignment, Prototype Pollution, Denial of Service, Clickjacking, CRLF/CSV/LaTeX Injection, Zip Slip, Web Cache Deception, and more (~65 categories total).

Below: each **OWASP Top 10 (2021)** category *(standard reference — this exact A01–A10 list/order is the official OWASP 2021 ranking, not the repo's own structure)*, one-line definition, cross-referenced to the matching repo category as a concrete example type.

**1. A01:2021 — Broken Access Control**
Users can act outside their intended permissions (view/modify others' data, bypass authorization checks).
*Repo example: Insecure Direct Object References, Directory Traversal, CORS Misconfiguration, Open Redirect.*

**2. A02:2021 — Cryptographic Failures**
Sensitive data exposed due to missing/weak encryption, weak algorithms, or poor key management (formerly "Sensitive Data Exposure").
*Repo example: Insecure Randomness, JSON Web Token (weak signing/`alg:none` issues).*

**3. A03:2021 — Injection**
Untrusted input is interpreted as code/commands by an interpreter (SQL, OS command, LDAP, etc.).
*Repo example: SQL Injection, Command Injection, NoSQL Injection, XPATH/LDAP/SAML Injection, XSS Injection.*

**4. A04:2021 — Insecure Design**
Missing or ineffective security controls baked into the design itself, not a specific implementation bug.
*Repo example: Business Logic Errors, Race Condition.*

**5. A05:2021 — Security Misconfiguration**
Insecure default configs, verbose errors, unnecessary features enabled, missing hardening.
*Repo example: CORS Misconfiguration, Reverse Proxy Misconfigurations, OAuth Misconfiguration.*

**6. A06:2021 — Vulnerable and Outdated Components**
Using libraries/frameworks/components with known vulnerabilities or that are unmaintained.
*Repo example: Dependency Confusion, CVE Exploits.*

**7. A07:2021 — Identification and Authentication Failures**
Weaknesses in login, session management, credential handling (formerly "Broken Authentication").
*Repo example: Brute Force / Rate Limit issues, Account Takeover, JSON Web Token forgery.*

**8. A08:2021 — Software and Data Integrity Failures**
Code/infrastructure that doesn't verify integrity — insecure deserialization, unsigned updates, compromised CI/CD.
*Repo example: Insecure Deserialization, Insecure Source Code Management, Prototype Pollution.*

**9. A09:2021 — Security Logging and Monitoring Failures**
Insufficient logging/alerting/monitoring lets breaches go undetected long enough to cause major damage.
*(No direct repo category — this class is inherently defensive/absence-of-control, not an exploitable payload type, so PayloadsAllTheThings has little to map here; standard reference gap.)*

**10. A10:2021 — Server-Side Request Forgery (SSRF)**
Server is tricked into making requests to an unintended destination (internal services, cloud metadata endpoints) using attacker-supplied URLs.
*Repo example: Server Side Request Forgery (dedicated repo category, matches 1:1).*

**Priority for your prep**: know the 10 category names *in order* (A01–A10) and a one-line definition each — that is the classic MCQ format ("which OWASP category does X vulnerability belong to?"). Injection (A03), Broken Access Control (A01), and SSRF (A10) are the ones with the clearest concrete named attack types behind them (SQLi, IDOR, SSRF itself) and are the highest-yield to be able to identify by example.

---

## Incident Response (The-Art-of-Hacking/h4cker — defensive-security) — Notes

**1. Defensive-security domain structure** *(repo-sourced — actual subdirectories in `cybersecurity-domains/defensive-security`)*
The repo organizes this domain into nine subareas: **DFIR** (Digital Forensics and Incident Response), **Threat Hunting**, **Threat Intelligence**, **Dark Web Research**, **Honeypots and Honeynets**, **Linux Hardening**, **macOS Hardening**, **Windows [Security]**, **SBOM** (Software Bill of Materials).

**2. IR lifecycle — as actually stated in the repo's DFIR README** *(repo-sourced: the DFIR subfolder README explicitly lists a seven-step process)*
```
prepare → detect → analyze → contain → eradicate → recover → post-incident handling
```
This is the repo's own phrasing and maps almost exactly onto the standard NIST framework below (NIST just groups contain/eradicate/recover into one combined phase).

**3. NIST IR lifecycle — 4-phase form** *(standard reference, not the repo's own grouping, but the version ISRO-style MCQs are more likely to quote verbatim)*
```
Preparation → Detection & Analysis → Containment, Eradication & Recovery → Post-Incident Activity
```
- **Preparation**: policies, tooling, training, playbooks set up before an incident occurs.
- **Detection & Analysis**: identifying and confirming an incident occurred, scoping impact.
- **Containment, Eradication & Recovery**: isolate affected systems, remove the root cause, restore normal operation.
- **Post-Incident Activity**: lessons-learned review, updating playbooks/controls to prevent recurrence.

**4. DFIR — key sub-concepts** *(repo-sourced, from the dfir subfolder README)*
Incident lifecycle management (creation, tracking, reporting, team assignment, closure documentation); evidence collection and analysis (disk images, memory dumps, mobile backups, live systems) to build timelines and identify indicators of compromise (IOCs); automation/integration with platforms like Active Directory, PagerDuty, Jira.

**5. Named DFIR tool categories** *(repo-sourced — actual tools listed in the dfir README, useful for "which tool does X" definitional questions)*
- **IR case-management platforms**: TheHive, Demisto, FIR, RTIR, SCOT, Cyphon
- **Memory forensics**: Volatility, Rekall, Memoryze
- **Disk/evidence forensics**: The Sleuth Kit, Autopsy, CDQR
- **Log analysis**: Plaso, Timesketch
- **Malware sandboxing**: Cuckoo Sandbox, Hybrid-Analysis
- **Malware ID**: YARA (rule-based malware signatures), VirusTotal

**6. Blue-team adjacent concepts** *(standard reference, implied by the repo's own subdirectory names but not elaborated in the fetched pages)*
- **Threat Hunting**: proactively searching for undetected intrusions rather than waiting for alerts.
- **Threat Intelligence**: structured knowledge about adversary TTPs (tactics, techniques, procedures), IOCs, threat actor attribution.
- **Honeypots/Honeynets**: decoy systems/networks deployed to attract, detect, and study attackers.
- **Hardening** (Linux/macOS/Windows): reducing attack surface via config baselines (disabling unused services, patching, least privilege).
- **SBOM**: an inventory of software components/dependencies used for supply-chain risk visibility (ties back to OWASP A06 — vulnerable/outdated components).

**Priority for your prep**: the four-phase NIST lifecycle (Preparation → Detection & Analysis → Containment/Eradication/Recovery → Post-Incident) is the highest-yield memorizable sequence — it's the standard answer shape for "what are the phases of incident response." The nine defensive-security subdomain names are good for matching-type questions (e.g. "which domain covers X").

---

*Sources actually fetched: all 4 — sobolevn/awesome-cryptography (README, full section structure), OISF/suricata (README self-description), swisskyrepo/PayloadsAllTheThings (GitHub contents API for the category directory list, since the README itself is a landing page without an inline TOC), The-Art-of-Hacking/h4cker defensive-security + dfir subfolder READMEs.*
