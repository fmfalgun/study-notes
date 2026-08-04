# Telemetry Claims Ledger

One-glance answer to "is this signal already spoken for?" — the analogue of `bluff`'s
lab2→...→lab9 lineage table, applied to real-system telemetry instead of BLE. Check this
table **before** writing a new topic's `scope.md` § Input. If a row already claims the
metric you're about to read, either build on that topic (same `<topic-slug>`, don't fork a
second consumer of the same source) or pick a different metric — never let two topics read
and analyze the same signal independently.

This file restates nothing from any `scope.md` — it only points at them. The `scope.md`
Input section remains the source of truth for exactly what's read; update this table in the
same commit that adds or changes a `scope.md` Input section.

## Claimed

| Metric / signal | Source | Device | Owning topic | Scope |
|---|---|---|---|---|
| CPU busy % | `/proc/stat` | `proone` | `distribution-fitting-toolkit` | [scope.md](distribution-fitting-toolkit/proone/scope.md) |
| Interrupts/interval | `/proc/interrupts` | `proone` | `distribution-fitting-toolkit` | [scope.md](distribution-fitting-toolkit/proone/scope.md) |
| Per-core busy count | `/proc/stat` (per-core) | `proone` | `distribution-fitting-toolkit` | [scope.md](distribution-fitting-toolkit/proone/scope.md) |

## Unclaimed (available per the utilities inventory, nobody reads these yet)

| Metric / signal | Source | Devices confirmed available |
|---|---|---|
| Memory / swap | `/proc/meminfo` | `garuda` (confirmed); `rpi5`/`probook`/`proone` pending verification |
| Per-interface network I/O | `/proc/net/dev`, `ip` | `garuda` (confirmed); others pending |
| Socket/connection state | `ss` | `garuda` (confirmed); others pending |
| Structured event log (auth, service start/stop, kernel) | `journalctl` | `garuda` (confirmed); others pending |
| Temperature/fan/voltage | `sensors` | `garuda` (confirmed; note `rpi5-utilities.md` flags this as unverified on that machine) |
| Process-level scheduling (run-queue, context-switches, per-PID state) | `/proc/<pid>/*`, `/proc/stat` | not yet checked on any machine |

Not on this list = not yet inventoried anywhere — run the verification command in that
device's `<device-key>-utilities.md` first, since a metric can't be claimed until it's
confirmed to exist on the machine in question.

## Non-homelab consumer: `bluff.py`

`bluff.py` (`tools/bluff.py`, not a `homelab-experiments` topic) reads real local state on
whichever machine it's launched from — typically `garuda`, the daily driver, which has no
`homelab-experiments` topic of its own. All reads are passive/local (`/proc/stat`,
`/proc/meminfo`, `/proc/vmstat`, `/proc/interrupts` TLB line, `/proc/net/tcp`,
`/proc/net/route`, `/proc/net/arp`, `/proc/<pid>/*`) — nothing is sent to another host.

| Metric / signal | Used for |
|---|---|
| CPU busy % (aggregate + per-core), via `/proc/stat` | RR-scheduling burst estimate, C-pointer array, Sobel edge-detection matrix, linear-regression trend |
| Minor/major page-fault rate, via `/proc/vmstat` | Paging panel |
| TLB shootdown rate, via `/proc/interrupts` | Cache-lookup panel |
| Process table (comm/cpu%/RSS), via `/proc/<pid>/*` | Banker's algorithm, RR burst, quicksort, KNN, K-Means, histogram equalization |
| TCP table / route table / ARP cache, via `/proc/net/*` | TCP window, CIDR/subnetting, Dijkstra node count |

**Flagging for confirmation, not deciding unilaterally**: this overlaps in *raw source*
(`/proc/stat` CPU busy%) with `distribution-fitting-toolkit`'s claim above, but not in
*device* (garuda vs. proone) or *purpose* (live UI grounding + one-shot algorithm demos vs.
MLE distribution-fitting with a persisted baseline/anomaly pipeline). Treating device+purpose
as the claim boundary — consistent with `bluff`'s BLE/Zigbee split being about the domain,
not literally every byte read — is a judgment call; if the intent was stricter (no metric
reused anywhere, full stop), this row needs to be renegotiated.

- `distribution-fitting-toolkit/proone/script/run_monitor.py` — reads `status.json`, which
  is the *output* of the claimed row above, not an independent read of the underlying
  source. Presentation layer, not a second analysis.

## Adding a row

When step 4 of the picking-a-task funnel (README.md) produces a new `scope.md` with a
real-telemetry Input, add one row to **Claimed** in the same commit, and remove the
corresponding row (or narrow it) from **Unclaimed** if it was listed there.
