# Operating Systems — GATE 2027 (CS + DA does not include it)

**Syllabus basis (CS):** system calls, processes, threads, inter-process communication, concurrency and synchronization, deadlock, CPU and I/O scheduling, memory management and virtual memory, file systems. This section was not rewritten for 2027, but note that COA no longer lists secondary storage, and OS still lists file systems and I/O scheduling (so disk scheduling stays here).
**Hbk** column: the Arihant Handbook OS chapter is pp. 182–217. Per-topic pages are not mapped. Marked `182–217*`. **Check:** the contents photos showed no separate process synchronization or disk scheduling sections. Those rows are marked `check`.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
Your day-to-day use of OS helps with concepts, but the numericals (scheduling, paging, banker's) are the scoring part. This is a weak subject for the exam (about 7.1 marks per year in GKP's 2011–2021 analysis).

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | OS basics, system calls, kernel vs user mode | 182–217* | [OS short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251006150112463046/Operating-System-.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Processes: states, PCB, context switch, fork() | 182–217* | [LMN Operating Systems](https://www.geeksforgeeks.org/operating-systems/last-minute-notes-operating-systems/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Threads (user vs kernel), multithreading | 182–217* | [LMN Operating Systems (threads)](https://www.geeksforgeeks.org/operating-systems/last-minute-notes-operating-systems/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | CPU scheduling: FCFS, SJF, SRTF, priority, RR | 182–217* | [Process scheduling](https://geeksforgeeks.org/gate-notes-operating-system-scheduler) · [CPU scheduling GATE set](https://www.geeksforgeeks.org/cpu-scheduling-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Critical section, mutual exclusion, Peterson | 182–217* **check** | [Process synchronization](https://www.geeksforgeeks.org/introduction-of-process-synchronization/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Semaphores, mutex, classic problems | 182–217* **check** | [Semaphores](https://www.geeksforgeeks.org/operating-systems/semaphores-in-process-synchronization/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Deadlock: conditions, prevention, avoidance, detection | 182–217* | [Introduction to deadlock](https://www.geeksforgeeks.org/introduction-of-deadlock-in-operating-system/) · [Handling deadlocks](https://www.geeksforgeeks.org/handling-deadlocks/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Banker's algorithm, resource allocation graph | 182–217* | [Banker's algorithm](https://www.geeksforgeeks.org/bankers-algorithm-in-operating-system-2/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Memory management: partitioning, paging, segmentation, TLB | 182–217* | [Memory management](https://www.geeksforgeeks.org/operating-systems/memory-management-in-operating-system/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Virtual memory, demand paging | 182–217* | [Virtual memory](https://www.geeksforgeeks.org/operating-systems/virtual-memory-in-operating-system/) · [Demand paging](https://www.geeksforgeeks.org/operating-systems/what-is-demand-paging-in-operating-system/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Page replacement: FIFO, LRU, optimal, Belady | 182–217* | [OS Set 8 (Belady)](https://www.geeksforgeeks.org/operating-systems/operating-systems-set-8/) · [OS Set 3](https://www.geeksforgeeks.org/operating-systems/operating-systems-set-3/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | File systems (allocation, directories, inodes) | 182–217* | [LMN Operating Systems (file systems)](https://www.geeksforgeeks.org/last-minute-notes-operating-systems/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 13 | Disk scheduling (FCFS, SSTF, SCAN, C-SCAN, LOOK) | 182–217* **check** | [OS short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251006150112463046/Operating-System-.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [IPC / sync / deadlock PYQs 2005–2026](https://www.geeksforgeeks.org/quizzes/gate-ipc-concurrency-and-synchronization-deadlock-pyq-2010-to2025/), [OS Set 14 (GATE 2006 scheduling)](https://geeksforgeeks.org/?p=20342).

**My links:** (NPTEL / textbook, add here)

---

## 1–3. Processes and threads
- Process states: new, ready, running, waiting (blocked), terminated. Context switch saves and restores registers, PC, and PCB state; its cost is pure overhead.
- A process with n sequential fork() calls ends up with 2ⁿ processes in total (2ⁿ − 1 new children).
- Threads share code, data and files; each has its own stack, registers and PC. Kernel-level threads are scheduled by the OS; a blocking call in one user-level thread blocks the whole process.

## 4. CPU scheduling
- Waiting time = turnaround − burst. Turnaround = completion − arrival. Response time = first run − arrival.
- FCFS: non-preemptive, convoy effect. SJF is optimal for average waiting time (non-preemptive); SRTF is its preemptive form and can starve long jobs.
- Round robin: preemptive, time quantum q. Too small a quantum means more context switches; too large turns into FCFS.
- Priority: starvation is fixed by aging.
- Dispatcher performs the context switch; the scheduler picks the process.

## 5–6. Synchronization
- Critical section needs mutual exclusion, progress, bounded waiting.
- Semaphore: integer with atomic wait(P) and signal(V). Binary semaphore ≈ mutex (but a mutex has an owner). Counting semaphore for multiple instances.
- Producer–consumer: empty = N, full = 0, mutex = 1. Readers–writers, dining philosophers. Wrong semaphore ordering causes deadlock.
- Peterson's algorithm (two processes): flag[] and turn; satisfies all three conditions in software.

## 7–8. Deadlock
- Four necessary conditions: mutual exclusion, hold and wait, no preemption, circular wait.
- Prevention breaks one condition. Avoidance (Banker's) keeps the system in a safe state. Detection: wait-for graph cycle (single-instance resources), or a Banker's-style detection for multiple instances.
- A cycle in a resource allocation graph means deadlock only if every resource has one instance; with multiple instances it is necessary but not sufficient.
- n processes each needing at most k units of one resource type: the system is deadlock-free if R > n(k − 1), i.e. R ≥ n(k − 1) + 1.
- Banker's: Need = Max − Allocation. A state is safe if some order lets every process finish.

## 9–11. Memory
- Paging: logical address = page number + offset. Page table size = (number of pages) × (entry size). Internal fragmentation: average half a page per process. Segmentation causes external fragmentation.
- Multi-level page tables shrink the table for sparse address spaces.
- Effective access time with TLB: EAT = h(t_TLB + t_mem) + (1 − h)(t_TLB + 2·t_mem) for a one-level page table.
- Demand paging: EAT = (1 − p)·t_mem + p·(page-fault service time).
- Page replacement: FIFO (Belady's anomaly possible), LRU (stack algorithm, no anomaly), optimal (lowest faults, needs the future). Thrashing = too many page faults from too few frames.
- Allocation: first fit, best fit, worst fit; buddy system.

## 12–13. Files and disks
- Allocation: contiguous (external fragmentation, fast sequential), linked (no random access), indexed (index block; inode with direct and indirect pointers).
- Max file size with inode of d direct pointers and one single-indirect block: (d + block size / pointer size) × block size.
- Disk scheduling total head movement: FCFS (arrival order), SSTF (nearest next, starvation possible), SCAN (elevator, goes to the disk edge), C-SCAN (one direction, jump back), LOOK (goes only as far as the last request).

---

## Worked examples (all recomputed in code)

**E1: SRTF context switches (GATE 2006).** P0 (arrives 0, burst 10), P1 (2, 20), P2 (6, 30). P0 runs to 10; P1 runs 10 to 30; P2 runs 30 to 60. Context switches: P0 → P1 and P1 → P2 = **2**.

**E2: FCFS vs round robin.** P1 (arrives 0, burst 5), P2 (1, 3), P3 (2, 8), P4 (3, 6). FCFS waiting times 0, 4, 6, 13: average **5.75**. Round robin with q = 2 (a newly arrived process queues ahead of the one just preempted): completion P2 = 11, P1 = 14, P4 = 20, P3 = 22; waiting P1 = 9, P2 = 7, P3 = 12, P4 = 11; average **9.75**. The tie-break convention for simultaneous arrival and requeue changes RR numbers, so check what a question assumes.

**E3: Banker's algorithm.** Available (3, 3, 2); Allocation rows P0 (0,1,0), P1 (2,0,0), P2 (3,0,2), P3 (2,1,1), P4 (0,0,2); Max rows (7,5,3), (3,2,2), (9,0,2), (2,2,2), (4,3,3). Need rows (7,4,3), (1,2,2), (6,0,0), (0,1,1), (4,3,1). Safe sequence: **P1, P3, P4, P0, P2**.

**E4: Deadlock-free resource count.** 3 processes each needing at most 2 units: R ≥ 3·(2 − 1) + 1 = **4**.

**E5: fork().** Three sequential fork() calls create **7** new processes (2³ − 1), 8 in total.

**E6: Page replacement.** Reference string 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1 with 3 frames: FIFO **15** faults, LRU **12**, optimal **9**.

**E7: Belady's anomaly.** String 1,2,3,4,1,2,5,1,2,3,4,5 with FIFO: 3 frames give **9** faults, 4 frames give **10**.

**E8: FIFO with reversed access (GATE 2014).** 4 frames, 100 distinct pages accessed in order, then in reverse: **196** faults.

**E9: Paging numbers.** 32-bit address, 4 KB pages, 4-byte entries: 2²⁰ entries × 4 B = **4 MB** page table. TLB hit ratio 90%, TLB 10 ns, memory 100 ns: EAT = 0.9 × 110 + 0.1 × 210 = **120 ns**.

**E10: Disk scheduling.** Head at 53, requests 98, 183, 37, 122, 14, 124, 65, 67. FCFS **640**, SSTF **236**, SCAN (moving toward 0 first) **236**, LOOK (down first) **208** cylinders.

---

## Notes / flags
- The uploaded `operating-system.md` covers deadlock, Banker's, RAG, virtual memory, page replacement, paging, demand paging, scheduling, synchronization and semaphores. It has no processes/threads, memory-allocation schemes, TLB, file systems or disk scheduling. Those rows are the gaps.
- Round robin results depend on the tie-break convention in E2.
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying.
