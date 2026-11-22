"""Patient driver: after an HTTP 429 halt, wait, clear the halt, try a SMALL batch, and back off if refused again.
Resumes the saved walk (security deep pages, then exploit). Stops on DONE / OFFLINE / LOCKED or after MAX_CYCLES.
Run from anywhere with the web-scrap venv. Never touches robots.txt."""
import sys, time
sys.path.insert(0, "../no-github-remote/web-scrap")
from plugins.job_search import REGISTRY
from plugins.job_search.qualcomm_live import TERMS

run = REGISTRY["qualcomm_live_security_roles"]["run"]
wait_min, MAX_CYCLES = 60, 12
for cycle in range(MAX_CYCLES):
    print(time.strftime("%F %T"), f"cycle {cycle}: sleeping {wait_min} min", flush=True)
    time.sleep(wait_min * 60)
    out = run(None, None, terms=TERMS, max_loads=8, clear_halt=True, no_early_stop=True)
    print(time.strftime("%F %T"), out, flush=True)
    if out["status"] == "DONE":
        break
    if out["status"] in ("OFFLINE_WAITING", "LOCKED"):
        wait_min = 30
    elif out["status"] == "PAUSED_BLOCKED":
        wait_min = min(wait_min * 2, 240)   # refused again: back off (1h, 2h, 4h, 4h...)
    else:
        wait_min = 20                       # batch went through: continue soon
