# VPN, Tor & SIEM — Mastery List for a Cybersecurity Expert (Analyst / Pentester / Blue Teamer)

Audience: complete beginner → mastery, from the perspective of someone who **uses** VPN/Tor and SIEM operationally (SOC analyst, pentester, threat hunter, incident responder). List only — no explanations.

## 0. Prerequisite Foundations

- Networking basics (OSI/TCP-IP, routing, NAT, DNS) — https://en.wikipedia.org/wiki/Internet_protocol_suite
- Applied cryptography fundamentals — https://www.schneier.com/books/cryptography-engineering/
- Free graduate-level applied crypto book — https://toc.cryptobook.us/book.pdf

## 1. VPN (Normal) — Topics to Master

- VPN concepts overview — https://en.wikipedia.org/wiki/Virtual_private_network
- WireGuard protocol & cryptography — https://www.wireguard.com/protocol/
- WireGuard project home — https://www.wireguard.com/
- OpenVPN fundamentals & community resources — https://blog.openvpn.net/wireguard-mesh-vpn-guide
- IPsec / IKEv2 concepts (RFC) — https://www.rfc-editor.org/rfc/rfc7296
- strongSwan (real-world IPsec deployment/config) — https://strongswan.org/
- WireGuard vs IPsec vs OpenVPN comparison — https://www.zenarmor.com/docs/network-security-tutorials/ipsec-vs-wireguard
- VPN internals: protocols, leaks, kill switches — https://latesthackingnews.com/2026/06/24/how-a-vpn-works-protocols-leaks/
- DNS leaks — https://en.wikipedia.org/wiki/DNS_leak

## 2. Tor / VPN-over-Tor — Topics to Master

- How Tor works (official overview) — https://support.torproject.org/about-tor/how-tor-works/overview/
- Short technical introduction to Tor — https://spec.torproject.org/intro/index.html
- Onion services overview — https://community.torproject.org/onion-services/overview/
- Setting up/using onion services — https://community.torproject.org/onion-services/setup/
- Running/understanding Tor relays — https://community.torproject.org/relay/
- Tor support/documentation hub — https://support.torproject.org/
- Combining Tor with VPN (concepts, tor-over-vpn vs vpn-over-tor) — https://windscribe.com/blog/what-is-tor/

## 3. SIEM — Topics to Master

- Splunk free official training — https://www.splunk.com/en_us/training/free-courses/overview.html
- Hands-on SOC practice path — https://tryhackme.com/path/outline/soclevel1
- SOC analyst tools & skills roadmap — https://www.networkershome.com/soc-analyst-tools-skills-roadmap/
- MITRE ATT&CK framework (core reference) — https://attack.mitre.org/
- MITRE ATT&CK complete guide — https://www.splunk.com/en_us/blog/learn/mitre-attack.html
- MITRE ATT&CK guide for SOC/DFIR — https://cyberdefenders.org/blog/mitre-attack-framework/
- Writing/reading Sigma detection rules — https://github.com/SigmaHQ/sigma
- Beginner's guide to Sigma rules — https://socprime.com/blog/sigma-rules-the-beginners-guide/
- Blue Team Labs Online (practice) — https://blueteamlabsonline.com/
- CyberDefenders (practice/investigations) — https://cyberdefenders.org/

## 4. Offensive Concepts You Must Be Aware Of

- MITRE ATT&CK — Defense Evasion tactic (TA0005) — https://attack.mitre.org/tactics/TA0005/
- Defense evasion detection/response guide — https://www.manageengine.com/log-management/mitre-attack/defense-evasion.html
- Log/AD database tampering case study — https://www.manageengine.com/log-management/siem-use-cases/threats/active-directory-database-tampering.html
- IPsec/IKE VPN pentesting methodology — https://book.hacktricks.xyz/network-services-pentesting/ipsec-ike-vpn-pentesting
- Real-world critical IKEv1 auth-bypass exploitation — https://thehackernews.com/2026/06/critical-check-point-vpn-flaw-exploited.html
- NCSC alert on exploited VPN vulnerabilities — https://www.ncsc.gov.uk/news/alert-vpn-vulnerabilities
- Client-side vulnerabilities in commercial VPNs (research) — https://arxiv.org/pdf/1912.04669
- Tor traffic correlation / de-anonymization attacks — https://blog.torproject.org/traffic-correlation-using-netflows/
- Thirteen years of Tor attacks (catalog) — https://github.com/Attacks-on-Tor/Attacks-on-Tor
- De-anonymisation attacks on Tor: a survey — https://www.researchgate.net/publication/352938766_De-anonymisation_attacks_on_Tor_A_Survey
- Deep-learning flow correlation attack (DeepCorr) — https://arxiv.org/pdf/1808.07285
- AS-level adversaries against Tor — https://arxiv.org/pdf/1505.05173

## 5. Defensive / Mitigation Topics (to counter the above)

- Detection engineering workflow (build detections from ATT&CK techniques) — https://www.splunk.com/en_us/blog/learn/detection-as-code.html
- Atomic Red Team (simulate attacks to validate detections) — https://github.com/redcanaryco/atomic-red-team
- Splunk Attack Range (instrumented lab to test detections) — https://github.com/splunk/attack_range
- Writing effective Sigma rules for novices — https://www.dogesec.com/blog/writing_effective_sigma_rules_for_beginners/
- Mitigating VPN perimeter-device exploitation (patch/hardening guidance) — https://www.ncsc.gov.uk/news/alert-vpn-vulnerabilities
- Tor Project guidance on traffic-correlation mitigations — https://blog.torproject.org/traffic-correlation-using-netflows/
