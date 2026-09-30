#!/usr/bin/env python3
import json, glob
from collections import defaultdict

SITTING_LABELS = {
    "classified/cs_2022_CS_QP.json": "2022-CS",
    "classified/cs_2023_CS_QP.json": "2023-CS",
    "classified/cs_2024_CS1_QP.json": "2024-CS1",
    "classified/cs_2024_CS2_QP.json": "2024-CS2",
    "classified/cs_2025_CS1_QP.json": "2025-CS1",
    "classified/cs_2025_CS2_QP.json": "2025-CS2",
    "classified/cs_2026_CS1_QP.json": "2026-CS1",
    "classified/cs_2026_CS2_QP.json": "2026-CS2",
    "classified/da_2024_DA_QP.json": "2024-DA",
    "classified/da_2025_DA_QP.json": "2025-DA",
    "classified/da_2026_DA_QP.json": "2026-DA",
}

TOPIC_NAMES = {
    "2-EngMath-LinearAlgebra": "Linear Algebra (Eng. Math)",
    "2-EngMath-Probability": "Probability & Statistics (Eng. Math)",
    "2-EngMath-Calculus": "Calculus (Eng. Math)",
    "3-DiscreteMath": "Discrete Mathematics",
    "4-DigitalLogic": "Digital Logic",
    "5-COA": "Computer Organization & Architecture",
    "6-ProgDS": "Programming & Data Structures",
    "7-Algorithms": "Algorithms",
    "8-ToC": "Theory of Computation",
    "9-Compiler": "Compiler Design",
    "10-OS": "Operating System",
    "11-DBMS": "Databases (DBMS)",
    "12-Networks": "Computer Networks",
    "13-ML": "Machine Learning",
    "14-AI": "Artificial Intelligence",
}

def load(files):
    return {f: json.load(open(f)) for f in files}

def per_sitting_summary(data):
    subj_all = [d for d in data if d['section'] != '1-GA']
    total_subj = len(subj_all)
    by_topic = defaultdict(lambda: {"count":0, "complex":0, "complex_qs":[]})
    unclassified = 0
    unclassified_qs = []
    for d in subj_all:
        if d['section'] is None:
            unclassified += 1
            unclassified_qs.append(d['q'])
            continue
        by_topic[d['section']]["count"] += 1
        if d['complex']:
            by_topic[d['section']]["complex"] += 1
            by_topic[d['section']]["complex_qs"].append(d['q'])
    return total_subj, by_topic, unclassified, unclassified_qs

def build(files, label):
    sittings = load(files)
    n = len(sittings)
    topic_pct_sum = defaultdict(float)
    topic_complex_sum = defaultdict(int)
    topic_count_total = defaultdict(int)
    topic_complex_cites = defaultdict(list)
    per_sitting_rows = {}
    total_unclassified = 0
    total_questions = 0
    for f, data in sittings.items():
        sl = SITTING_LABELS[f]
        total_subj, by_topic, unclassified, unclassified_qs = per_sitting_summary(data)
        total_questions += total_subj
        total_unclassified += unclassified
        per_sitting_rows[sl] = (total_subj, dict(by_topic), unclassified, unclassified_qs)
        for topic, v in by_topic.items():
            pct = 100.0 * v["count"] / total_subj if total_subj else 0
            topic_pct_sum[topic] += pct
            topic_complex_sum[topic] += v["complex"]
            topic_count_total[topic] += v["count"]
            for q in v["complex_qs"]:
                topic_complex_cites[topic].append(f"{sl} Q{q}")
    rows = []
    for topic in set(list(topic_pct_sum.keys())+list(topic_complex_sum.keys())):
        avg_pct = topic_pct_sum[topic] / n
        complex_ct = topic_complex_sum[topic]
        score = avg_pct + complex_ct * 1.5
        rows.append((topic, avg_pct, topic_count_total[topic], complex_ct, score))
    rows.sort(key=lambda r: -r[4])
    return rows, per_sitting_rows, total_unclassified, total_questions, topic_complex_cites, n

def print_markdown_table(rows, title):
    print(f"\n### {title}\n")
    print("| Topic | Avg weightage % | Total Qs (all sittings) | Total Complex | Score |")
    print("|---|---|---|---|---|")
    for topic, avg_pct, cnt, cplx, score in rows:
        name = TOPIC_NAMES.get(topic, topic)
        print(f"| {name} | {avg_pct:.1f}% | {cnt} | {cplx} | {score:.1f} |")

def print_per_sitting_table(per_sitting_rows, title):
    print(f"\n### {title}\n")
    all_topics = set()
    for sl, (total_subj, by_topic, unclassified, uq) in per_sitting_rows.items():
        all_topics.update(by_topic.keys())
    all_topics = sorted(all_topics)
    header = "| Sitting | " + " | ".join(TOPIC_NAMES.get(t,t) for t in all_topics) + " | Unclassified |"
    print(header)
    print("|" + "---|"*(len(all_topics)+2))
    for sl in sorted(per_sitting_rows.keys()):
        total_subj, by_topic, unclassified, uq = per_sitting_rows[sl]
        cells = [str(by_topic.get(t,{}).get("count",0)) for t in all_topics]
        print(f"| {sl} | " + " | ".join(cells) + f" | {unclassified} |")

if __name__ == "__main__":
    cs_files = sorted(glob.glob("classified/cs_*.json"))
    da_files = sorted(glob.glob("classified/da_*.json"))

    cs_rows, cs_per_sitting, cs_unclass, cs_total, cs_cites, cs_n = build(cs_files, "CS")
    da_rows, da_per_sitting, da_unclass, da_total, da_cites, da_n = build(da_files, "DA")

    print("=========== CS ===========")
    print_markdown_table(cs_rows, "CS Aggregate Topic Weightage (8 sittings, 2022-2026)")
    print_per_sitting_table(cs_per_sitting, "CS Per-Sitting Breakdown")
    print(f"\nTotal unclassified: {cs_unclass}/{cs_total} ({100*cs_unclass/cs_total:.1f}%)")
    print("\nComplex question citations by topic:")
    for t, cites in cs_cites.items():
        print(f"  {TOPIC_NAMES.get(t,t)}: {', '.join(cites)}")

    print("\n\n=========== DA ===========")
    print_markdown_table(da_rows, "DA Aggregate Topic Weightage (3 sittings, 2024-2026)")
    print_per_sitting_table(da_per_sitting, "DA Per-Sitting Breakdown")
    print(f"\nTotal unclassified: {da_unclass}/{da_total} ({100*da_unclass/da_total:.1f}%)")
    print("\nComplex question citations by topic:")
    for t, cites in da_cites.items():
        print(f"  {TOPIC_NAMES.get(t,t)}: {', '.join(cites)}")
