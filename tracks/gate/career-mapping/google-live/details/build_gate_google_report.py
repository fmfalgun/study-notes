"""Builds ../../gate-vs-google-security-topics.md: GATE topics vs Google's live security-job requirements vs cybersecurity.md,
mapped to the books in courses/READING_LIST.md (paths verified to exist) and other PDFs found on disk."""
import json, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "gate-vs-google-security-topics.md"
LIST = Path("../no-github-remote/courses/READING_LIST.md")
FIX = ("../hardisk/", "../hardisk/")   # READING_LIST.md paths miss the /Projects segment
OLD = "../hardisk/hdd/old_files/books/"

rows, sec = [], None
for line in LIST.read_text().splitlines():
    m = re.match(r"## (\d+)\. (.+)", line)
    if m:
        sec = m.group(1); continue
    m = re.match(r"\| (\d)/10 \| (.+?) \| `(.+?)`", line)
    if m and sec:
        rows.append({"sec": sec, "score": int(m.group(1)), "title": m.group(2), "path": m.group(3).replace(*FIX)})
assert all(os.path.exists(r["path"]) for r in rows), "a listed book path is missing"

def _n(t):
    return t.replace("\u2014", "-").replace("\u2013", "-").replace("\u2019", "'").lower()


def B(sub):
    hits = [r for r in rows if _n(sub) in _n(r["title"])]
    assert hits, sub
    return hits[0]

OUTSIDE = {   # not in READING_LIST.md, found on disk
 "Tanenbaum - Computer Networks": OLD + "Andrew S. Tanenbaum - Computer Networks.pdf",
 "CCNA 200-301 Official Cert Guide Vol 1 (Cisco Press)": OLD + "12381imguf_CiscoPress-CCNA-200-301-Official-Cert-Guide-Volume-1.pdf",
 "CCNA 200-301 Vol 2": OLD + "ccna-200-301-vol.-2.pdf",
 "Hacking: The Art of Exploitation, 2nd Ed": OLD + "Hacking - The Art of Exploitation_2nd Ed.pdf",
 "Rootkits: Subverting the Windows Kernel": OLD + "Rootkits - Subverting the Windows Kernel.pdf",
 "Hands-On System Programming with Linux": OLD + "Hands-On System Programming With Linux Explore Linux System Programming Interfaces, Theory, And Practice ( PDFDrive.com ).pdf",
 "C++ Primer": OLD + "CPPPrimer.pdf",
 "A Complete Guide to Standard C++ Algorithms": OLD + "a_complete_guide_to_standard_cpp_algorithms_v1_0_1.pdf",
 "Black Hat Python": OLD + "Black Hat Python_ Python Programming for Hackers and Pentesters ( PDFDrive.com ).pdf",
 "Black Hat Go": OLD + "Black_Hat_Go.pdf",
 "Gray Hat Python": OLD + "Gray_Hat_Python_Python_Programming.pdf",
 "Go in Action": OLD + "Go in Action.pdf",
 "Hacking Secret Ciphers with Python": OLD + "Hacking Secret Ciphers With Python By @TheCyberLeak.pdf",
 "Computer Organization and Design, RISC-V Ed (Patterson & Hennessy)": "../hardisk/pendrive-aug-26/summary/Book Materials/The.Morgan.Kaufmann.Series.in.Computer.Architecture.and.Design.David.A.Patterson.John.L.Hennessy.-.Computer.Organization.and.Design.RISC-V.Edition_.The.Hardware.Software.Interface-Morgan.Kaufmann.pdf",
 "Computer Architecture, 6th Ed, RISC-V": "../hardisk/pendrive-aug-26/summary/Book Materials/Computer_Architecture_6th_Edition_RISC_V.pdf",
 "Digital Design: A Systems Approach (Dally & Harting)": "../hardisk/pendrive-aug-26/summary/Book Materials/William J. Dally, R. Curtis Harting - Digital Design_ A Systems Approach-Cambridge University Press (2012).pdf",
 "The RISC-V Reader": "../hardisk/pendrive-aug-26/summary/Book Materials/David Patterson_ Andrew Waterman - The RISC-V Reader_ An Open Architecture Atlas-Strawberry Canyon LLC (2017).pdf",
 "Post-Quantum Cryptography Application Research Report 2023": "../hardisk/pendrive-aug-26/summary/Post-Quantum_Cryptography_Application_Research_Report_2023_CAICT-2023.pdf",
 "GATE 2023 question paper PDF (docs/GATE2023)": "../hardisk/hdd/old_files/docs/GATE2023/C425K74questionPaper.pdf",
}
for p in OUTSIDE.values():
    assert os.path.exists(p), p

TOPICS = [
 # (name, gate line, google evidence, list titles, outside titles, gap note)
 ("1. Computer networks and network security",
  "Computer Networks - Tier 2, score 14.8 (`exam-priority-report.md`)",
  "56 of 169 roles mention networking/protocols/network security; 40 as a MINIMUM (mostly the standard bullet 'experience with security engineering, computer and network security and security protocols'). Literal 'TCP/IP', 'DNS', 'TLS' appear in 0 descriptions.",
  ["Attacking Network Protocols", "Nmap Network Exploration", "Applied Network Security Monitoring", "Network Security Through Data Analysis", "Cisco Press - Penetration Testing and Network Defense", "Network Layer", "Wireshark Top Filters", "SILENCE ON THE WIRE"],
  ["Tanenbaum - Computer Networks", "CCNA 200-301 Official Cert Guide Vol 1 (Cisco Press)", "CCNA 200-301 Vol 2"],
  "Covers GATE's layered model (Tanenbaum, CCNA) plus the attacker/defender view. No Kurose & Ross on disk."),
 ("2. Discrete maths, number theory and cryptography",
  "Discrete Mathematics - Tier 1, score 30.6 (13 complex-question hits)",
  "Cryptography/encryption/PKI/TLS in 18 roles, but only 3 as a minimum (14 as preferred). Not a universal requirement; a specialist one.",
  ["Cryptography and Network Security - Principles and Practice", "Elementary Cryptanalysis", "Cryptography (31 pg)", "Cryptography and Network Security 5/e"],
  ["Hacking Secret Ciphers with Python", "Post-Quantum Cryptography Application Research Report 2023"],
  "Stallings is the book `cybersecurity.md` named for RSA/DH; the 9/10 entry in the list is a lecture-notes PDF (`1 introduction new.pdf`); the full book is the 7th Global Ed entry. No discrete-maths textbook PDF on disk."),
 ("3. Operating systems, Linux and memory-level security",
  "Operating System - Tier 2, score 13.4",
  "OS/kernel/Linux/virtualization in 21 roles (8 minimum); C/C++/Rust/memory-corruption in 37 (25 minimum); reverse engineering/assembly/exploitation in 29 (4 minimum).",
  ["Operating System Security", "Linux Essentials for Cybersecurity", "Penetration Testing with the Bash Shell", "Buffer Overflow Attacks", "Shellcoder", "Reverse Engineering for Beginners", "Rootkits and Bootkits", "Gray Hat Hacking"],
  ["Hacking: The Art of Exploitation, 2nd Ed", "Rootkits: Subverting the Windows Kernel", "Hands-On System Programming with Linux"],
  "No OS textbook (Silberschatz / Tanenbaum OS) on disk: process scheduling, deadlock, paging theory that GATE tests must come from your notes or GFG pages."),
 ("4. Programming, data structures and algorithms (the coding round)",
  "Programming & Data Structures - Tier 1, score 51.6 (highest of all GATE topics); Algorithms - Tier 2, score 10.9",
  "'Coding experience in a general-purpose language' is a MINIMUM in 68 of 169 roles (the most common technical minimum). Python in 47 roles (26 minimum), C++ in 35 (25), Go in 31 (24). Data structures / algorithms named in 20 roles (4 minimum, 16 preferred).",
  ["Coding for Penetration Testers", "Python Penetration Testing Essentials", "Learning Python Web Penetration Testing"],
  ["C++ Primer", "A Complete Guide to Standard C++ Algorithms", "Black Hat Python", "Black Hat Go", "Gray Hat Python", "Go in Action"],
  "**Biggest gap.** GATE's #1 topic and Google's #1 minimum requirement have no data-structures or algorithms textbook on disk. `cybersecurity.md` section 3 did not list this overlap at all. Your own markdown notes exist (`Documents/learning-docs/data_structures_complete.md`, `algorithms_masterclass.md`, `Projects/DSA/`) but they are not PDFs."),
 ("5. Computer organization, digital logic and hardware/platform security",
  "Digital Logic - Tier 2, score 15.0; Computer Organization - Tier 2, score 14.9",
  "Hardware/firmware/secure-boot/TPM/silicon in 29 roles (11 minimum).",
  ["A Practical Guide to TPM 2.0", "Hardware IP Security and Trust", "The Hardware Hacker", "Hacking The Xbox", "Security and Privacy in Internet of Things"],
  ["Computer Organization and Design, RISC-V Ed (Patterson & Hennessy)", "Computer Architecture, 6th Ed, RISC-V", "Digital Design: A Systems Approach (Dally & Harting)", "The RISC-V Reader"],
  "Good coverage: Patterson & Hennessy and Dally for the GATE side, the TPM and hardware-security books for the security side. Bhunia & Tehranipoor (named in `cybersecurity.md`) is NOT on disk."),
 ("6. Databases and SQL security",
  "Databases (DBMS) - Tier 2, score 16.8",
  "SQL/databases in 17 roles (10 minimum).",
  ["SQL Injection", "Securing SQL Server", "Database Forensics", "The Web Application Hacker's Handbook, 2nd Ed"],
  [],
  "Only the security angle is covered; no DBMS textbook (normalization, transactions, indexing) on disk."),
 ("7. Compilers, program analysis and reverse engineering",
  "Compiler Design - Tier 2, score 10.9",
  "Compilers/static analysis/fuzzing in 7 roles (1 minimum); reverse engineering/assembly/exploitation in 29 (see topic 3).",
  ["Reverse Engineering for Beginners", "Malware Analyst's Cookbook", "Hacking Exposed Malware", "Malware Analysis and Detection Engineering"],
  [],
  "Weak overlap. Worth it only for malware / vulnerability-research roles."),
 ("8. Theory of computation",
  "Theory of Computation - Tier 3, score 7.8",
  "Regex/parsing/automata in 1 role.",
  [], [], "Not a Google security requirement in the data. Study it for GATE only."),
]

NON_GATE = [
 ("Threat modeling and secure design", "54 roles (27 minimum)", [], "No threat-modeling book on disk (closest: Cybersecurity - Attack and Defense Strategies)", ["Cybersecurity - Attack and Defense Strategies"]),
 ("Incident response and detection", "IR 40 roles, detection/SIEM/SOC 51", ["Intelligence-Driven Incident Response", "Computer Incident Response and Forensics Team Management", "Malware Analysis and Detection Engineering", "Mastering Splunk"], "", []),
 ("Digital forensics", "23 roles (15 minimum)", ["File System Forensic Analysis", "Computer Forensics - Investigating Hard Disks", "Handbook of Digital Forensics and Investigation"], "", []),
 ("Web and application security", "application security / secure code review 31 roles", ["The Web Application Hacker's Handbook, 2nd Ed", "Mastering Modern Web Penetration Testing", "The Browser Hacker's Handbook", "Real-World Bug Hunting"], "", []),
 ("Threat intelligence / OSINT", "25 roles", ["Collaborative Cyber Threat Intelligence", "Practical Cyber Intelligence", "Open Source Intelligence Methods and Tools"], "", []),
 ("AI / ML and AI-security", "AI/ML in 64 roles (17 minimum)", ["Mastering Machine Learning for Penetration Testing", "Malware Data Science"], "Nothing on LLM/agent security on disk", []),
 ("Offensive security and certifications (OSCP/GIAC/CISSP as preferred)", "pentest/red team 35 roles; OSCP-family 11, GIAC 17, CISSP 11 (all mostly preferred)", ["Penetration Testing - A Hands-on Intro", "The Hacker Playbook 2", "Metasploit - The Penetration Tester's Guide", "CEH v13", "SANS SEC542 - Web App Penetration Testing, Day 2"], "", []),
]

def fmt(r):
    return f"{r['title']} ({r['score']}/10)"

L = ["# GATE topics vs Google's security-role requirements vs the books we have", "",
 "Compares three things: (1) the GATE topic map and priority tiers (`../topics/gfg-gate-topic-map.md`, `../exam-priority-report.md`); "
 "(2) the job descriptions of **Google's 169 live security roles** (`google-live/details-checklist.md`, 19-20 Sep 2026); "
 "(3) the earlier `cybersecurity.md` (its section 2 stack and section 3 GATE overlap). Books come from `Projects/no-github-remote/courses/READING_LIST.md` plus other PDFs found on disk. Built by `google-live/details/build_gate_google_report.py`.", "",
 "## Read this first", "",
 "- **Job descriptions are not interview questions.** They show what Google *requires or prefers*, not what an interview asks. Whatever is said about interviews below is general knowledge, not from our data.",
 "- Counts are roles out of 169 that mention the topic in minimum, preferred or responsibilities text; 'minimum' = in the stated minimum qualifications. Keyword matching, one-day snapshot.",
 "- GATE has **no Cyber Security section** (`gfg-gate-topic-map.md`, 'Not covered'). The overlap is foundational, through the sections below.",
 "- **Path fix:** `READING_LIST.md` prints paths starting `../hardisk/...`; the real location is `../hardisk/...`. All 171 listed PDFs exist at the corrected path. The list itself was not edited.", "",
 "## 1. GATE topics that Google's security roles also require (ranked by evidence)", ""]
for name, gate, ev, lst, out, gap in TOPICS:
    L += [f"### {name}", "", f"- **GATE:** {gate}", f"- **Google roles:** {ev}"]
    if lst:
        L.append("- **Books from the reading list:** " + "; ".join(fmt(B(s)) for s in lst))
    if out:
        L.append("- **Other PDFs on disk:** " + "; ".join(out))
    L += [f"- **Note:** {gap}", ""]

L += ["## 2. What Google requires that GATE does not test", "",
      "| Topic | Google roles | Books from the reading list | Gap |", "|---|---|---|---|"]
for name, ev, lst, gap, more in NON_GATE:
    titles = [fmt(B(s)) for s in lst + more]
    L.append(f"| {name} | {ev} | {'; '.join(titles) if titles else '-'} | {gap or '-'} |")
L.append("")

L += ["## 3. Comparison with `cybersecurity.md`", "",
 "**Confirmed by Google's descriptions:** Python, C/C++ and Rust (35 and 7 roles) as languages; threat modeling (33), incident response (40), forensics (23), penetration-testing methodology (18); hardware/firmware/TPM/secure boot (11 for the narrow TPM/UEFI terms); the four GATE overlaps in section 3 (networks, discrete maths/crypto, OS, digital logic/COA).", "",
 "**Missing from `cybersecurity.md` section 3, but strong in Google's data:** **Programming and data structures** (GATE Tier 1; coding is the most common technical minimum, 68 roles) and, weakly, **databases/SQL** (17 roles).", "",
 "**In `cybersecurity.md` but NOT supported by Google's descriptions** (the earlier list came from other companies' postings): AWS and Azure (0 roles), Nmap, Burp, Metasploit, LDAP, PKI, CVE/NVD (0 each), Splunk (2), Elastic (0), QRadar (1), CrowdStrike/SentinelOne/Defender (3), MISP/VirusTotal (0). Google's descriptions name few commercial tools; they name skills. Certifications are almost all *preferred* (any certification: 39 roles, 36 as preferred).", "",
 "**New since `cybersecurity.md`:** AI/ML appears in 64 roles (17 as a minimum); SOAR in 7; NIST in 7, ISO 27001 in 5, SOC 2 in 4.", ""]

L += ["## 4. Final list: cybersecurity topics common to GATE and Google, with the PDFs we have", "",
 "Ordered by combined weight: GATE tier/score first, Google minimum-requirement count second.", "",
 "| # | Topic | GATE | Google roles (minimum) | PDFs on disk |", "|---|---|---|---|---|",
 "| 1 | Programming, DS and algorithms, in Python/C++/Go | Tier 1 (51.6) + Algorithms 10.9 | 68 coding, 47 Python (26), 35 C++ (25), 31 Go (24) | C++ Primer, Std C++ Algorithms, Black Hat Python, Black Hat Go, Gray Hat Python, Go in Action, Coding for Penetration Testers. **No DS/algorithms textbook** |",
 "| 2 | Computer networks and network security | Tier 2 (14.8) | 56 (40) | Tanenbaum, CCNA vols 1-2, Attacking Network Protocols, Nmap Cookbook, Applied NSM |",
 "| 3 | Cryptography (from discrete maths / number theory) | Tier 1 (30.6) | 18 (3) | Stallings 7th Ed, Elementary Cryptanalysis, Hacking Secret Ciphers, PQC report |",
 "| 4 | OS internals, Linux, memory safety, exploitation basics | Tier 2 (13.4) | 21 (8); C/C++/memory 37 (25); RE/exploit 29 (4) | Jaeger OS Security, Art of Exploitation, Shellcoder's, Linux Essentials, Bash pentest, System Programming with Linux. **No OS textbook** |",
 "| 5 | Computer organization / digital logic -> hardware & platform security | Tier 2 (14.9, 15.0) | 29 (11) | Patterson & Hennessy (RISC-V), Dally Digital Design, Computer Architecture 6th Ed, TPM 2.0 guide, Hardware Hacker |",
 "| 6 | Databases / SQL security | Tier 2 (16.8) | 17 (10) | SQL Injection notes, Securing SQL Server, WAHH 2nd Ed. **No DBMS textbook** |",
 "| 7 | Compilers -> program analysis / reverse engineering | Tier 2 (10.9) | 7 (1) / 29 (4) | Reverse Engineering for Beginners, Malware Analyst's Cookbook, Rootkits and Bootkits |",
 "", "**Interview note (general knowledge, not from our data):** security-engineer interviews at large companies are commonly described as a coding round (data structures and algorithms), a networking/OS/systems round, and a security-design or threat-modeling round. Topics 1, 2, 4 and the threat-modeling row of section 2 match that pattern; topics 5 to 7 are role-specific.", "",
 "## 5. Appendix: paths", "", "### From the reading list (corrected prefix)", "", "| Book | Score | Section | Path |", "|---|---|---|---|"]
seen = set()
used = []
for name, gate, ev, lst, out, gap in TOPICS:
    used += lst
for name, ev, lst, gap, more in NON_GATE:
    used += lst + more
for s in used:
    r = B(s)
    if r["path"] in seen: continue
    seen.add(r["path"])
    L.append(f"| {r['title']} | {r['score']}/10 | {r['sec']} | `{r['path']}` |")
L += ["", "### Not in the reading list, found on disk", "", "| Book | Path |", "|---|---|"]
for t, p in OUTSIDE.items():
    L.append(f"| {t} | `{p}` |")
L += ["", "### Not found on disk", "", "- Data-structures/algorithms textbook (CLRS or similar), OS textbook (Silberschatz/Tanenbaum OS), DBMS textbook, discrete-mathematics textbook, Kurose & Ross, Bhunia & Tehranipoor, a threat-modeling book, an LLM/agent-security book.", "- The reading list has 171 entries (books, course slides and notes) and, apart from Stallings (crypto) and Forouzan network-layer slides, **no** core-CS textbooks; GATE-side theory is covered only by the extra PDFs listed above and by your own notes.", ""]
OUT.write_text("\n".join(L) + "\n")
print("wrote", OUT, len(L), "lines; listed books used:", len(seen))
