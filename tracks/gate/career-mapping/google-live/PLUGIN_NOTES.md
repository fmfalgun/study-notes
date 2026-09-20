# PLUGIN_NOTES: google_live (REGISTERED 21 Sep 2026 after the user's review: state saved after every page, 3-term default accepted; full suite 544 passed)

Files (web-scrap, uncommitted): `plugins/job_search/google_live.py`, `tests/test_google_live.py` (24 tests, no network,
run only that file: `.venv/bin/python3 -m pytest tests/test_google_live.py -q`).

## Registration (the parent does this after the user's review; the worker never edits `__init__.py`)

In `plugins/job_search/__init__.py`, next to the other imports (after the `.wayback_google_jobs` import line):

    from .google_live import google_live_security_roles

and inside `REGISTRY = {...}`:

    "google_live_security_roles": {
        "kind": "scrape",
        "run": google_live_security_roles,
        "timeout": 3600,
    },

Also add a short docstring paragraph in `__init__.py` next to the other Google ops: network to www.google.com/about/careers
only, intentionally slow (3-6 min between loads), resumable, never requests robots.txt.

## How to use

Signature: `google_live_security_roles(domain, data_repo_path=DEFAULT_DATA_REPO, terms=None, max_loads=7, fresh=False, clear_halt=False)`.
One call = at most `max_loads` live loads (default 7, clamped to 12) so it fits the router's one-hour cap; call it again to continue.
A full walk is about 83 loads (about 32 with `terms=SHORT_TERMS`), i.e. many calls over many hours. State and roles are saved in
the data repo as `google-live-security-roles.live.json` after every good page, so a crash or usage-limit loses nothing.

Statuses: COMPLETE, BUDGET_REACHED (call again), OFFLINE_WAITING (network down, not a block; call later), PAUSED / PAUSED_THROTTLED
(inside a saved pause; no request is made), PAUSED_BLOCKED (real block sign or 3 bad loads: 60 min off, then one probe), HALTED
(failed probe: needs a human, then `clear_halt=True`), REFUSED_URL.

## What it encodes (from the 2026-09-19 crawl, see analysis.md)

Terms: security, cybersecurity, threat, incident response, vulnerability, malware, red team, penetration testing, detection,
cryptography (`SHORT_TERMS` = first three: they found all 178 rows; the other seven added 0). Stop rule: first page with zero
security-tagged titles after page 2, or the last page, or 25 pages. GOOD page = `analyze_snapshot` finds at least one listing.
Dedupe on job id, matched by listing position (title-only matching collapsed the same role in two locations). Offline errors
(`ERR_INTERNET_DISCONNECTED`, DNS, proxy) are never counted and never treated as a block.

## Things to decide at review

1. Every good page commits the state file to scraper-data (about 83 small commits for a full walk, on top of the router's own
   page-capture commits). Say if you would rather save state only at term boundaries.
2. The default is the full 10-term walk (the verified procedure); consider making SHORT_TERMS the default given that the seven later
   terms added nothing.
3. The tag is a title keyword regex: the four Mandiant consulting titles in the "possible" list are not tagged. Adding `mandiant`
   and `appsec` to `wayback_google._CYBER_RE` is outside this worker's remit (R5) and would change the Wayback analyses too.
4. The plugin has NOT been run against the live site (per the brief); its live behaviour is what the tests and the earlier crawl
   scripts (`crawl_lib.py`, `phase2.py`) say it is, no more.
