"""C5: direction cross-check on front-page snapshots (read-only, local). Strict rule from the plugin applied to listing titles."""
import sys, json, math
sys.path.insert(0, ".")
from pathlib import Path
from collections import defaultdict
from plugins.job_search import wayback_google as W
from plugins.job_search import wayback_google_ai as A
from plugins.job_search.wayback_google import classify_title
h = W.build_history(Path("../no-github-remote/scraper-data"))
by = defaultdict(lambda: dict(snaps=0, listings=0, core=0, old=0, sec=0, both=0, ds=0, dm=0, adj=0)); per = []
for s in h["snapshots"]:
    y = s["timestamp"][:4]; b = by[y]; b["snaps"] += 1; k = 0
    for l in s["listings"]:
        t = l["title"]; f = A.classify_ai_title(t); tags = classify_title(t)
        b["listings"] += 1; b["core"] += f["core"]; k += f["core"]; b["ds"] += f["data_science_only"]; b["dm"] += f["deepmind_only"]; b["adj"] += f["adjacent"]
        b["old"] += "ai" in tags; b["sec"] += "cybersecurity" in tags; b["both"] += f["core"] and "cybersecurity" in tags
    per.append((s["timestamp"], len(s["listings"]), k))
def wil(k, n, z=1.96):
    if not n: return (0, 0)
    p = k/n; d = 1+z*z/n; c = p+z*z/(2*n); r = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return ((c-r)/d*100, (c+r)/d*100)
out = {}
for y in sorted(by):
    b = by[y]; lo, hi = wil(b["core"], b["listings"]); out[y] = dict(b, share=100*b["core"]/b["listings"], lo=lo, hi=hi)
    print(y, b, f"core {100*b['core']/b['listings']:.1f}% [{lo:.1f}-{hi:.1f}]")
print("unparseable", len(h["unparseable"]), "snapshots", len(h["snapshots"]), "listings/snap min-max", min(p[1] for p in per), max(p[1] for p in per))
core_titles = sorted({l["title"] for s in h["snapshots"] for l in s["listings"] if A.classify_ai_title(l["title"])["core"]})
print(len(core_titles), core_titles[:25])
json.dump({"by_year": out, "per_snapshot": per, "unparseable": len(h["unparseable"])}, open("./tracks/gate/career-mapping/google-ai/c5_frontpage.json", "w"), indent=1)
