# HP ProOne 440 G9 — Data Science & AI (Classical/CPU)

**Machine**: HP ProOne 440 23.8" G9 All-in-One (Intel i7-14700, 28 threads @ 5.4GHz, 16GB RAM, no dGPU, Kali GNU/Linux, always-plugged-in desktop)
**Field**: Data Science / AI (3rd priority)
**Character**: strongest CPU of the three idle machines, stationary and always-on — best suited as a continuously-running data pipeline / classical-ML service. No discrete GPU, so deep learning stays in `garuda-gpu.md`; this file is classical ML, statistics, classical computer vision, and CPU-heavy data engineering.

Every idea below is inspired by `../topics/gfg-isro-topic-map.md` and `../topics/gfg-gate-topic-map.md`. Each carries exactly one reference link. Ideas run as dev → deploy (days to 1-2 weeks) → analyze cycles.

The Databases section here is the **heaviest CPU-only tier** of a topic whose lighter versions live in `rpi5-cs-eng.md` (Tier 1) and `probook-cybersec.md` (Tier 2).

---

## Mathematics (Probability, Statistics & Linear Algebra — ML foundations)

- **Distribution-Fitting Toolkit** — implement PDF/CDF and MLE-based parameter fitting for Normal/Binomial/Poisson from scratch, validate against SciPy, deploy as a service other tasks can query. Ref: [Probability Distribution](https://www.geeksforgeeks.org/maths/probability-distribution/)
- **Bayesian Inference Engine (Naive Bayes as the running example)** — implement a Bayes'-theorem-driven classifier from scratch, deploy it classifying a real data stream you generate for a week. Ref: [Bayes's Formula](https://www.geeksforgeeks.org/maths/bayes-theorem/)
- **Eigen-Decomposition-Based PCA from Scratch** — implement eigenvalue/eigenvector computation via power iteration without `numpy.linalg`, validate against scikit-learn's PCA. Ref: [Eigenvalues and Eigenvectors](https://www.geeksforgeeks.org/engineering-mathematics/eigen-values/)

## AI/ML — Supervised Learning (Classical)

- **Linear / Ridge / Logistic Regression from Scratch** — implement gradient descent + closed-form solutions, benchmark vs scikit-learn, deploy as a small prediction API ingesting real telemetry you collect for a week. Ref: [Linear Regression](https://www.geeksforgeeks.org/machine-learning/linear-regression-python-implementation/)
- **KNN vs Naive Bayes vs SVM Bake-Off** — implement all three on the same dataset, deploy, compare accuracy/latency/memory over a week of varied inputs. Ref: [K-Nearest Neighbor](https://www.geeksforgeeks.org/machine-learning/k-nearest-neighbours/)
- **Decision Tree / Random Forest from Scratch** — implement recursive splitting with Gini/entropy criteria, benchmark against scikit-learn's `RandomForestClassifier`. Ref: [Random Forest Algorithm](https://www.geeksforgeeks.org/machine-learning/random-forest-algorithm-in-machine-learning/)
- **Cross-Validation & Bias-Variance Study** — build a harness that runs k-fold CV across model complexities, plot the bias-variance tradeoff empirically. Ref: [Bias-Variance Trade-off](https://www.geeksforgeeks.org/machine-learning/ml-bias-variance-trade-off/)

## AI/ML — Unsupervised Learning

- **K-Means / K-Medoids from Scratch + Convergence Visualizer** — deploy clustering a real dataset you continuously collect for a week, log convergence iterations/inertia over time. Ref: [K-Means/K-Medoid](https://www.geeksforgeeks.org/machine-learning/ml-k-medoids-clustering-with-example/)
- **Hierarchical Clustering with Dendrogram Renderer** — implement single/average/ward linkage, render dendrograms from scratch. Ref: [Hierarchical Clustering](https://www.geeksforgeeks.org/machine-learning/hierarchical-clustering/)
- **Dimensionality-Reduction Pipeline (PCA → Clustering)** — chain your own PCA with your own K-Means, deploy on high-dimensional real data (e.g. system-metrics or network-feature vectors). Ref: [Dimensionality Reduction](https://www.geeksforgeeks.org/machine-learning/dimensionality-reduction/)

## AI/ML — Search & Game AI

- **A\* / Uniform-Cost / Greedy-Best-First Pathfinder on Real Maps** — implement all three over a real road-network graph dataset, compare optimality/speed. Ref: [A* Search](https://www.geeksforgeeks.org/dsa/a-search-algorithm/)
- **Minimax + Alpha-Beta Pruning Game Engine (Tic-Tac-Toe / Connect-4)** — deploy as a playable service, log pruning efficiency vs plain minimax across game-tree depths. Ref: [Minimax Algorithm](https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-1-introduction/)

## Image and Vision Processing (Classical CV, CPU-bound)

- **Edge Detection & Morphology Suite from Scratch (Sobel, Canny, erosion/dilation)** — implement without OpenCV's built-ins first, then compare, deploy processing a week's worth of webcam/camera images. Ref: [Image Processing in Python](https://www.geeksforgeeks.org/image-processing-in-python/)
- **Custom-Transform Image Compression (block-based DCT, mini-JPEG)** — implement block-based DCT compression, measure compression ratio vs quality loss. Ref: [Introduction to Data Compression](https://www.geeksforgeeks.org/computer-networks/introduction-to-data-compression/)
- **Image Segmentation from Scratch (Thresholding + Watershed)** — implement global/adaptive thresholding and a basic watershed algorithm, deploy segmenting a week's worth of collected images, measure segmentation quality against manually labeled ground truth. Ref: [Image Processing in Python](https://www.geeksforgeeks.org/image-processing-in-python/)
- **Feature/Corner Detection from Scratch (Harris Corner Detector)** — implement the Harris response computation directly on pixel data, deploy detecting keypoints across a stream of images, compare stability of detected points across near-duplicate frames. Ref: [Image Processing in Python](https://www.geeksforgeeks.org/image-processing-in-python/)
- **Video Motion-Detection Pipeline (Frame Differencing)** — build a real-time frame-differencing motion detector, deploy watching a real camera feed for a week, log false-positive/negative rates against a manually reviewed sample. Ref: [Image Processing in Python](https://www.geeksforgeeks.org/image-processing-in-python/)

## General Aptitude → NLP Crossover *(previously excluded — reframed as real NLP mini-projects)*

- **Grammar / Subject-Verb-Agreement Checker (Rule-Based + ML Classifier)** — build a rule-based checker first, then a small ML classifier trained on labeled correct/incorrect sentences, compare their error-detection rates. Ref: [Subject-Verb Agreement](https://www.geeksforgeeks.org/english/subject-verb-agreement/)
- **Reading-Comprehension Extractive QA Model** — build a simple extractive question-answering pipeline (TF-IDF/embedding similarity based) over a corpus of passages, deploy answering a week's worth of generated questions, measure accuracy. Ref: [Reading Comprehension Questions](https://www.geeksforgeeks.org/english/reading-comprehension-questions/)
- **Idiom/Phrase Detector in Text (NLP Pattern Matching)** — build a detector that flags idiomatic expressions in arbitrary text using a curated idiom list plus fuzzy matching, deploy over a week's worth of real text (articles, chat logs), measure precision/recall. Ref: [30 Most Common Idioms and Phrases](https://www.geeksforgeeks.org/english/30-most-common-idioms-and-phrases/)

## Databases *(Tier 3 — heaviest CPU-only tier; Tier 1 in `rpi5-cs-eng.md`, Tier 2 in `probook-cybersec.md`)*

- **Multi-Node Replicated Key-Value Store (Raft or simplified leader-follower)** — deploy a 3-node cluster across ProOne/ProBook/Pi, run it for a week under simulated network hiccups, analyze consistency/failover behavior. Ref: [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)
- **OLTP vs OLAP Workload Simulator** — build a toy engine that can run in row-store or column-store mode, benchmark the same analytical queries in both, quantify the OLAP advantage. Ref: [OLTP vs OLAP](https://www.geeksforgeeks.org/dbms/differences-between-operational-database-systems-and-data-warehouse/)
- **Schemaless NoSQL Document Store from Scratch** — implement basic CRUD + secondary indexing on JSON documents, compare query patterns against the Pi's relational mini-engine. Ref: [Introduction to NoSQL](https://www.geeksforgeeks.org/nosql/introduction-to-nosql/)
