# Computer Organization and Architecture (CAO / COA) — GATE 2027 (CS + DA)

**2027 syllabus change (CS):** COA was restructured moderately. Per several secondary summaries comparing the 2026 and 2027 PDFs (GATENotes, ThemlHub, ProSyllabus, IAE Academy):
- Newly explicit: design of the ALU, hardwired and microprogrammed control units, memory interfacing and memory performance, cache memory mapping.
- "Main memory and secondary storage" is no longer listed as a separate item. The Operating System section still lists file systems and I/O scheduling.
- Unchanged in spirit: machine instructions and addressing modes, instruction pipelining and hazards, I/O interface (interrupt and DMA).
The sources differ slightly in wording, and I could not open the official PDF directly. Check the COA block in it once, and treat "secondary storage" as optional until you do.
**Hbk** column: the Handbook's "Switching Theory and Computer Architecture" chapter is pp. 353–404, shared with Digital Logic. Per-topic pages are not mapped. Marked `353–404*`.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
This is one of your weak subjects, so the file is a bit more detailed than the Databases one.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Instruction formats, expanding opcodes, RISC vs CISC | 353–404* | [COA short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251006151446572894/COA-SHORT-NOTES-_compressed_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Addressing modes | 353–404* | [LMN Computer Organization](https://www.geeksforgeeks.org/computer-organization-architecture/last-minute-notes-computer-organization/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Computer arithmetic: complements, overflow, Booth's algorithm | 353–404* | [COA for GATE](https://www.geeksforgeeks.org/computer-organization-architecture/computer-organization-and-architecture-coa-for-gate/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | ALU and data path design **new wording** | 353–404* | [Data path components](https://www.geeksforgeeks.org/computer-organization-architecture/differences-between-data-paths/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Control unit: hardwired vs microprogrammed (horizontal / vertical) **new wording** | 353–404* | [Control signals](https://www.geeksforgeeks.org/computer-organization-architecture/control-signal-types-and-role-1/) · [Control path](https://www.geeksforgeeks.org/computer-organization-architecture/control-path/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Instruction pipelining, speedup, throughput | 353–404* | [Basics of pipelining](https://www.geeksforgeeks.org/computer-organization-architecture/basics-of-pipelining/) · [Pipelining Set 1](https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-1-execution-stages-and-throughput/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Pipeline hazards (structural, data, control), forwarding, stalls | 353–404* | [Pipelining Set 2](https://www.geeksforgeeks.org/computer-organization-and-architecture-pipelining-set-2-dependencies-and-data-hazard/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Memory hierarchy, memory performance (AMAT, hit ratio) **new wording** | 353–404* | [LMN Computer Organization](https://www.geeksforgeeks.org/computer-organization-architecture/last-minute-notes-computer-organization/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Cache: direct, set-associative, fully associative mapping, replacement, misses | 353–404* | [GFG COA syllabus PDF (cache topics)](https://media.geeksforgeeks.org/courses/syllabus/2d4203f33ca93678d87faf3962765b84.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Memory interfacing (chips, address decoding) **new wording** | 353–404* | [COA short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251006151446572894/COA-SHORT-NOTES-_compressed_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | I/O interface: programmed I/O, interrupts, DMA | 353–404* | [I/O interface (interrupt and DMA)](https://www.geeksforgeeks.org/computer-organization-architecture/io-interface-interrupt-dma-mode/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | Disk and secondary storage (**optional**, see note above) | 353–404* | [GFG COA syllabus PDF (disk topics)](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20230302142337/GATE-PDF-1.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [GFG COA syllabus PDF (cache, addressing)](https://media.geeksforgeeks.org/courses/syllabus/2d4203f33ca93678d87faf3962765b84.pdf).

**My links:** (NPTEL / textbook, add here)

---

## 1. Instruction formats
- Fields: opcode, address/register fields, mode field. Instruction length = opcode + operand fields.
- Expanding opcode: leftover opcode patterns are reused as longer-opcode codes. With 16-bit instructions, a 4-bit opcode and 6-bit address fields, if 14 of 16 opcodes are two-address, the 2 spare patterns × 2⁶ give 128 one-address slots. Using 31 of those leaves (128 − 31) × 2⁶ = 6208 zero-address slots.
- RISC: load/store architecture, fixed-length instructions, many registers, simple addressing. CISC: variable length, memory operands, complex instructions.

## 2. Addressing modes
| Mode | Operand location / effective address |
|---|---|
| Immediate | in the instruction |
| Register | in a register |
| Direct | EA = address field |
| Indirect | EA = M[address field] |
| Register indirect | EA = content of register |
| Indexed / base register | EA = register + displacement |
| PC-relative | EA = PC + offset |
| Auto-increment / decrement | register used then updated (or updated first) |
- Your older notes cover 8086 modes. GATE asks generic modes, so focus on this table, not 8086 specifics.

## 3. Computer arithmetic
- Booth's algorithm (radix-2) examines (Q₀, Q₋₁): 10 → subtract multiplicand; 01 → add multiplicand; 00 or 11 → shift only; then arithmetic shift right. It handles signed multiplication in two's complement.
- Overflow rule and IEEE 754 are in the Digital Logic file.

## 4–5. ALU, data path, control unit
- Data path: registers, ALU, buses, multiplexers. Single-bus designs need extra temporary registers.
- Instruction cycle: fetch, decode, execute (plus memory / write-back stages in pipelines).
- Hardwired control: fixed logic, faster, hard to change. Microprogrammed: control store of microinstructions, flexible, slower.
- Horizontal microinstructions: one bit per control signal, wide, highly parallel, no decoding. Vertical: encoded fields, narrow, needs decoders, slower.
- Control memory size = number of microinstructions × microinstruction width.

## 6–7. Pipelining
- k stages, n instructions, clock Tp: pipelined time = (k + n − 1)·Tp. Non-pipelined: n·k·Tp. Speedup = nk/(k + n − 1) → k as n → ∞. Efficiency = speedup/k. Throughput = n/((k + n − 1)Tp).
- Clock period is set by the slowest stage plus latch delay.
- CPI with stalls = 1 + (stall cycles per instruction). Branch penalty example: CPI = 1 + (branch fraction) × (penalty cycles).
- Hazards: structural (resource conflict), data (RAW true dependency, WAR and WAW name dependencies), control (branches). Forwarding fixes most RAW hazards except load-use (still one stall).
- Amdahl's law: overall speedup = 1/((1 − f) + f/s).

## 8–10. Memory
- Average memory access time: AMAT = hit time + miss rate × miss penalty. Two-level: AMAT = T_L1 + m₁(T_L2 + m₂·T_mem).
- Address split for cache: offset = log₂(block size), index = log₂(number of sets), tag = address bits − index − offset. Lines = cache size / block size. Sets = lines / associativity. Direct-mapped: sets = lines. Fully associative: 1 set, no index.
- Miss types: compulsory (first access), capacity (cache too small), conflict (mapping collision). Replacement: LRU, FIFO, random.
- Write policies: write-through vs write-back (dirty bit); write-allocate vs no-write-allocate.
- Memory interfacing: chips needed = (total words / chip words) × (word width / chip width). The high address bits drive a decoder that selects a bank.
- Byte-addressable memory with a 32-bit address covers 2³² bytes = 4 GB.

## 11. I/O
- Programmed I/O: CPU polls. Interrupt-driven: device signals, CPU runs a handler. DMA: controller moves a block directly; CPU gives up the bus (burst mode or cycle stealing).
- Cycle stealing fraction = (words per second) × (memory cycle time).
- Isolated vs memory-mapped I/O: memory-mapped uses ordinary load/store and consumes address space.

## 12. Disk (optional)
- Access time = seek + rotational latency + transfer. Average rotational latency = half a rotation = 30000/rpm ms.

---

## Worked examples (all recomputed in code)

**E1: expanding opcode.** 16-bit instruction, 4-bit opcode, 6-bit addresses. 14 two-address opcodes leave 2 patterns, giving 2 × 64 = **128** one-address slots. Using 31 of them leaves (128 − 31) × 64 = **6208** zero-address slots.

**E2: instruction width.** 32-bit instruction, 8-bit opcode, three register operands from 64 registers (6 bits each) uses 8 + 18 = 26 bits, leaving **6** bits for an immediate.

**E3: Booth.** −3 × 5 = **−15**. 7 × (−6) = **−42**. 6 × 7 = **42**.

**E4: cache address split.** 32-bit address, direct-mapped, 1024 lines of 32 B: offset **5**, index **10**, tag **17**. For a 64 KB, 4-way cache with 64 B blocks: 1024 lines, 256 sets, offset **6**, index **8**, tag **18**. Fully associative (same size): no index, tag **26**.

**E5: AMAT.** Hit 1 ns, miss rate 5%, penalty 100 ns: AMAT = 1 + 0.05 × 100 = **6 ns**. Two-level: L1 1 ns, L1 miss 10%, L2 10 ns, L2 miss 20%, memory 100 ns: 1 + 0.1 × (10 + 0.2 × 100) = **4 ns**.

**E6: pipeline.** k = 5, n = 100: time = 104 cycles; non-pipelined = 500; speedup = **4.808**. With 20% branches and a 2-cycle penalty, CPI = 1 + 0.2 × 2 = **1.4**.

**E7: Amdahl.** 40% of the work sped up 4×: overall speedup = 1/(0.6 + 0.1) = **1.4286**.

**E8: memory interfacing.** A 64K × 8 memory from 16K × 4 chips: (64/16) × (8/4) = **8** chips, with 2 high address bits selecting the bank.

**E9: disk.** Seek 8 ms, 7200 rpm, 4 KB at 50 MB/s: rotational latency 4.167 ms, transfer 0.078 ms, total **12.245 ms**.

**E10: DMA cycle stealing.** A 1 MB/s device moving 4-byte words, memory cycle 100 ns: 250 000 words/s × 100 ns = **2.5%** of memory cycles.

---

## Notes / flags
- Your uploaded `computer-organization.md` is mostly ISRO-flavoured (8086 addressing, pipeline cycle tables, cache hit-ratio basics). It has no coverage of Booth's algorithm, control unit design, microprogramming, memory interfacing, DMA or disks, so those are gaps against the 2027 syllabus.
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying.
- GKP's chapter analysis puts CAO at about 8.4 marks per year (2011–2021). I haven't broken that down by topic, so I can't say which topics carry the marks. The cache and pipeline formulas above are standard; practise varying the parameters until you can do them quickly.
