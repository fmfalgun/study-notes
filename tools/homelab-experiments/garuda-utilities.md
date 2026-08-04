# Garuda — Available System Utilities & Real-Time Data Sources

Inventory of what's actually on this machine for pulling real-time system telemetry into an
experiment, so future topics don't re-discover this from scratch — check here first, then only
verify what's missing or look for a better alternative.

**Last verified**: 2026-07-17 · **OS/package manager**: Garuda Linux (Arch-based) → `pacman`

## Confirmed present

| Tool | Type | Useful for |
|---|---|---|
| `psutil` (Python, v7.2.2) | library | Single cross-platform source for CPU%, memory%, per-core %, network I/O, process counts — the default choice unless a specific gap needs a raw source below. |
| `/proc/stat`, `/proc/meminfo`, `/proc/net/dev`, `/proc/interrupts` | raw kernel interface | Same data as `psutil` without the dependency; per-core CPU ticks, per-IRQ interrupt counts, per-interface byte/packet counters. |
| `vmstat` | CLI | Quick CPU/mem/swap/IO snapshot, good for spot-checks. |
| `ss` | CLI | Active socket/connection counts and states at an instant. |
| `ip` | CLI | Interface-level network stats. |
| `journalctl` | CLI (systemd) | Structured event log — auth failures, service start/stop, kernel events; filterable by unit/time. |
| `sensors` (lm-sensors) | CLI | Temperature/fan/voltage readings, if sensors are configured. |

## Confirmed missing (installable via `pacman` if a task needs them)

| Tool | Type | Would add |
|---|---|---|
| `mpstat`, `sar`, `iostat` | CLI (`sysstat` package) | Per-core CPU breakdown (`mpstat -P ALL`) and historical sampling (`sar`) beyond what `vmstat`/`psutil` give as a single snapshot. |
| `nmon`, `dstat`, `glances` | CLI | Higher-level combined dashboards — not needed since `psutil` already covers this in scriptable form. |

## Known gotcha

Running a Python script with `homelab-experiments/` on `sys.path` (e.g. invoking from this
directory) shadows the stdlib `select` module with this folder's own `select.py`, which broke
`psutil`'s import chain (`subprocess` → `selectors` → `select.select`) until re-tested from a
different working directory. Any experiment script that needs `psutil` or anything importing
`selectors` should run from its own `script/` subdirectory, not from `homelab-experiments/` root.

## Verification command (re-run after installing anything, or on a fresh machine)

```bash
echo "CPU/mem/proc sources:"
for f in /proc/stat /proc/meminfo /proc/interrupts /proc/net/dev; do
  test -r "$f" && echo "$f: yes" || echo "$f: MISSING"
done
echo "Utility availability:"
for cmd in vmstat mpstat sar iostat ss ip journalctl sensors nmon dstat glances; do
  command -v "$cmd" >/dev/null 2>&1 && echo "$cmd: present" || echo "$cmd: MISSING"
done
cd /tmp && python3 -c "import psutil; print('psutil:', psutil.__version__)"
```
