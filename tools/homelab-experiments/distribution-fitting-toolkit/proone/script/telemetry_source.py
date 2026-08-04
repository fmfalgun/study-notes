"""stdlib-only real-time telemetry readers — reads directly from /proc, no external
dependencies (no psutil/numpy/scipy). /proc/stat and /proc/interrupts are always present on any
Linux (see ../../garuda-utilities.md), which is why this uses them directly instead of psutil:
nothing to install, nothing that can be missing on a machine we haven't verified yet.
"""

from pathlib import Path

PROC_STAT = Path("/proc/stat")
PROC_INTERRUPTS = Path("/proc/interrupts")


def read_cpu_lines() -> dict[str, list[int]]:
    """Parse /proc/stat's 'cpu' (aggregate) and 'cpuN' (per-core) lines into raw tick counters.

    Each line's fields after the label are, in order: user, nice, system, idle, iowait, irq,
    softirq, steal, guest, guest_nice (per the kernel's proc(5) documentation). We keep every
    field so the busy/idle split below stays exact rather than an approximation.
    """
    lines: dict[str, list[int]] = {}
    with PROC_STAT.open() as f:
        for line in f:
            parts = line.split()
            if parts and parts[0].startswith("cpu"):
                lines[parts[0]] = [int(x) for x in parts[1:]]
            elif lines:
                # cpu/cpuN lines are always first in /proc/stat; once we've collected at least
                # one and hit a non-cpu line, there are no more left to read.
                break
    return lines


def busy_fraction(prev_ticks: list[int], curr_ticks: list[int]) -> float:
    """Fraction of time a /proc/stat line was busy (not idle) between two snapshots.

    idle is field index 3 (0-based: user, nice, system, idle, ...); everything else counts as
    "busy" for our purposes — we don't need the iowait/irq/steal breakdown, just busy-vs-idle.
    """
    prev_total, curr_total = sum(prev_ticks), sum(curr_ticks)
    prev_idle, curr_idle = prev_ticks[3], curr_ticks[3]

    total_delta = curr_total - prev_total
    idle_delta = curr_idle - prev_idle
    if total_delta <= 0:
        return 0.0
    return 1.0 - (idle_delta / total_delta)


def read_interrupts_total() -> int:
    """Sum every interrupt count across every IRQ line in /proc/interrupts.

    Columns are: IRQ label, then one count per CPU, then a description. We sum only the numeric
    per-CPU columns — the int() conversion failing on the description text is what tells us
    we've run out of numeric columns on that line.
    """
    total = 0
    with PROC_INTERRUPTS.open() as f:
        next(f)  # header line ("CPU0 CPU1 ...") — not data, skip it
        for line in f:
            for token in line.split()[1:]:  # drop the leading "NN:" IRQ label
                try:
                    total += int(token)
                except ValueError:
                    break  # hit the description text; no more numeric columns on this line
    return total
