# WireGuard + Python — Learning Plan (Noob → Proficient)

Written for someone proficient in **C/C++**, new to **Python** and to
**WireGuard specifically**. Python explanations throughout the actual
teaching session will anchor to C/C++ mental models — e.g. "a Python
reference is like a pointer you can't do arithmetic on," "no `free()`, a GC
does it," "dataclasses are structs with methods bolted on," "no manual
`malloc`, but you can still leak via lingering references."

**End goal:** proficient enough to (1) explain the WireGuard protocol
unaided, without notes, (2) operate the real `wg`/`wg-quick` CLI surface
confidently, and (3) read and write real Python tooling that generates keys,
parses `wg show` output, and manages a live WireGuard interface.

This is a living document — checkboxes get ticked in place as each milestone
is actually completed in session, not when the concept is merely explained.

---

## Related documents

- **[`wireguard-python-deep-dive-plan.md`](./wireguard-python-deep-dive-plan.md)
  — Plan 2.** A separate, locked-until-Plan-1-is-done document covering the
  underlying math/crypto foundations (modular arithmetic, ECDLP, ARX design,
  MACs, KDF theory, etc.) that this plan treats as black boxes. Starts only
  once every module below is checked off and the Definition of Proficient
  bar is met.
- **[`study-files-log.md`](./study-files-log.md)** — running index of every
  markdown file generated during this study track (diagrams, notes, plans).
  Check this first in any new session before writing new material, to avoid
  regenerating something that already exists.

---

## How the sessions work

- Interactive, in-chat, one piece at a time: I teach a concept, you do a real
  hands-on task with it, we check in before moving to the next piece. Not a
  document dump.
- **A milestone is only checked off once its artifact has actually been
  built and run** — a working tunnel, a script's real output, a file that
  passes validation. Understanding the explanation is necessary but not
  sufficient.
- Modules are sequential (A → E); sub-milestones within a module are mostly
  sequential too, since each builds on the last.
- Grounded in your existing notes — `tool-wg.md` and
  `01-vpn-protocol-development/notes.md`/`exercise.md` in
  `cybersecurity-developer-vpn-tor-siem/` — rather than re-teaching crypto
  basics from scratch. Session time goes to what those docs don't already
  cover: live tunnel setup and the Python tooling layer.

---

## Module A — Protocol Foundations

- [ ] **A1. Noise_IK handshake + primitive suite, explained unaided.**
  Objective: understand the 2-message handshake (initiator → responder →
  data), and the fixed primitive suite (Curve25519 DH, ChaCha20-Poly1305
  AEAD, BLAKE2s hashing, HKDF, SipHash24).
  Artifact: you narrate the handshake back to me from memory, no notes.

  Small coding tasks (each ~15-20 min, basic Python, build up to the
  artifact above):
  - [x] A1.1 Toy Diffie-Hellman exchange (mod-p, two parties, matching
    shared secret) — `wireguard-python-exercises/a1_1_toy_dh.py`,
    explanation in `wireguard-python-exercises/note-a1_1-toy-dh.md`
  - [ ] A1.2 Toy key derivation step (HMAC/HKDF-style, deriving a
    symmetric key from the DH secret)
  - [ ] A1.3 Toy AEAD encrypt/decrypt round-trip (ChaCha20-Poly1305 via
    `cryptography`, tag-verification-fails-on-tamper check)
  - [ ] A1.4 Toy transcript-hash chaining (BLAKE2s, mixing each new
    message into a running hash state)
  - [ ] A1.5 Assemble: two-message toy handshake script (wires A1.1-A1.4
    together, two "parties" in one script, both arrive at the same final
    key)

- [ ] **A2. Cryptokey Routing mental model.**
  Objective: understand `AllowedIPs` as one table doing double duty —
  encryption-peer-selection *and* access control, not just a route.
  Artifact: you correctly predict routing/encryption behavior for 2–3
  `AllowedIPs` scenarios I pose on the spot.

- [ ] **A3. WireGuard vs. IPsec/IKEv2 vs. OpenVPN, cold.**
  Objective: compare crypto design, codebase size, handshake cost, NAT
  roaming, formal verification status.
  Artifact: you fill in a blank comparison table from memory; I cross-check
  it against `01-vpn-protocol-development/notes.md`.

## Module B — Practical WireGuard

- [ ] **B1. Generate a real keypair safely.**
  Objective: use `wg genkey | wg pubkey` correctly (stdin/stdout pipes, never
  a temp file), understand why `umask 077` beats `chmod 600` after the fact.
  Artifact: real key pair generated, permissions verified `600`, stored under
  the existing gitignored `generated-keys/` convention (see Safety Note
  below) — never committed.

- [ ] **B2. Hand-write a valid config from scratch.**
  Objective: write a correct `[Interface]`/`[Peer]` config without copying a
  template.
  Artifact: a `.conf` file that passes `wg-quick` syntax validation.

- [ ] **B3. Bring up a real local tunnel.**
  Objective: two interfaces (e.g. network namespaces) on this machine,
  talking to each other over WireGuard.
  Artifact: `wg show` displays a live handshake; a ping crosses the tunnel
  successfully.

- [ ] **B4. Live-reconfigure without downtime.**
  Objective: use `wg set` to change a peer's `AllowedIPs` or endpoint on a
  running interface, no teardown.
  Artifact: `wg show` output diffed before/after, tunnel never dropped.

## Module C — Python for This Domain

- [ ] **C1. Idioms you'll actually need.**
  Objective: typing, dataclasses, `pathlib`, `subprocess`, context managers —
  each explained against its closest C/C++ equivalent.
  Artifact: a short script that correctly uses all five.

- [ ] **C2. Generate a real X25519 keypair in pure Python.**
  Objective: use the `cryptography` library to reproduce what `wg
  genkey`/`pubkey` does — 32 raw bytes, base64-encoded, 44 chars with one
  `=` pad.
  Artifact: script's output round-trips through `wg pubkey` and matches
  byte-for-byte.

## Module D — Python ⇄ WireGuard Tooling

- [ ] **D1. Parse `wg show <if> dump` into a Python object.**
  Artifact: script prints structured peer data pulled from a real running
  interface.

- [ ] **D2. Generate a valid `.conf` programmatically.**
  Artifact: a Python-generated config file that passes the same validation
  as B2.

- [ ] **D3. Safely wrap `wg`/`wg-quick` via `subprocess`.**
  Objective: no `shell=True`, no secrets passed on argv.
  Artifact: script brings a tunnel up and down end-to-end.

- [ ] **D4. *(Stretch, time-permitting)* Netlink-level control via `pyroute2`.**
  Objective: same as D3, but without shelling out to `wg` at all.
  Artifact: tunnel controlled directly over netlink.

## Module E — Capstone: Peer Manager CLI

- [ ] **E1. A single CLI tool that:**
  generates peer keys, writes/updates configs, adds/removes a peer on a live
  interface, and reports status by parsing real `wg show` output.
  Artifact: the tool itself, run end-to-end on this machine. This is the
  plan's terminal milestone — completing it is the definition of "done" for
  the whole session.

---

## Definition of "proficient" (session-complete bar)

All three must be true, not just the checkboxes ticked:
1. You can explain the WireGuard protocol unaided, without referring back to
   notes.
2. You have a working local tunnel you configured by hand (not copy-pasted).
3. You have a working capstone tool (Module E) that you wrote and ran
   yourself.

---

## Safety note: key handling

Every hands-on step that generates real key material follows the same
convention already established in
`cybersecurity-developer-vpn-tor-siem/00-prerequisite-foundations/key-generation.md`:

- `umask 077` set *before* generation (stronger than `chmod 600` after —
  no exposure window).
- Output goes into
  `cybersecurity-developer-vpn-tor-siem/00-prerequisite-foundations/generated-keys/`,
  which is already listed in `.gitignore` — confirmed untracked.
- Real private key material generated during this session is **never
  committed to git**, regardless of which module produces it (B1, C2, D-series
  scripts).
