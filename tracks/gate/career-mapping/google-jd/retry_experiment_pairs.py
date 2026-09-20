"""OFFLINE: build the 18 URL+timestamp pairs of the retry experiment (13 tested in C1 + 5 new old-era). No network."""
import sys, json, random, re, os
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from collections import defaultdict
from scraper_core import data_repo
from plugins.job_search import wayback_google_jobs as j
D = Path("./tracks/gate/career-mapping/google-jd")
REPO = Path("../no-github-remote/scraper-data")
sec = json.loads(Path("./tracks/gate/career-mapping/google-wayback-job-trends.json").read_text())["security_postings"]
byid = {p["job_id"]: p for p in sec}
cap = data_repo.load_capture(REPO, j.CAPTURE_DOMAIN, kind="cdx"); caps = defaultdict(list)
for r in cap["rows"]:
    p = j.parse_job_url(r["original"])
    if p: caps[p["job_id"]].append((r["timestamp"], r["original"]))
is_new = lambda t, u: "www.google.com/about/careers" in u and t >= "20230701"
pairs = []
res = json.loads((D / "c1_probe_results.json").read_text())
c1_seen = set()
for p in res:
    a = [x for x in p["attempts"] if x["path"] == "raw_id_"][0]
    if a["timestamp"] >= "20230601": continue
    orig = a["final_url"].split("id_/", 1)[1]
    pairs.append({"job_id": p["job_id"], "ts": a["timestamp"], "url": orig, "origin": "c1_first_capture",
                  "c1_wire_bytes": a["bytes"], "c1_decoded_len": a["html_chars"], "c1_text_chars": a["text_chars"]})
    c1_seen.add(p["job_id"])
# the 6 alternative (last-capture) fetches of c1_probe2.out: title + first_month + last date
probe2 = [("202107","20211214",9272,58,"Security Solutions Engineer Google Cloud"), ("202301","20230311",9839,62,"Cloud Security Engineer Professional Service"),
 ("202212","20230123",9765,35,"Security Engineer Intern 2023"), ("202105","20230603",9618,35,"Security Specialist Solutions Engineering Goo"),
 ("202201","20220120",9257,55,"Trust Lead Security And Privacy Maps"), ("202207","20230321",9648,35,"Security Sales Specialist")]
for fm, last, dec, txt, title in probe2:
    m = [p for p in sec if p["first_month"] == fm and p["title"].startswith(title[:40]) and not any(is_new(t, u) for t, u in caps[p["job_id"]])]
    assert m, (fm, title)
    best = None
    for p in m:
        cs = sorted(caps[p["job_id"]])
        if cs and cs[-1][0].startswith(last): best = (p, cs[-1])
    assert best, (fm, title, last)
    p, (t, u) = best
    pairs.append({"job_id": p["job_id"], "ts": t, "url": u, "origin": "c1_alt_last_capture", "c1_wire_bytes": None, "c1_decoded_len": dec, "c1_text_chars": txt})
    c1_seen.add(p["job_id"])
# 5 new old-era captures across years, old-only postings never tried
random.seed(19)
old_only = [p for p in sec if caps[p["job_id"]] and not any(is_new(t, u) for t, u in caps[p["job_id"]]) and p["job_id"] not in c1_seen]
for yr in ["2019", "2020", "2021", "2022", "2022"]:
    pool = [p for p in old_only if p["first_month"][:4] == yr and p["job_id"] not in {x["job_id"] for x in pairs}]
    p = random.choice(pool)
    t, u = sorted(caps[p["job_id"]])[0]
    pairs.append({"job_id": p["job_id"], "ts": t, "url": u, "origin": "new_untried", "c1_wire_bytes": None, "c1_decoded_len": None, "c1_text_chars": None})
tmp = str(D / "retry_experiment_pairs.json.tmp")
Path(tmp).write_text(json.dumps(pairs, indent=1)); os.replace(tmp, D / "retry_experiment_pairs.json")
print(len(pairs), [ (x["origin"][:6], x["ts"][:8]) for x in pairs])
