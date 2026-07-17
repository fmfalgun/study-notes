# Garuda Linux Main Machine — GPU Overflow

**Machine**: Ryzen 7 7445HS (12 threads @ 3.2GHz), **NVIDIA RTX 4050 Max-Q (discrete GPU)**, AMD Radeon 740M integrated, Garuda Linux — your daily driver.
**Field**: overflow/advanced — not a fixed field of its own. This file only holds ideas pulled out of CS-Engineering, Cybersecurity, or DS/AI that genuinely need a GPU to be worth doing; nothing GPU-agnostic belongs here (e.g. Databases has no entry in this file — per your own call, a GPU makes no real difference there).

Every idea below is inspired by `../topics/gfg-isro-topic-map.md` and `../topics/gfg-gate-topic-map.md`. Each carries exactly one reference link. Ideas run as dev → deploy (days to 1-2 weeks) → analyze cycles — understanding this machine is your daily driver, so "deploy" here more often means a bounded multi-day training/benchmark run rather than a permanent background service.

---

## AI/ML — Deep Learning *(the primary reason this file exists)*

- **Feed-Forward Neural Net from Scratch (NumPy, then CUDA)** — implement forward/backprop manually on CPU first, then port the hot loop to GPU (CuPy or a simple CUDA kernel), measure the speedup. Ref: [karpathy/llm.c](https://github.com/karpathy/llm.c)
- **CNN Image Classifier Trained from Scratch on the RTX 4050** — build and train a small CNN (not transfer learning) on a real dataset, log training curves/GPU utilization over a multi-day run. Ref: [Convolutional Neural Network (CNN)](https://www.geeksforgeeks.org/deep-learning/convolutional-neural-network-cnn-in-machine-learning/)
- **Transfer-Learning Fine-Tune of a Pretrained Vision Model** — fine-tune a small pretrained CNN/ViT on your own image dataset, deploy inference as a local API, compare against the from-scratch CNN above. Ref: [Transfer Learning with CNNs](https://www.geeksforgeeks.org/deep-learning/ml-transfer-learning-with-convolutional-neural-networks/)
- **GAN from Scratch on a Small Image Dataset** — implement the generator/discriminator training loop, monitor mode collapse over a multi-day run. Ref: [Generative Adversarial Network (GAN)](https://www.geeksforgeeks.org/deep-learning/generative-adversarial-network-gan/)
- **Optimizer Bake-Off (SGD vs Adam vs RMSProp) on the Same Network** — implement each optimizer by hand, compare convergence speed/final loss on identical architectures. Ref: [Adam Optimizer](https://www.geeksforgeeks.org/deep-learning/adam-optimizer/)
- **Regularization Study (L1/L2/Dropout) on a CNN** — train the same architecture with different regularization schemes, quantify overfitting reduction on a held-out set. Ref: [Regularization in Machine Learning](https://www.geeksforgeeks.org/machine-learning/regularization-in-machine-learning/)
- **Tiny LLM Pretraining Run (nanoGPT-scale) on Your Own Text Corpus** — train a small transformer language model from scratch, log loss curves over a multi-day run, sample outputs at checkpoints. Ref: [karpathy/llm.c](https://github.com/karpathy/llm.c)
- **Local Model Fine-Tuning/Serving Benchmark** — fine-tune or quantize a small open model and serve it locally, benchmark tokens/sec vs CPU-only inference on the other three machines. Ref: [ollama/ollama](https://github.com/ollama/ollama)

## Image & Vision Processing — Deep Learning *(the GPU counterpart to ProOne's classical-CV section)*

- **Object Detection Model Trained from Scratch (YOLO-Tiny Style)** — build and train a small CNN-backbone detector on a real image set you collect, log mAP over training epochs on a multi-day run. Ref: [Convolutional Neural Network (CNN)](https://www.geeksforgeeks.org/deep-learning/convolutional-neural-network-cnn-in-machine-learning/)
- **Semantic Segmentation Network (U-Net Style)** — train an encoder-decoder segmentation network on your own labeled image set, compare pixel-accuracy/IoU against the classical watershed approach on ProOne. Ref: [Transfer Learning with CNNs](https://www.geeksforgeeks.org/deep-learning/ml-transfer-learning-with-convolutional-neural-networks/)

## Cyber Security — GPU-Accelerated Crypto Cost Analysis

- **Hash-Rate Benchmark Study (GPU vs CPU) for Password-Hashing Cost Tuning** — benchmark bcrypt/Argon2/SHA-256 hash rates on the RTX 4050 vs the CPU-only machines, use the numbers to reason about safe cost-factor choices for real systems (a defensive design lesson, not an attack on any real account). Ref: [sobolevn/awesome-cryptography](https://github.com/sobolevn/awesome-cryptography)

## Databases — GPU-Accelerated Vector Search *(the one DB angle that's genuinely GPU-bound)*

- **Embedding-Based Vector Index Benchmark** — generate embeddings for a text/image dataset using a GPU-run model, build and benchmark your own approximate-nearest-neighbor index against brute force, compare conceptually against how Weaviate does it. Ref: [weaviate/weaviate](https://github.com/weaviate/weaviate)
