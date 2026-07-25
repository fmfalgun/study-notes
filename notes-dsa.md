# Data Structures & Algorithms — Notes

Source: GeeksforGeeks "Notes for GATE Exam" pages (Array, Stack, Linked List, Searching & Sorting). Fetched directly from the live pages (not from training memory) and extracted from the page's own `MainArticleContent` HTML block, then cross-checked against the visible text. All four pages fetched successfully.

---
## Array Notes for GATE Exam — Notes

**1. Definition**
"An array is a collection of items of the same variable type that are stored at contiguous memory locations." Index starts at 0.
*Basic terms on the page: Array Index (starts at 0), Array Element (item accessed by index), Array Length (number of elements it can contain).*

**2. Types of arrays**
- **1D array**: linear list, fixed size, random access via index.
- **2D array**: "list of lists," aka Matrix, `array[M][N]` (M rows, N columns).
- **3D array**: collection of 2D arrays stacked; declared `data_type array_name[x][y][z]` where `x` = number of 2D arrays, `y` = rows per 2D array, `z` = columns per 2D array.

**3. Address formula — 1D array**
```
Address of A[I] = B + W * (I – LB)
```
B = base address, W = element size (bytes), I = index sought, LB = lower bound of subscript.
    Worked example (verbatim from page):
    Array `A[1300...1900]`, base address B = 1020, element size W = 2 bytes. Find address of `A[1700]`.
    ```
    Address of A[1700] = 1020 + 2 * (1700 – 1300)
                        = 1020 + 2 * (400)
                        = 1020 + 800
                        = 1820
    ```

**4. Address formula — 2D array, Row Major Order**
```
Address of A[I][J] = B + W * ((I – LR) * N + (J – LC))
```
N = number of columns, LR/LC = lower row/column bounds.
    Worked example (verbatim from page):
    `arr[1...10][1...15]`, B = 100, W = 1 byte, LR = LC = 1, N = 15 – 1 + 1 = 15. Find address of `arr[8][6]`.
    ```
    Address of A[8][6] = 100 + 1 * ((8 – 1) * 15 + (6 – 1))
                        = 100 + 1 * ((7) * 15 + (5))
                        = 100 + 1 * 110
                        = 210
    ```

**5. Address formula — 2D array, Column Major Order**
```
Address of A[I][J] = B + W * ((J – LC) * M + (I – LR))
```
M = number of rows.
    Worked example (verbatim from page, same array as #4, M = 10 – 1 + 1 = 10):
    ```
    Address of A[8][6] = 100 + 1 * ((6 – 1) * 10 + (8 – 1))
                        = 100 + 1 * ((5) * 10 + (7))
                        = 100 + 1 * 57
                        = 157
    ```
    Page's own note: "for the same position two different address locations are obtained... in row-major order movement is done across the rows... in column-major order, first move down to the first column... So both the answers are right."

**6. Address formula — 3D array, Row Major Order**
```
Address of A[i][j][k] = B + W * (M * N * (i-x) + N * (j-y) + (k-z))
```
M = total rows, N = total columns, x/y/z = lower bounds of block/row/column respectively.
    Worked example (verbatim from page):
    `arr[1:9, -4:1, 5:10]`, B = 400, W = 2 bytes. Find address of `arr[5][-1][8]`.
    x=1, y=-4, z=5; M = 1-(-4)+1 = 6; N = 10-5+1 = 6.
    ```
    Address = 400 + 2 * {[6*6*(5-1)] + 6*[(-1+4)] + [8-5]}
            = 400 + 2 * (144 + 18 + 3)
            = 400 + 2 * 165
            = 730
    ```

**7. Address formula — 3D array, Column Major Order — GOTCHA**
Page states the formula as `Address of A[i][j][k] = B + W(M*N*(i–x) + M*(k–z) + (j–y))` in the definition section, but then in the worked solution uses `Address of A[i][j][k] = B + W×(M×P×(k−z) + M×(j−y) + (i−x))` — i.e. it swaps in a variable `P` (not defined consistently with the earlier `N`). **This is an inconsistency in the source page itself** — flagging it rather than silently reconciling it. Treat the worked numeric example below as authoritative since it's the one GATE-style answer actually computed on the page.
    Worked example (verbatim from page):
    `arr[1:8, -5:5, -10:5]`, B = 400, W = 4 bytes. Find address of `arr[3][3][3]`.
    x=1 (block), y=-5 (row), z=-10 (column); M = 8-1+1 = 8; N(used as "P" in the solution) = 5-(-5)+1 = 11.
    ```
    Address = 400 + 4 * ((11*8*(3-(-10))) + 8*(3-(-5)) + (3-1))
            = 400 + 4 * (88*13 + 8*8 + 2)
            = 400 + 4 * 1210
            = 5240
    ```

**8. Previously Asked GATE Questions on Arrays (10 on page, all with page's own answers/explanations)**
1. 500 students, scores 0–100, print frequency of each score **above 50** → best storage: **(a) array of 50 numbers**.
2. `arr[2]={1,2}; cout<<0[arr]<<", "<<1[arr]` → **(a) "1, 2"** — `0[arr]` is just another way to write `arr[0]`.
3. Min comparisons to check if an integer appears **> n/2** times in a **sorted** array of n integers → **(b) O(log n)** — find first occurrence (O(log n) via binary search) and last occurrence (O(log n)); count = j−i+1; total = O(log n).
4. n×n matrix, loop swaps `A[i][j]` and `A[j][i]` for **all** i,j pairs (both loops 1..n) → **Answer: 1** (page's literal answer text; explanation: "every element A[l][m] would be swapped twice... Swapping twice means the matrix doesn't change" — i.e. output = original matrix, unchanged). *Flag: the page prints the bare answer as "1" with no visible option list in the extracted text — likely an MCQ option label that didn't render; treat the explanation, not the digit, as the ground truth.*
5. Algorithm needs (log N)^½ finds, N inserts, (log N)^½ deletes, (log N)^½ decrease-keys → best DS: **(a) Unsorted array** — insert O(1) in unsorted array vs O(log n) min-heap, O(n) sorted array/DLL.
6. Segregate +ve/−ve numbers in an array, worst-case time → **(c) O(N²)** — via quicksort-style partitioning around the first element as pivot.
7. Expected number of inversions (i<j, A[i]>A[j]) over all permutations of n distinct elements → **(b) n(n-1)/4** — there are n(n-1)/2 pairs with i<j, each has inversion probability 1/2, so expectation = ½ · n(n-1)/2 = n(n-1)/4.
8. `int array1[]={2,3}; int array2[3]={9};` then `printf("%d, %d", array1[1], array2[2]);` → **(b) "3, 0"**.
9. `int a[4][5] = {{1..5},{6..10},{11..15},{16..20}}; printf("%d", *(*(a+**a+2)+3));` → **Answer: 19**.
10. Which op **cannot** be O(1) on sorted array data? → **(c) Delete element** — "If we have to delete x and its index is last, it would take O(n)" (page's exact reasoning, as given).

**Priority for your prep (Array):** Address-calculation (row-major/column-major, 1D/2D/3D) is the single most reliably-testable direct-computation topic here — practice the formula plug-in exactly as shown above. The inversions formula `n(n-1)/4` and the "delete from sorted array" O(n) gotcha are also classic recurring GATE items.

---
## Stack Notes for GATE Exam — Notes

**1. Definition & LIFO**
"A stack is a linear data structure in which the insertion of a new element and removal of an existing element takes place at the same end represented as the top of the stack." LIFO: "the element that is inserted last will come out first."

**2. Basic operations — all `O(1)`**

| Operation | Complexity |
|---|---|
| push() | O(1) |
| pop() | O(1) |
| top() | O(1) (returns top element) |
| isEmpty() | O(1) |
| size() | O(1) |

**3. Implementation via singly linked list**
Push: init node → set data → link new node to current top → update top to new node.
Pop: check empty → `temp` = top, move top forward one step → free `temp`.
Peek: check empty → return top's value.
*Advantage over arrays: can shrink/grow dynamically — no fixed capacity, so no array-style overflow.*

**4. Applications (verbatim list)**
Function calls & recursion (state pushed on call, popped on return); Undo/redo; Expression evaluation (infix/postfix/prefix); Browser history (URL pushed on visit, popped on back); Balanced parentheses checking; Backtracking algorithms; Compiler design (parsing/syntax analysis).

**5. Advantages / Disadvantages (verbatim)**
- **Advantages**: easy implementation, efficient memory use, fast access time, supports recursion, supports backtracking, used in compiler design, enables undo/redo.
- **Disadvantages**: limited capacity, no random access (must pop everything above to reach a middle element), memory fragmentation risk, not suited to search/sort tasks, stack overflow/underflow risk, unbounded recursion → overflow.

**6. Infix → Postfix — algorithm (precedence/associativity rules as stated)**
Scan left→right. Operand → append to postfix output directly.
Operator: if scanned operator's precedence/associativity is higher than what's on stack top (or stack empty / top is `(`) → push it.
`^` is **right-associative**; `+ - * /` are **left-associative**.
Special case: if both stack-top and scanned operator are `^`, push the scanned one anyway (right-associativity wins).
If stack-top equals the scanned operator and it's left-associative → pop it first (lower effective precedence).
Otherwise: pop all operators from the stack with precedence ≥ scanned operator, then push the scanned operator (stop popping at a `(`).
`(` → push. `)` → pop and output until `(` is found, discard both parens.
At end of scan, pop everything remaining onto the output.

**7. Postfix evaluation**
Iterate left→right, push operands. On an operator, pop top two, evaluate, push the result back.

**8. Towers of Hanoi**
Rules: only one disk moved at a time; only the uppermost disk of a stack may move; no disk placed on a smaller disk.
Recursive pattern: shift N−1 disks A→B (via C); shift disk N, A→C; shift N−1 disks B→C (via A).
**Time complexity: O(2^N)** ("two possibilities for every disk... 2·2·2·...·2 (N times) = 2^N"). **Space: O(N)** (call-stack depth).
    Worked example (verbatim from page, N = 3 disks, rods A/B/C):
    ```
    Input: 3
    Output:
    Disk 1 moved from A to C
    Disk 2 moved from A to B
    Disk 1 moved from C to B
    Disk 3 moved from A to C
    Disk 1 moved from B to A
    Disk 2 moved from B to C
    Disk 1 moved from A to C
    ```

**9. Fibonacci via stack**
Sequence given on page: `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...`
    Worked example (verbatim): Input n = 9 → Output 34.

**10. Previously Asked GATE Questions on Stack (10 on page)**
1. The end of a stack where PUSH/POP happen is called: **TOP** (not FIFO/LIFO/FRONT — those are concepts/other structures, TOP is the physical position).
2. Convert postfix `M N O + * P / Q R S T / + * -` to infix → **`(((M*(N+O))/P) - (Q*(R+(S/T))))`**.
    Worked trace (verbatim from page):
    ```
    Step 1 - Push M, N, O onto the stack        → Stack: O, N, M
    Step 2 - Pop O, N, M, combine with + and *  → Stack: (M*(N+O))
    Step 3 - Push P                             → Stack: P, (M*(N+O))
    Step 4 - Pop P, combine with /              → Stack: ((M*(N+O))/P)
    Step 5 - Push Q, R, S, T                    → Stack: T, S, R, Q, ((M*(N+O))/P)
    Step 6 - Pop T,S,R,Q, combine with /,+,*    → Stack: (Q*(R+(S/T))), ((M*(N+O))/P)
    Step 7 - Pop final expression after "-"     → (((M*(N+O))/P) - (Q*(R+(S/T))))
    ```
3. Convert infix `(A + B) * C – D * E / F` to postfix → **`A B + C * D E * F / -`**.
    Worked trace (verbatim from page, left-to-right precedence collapse):
    ```
    (A + B) * C – D * E / F
    A B +  * C – D * E / F
    A B + C *  – D * E / F
    A B + C * – D E * / F
    A B + C * – D E * F /
    A B + C * D E * F / –
    ```
4. Evaluate postfix `10 5 + 60 6 / * 8 −` → **142**.
5. Push P,Q,R,S,T in order onto a stack. Pop 4 times, push each popped item into a queue. Delete 2 elements from the queue, push them back onto the stack. Pop the stack once → popped item is **S**.
6. Postfix `6 2 3 * / 4 2 * + 6 8 * -` (single-digit operands) — top two stack elements right after the **second** `*` is evaluated → **8, 1**.
7. Prefix expression `+, -, *, 3, 2, /, 8, 4, 1` evaluates to → **5**.
8. Array-based stack, `A[0..N-1]`, `push(x): A[pos]←x; pos←pos-1`, `pop(): pos←pos+1; return A[pos]` — to initialize an empty stack of capacity N → **`pos ← N - 1`**.
9. Implementing a stack using queues requires at least → **2 queues**.
10. Which applications may use a stack: (a) parenthesis balancing, (b) process scheduling OS, (c) infix→postfix conversion → **(a) and (c)** only.

**Priority for your prep (Stack):** Postfix/prefix evaluation and infix↔postfix conversion traces (Q2–Q7 above) are the single highest-yield stack topic — practice tracing the stack contents step by step exactly as done above, since GATE tends to ask you to either evaluate a given postfix/prefix string or identify intermediate stack contents. The O(1)-per-operation table and the array-stack `pos` initialization trick (Q8) are also easy direct-recall points.

---
## Linked List Notes for GATE Exam — Notes

**1. Definition**
"A linked list is a linear data structure, in which the elements are not stored at contiguous memory locations. Linked list consists of nodes where each node contains a data field and a reference(link) to the next node in the list."

**2. Types**
- **Singly linked list**: each node points only to the next node.
- **Doubly linked list (DLL)**: each node has both `prev` and `next` pointers; all SLL operations apply but prev pointers must also be updated on insert/delete.
- **Circular linked list**: last node points back to the first — no NULL terminator. Two sub-types: **circular singly** (last→first, no NULL anywhere) and **circular doubly** (last→first via next AND first→last via prev).
- **Gotcha (explicit page note)**: "Unlike other types of Linked Lists, Circular Doubly Linked List takes **O(1)** time for insertion or deletion **at the end** of the Linked List."

**3. Singly Linked List operation complexities**

| Operation | Time Complexity |
|---|---|
| Insertion at beginning | O(1) |
| Insertion at end / after a given node | O(N) (worst case traverses whole list) |
| Searching an element | O(N) |
| Find length | O(N) |
| Reverse (using `curr`, `prev`, `next` pointers) | O(N) |
| Deletion at beginning | O(1) |
| Deletion at end / after a given node | O(N) (worst case traverses whole list) |

**4. Applications (verbatim)**
Image viewer (prev/next image via links); Browser previous/next page; Music player (prev/next song); GPS navigation systems (store/manage locations & routes).

**5. Advantages / Disadvantages (verbatim)**
- **Advantages**: Dynamic size (runtime allocation); efficient insertion/deletion (especially for large lists); flexibility (no contiguous block needed).
- **Disadvantages**: No random access by index (must traverse); extra memory needed for storing pointers.

**6. GATE Archive Questions on Linked List (10 on page)**
1. Reversing a singly linked list in O(1) space — TRUE statement about time complexity? → **(A) Θ(N) in the worst case** (the best known O(1)-space algorithm is linear).
2. Worst-case time to insert n elements one-by-one into an **initially empty, sorted** linked list → **(C) Θ(n²)** — each insertion needs a traversal to find its sorted position.
3. Recursive function that calls itself on `head->next` first, *then* prints `head->data` → **(B) prints all nodes in reverse order** (traced: recursion unwinds from the last node backward, printing on the way back up).
4. Linked list vs array — which statements true: arrays have better cache locality; LL insert/delete is easy; LL has no random access; LL size is dynamic → **(E) All of the above**.
5. Doubly-linked-list reversal function (swap `prev`/`next` at every node, walk via new `prev`, fix head from `temp->prev` at the end) applied to **`1 <-> 2 <-> 3 <-> 4 <-> 5 <-> 6`**:
   **Result → `6 <-> 5 <-> 4 <-> 3 <-> 2 <-> 1`** (Answer C) — i.e. a full, clean reversal.
6. Best sort for a **random** (non-array-backed) linked list, minimizing time complexity → **(D) Merge Sort** — "worst case time complexity of Merge Sort is O(nLogn) and Insertion sort is O(n²), merge sort is preferred" (quicksort/heapsort are poor fits because LL lacks fast random access).
7. Singly-linked-list `reverse()` using `prev/current/next` pointers — missing final statement to fix the head pointer → **(A) `*head_ref = prev;`**
8. Function `fun(start)`: prints `start->data`, recurses on `start->next->next` while both next and next->next are non-NULL, then prints `start->data` **again** on the way back — run on list **`1->2->3->4->5->6`**:
   Trace: descends printing `1 3 5`, hits base case, then unwinds printing `5 3 1` → **Output: `1 3 5 5 3 1`** (Answer B).
9. `move_to_front`: walk to the last node with `p` (and `q` trailing one behind), then splice — correct code is **`q->next = NULL; p->next = head; head = p;`** (Answer D) — i.e. (1) cut the second-to-last node's next to NULL, (2) point old last node's next at the old head, (3) old last node becomes the new head.
10. `rearrange()` swaps the **data** of each node with the next node's data, advancing two nodes at a time, on list **`1,2,3,4,5,6,7`**:
   Trace: swap(1,2)→2,1,...; swap(3,4)→...,4,3,...; swap(5,6)→...,6,5,...; 7 is untouched (odd one out) → **Output: `2,1,4,3,6,5,7`** (Answer B).

**Priority for your prep (Linked List):** Q5, Q8, and Q10 above are genuine "trace this pointer-manipulation code on a concrete list" questions — this is exactly the ISRO-exam style (small-N trace, pick the resulting sequence). Practice re-deriving all three traces by hand from the pointer code, not just memorizing the final answer. The O(1) vs O(N) operation table (item 3) is the direct-recall backbone.

---
## Searching and Sorting Algorithm Notes for GATE Exam — Notes

**1. Linear Search**
`O(n)` time, sequential/one-end-to-the-other scan, works on **unsorted** data, "efficient for small lists" but degrades for large ones. Applicable to any sequentially-traversable collection (array or linked list).

**2. Binary Search**
`O(log n)` time, **divide-and-conquer**, requires **sorted** input, repeatedly halves the search interval. "Highly efficient... reduces the search space exponentially with each step."

**3. Linear vs Binary Search — comparison table (verbatim from page)**

| Linear Search | Binary Search |
|---|---|
| Input data need not be sorted | Input data needs to be in sorted order |
| Also called sequential search | Also called half-interval search |
| Time complexity O(n) | Time complexity O(log n) |
| Multidimensional array can be used | Only single dimensional array is used |
| Performs equality comparisons | Performs ordering comparisons |
| Less complex | More complex |
| Very slow process | Very fast process |

**4. Sorting complexity comparison table**
**Gotcha:** the source page does **not** contain one consolidated table like this — it states each fact in prose under a separate heading per algorithm. The table below is assembled purely from those literal per-algorithm statements (plus two data points pulled from the page's own GATE Question 2 about behavior on an already-sorted input); cells with no stated value on the page are marked "not stated on page" rather than filled from general knowledge.

| Algorithm | Best | Average | Worst | Space | Stable? |
|---|---|---|---|---|---|
| Selection Sort | not stated on page | O(n²) (page states plain "O(n²)") | O(n²) | in-place (O(1), implied by "in-place") | **Not stable** (explicit) |
| Bubble Sort | not stated on page as best-case; but page's GATE Q2 says bubble sort is Θ(n²) **even when input is already sorted** | O(n²) | O(n²) | in-place | **Stable** (explicit) |
| Insertion Sort | **Θ(n)** — from page's GATE Q2 (statement IV, "insertion sort runs in Θ(n) time" on already-ascending input, marked TRUE) | not stated on page | O(n²) (explicit, "worst case") | in-place | **Stable** (explicit) |
| Merge Sort | not stated on page as best-case; GATE Q2 confirms it is **not** Θ(n) even on sorted input (statement III marked FALSE) | O(n log n) | O(n log n) | **O(n)** (explicit) | **Stable** (explicit) |
| Quick Sort | **O(n log n)** (explicit, "average and best-case") | O(n log n) | **O(n²)** (explicit; GATE Q2 statement I says quicksort is Θ(n²) on already-sorted input, marked TRUE) | **O(log n)** (explicit, "due to the recursive nature") | not stated on page |
| Heap Sort | not stated on page | O(n log n) | O(n log n) | **O(1)** (explicit) | not stated on page |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) (explicit, non-comparison-based, "n" = elements, "k" = range of input values) | **O(k)** (explicit) | **Stable** (explicit) |

**5. Sort trace (added for practice, not from page — the page has no step-by-step array trace)**
Insertion Sort on `[5, 2, 9, 1, 5, 6]`:
```
Start:            [5, 2, 9, 1, 5, 6]
i=1 (key=2):       [2, 5, 9, 1, 5, 6]      (2 shifted left past 5)
i=2 (key=9):       [2, 5, 9, 1, 5, 6]      (9 already ≥ 5, no shift)
i=3 (key=1):       [1, 2, 5, 9, 5, 6]      (1 shifted left past 9, 5, 2)
i=4 (key=5, dup):  [1, 2, 5, 5, 9, 6]      (5 shifted left past 9 only, stops at the other 5)
i=5 (key=6):       [1, 2, 5, 5, 6, 9]      (6 shifted left past 9 only)
Sorted:            [1, 2, 5, 5, 6, 9]
```

**6. Previously Asked Problems on Searching & Sorting (10 on page, all tagged with the actual GATE year)**
1. [GATE-CS-2019] 25 distinct elements, quicksort, pivot chosen uniformly at random — probability pivot lands in the worst possible location on the first partition round → **0.08**.
2. [GATE-CS-2016] Input already ascending; which are TRUE: I. Quicksort Θ(n²); II. Bubble sort Θ(n²); III. Mergesort Θ(n); IV. Insertion sort Θ(n) → **(D) I and IV only**.
3. [GATE-CS-2015] Mergesort takes 30s (worst case) for input size 64. Max input size solvable in 6 minutes (≈ n log n scaling)? → **(B) 512**.
4. [GATE-CS-1996] Average key comparisons in a successful **sequential** search over a list of length n → **(D) (n+1)/2**.
5. [GATE-CS-2006] Which in-place sort needs the **minimum number of swaps**? → **(C) Selection Sort**.
6. [GATE-CS-1994] Recurrence relation for binary search complexity → **(B) T(n) = T(n/2) + c**, c constant.
7. [GATE-CS-2013] Tightest upper bound for inserting into a BST of n nodes → **(C) O(n)**.
8. [GATE-CS-2013] Balanced BST T with n numbers; sum all numbers between L and H, m of them exist; tightest bound O(n^a log^b n + m^c log^d n); find a + 10b + 100c + 1000d → **110**.
9. [GATE-CS-2009] Number of swaps for selection sort on n elements, worst case → **(A) O(n)**.
10. [GATE-CS-2007] Sorting algorithm with the **lowest worst-case complexity** among Merge/Bubble/Quick/Selection → **(A) Merge Sort**.

**Priority for your prep (Searching/Sorting):** The consolidated complexity table (item 4) plus GATE-2016's "behavior on already-sorted input" question (item 6, Q2) are the two facts most likely to be tested directly — ISRO loves the "which sort degrades to Θ(n²) / stays Θ(n) on sorted input" framing. Selection sort's O(n) swap-count (items 5/9) is a recurring distractor-buster: people assume O(n²) swaps, but it's actually O(n) swaps despite O(n²) comparisons.

---
## Overall Priority for your prep

Ranked by how directly ISRO-SC(CS)-style objective questions tend to hit these four topics:

1. **Searching/Sorting complexity table + trace** — highest yield. Direct MCQ recall (best/avg/worst/space/stability per sort) and small-array traces (insertion/selection/bubble by hand) are near-guaranteed question types. Also memorize the "behavior on already-sorted/reverse-sorted input" exceptions (bubble stays Θ(n²), insertion drops to Θ(n), quicksort with a bad pivot rule degrades to Θ(n²)).
2. **Linked List pointer-trace questions** — second highest. ISRO likes short pointer-manipulation code (reverse, swap-adjacent-data, move-last-to-front) run on a concrete small list (e.g. `1..6` or `1..7`); practice hand-tracing `prev/curr/next` pointer updates rather than memorizing outcomes.
3. **Stack expression conversion/evaluation** — very testable and mechanical: infix↔postfix↔prefix conversion and evaluation with actual stack-content traces (as in Stack GATE Q2/Q3/Q4/Q6/Q7 above) are exactly the kind of "grind through it" question ISRO sets since they're unambiguous and gradeable.
4. **Array address arithmetic** — lower frequency than the other three in typical ISRO sets but a guaranteed-solvable question type when it appears: row-major/column-major address formulas for 1D/2D/3D arrays are pure formula-substitution, so drill the exact formula and plug-in order shown above.

All four link fetches succeeded; no content came back garbled. One inconsistency was found and flagged in place (Array Notes, item 7: the page's own 3D column-major formula swaps a variable name between its definition and its worked solution).
