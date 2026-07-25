# Computer Networks — Notes

---

### Data Link Layer

## Hamming Code in Computer Network — Notes

**1. Redundant bits formula**
`2^r ≥ m + r + 1` — minimum number of parity/redundant bits `r` needed for `m` data bits so single-bit errors can be detected *and* corrected.
*e.g. m=7 data bits → try r=4: 2⁴=16 ≥ 7+4+1=12 ✓ (r=3 fails: 2³=8 < 11) → need 4 parity bits, 11-bit codeword.*
*(Flag: the fetched page text rendered this as "2r ≥ m+r+1" — missing the exponent. Corrected to the standard `2^r` form here.)*

**2. Even-parity rule**
Each parity bit is set so the total count of 1's among all positions it covers (itself included) is **even**. Page: *"If that count is odd, the parity bit value is set to 1, making the total count of occurrences of 1's an even number."*

**3. Parity bit coverage (which positions each parity bit checks)**
- `R1` → positions with a 1 in bit-0 of the binary index: 1,3,5,7,9,11,...
- `R2` → positions with a 1 in bit-1: 2,3,6,7,10,11,...
- `R4` → positions with a 1 in bit-2: 4,5,6,7,12–15,...
- `R8` → positions with a 1 in bit-3: 8,9,10,11,...
Parity bits themselves always sit at power-of-2 positions (1,2,4,8,...); everything else is a data bit.

**4. Worked example (from page, position table recomputed for internal consistency)**
Data = 7 bits → r=4 → 11-bit codeword. Position layout:
```
Pos:  1   2   3   4   5   6   7   8   9   10  11
Bit:  R1  R2  d1  R4  d2  d3  d4  R8  d5  d6  d7
```
Reading the page's own per-position values (d1=1, d2=0, d3=0, d4=1, d5=1, d6=0, d7=1) reconstructs the data word as **1001101**.
*(Flag: a separate extraction pass of this same page reported the data word as "1011001" — that does not match the page's own position table and is treated as a garbled re-extraction. 1001101 is used below since it is the value that makes every parity check below come out consistent.)*

Encoding:
- `R1` checks {1,3,5,7,9,11} → data values at 3,5,7,9,11 = 1,0,1,1,1 (four 1's → even) → `R1 = 0`
- `R2` checks {2,3,6,7,10,11} → data values at 3,6,7,10,11 = 1,0,1,0,1 (three 1's → odd) → `R2 = 1`
- `R4` checks {4,5,6,7} → data values at 5,6,7 = 0,0,1 (one 1 → odd) → `R4 = 1`
- `R8` checks {8,9,10,11} → data values at 9,10,11 = 1,0,1 (two 1's → even) → `R8 = 0`
- Final codeword (pos 1–11): **0 1 1 1 0 0 1 0 1 0 1**

Error detection (from page): bit at position 6 flips 0→1 in transit. Recompute each check bit (1 = mismatch found):
- `c1` (checks 1,3,5,7,9,11) → unaffected → `c1 = 0`
- `c2` (checks 2,3,6,7,10,11) → position 6 is inside this set → now odd → `c2 = 1`
- `c4` (checks 4,5,6,7) → position 6 is inside this set → now odd → `c4 = 1`
- `c8` (checks 8,9,10,11) → unaffected → `c8 = 0`
- Combine as `c8 c4 c2 c1 = 0 1 1 0` = binary **0110** = decimal **6** → error located at bit 6. Page: *"binary...decimal...is 6."*

**Priority for your prep:** This is the single highest-yield item in the whole set (flagged "Complex" in the priority report) — practice building the position table and the c8c4c2c1 → decimal error-position trick cold; it is asked almost verbatim in GATE/ISRO papers.

---

## Framing in Data Link Layer — Notes

**1. Fixed-size framing**
Frame length is predefined; *"No start or end delimiters are required, as the frame length defines the boundary."* Padding is added to handle internal fragmentation when the message doesn't exactly fill a frame.

**2. Variable-size framing**
Needs an explicit boundary marker, via either:
- **Length field** — frame carries its own size.
- **End Delimiter (ED)** — a unique bit/byte pattern marks frame end.

**3. Byte/character stuffing**
Used for character-oriented data: an escape character is inserted before any in-data byte that would otherwise be mistaken for the delimiter.

**4. Bit stuffing rule**
ED is a bit pattern (e.g. `01111110` in HDLC/PPP-style framing). Whenever **five consecutive 1's** appear inside the data, a `0` is stuffed in immediately after them, so the receiver never confuses data with the flag pattern. The receiver reverses this by deleting a `0` that follows five consecutive 1's.
*(Flag: the fetched page gave a specific numeric bit-stuffing example — data `011100011110` with ED `0111` → `011010001101100` — but re-deriving it bit-by-bit under the stated rule did not reproduce that exact output (length and insertion points didn't match), suggesting an extraction artifact. The standard textbook rule and a verified example are used below instead.)*

Worked example (standard form, independently verified):
```
Data (11 bits):  1 1 1 1 1 1 1 1 0 0 0
Scan, counting consecutive 1's, stuff a 0 after every 5th consecutive 1:
  bits 1-5 = 11111 (5 ones) → stuff 0 → counter resets
  bits 6-8 = 111 (3 ones, counter doesn't reach 5 again)
  bits 9-11 = 000
Output (12 bits): 1 1 1 1 1 0 1 1 1 0 0 0
```

**Priority for your prep:** Bit stuffing (5-ones rule) and the fixed vs variable framing distinction are the direct-numerical/definition items; byte stuffing is lower-yield, mostly definitional.

---

## Sliding Window Protocol — Notes

**1. Transmission & propagation delay**
`Tt = Data Size (D) / Bandwidth (B)`
`Tp = Distance (d) / Propagation Speed (s)`

**2. Stop-and-Wait efficiency**
`Efficiency = Tt / (Tt + 2Tp) = 1 / (1 + 2a)`, where `a = Tp / Tt`.

**3. Packets per cycle / sender window bits**
`Packets per cycle = 1 + 2a`
`Bits needed for sequence numbers = ⌈log₂(1 + 2a)⌉`
`Window Size (ws) = min(1 + 2a, 2^N)` where N = number of sequence-number bits.

**4. Effective bandwidth / link capacity**
`EB = Data Size (D) / (Tt + 2Tp)`
`Capacity = Bandwidth(B) × Tp` (half-duplex); `Capacity = 2 × Bandwidth(B) × Tp` (full-duplex).

**5. Worked example (from page)**
`Tt = 1 ms`, `Tp = 1.5 ms`.
- Sender transmits packet 0, then immediately sends packets 1, 2, 3 (sliding window, not waiting).
- ACK for packet 0 arrives after `2Tp = 3 ms`.
- Contrast: in plain **Stop-and-Wait**, only 1 packet is transferred per `Tt + 2Tp = 1 + 2(1.5) = 4 ms` cycle.

**Priority for your prep:** `Efficiency = 1/(1+2a)` and the window-size formula are direct numericals — practice plugging in Tt/Tp/bandwidth values. Go-Back-N vs Selective Repeat window-size derivations are lower-yield background on this page (the page names them but gives no separate formulas).

---

## Multiple Access Protocols in Computer Network — Notes

**1. ALOHA**
*"Designed for wireless LANs and shared media. Multiple stations can transmit simultaneously, leading to collisions."* Page lists Pure ALOHA and Slotted ALOHA as its two types but gives no formulas.

**2. CSMA (Carrier Sense Multiple Access)**
Rule (from page): *"Before transmitting, stations sense the medium: If idle → transmit. If busy → wait."* Still vulnerable to collisions due to propagation delay.

**3. CSMA/CD and CSMA/CA**
Listed on the page as Collision-Detection and Collision-Avoidance variants of CSMA, but no rules/details are given.

**4. ALOHA efficiency formulas (added for practice, not from page)**
`Pure ALOHA max throughput = 1/(2e) ≈ 18.4%`
`Slotted ALOHA max throughput = 1/e ≈ 36.8%`
Reasoning: slotting halves the vulnerable period for collisions vs. pure ALOHA, doubling max efficiency.

**Priority for your prep:** The page itself is thin — CSMA's sense-before-transmit rule is stated, but ALOHA/CSMA-CD/CA numeric efficiency is the actual exam content and is *not* on this page; treat the 18.4%/36.8% figures above as must-know even though sourced from general knowledge, not this GFG page.

---

### Transport Layer

## TCP 3-Way Handshake Process — Notes

**1. Step 1 — SYN**
*"Client wants to establish a connection with a server, so it sends a segment with SYN (Synchronize Sequence Number)"* — announces the client's starting sequence number.

**2. Step 2 — SYN-ACK**
*"Server responds to the client request with SYN-ACK signal bits set. Acknowledgement(ACK) signifies the response of the segment it received and SYN signifies with what sequence number it is likely to start."*

**3. Step 3 — ACK**
*"Client acknowledges the response of the server and they both establish a reliable connection with which they will start the actual data transfer."*

**4. Worked example (illustrative — flagged as not confirmed verbatim on the page; treat as practice, not a quoted GFG example)**
```
Client ISN = 1000, Server ISN = 5000
Step 1: Client → Server   SEQ = 1000, SYN = 1
Step 2: Server → Client   SEQ = 5000, ACK = 1001 (client's SEQ + 1), SYN = 1
Step 3: Client → Server   SEQ = 1001, ACK = 5001 (server's SEQ + 1)
```
General rule embedded in the example: each side's ACK number = other side's (SEQ + 1).

**Priority for your prep:** Know the 3 steps and the "ACK = peer's SEQ + 1" rule cold — that rule is what direct numericals test (given ISNs, compute the SEQ/ACK in each of the 3 segments).

---

## TCP Congestion Control — Notes

**1. Slow start (exponential growth)**
Starts at `cwnd = 1`; doubles every RTT: *"cwnd = 2^(1) = 2. 2 RTT, cwnd = 2^(2) = 4. 3 RTT, cwnd = 2^(3) = 8"* — i.e. `cwnd = 2^n` after `n` RTTs, until `cwnd` reaches `ssthresh`.

**2. Congestion avoidance (linear growth / additive increase)**
Once past `ssthresh`: *"cwnd = i. After 1 RTT, cwnd = i+1. 2 RTT, cwnd = i+2. 3 RTT, cwnd = i+3"* — i.e. `+1` segment per RTT.

**3. On timeout (severe congestion)**
`ssthresh = cwnd / 2`, then `cwnd = 1` → restart slow start from scratch.

**4. On 3 duplicate ACKs (fast recovery, milder signal)**
`ssthresh = cwnd / 2`, then `cwnd = ssthresh` → resume directly in congestion avoidance (no full reset).

**5. Worked example (added for practice — page only shows a graph with ssthresh reaching 32 at round 5, congestion avoidance to round 10, dup-ACKs at round 10, timeout at round 16, with no numeric table; table below is constructed consistent with the rules above)**
```
Round:    1  2  4  8  16  32  ← slow start (cwnd = 2^n), reaches ssthresh=32 at round 6
Round 7:  cwnd = 33  (congestion avoidance begins, +1/RTT)
Round 8:  cwnd = 34
  ...
Round 16: cwnd = 42, 3 duplicate ACKs detected
          → ssthresh = 42/2 = 21, cwnd = 21 (fast recovery, stay in congestion avoidance)
Round 22: cwnd = 27, timeout occurs
          → ssthresh = 27/2 = 13, cwnd = 1 (back to slow start)
```

**Priority for your prep:** Flagged "Complex" tier — practice the two growth rules (`2^n` vs `+1`) and especially the two different `ssthresh` reset rules (timeout → cwnd=1 vs 3-dup-ACK → cwnd=ssthresh), since exam questions typically give a round-by-round cwnd trace and ask you to identify which event occurred.

---

## Flow Control in Data Link Layer — Notes

**1. Stop-and-Wait flow control**
*"The sender transmits one frame at a time and waits for an acknowledgment from the receiver before sending the next frame."*

**2. Sliding window flow control**
*"The sender maintains a window of unacknowledged frames and moves (slides) the window forward as acknowledgments are received, enabling continuous and pipelined data transmission."*

**3. Worked example — no worked example on this page.**
*(added for practice, not from page)*: with a window size of 4 and frames numbered 0–7 (3-bit sequence numbers), sender can have frames 0,1,2,3 outstanding unacknowledged; once ACK for frame 0 arrives, the window slides to allow frame 4 to be sent.

**Priority for your prep:** This page is purely conceptual — the actual numericals for these two mechanisms live in the Sliding Window Protocol page above (efficiency/window-size formulas); use this page only for the definition-level distinction between the two.

---

### Network Layer

## Introduction of Classful IP Addressing — Notes

**1. Classful table (from page)**

| Class | Leading bits | Net ID bits | Host ID bits | # Networks | Usable hosts/network | Default mask | Range |
|---|---|---|---|---|---|---|---|
| A | `0` | 8 | 24 | 2⁷=128 | 2²⁴−2=16,777,214 | 255.0.0.0 | 0.0.0.0–127.255.255.255 |
| B | `10` | 16 | 16 | 2¹⁴=16,384 | 2¹⁶−2=65,534 | 255.255.0.0 | 128.0.0.0–191.255.255.255 |
| C | `110` | 24 | 8 | 2²¹=2,097,152 | 2⁸−2=254 | 255.255.255.0 | 192.0.0.0–223.255.255.255 |
| D | `1110` | — | — | — (multicast) | — | — | 224.0.0.0–239.255.255.255 |
| E | `1111` | — | — | — (reserved) | — | — | 240.0.0.0–255.255.255.255 |

**2. Why "−2" for usable hosts**
One host address per network is reserved as the network address (all host bits 0) and one as the broadcast address (all host bits 1); hence `2^(host bits) − 2`.

**3. Worked example — no worked example on this page** (page gives the table above but no step-by-step "classify this IP" walkthrough).
*(added for practice, not from page)*: classify `172.16.5.4` — first octet 172 falls in 128–191 → Class B → default mask `255.255.0.0` → network part = `172.16.0.0`, host part = `0.0.5.4`.

**Priority for your prep:** Memorize the class ranges/masks table cold (direct 1-mark identification questions) — Class D/E details are lower-yield.

---

## Classless Inter-Domain Routing (CIDR) — Notes

**1. CIDR notation**
`a.b.c.d/n` where `n` = number of leading bits that form the network prefix (replaces the rigid classful boundaries).

**2. Usable host count formula (added for practice — not explicitly derived on the page)**
`Usable hosts = 2^(32−n) − 2`

**3. Worked example (from page, extended)**
Page: *"192.168.1.0/24 first 24 bits are the network, and the remaining 8 bits are the host ID."*
Extension *(added for practice)*: host bits = 32−24 = 8 → usable hosts = `2^8 − 2 = 254`; subnet mask = `255.255.255.0`.

**4. Block-size rule**
Page notes CIDR blocks must be a power of 2 (`2ⁿ`) in size, which is why prefixes can be shorter (aggregating multiple classful networks) or longer (subdividing one) than the old class boundaries.

**Priority for your prep:** The `2^(32−n)−2` host-count formula plus converting between `/n` and dotted-decimal mask are the direct numericals — this page itself is thin on worked numbers, so practice the formula on several `/n` values (e.g. /24, /26, /28) yourself.

---

## Introduction to Subnetting — Notes

**1. Number of subnets**
`Number of subnets = 2^n` where `n` = number of bits borrowed from the host portion.

**2. Number of usable hosts per subnet**
`Number of hosts = 2^h − 2` where `h` = remaining host bits.

**3. Worked example (from page)**
A Class C network is divided into **two** subnets by borrowing 1 host bit (`2¹ = 2` subnets):
*(Flag: the fetched page labelled the starting network as "193.1.2.0/25", but a `/25` network only spans .0–.127 and could not itself contain a second subnet ranging .128–.255. The two resulting subnet masks are genuinely `/25` (`255.255.255.128`), so the correct original/parent network must be the full Class C block `193.1.2.0/24`, divided into two `/25` subnets — corrected below.)*
```
Parent network: 193.1.2.0/24, borrow 1 bit → 2 subnets, each /25

Subnet 1: 193.1.2.0   – 193.1.2.127   | Subnet ID 193.1.2.0   | Broadcast 193.1.2.127 | 126 usable hosts | mask 255.255.255.128
Subnet 2: 193.1.2.128 – 193.1.2.255   | Subnet ID 193.1.2.128 | Broadcast 193.1.2.255 | 126 usable hosts | mask 255.255.255.128
```

**Priority for your prep:** This is a direct GATE/ISRO numerical type — given a network + number of required subnets (or hosts), compute new mask, subnet IDs, broadcast addresses, and usable range. Practice the "borrow n bits → 2ⁿ subnets, 2^(8−n)−2 hosts" pattern until it's automatic.

---

## Network Address Translation (NAT) — Notes

**1. Definition**
*"Network Address Translation (NAT) allows multiple devices in a private network to access the internet using a single public IP address."*

**2. Static NAT**
*"Static NAT creates a one-to-one mapping between a private IP address and a public IP address."* Each private address permanently maps to one public address.

**3. Dynamic NAT**
*"Dynamic NAT maps private IP addresses to public IP addresses from a predefined pool."* Public IPs assigned temporarily as needed.

**4. PAT / NAT Overload**
*"PAT, also known as NAT Overload, allows multiple private IPs to share a single public IP using different port numbers."* Most commonly deployed type (this is what home routers use).

**5. Worked example — no worked example on this page.**
*(added for practice, not from page)*: PAT table entry mapping `192.168.1.5:5000 → 203.0.113.10:61000` and `192.168.1.6:5000 → 203.0.113.10:61001` — same public IP, different translated port distinguishes the two internal hosts.

**Priority for your prep:** Know the 3 types (static/dynamic/PAT) and that PAT is the many-to-one, port-distinguished variant — this is mostly a definitional/MCQ topic rather than a numerical one for ISRO.

---

## Classification of Routing Algorithms — Notes

**1. Adaptive (dynamic) algorithms**
*"Change their routing decisions whenever network topology or traffic load changes."* Subtypes:
- **Isolated** — each node decides independently, no consultation with others.
- **Centralized** — one node holds full network info, makes all decisions.
- **Distributed** — nodes exchange info with neighbors before deciding (e.g. distance-vector style).

**2. Non-adaptive (static) algorithms**
*"Do not change their routing decisions once they have been selected."* Subtypes:
- **Flooding** — every incoming packet sent out on all lines except the one it arrived on.
- **Random walk** — packet sent to a randomly chosen neighboring node.

**3. Hybrid algorithms**
Combine adaptive + non-adaptive by splitting the network into regions.
- **Link-state** — routers build/share full network maps.
- **Distance-vector** — routers keep tables of distance/direction to all destinations, sharing only with neighbors.

**4. Worked example — no worked example on this page** (purely classificatory).
*(added for practice, not from page)*: RIP is an adaptive, distributed, distance-vector protocol; OSPF is adaptive, distributed, link-state.

**Priority for your prep:** Definitional/classification MCQ topic — know adaptive-vs-non-adaptive and the isolated/centralized/distributed split cold; flooding/random-walk are lower-yield background. No numericals expected from this specific page's content.

---

**General note on method:** where a GFG page lacked a genuine worked example, one short practice example was added and explicitly labeled "(added for practice, not from page)" per the task rules; two extraction discrepancies (Hamming data word, subnetting parent-network prefix) were cross-checked against internal consistency of the page's own numbers and corrected with a flag rather than silently propagated.
