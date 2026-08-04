# Mathematics — Notes

Source: GeeksforGeeks GATE-notes pages for Combinatorics, Graph Theory, Linear Algebra, Calculus, and Probability & Statistics (as prioritized in `exam-priority-report.md` → Mathematics, Tier 1). Reconstructed from the ISRO-prep chat session (originally shown inline, never saved to a file) — content below is the final, corrected pass after gaps flagged during that session were filled in with real worked examples fetched from each page.

---
## Discrete Mathematics — Combinatorics

**1. Combinatorics Basics**
- `nCr = n!/(r!(n-r)!)`, `nPr = n!/(n-r)!`
- Addition principle (OR, mutually exclusive): `m + n`. Multiplication principle (AND, independent): `m × n`.
- *Worked example (from page):* 3 variables x,y,z, choose 2 → **Combinations**: xy, yz, zx (3 = C(3,2)). **Permutations**: xy, yx, yz, zy, zx, xz (6 = P(3,2)) — permutations double-count because order matters.

**2. Binomial Coefficients**
- `nCk = n!/(k!(n-k)!)`. Binomial theorem: `(a+b)ⁿ = ΣnCr·aⁿ⁻ʳbʳ`. General term: `T(r+1) = nCr·aⁿ⁻ʳ·bʳ`.
- Symmetry: `C(n,k)=C(n,n-k)`. Sum of all coefficients: `ΣC(n,k) = 2ⁿ`.
- Middle term: n even → one middle term at position `(n/2)+1`. n odd → two middle terms at positions `(n+1)/2` and `(n+3)/2`.
- *Worked examples:*
  - Does `(x²-2/x)¹⁸` have an `x¹⁰` term? `T(r+1) = (-1)ʳ2ʳ·18Cr·x^(36-3r)`. Set `36-3r=10 → r=26/3` — not an integer → **no such term**. *(Good check-pattern: always verify r comes out as a whole number.)*
  - Coefficient of `x²` in `(x+1/x)⁸`: exponent `8-2r=2 → r=3` → `C(8,3) = 56`.
  - Expand `(x+2)³ = x³+6x²+12x+8`.
  - Approximate `(1.01)⁵ ≈ 1+0.05+0.001 = 1.051` (binomial approx for small x: `1+nx+[n(n-1)/2]x²`).

**3. Generalized Permutations & Combinations**
- Permutations with repetition: `nʳ` — arrange `r` picks from `n` types, each type reusable, order matters. *e.g. 3-letter passwords from 26 letters, repeats allowed → 26³*
- Combinations with repetition (stars & bars): `C(r+n-1, r) = C(r+n-1, n-1)` — pick `r` items from `n` types, repeats allowed, order doesn't matter. Derivation trick: encode as `r` stars + `(n-1)` bars in a row, count arrangements.
- Constrained non-negative integer solutions: for `x₁+x₂+...+xₙ=r`, each `xᵢ≥0` → same as above: `C(r+n-1, n-1)`. If each `xᵢ≥mᵢ` (minimum required): substitute `yᵢ=xᵢ-mᵢ`, solve for `y`'s with `Σyᵢ=r-Σmᵢ`, apply the same formula on the reduced total.
- Polynomial/generating-function method: when variables also have an **upper bound** (`mᵢ≤xᵢ≤Mᵢ`), plain stars-and-bars breaks — take the coefficient of `xʳ` in the product `(x^{m₁}+...+x^{M₁})(x^{m₂}+...+x^{M₂})...`. Low-yield unless a question explicitly caps values.
- Inequality solutions (slack variable trick): for `x₁+x₂+...+xₙ≤r`, add a slack variable `xₙ₊₁≥0` to convert to `x₁+...+xₙ+xₙ₊₁=r`, then apply the stars-and-bars formula normally.
- **Priority:** the plain stars-and-bars form and the constrained-minimum variant are the ones that show up as direct GATE/ISRO-style numericals. The generating-function method is an extension — know it exists, don't over-invest.
- *Worked clarification — `C(13,11)` vs `C(13,3)`:* for `x₁+x₂+x₃=11`, each `xᵢ≥0`: `r=11` (stars), `n=3` (variables) → **bars needed = `n-1=2`**, not `n=3`. Total slots = `r+(n-1) = 11+2 = 13`. From those 13 slots: choose which 11 are stars → `C(13,11)`, or choose which 2 are bars → `C(13,2)` — both give 78 by the symmetry identity `C(n,k)=C(n,n-k)`. `C(13,3)` would only be right with 4 variables (`n-1=3` bars) or `r=3` — the trap is using the variable-count directly instead of variable-count-minus-one for the bars.

**4. Pigeonhole Principle**
*(standardized letters: `k` = holes/categories, `t` = target per hole, `n` = items/pigeons — GFG's own examples swap `n`/`k` inconsistently between problems, so ignore the page's lettering and track roles instead: "how many distinct categories?" = `k`, "how many of the same category do I want guaranteed?" = `t`.)*

- **Basic form:** if `n` items go into `k` holes and `n>k`, at least one hole has **≥2** items. *Ex: 13 pigeons, 12 holes → some hole has ≥2.*
- **Generalized form:** some hole holds at least `⌈n/k⌉` items. *Ex: 100 students, 12 birth months → `⌈100/12⌉=9` share a month.*
- **Inverse form (the one exam questions actually ask for):** minimum items to guarantee target `t` in some hole: `n = k(t-1)+1`. Reasoning: worst case fills every hole to `t-1` first (`k(t-1)` items, target still unmet anywhere) — the next item forces one hole to `t`.
  - *Socks* (k=2 colors, t=2 for a pair): `2(2-1)+1 = 3` socks.
  - *Marbles* (k=3 colors, t=4): `3(4-1)+1 = 10` marbles.
- **Averaging form:** if average `A=n/k` isn't whole, some hole has `≥⌈A⌉`. *Ex: `kt+1` pigeons in `k` holes → average `=t+1/k` → some hole gets `⌈t+1/k⌉=t+1` — this is just the inverse formula rewritten.*
- **Strong form (unequal targets per hole):** if hole `i` needs to hit target `qᵢ` to "count," minimum items needed: `n = (q₁+q₂+...+qₖ) - k + 1`. *Ex: need 10 first-yr OR 8 second-yr OR 6 third-yr OR 4 final-yr → `10+8+6+4-4+1=25`.* Watch for the mixed version where some categories have low caps (e.g. only 6 red balls exist so target caps at 6) — solve capped categories separately (add them fully), then apply the formula only to the uncapped rest.
- **Common "hidden pigeonhole" proof patterns** (GATE occasionally tests the idea, not full derivation):
  - Remainders as holes: 52 integers → 51 possible remainders mod 51 → two share a remainder → their difference divisible by 51.
  - Counting ranges as holes: 1001 people, friend-counts range over ≤1000 values → two people have equal friend count.
  - Geometric grid as holes: 5 points in a unit square, split into 4 sub-squares → 2 points share a sub-square, bounded by its diagonal.
  - Sequence-length assignment: 101 distinct reals → assign each a pair of (longest increasing run, longest decreasing run) → pigeonhole forces one run ≥11.
  - Subset-sum collision: 10 integers → 2¹⁰=1024 subsets, sum range smaller → two subsets share a sum.
- **Priority:** basic/generalized/strong numeric forms are highest ROI. The averaging form is the same idea restated. The proof patterns are worth recognizing by shape (remainder/range/grid-as-hole) since ISRO papers sometimes phrase pigeonhole as "prove that..." rather than a plain numeric question — don't memorize each proof word-for-word.

---
## Discrete Mathematics — Graphs

**1. Graph Theory Basics**
- `G=(V,E)`. Degree = edges incident (self-loop counts **twice**). Isolated vertex = degree 0. Pendant vertex = degree 1.
- **Handshaking theorem**: `2|E| = Σ deg(u)` (undirected); directed: `Σ in-deg = Σ out-deg = |E|`.
- Fact: any undirected graph has an **even number** of odd-degree vertices.
- Edge counts: `Kₙ → n(n-1)/2`, cycle `Cₙ → n`, wheel `Wₙ → 2(n-1)`, hypercube `Qₙ → n·2ⁿ⁻¹` (over `2ⁿ` vertices), complete bipartite `K_{m,n} → m·n`.
- Bipartite ⟺ 2-colorable (no odd cycle).
- *Worked examples (from page):*
  - Path A-B-C-D: degree(A)=1, B=2, C=2, D=1.
  - Triangle (3-cycle) A-B-C-A: **not bipartite** — odd cycle.
  - Handshaking check: 4 vertices, 3 edges → `2e=6` ✓ (e = edge count; ✓ just marks the identity checks out).
  - `K₅` edges: `5×4/2 = 10`. Wheel `W₆` edges: `2×5=10`.

**2. Planar Graphs and Coloring**
- Planar = drawable with zero edge crossings. **Euler's formula** (connected): `V - E + F = 2`.
- Necessary condition: `E ≤ 3V - 6` (fails this → definitely not planar; passes it → not proof of planarity, just doesn't rule it out).
- **Kuratowski's theorem**: planar ⟺ contains no `K₅` or `K_{3,3}` subgraph/subdivision.
- Chromatic number = min colors for proper vertex coloring. **Four Color Theorem** (standard add-on, essential for this topic though not explicit on the source page): every planar graph's chromatic number ≤ 4.
- *Page has no worked example — added for practice:* Graph with V=6, E=10 → check `3(6)-6=12 ≥ 10` → passes the necessary test, still needs an actual planar drawing to confirm.

**3. Graph Isomorphism and Connectivity**
- Isomorphic ⟺ a vertex bijection preserving adjacency exists. **Necessary (not sufficient) checks**: same `|V|`, same `|E|`, same degree sequence, same connection pattern.
- `κ(G)` = min vertices to remove to disconnect. `λ(G)` = min edges to remove to disconnect.
- *Page has no worked example — added for practice:* Two graphs can share the exact same degree sequence and still **not** be isomorphic — always verify by attempting the actual vertex mapping; degree-sequence match alone is a red flag check, not proof.

**4. Matching in Graph Theory**
- `M ⊆ E`, no two edges share a vertex. **Maximal** = can't add another edge. **Maximum** = largest possible `|M|`. **Perfect** = every vertex covered exactly once.
- *Flagged source error:* the page's own worked example gave `M = {AB, CD, DE}` as a valid matching, but `CD` and `DE` both touch vertex D — that violates the matching definition it just stated. From the edge list, `EF` is a valid edge; the intended matching was almost certainly `{AB, CD, EF}` (a **perfect matching** covering all 6 vertices A–F with no shared vertex) — `DE` looks like a typo for `EF`.
- **Takeaway check to run on any "is this a valid matching?" question:** list each edge's two endpoints, confirm no vertex repeats across the set.

**5. Euler and Hamiltonian Paths**
- Euler circuit ⟺ **all** vertices even degree. Euler path (no circuit) ⟺ **exactly 2** odd-degree vertices. `>2` odd vertices ⟺ neither exists.
- **Dirac's theorem**: n≥3 vertices, every vertex degree `≥ n/2` ⟹ Hamiltonian cycle exists (sufficient, not necessary).
- **Ore's theorem**: for every non-adjacent pair `u,v`, `deg(u)+deg(v) ≥ n` ⟹ Hamiltonian cycle exists.
- *Worked examples (from page):*
  - `{AB,BC,CD,DA,AC}`: degrees A(3),B(2),C(3),D(2) → A,C odd → **no Euler circuit**.
  - `{PQ,QR,RS,SP,PR}`: degrees P(3),Q(2),R(3),S(2) → exactly 2 odd → **Euler path exists**: `P-S-R-Q-P-R`.
  - `K₅` (complete graph on 5 vertices — the subscript is a concrete value, not the variable `n`) → always Hamiltonian for n≥3: `1-2-3-4-5-1`.
  - `K_{3,3}`: all degree 3 (odd) → no Euler circuit; **does** have a Hamiltonian cycle: `1-a-2-b-3-c-1`.
  - **Petersen graph**: 3-regular (odd) → no Euler circuit, and — famous exception — **no Hamiltonian cycle either**, despite looking "nice." Worth remembering as the standard counterexample.
  - Dirac check: n=8, every vertex degree≥4 (=n/2) → Hamiltonian cycle guaranteed.
- *Worked walkthrough (image example) — "Euler circuit not possible, but Euler path is":* Left graph, vertices A,B,C,D,E, edges A-E, A-B, E-C, B-C (a diamond) plus a C-D tail.
  - Degree check: A=2, B=2, E=2, C=3, D=1.
  - C and D are odd (degree 3 and 1); everything else even → exactly 2 odd vertices → **Euler path exists, circuit doesn't**.
  - Why the circuit fails specifically: D has degree 1 (only edge `C-D`) — enter D and there's no second edge to leave by, so you can never close the loop back to a start point. Any degree-1 vertex kills the circuit case outright.
  - The actual path, forced to start/end at the two odd vertices: `D → C → E → A → B → C`, using all 5 edges exactly once without returning to D.
  - **General rule to apply first on any Euler question:** count odd-degree vertices — `0` → circuit exists, `2` → path only (start/end forced at those two), `>2` → neither.

---
## Linear Algebra

**1. Introduction to Matrix**
- Order = rows×cols. Trace = sum of diagonal. Types worth knowing cold: symmetric (`Aᵗ=A`), skew-symmetric (`Aᵗ=-A`), orthogonal (`AAᵗ=I`), idempotent (`A²=A`), involutory (`A²=I`), singular (`det=0`) vs non-singular.
- Key inverse identities: `A⁻¹=adj(A)/|A|`; `A(adjA)=|A|I`; `|adjA|=|A|ⁿ⁻¹`; `adj(adjA)=|A|ⁿ⁻²A`; `(AB)⁻¹=B⁻¹A⁻¹`.
- *Worked examples (from page, A=[[1,2],[4,5]], B=[[2,3],[6,7]]):*
  - `A+B = [[3,5],[10,12]]`; `B-A = [[1,1],[2,2]]`; `3A = [[3,6],[12,15]]`
  - `AB = [[14,17],[38,47]]` *(row×column, e.g. top-left = 1×2+2×6=14)*
  - Transpose of `[[18,17],[38,47]]` → `[[18,38],[17,47]]`
  - Trace of `[[1,2,3],[4,5,6],[7,8,9]]` = `1+5+9 = 15`

**2. Determinants**
- `2×2`: `|A| = ad-bc`. *Worked example (from page):* `A=[[3,2],[2,3]] → |A| = 9-4 = 5`.
- *Page had no 3×3 example — added for practice:* `[[1,2,3],[0,1,4],[5,6,0]]` → expand along row 1: `1(1×0-4×6) - 2(0×0-4×5) + 3(0×6-1×5) = 1(-24)-2(-20)+3(-5) = -24+40-15 = 1`.

**3. Eigenvalues and Eigenvectors**
- `Av=λv`. Characteristic equation: `det(A-λI)=0`. Diagonalization: `A=XDX⁻¹`.
- *Worked examples (from page):*
  - `A=[[1,2],[5,4]]` → `λ=6` (eigenvector `[2,5]`), `λ=-1` (eigenvector `[1,-1]`).
  - `A=[[2,2,2],[2,2,2],[2,2,2]]` → `λ=6,0,0`; eigenvectors `[-1,1,0],[-1,0,1],[1,1,1]`.
  - Same matrix, diagonalized: `D=diag(6,0,0)`, `X=[[1,1,1],[1,-1,0],[1,0,-1]]`.
  - Upper-triangular `[[1,1,0],[0,1,1],[0,0,1]]` → repeated `λ=1` (triple), eigenvector `k[1,0,0]` — **watch for this pattern**: repeated eigenvalues on a triangular matrix often collapse to far fewer independent eigenvectors than the multiplicity suggests.
  - Scalar matrix `[[5,0],[0,5]]` → `λ=5,5`, eigenvectors `[1,0]` and `[0,1]` (here it *does* give 2 independent ones — contrast with the case above).

**4. System of Linear Equations**
- Methods: Cramer's Rule, Inverse method, Gauss elimination, LU decomposition — these four are the **direct** methods; Jacobi, Gauss-Seidel, SOR are the **iterative** methods (the "(direct)"/"(iterative)" labels split the list into these two top-level categories — LU decomposition is one of the direct methods, not its own separate category).
- Consistent (≥1 solution) vs inconsistent (none, parallel lines geometrically). `rank(A)` vs `rank([A|b])` decides it.
- *Page had no worked example — added for practice (Cramer's Rule):* `x+y=5`, `2x-y=1`. `det(A)=[[1,1],[2,-1]]=-1-2=-3`. `x = det([[5,1],[1,-1]])/-3 = (-5-1)/-3 = 2`. `y = det([[1,5],[2,1]])/-3 = (1-10)/-3 = 3`.

**5. LU Decomposition**
- `A = L×U` (L lower-triangular with 1's on diagonal, U upper-triangular). Solve via `Ly=b` then `Ux=y`.
- *Worked example (from page):* system `x₁+x₂+x₃=1`, `4x₁+3x₂-x₃=6`, `3x₁+5x₂+3x₃=4` → `L=[[1,0,0],[4,1,0],[3,-2,1]]`, `U=[[1,1,1],[0,-1,-5],[0,0,-10]]`. Forward-sub gives `z=(1,2,5)`, back-sub gives **`x₁=1, x₂=0.5, x₃=-0.5`**.

---
## Calculus

**1. Limits**
- Algebra of limits: sum/diff/product/quotient of limits = limit of sum/diff/product/quotient.
- Standard limits: `lim(x→a)(xⁿ-aⁿ)/(x-a)=naⁿ⁻¹`; `lim(x→0)sinx/x=1`; `lim(x→0)tanx/x=1`; `lim(x→0)(eˣ-1)/x=1`; `lim(x→∞)(1+1/x)ˣ=e`.
- *Worked examples (from page):*
  - `lim(x→6) x/3 = 2`
  - `lim(x→2)(x²-4)/(x-2)` → factor `(x-2)(x+2)/(x-2) = x+2 → 4`
  - `lim(x→1/2)(2x-1)/(4x²-1)` → factor denominator `(2x-1)(2x+1)` → cancel → `1/(2x+1) = 1/2`
  - Piecewise sign function: right-hand limit at 0⁺ = 1 (only the `x>0` branch matters approaching from the right).

**2. Continuity**
- 3-part test at `x=a`: `f(a)` defined, `lim(x→a)f(x)` exists (LHL=RHL), and they're equal to `f(a)`.
- Discontinuity types: **jump** (LHL≠RHL, both exist), **removable** (limit exists but ≠ f(a) or f(a) undefined), **infinite** (limit → ±∞).
- *Worked examples (from page):*
  - `sin(x)` at 0: LHL=RHL=f(0)=0 → **continuous**.
  - `f(x)=x+1 (x<3), x+5 (x≥3)` at x=3: LHL=4, RHL=8 → **jump discontinuity**.
  - `f(x)=(x²-1)/(x-1)` at x=1: cancels to `x+1`, LHL=RHL=2, but `f(1)` undefined → **removable** (redefine `f(1)=2` to fix).
  - `f(x)=1/x` at x=0: LHL=-∞, RHL=+∞ → **infinite discontinuity**.
  - Find `m` so `f(x)=mx+5 (x≠9), 8x (x=9)` is continuous at 9: `9m+5 = 72 → m=7.444`. *(Common GATE pattern: set LHL=RHL=f(a) and solve for the unknown parameter.)*
  - *(4 more worked variants — piecewise, factorization, trig-limit, two-parameter — exist on the page if you want extra reps on the same LHL=RHL technique.)*

**3. Differentiability**
- `f'(a)` exists ⟺ `lim(h→0)[f(a+h)-f(a)]/h` exists and is finite. **Differentiable ⟹ continuous** (not reverse).
- Test: compute LHD and RHD separately; equal & finite ⟺ differentiable.
- *Worked examples (from page):*
  - Greatest integer function `[x]` at x=1: `Rf'=0`, `Lf'=∞` → **not differentiable**. Same result at x=2.
  - Piecewise with `e^(1/x)` at x=0: `Rf'(0)=1`, `Lf'(0)=-1` → mismatch → **not differentiable**.
  - `f(x)=1+x (x<2), 5-x (x≥2)` at x=2: `Lf'=1`, `Rf'=-1` → **not differentiable** (classic "corner point" case).

**4. Lagrange's MVT**
- `f` continuous on `[a,b]`, differentiable on `(a,b)` ⟹ ∃c: `f'(c) = [f(b)-f(a)]/(b-a)`.
- *Worked example (from page):* `f(x)=x²` on `[1,3]`: slope `=(9-1)/2=4`. `f'(x)=2x=4 → c=2` ✓ (inside the interval, as required).
- *(Page also has sin(x) on [0,π/2] → c=arccos(2/π)≈0.6435, and ln(x) on [1,e] → c=e-1, if you want variety beyond polynomials.)*

**5. Absolute Minima and Maxima**
- Extreme Value Theorem: continuous on `[a,b]` ⟹ absolute max & min both exist on it.
- Procedure: find critical points (`f'=0`), evaluate `f` there **and** at the endpoints, compare.
- *Worked examples (from page):*
  - `f(x)=5x+2` on `[0,2]`: no critical points (`f'=5` always) → min=f(0)=2, max=f(2)=12.
  - `f(x)=x²-2x+5` on `[0,2]`: critical point x=1 → f(1)=4 (min); f(0)=f(2)=5 (max).
  - `f(x)=1/(x+4)` on `[0,1]`: no critical points → max=f(0)=1/4, min=f(1)=1/5.
  - `f(x)=x³-2x²+5` on `[-2,2]`: critical points x=0, 4/3 → min=f(-2)=-11; max=f(0)=f(2)=5.

**6. Indefinite Integrals**
- `∫xⁿdx=xⁿ⁺¹/(n+1)+C`; `∫eˣdx=eˣ+C`; `∫1/x dx=ln|x|+C`; `∫sinx dx=-cosx+C`; `∫cosx dx=sinx+C`.
- *Worked examples (from page):*
  - `∫(sinx+1)dx = -cosx+x+C`
  - `∫2eˣdx = 2eˣ+C`
  - `∫(5x⁻²)dx = -5/x+C` *(note: page's "5x-2" means `5x⁻²`, not `5x-2` — watch this exact notation trap)*
  - `∫(sinx+5cosx)dx = -cosx+5sinx+C`
  - `∫(5x⁻²+x⁴+x)dx = -5/x + x⁵/5 + x²/2 + C`

---
## Probability & Statistics

**1. Random Variable**
- Maps sample space → real numbers, `X:S→R`. Discrete → PMF (`Σp(xᵢ)=1`). Continuous → PDF (`∫f(x)dx=1`).
- *Worked examples (from page):*
  - 2 coins tossed, `X`=number of heads → sample space `{HH,HT,TH,TT}`.
  - Die roll: `P(X=i)=1/6` for each face, `Σ=1` ✓.
  - `S={0,1,2}`, given `P(X=1)=0.3, P(X=2)=0.5` → solve `P(X=0)=1-0.3-0.5=0.2`.
  - Continuous: `f(x)=kx³` on `[0,3]` → solve `k=4/81` from `∫f=1`; then `P(1<X<2)=15/81`.

**2. Normal Distribution**
- `f(x)=(1/(σ√2π))e^(-(x-μ)²/2σ²)`. Symmetric about μ; mean=median=mode.
- Empirical rule: 68% within 1σ, 95% within 2σ, 99.7% within 3σ.
- *Page has no worked example — added for practice:* test scores `μ=70, σ=10` → 68% of students score between `60-80`; 95% between `50-90`.

**3. Binomial Distribution**
- `P(X=r) = nCr·pʳ(1-p)ⁿ⁻ʳ`. Mean `=np`, Variance `=npq`, SD `=√(npq)`.
- *Worked examples (from page):*
  - Coin×3, exactly 2 heads: `3C2(0.5)²(0.5)¹ = 0.375`
  - Coin×20, exactly 10 heads: `C(20,10)(0.5)¹⁰(0.5)¹⁰ ≈ 0.176` *(the source text's `¹⁰C₂₀` is a typo — it's `C(20,10)`, top number = total trials, bottom = successes wanted)*
  - Coin×20, mean `=20×0.5=10`; variance `=20×0.5×0.5=5`; SD `=√5≈2.23`

**4. Mean, Median, Mode**
- `Mean=Σxᵢ/n`. Median: odd n → `[(n+1)/2]`th term; even n → avg of `(n/2)`th and `(n/2+1)`th terms. Mode = highest-frequency value.
- *Worked examples (from page):*
  - `{10,30,40,20,50}` → mean `=30`
  - Sorted `{10,20,30,40,50}`, n=5 (odd) → median = 3rd term = `30`
  - `{1,2,2,2,3,3,4,5}` → mode `=2` (appears 3×)
  - Even-length `{5,12,15,22,23,24,25,25}` → median `=(22+23)/2=22.5`
- *Note: this specific page only covers ungrouped data. **Grouped-data formulas** (needed if a GATE question gives a frequency table with class intervals) aren't on this page — worth a separate lookup if you hit one: `Median = l + [(n/2-cf)/f]×h`, `Mode = l + [(f₁-f₀)/(2f₁-f₀-f₂)]×h`.*

**5. Conditional Probability**
- `P(B|A) = P(A∩B)/P(A)`. Multiplication rule: `P(A∩B)=P(A)×P(B|A)`. Independent events: `P(A∩B)=P(A)P(B)`.
- *Worked examples (from page):*
  - Rain 30% of days, umbrella 50% of days, both 20% of days (2 of 10) → `P(Rain|Umbrella) = 2/5 = 40%`
  - Two independent coin tosses: `P(B|A)=P(B)=0.5` (conditioning on an independent event changes nothing)
  - Drawing 2 red cards without replacement: after 1st red drawn, `25 red / 51 total` left → `P(2nd red|1st red) ≈ 0.49`

**6. Bayes's Formula**
- 2-event: `P(A|B) = P(B|A)P(A)/P(B)`. n-event (partition): `P(Eᵢ|A) = P(Eᵢ)P(A|Eᵢ) / ΣP(Eₖ)P(A|Eₖ)`.
- *Page has no numeric worked example — added for practice (classic disease-test problem):* 1% of a population has a disease. Test is 90% sensitive (catches 90% of sick people) and 90% specific (correctly clears 90% of healthy people). Given a positive test, `P(disease|positive)`?
  - `P(D)=0.01`, `P(pos|D)=0.9`, `P(pos|¬D)=0.1`
  - `P(pos) = 0.9×0.01 + 0.1×0.99 = 0.009+0.099 = 0.108`
  - `P(D|pos) = 0.009/0.108 ≈ 0.083` (only ~8.3%! — the classic "even a good test is unreliable when the disease is rare" GATE-style trap.)

---

**Flagged gaps:** Planar Graphs, Isomorphism/Connectivity, System of Linear Equations, Normal Distribution, and Bayes's pages had **no worked numeric example** on the source — the ones added above are supplementary, not the page's own, so treat them as a starting point and hunt down 1-2 more practice problems per topic separately once you get there.
