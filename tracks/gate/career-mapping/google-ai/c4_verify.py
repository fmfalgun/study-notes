"""Exact-reproduction check: plugin op output vs (a) numbers published in CHECKPOINT 2/3 and (b) independent scratch recomputation."""
import sys, json
sys.path.insert(0, "../no-github-remote/web-scrap"); sys.path.insert(0, ".")
from pathlib import Path
from plugins.job_search import wayback_google_ai as A
res = A.google_wayback_ai_trends("google.com", Path("../no-github-remote/scraper-data"))
Y = res["years"]; assert Y == ["2019","2020","2021","2022","2023","2024","2025","2026"], Y
fails = []
def chk(label, got, exp):
    if got != exp: fails.append((label, got, exp))
f1 = lambda d: [f"{d[y]['share_pct']:.1f}" for y in Y]
# ---- (a) published constants
chk("observed", [res["observed_postings"][y] for y in Y], [269,572,2326,4276,2371,2469,6824,1925])
chk("core k", [res["headline_strict_core"][y]["k"] for y in Y], [5,19,58,130,99,275,671,239])
chk("(a) share", f1(res["sensitivity"]["strict_core"]), "1.9 3.3 2.5 3.0 4.2 11.1 9.8 12.4".split())
chk("(b) share", f1(res["sensitivity"]["plus_deepmind"]), "1.9 3.3 2.5 3.0 4.2 11.1 9.8 13.8".split())
chk("(c) share", f1(res["sensitivity"]["plus_ai_adjacent"]), "4.8 4.7 4.0 4.4 4.9 13.8 10.7 14.3".split())
chk("DS share", f1(res["sensitivity"]["data_science_only"]), "1.9 0.7 1.1 0.8 0.7 2.2 2.1 4.2".split())
chk("DS k", [res["sensitivity"]["data_science_only"][y]["k"] for y in Y], [5,4,25,36,17,54,142,80])
chk("adjacent k", [res["counts"]["ai_adjacent"][y]["k"] for y in Y], [8,8,35,60,17,65,56,37])
chk("deepmind-only k", [res["counts"]["deepmind_only"][y]["k"] for y in Y], [0,0,0,0,0,0,0,27])
d = res["deepmind"]; chk("deepmind A/B/core/C/old", (d["titled_A"], d["only_B"], d["core_by_other_words"], d["not_tagged_by_old_rule_C"], d["tagged_by_old_rule"]), (34,27,7,29,5))
chk("deepmind months", d["first_captured_month_counts"], {"202603":1,"202604":6,"202606":3,"202607":19,"202608":4,"202609":1})
rec = res["reconciliation"]
exp_rec = {"old_rule":[11,22,97,166,114,298,666,289], "removed_data_science":[5,4,25,36,17,54,142,80], "removed_quantum_ai":[1,1,16,8,4,5,15,31],
  "removed_other":[0]*8, "added_aiml_genai_mlops":[0,1,1,3,4,28,138,52], "added_tpu_vertex_gemma_notebooklm":[0,0,0,2,1,6,19,6],
  "added_agentic":[0,0,0,1,0,0,3,3], "added_other":[0,1,1,2,1,2,2,0], "new_core":[5,19,58,130,99,275,671,239]}
for k, v in exp_rec.items(): chk("reconciliation "+k, [rec[y][k] for y in Y], v)
chk("identity all years", all(rec[y]["identity_holds"] for y in Y), True)
e = res["published_rule_vs_core_exact"]; chk("exact overlap", (e["published_rule_tags"], e["core"], e["overlap"]), (1524,1385,1119))
fam = res["families"]; chk("family order", fam["order"], ["ai_safety_responsible","sales_consulting_gtm","product_program_mgmt","business_functions","research","infra_hardware","ml_ai_engineering","management_other","other_functions"])
exp_fam = {"ai_safety_responsible":[0,0,3,5,1,1,3,3], "sales_consulting_gtm":[20,21,22,7,18,12,16,15], "product_program_mgmt":[0,0,9,8,7,7,8,8],
  "business_functions":[0,0,9,3,7,4,10,7], "research":[0,26,12,7,4,15,3,6], "infra_hardware":[0,0,0,9,21,8,10,15],
  "ml_ai_engineering":[80,47,43,55,39,49,47,44], "management_other":[0,0,2,4,2,4,2,2], "other_functions":[0,5,0,2,0,0,0,1]}
for k, v in exp_fam.items(): chk("family "+k, [int(f"{fam['shares_pct'][k][y]:.0f}") for y in Y], v)
chk("family shares sum 100", [round(sum(fam["shares_pct"][k][y] for k in fam["order"])) for y in Y], [100]*8)
dom = res["ai_as_domain"]
chk("domain k", [dom[y]["domain_k"] for y in Y], [0,0,2,5,3,15,66,17]); chk("domain share", f1(dom), "0.0 0.0 3.4 3.8 3.0 5.5 9.8 7.1".split())
chk("borderline k", [dom[y]["borderline_k"] for y in Y], [0,0,0,3,2,8,25,5])
nm = res["naming_vs_size"]
chk("ML-family % core", [int(f"{nm[y]['ml_family_pct_of_core']:.0f}") for y in Y], [100,58,62,71,69,49,41,33])
chk("AI-only % core", [int(f"{nm[y]['ai_label_only_pct_of_core']:.0f}") for y in Y], [0,37,36,22,29,43,55,63])
chk("ML-family % obs", [f"{nm[y]['ml_family_pct_of_observed']:.1f}" for y in Y], "1.9 1.9 1.5 2.2 2.9 5.5 4.0 4.1".split())
chk("AI-only % obs", [f"{nm[y]['ai_label_only_pct_of_observed']:.1f}" for y in Y], "0.0 1.2 0.9 0.7 1.2 4.8 5.4 7.8".split())
exp_vocab = {"machine learning":[100,53,60,66,58,36,17,5], "AI (acronym)":[0,26,28,23,34,38,50,55], "Aiml spelling":[0,5,2,2,4,9,20,20],
  "generative / GenAI":[0,0,0,0,4,12,16,13], "Gemini":[0,0,0,0,0,7,5,3], "agent / agentic":[0,0,0,1,0,0,3,5], "Vertex":[0,0,0,0,0,0,1,2],
  "LLM / language model":[0,0,0,0,0,0,1,0], "TPU / tensor":[0,0,0,3,4,3,3,3], "responsible AI / AI safety":[0,0,2,4,0,1,2,1]}
for k, v in exp_vocab.items(): chk("vocab "+k, [int(f"{res['vocabulary'][k][y]:.0f}") for y in Y], v)
cx = res["crossover"]
chk("crossover raw/clean totals", (cx["raw_total_postings"], cx["clean_total_postings"]), (23, 22))
chk("crossover raw 2025/2026", (cx["by_year"]["2025"]["raw_k"], cx["by_year"]["2026"]["raw_k"]), (18, 5))
chk("crossover excluded", cx["excluded_false_positives"], ["Aiml Engineer National Security Public Sector"])
# ---- (b) independent scratch recomputation (earlier c1/c2/c3 modules)
sys.argv = [sys.argv[0]]
from c1_load import INDEX, Counter, classify_title
import c2_rules as R2, c3_rules as R3
FL = {j: R2.flags(e["title"]) for j, e in INDEX.items()}
core = {j for j, f in FL.items() if f["core"]}
yc = lambda S: Counter(y for j in S for y in INDEX[j]["years"])
chk("scratch core k", [yc(core)[y] for y in Y], [res["headline_strict_core"][y]["k"] for y in Y])
chk("scratch ds k", [yc({j for j,f in FL.items() if f['ds_only']})[y] for y in Y], [res["sensitivity"]["data_science_only"][y]["k"] for y in Y])
chk("scratch family counts", [{y: sum(1 for j in core if R3.family(INDEX[j]['title']).split(' ',1)[1] == k and y in INDEX[j]['years']) for y in Y} for k in fam["order"]],
    [fam["counts"][k] for k in fam["order"]])
chk("scratch domain k", [sum(1 for j in core if R3.nature(INDEX[j]['title'])[0]=='domain' and y in INDEX[j]['years']) for y in Y], [dom[y]["domain_k"] for y in Y])
print("MISMATCHES:", len(fails))
for lab, got, exp in fails: print(" -", lab, "\n     got     :", got, "\n     expected:", exp)
json.dump(res, open("c4_op_output.json", "w"))
print("op output saved:", len(res["flagged_postings"]), "flagged postings")
