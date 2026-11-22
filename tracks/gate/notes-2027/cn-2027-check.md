# Computer Networks: 2027 syllabus check against your networking.md

**Source:** the official CS GATE 2027 syllabus PDF (IIT Madras, gate2027.iitm.ac.in), read directly. The tool returned the section in part (an opening line quoted, the rest paraphrased), so the topic list below is complete in substance but not verbatim. This also corrects my earlier note that the official PDF couldn't be opened.

## What Section 10 now covers
1. Principles of layering.
2. Switching (circuit, packet, virtual circuit) and performance metrics.
3. Data link layer: error detection, MAC, Ethernet.
4. Routing: distance vector and link state.
5. IPv4: fragmentation, CIDR, NAT.
6. TCP flow control and congestion control.
7. Socket API.
8. Application layer: DNS and HTTP only.

## Compare with your networking.md

| Your section | Status for 2027 |
|---|---|
| Hamming code | Covered by "error detection" (still fine; CRC and checksum belong here too) |
| Framing | Not listed any more. Low priority |
| Sliding window / flow control (data link) | Keep for TCP flow control; stop-and-wait and Go-Back-N / Selective Repeat efficiency formulas still help as background |
| Multiple access (ALOHA, CSMA/CD) | Covered by "MAC" and Ethernet |
| TCP 3-way handshake | Not named in the summary I got; likely still useful for TCP, but lower priority |
| TCP congestion control | Keep: explicitly listed |
| Classful addressing, CIDR, subnetting, NAT | Keep: IPv4, CIDR, NAT are listed; subnetting is implied by CIDR |
| Routing algorithms classification | Keep distance vector and link state; flooding and shortest-path variants beyond these are dropped |

## Gaps to add (not in your file)
- Performance metrics: transmission, propagation, queuing delay; throughput; packet vs circuit switching delay comparisons.
- Ethernet: frame format, minimum frame size (2 × propagation delay × bandwidth), CSMA/CD.
- IPv4 fragmentation: offset and MF-flag numericals.
- Socket API: basic call sequence (socket, bind, listen, accept, connect, send/recv, close).
- DNS (resolution types, records) and HTTP (persistent vs non-persistent, request/response, status codes).

## Safe to drop for 2027
UDP, ARP, DHCP, ICMP, SMTP, FTP, email protocols, flooding, and framing as a separate topic: these are no longer listed (confirmed by several secondary sources and the official text's topic list). They are cheap to skip, but nothing stops a question using them as context.

## Related note
The same PDF confirms the Digital Logic and COA wording used in `digital-logic.md` and `computer-organization.md` (algebraic, K-map and tabular minimization; ALU design; hardwired and microprogrammed control; cache mapping; DMA and interrupts), so those two files need no change.
