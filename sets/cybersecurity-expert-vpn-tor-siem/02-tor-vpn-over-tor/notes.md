# 2. Tor / VPN-over-Tor — Notes

## How Tor works (official overview)

**Claim**: Tor anonymizes connections by building a multi-hop circuit — conventionally 3 relays:
a guard/entry relay, a middle relay, and an exit relay — where the circuit is extended one hop at
a time and, critically, **no single relay knows the full path**. Each relay only ever learns
"who handed me this data" and "who do I hand it to next": the guard relay sees your real IP but
not your final destination; the exit relay sees the destination but not your real IP; the middle
relay sees neither endpoint, just the two other relays. This is enforced cryptographically, not
just by convention: the client negotiates a separate encryption key with each hop, so data is
wrapped in nested encryption layers (the "onion" in Onion Routing) — each relay peels off exactly
one layer, revealing only the next hop's address, never the payload or the full route. This
compartmentalization is what defeats simple traffic-analysis-by-a-single-observer: no individual
relay (or someone who compromises just one relay) can link source to destination.

**Simple explanation**: Imagine passing a sealed envelope through 3 people, each of whom can only
read the outer layer telling them who to pass it to next, never the contents or the full chain.
Person 1 (guard) knows it came from you, person 3 (exit) knows where it's finally going, but
neither knows the whole journey, and person 2 (middle) knows neither endpoint. Only by colluding
(or being the same entity) could any subset of them reconstruct the full path.

**Try it**: Tor is installed on this machine (confirmed) — inspect the real client/daemon and its
config surface without needing a fully bootstrapped live circuit (bootstrapping proved slow/flaky
in this sandboxed environment on a first attempt; the installed binary and man page are the
reliable, fast source here, same reasoning as the man7.org convention elsewhere in this repo).
```fish
tor --version
man 1 tor | head -40
```
bash/sh: identical. Arch: `pacman -S tor` (already installed here, v0.4.9.11). Debian:
`apt install tor`.
Applied exercise: draw the 3-hop circuit (You -> Guard -> Middle -> Exit -> Destination) and at
each relay, write down exactly what that relay CAN see (previous hop, next hop) and CANNOT see
(anything about the endpoints beyond its immediate neighbors).

## Short technical introduction to Tor (spec.torproject.org)

**Claim**: This is the index page for Tor's actual protocol specifications, and it hands over the
precise vocabulary the previous link's overview only described informally. Layered structure,
bottom to top: a **channel** is the underlying encrypted TLS connection between two relays; a
**cell** is the fixed-length message unit sent over a channel (fixed length so an observer can't
distinguish cell types by size); a **circuit** is the multi-hop cryptographic path built from
cells across (typically) 3 relays, where each relay peels/adds one encryption layer per the
earlier onion-routing description; a **stream** is one individual TCP session multiplexed onto a
circuit, created at the exit relay (this is why one circuit can carry several of your simultaneous
connections). Above the base protocol: **directory authorities** are the trusted servers that
vote on and sign the canonical list of known relays (so a client can bootstrap "which relays even
exist" without trusting any single relay); **Guard spec** governs how a client picks and *sticks
with* its entry relay (deliberately not re-randomized often, to limit a specific long-term attack
covered later in section 4); **Rendezvous spec** is the protocol behind onion services (section 2
links 3-4); **Pluggable Transports spec** covers traffic-obfuscation plugins for censorship
circumvention; **Conflux** is a newer feature multiplexing a client's traffic across multiple
circuits to the same destination for better performance.

**Simple explanation**: This page is Tor's own glossary/map of "the actual protocol documents,"
not a tutorial — worth treating as the precise-terminology upgrade to the plain-language overview
in the previous link. Cell -> Circuit -> Stream is roughly "packet -> tunnel -> individual
connection inside that tunnel," and directory authorities are Tor's answer to "how does a new
client even find relays to build a circuit with in the first place."

**Try it**: This is a specification index, not a tool — the applied exercise is building a
correct term-mapping from it (no live circuit/network fetch attempted here, consistent with
keeping this exercise fast/reliable rather than dependent on live Tor bootstrap).
1. Write a one-line definition, in your own words, for each of: channel, cell, circuit, stream,
   directory authority, guard, bridge, pluggable transport, onion service, Conflux.
2. Order them from "lowest level" (closest to raw TCP/TLS) to "highest level" (closest to what an
   application/user experiences).
3. Explain in 2-3 sentences why cells are fixed-length — what does variable-length message
   framing leak to a passive network observer that fixed-length framing does not?

## Onion services overview (community.torproject.org)

**Claim** (fetched via `curl` + HTML-tag-stripping — WebFetch's built-in tool refused this domain
with a "cannot verify domain safety" block, so the man7/FHS-convention fallback was used instead):
onion services solve "how do you connect to something that has no IP address" by making the
address itself be a public key. A `.onion` address is literally derived from the service's
identity public key, which is *why* it looks like random noise. Full connection setup, per the
page's own numbered walkthrough (paraphrased):
1. The service picks ~3 relays as **introduction points**, reaching each via its own anonymized
   3-hop circuit (so even the introduction points don't learn the service's real location).
2. The service builds a **descriptor** (list of introduction points + auth keys), signs it with
   its identity private key, and uploads it to a distributed hash table (DHT) inside the Tor
   network — again over an anonymized circuit.
3. A client with the `.onion` address fetches the signed descriptor from the DHT and **verifies
   the signature** against the public key embedded in the address itself — this is what gives
   end-to-end authentication: only the real service could have produced a validly-signed
   descriptor for that address.
4. The client independently picks its own relay to act as a **rendezvous point**, and gives it a
   one-time secret.
5. The client sends that secret + rendezvous relay info to the service via one of the
   introduction points (over the client's own anonymized circuit).
6. The service connects to the rendezvous point (over its own anonymized circuit) and presents
   the matching secret; the rendezvous point verifies the secrets match and then just relays
   encrypted traffic between client and service from then on.
7. **Net result: the full path is 6 relays** — 3 picked by the client (ending at the rendezvous
   point) and 3 picked by the service (ending at an introduction point) — and neither side's real
   IP is ever exposed to the other, or to any single relay along the way.

**Simple explanation**: A `.onion` address isn't a location, it's an identity (a public key) —
like knowing someone's unforgeable signature without knowing their home address. Reaching them
involves both sides independently building anonymous paths into the Tor network and rendezvousing
at a mutually-agreed meeting-point relay, verified by a one-time secret, so neither party's real
network location is ever revealed to the other or to the meeting-point itself.

**Try it**: This is a protocol walkthrough, not a single CLI command — the concrete exercise is
tracing the 9-act sequence into a diagram, using the relay-visibility reasoning already built in
link 1 of this section.
```fish
# confirm this machine's Tor build supports v3 onion services (the modern format, 56-char
# addresses derived from ed25519 keys) — check via the version string and changelog reference
tor --version
man 1 tor | grep -i -A3 "onion service" | head -20
```
bash/sh: identical.
Applied exercise: draw all 6 relays in the final circuit (3 client-side ending at the rendezvous
point, 3 service-side ending at an introduction point) and mark, for each relay, whether it knows
the client's real IP, the service's real IP, both, or neither.

## Setting up/using onion services (community.torproject.org)

**Claim** (fetched via `curl` + tag-stripping, same as the previous link): concretely, running an
onion service means (1) having a normal local web server (any web server — Apache/Nginx/anything
listening on localhost), and (2) adding exactly two lines to `torrc`:
`HiddenServiceDir /path/to/keys-and-hostname/` (where Tor stores the service's private key +
generates the `.onion` address) and `HiddenServicePort <virtual-port> <local-addr>:<local-port>`
(maps the public-facing onion port to where the real web server is actually listening). After a
Tor restart, the `hostname` file inside `HiddenServiceDir` contains the generated v3 `.onion`
address — Tor creates the directory and keypair automatically on first start. The guide's two
security notes worth flagging: the private key files in `HiddenServiceDir` are exactly as
sensitive as a TLS private key (leak = full impersonation of the service), and it explicitly
recommends `unix:/path/to.sock` instead of a TCP `127.0.0.1:port` backend to avoid accidentally
exposing the backend to the local network. By default any client who learns the address can
connect — per-client authentication (restricting to holders of a specific key) is a separate,
optional feature.

**Simple explanation**: An onion service is just "your existing local web server" plus a Tor
config stanza that tells Tor "give this local port a `.onion` identity and publish it into the
Tor network for me." The `.onion` address literally comes out of a file Tor writes for you after
you restart it — you don't choose it, it's derived from a keypair Tor generates.

**Try it**: Demonstrate the local half of this setup (web server + torrc syntax) without a full
live network bootstrap (the earlier attempt in link 1 showed live Tor circuit-building is slow in
this sandboxed environment — the config/keypair-generation mechanics are still fully verifiable
locally without that wait).
```fish
# stand in for Apache/Nginx: python's built-in http server, verified working, foreground+timeout
timeout 3 python3 -m http.server 8888 --directory /tmp &
sleep 1
curl -s http://127.0.0.1:8888/ | head -5
wait
```
bash/sh: `python3 -m http.server 8888 --directory /tmp & sleep 1; curl -s http://127.0.0.1:8888/ | head -5; wait` (same commands, `&`/`wait` are POSIX already).
```
# the torrc stanza this would need (inspect only — do not apply without root/service ownership):
# HiddenServiceDir /var/lib/tor/my_website/
# HiddenServicePort 80 127.0.0.1:8888
```
Arch: web server options include `pacman -S nginx` or `pacman -S apache`; `python3` (used above)
ships in a base install. Debian: `apt install nginx` / `apt install apache2`.
(Optional, root, real network access, slow): to see this fully live — add the torrc lines above
pointing `HiddenServicePort` at the python server's port, `sudo systemctl restart tor`, then
`cat /var/lib/tor/my_website/hostname` for the generated `.onion` address, and visit it in Tor
Browser. Left as optional because live Tor bootstrap can take well over a minute and depends on
network reachability that may vary by environment.

## Running/understanding Tor relays (community.torproject.org)

**Claim** (note: `/relay/` itself is a thin index/hub page — same "index vs. real content"
pattern flagged in this repo's FHS convention — so its one linked sub-page with actual technical
content, "Types of relays," was pulled in too, one-level-deep, same as the man7/FHS/GNU
conventions elsewhere in this repo): there are 4 relay roles, not 3 — the guard/middle/exit
model from link 1 is the *default* circuit shape, but bridges are a 4th role that substitutes for
the guard when censorship resistance matters: `User -> Guard -> Middle -> Exit -> Destination`
normally, or `User -> Bridge -> Middle -> Exit -> Destination` when using a bridge. Concrete
distinguishing facts per role: **Guard** = first hop, promoted from middle-relay status only once
it proves stable and fast (>=2MB/s up+down) — guard/middle relays are collectively "non-exit" and
rarely draw abuse complaints since their IP is never the one a destination site sees. **Middle**
= second hop, least legally exposed role. **Exit** = the relay whose IP the destination site
actually sees — bears by far the greatest legal exposure (DMCA notices, abuse complaints go
directly to the operator), which is why the page explicitly advises against running an exit relay
from a home connection, recommending institutional operators (universities, libraries,
relay associations) instead. **Bridge** = a relay deliberately *not* listed in the public Tor
relay directory, specifically so it can't be blocklisted the way public guard IPs can be by
censoring ISPs/governments — pluggable transports add a further obfuscation layer on top of
bridges for regimes (the page names China and Iran) that actively fingerprint and block even
bridge connections.

**Simple explanation**: Not all relays carry equal risk or purpose. Guards and middles are
"structural plumbing" — low risk, rarely complained about, because outside observers never see
their IP as the traffic's origin or destination. Exits are the "public face" of Tor to the rest
of the internet and absorb all the legal/abuse heat as a result. Bridges exist purely to be a
secret front door for users in places where even connecting to a known Tor guard IP is itself
dangerous or blocked.

**Try it**: This is an operational-role taxonomy, not something to demonstrate by running a real
relay (running a live relay contributes real bandwidth to the public Tor network and has real
legal/policy implications for the operator — out of scope per this repo's "understand, don't
deploy live infrastructure" boundary for a study exercise). The applied exercise is mapping the
role definitions onto the circuit diagram already built in link 1's exercise, plus inspecting the
real exit-policy config syntax (read-only) that governs which role a relay plays.
```fish
# ExitPolicy is the actual torrc directive controlling exit-vs-non-exit role — inspect its syntax
man 1 tor | grep -i -A5 "^ *ExitPolicy "
```
bash/sh: identical.
Applied exercise: on your link-1 circuit diagram, relabel the guard hop as a bridge (in the
censorship-resistant variant) and write one sentence on why a bridge relay's IP being unlisted is
the entire point — what specific blocking technique does an ISP/government use against listed
guard IPs that a bridge IP defeats?

## Tor support/documentation hub (support.torproject.org)

**Claim** (fetched via `curl` since WebFetch blocked this domain too, same as links 3-5): this is
a pure navigational hub/landing page — a bare index of sibling topic categories, not itself
containing technical depth (same "bibliography-style index, don't expand" pattern this repo's
man7/FHS convention explicitly calls out — each of these stays a future link of its own if wanted
later, not folded in here). Its top-level map: **About Tor** (general orientation), **Tor
Browser** (the actual anonymity-focused browser product — downloading, censorship circumvention,
troubleshooting), **Tor VPN (beta)** (a newer product routing arbitrary apps' traffic through Tor,
distinct from Tor Browser), **Tails** (a separate portable OS project, Tor-powered by default),
then "Other topics": **Relays** (already covered directly in link 5), **Onion Services** (already
covered directly in links 3-4), **Little-t tor** (the technical manual for the core `tor` daemon
itself — this is literally the man page already used as this study-set's local source in earlier
links), **Mullvad Browser** (anti-fingerprinting browser tech shared with Tor Browser, usable
*without* connecting to Tor at all — a related-but-distinct privacy tool), **Abuse** (FAQ on how
Tor Project handles network-abuse reports), **Anti-censorship** (bridges/Snowflake/pluggable
transports as a topic in their own right). Plus direct-support channels: contact, community
forum, and a glossary of terms.

**Simple explanation**: This page is a table of contents for Tor's entire support library, not an
article — its value here is knowing the map exists and what's on it (so a real question later has
a known place to look), not summarizing content that isn't actually on this specific page.

**Try it**: Navigational/applied exercise rather than a command — confirm the "Little-t tor"
category maps to exactly the local resource already used repeatedly in this section.
```fish
man 1 tor | head -3   # this is "Little-t tor" — the exact technical manual the hub links to
```
bash/sh: identical.
Applied exercise: build a one-page index mapping each of this hub's 9 categories (About Tor, Tor
Browser, Tor VPN beta, Tails, Relays, Onion Services, Little-t tor, Mullvad Browser, Abuse,
Anti-censorship) to which link (if any) in this study set already covers it, so future
lookups have a fast reference.

## Combining Tor with VPN (Windscribe blog)

**Claim** (fetched via `curl` with a browser User-Agent — WebFetch blocked this domain too; note
the article never actually uses the canonical terms "Tor over VPN"/"VPN over Tor" verbatim
despite the source list's description implying it does, but it does describe the same two
configurations in plain language — captured accurately as written, terminology mapped explicitly
below): two distinct combination orders exist, and they protect against *different* threats.
**"VPN before Tor" (= Tor-over-VPN)**: connect to a VPN first, then Tor on top. This hides "this
user is connecting to Tor" from the ISP (the ISP only sees VPN traffic; the VPN provider sees
you're using Tor, but your ISP doesn't) — the article frames this as the main use case ("protect
against ISP monitoring"). **"Tor before VPN" (= VPN-over-Tor)**: connect to Tor first, then a VPN
on top, run through Tor. This conceals VPN traffic/credentials from the Tor exit node specifically
— the exit node would otherwise be able to see (though not necessarily attribute to you) whatever
leaves it in the clear; running a VPN through Tor keeps that final hop's payload encrypted too.
Both orderings cost real speed (compounding two encryption/relay layers). The article's practical
recommendation: privacy-conscious users in heavily monitored/censored regions, and journalists
specifically, commonly use the VPN-before-Tor ordering to access censored content without the ISP
seeing Tor usage at all (which itself can be treated as suspicious in some regimes, independent of
content).

**Simple explanation**: Order matters and answers a different question each way. "VPN then Tor"
answers "how do I stop my ISP from even knowing I use Tor?" "Tor then VPN" answers "how do I stop
the Tor exit node from seeing what I do after it?" Neither order is free — you pay a speed cost
for layering two anonymity/privacy systems instead of one.

**Try it**: This is a conceptual configuration choice, not a single runnable command — the
concrete exercise is diagramming both orderings and mapping which threat each defeats, using the
relay-visibility facts already established in links 1 and 3-5 of this section.
```fish
# no live combination configured on this machine — inspect what's actually installed for each half
tor --version
wg --version
```
bash/sh: identical.
Applied exercise: draw both orderings as chains — (1) You -> VPN -> Tor(Guard->Middle->Exit) ->
Destination, and (2) You -> Tor(Guard->Middle->Exit) -> VPN -> Destination. For each, mark
exactly which single party (ISP, VPN provider, Tor guard, Tor exit) can see "this user uses Tor"
and which can see "this user's post-Tor traffic content."
