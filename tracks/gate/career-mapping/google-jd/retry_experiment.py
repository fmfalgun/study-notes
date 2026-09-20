"""Detached, resumable retry experiment: re-fetch the SAME URL+timestamp pairs (guarded pace via ArchiveFetcher/RequestGuard).
Idempotent: pairs already in retry_experiment_results.json are skipped. Aborts if STOP exists or COMMANDS.md changed since start."""
import sys, json, os, re, time, hashlib
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from datetime import datetime
from scraper_core import wayback
D = Path("./tracks/gate/career-mapping/google-jd")
RES = D / "retry_experiment_results.json"
def atomic(path, text):
    tmp = str(path) + ".tmp"; Path(tmp).write_text(text); os.replace(tmp, path)
def textlen(b):
    t = re.sub(rb"(?s)<(script|style)[^>]*>.*?</\1>", b"", b); t = re.sub(rb"<[^>]+>", b" ", t)
    return len(re.sub(rb"\s+", b" ", t).strip())
pairs = json.loads((D / "retry_experiment_pairs.json").read_text())
results = json.loads(RES.read_text()) if RES.exists() else {}
cmd_mtime = (D / "COMMANDS.md").stat().st_mtime
fetcher = wayback.ArchiveFetcher()
last = None
for p in pairs:
    key = f'{p["job_id"]}_{p["ts"]}'
    if key in results: continue
    if (D / "STOP").exists() or (D / "COMMANDS.md").stat().st_mtime != cmd_mtime:
        print("abort: STOP or COMMANDS.md changed", flush=True); break
    try:
        r = fetcher.fetch(p["ts"], p["url"])
    except (wayback.Throttled, wayback.Offline) as e:
        print("halt:", type(e).__name__, e, flush=True); break
    now = time.time()
    body = r.get("body")
    rec = {**p, "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"), "gap_s": None if last is None else round(now - last, 1),
           "ok": r["ok"], "status": r.get("status"), "error": r.get("error"), "wire_bytes": r.get("bytes"), "decoded_len": r.get("decoded_bytes"),
           "secs": r.get("secs"), "sha256": hashlib.sha256(body).hexdigest() if body else None, "text_chars": textlen(body) if body else None}
    last = now
    if body: (D / "retry_raw" / f"{key}.html").write_bytes(body)
    results[key] = rec
    atomic(RES, json.dumps(results, indent=1))
    with open(D / "requests.jsonl", "a") as f: f.write(json.dumps({"t": rec["fetched_at"], "job_id": p["job_id"], "ts": p["ts"], "ok": r["ok"], "status": r.get("status"), "why": "retry_experiment"}) + "\n")
    print(rec["fetched_at"], key, rec["ok"], rec["wire_bytes"], rec["decoded_len"], rec["text_chars"], flush=True)
print("DONE", len(results), "/", len(pairs), flush=True)
