import json, sys
sys.path.insert(0, "./tracks/gate/career-mapping/google-live")
import crawl_lib as c
r = c.live_load("https://www.google.com/about/careers/applications/", "pilot", 0, kind="landing", follow_links=0)
if r.get("refused"): print(json.dumps(r)); sys.exit()
sig = r["signal"]
print(json.dumps(r["entry"]))
print("title:", sig.get("title"))
print("main_text chars:", {k: len(v) for k, v in sig["main_text"].items()})
print("job hrefs:", r["job_ids"][:3])
print("discovered_links:", json.dumps(sig.get("discovered_links", [])[:20], indent=0)[:1500])
print("signal_file:", r["signal_file"])
