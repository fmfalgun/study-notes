# Operating System — Notes

*Sourcing notes / judgment calls (per task rules): (1) The Process Synchronization page does not state the classic "Mutual Exclusion / Progress / Bounded Waiting" trio by name — one item below is explicitly labeled "(added for practice, not from page)" since it's near-certain exam material. (2) Virtual Memory and Demand Paging pages give formulas/definitions but no plugged-in numeric example — flagged inline rather than inventing page content. (3) The two Banker's Algorithm pages (main + "Set 1 Safety Algorithm") use different sample matrices; both are kept since both are genuine page content, and the second page's 0-indexed safe-sequence notation ("1 3 4 0 2") is decoded inline.*

### Deadlock

## Introduction of Deadlock in Operating System — Notes

**1. Deadlock definition**
State where two or more processes are stuck forever, each waiting for a resource held by another process.

**2. Four necessary conditions (Coffman conditions)** — all four must hold simultaneously for deadlock:
- `Mutual Exclusion` — "Only one process can use a resource at any given time i.e. the resources are non-sharable."
- `Hold and Wait` — "A process is holding at least one resource at a time and is waiting to acquire other resources held by some other process."
- `No Preemption` — "A resource cannot be taken from a process unless the process releases the resource."
- `Circular Wait` — "set of processes are waiting for each other in a circular fashion."
*Breaking any single one of the four prevents/resolves deadlock — this is the basis of all prevention strategies.*

**3. Handling methods**
Deadlock can be addressed via: prevention, avoidance (Banker's Algorithm), or detection and recovery.

Worked example (from page):
Available space for allocation = 200K bytes. P0 requests 80KB, then later requests 60KB more. P1 requests 70KB, then later requests 80KB more. "Deadlock occurs if both processes progress to their second request." (After first requests: 80K+70K=150K allocated, 50K free — neither's second request, 60K or 80K, can be satisfied, and neither process will release memory, so both block forever.)

## Banker's Algorithm — Notes

**1. Core data structures**
- `Available[m]` — 1-D array: number of available instances of each resource type.
- `Allocation[n][m]` — resources of each type currently allocated to each process.
- `Max[n][m]` — maximum demand of each process.
- `Need[i,j] = Max[i,j] - Allocation[i,j]` — remaining need per process per resource type.

**2. Safety Algorithm steps**
```
1) Work = Available; Finish[i] = false for all i
2) Find i such that Finish[i]=false and Need[i] <= Work
   (if none exists, go to step 4)
3) Work = Work + Allocation[i]; Finish[i] = true; go to step 2
4) If Finish[i]=true for all i -> system is in a SAFE state
```

**3. Resource-Request Algorithm steps**
```
1) Request[i] <= Need[i]?      else -> error (exceeds max claim)
2) Request[i] <= Available?    else -> process must wait
3) Tentatively allocate:
   Available -= Request[i]; Allocation[i] += Request[i]; Need[i] -= Request[i]
4) Run Safety Algorithm on the new state -> grant if safe, else roll back and process waits
```

Worked example (from page):
5 processes (P0–P4), 3 resource types (A,B,C). `Available = [2,3,2]`

| Process | Allocation | Max |
|---|---|---|
| P0 | [0,0,1] | [7,6,3] |
| P1 | [3,0,0] | [3,2,2] |
| P2 | [1,0,1] | [8,0,2] |
| P3 | [2,3,2] | [2,1,2] |
| P4 | [0,0,3] | [5,2,3] |

Safe sequence found: **P1 → P3 → P4 → P0 → P2**.

## Program for Banker's Algorithm — Set 1 (Safety Algorithm) — Notes

**1. Safety algorithm (as stated on page)**
"Work= Available Finish [i]=false; for i=1,2,......,n" → "Find an i such that both a) Finish [i]=false b) Need_i<=work. If no such i exists goto step (4)" → "Work=Work + Allocation_i Finish[i]= true goto step(2)" → "If Finish[i]=true for all i, then the system is in safe state"

Worked example (from page):
5 processes (P0–P4), 3 resources (A,B,C). `Available = [3,3,2]`

| Process | Max | Allocation |
|---|---|---|
| P0 | [7,5,3] | [0,1,0] |
| P1 | [3,2,2] | [2,0,0] |
| P2 | [9,0,2] | [3,0,2] |
| P3 | [2,2,2] | [2,1,1] |
| P4 | [4,3,3] | [0,0,2] |

Result: "System is in safe state. Safe sequence is: 1 3 4 0 2" → i.e. **P1 → P3 → P4 → P0 → P2** (page indexes processes from 0, so "1 3 4 0 2" = P1,P3,P4,P0,P2).

## Resource Allocation Graph (RAG) — Notes

**1. Request edge**
Arrow from process vertex → resource vertex: process is currently requesting that resource.

**2. Assignment edge**
Arrow from resource vertex → process vertex: resource is currently allocated to that process.

**3. Single-instance resource rule**
A cycle in the RAG is both **necessary and sufficient** for deadlock.

**4. Multi-instance resource rule**
A cycle is **necessary but NOT sufficient** for deadlock — "Even though there is a cycle, still there is no deadlock" is possible; you must check actual resource counts.

Worked example (from page):
3 processes (P1,P2,P3), 2 resources (R1,R2), multi-instance. P1 holds R1 and requests R2; P2 holds R2 and requests R1; P3 requests both R1 and R2. Available = (0,0). Result: deadlock, since no process's request can be satisfied and nothing will be released.

**Priority for your prep (Deadlock):** Banker's Algorithm safety-check numericals (given Allocation/Max/Available, compute Need, find a safe sequence) are the single highest-yield item here — drill the Need-matrix subtraction and the greedy safe-sequence search until it's mechanical. The four necessary (Coffman) conditions are near-guaranteed 1-mark theory recall. RAG cycle-detection (single- vs multi-instance rule) is an easy scoring MCQ once the rule is memorized. The Resource-Request Algorithm is a natural numerical follow-up to Banker's — know it, but it's secondary to the core safety algorithm.

### Virtual Memory & Paging

## Virtual Memory in Operating System — Notes

**1. Virtual memory**
Memory-management technique giving processes the illusion of a large contiguous memory space regardless of actual physical RAM size.

**2. Page / Frame / Swap file**
`Page` — fixed-size block of data in virtual memory. `Frame` — fixed-size block of physical memory (RAM) that holds a page. `Swap file` — disk area holding pages not currently in use.

**3. Effective (memory) Access Time**
`EAT = p×s + (1-p)×m`
where `p` = page fault rate, `s` = page fault service time, `m` = main memory access time.

No worked numeric example on this page — formula and definitions only, no numbers plugged in.

## Page Replacement Algorithms in Operating Systems — Notes

**1. FIFO**
"The oldest page is in the front of the queue. When a page needs to be replaced page in the front of the queue is selected for removal."

**2. Optimal**
Replace the page that "would not be used for the longest duration of time in the future" — impractical in real OSes (can't predict the future); used as a theoretical best-case bound.

**3. LRU (Least Recently Used)**
"Page will be replaced which is least recently used."

**4. MRU (Most Recently Used)**
"Page will be replaced which has been used recently" — can exhibit Belady's anomaly.

Worked example (from page) — FIFO:
Reference string `1, 3, 0, 3, 5, 6, 3`, frames = 3 → **total page faults = 6**.

Worked example (from page) — LRU / Optimal / MRU, same reference string, frames = 4:
Reference string `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 3`
- LRU → **6 page faults**
- MRU → **10 page faults**
- Optimal → traced on the page but total fault count not explicitly stated (by definition it should be ≤ LRU's 6).

## Paging in Operating System — Notes

**1. Logical address split**
`page number (p)` + `page offset (d)` — p selects the page, d selects the word within it.

**2. Physical address split**
`frame number (f)` + `frame offset (d)`.

**3. Physical address formula**
`Physical Address = (Frame Number << bits-in-frame-offset) + Frame Offset`

**4. Page/frame counts**
`Number of frames = Physical Address Space / Frame Size`
`Number of pages = Logical Address Space / Page Size`

Worked example (from page):
Physical Address = 12 bits → Physical Address Space = 4K words. Logical Address = 13 bits → Logical Address Space = 8K words. Page size = Frame size = 1K words.
- Number of frames = 4K / 1K = 4 = 2²
- Number of pages = 8K / 1K = 8 = 2³

## Demand Paging in Operating System — Notes

**1. Demand paging**
"Pages enter main memory only when requested or needed by the CPU" — OS loads only necessary pages at runtime instead of the whole program upfront.

**2. Page fault**
Occurs when "the program needed to access a page that is not currently in memory."

**3. Pure demand paging**
"No pages are initially loaded into memory when the program starts and all pages are initially marked as being on disk."

**4. Replacement algorithms referenced (no formulas on this page)**
FIFO, LRU, LFU, MRU, Random.

No worked numeric example on this page — only a conceptual illustration (process P with pages P0–P3, P1 & P3 resident), no calculation performed.

**Priority for your prep (Virtual Memory & Paging):** Page-replacement numericals (trace FIFO/LRU/Optimal frame contents and count faults on a reference string) are the highest-yield item — practice the frame-by-frame trace exactly as shown above. Paging address-decomposition numericals (bits → page/frame counts, physical address computation) are equally common and purely mechanical once page-size division is automatic. The EAT formula `p×s+(1-p)×m` is a direct plug-in-numbers question type even though the source page gave no worked numbers — expect a numeric variant on the actual exam. Demand paging theory (pure demand paging, page fault definition) is lower-yield background reading.

### CPU Scheduling & Synchronization

## CPU Scheduling in Operating Systems — Notes

**1. Turnaround Time**
`Turn Around Time = Completion Time – Arrival Time`

**2. Waiting Time**
`Waiting Time = Turn Around Time – Burst Time`

**3. Response Time**
Interval from process submission until its first response/output is produced.

**4. Algorithms listed on page**
FCFS, SJF, SRTF, Round Robin, Priority Scheduling, HRRN, Multiple Queue Scheduling, Multilevel Feedback Queue Scheduling.

Worked example (from page):
Three processes, preemptive Shortest Job First (SRTF). "P0 waits for 4 ms, P1 waits for 0 ms and P2 waits for 11 ms. So average waiting time is (0+4+11)/3 = 5." → **Average waiting time = 5.0 ms**.

## Introduction of Process Synchronization — Notes

**1. Race condition**
"A situation that may occur inside a critical section. This happens when the result of multiple process/thread execution in the critical section differs according to the order in which the threads execute."

**2. Critical section**
"A code segment that can be accessed by only one process at a time. The critical section contains shared variables that need to be synchronized to maintain the consistency of data variables."

**3. Mutual Exclusion (as stated on this page)**
"Allows only one process in the critical section at a time."

**4. (added for practice, not from page)** The formal Critical-Section-Problem requirements — extremely common in GATE/ISRO MCQs, but not stated by name on this fetched page:
- `Mutual Exclusion` — only one process may be in its critical section at a time.
- `Progress` — if no process is in the CS, one of the processes waiting to enter must be let in without indefinite postponement.
- `Bounded Waiting` — there is a bound on the number of times other processes may enter the CS after a process has requested entry and before that request is granted.

Worked example (from page): `ps | grep "chrome" | wc` — illustrates cooperating processes: `ps` produces data, `grep` filters it, `wc` consumes/counts it. (Illustrative pipeline, not a numeric example.)

## Semaphores in Process Synchronization — Notes

**1. Semaphore**
Synchronization tool controlling access to shared resources via an integer value.

**2. wait() / P operation**
Decrements the semaphore; "If the semaphore becomes negative, the calling process is blocked and placed in the waiting queue until another process performs signal()"; used to acquire a resource.

**3. signal() / V operation**
Increments the semaphore; "If one or more processes are waiting, one blocked process is awakened"; used to release a resource.

**4. Counting semaphore**
Value ranges over 0..any positive integer; used when multiple instances of a resource exist.

**5. Binary semaphore**
Value is only 0 or 1; used for mutual exclusion.

Worked example (from page):
Two processes P1, P2 share semaphore `S` initialized to 1.
```
Step 1: S = 1                       (free)
Step 2: P1 executes wait(S) -> S = 0, P1 enters critical section
Step 3: P2 executes wait(S) -> S would go negative -> P2 blocks/queues
Step 4: P1 executes signal(S) -> S = 1, P2 is awakened and enters critical section
```

## Mutex vs Semaphore — Notes

**1. Data type**
`Mutex` — "A mutex is an object" (a lock). `Semaphore` — "A semaphore is an integer" (a counter).

**2. Mechanism**
Mutex = locking mechanism (Lock / Unlock). Semaphore = signaling mechanism (Wait / Signal).

**3. Subtypes**
"Mutex does not have any subtypes." Semaphore has Binary and Counting subtypes.

**4. Ownership**
"A mutex can only be modified by the process that is requesting or releasing a resource" (strict ownership) — vs. a semaphore, whose wait/signal can be invoked by multiple different processes.

**5. Key misconception the page flags**
"a mutex is a binary semaphore. But it is not!" — the real distinguishing factor is ownership/release-rights, not just the value range.

**Priority for your prep (CPU Scheduling & Synchronization):** CPU scheduling numericals (build a Gantt chart, compute waiting/turnaround time for FCFS/SJF/SRTF/Round Robin/Priority) are extremely high-yield and near-certain — memorize `TAT = CT − AT` and `WT = TAT − BT` cold and practice a preemptive-SJF/SRTF trace like the one above. Semaphore wait()/signal() mechanics and the binary-vs-counting distinction are frequent MCQ material. Mutex-vs-Semaphore differences (ownership, who may signal) are a classic conceptual MCQ trap — remember "mutex is NOT just a binary semaphore." Race-condition/critical-section definitions are foundational recall, and the Mutual-Exclusion/Progress/Bounded-Waiting trio (added above, not found on the fetched page) is common enough as a direct-recall question that it should not be skipped despite the source page's omission.
