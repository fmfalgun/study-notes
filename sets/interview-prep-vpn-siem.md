# Interview Prep — VPN & SIEM

Summary/study document synthesized from `cybersecurity-expert-vpn-tor-siem.md` (operator angle:
SOC analyst / pentester / blue teamer) and `cybersecurity-developer-vpn-tor-siem.md` (builder
angle: protocol/detection engineering). Both angles covered below since interviewers for
security-adjacent roles routinely probe both "how would you use this" and "how does this actually
work under the hood." Tor is intentionally out of scope here — see the two source files if needed.

---

## 1. VPN

### 1.1 What it actually is, and the question interviewers are really asking

A VPN creates an encrypted tunnel between endpoints so traffic crossing an untrusted network
(public wifi, ISP, transit network) is confidential and (usually) authenticated. The interview
question underneath "explain VPN" is almost always **"what's your threat model, and does a VPN
actually address it?"** — a VPN protects traffic *in transit* to the VPN endpoint; it does nothing
about what the destination server logs, does nothing about endpoint compromise, and (depending on
protocol/config) can leak identifying data anyway. Be ready to say what a VPN does *not* solve.

### 1.2 The three protocols you must be able to compare cold

| | **WireGuard** | **IPsec/IKEv2** | **OpenVPN** |
|---|---|---|---|
| Crypto design | Fixed, modern suite (Curve25519, ChaCha20, Poly1305, BLAKE2s) via the **Noise Protocol Framework** handshake | Negotiated suite (flexible but larger attack surface); IKEv2 for key exchange, ESP for the data plane | TLS-based (OpenSSL), negotiated ciphersuite |
| Codebase / attack surface | ~4,000 lines, kernel-level (Linux) or userspace | Large, decades of accumulated complexity (IKEv1 legacy baggage still around) | Large, userspace, TLS stack dependency |
| Formal verification | Yes — mechanized proof of the handshake exists (Tamarin/ProVerif-class work) | Partial, protocol has known historical weaknesses (IKEv1 aggressive mode) | Inherits TLS's verification history |
| Performance | Fastest — minimal handshake, no negotiation | Fast, kernel-accelerated on most platforms | Slowest — userspace + TLS overhead |
| NAT traversal / roaming | Excellent — connectionless, roams across IP changes silently | Good | Good |
| Where you'll meet it | Modern deployments, mesh VPNs, cloud-native | Enterprise/site-to-site, mobile carriers, strongSwan | Legacy enterprise, still very common in the wild |

**Talking point that signals depth**: WireGuard's simplicity is the security feature — no
ciphersuite negotiation means no downgrade attacks, and the small codebase is auditable in a way
IPsec's never realistically will be. If asked "which would you deploy," the correct answer is
"depends on the fleet" — WireGuard if you control both ends and can standardize, IPsec if you need
to interoperate with existing enterprise/carrier infrastructure.

### 1.3 Operational failure modes (the analyst angle)

- **DNS leaks**: DNS queries escape the tunnel and go to the local/ISP resolver instead of through
  the VPN, revealing browsing activity even though the payload traffic is encrypted. Root cause is
  usually OS-level resolver misconfiguration, not the VPN protocol itself.
- **Kill switches**: block all traffic if the tunnel drops, specifically to prevent silent fallback
  to the raw (unencrypted, unmasked) connection. Ask "what happens on tunnel failure" for any VPN
  product being evaluated — no kill switch = the VPN's guarantee is conditional, not absolute.
- **Split tunneling**: deliberately routing only some traffic through the tunnel. A legitimate
  feature, but also a common misconfiguration that silently defeats the "everything's encrypted"
  assumption — worth naming as a detection blind spot from the SIEM side (see §3).
- **Traffic fingerprinting**: even encrypted OpenVPN traffic has identifiable packet-size/timing
  signatures that let a passive observer (e.g. a censoring ISP/state actor) detect *that* a VPN is
  in use, without breaking the encryption. Relevant if asked about censorship-circumvention
  contexts specifically.

### 1.4 Real vulnerability classes (know one concrete example of each)

- **Protocol/implementation flaws**: e.g. IKEv1 aggressive-mode authentication-bypass exploited in
  the wild against enterprise VPN gateways — the lesson isn't the specific CVE, it's that
  **perimeter VPN devices are a top real-world exploitation target** because they sit exposed on
  the internet with privileged network access behind them.
- **Client-side vulnerabilities**: bugs in the client application (not the protocol) — parsing
  bugs, privilege escalation via the VPN client's local helper process, config-injection. Distinct
  category from protocol weaknesses; interviewers sometimes test whether you conflate the two.
- **Traffic correlation** (more Tor-adjacent but relevant to VPN-over-Tor chains): an adversary who
  can observe both ends of a tunnel can correlate timing/volume even without breaking encryption.

### 1.5 Developer/builder-angle essentials

- **Noise Protocol Framework**: the handshake pattern language WireGuard's handshake is built from
  — know that it's a *framework* for composing Diffie-Hellman-based handshakes with different
  security properties (mutual auth, identity hiding, etc.), not a single fixed protocol.
- **Formal verification tooling**: Tamarin Prover is the name to know — used to mechanically verify
  protocol security properties for WireGuard-class handshakes and TLS 1.3. If the role is
  protocol-engineering-adjacent, expect a question testing whether you understand *why* formal
  verification matters more for a from-scratch handshake than for a well-trodden one.
- **Fuzzing**: AFL++ is the standard answer for "how would you test a protocol parser for
  robustness" — parsers (not the crypto math) are where most real-world protocol implementation
  bugs actually live.

---

## 2. SIEM

### 2.1 The one-sentence framing to lead with

A SIEM centralizes logs/telemetry from across an environment, correlates them against known
attack patterns, and surfaces alerts — the entire discipline exists because no single log source
tells the full story of an incident, and manual cross-referencing doesn't scale.

### 2.2 MITRE ATT&CK — the framework every other answer should reference back to

ATT&CK is a matrix of adversary **tactics** (the "why" — e.g. Defense Evasion, Persistence,
Exfiltration) each broken into concrete **techniques** (the "how" — e.g. T1055 Process Injection).
It's the shared vocabulary the whole field uses to talk about detections, so:
- Detection engineering = "which ATT&CK techniques do we have coverage for, and which are gaps."
- **Defense Evasion (TA0005)** is worth knowing by name specifically — it's the tactic category for
  techniques attackers use to blind or bypass the very logging/SIEM pipeline you're building, which
  makes it the tactic most directly relevant to a SIEM-focused interview (log tampering, disabling
  security tools, clearing event logs).

### 2.3 Detection engineering workflow (this is what "hands-on SIEM experience" actually means)

1. Pick an ATT&CK technique you lack coverage for.
2. Write a **Sigma rule** — a YAML-based, SIEM-agnostic detection-rule format (translates to
   Splunk SPL, Elastic queries, etc.) — this portability is *why* Sigma matters as an answer versus
   just saying "I wrote a Splunk query."
3. Validate the detection actually fires using **Atomic Red Team** (small, individually-executable
   attack simulations mapped 1:1 to ATT&CK techniques) or a purpose-built instrumented environment
   like **Splunk Attack Range**.
4. This loop — write detection → simulate attack → confirm/tune → repeat — is what
   **"detection-as-code"** means: treating detections as version-controlled, tested artifacts
   instead of one-off queries someone wrote during an incident and never revisited.

### 2.4 Log normalization (the unglamorous thing that actually determines whether a SIEM works)

Different sources emit wildly different log formats (Windows Event Log vs. syslog vs. cloud audit
logs vs. firewall logs). **Elastic Common Schema (ECS)** — or equivalent normalized schemas — maps
these into consistent field names so a single detection rule works across sources instead of being
rewritten per log format. Interviewers ask about this because it's the difference between a SIEM
that scales and one that becomes an unmaintainable pile of source-specific rules.

### 2.5 Concrete threat scenario to have ready: log/database tampering

An attacker who gains admin access modifies or deletes log entries (e.g. AD database tampering) to
erase evidence of the intrusion — this is the practical, "why does log integrity matter" answer:
detection coverage is worthless if the attacker can retroactively edit what the SIEM already
ingested. Mitigations to be able to name: write-once/immutable log storage, forwarding logs to a
separate trust boundary in near-real-time (so tampering the source doesn't erase the copy already
shipped), and alerting on the log-clearing/tampering events themselves (a Defense Evasion
technique, tying back to §2.2).

### 2.6 Tooling fluency checklist

- **Splunk**: SPL query language, free training path exists, has a full developer platform (SDKs +
  REST API) if the role leans build-vs-operate.
- **Elastic**: detection-rules repo as the open-source analogue of Splunk's content, ECS as its
  normalization layer.
- **Practice platforms** to be able to say you've used: TryHackMe SOC Level 1 path, Blue Team Labs
  Online, CyberDefenders — these are what "hands-on SOC experience" concretely means if you don't
  have production experience yet.

---

## 3. Where VPN and SIEM intersect (good cross-cutting talking point)

- VPN gateway logs (auth attempts, session start/end, source IPs) are a standard SIEM data source
  — and, per §1.4, VPN gateways are a top real-world exploitation target, which makes "do we have
  detection coverage on our own VPN infrastructure" a legitimately good answer to "tell me about a
  gap you'd prioritize."
- Split-tunnel VPN configs (§1.3) create a detection blind spot: traffic that should be visible to
  the SIEM (because it's "supposed" to be tunneled through monitored infrastructure) silently isn't.
  Worth naming if asked to describe a subtle monitoring gap.
- IKEv1/IKEv2 exploitation attempts against perimeter VPN devices are exactly the kind of external
  attack a properly tuned SIEM + ATT&CK-mapped detection set should catch before privilege
  escalation — a concrete example connecting both halves of this document if asked to walk through
  an end-to-end incident.

---

## 4. Fast self-check before the interview

Be able to answer each of these out loud, unscripted, in under 30 seconds:
1. WireGuard vs. IPsec — pick one for a given scenario and justify it.
2. What does a VPN *not* protect against?
3. What's the difference between a Sigma rule and a Splunk-specific search?
4. Name one ATT&CK Defense Evasion technique and how a SIEM would catch it.
5. Why does log normalization (ECS) matter more than any single detection rule?
6. Describe one real VPN vulnerability class with a concrete example (not just "VPNs can be
   hacked").
