"""Detached driver: repeat qualcomm_live_security_roles until DONE or a stop state.
Run from the web-scrap dir:  .venv/bin/python3 <this file>   (resumable; never touches robots.txt)"""
import sys, time
sys.path.insert(0, "../no-github-remote/web-scrap")
from plugins.job_search import REGISTRY
from plugins.job_search.qualcomm_live import TERMS

first = True   # the 429 halt from 2026-10-10 is cleared once, on the user's say-so (2026-10-11)
run = REGISTRY["qualcomm_live_security_roles"]["run"]
while True:
    out = run(None, None, terms=TERMS, max_loads=40, clear_halt=first, no_early_stop=True)
    first = False
    print(time.strftime("%F %T"), out, flush=True)
    if out["status"] in ("DONE", "PAUSED_BLOCKED", "HALTED", "OFFLINE_WAITING", "LOCKED"):
        break
    if out["status"] == "HOURLY_CAP":
        time.sleep(600)
