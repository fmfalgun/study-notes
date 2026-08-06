# 3. SIEM / Detection-Engineering Development — Notes

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 3.

## Sigma — SIEM-agnostic detection-rule spec & repo

**Note on sourcing**: a `git clone --depth 1` of this repo stalled/timed out twice (Sigma's rule
corpus is large even shallow) — flagged here for manual re-check with a longer timeout or
`--filter=blob:none` if a full local clone is wanted later. For this pass, the GitHub REST API
(`api.github.com/repos/...`) and `raw.githubusercontent.com` were used instead to pull metadata and
one real rule file without a full clone — verified working, much faster.

**Claim**: Sigma is a YAML-based, SIEM-agnostic generic signature format for log-based detection
rules — the "write once, convert to any SIEM's query language" layer (via the separate `pySigma`/
`sigma-cli` conversion tooling). Verified via the live repo's directory listing: rules are organized
by log source under `rules/` (e.g. `rules/windows/process_creation/`), with sibling directories for
`rules-emerging-threats`, `rules-threat-hunting`, `rules-compliance`, `rules-dfir`, and a
`deprecated/` archive — over 10,800 GitHub stars, confirming it's a widely-adopted community
standard, not a niche format. A real current rule file (fetched directly,
`proc_creation_win_7zip_password_compression.yml`) shows the canonical structure: `title`/`id`/
`status`/`description`/`references`/`author`/`date` metadata, `tags` mapping to MITRE ATT&CK
technique IDs (`attack.t1560.001` — directly the same taxonomy as section 4's ATT&CK link),
`logsource` (which log category/product the rule applies to — here `process_creation`/`windows`),
`detection` (named `selection_*` blocks combining field-match conditions, joined by a `condition:`
expression — here `all of selection_*` requires every named block to match), `falsepositives` (an
explicit, required field naming what legitimate activity might also trigger this), and a `level`
severity rating.

**Simple explanation**: A Sigma rule is a structured, portable "if you see this pattern in a log,
flag it" statement — the YAML equivalent of a detection use case, written independent of any one
SIEM's query syntax so it can be converted to Splunk SPL, Elastic KQL, Microsoft Sentinel KQL, etc.
by separate conversion tools. The `condition` field is effectively a small boolean expression over
named selection blocks — `all of selection_*` here means every block whose name starts with
`selection_` must match (a 7-Zip process, invoked with a `-p` password flag, doing an add/update
action), which is a compact way to express a multi-clause AND without repeating field names.

**Try it**: Pull a real, current rule directly (no full clone needed) and identify each YAML key's
role:
```fish
curl -s https://raw.githubusercontent.com/SigmaHQ/sigma/master/rules/windows/process_creation/proc_creation_win_7zip_password_compression.yml
```
```
# bash/sh:
curl -s https://raw.githubusercontent.com/SigmaHQ/sigma/master/rules/windows/process_creation/proc_creation_win_7zip_password_compression.yml
```
then browse the repo's directory structure via the GitHub API (works without cloning, verified
fast/reliable when a full clone stalls):
```fish
curl -s "https://api.github.com/repos/SigmaHQ/sigma/contents/" | python3 -c "import json,sys; [print(i['type'], i['name']) for i in json.load(sys.stdin)]"
```
```
# bash/sh:
curl -s "https://api.github.com/repos/SigmaHQ/sigma/contents/" | python3 -c "import json,sys; [print(i['type'], i['name']) for i in json.load(sys.stdin)]"
```

## Mastering Sigma rule-writing (deep dive)

**Claim**: This deep-dive fills in the `condition:` field's actual grammar that link 1's notes only
demonstrated one instance of (`all of selection_*`). The condition language supports: a bare
`selection` (direct pattern match), `1 of selection*` (at least one block in a wildcard-matched
group must match — a looser OR-style quantifier over grouped block names), and full boolean nesting
like `selection1 and (selection2 or selection3)`. It also covers field modifiers beyond plain
equality — `|contains` is used in its own worked example (a suspicious-PowerShell-download rule
matching several substrings in a command line) and a Mimikatz-credential-dumping detection rule
based on command-line pattern matching. Best practices highlighted: tag every rule with MITRE
ATT&CK technique IDs (same `tags: [attack.tXXXX]` convention seen in link 1's real rule), test rules
in non-production before deploying, keep naming conventions consistent, and normalize field names
so a rule stays portable across different log sources/products. Explicitly NOT covered (a real gap
worth knowing before assuming this one article is a complete Sigma reference): aggregation
conditions (counting/thresholding across a time window) and correlation rules (linking multiple
distinct Sigma rules into one multi-stage detection) — these are separate, more advanced Sigma
features not addressed here.

**Simple explanation**: If link 1's notes were "here's what one real rule's fields mean," this is
"here's the fuller grammar for the `condition:` line and a couple more worked examples" — still an
introductory-level piece, not a reference for Sigma's more advanced correlation/aggregation
features (which have their own separate spec pages in the main Sigma docs, not covered by this
particular article).

**Try it**: Extend the toy rule from link 1's exercise using the `1 of selection*` quantifier
instead of `all of selection_*`, and verify the change is still valid YAML — this directly exercises
the condition-grammar gap this article fills in versus link 1's single example.

## Elastic detection-rules repo (build/test/release pipeline)

**Claim**: Where Sigma (links 1-2) is a generic YAML rule format meant to be *converted* to any
SIEM, this repo is Elastic's own **vendor-specific, production rule source** for its Detection
Engine, and demonstrates a fuller "detections as code" pipeline than a bare rule-format spec does.
Verified via GitHub API + raw file fetch (a full clone wasn't attempted after the earlier Sigma
clone stalled — API access confirmed fast and sufficient again): rules are `.toml` files (not YAML),
organized under `rules/<platform>/`, with the actual query written in **KQL** (Kibana Query
Language) or other supported languages, not Sigma's abstracted field-modifier syntax. A real
production rule (`collection_posh_keylogger.toml`, fetched directly) shows a much richer structure
than a Sigma rule: `[metadata]` (maturity, integration, dates), `[rule]` (author, description,
severity/risk_score, the KQL `query`), a long-form `note` field containing a full **investigation
and triage runbook** (numbered investigation steps, false-positive analysis, response/remediation
guidance — written for the human analyst who receives the alert, not just the detection logic
itself), a `setup` field documenting *prerequisite log source configuration* (this rule requires
PowerShell Script Block Logging enabled, event ID 4104 — a rule is only as good as the telemetry
feeding it), and **structured MITRE ATT&CK objects** (`[[rule.threat]]` tables with nested
`technique`/`subtechnique`/`tactic` blocks carrying IDs, names, and reference URLs) rather than
Sigma's flat string tags. The repo's own README confirms this is intentional: "more than just
static rule files... includes code for building Detections-as-code pipelines, unit testing in
Python and integrating with the Detection Engine in Kibana" — `detection_rules/` is a Python module
for parsing/validating/packaging, `tests/` runs unit tests against the rules themselves, and
`kibana/`/`kql/` are libraries for talking to the live product.

**Simple explanation**: Sigma is a detection *language spec*; this repo is what a real vendor's
*production detection pipeline* actually looks like end to end — rules aren't just "if X then
alert," they carry the analyst-facing runbook, the required log-source setup, machine-checkable
unit tests, and a packaging/release process, because a detection rule that fires with no
investigation guidance just generates alert fatigue. This is the concrete difference between
"writing one detection rule" (links 1-2) and "engineering a detection *pipeline*" that this file's
section title promises.

**Try it**: Pull one real rule and compare its structure field-by-field against the toy Sigma rules
already written (link 1-2's exercises) — same underlying goal (detect X, tag it with ATT&CK, ship
it to a SIEM), very different level of operational maturity:
```fish
curl -s https://raw.githubusercontent.com/elastic/detection-rules/main/rules/windows/collection_posh_keylogger.toml | head -30
```
```
# bash/sh:
curl -s https://raw.githubusercontent.com/elastic/detection-rules/main/rules/windows/collection_posh_keylogger.toml | head -30
```
then confirm Python's `tomllib` (stdlib since 3.11, verified present on this machine's Python
3.14.6) can parse it — the TOML equivalent of the earlier `yaml.safe_load` checks, and pull out the
structured MITRE technique IDs to see the nested-table format in action:
```fish
set rule_toml (mktemp -t posh-keylogger.XXXX.toml)
curl -s https://raw.githubusercontent.com/elastic/detection-rules/main/rules/windows/collection_posh_keylogger.toml -o $rule_toml
python3 -c "
import tomllib
with open('$rule_toml', 'rb') as f:
    d = tomllib.load(f)
print('top-level keys:', list(d.keys()))
print('rule name:', d['rule']['name'])
print('MITRE technique IDs:', [t['id'] for entry in d['rule']['threat'] for t in entry['technique']])
"
rm -f $rule_toml
```
```
# bash/sh:
rule_toml=$(mktemp -t posh-keylogger.XXXX.toml)
curl -s https://raw.githubusercontent.com/elastic/detection-rules/main/rules/windows/collection_posh_keylogger.toml -o "$rule_toml"
python3 -c "
import tomllib
with open('$rule_toml', 'rb') as f:
    d = tomllib.load(f)
print('top-level keys:', list(d.keys()))
print('rule name:', d['rule']['name'])
print('MITRE technique IDs:', [t['id'] for entry in d['rule']['threat'] for t in entry['technique']])
"
rm -f "$rule_toml"
```
verified locally: top-level keys `['metadata', 'rule', 'transform']`, rule name "PowerShell
Keylogging Script", MITRE technique IDs `['T1056', 'T1059', 'T1106']` extracted from the nested
`[[rule.threat]]` tables.

## Splunk Developer Platform (SDKs, REST API)

**Partial sourcing note**: `dev.splunk.com` itself is a fully client-side-rendered SPA — both
WebFetch and `curl` returned essentially no body content (just a bare `<title>Splunk Developer
Program</title>`), and a follow-up probe of `docs.splunk.com/Documentation/Splunk/latest/RESTREF`
returned `HTTP 403`. Rather than leave this entirely unverified, the SDK inventory below was
independently confirmed through a different, more reliable channel — the GitHub API against the
`splunk` org — since "which SDKs actually exist" is answerable that way even when the landing page
isn't fetchable. The REST API / app-extension-model portion of the claim below is still
general-knowledge level and not independently verified this session.

**Claim**: the marketing/landing page content is unverified (see flag above), but the actual **SDK
inventory** was independently confirmed via the GitHub API against the `splunk` org (a much more
reliable source than the SPA landing page) — Splunk maintains official SDKs for Python, JavaScript,
Java, Ruby, PHP, C# (plus a portable-class-library C# variant and Xamarin iOS/Android bindings),
and separately a newer **Splunk Cloud** SDK family in JS/TypeScript and Go, distinct from the
classic on-prem Enterprise SDKs. This is more languages than commonly assumed from memory alone
(Ruby and PHP are easy to miss) and confirms the platform has been maintained across a real breadth
of ecosystems, not just Python/Java. Beyond SDKs, the platform's other pillar — the REST API and
the app/add-on extension model (custom search commands, alert actions, modular inputs,
"Technology Add-ons" for field extraction/parsing of new data sources) — remains general-knowledge
level for this entry and should still be checked against Splunk's own REST API reference before
being treated as authoritative.

**Simple explanation**: If Splunk is the SIEM/log-analytics product, this developer platform is
"how you extend it programmatically" rather than just writing searches in its UI — either by
scripting against the running instance from outside (SDKs + REST API) or by packaging new
functionality to install inside it (apps/add-ons/custom commands).

**Try it**: Reproduce the SDK-inventory verification via the GitHub API (verified working, more
reliable than the SPA landing page for this specific question):
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
and separately confirm the SPA problem for yourself before trusting the REST-API/app-model portion
of the claim above:
```fish
curl -sL https://dev.splunk.com/ -o (mktemp -t splunk-dev.XXXX.html)
```
```
# bash/sh:
curl -sL https://dev.splunk.com/ -o /tmp/splunk-dev.html
```

## Detection-as-Code methodology

**Claim**: Traditional SIEM rule management (editing rules through a vendor's web UI) has four
concrete failure modes this article names: no version control on detection logic (changes made
through a UI "get lost or overwritten with no clear traceability"), untested rules shipping
straight to production and causing alert fatigue, difficulty scaling manual per-environment updates
across cloud deployments, and drift between what's actually running and what anyone documented.
Detection-as-Code is the direct application of standard software-engineering discipline to fix
this: rules live in **Git** (audit trail, authorship, rollback — this is literally what the Sigma
and Elastic detection-rules repos from links 1-3 already demonstrate structurally), pass through
**CI/CD** (automated syntax/format validation, plus behavioral validation against known log
samples before merge — the same idea as this file's own `yaml.safe_load`/`tomllib` parse checks,
scaled up to a pipeline), get **code-reviewed** by peers, and share reusable logic instead of
duplicating boilerplate across rules. The **test-driven** workflow specifically: collect real log
samples from a past incident, define what alert(s) should fire against them, then validate a
candidate rule against that fixture set before it ships — directly mirrors `tests/` in the Elastic
detection-rules repo from link 3.

**Simple explanation**: This is "stop treating detection rules as configuration clicked into a web
UI, start treating them as code" — the exact same argument that motivated moving infrastructure
configuration into Terraform/Ansible years ago, applied to SIEM rule management specifically. Every
concrete artifact already inspected in this section (Sigma's YAML rules in a git repo, Elastic's
TOML rules with a `tests/` directory and CI badges in its README) is a real instance of this
methodology already in practice, not just a theoretical pitch.

**Try it**: Connect this methodology directly to what's already been verified hands-on in this
section — write a short paragraph mapping each Detection-as-Code practice named above to the
concrete artifact from links 1-3 that already demonstrates it: version control → (Sigma/Elastic
repos are git repos); automated syntax validation → (this section's own `yaml.safe_load`/`tomllib`
checks on the toy and real rules); testing against known samples → (Elastic's `tests/` directory,
seen in link 3's directory listing); CI → (the Elastic README's "Unit Tests" GitHub Actions badge,
visible in the raw README fetched for link 3).

## Splunk Attack Range (build instrumented environments, feed data into SIEM)

**Claim**: Attack Range solves a different problem than links 1-5 — not "how do I write/validate a
detection rule" but "where do I get realistic attack telemetry to test detection rules *against*."
Verified via the live repo (`splunk/attack_range`, 2536 stars, default branch `develop` — note: the
repo's README is only reachable at `develop`, not `main`, worth remembering for future fetches):
it provisions a small, production-like lab (Splunk + Windows/Linux servers, optionally Kali/Zeek)
across AWS/Azure/GCP via **Terraform** (infra provisioning) + **Ansible** (configuration), then runs
**Atomic Red Team** techniques (this section's link 8) against that lab to generate real attack
telemetry forwarded into Splunk — closing the loop from "detection rule" to "does it actually fire
on realistic data." A genuinely notable detail: access to a running range is shared over a
**WireGuard VPN** — the exact protocol covered in this file's section 1 — confirming the "VPN
protocol development" and "SIEM/detection engineering" halves of this study list aren't unrelated;
a real detection-engineering tool literally depends on VPN tooling for secure remote lab access.
The project ships four interfaces to the same underlying engine: a Docker-Compose-based web app
(port 4321), a REST API with OpenAPI/Swagger docs (port 4000), a CLI (`attack_range.py build
| destroy | simulate | apply-role | share`), all built on the same `templates/{aws,azure,gcp}/`
Terraform templates and per-range YAML configs under `config/`.

**Simple explanation**: This is a disposable, cloud-hosted shooting range — spin up a realistic
mini-network with a real Splunk instance, run real (but controlled/known) attack techniques against
it via Atomic Red Team, watch the telemetry land in Splunk, and use that to build/validate/tune
detection rules against actual log data instead of imagining what an attack "should" look like in
the logs. The WireGuard-for-access detail is a nice full-circle moment for this file: a
detection-engineering tool needs a secure VPN to let its own users reach the lab safely.

**Try it**: Confirm the repo structure and the WireGuard-for-access detail directly rather than
trusting a paraphrase (verified working — note the non-default `develop` branch requirement):
```fish
curl -s "https://api.github.com/repos/splunk/attack_range/contents/" | python3 -c "import json,sys; [print(i['type'], i['name']) for i in json.load(sys.stdin)]"
curl -s "https://raw.githubusercontent.com/splunk/attack_range/develop/README.md" | grep -E -i -n "wireguard|terraform|ansible|atomic red team"
```
```
# bash/sh:
curl -s "https://api.github.com/repos/splunk/attack_range/contents/" | python3 -c "import json,sys; [print(i['type'], i['name']) for i in json.load(sys.stdin)]"
curl -s "https://raw.githubusercontent.com/splunk/attack_range/develop/README.md" | grep -E -i -n "wireguard|terraform|ansible|atomic red team"
```
Note: this repo provisions real cloud infrastructure (AWS/Azure/GCP) when actually run — reading
the repo structure and README (as done here) stays within this repo's coding/analysis scope;
actually running `attack_range.py build` would provision real billable cloud resources and is out
of scope for this exercise.

## MITRE ATT&CK as a data model for SIEM use-case development

**Claim**: This article's core argument is that ATT&CK should be used as an **organizing taxonomy**
for a whole detection *portfolio*, not just a tag on individual rules (which is how it's been used
so far in this section — the `attack.t1560.001` tag on the real Sigma rule in link 1, the
`[[rule.threat]]` tables in the Elastic rule in link 3). Concretely: every rule gets annotated with
its tactic (the adversary's *goal*, e.g. Collection) and technique/sub-technique (the *how*, e.g.
T1560.001 archive-via-utility), specifically preferring the most granular applicable sub-technique
over a broad parent technique. Once every rule in a SIEM is tagged this way, the tag data itself
becomes a **coverage map** — plot which ATT&CK tactics/techniques have detections and which don't,
turning "do we have good detection coverage" from a subjective guess into a queryable heatmap. This
isn't hypothetical: the Sigma repo itself (link 1's directory listing) ships exactly this artifact
at its root — `sigma_attack_nav_coverage.svg`, an ATT&CK Navigator coverage heatmap generated
directly from the `tags:` fields across its thousands of rules, i.e. the real Sigma project already
does at repo-scale what this article describes doing manually. The methodology also specifies
quality control: peer review
that a mapping is *actually correct* (not just plausible), and keeping mappings current as ATT&CK
itself is revised over time (ATT&CK adds/splits techniques periodically).

**Simple explanation**: If each individual Sigma/Elastic rule's ATT&CK tag (already seen in links
1 and 3) is a single data point, this article is about what you can do once you have *many* such
data points: aggregate them into a matrix and immediately see "we have 12 detections for Execution
tactics but zero for Exfiltration" — turning tagging discipline (a small per-rule cost) into a
portfolio-level risk-prioritization tool (a large organizational benefit).

**Try it**: Take the two toy Sigma rules already written (section 3, links 1-2) and the real Elastic
rule inspected (link 3), and build a tiny 3-row coverage table by hand: {rule name, tactic,
technique ID} — this is a miniature version of the exact aggregation this article describes, using
data already gathered in this file rather than a hypothetical example.

## Atomic Red Team (generate telemetry to build/test detections against)

**Claim**: Atomic Red Team is a library of small, self-contained "atomic tests" — one test =
roughly one specific technique or sub-technique from MITRE ATT&CK, executed to generate the exact
telemetry a detection should catch. Verified via the live repo (`redcanaryco/atomic-red-team`,
12,350 stars): tests live under `atomics/<TECHNIQUE_ID>/`, and there's a genuinely satisfying direct
tie-back to this section's link 1 — `atomics/T1560.001/` is the exact technique ID referenced in the
real Sigma rule fetched in link 1 (`proc_creation_win_7zip_password_compression.yml`'s
`references:` field literally links to this technique's atomics page). Fetched directly, the
`T1560.001.yaml` test definition shows the canonical atomic-test structure: `attack_technique` +
`display_name` at the top, then a list of `atomic_tests`, each with a `name`, `description`,
`supported_platforms`, `input_arguments` (parameterized paths/values with sane defaults),
`dependencies` (a `prereq_command` to check if a tool is already installed, plus a
`get_prereq_command` to install it if not), and an `executor` block (the actual command to run,
plus a `cleanup_command` to reverse it afterward). The first `T1560.001` test compresses files with
WinRAR into an archive — i.e. running this atomic test is precisely the behavior the Sigma rule
from link 1 was written to detect, so the two repos form a matched pair: Atomic Red Team generates
the exact telemetry, Sigma/Elastic-style rules are what should fire on it. This closes the loop
Attack Range (link 6) automates at infrastructure scale.

**Simple explanation**: If a Sigma/Elastic rule is a claim ("I will detect X"), an Atomic Red Team
test is the experiment that proves or disproves it ("here's X, actually happening") — every test
comes with a `cleanup_command` specifically so it can be run safely and reversibly against a
disposable test environment, then undone.

**Try it**: Fetch the exact atomic test tied to link 1's Sigma rule and confirm the technique-ID
connection directly instead of trusting the cross-reference claim above:
```fish
curl -s "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1560.001/T1560.001.yaml" | head -20
```
```
# bash/sh:
curl -s "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1560.001/T1560.001.yaml" | head -20
```
validate it parses as well-formed YAML and inspect its top-level structure (same PyYAML check
already used on the toy Sigma rules):
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
Actually *running* an atomic test executes real (if small/reversible) attacker-technique behavior
on the host it runs on — per this repo's coding/analysis-only scope, this exercise stays at
"fetch and parse the test definition," not "execute it," even though the tests themselves are
designed to be safe on a disposable/owned test machine.
