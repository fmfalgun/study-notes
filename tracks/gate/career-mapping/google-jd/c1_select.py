import sys, json, random
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from collections import defaultdict
from scraper_core import data_repo
from plugins.job_search import wayback_google_jobs as j

REPO = Path("../no-github-remote/scraper-data")
D = Path("./tracks/gate/career-mapping/google-jd")
sec = json.loads(Path("./tracks/gate/career-mapping/google-wayback-job-trends.json").read_text())["security_postings"]
cap = data_repo.load_capture(REPO, j.CAPTURE_DOMAIN, kind="cdx")
caps = defaultdict(list)                      # job_id -> [(timestamp, original)]
for r in cap["rows"]:
    p = j.parse_job_url(r["original"])
    if p: caps[p["job_id"]].append((r["timestamp"], r["original"]))
for v in caps.values(): v.sort()

# capture-count stats for the security set
n = [len(caps[p["job_id"]]) for p in sec]
print("security postings:", len(sec), "| captures per posting min/median/max:", min(n), sorted(n)[len(n)//2], max(n))
print("postings with exactly 1 capture:", sum(1 for x in n if x == 1))
by_year = defaultdict(int)
for p in sec: by_year[p["first_month"][:4]] += 1
print("by first-month year:", dict(sorted(by_year.items())))

random.seed(7)
plan = [("2019",None),("2020",None),("2021",None),("2022",None),("2022",None),("2023",None),("2023",None),
        ("2024",None),("2024",None),("2025",None),("2025",None),("2026",None)]
themes = ["security_engineering","threat_intel_and_response","sales_and_consulting","other_security"]
picked, used = [], set()
for i, (yr, _) in enumerate(plan):
    pool = [p for p in sec if p["first_month"][:4] == yr and p["job_id"] not in used and p["theme"] != "physical_corporate_security"]
    pref = [p for p in pool if p["theme"] == themes[i % 4]] or pool
    if not pref: continue
    p = random.choice(pref); used.add(p["job_id"])
    picked.append({**p, "captures": caps[p["job_id"]]})
(D / "c1_probe_set.json").write_text(json.dumps(picked, indent=1))
for p in picked:
    print(p["first_month"], p["theme"][:14].ljust(14), len(p["captures"]), "caps |", p["title"][:60], "|", p["captures"][0][1][:70])
