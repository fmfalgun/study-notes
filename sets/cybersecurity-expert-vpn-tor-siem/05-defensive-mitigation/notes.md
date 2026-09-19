# 5. Defensive / Mitigation Topics (to counter the above) — Notes

## Detection engineering workflow / Detection as Code (Splunk blog)

**Claim** (fetched via `curl` + tag-stripping): Detection as Code (DaC) is the practice of treating
detection rules (SIEM rules, WAF filters, alert conditions) as software — written in a structured
format (YAML or Python, exactly matching Sigma's own format from section 3 link 7), stored in a
version-controlled repo (Git), and tested/deployed through a CI/CD pipeline (GitHub Actions/GitLab
CI) — rather than built ad hoc through a SIEM's UI with no ownership trail. The article names 5
concrete engineering practices this brings to detection logic: **reusable components** (shared
lookup tables/functions instead of rewriting logic per rule — mirrors how Sigma rules can share
common field-mapping conventions); **CI/CD and automated testing** (lint rule syntax, validate
against known log samples, block broken rules before they reach production — with a literal
example GitHub Actions job given: checkout -> `pip install -r requirements.txt` -> `pytest
tests/`); **version control** (Git as the single source of truth, enabling audit trails and
rollback — something a UI-built SIEM rule has none of); **test-driven development** — collect
real log events from past incidents or attack simulations (directly foreshadowing this section's
next link, Atomic Red Team), label which should/shouldn't trigger, then build and validate the
rule against those labeled samples, the security-detection equivalent of unit tests; and
**automation/integration** into existing dev pipelines so rule updates ship as fast and safely as
application code. Adoption gap cited: 63% of security professionals want to use DaC frequently,
but only 35% actually do today — a real, sizeable practice-vs-intent gap.

**Simple explanation**: DaC is applying ordinary software engineering discipline (version control,
automated tests, code review via pull requests) to detection rules instead of clicking through a
SIEM's web UI and hoping nobody accidentally breaks or forgets why a rule exists. Sigma rules
(section 3 link 7) are inherently DaC-compatible by design — they're already YAML files meant to
live in a Git repo — this article explains the *process* around that file format, not a
competing concept.

**Try it**: Build a minimal, real, working DaC pipeline locally — a git repo containing a Sigma
rule (reusing section 3 link 7's rule), plus a pytest-style test validating it, demonstrating the
"lint and test rules" CI step described above without needing an actual GitHub Actions runner.
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
python3 -m pytest tests/ -v 2>&1 | tail -15
git add -A
git commit -q -m "Add sudo brute-force Sigma rule with tests"
git log --oneline
'
rm -rf /tmp/dac-demo
```
bash/sh: drop the outer `bash -c '...'` wrapper, run the inner lines directly.
Applied exercise: verify all tests pass, then deliberately break the rule (remove the `condition`
key) and re-run `pytest` to confirm the test suite catches it — this is exactly the "prevent
broken rules from reaching production" CI behavior the article describes, demonstrated end-to-end
locally.

## Atomic Red Team (simulate attacks to validate detections)

**Claim**: Atomic Red Team (Red Canary) is a library of 1,817 "atomic tests" — small, individual,
portable technique simulations, each mapped to a specific MITRE ATT&CK technique ID — organized
one YAML file per technique under an `/atomics/` directory. This is the concrete tool the
detection-engineering workflow described across section 3 links 5-6 and this section's link 1
kept pointing to: "execute the technique in a controlled lab... to identify the exact artifacts it
produces" *is* running an Atomic Red Team test and watching what it generates in your logs. Each
test in a technique's YAML has: a `name`/`description`, `supported_platforms` (windows/macos/
linux), an `executor` block specifying the actual command(s) to run and which shell runs them, and
often a `cleanup_command` that undoes the test's effects afterward. Verified directly by fetching
the real T1082 (System Information Discovery) test file: it contains multiple platform-specific
variants, including a Linux one using entirely benign, standard commands (`uname -a`, reading
`/etc/os-release`, `uptime`) that write to an output file and then explicitly clean up after
themselves via `rm`. Not every atomic test is this benign — many simulate genuinely
higher-impact techniques — which is precisely why the project's own guidance is to run tests only
in a controlled/isolated environment, never against production or a system you don't own.

**Simple explanation**: Atomic Red Team is a library of "here's exactly what technique X looks
like when it actually runs" scripts, one per ATT&CK technique, specifically built so a defender
can generate the real log artifacts a technique produces and then check whether their detection
rules actually catch it — closing the loop between "we have a Sigma rule for T1082" and "we've
actually verified that rule fires."

**Try it**: Run the real T1082 (System Information Discovery) Linux atomic test directly — this
specific technique is Discovery-category and entirely non-destructive (reads and displays system
info, no modification of anything beyond a temp file it cleans up itself), making it safe to run
literally as designed, consistent with this repo's boundary (a real, intentionally-safe test from
the project itself, not a live attack against any target).
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
bash/sh: `output_file=/tmp/T1082_test.txt` replaces the `set` line; the `if test -f ...; ... end`
block becomes `if [ -f /etc/os-release ]; then cat /etc/os-release >> $output_file; fi` — rest
identical.
Applied exercise: while running the test above, in a second terminal watch `journalctl -f` (or
just re-run `journalctl --since "1 minute ago"` right after) to see what, if anything, this
benign command sequence actually logs on this machine — then write 2-3 sentences on why a real
System Information Discovery technique (e.g. malware profiling its environment) would likely
generate *no* distinctive log signal at all using only these commands, which is exactly why T1082
is a notoriously hard technique to detect reliably (legitimate admin activity looks identical).

## Splunk Attack Range (instrumented lab to test detections)

**Claim**: Attack Range is the full-scale, cloud-hosted version of the local pytest-based DaC
demo (link 1) and the T1082 atomic test (link 2) combined into one pipeline: it stands up an
**instrumented cloud lab** (AWS/Azure/GCP, provisioned via Terraform, configured via Ansible) with
real Windows and Linux hosts, **integrates Atomic Red Team directly** to simulate attack
techniques against those hosts, and **forwards the resulting telemetry into Splunk** so a
detection engineer can write and validate real SPL detections against real (if lab-generated)
attack artifacts — the literal "execute the technique in a controlled lab" step named repeatedly
across section 3 links 5-6 and this section's links 1-2, fully automated end to end. Confirmed
directly from the live repo's top-level structure: dedicated `terraform/` (infrastructure
provisioning), `attack_data/` (presumably pre-captured/sample telemetry), `capattack/`, `app`/`api`
(the web UI on port 4321 and REST API on port 4000 mentioned in the fetch), and `docker/`
(Docker Compose deployment path). Notably, it uses **WireGuard VPN** (section 1 links 2-3 of this
study set) specifically for secure remote access to the lab and for sharing lab access across a
team — a direct, concrete real-world application of a protocol already studied in depth earlier
in this repo.

**Simple explanation**: If Atomic Red Team is "the individual attack-simulation scripts" and
Splunk is "the tool you write detections in," Attack Range is "the disposable, real, cloud-hosted
practice range that wires the two together automatically" — deploy a lab, run atomic tests
against it, watch the telemetry land in Splunk, write/tune detections, tear the lab down.

**Try it**: This tool provisions real, billed cloud infrastructure (AWS/Azure/GCP) — deploying it
live is explicitly out of scope per this repo's no-live-paid-cloud-account rule. The available,
safe substitute is inspecting the project's real structure/architecture via the GitHub API (no
clone, no deployment, no cost) to understand what it automates, which is the useful conceptual
takeaway without needing to run it.
```fish
curl -s "https://api.github.com/repos/splunk/attack_range/contents/" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data:
    print(item['type'], item['name'])
"
```
bash/sh: identical.
Applied exercise: from the directory listing, identify which directory most likely corresponds to
each of the 3 workflow steps named in the project's own docs (Deploy -> `terraform/`/`docker/`;
Simulate -> likely inside `attack_range/` or a scripts dir referencing Atomic Red Team; Detect ->
`app`/`api` for the Splunk-facing UI) — write one sentence justifying each mapping from the
directory name alone, then note which ones you can't confidently map without reading further
(honest uncertainty is fine here — the point is practicing structural inference, not guessing).

## Writing effective Sigma rules for novices (dogesec blog)

**Claim**: This guide gives concrete best practices for turning a *structurally valid* Sigma rule
(section 3 link 7's bar — has the 3 required keys, parses correctly) into a *genuinely useful*
one — precisely the gap this study set's own hand-written rule hasn't closed yet. Named practices:
(1) **metadata discipline** — descriptive title, creation/modification dates, standardized ATT&CK
tags (already applied in section 3 link 8's exercise); (2) **precise logsource scoping** —
specify exact `product`/`category`/`service` rather than matching "anywhere" in a log, since an
overly broad logsource inflates false positives by matching irrelevant log types; (3) **specific
field selection** — match named fields from Sigma's standard taxonomy rather than searching raw
message text (this study set's own rule uses `message|contains`, a broad-message match — the
guide's advice would push toward a more specific field if the log source exposed one); (4)
**condition tuning with logical operators** — the guide's own example, `all of selection_1 and 1
of selection_2`, shows combining multiple named selections with AND/OR/parentheses/negation
produces materially more precise detections than one flat condition; (5) **explicit false-positive
mitigation** — not just documenting known-benign triggers in `falsepositives`, but actively adding
a `filter` selection (subtracted from the main condition) to exclude expected legitimate activity
— its own example: filtering out administrator accounts to prevent alert fatigue, directly
relevant to this study set's repeated "known interactive user on a single-user dev machine" false
positive discussed in section 3 links 5-6; (6) **a populated `fields` property** — listing exactly
which log fields an analyst should look at first when triaging a fired alert, speeding up triage.
Two real named worked examples: a CACTUSTORCH detection via process-image analysis, and a
Cicada3301 ransomware detection combining multiple `CommandLine` indicators with a PSExec-specific
filter.

**Simple explanation**: A Sigma rule that merely parses is like code that merely compiles — it
doesn't mean it's *good*. This guide is the difference between "technically valid YAML" and "a
rule a real SOC would actually want running," and its concrete example (filtering known-admin
accounts) is exactly the noise-reduction problem this study set's own sudo rule has had unresolved
since section 3.

**Try it**: Apply these exact principles to upgrade the sudo-brute-force rule already built and
validated in section 3 link 7 / this section's link 1 — adding a `filter` selection for the known
benign case, per the guide's own worked pattern.
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
bash/sh: drop the outer `bash -c '...'` wrapper, run the inner lines directly.
Applied exercise: write 2-3 sentences on why `condition: selection and not filter_known_admin |
count() by user > 5` is a meaningfully better rule for this specific machine than the original
version from section 3 link 7 — what alert volume reduction would you expect in practice, given
this study set's own observation that the known user routinely exceeds 5 sudo prompts per session?

## Mitigating VPN perimeter-device exploitation (patch/hardening guidance)

**Note**: this link uses the exact same URL as section 4 link 6
(`ncsc.gov.uk/news/alert-vpn-vulnerabilities`) — the source list places it here again specifically
for its **mitigation-guidance angle**, so this entry deliberately does not re-summarize the same
alert content already covered in section 4 link 6 (the 5 CVEs, the APT campaign, the sector
targeting). Instead it focuses on turning that alert's 6-step mitigation list into concrete,
actionable hardening practice — the "what do I actually configure" half the earlier entry didn't
drill into.

**Claim**: Perimeter-device hardening, generalized from the alert's guidance plus this study
set's own already-verified tooling, breaks into layers that map directly onto configuration
surfaces already inspected in sections 1 and 4: **patch management** (verifiable via version
checks — `ipsec version`, `wg --version`, already demonstrated in section 4 link 6); **credential
hygiene** (rotate PSKs/certs on any device that had a pre-auth exposure — directly connects to
section 4 link 4's Aggressive-Mode PSK-cracking risk and section 4 link 7's shared-PSK research
finding); **configuration integrity** (file permissions and change tracking on config files —
`/etc/swanctl/swanctl.conf`'s 0640 root-owned permissions, already inspected in section 1 link 6,
are exactly this kind of control); **MFA enforcement** (an orthogonal control that limits blast
radius even if a credential leaks — relevant directly to section 4 link 3's NTDS.dit/Kerberos
material, since MFA doesn't stop credential theft but does stop simple replay); **log-based
anomaly monitoring** (geolocation/connection-pattern monitoring — directly the kind of detection
this entire section 5 and section 3 have been building via Sigma rules); **assume-compromise
posture** (the alert's "consider factory reset" step) — a stronger stance than most orgs default
to, reflecting how thoroughly a pre-auth perimeter bug can compromise a device's trust.

**Simple explanation**: This is the "how do I actually harden a VPN gateway" checklist implied by
everything the attack-focused entries in section 4 described — every mitigation here maps to a
specific weakness this study set has already examined concretely (Aggressive Mode PSKs, shared
provider PSKs, pre-auth cert-check bypass, config file permissions).

**Try it**: Build a concrete hardening checklist for this machine's own real strongSwan/WireGuard
installs, applying the alert's 6 mitigation categories to actual, verifiable local checks —
consolidating checks already run individually across sections 1 and 4 into one audit pass.
```fish
echo "=== Patch/version check ==="
ipsec version
wg --version
echo "=== Config file permission check ==="
ls -la /etc/swanctl/swanctl.conf
echo "=== Aggressive Mode posture check (section 4 link 4) ==="
man 5 swanctl.conf | grep -A3 "connections.<conn>.aggressive"
echo "=== Protocol version exposure check (section 4 link 5) ==="
man 5 swanctl.conf | grep -A4 "connections.<conn>.version \[0\]"
```
bash/sh: identical.
Applied exercise: run the consolidated checklist above and write a short (5-7 line) hardening
report in the same style as a real security audit finding — one line per check: what was
verified, current state, and pass/fail/needs-attention against the NCSC alert's guidance.

## Tor Project guidance on traffic-correlation mitigations

**Note**: same URL as section 4 link 8 (`blog.torproject.org/traffic-correlation-using-netflows/`)
— that entry covered the attack-side content (traffic analysis vs. confirmation, base-rate
fallacy math). This entry deliberately focuses only on the parts of that same post that are
mitigation/design-guidance-relevant, and is honest about a real limitation: **the post is
fundamentally analytical, not a prescriptive mitigation checklist** — Tor Project's own response
to correlation attacks is architectural (baked into client design) rather than a list of user
actions, unlike the NCSC alert's actionable checklist in the previous link.

**Claim**: Two mitigation-relevant threads from the post, both already partially covered
elsewhere in this study set and consolidated here: (1) **Guard node stickiness** — a client keeps
the *same* guard relay for an extended period rather than randomizing per-circuit (already raised
as an open question in section 2 link 2's exercise). The post's implicit mitigation logic: if
guards rotated per-circuit, a client would eventually route through an adversary-controlled guard
with high probability given enough circuits over time (the adversary just waits); sticking with
one guard bounds the adversary's odds of *ever* being selected as your guard to roughly "is my
one guard malicious," a one-time risk instead of a repeated one. (2) **Driving up false-positive
rates as a design direction** — the post explicitly floats (without committing to specifics)
"simple, not too burdensome tricks" to increase an attacker's false-positive rate even in
small-sample cases, name-checking this as future design-improvement territory rather than a
shipped mitigation — an honest acknowledgment that Tor's defense against correlation is
fundamentally probabilistic/architectural (make the attacker's math harder), not something a user
can configure away, unlike a VPN's actionable PSK-rotation or patch-management steps.

**Simple explanation**: Unlike a VPN vendor's "patch this, rotate that" mitigation list, Tor's own
defense against its own worst-case attack (traffic confirmation) is baked into client design
choices like guard stickiness — there's no user-facing setting to "turn on correlation
resistance." The real, honest mitigation story here is architectural and probabilistic, not a
checklist a user runs through.

**Try it**: Since this post gives no concrete user-actionable mitigation commands (an honest,
important observation in itself), the applied exercise is contrasting Tor's architectural
mitigation model against the NCSC alert's actionable-checklist model from the previous link,
using facts already gathered across this study set.
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
Applied exercise: write 3-4 sentences on why a probabilistic/architectural mitigation model
(Tor) is fundamentally different from a checklist mitigation model (VPN/NCSC) — what does it mean
for a *user* of Tor that they cannot personally "harden" their circuit selection the way a VPN
admin can harden a gateway config, and why does that make Tor's own client-side defaults matter
so much more than user behavior?
