# 3. SIEM — Notes

## Splunk free official training (splunk.com)

**Claim** (fetched via `curl` with a browser User-Agent — WebFetch blocked this domain too, same
pattern as several Tor Project subdomains earlier): this is a course catalog, not training
content itself — it lists dozens of free self-paced eLearning modules grouped into 3 tracks:
**Splunk Enterprise/Cloud platform basics** (Intro to Splunk, Using Fields, Intro to Dashboards,
Search Under the Hood/architecture, Knowledge Objects, installation/config, SPL2 — the newer
search language generation), **Security** (Intro to Enterprise Security, Splunk SOAR — Security
Orchestration and Automated Response, Splunk UBA — User Behavior Analytics, Splunk Security
Essentials use cases/analytic stories), and **Observability** (not detailed in the fetch, implied
by nav structure). The core skill the whole catalog builds toward is **SPL (Search Processing
Language)** — Splunk's query language for searching/transforming ingested log/event data — with
progressively deeper modules (basic search -> fields/eval -> stats/transforming commands ->
data models -> dashboards/visualizations -> SPL2).

**Simple explanation**: This page itself teaches nothing directly — it's a menu. The throughline
across nearly every listed course is "learn to ask Splunk questions about your data" (SPL), which
is the one universal skill a SOC analyst needs regardless of which specific Splunk module they
end up using day to day.

**Try it**: No live Splunk instance is required or used here (per this repo's no-cloud-SIEM-
accounts rule) — instead, practice the *underlying skill* SPL courses teach (structured querying
of log data: filter, extract fields, aggregate) using this machine's own real local logs via
`journalctl`, which maps conceptually onto Splunk's `search` / `stats` / `where` SPL commands.
```fish
# SPL concept: `index=... | search ...` (filter to a source + criteria)
# journalctl equivalent: filter to systemd journal, priority=error, last 5 entries
journalctl -p err --no-pager -n 5

# SPL concept: `... | stats count by <field>` (aggregate/group)
# journalctl equivalent: count log lines per systemd unit over the last hour
journalctl --no-pager --since "1 hour ago" -o json 2>/dev/null | python3 -c "
import sys, json, collections
c = collections.Counter()
for line in sys.stdin:
    try:
        d = json.loads(line)
        c[d.get('_SYSTEMD_UNIT', d.get('SYSLOG_IDENTIFIER', 'unknown'))] += 1
    except Exception:
        pass
for k, v in c.most_common(10):
    print(v, k)
"
```
bash/sh: identical (journalctl/python3 syntax doesn't depend on shell).
Applied exercise: write the equivalent SPL query (as text, no Splunk instance needed) for each
journalctl command above — e.g. `index=main log_level=error | head 5` and
`index=main earliest=-1h | stats count by unit | sort - count | head 10` — to practice mapping
SPL syntax onto a query you already understand conceptually.

## Hands-on SOC practice path (TryHackMe SOC Level 1)

**Claim** (direct fetch attempts blocked: WebFetch refused the domain outright, and a `curl`
retry hit TryHackMe's Vercel bot-protection JS checkpoint page instead of real content — per the
"skip after one retry, note for manual re-check" instruction, this entry is built from a `WebSearch`
of independent sources describing the same official page, not the page itself; **flagged here for
a manual re-check against the live page** if precise wording/order matters later): TryHackMe's
SOC Level 1 path was rebuilt into 10 progressive modules covering, per multiple independent
write-ups: SOC Fundamentals (what a SOC does, the Junior Analyst role, how attacks/detection work
at a high level), SOC Team Internals (alert-triage workflow, report writing, SOC-effectiveness
metrics, escalation communication), Security Solutions (SIEM, EDR, SOAR — the three core tool
categories a SOC analyst operates), Alert Handling (triage/classify/escalate a security alert,
documentation), and Phishing Analysis (hands-on analysis of email headers and malicious
attachments), plus additional modules not confirmed by this pass's sources. The throughline across
all confirmed modules: this path is built around the actual daily workflow of a Tier-1 SOC
analyst (triage an alert -> investigate -> document -> escalate or close), not abstract theory.

**Simple explanation**: Where the Splunk catalog (previous link) teaches the *tool* (SPL/Splunk
product features), this path teaches the *job* — the repeatable loop of "an alert fires, what do
you actually do, in what order, and how do you communicate it" that a Tier-1 analyst performs
dozens of times a shift, using SIEM/EDR/SOAR as the toolset without requiring a specific vendor.

**Try it**: TryHackMe rooms require a live paid/free account and hosted VM infrastructure — out of
scope per this repo's no-live-SIEM-account rule. The available offline substitute is practicing
the *alert-triage workflow itself* on locally available real data, using this machine's own auth
log as a stand-in "alert source."
```fish
# stand-in "alert triage": find sudo/auth events in the last 2 hours (a realistic Tier-1 SOC
# starting point — "here's an auth event, investigate it"); verified working without a -u filter
# (journalctl's systemd-unit matching doesn't apply to sudo's syslog-style logging)
journalctl SYSLOG_IDENTIFIER=sudo --no-pager --since "2 hours ago" | grep -i "password is required\|incorrect password\|authentication failure"
```
bash/sh: identical.
Applied exercise: for any matches found, write a mini incident note following the triage workflow
named above — What fired (event)? Who/what (user, PWD, command)? When? Initial severity
assessment (benign/suspicious/needs escalation)? One sentence justifying the assessment.

## SOC analyst tools & skills roadmap (Networkers Home)

**Claim** (fetched via `curl` + tag-stripping; note this is a training-company marketing page
with real substantive content embedded — captured for its factual content, not its sales framing):
gives a concrete year-by-year skill progression for a SOC career. Year 0-1 (L1): SPL fluency,
**specific named Windows Security event IDs** (4624 logon success, 4625 logon failure, 4634
logoff, 4740 account lockout, 4720 account created, 4732 added to security-enabled group, 7045
service installed, 7036 service start/stop), Linux `journalctl`+`auditd`, MITRE ATT&CK (14
tactics, top 30 techniques), one EDR platform, network/Wireshark basics. Year 1-2: Sigma rule
writing + Git workflow, NIST IR lifecycle, hypothesis-driven threat hunting, Python for log
parsing. Year 2-3 (L2): cloud security specialty, SOAR playbooks, threat-intel platforms (MISP,
OTX, ThreatConnect). Year 3-5+ (L3/senior): detection-engineering portfolio, architecture
decisions, AI/ML-assisted SIEM features, specialization tracks (Detection Engineer, Threat Intel
Lead, Cloud Security Specialist). It also gives a SIEM platform comparison by claimed
Bangalore-market hiring share: Splunk ~70% of JDs (mature/expensive), Microsoft Sentinel ~30%
(cloud-native, KQL), Elastic/ELK ~15% (open-source, more ops burden), QRadar ~10% (legacy/BFSI,
declining). Free self-study resources it names: Splunk free tier, TryHackMe SOC Level 1 (already
covered, link 2), Blue Team Labs Online and CyberDefenders (both covered later in this section),
LetsDefend, MITRE ATT&CK Navigator, SigmaHQ GitHub (both covered later in this section), SANS
Reading Room, The DFIR Report.

**Simple explanation**: This is effectively a job-market-driven syllabus — "here's what actually
gets checked for at each career stage, based on real job postings," rather than an abstract skills
list. Its most concretely useful artifact for this study set is the named Windows event ID list
and the SIEM market-share comparison, both directly checkable facts rather than opinion.

**Try it**: The Windows event IDs listed are Windows-specific and not directly reproducible on
this Linux machine — but the roadmap's own Linux-side equivalent (`journalctl` + `auditd`) is
installed here, so demonstrate that half directly, and map the two systems' concepts.
```fish
# journalctl half already demonstrated in links 1-2 of this section — this adds auditd:
which auditctl ausearch aureport   # confirm the tools are installed (they are, on this machine)
systemctl is-active auditd          # confirm current state (inactive here — no service enabled)

# (Optional, root) real audit log query — requires the service active + root read access:
sudo ausearch -ts today | head -20
```
bash/sh: identical.
Applied exercise: build a 2-column mapping table pairing each named Windows event ID (4624, 4625,
4634, 4740, 4720, 4732, 7045, 7036) with its closest Linux/journalctl or auditd equivalent concept
(e.g. 4624/4625 logon success/failure <-> `journalctl SYSLOG_IDENTIFIER=sudo` / `sshd` auth lines
or `auditd`'s `USER_LOGIN`/`USER_AUTH` records).

## MITRE ATT&CK framework (core reference, attack.mitre.org)

**Claim** (fetched via `curl` + tag-stripping — WebFetch blocked this domain too): ATT&CK is a
knowledge base of adversary behavior organized as **Tactics** (the *why* — an adversary's
short-term goal, e.g. "Persistence" or "Credential Access") each containing multiple
**Techniques** (the *how* — a specific method to achieve that tactic, e.g. "Phishing" under
Initial Access), many of which further break into **Sub-techniques** (a specific variant, e.g.
Phishing's 4 sub-techniques: Spearphishing Service/Attachment/Link/Voice). Confirmed directly from
the live Enterprise matrix fetch: there are exactly **14 tactics** — Reconnaissance, Resource
Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion
(labeled "Stealth Defense Impairment" in this fetch's rendering), Credential Access, Discovery,
Lateral Movement, Collection, Command and Control, Exfiltration, Impact — with technique counts
per tactic ranging from 9 (Reconnaissance, Resource Development, Collection, Exfiltration) up to
34 (Discovery). It ships as 3 separate matrices for different environments: **Enterprise**
(traditional IT), **Mobile**, and **ICS** (industrial control systems) — each has its own tactic
list tuned to that domain. The stated purpose is to be a common, real-world-observation-grounded
vocabulary that both attackers' actual behavior and defenders' detections/mitigations can be
mapped to — the earlier roadmap link's "MITRE ATT&CK, top 30 techniques" and section 4/5 of this
study set (offensive concepts, defense evasion) both hang directly off this taxonomy.

**Simple explanation**: Tactic answers "what is the attacker trying to accomplish right now"
(a goal); technique answers "specifically how are they doing it" (a method); sub-technique adds
"which specific variant of that method." ATT&CK's real value for a SOC is giving everyone —
vendors, analysts, red teamers — the same names for the same behaviors, so a detection rule, an
incident report, and a threat intel report can all reference "T1566.002 (Spearphishing Link)" and
mean the exact same thing.

**Try it**: Pull real technique data directly from the live matrix (already done above) and
practice technique-ID lookups, without needing a local install of the ATT&CK Navigator tool.
```fish
curl -sL -A "Mozilla/5.0" https://attack.mitre.org/ -o /tmp/mitre.html
python3 -c "
import re, html
text = open('/tmp/mitre.html').read()
text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = html.unescape(text)
text = re.sub(r'\s+', ' ', text)
idx = text.find('Reconnaissance Resource Development')
print(text[idx:idx+400])
"
rm /tmp/mitre.html
```
bash/sh: identical.
Applied exercise: from the printed tactic list + technique counts, pick the tactic with the most
techniques (Discovery, 34) and the fewest (tied at 9: Reconnaissance/Resource
Development/Collection/Exfiltration), and write one sentence hypothesizing *why* Discovery would
naturally have so many more distinct techniques than Exfiltration (hint: think about how many
different things an attacker might want to enumerate on a compromised host/network vs. how many
fundamentally different ways there are to get data out).

## MITRE ATT&CK complete guide (Splunk blog)

**Claim** (fetched via `curl` + tag-stripping): adds history and practical usage on top of link 4's
structural facts. History: ATT&CK began in 2013 as MITRE's internal "FMX" research project to
improve post-compromise detection via endpoint telemetry, initially focused on Windows enterprise
APT activity; it was released publicly in May 2015. The article names 3 specific gaps in
pre-ATT&CK detection practice that motivated it: indicator-based detection (IPs, file hashes,
registry keys) only captures a single point in time and breaks the moment an attacker changes
infrastructure; higher-level lifecycle models like the Cyber Kill Chain or Diamond Model are too
abstract to map directly onto specific defensive analytics; and there was no shared taxonomy, so
different teams/vendors described the same behavior differently. On practical use, it lays out a
concrete detection-engineering workflow (directly setting up section 5's Detection-as-Code and
Atomic Red Team links): centralize relevant telemetry into a SIEM -> translate a chosen ATT&CK
technique into an actual query (often starting from existing ATT&CK-aligned analytics in a
repository like MITRE's own Cyber Analytics Repository, CAR) -> for deeper coverage, deliberately
execute the technique in a controlled lab using Atomic Red Team to see exactly what artifacts it
produces -> build detection logic from those real artifacts -> validate by having a red team try
to bypass it, then iterate. For threat intelligence use, ATT&CK gives a common vocabulary to
describe a specific threat group's TTPs (e.g. "this group persists via a specific registry run
key") in a way that's directly actionable for a defender, rather than staying at the abstract
level of "this group targets your industry."

**Simple explanation**: ATT&CK exists because older detection approaches broke too easily
(indicators go stale) or were too vague to act on (kill-chain stages). Its real workflow value is
a repeatable loop: pick a technique -> actually reproduce it safely in a lab -> see what it
actually leaves behind in logs -> write a detection for exactly that -> try to break your own
detection -> repeat. This loop, not just the taxonomy itself, is what "using ATT&CK" means
day-to-day for a detection engineer.

**Try it**: Trace the detection-engineering workflow described above using a real, already-covered
concept — MITRE ATT&CK's Defense Evasion tactic (TA0005, covered directly in section 4 of this
study set) — to practice translating "a technique" into "a real local artifact" without executing
any actual attack technique (per this repo's safety boundary: explain/detect, never attack).
```fish
# stand-in for step 1 of the workflow ("centralize relevant telemetry") — confirm this machine's
# local telemetry sources that a real SIEM pipeline would ingest
journalctl --no-pager -n 3
which auditctl   # auditd, already confirmed installed in link 3, is exactly this kind of source
```
bash/sh: identical.
Applied exercise (no live attack execution): pick one specific, well-documented ATT&CK technique
(e.g. T1055 Process Injection, or T1548.002 Bypass User Account Control) and, using only its
public ATT&CK page description (not running it), write out: what log source/telemetry would need
to be collected to detect it, and what specific field/event pattern in that telemetry a detection
rule would look for. This rehearses the "artifact -> detection logic" step of the workflow purely
through documentation research.

## MITRE ATT&CK guide for SOC/DFIR (CyberDefenders blog)

**Claim** (fetched via `curl` + tag-stripping): this is the most SOC-analyst-concrete of the 3
ATT&CK links in this study set — it maps specific technique IDs directly to specific alert text,
log sources, and even a sample SPL query, rather than staying at the framework level. Confirms
the Enterprise matrix has "over 200 techniques" across its 14 tactics (consistent with link 4's
directly-counted totals). Its stated value-adds for a SOC beyond "shared vocabulary": (1)
**detection-coverage-gap analysis** — tag detection rules with ATT&CK IDs, then see e.g. "50
detections exist for T1059 (Command and Scripting Interpreter) but zero for T1574 (Hijack
Execution Flow)" as a literal, measurable coverage gap; (2) **precise IR reporting** — write
"the threat actor leveraged T1021.002 (SMB/Windows Admin Shares)" instead of the vague "the
attacker moved laterally," which is reproducible/unambiguous to a second analyst; (3) **purple
team alignment** — red team operates by technique ID, blue team validates detections against the
same IDs, so results are directly comparable. Real worked examples given per tactic: **Initial
Access (TA0001)** — alert "repeated failed auth then success from IP 185.220.X.X" maps to T1078
Valid Accounts, with a literal sample SPL detection query provided (reproduced in Try It below).
**Execution (TA0002)** — Windows Event ID 4688 showing `cmd.exe` spawning `powershell.exe` with
an encoded command is the canonical artifact. **Persistence (TA0003)** — registry Run keys,
scheduled tasks, WMI event subscriptions, new out-of-window services. **Privilege Escalation
(TA0004)** — SeDebugPrivilege enablement, PsExec/Mimikatz indicators, low-priv process spawning
elevated children. **Lateral Movement (TA0008)** — same account authenticating to multiple hosts
in quick succession (T1021.001 RDP, T1021.002 SMB, T1047 WMI). It also details 5 specific
frequently-seen techniques with their concrete log sources: T1059 (PowerShell/Sysmon Event 1 and
4104, encoded-command indicators), T1003 OS Credential Dumping (LSASS/SAM/NTDS artifacts,
`comsvcs.dll` abuse — the classic Mimikatz-adjacent technique), T1021 Remote Services, T1036
Masquerading (a fake `svchost.exe` running from `C:\Users\Public` — wrong path is the tell), and
T1053 Scheduled Task persistence (`schtasks.exe`, common in cryptomining persistence).

**Simple explanation**: This page is "ATT&CK, but shown as actual SOC console alerts" rather than
an abstract taxonomy — for each tactic it gives the literal thing you'd see light up in a SIEM and
the specific technique ID that maps to it, which is exactly the translation step a working analyst
does dozens of times a shift.

**Try it**: Adapt the article's own sample SPL detection query for T1078 (repeated auth failure
then success — a brute-force-then-success pattern) into the journalctl-based SPL-practice pattern
already used earlier in this section (link 1), applied to this machine's real sudo auth log.
```fish
# article's SPL: index=authentication action=failure src_ip=* user=* | stats count by user, src_ip
#   | where count > 5 | join user [search index=authentication action=success]
# journalctl equivalent: count sudo "password is required" prompts per user in the last 2 hours
journalctl SYSLOG_IDENTIFIER=sudo --no-pager --since "2 hours ago" | awk -F'sudo\\[[0-9]+\\]:\\s+' '{print $2}' | awk '{print $1}' | sort | uniq -c | sort -rn
```
bash/sh: identical (this system's `grep` is a `ugrep` wrapper that rejects unbounded-length
lookbehind, so `awk` field-splitting was used instead — verified working on this machine).
Applied exercise: run it, and write one sentence on what a "count > 5" threshold (from the
article's query) would mean applied to this output — is 5+ prompts from the known interactive
user in 2 hours actually suspicious on this single-user dev machine, or expected noise? Contrast
with what the same pattern would mean on a multi-user production server.

## Writing/reading Sigma detection rules (SigmaHQ/sigma on GitHub)

**Claim**: Sigma is a vendor-agnostic, YAML-based detection-rule format — the repo's own framing
is the clearest one-liner: "Sigma is for log files what Snort is for network traffic and YARA is
for files." The point is writing a detection *once* in a generic form, then converting it to
whatever query language a specific SIEM actually speaks (SPL for Splunk, KQL for Sentinel/Elastic,
AQL for QRadar, etc.) via a backend converter — `sigma-cli` (official), `pySigma` (library for
custom toolchains), or hosted web converters. This directly closes the loop with the previous two
links: link 5/6's detection-engineering workflow ("translate an ATT&CK technique into an actual
query") is precisely what a Sigma rule *is* — a technique/behavior expressed as a portable,
reviewable, version-controllable YAML detection instead of a vendor-locked query. The repo hosts
3,000+ peer-reviewed rules across 5 categories: Generic (threat-agnostic behavioral detections),
Threat Hunting (broader investigative starting points, not necessarily alert-worthy alone),
Emerging Threat (campaign-specific, time-sensitive), Compliance (framework-violation detections),
and Placeholder (rules with a value finalized only at conversion time, e.g. "your org's admin
group name").

**Simple explanation**: A Sigma rule is a detection idea written in a SIEM-neutral YAML dialect —
"if you see this pattern in this kind of log, that's this technique" — that a converter tool then
translates into the specific query syntax of whatever product you actually run. It's the
detection-engineering equivalent of writing portable source code instead of one platform's binary.

**Try it**: Hand-write a real Sigma rule (following the format's actual required structure) for
the exact sudo-brute-force pattern already investigated in links 5-6 of this section, and validate
it parses correctly — no Sigma CLI install required, `pyyaml` (already available on this machine)
is enough to confirm structural validity. Note: this uses a multi-line heredoc, which **fish does
not support** (`fish: Expected a string, but found a redirection` — verified) — per this repo's
convention for multi-step sequences, the whole block is wrapped in `bash -c '...'` so it's
portable and runs correctly from a fish prompt.
```fish
bash -c '
cat > /tmp/test-sigma-rule.yml << "EOF"
title: Repeated Sudo Password Prompts From Same User
id: 8f3c1e2a-0000-4000-8000-000000000001
status: experimental
description: Detects more than 5 sudo password-required events from the same user within a short window, a possible brute-force or scripted credential-guessing pattern.
logsource:
  product: linux
  service: auth
detection:
  selection:
    process: sudo
    message|contains: "a password is required"
  condition: selection | count() by user > 5
falsepositives:
  - Legitimate interactive user running many sudo commands in a short session
level: low
EOF
python3 -c "
import yaml
rule = yaml.safe_load(open(\"/tmp/test-sigma-rule.yml\"))
for key in [\"title\", \"logsource\", \"detection\"]:
    print(key, \"present:\", key in rule)
print(\"condition:\", rule[\"detection\"][\"condition\"])
"
rm /tmp/test-sigma-rule.yml
'
```
bash/sh: drop the outer `bash -c '...'` wrapper and run the inner block directly — it's already
plain bash/sh syntax.
Verified on this machine: all 3 required top-level keys present, condition string parses as
expected. Note the `message|contains` field modifier and `count() by user > 5` aggregation syntax
are exactly Sigma's real detection DSL, not simplified for this exercise.

## Beginner's guide to Sigma rules (SOC Prime blog)

**FLAGGED FOR MANUAL RE-CHECK**: both a direct `curl` fetch and a `WebFetch` retry returned HTTP
403 Forbidden from `socprime.com` (a WAF/Cloudflare-style block, not a bot-detection JS challenge
like TryHackMe's) — per the "skip after one retry, note for manual re-check" instruction, this
entry does **not** quote or paraphrase this specific article's content, since it was never
successfully retrieved. Re-check manually at
`https://socprime.com/blog/sigma-rules-the-beginners-guide/` if this article's exact wording,
examples, or framing matter later.

**Claim**: in place of the blocked article, this entry captures the same beginner-level Sigma
syntax facts already verified structurally and hands-on in the previous link (SigmaHQ repo), laid
out explicitly as a standalone reference rather than attributed to this specific source. A minimal
valid Sigma rule needs exactly 3 top-level keys: `title` (human-readable name), `logsource`
(which log type/product/service this rule targets — e.g. `product: linux`, `service: auth`), and
`detection` (the actual matching logic, itself containing one or more named selections plus a
`condition` string combining them, e.g. `condition: selection`). Common optional-but-standard
fields: `id` (a UUID uniquely identifying the rule), `status` (experimental/test/stable),
`description`, `level` (informational/low/medium/high/critical severity), `falsepositives` (known
benign triggers), and `tags` (often ATT&CK technique IDs, directly linking back to links 4-6 of
this section). Field modifiers (appended with `|` to a field name inside `detection`) change match
behavior — `|contains`, `|startswith`, `|endswith`, `|re` (regex) are the most common, already
used correctly and validated in the previous link's `message|contains` example.

**Simple explanation**: A Sigma rule's minimum viable shape is "what am I calling this, what kind
of log am I looking at, and what pattern in that log counts as a match" — everything else
(severity, false-positive notes, ATT&CK tags) is useful metadata layered on top of those 3
required pieces.

**Try it**: Since the source article itself couldn't be retrieved, the exercise re-uses and
extends the already-verified rule-writing/validation pattern from the previous link rather than
inventing unverified claims about this specific guide's content.
```fish
# confirm pyyaml is available for rule validation (already used in link 7)
python3 -c "import yaml; print('pyyaml OK')"
```
bash/sh: identical.
Applied exercise: take the Sigma rule written and validated in link 7's Try It, and add the
optional metadata fields named above (`tags: [attack.persistence, attack.t1078]`, `status: test`)
— re-validate with the same `pyyaml` snippet, confirming the rule still parses after the addition.

## Blue Team Labs Online (practice)

**Claim** (note: the source list's domain, `blueteamlabsonline.com`, does not resolve at all —
DNS lookup failure confirmed directly with WebFetch; a `curl -I` check plus a `WebSearch` found
the platform's real current domain is `blueteamlabs.online`, with its parent training company
"Security Blue Team" separately rebranded to "Centri" as of June 2026 — the labs platform itself
is unaffected by that rebrand. Content below is from the correct working domain, flagged here
because the exact URL in the source list needs updating): BTLO is a gamified, scenario-based
practice platform covering Incident Response, Digital Forensics, Security Operations, Reverse
Engineering, and Threat Hunting — directly overlapping every topic named across this section's
links 2-8. Two content formats: **Investigations** (immersive lab scenarios simulating a full
incident, e.g. forensic analysis of a seized laptop, or log review during an active server
intrusion — answered via a series of graded questions) and **Challenges** (standalone downloadable
artifacts: memory dumps, phishing emails, PCAPs, logs, worked through offline at your own pace).
Free tier gets challenge downloads only (no in-browser lab VMs); PRO tier (paid, £15-144
depending on duration) unlocks 268+ full investigation labs with browser-based VMs (no local VM/
VPN setup needed) plus full leaderboard access.

**Simple explanation**: This is "practice SOC analyst work on realistic fake incidents" —
free-tier challenges are take-home evidence files you analyze with your own tools, paid-tier
investigations are guided, graded, full incident scenarios in a browser lab. It targets people who
already know the concepts (from links like MITRE ATT&CK, Sigma, SPL in this section) and want
reps applying them.

**Try it**: The free-tier download-and-analyze challenge format (memory dumps, PCAPs, logs) is
exactly the kind of offline artifact this repo already has tooling patterns for — this repo's
`pcap-analyze` skill exists for exactly this use case. No paid PRO account is used or required
here, consistent with this repo's no-live-paid-account rule.
```fish
# confirm this machine already has the core free-tier-relevant analysis tools available
which tshark   # present here (memory-forensics tool `volatility3` is not — would need separate install)
python3 -c "import yaml; print('yaml OK, for any Sigma-rule-based challenge scoring')"
```
bash/sh: identical.
Applied exercise: without downloading anything from the platform, write a 4-step plan for how
you'd approach a hypothetical free-tier "log analysis" challenge using only local/offline tools
already verified elsewhere in this study set — e.g. (1) `journalctl`/log source triage pattern
from links 1-2, (2) MITRE ATT&CK technique mapping from links 4-6, (3) a hand-written Sigma rule
from link 7 to codify the finding, (4) a written incident summary in the triage-note format
practiced in section 3 link 2's exercise.

## CyberDefenders (practice/investigations)

**Claim**: CyberDefenders (already used as a source domain earlier in this section for link 6's
MITRE ATT&CK guide) is a blue-team practice ecosystem with 3 parts: **Training/Certification** —
role-based, NICE/DoD-framework-aligned paths culminating in the Certified CyberDefender (CCD)
Level 1/2 certs, whose practical exam is explicitly described as a "brutal 48-hour" hands-on
assessment (analysts report 8-9 hour single-assignment sessions, i.e. genuinely deep investigation
work, not multiple-choice). **Cyber Range & Labs** — scenario-based investigations explicitly
built from real incidents and real APT tactics, using realistic forensic artifacts across a named
tool set (Nessus, Sentinel, Elastic, Volatility) with an explicit "no artificial data, no
simulated shortcuts" stance. **Enterprise** — team-performance benchmarking/dashboards, out of
scope for individual study. Investigation domains span threat hunting, disk/memory/network
forensics, perimeter defense, incident response, evidence collection, and cloud forensics —
directly covering the DFIR side that complements BTLO (previous link) and the ATT&CK/Sigma
detection-engineering side already built up earlier in this section.

**Simple explanation**: Where BTLO is broad gamified practice across many blue-team domains,
CyberDefenders leans harder into DFIR-specific realism and a genuine certification path with a
real multi-day practical exam — both platforms complement rather than duplicate each other, and
this study set has already used CyberDefenders directly as a *content* source (link 6), not just
as a practice platform.

**Try it**: Same no-live-paid-account boundary as the previous link — the applied exercise is
mapping CyberDefenders' named toolset (Nessus, Sentinel, Elastic, Volatility) against what's
locally available/inspectable on this machine, without needing an account.
```fish
# of the 4 named tools, check local availability/analogues
which nmap        # Nessus is a paid vuln scanner; nmap is the closest freely-available local analogue
which tshark       # network forensics analogue already confirmed present (link 9)
python3 -c "import yaml; print('yaml OK — used for Sigma rules earlier in this section')"
```
bash/sh: identical.
Applied exercise: write a one-paragraph comparison of BTLO (previous link) vs. CyberDefenders —
which one would you point a brand-new SOC trainee at first, and which one would you point someone
preparing for a DFIR-heavy certification at, and why, based on the concrete differences captured
above (breadth/gamification vs. depth/certification-exam realism).
