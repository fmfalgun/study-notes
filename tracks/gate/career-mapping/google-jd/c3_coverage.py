"""C3 end-of-run offline analysis (NO network): (a) coverage table, (b) edit-tracking candidate count. Writes c3_coverage.md + c3_edit_candidates.json atomically."""
import sys, json, os
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from plugins.job_search import wayback_google_details as g
D = Path("./tracks/gate/career-mapping/google-jd")
REPO = Path("../no-github-remote/scraper-data")
def atomic(p, t): tmp = str(p) + ".tmp"; Path(tmp).write_text(t); os.replace(tmp, p)
targets = g.security_targets(REPO)
shards, ledger = g._load_state(REPO)
stored = {jid: (y, r) for y, ps in shards.items() for jid, r in ps.items()}
assert len(targets) == 883, len(targets)
themes = sorted({t["theme"] for t in targets})
def outcome(t):
    if t["job_id"] in stored: return "described:" + stored[t["job_id"]][0]
    e = ledger.get(t["job_id"]); return "none:" + (e["reason"] if e else "UNACCOUNTED")
rows = [(t, outcome(t)) for t in targets]
assert not any(o.endswith("UNACCOUNTED") for _, o in rows)
# --- table 1: description-capture year x theme
cols = ["described:2023", "described:2024", "described:2025", "described:2026"]
noncols = ["none:old_spa_shell", "none:search_fallback_page", "none:http_404", "none:parse_failed"]
def cnt(theme=None, first=None):
    c = Counter(o for t, o in rows if (theme is None or t["theme"] == theme) and (first is None or t["first_month"][:4] == first))
    return c
L = []
L.append("# C3 coverage of security-posting descriptions (Wayback)\n")
L.append("**Scope note (applies to every table):** postings are only those Wayback archived (883 security postings, first-seen 2019-2026). 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026). Description-capture year = the year of the archived capture the text was parsed from (not the year the posting was first seen). Themes: physical_corporate_security is NOT cybersecurity and must be analysed separately. n<30 flagged weak (W).\n")
L.append("## Table 1. Description-capture year x theme (denominator = 883 postings)\n")
hdr = "| theme | postings | " + " | ".join(c.split(":")[1] for c in cols) + " | described total | no description | described % |"
L.append(hdr); L.append("|" + "---|" * (hdr.count("|") - 1))
def flag(n): return f"{n} W" if 0 < n < 30 else str(n)
allrows = [(th, cnt(theme=th)) for th in themes] + [("ALL", cnt())]
for th, c in allrows:
    tot = sum(c.values()); dsc = sum(c[k] for k in cols)
    L.append(f"| {th} | {tot} | " + " | ".join(flag(c[k]) for k in cols) + f" | {dsc} | {tot - dsc} | {100*dsc/tot:.1f}% |")
L.append("\nW = n<30 (weak: treat any share from that cell as anecdotal). The 4 year columns count each posting once, under the year of the capture whose text was stored.\n")
L.append("## Table 2. Why a posting has NO description, by theme (denominator per row = postings in that theme)\n")
hdr = "| theme | no description | old_spa_shell | search_fallback_page | http_404 | parse_failed |"
L.append(hdr); L.append("|" + "---|" * 6)
for th, c in allrows:
    L.append(f"| {th} | {sum(c[k] for k in noncols)} | " + " | ".join(str(c[k]) for k in noncols) + " |")
L.append("\nReasons: old_spa_shell = the posting was archived only in Google's OLD site format (<=2023-05), whose pages are empty single-page-app shells (0/18 retried pairs held any description, see retry_experiment_result.md); the 321 were never requested again. search_fallback_page = the archived URL returned Google's 'Jobs search' results page (the posting was gone at capture time; it lists OTHER jobs). http_404 = the archive returned 404 for the tried captures. parse_failed = a page came back but no description section parsed (6 postings).\n")
L.append("## Table 3. First-seen year x outcome (denominator = postings first seen that year)\n")
hdr = "| first-seen year | postings | described | described % | old_spa_shell | search_fallback | 404 | parse_failed |"
L.append(hdr); L.append("|" + "---|" * 8)
years = sorted({t["first_month"][:4] for t in targets})
for y in years:
    c = cnt(first=y); tot = sum(c.values()); dsc = sum(c[k] for k in cols)
    L.append(f"| {y} | {flag(tot)} | {dsc} | {100*dsc/tot:.0f}% | {c['none:old_spa_shell']} | {c['none:search_fallback_page']} | {c['none:http_404']} | {c['none:parse_failed']} |")
c = cnt(); tot = sum(c.values()); dsc = sum(c[k] for k in cols)
L.append(f"| ALL | {tot} | {dsc} | {100*dsc/tot:.0f}% | {c['none:old_spa_shell']} | {c['none:search_fallback_page']} | {c['none:http_404']} | {c['none:parse_failed']} |")
L.append("\nRead: a 2019-2022 posting is described only if it was captured again after mid-2023, and then the text is the 2023+ text (not the wording at the time it was first seen).\n")
L.append("## Table 4. Description-capture year x first-seen year (described postings only; shows how much 2023+ text belongs to older postings)\n")
hdr = "| first-seen year | " + " | ".join(c_.split(":")[1] for c_ in cols) + " | total |"
L.append(hdr); L.append("|" + "---|" * (len(cols) + 2))
for y in years:
    c = cnt(first=y); dsc = sum(c[k] for k in cols)
    L.append(f"| {y} | " + " | ".join(str(c[k]) for k in cols) + f" | {dsc} |")
L.append("")
# --- edit tracking candidates
cands, oneshot = [], 0
for jid, (y, r) in stored.items():
    t = next(t for t in targets if t["job_id"] == jid)
    new = sorted(c for c in t["captures"] if g.is_new_era(*c))
    base = r["capture_timestamp"]
    later = [c for c in new if c[0] > base]
    if not later: continue
    span_all = (datetime.strptime(new[-1][0][:8], "%Y%m%d") - datetime.strptime(new[0][0][:8], "%Y%m%d")).days
    gap = (datetime.strptime(later[-1][0][:8], "%Y%m%d") - datetime.strptime(base[:8], "%Y%m%d")).days
    cands.append({"job_id": jid, "theme": t["theme"], "stored_ts": base, "latest_ts": later[-1][0], "latest_url": later[-1][1], "gap_days": gap, "span_days_all_new_captures": span_all, "n_new_captures": len(new)})
all_span6 = [t for t in targets if (lambda new: len(new) > 1 and (datetime.strptime(new[-1][0][:8], "%Y%m%d") - datetime.strptime(new[0][0][:8], "%Y%m%d")).days >= 182)(sorted(c for c in t["captures"] if g.is_new_era(*c)))]
ge6 = [c for c in cands if c["gap_days"] >= 182]
L.append("## Edit-tracking candidate count (offline)\n")
L.append(f"- Postings with new-format captures spanning >=182 days (earliest to latest new-format capture), ANY outcome: {len(all_span6)} of 883.")
L.append(f"- Of the {len(stored)} described postings, ones with a later new-format capture than the stored text: {len(cands)}; with the latest capture >=182 days after the stored capture (a request is needed for each): **{len(ge6)}**.")
L.append(f"- By theme (>=182d): {dict(Counter(c['theme'] for c in ge6))}")
L.append(f"- By stored-text year (>=182d): {dict(Counter(c['stored_ts'][:4] for c in ge6))}")
atomic(D / "c3_coverage.md", "\n".join(L) + "\n")
atomic(D / "c3_edit_candidates.json", json.dumps(ge6, indent=1))
print("\n".join(L))
