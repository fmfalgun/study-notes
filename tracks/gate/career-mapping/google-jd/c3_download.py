"""C3: detached, resumable, balanced download of security-posting descriptions (web.archive.org only, guarded 60-120 s pace).
Resume: cd ../no-github-remote/web-scrap && nohup .venv/bin/python3 <this file> >> <dir>/c3_download.log 2>&1 &
Safe to kill any time: state lives in scraper-data shards+ledger; restart skips finished ids. Exits at the next posting if google-jd/STOP exists
or COMMANDS.md changed (the agent re-reads it and relaunches). Progress counters: c3_progress.json (atomic)."""
import sys, json, os, time, random
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from scraper_core import wayback
from plugins.job_search import wayback_google_details as g
D = Path("./tracks/gate/career-mapping/google-jd")
REPO = Path("../no-github-remote/scraper-data")
CHUNK = 25
YEAR_ORDER = ["2026", "2025", "2024", "2023"]
cmd_mtime = (D / "COMMANDS.md").stat().st_mtime

def now(): return datetime.now().astimezone().isoformat(timespec="seconds")
def log(*a):
    print(now(), *a, flush=True)
def atomic(path, text):
    tmp = str(path) + ".tmp"; Path(tmp).write_text(text); os.replace(tmp, path)
def heartbeat(msg):
    with open(D / "progress.md", "a") as f: f.write(f"[{datetime.now().strftime('%H:%M:%S IST')}] {msg}\n")

class Abort(Exception): pass
def check_abort(*_):
    if (D / "STOP").exists(): raise Abort("STOP file")
    if (D / "COMMANDS.md").stat().st_mtime != cmd_mtime: raise Abort("COMMANDS.md changed")

class LoggedFetcher(wayback.ArchiveFetcher):
    def fetch(self, timestamp, url, **kw):
        r = super().fetch(timestamp, url, **kw)
        with open(D / "requests.jsonl", "a") as f:
            f.write(json.dumps({"t": now(), "ts": timestamp, "ok": r["ok"], "status": r.get("status"), "why": "c3"}) + "\n")
        return r

def counts():
    shards, ledger = g._load_state(REPO)
    by_year = {y: len(p) for y, p in sorted(shards.items())}
    return shards, ledger, by_year

def ordered_pending(shards, ledger):
    stored = {j for p in shards.values() for j in p}
    per_year = defaultdict(lambda: defaultdict(list))
    for t in g.security_targets(REPO):
        if t["job_id"] in stored or t["job_id"] in ledger: continue
        caps = g.pick_captures(t["captures"])
        if not caps: continue
        per_year[caps[0][0][:4]][t["theme"]].append(t["job_id"])
    rng = random.Random(7)
    queues = {}
    for y, themes in per_year.items():
        for lst in themes.values(): rng.shuffle(lst)
        q, lists = [], [themes[k] for k in sorted(themes)]
        while any(lists):
            for l in lists:
                if l: q.append(l.pop())
        queues[y] = q
    order, years = [], [y for y in YEAR_ORDER if y in queues] + [y for y in sorted(queues) if y not in YEAR_ORDER]
    while any(queues[y] for y in years):
        for y in years:
            if queues[y]: order.append(queues[y].pop(0))
    return order

def write_progress(status, extra=""):
    shards, ledger, by_year = counts()
    stored = sum(by_year.values())
    pend = ordered_pending(shards, ledger)
    prog = {"updated": now(), "status": status, "stored_total": stored, "stored_by_description_year": by_year,
            "ledgered_by_reason": dict(Counter(e["reason"] for e in ledger.values())), "remaining_requestable": len(pend), "note": extra}
    atomic(D / "c3_progress.json", json.dumps(prog, indent=1))
    return prog, pend

def main():
    check_abort()
    # 1) ledger the old-only postings WITHOUT any request (they have no new-format capture)
    shards, ledger, _ = counts()
    old_only = [t["job_id"] for t in g.security_targets(REPO) if not g.pick_captures(t["captures"]) and t["job_id"] not in ledger]
    if old_only:
        r = g.fetch_details(REPO, job_ids=old_only, shard_size=100000)
        log("ledgered old-only (no requests):", r)
    fetcher = LoggedFetcher()
    prog, pend = write_progress("DOWNLOADING")
    log("start; stored", prog["stored_total"], "remaining", len(pend))
    last_stored = prog["stored_total"]
    while pend:
        chunk = pend[:CHUNK]
        try:
            res = g.fetch_details(REPO, job_ids=chunk, fetcher=fetcher, shard_size=CHUNK, on_progress=check_abort)
        except Abort as e:
            log("abort:", e); write_progress("ABORTED_" + str(e).split()[0]); return
        except wayback.Offline as e:
            log("offline; waiting 10 min", e); heartbeat(f"C3 DOWNLOADING: machine OFFLINE, waiting 10 min then retrying ({e})")
            time.sleep(600); fetcher.reset(); continue
        log("chunk", res)
        shards, ledger, by_year = counts()
        if sum(by_year.values()) < last_stored:
            log("VERIFY FAILED: stored count went DOWN; halting"); write_progress("HALTED_VERIFY"); return
        last_stored = sum(by_year.values())
        prog, pend = write_progress("DOWNLOADING")
        if res["status"] == "paused_throttled":
            heartbeat(f"STATUS: PAUSED_THROTTLED (C3; 5 consecutive failures) - no requests for 60 min, then one probe. stored {last_stored}")
            write_progress("PAUSED_THROTTLED")
            for _ in range(720):
                time.sleep(5)
                try: check_abort()
                except Abort as e: log("abort:", e); return
            fetcher.reset()
    write_progress("MAIN_RUN_DONE")
    log("MAIN RUN DONE"); heartbeat("C3 main run finished (see c3_progress.json)")

if __name__ == "__main__":
    main()
