# Google cybersecurity roles, 2018–2026: what changed and what stayed

Companion to `cybersecurity.md`. Built from Wayback Machine's archive of Google's
individual job-posting pages: **18,188 distinct postings** (URL = job ID + title slug,
capture date = it was live then), of which **883 are security-tagged** by title.

Files this is based on (all in this folder unless noted):

| File | What it holds |
|---|---|
| `google-wayback-security-roles-by-year.md` | Every security-tagged posting, by year and theme (690 distinct titles) |
| `google-wayback-job-trends.json` | Same data, machine-readable, with first/last month each posting was seen |
| `google-wayback-summary.md` | How the earlier front-page snapshots were downloaded, and their true coverage |
| `scraper-data/google-careers-job-urls.cdx.json` | The raw URL list (36,847 rows) — nothing needs re-fetching |

## What this data can and cannot tell you — read before the numbers

- **Not "every Google job."** It is every posting Wayback happened to archive. A posting
  nobody loaded through Wayback is invisible.
- **Counts are not comparable across years; shares are.** Postings archived per year swing
  from 269 (2019) to 6,824 (2025) purely with Wayback's crawl activity. So every figure below
  is a *share* of that year's observed postings, with the denominator shown. Shares cancel crawl
  intensity to a first approximation — not perfectly.
- **Small years are noisy.** 2019 has 8 security postings and 2020 has 16; a percentage there
  moves a lot per posting. 2026 is a partial year (through Sept).
- **Titles, not skills.** Titles come from URL slugs. They show *which kinds of role* existed,
  not which skills the job required. Claims about skills need job descriptions (see "Next step").
- **Classification is a keyword heuristic** on the title (security, cyber, threat, incident
  response, vulnerability, malware, forensics, cryptography…). A threat-team role titled just
  "Engineering Analyst" is missed; "Global Security Operations" physical-security roles are
  caught but separated into their own theme.
- **Causes below (acquisitions, rebrands) are inference**, not something the data proves.

## Security share of observed postings, by year

| Year | Observed postings | Security-tagged | Share |
|---|---|---|---|
| 2019 | 269 | 8 | 3.0% |
| 2020 | 572 | 16 | 2.8% |
| 2021 | 2,326 | 74 | 3.2% |
| 2022 | 4,276 | 202 | 4.7% |
| 2023 | 2,371 | 142 | 6.0% |
| 2024 | 2,469 | 142 | 5.8% |
| 2025 | 6,824 | 322 | 4.7% |
| 2026 (to Sep) | 1,925 | 118 | 6.1% |

Security roughly doubled its share of visible postings between 2019–2021 (~3%) and 2023–2026
(~5–6%), and has been broadly steady since 2023. (2018 had one posting in the data; ignored.)

## What kinds of security role — share of each year's security postings

| Role family (a title can match several) | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| n (security postings) | 8 | 16 | 74 | 202 | 142 | 142 | 322 | 118 |
| Cloud | 0% | 19% | 18% | 30% | 44% | 39% | 33% | 31% |
| Sales / consulting (go-to-market) | 0% | 12% | 7% | 13% | 22% | 27% | 26% | 27% |
| Mandiant | 0% | 0% | 0% | 0% | 8% | 24% | 18% | 18% |
| Threat / detection / response | 38% | 31% | 16% | 14% | 17% | 20% | 26% | 16% |
| Offensive / vulnerability | 0% | 0% | 7% | 4% | 2% | 5% | 6% | 7% |
| Privacy (word in title) | 25% | 19% | 11% | 10% | 11% | 6% | 5% | 3% |
| Chrome / Android / Pixel | 0% | 12% | 16% | 12% | 6% | 1% | 5% | 8% |
| Hardware / silicon / firmware | 0% | 0% | 1% | 0% | 1% | 4% | 2% | 1% |
| Governance / risk / compliance | 0% | 6% | 14% | 8% | 4% | 1% | 5% | 5% |
| AI in the title | 0% | 0% | 0% | 0% | 0% | 0% | 6% | 4% |
| Management (manager/director/head/lead) | 0% | 25% | 36% | 32% | 20% | 25% | 24% | 21% |

## What changed

1. **Security moved into Google Cloud.** Cloud-titled security roles went from ~0–18%
   (2019–2021) to 30–44% (2022 on). The most common title stems are Cloud-team ones
   ("Software Engineer, … Google Cloud Security and Privacy", "Customer Engineer, Security,
   Google Cloud").
2. **Go-to-market security roles became a quarter of the total.** Sales specialists, customer
   engineers and consultants: 0–12% in 2019–2021, then 22–27% from 2023. "Security Sales
   Specialist" is a repeated title. Newly seen since 2024: "consulting" (12 uses) and
   language-specific consultant roles (e.g. Arabic, 5 uses).
3. **Mandiant appears in 2023 and stays.** 0% until 2022, 8% in 2023, 24% in 2024, ~18% after
   — titles like "Incident Response Security Consultant, Mandiant" and "Red Team Security
   Consultant, Mandiant". This fits Google's acquisition of Mandiant (inference).
4. **A product name disappears.** "Chronicle" (5 uses before, none since 2023) — consistent
   with that product being folded into Google Cloud's branding (inference).
5. **Explicit "privacy" in security titles fell** from 25%→3% (2019→2026). Part of that is
   naming: in 2022–23 "Security and Privacy" was a Cloud team name that appears in many titles.
6. **New vocabulary since 2024** (used ≥3 times in 2024–26 titles, never 2019–2023):
   cryptography and quantum ("post-quantum" roles), supply chain, kubernetes / virtualization /
   distributed systems, hardware, federated, "agent", DeepMind.
7. **AI enters security titles only in 2025** (6%, then 4% in 2026), against a wider Google-wide
   AI share that rose from ~4% (2019–2023) to 12% (2024), 10% (2025), 15% (2026).
8. **Physical/corporate security exists throughout but is small** (Data Center Security Manager,
   Campus Security Manager: ~1–7 postings a year). It is tagged separately so it does not
   inflate the cybersecurity numbers. "Resilience" (Global Security & Resiliency Services)
   titles disappear after 2023.

## What stayed consistent (in demand every year)

- **Threat, detection and response** roles are present in every year (16–38% of security
  postings; higher in the early small years). Titles: "Security Engineer, Detection and
  Response", "Incident Response Security Consultant".
- **Core security engineering** — "Security Engineer" (most common stem overall, 12 postings),
  "Information Security Engineer" (9), "Software Engineer, Security/Privacy".
- **Management layer**: 20–36% of security postings every year since 2020.
- **Offensive / vulnerability** work (red team, penetration, vulnerability) exists steadily but
  small: 2–7% every year since 2021.

## Google roles beyond the earlier report

The earlier report had **1** Google cybersecurity title. The archive shows **690 distinct
security-tagged titles** across 883 postings (see `google-wayback-security-roles-by-year.md`).
Representative, one per family: Security Engineer, Detection and Response · Staff Software
Engineer, Virtual Machine Threat Detection · Information Security Engineer, Offensive Security,
Red Team · Cloud Security Architect · Manager, Red Team Security Consultant, Mandiant · Cyber Threat
Intelligence Analyst · Senior Software Engineer, Chrome Product Security · Security Sales
Specialist, Google Cloud · Data Center Security Manager (physical).

## Cross-check against the earlier front-page sample

The first analysis used only ~20 listings per monthly snapshot (79 of 84 snapshots parseable).
It suggested security was "roughly flat at 1–6%"; the wider data says it **rose from ~3% to
~5–6%**. The wider data is the one to trust: it is ~200× larger and not limited to
relevance-sorted first pages.

## Next step (not done)

Titles cannot show *skills*. To say which skills stayed in demand, we need job descriptions.
Options: the live crawler (running now, see `google-live/`) covers currently-active roles;
descriptions for them would need one extra page load per role — deliberately not requested yet
because you asked for a slow, gentle crawl.
