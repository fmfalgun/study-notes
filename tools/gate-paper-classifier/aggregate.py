#!/usr/bin/env python3
import json, glob, sys
from collections import defaultdict

def load(files):
    sittings = {}
    for f in files:
        data = json.load(open(f))
        sittings[f] = data
    return sittings

def per_sitting_summary(data):
    subj_all = [d for d in data if d['section'] != '1-GA']
    total_subj = len(subj_all)
    by_topic = defaultdict(lambda: {"count":0, "complex":0})
    unclassified = 0
    for d in subj_all:
        if d['section'] is None:
            unclassified += 1
            continue
        by_topic[d['section']]["count"] += 1
        if d['complex']:
            by_topic[d['section']]["complex"] += 1
    return total_subj, by_topic, unclassified

def aggregate(sittings, label):
    n = len(sittings)
    topic_pct_sum = defaultdict(float)
    topic_complex_sum = defaultdict(int)
    topic_count_total = defaultdict(int)
    total_unclassified = 0
    total_questions = 0
    print(f"=== {label}: {n} sittings ===")
    for f, data in sittings.items():
        total_subj, by_topic, unclassified = per_sitting_summary(data)
        total_questions += total_subj
        total_unclassified += unclassified
        print(f"  {f}: {total_subj} subject Qs, {unclassified} unclassified")
        for topic, v in by_topic.items():
            pct = 100.0 * v["count"] / total_subj if total_subj else 0
            topic_pct_sum[topic] += pct
            topic_complex_sum[topic] += v["complex"]
            topic_count_total[topic] += v["count"]
    print()
    print(f"{'Topic':30s} {'AvgPct':>8s} {'TotalCount':>10s} {'TotalComplex':>12s} {'Score':>8s}")
    rows = []
    for topic in sorted(set(list(topic_pct_sum.keys())+list(topic_complex_sum.keys()))):
        avg_pct = topic_pct_sum[topic] / n
        complex_ct = topic_complex_sum[topic]
        score = avg_pct + complex_ct * 1.5
        rows.append((topic, avg_pct, topic_count_total[topic], complex_ct, score))
    rows.sort(key=lambda r: -r[4])
    for topic, avg_pct, cnt, cplx, score in rows:
        print(f"{topic:30s} {avg_pct:8.2f} {cnt:10d} {cplx:12d} {score:8.2f}")
    print(f"\ntotal unclassified across all sittings: {total_unclassified} / {total_questions}")
    return rows

if __name__ == "__main__":
    cs_files = sorted(glob.glob("classified/cs_*.json"))
    da_files = sorted(glob.glob("classified/da_*.json"))
    cs_data = load(cs_files)
    da_data = load(da_files)
    aggregate(cs_data, "CS")
    print()
    aggregate(da_data, "DA")
