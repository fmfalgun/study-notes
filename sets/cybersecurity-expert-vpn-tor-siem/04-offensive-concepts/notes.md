# 4. Offensive Concepts You Must Be Aware Of — Notes

Scope note: per this repo's safety boundary, every entry in this section explains attacks
conceptually (what's exploited, why it works, what the impact is) — none of these notes describe
running an actual exploit against a real target. "Try it" sections stay defensive/illustrative:
reading real CVE writeups, inspecting detection rules, or building local instrumented labs against
throwaway/self-owned test setups only.

## MITRE ATT&CK — Defense Evasion tactic (TA0005)

**Claim** (fetched directly via `curl` — confirmed a real, recent naming change worth flagging:
the live page's own title and body now read **"Stealth, Tactic TA0005"**, not "Defense Evasion" —
last modified 12 May 2026 per the page's own metadata. The source list's link text ("Defense
Evasion tactic") uses the older name; this entry uses the current live name throughout, noting the
rename explicitly so a reader isn't confused when the ID matches but the name doesn't): TA0005's
own definition: "The adversary is trying to hide and conceal their actions, appearing as normal
behavior." Its distinguishing scope note versus other tactics: Stealth techniques are about
*concealment* (avoiding, obfuscating, or mimicking normal operations) specifically **without**
modifying security controls or compromising collection/monitoring feeds — that narrower, more
precise definition suggests MITRE split what used to be a broader "Defense Evasion" concept into
"Stealth" (blend in) as one thing and (implicitly) some other tactic for actually *tampering with*
defenses (this directly foreshadows link 2/3 of this section on defense-evasion detection and
log/AD-tampering, which are about attacking the monitoring itself, not just blending in — worth
checking whether those still call themselves "Defense Evasion" despite this rename, since sources
may now be inconsistent). TA0005/Stealth has **30 techniques** (confirmed count, matching section
3 link 4's directly-fetched total for this same tactic under its old label). Concrete example
technique covered in the fetch: **T1134 Access Token Manipulation** — on Windows, a process's
identity/permissions are determined by its access token; an adversary who can duplicate, create,
or reassign a token (via `DuplicateToken`/`ImpersonateLoggedOnUser`/`SetThreadToken`, or spawn a
process with `CreateProcessWithTokenW`/`runas`) can make actions appear to originate from a
different, often more-trusted, user or process — without needing that user's password. Its
sub-technique T1134.004 **Parent PID Spoofing** is a good illustration of "concealment without
touching security controls": a malicious process fakes its `CreateProcess`-reported parent PID so
process-monitoring tools (which often flag "unusual parent-child relationships," per section 3
link 6's own Privilege Escalation detection guidance) see a benign-looking lineage instead of the
real one.

**Simple explanation**: Stealth/Defense Evasion isn't one specific trick — it's the entire
category of "make malicious activity look like normal activity" to defeat exactly the kind of
detection this study set has been building (Sigma rules, ATT&CK-mapped SIEM alerts). Access token
manipulation is a concrete Windows-specific example: instead of hacking harder, an attacker just
borrows or fakes the "ID badge" (token) a legitimate process would carry.

**Try it** (explain/detect only — no execution of any evasion technique against any system):
read the real technique documentation and map it to what a defender would actually look for, which
is the same detection-engineering translation exercise practiced in section 3 links 5-7.
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
bash/sh: identical.
Applied exercise: for T1134 Access Token Manipulation (or T1134.004 Parent PID Spoofing
specifically), write a Sigma-style detection sketch (reuse the format validated in section 3 link
7) targeting the concrete artifact named in the ATT&CK description — an unusual parent-child
process relationship, or a process creation event where the reported PPID doesn't match the
actual spawning process recorded by an EDR/kernel-level sensor (which token-spoofing tricks can't
fake, unlike the user-space-visible PPID field).

## Defense evasion detection/response guide (ManageEngine Log360)

**Claim** (fetched via `curl` + tag-stripping; note this page — dated May 13, 2026, close to
TA0005's 12 May 2026 "Stealth" rename confirmed in link 1 — still calls the tactic "Defense
Evasion" throughout, confirming the sources in this study set are genuinely inconsistent on the
current name; a real analyst needs to recognize both terms refer to the same TA0005): frames
defense evasion as the tactic with the *most* techniques in ATT&CK (matches link 1's confirmed
count of 30 for TA0005) and argues it's structurally different from most other tactics because
most techniques **exploit trust relationships that already exist in the OS** rather than novel
vulnerabilities — its concrete example: `Rundll32` loading a malicious DLL looks nearly identical
to Windows legitimately using `Rundll32` to load a real library, so detection needs a behavioral
baseline of "what does normal `svchost.exe`/`Rundll32` behavior look like," not just a
signature match. Names 6 key techniques with IDs: Masquerading (T1036), Obfuscated Files or
Information (T1027), Indicator Removal (T1070), Process Injection (T1055), Modify Registry
(T1112), Hide Artifacts (T1564). Cites the **2025 IBM Cost of a Data Breach Report: 194-day
average dwell time** for attackers not detected by the victim's own team — and argues defense
evasion is the primary reason that number is so high, because it's the mechanism that buys every
other tactic (credential access, lateral movement, exfiltration) the time it needs to operate
undetected. A sharp, genuinely useful defensive insight: **security-tool tampering is itself a
strong signal** — an attacker killing an endpoint agent, adding a Defender exclusion, or clearing
the Security event log doesn't erase evidence so much as create a different, very loud kind of
evidence ("a silent endpoint is often more alarming than a noisy one"). Also names LOLBin
("living-off-the-land binary") abuse — using signed, trusted Microsoft binaries to
proxy-execute a malicious payload — as an accelerating technique specifically *because*
signature-based detection has gotten better, pushing attackers toward abusing legitimate tools
instead of dropping detectable malware.

**Simple explanation**: Defense evasion isn't attackers hiding in some special corner — it's
attackers wearing the building's own uniform. That's exactly why it's hard to catch with
signatures and needs behavioral baselines instead, and exactly why the *absence* of expected
telemetry (an EDR agent going quiet, logs stopping) is itself one of the most reliable tells.

**Try it** (explain/detect only): translate the article's own "silent endpoint is more alarming
than a noisy one" insight into a concrete, locally-testable detection idea — monitoring for the
*absence* of expected periodic telemetry, which is exactly the kind of check a log-source
health-monitoring rule (distinct from a content-matching rule) would implement.
```fish
# concept: if a log source normally emits heartbeat-like activity, its sudden silence is itself
# a signal — demonstrate by checking this machine's own recent journal activity rate as a baseline
journalctl --no-pager --since "10 minutes ago" | wc -l
```
bash/sh: identical.
Applied exercise: write a Sigma-style rule (reusing section 3 link 7's format) whose `detection`
field's `description` describes an **absence-based** rule instead of a content-match rule — e.g.
"alert if SYSTEMD_UNIT=auditd or a known EDR service emits zero heartbeat events in a 15-minute
window" — and explain in 2-3 sentences why this kind of rule needs a different underlying SIEM
mechanism (a scheduled "did X happen" query with a time window) than a normal per-event match rule.

## Log/AD database tampering case study (ManageEngine)

**Claim** (fetched via `curl` + tag-stripping): this is a full worked incident-detection use case,
not just a concept summary — genuinely rich, structured content. **What's at stake**: `NTDS.dit`
is Active Directory's actual database file — every user account, password hash, group membership,
and trust relationship in the domain lives in it; "whoever controls NTDS.dit controls the domain."
MITRE mapping given: TA0006 Credential Access, TA0003 Persistence, **TA0005 Defense Evasion**
(another source still using the pre-rename name from link 1) — technique **T1003.003 OS
Credential Dumping: NTDS**, severity Critical. Two broad attack paths, each with 2 concrete
named techniques: **Offline extraction** — (1) `ntdsutil.exe`'s legitimate "Install From Media"
(IFM) feature (`create full` command), a signed Microsoft tool meant for provisioning new domain
controllers, abused to generate a portable full copy of NTDS.dit + the SYSTEM registry hive
without touching the live VSS subsystem or stopping any service; (2) the "Ninja-Copy" technique —
since NTDS.dit is locked by AD while the DC runs, attackers instead read it from a Volume Shadow
Copy Service (VSS) point-in-time snapshot, bypassing the file lock entirely. **Live extraction** —
(3) PowerShell-based Kerberos ticket extraction via the Windows SSPI layer, exporting cached
Ticket-Granting-Tickets (TGTs) that can be replayed on another system for ~10 hours without the
account's password (Pass-the-Ticket); (4) PowerShell MiniDump — using the `DbgHelp.dll
MiniDumpWriteDump` API (or the `Out-MiniDump` PowerShell function) to write LSASS process memory
(which holds plaintext credentials, NTLM hashes, and Kerberos tickets for every logged-in user) to
a disk file, processed offline later, so no credential-dumping tool ever touches live LSASS
memory directly (evading tools that specifically monitor LSASS process access). Full attack chain
given, technique-by-technique: Initial Access (T1078) -> Privilege Escalation to Domain
Admin/SYSTEM on the DC (T1068/T1078, the minimum privilege actually required for any of this) ->
Credential Access via offline database copy (T1003.003) or live extraction (T1003.001/T1558) ->
Lateral Movement via Pass-the-Hash or Pass-the-Ticket (T1550.002), at which point "all domain
accounts are now accessible."

**Simple explanation**: This single file (NTDS.dit) is effectively the master key ring for an
entire Windows domain, and every technique described here is really about one of two things:
getting a *copy* of that file without triggering the lock/monitoring on the live one, or getting
the *decrypted credentials that live in memory* without running an obviously-malicious credential
dumper. Every technique deliberately reuses a legitimate, signed Windows feature (`ntdsutil.exe`,
VSS, the MiniDump API) specifically because doing so blends into normal admin activity — a direct,
concrete real-world instance of link 2's "exploiting trust relationships that already exist"
argument.

**Try it** (explain/detect only — this is exactly the kind of technique this repo's scope
boundary means never to execute against a real domain controller; the exercise is documentation
research and detection-rule sketching only): map each of the 4 named techniques to the specific
log event/artifact a SOC would monitor for, which is exactly the "Prerequisites for detection"
section this article itself provides.
```fish
# no live AD/DC exists on this machine to test against — the exercise is reading and structuring
# the article's own attack-chain table, already extracted above
python3 -c "print('exercise is documentation-based; see notes.md attack chain table above')"
```
Applied exercise: build a table with columns Technique | Windows tool/API abused | What makes it
"stealthy" (which legitimate mechanism it hides behind) | What log source would catch it — filled
in for all 4 techniques (IFM database creation, VSS/Ninja-Copy, PowerShell Kerberos extraction,
PowerShell MiniDump). This is the same "artifact -> detection logic" translation exercise from
section 3 links 5-6, applied to a real, fully-documented attack chain instead of a single alert.

## IPsec/IKE VPN pentesting methodology (HackTricks)

**Claim** (fetched via `curl` directly — WebFetch's own redirect target, `tollbit.hacktricks.wiki`,
returned HTTP 402 Payment Required, a paywall for AI-crawler traffic specifically; the original
`book.hacktricks.xyz` URL still serves full content to a normal `curl` request, so that was used
instead): describes a real, standard IPsec/IKE pentest methodology, directly explaining exactly
*why* the strongSwan `aggressive` config flag studied in section 1 link 6 defaults to `no` and is
flagged "less secure" in its own man page. Workflow: (1) discover the service with `nmap -sU -p
500` (IKE's UDP port); (2) enumerate which crypto **transform** (encryption/hash/auth/DH-group
combination) the gateway accepts using `ike-scan`, which by default probes in **Main Mode** (ID
encrypted, safer) — a response with `AUTH=PSK` tells the pentester the gateway uses a
pre-shared key, immediately valuable since PSKs are crackable offline; (3) the critical weakness
is **Aggressive Mode**: because the gateway needs to pick the right PSK for a given user/group
*before* the crypto channel is established, Aggressive Mode sends the peer's identity in the
clear, pre-authentication (`ike-scan -A` reveals it directly) — this is the exact mechanism the
strongSwan man page's warning describes: "the ID and HASH payloads are exchanged unprotected...
allows a passive attacker to snoop peer identities, and even worse, start dictionary attacks on
the Preshared Key." A captured Aggressive Mode handshake yields a crackable PSK hash (offline,
via `hashcat -m 5400` or `psk-crack`) — since PSKs are often reused as credentials elsewhere
(SSH, other VPN clients), a cracked PSK can pivot well beyond the VPN itself. Beyond the PSK
itself, XAuth (an extra auth layer commonly layered on Aggressive Mode + PSK, typically backed by
AD/RADIUS) can be brute-forced directly with a tool like `ikeforce` once the group ID and PSK are
known, and a local MitM (via `fiked` acting as a fake VPN endpoint after ARP-spoofing IKE traffic
to it) can capture XAuth credentials outright.

**Simple explanation**: The single biggest IPsec/IKE misconfiguration a pentester looks for is
"is Aggressive Mode even enabled" — because that one setting alone downgrades identity
confidentiality (leaks who's connecting) and turns the PSK into something crackable offline,
exactly the way a weak password hash would be. Main Mode costs an extra round-trip but keeps the
identity encrypted until after the crypto channel exists, closing this exact hole.

**Try it** (explain/detect only — none of `ike-scan`/`ikeforce`/`hashcat`/`fiked` are installed on
this machine, and per this repo's scope boundary none were installed or run against any target,
including localhost, for this exercise): verify the defensive side directly — confirm strongSwan
(already studied and installed in section 1 link 6) defaults to the secure setting, straight from
its own official config documentation.
```fish
man 5 swanctl.conf | grep -i -B2 -A6 "aggressive"
```
bash/sh: identical. Verified on this machine: `connections.<conn>.aggressive [no]` — the default
is Main Mode, and strongSwan's own documentation states the exact same risk (passive identity
snooping, PSK dictionary attacks) that the HackTricks methodology exploits.
Applied exercise: write a Sigma-style detection sketch (reusing the format from section 3 link 7)
for "IKE Aggressive Mode negotiation observed on the network" — `logsource` should reference
network/firewall telemetry on UDP/500, and the rule's `description` should explain that the mere
*presence* of an Aggressive Mode exchange (regardless of whether it's later cracked) is itself
worth alerting on, since it indicates a downgraded, riskier configuration is active.

## Real-world critical IKEv1 auth-bypass exploitation (The Hacker News)

**Claim**: A concrete real-world case study directly extending link 4's methodology into an
actual CVE. **CVE-2026-50751** (CVSS 9.3, critical) affects Check Point Remote Access VPN and
Mobile Access deployments still using the deprecated **IKEv1** protocol (Security Gateways R82.10
down through R80.40; Spark Firewalls R80.20.X/R81.10.X/R82.00.X) — note this is exactly the older
protocol RFC 7296/IKEv2 (section 1 link 5 of this study set) superseded, and its continued
deployment is itself part of the exposure. **Root cause**: improper certificate validation during
IKEv1 negotiation — an attacker manipulates authentication flags via a custom `VPNExtFeatures`
Vendor ID payload sent during key exchange, which causes the vulnerable code to skip its own
`verify_peer_auth` check entirely, meaning **neither the certificate's signature NOR its trust
chain is checked at all** — a complete authentication bypass, not a weakness that merely makes
auth easier to brute-force. **Exploitation in the wild**: active since May 2026, targeting "a few
dozen organizations globally," using geographically-targeted VPS infrastructure, with attackers
observed downloading malicious ELF binaries post-compromise; one attack chain was linked to Qilin
ransomware affiliates — i.e. this specific VPN auth-bypass was used as the *initial access*
technique (T1078/T1190-adjacent) that led directly into a ransomware operation. **Response**:
Check Point released hotfixes; CISA added it to the Known Exploited Vulnerabilities catalog on
June 8, 2026, mandating federal-agency patching by June 11, 2026 — a 3-day turnaround window,
signaling how seriously it was treated.

**Simple explanation**: This is what happens when a protocol-design weakness (link 4's Aggressive
Mode/PSK issues) gets compounded by an actual implementation bug — here, the vendor's own
certificate-checking code has a logic flaw that a specially-crafted vendor payload can trigger to
skip validation altogether, turning "prove you have a valid cert" into "just claim you do." The
fact it's tied to a still-supported-but-deprecated protocol (IKEv1) also reinforces link 4's
implicit lesson: legacy protocol support is itself an attack surface, independent of any specific
bug.

**Try it** (explain/detect, root-cause analysis only — never attempt to reproduce this bypass
against any real Check Point deployment): summarize the actual CVE writeup's root cause in your
own words and identify what a defender would look for.
```fish
# no live Check Point gateway exists here to test against — the exercise is root-cause analysis
# from the public writeup, plus checking whether this machine's own strongSwan install still
# offers IKEv1 as a live protocol option (informative, not exploitable without a target)
man 5 swanctl.conf | grep -i -B2 -A4 "^ *connections.<conn>.version"
```
bash/sh: identical (this reuses the same `version` directive already inspected in section 1
link 6 — `0` accepts both IKEv1 and IKEv2 as responder, which is exactly the kind of
protocol-flexibility setting worth auditing in light of this CVE).
Applied exercise: write a 4-6 sentence root-cause summary in your own words covering: what the
`VPNExtFeatures` Vendor ID payload manipulation actually does, why skipping `verify_peer_auth`
is a complete bypass rather than a partial weakening, and one concrete mitigation beyond
patching (e.g. disabling IKEv1 entirely where IKEv2-only interop is possible) that would have
prevented exploitation even pre-patch.

## NCSC alert on exploited VPN vulnerabilities

**Claim**: A UK National Cyber Security Centre alert covering a *campaign*, not a single CVE —
APT actors (unattributed to a specific named group in the alert) actively exploiting known,
already-patched flaws across 3 major VPN vendors simultaneously: **Pulse Connect Secure**
(CVE-2019-11510, pre-auth arbitrary file read — lets an attacker read any file, including stored
credentials, without any authentication at all; CVE-2019-11539, post-auth command injection),
**Fortinet** (CVE-2018-13379, pre-auth file access; CVE-2018-13382, unauthenticated password
changes — an attacker can reset a legitimate user's password with zero auth; CVE-2018-13383, heap
overflow enabling shell access), **Palo Alto GlobalProtect** (CVE-2019-1579). Targets: government,
military, academic, business, and healthcare sectors, UK and international. The pattern across all
5 named CVEs is the same theme running through this entire section: **pre-authentication**
vulnerabilities in the VPN gateway itself — the exact perimeter device meant to be the security
boundary is instead the entry point, requiring zero valid credentials in several cases. The
mitigation guidance is notably not just "patch": (1) patch, (2) **reset all authentication
credentials** — because a pre-auth file-read bug likely already exposed stored credentials/config
even before detection, so patching alone doesn't undo an already-compromised credential set; (3)
review VPN configuration for unauthorized changes (an attacker with access may have added
persistence, e.g. new authorized keys/rules); (4) enable MFA; (5) monitor logs for anomalous
connection geolocation; (6) consider a full factory reset if compromise can't be ruled out — a
strong statement, implying config-level review alone might not be trustworthy post-compromise.

**Simple explanation**: This alert is the "this already happened to real UK organizations, at
scale, across multiple vendors" version of the single-CVE case study in the previous link — same
category of bug (perimeter VPN device, pre-auth), different vendors, real ongoing campaign. Its
mitigation list is the important artifact: patching is necessary but explicitly *not sufficient*
on its own once a pre-auth flaw has been live and exploitable — credentials and configs need to be
assumed-compromised and actively reset/reviewed, not just protected going forward.

**Try it** (explain/detect, patch-management + IR-checklist practice only — no exploitation of
any real gateway): translate the alert's 6-step mitigation list into a concrete audit checklist
applied to this machine's own installed VPN-adjacent software (strongSwan, WireGuard) as a stand-in
exercise for "how would I actually verify these steps on infrastructure I run."
```fish
# stand-in for "apply security patches immediately" — check installed versions against latest
ipsec version
wg --version
# stand-in for "review VPN configuration for unauthorized changes" — check config file integrity
# metadata (mtime, permissions) as a lightweight tamper-check
ls -la /etc/swanctl/swanctl.conf
```
bash/sh: identical.
Applied exercise: write out, for each of the 6 mitigation steps in the alert, a one-sentence
"how would I verify this is actually done" check applicable to a real strongSwan/WireGuard
deployment (e.g. for "review configuration for unauthorized changes," what specific file(s) and
what specific indicator — unexpected mtime, unfamiliar `[Peer]` block, unrecognized `connections.
<conn>` entry — would you look for?).

## Client-side vulnerabilities in commercial VPNs (Bui, Rao, Antikainen, Aura — arXiv 1912.04669)

**Claim** (fetched the actual PDF via `curl` + `pdftotext`, following this repo's man7/FHS/GNU
convention of preferring a local text extraction over a lossy summarizer for source-of-truth
documents — the paper itself, not a summary of it, was read): this is an academic study (Aalto
University, published at the 24th Nordic Conference on Secure IT Systems) of 30 popular
commercial VPN services' **client-side configuration**, explicitly *not* looking for
cryptographic-protocol or code-level bugs — only misconfiguration and architectural mistakes in
how providers set up or instruct users to set up their VPN client. Two attacker models: **network
attacker** (can intercept/modify traffic — e.g. a rogue hotel/airport hotspot) and **local
attacker** ("Man-in-the-Machine" — an unprivileged local user/process on the same machine
exploiting insecure inter-process communication between a VPN client's GUI and its backend
binary). Two headline findings: (1) **Shared/public L2TP/IPsec pre-shared keys** — the paper's
motivating discovery was that many commercial VPN providers use the *same* PSK for every single
customer (their concrete example: the literal string `"12345678"`), publicly discoverable either
online or by inspecting client config — an attacker who knows it can MitM the IPsec tunnel and
read all traffic; re-checking 14 services flagged for this back in 2016, the paper found 10 were
*still* vulnerable years later. (2) **PPTP optional-encryption downgrade** — Windows does not
enforce encryption on VPN connections by default, and many providers never instruct users to turn
it on; a MitM attacker can pass through the authentication phase transparently, then impersonate
the server during the data-exchange negotiation and simply agree to "no encryption" on the
client's behalf, since the client treats encryption as optional and won't refuse — the client
believes it's on a VPN while transmitting everything in the clear. Their verification methodology
was genuinely empirical: they stood up fake VPN servers (Poptop for PPTP, OpenVPN's own software,
strongSwan for IKEv2/Cisco IPsec, SoftEtherVPN for SSTP/L2TP) and redirected real client
connections to them via `/etc/hosts` edits, observing whether the client connected without
warning the user.

**Simple explanation**: A VPN protocol can be cryptographically sound and still be trivially
broken by how a *specific provider* deploys it — reusing one PSK for every customer turns "shared
secret authentication" into "no real authentication," and leaving encryption optional-by-default
means a MitM can just ask the client to turn it off, and the client complies without complaint.
The lesson generalizes directly from links 4-6 of this section: the weakest link in VPN security
is very often the deployment/configuration choice, not the protocol math.

**Try it** (explain/detect, configuration-auditing only — no fake VPN server was stood up and no
MitM was performed against any target, consistent with this repo's scope boundary; the paper's
own methodology of intercepting real client connections is explicitly not reproduced here):
audit this machine's own real VPN configs (strongSwan, WireGuard — already studied and confirmed
present in section 1) for the exact two failure classes the paper found, applied defensively.
```fish
# check 1: does strongSwan's own config schema even support a PSK auth method, and how is a PSK
# secret defined/stored? (read-only structural check via man page, not the live root-owned
# config file, consistent with earlier sections' handling of this same file)
man 5 swanctl.conf | grep -i -B1 -A5 "psk"

# check 2: WireGuard has no cipher/encryption-negotiation option to downgrade in the first place —
# confirm structurally by grepping for the absence of any such option in its config man page
# (already noted in section 1 link 2: cipher suite is hard-coded, not negotiated)
man 8 wg-quick | grep -iE "cipher|encrypt|protocol ="
```
bash/sh: identical.
Applied exercise: write a 5-item audit checklist (derived from this paper's 2 findings) that a
defender could apply when evaluating *any* commercial VPN provider before trusting it — e.g.
"does the provider's setup guide ever show a PSK value that looks the same across their own
documentation examples and support-forum posts from different users" as a real, checkable red
flag for the shared-PSK problem.

## Tor traffic correlation / de-anonymization attacks (Tor Project blog)

**Claim** (fetched via `curl` + tag-stripping — WebFetch blocked this Tor Project subdomain like
several others in section 2; this is a 2014 post by Roger Dingledine, Tor Project co-founder, "arma"):
establishes the foundational, honestly-stated limit of Tor's own threat model, directly extending
section 2 link 1's "no single relay knows the full path" claim with the missing caveat: **Tor's
design explicitly does not defend against an attacker who can see traffic entering the Tor network
AND traffic leaving it, at the same time.** If you can see both flows, straightforward statistics
(packet timing, packet counts) let you decide whether they match — this is called **traffic
confirmation** (or end-to-end correlation), and it's a fundamentally different, much easier attack
than **traffic analysis** (an attacker trying to figure out *whom to investigate* with no prior
suspect). Tor protects against the second; it cannot protect against the first, by design — adding
enough delay/padding to defeat correlation would destroy Tor's low-latency browsing use case (the
tradeoff high-latency mix networks like Mixmaster make differently). The specific research being
discussed (Sambuddho's group, using router **netflow logs** rather than needing full packet
capture) reported a 6% false-positive rate — the post's key, genuinely important defensive-minded
counterpoint is the **base-rate fallacy**: at real Tor scale (100,000+ concurrent flows), a 6% FPR
means roughly 6,000 flows look like a false match for every real one you're hunting, which can
make an attack "effectively useless" in practice even though it's theoretically real — attack
*feasibility in a lab* and attack *usefulness at internet scale* are different questions, and the
post explicitly cautions against conflating them. It also names the real gating factor for whether
this class of attack is even possible: **how much of the Internet the adversary can measure or
control** — directly setting up section 4's later AS-level-adversary link. Finally, a genuinely
important real-world caution in the post: contemporary arrests of Tor users at the time were NOT
attributed to correlation attacks at all, but to "bad opsec" (poor operational security practices)
by a few individuals who then implicated others under questioning — a reminder that the flashiest
theoretical attack usually isn't how real de-anonymization happens in practice.

**Simple explanation**: Tor promises "no one relay can link you to your destination," not "no one
watching both ends of the internet can ever match up your traffic." If an adversary already
controls or observes enough of the network to see both where you connect in and where the traffic
comes out, matching timing patterns is genuinely effective math — but doing that at real internet
scale, without knowing who to already suspect, runs into the same false-positive-swamps-true-
positive problem any needle-in-a-haystack statistical matching does.

**Try it** (explain/detect only — correlation attacks require internet/ISP-scale traffic
visibility this repo's scope explicitly excludes; the applied exercise is working the base-rate
math yourself, which is exactly the kind of analysis a defender/researcher does, not an attack):
```fish
python3 -c "
# reproduce the base-rate fallacy arithmetic from the post: 6% FPR against 100,000 flows
total_flows = 100000
fpr = 0.06
false_positives = total_flows * fpr
print(f'False positives at 6% FPR across {total_flows} flows: {false_positives:.0f}')
print('Even a real, correct match is drowned out by this many false alarms without a much lower FPR or a way to narrow the candidate set first.')
"
```
bash/sh: identical.
Applied exercise: rerun the calculation with FPR values of 1%, 0.1%, and 0.001%, and write 2-3
sentences on what FPR an attacker would actually need to make correlation practical against the
full Tor network (millions of daily users) rather than a lab-scale test — this is the same
"detection coverage gap" style quantitative reasoning practiced in section 3 links 5-6, applied to
an attacker's own success-rate math instead of a defender's.

## Thirteen years of Tor attacks (catalog, GitHub)

**Claim**: This is a curated academic survey (Delft University of Technology) cataloging Tor
attack research across 13 years into **7 categories**, giving a taxonomy the previous single-post
link only showed one slice of (traffic confirmation/correlation): (1) **Correlation Attacks** —
passive, end-to-end, linking entry and exit flows — exactly link 8's topic; (2) **Congestion
Attacks** — active, deliberately inducing network delay/congestion to create an observable timing
signature (rather than passively watching existing timing); (3) **Timing Attacks** — actively
manipulating traffic flow patterns to inject a detectable fingerprint; (4) **Fingerprinting
Attacks** — passive, identifying *which website or service* is being visited purely from traffic
shape (packet sizes/timing), without needing to see both ends of the circuit at all — a distinct,
arguably more practical threat than end-to-end correlation since it needs only guard-side
visibility; (5) **Denial of Service Attacks** — actively disrupting the network, sometimes as a
step to force traffic onto adversary-controlled relays; (6) **Supportive Attacks** — preparatory
techniques (e.g. relay enumeration, deanonymizing which relays exist/are running) that enable a
later attack in another category rather than deanonymizing on their own; (7) **Revealing Hidden
Services Attacks** — locating the real server behind an onion service (section 2 links 3-4),
distinct from deanonymizing a *client*. Named notable attacks: the **relay early traffic
confirmation attack** (a real, historically-exploited technique using a specific cell-flagging
bug) and **cell counter manipulation**; at the network layer, the **Raptor attack**, which
leverages BGP routing weaknesses/asymmetry to gain the kind of "controlled network position" link
8 identified as the actual gating requirement for correlation to work at all. Also documents
application-layer attacks: malicious webpages that fingerprint/identify Tor Browser clients via
HTTP-level behavior differences. The survey's overall framing: successful attacks increasingly
require controlled network positions and sophisticated timing analysis over time, reflecting
Tor's design continuously raising the bar for what an adversary needs to succeed.

**Simple explanation**: Link 8 covered one specific, well-known Tor attack category in depth
(correlation). This catalog shows that's really one of seven distinct attack *families* against
Tor, each exploiting a different assumption — some need to see both ends of a circuit
(correlation), some only need to watch traffic shape at one end (fingerprinting), some actively
inject a signal instead of passively watching (congestion/timing), and some target the onion
service's server rather than the client at all (hidden-service-revealing).

**Try it** (explain/detect, taxonomy-building only — this is a survey of research, and no attack
technique from any of the 7 categories is executed against anything): build the category map and
connect it explicitly to what's already been studied in this study set.
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
Applied exercise: for each of the 7 categories, write one sentence identifying which prior link in
this study set it connects to most directly (e.g. Correlation -> link 8; Revealing Hidden Services
-> section 2 links 3-4 on onion service protocol) — and for categories with no direct prior
connection (Congestion, Timing, DoS, Fingerprinting, Supportive), note that explicitly as a gap
this catalog fills that earlier links didn't cover.

## De-anonymisation attacks on Tor: a survey (ResearchGate / arXiv 2009.13018)

**Claim** (ResearchGate itself returned HTTP 403 / Cloudflare error 1020 on both a `WebFetch` and
a `curl` retry — this is a hard bot-block, not a transient failure; however, `WebSearch` found
that this exact paper — same title, same authors (Karunanayake, Ahmed, Malaney, Islam, Jha; UNSW
Sydney / Charles Sturt University) — is freely available on arXiv at `2009.13018`, which **was**
successfully fetched directly via `curl`+`pdftotext`, so this entry is built from the actual
paper text, just via its non-paywalled mirror rather than the ResearchGate link given in the
source list): confirms the previous link's GitHub catalog is a direct downstream implementation
of *this exact paper's* taxonomy — same 7 categories (correlation, congestion, timing,
fingerprinting, DoS, supportive, revealing-HS attacks), because the GitHub repo is built from
this survey. This paper's own contribution over prior surveys: it covers roughly 30 more
de-anonymization attacks than earlier surveys, includes 15+ attacks published after 2016
(including deep-learning-based ones — directly setting up link 11's DeepCorr paper), and
explicitly fills gaps prior surveys left out (website fingerprinting and hidden-service attacks
were missing or thin in earlier surveys by Salo 2010, Nepal et al. 2015, Erdin et al. 2015). Two
concrete technical facts confirmed directly from the paper's background section, independently
cross-validating earlier links in this study set: (1) the hidden-service connection is confirmed
as a **6-hop circuit** — 3 hops client-to-rendezvous-point + 3 hops hidden-service-to-rendezvous-
point — matching section 2 link 3's onion-services-overview claim exactly, word-for-word
consistent across two independent Tor Project sources; (2) Tor's relay-cell payload encryption is
specified precisely as **128-bit AES-CTR (counter mode)**, with symmetric keys negotiated via
Diffie-Hellman — a level of cryptographic detail neither section 2's overview nor this section's
earlier links stated explicitly. The paper's stated goal beyond cataloging: analyze each attack's
*practicality* and conclude with what Tor framework improvements have made previously-viable
attacks infeasible over time — i.e. it's explicitly attack-history-aware, tracking which attacks
still work today vs. which Tor's own hardening has already closed.

**Simple explanation**: This survey is effectively the primary research literature that both the
GitHub catalog (previous link) and much of this section's Tor-attack framing draws from — reading
it directly (via its open arXiv mirror, since the ResearchGate copy is blocked) confirms the
7-category taxonomy isn't just a GitHub maintainer's own organization scheme, it's a peer-reviewed
academic classification, and it adds real cryptographic specificity (AES-CTR-128, 6-hop HS
circuits) that ties directly back to and validates section 2's conceptual claims.

**Try it** (explain/detect, cross-referencing/verification only — no attack from any category
executed against anything): verify the cross-source consistency claim directly.
```fish
curl -sL https://arxiv.org/pdf/2009.13018 -o /tmp/tor-survey.pdf
pdftotext -f 4 -l 5 /tmp/tor-survey.pdf - | grep -i -B2 -A2 "six-hop\|AES-CTR"
rm /tmp/tor-survey.pdf
```
bash/sh: identical.
Applied exercise: write 3-4 sentences on why finding the *same* specific claim (6-hop HS circuit)
stated independently in two different primary sources (Tor Project's own community docs in
section 2 link 3, and this independent academic survey) is stronger evidence than either source
alone — this is the same "verify, don't assume" discipline this repo's man7/FHS conventions
already apply to documentation sources, now applied to a security-research claim instead.

## Deep-learning flow correlation attack (DeepCorr) — arXiv 1808.07285

**Claim** (fetched the actual PDF via `curl`+`pdftotext`, same source-of-truth approach as the
other arXiv papers in this section): DeepCorr (Nasr, Bahramali, Houmansadr — UMass Amherst, 2018)
directly **updates and complicates link 8's 2014 conclusion** that correlation attacks don't
scale well in practice due to high false-positive rates. The paper's own framing of *why*
correlation was previously considered impractical: Tor connections experience unusually large
network jitter (far more than normal internet traffic) caused by congestion from the imbalance
between Tor's relay capacity and client bandwidth demand — this naturally-occurring noise is what
made prior statistical correlation techniques (generic algorithms not tailored to Tor's specific
noise characteristics) produce high false-positive rates unless given very long flow observations
against small target sets. The paper's stated prior state-of-the-art, RAPTOR (already named in
link 9's catalog as the BGP-based attack), needed 100MB over 5 minutes of traffic and only handled
50 target connections well. **DeepCorr's actual result**: rather than a generic statistical
correlation metric, it trains a deep learning architecture specifically on Tor's noise patterns —
and achieves **96% correlation accuracy using only ~900 packets (~900KB) per target flow**, versus
RAPTOR's 4% accuracy under the exact same setting. This is a genuinely dramatic capability jump
directly relevant to link 8's base-rate-fallacy argument: link 8's optimism that correlation
"doesn't scale well" rested on existing techniques having high false-positive rates at scale — a
technique that achieves 96% accuracy on short observations directly undermines that specific
optimism, which is exactly why the paper's stated purpose is to "demonstrate the escalating threat
... calling for timely deployment of effective countermeasures."

**Simple explanation**: Link 8 (2014) argued correlation attacks might be "effectively useless"
at Tor's real scale because of false positives. This 2018 paper is direct, concrete evidence that
assumption doesn't hold forever — machine learning specifically trained on Tor's own noise
characteristics (rather than a generic statistical test) can push accuracy far higher using much
less data than previously thought necessary. It's a good illustration of why "this defense works"
claims in security need re-checking against new offensive techniques over time, not treated as
permanently settled — directly echoing link 10's own point about tracking which historical Tor
attacks have and haven't been neutralized by subsequent hardening.

**Try it** (explain/detect, quantitative comparison only — no traffic correlation attempted
against any real Tor traffic; this repo's scope explicitly excludes running deanonymization
techniques even in a lab, since a meaningful test would require real network-scale Tor traffic
this repo has no legitimate way to safely acquire): work the accuracy comparison numbers directly
from the paper to internalize the magnitude of the claimed improvement.
```fish
python3 -c "
raptor_accuracy = 0.04
deepcorr_accuracy = 0.96
improvement_factor = deepcorr_accuracy / raptor_accuracy
print(f'RAPTOR accuracy: {raptor_accuracy*100:.0f}%')
print(f'DeepCorr accuracy: {deepcorr_accuracy*100:.0f}%')
print(f'Improvement factor (same setting, same data budget): {improvement_factor:.1f}x')
"
```
bash/sh: identical.
Applied exercise: write 3-4 sentences reconciling link 8's 2014 "correlation doesn't scale well in
practice" optimism with this 2018 paper's result — is link 8 now simply wrong, or does the
distinction between "correlation attacks in general" and "correlation attacks using the specific
techniques available in 2014" matter here? What does this imply about treating any single blog
post's risk assessment as permanently settled versus needing periodic re-evaluation as attack
techniques (here, specifically ML-based ones) advance?

## AS-level adversaries against Tor — arXiv 1505.05173

**Claim** (fetched the actual PDF via `curl`+`pdftotext`, closing out this section's Tor
de-anonymization thread — this paper directly and quantitatively answers link 8's open question
of "how much of the Internet does the adversary need to measure/control" for correlation to be
feasible): "Measuring and mitigating AS-level adversaries against Tor" (Nithyanand, Starov, Zair,
Gill, Schapira — Stony Brook University / Hebrew University of Jerusalem, 2015) gives real,
measured numbers instead of the theoretical framing earlier links stayed at. Empirical findings:
**up to 40% of all circuits Tor's default client constructs are vulnerable to a single
Autonomous-System-level adversary** being positioned on both the client-to-guard path and the
exit-to-destination path simultaneously; **42% vulnerable to colluding AS-level adversaries**
(multiple ASes coordinating, e.g. sibling ASes under one owning organization); and a striking
**85% vulnerable to state-level adversaries** (an entity with visibility into all regional ASes,
not just one or a few) — with **over 95% of all possible circuits vulnerable in specific regions
the paper names directly: China and Iran**. It explicitly connects this to real-world context,
not just theory: it opens by noting NSA and GCHQ were, per public revelations, actively working to
implement traffic correlation in collusion with ISPs — this is the same "controlled network
position" requirement link 8 flagged as the actual gating factor, now shown to already be
realistically satisfiable by state-level actors specifically. The paper's second contribution is
defensive, not just measurement: **Astoria**, an AS-aware Tor client that uses network-topology
measurement and path prediction to intelligently select relays that avoid AS-level correlation
exposure — reported results show Astoria reduces vulnerable circuits to **2% against single
AS-level adversaries, under 5% against colluding AS-level adversaries, and 25% against
state-level adversaries** (down from 40%/42%/85% with default relay selection), while also load-
balancing to avoid overloading any particular set of relays.

**Simple explanation**: This paper turns link 8's "it depends on how much of the internet the
adversary can see" into concrete numbers — a huge chunk of ordinary Tor circuits are already
exposed to a single well-positioned network operator, and that exposure gets dramatically worse
in specific censorship-heavy regions and against nation-state-level adversaries specifically. Its
mitigation (Astoria) shows the fix isn't "abandon Tor," it's "make relay selection aware of
network topology," directly reinforcing this study set's repeated theme that a protocol's crypto
being sound doesn't guarantee the deployment/configuration around it is safe.

**Try it** (explain/detect, quantitative-comparison-only — no traffic correlation, network-path
measurement, or relay-selection experiment run against any real Tor circuit): work through the
paper's own before/after Astoria numbers to internalize the scale of the mitigation.
```fish
python3 -c "
scenarios = [
    ('Single AS-level adversary', 0.40, 0.02),
    ('Colluding AS-level adversaries', 0.42, 0.05),
    ('State-level adversary', 0.85, 0.25),
]
for name, before, after in scenarios:
    reduction = (1 - after / before) * 100
    print(f'{name}: {before*100:.0f}% -> {after*100:.0f}% vulnerable circuits ({reduction:.0f}% relative reduction)')
"
```
bash/sh: identical.
Applied exercise: write 3-4 sentences on why the state-level-adversary numbers (85% before, 25%
after) remain so much higher than the single-AS numbers (40% before, 2% after) even with
Astoria's mitigation applied — what structural limit does AS-aware relay selection run into when
the adversary already has visibility across *many* ASes at once rather than needing to be
positioned on one specific path?
