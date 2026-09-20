"""Phase 2b (parent COMMANDS.md [1]): test whether the stop rule loses recall.

Waits for phase2.py to finish all terms. Then loads 5 deep pages of the
"security" search (20, 35, 50, 65, last) at the normal slow pace and records how
many security-tagged titles each has. If ALL are zero the stop rule is sound.
If ANY has a tagged title the rule is unsafe: re-walk every term that stopped on
a zero page, continuing from that page until 3 consecutive zero pages (the
observed zero page counts as the first), still capped at 25 pages per term.
Roles found are merged into security-roles-live.json as usual.
Same politeness as everything else (crawl_lib.live_load); never robots.txt.
"""
import json
import random
import re
import subprocess
import sys
import time
from math import ceil
from urllib.parse import quote_plus

sys.path.insert(0, "./tracks/gate/career-mapping/google-live")
import crawl_lib as c  # noqa: E402
import phase2 as p2  # noqa: E402

DEEP = c.WORK / "deepcheck.json"
DONE = c.WORK / "phase2b_done.json"
DRIVER_RE = "^../no-github-remote/web-scrap/.venv/bin/python3 phase2.py"


def driver_running():
    return subprocess.run(["pgrep", "-f", DRIVER_RE], capture_output=True).returncode == 0


def load_page(term, page, tries=4):
    """One polite load of a search page; retries only after the pause the lib set."""
    url = p2.BASE + "?q=" + quote_plus(term) + (f"&page={page}" if page > 1 else "")
    for _ in range(tries):
        if p2.STOP.exists():
            return None, url
        p2.CTX.update(last=f"2b: loading '{term}' page {page}", next="parse + merge", problems=p2.CTX["problems"])
        r = c.live_load(url, term, page, "results")
        if r.get("offline"):  # R3: machine offline is not a bad load; wait 10 min, retry, never counted
            p2.CTX["problems"] = f"2b machine offline ({r['marker']}) at '{term}' p{page}: retry in 10 min"
            c.heartbeat("2b", f"offline at '{term}' p{page}", "retry in 10 min", p2.CTX["problems"])
            if not p2.wait(c.OFFLINE_WAIT):
                return None, url
            return load_page(term, page, tries)
        if not r.get("refused") and r["entry"]["good"]:
            p2.CTX["problems"] = "none"
            return r, url
        st = c.load_state()
        reason = r.get("reason") or r["entry"]["blocked"] or r["entry"]["throttled"] or r["entry"]["error"] or "no listings parsed"
        p2.CTX["problems"] = f"2b non-good ('{term}' p{page}): {reason}"
        paused = st["paused_until"] - time.time()
        e = r.get("entry")
        if e and not e["blocked"] and not e["throttled"] and not e["error"]:
            return "EMPTY", url  # loaded fine but no listings: beyond the last page; do not retry
        if e and st["consecutive_bad"] >= 3:
            c.heartbeat("2b", "STATUS: PAUSED_BLOCKED during deep check", "waiting for commands", p2.CTX["problems"], force=True)
            with c.PROGRESS.open("a") as f:
                f.write(f"[{c.stamp()}] STATUS: PAUSED_BLOCKED {reason}\n")
            return "BLOCKED", url
        if not p2.wait(max(paused + 5, 120)):
            return None, url
    return "FAILED", url


def tagged_titles(parsed):
    return [x["title"] for x in parsed["listings"] if "cybersecurity" in c.wg.classify_title(x["title"])]


def main():
    if DONE.exists():
        return
    c.heartbeat("2b", "phase 2b armed: waiting for phase 2 to finish all terms", "then deep-check pages 20/35/50/65/last of 'security'", "none", force=True)
    while True:
        if p2.STOP.exists():
            return
        s = p2.load_p2()
        if s.get("phase2_done") and not driver_running():
            break
        if not driver_running() and not s.get("phase2_done"):
            c.heartbeat("2b", "phase 2 driver is not running and not done", "waiting for commands", "driver stopped early", force=True)
            return
        time.sleep(20)
        c.heartbeat("2b", "waiting for phase 2 terms to finish", "deep check", "none")

    s = p2.load_p2()
    total_pages = ceil(s["term_stats"]["security"]["jobs_matched"] / 20)
    pages = sorted({20, 35, 50, 65, total_pages})
    deep = json.loads(DEEP.read_text()) if DEEP.exists() else {"checked_at_utc": c.now_utc().isoformat(timespec="seconds"), "total_pages_security": total_pages, "pages": {}}
    total_before = deep.get("roles_before_deep") or json.loads(c.ROLES_JSON.read_text())["total"]
    deep["roles_before_deep"] = total_before
    c.heartbeat("2b", f"phase 2 done ({total_before} roles); starting deep check of security pages {pages}", "load deep pages at normal pace", "none", force=True)
    if not p2.wait(random.uniform(360, 600)):
        return

    for page in pages:
        if "tagged" in deep["pages"].get(str(page), {}):
            continue  # already done before a restart
        r, url = load_page("security", page)
        if r in (None, "BLOCKED", "FAILED", "EMPTY"):
            deep["pages"][str(page)] = {"status": r or "STOP"}
            DEEP.write_text(json.dumps(deep, indent=1))
            if r in (None, "BLOCKED"):
                return
            continue
        titles = tagged_titles(r["parsed"])
        new = c.add_roles("security", page, url, r["parsed"], r["job_ids"]) if titles else 0
        deep["pages"][str(page)] = {"listings": len(r["parsed"]["listings"]), "tagged": len(titles), "tagged_titles": titles, "new_roles": new}
        DEEP.write_text(json.dumps(deep, indent=1))
        c.heartbeat("2b", f"deep 'security' page {page}/{total_pages}: {len(titles)} security-tagged of {len(r['parsed']['listings'])}", "next deep page", p2.CTX["problems"], force=True)

    checked = {k: v for k, v in deep["pages"].items() if "tagged" in v}
    unsafe = any(v["tagged"] > 0 for v in checked.values())
    deep["stop_rule_safe"] = not unsafe
    deep.setdefault("rewalk", {})

    if unsafe:
        for term in s["done_terms"]:
            stats = s["term_stats"][term]
            m = re.match(r"zero security-tagged titles on page (\d+)", stats.get("stop_reason") or "")
            if not m:
                continue
            if term in deep.get("rewalk", {}):
                continue
            page, zeros, added, walked = int(m.group(1)) + 1, 1, 0, 0
            if not p2.wait(random.uniform(360, 600)):
                return
            while page <= p2.MAX_PAGES and zeros < 3:
                r, url = load_page(term, page)
                if r in (None, "BLOCKED", "FAILED", "EMPTY"):
                    break
                titles = tagged_titles(r["parsed"])
                zeros = zeros + 1 if not titles else 0
                added += c.add_roles(term, page, url, r["parsed"], r["job_ids"])
                walked += 1
                c.heartbeat("2b", f"re-walk '{term}' p{page}: {len(titles)} tagged, +{added} new so far", "continue until 3 consecutive zero pages", p2.CTX["problems"])
                page += 1
            deep["rewalk"][term] = {"pages_walked": walked, "roles_added": added, "ended_at_page": page - 1}
            stats["rewalk_added"] = added
            stats["stop_reason"] += f" -> re-walked {walked} pages after: +{added} roles (3-consecutive-zero rule)"
            p2.save_p2(s)
            DEEP.write_text(json.dumps(deep, indent=1))

    total_after = json.loads(c.ROLES_JSON.read_text())["total"]
    deep["roles_before"], deep["roles_after"], deep["roles_added"] = total_before, total_after, total_after - total_before
    DEEP.write_text(json.dumps(deep, indent=1))
    DONE.write_text(json.dumps({"stop_rule_safe": deep["stop_rule_safe"], "roles_added": deep["roles_added"]}))
    c.heartbeat("2b", f"deep check done: stop rule {'SOUND (all deep pages zero)' if deep['stop_rule_safe'] else 'UNSAFE'}; roles {total_before} -> {total_after} (+{total_after - total_before})",
                "phase 3 (analysis + plugin)", "none", force=True)


if __name__ == "__main__":
    main()
