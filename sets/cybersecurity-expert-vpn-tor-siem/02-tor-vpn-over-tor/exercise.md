# 2. Tor / VPN-over-Tor — Exercises

## 1. How Tor works (official overview)

1. Confirm Tor is installed and check its version:
   ```fish
   tor --version
   man 1 tor | head -40
   ```
   bash/sh: identical.
2. Draw the 3-hop circuit: You -> Guard relay -> Middle relay -> Exit relay -> Destination
   server. Label each of the 4 links with whether it's encrypted (all 3 relay-to-relay hops are;
   the exit-to-destination hop is only encrypted if the destination itself uses TLS/HTTPS).
3. For each of the 3 relays, write one line: "This relay can see: ___. This relay cannot see: ___."
4. Explain in 2-3 sentences why compromising (or operating) just the guard relay alone doesn't
   deanonymize a user, and why compromising just the exit relay alone doesn't either — what would
   an attacker need to control to link source and destination? (This sets up section 4's
   traffic-correlation attack links.)
5. Explain in 1-2 sentences the literal meaning of "onion routing" — connect it to the layered
   encryption removed one hop at a time.

## 2. Short technical introduction to Tor (spec.torproject.org)

1. Write one-line definitions (your own words, no copy-paste) for: channel, cell, circuit,
   stream, directory authority, guard, bridge, pluggable transport, onion service, Conflux.
2. Arrange those 10 terms into a layering diagram from lowest-level (TLS/network) to
   highest-level (user-facing feature).
3. Explain in 2-3 sentences why Tor cells are fixed-length, and what a passive network observer
   could infer from variable-length cells that they cannot from fixed-length ones.
4. Explain in 2-3 sentences why a client deliberately keeps the *same* guard relay for an extended
   period (per the Guard spec) rather than picking a fresh random guard for every new circuit —
   what attack does guard "stickiness" defend against, and what new risk does it introduce if that
   one guard is malicious? (Revisit this answer after section 4's Tor de-anonymization links.)
5. Explain in 1-2 sentences the practical difference between a "relay" (publicly listed) and a
   "bridge" (deliberately unlisted) — what problem does a bridge solve that a normal relay can't?

## 3. Onion services overview

1. Check this machine's Tor version and confirm v3 onion-service support in its error-code table:
   ```fish
   tor --version
   man 1 tor | grep -i -A3 "onion service" | head -20
   ```
   bash/sh: identical. Verified: this build's man page lists v3-specific onion-service error
   codes (descriptor not found, descriptor invalid, introduction failed), confirming v3 support.
2. Draw the full 9-act sequence as a numbered diagram: service picks introduction points ->
   service publishes signed descriptor to DHT -> client fetches descriptor -> client verifies
   signature -> client picks rendezvous point -> client sends secret via introduction point ->
   service connects to rendezvous point -> rendezvous point matches secrets -> traffic relayed.
3. In your diagram, draw all 6 relays in the final data path (3 client-side, 3 service-side) and
   mark for each one: does it know the client's real IP? The service's real IP? Neither?
4. Explain in 2-3 sentences how the descriptor signature check (Act 5 in the source page) gives
   "end-to-end authentication" — what specifically would fail if an attacker tried to serve a fake
   descriptor for someone else's `.onion` address?
5. Explain in 2 sentences why onion services don't need any inbound firewall ports open (the
   "NAT punching" property named on the page) — which direction do all the connections the service
   itself initiates go?

## 4. Setting up/using onion services

1. Stand up a throwaway local web server and confirm it responds (stand-in for Apache/Nginx):
   ```fish
   timeout 3 python3 -m http.server 8888 --directory /tmp &
   sleep 1
   curl -s http://127.0.0.1:8888/ | head -5
   wait
   ```
   bash/sh: `python3 -m http.server 8888 --directory /tmp & sleep 1; curl -s http://127.0.0.1:8888/ | head -5; wait`.
2. Write out (do not necessarily apply) the two torrc lines needed to expose that local server as
   an onion service on virtual port 80: `HiddenServiceDir` and `HiddenServicePort`. Explain in
   1-2 sentences what each line does.
3. Explain in 2-3 sentences why the guide recommends a Unix socket backend
   (`unix:/run/tor/my-website.sock`) over a TCP `127.0.0.1:port` backend — what does "leaking an
   Onion Service to the local network" mean concretely (hint: what else can reach 127.0.0.1 on a
   multi-user or containerized host)?
4. Explain in 2-3 sentences why the private key files inside `HiddenServiceDir` are exactly as
   sensitive as a web server's TLS private key, and what an attacker who steals them could do.
5. (Optional, root, real network access, slow — skip if short on time) Actually configure and
   restart Tor with the torrc lines from step 2 pointing at the python server, then read
   `/var/lib/tor/my_website/hostname` for the generated `.onion` address and visit it in Tor
   Browser. This step can take over a minute to bootstrap and depends on network reachability.

## 5. Running/understanding Tor relays

1. Inspect the real `ExitPolicy` torrc directive that controls whether a relay is exit or
   non-exit:
   ```fish
   man 1 tor | grep -i -A5 "^ *ExitPolicy "
   ```
   bash/sh: identical.
2. List the 4 relay roles (guard, middle, exit, bridge) and for each, write one sentence on its
   legal/abuse-complaint exposure level (none/low/high) and why.
3. Take your link-1 circuit diagram (You -> Guard -> Middle -> Exit -> Destination) and draw the
   bridge variant (You -> Bridge -> Middle -> Exit -> Destination). Explain in 2-3 sentences why
   the bridge substitutes for the guard specifically, not the middle or exit.
4. Explain in 2-3 sentences why the guide recommends exit relays be run by institutions
   (universities, libraries, relay associations) rather than from a home connection — what
   specific real-world consequence (name it) does a home exit operator risk that a guard/middle
   operator does not?
5. Explain in 2-3 sentences what a "pluggable transport" adds on top of a plain bridge, and why
   even bridges alone aren't sufficient against the most sophisticated censors (the page names
   China and Iran as examples that detect and block bridge connections directly).

## 6. Tor support/documentation hub

1. Confirm "Little-t tor" (one of the hub's 9 categories) maps to the local man page already used
   throughout this section:
   ```fish
   man 1 tor | head -3
   ```
   bash/sh: identical.
2. Build a table mapping each of the 9 hub categories (About Tor, Tor Browser, Tor VPN beta,
   Tails, Relays, Onion Services, Little-t tor, Mullvad Browser, Abuse, Anti-censorship) to the
   link number in this study set that already covers it (several map to links 1, 3, 4, 5 — some,
   like Tor VPN beta and Tails, aren't covered elsewhere in this set at all).
3. Write 2-3 sentences distinguishing "Tor Browser" from "Tor VPN (beta)" based on the hub's own
   description — which one anonymizes just browser traffic vs. all apps' traffic?
4. Write 1-2 sentences on what Mullvad Browser is and how it's related to but distinct from Tor
   Browser (hint: shared anti-fingerprinting tech, different network path).
5. Identify which single category on this hub you'd check first for "how does Tor Project handle
   reports that someone is using an exit relay for something illegal" — justify your choice in one
   sentence.

## 7. Combining Tor with VPN

1. Confirm both tools are available locally (no live combined tunnel needed for this exercise):
   ```fish
   tor --version
   wg --version
   ```
   bash/sh: identical.
2. Draw ordering 1 (Tor-over-VPN / "VPN before Tor"): You -> VPN -> Guard -> Middle -> Exit ->
   Destination. Mark which party sees "this user connects to Tor" (answer: only the VPN provider,
   not the ISP) and which sees final destination traffic content (answer: the exit relay, if
   unencrypted past it).
3. Draw ordering 2 (VPN-over-Tor / "Tor before VPN"): You -> Guard -> Middle -> Exit -> VPN ->
   Destination. Mark which party sees "this user connects to Tor" (answer: the ISP, this time)
   and which no longer can see the VPN traffic itself (answer: the exit relay, now VPN-encrypted).
4. Write 3-4 sentences on why a journalist in a heavily censored/monitored country would prefer
   ordering 1 specifically (hint: in some regimes, the mere fact of connecting to Tor — regardless
   of content — is itself treated as suspicious activity worth flagging).
5. Write 2-3 sentences on the practical cost both orderings share (hint: what happens to
   round-trip latency when you chain a VPN's encryption/relay hop with Tor's 3-relay circuit
   instead of using either alone)?
