import re, json
from collections import defaultdict
from classify import split_questions, classify_question, LEX

SEC_NAMES = {
 "2-EngMath-LinearAlgebra":"Lin.Alg","2-EngMath-Probability":"Prob.","2-EngMath-Calculus":"Calculus",
 "3-DiscreteMath":"Discrete Math","4-DigitalLogic":"Digital Logic","5-COA":"COA","6-ProgDS":"Prog&DS",
 "7-Algorithms":"Algorithms","8-ToC":"ToC","9-Compiler":"Compiler","10-OS":"OS","11-DBMS":"DBMS","12-Networks":"Networks","13-ML":"ML","14-AI":"AI"}

def density_count(text, nominal_subject_q=55):
    hits_per_sec = defaultdict(int)
    total_hits = 0
    tl = text.lower()
    for sec, patterns in LEX.items():
        if sec == "1-GA": continue
        c = sum(1 for w,pat in patterns if pat.search(tl))
        hits_per_sec[sec] = c
        total_hits += c
    if total_hits == 0:
        return {SEC_NAMES[s]:0 for s in SEC_NAMES}
    return {SEC_NAMES[s]: round(hits_per_sec.get(s,0)/total_hits*nominal_subject_q) for s in SEC_NAMES}

def clean_count(fn, ga=10):
    text = open(f"extracted-text-cache/{fn}.txt",encoding='utf-8',errors='ignore').read()
    chunks = split_questions(text,65)
    counts = defaultdict(int)
    unclassified=0
    complex_list=[]
    total_subject=0
    for qnum,chunk in chunks:
        if qnum<=ga: continue
        total_subject+=1
        sec,hits,nsec = classify_question(chunk, exclude_ga=True)
        if sec is None:
            unclassified+=1
        else:
            counts[SEC_NAMES[sec]]+=1
            if nsec>=2: complex_list.append(qnum)
    return counts, unclassified, total_subject, complex_list

clean_files = {"2007":"2007","2009":"2009","2011":"2011","2012":"2012","2013":"2013",
  "2016":"2016","2018":"2018","2019":"2019","2022":"2022","2023":"2023",
  "2024-CS1":"2024_CS1","2024-CS2":"2024_CS2","2025-CS1":"2025_CS1","2025-CS2":"2025_CS2",
  "2026-CS1":"2026_CS1","2026-CS2":"2026_CS2"}

print("=== Re-run with fixed lexicon (printf/probability/cfl/attributed) ===")
grand_unclass=0; grand_total=0
for label,fn in clean_files.items():
    counts,unc,tot,cplx = clean_count(fn)
    grand_unclass+=unc; grand_total+=tot
    print(label, dict(counts), "unclassified=",unc,"/",tot, "complex=",len(cplx))
print(f"TOTAL clean-split unclassified: {grand_unclass}/{grand_total} = {grand_unclass/grand_total*100:.1f}%")
