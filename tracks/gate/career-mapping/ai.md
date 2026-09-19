# AI — job roles, skills, GATE overlap, and practice projects

Consolidated from a `web-capture`-based job-listing analysis of Google, Anthropic,
Meta, SAP, Adobe, and Palo Alto Networks career pages, cross-referenced against
the GATE 2027 checklist (`../topics/gfg-gate-topic-map.md`) and web-vapt-style
practical project ideas.

---

## 1. Job titles found

**Google**
- AI Technical Delivery Lead, Google Cloud
- Senior Software Engineer, AI/ML, Google Cloud
- Staff Software Engineer, AI/ML GenAI, Google Cloud AI

**Anthropic**
- Research Manager, Interpretability
- Research Engineer / Research Scientist, Tokens
- Research Engineer / Scientist, Alignment
- Anthropic Fellows Program, ML Systems & Reinforcement Learning
- Data Infrastructure Engineer, Pre-training
- Engineering Manager, GPU (ML Accelerator)
- Full-Stack Software Engineer, Reinforcement Learning
- Machine Learning Infrastructure Engineer, Safeguards Research
- ML/Research Engineer, Safeguards
- Performance Engineer (+ GPU / Inference Engine / Inference Systems variants)
- Product Manager, Claude Science
- Research Engineer, Chip Design RL / Code RL / Computer Use / Discovery / Domain Scaling / Interpretability / Model Evaluations / Pretraining / Production Model Post-Training / RL Engineering / RL Scaling Science
- Research Scientist, Interpretability / Life Sciences

**Meta**
- Data Scientist (Technical Leadership)
- Data Scientist, Analytics (Ranking, AI)
- Data Scientist, Product Analytics
- Design Verification Engineer - AI Accelerators
- Director, AI Manufacturing Enablement
- Hardware Engineer, AI Accelerator Module Validation
- Production Systems Engineer, Fleet AI Systems

**SAP**
- SAP iXp Intern - Agentic AI Solutions Engineering Intern
- Junior AI Engineer

**Adobe**
- AI Studio - Content Operations Lead (GenStudio & Firefly)
- Machine Learning Engineer 3
- Senior Engineer, AI Edge

**Palo Alto Networks**
- Principal AI Tool Engineer for Software Automation/Testing

---

## 2. Technical stack, certifications, skills

**Technical stack**
- **Languages:** Python (primary), C++/CUDA, Rust (growing in ML infra)
- **Frameworks:** PyTorch (dominant), JAX, TensorFlow
- **LLM/transformer stack:** Hugging Face Transformers, DeepSpeed, Megatron-LM, FSDP
- **RL:** RLHF/PPO, TRL, RLlib
- **Serving/inference:** vLLM, TensorRT, Triton Inference Server
- **Distributed/hardware:** CUDA, NCCL, multi-GPU/TPU clusters
- **Data infra:** Spark, Ray, Airflow
- **MLOps:** MLflow, Weights & Biases, Kubeflow
- **RAG/agentic stack:** vector databases (Pinecone, Weaviate, FAISS), agent/tool-use frameworks
- **Cloud ML platforms:** AWS SageMaker, Google Vertex AI, Azure ML
- **Containers/orchestration:** Docker, Kubernetes

**Certifications**
- Google Professional Machine Learning Engineer
- AWS Certified Machine Learning – Specialty
- Microsoft Certified: Azure AI Engineer Associate
- NVIDIA Deep Learning Institute certificates
- TensorFlow Developer Certificate
- DeepLearning.AI / Coursera specializations (widely recognized informally)
- *Note:* for research scientist tracks (Interpretability, Alignment, Research Scientist roles), a strong publication record or PhD typically substitutes for formal certification

**Skills**
- Strong math foundation: linear algebra, probability/statistics, optimization
- Deep learning architectures: transformers, attention mechanisms
- Large-scale distributed training (mixed precision, checkpointing, sharding)
- Reinforcement learning fundamentals — heavily represented across the roles found
- Interpretability/explainability research methods
- Model evaluation & red-teaming methodology
- Data pipeline design and large-scale data engineering
- Prompt engineering & agentic system design
- Domain-specialization ability (roles spanned life sciences, chip design, and infra)
- Cross-functional communication of research to product/eng teams

---

## 3. GATE topics that overlap with this track

GATE DA has dedicated sections for this, unlike Cybersecurity:

- **Linear Algebra** (§2) — matrices, eigenvalues/eigenvectors, SVD
- **Probability & Statistics** (§2) — Bayes' Theorem, distributions, hypothesis testing
- **Calculus** (§2) — optimization foundations
- **Machine Learning** (§13, GATE DA) — Regression, Classification, Model Evaluation, Neural Networks (MLP), Clustering, PCA/Dimensionality Reduction
- **Artificial Intelligence** (§14, GATE DA) — Search algorithms, Adversarial Search, Logic, Bayesian Network reasoning
- **Data Structures & Algorithms** (§6–7)
- **Databases** (§11) — incl. Data Warehouse/NoSQL

---

## 4. Practical, code-first project ideas (web-vapt-style)

Each project is meant to be *built from scratch* against the named book — not
a tutorial followed, a chapter implemented in code.

**Linear Algebra** — *Gilbert Strang, "Linear Algebra and Its Applications"*
- Matrix class from scratch (no numpy): multiplication, determinant, rank via Gaussian elimination, inverse
- Eigenvalues/eigenvectors via power iteration or QR algorithm, built on your own matrix class
- PCA + SVD from scratch, applied to image compression

**Probability & Statistics** — *Sheldon Ross, "A First Course in Probability"*
- Naive Bayes spam classifier from scratch on a real spam dataset — no sklearn
- Hypothesis testing from scratch (t-test/z-test/chi-squared computed manually), verified against scipy.stats

**Calculus** — *Goodfellow, Bengio, Courville, "Deep Learning"* (Part I)
- Gradient descent from scratch with manually-derived gradients, visualized convergence
- Backpropagation from scratch for a small NN (manual chain rule, no autograd)

**Machine Learning** — *Christopher Bishop, "Pattern Recognition and Machine Learning"*
- Linear/Logistic/Ridge Regression from scratch, validated against sklearn
- KNN, Naive Bayes, Decision Tree (entropy/info-gain split) from scratch
- K-Means + Hierarchical Clustering from scratch on synthetic 2D data
- MLP from scratch trained on MNIST — capstone tying in the Calculus backprop project
- Random Forest from scratch, built on your own Decision Tree

**Artificial Intelligence** — *Russell & Norvig, "Artificial Intelligence: A Modern Approach"* (covers every GATE DA §14 subtopic directly)
- BFS/DFS/A*/Greedy/UCS solving an 8-puzzle or maze, compared head-to-head
- Minimax + Alpha-Beta Tic-Tac-Toe/Connect-4 agent
- Bayesian Network exact inference (variable elimination) on the classic Burglary-Earthquake-Alarm network
- Propositional logic resolution/inference engine (satisfiability, forward/backward chaining)

**Data Structures & Algorithms** — *Cormen, Leiserson, Rivest, Stein, "Introduction to Algorithms" (CLRS)*
- Hash table, tree, heap, graph implementations from scratch, then reuse your own heap to build Dijkstra/A* (feeds the AI search project above)
- Sorting/searching benchmark suite on large datasets — complexity theory made empirical

**Databases** — *Silberschatz, Korth, Sudarshan, "Database System Concepts"* + *Ralph Kimball, "The Data Warehouse Toolkit"* for star/snowflake schema design specifically
- Star-schema warehouse (fact + dimension tables) built from your own ML projects' experiment results, with OLAP aggregation queries
- Mini Redis: in-memory key-value store with append-only-log persistence, from scratch

---

*Companies with no usable job data (crawl blocked, or the capture tool's search-box
probe polluted results with a literal "test" query): Microsoft, Amazon, Apple,
Oracle, IBM, CrowdStrike, Fortinet, Zscaler, Okta, SentinelOne, Cloudflare,
Check Point, Tenable, Rapid7, Qualys, OpenAI, Nvidia, Mistral, Cohere, Databricks,
ServiceNow, Snowflake, Atlassian, Salesforce, VMware/Broadcom. Extending
`job_search` plugin's `SITE_CONFIGS` (extra_hop_hosts + skip_probe per company)
would likely recover most of these — not done yet.*
