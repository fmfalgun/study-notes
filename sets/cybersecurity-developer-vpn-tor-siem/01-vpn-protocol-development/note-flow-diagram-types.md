# Flow-Diagram Types Used in Cryptographic-Function Explanations

Reference list of diagram types commonly used when explaining crypto
protocols/primitives, and what each is best suited for.

- **Sequence diagrams** (message sequence charts / ladder diagrams) —
  show *who sends what to whom, in what order*. Best for protocol
  handshakes (e.g. Noise_IK). Used for `diagram-x25519-diffie-hellman.md`,
  `diagram-chacha20-poly1305.md`, `diagram-hkdf.md`.

- **Data-flow diagrams (DFDs)** — show how data transforms as it moves
  through a system, independent of timing/ordering. Useful for tracing a
  value (e.g. a key) through multiple derivation stages.

- **Key schedule / key derivation trees** — show how one root secret
  branches into multiple derived keys. Useful for HKDF chains that
  produce several outputs (chaining key + one or more session keys).

- **State machine diagrams (state transition diagrams)** — show the
  discrete states a protocol session can be in and what triggers a
  transition. Useful for connection lifecycle (e.g. handshake-pending →
  established → rekeying → expired).

- **Data/control flow graphs (block diagrams)** — show functional blocks
  and the data paths between them, without strict message-passing
  semantics. Useful for depicting a cipher's internal pipeline (e.g.
  keystream generation feeding into an XOR block).

- **Circuit diagrams** — show a primitive's actual internal wiring at the
  bit/round level. Best for block ciphers and permutation-based
  primitives (e.g. AES round structure, a Feistel network, ChaCha20's
  quarter-round ARX wiring).

- **Merkle / hash trees** — show hierarchical hashing where leaves
  combine pairwise up to a single root. Relevant to integrity structures
  (e.g. certificate transparency logs, some KDF trees), not directly to
  WireGuard's handshake.

- **Swimlane diagrams** — a sequence diagram variant with explicit
  parallel "lanes" per actor, useful when actors do significant internal
  work between messages (e.g. showing an actor's local computation steps
  alongside the messages it sends).

- **UML activity diagrams** — show algorithmic control flow (branches,
  loops, parallel forks) inside a single actor's process, rather than
  cross-actor communication. Useful for describing a single primitive's
  internal decision logic (e.g. AEAD's verify-then-decrypt branch).
