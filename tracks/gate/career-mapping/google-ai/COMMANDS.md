# COMMANDS for the AI-analysis worker (written by the parent; newest entry last)

Format: `## [n] <local time>` then instructions. The worker acts ONLY on entries here.
Entry [0] below authorises Checkpoint 1 work (the classifier audit) and nothing after it.

## [0] initial
Do Checkpoint 1 (classifier audit) as described in your brief, then write CHECKPOINT_1 to progress.md and wait for entry [1].

## [1] 18:08
Checkpoint 1 reviewed. Your "current published rule" year shares match our reference exactly, so the data load is right. Direction: **do Checkpoint 2**, then stop and write CHECKPOINT 2.

Decisions on your questions (these are definitions of "AI role"; everything excluded from the headline must still be REPORTED as a count, never dropped):
- Q2 YES: TPU / tensor processing / Vertex / Gemma / NotebookLM / agentic count as CORE. GPU alone does not.
- Q3 AI-adjacent (Assistant, ranking/recommendation/personalization, perception/robotics, translate/speech/MT, generic "Research Scientist, Google Research"): EXCLUDE from the headline, report as a separate count per year.
- Q4 YES: a data-scientist title that also carries a core AI word counts as CORE.
- Q5 YES: exclude "Quantum AI" (an org name) unless the title has separate ML words.
- Q1 DeepMind: EXCLUDE from the headline and report on its own line, BUT you called the "listing-source change" explanation "likely". Do not assert it. Check what the data can show: first/last month and URL variants of those 29 postings, and whether any DeepMind-labelled postings exist before 2026. If the data cannot settle it, say "all 29 appear only in 2026; cause not verifiable from this data (a change in what Wayback archived is one possibility)".

Specific fixes for C2:
1. **Sensitivity table.** Report per-year CORE share under three definitions so the user can see how much the choices matter: (a) strict CORE as decided above, (b) strict CORE + DeepMind, (c) strict CORE + AI-adjacent. Show the 2026 value with and without DeepMind explicitly.
2. **Precision/recall sample size.** 40 titles gives roughly +/-8 points on a 93% estimate. Draw a larger stratified sample (aim ~100 matched titles spread across years, ~100 unmatched) and report precision and recall with the sample sizes and the method used for the "recall ~79%" figure. State them as ranges, not single numbers.
3. **Same denominators as the published cybersecurity analysis:** a posting counts toward every year it was actually captured (analyze_job_index's rule), observed postings per year shown next to every share, so the AI and security tables are comparable.
4. Fix the "performance" family flaw you noted. Keep "Aiml" fixed via a case-insensitive whole-word rule.
5. Family shares are shares of that year's CORE AI postings; show n per year and flag any year with n < 30 as noisy.

Do not start Checkpoint 3.

## [2] 18:17
Checkpoint 2 reviewed. I recomputed your shares from your own counts (e.g. 275/2469 = 11.1%, 671/6824 = 9.8%, 239/1925 = 12.4%) and they match, and the C1->C2 numbers agree. Direction: **do Checkpoint 3**, then stop and write CHECKPOINT 3. Two things must be fixed/explained before the numbers go into a deliverable:

1. **Reconcile the DeepMind counts.** C1 said 29, C2 says 34 DeepMind-titled postings, and "27 are DeepMind-only". State exactly which definition each number uses (all titles containing DeepMind / those not already CORE by other words / those first captured in a given window) and make every later mention use one stated definition.
2. **2025 equals the old published rule (9.8%) only by offsetting changes** (rows added: Aiml, TPU, Vertex, agentic; rows removed: analytics, Quantum AI). Say so explicitly wherever 2025 is discussed, so nobody reads it as "the classifier did not change". Show the added and removed counts for 2025 (and for each year) as a small reconciliation table: old rule count -> minus removed -> plus added -> new count.

Decisions on your questions:
- Q6 YES: split "management_other" into a "business functions" family. Make families MUTUALLY EXCLUSIVE with a documented first-match order so each year's family shares sum to 100%; print that order.
- Q7: leave google-wayback-job-trends.json exactly as it is (it is the committed record of the earlier, broader rule). Your C4 analysis must state plainly that the earlier AI figures used a broader rule and are superseded FOR AI ONLY; cybersecurity numbers are unaffected. I will amend the AI sentence in the published cybersecurity analysis myself; do not touch it.

Specific requirements for C3:
- **The 2025 "AI as a team label" lead:** apply ONE rule-based classifier (AI-as-domain vs AI-as-work) to ALL CORE titles in ALL years, so 2025 is compared with the others on the same basis (not a rule for 2025 versus hand reading for the rest). Report the domain-only share per year with n and an interval, then hand-check a stratified sample (~60 titles across years, including all borderline ones). Only call it a finding if it survives that; otherwise keep it labelled "lead, not finding".
- **Vocabulary first appearance:** report each term's per-year share of CORE postings, not just its first year, and state that "first appearance in the archive" is not "first appearance at Google" (archive coverage varies). Use a data-driven token difference (early vs late years) as well as your named list; drop location/spoken-language tokens.
- **AI x cybersecurity crossover:** use classify_title's existing cybersecurity tag against strict CORE; counts and shares by year, and flag small n.
- **Data-science-only** (separate layer): report its own trend (you found it rises to 4.2% in 2026) with the caveat that it is analytics, not AI.
- State in every precision figure that it is a single, self-judged, unblinded sample (you are both the classifier's author and its judge). Give the raw and the year-weighted precision and explain the gap you found.
- Denominators next to every share; flag any year with n < 30 as noisy; label every explanation of cause as inference.

Do not start Checkpoint 4.

## [3] 18:36
Checkpoint 3 reviewed. I re-added your reconciliations (2025: 666-157+162 = 671; 2026: 289-111+61 = 239; 2024: 298-59+36 = 275), the DeepMind splits (34 = 27+7 = 29+5) and the domain shares (66/671 = 9.8%, 15/275 = 5.5%): all correct. Good catches: the missing case-insensitive flag, the 'Tele-communications' regex bug, and noticing that your crossover numbers agree with the cybersecurity analysis (5.6% / 4.2% of security postings). Direction: **do Checkpoint 4** (deliverables), then stop and write CHECKPOINT 4. Do not start Checkpoint 5.

Decisions on your questions:
- Q8: do NOT call the "AI as team label" result a finding. Label it **"supported lead"**: one judge who also wrote the rule, unblinded; the direction survives your hand-check and the uniform-rule comparison, the magnitude is uncertain (rule 9.8% vs hand-corrected ~8.4% for 2025). Say plainly what would upgrade it (an independent reader). Add an appendix listing your 40 borderline titles (with your verdict for each) so the user can check them themselves.
- Q9 YES: report the crossover both raw (23) and cleaned (22 genuine) with a footnote naming the excluded false positive.
- Q10 YES: roles-by-year list, CORE postings by year and family, with data-science-only and DeepMind-only in their own sections (use your definitions A=34, B=27 only). AI-adjacent: counts per year only, not titles.

C4 deliverables (NEW files only; do not touch existing ones):
1. ./tracks/gate/career-mapping/google-wayback-ai-analysis.md, mirroring google-wayback-analysis.md: a plain-language summary at the top; caveats up front; headline strict-CORE share table with denominators and n; sensitivity (b),(c); DS-only; AI-as-domain (as a supported lead); families with the printed first-match order; vocabulary and data-driven tokens; crossover; the reconciliation table; precision/recall with every figure labelled single-sample, self-judged, unblinded. **Lead the analysis with your renaming/mix finding**: the 2024 jump is largely ML-family titles retitled with "AI"/"GenAI" plus new AI-labelled roles, since ML-family titles stay ~4-5.5% of ALL postings while AI/GenAI-only titles grow 1.2% -> 7.8%. State explicitly that the earlier AI figures in google-wayback-job-trends.json and in the cybersecurity analysis used a broader rule and are **superseded for AI only** (cybersecurity numbers unaffected).
2. google-wayback-ai-roles-by-year.md (complete list, as in Q10).
3. google-wayback-ai-trends.json (per-year counts, denominators, definitions, rules version, and the per-posting flags: job_id, title, first/last month, family, flags).
4. **The reusable plugin, as our tooling:** create NEW web-scrap/plugins/job_search/wayback_google_ai.py holding your approved rules (a RULES_VERSION constant, the family order) and an analyze-kind op `google_wayback_ai_trends(domain, data_repo_path=DEFAULT_DATA_REPO)` that reproduces the headline, sensitivity, family, DS-only, domain, and crossover tables from the saved cdx capture; plus NEW tests/test_google_wayback_ai.py (no network: classification examples incl. Aiml, Quantum AI excluded, DeepMind handling, TPU/Vertex, analytics 'Data Scientist' vs 'Data Scientist, Generative AI'; family exclusivity; reconciliation identity on a synthetic capture). Run ONLY that test file. Do not edit plugins/job_search/__init__.py and do not commit: write the exact import + REGISTRY lines in google-ai/PLUGIN_NOTES.md.
5. The op's output on the real capture must reproduce your published tables EXACTLY; state in CHECKPOINT 4 that you checked this and how.
Every share keeps its denominator next to it; flag n < 30 as noisy; every cause is labelled inference.

## [4] 22:57  -- RESUME after a machine crash (a new agent continues you from these files)
The computer crashed and rebooted at 22:41, so the previous worker died mid-Checkpoint 4. You are its continuation. Your state is in this folder: progress.md (last heartbeat 18:39:59), c3_tables.md, c3_narrative.md, c3_rules.py, c3_samples.json, and web-scrap/plugins/job_search/wayback_google_ai.py (+ tests/test_google_wayback_ai.py, 41 tests) which the parent has ALREADY COMMITTED (e482437). Do not rewrite them unless a test or the reproduction check shows a bug.

Remaining for Checkpoint 4 (entry [3] still applies in full): generate google-wayback-ai-trends.json, google-wayback-ai-roles-by-year.md and google-wayback-ai-analysis.md FROM THE PLUGIN OP'S OUTPUT on the real capture; write google-ai/PLUGIN_NOTES.md; fix your own C3 vocabulary row 'LLM / language model' (case-sensitive bug; the plugin value is right) and note the correction in the analysis; then CHECKPOINT 4 and wait.

NEW pace rules (the user asked for the slowest pace possible; the previous workers exhausted the usage limit):
- Do the work in a FEW scripts and file writes, not many small steps; every turn is expensive.
- Heartbeat in progress.md every 30 MINUTES (not 5-10). While waiting for direction use one long wait per turn: `until [ -e STOP ] || [ COMMANDS.md changed ] || [ elapsed > 570s ]; do sleep 5; done` (Bash timeout 600000) and write a heartbeat only every third wait.
- Read only what you need; do not re-read large files.
Acknowledge this entry by number in your first heartbeat.

## [5] 23:07  -- resilience (parent asked for protection against agent failure / usage-limit loss)
Read google-ai/BRIEF.md (new): it holds your standing rules so a replacement agent can be launched from files alone. Create and keep google-ai/STATE.md truthful (atomic writes: temp file + os.replace) after every milestone, and persist every result to disk in the same turn it is produced. No change to your task or pace. Acknowledge by number in your next heartbeat.

## [6] 23:47
Checkpoint 4 reviewed and APPROVED. I verified it myself: the plugin op run fresh on the real cdx capture equals all 15 tables in your JSON exactly (observed denominators, k, shares, reconciliation, DeepMind splits); 41 tests pass; 5 sampled role-list entries exist in the JSON with family flags; the analysis leads with the renaming finding and carries the supersession, supported-lead, caveats and Appendix A. Your Q11 arithmetic checks (17/322 = 5.3%, 5/118 = 4.2%).
Done by the parent: the op is REGISTERED (web-scrap af52820), the three deliverables are COMMITTED (study-notes 8a8f430), and I corrected item 7 in google-wayback-analysis.md myself (do not touch that file). Q11: keep quoting cleaned with the raw count in brackets, as you do. Q12: keep all 1,976 flagged postings in the JSON. Q13: done.
Direction: **do Checkpoint 5** (cross-check and finalise), then stop and write CHECKPOINT 5:
1. Cross-check DIRECTION (not level) against the 79 parseable front-page snapshots (plugins.job_search.wayback_google.build_history on scraper-data, read-only): apply your strict rule to the titles of the ~20 listings per snapshot and report the per-year strict-CORE share of listings with n, clearly labelled a small, relevance-sorted sample; say whether the shape (low to 2023, jump 2024, no rise 2025, higher 2026) agrees.
2. Cross-check against the cybersecurity findings (crossover 2025/2026, the same denominators).
3. Fix the heading: the analysis says "2018–2026" but the archive has no AI posting before 2019; say 2019–2026 (edit your own file only).
4. Add a short "what this data cannot say" section (skills need job descriptions; archive-density vs hiring cannot be separated) and the sensible next step (the job-description worker is already recovering descriptions for postings archived from mid-2023).
5. Append these to the existing analysis file (do not rewrite finished sections), keep every figure with its denominator, then write CHECKPOINT 5, `DONE` in progress.md and go to STANDBY (one long wait per turn, heartbeat every 30 minutes).

## [7] 00:22
Checkpoint 5 reviewed and APPROVED. I recomputed your eight front-page shares (1/60, 4/160, 2/240, 7/240, 16/231, 29/240, 23/220, 28/179 = 1.7, 2.5, 0.8, 2.9, 6.9, 12.1, 10.5, 15.6%): all correct, and the sample is properly labelled small and relevance-sorted. The three replaced lines in the diff are only the heading year and two '%%' typos, as you said. Committed by the parent (study-notes). The AI analysis is COMPLETE. Stay in STANDBY (one long wait per turn, heartbeat every 30 minutes) and do nothing else unless a new numbered entry arrives or google-ai/STOP appears.
