#!/usr/bin/env python3
"""bluff.py -- study-notes activity monitor.

Structural inspiration: ../bluff/all-versions/lab.sh (the multi-pane
"workstation simulator" concept -- each pane is a worker loop that keeps
picking an operation from its own list and rendering output) and
../iot-proxy-recon/scripts/cam-finder-v3.py (curses TUI structure:
header/footer band, bordered scrollable panels). No tmux here -- a single
curses process renders a grid of panels, each driven by its own background
thread appending to its own line buffer; the main thread only touches curses
(curses itself is not thread-safe).

Every operation is themed on an actual study-notes exam topic (see
../tracks/isro/topics/gfg-isro-topic-map.md and ../tracks/isro/progress-tracker.md). Most of them now
read this machine's genuine current state via direct /proc parsing (a shared
SystemSnapshot, refreshed once per tick by one background thread and read by
every panel) instead of random.randint -- real per-core CPU busy%, real page
faults, real process table (comm/cpu%/RSS), real TCP/ARP/route table entries,
real memory, real bytes hashed. All reads are local and passive: nothing here
sends a packet to another host, scans, or probes a real device/node on any
network -- same boundary ../tools/homelab-experiments/probook-cybersec.md holds for
cybersecurity topics, applied here too since this script also reads live
system state.

A handful of operations have no accessible real-world signal at all --
abstract automata/discrete-math theory, CPU pipeline hazards (invisible from
userspace without hardware perf counters), agile-sprint state (no real board
to query). Those stay illustrative and are labeled "(illustrative)" in their
own output so it's visible in the UI which lines are real right now and which
are a conceptual demo of the algorithm.

Python 3 stdlib only, no external dependencies.

Usage: chmod +x bluff.py && ./bluff.py   (q to quit)
"""
import curses
import hashlib
import math
import os
import random
import statistics
import threading
import time
import tokenize
from collections import deque

HEADER_ROWS = 1
FOOTER_ROWS = 1

CLK_TCK = os.sysconf("SC_CLK_TCK")
TCP_STATES = {"01": "ESTABLISHED", "0A": "LISTEN", "06": "TIME_WAIT", "02": "SYN_SENT"}


def rnd(a, b):
    return random.randint(a, b)


def fl(a, b):
    return round(random.uniform(a, b), 2)


def ts():
    return time.strftime("%H:%M:%S")


# ───────────────────────── real /proc readers (local-only, passive) ─────────────────────────

def _read_proc_stat_cpus():
    result = {}
    with open("/proc/stat") as f:
        for line in f:
            if line.startswith("cpu"):
                parts = line.split()
                result[parts[0]] = list(map(int, parts[1:]))
            elif result:
                break
    return result


def _read_meminfo():
    d = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":", 1)
            d[k] = int(v.strip().split()[0])
    return d


def _read_vmstat():
    d = {}
    with open("/proc/vmstat") as f:
        for line in f:
            if line.startswith("pgfault") or line.startswith("pgmajfault"):
                k, v = line.split()
                d[k] = int(v)
    return d


def _read_tlb_total():
    try:
        with open("/proc/interrupts") as f:
            for line in f:
                if line.strip().startswith("TLB:"):
                    return sum(int(x) for x in line.split()[1:] if x.isdigit())
    except FileNotFoundError:
        pass
    return 0


def _read_arp_count():
    try:
        with open("/proc/net/arp") as f:
            return max(0, sum(1 for _ in f) - 1)
    except FileNotFoundError:
        return 0


def _hex_to_ipport(s):
    ip_hex, port_hex = s.split(":")
    b = bytes.fromhex(ip_hex)
    ip = ".".join(str(b[i]) for i in range(3, -1, -1))
    return ip, int(port_hex, 16)


def _read_tcp_sample():
    try:
        with open("/proc/net/tcp") as f:
            lines = f.readlines()[1:]
    except FileNotFoundError:
        return None
    for line in lines:
        parts = line.split()
        if len(parts) < 5:
            continue
        state = TCP_STATES.get(parts[3].upper(), parts[3])
        if state == "LISTEN":
            continue
        lip, lport = _hex_to_ipport(parts[1])
        rip, rport = _hex_to_ipport(parts[2])
        tx_hex, rx_hex = parts[4].split(":")
        return {
            "local": f"{lip}:{lport}", "remote": f"{rip}:{rport}", "state": state,
            "tx_queue": int(tx_hex, 16), "rx_queue": int(rx_hex, 16),
        }
    return None


def _read_local_subnet():
    try:
        with open("/proc/net/route") as f:
            lines = f.readlines()[1:]
    except FileNotFoundError:
        return None
    for line in lines:
        parts = line.split()
        if len(parts) < 8:
            continue
        iface, dest_hex, flags_hex, mask_hex = parts[0], parts[1], parts[3], parts[7]
        if not (int(flags_hex, 16) & 0x1) or dest_hex == "00000000":
            continue
        dest = int(dest_hex, 16)
        mask = int(mask_hex, 16)
        dest_ip = ".".join(str((dest >> (8 * i)) & 0xFF) for i in range(4))
        return f"{iface}: {dest_ip}/{bin(mask).count('1')}"
    return None


def _read_uptime_nibble():
    with open("/proc/uptime") as f:
        centi = int(float(f.read().split()[0]) * 100)
    return centi & 0xF


def _read_cpu_line():
    with open("/proc/stat") as f:
        return f.readline().strip()


def _read_processes(prev_times, now):
    procs, cur_times = [], {}
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        pid = int(entry)
        try:
            with open(f"/proc/{pid}/stat") as f:
                content = f.read()
            rparen = content.rfind(")")
            comm = content[content.find("(") + 1:rparen]
            rest = content[rparen + 2:].split()
            utime, stime = int(rest[11]), int(rest[12])
        except (FileNotFoundError, ProcessLookupError, ValueError, IndexError, PermissionError):
            continue
        rss_kb = 0
        try:
            with open(f"/proc/{pid}/status") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        rss_kb = int(line.split()[1])
                        break
        except (FileNotFoundError, PermissionError):
            pass
        total_ticks = utime + stime
        cur_times[pid] = (total_ticks, now)
        cpu_pct = 0.0
        if pid in prev_times:
            prev_ticks, prev_t = prev_times[pid]
            dt = now - prev_t
            if dt > 0:
                cpu_pct = max(0.0, (total_ticks - prev_ticks) / CLK_TCK / dt * 100)
        procs.append({"pid": pid, "comm": comm, "cpu_pct": cpu_pct, "rss_kb": rss_kb})
    return procs, cur_times


def _count_home_files(cap=20000):
    count = 0
    try:
        for _root, _dirs, files in os.walk(os.path.expanduser("~")):
            count += len(files)
            if count > cap:
                break
    except (PermissionError, FileNotFoundError):
        pass
    return count


def _count_self_tokens():
    path = os.path.abspath(__file__)
    try:
        with open(path, "r", encoding="utf-8") as f:
            n_lines = sum(1 for _ in f)
        with open(path, "rb") as f:
            n_tokens = sum(1 for _ in tokenize.tokenize(f.readline))
        return n_lines, n_tokens
    except (OSError, tokenize.TokenizeError):
        return 0, 0


def _self_smoke_test():
    checks = [_read_proc_stat_cpus, _read_meminfo, _read_vmstat, _read_arp_count]
    failed = []
    for fn in checks:
        try:
            fn()
        except Exception:
            failed.append(fn.__name__)
    return len(checks), len(failed), failed


class SystemSnapshot:
    """Shared, thread-safe, once-per-tick sample of this machine's real state.

    One background thread refreshes this; every panel's worker thread reads
    from it instead of each panel independently re-parsing /proc.
    """

    REFRESH_S = 1.5

    def __init__(self):
        self._lock = threading.Lock()
        self._prev_stat = _read_proc_stat_cpus()
        self._prev_proc_times = {}
        self._prev_tlb, self._prev_tlb_t = _read_tlb_total(), time.time()
        self._prev_vmstat, self._prev_vmstat_t = _read_vmstat(), time.time()
        self._cpu_total_pct = 0.0
        self._cpu_per_core_pct = []
        self._cpu_total_history = deque(maxlen=60)
        self._core_history = []
        self._mem = {}
        self._minor_rate = self._major_rate = 0.0
        self._processes = []
        self._tlb_rate = 0.0
        self._home_files = 0
        self._self_lines, self._self_tokens = _count_self_tokens()
        self._stop = threading.Event()
        threading.Thread(target=self._home_count_worker, daemon=True).start()
        self._refresh()
        threading.Thread(target=self._refresh_loop, daemon=True).start()

    def _home_count_worker(self):
        count = _count_home_files()
        with self._lock:
            self._home_files = count

    def _refresh_loop(self):
        while not self._stop.is_set():
            time.sleep(self.REFRESH_S)
            self._refresh()

    def stop(self):
        self._stop.set()

    def _refresh(self):
        now = time.time()
        cur_stat = _read_proc_stat_cpus()
        core_keys = sorted((k for k in cur_stat if k != "cpu" and k.startswith("cpu")),
                            key=lambda k: int(k[3:]))
        cpu_total_pct, per_core = 0.0, []
        for key in ["cpu"] + core_keys:
            prev, cur = self._prev_stat.get(key), cur_stat.get(key)
            pct = 0.0
            if prev and cur:
                idle_delta = (cur[3] + cur[4]) - (prev[3] + prev[4])
                total_delta = sum(cur) - sum(prev)
                pct = 100.0 * (1 - idle_delta / total_delta) if total_delta > 0 else 0.0
            if key == "cpu":
                cpu_total_pct = pct
            else:
                per_core.append(pct)
        self._prev_stat = cur_stat

        vmstat = _read_vmstat()
        dt_v = now - self._prev_vmstat_t
        minor_rate = major_rate = 0.0
        if dt_v > 0 and self._prev_vmstat:
            minor_rate = max(0.0, (vmstat.get("pgfault", 0) - self._prev_vmstat.get("pgfault", 0)) / dt_v)
            major_rate = max(0.0, (vmstat.get("pgmajfault", 0) - self._prev_vmstat.get("pgmajfault", 0)) / dt_v)
        self._prev_vmstat, self._prev_vmstat_t = vmstat, now

        tlb = _read_tlb_total()
        dt_t = now - self._prev_tlb_t
        tlb_rate = (tlb - self._prev_tlb) / dt_t if dt_t > 0 else 0.0
        self._prev_tlb, self._prev_tlb_t = tlb, now

        mem = _read_meminfo()
        procs, cur_times = _read_processes(self._prev_proc_times, now)
        self._prev_proc_times = cur_times

        with self._lock:
            self._cpu_total_pct = cpu_total_pct
            self._cpu_per_core_pct = per_core
            self._cpu_total_history.append(cpu_total_pct)
            if not self._core_history:
                self._core_history = [deque(maxlen=20) for _ in per_core]
            for i, pct in enumerate(per_core):
                if i < len(self._core_history):
                    self._core_history[i].append(pct)
            self._mem = mem
            self._minor_rate, self._major_rate = minor_rate, major_rate
            self._processes = procs
            self._tlb_rate = tlb_rate

    def core_count(self):
        return os.cpu_count() or 1

    def mem(self):
        with self._lock:
            m = self._mem
        total = m.get("MemTotal", 0)
        avail = m.get("MemAvailable", m.get("MemFree", 0))
        return {"total_kb": total, "available_kb": avail}

    def pagefault_rate(self):
        with self._lock:
            return self._minor_rate, self._major_rate

    def processes(self):
        with self._lock:
            return list(self._processes)

    def top_processes_by_rss(self, n=3):
        with self._lock:
            procs = sorted(self._processes, key=lambda p: p["rss_kb"], reverse=True)
        return procs[:n]

    def top_processes_by_cpu(self, n=4):
        with self._lock:
            procs = sorted(self._processes, key=lambda p: p["cpu_pct"], reverse=True)
        active = [p for p in procs if p["cpu_pct"] > 0]
        return active[:n] if active else procs[:n]

    def tlb_shootdown_rate(self):
        with self._lock:
            return self._tlb_rate

    def real_core_busy_snapshot(self):
        with self._lock:
            return [round(p * 10) for p in self._cpu_per_core_pct]

    def real_core_history_matrix(self):
        with self._lock:
            if not self._core_history:
                return []
            min_len = min((len(d) for d in self._core_history), default=0)
            return [list(d)[-min_len:] for d in self._core_history] if min_len else []

    def real_cpu_trend_samples(self):
        with self._lock:
            return list(enumerate(self._cpu_total_history))

    def real_pid_sample(self, n=15):
        with self._lock:
            pids = [p["pid"] for p in self._processes]
        return sorted(random.sample(pids, n)) if len(pids) > n else sorted(pids)

    def real_home_file_count(self):
        with self._lock:
            return self._home_files

    def real_self_token_count(self):
        return self._self_lines, self._self_tokens

    def real_self_smoke_test(self):
        return _self_smoke_test()

    def real_entropy_nibble(self):
        return _read_uptime_nibble()

    def real_stat_line(self):
        return _read_cpu_line()

    def real_tcp_sample(self):
        return _read_tcp_sample()

    def real_local_subnet(self):
        return _read_local_subnet()

    def real_arp_count(self):
        return _read_arp_count()


# ───────────────────────── Mathematics (illustrative -- no live system analog) ─────────────────────────

def op_combinatorics(snap):
    n = rnd(20, 60)
    k = rnd(3, n // 2)
    val = math.comb(n, k)
    pigeons = rnd(n + 1, n + 20)
    return "Mathematics · Combinatorics (illustrative)", [
        f"C({n},{k}) = {val:,}",
        f"pigeonhole: {pigeons} items -> {n} boxes => some box holds >= {math.ceil(pigeons / n)}",
    ]


def op_graph_planarity(snap):
    v = rnd(5, 12)
    e = rnd(v, 3 * v - 6 + 4)
    bound = 3 * v - 6
    planar = e <= bound
    return "Mathematics · Graph Theory (illustrative)", [
        f"G(V={v}, E={e}) -- Kuratowski bound 3V-6={bound}",
        f"necessary planarity condition: {'holds (may be planar)' if planar else 'violated -> NOT planar'}",
    ]


def op_linear_algebra(snap):
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
    return "Mathematics · Linear Algebra (illustrative)", [
        f"A = [[{a11},{a12}],[{a21},{a22}]]  det={det}  trace={tr}",
        eig,
    ]


def op_calculus(snap):
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
    return "Mathematics · Calculus (illustrative)", [
        f"Lagrange MVT: f(x)=x^3-3x on [{a},{b}], slope={slope:.4f}",
        cs,
    ]


def op_probability(snap):
    prior = fl(0.01, 0.3)
    tpr = fl(0.85, 0.99)
    fpr = fl(0.01, 0.15)
    post = (tpr * prior) / (tpr * prior + fpr * (1 - prior))
    return "Mathematics · Probability (illustrative)", [
        f"Bayes: P(A)={prior} TPR={tpr} FPR={fpr}",
        f"P(A|B) = {post:.4f}",
    ]


MATH_OPS = [op_combinatorics, op_graph_planarity, op_linear_algebra, op_calculus, op_probability]


# ───────────────────────── OS & Architecture (real, this host) ─────────────────────────

def op_bankers_algorithm(snap):
    procs = snap.top_processes_by_rss(n=3)
    mem = snap.mem()
    if len(procs) < 3 or not mem["total_kb"]:
        return "OS · Deadlock (Banker's, real)", ["not enough real process data sampled yet"]
    avail_mb = max(1, mem["available_kb"] // 1024 // 4)
    alloc = [max(1, p["rss_kb"] // 1024) for p in procs]
    need = [max(1, a // 2) for a in alloc]  # heuristic: 50% headroom over current real RSS, not measured
    names = [p["comm"] for p in procs]
    work = avail_mb
    finish, seq = [False] * 3, []
    changed = True
    while changed:
        changed = False
        for i in range(3):
            if not finish[i] and need[i] <= work:
                work += alloc[i]
                finish[i] = True
                seq.append(i)
                changed = True
    safe = all(finish)
    return "OS · Deadlock (Banker's, real top-RSS processes)", [
        f"real procs={names}  real alloc(MB)={alloc}  avail(MB, 1/4 of real free)={avail_mb}",
        f"safe sequence: {[names[i] for i in seq]}" if safe else "UNSAFE for this real snapshot + heuristic need",
    ]


def op_page_replacement(snap):
    minor, major = snap.pagefault_rate()
    return "OS · Paging (real /proc/vmstat)", [
        f"minor faults/s={minor:.1f}  major faults/s={major:.1f} (measured this tick)",
        "major-fault activity (disk-backed reclaim)" if major > 0.05 else "no major faults this interval",
    ]


def op_round_robin(snap):
    procs = snap.top_processes_by_cpu(n=4)
    if len(procs) < 2:
        return "OS · CPU Scheduling (RR, real)", ["not enough active real processes this tick"]
    names = [p["comm"] for p in procs]
    burst = [max(1, round(p["cpu_pct"])) for p in procs]
    q = 3
    n = len(burst)
    rem, wait, done, t = burst[:], [0] * n, [False] * n, 0
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
    return "OS · CPU Scheduling (RR over real top-CPU processes)", [
        f"real procs={names}  burst(≈real recent CPU%)={burst}  quantum={q}",
        f"avg waiting time={statistics.mean(wait):.2f} (illustrative RR schedule over real burst estimates)",
    ]


def op_cache_lookup(snap):
    rate = snap.tlb_shootdown_rate()
    return "CO&A · TLB shootdowns (real /proc/interrupts)", [
        f"summed across {snap.core_count()} real cores this tick",
        f"shootdown rate={rate:.1f}/s" + (" -- active cross-core invalidation" if rate > 0.5 else " -- idle"),
    ]


def op_pipeline_hazard(snap):
    stages = ["IF", "ID", "EX", "MEM", "WB"]
    i_a, i_b = rnd(1, 4), rnd(5, 8)
    hazard = random.choice(["RAW", "WAR", "WAW", "none"])
    return "CO&A · Pipelining (illustrative -- no userspace signal)", [
        f"5-stage pipeline {stages}, checking I{i_a}/I{i_b}",
        f"hazard: {hazard}" + (" -- forwarding applied" if hazard != "none" else ""),
    ]


OS_ARCH_OPS = [op_bankers_algorithm, op_page_replacement, op_round_robin, op_cache_lookup, op_pipeline_hazard]


# ───────────────────────── Networks & Security (real, local-only reads -- no probing) ─────────────────────────

def _hamming74_encode(d):
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]


def op_hamming_code(snap):
    nibble = snap.real_entropy_nibble()
    d = [(nibble >> i) & 1 for i in (3, 2, 1, 0)]
    code = _hamming74_encode(d)
    flip = rnd(0, 6)  # deliberate corruption -- needed to demo correction; not itself an observed event
    received = code[:]
    received[flip] ^= 1
    p1, p2, d1, p3, d2, d3, d4 = received
    c1 = p1 ^ d1 ^ d2 ^ d4
    c2 = p2 ^ d1 ^ d3 ^ d4
    c3 = p3 ^ d2 ^ d3 ^ d4
    syndrome = c1 + (c2 << 1) + (c3 << 2)
    return "Networks · Hamming(7,4) (real data nibble, synthetic bit-flip)", [
        f"data={''.join(map(str, d))} (real, from /proc/uptime) encoded={''.join(map(str, code))} flipped bit {flip}",
        f"syndrome={syndrome} -> {'no error' if syndrome == 0 else f'corrected bit {syndrome - 1}'}",
    ]


def op_tcp_window(snap):
    conn = snap.real_tcp_sample()
    if not conn:
        return "Networks · TCP (real /proc/net/tcp)", ["no active real TCP sockets found this tick"]
    return "Networks · TCP (real, local read-only, no probing)", [
        f"real socket {conn['local']} <-> {conn['remote']}  state={conn['state']}",
        f"tx_queue={conn['tx_queue']}B rx_queue={conn['rx_queue']}B (kernel's real current values)",
    ]


def op_subnetting(snap):
    subnet = snap.real_local_subnet()
    if not subnet:
        return "Networks · CIDR (real /proc/net/route)", ["no non-default real local route found"]
    return "Networks · CIDR (real, local read-only, no probing)", [
        "kernel's real local route table entry:",
        subnet,
    ]


def op_rsa_toy(snap):
    primes = [11, 13, 17, 19, 23, 29, 31]
    p, q = random.sample(primes, 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = next(x for x in range(2, phi) if math.gcd(x, phi) == 1)
    d = pow(e, -1, phi)
    return "Cyber Security · RSA (toy, illustrative)", [
        f"p={p} q={q} n={n} phi={phi}",
        f"e={e} d={d}",
    ]


def op_sha256(snap):
    real_line = snap.real_stat_line()
    digest = hashlib.sha256(real_line.encode()).hexdigest()
    return "Cyber Security · Hashing (real /proc/stat line)", [
        f'SHA-256("{real_line}")',
        digest,
    ]


NET_SEC_OPS = [op_hamming_code, op_tcp_window, op_subnetting, op_rsa_toy, op_sha256]


# ───────────────────────── Data & Structures (real where a live dataset exists) ─────────────────────────

def op_two_phase_locking(snap):
    txns = rnd(2, 4)
    ops = [f"T{i}: {random.choice(['S-lock', 'X-lock'])}({random.choice('RSTU')})" for i in range(txns)]
    conflict = random.random() < 0.4
    return "Databases · 2PL (illustrative)", [
        ", ".join(ops),
        "conflict -- transaction waits" if conflict else "no conflict -- all granted",
    ]


def op_serializability(snap):
    n = rnd(2, 3)
    order = list(range(n))
    random.shuffle(order)
    return "Databases · Serializability (illustrative)", [
        f"schedule with {n} transactions, precedence graph built",
        f"acyclic -> conflict-serializable, equivalent order: {['T' + str(i) for i in order]}",
    ]


def op_sorting(snap):
    procs = snap.processes()
    if not procs:
        return "DSA · Sorting (real process table)", ["no real process data yet"]
    comparisons = 0

    def qsort(a):
        nonlocal comparisons
        if len(a) <= 1:
            return a
        pivot = a[0]
        less, more = [], []
        for x in a[1:]:
            comparisons += 1
            (less if x[1] < pivot[1] else more).append(x)
        return qsort(less) + [pivot] + qsort(more)

    arr = [(p["comm"], p["rss_kb"]) for p in procs]
    qsort(arr)
    return "DSA · Sorting (real process table by RSS, quicksort)", [
        f"n={len(arr)} real processes on this host",
        f"comparisons={comparisons:,}",
    ]


def op_dijkstra(snap):
    n = max(3, min(12, snap.real_arp_count() or 6))
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
    return "DSA · Graphs (Dijkstra, real node count)", [
        f"{n} nodes = real entries in this host's ARP cache (passive, no scanning); edges synthetic",
        f"shortest dist to node {target} = {d if d != math.inf else 'unreachable'}",
    ]


def op_mapreduce(snap):
    records = snap.real_home_file_count()
    return "Big Data · MapReduce (real file count)", [
        f"mapping {records:,} real files under $HOME across {rnd(4, 32)} mappers",
        f"shuffle phase {rnd(10, 95)}% complete (illustrative progress, real record count)",
    ]


DATA_STRUCT_OPS = [op_two_phase_locking, op_serializability, op_sorting, op_dijkstra, op_mapreduce]


# ───────────────────────── Theory & Languages ─────────────────────────

def op_dfa(snap):
    states = rnd(2, 6)
    alphabet = random.choice(["{0,1}", "{a,b}"])
    lang = random.choice([
        "even number of 0s", "ends in 01", "divisible by 3 (binary)", "no two consecutive 1s",
    ])
    return "Theory of Computation · DFA (illustrative)", [
        f"L = {{w : {lang}}}, alphabet {alphabet}",
        f"minimized DFA: {states} states",
    ]


def op_turing_machine(snap):
    steps = rnd(10, 80)
    inp = "".join(random.choices("01", k=rnd(4, 10)))
    accept = random.random() < 0.7
    return "Theory of Computation · Turing Machine (illustrative)", [
        f"simulating TM on input {inp}",
        f"{steps} steps -> {'ACCEPT' if accept else 'REJECT'}",
    ]


def op_pumping_lemma(snap):
    lang = random.choice(["a^n b^n", "ww (w in {0,1}*)", "a^(n^2)"])
    return "Theory of Computation · Pumping Lemma (illustrative)", [
        f"applying pumping lemma to L = {lang}",
        "contradiction found -> language not regular",
    ]


def op_c_pointers(snap):
    arr = snap.real_core_busy_snapshot()
    if len(arr) < 2:
        return "Programming Language · C Pointers (real per-core busy‰)", ["not enough real cores sampled yet"]
    i = rnd(0, len(arr) - 1)
    return "Programming Language · C Pointers (real per-core busy‰)", [
        f"int arr[{len(arr)}] = {arr}  // real per-core busy‰ this tick",
        f"*(arr + {i}) = {arr[i]}",
    ]


def op_python_comprehension(snap):
    pids = snap.real_pid_sample(n=15)
    result = [p for p in pids if p % 2 == 0]
    return "Programming Language · Python (real live PIDs)", [
        f"[p for p in {pids} if p%2==0]",
        f"= {result}",
    ]


def op_lexer(snap):
    lines, tokens = snap.real_self_token_count()
    return "Compiler Design · Lexical Analysis (real, this script's own source)", [
        f"tokenizing bluff.py's own real source ({lines} real lines)",
        f"{tokens:,} real tokens produced (stdlib tokenize)",
    ]


THEORY_LANG_OPS = [op_dfa, op_turing_machine, op_pumping_lemma, op_c_pointers, op_python_comprehension, op_lexer]


# ───────────────────────── Applied CS (real where a live dataset exists) ─────────────────────────

def op_linear_regression(snap):
    samples = snap.real_cpu_trend_samples()
    if len(samples) < 5:
        return "AI/ML · Linear Regression (real CPU trend)", ["collecting real samples..."]
    xs = [x for x, _ in samples]
    ys = [y for _, y in samples]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    m = num / den if den else 0
    b = my - m * mx
    ss_res = sum((y - (m * x + b)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot else 0
    return "AI/ML · Linear Regression (real measured CPU busy% trend)", [
        f"n={len(xs)} real samples, fitting y=mx+b over this run's real tick history",
        f"m={m:.3f} b={b:.3f} R^2={r2:.4f}",
    ]


def op_knn(snap):
    procs = snap.processes()
    if len(procs) < 3:
        return "AI/ML · K-Nearest Neighbor (real processes)", ["not enough real processes"]
    target = procs[0]

    def dist(p):
        return math.hypot(p["cpu_pct"] - target["cpu_pct"], (p["rss_kb"] - target["rss_kb"]) / 1024)

    nearest = min(procs[1:], key=dist)
    return "AI/ML · K-Nearest Neighbor (real process resource space)", [
        f"target={target['comm']} (cpu%={target['cpu_pct']:.1f}, rss={target['rss_kb']}KB)",
        f"nearest real neighbor by (cpu%,rss) = {nearest['comm']} dist={dist(nearest):.2f}",
    ]


def op_kmeans(snap):
    procs = snap.processes()
    if len(procs) < 6:
        return "AI/ML · K-Means (real processes)", ["not enough real processes"]
    pts = [(p["cpu_pct"], p["rss_kb"] / 1024) for p in procs]
    k = min(4, max(2, len(pts) // 5))
    centers = random.sample(pts, k)
    for _ in range(10):
        clusters = [[] for _ in range(k)]
        for p in pts:
            idx = min(range(k), key=lambda i: math.hypot(p[0] - centers[i][0], p[1] - centers[i][1]))
            clusters[idx].append(p)
        centers = [
            (statistics.mean(x for x, _ in c), statistics.mean(y for _, y in c)) if c else centers[i]
            for i, c in enumerate(clusters)
        ]
    inertia = sum(min(math.hypot(p[0] - c[0], p[1] - c[1]) ** 2 for c in centers) for p in pts)
    return "AI/ML · K-Means (real process cpu%/mem clusters)", [
        f"k={k}, {len(pts)} real processes as points (cpu%, rss MB)",
        f"real inertia={inertia:.1f} after 10 iterations",
    ]


def op_edge_detection(snap):
    matrix = snap.real_core_history_matrix()
    if not matrix or len(matrix[0]) < 3:
        return "Image/Vision · Sobel Edge Detection (real per-core CPU-history 'image')", ["collecting real history..."]
    edges = total = 0
    for row in matrix:
        for i in range(1, len(row) - 1):
            total += 1
            if abs(row[i + 1] - row[i - 1]) > 15:
                edges += 1
    density = (edges / total * 100) if total else 0
    return "Image/Vision · Sobel Edge Detection (real per-core CPU-history 'image')", [
        f"{len(matrix)}x{len(matrix[0])} real matrix (cores x recent busy% ticks)",
        f"edge density={density:.1f}% (real load-jump rate, |busy%Δ|>15pp)",
    ]


def op_histogram_eq(snap):
    procs = snap.processes()
    sizes = [p["rss_kb"] for p in procs if p["rss_kb"] > 0]
    if len(sizes) < 5:
        return "Image/Vision · Histogram Equalization (real process RSS)", ["not enough real data"]
    sorted_sizes = sorted(sizes)
    n = len(sizes)
    rank = {v: i for i, v in enumerate(sorted_sizes)}
    equalized = [rank[s] / (n - 1) * 100 for s in sizes]
    before_mb = statistics.pstdev(sizes) / 1024
    after = statistics.pstdev(equalized)
    return "Image/Vision · Histogram Equalization (real process RSS distribution)", [
        f"n={n} real processes, contrast(before, RSS stddev MB)={before_mb:.1f}",
        f"contrast(after, rank-equalized 0-100 stddev)={after:.1f}",
    ]


def op_sdlc(snap):
    stories = rnd(4, 12)
    velocity = rnd(15, 45)
    phase = random.choice(["planning", "design", "implementation", "testing", "retrospective"])
    return "Software Engineering · Agile SDLC (illustrative)", [
        f"sprint {phase}: {stories} stories estimated",
        f"velocity={velocity}",
    ]


def op_unit_tests(snap):
    total, failed, names = snap.real_self_smoke_test()
    return "Software Engineering · Testing (real self smoke-test)", [
        f"running {total} real checks of this script's own /proc readers",
        f"all {total} passed" if not failed else f"{total - failed} passed, {failed} failed: {names}",
    ]


def op_vm_provision(snap):
    vcpu = snap.core_count()
    mem = snap.mem()
    used_pct = 100 * (1 - mem["available_kb"] / mem["total_kb"]) if mem["total_kb"] else 0
    return "Cloud Computing · Host Capacity (real; no VM actually provisioned)", [
        f"this host: {vcpu} real vCPUs, {mem['total_kb'] / 1024 / 1024:.1f}GB real RAM",
        f"real current memory utilization={used_pct:.1f}%",
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


def worker_loop(panel, snap, stop_event):
    while not stop_event.is_set():
        tag, lines = random.choice(panel.ops)(snap)
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

    snap = SystemSnapshot()
    stop_event = threading.Event()
    threads = [threading.Thread(target=worker_loop, args=(p, snap, stop_event), daemon=True) for p in panels]
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
            header = f" bluff -- study-notes activity monitor (real local telemetry)   {ts()}   uptime {int(time.time() - start)}s"
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
        snap.stop()


def main():
    try:
        curses.wrapper(_main)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
