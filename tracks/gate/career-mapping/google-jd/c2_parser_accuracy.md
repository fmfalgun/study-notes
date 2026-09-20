# Checkpoint 2 — parser accuracy: 8 parsed postings vs an independent extraction

Method: each archived page is parsed by `parse_job_detail` and, separately, run through the repo's generic
`scraper_core.extract.extract_main_text` (a different code path). Both texts are reduced to lowercase letters and digits.
Checks: (a) every parsed section appears inside the independent text; (b) the region from the first section start to the last
section end in the independent text is the same length as the parsed description (ratio ~1.00 = nothing dropped, nothing added);
(c) sections come in page order; (d) bullet counts match the HTML `<li>` counts.

| # | Description capture | Theme | Sections found | (a) all in independent text | (b) length ratio | (c) order | (d) bullets parsed / `<li>` | unknown headings |
|---|---|---|---|---|---|---|---|---|
| 1 | 20230703 | threat_intel_a | 4/4 | yes | 1.008 | yes | 12 / 12 | - |
| 2 | 20230801 | other_security | 4/4 | yes | 1.008 | yes | 15 / 15 | - |
| 3 | 20230828 | sales_and_cons | 4/4 | yes | 1.008 | yes | 15 / 15 | - |
| 4 | 20241003 | threat_intel_a | 4/4 | yes | 1.008 | yes | 12 / 12 | - |
| 5 | 20251129 | threat_intel_a | 4/4 | yes | 1.007 | yes | 13 / 13 | - |
| 6 | 20260102 | security_engin | 4/4 | yes | 1.006 | yes | 11 / 11 | - |
| 7 | 20260211 | sales_and_cons | 4/4 | yes | 1.010 | yes | 15 / 15 | - |
| 8 | 20260309 | other_security | 4/4 | yes | 1.006 | yes | 14 / 14 | - |

**Result: all 8 pass.**

## Side-by-side excerpts (start and end of each parsed description)

### 1. 20230703 — Security Engineer Cloud Detection

```
Minimum qualifications: | - Bachelor's degree or equivalent practical experience. | - 3 years of experience in cloud security research, network security, intrusion detection   ...  n large-scale security incidents. | - Work with teams from around Google to discover new detection capabilities and logging sources.
```

### 2. 20230801 — Cyber Defense Analyst Mandiant Google Cloud

```
Minimum qualifications: | - 3 years of experience in SOC analyst, malware research, threat hunting, or similar roles, working with EDR and SIEM technologies | - 3 years of ex  ...  age and collaborate with client stakeholders and other groups within customer environment to drive resolution for security issues.
```

### 3. 20230828 — Gotomarket Business Development Lead Security And Compliance

```
Minimum qualifications: | - Experience in collaborating across organizational boundaries, building relationships, and developing ideas to achieve organizational goals. | - Ex  ...  ate with the regional business leaders, the GCP cloud sellers, and the security specialists technical and promoting organizations.
```

### 4. 20241003 — Incident Response Security Consultant Mandiant Google Public

```
Minimum qualifications: | - 2 years of experience working end-to-end incident response investigations, analysis, or containment actions. | - 2 years of investigative experien  ...   external data sources. | - Investigate impact to customers to determine if new detection or compromise notifications are necessary.
```

### 5. 20251129 — Program Manager II Cyber Threat Intelligence Google Cloud

```
Minimum qualifications: | - Bachelor's degree or equivalent practical experience. | - 2 years of experience in program or project management. | - Experience with cyber threat i  ...  hreat actor naming conventions. | - Communicate schedules, priorities, and status to stakeholders and all levels within the company.
```

### 6. 20260102 — Security Engineer Technical Lead Identity

```
Minimum qualifications: | - Bachelor's degree or equivalent practical experience. | - 8 years of coding experience in one or more general purpose languages (e.g., Python, C,   ...  esign and policy decisions, drive and conclude information security risk discussions and escalations up to and including VP level.
```

### 7. 20260211 — Senior Strategic Cyber Security Operations Consultant Mandia

```
Minimum qualifications: | - Bachelor's degree in Computer Science, Information Systems, Cybersecurity, a related technical field, or equivalent practical experience. | - 5 ye  ...  s security posture. | - Advocate for cyber defense, articulate technical concepts to executive leadership and business stakeholders.
```

### 8. 20260309 — Senior Product Manager Security Google Distributed Cloud

```
Minimum qualifications: | - Bachelor's degree or equivalent practical experience. | - 5 years of experience in product management or related technical role. | - 2 years of expe  ...  ns. | - Partner with internal Google Cloud Security teams and external partners to integrate security tooling into the GDC platform.
```
