# Plugin notes — wayback_google_ai (NOT registered, NOT committed; parent to do both)

Files (new, in web-scrap):
- `plugins/job_search/wayback_google_ai.py` — approved rules (`RULES_VERSION`, `FAMILY_ORDER`), `classify_ai_title`, `analyze_ai_index`, and the analyze op `google_wayback_ai_trends`.
- `tests/test_google_wayback_ai.py` — 41 tests, no network. Run only this file: `.venv/bin/python3 -m pytest tests/test_google_wayback_ai.py -q`.

## Registration (edit `plugins/job_search/__init__.py`; I did not touch it)
Add next to the other wayback imports:

```python
from .wayback_google_ai import google_wayback_ai_trends
```

Add to `REGISTRY`:

```python
    "google_wayback_ai_trends": {
        "kind": "analyze",
        "run": google_wayback_ai_trends,
    },
```

Optionally add one sentence to that file's docstring: "`google_wayback_ai_trends` (wayback_google_ai.py) reads the same cdx capture and reports the AI-role tables; see that module's docstring for the rule definitions."

## Running it
Needs the cdx capture first (`google_wayback_collect_job_urls`, already done: `scraper-data/google-careers-job-urls.cdx.json`, range 201801-202609). Then, from the web-scrap dir:

```python
from pathlib import Path
from plugins.job_search import wayback_google_ai as a
res = a.google_wayback_ai_trends("google.com", Path("../no-github-remote/scraper-data"))
```

Returns headline/sensitivity/reconciliation/families/AI-as-domain (rule counts only)/naming-vs-size/vocabulary/crossover tables plus `flagged_postings`. No network, ~2 s.

## What the op does NOT produce (manual, documented in the analysis file)
- The hand-corrected AI-as-domain estimate (from a single-judge hand check, `google-ai/c3_samples.json`).
- Precision/recall sample estimates (`google-ai/c2_samples.json`).
- The data-driven early-vs-late token comparison (computed by the generator script `c4_generate.py`).

## Changing a rule
Bump `RULES_VERSION`, update the tests, and re-run `google-ai/c4_verify.py`-style comparisons; published numbers move when rules move.
