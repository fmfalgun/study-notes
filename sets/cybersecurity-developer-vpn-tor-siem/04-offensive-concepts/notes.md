# 4. Offensive Concepts Developers Must Be Aware Of — Notes

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 4.

**Scope note**: this section covers real attack techniques and vulnerability classes (VPN
client-side bugs, traffic fingerprinting, Tor flow correlation, log tampering). Consistent with
this repo's existing scope boundary (see `tools/homelab-experiments/README.md`'s "Cybersecurity
scope" note), every entry here stays at coding/analysis and conceptual understanding — root cause,
why it's a design flaw, what a defensive fix looks like — and never becomes a how-to for scanning,
exploiting, or targeting a real device/network/service that isn't a throwaway local test setup.
"Try it" exercises are explicitly defensive/illustrative/build-oriented: reading the actual research
and summarizing its threat model, inspecting how a real project is designed to avoid the flaw class,
or sketching what a fuzzing harness target would look like — never instructions to run an exploit
against a real target.

## Client-side vulnerabilities in commercial VPNs (research)

**Claim** (research paper — core argument, not attack instructions): Bui, Rao, Antikainen & Aura
(Aalto University, 2019, arXiv:1912.04669) systematically audited how commercial VPN client
software actually configures VPN tunnels on Windows/macOS/Ubuntu across 7 protocols (PPTP, SSTP,
IKEv2, OpenVPN, SoftEther, Cisco IPsec, L2TP/IPsec), and found the root cause of every
vulnerability is the same design-flaw class: **client configuration defaults that silently
downgrade or skip a security property**, not weaknesses in the underlying cryptography itself.
Concrete instances (read locally via `pdftotext`, not paraphrased from a lossy summary): (1) PPTP —
Windows leaves encryption "Optional" rather than mandatory by default, so a MITM can negotiate the
connection down to plaintext during the PPP phase; the client accepts this because encryption was
never mandatory in the first place. (2) SSTP — Ubuntu's `sstp-client` ignores TLS certificate
verification failures entirely, regardless of the connection-manager UI setting that claims to
control this (a **UI-state/actual-behavior mismatch**, discovered by reading the client's own
source code, not guessing). (3) IKEv2 — several providers' StrongSwan config sets `rightid=%any`,
meaning the client will accept *any* certificate-holding server as legitimate regardless of
identity — this silently downgrades IKEv2's server authentication to whatever MS-CHAPv2 (used for
client auth) alone provides, which the paper notes is "equal to the strength of a single DES
encryption." (4) Cisco IPsec / L2TP-IPsec — nearly every provider studied uses one hardcoded,
often-public pre-shared key (e.g. literally `"12345678"`) shared across *all* users for IPsec tunnel
authentication, letting anyone who knows that key MITM any customer's connection. The paper's
proposed mitigations are all about **removing the unsafe default or the unsafe fallback path**, not
patching cryptography: force encryption in PPTP config, deprecate/replace the broken `sstp-client`,
fix `rightid` to actually pin the expected server identity, and stop reusing a single PSK across a
whole customer base (use per-user credentials instead). A meta-finding worth internalizing: "secure
by default" is explicitly named as the design principle whose absence causes most of these bugs —
every single vulnerability here is a case where the *secure* configuration was technically possible
but not the default, and providers' setup instructions never told users to change it.

**Simple explanation**: None of this is a cryptographic break — Diffie-Hellman, AES, and TLS all
work exactly as designed in every case. The vulnerability class is entirely "the app shipped with a
setting that quietly makes the crypto optional or the identity check meaningless, and nobody
noticed because it still says 'Connected' in the UI." This is the practical, concrete version of
the "engineering vs. primitives" theme from section 0 (Cryptography Engineering) — a perfect primer
mismatch between "the protocol is secure" and "this specific client, configured this specific way,
is secure."

**Try it**: Read the paper's own threat model and mitigation table directly (verified locally via
`curl`+`pdftotext`, since arXiv PDFs render poorly through lossy web-summary tools) and connect each
vulnerability class back to a concept already covered earlier in this file — e.g. the IKEv2
`rightid=%any` bug directly parallels a *correctly*-configured strongSwan setup from section 1
(links 5-6), so compare what a correct `rightid` value should contain instead:
```fish
set paper_pdf (mktemp -t vpn-clientside.XXXX.pdf)
curl -sL -o $paper_pdf https://arxiv.org/pdf/1912.04669
pdftotext -layout $paper_pdf - | grep -n -B2 -A10 "rightid"
```
```
# bash/sh:
paper_pdf=/tmp/vpn-clientside.pdf
curl -sL -o "$paper_pdf" https://arxiv.org/pdf/1912.04669
pdftotext -layout "$paper_pdf" - | grep -n -B2 -A10 "rightid"
rm -f "$paper_pdf"
```
Then write, purely as a design exercise (no scanning/targeting anything real), what a *correct*
`ipsec.conf` `rightid` setting should contain to close this specific class of flaw (hint: it should
pin the expected server's actual identity — a DN or hostname the client will refuse to deviate
from — rather than accepting `%any`).

## OpenVPN traffic fingerprinting (protocol-identification attack)

**Note on sourcing**: the first `curl` download of this arXiv PDF was silently truncated (5.4 MB,
`pdftotext` threw xref/trailer errors) — a plain retry (`curl --retry 2`) produced the correct
11.7 MB file that parsed cleanly. Worth remembering: a PDF that "downloads" but fails to parse
isn't necessarily corrupted at the source — check the file size against a second attempt before
assuming the format itself is broken.

**Claim** (research paper — threat model and mitigations, not a working detector): Xue, Ramesh,
Jain, Kallitsis, Halderman, Crandall & Ensafi ("OpenVPN is Open to VPN Fingerprinting," USENIX
Security 2024) show that OpenVPN — including its commonly-deployed *obfuscated* variants meant to
evade DPI-based censorship — can still be reliably identified by a network-level adversary (an ISP
or state censor) using three protocol-level signals: **byte pattern** (structural features of the
OpenVPN header even under obfuscation), **packet size** (the handshake phase produces a
distinctive, stable sequence of packet-size patterns that a threshold detector can match even
without decrypting anything), and **server response behavior** (how the server reacts to a
malformed or incomplete handshake attempt — the classic "active probing" pattern also used against
Tor bridges and other circumvention protocols). Their attacker model is explicitly a network-level
observer, not an endpoint compromise: a two-phase pipeline first passively filters candidate flows
by byte/size patterns, then actively re-probes surviving candidates by replaying/mutating a
handshake attempt to confirm the server responds like a real OpenVPN endpoint. Evaluated in
partnership with a real mid-size ISP, they identified over 85% of both vanilla and obfuscated
OpenVPN flows with negligible false positives — i.e. **this is not a theoretical attack, it was
validated as practical at real-ISP scale**. Root cause, matching this section's recurring theme: the
protocol's cryptographic security was never the weak point — its *detectability from the outside*
was, because handshake timing/sizing/error-behavior leaks structure even when payload content is
encrypted.

**Simple explanation**: Encryption hides *what* you're saying, not necessarily *that you're using a
particular protocol to say it* — OpenVPN's handshake has a fingerprint-able shape (like a
recognizable knock pattern) independent of the encrypted content, and a censor doesn't need to break
the encryption to block the connection, just to recognize the shape and drop it. This is the same
class of problem as TLS fingerprinting (JA3/JA4) applied specifically to VPN protocols.

**Try it** (defensive/design only — read the paper's actual mitigations, do not build or run a
fingerprinting tool against real traffic): fetch and read Section 10 (Discussion and Mitigations)
directly:
```fish
set paper_pdf (mktemp -t openvpn-fp.XXXX.pdf)
curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/2403.03998
pdftotext -layout $paper_pdf - | grep -n -A5 "Short-Term Mitigation"
```
```
# bash/sh:
paper_pdf=/tmp/openvpn-fp.pdf
curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/2403.03998
pdftotext -layout "$paper_pdf" - | grep -n -A5 "Short-Term Mitigation"
rm -f "$paper_pdf"
```
The three mitigations named (verified locally): (1) don't co-locate obfuscated and vanilla OpenVPN
servers on the same infrastructure — separate them so a fingerprint on the vanilla protocol doesn't
also unmask the obfuscated bridge; (2) switch from static to **random** padding in obfuscation
layers, ideally including zero-length padding-only packets, specifically to break the
one-to-one size correspondence between the unobfuscated and obfuscated packet stream that made
threshold-based size fingerprinting possible; (3) servers should not close failed-handshake
connections immediately or in a predictable/timing-distinctive way, since predictable failure
behavior is exactly what enables active-probing detection (a pattern the paper explicitly notes has
been used against other circumvention protocols too, not just OpenVPN). Write one paragraph
connecting mitigation (2) to WireGuard's own design (section 1) — does WireGuard's "silence is a
virtue" property (from the WireGuard whitepaper's own section title, section 1 link 2's notes)
already avoid this exact fingerprinting vector, and if so, how?

## Real-world critical IKEv1 auth-bypass exploitation (design flaw class)

**Claim** (news coverage of a disclosed, patched CVE — conceptual root cause, not exploit
instructions): CVE-2026-50751 (CVSS 9.3) is a critical authentication-bypass flaw in Check Point
Security Gateways/Spark Firewalls, specifically in **IKEv1** Remote Access VPN / Mobile Access
configurations. The root cause is a **logic flaw that skips certificate validation entirely** — the
vulnerable code path bypasses its own `verify_peer_auth`/`verifyMessagePhase1` checks under a
crafted condition (attackers manipulate authentication flags via a custom `VPNExtFeatures` Vendor
ID payload sent during IKE negotiation), meaning neither the certificate's signature nor its trust
chain gets checked at all — the exact same *category* of flaw as section 4 link 1's IKEv2
`rightid=%any` misconfiguration (client/server accepts an unauthenticated peer as if it were
authenticated), except here it's a code-level logic bug in the vendor's own implementation rather
than a misconfiguration by the VPN provider. This was actively exploited in the wild starting May
2026 against "a few dozen targeted organizations globally," including at least one case with a
known ransomware affiliate (Qilin) performing post-exploitation activity after the auth bypass —
i.e. this is a demonstrated, real, high-impact case of the exact vulnerability *class* (VPN
gateway authentication that can be silently skipped) that the client-side-vulnerabilities paper
(link 1) and OWASP secure-coding checklist (section 0) both warn about in the abstract. Check Point
shipped hotfixes, and CISA added it to the Known Exploited Vulnerabilities catalog with a mandated
federal patch deadline — the standard disclosure-to-patch lifecycle for a critical, actively
exploited flaw.

**Simple explanation**: Authentication code has an implicit contract — "always run the signature
and trust-chain check before accepting a peer as authenticated" — and this bug is exactly what
happens when a code path exists that can be routed around that contract under a crafted input. It's
the same root-cause shape as a classic auth-bypass logic bug in any system (e.g. a web app that
checks a JWT signature on one code path but not another): the fix isn't "add more crypto," it's
"make sure every code path that grants access actually calls the verification function, with no
skip condition an attacker can trigger."

**Try it** (conceptual/defensive only — this is a patched, disclosed CVE; do not attempt to
reproduce the exploit or scan for vulnerable Check Point devices): Read the article's technical
description again and write a short design note: what would a **defense-in-depth** check look like
that could have caught this class of bug even if the primary verification call were accidentally
skipped? (e.g. a post-condition assertion right before granting VPN access — "assert peer identity
was verified in this session" — that fails closed if the verification flag was never set, rather
than defaulting to "verified" when the check didn't run). This connects directly to section 1's
IKEv2 exchange notes (`IKE_AUTH` — link 7): write one sentence on which of the four IKE exchange
types this bug most directly subverts, and why authentication logic living inside a single
exchange's handler is a single point of failure worth defending with a second, independent check.

## Flow correlation / traffic-analysis attacks on Tor onion services (SUMo, NDSS 2024)

**Claim** (research paper — attack model and defenses, not a working attack tool): Lopes, Dong,
Medeiros, Castro, Barradas, Portela, Vinagre, Ferreira, Christin & Santos present **Sliding Subset
Sum (SUMo)**, a flow-correlation deanonymization attack specifically targeting Tor **onion service**
sessions (as opposed to prior work, which mostly targeted client→clearnet traffic). Threat model:
a set of **colluding ISPs** at multiple vantage points in the Tor network passively observe traffic
timing/volume patterns (not content — Tor's encryption is not broken) and use a distributed
pipeline (ML classifiers + a similarity function based on the classic subset-sum problem) to match
flow pairs — i.e. correlate "this client's traffic pattern" with "this onion service's traffic
pattern" even though the rendezvous-point architecture from section 2 (links 3-4) was specifically
designed to prevent either side from learning the other's identity/location directly. SUMo's
distinguishing property versus prior deep-learning correlators (DeepCorr, DeepCoFFEA, referenced in
this file's own section 4 introduction): ~100x higher throughput (~153,000 flow pairs/sec vs.
DeepCoFFEA) and lower memory use, making large-scale correlation attacks more *practical* for a
real multi-ISP adversary, not just theoretically possible. Root cause, matching the recurring
pattern in this section: the vulnerability isn't in Tor's cryptography, it's that **traffic
metadata (timing, volume) survives encryption** and circuit design alone doesn't fully hide that
metadata from an adversary positioned to observe both ends of a circuit.

**Simple explanation**: Even though Tor hides *what* is being said and *who* is directly connecting
to whom at the protocol layer, the *shape* of a conversation (when packets go out, how many, how
big) can still line up between the client side and the service side if an adversary can watch both
ends — like recognizing two people are on a call together by their timing pattern of pauses and
talking, without ever hearing what they're saying.

**Try it**: Read the paper's own Section VI ("Attack Countermeasures") — this is the
defensive/design-oriented content this exercise should focus on, not the attack mechanism itself:
```fish
set paper_pdf (mktemp -t sumo.XXXX.pdf)
curl -sL --retry 2 -o $paper_pdf https://www.ndss-symposium.org/wp-content/uploads/2024-337-paper.pdf
pdftotext -layout $paper_pdf - | grep -n -A5 "ATTACK C OUNTERMEASURES"
```
```
# bash/sh:
paper_pdf=/tmp/sumo.pdf
curl -sL --retry 2 -o "$paper_pdf" https://www.ndss-symposium.org/wp-content/uploads/2024-337-paper.pdf
pdftotext -layout "$paper_pdf" - | grep -n -A5 "ATTACK C OUNTERMEASURES"
rm -f "$paper_pdf"
```
Four countermeasures the authors propose (verified locally): (1) traffic **obfuscation** (e.g.
obfs4-style perturbation, already shown in prior work to meaningfully degrade a correlator's true
positive rate); (2) client generates **concurrent dummy clearnet traffic** while accessing an onion
service, to make separating "which flow is the real onion-service session" harder for the attacker;
(3) the onion service itself generates **concurrent dummy traffic** (spurious requests from
dummy clients it controls) to increase ambiguity server-side; (4) **geographic diversity** between
a client's and a service's guard-node selection, since correlation is easiest when both circuits'
guard nodes sit in the same region/ISP footprint. Note the paper's own ethics section explicitly
describes responsible-disclosure practice (disclosed to the Tor project before publication,
correlated only their own self-generated traffic, kept test `.onion` addresses private during data
collection) — the same "coding/analysis, never targeting a real uninvolved party" boundary this
repo already enforces.

## Deep-learning flow correlation attack (DeepCorr)

**Claim** (research paper — model/results and defenses, not attack tooling): Nasr, Bahramali &
Houmansadr (2018) show that flow correlation on Tor — the general technique of linking a
connection's ingress and egress traffic segments by their timing/size characteristics (SUMo, link 4
above, is a later, faster instance of this same technique applied specifically to onion services) —
becomes dramatically more effective when the correlation function is *learned* via deep learning
rather than hand-designed via generic statistical correlation. Root cause this paper identifies:
Tor relays deliberately don't obfuscate packet timing (obfuscating it would slow connections down,
hurting Tor's low-latency goal), so Tor's *natural* network jitter was assumed to be enough noise
to make correlation impractical at scale — prior state-of-the-art (RAPTOR) needed ~100MB/5min per
flow and still only handled ~50 target connections reliably. DeepCorr's neural network instead
learns Tor's *specific* noise characteristics directly from real Tor traffic (trained on 25,000
self-generated flows over ~1 day on a single GPU, re-trainable monthly to stay current), and the
concrete headline number is stark: **96% correlation accuracy vs. RAPTOR's 4%**, using only ~900
packets (~900KB) per flow — i.e. deep learning didn't just incrementally improve flow correlation,
it broke the "impractical at scale" assumption the Tor threat model had implicitly relied on. A
specific, actionable defensive finding from their own evaluation of existing pluggable transports
(directly useful for a builder deciding which obfuscation to actually deploy): **`meek` and
`obfs4-iat0` provide little protection against DeepCorr, while `obfs4-iat1` provides meaningfully
better protection** — but the paper notes none of these were widely deployed by public Tor relays
at publication time, and even `obfs4-iat1` ran on only a small fraction of bridges. The paper's own
proposed countermeasure: traffic obfuscation must actually be deployed broadly (not just exist as
an option), and better mechanisms are needed that don't impose large bandwidth/performance costs.

**Simple explanation**: This is the specific technical justification behind "obfuscated bridges
matter" — Tor's core protocol intentionally leaves packet timing unobfuscated for performance, and
this paper is proof that leaving it unobfuscated is exploitable at practical scale once an attacker
uses a learned (rather than hand-designed) correlation function. The `iat0` vs `iat1` distinction
(inter-arrival-time padding variants of obfs4) is a concrete example of "not all obfuscation
settings are equally effective" — a detail easy to miss if you assume "using obfs4" alone is
sufficient.

**Try it**: Fetch the paper and confirm the headline accuracy numbers and the pluggable-transport
comparison directly rather than trusting a paraphrase:
```fish
set paper_pdf (mktemp -t deepcorr.XXXX.pdf)
curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/1808.07285
pdftotext -layout $paper_pdf - | grep -n -B2 -A5 "obfs4-iat1 provides"
```
```
# bash/sh:
paper_pdf=/tmp/deepcorr.pdf
curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/1808.07285
pdftotext -layout "$paper_pdf" - | grep -n -B2 -A5 "obfs4-iat1 provides"
rm -f "$paper_pdf"
```
Then, as a design exercise, write one paragraph on why "deploy obfuscation as an opt-in bridge
feature used by a small fraction of relays" (the actual 2018 deployment state per this paper) is a
weaker defense than "make it the default for everyone" — connect this to the OpenVPN fingerprinting
paper's own mitigation #1 (link 2 above: don't co-locate obfuscated and vanilla servers) — both
papers converge on the same lesson: an obfuscation mechanism that's optional/rare is itself a
distinguishing signal.

## AS-level / infrastructure adversaries against Tor

**Note on sourcing**: `pdftotext` threw an `Internal Error: xref num 588 not found but needed, try
to reconstruct` warning on this PDF but successfully auto-recovered (1218 lines extracted, 92
mentions of the paper's own tool "Astoria" found) — a case where the warning was non-fatal, worth
knowing about since it looks alarming but the extraction still succeeded here (contrast with the
OpenVPN fingerprinting paper, link 2, where a truncated download produced a *hard* failure instead).

**Claim** (research paper — measurement results and the defensive tool it proposes, not attack
tooling): Nithyanand, Starov, Zair, Gill & Schapira quantify a threat model different from the
flow-correlation papers above (links 4-5) — not "an adversary correlating traffic they observe,"
but **"which network paths even give an adversary the *opportunity* to observe both ends of a Tor
circuit in the first place."** An Autonomous System (AS) sitting on both the client→guard path and
the exit→destination path can perform traffic correlation without controlling any Tor relay at
all — it just needs to be a normal ISP/transit network positioned on both path segments. Their
empirical measurement (combining real Internet topology maps with path-prediction simulation):
**up to 40% of Tor circuits are vulnerable to a single AS-level adversary**, 42% to colluding
AS-level adversaries, and a striking **85% vulnerable to a state-level adversary** (one with
visibility into all regional ASes) — with specific countries (China, Iran) showing over 95% of
possible circuits vulnerable, because Tor's default relay-selection algorithm has no concept of
network-path awareness at all, only bandwidth-weighted relay selection. Root cause, matching this
section's pattern again: not a cryptographic weakness, but a **selection-algorithm blind spot** —
Tor's path-selection never considered "does this guard+exit combination create a network path where
one AS can see both ends." The paper's proposed defense, **Astoria**, is a concrete, positive
engineering result worth internalizing: an AS-aware Tor client that does path-prediction before
selecting a circuit's relays, explicitly avoiding guard/exit combinations that share a
correlation-capable AS — this reduces vulnerable circuits from 40% down to **2%** against AS-level
adversaries, under 5% against colluding ASes, and 25% against state-level adversaries (still
nonzero, since a true state-level adversary with total regional visibility is a much harder bar to
clear), while explicitly load-balancing so it doesn't overload a small set of "safe" relays.

**Simple explanation**: Tor's 3-hop circuit design assumes the *guard* and *exit* choices are
independent enough that no single network entity naturally sees both ends — this paper shows that
assumption is often false in practice because of how the real Internet's AS-level routing actually
works, and demonstrates a fix (network-topology-aware relay selection) rather than just describing
the problem. It's the network-routing equivalent of the section 1 IKEv2 `rightid=%any` bug and the
IKEv1 CVE (links 1 and 3): a piece of the system trusted an assumption ("guard and exit are
independent") that wasn't actually being verified/enforced.

**Try it**: Fetch the paper and confirm the headline vulnerability percentages and Astoria's
mitigation numbers directly:
```fish
set paper_pdf (mktemp -t astoria.XXXX.pdf)
curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/1505.05173
pdftotext -layout $paper_pdf - | grep -n -B2 -A5 "Astoria reduces"
```
```
# bash/sh:
paper_pdf=/tmp/astoria.pdf
curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/1505.05173
pdftotext -layout "$paper_pdf" - | grep -n -B2 -A5 "Astoria reduces"
rm -f "$paper_pdf"
```
Then write one sentence connecting this paper's finding to section 2's rendezvous protocol notes
(link 3): onion services build circuits to *both* an introduction point and a rendezvous point —
does this AS-level threat apply equally to both circuit halves, or does one side's circuit
construction (client-chosen rendezvous point vs. service-pre-selected introduction points) carry
different AS-correlation risk?

## MITRE ATT&CK — Defense Evasion tactic (what your SIEM/log pipeline must survive)

**Naming note, verified directly against the live page**: the source list's link text calls this
"Defense Evasion," but the live page (fetched via `curl`, title tag confirmed) is now titled
**"Stealth, Tactic TA0005"** — "Last Modified: 12 May 2026" per the page's own metadata, meaning
MITRE renamed this tactic sometime in 2026, after this assistant's Jan 2026 knowledge cutoff. The
tactic ID (TA0005) is unchanged, only the display name — worth remembering that ATT&CK tactic
*names* aren't as stable an anchor as their IDs for any tooling/documentation that references them
by name (the Sigma rule tags and Elastic `[[rule.threat.tactic]]` fields from section 3 reference
IDs like `TA0005`, which is the more future-proof choice).

**Claim**: Stealth/Defense Evasion (TA0005) is the tactic covering "the adversary is trying to hide
and conceal their actions, appearing as normal behavior" — 30 techniques as of this fetch, spanning
obfuscation (T1027), hiding artifacts (T1564 — hidden files/users/windows/NTFS attributes),
masquerading as legitimate processes/binaries (T1036, T1218), process injection (T1055), rootkits
(T1014), and, most directly relevant to a SIEM/log pipeline builder: **T1070 Indicator Removal** —
"adversaries may selectively delete or modify artifacts generated to reduce indications of their
presence... rather than broadly removing evidence, adversaries may target specific artifacts that
appear anomalous... while leaving sufficient data intact to maintain the appearance of normal
system behavior" (verified quote from the live page). Confirmed T1070 subtechniques on this page:
`.003` Clear Command History, `.004` File Deletion, `.005` Network Share Connection Removal,
`.006` Timestomp (modifying file MACE timestamps to blend malicious files in with legitimate
ones), `.007` Clear Network Connection History and Configurations, `.008` Clear Mailbox Data,
`.009` Clear Persistence, and a separate `.005`-numbered "Indicator Removal from Tools" (removing a
detection signature from a tool once it's known to be flagged). Notable and worth flagging
explicitly: the `.001`/`.002` subtechniques this assistant recalls from training data as "Clear
Windows Event Logs" / "Clear Linux or Mac System Logs" were **not found** in this live fetch — only
referenced obliquely inside `.003`'s own description ("in addition to clearing system logs...").
This may reflect a genuine restructuring of that subtechnique in the 2026 update; flagged here for
manual re-check rather than asserted as fact, since it contradicts prior training knowledge and
this session could not independently confirm the current state of those specific IDs. Also newly
notable: **T1211**, renamed to "Exploitation for Stealth" (from "Exploitation for Defense Evasion"),
explicitly calls out "suppressing logging" as one of its stated adversary goals — directly on-topic
for a SIEM pipeline builder.

**Simple explanation**: This tactic is the checklist of "ways an attacker tries to make your
detection pipeline blind or wrong" — for a SIEM/detection engineer specifically, T1070 (and its
subtechniques) is the direct threat model behind "why does my pipeline need tamper-evidence,"
which is exactly what this section's final link (log/database tampering) and section 3's Elastic
Common Schema link (section 5) address defensively.

**Try it**: Confirm the tactic's current display name and the T1070 subtechnique list directly
rather than trusting cached/remembered knowledge of ATT&CK (a genuinely important habit given the
naming drift just found):
```fish
curl -sL https://attack.mitre.org/tactics/TA0005/ -o (mktemp -t attack-ta0005.XXXX.html)
```
```
# bash/sh:
curl -sL https://attack.mitre.org/tactics/TA0005/ -o /tmp/attack-ta0005.html
```
then de-tag (same Python one-liner pattern used for the torproject.org pages in section 2) and
grep the `<title>` tag plus "Last Modified" to confirm the naming/version, and grep for "T1070" to
confirm the current subtechnique list before relying on any assumption about which log-clearing
subtechnique IDs exist today.

## Log/database tampering attack pattern (design tamper-resistant pipelines against this)

**Claim**: Despite the source list's generic "log/database tampering" framing, this specific
ManageEngine article covers a concrete instance: **Active Directory credential database (NTDS.dit)
extraction**, the technique adversaries use to pull password hashes/Kerberos secrets out of a
domain controller for offline cracking or Pass-the-Ticket reuse — this is squarely a
"database tampering" attack in the sense that the AD database itself (or its live in-memory
equivalent) is the target, and it directly feeds into the T1070/log-tampering theme from the
previous link because attackers use specific techniques to *avoid triggering the audit events a
SIEM would otherwise catch this with*. Four extraction techniques described: (1) **Install-From-
Media (IFM)** via the legitimate `ntdsutil.exe` — abusing a built-in admin tool to create a
portable NTDS.dit + SYSTEM hive copy *without triggering standard VSS (Volume Shadow Copy Service)
audit events*, i.e. the attack specifically routes around the expected detection signal; (2)
**"Ninja-Copy"** raw-disk reads that bypass file locks entirely, again circumventing normal audit
logging; (3) Kerberos ticket extraction from memory via PowerShell/SSPI for Pass-the-Ticket; (4)
LSASS memory dumping (the Windows MiniDump API) to pull plaintext credentials/NTLM hashes. The
recurring theme across all four: **each technique specifically targets the gap between "what a
naive detection setup watches for" and "what the actual extraction mechanism triggers"** — the
whole article is effectively a case study in why a detection engineer must think about *evasion of
the detector*, not just the primary malicious action. Concrete SIEM-relevant detection signals
named: Windows Event ID 4688 (process creation — catches `ntdsutil.exe` invoked with
`ifm`/`create full`/`activate instance ntds` arguments), Event ID 4663 (object access — catches
direct access attempts against the NTDS.dit file itself), Sysmon process-parent relationships, and
file-creation monitoring for `.dit`/`.dmp` files landing in unexpected user-writable paths.
Hardening recommendations: tiered access + privileged access workstations for domain controller
access, Credential Guard to isolate LSASS secrets from usermode access entirely, AppLocker/WDAC to
block `ntdsutil.exe` outside documented provisioning windows, Protected Users group membership to
prevent NTLM fallback, scheduled + emergency KRBTGT rotation, and PowerShell Constrained Language
Mode on domain controllers.

**Simple explanation**: This is a worked example of "attackers use legitimate admin tools in ways
that specifically avoid the logging you'd expect" — `ntdsutil.exe` is a real, documented Microsoft
tool, so its mere existence/execution isn't inherently suspicious; the SIEM detection has to be
specific enough (watching *which arguments* it's invoked with, *which* file it touches) to
distinguish a legitimate backup operation from a credential-theft attempt. It's the direct, concrete
payoff of everything in section 3 (Sigma/Elastic rule-writing): a well-written detection rule for
this exact scenario would be a `process_creation` Sigma rule matching `ntdsutil.exe` +
`CommandLine|contains: 'ifm'` — structurally identical to this file's own toy Sigma rules from
section 3.

**Try it**: Fetch the article and confirm the specific Event IDs and command-line indicators named,
then write a Sigma-style detection sketch for the IFM technique using this section 3's own
conventions (schema-valid YAML, no need to deploy it anywhere):
```fish
curl -sL https://www.manageengine.com/log-management/siem-use-cases/threats/active-directory-database-tampering.html -o (mktemp -t ad-tampering.XXXX.html)
```
```
# bash/sh:
curl -sL https://www.manageengine.com/log-management/siem-use-cases/threats/active-directory-database-tampering.html -o /tmp/ad-tampering.html
```
then sketch (defensive design only — do not run `ntdsutil.exe` against any real domain controller)
a Sigma rule: `logsource: {category: process_creation, product: windows}`, `detection: {selection:
{Image|endswith: '\ntdsutil.exe', CommandLine|contains: ['ifm', 'create full']}, condition:
selection}` — validate it with the same `yaml.safe_load` check used throughout section 3.
