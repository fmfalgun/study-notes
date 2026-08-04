# VPN, Tor & SIEM — Mastery List for a Cybersecurity Developer (Builder / Integrator)

Audience: complete beginner → mastery, from the perspective of someone who **builds/develops/integrates** VPN protocols, Tor-related tooling, and SIEM systems. List only — no explanations.

## 0. Prerequisite Foundations

- Cryptography Engineering (design principles book) — https://www.schneier.com/books/cryptography-engineering/
- A Graduate Course in Applied Cryptography (free) — https://toc.cryptobook.us/book.pdf
- OWASP Secure Coding Practices — Quick Reference — https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- Noise Protocol Framework (handshake design used by WireGuard) — https://en.wikipedia.org/wiki/Noise_Protocol_Framework

## 1. VPN Protocol Development

- WireGuard protocol & cryptography spec — https://www.wireguard.com/protocol/
- WireGuard official whitepaper (PDF) — https://www.wireguard.com/papers/wireguard.pdf
- WireGuard project/source — https://www.wireguard.com/
- Mechanised cryptographic proof of the WireGuard handshake — https://bblanche.gitlabpages.inria.fr/publications/LippBlanchetBhargavanEuroSP19.pdf
- strongSwan (production IPsec/IKEv2 implementation, source) — https://github.com/strongswan/strongswan
- strongSwan project docs — https://strongswan.org/
- IKEv2 protocol spec (RFC 7296) — https://www.rfc-editor.org/rfc/rfc7296
- OpenVPN community resources — https://blog.openvpn.net/wireguard-mesh-vpn-guide
- WireGuard vs IPsec vs OpenVPN architecture comparison — https://www.zenarmor.com/docs/network-security-tutorials/ipsec-vs-wireguard

## 2. Tor Development (relays, onion services, client libraries)

- Tor specifications index — https://spec.torproject.org/intro/index.html
- torspec source repository (tor-spec.txt = core protocol spec) — https://github.com/torproject/torspec
- Onion services rendezvous protocol overview — https://spec.torproject.org/rend-spec/protocol-overview.html
- Onion services developer overview — https://community.torproject.org/onion-services/overview/
- Setting up/automating onion services — https://community.torproject.org/onion-services/setup/
- Stem — Python controller library for Tor (docs) — https://stem.torproject.org/
- Stem Controller API reference — https://stem.torproject.org/api/control.html
- Tor Project GitLab (contribute to core code) — https://gitlab.torproject.org/

## 3. SIEM / Detection-Engineering Development

- Sigma — SIEM-agnostic detection-rule spec & repo — https://github.com/SigmaHQ/sigma
- Mastering Sigma rule-writing (deep dive) — https://www.akshayjain.blog/post/mastering-sigma-rules
- Elastic detection-rules repo (build/test/release pipeline) — https://github.com/elastic/detection-rules
- Splunk Developer Platform (SDKs, REST API) — https://dev.splunk.com/
- Detection-as-Code methodology — https://www.splunk.com/en_us/blog/learn/detection-as-code.html
- Splunk Attack Range (build instrumented environments, feed data into SIEM) — https://github.com/splunk/attack_range
- MITRE ATT&CK as a data model for SIEM use-case development — https://medium.com/@imanvanpersien/mitre-att-ck-framework-as-a-standard-for-developing-siem-use-cases-d7dc7db4e1ba
- Atomic Red Team (generate telemetry to build/test detections against) — https://github.com/redcanaryco/atomic-red-team

## 4. Offensive Concepts Developers Must Be Aware Of

- Client-side vulnerabilities in commercial VPNs (research) — https://arxiv.org/pdf/1912.04669
- OpenVPN traffic fingerprinting (protocol-identification attack) — https://arxiv.org/pdf/2403.03998
- Real-world critical IKEv1 auth-bypass exploitation (design flaw class) — https://thehackernews.com/2026/06/critical-check-point-vpn-flaw-exploited.html
- Flow correlation / traffic-analysis attacks on Tor onion services — https://www.ndss-symposium.org/wp-content/uploads/2024-337-paper.pdf
- Deep-learning flow correlation attack (DeepCorr) — https://arxiv.org/pdf/1808.07285
- AS-level / infrastructure adversaries against Tor — https://arxiv.org/pdf/1505.05173
- MITRE ATT&CK — Defense Evasion tactic (what your SIEM/log pipeline must survive) — https://attack.mitre.org/tactics/TA0005/
- Log/database tampering attack pattern (design tamper-resistant pipelines against this) — https://www.manageengine.com/log-management/siem-use-cases/threats/active-directory-database-tampering.html

## 5. Secure Design / Mitigation Topics for Developers

- Formal protocol verification with Tamarin Prover (used to verify WireGuard, TLS 1.3) — https://tamarin-prover.github.io/
- Specifying secure protocol implementations via model generation — https://arxiv.org/pdf/2606.19937
- Elastic Common Schema (normalize logs to resist parsing/evasion gaps) — https://www.elastic.co/guide/en/ecs/current/index.html
- Fuzzing implementations for protocol/parser robustness (AFL++) — https://github.com/AFLplusplus/AFLplusplus
- Detection-as-Code CI/CD validation workflow — https://www.splunk.com/en_us/blog/security/ci-cd-detection-engineering-splunk-security-content-part-1.html
