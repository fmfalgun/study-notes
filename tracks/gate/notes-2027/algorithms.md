# Algorithms — GATE 2027 (CS + DA)

**Syllabus basis:** CS: searching, sorting, hashing; asymptotic worst-case time and space complexity; algorithm design techniques (greedy, dynamic programming, divide-and-conquer); graph traversals; minimum spanning trees; shortest paths. DA covers a comparable list; confirm in the official PDF.
**Hbk** column: the Arihant Handbook Algorithms chapter is pp. 75–116. Per-topic pages are not mapped yet. Marked `75–116*`; fill exact pages as you read.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
Strength: this is one of your strong subjects. Use it for revision and PYQ speed.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Asymptotic notations, loop analysis | 75–116* | [Asymptotic notes](https://www.geeksforgeeks.org/dsa/asymptotic-analysis-of-algorithms-notes-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Recurrences, Master theorem | 75–116* | [Recurrence notes](https://www.geeksforgeeks.org/dsa/recurrence-relations-notes-for-gate-exam/) · [Master theorem](https://www.geeksforgeeks.org/dsa/advanced-master-theorem-for-divide-and-conquer-recurrences/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Searching and sorting | 75–116* | [Searching and sorting](https://www.geeksforgeeks.org/dsa/searching-and-sorting-algorithm-notes-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Divide and conquer | 75–116* | [LMN Algorithms](https://www.geeksforgeeks.org/dsa/lmns-algorithms-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Greedy (activity selection, Huffman, fractional knapsack) | 75–116* | [Greedy notes](https://www.geeksforgeeks.org/dsa/greedy-algorithm-notes-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Minimum spanning trees (Prim, Kruskal) | 75–116* | [Kruskal](https://www.geeksforgeeks.org/dsa/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/) · [Prim](https://www.geeksforgeeks.org/dsa/prims-minimum-spanning-tree-mst-greedy-algo-5/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Shortest paths (BFS, Dijkstra, Bellman-Ford, Floyd-Warshall) | 75–116* | [Graph-based algorithms](https://www.geeksforgeeks.org/dsa/graph-based-algorithms-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Graph traversals (BFS, DFS) | 75–116* | [Graph notes](https://geeksforgeeks.org/graphs-notes-for-gate-exam) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Dynamic programming (LCS, knapsack, matrix chain) | 75–116* | [GFG GATE syllabus PDF (DP topics)](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20230302142337/GATE-PDF-1.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Hashing as an algorithm topic | 75–116* | see Programming and DS file #11 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [GFG Algorithms short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806171706133130/ALGORTIHM-SHORT-NOTES_compressed.pdf), [MST and shortest-path PYQ quiz](https://www.geeksforgeeks.org/quizzes/shortest-path-algorithms-gate-cs-pyq-quiz/).

**My links:** (NPTEL / textbook, add here)

---

## 1. Asymptotics
- f = O(g): f ≤ c·g eventually. Ω: lower bound. Θ: both. o and ω are the strict versions.
- Growth order: 1 < log log n < log n < √n < n < n log n < n² < n³ < 2ⁿ < n! < nⁿ.
- Nested loops with i doubling: inner loop count log n. With i = i + 1: n. Count iterations, not statements.

## 2. Recurrences
- Master theorem for T(n) = aT(n/b) + f(n), a ≥ 1, b > 1, c = log_b a:
  - f = O(n^{c−ε}): T = Θ(n^c).
  - f = Θ(n^c): T = Θ(n^c log n).
  - f = Ω(n^{c+ε}) and regularity (a·f(n/b) ≤ k·f(n), k < 1): T = Θ(f).
- Subtract-and-conquer: T(n) = aT(n−b) + f(n). If a = 1: roughly n·f(n)/b. If a > 1: exponential.
- Standard: T(n) = T(n−1) + c → O(n). T(n) = T(n−1) + n → O(n²). T(n) = T(n/2) + c → O(log n). T(n) = 2T(√n) + c → O(log n).

## 3. Sorting and searching
| Algorithm | Best | Average | Worst | Notes |
|---|---|---|---|---|
| Bubble / Insertion | n | n² | n² | stable, in place |
| Selection | n² | n² | n² | n swaps |
| Merge | n log n | n log n | n log n | stable, O(n) space |
| Quick | n log n | n log n | n² | in place, not stable |
| Heap | n log n | n log n | n log n | in place, not stable |
- Any comparison sort needs Ω(n log n). Counting / radix / bucket sort can beat this under assumptions.
- Binary search: O(log n). Quicksort worst case T(n) = T(n−1) + n = n(n+1)/2.

## 5. Greedy
- Activity selection: sort by finish time, pick earliest-finishing compatible activity.
- Fractional knapsack: sort by value/weight. 0/1 knapsack is not greedy-solvable.
- Huffman: repeatedly merge the two smallest frequencies. Total cost = sum of internal node weights.

## 6. MST
- Kruskal: sort edges, union-find, O(E log E) = O(E log V).
- Prim: O(V²) with an array, O(E log V) with a binary heap.
- If all edge weights are distinct, the MST is unique. Cut property and cycle property justify both algorithms.
- Squaring all positive edge weights keeps the same MST. Adding a constant to every edge also keeps the same MST (since every spanning tree has the same number of edges).

## 7. Shortest paths
| Algorithm | Complexity | Notes |
|---|---|---|
| BFS | O(V + E) | unweighted |
| Dijkstra | O((V + E) log V) heap; O(V²) array | non-negative weights only |
| Bellman-Ford | O(VE) | negative edges OK; detects negative cycles. On a complete graph O(V³) |
| Floyd-Warshall | O(V³) | all pairs |

## 8. Traversals
- DFS: edge types (tree, back, forward, cross). A back edge means a cycle in a directed graph. Topological sort via DFS finish times, O(V + E).
- Connected components, bipartite check (BFS 2-colouring), articulation points / bridges (low-link) are usual GATE ideas.

## 9. Dynamic programming
- Needs optimal substructure and overlapping subproblems.
- LCS: O(mn) time. 0/1 knapsack: O(nW). Matrix chain: O(n³). Floyd-Warshall: O(n³). Subset sum: O(nS).
- Matrix chain cost for A(p₀×p₁)·B(p₁×p₂)·C(p₂×p₃): compare (p₀p₁p₂ + p₀p₂p₃) with (p₁p₂p₃ + p₀p₁p₃).

---

## Worked examples (all recomputed in code)

**E1: Master theorem, checked numerically.** T(n) = 2T(n/2) + n gives Θ(n log n): the ratio T(2n)/T(n) → 2.13 (slightly above 2, as n log n predicts). T(n) = 4T(n/2) + n gives Θ(n²): ratio **4.0**. T(n) = T(n/2) + n gives Θ(n): ratio **2.0**.

**E2: Quicksort worst case.** Sum 1 + … + 10 = **55** = n(n+1)/2.

**E3: Kruskal.** Edges (0,1)=10, (0,2)=6, (0,3)=5, (1,3)=15, (2,3)=4. Sorted: 4, 5, 6, 10, 15. Pick 4 (2–3), 5 (0–3), skip 6 (0–2 would close a cycle), pick 10 (0–1). MST weight **19**, matching the GFG page.

**E4: MST of a complete graph with weights |i − j|.** For 100 vertices the MST uses the 99 edges between consecutive vertices, weight **99**. With weights 2|i − j| and 6 vertices the answer is **10** (2n − 2).

**E5: Dijkstra.** S→B 1, S→B→A 3, S→B→A→C 4. Distances: S 0, B 1, A 3, C 4.

**E6: LCS.** LCS("AGGTAB", "GXTXAYB") has length **4** (GTAB).

**E7: 0/1 knapsack.** Weights [1, 3, 4, 5], values [1, 4, 5, 7], capacity 7: best value **9** (items of weight 3 and 4).

**E8: Matrix chain.** Dimensions 10×30, 30×5, 5×60: minimum multiplications **4500**.

**E9: Huffman.** Frequencies 5, 9, 12, 13, 16, 45: total weighted cost **224**.

---

## Notes / flags
- **Unresolved discrepancy, check in your GKP book:** the GFG page (Data Structures and Algorithms, Set 27) gives the MST cost for a complete graph on v₁…vₙ with edge weight i + j as n² − n + 1. My code (Kruskal, 1-based labels) gives 3, 7, 12, 18, 25 for n = 2 to 6, which equals (n² + 3n − 4)/2. The two agree for n = 2 and 3 but not for n ≥ 4. The original question's weight definition may differ from what the page shows. Don't rely on either until you see the original wording.
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying.
