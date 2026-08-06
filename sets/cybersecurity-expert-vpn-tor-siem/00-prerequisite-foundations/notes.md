# 0. Prerequisite Foundations — Notes

## Networking basics (OSI/TCP-IP, routing, NAT, DNS) — Internet protocol suite (Wikipedia)

**Claim**: The Internet runs on a 4-layer model (link, internet, transport, application) that
predates and simplifies OSI's 7 layers by merging session/presentation/application into one
application layer. Two core design principles hold the whole thing together: the end-to-end
principle (keep the network core dumb/stateless, push intelligence to the endpoints) and the
robustness principle (be strict about what you send, lenient about what you accept). Each layer
encapsulates the one above it in its own header, which is what lets IP not care whether it's
carrying TCP or UDP, and what lets Ethernet not care whether it's carrying IPv4 or IPv6.

**Simple explanation**: Think of it like a postal system — the link layer is the local delivery
truck (MAC addresses, one hop), the internet layer is the routing between post offices (IP
addresses, can cross networks), the transport layer decides whether you want a tracked/guaranteed
delivery (TCP) or a cheap best-effort postcard (UDP), and the application layer is the actual
letter content (HTTP, DNS, SMTP). Every layer just wraps the previous layer's output in another
envelope — that's encapsulation.

**Try it**: Show each layer concretely on this machine — link/internet layer with `ip`, transport
reachability with `traceroute`, application layer with `dig`.
```fish
# internet layer: this host's IP address and default route
ip -4 addr show
ip route show

# transport/internet layer path — each hop is a router terminating fewer layers than the endpoints
traceroute -m 5 -w 1 8.8.8.8

# application layer: DNS resolution (A record) — note this is itself an application-layer protocol
# riding on top of UDP/transport and IP/internet layers
dig +short A wikipedia.org
```
bash/sh: identical — all three commands (`ip`, `traceroute`, `dig`) take the same syntax in bash.

## Applied cryptography fundamentals — Cryptography Engineering (Ferguson/Schneier/Kohno)

**Claim**: The book's core argument is that cryptographic *theory* (knowing what AES or RSA is)
is not the same skill as cryptographic *engineering* (knowing how to deploy them safely inside a
real system). It reframes crypto as a systems-design problem: the interface between the algorithm
and people, hardware, software, economics, and policy is where real-world breaks happen — not
usually the math itself. It teaches a threat-modeling mindset: understand how an adversary thinks
before choosing a design, because most practical cryptographic failures are implementation/misuse
failures (bad key management, reused nonces, no authentication on ciphertext) rather than broken
algorithms.

**Simple explanation**: Knowing the recipe for a lock doesn't mean you know how to secure a
building — you also need to think about who has keys, how they're issued, what happens when one
is lost, and whether someone can just walk in the window instead. This book is about the "walk in
the window" failures: 99% of real crypto breaks are the surrounding system, not the cipher math.

**Try it**: Demonstrate one of the book's central practical lessons — encryption alone is not
authentication (confidentiality != integrity) — using OpenSSL locally.
```fish
# symmetric encryption round-trip (confidentiality only, no integrity check)
openssl enc -aes-256-cbc -pbkdf2 -in /etc/hostname -out /tmp/test.enc -pass pass:demo123
openssl enc -d -aes-256-cbc -pbkdf2 -in /tmp/test.enc -pass pass:demo123
rm /tmp/test.enc
```
bash/sh: identical (openssl CLI syntax does not depend on shell).
Follow-up (applied exercise, no command): read the book's chapter on authenticated encryption and
write 3-5 sentences explaining why plain CBC-mode encryption (as run above) is vulnerable to
ciphertext tampering, and what AEAD modes like AES-GCM add to close that gap.

## Free graduate-level applied crypto book — "A Graduate Course in Applied Cryptography" (Boneh & Shoup)

**Claim** (verified via local `pdftotext` extraction of the PDF — WebFetch could not parse the
binary-heavy PDF encoding directly): unlike the Schneier book above, this one's core method is
provable security — for every construction it states a precise security *definition* (e.g.
semantic security for encryption), then gives a proof, under stated assumptions, that the
construction meets that definition. It argues cryptography can't be unit-tested into correctness
("no amount of unit testing will uncover a security vulnerability in a cryptosystem") — you need
mathematical arguments instead. It's organized in three parts: Part I secret-key/symmetric crypto
(encryption, MACs, authenticated encryption), Part II public-key crypto (public-key encryption,
digital signatures — no pre-shared secret needed), Part III protocols built on top (identification,
key exchange, zero-knowledge, secure computation). Each chapter mixes real-world case studies of
deployed-system attacks with a "fun application" that uses the chapter's ideas in an unexpected
context.

**Simple explanation**: The Schneier book above teaches you to be a good crypto *builder*
(system-level judgment); this book teaches you to be a good crypto *prover* — for any scheme,
state exactly what "secure" means as a game an attacker could try to win, then prove the attacker
can't win it (assuming some hard math problem stays hard). It's the rigorous "why do we actually
believe AES-GCM is secure" companion to the practical "how do you not misuse AES-GCM" book.

**Try it**: This is a textbook, not a tool — the applied exercise is to engage with its actual
argument structure rather than run a command.
1. Open the PDF (`curl -sL -o cryptobook.pdf https://toc.cryptobook.us/book.pdf`, or read via
   `pdftotext cryptobook.pdf - | less`) and find the exact definition of "semantic security" in
   section 2.2.2.
2. In your own words (3-5 sentences), restate that definition as an attacker-vs-challenger game —
   what does the attacker get to see/choose, and what does it mean for the attacker to "win"?
3. Read section 2.4 ("A fun application: anonymous routing") and write 2-3 sentences on how it
   connects a symmetric-encryption security property to onion-routing (directly relevant to
   section 2 of this study set, Tor).
