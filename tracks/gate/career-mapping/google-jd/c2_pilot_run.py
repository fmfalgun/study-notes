import sys, json, time
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from scraper_core import wayback
from plugins.job_search import wayback_google_details as g
D = Path("./tracks/gate/career-mapping/google-jd"); REPO = Path("../no-github-remote/scraper-data")
pilot = json.loads((D / "c2_pilot_set.json").read_text()); ids = [p["job_id"] for p in pilot]
LOG = D / "c2_pilot.log"; t0 = time.time()
def log(m): line = f"[{time.time()-t0:5.0f}s] {m}"; print(line, flush=True); LOG.open("a").write(line + "\n")

class CachedThenLive:
    """serve the 4 pages already downloaded for parser development from disk; everything else goes to the polite live fetcher"""
    def __init__(self, live): self.live, self.hits, self.live_calls = live, 0, 0
    def fetch(self, timestamp, url, *, raw=True):
        for f in (D / "c2_raw").glob(f"*_{timestamp}.html"):
            self.hits += 1
            body = f.read_bytes()
            return {"ok": True, "status": 200, "body": body, "bytes": len(body), "decoded_bytes": len(body), "secs": 0.0, "cached": True}
        self.live_calls += 1
        return self.live.fetch(timestamp, url, raw=raw)
    def reset(self): self.live.reset()

fetcher = CachedThenLive(wayback.ArchiveFetcher())
log(f"pilot start: {len(ids)} postings")
result = g.fetch_details(REPO, job_ids=ids, fetcher=fetcher, shard_size=10, on_progress=lambda done, total, t: log(f"  {done}/{total} {t['first_month']} {t['title'][:45]}"))
log(f"RESULT {json.dumps(result)} | cache hits {fetcher.hits} | live requests {fetcher.live_calls}")
log("PILOT COMPLETE")
