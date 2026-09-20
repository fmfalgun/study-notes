"""Build the skills / technology / certification / experience checklist from the stored live job descriptions.

Reads details/roles/*.json (one record per live role, sections parsed from the job page) and counts, per checklist item,
in how many ROLES it appears in each section. Every number has a denominator (the roles with a stored description).
Output: google-live/details-checklist.json and details-checklist.md.

Groups (thresholds are stated in the md):
  MANDATORY  = item is in the MINIMUM qualifications of >= 20% of roles (Google's minimum qualifications are the stated
               requirements; the 20% bar picks what is near-universal).
  COMMON     = item is in >= 5 roles in any section, but not mandatory.
  ROLE-SPECIFIC = item is in 1-4 roles; listed with which roles.
Caveat: keyword/phrase matching over text. A hit means the phrase is in the posting, not how deep the need is.
"""
import glob, json, re, collections
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
SECS = ("minimum_qualifications", "preferred_qualifications", "responsibilities")   # NOT "about": that is Google boilerplate ("Google Cloud", "customers")
I = re.I

LEX = {
 "Skills and practices": {
  "Security engineering / secure design": r"security engineering|secure design|security architecture|design(?:ing)? secure|security design",
  "Security assessments / design reviews": r"security (?:assessment|design review|review)s?|design reviews?|architecture reviews?",
  "Threat modeling / risk assessment": r"threat model\w*|risk assessments?|risk management",
  "Incident response": r"incident response|incident (?:handling|management)|\bdfir\b",
  "Digital forensics / investigations": r"forensic\w*|investigat\w+",
  "Malware analysis / reverse engineering": r"malware|reverse engineer\w*",
  "Penetration testing / red team / offensive": r"penetration test\w*|pen ?test\w*|red team\w*|offensive security|adversar\w+ (?:simulation|emulation)|exploit\w*",
  "Vulnerability research / management": r"vulnerabilit\w+|fuzzing|bug bount\w+",
  "Threat intelligence": r"threat intel\w*|cyber threat|threat actors?|apt\b",
  "Detection engineering / SIEM / SOAR / SOC": r"detection engineering|\bsiem\b|\bsoar\b|\bsoc\b|security operations|detection and response|threat detection",
  "Application security / secure code review": r"application security|appsec|secure code|code review|owasp|web application",
  "Cloud security": r"cloud security|cloud (?:infrastructure|platform)s?|cloud computing|cloud environments?",
  "Network security / protocols": r"network security|network protocols?|tcp/?ip|networking|firewall\w*|\bdns\b",
  "Identity and access management": r"identity and access|\biam\b|authentication|authorization|zero trust",
  "Cryptography": r"cryptograph\w+|encryption|\bpki\b|\btls\b",
  "Privacy / data protection": r"\bprivacy\b|data protection|\bgdpr\b",
  "Compliance / GRC / audit": r"compliance|governance|\bgrc\b|audit\w*|regulator\w+|iso ?27001|soc ?2|\bnist\b|fedramp|pci",
  "Trust and safety / abuse": r"trust and safety|abuse|fraud|anti-?malware|spam",
  "AI / machine learning": r"\bai\b|machine learning|\bml\b|\bllms?\b|large language model|generative|gemini|agentic",
  "Data analysis / SQL / analytics": r"data analy\w+|\bsql\b|analytics|data science|dashboards?",
  "Automation / scripting": r"automat\w+|scripting|\bscripts?\b",
 },
 "Technology": {
  "Python": r"\bpython\b",
  "Java (not JavaScript)": r"\bjava\b(?!script)",
  "C++ / C/C++": r"c\+\+|\bc/c\+\+",
  "Go": r"\bgolang\b|(?:python|java|c\+\+|rust|javascript|bash)[^.\n]{0,40}\bGo\b|\bGo\b[^.\n]{0,30}(?:python|java|c\+\+|rust)",
  "JavaScript / TypeScript": r"javascript|typescript",
  "Rust": r"\brust\b",
  "SQL": r"\bsql\b",
  "Linux / Unix": r"\blinux\b|\bunix\b",
  "Windows / Active Directory": r"windows|active directory",
  "Android / iOS / mobile": r"android|\bios\b|mobile",
  "Chrome / browser": r"chrome|browser",
  "Kubernetes / containers": r"kubernetes|\bk8s\b|docker|container\w*|\bgke\b",
  "Infrastructure as code / DevOps": r"terraform|infrastructure as code|ci/cd|devops",
  "AWS": r"\baws\b|amazon web services",
  "Azure": r"\bazure\b",
  "Endpoint / EDR tools": r"\bedr\b|endpoint (?:detection|security|protection)|crowdstrike|carbon black|sentinelone",
  "SIEM products (Splunk, Chronicle, etc.)": r"splunk|chronicle|qradar|sentinel\b|elastic",
  "Pentest / analysis tools (Burp, Metasploit, Ghidra, IDA, YARA)": r"burp|metasploit|nmap|ghidra|\bida\b|yara|wireshark|cobalt strike",
  "Hardware / firmware / silicon": r"firmware|hardware|silicon|\bsoc\b chip|bootloader|trusted execution|root of trust",
  "Databases / big data": r"bigquery|databases?|big data|spark",
 },
 "Certifications": {
  "CISSP": r"\bcissp\b",
  "CISM / CISA / CRISC (ISACA)": r"\bcism\b|\bcisa\b|\bcrisc\b",
  "CCSP / cloud security certification": r"\bccsp\b|cloud certification|certifications? in cloud",
  "OSCP / OSCE / OSEP / OSED / OSWE (Offensive Security)": r"\boscp\b|\bosce\b|\bosep\b|\bosed\b|\boswe\b|offensive security certif\w+",
  "GIAC / SANS (GCIH, GCIA, GCFA, GCFE, GPEN, GSEC...)": r"\bgiac\b|\bsans\b|\bgcih\b|\bgcia\b|\bgcfa\b|\bgcfe\b|\bgpen\b|\bgsec\b",
  "CEH": r"\bceh\b|certified ethical hacker",
  "CompTIA Security+ / similar": r"comptia|security\+",
  "Cisco (CCNA / CCNP)": r"\bccna\b|\bccnp\b|cisco cert\w+",
  "PMP / project-management certification": r"\bpmp\b",
  "Any 'certification' mentioned": r"certif\w+",
 },
 "Experience, education and other requirements": {
  "Bachelor's degree or equivalent practical experience": r"bachelor.s degree",
  "Bachelor's in CS / security / technical field": r"bachelor.s degree in (?:computer science|information|cyber|a technical|technical|engineering|a related)",
  "Master's / PhD (preferred)": r"master.s degree|\bphd\b|doctorate",
  "Leading teams / technical leadership": r"leading (?:a )?teams?|technical leadership|leadership role|people management|managing (?:a )?teams?|team lead\w*|managing people",
  "Program / project management": r"program management|project management|programs? manag\w+",
  "Cross-functional collaboration / stakeholders": r"cross-functional|cross-team|stakeholders?",
  "Written and verbal communication / presenting": r"communicat\w+|present\w+|executive",
  "Customer-facing / consulting / sales": r"customer|client|consult\w+|sales|pre-?sales|solution\w*|account",
  "Coding experience (general purpose languages)": r"coding|programming|software development|general.purpose (?:programming )?language",
  "Data structures and algorithms": r"data structures|algorithms",
  "Security competitions / CTFs": r"capture the flag|\bctfs?\b|security competitions?",
  "Travel required": r"travel",
  "Security clearance": r"clearance|ts/sci|top secret|\bsci\b",
  "Language fluency (non-English + English)": r"fluen\w+|bilingual|japanese|korean|hebrew|mandarin|thai|bahasa|arabic|german|french|spanish|portuguese",
  "Public sector / government": r"public sector|government|federal|national security|\bsled\b|defense",
 },
}


def load():
    roles = []
    for f in sorted(glob.glob(str(HERE / "roles" / "*.json"))):
        r = json.load(open(f))
        roles.append(r)
    return roles


def main():
    roles = load()
    n = len(roles)
    themes = collections.Counter(r["theme"] for r in roles)
    out = {"roles_with_description": n, "themes": dict(themes), "categories": {}}
    comp = {cat: {name: re.compile(p, I) for name, p in d.items()} for cat, d in LEX.items()}
    for cat, d in comp.items():
        items = []
        for name, rx in d.items():
            per = {s: 0 for s in SECS}
            hit = []
            for r in roles:
                any_hit = False
                for s in SECS:
                    if rx.search(r["sections"].get(s, "")):
                        per[s] += 1
                        any_hit = True
                if any_hit:
                    hit.append(r)
            n_any = len(hit)
            if n_any == 0:
                grp = "not seen"
            elif per["minimum_qualifications"] >= 0.20 * n:
                grp = "MANDATORY"
            elif n_any >= 5:
                grp = "COMMON"
            else:
                grp = "ROLE-SPECIFIC"
            th = collections.Counter(r["theme"] for r in hit)
            items.append({"item": name, "group": grp, "roles_any": n_any, "pct_any": round(100 * n_any / n, 1),
                          "in_minimum": per["minimum_qualifications"], "in_preferred": per["preferred_qualifications"],
                          "in_responsibilities": per["responsibilities"],
                          "themes": dict(th.most_common()),
                          "example_roles": [r["title"] for r in hit[:4]] if grp == "ROLE-SPECIFIC" else []})
        out["categories"][cat] = sorted(items, key=lambda x: (-x["in_minimum"], -x["roles_any"]))
    # years of experience required (largest "N years" in minimum qualifications, per role)
    yrs = collections.Counter()
    for r in roles:
        vals = [int(m) for m in re.findall(r"(\d+)\+?\s+years?", r["sections"].get("minimum_qualifications", ""), I)]
        yrs[max(vals) if vals else 0] += 1
    out["max_years_in_minimum_qualifications"] = {str(k): v for k, v in sorted(yrs.items())}
    (OUT / "details-checklist.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))

    L = [f"# Checklist from the job descriptions of Google's live security roles ({n} roles, 19-20 Sep 2026)", "",
         "Built by `details/build_checklist.py` from `details/roles/*.json` (sections counted: minimum qualifications, preferred qualifications, responsibilities; the About-the-job boilerplate is ignored because it names Google Cloud and customers in every posting).", "",
         "## How to read this", "",
         f"- Denominator: **{n} roles** that have a stored description (169 live roles have a link; 1 role has no id and was not fetched). Themes: " + ", ".join(f"{k} {v}" for k, v in themes.most_common()) + ".",
         "- **MANDATORY** = the item is in the *minimum qualifications* of at least 20% of roles (Google's minimum qualifications are its stated requirements). **COMMON** = in 5 or more roles in any section but below that bar. **ROLE-SPECIFIC** = in 1 to 4 roles (the roles are named).",
         "- MANDATORY is measured against ALL roles, so role-family items (customer-facing, travel, language) can be mandatory overall because a fifth of roles are sales/consulting; check the 'Main themes' column. Google Cloud / GCP is left out as a technology: it is the employer's product name in almost every posting. AWS and Azure appear in no posting.",
         "- Counts are roles, not mentions. It is keyword matching: a hit means the phrase is in the posting, not how deep the need is. Preferred qualifications are wishes, not requirements. This is a one-day snapshot of open roles, not a hiring trend.", ""]
    for cat, items in out["categories"].items():
        L += [f"## {cat}", ""]
        for grp in ("MANDATORY", "COMMON", "ROLE-SPECIFIC"):
            rows = [x for x in items if x["group"] == grp]
            if not rows:
                continue
            L += [f"### {grp}", "", "| Item | Roles (any) | % of roles | In minimum | In preferred | In responsibilities | Main themes |", "|---|---|---|---|---|---|---|"]
            for x in sorted(rows, key=lambda x: (-x["roles_any"], x["item"])):
                th = ", ".join(f"{k} {v}" for k, v in list(x["themes"].items())[:3])
                L.append(f"| {x['item']} | {x['roles_any']} | {x['pct_any']}% | {x['in_minimum']} | {x['in_preferred']} | {x['in_responsibilities']} | {th} |")
            if grp == "ROLE-SPECIFIC":
                L += [""] + [f"- *{x['item']}*: " + "; ".join(x["example_roles"]) for x in rows if x["example_roles"]]
            L.append("")
        nots = [x["item"] for x in items if x["group"] == "not seen"]
        if nots:
            L += ["Not found in any role: " + ", ".join(nots), ""]
    L += ["## Years of experience (largest 'N years' in a role's minimum qualifications)", "", "| Years | Roles |", "|---|---|"]
    for k, v in sorted(yrs.items()):
        L.append(f"| {'none stated' if k == 0 else str(k) + '+'} | {v} |")
    L.append("")
    (OUT / "details-checklist.md").write_text("\n".join(L) + "\n")
    print("roles", n, "wrote md/json")


if __name__ == "__main__":
    main()
