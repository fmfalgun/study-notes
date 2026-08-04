# Cybersecurity Portfolio — Master Topic List

Compiled from a full file-by-file analysis of 874 Python files across `Projects/`, `Documents/`, and `Downloads/` (excluding non-cybersecurity and confidential folders). Each topic listed once. Full per-file backing detail: `topics_progress.log` (see note at bottom).

## 1. Offensive Security — Systematic Attack-Technique Implementation
Built a structured, multi-version (Python 3.8/3.10/3.11+) attack-technique library across 4 wireless protocols × 3 attack classes:

- **BLE**: DoS (advertising/address-rotation/ATT-read/ATT-write/connection/empty-packet/indication/notification/retransmission floods, connection-param abuse, L2CAP signaling storm, SMP pairing spam, scan-response amplification), Injection (malformed adv-data, packet crafting, protocol fuzzing), MITM (connection hijacking, data manipulation, pairing interception), plus GATT replay, BD_ADDR spoofing, just-works pairing bypass, device impersonation/relay
- **WiFi**: DoS (assoc/auth/beacon/deauth/disassoc floods, CTS/RTS flood, virtual carrier sense, channel flood, probe flood), Injection (ARP poison, DNS spoof, frame manipulation, packet injection, EAPOL injection, SSL strip), MITM (evil twin, karma attack, rogue AP), KRACK wrapper, reassociation attack
- **Zigbee**: DoS (ACK spoofing, assoc-request/beacon floods, PAN ID conflict, RF jamming), Injection (default-key exploit, insecure rejoin, malicious OTA firmware, replay, routing manipulation, touchlink factory reset, ZCL level-control/onoff injection), MITM (key-transport interception, malicious coordinator, router impersonation, touchlink MITM)
- **LoRa**: DoS (ACK flood, collision attack, join-request flood, RF jamming, uplink flood), Injection (application-payload/downlink-command/MAC-command injection, malicious uplink, payload fuzzing), MITM (downlink injection, join-accept manipulation, replay, rogue gateway, wormhole attack)

## 2. Zero-Trust IoT Authentication & Authorization (production system, ~500 files)
SPIFFE/SPIRE workload identity provisioning · X.509 certificate issuance/verification/mutual auth · multi-protocol (BLE/WiFi/Zigbee/XBee/LoRa) device-authentication agents · OPA/Rego policy-based authorization · AES-256-GCM encrypted control channel · MAC-hash device identity · device lifecycle state machines · network micro-segmentation enforcement · gateway/device registration & approval workflows · certificate lifecycle management (CLM) app · **post-quantum cryptography algorithm registry (ML-DSA/ML-KEM/hybrid)** · CRL/OCSP revocation · policy lifecycle management (versioning/approval/deployment/rollback) · policy anomaly-detection & effectiveness scoring · OPA bundle distribution

## 3. ML-Based Wireless Intrusion Detection
AWID3 WiFi IDS (two-stage MLP + XGBoost) · BLE anomaly detection (PyTorch autoencoder) · BLE Mesh IDS training pipeline (dataset gen, preprocessing, train/test split, confusion-matrix eval) · attacker/victim MAC attribution with confidence scoring · PCAP feature extraction (Shannon entropy, flow/window stats) · isolation-forest anomaly detection · ML model integrity verification (SHA-256 checksum manifests)

## 4. SDR / RF Signal Processing (GNU Radio)
HackRF/osmosdr flowgraphs · WFM broadcast receiver · custom BLE advertising receiver (access-address correlator, LFSR dewhitening, CRC-24 verification, AFH/frequency-hopping reconstruction) · Zigbee 802.15.4 O-QPSK receiver (chip correlation → DSSS despread → SFD → MAC → NWK → APS → ZCL full decode chain) · SX126x LoRa HAT driver · LoRa passive sniffing · channel-hopping IQ capture

## 5. Network Reconnaissance / OSINT
WHOIS enumeration & automated risk scoring · theHarvester integration · certificate-transparency (crt.sh) subdomain enumeration · passive subdomain enumeration (subfinder) · DNS reconnaissance (zone transfer, SPF/DMARC, brute-forcing) · HTTP liveness probing & TLS inspection · web technology fingerprinting (WhatWeb) · IoT/camera device discovery (ASN/CIDR enumeration, RTSP/Telnet banner grabbing, default-login detection) · CVE/vulnerability intelligence aggregation (NVD, EPSS, KEV, MITRE ATT&CK, Exploit-DB, Shadowserver, AttackerKB)

## 6. Web/App Pentest Infrastructure
Config-driven pentest pipeline orchestration · EAV-based findings database (repository pattern) · automated markdown report generation · HTTP file server with path-traversal protection · curses/TUI recon dashboards

## 7. Malware-Adjacent Tooling
Keylogger (input capture, buffering, log rotation, periodic screenshot capture, SMTP exfiltration, anti-detection/evasion, stealth/persistence)

## 8. Blockchain
Hyperledger Fabric connection-profile/MSP configuration repair

## 9. Full-Stack Security Dashboards (production MVC apps)
Flask MVC architecture (controllers/models/pytest suites) · JWT/RBAC authentication middleware · MySQL-backed device/policy/audit data layer · device blocking/quarantine (MAC-level and protocol-level) · CVE data scraping/ingestion CLI · authentication event-log ingestion

## 10. General Software/Platform Engineering
FastAPI/Flask REST API design · SQLite/MySQL schema migration & persistence · CORS/security-header hardening · rate limiting · CI/CD data-pipeline generation

---

**Source data**: full per-file topic breakdown (874 lines, one per file) was compiled from a
session-scoped scratchpad that no longer exists — ask if you want the raw per-file breakdown
regenerated somewhere permanent.
