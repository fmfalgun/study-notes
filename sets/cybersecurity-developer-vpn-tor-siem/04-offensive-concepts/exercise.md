# 4. Offensive Concepts Developers Must Be Aware Of — Exercises

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 4.

**Scope note**: every exercise in this file stays defensive/illustrative — read and summarize real
research, inspect how a real project defends against a flaw class, or sketch (without running) what
a test/fuzzing harness would target. None of these exercises scan, exploit, or target a real
device/network/service outside a throwaway local setup.

## 1. Client-side VPN vulnerabilities — read the paper and design the fixes (no exploiting)

1. Fetch the paper locally (arXiv PDFs render poorly through web-summary tools; `pdftotext`
   preserves the protocol-diagram/config-snippet text better):
   ```fish
   set paper_pdf (mktemp -t vpn-clientside.XXXX.pdf)
   curl -sL -o $paper_pdf https://arxiv.org/pdf/1912.04669
   ```
   ```
   # bash/sh:
   paper_pdf=/tmp/vpn-clientside.pdf
   curl -sL -o "$paper_pdf" https://arxiv.org/pdf/1912.04669
   ```
2. Read Section 4 (Study Results) and, for each of the 4 vulnerability classes in the notes above
   (PPTP optional encryption, SSTP's `sstp-client` ignoring cert failures, IKEv2 `rightid=%any`,
   hardcoded/shared IPsec PSKs), write one sentence stating the root cause in the form "the client
   was configured to accept X when it should have required Y."
3. Read Section 5 (Mitigation Solutions) and match each vulnerability to its proposed fix:
   ```fish
   pdftotext -layout $paper_pdf - | grep -n -A5 "5   MITIGATION SOLUTIONS"
   ```
   ```
   # bash/sh:
   pdftotext -layout "$paper_pdf" - | grep -n -A5 "5   MITIGATION SOLUTIONS"
   ```
4. Design exercise (defensive only): write a corrected `ipsec.conf` snippet fixing the `rightid`
   issue — replace `rightid=%any` with a value that actually pins the expected server identity (a
   specific DN or FQDN), and explain in one sentence why `%any` is described in the paper as
   acceptable *only* for testing a server, never in production.
5. Cross-reference: pull up the strongSwan config concepts from section 1 (links 5-6) and note
   whether anything in that section's exercises already touched `rightid`-equivalent settings —
   if not, this is a good candidate to add when strongSwan is revisited.
6. Clean up:
   ```fish
   rm -f $paper_pdf
   ```
   ```
   # bash/sh:
   rm -f "$paper_pdf"
   ```

## 2. OpenVPN traffic fingerprinting — read mitigations and compare against WireGuard's design

1. Fetch the paper (note: a first download attempt without `--retry` produced a truncated,
   unparseable PDF during research — use `--retry` to avoid the same issue):
   ```fish
   set paper_pdf (mktemp -t openvpn-fp.XXXX.pdf)
   curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/2403.03998
   ```
   ```
   # bash/sh:
   paper_pdf=/tmp/openvpn-fp.pdf
   curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/2403.03998
   ```
2. Read the abstract and identify the three fingerprint signals named (byte pattern, packet size,
   server response) — write one sentence per signal explaining what network-level observable it
   relies on, without needing to decrypt any traffic content.
3. Read Section 10's "Short-Term Mitigation" paragraph:
   ```fish
   pdftotext -layout $paper_pdf - | grep -n -A20 "Short-Term Mitigation"
   ```
   ```
   # bash/sh:
   pdftotext -layout "$paper_pdf" - | grep -n -A20 "Short-Term Mitigation"
   ```
4. Design exercise (defensive/comparative only): write a short paragraph on whether WireGuard
   (section 1) is inherently resistant to each of the three fingerprint signals — recall from
   section 1's whitepaper notes that WireGuard has a "Silence is a Virtue" design property (it does
   not respond at all to unauthenticated/invalid packets) and a fixed, non-negotiated 2-message
   handshake. Does fixed packet sizing help or hurt fingerprint-resistance compared to OpenVPN's
   TLS-based negotiation? Is "always the same shape" more or less detectable than "shape depends on
   negotiated options"?
5. Clean up:
   ```fish
   rm -f $paper_pdf
   ```
   ```
   # bash/sh:
   rm -f "$paper_pdf"
   ```

## 3. IKEv1 auth-bypass CVE — design a defense-in-depth check (no exploit reproduction)

This is a patched, publicly disclosed CVE (CVE-2026-50751). This exercise is entirely conceptual —
reading the disclosed root cause and designing a defensive check, never reproducing the exploit or
scanning for vulnerable devices.

1. Read the article's technical summary and write the root cause in your own words in one sentence:
   what specific verification calls were skipped, and under what crafted condition?
2. Compare this bug's *shape* against section 4 link 1's IKEv2 `rightid=%any` misconfiguration:
   write one sentence on what's the same (both result in "peer accepted without real authentication")
   and one sentence on what's different (config-time misconfiguration by the VPN provider vs. a
   code-level logic bug in the vendor's own IKEv1 implementation).
3. Design exercise: sketch (in pseudocode, no real code needed) a defense-in-depth
   "fail-closed" assertion that could catch this class of bug even if the primary verification call
   were accidentally skipped by a code path — e.g.:
   ```
   # pseudocode, illustrative only
   peer_verified = False
   if verify_peer_auth(peer_cert):
       peer_verified = True
   # ... (any other code paths that might set peer_verified) ...

   assert peer_verified == True, "refusing to grant VPN access: peer_verified flag never set"
   grant_vpn_access(peer)
   ```
   Write one sentence on why an explicit "was this actually checked" flag with a fail-closed
   assertion is more robust than trusting that every code path correctly calls the verification
   function.
4. Cross-reference to section 1: which of the four IKE exchange types (`IKE_SA_INIT`, `IKE_AUTH`,
   `CREATE_CHILD_SA`, `INFORMATIONAL` — section 1, link 7) does this bug most directly subvert?
   Write one sentence on why authentication logic concentrated in a single exchange handler is a
   single point of failure worth defending with an independent, redundant check.

## 4. Tor flow correlation (SUMo) — read the countermeasures and connect to section 2's design

This is research-paper analysis only — no traffic collection, no correlation tooling, no observing
real Tor circuits. The exercise is entirely "read, summarize, connect to design decisions already
covered in section 2."

1. Fetch the paper (a NDSS PDF, generally reliable to download — verified working with `--retry`
   as a habit from the earlier corrupted-download lesson):
   ```fish
   set paper_pdf (mktemp -t sumo.XXXX.pdf)
   curl -sL --retry 2 -o $paper_pdf https://www.ndss-symposium.org/wp-content/uploads/2024-337-paper.pdf
   ```
   ```
   # bash/sh:
   paper_pdf=/tmp/sumo.pdf
   curl -sL --retry 2 -o "$paper_pdf" https://www.ndss-symposium.org/wp-content/uploads/2024-337-paper.pdf
   ```
2. Read Section VI (Attack Countermeasures):
   ```fish
   pdftotext -layout $paper_pdf - | grep -n -A40 "ATTACK C OUNTERMEASURES"
   ```
   ```
   # bash/sh:
   pdftotext -layout "$paper_pdf" - | grep -n -A40 "ATTACK C OUNTERMEASURES"
   ```
3. List the four proposed countermeasures in your own words (traffic obfuscation, client-side
   dummy concurrent traffic, server-side dummy concurrent traffic, geographic guard-node diversity).
4. Cross-reference to section 2: for each countermeasure, name which existing Tor mechanism from
   section 2's notes it most resembles or could build on — e.g. does "geographic guard-node
   diversity" relate to anything already covered about guard selection, and does the rendezvous
   protocol's own architecture (link 3) already provide any partial defense against this class of
   correlation, or is it explicitly orthogonal (protects identity linkage, not traffic timing)?
5. Read the paper's own Ethical Considerations section and write one sentence on how its
   "responsible data collection" practice (correlating only self-generated traffic, keeping test
   `.onion` addresses private) mirrors this repo's own scope boundary for offensive-concept links.
6. Clean up:
   ```fish
   rm -f $paper_pdf
   ```
   ```
   # bash/sh:
   rm -f "$paper_pdf"
   ```

## 5. DeepCorr — compare pluggable transport effectiveness and connect to prior links

Research-paper analysis only — no traffic collection or correlation tooling.

1. Fetch the paper:
   ```fish
   set paper_pdf (mktemp -t deepcorr.XXXX.pdf)
   curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/1808.07285
   ```
   ```
   # bash/sh:
   paper_pdf=/tmp/deepcorr.pdf
   curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/1808.07285
   ```
2. Confirm the headline accuracy numbers directly (verified locally: 96% for DeepCorr vs 4% for
   RAPTOR at 900 packets/flow):
   ```fish
   pdftotext -layout $paper_pdf - | grep -n -B2 -A5 "96%"
   ```
   ```
   # bash/sh:
   pdftotext -layout "$paper_pdf" - | grep -n -B2 -A5 "96%"
   ```
3. Confirm the pluggable-transport comparison (verified locally: `meek`/`obfs4-iat0` weak, `obfs4-
   iat1` meaningfully better, but rarely deployed at publication time):
   ```fish
   pdftotext -layout $paper_pdf - | grep -n -B2 -A5 "obfs4-iat1 provides"
   ```
   ```
   # bash/sh:
   pdftotext -layout "$paper_pdf" - | grep -n -B2 -A5 "obfs4-iat1 provides"
   ```
4. Write one paragraph connecting this finding to the OpenVPN fingerprinting paper's mitigation #1
   (section 4, link 2 — don't co-locate obfuscated and vanilla servers): both papers converge on the
   same underlying lesson about optional/rare obfuscation. State that lesson in one sentence.
5. Write one sentence on why Tor deliberately doesn't obfuscate packet timing at the protocol level
   (hint: connects to Tor's low-latency design goal, mentioned in section 2's rendezvous-protocol
   notes) — i.e. this isn't an oversight, it's a real design tradeoff between anonymity strength and
   usability that this paper's findings put a concrete number on.
6. Clean up:
   ```fish
   rm -f $paper_pdf
   ```
   ```
   # bash/sh:
   rm -f "$paper_pdf"
   ```

## 6. AS-level adversaries (Astoria) — confirm the measurement numbers and reason about onion services

Research-paper analysis only — no path prediction, no relay-selection tooling, no measurement of
the real Tor network.

1. Fetch the paper (note: this PDF throws a non-fatal `xref` warning from `pdftotext` that still
   auto-recovers — don't assume the warning means extraction failed, verify the output length):
   ```fish
   set paper_pdf (mktemp -t astoria.XXXX.pdf)
   curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/1505.05173
   pdftotext -layout $paper_pdf - | wc -l
   ```
   ```
   # bash/sh:
   paper_pdf=/tmp/astoria.pdf
   curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/1505.05173
   pdftotext -layout "$paper_pdf" - | wc -l
   ```
2. Confirm the headline vulnerability percentages (40% AS-level, 42% colluding AS-level, 85%
   state-level) and Astoria's mitigation (2% / <5% / 25% respectively):
   ```fish
   pdftotext -layout $paper_pdf - | grep -n -B2 -A5 "Astoria reduces"
   ```
   ```
   # bash/sh:
   pdftotext -layout "$paper_pdf" - | grep -n -B2 -A5 "Astoria reduces"
   ```
3. Write one sentence on the root cause this paper identifies: what assumption does Tor's default
   relay-selection algorithm make that turns out to be false for a meaningful fraction of circuits?
4. Cross-reference to section 2 (onion services): onion-service sessions build circuits to *both*
   an introduction point (pre-selected by the service) and a rendezvous point (freshly chosen by the
   client) — write one paragraph reasoning about whether AS-level correlation risk is the same for
   both circuit halves, or whether one side's more "fixed" relay choice (the service's long-lived
   introduction-point circuits, from section 2 link 4's notes) could make it an easier target for an
   AS-level adversary to position against over time, compared to the client's freshly-chosen
   rendezvous circuit.
5. Clean up:
   ```fish
   rm -f $paper_pdf
   ```
   ```
   # bash/sh:
   rm -f "$paper_pdf"
   ```

## 7. MITRE ATT&CK Stealth/Defense Evasion (TA0005) — verify the current tactic name and T1070 subtechniques

1. Fetch the live page and confirm its actual current title before assuming it's still called
   "Defense Evasion" (verified: this session found it renamed to "Stealth," last modified 12 May
   2026 — after this assistant's Jan 2026 training cutoff):
   ```fish
   curl -sL https://attack.mitre.org/tactics/TA0005/ -o (mktemp -t attack-ta0005.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://attack.mitre.org/tactics/TA0005/ -o /tmp/attack-ta0005.html
   ```
2. Extract the `<title>` tag and confirm the naming:
   ```fish
   grep -o "<title>[^<]*</title>" /tmp/attack-ta0005.html
   ```
   ```
   # bash/sh:
   grep -o "<title>[^<]*</title>" /tmp/attack-ta0005.html
   ```
3. De-tag the page (same Python one-liner pattern used in section 2 for torproject.org pages) and
   locate T1070 (Indicator Removal) and its current subtechnique list:
   ```fish
   python3 -c "
   import re, html
   with open('/tmp/attack-ta0005.html') as f:
       t = f.read()
   t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
   t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
   t = re.sub(r'<[^>]+>', ' ', t)
   print(html.unescape(t))
   " > /tmp/attack-ta0005.txt
   grep -n -A5 "T1070" /tmp/attack-ta0005.txt
   ```
4. Check specifically whether subtechniques historically known as "Clear Windows Event Logs" /
   "Clear Linux or Mac System Logs" (T1070.001/.002) are present under this current fetch — this
   session did NOT find them and flagged it for manual re-check rather than asserting they were
   removed; independently confirm either way and correct the notes entry if your result differs.
5. Write one sentence on why referencing ATT&CK techniques by **ID** (e.g. `T1070`, `TA0005`) in a
   Sigma or Elastic rule (section 3, links 1 and 3) is more robust than referencing them by display
   name, given what this exercise just found about a tactic name changing while its ID stayed fixed.
6. Clean up:
   ```fish
   rm -f /tmp/attack-ta0005.html /tmp/attack-ta0005.txt
   ```

## 8. AD database tampering — write and validate a real Sigma detection for the IFM technique

This exercise builds a defensive detection rule for a documented attack technique — no execution of
`ntdsutil.exe` or any credential-extraction tool against any real system, domain controller or
otherwise.

1. Fetch the article and confirm the four extraction techniques and their SIEM-relevant Event IDs
   (4688 process creation, 4663 object access):
   ```fish
   curl -sL https://www.manageengine.com/log-management/siem-use-cases/threats/active-directory-database-tampering.html -o (mktemp -t ad-tampering.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://www.manageengine.com/log-management/siem-use-cases/threats/active-directory-database-tampering.html -o /tmp/ad-tampering.html
   ```
2. Write a full Sigma rule (using this file's section 3 conventions) detecting the Install-From-
   Media (IFM) technique specifically:
   ```yaml
   title: Potential NTDS.dit Extraction via ntdsutil IFM
   id: 3f8e2a1c-0000-4a00-8000-000000000003
   status: experimental
   description: Detects ntdsutil.exe being invoked with Install-From-Media (IFM) arguments, a technique used to extract a portable copy of the AD credential database.
   logsource:
       category: process_creation
       product: windows
   detection:
       selection:
           Image|endswith: '\ntdsutil.exe'
           CommandLine|contains:
               - 'ifm'
               - 'create full'
       condition: selection
   falsepositives:
       - Legitimate AD backup/DC provisioning workflows using ntdsutil
   level: high
   ```
3. Validate it parses (verified working, same `yaml.safe_load` pattern as section 3):
   ```fish
   python3 -c "
   import yaml
   with open('ntdsutil-sigma.yml') as f:
       d = yaml.safe_load(f)
   print('parsed OK, condition:', d['detection']['condition'])
   "
   ```
4. Add MITRE ATT&CK tags to the rule connecting it to the previous link's tactic — use technique
   T1003 (OS Credential Dumping) and tactic `TA0006` (Credential Access), noting this is a
   *different* tactic than TA0005/Stealth even though the *evasion methods* used (avoiding VSS
   audit events, raw disk reads) are Stealth-tactic behaviors layered on top of a Credential-Access
   goal — write one sentence on why a single attack technique can legitimately map to multiple
   ATT&CK tactics simultaneously.
5. Write one sentence on why Event ID 4663 (object access against the NTDS.dit file specifically)
   is a stronger detection signal than Event ID 4688 (process creation) alone for this technique —
   what does 4663 catch that a process-creation-only rule would miss (hint: the "Ninja-Copy" raw
   disk-read technique described in the article specifically avoids normal process-level file
   access patterns).
6. Clean up:
   ```fish
   rm -f /tmp/ad-tampering.html
   ```

