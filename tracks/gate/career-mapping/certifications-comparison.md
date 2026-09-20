# Certification comparison: GIAC/SANS, OffSec, CISSP, CCSP

Written 20 Sep 2026. Prices and rules were looked up on the web the same day (sources at the bottom); items marked
**(knowledge)** come from general knowledge and were **not** re-checked today. Google's demand comes from our own data
(`google-live/details-checklist.md`, 169 live security roles). INR figures use a rough ₹85 per US dollar; exchange rates
and India-specific prices move, so treat rupee amounts as estimates.

## 1. At a glance

| | **GIAC / SANS** | **OffSec (OSCP family)** | **CISSP (ISC2)** | **CCSP (ISC2)** |
|---|---|---|---|---|
| What it is | 30+ single-topic certifications, each usually tied to a SANS course | Hands-on practical exams; flagship OSCP (PEN-200), plus OSWE, OSEP, OSED, OSEE **(knowledge)** | Broad security management and architecture, 8 domains | Cloud security, 6 domains |
| Field | Defense, incident response, forensics, pentest, cloud, management (e.g. GSEC, GCIH, GCIA, GCFA, GPEN, GXPN) **(knowledge)** | Offensive: pentest, web exploitation, evasion, exploit development | Governance, risk, architecture, IAM, operations, secure software | Cloud architecture, data, platform, application, operations, legal/risk/compliance |
| Style | Multiple choice, **open book** | **No multiple choice.** 23 h 45 min hacking exam, then 24 h to write the report | Adaptive test, 125-175 questions, up to 4 h | Adaptive test since 1 Oct 2025, 100-150 questions |
| Prerequisite | None | None formal (PEN-200 skills assumed) | 5 years' paid experience in 2+ of the 8 domains, 1 year waived with a degree or approved cert; or pass and become an **Associate of ISC2** **(knowledge)** | 5 years in IT, 3 in security, 1 in a CCSP domain; **an active CISSP replaces all of it** |
| Exam price | ~$999 standalone (one source says $949); retake $879 | Included in the course plans below; retake $249 | $749 | $599 |
| Training price | SANS course ~$8,780-8,900 (one 2026 SEC504 listing: $8,900) | Learn One $2,749 per year (one course, 1 year of labs, 2 exam attempts); Course+Cert bundle $1,749 (90 days, 1 attempt) | Self-study books or a bootcamp (not priced here) | Self-study or a course (not priced here) |
| Lasts | 4 years; renew with 36 CPE plus about $469-499, or retake | OSCP never expires; **OSCP+** expires after 3 years, renewed by a recert exam within 6 months, another OffSec exam, or OffSec's CPE program | 3-year cycle: 120 CPE (at least 90 directly relevant, at least 15 a year) plus **$135 a year** | Same $135 a year; **one fee covers all your ISC2 certs** |
| Recognized for | Technical depth; strong in incident response and forensics | Proof you can actually attack; the practical standard for pentest/red team | HR filters, management and senior roles, government/defense requirements | Cloud-security roles; DoD-approved |

In rupees (approx.): CISSP exam ₹64,000 and ₹11,500 a year after; CCSP exam ₹51,000; OSCP Learn One ₹2.3 lakh, bundle ₹1.5 lakh; GIAC exam ₹85,000; SANS course plus exam about ₹8.4 lakh (an Indian source quotes ₹5-7 lakh for the course through a partner).

## 2. What Google's job descriptions say (our data, 169 roles)

| Certification family | Roles mentioning it | As a minimum | As preferred | Which role types |
|---|---|---|---|---|
| GIAC / SANS | 18 | 1 | 17 | threat and response 14, sales/consulting 2 |
| OffSec (OSCP, OSCE, OSEP, OSED, OSEE) | 11 | **0** | 11 | threat and response 9 |
| CISSP | 11 | 1 | 10 | threat and response 4, other 3, sales/consulting 3, physical 1 |
| CCSP | 3 | 1 | 2 | other 2, sales/consulting 1 |
| Any 'certification' wording | 39 | 2 | 36 | threat and response 22 of 39 |

- Certifications are **almost never required**: only 2 of 169 roles list one in the minimum qualifications. Coding (68 roles) and security-engineering experience are the requirements.
- They cluster in **incident-response and red-team roles, mostly Mandiant consulting**. Typical wording: "Certifications related to offensive security including OSCE, OSEP, OSEE, OSCP, CISSP, CISA or relevant SANS courses."
- **CCSP is nearly absent** (3 roles). Cloud security is asked for as knowledge ("certifications in cloud platforms", 13 roles), not as CCSP specifically.
- A title-only or role-count view cannot show whether a certification changes an interview outcome. This is what job descriptions ask for, not what gets hired.

## 3. Cost of ownership (first 4 years, exam plus upkeep only, no study materials)

| | Up-front | Upkeep over 4 years | Total (USD) | Total (approx. INR) |
|---|---|---|---|---|
| CISSP | $749 | 4 x $135 = $540 | **$1,289** | ₹1.1 lakh |
| CCSP | $599 | 4 x $135 = $540 (shared if you also hold CISSP) | **$1,139** (or **$599** extra with CISSP) | ₹97,000 (₹51,000 extra) |
| OSCP (bundle) | $1,749 | none for OSCP; OSCP+ needs renewal after 3 years | **$1,749** | ₹1.5 lakh |
| OSCP (Learn One) | $2,749 | none for OSCP | **$2,749** | ₹2.3 lakh |
| GIAC via SANS course | ~$8,900 course + $999 exam (approx.) | renewal about $499 at year 4 | **about $10,400** | ₹8.8 lakh |
| GIAC exam only | $999 | renewal about $499 at year 4 | **about $1,500** | ₹1.3 lakh |

A failed exam adds: OSCP $249, GIAC $879. The GIAC exam alone is far cheaper than the course, but the exams are built around the SANS course books (open book), so skipping the course raises the difficulty considerably **(knowledge)**.

## 4. ROI: what the pay claims say, and how far to trust them

Salary figures below are from web salary guides and training-vendor blogs (linked at the bottom). Vendors sell these courses, and holders of a certification also tend to be more experienced, so **a higher salary among holders does not prove the certification caused it.**

| | US claims | India claims | Simple payback if the claim held |
|---|---|---|---|
| CISSP | median about $164K, a $25K-35K premium | ₹6-8 lakh under 5 years' experience, ₹15-20 lakh at 5-10 years | Cost is small ($749); the barrier is the 5-year experience rule |
| CCSP | $140K-170K | not found | Only worthwhile on a cloud-security career path |
| OSCP | $120K-160K, consultants above $200K | adds about ₹3-5 lakh a year; ₹18-35 lakh at red-team-friendly product companies | Bundle ₹1.5 lakh -> about 4-6 months; Learn One ₹2.3 lakh -> about 6-9 months |
| GIAC | $76K-219K (very wide) | not found | ₹8.4 lakh course cost makes sense mostly when an **employer pays** |

Read the payback column as arithmetic on an optimistic claim, not a forecast.

## 5. Which one fits what

- **OSCP:** the cheapest hands-on proof, no experience prerequisite, and the only one of the four you cannot pass by memorizing. Best fit for pentest, red team and vulnerability roles. Of Google's 11 OffSec mentions, 9 are in threat-and-response (Mandiant) roles.
- **GIAC/SANS:** the strongest for incident response and forensics (14 of Google's 18 mentions are in threat-and-response). The price only makes sense with an employer or a scholarship; pick the certification matching one job function (GCIH, GCIA, GCFA, GPEN and similar).
- **CISSP:** broad and management-flavoured. Useful for HR filters and senior/government roles; it needs 5 years' experience for the full credential, so a fresher can only become an Associate. Not a Google-specific requirement (1 minimum in 169 roles).
- **CCSP:** only if you are heading into cloud security. It is cheap if you already hold the CISSP (the experience rule is waived and the yearly fee is shared). A **new CCSP exam outline takes effect on 1 Aug 2026**, so check that study material matches it.

## 6. Recommendation for your case (technical profile, GATE 2027, targeting Google security roles)

1. For Google security-engineering roles the data says **spend the effort on coding and data structures first**, not certifications (2 of 169 roles require one).
2. If you add one certification, **OSCP** (bundle first, about ₹1.5 lakh) is the best value and fits the threat/red-team roles where certifications are actually named.
3. Defer **CISSP** until you have the years of experience (or take the Associate route); add **CCSP** only if you go cloud-security.
4. **GIAC/SANS** only if an employer sponsors it.

## Sources

- ISC2 CCSP page: https://www.isc2.org/certifications/ccsp (domains, 5-year rule, accreditation). CISSP and CCSP prices, $135 fee, CPE and CAT format come from the web-search summaries of destcert.com, stormwindstudios.com, certiguard.io and destcert.com/resources/ccsp-exam-update (secondary sources, not ISC2's own pages, which returned 404 to our fetch).
- OffSec pricing page: https://www.offsec.com/pricing/ (Learn One $2,749, bundle $1,749, CyberCore $899, Aspire discount). Retake $249, OSCP+ validity and renewal: offsec.com/courses/pen-200 and certiguard.io/certifications/offsec-oscp (secondary).
- GIAC pricing: https://www.giac.org/pricing and https://www.giac.org/renewal (search summary; $949-999 exam, $879 retake, $469-499 renewal, 36 CPE). SANS SEC504 price: sans.org event listing summary (about $8,900).
- Salary claims: stationx.net/cissp-salary, certselect.com, deepstrike.io, knowledgehut.com/blog/security/cissp-salary-india, networkershome.com (vendor and salary-guide sites).
