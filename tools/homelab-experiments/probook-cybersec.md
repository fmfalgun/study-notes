# HP ProBook 445 G11 — Cybersecurity (Build & Analysis)

**Machine**: HP ProBook 445 14" G11 (Ryzen 5 7535U, 12 threads @ 4.6GHz, 16GB RAM, Kali GNU/Linux, portable/battery)
**Field**: Cybersecurity (2nd priority)
**Scope**: coding/analysis side of security — cryptography & math, digital forensics, blockchain, and the low-level fundamentals malware analysis leans on. Explicitly **not** offensive/hacking practice — nothing here targets a real device or node on any network. Every target is self-generated, self-compiled, or a public dataset/sample used for static reference only.

Every idea below is inspired by `../../tracks/isro/topics/gfg-isro-topic-map.md` and `../../tracks/gate/topics/gfg-gate-topic-map.md`. Each carries exactly one reference link. Ideas run as dev → deploy (days to 1-2 weeks) → analyze cycles.

Some categories here are a **heavier compute tier** of a topic whose lightest version lives in `rpi5-cs-eng.md` (noted inline).

---

## Mathematics (Number Theory & Modular Arithmetic — crypto foundations)

- **Modular Exponentiation & Miller-Rabin Primality Library** — implement fast modular exponentiation and Miller-Rabin primality testing, use both as the foundation for your own RSA below. Ref: [Modular Multiplication](https://www.geeksforgeeks.org/dsa/modular-multiplication/)
- **Extended Euclidean Algorithm + Modular Inverse Toolkit** — build it, verify against known RSA key pairs. Ref: [Modular Addition](https://www.geeksforgeeks.org/engineering-mathematics/modular-addition/)
- **Cyclic Group Sandbox (Generators, Discrete Log)** — implement finite cyclic-group arithmetic used in Diffie-Hellman, visualize generator orbits. Ref: [Groups](https://www.geeksforgeeks.org/engineering-mathematics/groups-discrete-mathematics/)

## Cyber Security — Cryptography (build from scratch)

- **Classical Cipher Suite (Caesar → Vigenère → Playfair)** — implement each, then break each with frequency analysis on ciphertexts you generate yourself. Ref: [sobolevn/awesome-cryptography](https://github.com/sobolevn/awesome-cryptography)
- **AES from Scratch (S-box, key schedule, GF(2⁸) arithmetic)** — implement the full block cipher, validate against NIST test vectors, benchmark vs OpenSSL. Ref: [sobolevn/awesome-cryptography](https://github.com/sobolevn/awesome-cryptography)
- **RSA from Scratch + Timing Side-Channel Study** — implement naive vs constant-time modular exponentiation, deploy a small encrypted-message service between your own machines for a week, log and compare timing distributions. Ref: [pFarb/awesome-crypto-papers](https://github.com/pFarb/awesome-crypto-papers)
- **Diffie-Hellman Key Exchange Across Your Own Machines** — implement key exchange between Pi/ProOne/ProBook over your LAN, verify shared-secret correctness — never touching any device you don't own. Ref: [pFarb/awesome-crypto-papers](https://github.com/pFarb/awesome-crypto-papers)
- **Password-Hashing Cost Analysis (bcrypt/Argon2 parameter tuning)** — implement/benchmark different cost factors on your own CPU, reason mathematically about crack-time estimates (no cracking real accounts). Ref: [sobolevn/awesome-cryptography](https://github.com/sobolevn/awesome-cryptography)

## Cyber Security — Digital Forensics

- **Disk-Image File Carver (deleted-file recovery via magic bytes)** — generate your own FAT32/ext4 test images, delete files, recover via signature scanning, measure recovery accuracy. Ref: [The-Art-of-Hacking/h4cker](https://github.com/The-Art-of-Hacking/h4cker)
- **Mini Memory-Forensics Tool (process-list/string extractor from a raw memory dump)** — dump your own VM's memory offline, parse process structures, extract artifacts — a tiny Volatility. Ref: [CERT-Polska/drakvuf-sandbox](https://github.com/CERT-Polska/drakvuf-sandbox)
- **Log-Based Forensic Timeline Builder** — ingest your own system/auth logs for a week, reconstruct an activity timeline, flag anomalies (failed logins, unusual process spawns) on your own machine's data only. Ref: [The-Art-of-Hacking/h4cker (defensive-security)](https://github.com/The-Art-of-Hacking/h4cker/tree/master/cybersecurity-domains/defensive-security)
- **Hash-Based Evidence Integrity / Chain-of-Custody Tool** — build a tool that hashes+signs "evidence" files and logs a verifiable custody chain, run it over your own generated files for a week. Ref: [alphaSeclab/awesome-reverse-engineering](https://github.com/alphaSeclab/awesome-reverse-engineering)

## Cyber Security — Blockchain

- **Minimal Blockchain from Scratch (blocks, Merkle trees, proof-of-work)** — implement hashing/PoW/Merkle proofs, deploy a 2-3 node private chain across your own machines only (ProBook + Pi + ProOne), run it mining/syncing for 1-2 weeks. Ref: [ethereumbook/ethereumbook](https://github.com/ethereumbook/ethereumbook)
- **Hyperledger Fabric Local Network Walkthrough** — stand up a permissioned-chain sample network locally, deploy a simple chaincode, analyze the consensus/endorsement flow. Ref: [hyperledger/fabric-samples](https://github.com/hyperledger/fabric-samples)
- **Merkle-Proof Verifier for Your Own Chain's Transactions** — build inclusion-proof generation/verification independent of the chain implementation above. Ref: [ethereumbook/ethereumbook](https://github.com/ethereumbook/ethereumbook)

## Cyber Security — Malware-Analysis Fundamentals *(binary internals, no real malware execution)*

- **PE/ELF Format Parser from Scratch** — parse headers/sections/import-tables of your own compiled binaries, build a mini `file`/`readelf`. Ref: [alphaSeclab/awesome-reverse-engineering](https://github.com/alphaSeclab/awesome-reverse-engineering)
- **Toy Packer + Unpacker** — write a simple XOR/RLE packer for a benign binary you compiled, then write the unpacker and an entropy-spike heuristic that flags packed sections. Ref: [alphaSeclab/awesome-reverse-engineering](https://github.com/alphaSeclab/awesome-reverse-engineering)
- **Static-Analysis Heuristics Engine (entropy, import-table suspicion scoring)** — run it over a corpus of benign binaries you compile with varying compilers/flags, tune the false-positive rate. Ref: [fabrimagic72/malware-samples](https://github.com/fabrimagic72/malware-samples) *(hash/metadata reference only — not detonation)*
- **Mini Disassembler for a Subset of x86/ARM** — decode real instruction bytes from your own compiled binaries into mnemonics, verify against `objdump`. Ref: [alphaSeclab/awesome-reverse-engineering](https://github.com/alphaSeclab/awesome-reverse-engineering)

## Cyber Security — Network Security *(previously missed — build/analysis only, still no real targets)*

- **Custom IDS Rule Engine (Suricata-Style Signature Matching)** — write your own signature-matching engine, generate your own pcaps (from your Diffie-Hellman/blockchain traffic above) to test detection rules against, deploy it sniffing your own machines' traffic for a week. Ref: [OISF/suricata](https://github.com/OISF/suricata)
- **Deliberately-Vulnerable Local Web App + OWASP Top 10 Static Analyzer** — build a small intentionally-vulnerable app that never leaves localhost, then write your own static-analysis checks that detect SQLi/XSS/SSRF-shaped code patterns in it (and in other code you write). Ref: [swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) *(used only as a vulnerability-class reference, not against any real target)*
- **Firewall Rule Simulator (Packet-Filter Logic Engine)** — implement a rule-matching engine (allow/deny by IP/port/protocol) over synthetic packet streams, deploy logging which of your own rules fire over a week of your own traffic. Ref: [Types of Network Firewall](https://www.geeksforgeeks.org/computer-networks/types-of-network-firewall/)
- **Incident-Response Playbook Automation Tool** — build a small tool that ingests your own logs, matches them against IR runbook triggers (e.g. repeated failed logins → lockout playbook step), and logs which playbook steps would fire. Ref: [The-Art-of-Hacking/h4cker (defensive-security)](https://github.com/The-Art-of-Hacking/h4cker/tree/master/cybersecurity-domains/defensive-security)

## Databases *(Tier 2 — heavier than `rpi5-cs-eng.md`; forensics/concurrency angle)*

- **Write-Ahead-Log Recovery Simulator with Crash Injection** — build a DB engine with a WAL, randomly `kill -9` it mid-write, verify ARIES-style recovery restores consistency, analyze recovery time vs log size. Ref: [Log-Based Recovery](https://www.geeksforgeeks.org/dbms/log-based-recovery-in-dbms/)
- **Concurrency-Control Protocol Comparator (2PL vs Timestamp Ordering)** — implement both over a toy transactional store, generate conflicting-transaction workloads, measure abort rates/throughput. Ref: [Two Phase Locking](https://www.geeksforgeeks.org/dbms/two-phase-locking-protocol/)
- **Forensics-on-a-Database-File** — given a raw SQLite/custom DB file with "deleted" rows, recover un-vacuumed/freed pages to reconstruct the deleted records. Ref: [File Organization in DBMS](https://www.geeksforgeeks.org/dbms/file-organization-in-dbms-set-1/)

## Data Structures & Algorithms *(Tier 2 — heavier than `rpi5-cs-eng.md`)*

- **External Merge Sort at Multi-GB Scale + I/O Profiling** — same idea as the Pi's tier-1 version but at a scale that needs ProBook's extra RAM/disk; compare I/O-bound behavior across the two machines. Ref: [Divide & Conquer Notes for GATE](https://www.geeksforgeeks.org/dsa/divide-and-conquer-notes-for-gate-exam/)
- **Large-Graph Shortest-Path Benchmark (Bellman-Ford vs Floyd-Warshall vs Dijkstra at scale)** — generate large synthetic graphs, benchmark all three, analyze where each wins. Ref: [Graph Algorithms Notes for GATE](https://www.geeksforgeeks.org/dsa/graph-based-algorithms-for-gate-exam/)
