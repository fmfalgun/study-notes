# Raspberry Pi 5 — Available System Utilities & Real-Time Data Sources

**Last verified**: not yet — this machine hasn't been checked directly from a Claude Code session.
**OS/package manager**: Debian trixie (per `rpi5-cs-eng.md`) → `apt`

Run the verification command below the first time work starts on this machine, then fill in the
Confirmed present/missing tables the same way `garuda-utilities.md` does — don't re-derive from
scratch, just check what's actually different here vs. `garuda-utilities.md`'s findings. Note this
machine has no `sensors`-visible thermal setup guaranteed (SD-card/ARM64 specifics may differ from
the other three) — worth double-checking rather than assuming.

## Verification command

```bash
echo "CPU/mem/proc sources:"
for f in /proc/stat /proc/meminfo /proc/interrupts /proc/net/dev; do
  test -r "$f" && echo "$f: yes" || echo "$f: MISSING"
done
echo "Utility availability:"
for cmd in vmstat mpstat sar iostat ss ip journalctl sensors nmon dstat glances; do
  command -v "$cmd" >/dev/null 2>&1 && echo "$cmd: present" || echo "$cmd: MISSING"
done
python3 -c "import psutil; print('psutil:', psutil.__version__)" 2>&1 || echo "psutil: MISSING (pip/apt install)"
```

## Confirmed present

*(pending — run the command above on this machine)*

## Confirmed missing

*(pending)*
