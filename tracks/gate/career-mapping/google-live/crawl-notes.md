# Live crawl notes (Google careers) - what was verified, when

Times are UTC. Tooling: `router.run_generic_capture(url, scraper-data, follow_links=0, capture_screenshot=False, probe_input=False)`
wrapped by `crawl_lib.live_load()` which enforces politeness in code (one load at a time via lock file, random 60-120 s
gap, <=30 loads/rolling hour, pause state after blocks/throttling, host+path allow-list, refuses any robots.txt URL).

## Pilot (2026-09-19)
| load | URL | result |
|---|---|---|
| 1 (12:24) | https://www.google.com/about/careers/applications/ | good; 20 s; title "Search for your career at Google."; only 219 chars of text (JS-rendered hub); one discovered link, `/about/careers/applications/dashboard` (personal "Your career" page - not followed) |
| 2 (12:26, >=2 min gap enforced) | https://www.google.com/about/careers/applications/jobs/results | good; 22.5 s; format `current`; **3,338 jobs matched**; **20 listings/page**; no block/throttle signs |

## Verified facts
- Page size is 20 listings; total pages = ceil(jobs_matched / 20) (3,338 -> 167 pages for the whole board).
- Pagination: the page contains a real link `.../jobs/results?page=2` ("Go to next page" control) -> param is `page`.
- Job links are RELATIVE hrefs `jobs/results/<15+ digit id>-<slug>` (no leading slash); 20 per page, in listing order;
  the same ids also appear in `jsdata="Aiqs8c;<id>;$3"` attributes. Regex `results/(\d{15,})-([A-Za-z0-9%\-]+)` on the
  raw capture's HTML gives exactly the 20 ids; 20/20 titles matched their slug. (A first regex with a leading `/jobs/`
  found 0 - the relative form has no leading slash.)
- The plugin-parsed listing text uses `wayback_google.analyze_snapshot` (`current` format) - works unchanged on live pages.
- The search box has an obfuscated input name (`YPqjbf`); no `q=` link is present in the static HTML, so the search param
  `q` is a HYPOTHESIS until the first search load below confirms it changes "N jobs matched".
- Both stages (initial, after_interaction) of a capture are identical when `probe_input=False`.

## To verify next
- `?q=<term>` changes jobs_matched and results; `?q=<term>&page=2` works together.

## Search verified (2026-09-19 12:29 UTC)
- `.../jobs/results?q=security` -> **1,409 jobs matched** (vs 3,338 unfiltered), 20 listings, 20 job links, 26 s, no block signs.
  So `q` is the search param; pages are `&page=N` (page 1 has no page param). Search is broad: it matches roles that
  mention the term anywhere, not only in the title (all 20 page-1 titles happened to be security-tagged).
- Bug found + fixed: matching listings to job ids via a title->slug dict collapsed identical titles (same role in two
  locations = same slug, different ids) onto one id (19 roles from 20 listings). Now matched by POSITION (page links are
  1:1, in order, with listings), slug dict only as fallback. Page 1 re-merged from its saved capture: 20/20 distinct.
- Interrupting a capture with SIGINT tears the throwaway browser down cleanly (verified: no orphan headless processes).
