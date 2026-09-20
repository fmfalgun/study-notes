import json, re, sys
sys.path.insert(0, "./tracks/gate/career-mapping/google-live")
import crawl_lib as c
r = c.live_load("https://www.google.com/about/careers/applications/jobs/results", "pilot", 1, kind="results", follow_links=0, min_gap=125)
if r.get("refused"): print(json.dumps(r)); sys.exit()
print(json.dumps(r["entry"]))
p = r["parsed"]
print("format:", p["format"], "jobs_matched:", p["jobs_matched"], "listings:", len(p["listings"]))
for l in p["listings"][:5]: print("  ", l)
print("job ids/slugs:", len(r["job_ids"]), r["job_ids"][:3])
raw = json.load(open(r["raw_file"]))
html = raw["pages"][0]["stages"][-1]["html"]
print("html chars:", len(html))
print("page= hrefs:", sorted(set(re.findall(r'href="([^"]*[?&]page=\d+[^"]*)"', html)))[:8])
print("q= hrefs:", sorted(set(re.findall(r'href="([^"]*[?&]q=[^"]*)"', html)))[:5])
print("pagination-ish snippets:", [m[:140] for m in re.findall(r'(?i)(?:aria-label="[^"]*(?:page|next)[^"]*"|>Next<|>Previous<)', html)][:6])
print("input names:", sorted(set(re.findall(r'<input[^>]*?(?:name|aria-label|placeholder)="([^"]+)"', html)))[:10])
print("discovered:", [(d["href"][:110], d["text"][:30]) for d in r["signal"].get("discovered_links", [])[:10]])
