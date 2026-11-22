# Computer Networks: GATE 2027 (CS only; not in the DA paper)

**Syllabus basis (official CS 2027 PDF, partly read):** principles of layering; switching (circuit, packet, virtual circuit) and performance metrics; data link layer (error detection, MAC, Ethernet); distance-vector and link-state routing; IPv4 (fragmentation, CIDR, NAT); TCP flow and congestion control; socket API; application layer: DNS and HTTP. Dropped from the list: UDP, ARP, DHCP, ICMP, SMTP, FTP, email, flooding. See `cn-2027-check.md`.
**Hbk** column: the Arihant Handbook CN chapter is pp. 218–272. Per-topic pages are not mapped. Marked `218–272*`.
**Links:** only URLs returned by search. I did not open each one. No NPTEL links were verified; add yours under *My links*. I found no DNS-specific GFG page and only a C# socket page, so rows 12 and 13 are thin.
This is a strong subject for you, so the notes are compact: formulas plus examples.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Layering (OSI, TCP/IP), switching, delays, performance metrics | 218–272* | [LMN Computer Networks](https://www.geeksforgeeks.org/computer-networks/last-minute-notes-computer-network/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Error detection: parity, checksum, CRC | 218–272* | [Error detection](https://www.geeksforgeeks.org/computer-networks/error-detection-in-computer-networks/) · [Checksum vs CRC](https://www.geeksforgeeks.org/computer-networks/difference-between-checksum-and-crc/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Hamming code (error correction) | 218–272* | [How CRC / Hamming fit in error control](https://www.geeksforgeeks.org/computer-networks/how-does-crc-in-a-frame-determine-if-data-is-intact/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Stop-and-wait, Go-Back-N, Selective Repeat | 218–272* | [Stop and Wait](https://www.geeksforgeeks.org/computer-networks/stop-and-wait-arq/) · [Go-Back-N](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocol-set-2-receiver-side/) · [Selective Repeat](https://www.geeksforgeeks.org/sliding-window-protocol-set-3-selective-repeat/) · [Compare all three](https://www.geeksforgeeks.org/difference-between-stop-and-wait-gobackn-and-selective-repeat/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | MAC: ALOHA, CSMA, CSMA/CD, Ethernet frame size | 218–272* | [CSMA variants](https://www.geeksforgeeks.org/computer-networks/difference-between-1-persistent-p-persistent-and-non-persistent-csma/) · [LMN (MAC section)](https://www.geeksforgeeks.org/computer-networks/last-minute-notes-computer-network/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | IPv4 addressing, subnetting, CIDR, supernetting | 218–272* | [Network layer GATE set](https://www.geeksforgeeks.org/network-layer-gq/) · [LMN (network layer)](https://www.geeksforgeeks.org/computer-networks/last-minute-notes-computer-network/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | IPv4 header, fragmentation (MTU, offset, MF), TTL | 218–272* | [Network layer in OSI](https://www.geeksforgeeks.org/computer-networks/network-layer-in-osi-model/) · [TTL](https://www.geeksforgeeks.org/computer-networks/what-is-time-to-live-ttl/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | NAT | 218–272* | [LMN (network layer)](https://www.geeksforgeeks.org/computer-networks/last-minute-notes-computer-network/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Distance-vector routing, count-to-infinity, split horizon | 218–272* | [DV vs LS](https://www.geeksforgeeks.org/computer-networks/difference-between-distance-vector-routing-and-link-state-routing/) · [Classification of routing](https://www.geeksforgeeks.org/computer-networks/classification-of-routing-algorithms/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Link-state routing (Dijkstra at each router) | 218–272* | [Link state routing](https://www.geeksforgeeks.org/unicast-routing-link-state-routing/) · [RIP vs OSPF](https://www.geeksforgeeks.org/computer-networks/difference-between-rip-and-ospf/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | TCP: header, connection setup and teardown, flow control (window), timers | 218–272* | [LMN (transport layer)](https://www.geeksforgeeks.org/computer-networks/last-minute-notes-computer-network/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | TCP congestion control: slow start, AIMD, fast retransmit / recovery | 218–272* | [LMN (transport layer)](https://www.geeksforgeeks.org/computer-networks/last-minute-notes-computer-network/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 13 | Socket API (socket, bind, listen, accept, connect) | 218–272* **check** | [Socket programming (C#, thin)](https://www.geeksforgeeks.org/c-sharp/socket-programming-in-c-sharp/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 14 | Application layer: DNS | 218–272* **check** | no GFG link found; add yours | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 15 | Application layer: HTTP (persistent vs non-persistent, stateless) | 218–272* | [HTTP persistent and non-persistent](https://www.geeksforgeeks.org/computer-networks/http-non-persistent-persistent-connection/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [Computer Network tutorial](https://www.geeksforgeeks.org/computer-network-tutorials/), [200-day plan: CN days 161–180](https://www.geeksforgeeks.org/blogs/200-days-of-gate-cs/). Your existing `networking.md` has question-history analysis and lab tools; keep using it alongside this file.

**My links:** (NPTEL / textbook, add here)

---

## 1. Delays and switching
- Transmission delay Tt = L/B. Propagation delay Tp = d/v. RTT = 2·Tp (plus processing and queuing if given).
- Store-and-forward over k links, one packet: total = k·Tt + k·Tp (ignoring queuing).
- Bandwidth-delay product = B × RTT (bits in flight). Link utilisation = useful time / total time.
- Circuit switching: setup cost, then fixed rate. Packet switching: no setup, statistical sharing, delay varies. Virtual circuit: setup, then fixed path with short VC identifiers.

## 2–3. Error detection and correction
- Parity detects odd-bit errors. Checksum: 1's complement of the 1's complement sum of 16-bit words; receiver sum of all words including the checksum is all 1s.
- CRC: append (r − 1) zeros for an r-bit generator, divide modulo 2, append the remainder. It detects all burst errors up to length r − 1 and all odd-bit errors if the generator has factor (x + 1).
- Hamming: r parity bits for m data bits need 2^r ≥ m + r + 1. Minimum distance d detects d − 1 errors and corrects ⌊(d − 1)/2⌋.

## 4. Sliding window
- a = Tp/Tt. Stop-and-wait efficiency = 1/(1 + 2a). Go-Back-N and Selective Repeat efficiency = min(1, N/(1 + 2a)).
- Window to fill the pipe: N = 1 + 2a.
- Sequence bits k: Go-Back-N window ≤ 2^k − 1; Selective Repeat window ≤ 2^(k−1).
- Go-Back-N: receiver window 1, cumulative ACK, resend from the lost frame. Selective Repeat: both windows N, individual ACK, buffering.

## 5. MAC and Ethernet
- Pure ALOHA max efficiency 1/(2e) ≈ 18.4%; slotted ALOHA 1/e ≈ 36.8%.
- CSMA/CD: minimum frame time ≥ 2·Tp, so minimum frame size = 2·Tp × B. Binary exponential backoff after collisions. Standard 10 Mbps Ethernet: 64-byte minimum frame (512 bits).
- Efficiency of CSMA/CD ≈ 1/(1 + 6.44a) (approximate textbook form).

## 6–8. IPv4
- Classful: A 0–127 (/8), B 128–191 (/16), C 192–223 (/24). Usable hosts = 2^h − 2. CIDR a.b.c.d/n: network = address AND mask; broadcast = host bits all 1.
- Subnetting borrows host bits. Supernetting/aggregation merges contiguous blocks with a common prefix.
- Header: minimum 20 bytes (HLEN × 4). Fragment offset is in units of 8 bytes; MF = 1 on all but the last fragment. Each fragment's data (except the last) must be a multiple of 8 bytes and ≤ MTU − header.
- TTL decrements at each router; discarded at 0.
- NAT: translates private to public address and port; the router keeps a mapping table.

## 9–10. Routing
- Distance vector (Bellman-Ford): each node tells neighbours its table; D_x(y) = min over neighbours v of [c(x, v) + D_v(y)]. Count-to-infinity; fixed partly by split horizon, poison reverse, hop limit (RIP 15).
- Link state (Dijkstra): flood link-state packets, each router knows the full topology and computes its own shortest paths. Faster convergence, more overhead. RIP is distance vector; OSPF is link state.

## 11–12. TCP
- Flow control: receiver window rwnd. Sender window = min(cwnd, rwnd). Throughput ≤ window/RTT.
- Sequence numbers count bytes; 32-bit space wraps in 2³²·8/B seconds.
- Congestion: slow start doubles cwnd per RTT until ssthresh, then +1 MSS per RTT (congestion avoidance). Timeout: ssthresh = cwnd/2, cwnd = 1. Triple duplicate ACK (fast retransmit and recovery): ssthresh = cwnd/2, cwnd = ssthresh (Reno).

## 13–15. Application layer
- Socket calls (TCP server): socket → bind → listen → accept → recv/send → close. Client: socket → connect → send/recv → close.
- HTTP is stateless; non-persistent uses a new TCP connection per object (2 RTT per object, no pipelining); persistent keeps it open; pipelined persistent sends requests back to back.
- DNS: name → IP; hierarchical (root, TLD, authoritative); iterative vs recursive queries; records are cached for their TTL.

---

## Worked examples (all recomputed in code)

**E1: Delays.** 1500 B packet, 10 Mbps, 2000 km at 2×10⁸ m/s: Tt = **1.2 ms**, Tp = **10 ms**. Over three links, store-and-forward transmission time totals **3.6 ms**.

**E2: Stop-and-wait.** Tt = 1 ms, Tp = 24.5 ms: a = 24.5, efficiency = 1/50 = **2%**. Window to fill the pipe = 1 + 2a = **50**.

**E3: Sequence bits.** Go-Back-N with window 7 needs **3** bits (7 ≤ 2³ − 1). Selective Repeat with window 4 needs **3** bits (2 × 4 = 8 ≤ 2³).

**E4: CRC.** Data 1101011011, generator 10011: remainder (check bits) = **1110**.

**E5: Hamming.** 7 data bits need **4** parity bits (2⁴ = 16 ≥ 7 + 4 + 1).

**E6: Ethernet minimum frame.** 10 Mbps, 2.5 km at 2×10⁸ m/s: 2·Tp·B = **250 bits** minimum frame.

**E7: Internet checksum.** Header words 4500, 0073, 0000, 4000, 4011, c0a8, 0001, c0a8, 00c7 (checksum field 0): checksum = **0xB861**.

**E8: CIDR.** 192.168.10.0/26: mask **255.255.255.192**, **62** usable hosts, broadcast **192.168.10.63**. Splitting 192.168.1.0/24 into /26 blocks, the third is **192.168.1.128/26**. A /23 has **510** usable hosts. 10.0.0.0/25 and 10.0.0.128/25 aggregate to **10.0.0.0/24**.

**E9: Fragmentation.** 4000-byte datagram (20-byte header), MTU 1500: data 3980 bytes split as 1480, 1480, 1020. Fragments: size 1500, offset **0**, MF 1; size 1500, offset **185**, MF 1; size 1040, offset **370**, MF 0.

**E10: Distance vector.** Links A–B 1, B–C 2, A–C 5: A's cost to C = min(5, 1 + 2) = **3**.

**E11: TCP congestion.** ssthresh 16, cwnd starts at 1: cwnd per RTT = **1, 2, 4, 8, 16, 17, 18, 19**. A timeout at cwnd 24 sets ssthresh to **12**.

**E12: TCP numbers.** 65535-byte window, RTT 100 ms: throughput ≤ **5.24 Mbps**. 32-bit sequence space at 1 Gbps wraps in **34.4 s**.

**E13: ALOHA.** Pure **0.184**, slotted **0.368**.

**E14: HTTP.** 1 base page + 5 objects, RTT = 1 unit: non-persistent without parallelism = **12** RTT; persistent without pipelining = **7**; persistent with pipelining = **3**.

---

## Notes / flags
- Rows 13 and 14 (socket API and DNS) are the weakest link coverage and the likeliest Handbook gaps (**check**).
- Section 5's CSMA/CD efficiency formula is the common textbook approximation; confirm against your book before using it.
- UDP, ARP, DHCP, ICMP, SMTP, FTP, email and flooding are dropped from the 2027 list, so they have no rows here.
- Past-paper analysis is in your `networking.md`, not repeated here.
