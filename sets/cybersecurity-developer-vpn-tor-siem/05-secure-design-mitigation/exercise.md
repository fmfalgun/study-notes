# 5. Secure Design / Mitigation Topics for Developers — Exercises

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 5.

## 1. Tamarin Prover — inspect a real .spthy file's rule/lemma structure

1. Confirm Tamarin is installable on this machine without installing it yet (verified: official
   Arch `extra` repo, ~1.1MB download):
   ```fish
   pacman -Si tamarin-prover
   ```
   ```
   # bash/sh:
   pacman -Si tamarin-prover
   ```
   (Optional, root: `sudo pacman -S tamarin-prover` to actually install and run it later — not
   required for this exercise.)
2. Fetch the project's own tutorial `.spthy` file:
   ```fish
   curl -s https://raw.githubusercontent.com/tamarin-prover/tamarin-prover/master/examples/Tutorial.spthy -o (mktemp -t Tutorial.XXXX.spthy)
   ```
   ```
   # bash/sh:
   curl -s https://raw.githubusercontent.com/tamarin-prover/tamarin-prover/master/examples/Tutorial.spthy -o /tmp/Tutorial.spthy
   ```
3. List its rule/lemma structure (use `grep -E` with an unescaped `|` — `\|` silently fails under
   this machine's fish `grep`/`ugrep` alias, verified in section 1):
   ```fish
   grep -E -n "^rule|^lemma" /tmp/Tutorial.spthy
   ```
   ```
   # bash/sh:
   grep -En "^rule|^lemma" /tmp/Tutorial.spthy
   ```
4. Read the tutorial's own prose (open the file directly) describing the toy protocol it models (a
   client encrypts a fresh symmetric key to a server's public key; the server confirms receipt with
   a hash of the key) and match each `rule` block to a step of that protocol.
5. Read the `Client_session_key_secrecy` lemma and write one sentence, in your own words, on what
   security property it's asserting and under what assumption (hint: it's conditional on the server
   being uncompromised — note the exact wording in the file).
6. Summarize the specific theorem being proved by ONE of the four lemmas, and why it matters for a
   real protocol like WireGuard's Noise_IK handshake (section 0's Noise notes, section 1's WireGuard
   whitepaper notes) — i.e. what would go wrong for WireGuard if the equivalent of this lemma were
   false for its handshake.
7. Clean up:
   ```fish
   rm -f /tmp/Tutorial.spthy
   ```

## 2. AutoTam — read the WireGuard case study and reason about its scope limits

1. Fetch the paper:
   ```fish
   set paper_pdf (mktemp -t autotam.XXXX.pdf)
   curl -sL --retry 2 -o $paper_pdf https://arxiv.org/pdf/2606.19937
   ```
   ```
   # bash/sh:
   paper_pdf=/tmp/autotam.pdf
   curl -sL --retry 2 -o "$paper_pdf" https://arxiv.org/pdf/2606.19937
   ```
2. Confirm the WireGuard interoperability claim directly (verified locally: interoperable with
   both the official Linux kernel implementation and the official Go userspace implementation):
   ```fish
   pdftotext -layout $paper_pdf - | grep -n -B2 -A5 "interoperable with"
   ```
   ```
   # bash/sh:
   pdftotext -layout "$paper_pdf" - | grep -n -B2 -A5 "interoperable with"
   ```
3. Read Section 7.2 ("The WireGuard VPN Protocol") and write 2-3 sentences summarizing what
   AutoTam's WireGuard implementation actually covers (the handshake, transport-phase message
   exchange, cryptographic operations) versus what it explicitly omits (DoS mitigation/cookies,
   timed renegotiation).
4. Cross-reference to section 1's WireGuard whitepaper notes (link 2): explain in one paragraph why
   the omitted features (cookie-based DoS mitigation specifically) might be structurally harder to
   express in a finite-state-machine-based DSL than the core 2-message handshake — think about
   whether DoS mitigation is a fixed message sequence or a *load/timing-conditional* decision.
5. Write one sentence on how this paper's approach (verify-by-construction from a single DSL
   source) differs from the two other verification approaches already covered in this file: the
   CryptoVerif computational proof (section 1, link 4, verifies a hand-written model against real
   WireGuard's spec) and Tamarin symbolic proofs (this section, link 1, also verifies a hand-written
   model) — what's the key structural difference in where the "translation gap" risk lives?
6. Clean up:
   ```fish
   rm -f $paper_pdf
   ```
   ```
   # bash/sh:
   rm -f "$paper_pdf"
   ```

## 3. Elastic Common Schema — list field sets and map them onto this file's own rules

1. Fetch the live ECS field reference (note current version, e.g. `9.4.0` as of this fetch — ECS
   versions regularly, so re-confirm the version when revisiting):
   ```fish
   curl -sL "https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html" -o (mktemp -t ecs-fields.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL "https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html" -o /tmp/ecs-fields.html
   ```
2. De-tag it (same Python pattern used in sections 2 and 4) and list the field-set table:
   ```fish
   python3 -c "
   import re, html
   with open('/tmp/ecs-fields.html') as f:
       t = f.read()
   t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
   t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
   t = re.sub(r'<[^>]+>', ' ', t)
   print(html.unescape(t))
   " > /tmp/ecs-fields.txt
   sed -n '/Field sets/,/^ Base /p' /tmp/ecs-fields.txt | head -60
   ```
3. For each of the field names actually used in this file's toy/real Sigma and Elastic rules
   (section 3: `Image`, `CommandLine`; section 4: `process.command_line` style fields from the real
   Elastic TOML rule), identify which ECS field set it would fall under (`Process`, most likely) —
   write down the mapping.
4. Write one sentence on what "permissive/extensible" schema design means in practice: if a log
   source has a genuinely unique field with no ECS equivalent, what's the correct thing to do
   according to ECS's own design philosophy (hint: it's not "force it into the nearest existing
   field" or "drop the data").
5. Connect to section 4's MITRE ATT&CK notes: write one sentence on how a consistent, shared field
   schema across log sources narrows the "parsing gap" attack surface an adversary might otherwise
   exploit by crafting logs that a naive, source-specific parser mis-extracts.
6. Clean up:
   ```fish
   rm -f /tmp/ecs-fields.html /tmp/ecs-fields.txt
   ```

## 4. AFL++ — sketch a fuzzing harness for a WireGuard message parser (no actual fuzz campaign)

This exercise sketches a harness target as illustrative design work — it does not compile, build,
or run an actual multi-hour fuzz campaign, per this repo's scope for offensive-adjacent tooling.

1. Confirm AFL++ is installable here (verified: Arch `extra` repo, no need to install for this
   exercise):
   ```fish
   pacman -Si afl++
   ```
   ```
   # bash/sh:
   pacman -Si afl++
   ```
2. Fetch AFL++'s own canonical minimal harness (`test-instr.c`) as a structural template:
   ```fish
   curl -s https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/stable/test-instr.c -o (mktemp -t test-instr.XXXX.c)
   ```
   ```
   # bash/sh:
   curl -s https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/stable/test-instr.c -o /tmp/test-instr.c
   ```
   read it and identify the three structural parts every harness needs: (a) get bytes in (stdin or
   file argument), (b) feed them to the function under test, (c) exit/return normally on valid-but-
   uninteresting input so AFL++ can tell "handled gracefully" apart from "crashed."
3. Sketch (pseudocode/comments only, no need to compile) a harness for parsing a WireGuard
   handshake Type-1 message, using section 1 link 1's documented byte layout (sender index,
   unencrypted ephemeral pubkey, encrypted static pubkey, encrypted timestamp, two MACs):
   ```c
   // illustrative sketch only — not a working harness
   #include <stdio.h>
   #include <unistd.h>

   // assume this function exists in the real codebase under test:
   // int parse_handshake_init(const uint8_t *buf, size_t len);

   int main(int argc, char **argv) {
       uint8_t buf[256];
       ssize_t n = read(0, buf, sizeof(buf));  // read attacker-controlled bytes from stdin
       if (n < 0) return 1;

       // feed the raw bytes straight to the parser under test —
       // this is the exact code path AFL++ will fuzz
       int result = parse_handshake_init(buf, (size_t)n);

       // exit cleanly on any outcome; a crash/ASAN abort is what AFL++ is looking for
       return 0;
   }
   ```
4. Write one sentence on why the harness should call the *real* parsing function from the codebase
   (not a reimplementation) — what would be lost if the harness tested a simplified stand-in instead
   of the actual parser shipped in production?
5. Cross-reference: confirm `wireguard-tools`' own `src/fuzz/` directory (found in section 1, link
   3's exercise) already does something structurally similar — note which of its files (`config.c`,
   `setconf.c`, `uapi.c`) are fuzz-harness wrappers around real parsing code, by re-fetching that
   listing if needed:
   ```fish
   git clone --depth 1 https://git.zx2c4.com/wireguard-tools /tmp/wg-tools-src ; and ls /tmp/wg-tools-src/src/fuzz ; and rm -rf /tmp/wg-tools-src
   ```
   ```
   # bash/sh:
   git clone --depth 1 https://git.zx2c4.com/wireguard-tools /tmp/wg-tools-src && ls /tmp/wg-tools-src/src/fuzz && rm -rf /tmp/wg-tools-src
   ```
6. Clean up:
   ```fish
   rm -f /tmp/test-instr.c
   ```

## 5. Splunk CI/CD detection engineering — write a UUID-uniqueness validation check

1. Fetch the article and identify all 6 pipeline stages (Customize, Validate, Generate, Package,
   Test, Deploy) plus which article-part covers Testing (Part 2, via Attack Range):
   ```fish
   curl -sL https://www.splunk.com/en_us/blog/security/ci-cd-detection-engineering-splunk-security-content-part-1.html -o (mktemp -t splunk-cicd.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://www.splunk.com/en_us/blog/security/ci-cd-detection-engineering-splunk-security-content-part-1.html -o /tmp/splunk-cicd.html
   ```
2. Recreate two toy rules with a **deliberately duplicated** `id:` field to test a UUID-uniqueness
   validator (this mirrors a real bug `validate.py`-style checks are designed to catch):
   ```fish
   mkdir -p /tmp/dac-demo2/rules
   ```
   ```
   # bash/sh:
   mkdir -p /tmp/dac-demo2/rules
   ```
   ```yaml
   # rules/rule1.yml
   title: Rule One
   id: bbbb0000-0000-0000-0000-000000000001
   logsource: {category: process_creation, product: linux}
   detection: {selection: {Image|endswith: '/a'}, condition: selection}
   level: low
   ```
   ```yaml
   # rules/rule2.yml — same id as rule1.yml, deliberately
   title: Rule Two
   id: bbbb0000-0000-0000-0000-000000000001
   logsource: {category: process_creation, product: linux}
   detection: {selection: {Image|endswith: '/b'}, condition: selection}
   level: low
   ```
3. Write and run a UUID-uniqueness check (verified working — correctly flags the deliberate
   duplicate):
   ```python
   import sys, glob, yaml

   seen_ids = {}
   failures = []
   for path in glob.glob("/tmp/dac-demo2/rules/*.yml"):
       with open(path) as f:
           rule = yaml.safe_load(f)
       rule_id = rule.get("id")
       if rule_id in seen_ids:
           failures.append(f"{path}: duplicate id {rule_id} (also used by {seen_ids[rule_id]})")
       else:
           seen_ids[rule_id] = path

   if failures:
       print("FAILED:")
       for f in failures:
           print(" -", f)
       sys.exit(1)
   print("All rule IDs unique.")
   ```
4. Fix the duplicate (change `rule2.yml`'s `id:` to a different UUID) and re-run to confirm the
   check now passes.
5. Write one sentence on why UUID uniqueness matters operationally (hint: think about what breaks
   if a SOC's alert-triage tooling or a SIEM's rule-management UI keys off `id:` to look up a rule's
   metadata, and two different rules silently share the same key).
6. Clean up:
   ```fish
   rm -rf /tmp/dac-demo2 /tmp/splunk-cicd.html
   ```

