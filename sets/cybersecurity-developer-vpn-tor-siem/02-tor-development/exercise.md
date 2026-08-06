# 2. Tor Development (relays, onion services, client libraries) — Exercises

Source list: `sets/cybersecurity-developer-vpn-tor-siem.md`, section 2.

## 1. Tor specifications index — map the spec suite

1. List every linked spec document from the index page (verified working):
   ```fish
   curl -sL https://spec.torproject.org/intro/index.html | grep -oE 'href="[^"]*\.html"' | sort -u
   ```
   ```
   # bash/sh:
   curl -sL https://spec.torproject.org/intro/index.html | grep -oE 'href="[^"]*\.html"' | sort -u
   ```
2. Sort the results into three buckets by hand: (a) core wire-protocol docs under `tor-spec/`,
   (b) numbered proposals under `proposals/`, (c) meta/navigation pages (`index.html`,
   `conventions.html`, `print.html`).
3. Note which of the two listed proposals (329, 340) is already implemented in the C tor codebase
   per the index page text but not yet merged into the formal spec — this is the "spec lags
   implementation" pattern to watch for when reading any single spec page as if it were 100% current.
4. Bookmark (in this note) that `rend-spec` (onion services rendezvous protocol) is NOT listed on
   this particular index page's link list — it lives at a different path, covered directly as this
   section's link 3. Don't assume one index page enumerates the entire spec suite.

## 2. torspec source — clone and read the Cell Packet Format section

1. Shallow-clone the repo (verified: completes in seconds):
   ```fish
   git clone --depth 1 https://github.com/torproject/torspec /tmp/torspec-src
   ```
   ```
   # bash/sh:
   git clone --depth 1 https://github.com/torproject/torspec /tmp/torspec-src
   ```
2. List all top-level spec files and note which ones map to concepts referenced elsewhere in this
   section (`rend-spec-v3.txt` → links 3-4; `control-spec.txt` → links 6-7):
   ```fish
   ls /tmp/torspec-src/*.txt
   ```
3. Extract Section 3 (Cell Packet Format) of `tor-spec.txt` and read the full list of named cell
   commands:
   ```fish
   grep -n -A40 "^3. Cell Packet format" /tmp/torspec-src/tor-spec.txt | head -60
   ```
4. By hand, draw the byte layout of a fixed-length cell (`CircID | Command | Payload`) and a
   variable-length cell (`CircID | Command | Length | Payload`), labeling each field's byte width
   from the spec text (`CIRCID_LEN` is 2 or 4 bytes depending on link protocol version; `Command` is
   1 byte; `Length` is 2 bytes big-endian for variable-length cells).
5. Clean up (must not be committed):
   ```fish
   rm -rf /tmp/torspec-src
   ```

## 3. Onion services rendezvous protocol overview — draw the 5-step sequence

1. WebFetch could not verify this specific domain on this run — fetch and de-tag the page with
   `curl` instead (verified working):
   ```fish
   curl -sL https://spec.torproject.org/rend-spec/protocol-overview.html -o (mktemp -t rend-overview.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://spec.torproject.org/rend-spec/protocol-overview.html -o /tmp/rend-overview.html
   ```
2. Strip HTML tags for readability (quick approximation; good enough for prose pages like this):
   ```fish
   sed -e 's/<[^>]*>//g' /tmp/rend-overview.html | sed -n '150,220p'
   ```
   ```
   # bash/sh:
   sed -e 's/<[^>]*>//g' /tmp/rend-overview.html | sed -n '150,220p'
   ```
3. By hand, draw a 5-actor sequence diagram: Hidden Service → Introduction Points (setup phase,
   dashed/pre-established) → HSDir (descriptor upload) → Client → Rendezvous Point (fresh circuit)
   → Introduction Point (introduction request) → Hidden Service (completes handshake at rendezvous
   point). Label which circuits are "already built before the client shows up" vs "built fresh per
   connection."
4. Write one sentence on why the *rendezvous point* is chosen fresh by the client per-connection
   while *introduction points* are chosen and pre-committed by the service — what anonymity property
   would break if the roles were reversed?
5. Clean up:
   ```fish
   rm -f /tmp/rend-overview.html
   ```

## 4. Onion services developer overview — verify all 9 Acts and the 6-hop total

1. Fetch and de-tag the community.torproject.org overview page (same curl fallback as exercise 3):
   ```fish
   curl -sL https://community.torproject.org/onion-services/overview/ -o (mktemp -t onion-overview.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://community.torproject.org/onion-services/overview/ -o /tmp/onion-overview.html
   ```
2. Strip tags with a short Python one-liner (handles `&quot;`/entities better than pure `sed`):
   ```fish
   python3 -c "
   import re, html
   with open('/tmp/onion-overview.html') as f:
       t = f.read()
   t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
   t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
   t = re.sub(r'<[^>]+>', ' ', t)
   print(html.unescape(t))
   " > /tmp/onion-overview.txt
   ```
3. Confirm all 9 Acts are present (a first-pass partial fetch during initial research only caught 4
   — don't assume a truncated read is the whole page):
   ```fish
   grep -E -n "^ Act [0-9]" /tmp/onion-overview.txt
   ```
4. Read Act 6 and Act 8 specifically and write one sentence on what the "one-time secret" prevents
   — why can't the rendezvous point just blindly splice any two circuits that show up asking for
   the same rendezvous cookie?
5. Confirm the "6 relay hops total" claim from Act 9 (3 client-picked + 3 service-picked) and
   contrast it with ordinary Tor browsing's 3-hop circuit — write down why an onion-service
   connection costs double the relay hops of regular Tor browsing.
6. Clean up:
   ```fish
   rm -f /tmp/onion-overview.html /tmp/onion-overview.txt
   ```

## 5. Setting up onion services — validate a torrc without touching the network

1. Confirm Tor is installed locally (verified present: 0.4.9.11 on this machine):
   ```fish
   tor --version
   ```
   ```
   # bash/sh:
   tor --version
   ```
2. Build a minimal, throwaway `torrc` fragment with the two required directives from the guide:
   ```fish
   set hsdir (mktemp -d -t tor-hs-test.XXXX)
   set torrc (mktemp -t torrc.XXXX)
   printf "DataDirectory %s/data\nHiddenServiceDir %s\nHiddenServicePort 80 127.0.0.1:8080\n" $hsdir $hsdir > $torrc
   ```
   ```
   # bash/sh:
   hsdir=$(mktemp -d -t tor-hs-test.XXXX)
   torrc=$(mktemp -t torrc.XXXX)
   printf "DataDirectory %s/data\nHiddenServiceDir %s\nHiddenServicePort 80 127.0.0.1:8080\n" "$hsdir" "$hsdir" > "$torrc"
   ```
3. Validate the config offline with `--verify-config` (parses/checks only — does NOT start the
   daemon or contact the live Tor network, so this stays within the "coding/analysis, not live
   infrastructure" boundary):
   ```fish
   tor --verify-config -f $torrc
   ```
   ```
   # bash/sh:
   tor --verify-config -f "$torrc"
   ```
4. Deliberately break the permission requirement to see Tor's own defense fire (verified: this
   produces `[warn] Permissions on directory ... are too permissive` then `[err] Reading config
   failed`), then fix it and re-verify:
   ```fish
   chmod 755 $hsdir; tor --verify-config -f $torrc
   chmod 700 $hsdir; tor --verify-config -f $torrc
   ```
   ```
   # bash/sh:
   chmod 755 "$hsdir"; tor --verify-config -f "$torrc"
   chmod 700 "$hsdir"; tor --verify-config -f "$torrc"
   ```
5. Write one sentence on why this permission check matters even on a single-user machine (hint:
   multi-user systems, containers with shared volumes, backup tools that reset permissions).
6. Clean up (must not be committed, and never actually start the daemon against this config):
   ```fish
   rm -rf $hsdir $torrc
   ```
   ```
   # bash/sh:
   rm -rf "$hsdir" "$torrc"
   ```

## 6. Stem docs — install in a venv and syntax-check a controller snippet

1. Note the maintenance status first (this is a real project-health finding to record before
   depending on any library): Stem's own docs state it is "mostly unmaintained" as of its last
   release, 1.8.1 (September 2022) — verified via `curl` fallback since WebFetch couldn't reach
   `stem.torproject.org` this session.
2. Create an isolated venv (don't pollute the system Python) and install Stem into it:
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
3. Write a minimal controller snippet to a scratch file (connects to a control port that doesn't
   exist yet in this exercise — the goal here is syntax/API correctness, not a live connection):
   ```python
   import stem.connection
   from stem.control import Controller

   with Controller.from_port(port=9051) as controller:
       controller.authenticate()
       print("Tor version:", controller.get_version())
       for circ in controller.get_circuits():
           print(circ.id, circ.status, [hop[0] for hop in circ.path])
   ```
4. Syntax-check it with the venv's Python (verified working: compiles cleanly):
   ```fish
   $venv/bin/python3 -m py_compile controller_snippet.py
   ```
   ```
   # bash/sh:
   "$venv/bin/python3" -m py_compile controller_snippet.py
   ```
5. Confirm the real `Controller.from_port` and `Controller.authenticate` signatures via
   `inspect.signature` instead of trusting memory (verified: `from_port(address='127.0.0.1',
   port='default')`):
   ```fish
   $venv/bin/python3 -c "from stem.control import Controller; import inspect; print(inspect.signature(Controller.from_port))"
   ```
   ```
   # bash/sh:
   "$venv/bin/python3" -c "from stem.control import Controller; import inspect; print(inspect.signature(Controller.from_port))"
   ```
6. Cross-reference: the `get_circuits()` call in the snippet maps to a `GETINFO circuit-status`
   control-protocol command — locate that command name in the `control-spec.txt` file cloned in
   exercise 2, confirming Stem is a thin wrapper over the same protocol already read there.
7. Clean up (must not be committed):
   ```fish
   rm -rf $venv
   ```
   ```
   # bash/sh:
   rm -rf "$venv"
   ```

## 7. Stem Controller API reference — cross-check CircPurpose against the rendezvous protocol notes

1. Fetch and de-tag the API reference page (same curl + Python de-tag fallback as exercise 6):
   ```fish
   curl -sL https://stem.torproject.org/api/control.html -o (mktemp -t stem-control.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://stem.torproject.org/api/control.html -o /tmp/stem-control.html
   ```
2. After de-tagging to `stem-control.txt`, extract the `CircPurpose` enum table:
   ```fish
   grep -E -A10 "CircPurpose \( enum \)" /tmp/stem-control.txt
   ```
   ```
   # bash/sh:
   grep -E -A10 "CircPurpose \( enum \)" /tmp/stem-control.txt
   ```
3. Without looking back at exercise 3/4, write down from memory the 4-role split you already
   derived there (client→intro, client→rendezvous, service→intro, service→rendezvous), then check
   it against the actual `HS_CLIENT_INTRO` / `HS_CLIENT_REND` / `HS_SERVICE_INTRO` /
   `HS_SERVICE_REND` values — confirm they line up 1:1.
4. Extract `CircStatus` too and write the circuit lifecycle as a small state diagram:
   `LAUNCHED → (GUARD_WAIT) → EXTENDED → BUILT`, with `FAILED`/`CLOSED` as terminal states from any
   point:
   ```fish
   grep -E -A15 "CircStatus \( enum \)" /tmp/stem-control.txt
   ```
5. Locate the `NEWNYM` signal description and confirm it matches Tor Browser's "New Identity"
   button behavior (new circuits + cleared DNS cache) — one sentence on why clearing the DNS cache
   specifically matters for anonymity (hint: cached DNS answers can correlate old and new
   identities if reused across a circuit switch).
6. Clean up:
   ```fish
   rm -f /tmp/stem-control.html /tmp/stem-control.txt
   ```

## 8. Tor Project GitLab — locate the core repo and the first-contributor path

1. Fetch the org landing page and confirm it's a wiki-style contributor index rather than a plain
   marketing page:
   ```fish
   curl -sL https://gitlab.torproject.org/ -o (mktemp -t tor-gitlab.XXXX.html)
   ```
   ```
   # bash/sh:
   curl -sL https://gitlab.torproject.org/ -o /tmp/tor-gitlab.html
   ```
2. Confirm the core C `tor` implementation's repo path resolves (verified: `HTTP/2 200`):
   ```fish
   curl -sIL https://gitlab.torproject.org/tpo/core/tor
   ```
   ```
   # bash/sh:
   curl -sIL https://gitlab.torproject.org/tpo/core/tor
   ```
3. Write down, from the org page, the three things a first-time contributor needs to find: (a)
   the first-contributor issue list, (b) the onboarding page, (c) which team's process page is
   relevant to a given contribution area (e.g. a censorship-circumvention patch → Anti-censorship
   Team page).
4. Cross-reference: note that `torproject/torspec` (link 2, on GitHub) and `tpo/core/tor` (this
   link, on GitLab) are two different forges for two different repos — spec text lives on GitHub,
   the reference implementation's primary development happens on GitLab. Don't assume one hosting
   platform covers the whole project.
5. Clean up:
   ```fish
   rm -f /tmp/tor-gitlab.html
   ```

