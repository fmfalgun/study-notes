# Linear Algebra — GATE 2027 (CS + DA)

**Syllabus basis:** CS: matrices, determinants, systems of linear equations, eigenvalues and eigenvectors, LU decomposition. DA adds: vector spaces, subspaces, linear dependence, rank/nullity, projections, quadratic forms, Gram-Schmidt, SVD.
Items marked **[DA]** are DA-only. If you pick CS you can skip them.
**Hbk** column: the Arihant Handbook has no Maths chapter, so it is "—".
**Links:** only GFG URLs returned by search are used. NPTEL links for this subject are still unverified, so search "NPTEL Linear Algebra" yourself and paste the one you like under *My links* at the bottom.

## Checklist (index)

Tick the boxes as you go. Legend: C = concept, N = notes, P = PYQ, E = error log, R1 / R2 = revision rounds.

| # | Topic | Hbk | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Matrix types and operations (symmetric, orthogonal, idempotent, nilpotent) | — | [LMN Linear Algebra](https://www.geeksforgeeks.org/lmns-linear-algebra/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Determinant and its properties, adjoint, inverse | — | [LMN Engg Maths](https://www.geeksforgeeks.org/engineering-mathematics/last-minute-notes-engineering-mathematics/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Rank of a matrix, row echelon form | — | [Row Echelon Form](https://www.geeksforgeeks.org/row-echelon-form/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | System of linear equations (consistency, unique / infinite / none) | — | [Gaussian Elimination](https://www.geeksforgeeks.org/dsa/gaussian-elimination/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Eigenvalues, eigenvectors, Cayley-Hamilton | — | [LMN Linear Algebra](https://www.geeksforgeeks.org/lmns-linear-algebra/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | LU decomposition | — | [LU Decomposition](https://www.geeksforgeeks.org/engineering-mathematics/l-u-decomposition-system-linear-equations/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Null space, column space, rank-nullity **[DA]** | — | [Null Space](https://www.geeksforgeeks.org/engineering-mathematics/null-space-of-a-matrix/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Quadratic forms, definiteness **[DA]** | — | [Quadratic Form](https://www.geeksforgeeks.org/engineering-mathematics/quadratic-form-of-a-matrix/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Projection matrices **[DA]** | — | [LMN Linear Algebra](https://www.geeksforgeeks.org/data-science/lmns-linear-algebra/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | SVD **[DA]** | — | [SVD](https://www.geeksforgeeks.org/data-science/singular-value-decomposition-svd/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [Matrices PYQs](https://www.geeksforgeeks.org/engineering-mathematics/matrices-pyqs/), [Doolittle LU](https://www.geeksforgeeks.org/dsa/doolittle-algorithm-lu-decomposition/), [GFG Linear Algebra short-notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20251126180646176778/Linear-Algebra-Short-Notes.pdf).

**My links:** (NPTEL / textbook, add here)

---

## 1. Matrix types
- Symmetric: Aᵀ = A. Skew-symmetric: Aᵀ = −A (diagonal is 0).
- Orthogonal: AᵀA = I, so det = ±1 and the eigenvalues have |λ| = 1.
- Idempotent: A² = A. Eigenvalues are 0 or 1, and trace = rank.
- Nilpotent: Aᵏ = 0. All eigenvalues are 0.
- (AB)ᵀ = BᵀAᵀ and (AB)⁻¹ = B⁻¹A⁻¹.

## 2. Determinant and inverse
- det(AB) = det A · det B. det(Aᵀ) = det A. det(kA) = kⁿ det A for an n×n matrix.
- A row swap flips the sign. Adding a multiple of one row to another leaves det unchanged.
- A⁻¹ = adj(A)/det(A). det(adj A) = det(A)ⁿ⁻¹.
- Triangular matrix: det is the product of the diagonal.

## 3. Rank
- Rank is the number of non-zero rows in the row echelon form. rank(A) ≤ min(m, n).
- rank(AB) ≤ min(rank A, rank B).

## 4. Linear systems AX = B (n unknowns)
| Condition | Result |
|---|---|
| rank(A) = rank([A:B]) = n | unique solution |
| rank(A) = rank([A:B]) < n | infinite solutions (n − r free variables) |
| rank(A) < rank([A:B]) | no solution |

Homogeneous AX = 0 always has the trivial solution. It has non-trivial solutions iff rank < n (for square A, iff det = 0).

## 5. Eigenvalues
- Characteristic equation: det(A − λI) = 0.
- Sum of eigenvalues = trace. Product of eigenvalues = det.
- Eigenvalues of A⁻¹ are 1/λ. Of Aᵏ they are λᵏ. Of A + cI they are λ + c.
- Triangular matrix: the eigenvalues are the diagonal entries.
- Cayley-Hamilton: A satisfies its own characteristic equation. For 2×2, A⁻¹ = (trace(A)·I − A)/det(A).
- Eigenvectors for distinct eigenvalues are linearly independent. Symmetric matrices have real eigenvalues and orthogonal eigenvectors.

## 6. LU decomposition
A = LU, with L unit lower-triangular (the multipliers) and U upper-triangular (the result of Gaussian elimination). To solve AX = C, solve LZ = C by forward substitution, then UX = Z by back substitution.

## 7. [DA] Subspaces
- rank(A) + nullity(A) = number of columns.
- Row rank = column rank.

## 8. [DA] Quadratic forms
Q(x) = xᵀAx with A symmetric. All eigenvalues > 0 means positive definite. All ≥ 0 means positive semidefinite. Mixed signs mean indefinite.

## 9. [DA] Projection
P is a projection if P² = P. The orthogonal projection onto the column space of A is P = A(AᵀA)⁻¹Aᵀ. This P is symmetric.

## 10. [DA] SVD
A = UΣVᵀ. The singular values are σᵢ = √(eigenvalues of AᵀA), with σ₁ ≥ σ₂ ≥ … ≥ 0. rank(A) is the number of non-zero singular values.

---

## Worked examples (all recomputed in code)

**E1: rank and consistency.** A = [[1,2,3],[2,4,6],[1,1,1]]. Row 2 = 2 × Row 1, so the rows are dependent. rank(A) = **2**. For AX = B with n = 3 unknowns, rank < n, so there are either infinitely many solutions or none. Which one depends on whether rank([A:B]) is also 2.

**E2: parameter in a system.** The matrix [[1,1,1],[1,2,3],[1,2,k]] has det = **k − 3**. So the system has a unique solution when k ≠ 3. At k = 3 it needs a rank check on the augmented matrix.

**E3: eigenvalues.** A = [[2,1],[1,2]]. trace = 4 and det = 3, so λ² − 4λ + 3 = 0 and **λ = 3, 1**. Check: 3 + 1 = 4 and 3 × 1 = 3.

**E4: Cayley-Hamilton inverse.** A = [[1,2],[3,4]]. Characteristic polynomial: λ² − 5λ − 2. Then A² − 5A − 2I = 0, so A(A − 5I) = 2I and A⁻¹ = (A − 5I)/2 = **[[−2, 1],[3/2, −1/2]]**. This matches the direct inverse.

**E5: LU.** A = [[4,3],[6,3]]. The multiplier is 6/4 = 3/2. L = [[1,0],[3/2,1]] and U = [[4,3],[0,−3/2]]. Check: LU = A.

**E6 [DA]: SVD.** A = [[1,1],[1,1]]. AᵀA has eigenvalues 4 and 0, so the singular values are **2 and 0**, and rank = 1.

---

## Notes / flags
- **Careful:** "trace = rank" holds only for idempotent matrices (such as projections), not in general. The GFG LMN page states it in a list of matrix properties, so read it in that context.
- Past-paper analysis is not included, as agreed. Add GATE 2022–2026 data here while studying.
