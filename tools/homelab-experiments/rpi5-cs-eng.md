# Raspberry Pi 5 — Computer Science Engineering

**Machine**: Raspberry Pi 5 Model B (BCM2712, 4-core @ 2.4GHz, 8GB RAM, Debian trixie, ARM64, small SD storage)
**Field**: Computer Science Engineering (top priority)
**Character**: low-power, always-on, embedded-native — the natural continuation of the ble-monitor-public lineage (Debian packaging, protocol-level work), but scoped to fresh topics rather than extending that project.

Every idea below is inspired by `../../tracks/isro/topics/gfg-isro-topic-map.md` and `../../tracks/gate/topics/gfg-gate-topic-map.md`. Each carries exactly one reference link (GFG article, a starred GitHub repo, or a link already present in those two files). Ideas are meant to run as dev → deploy (days to 1-2 weeks) → analyze cycles, not one-shot scripts.

Some categories here are the **lightest tier** of a topic that also appears in `probook-cybersec.md` and/or `proone-dsai.md` at heavier compute tiers (noted inline where relevant).

---

## Mathematics (Discrete Math foundations)

- **Graph Algorithms Visualizer & Analyzer** — build BFS/DFS/Dijkstra/Bellman-Ford from scratch, deploy as a long-running service ingesting random graph batches for a week, analyze runtime scaling vs theoretical complexity. Ref: [Graph Algorithms Notes for GATE](https://www.geeksforgeeks.org/dsa/graph-based-algorithms-for-gate-exam/)
- **Combinatorics-Driven Keyspace/Entropy Calculator** — compute password-policy keyspace size and entropy using permutations/combinations, deploy as a small CLI/API, log usage over time. Ref: [Combinatorics Basics](https://www.geeksforgeeks.org/engineering-mathematics/mathematics-combinatorics-basics/)
- **Hasse Diagram / Lattice Renderer** — parse a partial-order relation, build the lattice/Hasse diagram from scratch with your own graph-layout code. Ref: [Partial Orders and Lattices](https://www.geeksforgeeks.org/engineering-mathematics/partial-orders-lattices/)

## Calculus (Numerical Methods) *(previously skipped — reframed as buildable numerical-computing tools)*

- **Numerical Integrator/Differentiator Library (Simpson's/trapezoidal rule, finite differences)** — implement from scratch, validate against SciPy, deploy as a small math-service API. Ref: [Indefinite Integrals](https://www.geeksforgeeks.org/maths/indefinite-integrals/)
- **Newton-Raphson Root Finder + Derivative-Based Optimization Demo** — implement root-finding and simple gradient-based optimization on functions you define, log convergence behavior across function shapes. Ref: [Application of Derivatives](https://www.geeksforgeeks.org/maths/application-of-derivatives/)
- **Taylor/Maclaurin Series Function Approximator** — build a tool that approximates arbitrary functions via truncated series expansions, deploy comparing approximation error vs term count over a batch of test functions. Ref: [Taylor's Theorem/Series](https://www.geeksforgeeks.org/engineering-mathematics/taylor-series/)

## Computer Organization & Architecture

- **Mini CPU Simulator (your own small RISC ISA)** — design an instruction set, build fetch-decode-execute + pipelining with hazards, run compiled toy programs, analyze CPI/throughput under different hazard strategies. Ref: [Pipelining Set 1](https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-and-architecture-pipelining-set-1-execution-stages-and-throughput/)
- **Cache Simulator & Hit-Rate Analyzer** — implement direct-mapped/set-associative cache simulation over memory-access traces generated from real programs, log hit rates across workloads for a week. Ref: [Cache Organization](https://www.geeksforgeeks.org/computer-organization-architecture/cache-organization-set-1-introduction/)
- **Booth's Algorithm & Restoring-Division Emulator** — implement both as if simulating a real ALU datapath, verify against native integer division. Ref: [Booth's Algorithm](https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-booths-algorithm/)
- **Boolean Expression Minimizer (K-Map / Quine-McCluskey Solver)** — take an arbitrary truth table, auto-generate the minimized SOP/POS expression, verify against hand-solved K-maps. Ref: [Quine-McCluskey Method](https://www.geeksforgeeks.org/digital-logic/quine-mccluskey-method/)
- **Sequential Circuit Simulator (Flip-Flops, Counters, Shift Registers)** — implement SR/JK/D/T flip-flop behavior and ripple/ring/Johnson counters purely in software, drive them with a clock-tick loop, log state transitions. Ref: [Flip-Flop Types, Conversion and Applications](https://www.geeksforgeeks.org/digital-logic/flip-flop-types-their-conversion-and-applications/)
- **Interrupt/DMA-Driven I/O Simulator** — model interrupt-driven vs DMA-driven I/O transfer for a synthetic device, compare CPU-cycles-spent-on-I/O under each mode. Ref: [I/O Interface — Interrupt & DMA Mode](https://www.geeksforgeeks.org/computer-organization-architecture/io-interface-interrupt-dma-mode/)

## Programming Languages / Compiler Design

- **Toy Language Interpreter (build-your-own-x style)** — design a small grammar, hand-write lexer/parser/tree-walking interpreter, deploy as a REPL running for a week, analyze which language features you actually needed. Ref: [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)
- **Recursive-Descent Parser + FIRST/FOLLOW Set Generator** — given any CFG, auto-compute FIRST/FOLLOW sets and generate a working parser from them. Ref: [FIRST Set in Syntax Analysis](https://www.geeksforgeeks.org/compiler-design/first-set-in-syntax-analysis/)
- **Static vs Dynamic Scope Demonstrator** — implement both resolution strategies in a mini interpreter, show divergent behavior on the same program. Ref: [Static and Dynamic Scoping](https://www.geeksforgeeks.org/dsa/static-and-dynamic-scoping/)
- **Three-Address-Code Generator + Basic Optimizer** — lower a toy-language AST to TAC, implement constant folding/dead-code elimination, measure instruction-count reduction. Ref: [Three Address Code](https://www.geeksforgeeks.org/compiler-design/three-address-code-compiler/)
- **SLR/LALR Parser Table Generator** — build the parsing-table construction algorithm for your toy grammar, feed it real (and deliberately ambiguous) grammars, log conflicts detected. Ref: [SLR/CLR/LALR Parsers](https://www.geeksforgeeks.org/compiler-design/slr-clr-and-lalr-parsers-set-3/)
- **Runtime Environment Simulator (stack/heap allocation, parameter-passing modes)** — model activation records for your toy language, implement call-by-value/reference/copy-restore/name, compare resulting semantics on the same test program. Ref: [Runtime Environments in Compiler Design](https://www.geeksforgeeks.org/compiler-design/runtime-environments-in-compiler-design/)
- **Data-Flow Optimization Pass Suite** — implement constant propagation, common-subexpression elimination, and dead-code elimination as composable passes over your TAC, measure instruction-count reduction pass-by-pass. Ref: [Data Flow Analysis in Compiler Design](https://www.geeksforgeeks.org/compiler-design/data-flow-analysis-compiler/)

## Data Structures & Algorithms *(Tier 1 — simplest; heavier tiers in `probook-cybersec.md`)*

- **Self-Balancing Tree Library from Scratch (AVL/B-Tree)** — implement, benchmark insert/delete/search against Python's built-ins, deploy as the indexing backend for one of your other projects. Ref: [Trees Notes for GATE](https://www.geeksforgeeks.org/dsa/trees-notes-for-gate-exam/)
- **External Merge Sort for Files Larger Than RAM** — build+test external sorting on synthetic multi-GB datasets against the Pi's 8GB RAM ceiling, measure I/O-bound behavior over the SD card. Ref: [Divide & Conquer Notes for GATE](https://www.geeksforgeeks.org/dsa/divide-and-conquer-notes-for-gate-exam/)
- **Huffman Coding Compressor from Scratch** — implement the greedy tree-building algorithm, build a working file compressor/decompressor, benchmark compression ratio against gzip on real files. Ref: [Huffman Coding for Sorted Input](https://www.geeksforgeeks.org/dsa/efficient-huffman-coding-for-sorted-input-greedy-algo-4/)
- **Fractional vs 0-1 Knapsack Solver (Greedy vs DP Comparison)** — implement both, generate item sets where greedy fails on the 0-1 variant, deploy a small benchmark harness logging optimal-vs-greedy gaps. Ref: [Fractional Knapsack Problem](https://www.geeksforgeeks.org/dsa/fractional-knapsack-problem/)
- **Minimum Spanning Tree Builder (Prim's vs Kruskal's) with Visualization** — implement both, run on the same weighted graphs, compare runtime/behavior on dense vs sparse graphs. Ref: [Prim's Minimum Spanning Tree](https://www.geeksforgeeks.org/dsa/prims-minimum-spanning-tree-mst-greedy-algo-5/)
- **LCS & Matrix Chain Multiplication DP Solver** — implement both classic DP formulations from scratch, trace back optimal solutions, benchmark against brute-force recursion to show the speedup. Ref: [Dynamic Programming Notes for GATE](https://www.geeksforgeeks.org/dsa/dynamic-programming-notes-for-gate-exam/)
- **Double Hashing / Quadratic Probing Hash Table from Scratch** — implement both open-addressing schemes, deploy as the backend for a small key-value tool, measure clustering/probe-length under different load factors. Ref: [Double Hashing](https://www.geeksforgeeks.org/dsa/double-hashing/)

## Theory of Computation

- **Regex Engine from Scratch (Thompson's construction + subset construction)** — implement NFA→DFA conversion, deploy as a CLI regex tool, test against real text corpora. Ref: [NFA to DFA Conversion](https://www.geeksforgeeks.org/theory-of-computation/conversion-from-nfa-to-dfa/)
- **Turing Machine Simulator + Halting-Heuristic Tester** — build a generic TM simulator, run classic constructions (addition, palindrome check), explore where naive halting-detection heuristics fail. Ref: [Introduction to Turing Machine](https://www.geeksforgeeks.org/theory-of-computation/turing-machine-in-toc/)
- **Pushdown Automaton Syntax Checker** — build a PDA validating balanced expressions / a simple grammar. Ref: [Introduction to Pushdown Automata](https://www.geeksforgeeks.org/theory-of-computation/introduction-of-pushdown-automata/)

## Operating Systems

- **Deadlock Simulator (Banker's Algorithm + Detection/Recovery)** — model resource-allocation graphs for real background services, run Banker's algorithm as a monitor daemon over the Pi's own process/resource usage for a week. Ref: [Banker's Algorithm](https://www.geeksforgeeks.org/operating-systems/bankers-algorithm-in-operating-system-2/)
- **CPU Scheduler Playground on Real Workloads (FCFS/SJF/RR/Priority)** — build a userspace scheduler simulator fed by real process traces captured from `/proc`, compare turnaround/waiting time across policies. Ref: [CPU Scheduling](https://www.geeksforgeeks.org/operating-systems/cpu-scheduling-in-operating-systems/)
- **Custom Toy Filesystem via FUSE** — design an inode-based filesystem, mount it for a week storing real files, analyze fragmentation/performance vs ext4. Ref: [File Systems in OS](https://www.geeksforgeeks.org/operating-systems/file-systems-in-operating-system/)
- **Page Replacement Algorithm Comparator (LRU/FIFO/Optimal)** — simulate against real memory-access traces from a running app, log hit/miss rates over a week of varied workloads. Ref: [Page Replacement Algorithms](https://www.geeksforgeeks.org/operating-systems/page-replacement-algorithms-in-operating-systems/)
- **Producer-Consumer Simulator (Semaphores)** — implement the bounded-buffer problem with real concurrent processes/threads, deploy running continuously for a week, log throughput and any race conditions surfaced. Ref: [Producer-Consumer Problem Using Semaphores](https://www.geeksforgeeks.org/operating-systems/producer-consumer-problem-using-semaphores-set-1/)
- **Dining Philosophers Deadlock-Free Simulator** — implement multiple solutions (resource hierarchy, arbitrator), deploy running for a week with randomized think/eat timing, verify no deadlock/starvation occurs. Ref: [Dining Philosophers Problem](https://www.geeksforgeeks.org/operating-systems/dining-philosophers-problem/)
- **Readers-Writers Problem (Both Preference Variants)** — implement reader-preference and writer-preference solutions, deploy against a shared resource under real concurrent load, measure fairness/starvation differences. Ref: [Readers-Writers Problem](https://www.geeksforgeeks.org/operating-systems/readers-writers-problem-set-1-introduction-and-readers-preference-solution/)
- **Monitor-Based Synchronization Demo** — reimplement one of the above (producer-consumer or readers-writers) using monitors instead of raw semaphores, compare code clarity and correctness guarantees. Ref: [Monitors in Process Synchronization](https://www.geeksforgeeks.org/operating-systems/monitors-in-process-synchronization/)

## Databases *(Tier 1 — simplest; Tier 2 in `probook-cybersec.md`, Tier 3 in `proone-dsai.md`)*

- **Minimal Key-Value Store with Write-Ahead Log** — build from scratch (mini Redis/Bitcask style), deploy backing a small real workload (your own notes/metrics), analyze durability after simulated crashes. Ref: [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)
- **B+ Tree Index Engine for a Toy Table Format** — implement an on-disk B+ tree, benchmark point/range queries against SQLite on the same dataset. Ref: [B+ Tree](https://www.geeksforgeeks.org/dbms/introduction-of-b-tree/)
- **Normalization Checker Tool** — given a relation + functional dependencies, auto-detect current normal form and suggest a decomposition. Ref: [How to Find the Highest Normal Form](https://www.geeksforgeeks.org/dbms/how-to-find-the-highest-normal-form-of-a-relation/)

## Computer Networks

- **Mini Reliable-Transport Protocol Over Raw UDP** — implement your own sliding-window + ARQ on top of UDP sockets between your own machines only, deploy for a week measuring throughput/loss recovery on real home-network conditions. Ref: [Sliding Window Protocol Set 1](https://www.geeksforgeeks.org/computer-networks/sliding-window-protocol-set-1/)
- **Distance-Vector Routing Simulator on a Virtual Topology** — build a small simulated network of nodes (processes) exchanging routing tables, converge and analyze count-to-infinity behavior. Ref: [Distance Vector vs Link State Routing](https://www.geeksforgeeks.org/computer-networks/difference-between-distance-vector-routing-and-link-state-routing/)
- **DNS Resolver Built from Scratch** — implement recursive resolution by hand (root → TLD → authoritative), run it as your own local resolver for a week, log resolution times vs the system resolver. Ref: [DNS](https://www.geeksforgeeks.org/computer-networks/domain-name-system-dns-in-application-layer/)
- **Hamming Code Error Detection/Correction Tool** — implement encode/decode over your own generated bitstreams, inject random bit-flip errors, measure correction success rate vs error rate. Ref: [Hamming Code in Computer Network](https://www.geeksforgeeks.org/computer-networks/hamming-code-in-computer-network/)
- **CSMA/CD Collision Simulator** — simulate multiple senders on a shared virtual medium with the back-off algorithm, log collision rate and effective throughput as sender count scales. Ref: [Back-off Algorithm for CSMA/CD](https://www.geeksforgeeks.org/computer-networks/back-off-algorithm-csmacd/)
- **Leaky Bucket / TCP Congestion Control Simulator** — implement leaky-bucket traffic shaping and a simplified TCP congestion-window (slow start/congestion avoidance) simulator, deploy over synthetic bursty traffic for a week, plot window-size behavior. Ref: [TCP Congestion Control](https://www.geeksforgeeks.org/computer-networks/tcp-congestion-control/)

## Embedded / IoT / Hardware *(previously missed — the Pi is a physical device, this is where that should live)*

- **ESP32 Sensor Telemetry Bridge (Pi5 as Gateway/Aggregator)** — flash an ESP32 with sensor-reading firmware, have the Pi aggregate/log telemetry over serial or Wi-Fi for a week, analyze sensor drift/packet loss. Ref: [nkolban/esp32-snippets](https://github.com/nkolban/esp32-snippets)
- **LoRa Long-Range Sensor Network Gateway** — set up the Pi as a LoRa gateway receiving from one or more low-power nodes, deploy collecting readings over a week, analyze range/reliability vs transmit power. Ref: [CongducPham/LowCostLoRaGw](https://github.com/CongducPham/LowCostLoRaGw)
- **GPIO-Driven Real-Time Environmental Logger** — wire up a temperature/humidity/motion sensor directly to the Pi's GPIO, deploy a week-long continuous logging service, analyze daily/weekly patterns in the collected data. Ref: [nkolban/esp32-snippets](https://github.com/nkolban/esp32-snippets)

## General Aptitude (as Computational Problems) *(previously excluded — reframed as algorithmic solvers rather than exam drills)*

- **Automated Paper-Folding/Rotation/Mirroring Solver** — implement the geometric transformations these puzzles rely on as actual code (matrix rotations, reflections, fold-simulation), verify against known puzzle answers. Ref: [Rotation of Shapes](https://www.geeksforgeeks.org/aptitude/rotation-of-shapes/)
- **Number/Alphanumeric Series Predictor** — build a pattern-detection algorithm (difference sequences, ratio sequences) that predicts the next term in arbitrary series, test it against a large generated puzzle set. Ref: [Number Series in Quantitative Aptitude](https://www.geeksforgeeks.org/aptitude/number-series-in-quantitative-aptitude/)
- **Syllogism Logic Solver (Propositional Inference Engine)** — build a small inference engine that evaluates syllogism validity using rules of inference, test it against a bank of syllogism puzzles. Ref: [Rules of Inference](https://www.geeksforgeeks.org/engineering-mathematics/rules-of-inference/)
