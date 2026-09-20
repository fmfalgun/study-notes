"""Politeness-enforcing helper for the live Google careers crawl.

Every live page load goes through live_load(); the rules live here in code so
no calling script can skip them: one load at a time (lock file), random
180-360 s gap after the previous load, <=12 loads per rolling hour, pause
state after blocks, host/path allow-list, and refusal of any robots.txt URL.
"""
import fcntl
import os
import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

WORK = Path("./tracks/gate/career-mapping/google-live")
DATA_REPO = Path("../no-github-remote/scraper-data")
sys.path.insert(0, "../no-github-remote/web-scrap")

from plugins.job_search import wayback_google as wg  # noqa: E402
from plugins.job_search import wayback_google_jobs as wj  # noqa: E402
from scraper_core import router  # noqa: E402

STATE = WORK / "state.json"
PAGES = WORK / "pages.jsonl"
ROLES_JSON = WORK / "security-roles-live.json"
ROLES_MD = WORK / "security-roles-live.md"
PROGRESS = WORK / "progress.md"
LOCK = WORK / ".live.lock"

MIN_GAP, MAX_GAP = 180, 360   # R2: 3-6 min between loads
HOURLY_CAP = 12                # R2: at most ~12 live loads per hour
OFFLINE_WAIT = 600             # R3: machine offline -> wait 10 min, retry same page
BLOCK_PAUSE = 3600             # R3: real block -> stay off the site 60 min
OFFLINE_MARKERS = ("ERR_INTERNET_DISCONNECTED", "ERR_NAME_NOT_RESOLVED", "ERR_NETWORK_CHANGED", "ERR_ADDRESS_UNREACHABLE", "ERR_PROXY_CONNECTION_FAILED")
OFFLINE_LOG = WORK / "offline.jsonl"
BLOCK_MARKERS = ("unusual traffic", "captcha", "verify you are human", "are you a robot", "too many requests", "403 forbidden", "error 429", "error 403")
THROTTLE_MARKERS = ("ERR_CONNECTION_REFUSED", "ERR_CONNECTION_RESET", "ERR_TIMED_OUT", "timeout", "ERR_EMPTY_RESPONSE")
_JOB_HREF = re.compile(r"results/(\d{15,})-([A-Za-z0-9%\-]+)")


def now_utc():
    return datetime.now(timezone.utc)


def stamp():
    return f"{datetime.now().strftime('%H:%M:%S %Z')} | {now_utc().strftime('%H:%M:%S UTC')}"


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"loads": [], "paused_until": 0, "consecutive_bad": 0, "backoff_level": 0, "last_heartbeat": 0}


def save_state(s):
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(s))
    os.replace(tmp, STATE)


def allowed(url):
    if "robots" in url.lower():
        return False
    p = urlparse(url)
    return p.scheme == "https" and p.netloc == "www.google.com" and p.path.startswith("/about/careers/applications")


def heartbeat(phase, last, nxt, problems="none", force=False):
    s = load_state()
    if not force and time.time() - s.get("last_heartbeat", 0) < 1800:
        return
    roles = 0
    if ROLES_JSON.exists():
        roles = json.loads(ROLES_JSON.read_text()).get("total", 0)
    loads = sum(1 for l in PAGES.open() if '"offline": true' not in l)
    line = (f"[{stamp()}] PHASE {phase} | live loads so far {loads} "
            f"| security roles so far {roles} | last action: {last} | next action: {nxt} | problems: {problems}")
    with PROGRESS.open("a") as f:
        f.write(line + "\n")
    s = load_state()
    s["last_heartbeat"] = time.time()
    save_state(s)


def _job_ids_from_raw(raw_file):
    try:
        raw = json.loads(Path(raw_file).read_text())
        html = raw["pages"][0]["stages"][-1]["html"]
    except Exception:
        return []
    seen, out = set(), []
    for job_id, slug in _JOB_HREF.findall(html):
        if job_id not in seen:
            seen.add(job_id)
            out.append((job_id, slug))
    return out


def live_load(url, term, page, kind="results", follow_links=0, min_gap=MIN_GAP, scan_page_text=True):
    """One polite live page load. kind: 'landing' (no listings expected) or
    'results' (GOOD iff >=1 listing parses). Returns a result dict; never
    raises for site problems. Sleeps as needed BEFORE the request."""
    if not allowed(url):
        return {"refused": True, "reason": "url not allowed (host/path allow-list or robots)", "url": url}
    with LOCK.open("w") as lockf:
        fcntl.flock(lockf, fcntl.LOCK_EX)
        s = load_state()
        if time.time() < s["paused_until"]:
            return {"refused": True, "reason": f"paused until {datetime.fromtimestamp(s['paused_until'])}", "url": url}
        s["loads"] = [t for t in s["loads"] if time.time() - t < 3600]
        if len(s["loads"]) >= HOURLY_CAP:
            wait = 3600 - (time.time() - s["loads"][0]) + 5
            time.sleep(max(wait, 5))
            s["loads"] = [t for t in s["loads"] if time.time() - t < 3600]
        gap = random.uniform(max(min_gap, MIN_GAP), max(MAX_GAP, min_gap))
        if s["loads"]:
            elapsed = time.time() - s["loads"][-1]
            if elapsed < gap:
                time.sleep(gap - elapsed)
        started = time.time()
        s["loads"].append(started)
        save_state(s)

        try:
            result = router.run_generic_capture(url, DATA_REPO, follow_links=follow_links,
                                                capture_screenshot=False, probe_input=False)
            signal = json.loads(Path(result["signal_file"]).read_text())
            error = None
        except Exception as exc:  # capture-level failure
            result, signal, error = {}, {"main_text": {}, "errors": [str(exc)], "discovered_links": [], "title": None}, str(exc)

        main_text = signal.get("main_text", {})
        errors = signal.get("errors", [])
        full_err = " ".join(errors) + " " + (error or "")
        off = next((m for m in OFFLINE_MARKERS if m in full_err), None)
        if off:
            # R3: the MACHINE is offline; the request never reached Google. Not a block, not a bad load:
            # log it separately, do not count it as a load or toward any streak, tell the caller to wait+retry.
            s = load_state()
            if s["loads"]:
                s["loads"].pop()
            save_state(s)
            with OFFLINE_LOG.open("a") as f:
                f.write(json.dumps({"time_utc": now_utc().isoformat(), "url": url, "marker": off}) + "\n")
            return {"offline": True, "marker": off, "url": url}
        parsed = wg.analyze_snapshot(main_text)
        # Markers are checked in errors always, but in page text only when no
        # listings parsed (a real results page can legitimately contain numbers/words).
        # scan_page_text=False (job-detail pages): a security posting can legitimately mention "captcha" or
        # "unusual traffic", so only the load's own errors count as block markers there.
        blob = (" ".join(errors) + " " + ("" if parsed["listings"] or not scan_page_text else " ".join(main_text.values()))).lower()
        blocked = next((m for m in BLOCK_MARKERS if m in blob), None)
        throttled = next((m for m in THROTTLE_MARKERS if m.lower() in blob), None)
        good = bool(parsed["listings"]) if kind == "results" else bool(main_text) and not (blocked or throttled)
        ids = _job_ids_from_raw(result["raw_file"]) if result.get("raw_file") else []

        entry = {
            "time_utc": now_utc().isoformat(), "url": url, "term": term, "page": page, "kind": kind,
            "jobs_matched": parsed["jobs_matched"], "listing_count": len(parsed["listings"]),
            "job_hrefs": len(ids), "good": good, "blocked": blocked, "throttled": throttled,
            "elapsed_s": round(time.time() - started, 1), "error": (error or (errors[0][:160] if errors else None)),
        }
        with PAGES.open("a") as f:
            f.write(json.dumps(entry) + "\n")

        s = load_state()
        if good:
            s["consecutive_bad"], s["backoff_level"] = 0, 0
        else:
            s["consecutive_bad"] += 1
            if blocked or s["consecutive_bad"] >= 3:
                s["paused_until"] = time.time() + BLOCK_PAUSE
            elif throttled:
                s["paused_until"] = time.time() + [900, 1800, 3600][min(s["backoff_level"], 2)]
                s["backoff_level"] += 1
        save_state(s)
        return {"entry": entry, "parsed": parsed, "job_ids": ids, "signal": signal, "paused_until": s["paused_until"],
                "signal_file": result.get("signal_file"), "raw_file": result.get("raw_file")}


def add_roles(term, page, url, parsed, job_ids):
    """Merge a results page into security-roles-live.json (+ md). Returns number of NEW roles."""
    data = json.loads(ROLES_JSON.read_text()) if ROLES_JSON.exists() else {"roles": {}, "possible": {}}
    by_slug = {}
    for job_id, slug in job_ids:
        by_slug[wj.title_from_slug(slug.lower()).lower()] = (job_id, slug)
    new = 0
    ordered = list(job_ids)
    for i, listing in enumerate(parsed["listings"]):
        title = listing["title"]
        key = wj.title_from_slug(re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")).lower()
        aligned = len(ordered) == len(parsed["listings"])
        hit = None
        # Position first: the page's job links are 1:1 with its listings, in order. A title->slug
        # dict alone collapses identical titles (same role in two locations) onto one id.
        if aligned and wj.title_from_slug(ordered[i][1].lower()).lower() == key:
            hit = ordered[i]
        if hit is None:
            hit = by_slug.get(key)
        if hit is None and aligned:
            hit = ordered[i]
        job_id = hit[0] if hit else "title:" + title + "|" + listing["location"]
        url_job = (f"https://www.google.com/about/careers/applications/jobs/results/{hit[0]}-{hit[1]}" if hit else None)
        tags = wg.classify_title(title)
        if "cybersecurity" in tags:
            if job_id not in data["roles"]:
                data["roles"][job_id] = {"job_id": job_id, "title": title, "org": listing["org"], "location": listing["location"],
                                          "theme": wj.security_theme(title), "first_seen_utc": now_utc().isoformat(timespec="seconds"),
                                          "url": url_job, "terms": [term]}
                new += 1
            elif term not in data["roles"][job_id]["terms"]:
                data["roles"][job_id]["terms"].append(term)
        elif term in ("security", "cybersecurity") and page <= 2:
            data["possible"][job_id] = {"job_id": job_id, "title": title, "org": listing["org"], "location": listing["location"],
                                         "term": term, "page": page, "url": url_job}
    data["total"] = len(data["roles"])
    themes = {}
    for r in data["roles"].values():
        themes[r["theme"]] = themes.get(r["theme"], 0) + 1
    data["by_theme_counts"] = themes
    data["updated_utc"] = now_utc().isoformat(timespec="seconds")
    ROLES_JSON.write_text(json.dumps(data, indent=1))
    lines = [f"# Google security roles (live) - {data['total']} total", "", f"Updated {data['updated_utc']}. Counts by theme: {themes}", ""]
    for theme in sorted(themes):
        lines += [f"## {theme} ({themes[theme]})", "", "| job_id | title | org | location | first_seen_utc | url |", "|---|---|---|---|---|---|"]
        for r in sorted((r for r in data["roles"].values() if r["theme"] == theme), key=lambda r: r["title"]):
            lines.append(f"| {r['job_id']} | {r['title']} | {r['org']} | {r['location']} | {r['first_seen_utc']} | {r['url'] or ''} |")
        lines.append("")
    lines += [f"## POSSIBLE (not tagged by title, from first two pages of 'security'/'cybersecurity' searches) - {len(data['possible'])}", ""]
    for r in sorted(data["possible"].values(), key=lambda r: r["title"]):
        lines.append(f"- {r['title']} | {r['org']} | {r['location']} | term={r['term']} p{r['page']}")
    ROLES_MD.write_text("\n".join(lines) + "\n")
    return new
