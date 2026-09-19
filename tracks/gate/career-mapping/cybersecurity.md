# Cybersecurity — job roles, skills, GATE overlap, and practice projects

Consolidated from a `web-capture`-based job-listing analysis of Google, Anthropic,
Cloudflare, Snowflake, SAP, and Adobe career pages, cross-referenced against the
GATE 2027 checklist (`../topics/gfg-gate-topic-map.md`) and web-vapt-style
practical project ideas.

---

## 1. Job titles found

**Google**
- Software Engineer, Chrome Networking Security

**Anthropic**
- Anthropic Fellows Program, AI Safety & Security
- Research Engineer, Cybersecurity RL (Reinforcement Learning)
- Applied AI Security Architect
- Applied AI Architect, Cyber
- Strategic Account Executive, Cybersecurity
- Solutions Marketing Manager, Cybersecurity
- Product Manager, Cybersecurity
- Engineering Manager, Cybersecurity Products
- Staff+ Researcher, Cybersecurity Products
- Cyber Evaluations Engineer
- Security Engineer – Threat Intel
- Security Engineer, Corporate Security
- Security Engineer, Detection & Response
- Security Engineer, Offensive Security
- Senior Software Security Engineer
- Staff+ Application Security Engineer (+ M&A variant)
- Staff+ Security Engineer, Risk Engineering
- Staff+ / Staff Software Security Engineer
- Software Security Engineering Manager, Secure Frameworks
- Platform Security Engineer, DRTM / Secure Launch
- Platform Security Engineer, OpenBMC
- Platform Security Engineering, Operating Systems
- Offensive Hardware Security Engineer, Platform Security
- Safeguards Enforcement Analyst / Lead, Cyber Harms
- Safeguards Policy Analyst / Senior Lead, Cyber Harms
- Technical Cyber Threat Investigator
- Technical CBRN-E Threat Investigator

**Cloudflare**
- IAM Security Engineer
- Senior Product Manager, Email Security

**Snowflake**
- Senior Software Engineer - Identity, Data Security and Trust
- Senior Product Manager - Identity & Access Intelligence

**SAP**
- Senior Product Security Engineer (f/m/d)

**Adobe**
- Adversarial Fraud Engineer — Global Consumer Trust

---

## 2. Technical stack, certifications, skills

**Technical stack**
- **Languages:** Python, C/C++, Go, Rust (systems/security tooling), Bash/PowerShell
- **Networking & protocols:** TCP/IP, DNS, TLS/SSL, VPN, Zero Trust architecture
- **SIEM/SOC:** Splunk, Elastic/ELK, Microsoft Sentinel, IBM QRadar; SOAR platforms
- **Vulnerability management:** Nessus/Tenable, Qualys, Rapid7 InsightVM; CVE/NVD/CISA KEV familiarity
- **Endpoint/EDR:** CrowdStrike Falcon, SentinelOne, Microsoft Defender
- **Offensive security:** Nmap, Burp Suite, Metasploit, Cobalt Strike / C2 frameworks
- **Application security:** SAST/DAST (Checkmarx, Veracode, Snyk), OWASP Top 10, secure SDLC
- **Cloud security:** AWS/Azure/GCP native security services (GuardDuty, Security Command Center), CSPM tooling
- **Identity & access:** Okta, Azure AD/Entra ID, SAML/OAuth2/OIDC, LDAP
- **Platform/hardware security:** TPM, Secure Boot, UEFI, firmware security, DRTM, OpenBMC
- **Cryptography:** PKI, key management (HSM/KMS), encryption at rest/in transit
- **Threat intel:** MISP, ThreatConnect, Recorded Future, VirusTotal
- **Frameworks:** MITRE ATT&CK, NIST CSF, ISO 27001, SOC 2

**Certifications**
- CompTIA Security+ / Network+ / CySA+ (foundation, SOC)
- CEH, OSCP (offensive/red team)
- GIAC (GSEC, GCIH, GPEN, GCFA) — SANS
- CISSP, CISM (senior/management track)
- CCSP, cloud-vendor security specialty certs (AWS/Azure/GCP)
- CRISC (risk-focused roles)

**Skills**
- Threat modeling & risk assessment
- Incident response & digital forensics
- Secure coding & code review
- Penetration testing methodology
- Security architecture design
- AI/model security awareness (prompt injection, adversarial robustness, model safeguards) — a distinct niche visible in several Anthropic roles
- Policy/compliance literacy and ability to translate technical risk for non-technical stakeholders (visible in the Safeguards Policy/PM/marketing roles found)

---

## 3. GATE topics that overlap with this track

GATE has **no dedicated Cyber Security section** (flagged as a gap in
`../topics/gfg-gate-topic-map.md`'s own "Not covered" note) — overlap is
foundational, not direct:

- **Computer Networks** (§12) — TCP/IP, DNS, Firewalls, Wi-Fi security (WPA), Encryption reference
- **Discrete Mathematics** (§3) — Number theory/Modular Arithmetic/Groups, the basis for RSA/cryptography
- **Operating Systems** (§10) — process/memory protection, access control concepts
- **Digital Logic & Computer Organization** (§4–5) — hardware/firmware foundations relevant to platform/secure-boot security roles

---

## 4. Practical, code-first project ideas (web-vapt-style)

Each project is meant to be *built from scratch* against the named book — not
a tutorial followed, a chapter implemented in code.

**Computer Networks** — *Kurose & Ross, "Computer Networking: A Top-Down Approach"* + *Tanenbaum & Wetherall, "Computer Networks"*
- Raw-socket packet sniffer: parse Ethernet/IP/TCP headers byte-by-byte off the wire — no scapy
- Minimal SYN scanner using raw sockets (a tiny nmap) — implement the TCP handshake state machine yourself
- DNS resolver from scratch: craft/parse raw DNS query and response packets over UDP — no dnspython
- Userspace packet-filtering firewall (netfilterqueue or raw sockets) enforcing real allow/deny rules — stateful vs. stateless
- WPA2 4-way handshake capture + offline dictionary crack pipeline, coded end-to-end

**Discrete Mathematics (crypto foundations)** — *William Stallings, "Cryptography and Network Security: Principles and Practice"*
- RSA from scratch: your own modular exponentiation + Extended Euclidean Algorithm for keygen, encrypt/decrypt — no crypto library
- Diffie-Hellman from scratch, then demonstrate a MITM attack against your own unauthenticated version
- Classical ciphers (Caesar, Vigenère) + their cryptanalysis via frequency analysis
- Birthday-attack hash-collision simulator

**Operating Systems** — *Silberschatz, Galvin, Gagne, "Operating System Concepts"*
- Deliberately vulnerable C program + your own stack-smashing exploit, then re-run against ASLR/stack canaries to see the mitigation work
- A Role-Based Access Control engine you build, then attack for logic-bug privilege escalation
- A `/proc`-parsing Linux enumeration tool (mini linpeas) — real OS internals, not a wrapper around an existing tool

**Digital Logic & Computer Organization (hardware/platform security)** — *Bhunia & Tehranipoor, "Hardware Security: A Hands-On Learning Approach"* (+ Stallings' COA book for the architecture baseline)
- Secure-boot chain-of-trust simulator: hash-verify each "stage" before continuing, refuse on mismatch
- Timing side-channel demo: naive string-compare password check vs. constant-time compare, measured
- UEFI/BIOS firmware image parser on a real firmware dump

---

*Companies with no usable job data (crawl blocked, or the capture tool's search-box
probe polluted results with a literal "test" query): Amazon, Oracle, IBM,
Microsoft, CrowdStrike, Palo Alto Networks, Fortinet, Zscaler, Okta, SentinelOne,
Tenable, Rapid7, Qualys, Check Point, Nvidia, Mistral, Cohere, Databricks,
ServiceNow, Atlassian, Salesforce, VMware/Broadcom. Extending `job_search`
plugin's `SITE_CONFIGS` (extra_hop_hosts + skip_probe per company) would likely
recover most of these — not done yet.*
