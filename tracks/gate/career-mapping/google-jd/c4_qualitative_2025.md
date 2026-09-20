# C4 qualitative notes, 2025 description-capture year (15 postings read in full, seed 2025, listed in c4_sample_2025.txt)

Scope: postings are only those Wayback archived. 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023. These notes read 15 of the 194 postings captured in 2025 (security_engineering 4, threat_intel_and_response 4, sales_and_consulting 3, other_security 2, physical_corporate_security 2). A sample of 15 illustrates; it proves no share. Quotes are verbatim, at most 25 words, each with (job_id, theme).

## What the role asks for that the term counts miss

**1. Some "security" postings are a generic template with a security topic.** The software-engineer template ("2 years of experience with software development ...", "data structures or algorithms") appears under security titles, so counts such as software development or code review measure the template, not a security skill.
- Incident-response-titled engineer (116557511640654534): the work is an internal tool. > "Work with executive engineers and Program Managers/UX to design, implement, and land functionality related to incident response focused on the Postmortem process." (116557511640654534, threat_intel_and_response)
- Its responsibilities also read as a general full-stack role: "Be responsible for all parts of the application- the front-end, back-end, and data processing pipelines." (116557511640654534, threat_intel_and_response)
- Open-source security (131896388727251654): the security content is in the artifact-signing work. "Develop tools and services to sign and verify software artifacts." (131896388727251654, security_engineering)

**2. The theme label comes from title keywords and is sometimes off.** One sampled posting labelled security_engineering is an AI/ML customer-engineering role whose "security" is the customer segment (national security): "Be a trusted technical advisor to customers and solve Machine Learning tests." (74534317350363846, security_engineering). It counts in the security_engineering cell. Treat theme cells as title-derived groups, not verified job families (1 clear case in 15 read; cannot be extrapolated).

**3. Gating requirements that are not skills (clearance, vetting, language, travel).** Counts of "clearance" show frequency but not the effect: they restrict who can apply by nationality and location.
- "US Government Top Secret/Sensitive Compartmentalized Information security clearance with polygraph." (101807747569197766, sales_and_consulting)
- "United Kingdom Security Vetting Developed Vetting (DV) clearance." (86120617354371782, threat_intel_and_response)
- "Ability to travel up to 30% of the time internationally." (101807747569197766, sales_and_consulting)
- Language as a hard requirement: "Ability to communicate in English and French fluently to engage with local stakeholders." (89199600757285574, physical_corporate_security)

**4. Consulting and sales roles are advisory: delivery, customer-facing, and on-site.** The counts show client/customer/cloud; the text shows the job is running a client's security operations or training their staff.
- "Provide consultation and support for deployment and operations of Google SecOps in client environments." (130800037121663686, sales_and_consulting)
- Threat-intel consulting is partly teaching: "Deliver engaging training sessions to security analysts, engineers, and other team members on threat intelligence concepts, methodologies, and tools." (82888232148050630, threat_intel_and_response)
- A leadership sales posting is about quota and market, not security depth: "Experience in leadership within a quota-carrying team, such as people management, team lead, mentorship or coaching." (103872267078771398, sales_and_consulting)

**5. Certifications appear as named lists in the preferred section.** One consulting posting names vendors and exam families: "Certification in one or more of the following: CompTIA Security+; CompTIA Network+; ISC2 (CISSP)" (130800037121663686, sales_and_consulting). An incident-response posting makes a certification a MINIMUM: "Certification in Certified Ethical Hacker (CEH), Global Information Assurance Certification (GIAC) or Computing Technology Industry Association Security (CompTIA Sec+)." (86120617354371782, threat_intel_and_response). The term counts show that certifications are mostly preferred; one posting can still require it.

**6. Offensive/defensive work is described by activity, at fine grain.** The silicon security posting lists the tasks: "Conduct offensive security (red teaming) activities including vulnerability discovery, exploit development, mitigation recommendations." (75352161466098374, security_engineering). Its preferred list moves the same skills into research techniques: "Experience in reverse engineering, static analysis or dynamic analysis (Fuzzing) or exploit development." (75352161466098374, security_engineering). Threat-response postings describe operational duty: "Respond to security incidents escalated from the front line 24/7 team." (86120617354371782, threat_intel_and_response). Malware analysis appears as scale plus management: "Perform reverse engineering, analyse and detect malware at scale." (105528902872376006, threat_intel_and_response) and "Manage a team of security engineers (malware analysts) in Bengaluru." (105528902872376006, threat_intel_and_response).

**7. Non-cyber and adjacent security postings look different in kind.**
- other_security, enterprise operations: "Apply security judgment to approve/deny/escalate requests based on risk and policy alignment." (82939729745453766, other_security). This is a review-and-approve role, closer to governance than engineering.
- other_security, SAP application security: compliance and audit vocabulary, not attack/defence: "Understanding of Sarbanes-Oxley (SOX) and other compliance requirements that may impact SAP Security." (120817915254448838, other_security).
- physical_corporate_security (NOT cybersecurity; n=11 in the year, weak): vendor and guard-force management. "Experience working with vendors, suppliers and managing a contracted guard team." (98215481499886278, physical_corporate_security) and "Experience with security technologies, including CCTV, access control, incident management systems, and security operations centers." (89199600757285574, physical_corporate_security). The shared word "security operations" appears in both physical and cyber postings; a term count would merge them if themes were not separated.

**8. An internship posting shows entry-level phrasing.** "Develop scripts to automate routine tasks." (107132933369668294, security_engineering) and "Currently pursuing a Bachelor's or Master's degree in Computer Science, Information Security, or related technical field." (107132933369668294, security_engineering). Interns are inside the security_engineering counts.

## Caveats on this reading
15 of 194 postings, chosen by a fixed random seed inside theme quotas; the same fixed seed regenerates the sample. Observations are illustrations of mechanisms the counts hide; they are not frequencies. Causes (why Google words a requirement a certain way) are not observable here.
