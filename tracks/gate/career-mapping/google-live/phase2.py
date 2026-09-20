"""Phase 2 driver: walk search terms slowly, collect security-tagged roles.

Detached (nohup). Resumable via phase2_state.json. Stops on STOP file.
Politeness is enforced inside crawl_lib.live_load (180-360 s jitter, 12/hour cap,
pause state); this driver adds 6-10 min between terms and the stop rules.
Never requests robots.txt (crawl_lib refuses it) and never leaves the
www.google.com/about/careers/applications/ allow-list.
"""
import json
import os
import random
import sys
import time
import traceback
from math import ceil
from urllib.parse import quote_plus

sys.path.insert(0, "./tracks/gate/career-mapping/google-live")
import crawl_lib as c  # noqa: E402

TERMS = ["security", "cybersecurity", "threat", "incident response", "vulnerability",
         "malware", "red team", "penetration testing", "detection", "cryptography"]
BASE = "https://www.google.com/about/careers/applications/jobs/results"
MAX_PAGES = 25
STOP = c.WORK / "STOP"
P2 = c.WORK / "phase2_state.json"
CTX = {"last": "starting", "next": "first search page", "problems": "none"}


def load_p2():
    if P2.exists():
        return json.loads(P2.read_text())
    return {"done_terms": [], "term_stats": {}, "cur_term": None, "next_page": 1, "phase2_done": False, "probe_after_pause": False}


def save_p2(s):
    tmp = P2.with_suffix(".tmp")
    tmp.write_text(json.dumps(s, indent=1))
    os.replace(tmp, P2)


def wait(seconds):
    """Sleep in small chunks, heartbeating and honoring STOP. False if STOP seen."""
    end = time.time() + seconds
    while time.time() < end:
        if STOP.exists():
            return False
        c.heartbeat("2", CTX["last"], CTX["next"], CTX["problems"])
        time.sleep(min(20, max(1, end - time.time())))
    return not STOP.exists()


def main():
    s = load_p2()
    s["probe_after_pause"] = False  # stale flag from the offline episode (not a block)
    st0 = c.load_state()
    st0["consecutive_bad"], st0["paused_until"], st0["backoff_level"] = 0, 0, 0
    c.save_state(st0)
    consecutive_exceptions = 0
    for term in TERMS:
        if term in s["done_terms"]:
            continue
        stats = s["term_stats"].setdefault(term, {"pages": 0, "jobs_matched": None, "new_roles": 0, "tagged_titles_seen": 0, "stop_reason": None})
        page = s["next_page"] if s["cur_term"] == term else 1
        s["cur_term"] = term
        while page <= MAX_PAGES:
            if STOP.exists():
                c.heartbeat("2", "STOP file seen, driver exiting", "none", "none", force=True)
                return
            if stats["jobs_matched"] is not None and (page - 1) * 20 >= stats["jobs_matched"]:
                stats["stop_reason"] = f"reached last page ({ceil(stats['jobs_matched'] / 20)} pages)"
                break
            url = BASE + "?q=" + quote_plus(term) + (f"&page={page}" if page > 1 else "")
            CTX.update(last=f"loading '{term}' page {page}", next="parse, save roles, continue", problems=CTX["problems"])
            try:
                r = c.live_load(url, term, page, "results")
                consecutive_exceptions = 0
            except Exception:
                consecutive_exceptions += 1
                CTX["problems"] = f"exception #{consecutive_exceptions} in driver: {traceback.format_exc().splitlines()[-1][:120]}"
                c.heartbeat("2", CTX["last"], "retry after 2 min", CTX["problems"], force=True)
                if consecutive_exceptions >= 5:
                    c.heartbeat("2", "driver giving up after 5 exceptions", "waiting for commands", CTX["problems"], force=True)
                    return
                if not wait(120):
                    return
                continue

            if r.get("offline"):
                CTX["problems"] = f"machine offline ({r['marker']}) at '{term}' p{page}: not a block; retrying in 10 min"
                s["next_page"] = page
                save_p2(s)
                c.heartbeat("2", f"offline at '{term}' p{page}", "retry same page in 10 min", CTX["problems"])
                if not wait(c.OFFLINE_WAIT):
                    return
                continue

            st = c.load_state()
            if r.get("refused") or not r["entry"]["good"]:
                reason = r.get("reason") or (r["entry"]["blocked"] or r["entry"]["throttled"] or r["entry"]["error"] or "no listings parsed")
                paused = st["paused_until"] - time.time()
                CTX["problems"] = f"non-good load ('{term}' p{page}): {reason}"
                if s["probe_after_pause"] and not r.get("refused"):
                    c.heartbeat("2", "STATUS: PAUSED_BLOCKED (the single post-pause probe also failed)", "none - waiting for commands", CTX["problems"], force=True)
                    with c.PROGRESS.open("a") as f:
                        f.write(f"[{c.stamp()}] STATUS: PAUSED_BLOCKED {reason}\n")
                    save_p2(s)
                    return
                if paused > 0:
                    s["probe_after_pause"] = st["consecutive_bad"] >= 3 or bool(r.get("entry", {}).get("blocked"))
                    s["next_page"] = page
                    save_p2(s)
                    c.heartbeat("2", f"backing off {int(paused / 60)} min", "retry same page after the pause", CTX["problems"], force=True)
                    if not wait(paused + 5):
                        return
                else:
                    if not wait(120):
                        return
                continue

            s["probe_after_pause"] = False
            CTX["problems"] = "none"
            e = r["entry"]
            stats["pages"] += 1
            if page == 1:
                stats["jobs_matched"] = e["jobs_matched"]
            tagged = sum("cybersecurity" in c.wg.classify_title(x["title"]) for x in r["parsed"]["listings"])
            stats["tagged_titles_seen"] += tagged
            new = c.add_roles(term, page, url, r["parsed"], r["job_ids"])
            stats["new_roles"] += new
            CTX.update(last=f"'{term}' p{page}: {e['listing_count']} listings, {tagged} security-tagged, {new} new (jobs_matched={e['jobs_matched']})",
                       next=f"'{term}' page {page + 1}")
            c.heartbeat("2", CTX["last"], CTX["next"], CTX["problems"])
            page += 1
            s["next_page"] = page
            save_p2(s)
            if page > 2 and tagged == 0:
                stats["stop_reason"] = f"zero security-tagged titles on page {page - 1}"
                break
            if page - 1 == 1 and tagged == 0 and (e["jobs_matched"] or 0) == 0:
                stats["stop_reason"] = "no results for this term"
                break
        else:
            stats["stop_reason"] = f"hit {MAX_PAGES}-page cap"

        s["done_terms"].append(term)
        s["cur_term"], s["next_page"] = None, 1
        save_p2(s)
        c.heartbeat("2", f"term '{term}' finished: {stats['stop_reason']}; {stats['pages']} pages, {stats['new_roles']} new roles",
                    "pause 6-10 min then next term", CTX["problems"], force=True)
        if term != TERMS[-1] and not wait(random.uniform(360, 600)):
            return

    s["phase2_done"] = True
    save_p2(s)
    c.heartbeat("2", "ALL TERMS DONE", "phase 3: analyse + craft plugin", "none", force=True)


if __name__ == "__main__":
    main()
