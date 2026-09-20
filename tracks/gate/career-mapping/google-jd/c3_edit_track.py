"""C3 extra (b): edit tracking. For described postings whose LATEST new-format capture is >=182 days after the stored text's capture,
fetch that latest capture (ONE request each, web.archive.org only, default guard 60-120 s / floor 45 s / 40 per h) and compare with stored text.
Resumable: results appended (fsync) to c3_edit_results.jsonl; finished ids skipped. Aborts if google-jd/STOP exists or COMMANDS.md changed.
Resume: cd ../no-github-remote/web-scrap && nohup .venv/bin/python3 <this file> >> <dir>/c3_edit_track.log 2>&1 &"""
import sys, json, os, time, difflib
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from datetime import datetime
from scraper_core import wayback
from plugins.job_search import wayback_google_details as g
D = Path("./tracks/gate/career-mapping/google-jd")
REPO = Path("../no-github-remote/scraper-data")
OUT = D / "c3_edit_results.jsonl"
cmd_mtime = (D / "COMMANDS.md").stat().st_mtime
def now(): return datetime.now().astimezone().isoformat(timespec="seconds")
def log(*a): print(now(), *a, flush=True)
def norm(s): return [l.strip().lstrip("- ").strip() for l in s.split("\n") if l.strip()]
class LoggedFetcher(wayback.ArchiveFetcher):
    def fetch(self, timestamp, url, **kw):
        r = super().fetch(timestamp, url, **kw)
        with open(D / "requests.jsonl", "a") as f:
            f.write(json.dumps({"t": now(), "ts": timestamp, "ok": r["ok"], "status": r.get("status"), "why": "c3_edit"}) + "\n")
        return r
def compare(stored, parsed):
    res = {}
    for sec in ["about", "responsibilities", "minimum_qualifications", "preferred_qualifications"]:
        a, b = norm(stored["sections"].get(sec, "")), norm(parsed["sections"].get(sec, ""))
        res[sec] = {"identical": a == b, "stored_lines": len(a), "latest_lines": len(b),
                    "removed": [x for x in a if x not in b][:8], "added": [x for x in b if x not in a][:8],
                    "ratio": round(difflib.SequenceMatcher(None, "\n".join(a), "\n".join(b)).ratio(), 4)}
    res["all_identical"] = all(v["identical"] for v in res.values())
    return res
def main():
    cands = json.load(open(D / "c3_edit_candidates.json"))
    done = set()
    if OUT.exists():
        for l in OUT.read_text().splitlines():
            try: done.add(json.loads(l)["job_id"])
            except Exception: pass
    shards, _ = g._load_state(REPO)
    stored = {j: r for ps in shards.values() for j, r in ps.items()}
    fetcher = LoggedFetcher()
    todo = [c for c in cands if c["job_id"] not in done]
    log("start; candidates", len(cands), "todo", len(todo))
    for c in todo:
        if (D / "STOP").exists() or (D / "COMMANDS.md").stat().st_mtime != cmd_mtime:
            log("abort (STOP or COMMANDS changed)"); return
        try:
            r = fetcher.fetch(c["latest_ts"], c["latest_url"])
        except wayback.Offline as e:
            log("offline; waiting 10 min", e); time.sleep(600); fetcher.reset(); continue
        except wayback.Throttled as e:
            log("THROTTLED: stopping for 60 min minimum", e)
            with open(D / "progress.md", "a") as f: f.write(f"[{datetime.now().strftime('%H:%M:%S IST')}] STATUS: PAUSED_THROTTLED (C3 edit tracking); no requests for 60 min. Rerun script to resume.\n")
            return
        rec = {"job_id": c["job_id"], "theme": c["theme"], "stored_ts": c["stored_ts"], "latest_ts": c["latest_ts"], "gap_days": c["gap_days"], "fetched_at": now()}
        if not r["ok"]:
            rec.update(status="fetch_failed", error=r.get("error"))
        else:
            parsed = g.parse_job_detail(r["body"].decode("utf-8", errors="replace"))
            if g._is_good(parsed):
                rec.update(status="compared", cmp=compare(stored[c["job_id"]], parsed), latest_sections=parsed["sections"], unknown_headings=parsed["unknown_headings"])
            elif not parsed["sections"] and parsed["title"].lower().startswith("jobs search"):
                rec.update(status="search_fallback_page")
            else:
                rec.update(status="parse_failed")
        with open(OUT, "a") as f:
            f.write(json.dumps(rec) + "\n"); f.flush(); os.fsync(f.fileno())
        log(rec["job_id"], rec["status"], rec.get("cmp", {}).get("all_identical"))
    log("EDIT TRACK DONE")
    with open(D / "progress.md", "a") as f: f.write(f"[{datetime.now().strftime('%H:%M:%S IST')}] C3 edit-tracking fetches finished (c3_edit_results.jsonl)\n")
main()
