import sys, json, random
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from collections import defaultdict, Counter
from scraper_core import data_repo
from plugins.job_search import wayback_google_jobs as j
REPO = Path("../no-github-remote/scraper-data"); D = Path("./tracks/gate/career-mapping/google-jd")
sec = json.loads(Path("./tracks/gate/career-mapping/google-wayback-job-trends.json").read_text())["security_postings"]
cap = data_repo.load_capture(REPO, j.CAPTURE_DOMAIN, kind="cdx"); caps = defaultdict(list)
for r in cap["rows"]:
    p = j.parse_job_url(r["original"])
    if p: caps[p["job_id"]].append((r["timestamp"], r["original"]))
is_new = lambda t, u: "www.google.com/about/careers" in u and t >= "20230701"
reach = []
for p in sec:
    nc = sorted((t, u) for t, u in caps[p["job_id"]] if is_new(t, u))
    if nc: reach.append({**p, "earliest_new": nc[0], "n_new": len(nc)})
mon = Counter(r["earliest_new"][0][:6] for r in reach if "20230701" <= r["earliest_new"][0] < "20240101")
print("earliest-new-capture by month, 2023-07..2023-12:", dict(sorted(mon.items())))
random.seed(11); pick = []
def take(pool, n, tag):
    pool = [r for r in pool if r["job_id"] not in {x["job_id"] for x in pick}]
    for r in random.sample(pool, min(n, len(pool))): pick.append({**r, "why": tag})
for m in ["202307","202308","202309","202310","202311","202312"]:
    take([r for r in reach if r["earliest_new"][0][:6] == m], 2, f"migration {m}")
take([r for r in reach if r["earliest_new"][0][:4] == "2024" and r["theme"] == "security_engineering"], 2, "2024 engineering")
take([r for r in reach if r["earliest_new"][0][:4] == "2024" and r["theme"] == "threat_intel_and_response"], 1, "2024 threat")
take([r for r in reach if r["earliest_new"][0][:4] == "2025" and r["theme"] == "sales_and_consulting"], 2, "2025 sales/consulting")
take([r for r in reach if r["earliest_new"][0][:4] == "2025" and r["theme"] == "other_security"], 1, "2025 other")
take([r for r in reach if r["earliest_new"][0][:4] == "2025" and r["theme"] == "threat_intel_and_response"], 1, "2025 threat")
take([r for r in reach if r["earliest_new"][0][:4] == "2026" and r["theme"] == "security_engineering"], 2, "2026 engineering")
take([r for r in reach if r["earliest_new"][0][:4] == "2026" and r["theme"] == "sales_and_consulting"], 1, "2026 sales/consulting")
take([r for r in reach if r["earliest_new"][0][:4] == "2026" and r["theme"] == "other_security"], 1, "2026 other")
take([r for r in reach if r["theme"] == "physical_corporate_security" and r["earliest_new"][0][:4] >= "2024"], 2, "physical")
take([r for r in reach if r["earliest_new"][0][:4] in ("2023",)], 3, "extra 2023")
print("pilot size:", len(pick), "| by theme:", dict(Counter(p["theme"] for p in pick)))
(D / "c2_pilot_set.json").write_text(json.dumps(pick, indent=1))
for p in pick[:4]: print(p["why"], p["earliest_new"][0], p["title"][:50])
