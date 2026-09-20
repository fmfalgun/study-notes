"""Generates the three C4 deliverables from the plugin's output (tables) + saved hand-check judgements. New files only."""
import sys, json, math, re, datetime
sys.path.insert(0, "../no-github-remote/web-scrap"); sys.path.insert(0, ".")
from pathlib import Path
from collections import Counter, defaultdict
from plugins.job_search import wayback_google_ai as A
from plugins.job_search import wayback_google_jobs as J
from scraper_core import data_repo

OUT = Path("./tracks/gate/career-mapping")
REPO = Path("../no-github-remote/scraper-data")
res = A.google_wayback_ai_trends("google.com", REPO)
Y = res["years"]; obs = res["observed_postings"]; nC = res["families"]["n_core"]
S2, S3 = json.load(open("c2_samples.json")), json.load(open("c3_samples.json"))
capture = data_repo.load_capture(REPO, J.CAPTURE_DOMAIN, kind="cdx"); INDEX = J.build_job_index(capture["rows"])
P = {p["job_id"]: p for p in res["flagged_postings"]}
f1 = lambda v: "-" if v is None else f"{v:.1f}%"
f0 = lambda v: "-" if v is None else f"{v:.0f}%"
star = lambda y: "*" if nC[y] < 30 else ""
def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k/n; d = 1+z*z/n; c = p+z*z/(2*n); h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (max(0, (c-h)/d), (c+h)/d)
def row(label, cells): return "| " + label + " | " + " | ".join(str(c) for c in cells) + " |"
def head(first): return row(first, [y + (" (to Sep)" if y == "2026" else "") for y in Y]) + "\n|---|" + "---|" * len(Y)

# ---------- hand-check derived numbers (manual adjustment; not produced by the op) ----------
J_ = S3["judgements"]; wrong_ids = {S3["borderline"][i]["id"] for i in J_["B_rule_wrong_should_be_work_idx"]}
border_ids = {b["id"] for b in S3["borderline"]}; op_border = {j for j, p in P.items() if p["borderline"]}
assert border_ids == op_border, ("borderline sets differ", len(border_ids), len(op_border))
err_nb = (len(J_["D_rule_wrong_idx"]) - len(J_["D_wrong_due_to_regex_bug_idx"])) / (len(S3["domain_nonborderline"]) - len(J_["D_wrong_due_to_regex_bug_idx"]))
dom = res["ai_as_domain"]; corrected = {}
for y in Y:
    corr_b = sum(1 for j in wrong_ids if y in P[j]["years"])
    nb = dom[y]["domain_k"] - dom[y]["borderline_k"]
    corrected[y] = dom[y]["domain_k"] - corr_b - err_nb * nb
early = ["2021", "2022", "2023", "2024"]
p_early = sum(corrected[y] for y in early) / sum(nC[y] for y in early); n_early = sum(nC[y] for y in early)
lo25, hi25 = wilson(round(corrected["2025"]), nC["2025"]); loE, hiE = wilson(round(p_early * n_early), n_early)
# baseline: domain-function words among ALL observed postings
allobs = Counter(y for e in INDEX.values() for y in e["years"]); base = Counter()
for e in INDEX.values():
    if A._DOMAIN_FUNC.search(e["title"]):
        for y in e["years"]: base[y] += 1
# composition of rule-domain titles
FUNCS = [("marketing / brand", r"marketing|brand"), ("UX / design", r"\bux\b|design|interaction"), ("ops / support / escalations", r"operations manager|escalations?|enforcement|support\b|vendor"),
         ("generic front-end / full-stack / mobile / web engineering", r"front ?end|full ?stack|\bmobile\b|\bandroid\b|\bios\b|\bweb\b"), ("policy / government affairs", r"policy|government affairs"),
         ("comms / writing", r"\bcommunications\b|comms\b|writer"), ("finance / people / recruiting", r"finance|accountant|recruit|talent|\bhr\b"), ("legal / counsel", r"legal|counsel"), ("strategy", r"strategist|strategy")]
def comp(period):
    c = Counter(); tot = 0
    for p in P.values():
        if p["nature"] == "domain" and any(y in period for y in p["years"]):
            tot += 1
            for name, rx in FUNCS:
                if re.search(rx, p["title"], re.I): c[name] += 1; break
    return tot, c
# data-driven tokens
STOP = set("and of the for at in on to a an with google cloud".split())
LANG = set("english spanish portuguese french german japanese korean mandarin arabic hindi italian dutch polish turkish russian thai indonesian bahasa vietnamese chinese cantonese hebrew swedish czech ukrainian romanian hungarian greek tagalog swahili".split())
LOC = set("india london zurich munich paris tokyo singapore sydney toronto kirkland seattle bengaluru hyderabad dublin tel aviv mountain view york san francisco sunnyvale cambridge boston austin cupertino waterloo pittsburgh warsaw amsterdam mexico brazil emea apac latam americas na".split())
LEVEL = set("i ii iii iv v vi senior staff principal sr lead early career intern campus start phd ms bs msc fixed term employee resident university graduate year summer fall winter".split())
DROP = STOP | LANG | LOC | LEVEL
toks = lambda t: {w.lower() for w in re.findall(r"[A-Za-z]+", t) if len(w) > 2 and w.lower() not in DROP}
core_p = [p for p in P.values() if p["core"]]
earlyP = [p for p in core_p if p["first_month"][:4] <= "2023"]; lateP = [p for p in core_p if p["first_month"][:4] >= "2024"]
ce, cl = Counter(), Counter()
for p in earlyP: ce.update(toks(p["title"]))
for p in lateP: cl.update(toks(p["title"]))
Ne, Nl = len(earlyP), len(lateP); trows = []
for w in set(ce) | set(cl):
    a, b = ce[w], cl[w]
    if a + b < 12: continue
    lo = math.log((b+.5)/(Nl-b+.5)) - math.log((a+.5)/(Ne-a+.5)); se = math.sqrt(1/(a+.5)+1/(b+.5)+1/(Ne-a+.5)+1/(Nl-b+.5)); trows.append((lo/se, w, a, b))
trows.sort(); rising = [f"{w} ({100*b/Nl:.0f}% vs {100*a/Ne:.0f}%)" for z, w, a, b in trows[::-1][:24]]; falling = [f"{w} ({100*b/Nl:.0f}% vs {100*a/Ne:.0f}%)" for z, w, a, b in trows[:12]]

# ---------- 1. trends.json ----------
gen = datetime.datetime.now(datetime.timezone.utc).isoformat()
trends = {"meta": {"generated_utc": gen, "rules_version": res["rules_version"], "source_capture": "scraper-data/google-careers-job-urls.cdx.json", "capture_range": res["capture_range"],
                   "total_postings": res["total_postings"], "produced_by": "plugins/job_search/wayback_google_ai.py :: google_wayback_ai_trends (+ c4_generate.py for the hand-check block)"},
          "definitions": {"core": "title (after removing 'Quantum AI' and 'data scien*') names AI/ML work by keyword/acronym", "data_science_only": "'data scien*' with no core word (analytics; separate layer)",
                          "deepmind_titled_A": "title contains DeepMind", "deepmind_only_B": "A that is not CORE by other words", "ai_adjacent": "Assistant/ranking/recommendation/personalization/perception/robotics/translate/speech/generic research titles; counts only",
                          "families_first_match_order": res["families"]["order"], "ai_as_domain": "function unrelated to AI expertise or generic front-end/full-stack/mobile/web engineering with AI only as a label (heuristic)",
                          "year_rule": "a posting counts toward every year it was captured (same as the cybersecurity analysis)"},
          "caveats": ["postings are only those Wayback archived, not every Google opening", "yearly archived counts swing with crawl activity, so shares of observed postings are used",
                      "titles come from URL slugs: role types, not skills", "classification is a keyword heuristic", "causes are inference", "2019/2020 CORE n<30 (noisy); 2026 is partial"],
          "supersedes": "AI figures in google-wayback-job-trends.json and google-wayback-analysis.md used the broader older rule (analytics + Quantum AI included, Aiml spellings missed); superseded FOR AI ONLY. Cybersecurity numbers unaffected.",
          "tables": {k: v for k, v in res.items() if k not in ("flagged_postings", "rules_version", "domain")},
          "hand_check": {"single_judge_unblinded": True, "borderline_verdicts": [{"job_id": b["id"], "title": b["title"], "first_year": b["year"],
                         "verdict": ("work (rule wrong)" if i in J_["B_rule_wrong_should_be_work_idx"] else "domain (marginal)" if i in J_["B_marginal_kept_domain_idx"] else "domain (agree)")} for i, b in enumerate(S3["borderline"])],
                         "samples": {"borderline_all": len(S3["borderline"]), "domain_nonborderline": len(S3["domain_nonborderline"]), "work": len(S3["work"])},
                         "non_borderline_error_rate_after_regex_fix": err_nb, "ai_as_domain_hand_corrected_pct": {y: 100*corrected[y]/nC[y] for y in Y}},
          "precision_recall": {"precision_sample": S2["precision_result"], "recall": S2["recall_result"], "exact_overlap_published_vs_core": S2["exact_overlap"], "note": "single sample, judged by the rule's author, unblinded"},
          "postings": res["flagged_postings"]}
(OUT / "google-wayback-ai-trends.json").write_text(json.dumps(trends, indent=1))

# ---------- 2. roles-by-year.md ----------
FAM_LABEL = {"ai_safety_responsible": "AI safety / responsible AI", "sales_consulting_gtm": "Sales, consulting & go-to-market", "product_program_mgmt": "Product & program management",
             "business_functions": "Business functions (marketing, policy, legal, design/UX, ops…)", "research": "Research", "infra_hardware": "Infrastructure & hardware",
             "ml_ai_engineering": "ML / AI engineering", "management_other": "Management (other)", "other_functions": "Other"}
L = ["# Google AI-tagged job postings by year (Wayback-archived posting URLs)", "",
     "Every posting Wayback archived for Google that the **strict CORE AI/ML** rule tags, grouped by the year it was **captured** and by role family. Companion to `google-wayback-security-roles-by-year.md`; analysis in `google-wayback-ai-analysis.md`.", "",
     "**Read first:** postings are only those Wayback archived, not every Google opening; a posting appears under every year it was captured; titles come from URL slugs (re-cased, punctuation lost); classification is a keyword heuristic (rules version `" + res["rules_version"] + "`). A number in brackets means several distinct postings share that title in that year.",
     "Families are mutually exclusive, first match wins: " + " > ".join(res["families"]["order"]) + ".", "",
     "Definitions used throughout: **DeepMind-titled (A)** = title contains DeepMind (34 postings); **DeepMind-only (B)** = A that is not CORE by other words (27); the other 7 are listed in the CORE sections.", ""]
by = defaultdict(lambda: defaultdict(Counter))
for p in P.values():
    if p["core"]:
        for y in p["years"]:
            if y in Y: by[y][p["family"]][p["title"]] += 1
for y in Y:
    L += [f"## {y}{' (to Sep)' if y == '2026' else ''}  --  {nC[y]} CORE postings of {obs[y]} observed ({f1(res['headline_strict_core'][y]['share_pct'])}){'  [n<30: noisy]' if nC[y] < 30 else ''}", ""]
    for fam in res["families"]["order"]:
        c = by[y].get(fam)
        if not c: continue
        L.append(f"### {FAM_LABEL[fam]} ({sum(c.values())})")
        L += [f"- {t}" + (f" [{n}]" if n > 1 else "") for t, n in sorted(c.items())]; L.append("")
L += ["---", "", "## Data-science-only postings (analytics, NOT AI) — separate layer", "",
      "Titles with a data-scientist word and no separate AI/ML word. Google's data scientists are mostly Ads/product analytics, so these are excluded from the headline. Grouped by year captured.", ""]
dsby = defaultdict(Counter)
for p in P.values():
    if p["data_science_only"]:
        for y in p["years"]:
            if y in Y: dsby[y][p["title"]] += 1
for y in Y:
    if not dsby[y]: continue
    L += [f"### {y} ({sum(dsby[y].values())} postings of {obs[y]} observed = {f1(100*sum(dsby[y].values())/obs[y])})"] + [f"- {t}" + (f" [{n}]" if n > 1 else "") for t, n in sorted(dsby[y].items())] + [""]
L += ["---", "", "## DeepMind-only postings (B = 27) — own section, excluded from the headline", "",
      "All were first captured Mar–Sep 2026; none earlier. Why they appear only in 2026 is not verifiable from this data (a change in what Wayback archived is one possibility).", ""]
dm = sorted((p["first_month"], p["title"]) for p in P.values() if p["deepmind_only"])
L += [f"- {t}  (first captured {m})" for m, t in dm] + ["", "---", "", "## AI-adjacent titles — counts only (titles not listed)", "",
      "Assistant / ranking / recommendation / personalization / perception / robotics / translate / speech / generic research titles: excluded from the headline because a title alone cannot show AI/ML work.", "",
      head("year"), row("AI-adjacent postings", [res["counts"]["ai_adjacent"][y]["k"] for y in Y]), row("observed postings", [obs[y] for y in Y]), ""]
(OUT / "google-wayback-ai-roles-by-year.md").write_text("\n".join(L))
n_titles = len({p["title"] for p in P.values() if p["core"]})

# ---------- 3. analysis.md ----------
H, Sx, R = res["headline_strict_core"], res["sensitivity"], res["reconciliation"]; NM = res["naming_vs_size"]; V = res["vocabulary"]; F = res["families"]; X = res["crossover"]; D = res["deepmind"]
firstyr = lambda term: next((y for y in Y if V[term][y]), "-")
ds = Sx["data_science_only"]
md = []
md += ["# Google AI roles, 2018–2026: what changed and what stayed", "",
       "Companion to `google-wayback-analysis.md` (the cybersecurity write-up) and built the same way: Wayback Machine's archive of Google's individual job-posting pages — **" + f"{res['total_postings']:,}" + " distinct postings** (URL = job ID + title slug; capture date = it was live then), of which **" + f"{sum(1 for p in P.values() if p['core']):,}" + " are AI/ML by the strict rule**.", "",
       "> **Supersedes the earlier AI figures, for AI only.** The AI columns in `google-wayback-job-trends.json` and the AI sentences in `google-wayback-analysis.md` used a broader keyword rule (it counted data-scientist analytics titles and Google's \"Quantum AI\" org, and missed titles spelled \"Aiml\"). Those AI figures are superseded by this file. **The cybersecurity numbers are unaffected.** `google-wayback-job-trends.json` is deliberately left unchanged as the record of the earlier rule.", "",
       "## Plain-language summary", "",
       f"1. **The 2024 jump is mostly a change in wording plus AI-labelled roles, not more roles called \"machine learning\".** Titles containing the phrase \"machine learning\" fell from {f0(V['machine learning']['2020'])}–{f0(V['machine learning']['2022'])} of AI titles (2020–2023) to {f0(V['machine learning']['2026'])} in 2026, while the acronym \"AI\" rose from about a quarter to {f0(V['AI (acronym)']['2026'])}. Counting every ML spelling together (machine learning / ML / Aiml), ML-family titles roughly doubled their share of *all* postings in 2024 ({f1(NM['2023']['ml_family_pct_of_observed'])} → {f1(NM['2024']['ml_family_pct_of_observed'])}) and then held ({f1(NM['2025']['ml_family_pct_of_observed'])}, {f1(NM['2026']['ml_family_pct_of_observed'])}), while titles that say AI/GenAI/Gemini *without* an ML word grew from {f1(NM['2023']['ai_label_only_pct_of_observed'])} (2023) to {f1(NM['2026']['ai_label_only_pct_of_observed'])} (2026). So most growth after 2023 is AI/GenAI-labelled titles. **What the data cannot say:** whether those are existing ML roles retitled or new roles — nothing here links an old posting to a new one.",
       f"2. **Level:** AI/ML titles were {f1(H['2019']['share_pct'])}–{f1(H['2023']['share_pct'])} of observed postings in 2019–2023, {f1(H['2024']['share_pct'])} in 2024, {f1(H['2025']['share_pct'])} in 2025 and {f1(H['2026']['share_pct'])} in 2026 (to Sep). A step up in 2024, then roughly flat. (Yearly archived counts swing from {min(obs.values()):,} to {max(obs.values()):,}, so only shares are compared.)",
       f"3. **Data-science analytics is a separate, growing thing:** {f1(min(ds[y]['share_pct'] for y in ('2020','2021','2022','2023')))}–{f1(max(ds[y]['share_pct'] for y in ('2020','2021','2022','2023')))} of postings in 2020–2023, {f1(ds['2024']['share_pct'])}, {f1(ds['2025']['share_pct'])}, then {f1(ds['2026']['share_pct'])} in 2026. It is Ads/product analytics, not AI, and is kept out of the headline.",
       f"4. **Supported lead (not a finding): AI as a team label on non-AI work.** The share of AI-titled postings whose function is unrelated to AI expertise (marketing, UX/design, ops/escalations, policy…) is about {100*corrected['2025']/nC['2025']:.0f}% in 2025 (rule {f1(dom['2025']['share_pct'])}) against about {100*p_early:.1f}% pooled 2021–2024. One judge, who also wrote the rule, checked it; see the section below for what would upgrade it.",
       f"5. **AI × security appears only from 2025:** none before 2025; {X['by_year']['2025']['raw_k']} postings in 2025 ({X['by_year']['2025']['clean_k']} after removing a false positive) and {X['by_year']['2026']['raw_k']} in 2026 (to Sep), about {f1(X['by_year']['2025']['clean_pct_of_security'])} and {f1(X['by_year']['2026']['clean_pct_of_security'])} of that year's security postings.", ""]
md += ["## What this data can and cannot tell you — read before the numbers", "",
       "- **Not every Google job.** Only postings Wayback archived.",
       f"- **Counts are not comparable across years; shares are.** Archived postings per year swing from {obs['2019']:,} (2019) to {obs['2025']:,} (2025) with Wayback's crawl activity. Every share below shows its denominator. Shares cancel crawl intensity to a first approximation, not perfectly — the 2025 dip may be partly broader archive coverage (observed postings ×{obs['2025']/obs['2024']:.1f} vs AI postings ×{nC['2025']/nC['2024']:.1f}); that is inference and cannot be checked here.",
       f"- **Small years are noisy.** 2019 ({nC['2019']}) and 2020 ({nC['2020']}) have fewer than 30 AI postings (marked `*`); 2026 is partial (to Sep).",
       "- **Titles, not skills.** Titles come from URL slugs; they show role types, not required skills.",
       "- **Keyword classification, one judge.** Every precision/recall figure below comes from a single sample judged by the classifier's own author, unblinded.",
       "- **Every cause given below (product launches, renames, reorganisations) is inference**, not something the data proves.", "",
       "Files this is based on: `google-wayback-ai-roles-by-year.md` (every AI posting by year and family), `google-wayback-ai-trends.json` (all tables + per-posting flags + the hand-check), `scraper-data/google-careers-job-urls.cdx.json` (raw URL list), code `plugins/job_search/wayback_google_ai.py` (op `google_wayback_ai_trends`, rules version `" + res["rules_version"] + "`).", ""]
md += ["## Headline: AI/ML share of observed postings (strict CORE)", "", head("") ,
       row("observed postings (denominator)", [f"{obs[y]:,}" for y in Y]), row("strict CORE postings (n)", [f"{nC[y]}{star(y)}" for y in Y]),
       row("**strict CORE share**", [f1(H[y]["share_pct"]) for y in Y]), "", "`*` = n<30, noisy.", "",
       "### Sensitivity: how much do the definitions matter?", "", head("share of observed postings"),
       row("(a) strict CORE — headline", [f1(Sx["strict_core"][y]["share_pct"]) for y in Y]), row("(b) strict CORE + DeepMind-titled", [f1(Sx["plus_deepmind"][y]["share_pct"]) for y in Y]),
       row("(c) strict CORE + AI-adjacent", [f1(Sx["plus_ai_adjacent"][y]["share_pct"]) for y in Y]), row("data-science-only (separate layer)", [f1(ds[y]["share_pct"]) for y in Y]),
       row("memo: earlier broader rule", [f"{100*R[y]['old_rule']/obs[y]:.1f}%" for y in Y]), "",
       f"2026 with and without DeepMind: {f1(Sx['strict_core']['2026']['share_pct'])} ({H['2026']['k']}/{obs['2026']}) vs {f1(Sx['plus_deepmind']['2026']['share_pct'])} ({Sx['plus_deepmind']['2026']['k']}/{obs['2026']}). Counts behind the separate lines — AI-adjacent: " + ", ".join(f"{y} {res['counts']['ai_adjacent'][y]['k']}" for y in Y) + "; data-science-only: " + ", ".join(f"{y} {ds[y]['k']}" for y in Y) + ".", "",
       f"**DeepMind — one definition per number.** A = titles containing \"DeepMind\": **{D['titled_A']}**. B = A not AI by other words (\"DeepMind-only\"): **{D['only_B']}**. The other {D['core_by_other_words']} are already in the headline by other words. (The earlier broader rule tagged {D['tagged_by_old_rule']} of the {D['titled_A']}; {D['not_tagged_by_old_rule_C']} it did not.) All {D['titled_A']} were first captured March–September 2026 (" + ", ".join(f"{m[4:]}/{m[:4]}: {c}" for m, c in D['first_captured_month_counts'].items()) + f"); none earlier. About half were archived through URLs carrying a `?company=DeepMind` listing filter. The earliest front-page snapshot that mentions DeepMind is 2026-07-02, and none of 25 old-layout snapshots (Jun 2021–Jun 2023) lists DeepMind in its organisation filter; for Jul 2023–Jun 2026 the filter list is not visible in the captures. **All {D['titled_A']} appear only in 2026; the cause is not verifiable from this data** (a change in what Wayback archived is one possibility). DeepMind is excluded from the headline and reported on its own.", ""]
md += ["## Reconciliation: earlier broader rule → strict CORE", "", "The 2025 share is 9.8% under both rules **only because large changes offset each other** — not because the classifier did not change.", "",
       head("postings per year"), row("earlier broader rule", [R[y]["old_rule"] for y in Y]),
       row("− data-scientist analytics", [R[y]["removed_data_science"] for y in Y]), row("− \"Quantum AI\" org name", [R[y]["removed_quantum_ai"] for y in Y]), row("− other", [R[y]["removed_other"] for y in Y]),
       row("+ Aiml / GenAI / MLOps spellings", [R[y]["added_aiml_genai_mlops"] for y in Y]), row("+ TPU / Vertex / Gemma / NotebookLM", [R[y]["added_tpu_vertex_gemma_notebooklm"] for y in Y]),
       row("+ agentic", [R[y]["added_agentic"] for y in Y]), row("+ other (natural language processing)", [R[y]["added_other"] for y in Y]), row("**= strict CORE**", [R[y]["new_core"] for y in Y]),
       row("identity holds", ["yes" if R[y]["identity_holds"] else "NO" for y in Y]), "",
       f"2025: {R['2025']['old_rule']} − {R['2025']['removed_data_science']+R['2025']['removed_quantum_ai']+R['2025']['removed_other']} removed + {R['2025']['added_aiml_genai_mlops']+R['2025']['added_tpu_vertex_gemma_notebooklm']+R['2025']['added_agentic']+R['2025']['added_other']} added = {R['2025']['new_core']}. Exact overlap of the two rules (no sampling): the earlier rule tags {res['published_rule_vs_core_exact']['published_rule_tags']}, strict CORE {res['published_rule_vs_core_exact']['core']}, both {res['published_rule_vs_core_exact']['overlap']} → the earlier rule's recall against strict CORE is {100*res['published_rule_vs_core_exact']['overlap']/res['published_rule_vs_core_exact']['core']:.1f}%, its precision {100*res['published_rule_vs_core_exact']['overlap']/res['published_rule_vs_core_exact']['published_rule_tags']:.1f}%.", ""]
md += ["## Wording versus size (the lead finding)", "", head("AI-titled postings only"),
       row("ML-family (machine learning / ML / Aiml / MLOps), % of AI postings", [f0(NM[y]["ml_family_pct_of_core"]) for y in Y]),
       row("AI/GenAI/Gemini **without** an ML-family word, % of AI postings", [f0(NM[y]["ai_label_only_pct_of_core"]) for y in Y]),
       row("ML-family, % of **all observed** postings", [f1(NM[y]["ml_family_pct_of_observed"]) for y in Y]),
       row("AI/GenAI-only, % of **all observed** postings", [f1(NM[y]["ai_label_only_pct_of_observed"]) for y in Y]),
       row("(counts: ML-family / AI-only)", [f"{NM[y]['ml_family_k']} / {NM[y]['ai_label_only_k']}" for y in Y]), "",
       "Reading it: as a share of AI titles, ML-family words fall (58–71% in 2020–2023 → 33% in 2026) — but as a share of *all* postings they rose in 2024 and then held around 4%. The growth after 2023 is mostly titles labelled AI/GenAI without an ML word. **Not supported:** that ML roles were \"retitled\" — that would need the same role tracked across years, which this data cannot do.", "",
       "### Vocabulary: share of each year's AI postings whose title contains the term", "", head("term"), row("n (AI postings)", [f"{nC[y]}{star(y)}" for y in Y])]
for term in V: md.append(row(term, [f0(V[term][y]) for y in Y]) .rstrip(" |") + f" | {firstyr(term)} |")
md[-len(V)-1:] = [l for l in md[-len(V)-1:]]
md += ["", "The last column is the first year the term appears in the *archive* — not necessarily its first year at Google (archive coverage varies). Note: \"LLM / language model\" is rare in titles (about 1% from 2022) — an earlier draft of this analysis understated it because of a matching bug that missed capitalised \"Large Language Models\"; this table is the corrected version.", "",
       f"### Data-driven comparison (AI postings first captured ≤2023, n={Ne}, vs ≥2024, n={Nl}); location, spoken-language and level words dropped; ≥12 uses", "",
       "- **Rising:** " + ", ".join(rising), "- **Falling:** " + ", ".join(falling), "",
       "Reading it (inference): generative/GenAI/Gemini/agent vocabulary arrives from 2023; the \"Cloud AI and Industry Solutions\" team-name words (\"industry\", \"solutions\", \"conversational\") fade; \"research\" falls; \"data\", \"analyst\", \"safety\", \"trust\" rise.", ""]
md += ["## Role families (mutually exclusive, first match wins)", "", "Order: " + " > ".join(f"{i+1} {n}" for i, n in enumerate(F["order"])) + ".", "",
       head("share of that year's AI postings"), row("n (AI postings)", [f"{nC[y]}{star(y)}" for y in Y])]
for fam in F["order"]: md.append(row(fam, [f0(F["shares_pct"][fam][y]) for y in Y]))
md += [row("sum", [f"{sum(F['shares_pct'][f][y] for f in F['order']):.0f}%" for y in Y]), "",
       "- **Constant:** ML/AI engineering is the largest family every year (" + ", ".join(f"{y} {f0(F['shares_pct']['ml_ai_engineering'][y])}" for y in Y[2:]) + "); sales/consulting/go-to-market 7–22%; product/program management 7–9% since 2021; AI safety/responsible AI small (≤5%).",
       "- **Moved:** infrastructure & hardware " + ", ".join(f"{y} {f0(F['shares_pct']['infra_hardware'][y])}" for y in Y[2:]) + " (bouncy; 2023 n=99); research is noisy (26% in 2020 on n=19, 15% in 2024, 3% in 2025).", "",
       "Families are heuristics (about 1 wrong in 24 in a spot check); the \"business functions\" family was split out of a mixed management bucket after review.", ""]
t25, c25 = comp({"2025"}); tE, cE = comp(set(early)); t26, c26 = comp({"2026"})
md += ["## AI as a team label on non-AI work — a supported lead, not a finding", "",
       "**What is claimed:** a growing share of AI-titled postings are functions unrelated to AI expertise (marketing, UX/design, ops/support/escalations, policy/government affairs, HR/finance, generic front-end/full-stack engineering) where \"AI\" is only the team or product name. One rule was applied to every year (so 2025 is compared on the same basis as the rest).", "",
       head("share of AI postings"), row("n (AI postings)", [f"{nC[y]}{star(y)}" for y in Y]), row("rule: domain-only postings (k)", [dom[y]["domain_k"] for y in Y]),
       row("rule: share", [f1(dom[y]["share_pct"]) for y in Y]), row("hand-corrected estimate", [f1(100*corrected[y]/nC[y]) for y in Y]), "",
       f"2025 hand-corrected ≈ {100*corrected['2025']/nC['2025']:.1f}% (95% Wilson interval {100*lo25:.1f}–{100*hi25:.1f}%) against ≈ {100*p_early:.1f}% pooled over 2021–2024 (n={n_early}; {100*loE:.1f}–{100*hiE:.1f}%). The intervals do not overlap; 2026 (≈{100*corrected['2026']/nC['2026']:.1f}%) overlaps both.", "",
       f"**Checks it survived:** one rule on all years; a hand check of 118 titles (all 40 borderline, 18 other domain calls, 60 \"work\" calls); a baseline showing that domain-function words among *all* observed postings did not rise in 2025 ({', '.join(f'{y} {100*base[y]/allobs[y]:.0f}%' for y in Y)}), so it is not simply broader archive coverage of non-technical roles.",
       "**What the hand check found:** of 40 borderline titles the rule wrongly called 10 \"domain\" (e.g. \"Android AI Core\", \"Chrome Web AI Platform\", \"Group Product Manager, Compliance and Policy, Generative AI\"); of 18 other domain calls, 3 were wrong (one was a regex bug: \"Tele*communications*\" matched \"communications\"); of 60 \"work\" calls, none was a clear domain miss and 2 were ambiguous. The hand-corrected row applies those corrections (exact for the borderline group; the non-borderline group scaled by its 2-in-17 error rate).", "",
       f"**Composition (rule, uncorrected)** — 2025 (n={t25}): " + ", ".join(f"{k} {v}" for k, v in c25.most_common()) + f". 2021–2024 (n={tE}): " + ", ".join(f"{k} {v}" for k, v in cE.most_common()) + f". 2026 (n={t26}): " + ", ".join(f"{k} {v}" for k, v in c26.most_common()) + ". The 2025 excess is marketing/brand, UX/design and ops/support/escalations (the last had none in 2021–2024).", "",
       "**Why only a *supported lead*:** the checker is one judge who also wrote the rule, unblinded. The direction survives the hand check and the uniform-rule comparison; the size is uncertain (rule 9.8% vs corrected ≈8.4% for 2025). **What would upgrade it:** an independent reader classifying the same 40 borderline titles (Appendix A) and a fresh random sample of ~100 AI titles from 2021–2024 and 2025. Cause (AI becoming a product-wide theme, so non-AI functions were hired under AI team names) is inference; also unresolved is whether Google hired more of these roles or Wayback archived more of them.", ""]
xy = X["by_year"]
md += ["## AI × cybersecurity", "", head("postings"), row("AI postings that are also security-tagged — raw", [xy[y]["raw_k"] for y in Y]), row("— cleaned (false positive removed)", [xy[y]["clean_k"] for y in Y]),
       row("AI postings (n)", [f"{nC[y]}{star(y)}" for y in Y]), row("cleaned, % of AI postings", [f1(xy[y]["clean_pct_of_core"]) for y in Y]),
       row("security-tagged postings (n)", [xy[y]["security_tagged"] for y in Y]), row("cleaned, % of security postings", [f1(xy[y]["clean_pct_of_security"]) for y in Y]), "",
       f"Raw {X['raw_total_postings']} postings, cleaned {X['clean_total_postings']}. Footnote: the one excluded false positive is \"{X['excluded_false_positives'][0]}\" — \"security\" there means *national* security. Counts under 10 are noisy (2026: {xy['2026']['clean_k']}). Titles: " + "; ".join(X["titles"]) + ". The shares of security postings (about 5–6% in 2025, 4% in 2026) agree with the cybersecurity analysis's AI-in-security-titles figures.", ""]
pr = S2["precision_result"]; rr = S2["recall_result"]
md += ["## Data science (analytics) — separate layer", "", head("share of observed postings"), row("data-science-only postings (k)", [ds[y]["k"] for y in Y]), row("share", [f1(ds[y]["share_pct"]) for y in Y]),
       row("95% interval", [f"{100*wilson(ds[y]['k'], obs[y])[0]:.1f}–{100*wilson(ds[y]['k'], obs[y])[1]:.1f}%" for y in Y]), "",
       "This is Ads/product analytics, not AI. It rises from 0.7–1.1% (2020–2023) to 4.2% in 2026 (2026 does not overlap 2025). Cause unknown. 2019 (k=5) and 2020 (k=4) are noisy.", "",
       "## Quality of the classifier", "",
       f"Every figure here is from **one sample, judged by the classifier's own author, unblinded.**", "",
       f"- **Precision** (100 matched titles, stratified by year): raw {pr['judgement_counts'].get('Y',0)} of 100 judged AI-as-work (6 domain-only, 0 outright false matches); **year-weighted strict precision {pr['strict_pct']}% ± {pr['strict_halfwidth']}**. The gap between 94 and 86: sampling gave roughly equal titles per year, but the 2025 stratum is 45% of all AI postings and held 5 of the 6 domain-only titles, so population weighting lowers precision. Counting domain-only titles as correct, precision is ≈100% (no outright false match in 100, i.e. below about 3–4%).",
       f"- **Recall** of the strict rules: 100 weak-signal and 150 remainder titles among the unmatched; missed ≈{rr['missed_W_strict'][0]} (95% interval {rr['missed_W_strict'][1]}–{rr['missed_W_strict'][2]}) clear plus ≈{rr['missed_W_incl_ambiguous'][0]} (interval {rr['missed_W_incl_ambiguous'][1]}–{rr['missed_W_incl_ambiguous'][2]}) if ambiguous titles count; 0 of 150 remainder titles positive (rule-of-three upper bound {rr['missed_R_upper_bound']}). Residual recall {rr['recall_central_with_ambiguous_pct']}–{rr['recall_central_strict_pct']}% central; conservative floor {rr['recall_floor_pct']}% (loose, from the small remainder sample).",
       "- Not countable from titles and excluded: generic \"Research Scientist, Google Research\" (~157), Google Assistant roles (~63), ranking/recommendation/personalization, perception/robotics, translate/speech.", ""]
md += ["## What changed / what stayed", "",
       f"**Changed:** a step up in AI share in 2024 ({f1(H['2023']['share_pct'])} → {f1(H['2024']['share_pct'])}); wording moved from \"machine learning\" to \"AI\"/\"Aiml\"/GenAI (generative/GenAI 0% to 2022, {f0(V['generative / GenAI']['2023'])} in 2023, {f0(V['generative / GenAI']['2024'])} in 2024; Gemini {f0(V['Gemini']['2024'])}% in 2024; agentic/agent from {firstyr('agent / agentic')}, {f0(V['agent / agentic']['2026'])} in 2026; Vertex only from {firstyr('Vertex')}); AI × security titles from 2025; analytics titles rising; a supported lead that AI became a team label for non-AI functions in 2025.",
       "**Stayed:** ML/AI engineering is the largest family every year; sales/consulting/go-to-market is a steady 7–22% of AI titles; product/program management 7–9%; AI safety small.", "",
       "## What the data cannot say — and the sensible next step", "",
       "Titles cannot show skills, seniority mix or whether roles were retitled rather than created. Skills need job descriptions: the live crawler (`google-live/`) covers currently-active security roles; descriptions for AI roles would need one extra page load per role, which has not been requested. A second, independent reader for the classifier (Appendix A) is the cheapest way to firm up the team-label lead.", ""]
md += ["## Appendix A — the 40 borderline titles and the hand-check verdict for each", "",
       "\"Rule\" = the rule called it AI-as-domain. \"Verdict\" = my reading, single judge, unblinded. Please check them yourself.", "", "| # | first captured | title | rule | my verdict |", "|---|---|---|---|---|"]
for i, b in enumerate(S3["borderline"]):
    v = "**work** (rule wrong)" if i in J_["B_rule_wrong_should_be_work_idx"] else "domain (marginal)" if i in J_["B_marginal_kept_domain_idx"] else "domain (agree)"
    md.append(f"| {i+1} | {b['year']} | {b['title']} | domain | {v} |")
md += ["", "## Appendix B — how to reproduce", "",
       f"`plugins/job_search/wayback_google_ai.py`, op `google_wayback_ai_trends(domain, data_repo_path)` (analyze kind, no network, ~2 s) regenerates every table in this file except the hand-check block, the precision/recall samples and the data-driven token comparison (`google-ai/c4_generate.py`). Rules version `{res['rules_version']}`; tests in `tests/test_google_wayback_ai.py` (41). Registration in `plugins/job_search/__init__.py` is left to the maintainer (`google-ai/PLUGIN_NOTES.md`)."]
(OUT / "google-wayback-ai-analysis.md").write_text("\n".join(md))
print("wrote trends.json", len(res["flagged_postings"]), "postings | roles-by-year:", n_titles, "distinct CORE titles | analysis lines:", len(md))
print("corrected shares:", {y: round(100*corrected[y]/nC[y], 1) for y in Y}, "| pooled 2021-24:", round(100*p_early, 1), "| 2025 CI:", round(100*lo25, 1), round(100*hi25, 1), "| early CI:", round(100*loE, 1), round(100*hiE, 1))
