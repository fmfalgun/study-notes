#!/usr/bin/env python3
"""Live dashboard for sampling_daemon.py — a btop-style view, fully decoupled from the daemon.

This never talks to the daemon process directly; it only polls results/status.json (written
atomically every tick by sampling_daemon.py) once a second and redraws. That means you can start
this in its own terminal at any time — before the daemon starts, while it's running detached
under nohup, over a separate SSH session, whatever — without touching the running daemon at all.
Closing this monitor never affects the daemon, and vice versa.

Usage: python3 run_monitor.py
Quit: press q (or Ctrl+C)

Stdlib only (curses) — nothing to install, same "just transfer and run" principle as the daemon.
"""

import curses
import json
import time
from pathlib import Path

STATUS_FILE = Path(__file__).parent / "results" / "status.json"

# If the daemon hasn't written a fresh status in longer than this many multiples of its own
# interval, treat it as stopped/stuck rather than just "between ticks" — a single missed tick is
# normal, several in a row means the process is gone.
STALE_AFTER_INTERVALS = 3


def load_status() -> dict | None:
    if not STATUS_FILE.exists():
        return None
    try:
        return json.loads(STATUS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        # Extremely unlikely given the atomic write in sampling_daemon.py, but if it ever
        # happens, just skip this frame rather than crash the monitor over a display glitch.
        return None


def format_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def draw(win, status: dict | None) -> None:
    win.erase()
    max_y, max_x = win.getmaxyx()

    def put(row: int, text: str, attr=0) -> None:
        if 0 <= row < max_y:
            win.addstr(row, 0, text[: max_x - 1], attr)

    bold = curses.A_BOLD
    put(0, "Distribution-Fitting Toolkit — Live Monitor (proone)", bold)

    if status is None:
        put(2, f"Waiting for daemon... no {STATUS_FILE} yet.")
        put(3, "Start it in another terminal: python3 run_daemon.py")
        put(max_y - 1, "Press q to quit — polling every 1s", curses.A_DIM)
        return

    now = time.time()
    interval = status["interval_seconds"]
    since_last_tick = now - status["last_tick_at"]
    is_stale = since_last_tick > interval * STALE_AFTER_INTERVALS

    state_label = "STALE (daemon may have stopped)" if is_stale else "RUNNING"
    state_attr = (curses.color_pair(2) | bold) if is_stale else (curses.color_pair(1) | bold)
    put(1, f"Status: {state_label}", state_attr)

    next_in = max(0.0, interval - since_last_tick)
    put(3, f"PID: {status['pid']}   Uptime: {format_duration(now - status['started_at'])}   "
           f"Interval: {interval:.0f}s   Next sample in: ~{next_in:.0f}s")

    row = 5
    put(row, "Latest sample:", bold)
    row += 1
    sample = status["last_sample"]
    if sample is None:
        put(row, "  (warming up — first tick has no delta to compute yet)")
        row += 1
    else:
        age = now - sample["timestamp"]
        put(row, f"  CPU busy: {sample['cpu_busy_pct']:5.1f}%   "
                 f"Busy cores: {sample['busy_cores']}/{sample['n_cores']}   "
                 f"Interrupts/interval: {sample['interrupts_delta']}   ({age:.0f}s ago)")
        row += 1
    row += 1

    progress = status["batch_progress"]
    size = status["batch_size"]
    filled = int((progress / size) * 20) if size else 0
    bar = "#" * filled + "." * (20 - filled)
    put(row, f"Batch progress: [{bar}] {progress}/{size}", bold)
    row += 2

    baseline = status["baseline_fit"]
    put(row, "Baseline:", bold)
    row += 1
    if baseline is None:
        put(row, "  not yet established (needs one full batch)")
        row += 1
    else:
        put(row, f"  normal:   mu={baseline['normal']['mu']:.2f}  sigma={baseline['normal']['sigma']:.2f}")
        row += 1
        put(row, f"  poisson:  lambda={baseline['poisson']['lam']:.2f}")
        row += 1
        put(row, f"  binomial: p={baseline['binomial']['p']:.4f}")
        row += 1
    row += 1

    put(row, "Last batch fit / drift check:", bold)
    row += 1
    last_fit = status["last_batch_fit"]
    drift = status["last_drift"] or []
    if last_fit is None:
        put(row, "  (no batch completed yet)")
        row += 1
    else:
        for name, value in (
            ("normal", f"mu={last_fit['normal']['mu']:.2f}"),
            ("poisson", f"lambda={last_fit['poisson']['lam']:.2f}"),
            ("binomial", f"p={last_fit['binomial']['p']:.4f}"),
        ):
            flag = "DRIFT" if name in drift else "OK"
            attr = (curses.color_pair(2) | bold) if name in drift else curses.color_pair(1)
            put(row, f"  {name:<9} {value:<20} [{flag}]", attr)
            row += 1
    row += 1

    counters = status["counters"]
    put(row, f"Totals: samples={counters['total_samples']}  batches={counters['total_batches']}  "
             f"anomalies={counters['total_anomalies']}  errors={counters['total_errors']}", bold)
    row += 2

    put(row, f"Results dir: {STATUS_FILE.parent}", curses.A_DIM)
    put(max_y - 1, "Press q to quit — refreshing every 1s", curses.A_DIM)


def main(win) -> None:
    curses.curs_set(0)  # hide the cursor — this is a dashboard, not an input prompt
    win.timeout(1000)  # blocks up to 1s waiting for a keypress, giving us a 1Hz refresh for free

    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)

    while True:
        draw(win, load_status())
        win.refresh()
        key = win.getch()
        if key in (ord("q"), ord("Q")):
            break


if __name__ == "__main__":
    curses.wrapper(main)
