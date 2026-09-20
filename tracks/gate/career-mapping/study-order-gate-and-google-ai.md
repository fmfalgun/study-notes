# Study order: GATE 2027 and Google AI roles

Written 21 Sep 2026 from files we already saved (list at the end). No new research and no web lookups. Companion to `study-order-gate-and-google-redteam.md`; the two plans share most of the early weeks, see section 6.

## What this plan assumes and what is weaker than the red-team plan

- **Person:** the profile in `profile-fit-google.md`. AI-relevant strengths: Python, labelled dataset construction, classical ML (XGBoost/Random Forest IDS), security x ML, an LLM-agent research roadmap (AURA). Gaps: deep-learning frameworks 1/5, LLM work shipped 2/5, ML systems 1/5, research output 2/5.
- **Exam date:** not in our files. GATE is normally in early February (general knowledge, please confirm): about **19 weeks** from 21 Sep 2026. Shift the weeks if it differs.
- **The demand side is weaker than for cybersecurity.** We **never analysed Google AI job descriptions**. What we have for AI: (a) Google's AI role families from archived titles, 2019-2026 (`google-wayback-ai-analysis.md`): in 2026, ML/AI engineering 44%, infrastructure/hardware 15%, sales/GTM 15%, product/program 8%, research 6%, AI safety 3% (n = 239); (b) the AI skills seen on the career pages of Google, Anthropic, Meta, SAP, Adobe and Palo Alto Networks (`ai.md`); (c) AI wording in Google's 169 live security descriptions: 64 roles, 17 as a minimum; 15 live security roles have AI in the title and 13 of them ask 5+ years while 2 require a PhD. **Years of experience and requirements for general Google ML roles are not measured.**
- The ordering rules (prerequisites, daily practice) are my judgement; the weights and counts come from the saved files.

## 1. Decision first: which GATE paper?

Our files hold analysis for **both** GATE CS (8 sittings, 2022-2026) and **GATE DA (Data Science and AI; only 3 sittings, 2024-2026)**. The choice changes the plan:

| | GATE CSE | GATE DA |
|---|---|---|
| Subjects that also feed an AI role | Programming/DS, discrete maths, linear algebra, probability, algorithms, DBMS | Probability and statistics, DBMS, programming/DS, discrete maths, **machine learning, linear algebra, AI**, algorithms, calculus |
| Subjects that only serve the exam | OS, COA, digital logic, networks, TOC, compilers | (none of those) |
| Fit with the red-team goal | high (OS, COA, networks, compilers) | low |
| Your history | CSE rank 3547 in 2023 | not attempted (per the resume) |

**Recommendation from the files:** if red-team roles stay the main goal, **keep GATE CSE** and treat AI as a parallel hands-on track (variant 1). If the AI role becomes the main goal, GATE DA covers classical ML and AI inside the exam (variant 2). DA scores come from only 3 sittings, so treat them as weaker evidence.

## 2. Variant 1: GATE CSE + Google AI role

### Track A. Strict-order theory (finish each, then revise)

CSE scores from `exam-priority-report.md`. Order: prerequisites for machine learning first (they are also high-weight CSE topics), the CSE-only subjects last.

| # | Subject | Why here | GATE CSE (score) | Link to AI roles | Your status | Finish by |
|---|---|---|---|---|---|---|
| A1 | **C/Python programming core and data structures** | Coding is asked in every technical role; needed for everything | Tier 1 (51.6) | Python is the primary language in `ai.md` (with C++/CUDA); Google's coding minimum applies to AI roles too (general knowledge) | Python 4/5 | Week 2 |
| A2 | **Linear algebra** (matrices, rank, eigen, SVD) | First prerequisite of machine learning | Tier 2 (14.2) | "Strong math foundation: linear algebra, probability/statistics, optimization" (`ai.md`) | not shown | Week 4 |
| A3 | **Probability and statistics** (Bayes, distributions, expectation, hypothesis tests) | Second prerequisite of ML | Tier 3 (5.9, only 6 hits in 8 sittings) | same line; also the base of ML evaluation | not shown | Week 6 |
| A4 | **Discrete mathematics** (logic, combinatorics, graphs) | Tier 1 for the exam; graphs and logic feed search and algorithms | Tier 1 (30.6) | AI search / logic topics | not shown | Week 8 |
| A5 | **Algorithms** (with DSA practice) | Needs A1 and A4 | Tier 2 (10.9) | coding interviews | not shown | Week 9 |
| A6 | **Databases** | Data infrastructure and SQL | Tier 2 (16.8) | data pipelines, "Data infra: Spark, Ray, Airflow" (`ai.md`) | SQLite 3/5 | Week 11 |
| A7 | **Operating systems** | Needed for ML systems (processes, memory) and the exam | Tier 2 (13.4) | distributed/serving work (general knowledge) | Linux 4/5 | Week 12 |
| A8 | **COA and digital logic** | CPU/GPU memory hierarchy background | Tier 2 (14.9 and 15.0) | "CUDA, multi-GPU/TPU clusters" (`ai.md`) | hardware 2/5 | Week 14 |
| A9 | **Computer networks** | Exam only for this plan (strong already) | Tier 2 (14.8) | distributed training uses NCCL-type networking (general knowledge) | 4/5 | Week 15 |
| A10 | **Theory of computation, then compilers** | Exam only | Tier 3 (7.8), Tier 2 (10.9) | little | not shown | Week 16 |

Weeks 17-19: revision, weakest first, full mocks.

### Track B. Consistency (every day)

| Item | Why daily | Files | Dose |
|---|---|---|---|
| DSA and coding problems | Improves only by repetition; top GATE topic; the coding round | PDS 51.6, Algorithms 10.9 | 1.5 h |
| Math problem-solving (LA, probability, calculus) | The foundation of ML; calculus is a "wildcard" in the priority report | LA 14.2, probability 5.9 | 1 h |
| PYQs and timed mocks | speed and accuracy compound | `topics/exam-analysis-report.md` | one section a week, full mock every 2-3 weeks from week 12 |
| Implement-from-scratch ML code | Building small models repeatedly is how ML skill compounds | project list in `ai.md` section 4 | 30-45 min |
| Reading one paper or blog a week | Research literacy, needed for research and AI-safety roles | `ai.md`: "Interpretability/explainability research methods" | weekly |

### Track C. AI hands-on (one block a week, starts when A2 is done, about week 5)

Order follows the dependency: math -> classical ML -> deep learning -> LLMs -> systems.

| # | Skill | What to build | Source in our files | Why here |
|---|---|---|---|---|
| C1 | **Classical ML from scratch and with libraries** | regression, KNN, Naive Bayes, decision tree, K-means, PCA, model evaluation | `ai.md` section 4 (Bishop, Ross, Strang projects) | you are at 3/5; needs A2, A3 |
| C2 | **Deep learning**: MLP and backpropagation, then CNN/RNN, then **attention and a small transformer** in PyTorch | gradient descent and backprop by hand, then an MLP on MNIST, then a tiny transformer | `ai.md`: "PyTorch (dominant), JAX, TensorFlow"; "Deep learning architectures: transformers, attention" | biggest gap (1/5) and the core of ML/AI engineering (44% of AI titles) |
| C3 | **LLM/GenAI**: use a pretrained model, fine-tune a small one, RAG, an agent with evaluation | one working agent with a written evaluation | `ai.md`: "RAG/agentic stack", "Model evaluation and red-teaming methodology" | AI/GenAI words without ML words are 63% of 2026 AI titles |
| C4 | **Security x ML project (your edge)** | retrain your BLE/Wi-Fi attack-detection models with a modern framework and honest evaluation; then attack the model (adversarial inputs) and write up the result | your projects; Google AI-security titles (15 live) | it counts for both goals: red-team portfolio and AI portfolio |
| C5 | **ML systems**: GPU training, experiment tracking, serving, one distributed run | small scale on rented or local GPU | `ai.md`: "vLLM, TensorRT, Triton", "MLflow, W&B", "Kubernetes" | second gap (1/5); infra/hardware is 15% of AI titles |
| C6 | **Google-specific**: Vertex AI and the Google Professional Machine Learning Engineer certificate | one deployed model on Google Cloud | `ai.md` certifications list | shows cloud + ML together; ties to the cloud gap from the red-team plan |
| C7 | **Research output** (only if targeting research or AI safety) | one reproducible experiment and a short preprint | `ai.md` note: research tracks expect a PhD or strong publications | last; long horizon |

### Schedule (about 19 weeks)

| Phase | Weeks | Track A (one at a time) | Track B (daily) | Track C (one block a week) |
|---|---|---|---|---|
| 1 | 1-4 | A1, A2 | DSA, math, from-scratch code | none (setup); start C1 in week 4 |
| 2 | 5-9 | A3, A4, A5 | + timed sections from week 8 | C1 classical ML |
| 3 | 10-14 | A6, A7, A8 | mocks from week 12 | C2 deep learning (to a small transformer) |
| 4 | 15-19 | A9, A10, then **revision only** | full mocks, PYQs | C4 security x ML (keep it small) |
| After the exam | | done | keep DSA daily | C3 LLM -> C5 systems -> C6 Google cloud ML -> C7 research |

## 3. Variant 2: GATE DA + Google AI role

DA scores from `exam-priority-report-da.md` (3 sittings only; the file warns Machine Learning and AI are probably under-counted and says not to leave AI last).

| # | Subject (DA order from the report) | GATE DA (score) | Link to the AI role |
|---|---|---|---|
| 1 | **Probability and statistics** | Tier 1 (30.2, the highest) | ML foundation and evaluation |
| 2 | **Databases** | Tier 1 (28.0) | data infrastructure |
| 3 | **Programming and data structures** | Tier 2 (22.9) | coding rounds |
| 4 | **Discrete mathematics** | Tier 2 (22.3) | search, logic |
| 5 | **Machine learning** (clustering, regression variants, SVM, PCA) | Tier 2 (15.1, under-counted) | the core of the role |
| 6 | **Linear algebra** | Tier 2 (11.2) | prerequisite of ML: study it **before** item 5 in practice |
| 7 | **Algorithms** | Tier 3 (6.0; graph traversal only) | interviews |
| 8 | **Calculus** | Tier 3 (2.7, likely under-counted) | optimization, backpropagation |
| 9 | **Artificial intelligence** (search, adversarial search, Bayesian networks) | Tier 3 (2.4, but treat as Tier 2) | AI fundamentals |

Suggested practical order (prerequisites first): PDS core -> linear algebra -> probability and statistics -> calculus -> machine learning -> discrete maths -> databases -> algorithms -> AI, with Track B daily and Track C (deep learning, LLM, systems, security x ML) as in variant 1, but starting earlier (about week 3) because there are fewer exam subjects.

## 4. Books and material (only what our files name or hold)

- **Named in `ai.md` as the from-scratch project books (not on disk):** Strang (Linear Algebra and Its Applications), Sheldon Ross (A First Course in Probability), Goodfellow, Bengio and Courville (Deep Learning), Bishop (Pattern Recognition and Machine Learning), Russell and Norvig (AI: A Modern Approach), CLRS (Introduction to Algorithms).
- **On disk and relevant (from `gate-vs-google-security-topics.md` appendix and the reading list):** *Mastering Machine Learning for Penetration Testing* (`../hardisk/hdd/disk/course/WEEK-23/Security_Study_Material/Mastering Machine Learning for Penetration Testing.pdf`); *Malware Data Science* (`../hardisk/hdd/old_files/books/Joshua Saxe, Hillary Sanders - Malware Data Science_ Attack Detection and Attribution-No Starch Press (2018).pdf`); a short chapter *Introduction to Artificial Intelligence* (`../hardisk/pendrive-aug-26/summary/Book Materials/genetic algorithm books/01_Introduction_to_Artificial_Intelligence.pdf`).
- **Not found on disk:** any core ML, deep-learning, probability, linear-algebra or AI textbook, and any LLM or ML-systems book. Those seven named books need to be obtained; nothing else in our files replaces them.
- The GATE side of each subject is covered by the GeeksforGeeks link sets in `topics/gfg-gate-topic-map.md` and the priority reports.

## 5. Where the AI role and the red-team role reinforce each other

- **AI security is the overlap:** Google has AI-titled security roles (15 live), and the profile-fit report puts AI x security as the best skills match. C4 (security x ML with adversarial testing) is also red-team portfolio work.
- **Cloud helps both:** a Google Cloud ML deployment (C6) and the GCP security project from the red-team plan can share one project.
- **Coding and DSA are the same daily block for both.**
- **Reality check from the live data:** the AI-titled security roles ask 5+ years or a PhD, so this route is a 3-5 year goal reached through an earlier 2-3 year role, not an entry point.

## 6. If you are doing both plans at once

Weeks 1-4 are the same for both (programming core, mathematics, daily DSA). After that the plans differ: the red-team plan continues with discrete maths, COA and OS before networks, and puts web/AD/cloud labs in the weekly block; this plan takes probability, discrete maths and algorithms first and puts ML labs in the weekly block. With one weekly block, use it for the **security x ML project (C4)** and the **cloud project**, which serve both. Do not run two Track C blocks a week.

## 7. What our files cannot tell us

- The GATE 2027 date, your daily hours, and your current level per subject (a diagnostic mock would replace my guesses).
- What Google's ML/AI roles require (years, degrees, frameworks): never measured; only titles and the six-company career-page skills.
- Google interview content.
- GATE DA's weights rest on 3 sittings and the report itself flags ML and AI as under-counted.

## Files this is based on (under `./tracks/gate/`)

`exam-priority-report.md`, `exam-priority-report-da.md`, `topics/gfg-gate-topic-map.md`, `topics/exam-analysis-report*.md` - `career-mapping/ai.md`, `google-wayback-ai-analysis.md`, `profile-fit-google.md`, `gate-vs-google-security-topics.md`, `google-jd/google-security-jd-trends.md` (AI wording), `google-live/details-checklist.md`.
