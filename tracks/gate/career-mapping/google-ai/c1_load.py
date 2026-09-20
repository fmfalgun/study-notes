import sys, re, json, random
sys.path.insert(0, "../no-github-remote/web-scrap")
from pathlib import Path
from collections import Counter, defaultdict
from plugins.job_search import wayback_google_jobs as j
from plugins.job_search.wayback_google import classify_title
from scraper_core import data_repo

REPO = Path("../no-github-remote/scraper-data")
cap = data_repo.load_capture(REPO, "google-careers-job-urls", kind="cdx")
INDEX = j.build_job_index(cap["rows"])
