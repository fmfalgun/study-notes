# 3. SIEM — Exercises

## 1. Splunk free official training

1. List the 3 training tracks the catalog groups courses into (Platform, Security,
   Observability) and pick 2 course titles from each that a SOC analyst (not an admin/developer)
   would prioritize first.
2. Run the journalctl "filter" exercise (SPL `search` equivalent):
   ```fish
   journalctl -p err --no-pager -n 5
   ```
   bash/sh: identical.
3. Run the journalctl "aggregate" exercise (SPL `stats count by` equivalent):
   ```fish
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
   bash/sh: identical.
4. Write the SPL query text (no Splunk instance needed) that would produce equivalent results to
   each journalctl command above.
5. Explain in 2-3 sentences why "learn SPL" is effectively the one skill that transfers across
   almost every course in the catalog (Platform, Security, and Observability alike) — what role
   does a query language play in any SIEM regardless of which specific product features you use?

## 2. Hands-on SOC practice path (TryHackMe SOC Level 1)

Note: the live page was blocked by a bot-protection checkpoint during research — this section's
notes are built from independent write-ups about the path, flagged for a manual re-check against
`https://tryhackme.com/path/outline/soclevel1` directly if exact module wording/order matters.

1. List the 5 confirmed modules (SOC Fundamentals, SOC Team Internals, Security Solutions, Alert
   Handling, Phishing Analysis) and write one sentence per module on what Tier-1 SOC skill it
   builds.
2. Run the local alert-triage stand-in exercise:
   ```fish
   journalctl SYSLOG_IDENTIFIER=sudo --no-pager --since "2 hours ago" | grep -i "password is required\|incorrect password\|authentication failure"
   ```
   bash/sh: identical.
3. For up to 3 matching log lines, write a mini triage note in this format: **Event**: what
   happened. **Who/what**: user, working directory, command attempted. **When**: timestamp.
   **Initial assessment**: benign / needs-a-second-look / escalate, with one sentence justifying
   the call (hint: on a single-user personal machine, repeated `sudo` password prompts from the
   known local user during active interactive work are expected/benign — the same pattern from an
   unfamiliar account or off-hours would warrant escalation).
4. Explain in 2-3 sentences the difference in focus between this path (SOC Level 1) and the
   Splunk training catalog from link 1 — one teaches a specific vendor's tool, the other teaches
   a role's workflow; why does a real SOC analyst need both?
5. Write down the exact URL to manually re-check later (`https://tryhackme.com/path/outline/soclevel1`)
   and what specifically to verify once accessible (full 10-module list, in order).

## 3. SOC analyst tools & skills roadmap

1. Confirm the Linux-side tools named in the roadmap's Year 0-1 skill list are present on this
   machine:
   ```fish
   which auditctl ausearch aureport
   systemctl is-active auditd
   ```
   bash/sh: identical. Verified here: tools present, service currently inactive.
2. Build the 8-entry mapping table: Windows event ID -> what it means -> closest Linux
   equivalent. Cover 4624, 4625, 4634, 4740, 4720, 4732, 7045, 7036.
3. Write the year range (0-1, 1-2, 2-3, 3-4, 4-5, 5+) next to each of these skills, matching the
   roadmap's own progression: MITRE ATT&CK fundamentals, Sigma rule writing, SOAR playbook
   development, cloud security specialty cert, mentoring L1/L2 analysts.
4. Reproduce the SIEM platform comparison table (Splunk / Sentinel / Elastic / QRadar) with
   columns: claimed hiring share, one strength, one weakness — from the roadmap's own numbers.
5. (Optional, root) If you want to see real audit records: `sudo ausearch -ts today | head -20`
   (requires auditd to actually be logging — inactive by default on this machine, so this may
   return nothing without first enabling the service).

## 4. MITRE ATT&CK framework (core reference)

1. Pull the live tactic list and technique counts directly:
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
2. List all 14 tactics in their kill-chain-ish order (Reconnaissance through Impact) and, for
   each, write one sentence describing the adversary's goal at that stage in plain language.
3. Explain in 2-3 sentences the difference between a tactic, a technique, and a sub-technique,
   using "Phishing" (Initial Access technique) and its 4 named sub-techniques (Spearphishing
   Service/Attachment/Link/Voice) as a concrete example.
4. Explain in 1-2 sentences why Discovery (34 techniques) has so many more distinct techniques
   than Exfiltration or Reconnaissance (9 each) — what's structurally different about "enumerate
   things on a compromised system" vs. "get data out" that would produce more distinct methods?
5. Name the 3 ATT&CK matrices (Enterprise, Mobile, ICS) and write one sentence on why a single
   unified matrix wouldn't work well across all three environments (hint: think about what
   techniques even make sense on a mobile phone vs. a SCADA/ICS system vs. a normal enterprise
   network).

## 5. MITRE ATT&CK complete guide

1. List the 3 gaps in pre-ATT&CK detection practice the article names (indicator staleness,
   kill-chain abstraction, lack of shared taxonomy) and write one sentence per gap explaining the
   specific failure mode.
2. Confirm this machine's local telemetry-source tooling (the same building block a real SIEM
   pipeline ingests from):
   ```fish
   journalctl --no-pager -n 3
   which auditctl
   ```
   bash/sh: identical.
3. Draw the 5-step detection-engineering workflow as a loop diagram: centralize telemetry ->
   translate technique to query -> execute technique in a lab (Atomic Red Team) -> build
   detection from real artifacts -> validate via red-team bypass attempt -> (loop back).
4. Pick one specific ATT&CK technique (e.g. T1055 Process Injection or T1548.002 Bypass User
   Account Control). Using only its public ATT&CK description (no execution), write: (a) what log
   source would need to be collected to detect it, (b) what specific field/event pattern a
   detection rule would look for. This is documentation research only — no attack execution.
5. Explain in 2-3 sentences how ATT&CK changes a threat-intel report from "Group X targets the
   finance industry" (not actionable) to something a defender can build a detection from (hint:
   the registry-run-key persistence example in the article).

## 6. MITRE ATT&CK guide for SOC/DFIR

1. Run the adapted T1078 (Valid Accounts) detection query against this machine's real sudo log:
   ```fish
   journalctl SYSLOG_IDENTIFIER=sudo --no-pager --since "2 hours ago" | awk -F'sudo\\[[0-9]+\\]:\\s+' '{print $2}' | awk '{print $1}' | sort | uniq -c | sort -rn
   ```
   bash/sh: identical.
2. Write one sentence on whether the count you got would trip the article's "count > 5" threshold,
   and whether that's actually suspicious here (single-user dev machine, known interactive user)
   versus what the same pattern/threshold would mean on a shared production server.
3. Build a 5-row table: Technique ID | Name | Log source | Concrete artifact/indicator — using
   the 5 techniques detailed in the article (T1059, T1003, T1021, T1036, T1053).
4. Explain in 2-3 sentences the "detection coverage gap" use case: if your SIEM has 50 detections
   tagged T1059 and zero tagged T1574, what does that tell you, and what should you do next?
5. Take one alert-to-technique mapping from the article (e.g. "repeated failed auth then success
   from an anomalous IP" -> T1078 Valid Accounts) and write the equivalent for a technique of
   your choice not covered in the article, using only its public ATT&CK technique page as your
   source (documentation research only, no execution).

## 7. Writing/reading Sigma detection rules

1. Write and validate the sudo-brute-force Sigma rule (note: uses a heredoc, which fish does not
   support — wrap in `bash -c '...'` as shown, verified working on this machine):
   ```fish
   bash -c '
   cat > /tmp/test-sigma-rule.yml << "EOF"
   title: Repeated Sudo Password Prompts From Same User
   id: 8f3c1e2a-0000-4000-8000-000000000001
   status: experimental
   logsource:
     product: linux
     service: auth
   detection:
     selection:
       process: sudo
       message|contains: "a password is required"
     condition: selection | count() by user > 5
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
   bash/sh: drop the outer `bash -c '...'` wrapper, run the inner lines directly.
2. Identify, in the rule you just validated, which YAML key is the `logsource` (what kind of log
   this rule applies to) and which is the `detection` (the actual matching logic) — explain in
   1-2 sentences why separating these two concerns is what makes a Sigma rule portable across
   different SIEMs (the same `detection` logic can target different `logsource` definitions per
   platform, and a converter maps the rest).
3. Modify the rule's `level` field from `low` to `high` and its condition threshold from `> 5` to
   `> 20`. Explain in 1-2 sentences a real scenario where raising the threshold this much would be
   the correct tuning decision (hint: revisit your answer from link 6, question 2, about this
   being a single-user dev machine).
4. Write, by hand, a second toy Sigma rule (any topic covered elsewhere in this study set is
   fine — e.g. WireGuard handshake failures, or repeated DNS queries to a debug record domain
   from link 9 of section 1) with the same 3 required keys (`title`, `logsource`, `detection`),
   and validate it the same way with the `pyyaml` snippet above.
5. List the 5 Sigma rule categories in the SigmaHQ repo (Generic, Threat Hunting, Emerging
   Threat, Compliance, Placeholder) and classify which category your rule from step 1 and step 4
   would each best fit into, with one sentence justifying each choice.

## 8. Beginner's guide to Sigma rules

Note: the source article (`socprime.com/blog/sigma-rules-the-beginners-guide/`) returned HTTP 403
on both a direct fetch and a retry — flagged for manual re-check; this section's exercise reuses
already-verified Sigma syntax instead of unverified claims about this specific article.

1. List the 3 required top-level Sigma keys (`title`, `logsource`, `detection`) and the 5 common
   optional ones (`id`, `status`, `description`, `level`, `falsepositives`, `tags`) — 8 total,
   write one sentence on what each holds.
2. Extend the rule from section 3 link 7's exercise with `tags` (ATT&CK technique IDs) and
   `status: test`:
   ```fish
   bash -c '
   cat > /tmp/test-sigma-rule2.yml << "EOF"
   title: Repeated Sudo Password Prompts From Same User
   id: 8f3c1e2a-0000-4000-8000-000000000001
   status: test
   tags:
     - attack.persistence
     - attack.t1078
   logsource:
     product: linux
     service: auth
   detection:
     selection:
       process: sudo
       message|contains: "a password is required"
     condition: selection | count() by user > 5
   level: low
   EOF
   python3 -c "
   import yaml
   rule = yaml.safe_load(open(\"/tmp/test-sigma-rule2.yml\"))
   for key in [\"title\", \"logsource\", \"detection\", \"tags\", \"status\"]:
       print(key, \"present:\", key in rule)
   print(\"tags:\", rule[\"tags\"])
   "
   rm /tmp/test-sigma-rule2.yml
   '
   ```
   bash/sh: drop the outer `bash -c '...'` wrapper, run the inner lines directly.
3. Explain in 1-2 sentences why the `tags` field using `attack.t1078` format is a direct,
   deliberate link back to MITRE ATT&CK (studied in links 4-6 of this section) rather than a
   free-text label.
4. List the 4 common field modifiers (`|contains`, `|startswith`, `|endswith`, `|re`) and write a
   one-line example detection selection using each one against a hypothetical `CommandLine` field.
5. Write down the URL to manually re-check (`https://socprime.com/blog/sigma-rules-the-beginners-guide/`)
   and what to verify once accessible (whether it covers anything beyond the syntax already
   confirmed here — e.g. a specific worked example or a different explanatory angle).

## 9. Blue Team Labs Online (practice)

Note: the source list's URL (`blueteamlabsonline.com`) does not resolve (DNS failure, confirmed).
The platform's real current domain is `blueteamlabs.online` — use that going forward.

1. Confirm the correct domain resolves and the old one doesn't:
   ```fish
   curl -sL -I https://blueteamlabs.online/ | head -3
   ```
   bash/sh: identical.
2. List the 2 content formats (Investigations, Challenges) and write one sentence on the
   practical difference between them (guided browser-based lab with grading vs. self-paced
   downloaded artifact).
3. Confirm which offline analysis tools are already available on this machine for a hypothetical
   free-tier challenge:
   ```fish
   which tshark
   python3 -c "import yaml; print('yaml OK')"
   ```
   bash/sh: identical. Note: `volatility3` (memory forensics) is not installed here — would need
   a separate install if a real memory-dump challenge were attempted.
4. Write a 4-step plan for approaching a hypothetical "log analysis" free-tier challenge using
   only tools/techniques already verified elsewhere in this study set: (1) log triage
   (journalctl-style filtering from links 1-2), (2) technique mapping (ATT&CK from links 4-6),
   (3) codify the finding as a Sigma rule (link 7), (4) write an incident summary (triage-note
   format from link 2's exercise).
5. Explain in 2-3 sentences why this repo's rules require sticking to the free tier / offline
   artifacts for this exercise rather than signing up for a paid PRO account to try a real
   investigation lab.

## 10. CyberDefenders (practice/investigations)

1. Confirm local analogues of CyberDefenders' named toolset are available:
   ```fish
   which nmap
   which tshark
   python3 -c "import yaml; print('yaml OK')"
   ```
   bash/sh: identical. Verified present here: `nmap` (closest free analogue to Nessus), `tshark`.
2. List the 3 parts of the CyberDefenders ecosystem (Training/Certification, Cyber Range & Labs,
   Enterprise) and write one sentence on which one an individual self-studying SOC analyst would
   actually use (hint: Enterprise is for organizations, not individuals).
3. List the investigation domains named on the platform (threat hunting; disk, memory, and
   network forensics as 3 separate items; perimeter defense; incident response; evidence
   collection; cloud forensics — 8 total) and mark which ones this study set has already touched
   (hint: link 6 of this section already used CyberDefenders directly as a content source for
   MITRE ATT&CK mapping — that's threat-hunting/detection-adjacent).
4. Write a one-paragraph comparison: BTLO (link 9) vs. CyberDefenders (this link) — which would
   you recommend to a brand-new SOC trainee vs. someone preparing for a DFIR-heavy certification,
   and why, based on the concrete differences captured in each link's notes (breadth/gamification
   vs. depth/certification-exam realism).
5. Write 2-3 sentences on what "no artificial data, no simulated shortcuts" (the platform's own
   stated design philosophy) is meant to solve for compared to a purely synthetic/toy training lab
   — why does forensic realism matter more here than in, say, a beginner SPL tutorial?
