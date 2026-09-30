import re, glob
from classify import split_questions, classify_question

files = {
  "2016":10, "2018":10, "2019":10, "2022":10, "2023":10,
  "2024_CS1":10, "2024_CS2":10, "2025_CS1":10, "2025_CS2":10, "2026_CS1":10, "2026_CS2":10,
}
unclassified_samples = []
calc_candidates = []
for fn, ga in files.items():
    path = f"extracted-text-cache/{fn}.txt"
    try:
        text = open(path, encoding='utf-8', errors='ignore').read()
    except FileNotFoundError:
        continue
    chunks = split_questions(text, 65)
    for qnum, chunk in chunks:
        if qnum <= ga:
            continue
        sec, hits, nsec = classify_question(chunk, exclude_ga=True)
        if sec is None:
            unclassified_samples.append((fn, qnum, len(chunk)))
        # look for calculus-adjacent signals missed
        if re.search(r'\bf\'\(|\bdx\b|\bderivative\b|\bdefinite integral\b|\bd/dx\b|\bf\(x\)\b', chunk, re.I) and sec != "2-EngMath-Calculus":
            calc_candidates.append((fn, qnum, sec))

print("Total unclassified sample count:", len(unclassified_samples))
print("Calculus-notation-but-misclassified count:", len(calc_candidates))
print(calc_candidates[:15])
