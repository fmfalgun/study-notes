# AI and Machine Learning — Notes

---
## Linear Regression (Python Implementation) — Notes

**FLAG:** This GFG page is implementation-focused. It does **not** explicitly write out the MSE cost function or a gradient-descent update rule anywhere in the text — it only shows the Normal Equation as a line of NumPy code. Formula below is reconstructed directly from that code (not invented), and the gap is called out rather than papered over.

**1. Normal Equation (as literally implemented on the page)**
Page code: `self.coefficients_ = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)`
Formula this implements:
```
θ = (XᵀX)⁻¹ Xᵀy
```
`X_b` is the design matrix (with a bias/intercept column of 1s prepended), `y` the target vector, `θ` the solved coefficient vector.
*e.g. solves for slope+intercept in one closed-form matrix step, no iteration needed.*

**2. Cost function / gradient descent update rule**
Not stated on this page at all — no MSE formula, no `θ := θ - α·∇J(θ)` update shown. (Standard MSE is `J(θ) = (1/2m)Σ(hθ(xᵢ) - yᵢ)²`, but since GFG doesn't state it here, treat this as a gap to fill from a textbook, not from this source.)

**3. Worked example (verbatim data from the page)**
```
X_simple = [1,2,3,4,5,6,7,8,9,10]   (reshaped to column vector)
y_simple = [2,4,5,4,5,7,8,9,10,12]
```
Page output: `"Simple LR Coefficients"` and `"R² Score: 0.95"` — the page prints these labels but does **not** display the actual numeric coefficient values (slope/intercept), only the R² score. So the example is real but incomplete as given.

Priority for your prep: LOW-MEDIUM as sourced from this page — you'll need the standard MSE/gradient-descent formulas from elsewhere since this page skips them; the normal equation form here is reliable.

---
## Logistic Regression (Understanding Logistic Regression) — Notes

**4. Sigmoid function**
```
σ(z) = 1 / (1 + e^(-z))
```
Converts any real value into a probability in (0,1).

**5. Logistic regression hypothesis**
Page states:
```
p(X; b, w) = e^(w·X + b) / (1 + e^(w·X + b)) = 1 / (1 + e^(-(w·X + b)))
```
*i.e. sigmoid applied to the linear combination `w·X + b`.*

**6. Log-likelihood (cost) function**
Page states:
```
log(L(b,w)) = Σ [ yᵢ·log(p(xᵢ)) + (1-yᵢ)·log(1-p(xᵢ)) ]
```
This is *maximized* over `w,b` (equivalently, its negative — log-loss — is minimized) to fit the model.

**7. Worked example**
No numeric step-by-step worked example on this page. It only reports final results from two code demos:
- Binary classification (breast cancer dataset): *"Logistic Regression model accuracy: 96.49%"*
- Multinomial classification (digits dataset): *"Logistic Regression model accuracy: 96.66%"*
No specific data point/probability trace is shown — say so explicitly rather than inventing one.

Priority for your prep: HIGH — sigmoid + log-loss formulas are exam staples and both are clearly given verbatim above.

---
## K-Nearest Neighbours — Notes

**8. Euclidean distance formula**
Page states:
```
d(x, Xᵢ) = √( Σⱼ₌₁ⁿ (xⱼ - Xᵢⱼ)² )
```
Straight-line distance between the query point `x` and a training point `Xᵢ` across `n` features.

**9. KNN algorithm (as given on page)**
1. Select the value of `K` (number of nearest neighbours to consider).
2. Calculate distance between the query point and every point in the dataset.
3. Find the `K` points with the smallest distances (the nearest neighbours).
4. Majority voting: *"The algorithm then looks at which category the neighbors belong to and picks the one that appears the most."*

**10. Worked example (verbatim from page)**
```
Training points: [[1,2], [2,3], [3,4], [6,7], [7,8]]
Training labels: ['A','A','A','B','B']
Test point: [4,5], K = 3
Result: 'A'  (majority of the 3 nearest points are labeled 'A')
```
Note: the page gives this exact setup and result but does not print the individual computed distances — only the final majority-vote outcome.

Priority for your prep: HIGH — distance formula + majority-vote rule are exactly what "easy/definitional" questions target; the worked example above is real and small enough to redo by hand (compute the 5 distances from (4,5) yourself as practice).

---
## Naive Bayes Classifiers — Notes

**11. Bayes' theorem**
Page states:
```
P(y|X) = [ P(X|y) · P(y) ] / P(X)
```
- `P(y|X)`: posterior probability of class `y` given features `X`
- `P(X|y)`: likelihood
- `P(y)`: prior probability of class `y`
- `P(X)`: evidence/marginal likelihood

**12. Naive (conditional) independence assumption**
Page states:
```
P(x₁, x₂, ..., xₙ | y) = P(x₁|y) · P(x₂|y) · ... · P(xₙ|y)
```
giving the classifier rule:
```
P(y | x₁,...,xₙ) ∝ P(y) · Πᵢ₌₁ⁿ P(xᵢ|y)
```

**13. Worked example (verbatim numbers from page — Play Golf dataset)**
Query: `X = (Sunny, Hot, Normal, False)`
Class priors: `P(Yes) = 9/14`, `P(No) = 5/14`
Unnormalized posteriors: `P(Yes|today) ≈ 0.02116`, `P(No|today) ≈ 0.0068`
Normalized: `P(Yes|today) ≈ 0.756`, `P(No|today) ≈ 0.244`
**Prediction: "Yes (Play Golf)"** since 0.756 > 0.244.

Priority for your prep: HIGH — this is the canonical Naive Bayes worked example (weather/play-golf), commonly reused in exam questions; formula + independence assumption + full numeric trace are all present.

---
## K-Medoids Clustering (with Example) — Notes

**14. K-Medoids algorithm steps (as given on page)**
1. **Initialize:** randomly select `k` data points from the dataset as initial medoids.
2. **Assign:** assign each remaining point to the nearest medoid using a distance metric (e.g. Manhattan or Euclidean).
3. **Update (swap):** for each medoid, try swapping it with a non-medoid point; recompute total cost; accept the swap only if cost decreases.
4. **Repeat** until no further cost reduction is possible.

**15. Worked example (verbatim numbers from page)**
9 data points labeled 0–8, `k = 2`.
Initial medoids: `C1 = (4,5)`, `C2 = (8,5)`
Using Manhattan distance, initial clustering:
- Cluster 1 (around C1): points 1, 2, 5
- Cluster 2 (around C2): points 0, 3, 6, 7, 8
- **Total cost = 20**

Swap attempt: replace a medoid with `(8,4)` → **new cost = 22**
```
Swap Cost = New Cost − Previous Cost = 22 − 20 = 2   (> 0 → reject)
```
Since the swap cost is positive, the swap is rejected and the original medoids `(4,5)` and `(8,5)` are kept as final.

Priority for your prep: HIGH — the swap-cost decision rule (`if new_cost - old_cost < 0, accept`) is the key testable mechanic, and the numeric trace above (cost 20 → 22, reject) is real and reusable as a redo-by-hand drill.

---
## Breadth First Search (BFS) for a Graph — Notes

**16. BFS algorithm (C++ pseudocode from page)**
```cpp
vector<int> bfs(vector<vector<int>>& adj) {
    int V = adj.size();
    vector<bool> visited(V, false);
    vector<int> res;
    queue<int> q;
    int src = 0;
    visited[src] = true;
    q.push(src);
    while (!q.empty()) {
        int curr = q.front();
        q.pop();
        res.push_back(curr);
        for (int x : adj[curr]) {
            if (!visited[x]) {
                visited[x] = true;
                q.push(x);
            }
        }
    }
    return res;
}
```
Core idea: mark start visited, push to queue; repeatedly pop front, record it, push all unvisited neighbours (marking them visited immediately to avoid duplicate enqueues).

**17. Worked trace (verbatim from page)**
Graph adjacency list: `[[1,2], [0,2], [0,1,3,4], [2], [2]]`
Trace as given:
- Visit 0 → print 0
- Visit 1 (neighbor of 0) → print 1
- Visit 2 (next neighbor of 0) → print 2
- Visit 3 (first unvisited neighbor of 2) → print 3
- Visit 4 (next neighbor of 2) → print 4

**Output: `[0, 1, 2, 3, 4]`**

Priority for your prep: HIGH — queue-based level order traversal is a guaranteed easy-level question; the trace above is small enough to redraw from memory.

---
## Depth First Search (DFS) for a Graph — Notes

**18. DFS algorithm (pseudocode pattern from page, recursive form)**
```
visited[s] = true
res.push_back(s)
for i in adj[s]:
    if not visited[i]:
        dfsRec(adj, visited, i, res)
```
Core idea: mark current node visited and record it, then recurse into each unvisited neighbour before backtracking (stack-based/recursive, unlike BFS's queue).

**19. Worked trace (verbatim from page)**
Same graph as BFS: adjacency list `[[1,2], [0,2], [0,1,3,4], [2], [2]]`
Trace as given:
*"Start at 0: Mark as visited. Print 0. Move to 1: Mark as visited. Print 1. Move to 2: Mark as visited. Print 2. Move to 3: Mark as visited. Print 3. (backtrack to 2) Move to 4: Mark as visited. Print 4"*

**Output: `[0, 1, 2, 3, 4]`**

Second example on page — disconnected graph:
**Output: `0 3 2 1 4 5`** — page notes this demonstrates DFS looping over all vertices to also cover separate connected components (not just one DFS call from a single source).

Priority for your prep: HIGH — contrast with BFS is a classic definitional question (stack/recursion vs queue); both traces above are real and worth redrawing.

---
## A* Search Algorithm — Notes

**20. Core formula**
Page states:
```
f = g + h
```
- `g`: movement cost from the start node to the current node along the path taken so far.
- `h`: heuristic — estimated movement cost from the current node to the goal.
- `f`: total estimated cost of the path through this node (used to pick which node to expand next — always expand lowest `f`).

**21. Successor update rule (as given on page)**
```
successor.g = q.g + distance(successor, q)
successor.h = distance(goal, successor)
successor.f = successor.g + successor.h
```
(`q` is the node currently being expanded; `successor` is a neighbour reached from `q`.)

**22. Worked example**
No numeric worked example on this page — it shows grid/path diagrams (mentioning Euclidean-distance heuristic among others) but never fills in actual g/h/f numbers for specific nodes. Flagging this rather than inventing numbers.

*(Added for practice, not from page): start node A, goal C, direct edge A→B cost 1, B→C cost 2, straight-line heuristic h(A)=2, h(B)=1, h(C)=0. At B: g=1, h=1, f=2. At C via B: g=3, h=0, f=3 — A* would expand B before considering any alternative with f>2.)*

Priority for your prep: MEDIUM — formula `f=g+h` and the successor-update rule are definitely testable and are verbatim from the page; since no real numeric example exists on the page, be ready to compute f-values on a small hand-drawn grid yourself (the toy example above is a placeholder, not sourced).

---
## Priority for your prep (overall)

1. **HIGH — do these first:** Naive Bayes (full numeric worked example, formula-complete), K-Medoids (full numeric worked example with swap-cost decision), KNN (distance formula + majority vote + concrete point setup), BFS and DFS (both have full pseudocode + identical graph trace — great for direct comparison), Logistic Regression (sigmoid + log-loss formulas are clean and exam-ready even without a numeric trace).
2. **MEDIUM:** A* Search — formula and update rule are solid, but you must supply your own numeric practice example since GFG's page has none.
3. **LOW-MEDIUM / needs supplementing:** Linear Regression — this specific GFG page only gives the Normal Equation (via code) and an incomplete data example (inputs given, coefficients never printed); bring the standard MSE cost function and gradient-descent update rule from a textbook/other source since this page omits them entirely.
4. All 8 links fetched successfully; no pages returned garbled/unreadable content, but the Linear Regression and A* Search pages are flagged above as missing content the exam syllabus expects (cost function/GD rule; numeric worked example, respectively).
