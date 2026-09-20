# GATE topics vs Google's security-role requirements vs the books we have

Compares three things: (1) the GATE topic map and priority tiers (`../topics/gfg-gate-topic-map.md`, `../exam-priority-report.md`); (2) the job descriptions of **Google's 169 live security roles** (`google-live/details-checklist.md`, 19-20 Sep 2026); (3) the earlier `cybersecurity.md` (its section 2 stack and section 3 GATE overlap). Books come from `Projects/no-github-remote/courses/READING_LIST.md` plus other PDFs found on disk. Built by `google-live/details/build_gate_google_report.py`.

## Read this first

- **Job descriptions are not interview questions.** They show what Google *requires or prefers*, not what an interview asks. Whatever is said about interviews below is general knowledge, not from our data.
- Counts are roles out of 169 that mention the topic in minimum, preferred or responsibilities text; 'minimum' = in the stated minimum qualifications. Keyword matching, one-day snapshot.
- GATE has **no Cyber Security section** (`gfg-gate-topic-map.md`, 'Not covered'). The overlap is foundational, through the sections below.
- **Path fix:** `READING_LIST.md` prints paths starting `../hardisk/...`; the real location is `../hardisk/...`. All 171 listed PDFs exist at the corrected path. The list itself was not edited.

## 1. GATE topics that Google's security roles also require (ranked by evidence)

### 1. Computer networks and network security

- **GATE:** Computer Networks - Tier 2, score 14.8 (`exam-priority-report.md`)
- **Google roles:** 56 of 169 roles mention networking/protocols/network security; 40 as a MINIMUM (mostly the standard bullet 'experience with security engineering, computer and network security and security protocols'). Literal 'TCP/IP', 'DNS', 'TLS' appear in 0 descriptions.
- **Books from the reading list:** Attacking Network Protocols — Hacker's Guide to Capture, Analysis, Exploitation (7/10); Nmap Network Exploration and Security Auditing Cookbook, 2nd Ed (7/10); Applied Network Security Monitoring (8/10); Network Security Through Data Analysis, 2nd Ed (7/10); Cisco Press — Penetration Testing and Network Defense (7/10); Network Layer — Forouzan (slides) (5/10); Wireshark Top Filters (quick ref) (7/10); SILENCE ON THE WIRE — Passive Reconnaissance and Indirect Attacks (6/10)
- **Other PDFs on disk:** Tanenbaum - Computer Networks; CCNA 200-301 Official Cert Guide Vol 1 (Cisco Press); CCNA 200-301 Vol 2
- **Note:** Covers GATE's layered model (Tanenbaum, CCNA) plus the attacker/defender view. No Kurose & Ross on disk.

### 2. Discrete maths, number theory and cryptography

- **GATE:** Discrete Mathematics - Tier 1, score 30.6 (13 complex-question hits)
- **Google roles:** Cryptography/encryption/PKI/TLS in 18 roles, but only 3 as a minimum (14 as preferred). Not a universal requirement; a specialist one.
- **Books from the reading list:** Cryptography and Network Security — Principles and Practice, 7th Global Ed (6/10); Elementary Cryptanalysis (227 pg) (7/10); Cryptography (31 pg) (7/10); Cryptography and Network Security 5/e — William Stallings (9/10)
- **Other PDFs on disk:** Hacking Secret Ciphers with Python; Post-Quantum Cryptography Application Research Report 2023
- **Note:** Stallings is the book `cybersecurity.md` named for RSA/DH; the 9/10 entry in the list is a lecture-notes PDF (`1 introduction new.pdf`); the full book is the 7th Global Ed entry. No discrete-maths textbook PDF on disk.

### 3. Operating systems, Linux and memory-level security

- **GATE:** Operating System - Tier 2, score 13.4
- **Google roles:** OS/kernel/Linux/virtualization in 21 roles (8 minimum); C/C++/Rust/memory-corruption in 37 (25 minimum); reverse engineering/assembly/exploitation in 29 (4 minimum).
- **Books from the reading list:** Operating System Security — Jaeger (236 pg) (7/10); Linux Essentials for Cybersecurity (6/10); Penetration Testing with the Bash Shell (8/10); Buffer Overflow Attacks — Detect, Exploit, Prevent (5/10); The Shellcoder's Handbook — Discovering and Exploiting Security Holes (6/10); Reverse Engineering for Beginners (5/10); Rootkits and Bootkits — Reversing Modern Malware (No Starch, 2019) (6/10); Gray Hat Hacking, 4th Ed (6/10)
- **Other PDFs on disk:** Hacking: The Art of Exploitation, 2nd Ed; Rootkits: Subverting the Windows Kernel; Hands-On System Programming with Linux
- **Note:** No OS textbook (Silberschatz / Tanenbaum OS) on disk: process scheduling, deadlock, paging theory that GATE tests must come from your notes or GFG pages.

### 4. Programming, data structures and algorithms (the coding round)

- **GATE:** Programming & Data Structures - Tier 1, score 51.6 (highest of all GATE topics); Algorithms - Tier 2, score 10.9
- **Google roles:** 'Coding experience in a general-purpose language' is a MINIMUM in 68 of 169 roles (the most common technical minimum). Python in 47 roles (26 minimum), C++ in 35 (25), Go in 31 (24). Data structures / algorithms named in 20 roles (4 minimum, 16 preferred).
- **Books from the reading list:** Coding for Penetration Testers — Building Better Tools (6/10); Python Penetration Testing Essentials (5/10); Learning Python Web Penetration Testing (6/10)
- **Other PDFs on disk:** C++ Primer; A Complete Guide to Standard C++ Algorithms; Black Hat Python; Black Hat Go; Gray Hat Python; Go in Action
- **Note:** **Biggest gap.** GATE's #1 topic and Google's #1 minimum requirement have no data-structures or algorithms textbook on disk. `cybersecurity.md` section 3 did not list this overlap at all. Your own markdown notes exist (`Documents/learning-docs/data_structures_complete.md`, `algorithms_masterclass.md`, `Projects/DSA/`) but they are not PDFs.

### 5. Computer organization, digital logic and hardware/platform security

- **GATE:** Digital Logic - Tier 2, score 15.0; Computer Organization - Tier 2, score 14.9
- **Google roles:** Hardware/firmware/secure-boot/TPM/silicon in 29 roles (11 minimum).
- **Books from the reading list:** A Practical Guide to TPM 2.0 (375 pg) (7/10); Hardware IP Security and Trust (6/10); The Hardware Hacker (8/10); Hacking The Xbox (hardware security) (8/10); Security and Privacy in Internet of Things — Models, Algorithms, Implementations (7/10)
- **Other PDFs on disk:** Computer Organization and Design, RISC-V Ed (Patterson & Hennessy); Computer Architecture, 6th Ed, RISC-V; Digital Design: A Systems Approach (Dally & Harting); The RISC-V Reader
- **Note:** Good coverage: Patterson & Hennessy and Dally for the GATE side, the TPM and hardware-security books for the security side. Bhunia & Tehranipoor (named in `cybersecurity.md`) is NOT on disk.

### 6. Databases and SQL security

- **GATE:** Databases (DBMS) - Tier 2, score 16.8
- **Google roles:** SQL/databases in 17 roles (10 minimum).
- **Books from the reading list:** SQL Injection (22 pg) (7/10); Securing SQL Server — Protecting Your Database from Attackers (5/10); Database Forensics (220 pg) (7/10); The Web Application Hacker's Handbook, 2nd Ed (8/10)
- **Note:** Only the security angle is covered; no DBMS textbook (normalization, transactions, indexing) on disk.

### 7. Compilers, program analysis and reverse engineering

- **GATE:** Compiler Design - Tier 2, score 10.9
- **Google roles:** Compilers/static analysis/fuzzing in 7 roles (1 minimum); reverse engineering/assembly/exploitation in 29 (see topic 3).
- **Books from the reading list:** Reverse Engineering for Beginners (5/10); Malware Analyst's Cookbook (2011) (6/10); Hacking Exposed Malware & Rootkits (6/10); Malware Analysis and Detection Engineering (8/10)
- **Note:** Weak overlap. Worth it only for malware / vulnerability-research roles.

### 8. Theory of computation

- **GATE:** Theory of Computation - Tier 3, score 7.8
- **Google roles:** Regex/parsing/automata in 1 role.
- **Note:** Not a Google security requirement in the data. Study it for GATE only.

## 2. What Google requires that GATE does not test

| Topic | Google roles | Books from the reading list | Gap |
|---|---|---|---|
| Threat modeling and secure design | 54 roles (27 minimum) | Cybersecurity — Attack and Defense Strategies (Red + Blue Team) (8/10) | No threat-modeling book on disk (closest: Cybersecurity - Attack and Defense Strategies) |
| Incident response and detection | IR 40 roles, detection/SIEM/SOC 51 | Intelligence-Driven Incident Response (6/10); Computer Incident Response and Forensics Team Management (8/10); Malware Analysis and Detection Engineering (8/10); Mastering Splunk (7/10) | - |
| Digital forensics | 23 roles (15 minimum) | File System Forensic Analysis — Brian Carrier (382 pg) (7/10); Computer Forensics — Investigating Hard Disks, File & Operating Systems (240 pg) (8/10); Handbook of Digital Forensics and Investigation (7/10) | - |
| Web and application security | application security / secure code review 31 roles | The Web Application Hacker's Handbook, 2nd Ed (8/10); Mastering Modern Web Penetration Testing (298 pg) (8/10); The Browser Hacker's Handbook (6/10); Real-World Bug Hunting — A Field Guide to Web Hacking (5/10) | - |
| Threat intelligence / OSINT | 25 roles | Collaborative Cyber Threat Intelligence — Detecting and Responding to Advanced Attacks (8/10); Practical Cyber Intelligence (7/10); Open Source Intelligence Methods and Tools (7/10) | - |
| AI / ML and AI-security | AI/ML in 64 roles (17 minimum) | Mastering Machine Learning for Penetration Testing (8/10); Malware Data Science — Attack Detection and Attribution (No Starch) (5/10) | Nothing on LLM/agent security on disk |
| Offensive security and certifications (OSCP/GIAC/CISSP as preferred) | pentest/red team 35 roles; OSCP-family 11, GIAC 17, CISSP 11 (all mostly preferred) | Penetration Testing — A Hands-on Intro to Hacking, Georgia Weidman (531 pg) (8/10); The Hacker Playbook 2 — Practical Guide to Penetration Testing (8/10); Metasploit — The Penetration Tester's Guide (6/10); CEH v13 — Certified Ethical Hacker (latest, 80MB) (8/10); SANS SEC542 — Web App Penetration Testing, Day 2 (8/10) | - |

## 3. Comparison with `cybersecurity.md`

**Confirmed by Google's descriptions:** Python, C/C++ and Rust (35 and 7 roles) as languages; threat modeling (33), incident response (40), forensics (23), penetration-testing methodology (18); hardware/firmware/TPM/secure boot (11 for the narrow TPM/UEFI terms); the four GATE overlaps in section 3 (networks, discrete maths/crypto, OS, digital logic/COA).

**Missing from `cybersecurity.md` section 3, but strong in Google's data:** **Programming and data structures** (GATE Tier 1; coding is the most common technical minimum, 68 roles) and, weakly, **databases/SQL** (17 roles).

**In `cybersecurity.md` but NOT supported by Google's descriptions** (the earlier list came from other companies' postings): AWS and Azure (0 roles), Nmap, Burp, Metasploit, LDAP, PKI, CVE/NVD (0 each), Splunk (2), Elastic (0), QRadar (1), CrowdStrike/SentinelOne/Defender (3), MISP/VirusTotal (0). Google's descriptions name few commercial tools; they name skills. Certifications are almost all *preferred* (any certification: 39 roles, 36 as preferred).

**New since `cybersecurity.md`:** AI/ML appears in 64 roles (17 as a minimum); SOAR in 7; NIST in 7, ISO 27001 in 5, SOC 2 in 4.

## 4. Final list: cybersecurity topics common to GATE and Google, with the PDFs we have

Ordered by combined weight: GATE tier/score first, Google minimum-requirement count second.

| # | Topic | GATE | Google roles (minimum) | PDFs on disk |
|---|---|---|---|---|
| 1 | Programming, DS and algorithms, in Python/C++/Go | Tier 1 (51.6) + Algorithms 10.9 | 68 coding, 47 Python (26), 35 C++ (25), 31 Go (24) | C++ Primer, Std C++ Algorithms, Black Hat Python, Black Hat Go, Gray Hat Python, Go in Action, Coding for Penetration Testers. **No DS/algorithms textbook** |
| 2 | Computer networks and network security | Tier 2 (14.8) | 56 (40) | Tanenbaum, CCNA vols 1-2, Attacking Network Protocols, Nmap Cookbook, Applied NSM |
| 3 | Cryptography (from discrete maths / number theory) | Tier 1 (30.6) | 18 (3) | Stallings 7th Ed, Elementary Cryptanalysis, Hacking Secret Ciphers, PQC report |
| 4 | OS internals, Linux, memory safety, exploitation basics | Tier 2 (13.4) | 21 (8); C/C++/memory 37 (25); RE/exploit 29 (4) | Jaeger OS Security, Art of Exploitation, Shellcoder's, Linux Essentials, Bash pentest, System Programming with Linux. **No OS textbook** |
| 5 | Computer organization / digital logic -> hardware & platform security | Tier 2 (14.9, 15.0) | 29 (11) | Patterson & Hennessy (RISC-V), Dally Digital Design, Computer Architecture 6th Ed, TPM 2.0 guide, Hardware Hacker |
| 6 | Databases / SQL security | Tier 2 (16.8) | 17 (10) | SQL Injection notes, Securing SQL Server, WAHH 2nd Ed. **No DBMS textbook** |
| 7 | Compilers -> program analysis / reverse engineering | Tier 2 (10.9) | 7 (1) / 29 (4) | Reverse Engineering for Beginners, Malware Analyst's Cookbook, Rootkits and Bootkits |

**Interview note (general knowledge, not from our data):** security-engineer interviews at large companies are commonly described as a coding round (data structures and algorithms), a networking/OS/systems round, and a security-design or threat-modeling round. Topics 1, 2, 4 and the threat-modeling row of section 2 match that pattern; topics 5 to 7 are role-specific.

## 5. Appendix: paths

### From the reading list (corrected prefix)

| Book | Score | Section | Path |
|---|---|---|---|
| Attacking Network Protocols — Hacker's Guide to Capture, Analysis, Exploitation | 7/10 | 3 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Attacking Network Protocols A Hacker's Guide to Capture, Analysis, and Exploitation.pdf` |
| Nmap Network Exploration and Security Auditing Cookbook, 2nd Ed | 7/10 | 3 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Nmap Network Exploration and Security Auditing Cookbook - Second Edition.pdf` |
| Applied Network Security Monitoring | 8/10 | 3 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Applied Network Security Monitoring.pdf` |
| Network Security Through Data Analysis, 2nd Ed | 7/10 | 3 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Network Security Through Data Analysis, 2nd Edition.pdf` |
| Cisco Press — Penetration Testing and Network Defense | 7/10 | 3 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Cisco Press - Penetration Testing and Network Defense.pdf` |
| Network Layer — Forouzan (slides) | 5/10 | 3 | `../hardisk/hdd/disk/course/WEEK-14/Dr. Nitin kumar/Network-Layer-Forouzan.pdf` |
| Wireshark Top Filters (quick ref) | 7/10 | 12 | `../hardisk/hdd/disk/course/WEEK-4/Wireshark Top Filters.pdf` |
| SILENCE ON THE WIRE — Passive Reconnaissance and Indirect Attacks | 6/10 | 3 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/SILENCE ON THE WIRE A Field Guide to Passive Reconnaissance and Indirect Attacks.pdf` |
| Cryptography and Network Security — Principles and Practice, 7th Global Ed | 6/10 | 13 | `../hardisk/hdd/old_files/downloads/Download/cryptography-and-network-security_-principles-and-practice-7th-global-edition.pdf` |
| Elementary Cryptanalysis (227 pg) | 7/10 | 13 | `../hardisk/hdd/old_files/downloads/Download/(New mathematical library 22) Sinkov, Abraham - Elementary cryptanalysis-Cambridge University Press [distributor], Mathematical Association of America (2009).pdf` |
| Cryptography (31 pg) | 7/10 | 13 | `../hardisk/hdd/disk/course/New folder/Prasad Docs/20. Cryptography.pdf` |
| Cryptography and Network Security 5/e — William Stallings | 9/10 | 13 | `../hardisk/hdd/old_files/coursework/2_sem/1 NCS/notes/1 introduction new.pdf` |
| Operating System Security — Jaeger (236 pg) | 7/10 | 13 | `../hardisk/hdd/old_files/books/Jaeger - Operating System Security-ebook.pdf` |
| Linux Essentials for Cybersecurity | 6/10 | 14 | `../hardisk/hdd/old_files/books/Linux Essentials for Cybersecurity.pdf` |
| Penetration Testing with the Bash Shell | 8/10 | 14 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Penetration Testing with the Bash Shell.pdf` |
| Buffer Overflow Attacks — Detect, Exploit, Prevent | 5/10 | 5 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Buffer Overflow Attacks -  Detect, Exploit, Prevent.pdf` |
| The Shellcoder's Handbook — Discovering and Exploiting Security Holes | 6/10 | 5 | `../hardisk/hdd/old_files/books/The Shellcoder's Handbook Discovering and Exploiting Security Holes ( PDFDrive ).pdf` |
| Reverse Engineering for Beginners | 5/10 | 5 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Reverse Engineering for Beginners.pdf` |
| Rootkits and Bootkits — Reversing Modern Malware (No Starch, 2019) | 6/10 | 5 | `../hardisk/hdd/old_files/books/Alex Matrosov, Eugene Rodionov, Sergey Bratus - Rootkits and Bootkits_ Reversing Modern Malware and Next Generation Threats-No Starch Press (2019).pdf` |
| Gray Hat Hacking, 4th Ed | 6/10 | 2 | `../hardisk/hdd/old_files/books/Gray_Hat_Hacking_4th_Edition.pdf` |
| Coding for Penetration Testers — Building Better Tools | 6/10 | 2 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Coding for Penetration Testers_ Building Better Tools.pdf` |
| Python Penetration Testing Essentials | 5/10 | 2 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Python Penetration Testing Essentials.pdf` |
| Learning Python Web Penetration Testing | 6/10 | 1 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Learning Python Web Penetration Testing.pdf` |
| A Practical Guide to TPM 2.0 (375 pg) | 7/10 | 8 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/A Practical Guide to TPM 2.0_ Using the New Trusted Platform Module in the New Age of Security.pdf` |
| Hardware IP Security and Trust | 6/10 | 8 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Hardware IP Security and Trust.pdf` |
| The Hardware Hacker | 8/10 | 8 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/The Hardware Hacker.pdf` |
| Hacking The Xbox (hardware security) | 8/10 | 8 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Hacking The Xbox.pdf` |
| Security and Privacy in Internet of Things — Models, Algorithms, Implementations | 7/10 | 8 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Security and Privacy in Internet of Things (IoTs) - Models, Algorithms and Implementations.pdf` |
| SQL Injection (22 pg) | 7/10 | 1 | `../hardisk/hdd/disk/course/New folder/Prasad Docs/15. SQL Injection (1).pdf` |
| Securing SQL Server — Protecting Your Database from Attackers | 5/10 | 1 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Securing SQL Server Protecting Your Database from Attackers 3rd Edition.pdf` |
| Database Forensics (220 pg) | 7/10 | 6 | `../hardisk/hdd/old_files/coursework/1_sem/3_DF/Misc Part 2/Database Forensics.pdf` |
| The Web Application Hacker's Handbook, 2nd Ed | 8/10 | 1 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/The Web Application Hackers Handbook (2nd Edition).pdf` |
| Malware Analyst's Cookbook (2011) | 6/10 | 5 | `../hardisk/hdd/old_files/coursework/2_sem/3_REMA/Books/2011_Malware Analysts Cookbook.pdf` |
| Hacking Exposed Malware & Rootkits | 6/10 | 5 | `../hardisk/hdd/old_files/books/Hacking exposed malware & rootkits_ malware & rootkits security secrets & solutions ( PDFDrive.com ).pdf` |
| Malware Analysis and Detection Engineering | 8/10 | 5 | `../hardisk/hdd/disk/course/WEEK-4/Malware Analysis and Detection Engineering.pdf` |
| Cybersecurity — Attack and Defense Strategies (Red + Blue Team) | 8/10 | 2 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Cybersecurity – Attack and Defense Strategies Infrastructure security with Red Team and Blue Team tactics.pdf` |
| Intelligence-Driven Incident Response | 6/10 | 6 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Intelligence-Driven Incident Response.pdf` |
| Computer Incident Response and Forensics Team Management | 8/10 | 6 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Computer Incident Response and Forensics Team Management - Conducting a Succesful Incident Response.pdf` |
| Mastering Splunk | 7/10 | 10 | `../hardisk/hdd/disk/course/WEEK-24/CEH/mastering-splunk.pdf` |
| File System Forensic Analysis — Brian Carrier (382 pg) | 7/10 | 6 | `../hardisk/hdd/old_files/coursework/1_sem/3_DF/Misc Part 2/info_file_system_forensic_analysis.pdf` |
| Computer Forensics — Investigating Hard Disks, File & Operating Systems (240 pg) | 8/10 | 6 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Computer Forensics - Investigating Hard Disks, File & Operating Systems.pdf` |
| Handbook of Digital Forensics and Investigation | 7/10 | 6 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Handbook of Digital Forensics and Investigation.pdf` |
| Mastering Modern Web Penetration Testing (298 pg) | 8/10 | 1 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Mastering Modern Web Penetration Testing.pdf` |
| The Browser Hacker's Handbook | 6/10 | 1 | `../hardisk/hdd/old_files/books/The Browser Hacker's Handbook ( PDFDrive ).pdf` |
| Real-World Bug Hunting — A Field Guide to Web Hacking | 5/10 | 1 | `../hardisk/hdd/old_files/books/Real-World Bug Hunting A Field Guide to Web Hacking Real-World Bug Hunting A Field Guide to Web Hacking.pdf` |
| Collaborative Cyber Threat Intelligence — Detecting and Responding to Advanced Attacks | 8/10 | 9 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Collaborative Cyber Threat Intelligence Detecting and Responding to Advanced Cyber Attacks at the National Level.pdf` |
| Practical Cyber Intelligence | 7/10 | 9 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Practical Cyber Intelligence.pdf` |
| Open Source Intelligence Methods and Tools | 7/10 | 9 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Open Source Intelligence Methods and Tools.pdf` |
| Mastering Machine Learning for Penetration Testing | 8/10 | 2 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Mastering Machine Learning for Penetration Testing.pdf` |
| Malware Data Science — Attack Detection and Attribution (No Starch) | 5/10 | 5 | `../hardisk/hdd/old_files/books/Joshua Saxe, Hillary Sanders - Malware Data Science_ Attack Detection and Attribution-No Starch Press (2018).pdf` |
| Penetration Testing — A Hands-on Intro to Hacking, Georgia Weidman (531 pg) | 8/10 | 2 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Penetration Testing - A hands-on introduction to Hacking.pdf` |
| The Hacker Playbook 2 — Practical Guide to Penetration Testing | 8/10 | 2 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/The Hacker Playbook 2- Practical Guide To Penetration Testing.pdf` |
| Metasploit — The Penetration Tester's Guide | 6/10 | 2 | `../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Metasploit The Penetration Tester's Guide.pdf` |
| CEH v13 — Certified Ethical Hacker (latest, 80MB) | 8/10 | 12 | `../hardisk/hdd/disk/course/WEEK-24/CEH/CEH v13.pdf` |
| SANS SEC542 — Web App Penetration Testing, Day 2 | 8/10 | 12 | `../hardisk/hdd/disk/course/WEEK-15/SANS Web VAPT/sans 542-Day2.pdf` |

### Not in the reading list, found on disk

| Book | Path |
|---|---|
| Tanenbaum - Computer Networks | `../hardisk/hdd/old_files/books/Andrew S. Tanenbaum - Computer Networks.pdf` |
| CCNA 200-301 Official Cert Guide Vol 1 (Cisco Press) | `../hardisk/hdd/old_files/books/12381imguf_CiscoPress-CCNA-200-301-Official-Cert-Guide-Volume-1.pdf` |
| CCNA 200-301 Vol 2 | `../hardisk/hdd/old_files/books/ccna-200-301-vol.-2.pdf` |
| Hacking: The Art of Exploitation, 2nd Ed | `../hardisk/hdd/old_files/books/Hacking - The Art of Exploitation_2nd Ed.pdf` |
| Rootkits: Subverting the Windows Kernel | `../hardisk/hdd/old_files/books/Rootkits - Subverting the Windows Kernel.pdf` |
| Hands-On System Programming with Linux | `../hardisk/hdd/old_files/books/Hands-On System Programming With Linux Explore Linux System Programming Interfaces, Theory, And Practice ( PDFDrive.com ).pdf` |
| C++ Primer | `../hardisk/hdd/old_files/books/CPPPrimer.pdf` |
| A Complete Guide to Standard C++ Algorithms | `../hardisk/hdd/old_files/books/a_complete_guide_to_standard_cpp_algorithms_v1_0_1.pdf` |
| Black Hat Python | `../hardisk/hdd/old_files/books/Black Hat Python_ Python Programming for Hackers and Pentesters ( PDFDrive.com ).pdf` |
| Black Hat Go | `../hardisk/hdd/old_files/books/Black_Hat_Go.pdf` |
| Gray Hat Python | `../hardisk/hdd/old_files/books/Gray_Hat_Python_Python_Programming.pdf` |
| Go in Action | `../hardisk/hdd/old_files/books/Go in Action.pdf` |
| Hacking Secret Ciphers with Python | `../hardisk/hdd/old_files/books/Hacking Secret Ciphers With Python By @TheCyberLeak.pdf` |
| Computer Organization and Design, RISC-V Ed (Patterson & Hennessy) | `../hardisk/pendrive-aug-26/summary/Book Materials/The.Morgan.Kaufmann.Series.in.Computer.Architecture.and.Design.David.A.Patterson.John.L.Hennessy.-.Computer.Organization.and.Design.RISC-V.Edition_.The.Hardware.Software.Interface-Morgan.Kaufmann.pdf` |
| Computer Architecture, 6th Ed, RISC-V | `../hardisk/pendrive-aug-26/summary/Book Materials/Computer_Architecture_6th_Edition_RISC_V.pdf` |
| Digital Design: A Systems Approach (Dally & Harting) | `../hardisk/pendrive-aug-26/summary/Book Materials/William J. Dally, R. Curtis Harting - Digital Design_ A Systems Approach-Cambridge University Press (2012).pdf` |
| The RISC-V Reader | `../hardisk/pendrive-aug-26/summary/Book Materials/David Patterson_ Andrew Waterman - The RISC-V Reader_ An Open Architecture Atlas-Strawberry Canyon LLC (2017).pdf` |
| Post-Quantum Cryptography Application Research Report 2023 | `../hardisk/pendrive-aug-26/summary/Post-Quantum_Cryptography_Application_Research_Report_2023_CAICT-2023.pdf` |
| GATE 2023 question paper PDF (docs/GATE2023) | `../hardisk/hdd/old_files/docs/GATE2023/C425K74questionPaper.pdf` |

### Not found on disk

- Data-structures/algorithms textbook (CLRS or similar), OS textbook (Silberschatz/Tanenbaum OS), DBMS textbook, discrete-mathematics textbook, Kurose & Ross, Bhunia & Tehranipoor, a threat-modeling book, an LLM/agent-security book.
- The reading list has 171 entries (books, course slides and notes) and, apart from Stallings (crypto) and Forouzan network-layer slides, **no** core-CS textbooks; GATE-side theory is covered only by the extra PDFs listed above and by your own notes.

