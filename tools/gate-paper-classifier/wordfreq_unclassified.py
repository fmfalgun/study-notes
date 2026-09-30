import re
from collections import Counter
from classify import split_questions, classify_question

STOP = set("""the a an is are of to in for and or if then else with on at as by this that which
those these not can be will would could should has have had it its their there here when where
what which who whom from into over under between such other same more most less least also only
each every both either neither than but so because while do does did done given following below
above value values case cases number numbers following options option answer correct true false
following: statement statements consider let assume suppose""".split())

files = ["2016","2018","2019","2022","2023","2024_CS1","2024_CS2","2025_CS1","2025_CS2","2026_CS1","2026_CS2",
         "2008","2010","2014","2017_CS1","2017_CS2","2020","DA_2024","DA_2025","DA_2026"]
words = Counter()
n=0
for fn in files:
    try:
        text = open(f"extracted-text-cache/{fn}.txt", encoding='utf-8', errors='ignore').read()
    except FileNotFoundError:
        continue
    chunks = split_questions(text, 65)
    for qnum, chunk in chunks:
        if qnum <= 10: continue
        sec, hits, nsec = classify_question(chunk, exclude_ga=True)
        if sec is None:
            n+=1
            for w in re.findall(r"[a-z]{4,}", chunk.lower()):
                if w not in STOP:
                    words[w]+=1
print("n unclassified:", n)
for w,c in words.most_common(40):
    print(c,w)
