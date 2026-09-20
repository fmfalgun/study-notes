import sys; sys.path.insert(0, ".")
from c1_load import *
import c2_rules as R
FL = {jid: R.flags(e["title"]) for jid, e in INDEX.items()}
core = {j for j, f in FL.items() if f["core"]}
old = {j for j, e in INDEX.items() if "ai" in classify_title(e["title"])}
obs = Counter(y for e in INDEX.values() for y in e["years"]); years = [y for y in sorted(obs) if y >= "2019"]

# ---- DeepMind definitions
A = {j for j, f in FL.items() if f["deepmind"]}
print("DEEPMIND definitions:")
print(f"  A = titles containing 'DeepMind' (any rule)                      : {len(A)}")
print(f"  B = A not CORE by other words (= 'DeepMind-only', used in C2)     : {len(A - core)}")
print(f"  A in strict CORE by other words                                   : {len(A & core)}")
print(f"  C = A not tagged by the OLD published rule (the '29' in C1)       : {len(A - old)}")
print(f"  A tagged by the OLD rule                                          : {len(A & old)}")
print(f"  A first captured in 2026 (all of A): {sum(1 for j in A if INDEX[j]['first_month'] >= '202601')}; earliest {min(INDEX[j]['first_month'] for j in A)}")
print(f"  check: |A|={len(A)} = |A-old|({len(A-old)}) + |A&old|({len(A&old)}) ; = |A-core|({len(A-core)}) + |A&core|({len(A&core)})")

# ---- reconciliation old -> new, per year (postings counted in every year captured)
def reason_removed(j):
    t = INDEX[j]["title"]
    if re.search(r"\bdata scien\w+", t, re.I): return "removed: data-scientist (analytics)"
    if re.search(r"\bquantum ai\b", t, re.I): return "removed: 'Quantum AI' org name"
    return "removed: other"
def reason_added(j):
    t = INDEX[j]["title"]
    if re.search(r"\b(aiml|genai|mlops|aimachine)\b", t, re.I): return "added: Aiml/GenAI/MLOps spelling"
    if re.search(r"\b(tensor processing|vertex|tpus?|gemma|notebooklm|bard)\b", t, re.I): return "added: TPU/Vertex/Gemma/NotebookLM"
    if re.search(r"\b(agentic|autonomous agents?|agent platform)\b", t, re.I): return "added: agentic"
    return "added: other"
rows = defaultdict(Counter)
for j in old - core:
    for y in INDEX[j]["years"]: rows[reason_removed(j)][y] += 1
for j in core - old:
    for y in INDEX[j]["years"]: rows[reason_added(j)][y] += 1
oc = Counter(y for j in old for y in INDEX[j]["years"]); nc = Counter(y for j in core for y in INDEX[j]["years"])
print("\nRECONCILIATION (postings per year; old published rule -> strict CORE)")
print(f"{'':40}" + "".join(f"{y:>7}" for y in years))
print(f"{'old published rule':40}" + "".join(f"{oc[y]:>7}" for y in years))
for k in ["removed: data-scientist (analytics)", "removed: 'Quantum AI' org name", "removed: other",
          "added: Aiml/GenAI/MLOps spelling", "added: TPU/Vertex/Gemma/NotebookLM", "added: agentic", "added: other"]:
    sign = "-" if k.startswith("removed") else "+"
    print(f"{sign+' '+k.split(': ')[1]:40}" + "".join(f"{rows[k][y]:>7}" for y in years))
chk = {y: oc[y] - sum(rows[k][y] for k in rows if k.startswith("removed")) + sum(rows[k][y] for k in rows if k.startswith("added")) for y in years}
print(f"{'new strict CORE':40}" + "".join(f"{nc[y]:>7}" for y in years))
print(f"{'identity check (old-removed+added)':40}" + "".join(f"{chk[y]:>7}" for y in years), "| all equal new:", all(chk[y] == nc[y] for y in years))
print("\nsample of 'removed: other':", [INDEX[j]["title"] for j in (old - core) if reason_removed(j) == "removed: other"][:6])
print("sample of 'added: other'  :", [INDEX[j]["title"] for j in (core - old) if reason_added(j) == "added: other"][:6])
