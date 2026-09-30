# Networking — Consolidated Study Material (GATE + Google)

Everything Computer-Networks-related that's scattered across this repo, copy-pasted into one
file for convenience. **The source files below remain the source of truth** — this is a static
snapshot; if any source file is updated later, this file will not auto-update and should be
re-synced by hand (or ask to regenerate it).

**Source files merged here:**
1. `topics/gfg-gate-topic-map.md` §12 (Computer Networks study links) and §15 (hands-on lab tools)
2. `../../subjects/computer-networks.md` (deep-dive worked-formula notes)
3. `exam-priority-report.md` (Computer Networks tier placement, filtered priority links)
4. `topics/networking-question-analysis.md` (full 27-sitting question-history analysis)
5. `career-mapping/gate-vs-google-security-topics.md` §1.1 (Google job-market findings + books on disk)

**Not included** (exists only as chat output, not yet saved to any file): the deeper Google
year-over-year drift findings from a later research pass — the finding that "network security"
mentions in Google's live security-role postings roughly doubled 2024→2026 (19%→14%→45%), tied to
a shift toward "security-engineer" style requirement templates. Say the word if you want that
persisted into this file (or its own file) too.

---

# 1. GFG Study Links — from `gfg-gate-topic-map.md` §12

## 12. Computer Networks

**Fundamentals & Physical Layer**: [Basics of Networking](https://www.geeksforgeeks.org/computer-networks/basics-computer-networking/) · [Network Goals](https://www.geeksforgeeks.org/computer-networks/goals-of-networks/) · [Network Topologies](https://www.geeksforgeeks.org/computer-networks/types-of-network-topology/) · [LAN/MAN/WAN](https://www.geeksforgeeks.org/types-of-area-networks-lan-man-and-wan/) · [Transmission Media](https://www.geeksforgeeks.org/computer-networks/types-transmission-media/) · [Transmission Modes](https://www.geeksforgeeks.org/computer-networks/transmission-modes-computer-networks/) · [Line Coding Schemes](https://www.geeksforgeeks.org/digital-logic/difference-between-unipolar-polar-and-bipolar-line-coding-schemes/) · [Broadband vs Baseband](https://www.geeksforgeeks.org/digital-logic/difference-between-broadband-and-baseband-transmission/) · [OSI Model](https://www.geeksforgeeks.org/computer-networks/open-systems-interconnection-model-osi/) · [TCP/IP Model](https://www.geeksforgeeks.org/computer-networks/tcp-ip-model/)

**Data Link Layer**: [Multiple Access Protocols](https://www.geeksforgeeks.org/computer-networks/multiple-access-protocols-in-computer-network/) · [Framing](https://www.geeksforgeeks.org/computer-networks/framing-in-data-link-layer/) · [Ethernet](https://www.geeksforgeeks.org/computer-networks/what-is-ethernet/) · [Bit Stuffing](https://www.geeksforgeeks.org/computer-networks/bit-stuffing-in-computer-network/) · [Hamming Code](https://www.geeksforgeeks.org/computer-networks/hamming-code-in-computer-network/) · [Aloha (Pure/Slotted)](https://www.geeksforgeeks.org/computer-networks/what-is-pure-aloha/) · [CSMA](https://www.geeksforgeeks.org/computer-networks/carrier-sense-multiple-access-csma/) · [Controlled Access Protocols](https://www.geeksforgeeks.org/computer-networks/controlled-access-protocols-in-computer-network/) · [CSMA/CD Back-off Algorithm](https://www.geeksforgeeks.org/computer-networks/back-off-algorithm-csmacd/) · [Error Detection](https://www.geeksforgeeks.org/computer-networks/error-detection-in-computer-networks/) · [Stop and Wait ARQ](https://www.geeksforgeeks.org/computer-networks/stop-and-wait-arq/) · [Sliding Window Protocol Set 1](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocol-set-1/)/[2](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocol-set-2-receiver-side/)/[3 (Selective Repeat)](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocol-set-3-selective-repeat/) · [MAC Address](https://www.geeksforgeeks.org/computer-networks/mac-address-in-computer-network/) · [Channel Capacity](https://www.geeksforgeeks.org/computer-networks/maximum-data-rate-channel-capacity-for-noiseless-and-noisy-channels/) · [Switches](https://www.geeksforgeeks.org/computer-networks/what-is-a-network-switch-and-how-does-it-work/) · [Routers](https://www.geeksforgeeks.org/computer-networks/introduction-of-a-router/)

**Network Layer**: [Internetworking](https://www.geeksforgeeks.org/computer-networks/introduction-of-internetworking/) · [Classful IP Addressing](https://www.geeksforgeeks.org/computer-networks/introduction-of-classful-ip-addressing/) · [IPv4 Datagram Header](https://www.geeksforgeeks.org/computer-networks/introduction-and-ipv4-datagram-header/) · [Fragmentation](https://www.geeksforgeeks.org/computer-networks/fragmentation-network-layer/) · [IPv6](https://www.geeksforgeeks.org/computer-networks/internet-protocol-version-6-ipv6/) · [Classless Addressing](https://www.geeksforgeeks.org/computer-networks/ip-addressing-classless-addressing/) · [Classless Inter-Domain Routing (CIDR)](https://www.geeksforgeeks.org/computer-networks/classless-inter-domain-routing-cidr/) · [Subnetting](https://www.geeksforgeeks.org/computer-networks/introduction-to-subnetting/) · [Supernetting](https://www.geeksforgeeks.org/computer-networks/supernetting-in-network-layer/) · [Longest Prefix Matching](https://www.geeksforgeeks.org/computer-networks/longest-prefix-matching-in-routers/) · [NAT](https://www.geeksforgeeks.org/computer-networks/network-address-translation-nat/) · [Routing Algorithms Classification](https://www.geeksforgeeks.org/computer-networks/classification-of-routing-algorithms/) · [Distance Vector vs Link State Routing](https://www.geeksforgeeks.org/computer-networks/difference-between-distance-vector-routing-and-link-state-routing/) · [ICMP](https://www.geeksforgeeks.org/computer-networks/internet-control-message-protocol-icmp/) · [OSPF Fundamentals](https://www.geeksforgeeks.org/computer-networks/open-shortest-path-first-ospf-protocol-fundamentals/) · [Border Gateway Protocol (BGP)](https://www.geeksforgeeks.org/computer-networks/border-gateway-protocol-bgp/) *(added per exam history — appeared in the 2007 CS paper, previously uncovered here)* · [Spanning Tree Protocol](https://www.geeksforgeeks.org/computer-networks/types-of-spanning-tree-protocol-stp/) · [RIP](https://www.geeksforgeeks.org/computer-networks/routing-information-protocol-rip/) · [Circuit Switching](https://www.geeksforgeeks.org/computer-networks/circuit-switching-in-computer-network/) · [Packet Switching](https://www.geeksforgeeks.org/computer-networks/packet-switching-and-delays-in-computer-network/) · [Virtual Circuit in Computer Network](https://www.geeksforgeeks.org/computer-networks/virtual-circuit-in-computer-network/) *(GATE CS — explicit "basics of switching: circuit, packet and virtual circuit" syllabus item)* · [Datagram vs Virtual Circuit Switching](https://www.geeksforgeeks.org/computer-networks/difference-between-datagram-switching-virtual-circuit/) · [ARP/RARP](https://www.geeksforgeeks.org/computer-networks/arp-reverse-arprarp-inverse-arp-inarp-proxy-arp-and-gratuitous-arp/) · [Traceroute](https://www.geeksforgeeks.org/computer-networks/traceroute-in-network-layer/)

**Transport Layer**: [Transport Layer Responsibilities](https://www.geeksforgeeks.org/computer-networks/transport-layer-responsibilities/) · [Flow Control in Data Link/Transport Layer](https://www.geeksforgeeks.org/computer-networks/flow-control-in-data-link-layer/) · [Flow Control vs Error Control](https://www.geeksforgeeks.org/difference-between-flow-control-and-error-control/) · [Congestion Control](https://www.geeksforgeeks.org/computer-networks/congestion-control-in-computer-networks/) · [Leaky Bucket Algorithm](https://www.geeksforgeeks.org/computer-networks/leaky-bucket-algorithm/) · [TCP Services & Segment Structure](https://www.geeksforgeeks.org/computer-networks/services-and-segment-structure-in-tcp/) · [TCP Congestion Control](https://www.geeksforgeeks.org/computer-networks/tcp-congestion-control/) · [TCP 3-Way Handshake](https://www.geeksforgeeks.org/computer-networks/tcp-3-way-handshake-process/) · [TCP Connection Establishment/Termination](https://www.geeksforgeeks.org/computer-networks/tcp-connection-establishment/) · [Error Control in TCP](https://www.geeksforgeeks.org/computer-networks/error-control-in-tcp/) · [TCP Flags](https://www.geeksforgeeks.org/computer-networks/tcp-flags/) · [UDP](https://www.geeksforgeeks.org/computer-networks/user-datagram-protocol-udp/) · [TCP vs UDP](https://www.geeksforgeeks.org/computer-networks/differences-between-tcp-and-udp/) · [Multiplexing/Demultiplexing](https://www.geeksforgeeks.org/computer-networks/multiplexing-and-demultiplexing-in-transport-layer/) · [Socket in Computer Network](https://www.geeksforgeeks.org/computer-networks/socket-in-computer-network/) *(GATE CS — explicit "socket API" syllabus item)* · [Socket Programming in C](https://www.geeksforgeeks.org/c/socket-programming-cc/)

**Application Layer**: [Application Layer Protocols](https://www.geeksforgeeks.org/computer-networks/protocols-application-layer/) · [DNS](https://www.geeksforgeeks.org/computer-networks/domain-name-system-dns-in-application-layer/) · [DHCP](https://www.geeksforgeeks.org/computer-networks/dynamic-host-configuration-protocol-dhcp/) · [SNMP](https://www.geeksforgeeks.org/computer-networks/simple-network-management-protocol-snmp/) · [SMTP](https://www.geeksforgeeks.org/computer-networks/simple-mail-transfer-protocol-smtp/) · [FTP](https://www.geeksforgeeks.org/computer-networks/file-transfer-protocol-ftp-in-application-layer/) · [SFTP](https://www.geeksforgeeks.org/computer-networks/sftp-file-transfer-protocol/) · [FTP vs SFTP](https://www.geeksforgeeks.org/computer-networks/difference-between-file-transfer-protocol-ftp-and-secure-file-transfer-protocol-sftp/) · [HTTP Persistent/Non-Persistent](https://www.geeksforgeeks.org/computer-networks/http-non-persistent-persistent-connection/) · [MIME](https://www.geeksforgeeks.org/computer-networks/multipurpose-internet-mail-extension-mime-protocol/) · [Introduction to Data Compression](https://www.geeksforgeeks.org/computer-networks/introduction-to-data-compression/) · [Introduction of Firewall](https://www.geeksforgeeks.org/computer-networks/introduction-of-firewall-in-computer-network/) · [Types of Network Firewall](https://www.geeksforgeeks.org/computer-networks/types-of-network-firewall/) · [Wi-Fi Basics](https://www.geeksforgeeks.org/computer-networks/basics-of-wi-fi/) · [WPS](https://www.geeksforgeeks.org/computer-networks/wifi-protected-setup-wps/) · [WPA](https://www.geeksforgeeks.org/computer-networks/wifi-protected-access-wpa/) · [Network Devices](https://www.geeksforgeeks.org/computer-networks/network-devices-hub-repeater-bridge-switch-router-gateways/) · [GATE PYQs of CN](https://www.geeksforgeeks.org/computer-networks/computer-networks-gate-questions/)

*"Encryption" (syllabus item 8, Application Layer) is covered by the Cyber Security cluster instead — see `gfg-isro-topic-map.md` §11 (Classical Ciphers → RSA/Diffie-Hellman).*

---

# 2. Hands-On Lab Tools — from `gfg-gate-topic-map.md` §15

## 15. Hands-On Networking Lab Tools (practical, non-GFG)

Not study links — official docs/project sites for actually running and observing the §12 Computer
Networks concepts above on a real Linux box, plus the security-tooling side relevant to the Google
track (`career-mapping/gate-vs-google-security-topics.md`).

**OS/kernel-level network config & inspection** *(ties to Socket API, TCP state machine, congestion
control)*: [ip / iproute2](https://man7.org/linux/man-pages/man8/ip.8.html) · [Netplan](https://netplan.io/) · [systemd-networkd](https://www.freedesktop.org/software/systemd/man/systemd-networkd.service.html) · [systemd.socket](https://www.freedesktop.org/software/systemd/man/systemd.socket.html) *(a live, inspectable instance of the "socket API" syllabus item)* · [sysctl](https://man7.org/linux/man-pages/man8/sysctl.8.html) · [ethtool](https://man7.org/linux/man-pages/man8/ethtool.8.html) · [bridge (iproute2)](https://man7.org/linux/man-pages/man8/bridge.8.html) · [NetworkManager / nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html) · [systemd-resolved / resolvectl](https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html)

**Diagnostics & packet inspection**: [ss](https://man7.org/linux/man-pages/man8/ss.8.html) · [iputils (ping, tracepath)](https://github.com/iputils/iputils) · [mtr](https://github.com/traviscross/mtr) · [BIND utilities (dig/nslookup/host)](https://bind9.readthedocs.io/) · [tcpdump](https://www.tcpdump.org/) · [Wireshark / tshark](https://www.wireshark.org/) · [Nmap](https://nmap.org/) · [iftop](http://www.ex-parrot.com/pdw/iftop/) · [nethogs](https://github.com/raboof/nethogs) · [vnstat](https://humdi.net/vnstat/) · [Ncat](https://nmap.org/ncat/) · [socat](http://www.dest-unreach.org/socat/)

**Packet crafting / low-level protocol work** *(ties to TCP flags, segment structure, handshake)*: [Scapy](https://scapy.net/) · [hping3](http://www.hping.org/)

**Firewalls / access control** *(ties to §12 Application Layer Firewall topic)*: [netfilter (iptables/nftables)](https://www.netfilter.org/) · [UFW](https://wiki.ubuntu.com/UncomplicatedFirewall) · [firewalld](https://firewalld.org/) · [fail2ban](https://github.com/fail2ban/fail2ban)

**VPN / tunneling / TLS**: [WireGuard](https://www.wireguard.com/) · [OpenVPN](https://openvpn.net/) · [strongSwan](https://www.strongswan.org/) · [OpenSSL](https://www.openssl.org/)

**Traffic shaping / simulation / throughput testing** *(can reproduce the Sliding Window Protocol
efficiency and bandwidth-delay numericals against a real simulated link)*: [tc + netem](https://wiki.linuxfoundation.org/networking/netem) · [iperf3](https://iperf.fr/) · [Mininet](http://mininet.org/)

**Containers & labs**: [Docker networking](https://docs.docker.com/network/) · [ip netns (network namespaces)](https://man7.org/linux/man-pages/man8/ip-netns.8.html) · *(optional, heavier)* [GNS3](https://www.gns3.com/) · [EVE-NG](https://www.eve-ng.net/)

**Security monitoring (Google security-track relevance)**: [Suricata](https://suricata.io/) · [Zeek](https://zeek.org/)

---

# 3. Deep-Dive Worked Notes — from `subjects/computer-networks.md`

## Computer Networks — Notes

### Data Link Layer

## Hamming Code in Computer Network — Notes

**1. Redundant bits formula**
`2^r ≥ m + r + 1` — minimum number of parity/redundant bits `r` needed for `m` data bits so single-bit errors can be detected *and* corrected.
*e.g. m=7 data bits → try r=4: 2⁴=16 ≥ 7+4+1=12 ✓ (r=3 fails: 2³=8 < 11) → need 4 parity bits, 11-bit codeword.*

**2. Even-parity rule**
Each parity bit is set so the total count of 1's among all positions it covers (itself included) is **even**.

**3. Parity bit coverage (which positions each parity bit checks)**
- `R1` → positions with a 1 in bit-0 of the binary index: 1,3,5,7,9,11,...
- `R2` → positions with a 1 in bit-1: 2,3,6,7,10,11,...
- `R4` → positions with a 1 in bit-2: 4,5,6,7,12–15,...
- `R8` → positions with a 1 in bit-3: 8,9,10,11,...
Parity bits themselves always sit at power-of-2 positions (1,2,4,8,...); everything else is a data bit.

**4. Worked example**
Data = 7 bits → r=4 → 11-bit codeword. Position layout:
```
Pos:  1   2   3   4   5   6   7   8   9   10  11
Bit:  R1  R2  d1  R4  d2  d3  d4  R8  d5  d6  d7
```
Data word: **1001101** (d1=1, d2=0, d3=0, d4=1, d5=1, d6=0, d7=1)

Encoding:
- `R1` checks {1,3,5,7,9,11} → data values at 3,5,7,9,11 = 1,0,1,1,1 (four 1's → even) → `R1 = 0`
- `R2` checks {2,3,6,7,10,11} → data values at 3,6,7,10,11 = 1,0,1,0,1 (three 1's → odd) → `R2 = 1`
- `R4` checks {4,5,6,7} → data values at 5,6,7 = 0,0,1 (one 1 → odd) → `R4 = 1`
- `R8` checks {8,9,10,11} → data values at 9,10,11 = 1,0,1 (two 1's → even) → `R8 = 0`
- Final codeword (pos 1–11): **0 1 1 1 0 0 1 0 1 0 1**

Error detection: bit at position 6 flips 0→1 in transit. Recompute each check bit (1 = mismatch found):
- `c1` (checks 1,3,5,7,9,11) → unaffected → `c1 = 0`
- `c2` (checks 2,3,6,7,10,11) → position 6 is inside this set → now odd → `c2 = 1`
- `c4` (checks 4,5,6,7) → position 6 is inside this set → now odd → `c4 = 1`
- `c8` (checks 8,9,10,11) → unaffected → `c8 = 0`
- Combine as `c8 c4 c2 c1 = 0 1 1 0` = binary **0110** = decimal **6** → error located at bit 6.

**Priority for your prep:** This is the single highest-yield item in the whole set (flagged "Complex" in the priority report) — practice building the position table and the c8c4c2c1 → decimal error-position trick cold; it is asked almost verbatim in GATE/ISRO papers.

---

## Framing in Data Link Layer — Notes

**1. Fixed-size framing**
Frame length is predefined — no start/end delimiters needed, padding handles internal fragmentation.

**2. Variable-size framing**
Needs an explicit boundary marker: a **Length field** (frame carries its own size) or an **End Delimiter (ED)** (a unique bit/byte pattern marks frame end).

**3. Byte/character stuffing**
Used for character-oriented data: an escape character is inserted before any in-data byte that would otherwise be mistaken for the delimiter.

**4. Bit stuffing rule**
ED is a bit pattern (e.g. `01111110` in HDLC/PPP-style framing). Whenever **five consecutive 1's** appear inside the data, a `0` is stuffed in immediately after them, so the receiver never confuses data with the flag pattern. The receiver reverses this by deleting a `0` that follows five consecutive 1's.

Worked example:
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

**5. Worked example**
`Tt = 1 ms`, `Tp = 1.5 ms`. Sender transmits packet 0, then immediately sends packets 1, 2, 3 (sliding window, not waiting). ACK for packet 0 arrives after `2Tp = 3 ms`. Contrast: in plain Stop-and-Wait, only 1 packet is transferred per `Tt + 2Tp = 1 + 2(1.5) = 4 ms` cycle.

**Priority for your prep:** `Efficiency = 1/(1+2a)` and the window-size formula are direct numericals — practice plugging in Tt/Tp/bandwidth values. Go-Back-N vs Selective Repeat window-size derivations are lower-yield background on this page.

---

## Multiple Access Protocols in Computer Network — Notes

**1. ALOHA**: Pure ALOHA and Slotted ALOHA — multiple stations can transmit simultaneously, leading to collisions.

**2. CSMA (Carrier Sense Multiple Access)**: Before transmitting, stations sense the medium — if idle, transmit; if busy, wait. Still vulnerable to collisions due to propagation delay.

**3. CSMA/CD and CSMA/CA**: Collision-Detection and Collision-Avoidance variants of CSMA.

**4. ALOHA efficiency formulas**
`Pure ALOHA max throughput = 1/(2e) ≈ 18.4%`
`Slotted ALOHA max throughput = 1/e ≈ 36.8%`
Reasoning: slotting halves the vulnerable period for collisions vs. pure ALOHA, doubling max efficiency.

**Priority for your prep:** ALOHA/CSMA-CD/CA numeric efficiency (18.4%/36.8%) is must-know exam content.

---

### Transport Layer

## TCP 3-Way Handshake Process — Notes

**1. Step 1 — SYN**: Client sends a segment with SYN set, announcing its starting sequence number.
**2. Step 2 — SYN-ACK**: Server responds with SYN-ACK — ACK for the client's segment, SYN with its own starting sequence number.
**3. Step 3 — ACK**: Client acknowledges the server's response; reliable connection established.

**4. Worked example**
```
Client ISN = 1000, Server ISN = 5000
Step 1: Client → Server   SEQ = 1000, SYN = 1
Step 2: Server → Client   SEQ = 5000, ACK = 1001 (client's SEQ + 1), SYN = 1
Step 3: Client → Server   SEQ = 1001, ACK = 5001 (server's SEQ + 1)
```
General rule: each side's ACK number = other side's (SEQ + 1).

**Priority for your prep:** Know the 3 steps and the "ACK = peer's SEQ + 1" rule cold — that rule is what direct numericals test.

---

## TCP Congestion Control — Notes

**1. Slow start (exponential growth)**: Starts at `cwnd = 1`; doubles every RTT (`cwnd = 2^n` after `n` RTTs) until `cwnd` reaches `ssthresh`.

**2. Congestion avoidance (linear growth)**: Once past `ssthresh`, `+1` segment per RTT.

**3. On timeout (severe congestion)**: `ssthresh = cwnd / 2`, then `cwnd = 1` → restart slow start from scratch.

**4. On 3 duplicate ACKs (fast recovery, milder signal)**: `ssthresh = cwnd / 2`, then `cwnd = ssthresh` → resume directly in congestion avoidance (no full reset).

**5. Worked example**
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

**Priority for your prep:** Flagged "Complex" tier — practice the two growth rules (`2^n` vs `+1`) and especially the two different `ssthresh` reset rules (timeout → cwnd=1 vs 3-dup-ACK → cwnd=ssthresh).

---

## Flow Control in Data Link Layer — Notes

**1. Stop-and-Wait flow control**: Sender transmits one frame at a time, waits for ACK before the next.
**2. Sliding window flow control**: Sender maintains a window of unacknowledged frames, slides it forward as ACKs arrive — continuous/pipelined transmission.

*(Added for practice)*: window size 4, frames numbered 0–7 (3-bit sequence numbers) — sender can have frames 0,1,2,3 outstanding; once ACK for frame 0 arrives, window slides to allow frame 4.

**Priority for your prep:** This page is purely conceptual — the actual numericals live in the Sliding Window Protocol page above; use this only for the definition-level distinction.

---

### Network Layer

## Introduction of Classful IP Addressing — Notes

**1. Classful table**

| Class | Leading bits | Net ID bits | Host ID bits | # Networks | Usable hosts/network | Default mask | Range |
|---|---|---|---|---|---|---|---|
| A | `0` | 8 | 24 | 2⁷=128 | 2²⁴−2=16,777,214 | 255.0.0.0 | 0.0.0.0–127.255.255.255 |
| B | `10` | 16 | 16 | 2¹⁴=16,384 | 2¹⁶−2=65,534 | 255.255.0.0 | 128.0.0.0–191.255.255.255 |
| C | `110` | 24 | 8 | 2²¹=2,097,152 | 2⁸−2=254 | 255.255.255.0 | 192.0.0.0–223.255.255.255 |
| D | `1110` | — | — | — (multicast) | — | — | 224.0.0.0–239.255.255.255 |
| E | `1111` | — | — | — (reserved) | — | — | 240.0.0.0–255.255.255.255 |

**2. Why "−2" for usable hosts**: one address reserved for network (all host bits 0), one for broadcast (all host bits 1) → `2^(host bits) − 2`.

**3. Worked example**: classify `172.16.5.4` — first octet 172 falls in 128–191 → Class B → default mask `255.255.0.0` → network part = `172.16.0.0`, host part = `0.0.5.4`.

**Priority for your prep:** Memorize the class ranges/masks table cold — Class D/E details are lower-yield.

---

## Classless Inter-Domain Routing (CIDR) — Notes

**1. CIDR notation**: `a.b.c.d/n` where `n` = number of leading bits forming the network prefix.

**2. Usable host count formula**: `Usable hosts = 2^(32−n) − 2`

**3. Worked example**: `192.168.1.0/24` → first 24 bits are network, remaining 8 bits are host ID → host bits = 32−24 = 8 → usable hosts = `2^8 − 2 = 254`; subnet mask = `255.255.255.0`.

**4. Block-size rule**: CIDR blocks must be a power of 2 (`2ⁿ`) in size.

**Priority for your prep:** The `2^(32−n)−2` host-count formula plus converting between `/n` and dotted-decimal mask are the direct numericals — practice on several `/n` values (e.g. /24, /26, /28).

---

## Introduction to Subnetting — Notes

**1. Number of subnets**: `Number of subnets = 2^n` where `n` = bits borrowed from the host portion.
**2. Number of usable hosts per subnet**: `Number of hosts = 2^h − 2` where `h` = remaining host bits.

**3. Worked example**
```
Parent network: 193.1.2.0/24, borrow 1 bit → 2 subnets, each /25

Subnet 1: 193.1.2.0   – 193.1.2.127   | Subnet ID 193.1.2.0   | Broadcast 193.1.2.127 | 126 usable hosts | mask 255.255.255.128
Subnet 2: 193.1.2.128 – 193.1.2.255   | Subnet ID 193.1.2.128 | Broadcast 193.1.2.255 | 126 usable hosts | mask 255.255.255.128
```

**Priority for your prep:** This is a direct GATE/ISRO numerical type — given a network + number of required subnets (or hosts), compute new mask, subnet IDs, broadcast addresses, and usable range. Practice the "borrow n bits → 2ⁿ subnets, 2^(8−n)−2 hosts" pattern until it's automatic.

---

## Network Address Translation (NAT) — Notes

**1. Definition**: NAT allows multiple devices in a private network to access the internet using a single public IP address.
**2. Static NAT**: One-to-one mapping between a private and public IP, permanent.
**3. Dynamic NAT**: Maps private IPs to public IPs from a predefined pool, assigned temporarily.
**4. PAT / NAT Overload**: Multiple private IPs share a single public IP using different port numbers — the most commonly deployed type (home routers).

*(Added for practice)*: PAT table entry mapping `192.168.1.5:5000 → 203.0.113.10:61000` and `192.168.1.6:5000 → 203.0.113.10:61001` — same public IP, different translated port distinguishes the two internal hosts.

**Priority for your prep:** Know the 3 types (static/dynamic/PAT) and that PAT is the many-to-one, port-distinguished variant — mostly definitional/MCQ rather than numerical.

---

## Classification of Routing Algorithms — Notes

**1. Adaptive (dynamic) algorithms**: Change routing decisions as topology/traffic changes.
- **Isolated** — each node decides independently.
- **Centralized** — one node holds full network info, makes all decisions.
- **Distributed** — nodes exchange info with neighbors before deciding.

**2. Non-adaptive (static) algorithms**: Routing decisions fixed once selected.
- **Flooding** — every incoming packet sent out on all lines except the one it arrived on.
- **Random walk** — packet sent to a randomly chosen neighboring node.

**3. Hybrid algorithms**: Combine adaptive + non-adaptive by splitting the network into regions.
- **Link-state** — routers build/share full network maps.
- **Distance-vector** — routers keep tables of distance/direction to all destinations, sharing only with neighbors.

*(Added for practice)*: RIP is adaptive, distributed, distance-vector; OSPF is adaptive, distributed, link-state.

**Priority for your prep:** Definitional/classification MCQ topic — know adaptive-vs-non-adaptive and the isolated/centralized/distributed split cold; flooding/random-walk are lower-yield background.

---

# 4. Priority Tier Placement — from `exam-priority-report.md`

### 7. Computer Networks (score 14.0 as shown — not yet recomputed for the corrected sitting count, see below)

Most-hit (post-bug-fix): TCP (still the top genuine keyword, 80 hits), HTTP, DNS, OSPF, subnetting, IP addressing, MAC address, UDP.

**Sitting-count correction note**: `topics/exam-analysis-report.md` now has verified Networks-question counts across the corrected 20-sitting recent era (90 total, vs. 78/17 above) — 2015 turned out to be 3 sessions and 2021 turned out to be 2 sets, not 1 each. The score above (14.0) still reflects the pre-correction 17-sitting count; a recomputed score using the 20-sitting figure is a deferred follow-up. Directionally, more data at a similar per-sitting rate (90/20=4.5 avg vs. 78/17=4.6 avg) suggests the corrected score will land very close to 14.0, not meaningfully different — but treat that as an estimate, not a verified recomputation.

[TCP Services & Segment Structure](https://www.geeksforgeeks.org/computer-networks/services-and-segment-structure-in-tcp/) · [TCP Congestion Control](https://www.geeksforgeeks.org/computer-networks/tcp-congestion-control/) · [TCP 3-Way Handshake](https://www.geeksforgeeks.org/computer-networks/tcp-3-way-handshake-process/) · [Classful IP Addressing](https://www.geeksforgeeks.org/computer-networks/introduction-of-classful-ip-addressing/) · [Subnetting](https://www.geeksforgeeks.org/computer-networks/introduction-to-subnetting/) · [OSPF Fundamentals](https://www.geeksforgeeks.org/computer-networks/open-shortest-path-first-ospf-protocol-fundamentals/) · [DNS](https://www.geeksforgeeks.org/computer-networks/domain-name-system-dns-in-application-layer/) · [MAC Address](https://www.geeksforgeeks.org/computer-networks/mac-address-in-computer-network/)

---

# 5. Full Question-History Analysis — from `topics/networking-question-analysis.md`

## GATE Computer Networks — Full Question-History Analysis (CS 2007–2026, DA 2024–2026)

Dedicated deep-dive on networking questions specifically, built from every previous-year paper currently on disk — **27 real CS sittings** (2007–2026; several years turned out to bundle more than one official paper per PDF) and all 3 DA sittings that have ever existed (2024–2026). This is a companion to, not a replacement for, `exam-priority-report.md`'s Computer Networks section (above) — that section uses primary-topic-per-question classification for apples-to-apples scoring against the other 11 CS subjects; this file uses a broader "any networking mention" lexicon built specifically to surface every networking-adjacent question, including secondary references. Expect this file's counts to run higher than the priority report's for the same years — that's by design, not an error.

**Sitting-count correction**: the original "24 CS sittings" framing undercounted the real paper count by 3. Two files turned out to bundle multiple official sittings into one PDF: **2015 is three full sessions** (Session-1/2/3, 65 questions each, each with its own answer-key table), not one paper, and **2021 is two full sets** (Set-1, Set-2), each with its own answer key. The true count is 27 (2007–2014 singly = 8, 2015 ×3, 2016 singly = 1, 2017 ×2, 2018 singly = 1, 2019 singly = 1, 2020 singly = 1, 2021 ×2, 2022 singly = 1, 2023 singly = 1, 2024 ×2, 2025 ×2, 2026 ×2 = 27).

## Combined per-sitting count, all 27 CS + 3 DA sittings

| Year | Shift | Networking Qs | Confidence | Extraction method |
|---|---|---|---|---|
| 2007 | — | 6 | high | OCR |
| 2008 | — | 3 | high | OCR |
| 2009 | — | 2 | high | OCR |
| 2010 | — | 3 | high | OCR |
| 2011 | — | 3 | high | OCR |
| 2012 | — | 9 | high | pdftotext |
| 2013 | — | 7 | high | pdftotext *(source PDF had the paper repeated ~4×; deduplicated)* |
| 2014 | — | 7 | high | pdftotext |
| 2015 | Session-1 | 5 | high | direct PDF read |
| 2015 | Session-2 | 6 | high | direct PDF read |
| 2015 | Session-3 | 6 | high | direct PDF read |
| 2016 | — | 6 | high | pdftotext |
| 2017 | CS1 | 3 | high | direct PDF read |
| 2017 | CS2 | 5 | high | direct PDF read |
| 2018 | — | 5 | high | pdftotext |
| 2019 | — | 4 | high | direct PDF read |
| 2020 | — | 4 | high | direct PDF read |
| 2021 | Set-1 | 4 | high | direct PDF read |
| 2021 | Set-2 | 4 | high | direct PDF read |
| 2022 | — | 6 | high | pdftotext |
| 2023 | — | 5 | high | pdftotext |
| 2024 | CS1 | 5 | high | pdftotext |
| 2024 | CS2 | 7 | high | pdftotext |
| 2025 | CS1 | 5 | high | pdftotext |
| 2025 | CS2 | 5 | high | pdftotext |
| 2026 | CS1 | 5 | high | pdftotext |
| 2026 | CS2 | 4 | high | pdftotext |
| **2024** | DA | **0** | high | pdftotext *(only "network" hits are ML terms — Bayesian/Neural Network — not real networking)* |
| **2025** | DA | **0** | high | pdftotext |
| **2026** | DA | **0** | high | pdftotext |

**CS total: 134 networking questions across 27 sittings, every sitting now high-confidence.** No estimates remain — every year that originally needed OCR-based density estimation was re-verified via direct page-by-page PDF reading, which also corrected the sitting count upward. **DA total: 0 across all 3 sittings that have ever existed** — expected, DA's syllabus has no Computer Networks section at all.

## Most-hit sub-clusters (CS, across all years with reliable per-question data)

**Transport Layer dominates**, consistently: TCP/TCP-segment-structure questions (header fields, port numbers, segment-size numericals) recur in almost every single year 2007–2026 — the single most-tested networking sub-cluster across the entire 20-year history, not just recent years.

Behind that: **Network Layer routing** (distance-vector vs. link-state, every other year roughly), **IP addressing/subnetting/CIDR numericals**, and **Data Link Layer ARQ/sliding-window numericals** (clustered in specific years — 2009, 2014 — rather than every year). Ethernet and HTTP show up with real but lower frequency.

## Topic-map gap found (now resolved)

**BGP** (2007 Q70) didn't map to any current sub-cluster in `gfg-gate-topic-map.md` §12's Network Layer list when this analysis was first built — a link has since been added (see Section 1 above). It appeared exactly once, in the oldest paper on file, never recurring since (including all of 2014–2026) — low prep priority despite now having a link.

*(Token ring — 2007 Q68, 2014 Q55 — also flagged but is obsolete syllabus content GATE stopped testing; not a real gap.)*

## Limitations (read before trusting the numbers above)

1. **(Resolved)** Originally, 13 of the then-assumed 24 sittings needed OCR and several only produced density-based estimates. A follow-up pass re-extracted all of these via direct, page-by-page PDF reading instead — every sitting above is now high-confidence. 2020 was the most deceptive of the original OCR failures: `pdftotext` returned plausible-looking output that was actually just question numbers and option labels, with the real question content rasterized as images.
2. **The two forks' lexicons differ slightly in strictness** — spot-checked against source text but not cross-validated against each other question-by-question.
3. **Automated keyword classification, not question-by-question human reading** — a keyword hit could occasionally land on a distractor answer choice rather than the question's actual subject.
4. **Old-syllabus drift**: GATE CS's Computer Networks content has narrowed since 2007 (BGP, token ring are the clearest examples).
5. This file's "any mention" lexicon is deliberately broader than `exam-priority-report.md`'s primary-topic-per-question classification — the two files' numbers for the same years will not match, and that's expected.
6. **Minor question-number uncertainty for 2019/2020**: unlike 2015/2017/2021, the 2019/2020 pass wasn't cross-checked against every printed `Q.<N>` label — question numbers carry a small (±1) risk of being off, though topics found and total counts are solid.

---

# 6. Books on Disk + Google Job-Market Findings — from `career-mapping/gate-vs-google-security-topics.md` §1.1

### 1. Computer networks and network security

- **GATE:** Computer Networks - Tier 2, score 14.8 (pre-correction figure at time of writing; see Section 4 above for the current number)
- **Google roles:** 56 of 169 roles mention networking/protocols/network security; 40 as a MINIMUM (mostly the standard bullet 'experience with security engineering, computer and network security and security protocols'). Literal 'TCP/IP', 'DNS', 'TLS' appear in 0 descriptions.
- **Books from the reading list:** Attacking Network Protocols — Hacker's Guide to Capture, Analysis, Exploitation (7/10); Nmap Network Exploration and Security Auditing Cookbook, 2nd Ed (7/10); Applied Network Security Monitoring (8/10); Network Security Through Data Analysis, 2nd Ed (7/10); Cisco Press — Penetration Testing and Network Defense (7/10); Network Layer — Forouzan (slides) (5/10); Wireshark Top Filters (quick ref) (7/10); SILENCE ON THE WIRE — Passive Reconnaissance and Indirect Attacks (6/10)
- **Other PDFs on disk:** Tanenbaum - Computer Networks; CCNA 200-301 Official Cert Guide Vol 1 (Cisco Press); CCNA 200-301 Vol 2
- **Note:** Covers GATE's layered model (Tanenbaum, CCNA) plus the attacker/defender view. No Kurose & Ross on disk.

**Paths (from the reading-list appendix, corrected prefix `../hardisk/...`):**

| Book | Path |
|---|---|
| Attacking Network Protocols | `.../hdd/disk/course/WEEK-23/Security_Study_Material/Attacking Network Protocols A Hacker's Guide to Capture, Analysis, and Exploitation.pdf` |
| Nmap Network Exploration and Security Auditing Cookbook, 2nd Ed | `.../WEEK-23/Security_Study_Material/Nmap Network Exploration and Security Auditing Cookbook - Second Edition.pdf` |
| Applied Network Security Monitoring | `.../WEEK-23/Security_Study_Material/Applied Network Security Monitoring.pdf` |
| Network Security Through Data Analysis, 2nd Ed | `.../WEEK-23/Security_Study_Material/Network Security Through Data Analysis, 2nd Edition.pdf` |
| Cisco Press — Penetration Testing and Network Defense | `.../WEEK-23/Security_Study_Material/Cisco Press - Penetration Testing and Network Defense.pdf` |
| Network Layer — Forouzan (slides) | `.../WEEK-14/Dr. Nitin kumar/Network-Layer-Forouzan.pdf` |
| Wireshark Top Filters | `.../WEEK-4/Wireshark Top Filters.pdf` |
| SILENCE ON THE WIRE | `.../WEEK-23/Security_Study_Material/SILENCE ON THE WIRE A Field Guide to Passive Reconnaissance and Indirect Attacks.pdf` |
| Tanenbaum - Computer Networks | `.../hdd/old_files/books/Andrew S. Tanenbaum - Computer Networks.pdf` |
| CCNA 200-301 Official Cert Guide Vol 1 | `.../hdd/old_files/books/12381imguf_CiscoPress-CCNA-200-301-Official-Cert-Guide-Volume-1.pdf` |
| CCNA 200-301 Vol 2 | `.../hdd/old_files/books/ccna-200-301-vol.-2.pdf` |
