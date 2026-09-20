"""C3 extra (c), OFFLINE (reads already-captured front-page snapshots in scraper-data; no requests): security-title 'Qualifications:' snippets. Anecdotal appendix only."""
import sys, json, re, os, html as H, glob, statistics
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from collections import defaultdict
from plugins.job_search.wayback_google import classify_title
from plugins.job_search.wayback_google_jobs import security_theme
D = Path("./tracks/gate/career-mapping/google-jd")
S = "../no-github-remote/scraper-data/"
def atomic(p, t): tmp = str(p) + ".tmp"; Path(tmp).write_text(t); os.replace(tmp, p)
def txt(s): return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
files = sorted(glob.glob(S + "https___web.archive.org_web_*careers.google.com_jobs_results_.raw.json"))
skipped = []; snap = 0; cards_total = 0; sec = {}; per_snap = []
for f in files:
    ts = re.search(r"_web_(\d{14})_", f).group(1)
    d = json.load(open(f))
    if not d.get("pages") or not d["pages"][0].get("stages"): skipped.append(ts); continue
    h = d["pages"][0]["stages"][-1]["html"]
    snap += 1
    parts = re.split(r'(?=<h2 itemprop="title")', h)[1:]
    n = 0
    for p in parts:
        title = txt(re.match(r'<h2[^>]*>(.*?)</h2>', p, re.S).group(1))
        m = re.search(r'itemprop="qualifications"[^>]*>(.*?)</div>', p, re.S)
        cards_total += 1
        if not m: continue
        href = re.search(r'/jobs/results/(\d+)-', p)
        if "cybersecurity" in classify_title(title):
            n += 1
            e = sec.setdefault(title, {"title": title, "theme": security_theme(title), "snaps": [], "job_ids": set(), "quals": {}})
            e["snaps"].append(ts); e["job_ids"].add(href.group(1) if href else "")
            items = [txt(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.S)]
            e["quals"][ts] = items
    per_snap.append((ts, len(parts), n))
res = sorted(sec.values(), key=lambda e: min(e["snaps"]))
L = ["# APPENDIX (anecdotal only): 'Qualifications:' snippets on archived Google careers front pages\n",
     "**Read this first.** This is NOT a sample of security roles and supports NO trend claim. Each archived front-page snapshot of the jobs-results page lists ~20 job cards in whatever order Google's search returned that day; some cards carry a 'Qualifications:' preview (minimum qualifications only, as bullets). I kept the cards whose TITLE the project's security classifier flags as cybersecurity. Postings/titles here are whichever happened to sit on a front page; 2019-2022 postings are title-based only elsewhere in this study, and these snippets do not change that. Source: already-captured snapshots in scraper-data (offline, no new requests).\n",
     f"Snapshots read: {snap} (of {len(files)} matching files; {len(skipped)} had no stored page) old-format front pages (careers.google.com, captures {files[0].split('_web_')[1][:8]} to {files[-1].split('_web_')[1][:8]}); job cards seen in total: {cards_total}; cards with a security title AND a Qualifications preview: {sum(len(e['snaps']) for e in res)} card-appearances = **{len(res)} unique titles** (denominator for anything below: {len(res)}; n<30 = weak).\n",
     "Each title is listed once with its first and last snapshot date and the snippet from its FIRST appearance (verbatim bullets; the number of snapshots where the snippet text differed is noted).\n"]
lens = []
for i, e in enumerate(res, 1):
    first = min(e["snaps"]); last = max(e["snaps"])
    q = e["quals"][first]; distinct = len({tuple(v) for v in e["quals"].values()})
    lens.append(sum(len(x) for x in q))
    L.append(f"### {i}. {e['title']}  [{e['theme']}]")
    L.append(f"- snapshots: {len(e['snaps'])} (first {first[:8]}, last {last[:8]}); distinct snippet texts: {distinct}")
    for x in q: L.append(f"  - {x}")
    L.append("")
L.append(f"Snippet length (chars, first appearance): median {statistics.median(lens):.0f}, range {min(lens)}-{max(lens)}. Observation only: every snippet is a few minimum-qualification bullets; none has responsibilities, preferred qualifications or an about section, so they cannot be compared with the 2023-2026 full descriptions.")
by_year = defaultdict(int)
for e in res: by_year[min(e["snaps"])[:4]] += 1
L.append(f"\nUnique titles by year of first appearance (anecdotal counts, not prevalence): {dict(sorted(by_year.items()))}")
atomic(D / "c3_frontpage_snippets_appendix.md", "\n".join(L) + "\n")
print("\n".join(L[:12])); print(len(res), dict(by_year), sorted(per_snap)[:3], sum(1 for x in per_snap if x[2]))
