# Machine Learning — GATE 2027 (DA only; not in the CS paper)

**Syllabus basis (DA):** supervised learning (regression and classification; simple and multiple linear regression, ridge, logistic regression, k-nearest neighbour, naive Bayes, linear discriminant analysis, SVM, decision trees), bias-variance trade-off, cross-validation (LOO, k-fold), multi-layer perceptron and feed-forward networks; unsupervised learning (clustering: k-means / k-medoid, hierarchical, linkage; dimensionality reduction: PCA). Syllabus lists are from GFG pages, not the official PDF, so check against the official DA syllabus once.
**Hbk** column: the Arihant Handbook is a CS handbook and has **no ML chapter**. So there is no page column here. Use the GFG and textbook links.
**Links:** only URLs returned by search. NPTEL links are unverified; add yours under *My links*.
Only needed if you choose DA on ~27 Dec. If you stay with CS, skip this file.

## Checklist (index)

| # | Topic | Ref link | C | N | P | E | R1 | R2 |
|---|---|---|---|---|---|---|---|---|
| 1 | ML basics, train/test, bias-variance, cross-validation (LOO, k-fold) | [GATE DA notes (2027 syllabus)](https://www.geeksforgeeks.org/gate/gate-da-notes-according-to-gate-2025-syllabus/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Simple and multiple linear regression | [GATE DA notes (regression)](https://www.geeksforgeeks.org/gate/gate-da-notes-according-to-gate-2025-syllabus/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Ridge regression (and lasso for contrast) | [ML short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174515594826/MACHINE-LEARNING-SHORT--NOTES-GFG_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Logistic regression | [GATE DA notes](https://www.geeksforgeeks.org/gate/gate-da-notes-according-to-gate-2025-syllabus/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | k-nearest neighbour | [GATE DA notes](https://www.geeksforgeeks.org/gate/gate-da-notes-according-to-gate-2025-syllabus/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Naive Bayes classifier | [GATE DA notes](https://www.geeksforgeeks.org/gate/gate-da-notes-according-to-gate-2025-syllabus/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Linear discriminant analysis | [ML short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174515594826/MACHINE-LEARNING-SHORT--NOTES-GFG_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | SVM (margin, hard and soft, kernels) | [100 Days of GATE DA (list)](https://www.geeksforgeeks.org/gate/100-days-of-gate-data-science-ai/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Decision trees (entropy, information gain, Gini) | [ML short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174515594826/MACHINE-LEARNING-SHORT--NOTES-GFG_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Performance metrics: accuracy, precision, recall, F1, AUC, MSE, R² | [ML short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174515594826/MACHINE-LEARNING-SHORT--NOTES-GFG_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | Perceptron, multi-layer perceptron, feed-forward network, backprop | [100 Days of GATE DA (list)](https://www.geeksforgeeks.org/gate/100-days-of-gate-data-science-ai/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 12 | Clustering: k-means / k-medoid, hierarchical and linkage | [GATE DA notes](https://www.geeksforgeeks.org/gate/gate-da-notes-according-to-gate-2025-syllabus/) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| 13 | Dimensionality reduction: PCA | [ML short notes PDF](https://media.geeksforgeeks.org/wp-content/uploads/20250806174515594826/MACHINE-LEARNING-SHORT--NOTES-GFG_compressed.pdf) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

**Also useful:** [GATE DA subject-wise tips](https://www.geeksforgeeks.org/gate/gate-da-subject-wise-preparation-tips/) (suggests the Andrew Ng course for practice), [GATE DA syllabus 2027 list](https://www.geeksforgeeks.org/competitive-exam-experiences/gate-data-science-and-artificial-intelligence-syllabus/).

**My links:** (NPTEL / textbook, add here)

---

## 1. Basics
- Bias-variance: expected test MSE = bias² + variance + irreducible noise. Simple models: high bias, low variance (underfit). Complex: low bias, high variance (overfit).
- k-fold CV: train k times, each fold held out once; LOOCV is k = n (n fits).

## 2–3. Linear and ridge regression
- Simple: β₁ = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)², β₀ = ȳ − β₁x̄.
- Multiple: β̂ = (XᵀX)⁻¹Xᵀy. R² = 1 − SS_res/SS_tot. Adjusted R² penalizes extra predictors.
- Ridge: β̂ = (XᵀX + λI)⁻¹Xᵀy; shrinks coefficients (L2). Lasso uses L1 and can set coefficients exactly to 0. Increasing λ raises bias and lowers variance.

## 4. Logistic regression
- p = σ(wᵀx + b), σ(z) = 1/(1 + e⁻ᶻ). Loss (cross-entropy) = −mean[y log p + (1−y) log(1−p)].
- Gradient: ∂L/∂w = mean[(p − y)·x], ∂L/∂b = mean(p − y). Decision boundary is linear.

## 5–7. KNN, naive Bayes, LDA
- KNN: lazy learner; predict by majority of the k nearest points (Euclidean distance). Small k means high variance. Scale features first.
- Naive Bayes: P(c|x) ∝ P(c)·∏P(xᵢ|c), assuming conditional independence.
- LDA: common covariance, linear boundary; maximizes between-class over within-class scatter.

## 8–9. SVM and trees
- SVM margin = 2/‖w‖. Maximize margin ⇒ minimize ‖w‖². Support vectors are the points on the margin. Soft margin adds C·Σξ. Kernel trick replaces xᵀx′ with K(x, x′).
- Entropy H = −Σpᵢ log₂ pᵢ; information gain = H(parent) − weighted H(children). Gini = 1 − Σpᵢ².

## 10. Metrics
- Accuracy = (TP + TN)/N. Precision = TP/(TP + FP). Recall = TP/(TP + FN). Specificity = TN/(TN + FP). F1 = 2PR/(P + R).

## 11. Neural networks
- Neuron: o = σ(wx + b). Sigmoid derivative σ′ = σ(1 − σ). Squared-error loss ½(o − t)²: ∂L/∂w = (o − t)·σ′·x.
- A single perceptron can't learn XOR; an MLP with one hidden layer can.

## 12–13. Unsupervised
- k-means: assign to the nearest centroid, recompute means, repeat. Converges to a local optimum. Hierarchical: single linkage = min distance, complete = max, average.
- PCA: eigenvectors of the covariance matrix; variance explained by component = λᵢ/Σλ. Components are orthogonal.

---

## Worked examples (all recomputed in code)

**E1: Simple linear regression.** x = 1..5, y = 2, 4, 5, 4, 5: β₁ = **0.6**, β₀ = **2.2**, R² = **0.6**.

**E2: Ridge.** Same centred data, no intercept: slope = 0.6 at λ = 0 and **0.4** at λ = 5 (shrinks).

**E3: Metrics.** TP 40, FP 10, FN 20, TN 30: accuracy **0.70**, precision **0.80**, recall **0.667**, F1 **0.727**, specificity **0.75**.

**E4: Logistic, first step.** w = b = 0, x = 0, 1, 2, 3, y = 0, 0, 1, 1: every p = 0.5, loss = ln 2 = **0.693**, ∂L/∂w = **−0.5**, ∂L/∂b = **0**.

**E5: Naive Bayes.** Prior(yes) = 9/14, prior(no) = 5/14; P(sunny|yes) = 2/9, P(sunny|no) = 3/5; P(windy|yes) = 3/9, P(windy|no) = 3/5. Scores: yes = 1/21, no = 9/70, so P(yes|x) = **0.270**.

**E6: Information gain.** Parent (9, 5): H = **0.940**. Split into children (2, 3), (4, 0), (3, 2): gain = **0.247**.

**E7: k-means.** Points 1, 2, 9, 10, 11 with initial centres 1 and 9: clusters {1, 2} and {9, 10, 11}, centres **1.5** and **10**, stable after one update.

**E8: PCA.** Covariance [[4, 2], [2, 3]]: eigenvalues **1.438** and **5.562**; the first component explains 5.562/7 = 79.5% of the variance.

**E9: SVM and bias-variance.** w = (3, 4): margin = 2/5 = **0.4**. Bias² 4, variance 3, noise 1 ⇒ expected MSE = **8**.

**E10: Backprop, one neuron.** w = 0.5, b = 0, x = 1, target 1: o = **0.6225**, ∂L/∂w = **−0.0887**.

---

## Notes / flags
- Naive Bayes and decision-tree numbers use the standard play-tennis counts, not a GATE question.
- Your uploaded `ai-ml.md` covers linear and logistic regression, KNN, naive Bayes and k-medoids. It has no ridge, LDA, SVM, decision trees, metrics, neural networks, k-means vs hierarchical or PCA; those rows are the gaps.
- The Handbook has no ML coverage; GFG short notes are the quickest single source.
- Past-paper analysis is not included. Add GATE DA 2024–2026 data while studying.
