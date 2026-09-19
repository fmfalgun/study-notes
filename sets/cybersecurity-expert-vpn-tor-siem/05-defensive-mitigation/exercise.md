# 5. Defensive / Mitigation Topics (to counter the above) — Exercises

## 1. Detection engineering workflow / Detection as Code

1. Build the local DaC demo (git repo + Sigma rule + pytest tests, no real CI runner needed):
   ```fish
   bash -c '
   mkdir -p /tmp/dac-demo/tests
   cd /tmp/dac-demo
   git init -q
   cat > sudo-bruteforce.sigma.yml << "EOF"
   title: Repeated Sudo Password Prompts From Same User
   id: 8f3c1e2a-0000-4000-8000-000000000001
   status: test
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
   cat > tests/test_sigma_rules.py << "EOF"
   import glob, yaml

   def test_all_sigma_rules_have_required_keys():
       for path in glob.glob("*.sigma.yml"):
           rule = yaml.safe_load(open(path))
           for key in ("title", "logsource", "detection"):
               assert key in rule, f"{path} missing required key: {key}"

   def test_condition_is_present():
       for path in glob.glob("*.sigma.yml"):
           rule = yaml.safe_load(open(path))
           assert "condition" in rule["detection"], f"{path} missing detection.condition"
   EOF
   python3 -m pytest tests/ -v
   git add -A
   git commit -q -m "Add sudo brute-force Sigma rule with tests"
   git log --oneline
   '
   ```
   bash/sh: drop the outer `bash -c '...'` wrapper.
2. Confirm both tests pass, then deliberately remove the `condition:` line from the rule file and
   re-run `python3 -m pytest tests/ -v` from inside `/tmp/dac-demo`. Confirm the test suite now
   fails and reports exactly which rule/key is missing.
3. Explain in 2-3 sentences how this mirrors the article's example GitHub Actions CI job
   (`pip install -r requirements.txt` + `pytest tests/`) — what would be different in a real CI
   pipeline versus this local demo (hint: what triggers the run, and where results get reported)?
4. Explain in 2-3 sentences what "test-driven development" means specifically for detection rules
   (collecting labeled log samples first, then building the rule) — how is this different from
   writing a rule first and hoping it's correct?
5. Clean up: `rm -rf /tmp/dac-demo`. Then write 2-3 sentences on why the article's cited 63%
   want-to-use vs. 35%-actually-use gap likely exists in real organizations — what practical
   barriers (tooling, process change, skill gap) would slow DaC adoption even when teams want it?

## 2. Atomic Red Team

1. Run the real T1082 (System Information Discovery) Linux atomic test — safe, non-destructive,
   self-cleaning:
   ```fish
   set output_file /tmp/T1082_test.txt
   uname -a >> $output_file
   if test -f /etc/os-release
     cat /etc/os-release >> $output_file
   end
   uptime >> $output_file
   cat $output_file
   rm $output_file
   ```
   bash/sh: `output_file=/tmp/T1082_test.txt`, then `if [ -f /etc/os-release ]; then cat
   /etc/os-release >> $output_file; fi`, rest identical.
2. Right after running it, check what this machine's own journal captured:
   ```fish
   journalctl --since "1 minute ago" --no-pager | wc -l
   ```
   bash/sh: identical.
3. Write 2-3 sentences on why T1082 (System Information Discovery) is a notoriously hard
   technique to build a reliable detection for — what does legitimate admin/sysadmin activity
   look like compared to this "attack," and why is there no clean way to tell them apart from the
   commands alone?
4. Explain in 2-3 sentences how running an atomic test like this one closes the loop from section
   3 links 5-6's detection-engineering workflow — specifically, what step ("execute the technique
   in a lab to see its real artifacts") does this exercise satisfy?
5. Explain in 2-3 sentences why Atomic Red Team's own guidance is to run tests only in a
   controlled/isolated environment rather than production — name one plausible higher-impact
   technique category (not T1082) where running the test carelessly could cause real disruption.

## 3. Splunk Attack Range

Scope reminder: no live cloud infrastructure (AWS/Azure/GCP) is deployed for this exercise — that
would incur real cost and requires a live paid cloud account, out of scope per this repo's rules.

1. Inspect the real repo structure via the GitHub API (no clone, no deployment, no cost):
   ```fish
   curl -s "https://api.github.com/repos/splunk/attack_range/contents/" | python3 -c "
   import json, sys
   data = json.load(sys.stdin)
   for item in data:
       print(item['type'], item['name'])
   "
   ```
   bash/sh: identical.
2. Map each of the project's 3 documented workflow steps (Deploy, Simulate, Detect) to the
   directory/file from the listing you think is most responsible for it, with one sentence of
   justification each. Explicitly note any step you can't confidently map from the directory name
   alone.
3. Explain in 2-3 sentences how Attack Range chains together 3 tools already studied in this
   study set (WireGuard for lab access, Atomic Red Team for attack simulation, Splunk for
   detection) into one pipeline — what does automating this chain save a detection engineer from
   doing manually each time?
4. Explain in 2-3 sentences why WireGuard specifically (rather than, say, a commercial VPN
   service) makes sense for this use case — connect back to section 1's WireGuard notes (small
   codebase, fast setup, roaming) and why those properties matter for a disposable lab a team
   needs to spin up and tear down repeatedly.
5. Write 2-3 sentences on why this repo's rules exclude actually deploying Attack Range (real
   cloud cost, live account requirement) even though it would be the most complete way to
   practice this section's detection-engineering workflow end-to-end.

## 4. Writing effective Sigma rules for novices

1. Build the upgraded sudo-brute-force rule (adds `filter`, `fields`, `tags`, `date` on top of
   section 3 link 7's original) and validate it:
   ```fish
   bash -c '
   cat > /tmp/sudo-bruteforce-v2.sigma.yml << "EOF"
   title: Repeated Sudo Password Prompts From Same User (excluding known admin)
   id: 8f3c1e2a-0000-4000-8000-000000000002
   status: test
   date: 2026/08/05
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
     filter_known_admin:
       user: USER
     condition: selection and not filter_known_admin | count() by user > 5
   fields:
     - user
     - src_ip
     - process
   falsepositives:
     - Known administrator running many sudo commands in a legitimate session
   level: low
   EOF
   python3 -c "
   import yaml
   rule = yaml.safe_load(open(\"/tmp/sudo-bruteforce-v2.sigma.yml\"))
   print(\"has filter:\", \"filter_known_admin\" in rule[\"detection\"])
   print(\"has fields:\", \"fields\" in rule)
   print(\"condition:\", rule[\"detection\"][\"condition\"])
   "
   rm /tmp/sudo-bruteforce-v2.sigma.yml
   '
   ```
   bash/sh: drop the outer `bash -c '...'` wrapper.
2. Write 2-3 sentences on why `condition: selection and not filter_known_admin | count() by user
   > 5` produces meaningfully fewer false positives on this specific machine than the original
   version from section 3 link 7, given this study set's own observation (section 3 links 5-6)
   that the known interactive user routinely exceeds 5 sudo prompts per session.
3. List the 6 best practices named in the guide (metadata discipline, precise logsource scoping,
   specific field selection, condition tuning with logical operators, explicit false-positive
   filtering, populated `fields` property) and mark which ones the v2 rule above now satisfies.
4. Explain in 2-3 sentences the difference between documenting a false positive in
   `falsepositives` (informational) versus actively excluding it with a `filter` selection
   (operational) — why does a real SOC need both, not just one?
5. Pick one of the guide's 2 named worked examples (CACTUSTORCH or Cicada3301) and write 2-3
   sentences on what makes combining multiple indicators (e.g. multiple `CommandLine` substrings)
   more precise than matching on any single one alone.

## 5. Mitigating VPN perimeter-device exploitation (patch/hardening guidance)

Note: same source URL as section 4 link 6 — this exercise focuses on the hardening-checklist
angle, not re-covering the CVE/campaign content already exercised there.

1. Run the consolidated local hardening checklist:
   ```fish
   echo "=== Patch/version check ==="
   ipsec version
   wg --version
   echo "=== Config file permission check ==="
   ls -la /etc/swanctl/swanctl.conf
   echo "=== Aggressive Mode posture check ==="
   man 5 swanctl.conf | grep -A3 "connections.<conn>.aggressive"
   echo "=== Protocol version exposure check ==="
   man 5 swanctl.conf | grep -A4 "connections.<conn>.version \[0\]"
   ```
   bash/sh: identical.
2. Write a 5-7 line hardening report in real-audit-finding style: one line per check (patch
   version, config permissions, aggressive mode default, protocol version default), stating what
   was verified, the current state, and pass/needs-attention against the NCSC alert's guidance.
3. Map each of the alert's 6 mitigation categories (patch, reset credentials, review config
   for changes, enable MFA, monitor logs, consider factory reset) to a specific prior link in
   this study set that covered the underlying weakness it addresses (e.g. "reset credentials" ->
   section 4 link 7's shared-PSK research, section 4 link 4's Aggressive-Mode PSK cracking).
4. Explain in 2-3 sentences why MFA is described as limiting "blast radius" rather than
   preventing credential theft outright — what attack from section 4 (e.g. the NTDS.dit/Kerberos
   chain in link 3) does MFA NOT stop, and what does it stop instead?
5. Explain in 2-3 sentences why "consider a factory reset" is a notably stronger recommendation
   than most organizations' default incident response posture — what specific risk does a
   config-only cleanup fail to address that a full reset does?

## 6. Tor Project guidance on traffic-correlation mitigations

Note: same URL as section 4 link 8 — this exercise focuses only on the mitigation/design-guidance
angle of that post, not re-covering the base-rate-fallacy attack math already exercised there.

1. Run the mitigation-model comparison:
   ```fish
   python3 -c "
   print('VPN mitigation model (NCSC alert, link 5): user/admin-actionable')
   print('  - patch, rotate credentials, review config, enable MFA, monitor logs, factory reset')
   print()
   print('Tor mitigation model (this post): architectural/probabilistic, not user-configurable')
   print('  - guard stickiness (bounds one-time selection risk instead of eliminating it)')
   print('  - future design research (raise attacker false-positive rate) -- not a shipped control')
   "
   ```
   bash/sh: identical.
2. Explain in 2-3 sentences the guard-stickiness mitigation logic: why does keeping the *same*
   guard relay over time bound an adversary's odds of ever being selected, compared to rotating
   guards per-circuit (which would let the adversary just wait for a match)?
3. Explain in 2-3 sentences what the post means by floating "simple, not too burdensome tricks"
   to raise an attacker's false-positive rate — is this a shipped Tor feature or an open research
   direction? What does the honest hedging in that phrasing tell you about how settled this
   problem is?
4. Write 3-4 sentences contrasting the VPN/NCSC checklist mitigation model with Tor's
   architectural mitigation model — what can a Tor *user* personally do to harden their own
   circuit selection, compared to what a VPN admin can do to harden a gateway config?
5. Write a closing 4-6 sentence summary of this entire study set's throughline across sections
   4-5: pick 3 specific weaknesses studied in section 4 (e.g. Aggressive Mode PSK cracking,
   shared commercial-VPN PSKs, Tor traffic correlation) and connect each to the specific
   defensive/detection concept from section 5 that would catch or mitigate it (Sigma detection
   rules, Detection as Code testing, Atomic Red Team validation, or Tor's own architectural
   defaults).
