# 3. SIEM / Detection-Engineering Development — Exercises

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 3.

## 1. Sigma — read a real rule, then write and validate a toy one

1. Pull a real, current Sigma rule directly (a full `git clone` of this repo stalled twice during
   research — use the GitHub API/raw content endpoints instead, verified fast and reliable):
   ```fish
   curl -s https://raw.githubusercontent.com/SigmaHQ/sigma/master/rules/windows/process_creation/proc_creation_win_7zip_password_compression.yml
   ```
   ```
   # bash/sh:
   curl -s https://raw.githubusercontent.com/SigmaHQ/sigma/master/rules/windows/process_creation/proc_creation_win_7zip_password_compression.yml
   ```
2. Label each top-level YAML key's purpose in your own words (`title`, `id`, `status`,
   `logsource`, `detection`, `condition`, `falsepositives`, `level`).
3. Write a toy Sigma rule of your own, tying back to this file's VPN material: detect `wg-quick`
   being invoked against a config file outside `/etc/wireguard/` (a simple heuristic for "someone
   is running WireGuard from an unexpected location," which could indicate an unauthorized tunnel).
   Save it to a scratch file:
   ```yaml
   title: Suspicious wg-quick Invocation With Non-Standard Config Path
   id: 3f8e2a1c-0000-4a00-8000-000000000001
   status: experimental
   description: Detects wg-quick being invoked against a config file outside the usual /etc/wireguard directory.
   references:
       - internal-study-notes-toy-rule
   author: study-notes
   date: 2026-08-05
   tags:
       - attack.command_and_control
       - attack.t1572
   logsource:
       category: process_creation
       product: linux
   detection:
       selection_cmd:
           Image|endswith: '/wg-quick'
       filter_standard_path:
           CommandLine|contains: '/etc/wireguard/'
       condition: selection_cmd and not filter_standard_path
   falsepositives:
       - Administrators intentionally testing a WireGuard config from a non-standard path
   level: medium
   ```
4. Validate it parses as well-formed YAML with the expected structure (verified working locally,
   PyYAML available):
   ```fish
   python3 -c "
   import yaml
   with open('toy-sigma-rule.yml') as f:
       d = yaml.safe_load(f)
   print('parsed OK, keys:', list(d.keys()))
   print('condition:', d['detection']['condition'])
   "
   ```
5. Note explicitly: this only validates YAML *syntax*, not that the rule is semantically valid
   Sigma (that requires `pysigma`/`sigma-cli`, not exercised here) — write one sentence on what
   `condition: selection_cmd and not filter_standard_path` is actually excluding, and why the
   `filter_` naming prefix (vs `selection_`) is a Sigma convention worth following even though the
   condition expression could reference any block name.

## 2. Mastering Sigma rules — practice the `1 of selection*` quantifier

1. Write a second toy rule using the OR-style `1 of selection*` quantifier (looser than exercise
   1's `all of selection_*`) — detect any of three common VPN client binaries running from a `/tmp`
   path:
   ```yaml
   title: Suspicious VPN Client Binary Executed From Unusual Location
   id: 3f8e2a1c-0000-4a00-8000-000000000002
   status: experimental
   description: Detects execution of common VPN client binaries (wg, openvpn, ipsec) from a temp or download directory instead of a standard system path.
   logsource:
       category: process_creation
       product: linux
   detection:
       selection1:
           Image|endswith: '/wg'
           CommandLine|contains: '/tmp/'
       selection2:
           Image|endswith: '/openvpn'
           CommandLine|contains: '/tmp/'
       selection3:
           Image|endswith: '/ipsec'
           CommandLine|contains: '/tmp/'
       condition: 1 of selection*
   falsepositives:
       - Developer testing a locally built VPN client binary
   level: low
   ```
2. Validate it parses (verified working):
   ```fish
   python3 -c "
   import yaml
   with open('toy-sigma-rule2.yml') as f:
       d = yaml.safe_load(f)
   print('parsed OK, condition:', d['detection']['condition'])
   "
   ```
3. Write one sentence contrasting `all of selection_*` (exercise 1) vs `1 of selection*` (this
   exercise): which one is stricter, and which real-world scenario (a rule that must match several
   simultaneous conditions vs a rule that should fire on any of several equivalent indicators) calls
   for each.
4. Add MITRE ATT&CK tags to this rule (`attack.execution`, `attack.t1219` or similar — pick
   whichever technique ID best fits "unauthorized remote access tooling") and note that this is the
   same tagging convention already seen in link 1's real Sigma rule and will reappear in section 4's
   ATT&CK link.
5. Note the explicit gap: this article does not cover aggregation (count/threshold-over-time rules)
   or correlation (multi-rule chaining) — both real Sigma features, just out of scope for what was
   read here. Don't assume rule-writing knowledge is complete after just these two links.

## 3. Elastic detection-rules — parse a real production TOML rule and extract ATT&CK mappings

1. Fetch a real, current production rule directly (GitHub API/raw content, same pattern as link 1
   — avoids repeating the earlier stalled full clone):
   ```fish
   set rule_toml (mktemp -t posh-keylogger.XXXX.toml)
   curl -s https://raw.githubusercontent.com/elastic/detection-rules/main/rules/windows/collection_posh_keylogger.toml -o $rule_toml
   ```
   ```
   # bash/sh:
   rule_toml=$(mktemp -t posh-keylogger.XXXX.toml)
   curl -s https://raw.githubusercontent.com/elastic/detection-rules/main/rules/windows/collection_posh_keylogger.toml -o "$rule_toml"
   ```
2. Parse it with Python's stdlib `tomllib` (verified working, no extra install needed on Python
   3.11+) and extract the MITRE ATT&CK technique IDs from the nested `[[rule.threat]]` tables:
   ```fish
   python3 -c "
   import tomllib
   with open('$rule_toml', 'rb') as f:
       d = tomllib.load(f)
   print('top-level keys:', list(d.keys()))
   print('rule name:', d['rule']['name'])
   print('MITRE technique IDs:', [t['id'] for entry in d['rule']['threat'] for t in entry['technique']])
   "
   ```
   ```
   # bash/sh:
   python3 -c "
   import tomllib
   with open('$rule_toml', 'rb') as f:
       d = tomllib.load(f)
   print('top-level keys:', list(d.keys()))
   print('rule name:', d['rule']['name'])
   print('MITRE technique IDs:', [t['id'] for entry in d['rule']['threat'] for t in entry['technique']])
   "
   ```
3. List the fields this rule has that neither of the toy Sigma rules (exercises 1-2) did: `note`
   (analyst triage runbook), `setup` (required log-source prerequisites), `risk_score` (a numeric
   score vs Sigma's simple `level` string), structured `[[rule.threat.technique.subtechnique]]`
   tables. Write 2-3 sentences on which of these fields you'd want to add to the toy Sigma rules to
   make them production-ready, and why "which log source must be enabled" (the `setup` field) is
   often the single most-overlooked prerequisite in a real deployment.
4. Clean up:
   ```fish
   rm -f $rule_toml
   ```
   ```
   # bash/sh:
   rm -f "$rule_toml"
   ```

## 4. Splunk Developer Platform — verify the SDK inventory through a fallback channel

The `dev.splunk.com` landing page is a client-side-rendered SPA — neither WebFetch nor `curl`
returns usable body content for it. Rather than give up on this link, use a different, more
reliable channel (the GitHub API) to verify the one concrete, checkable claim: which SDKs Splunk
actually maintains.

1. Confirm the SPA problem yourself first (verified: near-empty body, just a `<title>` tag):
   ```fish
   curl -sL https://dev.splunk.com/ -o (mktemp -t splunk-dev.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://dev.splunk.com/ -o /tmp/splunk-dev.html
   ```
2. Query the `splunk` GitHub org for SDK repos instead (verified working — returns real data even
   though the landing page doesn't):
   ```fish
   curl -s "https://api.github.com/orgs/splunk/repos?per_page=100" | python3 -c "
   import json, sys
   repos = json.load(sys.stdin)
   for r in repos:
       if 'sdk' in r['name'].lower():
           print(r['name'], '-', r.get('language'))
   "
   ```
   ```
   # bash/sh:
   curl -s "https://api.github.com/orgs/splunk/repos?per_page=100" | python3 -c "
   import json, sys
   repos = json.load(sys.stdin)
   for r in repos:
       if 'sdk' in r['name'].lower():
           print(r['name'], '-', r.get('language'))
   "
   ```
3. Confirmed languages (verified, at time of this exercise): Python, JavaScript, Java, Ruby, PHP,
   C# (plus a PCL variant and Xamarin iOS/Android bindings), and a separate Splunk Cloud SDK family
   in TypeScript and Go. Note which of these you would NOT have guessed from memory alone (Ruby and
   PHP are easy to miss) — this is the value of verifying via a structured API instead of relying on
   what "everyone knows" about a platform.
4. Write one sentence on why a page being SPA-rendered matters for this repo's research workflow:
   the usual "curl instead of WebFetch for a lossy render" fallback (used successfully throughout
   sections 1-2 for torproject.org) only works when the server sends real HTML that a client-side
   framework then enhances — it does nothing when the server sends an empty shell and all content
   is fetched by JavaScript after page load, which is the case here and is a fundamentally different
   failure mode.

## 5. Detection-as-Code — write a CI validation script for the toy Sigma rules

1. Recreate the two toy Sigma rules from exercises 1-2 in a scratch directory (or reuse them if
   still present):
   ```fish
   mkdir -p /tmp/dac-demo/rules
   ```
   ```
   # bash/sh:
   mkdir -p /tmp/dac-demo/rules
   ```
2. Write a tiny "CI" validation script that mimics the Detection-as-Code pipeline pattern —
   syntax-check every `.yml` file in the rules directory and fail loudly on the first broken one
   (this is a miniature version of what the Elastic repo's GitHub Actions "Unit Tests" workflow
   does at much larger scale):
   ```python
   import sys, glob, yaml

   failures = []
   for path in glob.glob("/tmp/dac-demo/rules/*.yml"):
       try:
           with open(path) as f:
               rule = yaml.safe_load(f)
           required = {"title", "id", "logsource", "detection", "level"}
           missing = required - rule.keys()
           if missing:
               failures.append(f"{path}: missing required fields {missing}")
       except yaml.YAMLError as e:
           failures.append(f"{path}: YAML parse error: {e}")

   if failures:
       print("FAILED:")
       for f in failures:
           print(" -", f)
       sys.exit(1)
   print("All rules valid.")
   ```
3. Place both toy rules from exercises 1-2 into `/tmp/dac-demo/rules/` and run the script — it
   should report "All rules valid." Then deliberately delete a required field (e.g. `level`) from
   one copy and re-run to confirm the script actually catches the regression (this is the same
   "prove it catches real breakage" discipline used earlier for the wg-quick permission check in
   section 2, exercise 5).
4. Write 2-3 sentences connecting this toy script to what a real CI pipeline (like Elastic's) adds
   on top: running on every pull request automatically (not manually), testing against real log
   samples (not just schema validity), and blocking merge on failure rather than just printing a
   warning.
5. Clean up:
   ```fish
   rm -rf /tmp/dac-demo
   ```
   ```
   # bash/sh:
   rm -rf /tmp/dac-demo
   ```

## 6. Splunk Attack Range — trace the WireGuard cross-reference and repo structure

1. List the repo's top-level structure via the GitHub API (no clone needed):
   ```fish
   curl -s "https://api.github.com/repos/splunk/attack_range/contents/" | python3 -c "import json,sys; [print(i['type'], i['name']) for i in json.load(sys.stdin)]"
   ```
   ```
   # bash/sh:
   curl -s "https://api.github.com/repos/splunk/attack_range/contents/" | python3 -c "import json,sys; [print(i['type'], i['name']) for i in json.load(sys.stdin)]"
   ```
2. Fetch the README from the correct branch — note this repo's default branch is `develop`, not
   `main`, which caused a 404 on first attempt (verified: confirm via
   `curl -s https://api.github.com/repos/splunk/attack_range | python3 -c "import json,sys; print(json.load(sys.stdin)['default_branch'])"`):
   ```fish
   curl -s "https://raw.githubusercontent.com/splunk/attack_range/develop/README.md" | grep -E -i -n "wireguard|terraform|ansible|atomic red team"
   ```
   ```
   # bash/sh:
   curl -s "https://raw.githubusercontent.com/splunk/attack_range/develop/README.md" | grep -E -i -n "wireguard|terraform|ansible|atomic red team"
   ```
3. Write down the full pipeline this tool implements, end to end, in your own words: Terraform
   provisions cloud infra → Ansible configures it → WireGuard secures remote access to it → Atomic
   Red Team generates attack telemetry inside it → Splunk ingests the telemetry → a detection
   engineer builds/tests Sigma or Elastic-style rules (links 1-3) against that real data.
4. Note explicitly which section-1 (VPN) content this connects back to: WireGuard's `AllowedIPs`/
   config-distribution problem (section 1, link 8's exercise) is exactly what "generate additional
   client configs to share the range with others" is solving for this specific tool.
5. This repo provisions real, billable cloud infrastructure when actually run — reading the repo
   structure and README (steps 1-2 above) stays within scope; do NOT run `attack_range.py build`
   or otherwise provision real cloud resources as part of this exercise.

## 7. MITRE ATT&CK as a data model — build a 3-row coverage table from this file's own rules

1. Gather the ATT&CK tags already recorded in this file's earlier entries: the toy rule from
   exercise 1 (`attack.command_and_control`, `attack.t1572`), the toy rule from exercise 2 (whatever
   technique ID you picked for "unauthorized remote access tooling"), and the real Elastic rule from
   exercise 3 (`T1056`/`T1059`/`T1106`, tactics `TA0009` Collection and `TA0002` Execution).
2. Build a small table by hand:

   | Rule | Tactic | Technique ID |
   |---|---|---|
   | Suspicious wg-quick invocation (toy) | Command and Control | T1572 |
   | Suspicious VPN client from /tmp (toy) | ? | ? |
   | PowerShell Keylogging Script (real, Elastic) | Collection / Execution | T1056 / T1059 / T1106 |

3. Confirm the Sigma project does exactly this aggregation at scale — check for the coverage
   heatmap artifact referenced in the Sigma repo's own root listing (from section 3, link 1):
   ```fish
   curl -s "https://api.github.com/repos/SigmaHQ/sigma/contents/" | python3 -c "import json,sys; [print(i['name']) for i in json.load(sys.stdin) if 'coverage' in i['name'].lower() or 'nav' in i['name'].lower()]"
   ```
   ```
   # bash/sh:
   curl -s "https://api.github.com/repos/SigmaHQ/sigma/contents/" | python3 -c "import json,sys; [print(i['name']) for i in json.load(sys.stdin) if 'coverage' in i['name'].lower() or 'nav' in i['name'].lower()]"
   ```
4. Write two sentences: which ATT&CK tactics does this file's tiny 3-rule table have zero coverage
   for (compare against the full list of ATT&CK tactics: Reconnaissance, Resource Development,
   Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access,
   Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact), and why that
   gap is exactly the kind of signal this methodology is meant to surface at real scale.

## 8. Atomic Red Team — trace the T1560.001 cross-reference back to link 1's Sigma rule

1. Fetch the atomic test definition for T1560.001 — the exact technique ID referenced in link 1's
   real Sigma rule (`proc_creation_win_7zip_password_compression.yml`):
   ```fish
   curl -s "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1560.001/T1560.001.yaml" | head -20
   ```
   ```
   # bash/sh:
   curl -s "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1560.001/T1560.001.yaml" | head -20
   ```
2. Parse it and confirm the structure (verified working):
   ```fish
   set atomic_yaml (mktemp -t t1560-001.XXXX.yaml)
   curl -s "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1560.001/T1560.001.yaml" -o $atomic_yaml
   python3 -c "
   import yaml
   with open('$atomic_yaml') as f:
       d = yaml.safe_load(f)
   print('attack_technique:', d['attack_technique'])
   print('number of atomic tests:', len(d['atomic_tests']))
   print('first test name:', d['atomic_tests'][0]['name'])
   "
   rm -f $atomic_yaml
   ```
   ```
   # bash/sh:
   atomic_yaml=$(mktemp -t t1560-001.XXXX.yaml)
   curl -s "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1560.001/T1560.001.yaml" -o "$atomic_yaml"
   python3 -c "
   import yaml
   with open('$atomic_yaml') as f:
       d = yaml.safe_load(f)
   print('attack_technique:', d['attack_technique'])
   print('number of atomic tests:', len(d['atomic_tests']))
   print('first test name:', d['atomic_tests'][0]['name'])
   "
   rm -f "$atomic_yaml"
   ```
3. Read the first test's `executor.command` and `cleanup_command` fields and write down, in your own
   words, why every atomic test ships a cleanup command — what would go wrong running these
   repeatedly against a test environment without one?
4. Draw the full loop this section has now assembled, end to end: Atomic Red Team test (this link)
   generates telemetry → Attack Range (link 6) is the disposable infrastructure that telemetry lands
   in → a Sigma rule (link 1) or Elastic rule (link 3) is the detection written against that
   telemetry → ATT&CK tags (link 7) let you track coverage across many such rules → Detection-as-Code
   (link 5) is the engineering discipline keeping all of the above versioned and tested.
5. Do NOT actually execute any atomic test command on this machine — per this repo's scope, this
   exercise is fetch-and-parse only, even though the tests are designed to be safe/reversible on a
   disposable environment.

