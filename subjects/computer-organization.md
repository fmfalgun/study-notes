# Computer Organization & Architecture — Notes

---
## Machine Instructions — Notes

**1. What a machine instruction is**
`machine instruction = several bytes in memory telling the processor to perform ONE machine operation`
Machine code = instructions executed directly by the CPU; a machine language program is a collection of these instructions in main memory. Each instruction does one specific task (load, jump, ALU op, etc.) on data in a register or memory.

**2. General instruction-line format (as given on the page)**
`Label: OPCODE operand(s) ; comment`
- Label — identifier assigned to the address of the first byte of the instruction, must be followed by `:`
- At least one space is required between fields (no space → ambiguity)
- Comment field begins with `;`
*e.g. `Here: MOV R5,#25H;load 25H into R5`*

**3. 8086 instruction categories (know one example each)**
- Data transfer: `MOV, IN, OUT, LEA, LDS, LES, PUSH, POP, XCHG, XLAT`
- Arithmetic: `ADD, SUB, ADC, SBB, INC, DEC, NEG, CMP, MUL, DIV, IMUL, IDIV, CBW, CWD, AAA/AAS/AAM/AAD, DAA/DAS`
- Logic: `NOT, AND, OR, XOR, TEST, SHL/SHR, SAL/SAR, ROL/ROR, RCL/RCR`
- String manipulation: `MOVS, MOVSB, MOVSW, CMPS, SCAS, LODS, STOS`
- Control transfer: `JMP, JNZ`
- Loop control: `LOOP, LOOPE/LOOPZ, LOOPNE/LOOPNZ, JCXZ`
- Subroutine/Interrupt: `CALL, RET, INT, INTO, IRET`
- Processor control (flags): `STC, CLC, CMC, STD, CLD, STI, CLI, PUSHF, POPF`

**4. Worked example (verbatim GATE CSE 2015 question on this page)**
Sequence, with R0–R8 general purpose registers, first register = result of the other two:
```
MUL R5, R0, R1
DIV R6, R2, R3
ADD R7, R5, R6
SUB R8, R7, R4
```
4-stage pipeline: IF (Instruction Fetch/Decode), OF (Operand Fetch), PO (Perform Operation), WB (Write Back).
IF, OF, WB each take **1 cycle**. PO takes **1 cycle** for ADD/SUB, **3 cycles** for MUL, **5 cycles** for DIV. Operand forwarding is used from PO → OF.

Options given: (A) 11 (B) 12 **(C) 13** (D) 14 — correct answer is **13**, shown by this cycle table from the page:
```
Cycle:   1  2  3  4  5  6  7  8  9 10 11 12 13
MUL R5: IF OF PO PO PO WB
DIV R6:          IF OF PO PO PO PO PO WB
ADD R7:                            IF OF PO WB
SUB R8:                                  IF OF PO WB
```
Reasoning: MUL occupies PO for 3 cycles, DIV for 5 cycles (each blocking the pipeline behind it); ADD/SUB need their forwarded operands from the preceding instruction's PO stage before they can enter OF, so they slot in right after.

**Priority for your prep:** the GATE-2015 pipeline-cycle-counting question (#4) is exactly the ISRO-style numerical — practice re-deriving cycle tables like this for different stage-cycle counts. #1–#3 are recall/definition fodder, useful for 1-mark MCQs on instruction categories.

---
## Addressing Modes in 8086 — Notes

**1. Effective address (EA) components**
`Offset = Displacement + Base register content + Index register content` (any combination)
- Displacement: 8/16-bit immediate value in the instruction
- Base: `BX` or `BP`
- Index: `SI` or `DI`

**2. Implied mode**
Operand is specified in the instruction itself (used for zero-address instructions).
*e.g. `CLC` — resets the Carry flag to 0*

**3. Immediate addressing** (symbol `#`)
Data itself is present in the address field of the instruction; range limited by the size of the address field.
*e.g. `MOV AL, 35H` — moves the data 35H into AL register*

**4. Register mode**
Operand is in an 8-bit or 16-bit general-purpose register named in the instruction (one register reference).
*e.g. `MOV AX, CX` — move contents of CX to AX*

**5. Register Indirect mode**
Operand's offset is held in `BX/BP/SI/DI` (two register references: one to get the address, one to get the data).
*e.g. `MOV AX, [BX]` — move contents of memory location addressed by BX into AX*

**6. Auto-increment / Auto-decrement mode**
`Add R1, (R2)+  →  R1 = R1 + M[R2]; R2 = R2 + d`   (increment, post-access)
`Add R1, -(R2)  →  R2 = R2 - d; R1 = R1 + M[R2]`   (decrement, pre-access)
Useful for stepping through arrays; basis of LIFO stack push/pop implementation.

**7. Direct / Absolute addressing** (symbol `[ ]`)
16-bit effective address of the data is part of the instruction itself (one memory reference).
*e.g. `ADD AL,[0301]` — add contents of offset address 0301H to AL*

**8. Indirect addressing** (symbol `@` or `()`)
Address field holds the *address of the effective address* — two references needed (1st to get EA, 2nd to get data).
- Register Indirect: EA is in a register — *e.g. `MOV A, @R0`*
- Memory Indirect: EA is in memory — *e.g. `MOV AX, [[5000H]]`*

**9. Indexed addressing**
`Offset = index register (SI or DI) + displacement`
*e.g. `MOV AX, [SI + 05]`*

**10. Based-Indexed addressing**
`Offset = base register (BX) + index register (SI or DI)`
*e.g. `ADD AX, [BX+SI]`*

**11. PC-relative addressing** (intra-segment transfer of control)
```
EA = PC + Address field value
PC = PC + Relative value
```

**12. Base-register addressing** (inter-segment transfer of control; good for position-independent code)
```
EA = Base register + Address field value
PC = Base register + Relative value
```

**13. Worked example (verbatim GATE sample question on this page)**
Match each high-level statement to its most natural addressing mode:
```
1. A[1] = B[J];      a. Indirect addressing
2. while (*A++);     b. Indexed addressing
3. int temp = *x;    c. Autoincrement
```
Answer: **(C) → (1,b), (2,c), (3,a)**
- `A[1] = B[J]` → indexed addressing (indexing used for array access)
- `while (*A++)` → autoincrement (memory location auto-incremented)
- `int temp = *x` → indirect addressing (temp gets the value stored at the address held in x)

**Priority for your prep:** #2–#10 (know each mode + one-liner example) are direct MCQ material; #11/#12 (PC-relative vs base-register EA formulas) show up in "which addressing mode suits position-independent code" questions. #13's mapping style (HLL construct → addressing mode) is a recurring GATE question pattern — practice it.

---
## Cache Memory — Notes

**1. Cache hit / cache miss**
- Cache hit: CPU finds the required data in cache → fast access.
- Cache miss: data not found in cache → CPU must fetch from slower main memory.

**2. Hit ratio (the only formula given on this page)**
```
Hit ratio = (Number of cache hits) / (Number of searches)
```
This is literally the only performance formula the page states. It does **not** give a miss-ratio formula, an AMAT formula, hit time, or miss penalty, and it has **no worked numeric example** — flagging this explicitly per instructions rather than inventing page content.

**3. Locality of reference**
Cache effectiveness relies on recently/nearby-accessed items being likely accessed again (temporal + spatial locality) — stated conceptually, no formula.

**4. Cache vs RAM (quick contrast table from the page)**
Cache: very close to CPU, SRAM, nanosecond access, KB–few MB, multi-level (L1/L2/L3).
RAM: connected via memory bus, DRAM, tens-of-nanoseconds access, GB–TB, single level.

**5. (Added for practice, not from page) Standard AMAT formula — memorize this even though GFG's page omits it:**
```
Miss ratio = 1 - Hit ratio
AMAT = Hit time + Miss ratio × Miss penalty
```
*Worked example (added for practice, not from page): Hit time = 2 ns, Miss penalty = 20 ns, Hit ratio = 0.9 (Miss ratio = 0.1)*
`AMAT = 2 + 0.1 × 20 = 2 + 2 = 4 ns`

**Priority for your prep:** the page only gives the hit-ratio formula — memorize miss-ratio/AMAT from standard COA references (item #5 above) since ISRO/GATE numericals are built on AMAT, not just hit ratio. #1/#3/#4 are quick recall for 1-mark conceptual questions.

---
## Cache Organization | Set 1 (Introduction) — Notes

**1. Why cache organization matters**
Cache is close to CPU, faster than main memory, but smaller — cache organization = mapping data in main memory to locations in cache.

**2. Simple mapping idea and its problem**
Use the last few bits of a long memory address as the cache address. Problem: you lose the high-order bits, so you can't tell which higher-order block the data actually belongs to → need a **Tag**: extra stored info identifying which memory block currently sits in that cache line.

**3. Cache block**
Because of spatial locality, cache is organized into blocks; typical block sizes are **32 bytes or 64 bytes** (this is the only concrete number the page gives, no formula built around it).

**4. Direct-Mapped Cache**
Last few bits of the memory address select the cache line directly; remaining bits stored as tag.
- Pros: simple, low hardware overhead, fast hit time.
- Cons: high miss rate (limited blocks), conflict misses from block collisions, limited placement flexibility.
- Illustrative problem from the page: with a 2-bit cache address (4 lines) and a program that accesses addresses `2, 6, 2, 6, 2, ...` repeatedly — since 2 and 6 map to the *same* cache line (they share the same low-order bits), every access is a miss even though only 2 distinct addresses are being reused.

**5. Set-Associative Cache**
Middle ground between direct-mapped and fully-associative — each set holds multiple blocks.
- Pros: higher hit rate than direct-mapped, more flexible placement, fewer conflict misses.
- Cons: higher hardware overhead, longer hit time (search multiple ways), scalability limited by fixed ways/set.

**6. Fully-Associative Cache**
Data can go anywhere in the cache.
- Pros: highest hit rate, most flexible placement, no conflict misses.
- Cons: highest hardware overhead, longest hit time (must search entire cache), poor scalability (large tag storage).

**No worked numeric example on this page** — it is a purely conceptual introduction (no tag/line/offset bit-count calculation, no hit-ratio or AMAT numbers are given here despite the topic name).

**7. (Added for practice, not from page) Standard address-splitting formula for direct-mapped cache:**
```
Number of lines in cache = Cache size / Block size
Line/Index bits = log2(number of lines)
Block offset bits = log2(block size)
Tag bits = Total address bits - Index bits - Offset bits
```
*Worked example (added for practice, not from page): 32-bit address, direct-mapped cache with 1024 lines, block size 32 bytes.*
`Offset bits = log2(32) = 5`, `Index bits = log2(1024) = 10`, `Tag bits = 32 - 10 - 5 = 17`

**Priority for your prep:** the direct-mapped "aliasing" example (#4) is the conceptual seed for the classic tag/index/offset-bit numericals — since GFG doesn't compute those bit-splits here, drill the added formula (#7) with different address-width/cache-size/block-size combinations, since that's the actual ISRO/GATE question shape.

---
## Pipelining Set 1: Execution and Throughput — Notes

**1. Pipeline execution time**
```
ET_pipeline = (k + n - 1) cycles = (k + n - 1) × Tp
```
`k` = number of pipeline stages/segments, `n` = number of tasks/instructions, `Tp` = clock cycle time. Logic: the first instruction takes `k` cycles to exit the pipeline; each of the remaining `n-1` instructions adds only 1 more cycle.

**2. Non-pipelined execution time**
```
ET_non-pipeline = n × k × Tp
```

**3. Speedup**
```
S = ET_non-pipeline / ET_pipeline = (n × k) / (k + n - 1)
```
When `n >> k`: `S → k` (speedup approaches the number of pipeline stages).

**4. Efficiency and Throughput**
```
Efficiency = S / S_max = S / k
Throughput = n / [(k + n - 1) × Tp]
```
Note (as stated on page, slightly loosely worded): "CPI of an ideal pipelined processor is 1/Tp when n is very large" — read this as: ideal throughput → 1 instruction per Tp.

**5. Latency**
```
Latency = k × Tp
```

**6. RISC 5-stage pipeline (the stages referenced by the formulas above)**
IF (Instruction Fetch) → ID (Instruction Decode, register read) → EX (Execute/ALU) → MEM (Memory Access) → WB (Write Back)

**7. Worked example (verbatim numbers from the page)**
"Consider a processor having **4 stages** and let there be **2 instructions** to be executed."
- Non-overlapped execution (no pipelining) — space-time diagram given:
```
Stage/Cycle: 1  2  3  4  5  6  7  8
S1:          I1          I2
S2:             I1          I2
S3:                I1          I2
S4:                   I1          I2
Total time = 8 cycles
```
- Overlapped execution (pipelined) — space-time diagram given:
```
Stage/Cycle: 1  2  3  4  5
S1:          I1 I2
S2:             I1 I2
S3:                I1 I2
S4:                   I1 I2
Total time = 5 cycles
```
Check against the formulas: `ET_non-pipeline = n×k = 2×4 = 8` ✓. `ET_pipeline = k+n-1 = 4+2-1 = 5` ✓.

**Priority for your prep:** #1–#5 (the five formulas: pipeline time, non-pipeline time, speedup, efficiency/throughput, latency) are the direct plug-and-chug numericals ISRO loves — practice with different k/n/Tp values, using #7's k=4,n=2 case as your sanity check.

---
## Pipelining Set 2: Dependencies and Data Hazard — Notes

**1. Three types of dependency**
Structural, Control, Data — each can introduce **stalls** (a stall = a cycle in the pipeline with no new input).

**2. Structural dependency — worked example (verbatim from page)**
Resource conflict: instructions I1 and I4 both need the same memory resource in the same cycle.
```
Instr/Cycle: 1        2   3   4
I1:          IF(Mem)  ID  EX  Mem
I2:                   IF(Mem) ID  EX
I3:                       IF(Mem) ID  EX
I4:                           IF(Mem) ID   <- conflicts with I1 at cycle 4
```
Fix = stall I4 until the resource is free, which stretches total execution:
```
Cycle: 1        2   3   4   5   6   7   8
I1:    IF(Mem)  ID  EX  Mem WB
I2:             IF(Mem) ID  EX  Mem WB
I3:                 IF(Mem) ID  EX  Mem WB
I4:                     -   -   -   IF(Mem)  ...
```
Fix: separate instruction/data memory (Harvard architecture) or duplicate resources.

**3. Control dependency (branch hazard) — worked example (verbatim from page)**
```
100: I1
101: I2 (JMP 250)
102: I3
...
250: BI1
```
Expected correct sequence: `I1 → I2 → BI1`. But since the JMP target is only known after the **ID** stage, the naive pipeline fetches I3 anyway, giving wrong sequence `I1 → I2 → I3 → BI1`. Fix = insert a delay slot until target address is known:
```
Cycle:   1   2         3   4    5   6
I1:      IF  ID        EX  MEM  WB
I2:      -   IF ID(PC:250) EX  MEM WB
Delay:   -   -         -   -   -   -
BI1:     -   -         -   -   IF  ID  EX
```
Correct sequence restored: `I1 → I2 → Delay(stall) → BI1`.

**4. Branch penalty formula**
```
If target address is known after the k-th stage → (k - 1) stalls introduced
Total stalls due to branches = Branch frequency × Branch Penalty
```
(Here target known after ID = stage 2, so branch penalty = 1 stall, matching the diagram above.)

**5. Data dependency — Bernstein condition**
For instruction `S: ADD R1, R2, R3`: `I(S) = {R2, R3}` (read set), `O(S) = {R1}` (write set).
- **Flow/True dependence**: `O(S1) ∩ I(S2) ≠ ∅` — S2 reads a value S1 writes.
- **Anti-dependence**: `I(S1) ∩ O(S2) ≠ ∅` — S1 reads before S2 overwrites it.
- **Output dependence**: `O(S1) ∩ O(S2) ≠ ∅` — both write the same location.

**6. Data hazard — worked example (verbatim from page)**
```
I1: ADD R1, R2, R3
I2: SUB R4, R1, R2
```
Without forwarding — I2 reads R1 in its ID stage (cycle 2) before I1 has written it in DM (cycle 4), so I2 gets the **old/stale** value of R1:
```
Cycle:  1   2            3   4
I1:     IF  ID           EX  DM
I2:         IF  ID(Old value)  EX
```
Fix = **operand forwarding**: interface registers between stages hold intermediate results so the dependent instruction reads the new value directly (works only when the dependent instruction is ALU-type):
```
Cycle:  1   2   3   4
I1:     IF  ID  EX  DM
I2:         IF  ID  EX
```

**7. Three named data hazards**
Let `I` then `J` (J follows I):
- **RAW** (Read After Write / true dependency): `J` reads before `I` writes. *e.g. `I: R2 ← R1+R3`; `J: R4 ← R2+R3`*
- **WAR** (Write After Read / anti-dependency): `J` writes before `I` reads. *e.g. `I: R2 ← R1+R3`; `J: R3 ← R4+R5`*
- **WAW** (Write After Write / output dependency): `J` writes before `I` writes. *e.g. `I: R2 ← R1+R3`; `J: R2 ← R4+R5`*
(WAR and WAW occur only under out-of-order execution.)

**Priority for your prep:** #2/#3/#6 (the actual cycle-diagram worked examples for structural, control, and data hazards) are the highest-value items — ISRO questions often give you a pipeline diagram and ask you to spot the hazard type or count stalls. #4 (branch penalty formula) and #7 (RAW/WAR/WAW naming from register examples) are the quick-recall MCQ layer on top.

---
## Overall Priority for Your Prep

1. **Pipelining cycle-counting numericals** (Machine Instructions #4, Pipelining Set 1 #1–#5 and #7, Pipelining Set 2 #2/#3/#6) — this is the single most exam-relevant cluster; practice building space-time diagrams and computing speedup/throughput/stalls for varying k, n, Tp, and hazard scenarios.
2. **Addressing modes with EA formulas** (Addressing Modes #6, #11, #12, and the HLL→mode mapping in #13) — reliable 1–2 mark questions.
3. **Cache AMAT/miss-ratio** — GFG's own pages are weak here (only hit-ratio is stated); rely on the standard formulas added under Cache Memory #5 and Cache Organization #7, since ISRO numericals are built on AMAT and tag/index/offset bit splits, not just the bare hit-ratio definition.
4. **RAW/WAR/WAW naming and branch-penalty formula** — fast recall points once the cycle-diagram intuition (priority #1) is solid.
5. **8086 instruction-category recall** (Machine Instructions #3) — lowest yield, review only if time remains.
