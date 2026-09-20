"""Detached, resumable, BATCHED fetch of the live job DESCRIPTIONS of the 170 security roles (google.com/about/careers only).

Run one batch (default 20 roles), then exit; the parent reviews the batch before the next one is started:
  cd ../no-github-remote/web-scrap && nohup .venv/bin/python3 <this file> --count 20 >> <dir>/details/download.log 2>&1 &
Safe to kill any time or lose power: every role is written atomically to details/roles/<job_id>.json the moment it is
parsed; a restart skips finished ids. Pace is enforced in crawl_lib.live_load (lock, 180-360 s gap, <=12 loads/hour,
offline handling, block pause, allow-list, refuses any robots URL). No robots.txt request is ever made.
Raw page captures are saved by the generic capture into scraper-data (own git repo). Exits at once if STOP exists.
Counters: details/progress.json (atomic). Failures: details/failed.json (not retried automatically).
"""
import argparse, json, os, sys, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import crawl_lib as cl  # noqa: E402  (also puts web-scrap on sys.path)
from plugins.job_search import wayback_google_details as wd  # noqa: E402

D = HERE / "details"
ROLES = D / "roles"
FAILED = D / "failed.json"
PROGRESS = D / "progress.json"
cl.PAGES = D / "pages.jsonl"          # keep the detail loads out of the search-crawl log (analysis.md counts 83 loads)
cl.OFFLINE_LOG = D / "offline.jsonl"
MAX_OFFLINE_WAITS = 6                 # 6 x 10 min, then exit and let the parent look


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def log(*a):
    print(now(), *a, flush=True)


def atomic(path, obj):
    tmp = str(path) + ".tmp"
    Path(tmp).write_text(json.dumps(obj, indent=1, ensure_ascii=False))
    os.replace(tmp, path)


def order():
    """Deterministic order: round-robin across themes so every batch is a mixed sample."""
    roles = json.loads((HERE / "security-roles-live.json").read_text())["roles"]
    by_theme = {}
    for r in roles.values():
        if r.get("url"):
            by_theme.setdefault(r["theme"], []).append(r)
    lists = [sorted(v, key=lambda r: r["job_id"]) for _, v in sorted(by_theme.items())]
    out = []
    while any(lists):
        for l in lists:
            if l:
                out.append(l.pop(0))
    return out, len(roles) - len(out)


def state():
    done = {p.stem for p in ROLES.glob("*.json")}
    failed = json.loads(FAILED.read_text()) if FAILED.exists() else {}
    return done, failed


def progress(status, note="", batch_done=0, batch_size=0):
    seq, no_id = order()
    done, failed = state()
    atomic(PROGRESS, {"updated": now(), "status": status, "note": note, "roles_total": len(seq) + no_id,
                      "roles_with_url": len(seq), "no_id_skipped": no_id, "done": len(done), "failed": len(failed),
                      "pending": sum(1 for r in seq if r["job_id"] not in done and r["job_id"] not in failed),
                      "this_run": {"done": batch_done, "of": batch_size}})


def fail(job_id, reason, extra=None):
    done, failed = state()
    failed[job_id] = {"reason": reason, "at": now(), **(extra or {})}
    atomic(FAILED, failed)


def raw_html(raw_file):
    try:
        return json.loads(Path(raw_file).read_text())["pages"][0]["stages"][-1]["html"]
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    ROLES.mkdir(parents=True, exist_ok=True)
    seq, _ = order()
    done, failed = state()
    todo = [r for r in seq if r["job_id"] not in done and r["job_id"] not in failed][:args.count]
    if args.dry_run:
        for r in todo:
            print(r["job_id"], r["theme"], r["title"])
        return
    if (HERE / "STOP").exists():
        log("STOP file present - not starting"); progress("STOPPED"); return
    log("batch start:", len(todo), "roles")
    progress("RUNNING", batch_size=len(todo))
    ok_count = 0
    for i, role in enumerate(todo):
        if (HERE / "STOP").exists():
            log("STOP file"); progress("STOPPED", batch_done=ok_count, batch_size=len(todo)); return
        waits = 0
        while True:
            res = cl.live_load(role["url"], "detail", 0, kind="detail", follow_links=0, scan_page_text=False)
            if res.get("offline"):
                waits += 1
                log("offline", res["marker"], "wait", waits)
                progress("WAITING_OFFLINE", note=f"machine offline, retry {waits}/{MAX_OFFLINE_WAITS}", batch_done=ok_count, batch_size=len(todo))
                if waits >= MAX_OFFLINE_WAITS:
                    progress("OFFLINE_EXIT", batch_done=ok_count, batch_size=len(todo)); return
                time.sleep(cl.OFFLINE_WAIT)
                continue
            break
        if res.get("refused"):
            log("refused:", res["reason"]); progress("PAUSED_OR_REFUSED", note=res["reason"], batch_done=ok_count, batch_size=len(todo)); return
        entry = res["entry"]
        html = raw_html(res.get("raw_file"))
        parsed = wd.parse_job_detail(html) if html else {"sections": {}, "description_text": ""}
        text = " ".join((res["signal"].get("main_text") or {}).values())
        if wd._is_good(parsed):
            atomic(ROLES / f"{role['job_id']}.json", {
                "job_id": role["job_id"], "title": role["title"], "title_on_page": parsed.get("title"), "org": role["org"],
                "location": role["location"], "theme": role["theme"], "url": role["url"], "fetched_utc": entry["time_utc"],
                "parser_version": wd.PARSER_VERSION, "sections": parsed["sections"], "description_text": parsed["description_text"],
                "unknown_headings": parsed.get("unknown_headings"), "region_fallback": parsed.get("region_fallback"),
                "page_text": text[:60000], "raw_file": res.get("raw_file"), "signal_file": res.get("signal_file"),
                "load": {"elapsed_s": entry["elapsed_s"], "blocked": entry["blocked"], "throttled": entry["throttled"]}})
            ok_count += 1
            log(f"[{i+1}/{len(todo)}] stored {role['job_id']} sections={list(parsed['sections'])} chars={len(parsed['description_text'])}")
        else:
            reason = "blocked_or_throttled" if (entry["blocked"] or entry["throttled"]) else "no_description_parsed"
            fail(role["job_id"], reason, {"page_text_chars": len(text), "error": entry["error"], "raw_file": res.get("raw_file")})
            log(f"[{i+1}/{len(todo)}] FAILED {role['job_id']} {reason} text_chars={len(text)}")
            if len(text) < 2000 and any(m in text.lower() for m in cl.BLOCK_MARKERS):
                s = cl.load_state(); s["paused_until"] = time.time() + cl.BLOCK_PAUSE; cl.save_state(s)
                progress("BLOCK_SUSPECTED", note="short page with block wording; paused 60 min", batch_done=ok_count, batch_size=len(todo)); return
            if i == 0 and ok_count == 0:
                progress("PILOT_FAILED", note="first role did not parse: stop and let the parent inspect the raw page", batch_done=0, batch_size=len(todo)); return
            if res.get("paused_until", 0) > time.time():
                progress("PAUSED", note="crawl_lib paused after bad loads", batch_done=ok_count, batch_size=len(todo)); return
        progress("RUNNING", batch_done=ok_count, batch_size=len(todo))
    progress("BATCH_DONE", batch_done=ok_count, batch_size=len(todo))
    log("batch done:", ok_count, "stored of", len(todo))


if __name__ == "__main__":
    main()
