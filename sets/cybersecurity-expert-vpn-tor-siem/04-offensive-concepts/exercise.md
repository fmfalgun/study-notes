# 4. Offensive Concepts You Must Be Aware Of — Exercises

Scope note: same safety boundary as notes.md — every exercise below is explain/detect/lab-locally
only, never an instruction to scan, exploit, or target a real device/network/service that isn't
your own throwaway local test setup.

## 1. MITRE ATT&CK — Defense Evasion tactic (TA0005, now named "Stealth")

1. Fetch the live tactic page and confirm the current name/technique count:
   ```fish
   curl -sL -A "Mozilla/5.0" https://attack.mitre.org/tactics/TA0005/ -o /tmp/ta0005.html
   python3 -c "
   import re, html
   text = open('/tmp/ta0005.html').read()
   text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
   text = re.sub(r'<[^>]+>', ' ', text)
   text = html.unescape(text)
   text = re.sub(r'\s+', ' ', text)
   idx = text.find('Techniques: 30')
   print(text[idx:idx+600])
   "
   rm /tmp/ta0005.html
   ```
   bash/sh: identical. Verified on this machine: TA0005 is now titled "Stealth," last modified 12
   May 2026, with 30 techniques.
2. Write TA0005/Stealth's own definition from the fetch in your own words (1-2 sentences), and
   specifically note what it says it does NOT cover (tampering with security controls or
   monitoring feeds themselves) — this sets up links 2-3 of this section.
3. Explain T1134 Access Token Manipulation in 2-3 sentences: what a Windows access token actually
   represents, and how duplicating/spoofing one lets an attacker act with a different identity
   without needing that identity's password.
4. Explain T1134.004 Parent PID Spoofing specifically: what field does it fake, and why does that
   defeat a naive "flag unusual parent-child process relationships" detection rule?
5. Write a Sigma-style detection sketch (reuse the 3-required-key format from section 3 link 7)
   targeting Parent PID Spoofing — `logsource` should reference process-creation telemetry (e.g.
   Sysmon Event ID 1), and `detection` should describe (in the `description` field, since a real
   EDR-vs-reported-PPID mismatch check needs sensor-specific fields this toy rule can't fully
   express) what an EDR would need to cross-check to catch a spoofed PPID that a naive log-based
   rule would miss.

## 2. Defense evasion detection/response guide (ManageEngine)

1. List the 6 key techniques named with their IDs (Masquerading T1036, Obfuscated Files or
   Information T1027, Indicator Removal T1070, Process Injection T1055, Modify Registry T1112,
   Hide Artifacts T1564) and write one sentence per technique on what it conceals or removes.
2. Explain in 2-3 sentences why the article says most defense-evasion techniques "exploit trust
   relationships that already exist in the OS" rather than novel vulnerabilities, using the
   `Rundll32` example (legitimate library loading vs. malicious DLL loading looking identical).
3. Write 2-3 sentences on the 194-day average dwell time statistic cited (2025 IBM Cost of a Data
   Breach Report) and why the article argues defense evasion specifically (not just "attackers
   being clever") is the primary reason that number stays high.
4. Baseline this machine's own journal activity rate as a stand-in for "what does normal log
   volume look like" (the prerequisite for detecting *absence* as a signal):
   ```fish
   journalctl --no-pager --since "10 minutes ago" | wc -l
   ```
   bash/sh: identical.
5. Write a Sigma-style rule sketch for an absence-based detection ("EDR agent / auditd goes
   silent for 15 minutes") and explain in 2-3 sentences why this needs a scheduled "did X NOT
   happen" query rather than the normal per-event content-match pattern used in every other
   Sigma rule written so far in this study set.

## 3. Log/AD database tampering case study

Scope reminder: this is documentation research and detection-rule sketching only — never run any
of the described techniques against a real domain controller or any system you don't own.

1. Explain in 2-3 sentences why `NTDS.dit` is described as "whoever controls NTDS.dit controls
   the domain" — what specifically does the file contain?
2. Build the technique table: for each of the 4 named techniques (Install-From-Media via
   `ntdsutil.exe`, Ninja-Copy via VSS, PowerShell Kerberos ticket extraction, PowerShell
   MiniDump of LSASS), fill in columns: Windows tool/API abused | What legitimate purpose that
   tool/API normally serves | Why abusing it evades naive detection.
3. Reproduce the attack-chain table from the notes (Initial Access -> Privilege Escalation ->
   Credential Access -> Lateral Movement) with each stage's MITRE technique ID, and write one
   sentence per stage on what has to be true for the attacker to reach it (e.g. Privilege
   Escalation to Domain Admin/SYSTEM is the actual gating requirement — nothing after it is
   possible without it).
4. Explain Pass-the-Hash vs. Pass-the-Ticket in 2-3 sentences each: what's being replayed in each
   case, and why neither requires knowing the victim account's actual password.
5. Explain in 2-3 sentences why VSS-based extraction ("Ninja-Copy") specifically defeats a
   detection strategy that only monitors direct reads/writes to the live `NTDS.dit` file path —
   what does reading from the shadow-copy path sidestep?

## 4. IPsec/IKE VPN pentesting methodology

Scope reminder: no pentesting tool (`ike-scan`, `ikeforce`, `hashcat`, `fiked`) is installed or
run against anything, including localhost, for this exercise — documentation research and
defensive verification only.

1. Confirm strongSwan's own documentation states the exact risk this methodology exploits:
   ```fish
   man 5 swanctl.conf | grep -i -B2 -A6 "aggressive"
   ```
   bash/sh: identical. Verified here: default is `no` (Main Mode), man page explicitly warns about
   identity snooping and PSK dictionary attacks under Aggressive Mode.
2. Explain in 2-3 sentences why Aggressive Mode has to send the peer's identity before the crypto
   channel exists (hint: the gateway needs to know which PSK to try — what would it look up the
   PSK by, if not the identity?).
3. Explain the difference between what `nmap -sU -p 500` discovers versus what `ike-scan`
   discovers — write one sentence per tool on what question each answers (service presence vs.
   accepted crypto transform/PSK usage).
4. Write 2-3 sentences on why a cracked PSK is dangerous beyond just the VPN itself (hint: PSK
   reuse across services named in the source: SSH, other VPN clients).
5. Write a Sigma-style detection sketch (reusing section 3 link 7's format) for "IKE Aggressive
   Mode exchange observed" — explain in the rule's `description` field why detecting the mode
   itself (not waiting for a successful crack) is the right defensive posture.

## 5. Real-world critical IKEv1 auth-bypass exploitation (CVE-2026-50751)

Scope reminder: root-cause analysis and defensive auditing only — no attempt to reproduce this
bypass against any Check Point deployment or any other target.

1. Write down the 4 key facts: CVE ID, CVSS score, affected product/protocol, root cause
   (certificate validation skip via `VPNExtFeatures` Vendor ID payload manipulation).
2. Explain in 2-3 sentences why "skips `verify_peer_auth` entirely" is categorically worse than a
   weak-but-present check (e.g. a weak PSK, as in link 4) — what's the difference between an
   attack that requires cracking something vs. one that requires nothing at all?
3. Check this machine's strongSwan documentation for the protocol-version setting relevant to
   this CVE's lesson (legacy protocol exposure):
   ```fish
   man 5 swanctl.conf | grep -i -B2 -A4 "^ *connections.<conn>.version"
   ```
   bash/sh: identical. Note the default (`0`) still *accepts* IKEv1 as a responder even though it
   actively initiates with IKEv2 — write 1-2 sentences on why that asymmetry matters for exposure.
4. Write 4-6 sentences summarizing the root cause in your own words: what the crafted Vendor ID
   payload does, and why it results in a complete bypass rather than a partial weakening.
5. Name one mitigation beyond simply patching (hint: disabling IKEv1 entirely where IKEv2-only
   interop is feasible) and explain in 1-2 sentences why that specific mitigation would have
   prevented exploitation even before Check Point's hotfix existed.

## 6. NCSC alert on exploited VPN vulnerabilities

1. List the 5 named CVEs with vendor and one-line description each (Pulse Connect Secure x2,
   Fortinet x3, Palo Alto GlobalProtect x1).
2. Explain in 2-3 sentences what makes "pre-authentication" vulnerabilities specifically dangerous
   for a perimeter VPN gateway (hint: what's the whole point of authentication as a boundary, and
   what happens when the vulnerability is reachable before that boundary is even checked?).
3. Run the version-check stand-in exercise:
   ```fish
   ipsec version
   wg --version
   ls -la /etc/swanctl/swanctl.conf
   ```
   bash/sh: identical.
4. Write out, for each of the alert's 6 mitigation steps (patch, reset credentials, review config,
   enable MFA, monitor logs, consider factory reset), one concrete "how would I verify this is
   actually done" check for a real strongSwan/WireGuard deployment.
5. Explain in 2-3 sentences why the alert recommends resetting credentials as a *separate* step
   from patching — what specific risk does patching alone fail to address if a pre-auth
   credential-exposure bug was live before the patch was applied?

## 7. Client-side vulnerabilities in commercial VPNs (arXiv 1912.04669)

Scope reminder: configuration-auditing only — no fake VPN server, no MitM, no reproduction of the
paper's own experimental methodology against any target.

1. Download and extract the actual paper (source-of-truth, not a summary):
   ```fish
   curl -sL https://arxiv.org/pdf/1912.04669 -o /tmp/vpn-clientside.pdf
   pdftotext -l 5 /tmp/vpn-clientside.pdf - | head -60
   rm /tmp/vpn-clientside.pdf
   ```
   bash/sh: identical.
2. Explain in 2-3 sentences the shared/public PSK finding: what makes a PSK like `"12345678"`
   shared across every customer of a provider functionally equivalent to having no authentication
   at all?
3. Explain in 3-4 sentences the PPTP optional-encryption downgrade attack: what does the attacker
   do during the authentication phase, and why does the client agree to disable encryption during
   data exchange without warning the user?
4. Run the structural audit checks against this machine's real VPN tooling:
   ```fish
   man 5 swanctl.conf | grep -i -B1 -A5 "psk"
   man 8 wg-quick | grep -iE "cipher|encrypt|protocol ="
   ```
   bash/sh: identical. Note what the second command's (near-)empty output itself demonstrates
   about WireGuard's design (link 2 of section 1: no negotiable cipher suite to downgrade).
5. Write a 5-item audit checklist a defender could apply when evaluating any commercial VPN
   provider before trusting it, derived from this paper's 2 headline findings (shared PSKs,
   optional/downgradable encryption) — make each item concrete and checkable, not vague.

## 8. Tor traffic correlation / de-anonymization attacks

1. Explain in 2-3 sentences the difference between traffic *analysis* (what Tor defends against)
   and traffic *confirmation*/end-to-end correlation (what Tor explicitly does not defend
   against) — what does each attacker already know or not know at the start?
2. Explain in 1-2 sentences why Tor doesn't add the heavy delay/padding that would defeat
   correlation attacks (hint: what would that cost, and why would it break Tor's actual use case
   compared to a high-latency mix network like Mixmaster)?
3. Run and extend the base-rate fallacy calculation:
   ```fish
   python3 -c "
   for fpr in [0.06, 0.01, 0.001, 0.00001]:
       total_flows = 100000
       false_positives = total_flows * fpr
       print(f'FPR {fpr*100}%: {false_positives:.1f} false positives out of {total_flows} flows')
   "
   ```
   bash/sh: identical. Write 2-3 sentences on what FPR would actually be needed for a correlation
   attack to be practical against the real Tor network (millions of daily flows), not just a
   lab-scale test of a few hundred/thousand.
4. Explain in 2-3 sentences what "how much of the Internet the adversary can measure or control"
   has to do with whether a correlation attack is even possible in the first place — this sets up
   the AS-level-adversary link later in this section.
5. Write 2-3 sentences on the post's caution about contemporaneous arrests being attributed to
   "bad opsec," not correlation attacks — why does this matter for how a SOC analyst or threat
   modeler should weigh a flashy theoretical attack against more mundane real-world causes when
   assessing actual risk?

## 9. Thirteen years of Tor attacks (catalog)

1. Print and review the 7-category taxonomy:
   ```fish
   python3 -c "
   categories = {
       'Correlation': 'passive, needs both entry+exit visibility',
       'Congestion': 'active, injects delay to create a timing signature',
       'Timing': 'active, manipulates flow patterns directly',
       'Fingerprinting': 'passive, needs only one-side traffic shape (no both-ends visibility)',
       'Denial of Service': 'active, disrupts network, can force traffic onto adversary relays',
       'Supportive': 'preparatory, enables other categories rather than deanonymizing alone',
       'Revealing Hidden Services': 'targets the SERVER behind an onion service, not the client',
   }
   for name, desc in categories.items():
       print(f'{name}: {desc}')
   "
   ```
   bash/sh: identical.
2. For each of the 7 categories, write one sentence identifying which prior link in this study
   set connects to it most directly (Correlation -> link 8; Revealing Hidden Services -> section
   2 links 3-4), and explicitly flag the categories with no prior direct connection as new ground
   this catalog covers.
3. Explain in 2-3 sentences why Fingerprinting Attacks are arguably more practical for a real
   adversary than Correlation Attacks — what visibility does an attacker need for each, and why
   is one requirement much easier to obtain than the other (single guard-side vantage point vs.
   both entry+exit)?
4. Explain in 2-3 sentences what the Raptor attack exploits (BGP routing weaknesses) and how that
   connects to link 8's "how much of the Internet can the adversary measure or control" gating
   factor for correlation attacks.
5. Explain in 1-2 sentences the practical difference between a "Supportive" attack and every other
   category — why would an attacker need one before attempting, say, a correlation attack?

## 10. De-anonymisation attacks on Tor: a survey

Note: the ResearchGate URL from the source list is hard-blocked (HTTP 403 / Cloudflare error
1020) — the same paper is freely available on arXiv at `2009.13018` and was used instead.

1. Fetch the actual paper and verify the two cross-referenced technical claims:
   ```fish
   curl -sL https://arxiv.org/pdf/2009.13018 -o /tmp/tor-survey.pdf
   pdftotext -f 4 -l 5 /tmp/tor-survey.pdf - | grep -i -B2 -A2 "six-hop\|AES-CTR"
   rm /tmp/tor-survey.pdf
   ```
   bash/sh: identical.
2. Write 3-4 sentences on why finding the same specific claim (6-hop hidden-service circuit)
   stated independently in two different primary sources (section 2 link 3's Tor Project docs,
   and this academic survey) is stronger evidence than either source alone.
3. Explain in 1-2 sentences what AES-CTR-128 is doing in the Tor relay-cell encryption pipeline,
   and how it connects to the layered "onion" encryption concept from section 2 link 1 (each
   relay decrypts one layer — what cipher mode makes that per-hop peeling practical).
4. List the 3 prior surveys this paper explicitly improves on (Salo 2010, Nepal et al. 2015,
   Erdin et al. 2015) and write one sentence per each on the specific gap this new survey fills
   (HS attacks, website fingerprinting, or attack-count coverage).
5. Explain in 2-3 sentences why this paper's stated goal of tracking "which Tor hardening
   improvements have made previously-viable attacks infeasible over time" matters for a security
   practitioner reading attack research — why is attack age/publication date directly relevant to
   whether a described technique still works against the current Tor network?

## 11. Deep-learning flow correlation attack (DeepCorr)

Scope reminder: quantitative/comparative analysis only — no traffic correlation attempted against
real Tor traffic; this repo has no legitimate way to safely acquire the data such a test needs.

1. Fetch the paper and confirm the headline accuracy numbers:
   ```fish
   curl -sL https://arxiv.org/pdf/1808.07285 -o /tmp/deepcorr.pdf
   pdftotext -l 2 /tmp/deepcorr.pdf - | grep -i -B2 -A2 "96%\|RAPTOR"
   rm /tmp/deepcorr.pdf
   ```
   bash/sh: identical.
2. Run the accuracy-improvement calculation:
   ```fish
   python3 -c "
   raptor_accuracy = 0.04
   deepcorr_accuracy = 0.96
   improvement_factor = deepcorr_accuracy / raptor_accuracy
   print(f'RAPTOR: {raptor_accuracy*100:.0f}%, DeepCorr: {deepcorr_accuracy*100:.0f}%, improvement: {improvement_factor:.1f}x')
   "
   ```
   bash/sh: identical.
3. Explain in 2-3 sentences why Tor connections have unusually large network jitter compared to
   normal internet traffic (hint: relay capacity vs. client bandwidth demand) — and why that
   jitter is what made prior correlation techniques struggle.
4. Explain in 2-3 sentences what DeepCorr does differently from prior statistical correlation
   techniques (hint: generic algorithm vs. a model trained specifically on Tor's own noise
   characteristics) — why would a Tor-specific model outperform a generic one on this exact task?
5. Write 3-4 sentences reconciling link 8's 2014 optimism ("correlation doesn't scale well") with
   this paper's 2018 result — does this mean link 8 was wrong, or does it illustrate why any
   single point-in-time security assessment needs periodic re-evaluation as attack techniques
   (here, ML-based) advance?

## 12. AS-level adversaries against Tor

Scope reminder: quantitative analysis of the paper's own published numbers only — no network-path
measurement, AS mapping, or relay-selection experiment run against the real Tor network.

1. Fetch the paper and confirm the 3 headline vulnerability percentages (single AS, colluding AS,
   state-level):
   ```fish
   curl -sL https://arxiv.org/pdf/1505.05173 -o /tmp/as-level-tor.pdf
   pdftotext -l 2 /tmp/as-level-tor.pdf - | grep -i "vulnerable to\|Astoria reduces"
   rm /tmp/as-level-tor.pdf
   ```
   bash/sh: identical.
2. Run the before/after Astoria mitigation calculation:
   ```fish
   python3 -c "
   scenarios = [
       ('Single AS-level adversary', 0.40, 0.02),
       ('Colluding AS-level adversaries', 0.42, 0.05),
       ('State-level adversary', 0.85, 0.25),
   ]
   for name, before, after in scenarios:
       reduction = (1 - after / before) * 100
       print(f'{name}: {before*100:.0f}% -> {after*100:.0f}% ({reduction:.0f}% relative reduction)')
   "
   ```
   bash/sh: identical.
3. Explain in 2-3 sentences why China and Iran specifically show over 95% circuit vulnerability —
   what does that imply about those countries' Internet topology/AS structure relative to Tor
   relay placement?
4. Explain in 2-3 sentences what Astoria does differently from Tor's default relay selection
   (hint: AS-aware path prediction vs. no topology awareness at all).
5. Write 3-4 sentences on why the state-level-adversary reduction (85%->25%) is much less
   complete than the single-AS reduction (40%->2%) even with Astoria applied — what structural
   limit does AS-aware relay selection hit when the adversary already sees traffic across many
   ASes simultaneously rather than needing to be positioned on one specific path?
