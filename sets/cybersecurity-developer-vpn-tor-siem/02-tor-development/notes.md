# 2. Tor Development (relays, onion services, client libraries) — Notes

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 2.

## Tor specifications index

**Claim**: The Tor spec suite is split into focused documents rather than one monolith — verified
locally by listing the actual links on the index page: `tor-spec` covers the core wire protocol
(channels/TLS transport, cell packet format, circuit management, CREATE/CREATED cell handshakes,
relay cells, opening streams, routing relay cells); separate documents cover the directory protocol
(how clients discover relays via directory authorities), path/guard selection, and the rendezvous
protocol for onion services (covered directly in this section's link 3). New features enter through
a **numbered proposal process** before being folded into the formal spec — the index page currently
references proposal 340 ("packed and fragmented relay cells") and proposal 329 ("traffic splitting
via conflux") as still-separate documents, with 329 explicitly noted as already implemented in the
C tor codebase but not yet merged into the main spec text, showing the proposal → implementation →
spec-merge pipeline is asynchronous (code can ship before the spec document catches up).

**Simple explanation**: Rather than one giant RFC, Tor's protocol is documented as a set of linked
specs (like a codebase split into modules) plus a staging area (numbered proposals) for anything not
yet finalized. For a developer, this means: read `tor-spec` for the wire format, `rend-spec` for
onion services, and check the proposals directory for anything recent/experimental that isn't in
the stable spec pages yet.

**Try it**: List the actual linked spec documents rather than trusting a summary (verified working):
```fish
curl -sL https://spec.torproject.org/intro/index.html | grep -oE 'href="[^"]*\.html"' | sort -u
```
```
# bash/sh:
curl -sL https://spec.torproject.org/intro/index.html | grep -oE 'href="[^"]*\.html"' | sort -u
```

## torspec source repository (tor-spec.txt = core protocol spec)

**Claim**: The `torspec` git repo (verified locally via shallow clone) contains ~20 individual spec
text files at its root, not just `tor-spec.txt` — `dir-spec.txt` (directory protocol), `cert-spec.txt`
(certificate formats), `rend-spec-v3.txt` (onion services v3, this section's link 3-4 territory),
`guard-spec.txt`, `path-spec.txt`, `pt-spec.txt` (pluggable transports), `control-spec.txt` (the
ControlPort protocol Stem talks to — this section's links 6-7), plus a `proposals/` subdirectory.
`tor-spec.txt` itself (verified: 2492 lines) is organized as: Section 0 preliminaries (notation,
security parameters, ciphers); Section 1 system overview (keys/names); Section 2 connections (TLS
setup); **Section 3 Cell Packet Format** — the fixed-width "cell" is Tor's fundamental unit, with a
`CircID` + `Command` (1 byte) + `Payload` layout, fixed-length or variable-length depending on link
protocol version, and named commands like `CREATE`/`CREATED`/`RELAY`/`DESTROY`/`CREATE2`/`CREATED2`;
Section 4 connection negotiation (VERSIONS/CERTS/AUTH cells); Section 5 circuit management
(CREATE/CREATED, setting circuit keys, tearing down); Section 6 stream management (RELAY cells,
opening streams); Section 7 flow control.

**Simple explanation**: Everything in Tor's wire protocol is built out of fixed-format "cells" —
think of them as Tor's equivalent of WireGuard's typed packets (link 1 of section 1) or IKEv2's
typed exchanges (section 1 link 7): a small CircID+Command header identifies what kind of cell it
is and which circuit it belongs to, and the command byte (`CREATE`, `RELAY`, `DESTROY`, etc.)
determines how the payload is interpreted. Multi-hop circuits are built by chaining `CREATE`/
`CREATED` cell exchanges hop by hop, then application data flows inside `RELAY` cells layered with
onion encryption.

**Try it**: Shallow-clone the repo (verified: fast, completes in seconds) and inspect the cell
command table directly instead of trusting a paraphrase:
```fish
git clone --depth 1 https://github.com/torproject/torspec /tmp/torspec-src
grep -n -A20 "^3. Cell Packet format" /tmp/torspec-src/tor-spec.txt | head -40
```
```
# bash/sh:
git clone --depth 1 https://github.com/torproject/torspec /tmp/torspec-src
grep -n -A20 "^3. Cell Packet format" /tmp/torspec-src/tor-spec.txt | head -40
```
then clean up (do not leave the clone in the repo):
```fish
rm -rf /tmp/torspec-src
```

## Onion services rendezvous protocol overview

**Claim** (WebFetch could not verify this domain twice in a row — content pulled via `curl` +
HTML-tag-stripping instead, same fallback pattern as this repo's FHS work): the onion-service
connection sequence has five distinct roles/steps. (1) The service picks several relays as
**introduction points**, builds circuits to them, and asks them to forward introduction requests.
(2) The service bundles its introduction-point list into a signed **hidden service descriptor** and
uploads it to a set of **HSDir** nodes (a distributed hash-ring of directory relays, position
determined by a periodically-agreed shared-random value + the HSDir's identity key — explicitly
designed so no single directory is a DoS target for taking a service offline). (3) A client picks a
random relay as its own **rendezvous point** and builds a circuit to it, then fetches the service's
descriptor from an appropriate HSDir if it doesn't have a current one. (4) The client builds an
anonymous circuit to one of the service's introduction points and sends an introduction request
containing the chosen rendezvous point + the first half of a crypto handshake. (5) The service
receives this via its introduction-point circuit, builds its own anonymous circuit to that same
rendezvous point, and completes the handshake; the rendezvous point then just splices the two
circuits together, forwarding `RELAY`/`RELAY_EARLY` cells between them as ordinary `RELAY` cells.
After that, it's ordinary Tor stream traffic (`RELAY_BEGIN`/`RELAY_DATA`) over the joined circuit.
Onion addresses are the Base32 encoding of a full Ed25519 master identity public key + version
byte + checksum (56 chars + `.onion`) — a deliberate move away from the older 80-bit truncated-hash
addressing scheme, so the address itself cryptographically commits to the full key, not just a hash
of it.

**Simple explanation**: Neither side of an onion-service connection ever learns the other's real
network location, because neither one connects directly to the other — the rendezvous point is a
third, mutually-untrusted relay that just relays already-encrypted circuit traffic between two
independently-built anonymous circuits. Introduction points are like a mailbox the service checks
(circuits it already trusts and pre-established); the rendezvous point is a meeting room picked
fresh by the client that neither party's identity is tied to.

**Try it**: Since WebFetch failed against this exact domain, verify the `curl` + strip-HTML fallback
works and locate the "View from 10,000 feet" summary paragraph directly:
```fish
curl -sL https://spec.torproject.org/rend-spec/protocol-overview.html -o (mktemp -t rend-overview.XXXX.html)
```
```
# bash/sh:
curl -sL https://spec.torproject.org/rend-spec/protocol-overview.html -o /tmp/rend-overview.html
```
then strip tags with `sed`/`python3` (verified working: `sed -e 's/<[^>]*>//g'` is a quick
approximation; for cleaner text use a short Python one-liner with `re.sub`), and grep for
"rendezvous point" to confirm the 5-step sequence above matches the source text.

## Onion services developer overview

**Claim** (WebFetch again couldn't verify this `torproject.org` subdomain after two attempts;
`curl` + tag-stripping used instead): this community/developer-facing page states four concrete
benefits of onion services over a regular clearnet service, then narrates the protocol as four
"Acts" that map directly onto the more formal rend-spec overview (link 3) with friendlier framing.
The four benefits: **location hiding** (IP addresses aren't even part of the onion-service
protocol — the overlay network doesn't use them at all, stronger than "the IP is hidden," it's "the
IP is structurally irrelevant"); **end-to-end authentication** (the `.onion` address itself IS the
service's identity public key, so reaching a given onion address cryptographically guarantees
you're talking to the key-holder — no DNS/CA trust chain to attack); **end-to-end encryption**
("SSL/HTTPS for free" — a plain HTTP onion service still gets Tor's circuit encryption; verified
this is *layered on top of*, not a replacement for, application-level TLS one should still use where
available); **NAT punching** (an onion service never needs an open inbound port — it only makes
*outgoing* connections to build its introduction-point circuits, so it works unmodified behind
CGNAT, university/office firewalls, mobile carrier NAT). The page narrates the full connection as
**nine Acts** (verified locally — an earlier partial fetch only surfaced the first four; re-fetched
in full to confirm), which is a friendlier walk-through of the same mechanism as link 3's formal
overview, with two extra concrete details link 3's abstract description didn't spell out: Act 6
has the client hand its rendezvous relay a fresh **one-time secret** as part of establishing the
rendezvous point, and Act 8 has the rendezvous point do a final **secret-matching check** (comparing
the client's original secret against the copy relayed back through the service) before it starts
forwarding traffic — i.e. the rendezvous point isn't just blindly splicing two circuits, it
verifies both sides are talking about the same rendezvous attempt first. Act 9 states the concrete
topology number: a complete onion-service connection is **6 relay hops total** — 3 chosen by the
client (ending in the rendezvous point) and 3 chosen by the service (ending in an introduction
point's circuit) — which is the numeric answer to "how much does an onion-service connection cost
in circuit hops" versus ordinary Tor browsing's 3-hop circuit.

**Simple explanation**: This is the "why would I build this" pitch, complementary to link 3's "how
does it actually work" spec. The NAT-punching property is probably the most underrated one for a
*builder* audience specifically: it means an onion service can be self-hosted from literally any
network with outbound internet — no port forwarding, no static IP, no dealing with a hosting
provider's firewall — which is why projects like SecureDrop (the page's own example: anonymous tip
submission for journalists) use onion services rather than a conventional hosted web server.

**Try it**: Fetch and de-tag this page (same fallback as link 3) and locate all "Act N" section
headers — read the whole page rather than stopping at a partial fetch, since only reading the first
few thousand characters here would misleadingly suggest there are just 4 Acts when there are 9:
```fish
curl -sL https://community.torproject.org/onion-services/overview/ -o (mktemp -t onion-overview.XXXX.html)
```
```
# bash/sh:
curl -sL https://community.torproject.org/onion-services/overview/ -o /tmp/onion-overview.html
```
then de-tag and `grep -E -n "^ Act [0-9]"` to confirm all 9 headings, matching the corrected count
above.

## Setting up/automating onion services

**Claim**: The actual config surface for a basic onion service is two `torrc` directives:
`HiddenServiceDir <path>` (where Tor stores the service's keys + descriptor state) and
`HiddenServicePort <virtual-port> <target-host>:<target-port>` (or `unix:<path>` for a Unix socket,
recommended specifically to avoid accidentally exposing the backend on the local network's TCP
stack). Verified locally: Tor enforces strict permissions on `HiddenServiceDir` — a world/group
-readable directory is rejected at config-validation time (`tor --verify-config` fails with
"Permissions on directory ... are too permissive" until it's `chmod 700`). Multiple virtual ports
for one service just add more `HiddenServicePort` lines under the same `HiddenServiceDir`; multiple
independent services on one Tor client just add another `HiddenServiceDir` block. After a restart,
the onion address (v3, the 56-char format from link 3's notes) appears in a `hostname` file inside
`HiddenServiceDir`, alongside the service's private keys — the page explicitly warns these key
files must stay private, since leaking them lets someone else impersonate the service. By default
an onion service configured this way is reachable by anyone who knows/discovers the address;
restricting access to specific clients requires separate "client authorization" configuration
(covered as restricted-discovery mode in link 3's access-control notes).

**Simple explanation**: Setting up a basic onion service is genuinely just "point Tor at your
already-running local web server" — two lines of config, no port-forwarding, no firewall changes
(ties directly back to the NAT-punching property from link 4), no certificate to obtain, because
the onion address itself acts as the identity/cert. The permission enforcement on
`HiddenServiceDir` is Tor defending against a real local-privilege-escalation-adjacent mistake: if
other local users could read the service's private key, they could clone the service's identity.

**Try it**: Validate a real `torrc` fragment locally using `tor --verify-config` — this parses and
checks the configuration but does *not* start the daemon or touch the live Tor network, so it's
safe, offline, no-root, and non-network-touching (verified working on this machine, Tor 0.4.9.11
installed):
```fish
set hsdir (mktemp -d -t tor-hs-test.XXXX)
set torrc (mktemp -t torrc.XXXX)
printf "DataDirectory %s/data\nHiddenServiceDir %s\nHiddenServicePort 80 127.0.0.1:8080\n" $hsdir $hsdir > $torrc
tor --verify-config -f $torrc
```
```
# bash/sh:
hsdir=$(mktemp -d -t tor-hs-test.XXXX)
torrc=$(mktemp -t torrc.XXXX)
printf "DataDirectory %s/data\nHiddenServiceDir %s\nHiddenServicePort 80 127.0.0.1:8080\n" "$hsdir" "$hsdir" > "$torrc"
tor --verify-config -f "$torrc"
```
On this machine `mktemp -d` already creates the directory `0700`, so the run above should print
`Configuration was valid` immediately. To actually see Tor's permission enforcement fire (verified),
loosen the permissions and re-check, then restore them:
```fish
chmod 755 $hsdir; tor --verify-config -f $torrc   # expect: [warn] ... too permissive / [err] Reading config failed
chmod 700 $hsdir; tor --verify-config -f $torrc   # expect: Configuration was valid
```
```
# bash/sh:
chmod 755 "$hsdir"; tor --verify-config -f "$torrc"
chmod 700 "$hsdir"; tor --verify-config -f "$torrc"
```
Clean up afterward:
```fish
rm -rf $hsdir $torrc
```
```
# bash/sh:
rm -rf "$hsdir" "$torrc"
```

## Stem — Python controller library for Tor (docs)

**Claim** (WebFetch again failed against this `torproject.org` subdomain; `curl` fallback used):
Stem is a Python library for scripting against a running Tor process over Tor's **control
protocol** — used to build tools like Nyx (a `top`-style Tor process monitor). Verified locally,
important and easy-to-miss caveat straight from the project's own docs: **Stem is "mostly
unmaintained"** as of its last release (1.8.1, September 2022) — the maintainers explicitly say
they'll accept issues/PRs but aren't doing active development, which matters for a builder deciding
whether to depend on it for new production tooling versus e.g. talking to the control protocol
directly. Functionally, Stem wraps: connecting to Tor's control port/socket and authenticating,
issuing control-protocol commands (matches `control-spec.txt` from link 2's torspec clone),
listening for async events, reading/parsing relay descriptors, and building/inspecting circuits.

**Simple explanation**: Stem is to Tor's control protocol what a typed SDK is to a raw REST API —
instead of hand-rolling the text-based control-protocol commands from `control-spec.txt`, Stem
gives Python objects (`Controller`, `Circuit`, descriptor classes) that wrap them. The "mostly
unmaintained" flag is worth treating like any other supply-chain signal: it still works and is
usable for scripting/analysis today, but a builder should check for that status before basing new
production infrastructure on it, and diff its behavior against the current `control-spec.txt` if
something seems off, since the library predates recent protocol changes.

**Try it**: Install Stem into an isolated venv and syntax-check a minimal controller snippet rather
than trusting a memorized/paraphrased example — verified working (compiles cleanly, `Controller.
from_port` signature confirmed as `(address='127.0.0.1', port='default')` via `inspect.signature`):
```fish
set venv (mktemp -d -t stem-venv.XXXX)
python3 -m venv $venv
$venv/bin/pip install stem
```
```
# bash/sh:
venv=$(mktemp -d -t stem-venv.XXXX)
python3 -m venv "$venv"
"$venv/bin/pip" install stem
```
then write and syntax-check a minimal controller snippet (does not connect anywhere — no live Tor
control port needed for this check):
```python
import stem.connection
from stem.control import Controller

with Controller.from_port(port=9051) as controller:
    controller.authenticate()  # or authenticate(password="...") if a control password is set
    print("Tor version:", controller.get_version())
    for circ in controller.get_circuits():
        print(circ.id, circ.status, [hop[0] for hop in circ.path])
```
```fish
$venv/bin/python3 -m py_compile controller_snippet.py
rm -rf $venv
```
```
# bash/sh:
"$venv/bin/python3" -m py_compile controller_snippet.py
rm -rf "$venv"
```

## Stem Controller API reference

**Claim** (curl fallback again, same domain issue as link 6): the `stem.control` module reference
page is mostly a catalogue of **enums and exceptions** the `Controller` class's methods return or
raise, not the method list itself — and several of these enums are a direct, concrete payoff from
this section's earlier reading. `CircPurpose` (verified locally) has exactly the four onion-service
circuit roles predicted by the rendezvous protocol overview (link 3) and developer overview (link
4): `HS_CLIENT_INTRO` (client's circuit to an introduction point), `HS_CLIENT_REND` (client's
circuit to its rendezvous point), `HS_SERVICE_INTRO` (service's circuit to an introduction point),
`HS_SERVICE_REND` (service's circuit to the rendezvous point) — i.e. Stem's own type system encodes
the same 4-role split already reconstructed by hand in link 3's exercise. `CircStatus` (`LAUNCHED`
→ `BUILT`/`GUARD_WAIT` → `EXTENDED` → `FAILED`/`CLOSED`) gives the circuit lifecycle state machine a
controller script would poll or listen for. `Signal.NEWNYM` is the exact control-protocol signal
behind Tor Browser's "New Identity" button — verified: its description is literally "switch to new
circuits, so new application requests don't share any circuits with old ones (this also clears our
DNS cache)". `CircBuildFlag` (`ONEHOP_TUNNEL`, `IS_INTERNAL`, `NEED_CAPACITY`, `NEED_UPTIME`) and
`Flag` (relay flags like `GUARD`, `EXIT`, `HSDIR`, `STABLE`, `FAST`) round out the vocabulary needed
to actually filter/select relays or interpret circuit-building behavior from code.

**Simple explanation**: Where link 6's Stem docs entry covered "how do I connect and issue
commands," this page is "what do the responses actually mean" — the enums are the typed vocabulary
a controller script needs to interpret events and circuit states without guessing at Tor's raw
text-protocol strings. The `CircPurpose` enum in particular is a nice sanity-check: if the rendezvous
protocol notes from links 3-4 were understood correctly, this enum should have no surprises in it.

**Try it**: Fetch and de-tag the page (same fallback as link 6) and confirm the `CircPurpose` enum
independently matches the 4-role breakdown already written down for links 3-4, rather than assuming
it does:
```fish
curl -sL https://stem.torproject.org/api/control.html -o (mktemp -t stem-control.XXXX.html)
```
```
# bash/sh:
curl -sL https://stem.torproject.org/api/control.html -o /tmp/stem-control.html
```
then de-tag with the same Python one-liner as link 4 and grep:
```fish
grep -E -A10 "CircPurpose \( enum \)" /tmp/stem-control.txt
```

## Tor Project GitLab (contribute to core code)

**Claim**: `gitlab.torproject.org` is Tor's actual development hub — verified locally via `curl`:
the org landing page (`tpo` organization, created July 2020) is a wiki-style index pointing to
Official Resources (main site, Support/Community Portals, Tor News), **Contributions** (the
official bug tracker is this GitLab instance itself — "GitLab Ultimate," with a curated
first-contributor issue list), Documentation (Tor Relay Guide, Tor Browser User Manual, a Tor User
Documentation Style Guide), Services (package archive, media archive, the `Check` service that
tells a browser whether it's using Tor, a public Metrics site, a Status page), and per-team process
pages (Anti-censorship, Applications, Network Health, Network, Tails teams each have their own
processes/policies documented). The core C `tor` implementation itself lives at
`gitlab.torproject.org/tpo/core/tor` (the canonical repo path referenced across Tor's own docs and
this file's earlier links) — re-verified directly: `curl -sIL` against that path returns `HTTP/2
200`, confirming the repo path is live (an earlier attempt to fetch its full page body during this
session returned an empty/truncated result, which is why this was double-checked with a plain HEAD
request before writing this claim down).

**Simple explanation**: This is "where do I actually go to file a bug or submit a patch against
Tor" — GitLab, not GitHub, is Tor's primary forge (torproject/torspec on GitHub, seen in link 2, is
a mirror/companion repo for the spec text specifically). For a developer wanting to contribute
code rather than just read specs, GitLab's first-contributor issue list is the concrete on-ramp.

**Try it**: Confirm the org wiki content directly and locate the first-contributor issue list
pointer (verified working):
```fish
curl -sL https://gitlab.torproject.org/ -o (mktemp -t tor-gitlab.XXXX.html)
```
```
# bash/sh:
curl -sL https://gitlab.torproject.org/ -o /tmp/tor-gitlab.html
```
then confirm the core `tor` repo path resolves (verified: `HTTP/2 200`):
```fish
curl -sIL https://gitlab.torproject.org/tpo/core/tor
```
```
# bash/sh:
curl -sIL https://gitlab.torproject.org/tpo/core/tor
```
Standing up a live onion service (actually running the daemon, publishing a descriptor to the real
Tor network) is out of scope here — same restraint as section 1's WireGuard exercises; this repo's
convention is coding/analysis, not operating live network-facing infrastructure.
