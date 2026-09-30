#!/usr/bin/env python3
import re, os, json, sys
from collections import defaultdict

EXTRACT_DIR = "/tmp/gate-extract"

# Keyword lexicon per GATE topic-map section (built from gfg-gate-topic-map.md cluster titles/sub-items)
LEXICON = {
    "1-GA": ["general aptitude", "verbal", "analogy", "syllogism", "inference", "paragraph",
             "reading comprehension", "ratio", "proportion", "percentage", "logarithm",
             "permutation", "combination", "series", "mensuration", "probability aptitude",
             "bar graph", "pie chart", "table chart", "statement", "conclusion", "assumption",
             "rotation", "mirror", "folding", "cutting", "assembling"],
    "2-EngMath-LinearAlgebra": ["matrix", "matrices", "determinant", "rank of", "eigenvalue",
             "eigenvector", "lu decomposition", "system of linear equations", "diagonaliz",
             "cayley hamilton", "orthogonal", "projection matrix", "singular value decomposition",
             "svd", "row echelon", "null space", "nullity", "idempotent", "quadratic form"],
    "2-EngMath-Probability": ["probability", "random variable", "probability distribution", "uniform distribution",
             "exponential distribution", "normal distribution", "binomial distribution",
             "poisson distribution", "covariance", "correlation", "conditional probability",
             "bayes", "expectation", "variance", "standard deviation", "central limit theorem",
             "hypothesis testing", "z-test", "t-test", "chi-square", "confidence interval",
             "mean", "median", "mode"],
    "2-EngMath-Calculus": ["limit", "continuity", "differentiab", "mean value theorem",
             "taylor series", "maclaurin", "chain rule", "integral", "integration", "maxima",
             "minima", "sequence and series", "indeterminate form", "rolle", "lagrange",
             "cauchy's mean"],
    "3-DiscreteMath": ["propositional logic", "predicate logic", "first order logic",
             "quantifier", "rules of inference", "set theory", "power set", "cartesian product",
             "relation", "equivalence relation", "function", "group", "monoid", "lattice",
             "hasse diagram", "partial order", "combinatorics", "pigeonhole",
             "binomial coefficient", "generating function", "graph theory", "isomorphism",
             "planar graph", "hamiltonian", "euler", "graph coloring", "matching",
             "connected graph", "degree sequence"],
    "4-DigitalLogic": ["boolean algebra", "k-map", "karnaugh", "quine-mccluskey", "logic gate",
             "nand", "nor gate", "nor operation", "exclusive nor", "flip-flop", "flip flop", "latch", "combinational circuit",
             "sequential circuit", "multiplexer", "demultiplexer", "encoder", "decoder",
             "adder", "subtractor", "counter", "shift register", "number system",
             "floating point representation", "gray code", "2's complement", "1's complement",
             "minimization of boolean"],
    "5-COA": ["addressing mode", "instruction format", "risc", "cisc", "pipelin", "cache",
             "memory hierarchy", "amdahl", "booth's algorithm", "control unit",
             "microprogrammed", "hardwired", "register transfer", "alu", "dma", "interrupt",
             "bus arbitration", "von neumann", "flynn's taxonomy", "branch prediction",
             "instruction level parallelism", "tlb", "cache mapping", "hazard"],
    "6-ProgDS": ["pointer", "recursion", "array", "stack", "queue", "linked list", "binary tree",
             "avl tree", "binary search tree", "bst", "heap", "hashing", "hash table",
             "hash function", "collision", "python", "scope of a variable", "struct",
             "union", "enum", "type casting", "circular queue", "deque", "postfix",
             "infix", "towers of hanoi", "printf", "scanf", "stdio", "#include"],
    "7-Algorithms": ["asymptotic", "time complexity", "recurrence relation", "master theorem",
             "divide and conquer", "merge sort", "quick sort", "binary search",
             "greedy algorithm", "huffman", "knapsack", "minimum spanning tree", "prim's",
             "kruskal", "dijkstra", "dynamic programming", "longest common subsequence",
             "matrix chain multiplication", "topological sort", "bellman-ford",
             "floyd-warshall", "articulation point", "bfs", "dfs", "graph traversal",
             "np-complete", "np-hard"],
    "8-ToC": ["finite automata", "dfa", "nfa", "regular expression", "regular language",
             "context-free grammar", "context free grammar", "context-free language",
             "context free language", "pushdown automata", "cfg",
             "pumping lemma", "turing machine", "halting problem", "decidability",
             "undecidab", "chomsky", "mealy machine", "moore machine", "np-complete",
             "recursively enumerable"],
    "9-Compiler": ["compiler", "lexical analysis", "parser", "parsing", "syntax tree",
             "syntax-directed", "s-attributed", "l-attributed", "first set", "follow set", "lalr", "slr", "shift-reduce",
             "recursive descent", "three address code", "intermediate code",
             "code optimization", "constant propagation", "constant folding",
             "common subexpression", "dead code elimination", "symbol table",
             "runtime environment", "ambiguous grammar"],
    "10-OS": ["cpu scheduling", "process synchronization", "semaphore", "mutex",
             "deadlock", "banker's algorithm", "resource allocation graph", "paging",
             "page table", "page replacement", "segmentation", "virtual memory",
             "demand paging", "thrashing", "translation lookaside buffer", "disk scheduling",
             "file system", "system call", "thread", "context switch", "producer-consumer",
             "readers-writers", "dining philosophers", "monitor", "critical section",
             "belady", "fifo page", "lru page", "optimal page", "fork()", "ipc",
             "inter-process communication"],
    "11-DBMS": ["er model", "e-r diagram", "entity-relationship", "relational algebra",
             "relational calculus", "normalization", "normal form", "functional dependency",
             "candidate key", "primary key", "foreign key", "decomposition", "lossless",
             "sql", "query", "join", "b-tree", "b+ tree", "indexing", "acid propert",
             "serializability", "concurrency control", "two phase locking", "transaction",
             "schedule", "deadlock in dbms", "data warehouse", "olap", "oltp", "nosql",
             "star schema", "snowflake schema", "dimensional model"],
    "12-Networks": ["osi model", "tcp/ip", "data link layer", "network layer", "transport layer",
             "application layer", "ip address", "subnet", "cidr", "network address translation",
             "static nat", "dynamic nat", "nat table", "routing algorithm",
             "distance vector", "link state", "ospf", "rip", "tcp", "udp",
             "congestion control", "flow control", "sliding window", "hamming code",
             "error detection", "checksum", "crc", "csma", "aloha", "ethernet",
             "circuit switching", "packet switching", "virtual circuit", "socket",
             "dns", "dhcp", "http", "ftp", "smtp", "arp", "three-way handshake",
             "3-way handshake", "mac address", "firewall", "bandwidth", "throughput",
             "channel capacity"],
    "13-ML": ["regression", "linear regression", "logistic regression", "ridge regression",
             "k-nearest neighbour", "knn", "naive bayes", "linear discriminant analysis",
             "support vector machine", "svm", "decision tree", "random forest",
             "bias-variance", "cross validation", "k-fold", "leave-one-out",
             "multi-layer perceptron", "feed-forward", "feedforward", "neural network",
             "clustering", "k-means", "k-medoid", "hierarchical clustering",
             "dimensionality reduction", "principal component analysis", "pca",
             "confusion matrix", "precision", "recall", "f1 score", "overfitting",
             "underfitting", "gradient descent", "loss function", "activation function"],
    "14-AI": ["informed search", "uninformed search", "adversarial search", "minimax",
             "alpha-beta pruning", "a* search", "greedy best-first", "uniform cost search",
             "breadth first search", "depth first search", "propositional logic",
             "predicate logic", "bayesian network", "conditional independence",
             "variable elimination", "exact inference", "approximate inference", "sampling",
             "heuristic function", "game tree", "constraint satisfaction"],
}

def load_lexicon_patterns():
    # word-boundary regex per keyword — prevents short keywords (e.g. "alu", "nat")
    # from matching as substrings inside unrelated words ("value", "national")
    compiled = {}
    for sec, words in LEXICON.items():
        compiled[sec] = [(w, re.compile(r'\b' + re.escape(w.lower()) + r'\b')) for w in words]
    return compiled

LEX = load_lexicon_patterns()

def classify_question(text, exclude_ga=False):
    t = text.lower()
    scores = {}
    for sec, patterns in LEX.items():
        if exclude_ga and sec == "1-GA":
            continue
        hits = [w for w, pat in patterns if pat.search(t)]
        if hits:
            scores[sec] = hits
    if not scores:
        return None, [], 0
    # best section = most keyword hits
    best_sec = max(scores.items(), key=lambda kv: len(kv[1]))[0]
    total_sections_hit = len(scores)
    return best_sec, scores[best_sec], total_sections_hit

RANGE_HEADER = re.compile(r'Q\.?\s?\d{1,2}\s*[-–]\s*Q\.?\s?\d{1,2}[^\n]{0,40}[Cc]arry[^\n]{0,20}[Mm]arks?[^\n]{0,10}')

def strip_range_headers(text):
    return RANGE_HEADER.sub(' ', text)

def split_questions(text, total_expected=65):
    """Split GATE paper text into (qnum, chunk) using Q.N markers, strict +1 stepping."""
    text = strip_range_headers(text)
    pattern = re.compile(r'\bQ\.?\s?(\d{1,2})\b')
    matches = list(pattern.finditer(text))
    ordered = []
    last_num = 0
    for i, m in enumerate(matches):
        qnum = int(m.group(1))
        if qnum != last_num + 1:
            continue  # only accept strict sequential stepping -> filters page-footer/other noise
        start = m.end()
        # tentative end = next accepted match's start, refined after loop
        ordered.append([qnum, start, None])
        last_num = qnum
        if last_num == total_expected:
            break
    # fill ends
    for i in range(len(ordered)):
        ordered[i][2] = ordered[i+1][1] - (len(f"Q.{ordered[i+1][0]}")+2) if i+1 < len(ordered) else len(text)
        # simpler: just use next start position, minor overlap of a few chars doesn't matter for keyword search
    chunks = []
    for i, (qnum, start, _) in enumerate(ordered):
        end = ordered[i+1][1] if i+1 < len(ordered) else len(text)
        chunks.append((qnum, text[start:end]))
    return chunks

def process_paper(path, ga_count=10, total_expected=65):
    with open(path, encoding='utf-8', errors='ignore') as f:
        text = f.read()
    chunks = split_questions(text, total_expected)
    results = []
    for qnum, chunk in chunks:
        if qnum <= ga_count:
            section, hits, nsec = "1-GA", [], 0
        else:
            sec, hits, nsec = classify_question(chunk, exclude_ga=True)
            section = sec
        complex_flag = (nsec >= 2) and section != "1-GA"
        results.append({"q": qnum, "section": section, "hits": hits, "multi_section_hits": nsec, "complex": complex_flag})
    return results

if __name__ == "__main__":
    paper = sys.argv[1]
    ga = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    res = process_paper(paper, ga)
    print(json.dumps(res, indent=1))
