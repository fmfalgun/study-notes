import re, json, sys
sys.path.insert(0, '.')
from classify import split_questions, classify_question, strip_range_headers

def classify_paper_text(text, label, ga_count=10, total_expected=65):
    chunks = split_questions(text, total_expected)
    results = []
    for qnum, chunk in chunks:
        if qnum <= ga_count:
            section, hits, nsec = "1-GA", [], 0
        else:
            sec, hits, nsec = classify_question(chunk, exclude_ga=True)
            section = sec
        complex_flag = (nsec >= 2) and section != "1-GA"
        results.append({"sitting": label, "q": qnum, "section": section, "complex": complex_flag})
    return results

CACHE = "extracted-text-cache/"

def load(fn):
    with open(CACHE+fn, encoding='utf-8', errors='ignore') as f:
        return f.read()

# 2015: split into 3 sessions
t2015 = load("2015.txt")
session_markers = list(re.finditer(r'SESSION\s*-\s*\d', t2015, re.IGNORECASE))
print("2015 session markers found:", [ (m.group(), m.start()) for m in session_markers])

boundaries = [0, 26520, 54104, len(t2015)]
all_2015_results = []
for i in range(3):
    seg = t2015[boundaries[i]:boundaries[i+1]]
    chunks = split_questions(seg, 65)
    qnums = [q for q,_ in chunks]
    print(f"Session-{i+1}: {len(chunks)} chunks, max q={max(qnums) if qnums else 0}, min q={min(qnums) if qnums else 0}")
