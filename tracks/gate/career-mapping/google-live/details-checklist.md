# Checklist from the job descriptions of Google's live security roles (169 roles, 19-20 Sep 2026)

Built by `details/build_checklist.py` from `details/roles/*.json` (sections counted: minimum qualifications, preferred qualifications, responsibilities; the About-the-job boilerplate is ignored because it names Google Cloud and customers in every posting).

## How to read this

- Denominator: **169 roles** that have a stored description (169 live roles have a link; 1 role has no id and was not fetched). Themes: security_engineering 57, threat_intel_and_response 41, sales_and_consulting 34, other_security 31, physical_corporate_security 6.
- **MANDATORY** = the item is in the *minimum qualifications* of at least 20% of roles (Google's minimum qualifications are its stated requirements). **COMMON** = in 5 or more roles in any section but below that bar. **ROLE-SPECIFIC** = in 1 to 4 roles (the roles are named).
- MANDATORY is measured against ALL roles, so role-family items (customer-facing, travel, language) can be mandatory overall because a fifth of roles are sales/consulting; check the 'Main themes' column. Google Cloud / GCP is left out as a technology: it is the employer's product name in almost every posting. AWS and Azure appear in no posting.
- Counts are roles, not mentions. It is keyword matching: a hit means the phrase is in the posting, not how deep the need is. Preferred qualifications are wishes, not requirements. This is a one-day snapshot of open roles, not a hiring trend.

## Skills and practices

### MANDATORY

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| Network security / protocols | 56 | 33.1% | 40 | 23 | 2 | security_engineering 24, threat_intel_and_response 14, sales_and_consulting 12 |
| Security engineering / secure design | 48 | 28.4% | 37 | 8 | 15 | security_engineering 27, sales_and_consulting 8, threat_intel_and_response 8 |

### COMMON

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| Automation / scripting | 67 | 39.6% | 16 | 34 | 33 | threat_intel_and_response 23, security_engineering 21, sales_and_consulting 16 |
| AI / machine learning | 64 | 37.9% | 17 | 51 | 43 | security_engineering 26, sales_and_consulting 13, other_security 13 |
| Cloud security | 52 | 30.8% | 9 | 34 | 23 | security_engineering 19, threat_intel_and_response 15, sales_and_consulting 13 |
| Detection engineering / SIEM / SOAR / SOC | 51 | 30.2% | 19 | 32 | 20 | sales_and_consulting 13, other_security 11, security_engineering 11 |
| Vulnerability research / management | 46 | 27.2% | 11 | 29 | 29 | security_engineering 23, other_security 8, threat_intel_and_response 8 |
| Security assessments / design reviews | 45 | 26.6% | 25 | 10 | 23 | security_engineering 30, threat_intel_and_response 9, sales_and_consulting 4 |
| Threat modeling / risk assessment | 45 | 26.6% | 25 | 18 | 21 | security_engineering 18, other_security 11, threat_intel_and_response 7 |
| Incident response | 43 | 25.4% | 21 | 20 | 16 | threat_intel_and_response 22, security_engineering 7, other_security 6 |
| Compliance / GRC / audit | 42 | 24.9% | 11 | 25 | 30 | other_security 13, sales_and_consulting 12, security_engineering 9 |
| Digital forensics / investigations | 42 | 24.9% | 17 | 31 | 27 | threat_intel_and_response 24, security_engineering 8, sales_and_consulting 5 |
| Data analysis / SQL / analytics | 36 | 21.3% | 17 | 15 | 12 | sales_and_consulting 11, security_engineering 9, other_security 8 |
| Penetration testing / red team / offensive | 35 | 20.7% | 15 | 27 | 19 | threat_intel_and_response 14, security_engineering 11, sales_and_consulting 6 |
| Identity and access management | 33 | 19.5% | 11 | 20 | 10 | security_engineering 20, sales_and_consulting 6, threat_intel_and_response 5 |
| Malware analysis / reverse engineering | 33 | 19.5% | 16 | 15 | 15 | threat_intel_and_response 23, security_engineering 6, sales_and_consulting 4 |
| Application security / secure code review | 31 | 18.3% | 15 | 16 | 13 | security_engineering 11, threat_intel_and_response 11, sales_and_consulting 5 |
| Threat intelligence | 30 | 17.8% | 6 | 10 | 22 | threat_intel_and_response 14, security_engineering 8, sales_and_consulting 4 |
| Privacy / data protection | 27 | 16.0% | 11 | 8 | 14 | security_engineering 11, other_security 7, threat_intel_and_response 6 |
| Cryptography | 17 | 10.1% | 3 | 14 | 1 | security_engineering 11, sales_and_consulting 4, threat_intel_and_response 2 |
| Trust and safety / abuse | 11 | 6.5% | 2 | 7 | 6 | security_engineering 4, threat_intel_and_response 3, sales_and_consulting 3 |

## Technology

### COMMON

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| Python | 47 | 27.8% | 26 | 20 | 2 | security_engineering 22, threat_intel_and_response 11, sales_and_consulting 10 |
| C++ / C/C++ | 35 | 20.7% | 25 | 10 | 0 | security_engineering 19, threat_intel_and_response 9, sales_and_consulting 5 |
| Go | 31 | 18.3% | 24 | 6 | 1 | security_engineering 20, sales_and_consulting 5, threat_intel_and_response 4 |
| Hardware / firmware / silicon | 29 | 17.2% | 11 | 14 | 18 | security_engineering 18, other_security 5, sales_and_consulting 3 |
| Android / iOS / mobile | 19 | 11.2% | 12 | 8 | 16 | threat_intel_and_response 13, security_engineering 5, other_security 1 |
| Java (not JavaScript) | 18 | 10.7% | 13 | 5 | 0 | security_engineering 11, sales_and_consulting 3, threat_intel_and_response 2 |
| Linux / Unix | 13 | 7.7% | 6 | 7 | 1 | threat_intel_and_response 5, sales_and_consulting 3, security_engineering 3 |
| SQL | 12 | 7.1% | 9 | 3 | 0 | other_security 4, security_engineering 4, sales_and_consulting 3 |
| Endpoint / EDR tools | 10 | 5.9% | 3 | 6 | 1 | threat_intel_and_response 7, other_security 1, sales_and_consulting 1 |
| JavaScript / TypeScript | 8 | 4.7% | 6 | 2 | 0 | security_engineering 6, threat_intel_and_response 1, sales_and_consulting 1 |
| Databases / big data | 7 | 4.1% | 3 | 2 | 3 | security_engineering 4, other_security 2, sales_and_consulting 1 |
| Kubernetes / containers | 7 | 4.1% | 2 | 5 | 2 | threat_intel_and_response 2, security_engineering 2, other_security 2 |
| Rust | 7 | 4.1% | 2 | 6 | 0 | threat_intel_and_response 4, security_engineering 2, other_security 1 |
| Windows / Active Directory | 5 | 3.0% | 0 | 5 | 0 | sales_and_consulting 3, threat_intel_and_response 1, security_engineering 1 |

### ROLE-SPECIFIC

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| Infrastructure as code / DevOps | 4 | 2.4% | 2 | 2 | 0 | security_engineering 3, other_security 1 |
| Chrome / browser | 3 | 1.8% | 1 | 1 | 2 | security_engineering 2, other_security 1 |
| SIEM products (Splunk, Chronicle, etc.) | 2 | 1.2% | 0 | 2 | 0 | sales_and_consulting 1, security_engineering 1 |
| Pentest / analysis tools (Burp, Metasploit, Ghidra, IDA, YARA) | 1 | 0.6% | 0 | 1 | 0 | threat_intel_and_response 1 |

- *Infrastructure as code / DevOps*: Staff Security Engineer, Cloud; Senior Security Engineer, AutoVM, Cloud Usage Taskforce; Group Product Manager, Agentic Code Security; Security Platform Engineer, Google Cloud Public Sector
- *Chrome / browser*: Software Engineer, Chrome Networking Security; Technical Program Manager, Product Security PMO; Security Engineering Intern, BS/MS, Summer 2027
- *SIEM products (Splunk, Chronicle, etc.)*: Security Consultant, SOAR, Mandiant, Google Cloud; Security Engineer, Google Cloud (Japanese, English)
- *Pentest / analysis tools (Burp, Metasploit, Ghidra, IDA, YARA)*: Security Engineer, Google Threat Intelligence

Not found in any role: AWS, Azure

## Certifications

### COMMON

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| Any 'certification' mentioned | 39 | 23.1% | 2 | 36 | 2 | threat_intel_and_response 22, sales_and_consulting 8, other_security 6 |
| GIAC / SANS (GCIH, GCIA, GCFA, GCFE, GPEN, GSEC...) | 17 | 10.1% | 1 | 16 | 0 | threat_intel_and_response 14, sales_and_consulting 2, other_security 1 |
| CCSP / cloud security certification | 16 | 9.5% | 1 | 15 | 0 | threat_intel_and_response 12, other_security 2, sales_and_consulting 2 |
| CISSP | 11 | 6.5% | 1 | 10 | 0 | threat_intel_and_response 4, sales_and_consulting 3, other_security 3 |
| OSCP / OSCE / OSEP / OSED / OSWE (Offensive Security) | 11 | 6.5% | 0 | 11 | 0 | threat_intel_and_response 9, security_engineering 1, other_security 1 |
| CISM / CISA / CRISC (ISACA) | 8 | 4.7% | 1 | 7 | 0 | threat_intel_and_response 4, other_security 2, sales_and_consulting 2 |

### ROLE-SPECIFIC

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| CompTIA Security+ / similar | 3 | 1.8% | 1 | 3 | 0 | sales_and_consulting 2, threat_intel_and_response 1 |
| CEH | 2 | 1.2% | 1 | 1 | 0 | threat_intel_and_response 1, sales_and_consulting 1 |
| Cisco (CCNA / CCNP) | 2 | 1.2% | 0 | 2 | 0 | sales_and_consulting 2 |
| PMP / project-management certification | 1 | 0.6% | 0 | 1 | 0 | other_security 1 |

- *CompTIA Security+ / similar*: Incident Response Engineer, UK Security Operations, Hampshire; Security Consultant, SOAR, Mandiant, Google Cloud; Security Engineering Technology Specialist
- *CEH*: Incident Response Engineer, UK Security Operations, Hampshire; Customer Engineer, Google Cloud Security
- *Cisco (CCNA / CCNP)*: Security Consultant, SOAR, Mandiant, Google Cloud; Security Engineering Technology Specialist
- *PMP / project-management certification*: Cyber Security Auditor, Internal Audit

## Experience, education and other requirements

### MANDATORY

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| Bachelor's degree or equivalent practical experience | 160 | 94.7% | 159 | 2 | 0 | security_engineering 54, threat_intel_and_response 40, sales_and_consulting 32 |
| Customer-facing / consulting / sales | 122 | 72.2% | 47 | 64 | 103 | security_engineering 34, sales_and_consulting 34, threat_intel_and_response 32 |
| Coding experience (general purpose languages) | 86 | 50.9% | 68 | 18 | 11 | security_engineering 50, threat_intel_and_response 18, sales_and_consulting 10 |
| Bachelor's in CS / security / technical field | 61 | 36.1% | 61 | 1 | 0 | threat_intel_and_response 23, other_security 15, security_engineering 13 |

### COMMON

| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |
|---|---|---|---|---|---|---|
| Cross-functional collaboration / stakeholders | 99 | 58.6% | 23 | 34 | 74 | security_engineering 29, sales_and_consulting 26, other_security 23 |
| Written and verbal communication / presenting | 96 | 56.8% | 28 | 70 | 58 | threat_intel_and_response 29, sales_and_consulting 28, other_security 21 |
| Language fluency (non-English + English) | 53 | 31.4% | 17 | 22 | 22 | sales_and_consulting 18, other_security 13, threat_intel_and_response 12 |
| Master's / PhD (preferred) | 53 | 31.4% | 6 | 47 | 0 | security_engineering 31, sales_and_consulting 10, other_security 6 |
| Leading teams / technical leadership | 47 | 27.8% | 25 | 18 | 9 | security_engineering 28, threat_intel_and_response 10, other_security 4 |
| Travel required | 33 | 19.5% | 23 | 2 | 10 | threat_intel_and_response 18, sales_and_consulting 9, security_engineering 4 |
| Program / project management | 32 | 18.9% | 18 | 16 | 3 | threat_intel_and_response 13, other_security 11, security_engineering 4 |
| Public sector / government | 21 | 12.4% | 5 | 12 | 12 | sales_and_consulting 7, other_security 6, threat_intel_and_response 4 |
| Data structures and algorithms | 20 | 11.8% | 4 | 16 | 0 | security_engineering 15, threat_intel_and_response 4, sales_and_consulting 1 |
| Security competitions / CTFs | 12 | 7.1% | 0 | 12 | 0 | threat_intel_and_response 12 |
| Security clearance | 11 | 6.5% | 11 | 2 | 0 | security_engineering 4, threat_intel_and_response 3, sales_and_consulting 2 |

## Years of experience (largest 'N years' in a role's minimum qualifications)

| Years | Roles |
|---|---|
| none stated | 4 |
| 1+ | 2 |
| 2+ | 19 |
| 3+ | 7 |
| 4+ | 1 |
| 5+ | 66 |
| 6+ | 7 |
| 7+ | 4 |
| 8+ | 33 |
| 10+ | 20 |
| 12+ | 1 |
| 15+ | 5 |

