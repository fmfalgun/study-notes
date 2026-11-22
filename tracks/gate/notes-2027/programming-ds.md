# Programming and Data Structures — GATE 2027 (CS + DA)

**Syllabus basis:** CS: programming in C, recursion, arrays, stacks, queues, linked lists, trees, binary search trees, binary heaps, graphs. DA has a similar block (programming, data structures; see the official PDF to confirm exact wording).
**Hbk** column: the Arihant Handbook chapter "Data Structures / C" is pp. 30–74. Per-topic pages are not mapped yet (I only have the chapter range), so fill in exact pages while you read. Marked `30–74*`.
**Links:** only URLs that search returned. NPTEL links are unverified, so add yours under *My links*.
Strength: you said this is your strong subject, so use the checklist mainly for gaps and revision.

## Checklist (index)

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | C basics: types, operators, scope, functions | 30–74* | [GATE CS Notes index](https://www.geeksforgeeks.org/gate/gate-cs-notes-gq/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Pointers, structs, unions, type casting | 30–74* | [C PYQs](https://www.geeksforgeeks.org/c/data-structures-programming-gate-questions/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Function call stack, activation records, scope | 30–74* | [Function call stack](https://www.geeksforgeeks.org/c/function-call-stack-in-c/) · [C Language Set 4](https://www.geeksforgeeks.org/c/c-language-set-4/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Recursion | 30–74* | [Recursion notes](https://www.geeksforgeeks.org/dsa/recursion-notes-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Arrays, row/column-major addressing | 30–74* | [Array notes](https://www.geeksforgeeks.org/dsa/array-notes-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Stacks (infix/postfix, applications) | 30–74* | [Stack notes](https://geeksforgeeks.org/stack-notes-for-gate-exam) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Queues, linked lists | 30–74* | [LMN Data Structures using C](https://www.geeksforgeeks.org/dsa/lmns-data-structures/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Trees, traversals, reconstruction | 30–74* | [Trees notes](https://www.geeksforgeeks.org/dsa/trees-notes-for-gate-exam/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | BST, AVL | 30–74* | [Types of binary tree](https://www.geeksforgeeks.org/dsa/types-of-binary-tree/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Binary heap, heapsort, priority queue | 30–74* | [Tree and Hashing PYQs 2010–2025](https://www.geeksforgeeks.org/quizzes/gate-tree-graph-pyqs-2010-to-2025/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Hashing: collisions, probing, chaining | 30–74* | [Hierarchical DS intro](http://www.geeksforgeeks.org/overview-of-data-structures-set-2-binary-tree-bst-heap-and-hash/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | Graph representations and basics | 30–74* | [Graph notes](https://geeksforgeeks.org/graphs-notes-for-gate-exam) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [DSA guide for GATE CS](https://www.geeksforgeeks.org/dsa/data-structures-and-algorithms-dsa-guide-for-gate-cs-exam/), [Searching and sorting notes](https://www.geeksforgeeks.org/dsa/searching-and-sorting-algorithm-notes-for-gate-exam/) (sorting is also in the Algorithms file).

**My links:** (NPTEL / textbook, add here)

---

## 1–3. C and memory
- In C, scoping is static (lexical), not dynamic. All activation records live on one call stack.
- Each call pushes a frame (parameters, locals, return address). Recursion depth d uses O(d) stack space.
- `arr[i]` is `*(arr + i)`. Pointer arithmetic scales by the size of the pointed-to type.
- Array name in an expression decays to a pointer to its first element, but `sizeof(arr)` still gives the whole array size.
- `static` locals keep their value between calls and are initialised once. Globals default to 0.
- Pass by value only. Passing a pointer lets the callee change the caller's data.

## 4. Recursion
- Count calls by writing the recurrence. Fibonacci naive is exponential; with memoisation it is O(n).
- Tail recursion can be turned into a loop. Stack depth for naive Fibonacci recursion is O(n), not O(2ⁿ).

## 5. Arrays
- 0-indexed row-major: address(A[i][j]) = base + (i·cols + j)·w. Column-major: base + (j·rows + i)·w.
- 1-indexed versions subtract the lower bound from each index first.

## 6. Stacks and queues
- Push and pop are O(1). Infix to postfix: operands go straight to output; operators wait on the stack until one of equal or higher precedence is on top.
- Evaluate postfix with a stack: push operands, apply each operator to the top two.
- Two stacks make a queue and two queues make a stack (cost is amortised O(1) vs O(n) per operation, depending on the design).

## 7. Linked lists
- Singly list: insert at head O(1), delete a given-pointer node needs the previous node (O(n)) unless doubly linked.
- Reversal is O(n) time and O(1) extra space. Floyd's cycle detection uses two pointers.

## 8. Trees
- Binary tree with n nodes has n − 1 edges. Number of leaves = (internal nodes with 2 children) + 1.
- Max nodes at height h: 2^(h+1) − 1 (root height 0). Min height for n nodes: ⌊log₂ n⌋. Max height: n − 1.
- Inorder + preorder (or inorder + postorder) uniquely identifies a binary tree; preorder + postorder does not in general.
- Number of binary trees with n nodes, and of BST shapes: Catalan Cₙ = C(2n, n)/(n+1).
- Inorder of a BST is sorted ascending.

## 9. BST and AVL
- BST search / insert / delete: O(h). h is O(n) worst case and O(log n) if balanced.
- AVL: height difference of children ≤ 1. Minimum nodes N(h) = N(h−1) + N(h−2) + 1, with N(0) = 1, N(1) = 2.
- Rotations: LL → right rotation, RR → left rotation, LR and RL → double rotation.

## 10. Heaps
- Array layout (0-based): children of i at 2i+1 and 2i+2; parent at ⌊(i−1)/2⌋.
- Insert O(log n), extract-max O(log n), build-heap O(n), heapsort O(n log n).
- In a max-heap the minimum is at a leaf; the second largest is a child of the root.
- Max-heap from a BST in Θ(n), but a BST from a max-heap takes Ω(n log n) (comparison-based).

## 11. Hashing
- h(k) = k mod m. Load factor α = n/m.
- Linear probing: try i, i+1, i+2 … (primary clustering). Quadratic probing and double hashing reduce clustering.
- Chaining: average successful search ≈ 1 + α/2. Unsuccessful ≈ α (plus the hash computation).
- Delete in open addressing needs a tombstone marker.

## 12. Graphs
- Adjacency matrix: O(V²) space, O(1) edge check. Adjacency list: O(V + E) space.
- BFS and DFS: O(V + E) with lists, O(V²) with a matrix.

---

## Worked examples (all recomputed in code)

**E1: array address.** `int A[10][20]`, base 1000, 4 bytes. A[3][5] row-major = 1000 + (3·20 + 5)·4 = **1260**. Column-major = 1000 + (5·10 + 3)·4 = **1212**.

**E2: max-heap check.** Of 25,12,16,13,10,8,14 / 25,14,13,16,10,8,12 / 25,14,16,13,10,8,12 / 25,14,12,13,10,8,16, only **25,14,16,13,10,8,12** satisfies parent ≥ both children.

**E3: tree reconstruction.** Postorder 8,9,6,7,4,5,2,3,1 and inorder 8,6,9,4,7,2,5,1,3. Root is 1 (last of postorder). Preorder = **1, 2, 4, 6, 8, 9, 7, 5, 3**.

**E4: BST heights.** 15 nodes: minimum height ⌊log₂ 15⌋ = **3**, maximum **14**.

**E5: AVL.** Minimum nodes for heights 0 to 5: 1, 2, 4, 7, 12, 20.

**E6: postfix.** a + b * c − d becomes **abc*+d−**. For 5 3 2 * + 4 − the answer is 7.

**E7: Catalan.** Binary tree shapes with 3 nodes: **5**; with 4 nodes: **14**.

**E8: linear probing.** Table size 10, keys 12, 25, 35, 26, 22 inserted in order. 12 → slot 2. 25 → 5. 35 → collides at 5, goes to 6. 26 → collides at 6, goes to 7. 22 → collides at 2, goes to 3. Final table: slots 2, 3, 5, 6, 7 hold 12, 22, 25, 35, 26.

---

## Notes / flags
- Past-paper analysis is not included. Add GATE 2022–2026 data while studying.
- Check the AVL height convention in each question: GATE usually counts a single node as height 0. If a question counts it as height 1, N(h) shifts by one.
- DA's data-structure list may differ slightly from CS. Confirm against the official DA PDF if you choose DA.
