# 5. Secure Design / Mitigation Topics for Developers — Notes

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 5.

## Formal protocol verification with Tamarin Prover (used to verify WireGuard, TLS 1.3)

**Note**: `tamarin-prover.github.io` redirects (301) to `tamarin-prover.com` — the project moved
its docs off GitHub Pages at some point; both WebFetch and a manual follow of the redirect worked
fine here.

**Claim**: Tamarin is a **symbolic** (Dolev-Yao model) protocol verifier — distinct from and
complementary to the **computational** verifier (CryptoVerif) used in section 1's WireGuard
mechanised-proof paper (link 4): a symbolic prover treats cryptographic primitives as perfect black
boxes (an attacker can never break the crypto itself, only misuse protocol logic), which makes it
faster/more automatable at finding *logic* flaws, at the cost of not being able to rule out
cryptanalytic weaknesses in the primitives themselves — exactly the gap the WireGuard mechanised
proof paper's own introduction pointed out when explaining why it went further than a prior
Tamarin analysis of WireGuard. Protocols are specified in **multiset rewriting rules** (`.spthy`
files, "security protocol theory") — verified by fetching a real example: the tutorial file
defines `rule` blocks (`Register_pk`, `Client_1`, `Client_2`, `Serv_1`, etc. — one rule per protocol
step/message) and separate `lemma` blocks stating the properties to check (`Client_session_key_
secrecy`, `Client_auth`, `Client_auth_injective`) using first-order logic quantified over
timepoints. Tamarin has three operating modes: a GUI that auto-searches for attacks/proofs with
visual attack-graph output, an interactive mode for manually guiding the proof/attack search on
protocols too complex to fully automate, and a command-line batch mode. Verified-relevant protocols
it has analyzed (from the live site): TLS 1.3, 5G-AKA, **Noise** (the framework underlying
WireGuard's handshake, section 0's last entry), EMV chip-and-pin, Apple iMessage — and a dedicated
`wireguard-tamarin` repo exists under the WireGuard project's own git host (found in section 1,
link 3's repo-family listing), confirming the "used to verify WireGuard" claim directly rather than
by association with Noise alone.

**Simple explanation**: Where the WireGuard CryptoVerif paper (section 1, link 4) asks "could an
attacker break the actual math," Tamarin asks "even assuming the math is unbreakable, could an
attacker trick the protocol's *logic* into doing the wrong thing" (e.g. replaying a message,
confusing two sessions, impersonating a party by reordering steps) — both angles matter, which is
why real high-stakes protocols (TLS 1.3, WireGuard) tend to get verified by both approaches rather
than just one.

**Try it**: Since this is a formal-verification tool rather than a runnable CLI utility in the usual
sense, the concrete exercise is: confirm it's installable on this machine (Arch ships it in the
official `extra` repo, verified via `pacman -Si`, ~1.1MB download) without necessarily installing it
system-wide in this session, and fetch a real `.spthy` example file to read its rule/lemma structure
directly:
```fish
pacman -Si tamarin-prover
```
```
# bash/sh:
pacman -Si tamarin-prover
```
(install with `sudo pacman -S tamarin-prover` if you want to actually run it — optional, root,
not required for this exercise)
```fish
curl -s https://raw.githubusercontent.com/tamarin-prover/tamarin-prover/master/examples/Tutorial.spthy -o (mktemp -t Tutorial.XXXX.spthy)
```
```
# bash/sh:
curl -s https://raw.githubusercontent.com/tamarin-prover/tamarin-prover/master/examples/Tutorial.spthy -o /tmp/Tutorial.spthy
```
then confirm the rule/lemma structure with `grep -E` (unescaped `|` — recall the fish/`ugrep`
alternation note from section 1: `\|` silently matches nothing here):
```fish
grep -E -n "^rule|^lemma" /tmp/Tutorial.spthy
```
```
# bash/sh:
grep -En "^rule|^lemma" /tmp/Tutorial.spthy
```
verified locally: 6 `rule` blocks (`Register_pk`, `Get_pk`, `Reveal_ltk`, `Client_1`, `Client_2`,
`Serv_1`), 4 `lemma` blocks (`Client_session_key_secrecy`, `Client_auth`, `Client_auth_injective`,
`Client_session_key_honest_setup`) — read the tutorial's own prose explaining what each models; no
Tamarin installation required just to read and understand the `.spthy` syntax.

## Specifying secure protocol implementations via model generation (AutoTam)

**Claim** (research paper — core argument/model, June 2026, arXiv:2606.19937): Wilson, Asplund &
Johansson identify the practical gap this whole section keeps circling back to — a Tamarin proof
(link 1) verifies an abstract *model* of a protocol, not the actual *implementation* code, and
bridging that gap has historically required expert manual modeling effort, which is exactly why
formal verification sees low industrial adoption despite good tooling. **AutoTam** is their answer:
a domain-specific language in which you write the protocol implementation directly (state machine,
message parsing/serialization, crypto operations, in an imperative style resembling normal code),
and the tool both (a) executes the DSL directly via an interpreter (for real interoperability
testing) and (b) automatically translates the same DSL description into a **sound, verifiable
Tamarin model** — with a soundness proof that verified trace properties on the generated model
actually transfer back to the implementation. Unlike prior model-extraction approaches (ProScript,
SPS) which explicitly forbid loops/recursion and are limited to linear handshakes, AutoTam encodes
arbitrary finite state machines, so it can also model unbounded transport phases (not just the
handshake) — directly relevant to VPN protocols, which are mostly transport-phase traffic after a
short handshake. Their two case studies: a signed Diffie-Hellman key exchange, and a **full
WireGuard implementation** written in AutoTam — and the concrete, verified-strong result: their
generated WireGuard implementation is **interoperable with both the official Linux kernel
implementation and the official Go userspace implementation** (some features omitted: DoS
mitigation/cookies and timed renegotiation), meaning this isn't just a toy model, it's a working
WireGuard peer that happens to also be formally verified by construction. This directly extends
section 1's WireGuard mechanised-proof paper (link 4, CryptoVerif) and this section's link 1
(Tamarin symbolic proofs) with a third angle: verify the *actual code path*, not just a hand-written
abstraction of the protocol.

**Simple explanation**: Normally there's a translation gap between "we proved this abstract protocol
model secure" and "this specific line of C/Go code correctly implements that model" — a bug could
live entirely in that gap (the model is right, the code diverges from it). AutoTam's pitch is
"write the implementation and get the verified model as an automatic byproduct of the same source,"
which closes that gap by construction instead of requiring a separate, error-prone manual step to
keep the model and the code in sync.

**Try it**: Read the paper's own Contributions and WireGuard case-study sections directly:
```fish
set paper_pdf (mktemp -t autotam.XXXX.pdf)
curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/2606.19937
pdftotext -layout $paper_pdf - | grep -n -B2 -A5 "interoperable with"
```
```
# bash/sh:
paper_pdf=/tmp/autotam.pdf
curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/2606.19937
pdftotext -layout "$paper_pdf" - | grep -n -B2 -A5 "interoperable with"
rm -f "$paper_pdf"
```
Then write a short paragraph, as a design exercise, on what "features omitted: DoS mitigation and
timed renegotiation" implies about the current practical scope of this approach — connect it back
to the WireGuard whitepaper's own cookie/DoS-mitigation mechanism (section 1, link 2's notes) and
consider why that specific mechanism might be harder to model formally than the core handshake
(hint: it involves timing/load-based decisions, not just a fixed message exchange).

## Elastic Common Schema (normalize logs to resist parsing/evasion gaps)

**Claim**: ECS solves a problem this file has implicitly relied on throughout section 3 — every
Sigma rule's `logsource:` block and every Elastic rule's `query:` assumes specific field names
(`Image`, `CommandLine`, `process.pid`, etc.), and those field names only mean the same thing across
different log sources if there's a shared naming convention normalizing them. ECS is exactly that:
an open specification of standardized field names + Elasticsearch datatypes so events from Elastic
products, third-party tools, or custom applications all normalize onto the same schema — "was this
field called `src_ip`, `source_address`, or `client.ip` in the raw log" becomes a solved problem
instead of a per-source parsing puzzle a detection engineer has to redo for every new data source.
Structurally (verified against the live field reference, ECS v9.4.0 at time of fetch): fields are
organized into **"field sets"** — `Base` (fields at the root of every event), then object-namespaced
sets like `Host`, `User`, `Network`, `Event`, `Client`/`Destination`/`Source` (network connection
endpoints), `Process`, `Cloud`, `Container`, `Code Signature`, `Autonomous System`, and more. The
schema is explicitly **permissive/extensible** — organizations can append custom fields for data
that doesn't fit standard mappings, rather than being forced to discard non-standard data or corrupt
the schema to fit it.

**Simple explanation**: If Sigma (section 3) is "one rule format that many SIEMs can consume," ECS
is the field-naming equivalent one layer down — "one set of field names that many log sources can
normalize onto," so a rule written against `process.command_line` behaves consistently regardless
of whether the underlying event originated from a Windows Sysmon log, a Linux auditd log, or a
custom application log, as long as all three were normalized into ECS first. The "resist
parsing/evasion gaps" framing in the source list's link title connects directly to section 4's
MITRE ATT&CK Stealth/T1070 notes — an attacker who structures a log-worthy action to exploit
inconsistent field parsing (e.g. an ambiguous log line that a naive parser mis-extracts) is
attacking the normalization layer itself; a consistent, well-specified schema like ECS narrows that
attack surface by making "how do I parse this field" a solved, shared problem rather than an
ad-hoc one per pipeline.

**Try it**: List the actual field sets from the live reference (not from memory) and note which
ones map onto fields already used in this file's own Sigma/Elastic rule exercises (section 3):
```fish
curl -sL "https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html" -o (mktemp -t ecs-fields.XXXX.html)
```
```
# bash/sh:
curl -sL "https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html" -o /tmp/ecs-fields.html
```
then de-tag (same Python pattern used throughout sections 2 and 4) and confirm the `Host`,
`Network`, `Event`, and `User` field sets exist, along with their one-line descriptions.

## Fuzzing implementations for protocol/parser robustness (AFL++)

**Claim**: AFL++ is a coverage-guided fuzzer — a maintained successor to the original AFL
(american fuzzy lop) with community patches (QEMU mode, collision-free coverage, laf-intel/RedQueen
instrumentation, AFLfast++ power schedules, custom mutators, etc), verified live via GitHub API
(6,692 stars, C, actively maintained). Its core idea, directly relevant to every parser this file
has touched (WireGuard's fixed-format cells from section 1, Tor's cell format from section 2,
Sigma/Elastic rule parsers from section 3): **feed a target program semi-random, mutated input and
use code-coverage feedback to steer future mutations toward inputs that reach new code paths** —
this is exactly how a WireGuard handshake-message parser, a Tor cell parser, or a Sigma YAML loader
could be tested for crashes/memory-safety bugs on malformed input, which is precisely the class of
bug the client-side VPN vulnerabilities paper (section 4, link 1) and the OWASP secure-coding
checklist (section 0) both warn about generically. Verified locally by fetching the repo's own
canonical minimal target, `test-instr.c` (the file AFL's own build system uses to test itself): the
harness pattern is simple — read bytes from stdin or a file argument into a fixed-size buffer, then
branch on the content (`switch (buf[0])`). This is the template shape every real harness follows:
**take attacker-controlled bytes in, feed them to the parsing/decoding logic under test, and let
AFL++'s instrumentation observe which code paths get hit.** Directly connecting to something already
found in this file: section 1's `wireguard-tools` clone (link 3's exercise) has its own `src/fuzz/`
directory — confirming a real WireGuard-adjacent codebase already does exactly this kind of testing
on its config/key parsing code.

**Simple explanation**: A fuzzer is an automated "throw weird, broken, or unexpected input at the
parser and see if it crashes" tool — parsers are exactly where a lot of real vulnerabilities live
(buffer overflows, integer overflows, out-of-bounds reads) because they're the code that must
handle attacker-controlled bytes before any validation has happened. AFL++'s coverage feedback is
what makes it smarter than pure random fuzzing: it remembers which mutations reached new code, and
mutates further from there, so it explores the parser's actual logic instead of just retrying blind
guesses.

**Try it** (sketch a harness target, no multi-hour fuzz campaign required — this is explicitly the
recommended scope for this kind of link per this repo's conventions): fetch the real minimal
example harness and use it as a template to sketch (in comments/pseudocode, not necessarily
compiled+run) what a harness for a small, real parsing function from this file's own material would
look like — e.g. a function that parses a WireGuard handshake Type-1 message's fixed byte layout
(section 1, link 1's notes: `CircID`/sender index, ephemeral pubkey, encrypted static key, encrypted
timestamp, 2 MACs):
```fish
curl -s https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/stable/test-instr.c | head -40
```
```
# bash/sh:
curl -s https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/stable/test-instr.c | head -40
```
Confirm AFL++ is installable here without installing it yet (verified: Arch `extra` repo):
```fish
pacman -Si afl++
```
```
# bash/sh:
pacman -Si afl++
```

## Detection-as-Code CI/CD validation workflow

**Claim**: This article is the *concrete implementation* of two things already covered separately
in this file: section 3's Detection-as-Code methodology (link 5) and Splunk Attack Range (link 6) —
it's Splunk's own real security-content repository's CI/CD pipeline, split into stages: (1)
**Customize** (fork the repo, modify deployments/macros for a specific environment), (2)
**Validate** (automated checks before anything ships), (3) **Generate** (produce actual Splunk
config files from the source YAML), (4) **Package** (build the deployable app), (5) **Test** (this
article's own Part 2, which uses **Attack Range** — section 3, link 6 — to generate real telemetry
and confirm detections actually fire), (6) **Deploy** via CI. The concrete validation script
(`validate.py`) is the direct real-world analogue of this file's own toy CI validation script
(section 3, link 5's exercise) — it checks YAML syntax, spec adherence, that lookups/macros
referenced in a detection actually exist and are defined, UUID uniqueness (preventing duplicate
rule IDs — directly the same concern as this file's own toy Sigma rules' `id:` fields), naming
conventions, and field-format validation (dates, ASCII content). This closes the loop the whole
file has been building toward: **Sigma/Elastic rule format (section 3) → written rules stored as
version-controlled YAML → validated by an automated script (this link) → tested against real
telemetry from Attack Range (section 3, link 6) → deployed via CI** — a complete, real, end-to-end
detection-engineering pipeline, not a hypothetical one.

**Simple explanation**: This is Splunk showing its own homework — a real six-stage pipeline that
takes a YAML detection rule from "someone wrote it" to "it's running in production and was tested
against actual attack telemetry first," with an automated validation gate at every stage so a
malformed or duplicate rule can't silently ship. It validates the exact things this file's own toy
CI script (section 3) checked in miniature (`title`/`id`/`logsource`/`detection`/`level` fields
present) plus more real-world specifics (macro/lookup existence, UUID uniqueness, date formats).

**Try it**: Read the article directly and connect its 6-stage pipeline to the two other tools
already covered in this file (Attack Range for step 5, this file's own toy validation script from
section 3 as a miniature of step 2's `validate.py`):
```fish
curl -sL https://www.splunk.com/en_us/blog/security/ci-cd-detection-engineering-splunk-security-content-part-1.html -o (mktemp -t splunk-cicd.XXXX.html)
```
```
# bash/sh:
curl -sL https://www.splunk.com/en_us/blog/security/ci-cd-detection-engineering-splunk-security-content-part-1.html -o /tmp/splunk-cicd.html
```
Then extend this file's own toy CI validation script (section 3, link 5's exercise) with one more
check inspired by `validate.py`'s real checks: **UUID uniqueness across all rules in the directory**
(not just per-rule field presence) — sketch the extra check needed (a `set()` of seen `id:` values,
raising a failure on a second occurrence of the same UUID).
