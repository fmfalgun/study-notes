#!/usr/bin/env python3
"""bluff.py -- isroprep activity simulator.

Structural inspiration: ~/Projects/bluff/all-versions/lab.sh (the multi-pane
"workstation simulator" concept -- each pane is a worker loop that keeps
picking a random operation from its own list and rendering plausible fake
output) and ~/Projects/iot-proxy-recon/scripts/cam-finder-v3.py (curses TUI
structure: header/footer band, bordered scrollable panels). No tmux here --
a single curses process renders a grid of panels, each driven by its own
background thread appending to its own line buffer; the main thread only
touches curses (curses itself is not thread-safe).

Every operation below is themed on an actual isroprep exam topic (see
../topics/gfg-isro-topic-map.md and progress-tracker.md) instead of generic
security/AI/dev-ops busywork. Where cheap, the numbers shown are genuinely
computed (Banker's algorithm, Hamming(7,4) encode/correct, Dijkstra, a toy
RSA keygen, least-squares regression, ...) rather than just plausible-looking
random text -- the rest is formatted random data, same spirit as lab.sh.

Python 3 stdlib only, no external dependencies.

Usage: chmod +x bluff.py && ./bluff.py   (q to quit)
"""
import curses
import hashlib
import math
import random
import statistics
import threading
import time
from collections import deque

HEADER_ROWS = 1
FOOTER_ROWS = 1


def rnd(a, b):
    return random.randint(a, b)


def fl(a, b):
    return round(random.uniform(a, b), 2)


def ts():
    return time.strftime("%H:%M:%S")


# ───────────────────────── Mathematics ─────────────────────────

def op_combinatorics():
    n = rnd(20, 60)
    k = rnd(3, n // 2)
    val = math.comb(n, k)
    pigeons = rnd(n + 1, n + 20)
    return "Mathematics · Combinatorics", [
        f"C({n},{k}) = {val:,}",
        f"pigeonhole: {pigeons} items -> {n} boxes => some box holds >= {math.ceil(pigeons / n)}",
    ]


def op_graph_planarity():
    v = rnd(5, 12)
    e = rnd(v, 3 * v - 6 + 4)
    bound = 3 * v - 6
    planar = e <= bound
    return "Mathematics · Graph Theory", [
        f"G(V={v}, E={e}) -- Kuratowski bound 3V-6={bound}",
        f"necessary planarity condition: {'holds (may be planar)' if planar else 'violated -> NOT planar'}",
    ]


def op_linear_algebra():
    a11, a12, a21, a22 = (rnd(-9, 9) for _ in range(4))
    tr = a11 + a22
    det = a11 * a22 - a12 * a21
    disc = tr * tr - 4 * det
    if disc >= 0:
        r = math.sqrt(disc)
        eig = f"lambda = {(tr + r) / 2:.3f}, {(tr - r) / 2:.3f}"
    else:
        r = math.sqrt(-disc)
        eig = f"lambda = {tr / 2:.3f} +/- {r / 2:.3f}i"
    return "Mathematics · Linear Algebra", [
        f"A = [[{a11},{a12}],[{a21},{a22}]]  det={det}  trace={tr}",
        eig,
    ]


def op_calculus():
    a, b = sorted(random.sample(range(-4, 5), 2))
    if a == b:
        b += 1
    f = lambda x: x ** 3 - 3 * x
    slope = (f(b) - f(a)) / (b - a)
    target = (slope + 3) / 3
    if target >= 0:
        c = math.sqrt(target)
        cs = f"c = {c:.4f} (root in [{a},{b}] per MVT)"
    else:
        cs = "no real root -- check interval"
    return "Mathematics · Calculus", [
        f"Lagrange MVT: f(x)=x^3-3x on [{a},{b}], slope={slope:.4f}",
        cs,
    ]


def op_probability():
    prior = fl(0.01, 0.3)
    tpr = fl(0.85, 0.99)
    fpr = fl(0.01, 0.15)
    post = (tpr * prior) / (tpr * prior + fpr * (1 - prior))
    return "Mathematics · Probability", [
        f"Bayes: P(A)={prior} TPR={tpr} FPR={fpr}",
        f"P(A|B) = {post:.4f}",
    ]


MATH_OPS = [op_combinatorics, op_graph_planarity, op_linear_algebra, op_calculus, op_probability]


# ───────────────────────── OS & Architecture ─────────────────────────

def op_bankers_algorithm():
    n, m = 3, 2
    alloc = [[rnd(0, 3) for _ in range(m)] for _ in range(n)]
    need = [[rnd(0, 3) for _ in range(m)] for _ in range(n)]
    avail = [rnd(2, 6) for _ in range(m)]
    work = avail[:]
    finish = [False] * n
    seq = []
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += alloc[i][j]
                finish[i] = True
                seq.append(i)
                changed = True
    safe = all(finish)
    return "OS · Deadlock (Banker's)", [
        f"{n} processes, {m} resource types, avail={avail}",
        f"safe sequence: {['P' + str(i) for i in seq]}" if safe else "UNSAFE -- no safe sequence found",
    ]


def op_page_replacement():
    ref = [rnd(0, 4) for _ in range(rnd(12, 20))]
    frames = 3
    memory, faults = [], 0
    for p in ref:
        if p not in memory:
            faults += 1
            if len(memory) >= frames:
                memory.pop(0)
            memory.append(p)
        else:
            memory.remove(p)
            memory.append(p)
    rate = faults / len(ref) * 100
    return "OS · Paging (FIFO/LRU)", [
        f"ref string len={len(ref)}, frames={frames}",
        f"page faults={faults}  fault-rate={rate:.1f}%",
    ]


def op_round_robin():
    n = rnd(3, 6)
    burst = [rnd(2, 15) for _ in range(n)]
    q = rnd(2, 5)
    rem = burst[:]
    t = 0
    wait = [0] * n
    done = [False] * n
    while not all(done):
        for i in range(n):
            if done[i]:
                continue
            run = min(q, rem[i])
            rem[i] -= run
            t += run
            if rem[i] == 0:
                done[i] = True
                wait[i] = t - burst[i]
    return "OS · CPU Scheduling (RR)", [
        f"{n} processes, burst={burst}, quantum={q}",
        f"avg waiting time={statistics.mean(wait):.2f}",
    ]


def op_cache_lookup():
    sets = 16
    addr = rnd(0, 0xFFFF)
    idx = (addr // 4) % sets
    hit = random.random() < 0.7
    return "CO&A · Cache", [
        f"direct-mapped, {sets} sets, address=0x{addr:04X} -> set {idx}",
        "HIT (tag match)" if hit else "MISS -- fetching from memory",
    ]


def op_pipeline_hazard():
    stages = ["IF", "ID", "EX", "MEM", "WB"]
    i_a, i_b = rnd(1, 4), rnd(5, 8)
    hazard = random.choice(["RAW", "WAR", "WAW", "none"])
    return "CO&A · Pipelining", [
        f"5-stage pipeline {stages}, checking I{i_a}/I{i_b}",
        f"hazard: {hazard}" + (" -- forwarding applied" if hazard != "none" else ""),
    ]


OS_ARCH_OPS = [op_bankers_algorithm, op_page_replacement, op_round_robin, op_cache_lookup, op_pipeline_hazard]


# ───────────────────────── Networks & Security ─────────────────────────

def _hamming74_encode(d):
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]


def op_hamming_code():
    d = [rnd(0, 1) for _ in range(4)]
    code = _hamming74_encode(d)
    flip = rnd(0, 6)
    received = code[:]
    received[flip] ^= 1
    p1, p2, d1, p3, d2, d3, d4 = received
    c1 = p1 ^ d1 ^ d2 ^ d4
    c2 = p2 ^ d1 ^ d3 ^ d4
    c3 = p3 ^ d2 ^ d3 ^ d4
    syndrome = c1 + (c2 << 1) + (c3 << 2)
    return "Networks · Hamming(7,4)", [
        f"data={''.join(map(str, d))} encoded={''.join(map(str, code))} flipped bit {flip}",
        f"syndrome={syndrome} -> {'no error' if syndrome == 0 else f'corrected bit {syndrome - 1}'}",
    ]


def op_tcp_window():
    field = rnd(1, 65535)
    scale = rnd(0, 14)
    window = field << scale
    return "Networks · TCP Window", [
        f"window field={field} scale factor={scale}",
        f"effective window = {window:,} bytes",
    ]


def op_subnetting():
    octet = rnd(0, 63) * 4
    base = f"192.168.{octet}.0/22"
    subs = ", ".join(f"192.168.{octet + i}.0/24" for i in range(4))
    return "Networks · CIDR", [
        f"aggregating {subs}",
        f"supernet -> {base}",
    ]


def op_rsa_toy():
    primes = [11, 13, 17, 19, 23, 29, 31]
    p, q = random.sample(primes, 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = next(x for x in range(2, phi) if math.gcd(x, phi) == 1)
    d = pow(e, -1, phi)
    return "Cyber Security · RSA (toy)", [
        f"p={p} q={q} n={n} phi={phi}",
        f"e={e} d={d}",
    ]


def op_sha256():
    msg = "".join(random.choices("abcdef0123456789", k=16))
    digest = hashlib.sha256(msg.encode()).hexdigest()
    return "Cyber Security · Hashing", [
        f'SHA-256("{msg}")',
        digest,
    ]


NET_SEC_OPS = [op_hamming_code, op_tcp_window, op_subnetting, op_rsa_toy, op_sha256]


# ───────────────────────── Data & Structures ─────────────────────────

def op_two_phase_locking():
    txns = rnd(2, 4)
    ops = [f"T{i}: {random.choice(['S-lock', 'X-lock'])}({random.choice('RSTU')})" for i in range(txns)]
    conflict = random.random() < 0.4
    return "Databases · 2PL", [
        ", ".join(ops),
        "conflict -- transaction waits" if conflict else "no conflict -- all granted",
    ]


def op_serializability():
    n = rnd(2, 3)
    order = list(range(n))
    random.shuffle(order)
    return "Databases · Serializability", [
        f"schedule with {n} transactions, precedence graph built",
        f"acyclic -> conflict-serializable, equivalent order: {['T' + str(i) for i in order]}",
    ]


def op_sorting():
    arr = [rnd(1, 1000) for _ in range(rnd(200, 2000))]
    comparisons = 0

    def qsort(a):
        nonlocal comparisons
        if len(a) <= 1:
            return a
        pivot = a[0]
        less, more = [], []
        for x in a[1:]:
            comparisons += 1
            (less if x < pivot else more).append(x)
        return qsort(less) + [pivot] + qsort(more)

    qsort(arr)
    return "DSA · Sorting (quicksort)", [
        f"n={len(arr)} elements",
        f"comparisons={comparisons:,}",
    ]


def op_dijkstra():
    n = rnd(6, 10)
    edges = {i: {} for i in range(n)}
    for i in range(n):
        for _ in range(rnd(1, 3)):
            j = rnd(0, n - 1)
            if j != i:
                w = rnd(1, 20)
                edges[i][j] = w
                edges[j][i] = w
    dist = {i: math.inf for i in range(n)}
    dist[0] = 0
    visited = set()
    while len(visited) < n:
        u = min((i for i in range(n) if i not in visited), key=lambda i: dist[i], default=None)
        if u is None or dist[u] == math.inf:
            break
        visited.add(u)
        for v, w in edges[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    target = rnd(1, n - 1)
    d = dist[target]
    return "DSA · Graphs (Dijkstra)", [
        f"{n} nodes, source=0",
        f"shortest dist to node {target} = {d if d != math.inf else 'unreachable'}",
    ]


def op_mapreduce():
    records = rnd(100000, 5000000)
    return "Big Data · MapReduce", [
        f"mapping {records:,} records across {rnd(4, 32)} mappers",
        f"shuffle phase {rnd(10, 95)}% complete",
    ]


DATA_STRUCT_OPS = [op_two_phase_locking, op_serializability, op_sorting, op_dijkstra, op_mapreduce]


# ───────────────────────── Theory & Languages ─────────────────────────

def op_dfa():
    states = rnd(2, 6)
    alphabet = random.choice(["{0,1}", "{a,b}"])
    lang = random.choice([
        "even number of 0s", "ends in 01", "divisible by 3 (binary)", "no two consecutive 1s",
    ])
    return "Theory of Computation · DFA", [
        f"L = {{w : {lang}}}, alphabet {alphabet}",
        f"minimized DFA: {states} states",
    ]


def op_turing_machine():
    steps = rnd(10, 80)
    inp = "".join(random.choices("01", k=rnd(4, 10)))
    accept = random.random() < 0.7
    return "Theory of Computation · Turing Machine", [
        f"simulating TM on input {inp}",
        f"{steps} steps -> {'ACCEPT' if accept else 'REJECT'}",
    ]


def op_pumping_lemma():
    lang = random.choice(["a^n b^n", "ww (w in {0,1}*)", "a^(n^2)"])
    return "Theory of Computation · Pumping Lemma", [
        f"applying pumping lemma to L = {lang}",
        "contradiction found -> language not regular",
    ]


def op_c_pointers():
    arr = [rnd(0, 100) for _ in range(8)]
    i = rnd(0, 7)
    return "Programming Language · C Pointers", [
        f"int arr[8] = {arr}",
        f"*(arr + {i}) = {arr[i]}",
    ]


def op_python_comprehension():
    n = rnd(6, 15)
    result = [x ** 2 for x in range(n) if x % 2 == 0]
    return "Programming Language · Python", [
        f"[x**2 for x in range({n}) if x%2==0]",
        f"= {result}",
    ]


def op_lexer():
    lines = rnd(50, 500)
    tokens = lines * rnd(3, 6)
    return "Compiler Design · Lexical Analysis", [
        f"tokenizing source ({lines} lines)",
        f"{tokens:,} tokens produced",
    ]


THEORY_LANG_OPS = [op_dfa, op_turing_machine, op_pumping_lemma, op_c_pointers, op_python_comprehension, op_lexer]


# ───────────────────────── Applied CS ─────────────────────────

def op_linear_regression():
    n = rnd(30, 200)
    true_m, true_b = fl(-5, 5), fl(-10, 10)
    xs = [fl(0, 20) for _ in range(n)]
    ys = [true_m * x + true_b + fl(-2, 2) for x in xs]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    m = num / den if den else 0
    b = my - m * mx
    ss_res = sum((y - (m * x + b)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot else 0
    return "AI/ML · Linear Regression", [
        f"n={n} samples, fitting y = mx + b",
        f"m={m:.3f} b={b:.3f} R^2={r2:.4f}",
    ]


def op_knn():
    k = rnd(3, 9)
    acc = fl(78, 97)
    return "AI/ML · K-Nearest Neighbor", [
        f"k={k}, test set n={rnd(50, 500)}",
        f"accuracy={acc}%",
    ]


def op_kmeans():
    k = rnd(2, 6)
    iters = rnd(4, 25)
    inertia = fl(50, 900)
    return "AI/ML · K-Means", [
        f"k={k}, {rnd(200, 2000)} points",
        f"converged after {iters} iterations, inertia={inertia}",
    ]


def op_edge_detection():
    density = fl(2, 30)
    return "Image/Vision · Sobel Edge Detection", [
        f"3x3 kernel on {rnd(128, 1024)}x{rnd(128, 1024)} grayscale image",
        f"edge density={density}%",
    ]


def op_histogram_eq():
    before = fl(20, 60)
    after = before + fl(10, 30)
    return "Image/Vision · Histogram Equalization", [
        f"contrast before={before:.1f}",
        f"contrast after={after:.1f}",
    ]


def op_sdlc():
    stories = rnd(4, 12)
    velocity = rnd(15, 45)
    phase = random.choice(["planning", "design", "implementation", "testing", "retrospective"])
    return "Software Engineering · Agile SDLC", [
        f"sprint {phase}: {stories} stories estimated",
        f"velocity={velocity}",
    ]


def op_unit_tests():
    total = rnd(50, 300)
    failed = 0 if random.random() < 0.7 else rnd(1, 4)
    return "Software Engineering · Testing", [
        f"running unit test suite ({total} tests)",
        f"all {total} passed" if not failed else f"{total - failed} passed, {failed} failed",
    ]


def op_vm_provision():
    vcpu = rnd(1, 8)
    ram = rnd(1, 32)
    return "Cloud Computing · Virtualization", [
        f"provisioning VM: {vcpu} vCPU, {ram}GB RAM",
        "status=running",
    ]


APPLIED_CS_OPS = [op_linear_regression, op_knn, op_kmeans, op_edge_detection, op_histogram_eq,
                  op_sdlc, op_unit_tests, op_vm_provision]


PANELS_DEF = [
    ("Mathematics", MATH_OPS),
    ("OS & Architecture", OS_ARCH_OPS),
    ("Networks & Security", NET_SEC_OPS),
    ("Data & Structures", DATA_STRUCT_OPS),
    ("Theory & Languages", THEORY_LANG_OPS),
    ("Applied CS", APPLIED_CS_OPS),
]


class Panel:
    def __init__(self, title, ops):
        self.title = title
        self.ops = ops
        self.lines = deque(maxlen=500)
        self.lock = threading.Lock()
        self.win = None

    def append(self, text):
        with self.lock:
            self.lines.append(text)

    def resize(self, y, x, h, w):
        try:
            self.win = curses.newwin(h, w, y, x)
        except curses.error:
            self.win = None

    def render(self):
        if self.win is None:
            return
        h, w = self.win.getmaxyx()
        if h < 3 or w < 6:
            return
        self.win.erase()
        try:
            self.win.border()
            self.win.addstr(0, 2, f" {self.title} "[: max(0, w - 4)], curses.A_BOLD | curses.color_pair(2))
        except curses.error:
            pass
        with self.lock:
            visible = list(self.lines)[-(h - 2):]
        for i, line in enumerate(visible):
            try:
                self.win.addstr(1 + i, 1, line[: w - 2])
            except curses.error:
                pass
        self.win.noutrefresh()


def grid_dims(n):
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return rows, cols


def layout_panels(panels, term_h, term_w):
    rows, cols = grid_dims(len(panels))
    body_h = max(1, term_h - HEADER_ROWS - FOOTER_ROWS)
    cell_h = max(1, body_h // rows)
    cell_w = max(1, term_w // cols)
    for idx, panel in enumerate(panels):
        r, c = idx // cols, idx % cols
        y = HEADER_ROWS + r * cell_h
        x = c * cell_w
        h = cell_h if r < rows - 1 else max(1, body_h - cell_h * (rows - 1))
        w = cell_w if c < cols - 1 else max(1, term_w - cell_w * (cols - 1))
        panel.resize(y, x, h, w)


def worker_loop(panel, stop_event):
    while not stop_event.is_set():
        tag, lines = random.choice(panel.ops)()
        panel.append(f"> {tag}")
        for line in lines:
            if stop_event.is_set():
                return
            panel.append(f"  {line}")
            time.sleep(random.uniform(0.15, 0.5))
        panel.append("")
        time.sleep(random.uniform(0.8, 2.2))


def _main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(150)
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW, -1)
        curses.init_pair(2, curses.COLOR_CYAN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
    except curses.error:
        pass

    panels = [Panel(title, ops) for title, ops in PANELS_DEF]
    h, w = stdscr.getmaxyx()
    layout_panels(panels, h, w)

    stop_event = threading.Event()
    threads = [threading.Thread(target=worker_loop, args=(p, stop_event), daemon=True) for p in panels]
    for t in threads:
        t.start()

    start = time.time()
    try:
        while True:
            ch = stdscr.getch()
            if ch in (ord("q"), ord("Q")):
                break
            if ch == curses.KEY_RESIZE:
                stdscr.erase()
                stdscr.refresh()
                h, w = stdscr.getmaxyx()
                layout_panels(panels, h, w)

            stdscr.erase()
            header = f" bluff -- isroprep activity simulator   {ts()}   uptime {int(time.time() - start)}s"
            footer = " q: quit"
            try:
                stdscr.addstr(0, 0, header[: w - 1], curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(h - 1, 0, footer[: w - 1], curses.color_pair(3) | curses.A_DIM)
            except curses.error:
                pass
            stdscr.noutrefresh()
            for p in panels:
                p.render()
            curses.doupdate()
    finally:
        stop_event.set()


def main():
    try:
        curses.wrapper(_main)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
