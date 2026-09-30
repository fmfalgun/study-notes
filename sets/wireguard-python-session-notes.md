# WireGuard + Python Study Track — Session Notes

Quick-context snapshot for this track, so a new session can get oriented
fast. The plan files themselves are the source of truth for progress —
this file is a pointer/summary, not a duplicate.

## Documents

- [`wireguard-python-learning-plan.md`](./wireguard-python-learning-plan.md)
  — **Plan 1**, main operational roadmap (Modules A–E), living checklist.
- [`wireguard-python-deep-dive-plan.md`](./wireguard-python-deep-dive-plan.md)
  — **Plan 2**, math/crypto foundations. Locked until Plan 1 is complete.
- [`study-files-log.md`](./study-files-log.md) — index of every markdown
  file generated during this track.
- Diagram/reference files in
  `cybersecurity-developer-vpn-tor-siem/01-vpn-protocol-development/`:
  `diagram-x25519-diffie-hellman.md`, `diagram-chacha20-poly1305.md`,
  `diagram-hkdf.md`, `diagram-wireguard-full-handshake.md`,
  `note-flow-diagram-types.md` — each has a layman version and a precise
  math/crypto version.
- [`wireguard-python-exercises/`](./wireguard-python-exercises/) — small
  (~15-20 min) coding-task scripts for each module's sub-milestones
  (A1.1-A1.5, etc.), one `.py` file per task.

## Collaboration context

See `../meta/collaboration-notes.md` (explanation style, verification
style) and `../meta/user-background.md` (C/C++ background) — both apply
to this track specifically as well as the rest of the repo.

## Status (as of 2026-08-21)

Module A1 (Noise_IK handshake) in progress. A1 was broken into 5 small
coding sub-tasks (A1.1–A1.5: toy DH exchange, toy KDF step, toy AEAD
round-trip, toy hash chaining, assembled toy handshake script) added
directly into Plan 1. None of the A1 sub-tasks completed yet.

**Next step when resuming:** start A1.1 — a toy Diffie-Hellman exchange
in Python (small integers, `pow(base, exp, mod)`, two parties arriving at
the same shared secret). Save it as
`wireguard-python-exercises/a1_1_toy_dh.py`.
