"""C5: per-year description analysis, generalising c4_pilot_2025.py. OFFLINE (no network).
Run:  .venv/bin/python3 c4_years.py <year|drift|all>      (venv: ../no-github-remote/web-scrap/.venv/bin/python3)
  <year>  -> c5_terms_<year>.md/.json, c5_sample_<year>.txt, findings/<year>.md (+ c5_quote_check_<year>.txt)
  drift   -> c5_drift.md (2024 -> 2025 -> 2026, groups with n>=30 in EVERY year compared)
  all     -> 2025 2024 2026 2023 drift
Scope: postings are only those Wayback archived. 2019-2022 postings are title-based only; descriptions cover postings archived
from mid-2023 (capture years 2023-2026). Same extraction rules for every year (see c4_method.md + c5_method.md).
Change vs the pilot (entry [10]): the degree-line rule now drops only lines that ARE the degree requirement."""
import sys, os, re, json, random
from pathlib import Path
from collections import Counter, defaultdict
sys.path.insert(0, "../no-github-remote/web-scrap")
from plugins.job_search import wayback_google_details as g
D = Path("./tracks/gate/career-mapping/google-jd")
REPO = Path("../no-github-remote/scraper-data")
SECS = ["minimum_qualifications", "preferred_qualifications", "responsibilities"]
SECNAME = {"minimum_qualifications": "required (minimum)", "preferred_qualifications": "preferred", "responsibilities": "responsibilities", "any": "any section"}
SHORT = {"minimum_qualifications": "required", "preferred_qualifications": "preferred", "responsibilities": "responsibilities", "any": "any"}
BOILER, MIN_DF, SUBSUME, WEAK = 0.90, 5, 0.80, 30
QUOTAS = {  # postings read qualitatively per theme (seeded); 2025 keeps the pilot's 15
    "2025": {"security_engineering": 4, "threat_intel_and_response": 4, "sales_and_consulting": 3, "other_security": 2, "physical_corporate_security": 2},
    "2024": {"security_engineering": 4, "threat_intel_and_response": 3, "sales_and_consulting": 2, "other_security": 2, "physical_corporate_security": 2},
    "2026": {"security_engineering": 4, "threat_intel_and_response": 3, "sales_and_consulting": 2, "other_security": 2, "physical_corporate_security": 1},
    "2023": {"security_engineering": 3, "threat_intel_and_response": 3, "sales_and_consulting": 1, "other_security": 1},
}
def atomic(p, t):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True); tmp = str(p) + ".tmp"; Path(tmp).write_text(t); os.replace(tmp, p)

STOP = set("""a an the and or nor but if then else of in on at to for from by with without within into onto over under about as is are was were be been being
am do does did doing have has had having it its this that these those there their they them we our you your he she his her who whom whose which what when where why how
not no yes so than too very can could should would will shall may might must also just only such each every any all both either neither some most more less many much
other another own same via per across through between among during after before above below up down out off again further once here e.g eg i.e ie etc and/or vs
experience experienced experiences year years ability able strong including include includes included knowledge understanding work working works related relevant similar plus
using use used uses new well good excellent preferred minimum qualification qualifications equivalent practical role position ideally least one two three four five multiple various
demonstrated proven proficient proficiency skill skills capable familiarity familiar background hands hand-on largely highly additional additionally ensure ensuring across
etc. others like way ways well-versed variety wide range diverse need needs needed based both able get make making take taking help helping provide providing part
also team teams member members""".split())
COMPANY = {"google", "alphabet", "mandiant"}
FILLER_OK_INTERNAL = {"of"}
GENERIC_UNI_RAW = """technical field develop lead drive collaborate practices strategies solutions reviews tools technologies languages project services management systems design
development analysis information support business environments environment level implement identify manage build create ensure maintain perform provide partner
key major complex large scale communication communicate stakeholders organization organizations process processes application applications""".split()

# ---- degree-line rule (FIXED per entry [10]): drop only lines that ARE the degree requirement
def _apos(t): return t.replace("’", "'").replace("‘", "'")
DEG_START = re.compile(r"^\W*(?:bachelor|master|ph\.?\s?d|doctorate|degree|associate)\b", re.I)
DEG_CONTAINS = re.compile(r"bachelor'?s? degree|master'?s? degree", re.I)
def is_degree_line(l):
    l = _apos(l); return bool(DEG_START.search(l) or DEG_CONTAINS.search(l))
def strip_degree(text): return "\n".join(l for l in text.split("\n") if not is_degree_line(l))

# ---- documented regexes for the headline numbers (same for every year; applied to the RAW section text, lower-cased, apostrophes normalised)
ADV = r"(?<![a-z])(?:master'?s?|ph\.?\s?d|doctorate|doctoral)(?![a-z])"   # 'advanced degree' is counted separately: it also occurs in 'N years of experience with an advanced degree' equivalence lines
REQ, PREF, RESP = "minimum_qualifications", "preferred_qualifications", "responsibilities"
METRICS = [  # key, description, regex, section
    ("bachelor_req", "'bachelor' in required", r"bachelor", REQ),
    ("adv_pref", "master/masters/PhD/doctorate/doctoral wording in preferred", ADV, PREF),
    ("adv_req", "same wording in required", ADV, REQ),
    ("advdeg_pref", "the phrase 'advanced degree' in preferred (often 'or N years of experience with an advanced degree')", r"advanced degree", PREF),
    ("cert_pref", "'certification' in preferred", r"certification", PREF),
    ("cert_req", "'certification' in required", r"certification", REQ),
    ("clearance_req", "'clearance' in required", r"clearance", REQ),
    ("travel_req", "'travel' in required", r"\btravel", REQ),
    ("python_req", "'python' in required", r"\bpython\b", REQ),
    ("cpp_req", "'c++' in required", r"c\+\+", REQ),
    ("java_req", "'java' (word) in required", r"\bjava\b", REQ),
    ("swdev_req", "'software development' in required", r"software development", REQ),
    ("proglang_req", "'programming language' in required", r"programming language", REQ),
    ("netforensics_req", "'network forensics' in required", r"network forensics", REQ),
    ("ir_req", "'incident response' in required", r"incident response", REQ),
    ("ir_pref", "'incident response' in preferred", r"incident response", PREF),
    ("malware_req", "'malware' in required", r"malware", REQ),
    ("cloud_req", "'cloud' (word) in required", r"\bcloud\b", REQ),
    ("cybersec_req", "'cybersecurity'/'cyber security' in required", r"cyber[\s-]?security", REQ),
    ("threatintel_pref", "'threat intelligence' in preferred", r"threat intelligence", PREF),
    ("swe_tpl_req", "software-engineer template: required has 'software development' AND ('programming language' OR 'data structures')", r"(?s)^(?=.*software development)(?=.*(?:programming language|data structures))", REQ),
    ("sec_tpl_req", "security-engineer template: required has 'security assessments' AND 'security protocols'", r"(?s)^(?=.*security assessments)(?=.*security protocols)", REQ),
    ("ai_ml_any", "'machine learning' or 'artificial intelligence' or 'AI' (word) in any section", r"machine learning|artificial intelligence|\bai\b|\bllms?\b", "any"),
]
METRIC = {m[0]: m for m in METRICS}
def rtext(r, sec):
    s = (r["sections"].get(REQ, "") + "\n" + r["sections"].get(PREF, "") + "\n" + r["sections"].get(RESP, "")) if sec == "any" else r["sections"].get(sec, "")
    return _apos(s).lower()
def has_metric(r, key): return re.search(METRIC[key][2], rtext(r, METRIC[key][3])) is not None

def norm_text(t):
    t = _apos(t).lower().replace("“", '"').replace("”", '"')
    t = re.sub(r"cyber[\s-]security", "cybersecurity", t)
    t = re.sub(r"'s\b", "", t)
    t = re.sub(r"(?<=[a-z0-9])-(?=[a-z0-9])", " ", t)
    return t
def stem(w):
    if len(w) > 4 and w.endswith("ies"): return w[:-3] + "y"
    if len(w) > 5 and w.endswith("sses"): return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is")): return w[:-1]
    return w
GENERIC_UNI = set(stem(w) for w in GENERIC_UNI_RAW)
def clauses(text):
    t = norm_text(text); out = []
    for part in re.split(r"[\n,;:()\[\]!?\"]|\.(?:\s|$)|\s[-–—]\s|\s/\s|&", t):
        toks = [x.strip(".'/") for x in re.findall(r"[a-z0-9][a-z0-9+#./']*", part)]
        toks = [x for x in toks if len(x) >= 2 or x == "c"]
        if toks: out.append(toks)
    return out
def ngrams(text):
    for toks in clauses(text):
        for n in (1, 2, 3):
            for i in range(len(toks) - n + 1):
                w = toks[i:i + n]
                if w[0] in STOP or w[-1] in STOP or w[0].isdigit() or w[-1].isdigit(): continue
                if any((x in STOP and x not in FILLER_OK_INTERNAL) or x.isdigit() for x in w[1:-1]): continue
                if any(x in COMPANY for x in w): continue
                if n == 1 and stem(w[0]) in GENERIC_UNI: continue
                yield tuple(stem(x) for x in w), " ".join(w)

_SHARDS = None
def load(year):
    global _SHARDS
    if _SHARDS is None:
        _SHARDS = g._load_state(REPO)[0]
        for y in _SHARDS:
            for r in _SHARDS[y].values():   # some postings lack a section: treat as empty text
                r["sections"] = {**{k: "" for k in ("about", REQ, PREF, RESP)}, **(r.get("sections") or {})}
    return _SHARDS[year]

def analyse(year):
    P = load(year); ids = sorted(P); N = len(ids)
    theme = {j: P[j]["theme"] for j in ids}; THEMES = sorted(set(theme.values())); TN = Counter(theme.values())
    surf = defaultdict(Counter); sets = {s: {} for s in SECS}; anyset = {}
    for j in ids:
        u = set()
        for s in SECS:
            st = set()
            for k, sf in ngrams(strip_degree(P[j]["sections"].get(s, ""))): st.add(k); surf[k][sf] += 1
            sets[s][j] = st; u |= st
        anyset[j] = u
    df_any = Counter(k for j in ids for k in anyset[j])
    cand = {k for k, c in df_any.items() if c >= MIN_DF}
    dropped_boiler = sorted(((k, df_any[k]) for k in cand if df_any[k] > BOILER * N), key=lambda x: -x[1])
    cand -= {k for k, _ in dropped_boiler}
    sub_of = defaultdict(list)
    for T in cand:
        if len(T) >= 2:
            for n in range(1, len(T)):
                for i in range(len(T) - n + 1): sub_of[T[i:i + n]].append(T)
    dropped_sub = []; keep = set(cand)
    for t in sorted(cand, key=lambda k: -len(k)):
        for T in sub_of.get(t, []):
            if T in cand and df_any[T] >= SUBSUME * df_any[t]: keep.discard(t); dropped_sub.append((t, T)); break
    label = {k: surf[k].most_common(1)[0][0] for k in keep}
    return dict(year=year, P=P, ids=ids, N=N, theme=theme, THEMES=THEMES, TN=TN, surf=surf, sets=sets, anyset=anyset, keep=keep,
                label=label, dropped_boiler=dropped_boiler, dropped_sub=dropped_sub, df_any=df_any)
def dfk(c, k, s, th=None, ids=None):
    S = c["anyset"] if s == "any" else c["sets"][s]
    return sum(1 for j in (ids if ids is not None else c["ids"]) if k in S[j] and (th is None or c["theme"][j] == th))
def mcount(c, key, th=None, ids=None):
    return sum(1 for j in (ids if ids is not None else c["ids"]) if (th is None or c["theme"][j] == th) and has_metric(c["P"][j], key))
def wk(d): return " W" if d < WEAK else ""
def cellf(c):
    ns = c["N"] < WEAK   # year total <30: counts only, no shares
    return lambda n, d: (f"{n}/{d}" if ns else (f"{n} ({100*n/d:.0f}%)" if d else "0"))

def maxyears(txt):
    v = [int(x) for x in re.findall(r"(\d{1,2})\+?\s*(?:or more\s*)?years", txt.lower())]
    return max(v) if v else None

def build_tables(c):
    year, P, ids, N, theme, THEMES, TN = c["year"], c["P"], c["ids"], c["N"], c["theme"], c["THEMES"], c["TN"]
    keep, label = c["keep"], c["label"]; cell = cellf(c)
    keys = sorted(keep, key=lambda k: label[k])
    df = lambda k, s, th=None: dfk(c, k, s, th)
    T = {k: {s: df(k, s) for s in SECS + ["any"]} for k in keys}
    L = []; A = L.append
    A(f"# C5 data-driven terms, {year} description-capture year (n = {N} postings)\n")
    if N < WEAK:
        A(f"**WEAK YEAR: n = {N} < 30 in total, so EVERY cell is weak. Counts only (n/denominator), no percentages, no share-based claim; descriptive use only.**\n")
    A("**Scope:** postings are only those Wayback archived. 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026). "
      f"This file covers the {year} capture year only. Denominators: all = {N}; " + ", ".join(f"{t} = {TN[t]}{wk(TN[t])}" for t in THEMES) +
      ". W = n<30 (weak). physical_corporate_security is NOT cybersecurity and is shown separately.\n")
    A("**Reading the counts:** a cell = postings whose text in that section contains the term / posting denominator. Terms come from phrase matching (heuristic, see c4_method.md and c5_method.md); "
      "a posting counts once per term; near-identical postings each count. Degree lines (lines that ARE the degree requirement) are removed before term extraction; degree wording is counted by documented regexes (Table 'Regex metrics').\n")
    def top(lst, sec, th=None, n=40):
        rows = [(df(k, sec, th), k) for k in lst]; rows = [r for r in rows if r[0]]
        rows.sort(key=lambda x: (-x[0], label[x[1]])); return rows[:n]
    n1 = min(40, 40)
    A(f"## Table 1. Top 40 terms overall (any of the 3 sections; denominator {N}) [phrase-term counts]\n")
    A("| # | term | any section | required | preferred | responsibilities |"); A("|---|---|---|---|---|---|")
    for i, (cc, k) in enumerate(top(keys, "any"), 1):
        A(f"| {i} | {label[k]} | {cell(cc, N)} | {cell(T[k][REQ], N)} | {cell(T[k][PREF], N)} | {cell(T[k][RESP], N)} |")
    A(f"\n## Table 1b. Top 40 PHRASES (2-3 words) overall (denominator {N}) [phrase-term counts]\n")
    A("| # | term | any section | required | preferred | responsibilities |"); A("|---|---|---|---|---|---|")
    for i, (cc, k) in enumerate(top([k for k in keys if len(k) >= 2], "any"), 1):
        A(f"| {i} | {label[k]} | {cell(cc, N)} | {cell(T[k][REQ], N)} | {cell(T[k][PREF], N)} | {cell(T[k][RESP], N)} |")
    tb = 2
    for s in SECS:
        A(f"\n## Table {tb}. Top 30 terms in {SECNAME[s].upper()} (denominator {N}) [phrase-term counts]\n"); tb += 1
        A("| # | term | in this section | any section |"); A("|---|---|---|---|")
        for i, (cc, k) in enumerate(top(keys, s, None, 30), 1): A(f"| {i} | {label[k]} | {cell(cc, N)} | {cell(T[k]['any'], N)} |")
    big = [t for t in THEMES if TN[t] >= WEAK]
    for th in big:
        for s in SECS:
            rest_n = N - TN[th]
            A(f"\n## Table {tb}. {th} (n = {TN[th]}): top 15 terms in {SECNAME[s].upper()} [phrase-term counts]\n"); tb += 1
            A(f"| # | term | in {th} | in all other themes (n={rest_n}) |"); A("|---|---|---|---|")
            for i, (cc, k) in enumerate(top(keys, s, th, 15), 1): A(f"| {i} | {label[k]} | {cell(cc, TN[th])} | {cell(df(k, s) - cc, rest_n)} |")
    A(f"\n## Table {tb}. Theme-distinctive terms (any section; in >=15% of the theme's postings and >= 5 postings; ranked by share in theme minus share elsewhere, pp)\n"); tb += 1
    if not big: A("No theme has n>=30 in this year: no theme-level ranking is given.\n")
    dist = {}
    for th in big:
        rest_n = N - TN[th]; rows = []
        for k in keys:
            cc = df(k, "any", th)
            if cc >= max(5, 0.15 * TN[th]): r = df(k, "any") - cc; rows.append((100 * cc / TN[th] - 100 * r / rest_n, cc, r, k))
        rows.sort(key=lambda x: (-x[0], label[x[3]])); dist[th] = rows[:12]
        A(f"**{th} (n = {TN[th]}; others n = {rest_n})**\n"); A("| term | in theme | elsewhere | diff (pp) |"); A("|---|---|---|---|")
        for d, cc, r, k in dist[th]: A(f"| {label[k]} | {cell(cc, TN[th])} | {cell(r, rest_n)} | {d:+.0f} |")
        A("")
    A(f"## Table {tb}. Weak themes (n<30, ANECDOTAL; no share should be generalised): top 10 terms, any section [phrase-term counts]\n"); tb += 1
    for th in [t for t in THEMES if TN[t] < WEAK]:
        note = " (physical/corporate security: NOT cybersecurity)" if th.startswith("physical") else ""
        A(f"**{th}, n = {TN[th]} W{note}**\n"); A("| term | any section | required | preferred | responsibilities |"); A("|---|---|---|---|---|")
        for cc, k in top(keys, "any", th, 10):
            A(f"| {label[k]} | {cellf(dict(N=0))(cc, TN[th])} | {cellf(dict(N=0))(df(k, REQ, th), TN[th])} | {cellf(dict(N=0))(df(k, PREF, th), TN[th])} | {cellf(dict(N=0))(df(k, RESP, th), TN[th])} |")
        A("")
    groups = [("ALL", ids)] + [(t, [j for j in ids if theme[j] == t]) for t in THEMES]
    # regex metrics
    A(f"## Table {tb}. Regex metrics (documented regexes, identical for every year; applied to the raw section text, lower-cased; denominators = postings in the column)\n"); tb += 1
    A("| metric (regex on section) | " + " | ".join(f"{n}{wk(len(s))} (n={len(s)})" for n, s in groups) + " |"); A("|---|" + "---|" * len(groups))
    for key, desc, rx, sec in METRICS:
        A(f"| {desc}: `{rx}` | " + " | ".join(cell(mcount(c, key, None, s), len(s)) for n, s in groups) + " |")
    # years/degree
    A(f"\n## Table {tb}. Stated years of experience (regex heuristic `(\\d{{1,2}})\\+?\\s*(?:or more\\s*)?years` on the required text; the HIGHEST figure per posting; a lone '1 year' is not matched; denominators = postings in the row)\n"); tb += 1
    buckets = [("none stated", lambda y: y is None), ("1-2", lambda y: y is not None and 1 <= y <= 2), ("3-4", lambda y: y is not None and 3 <= y <= 4), ("5-6", lambda y: y is not None and 5 <= y <= 6), ("7-9", lambda y: y is not None and 7 <= y <= 9), ("10+", lambda y: y is not None and y >= 10)]
    yrs = {j: maxyears(P[j]["sections"][REQ]) for j in ids}
    A("| group | n | " + " | ".join(b[0] for b in buckets) + " |"); A("|---|---|" + "---|" * len(buckets))
    for name, sel in groups: A(f"| {name}{wk(len(sel))} | {len(sel)} | " + " | ".join(str(sum(1 for j in sel if b[1](yrs[j]))) for b in buckets) + " |")
    A("\n(counts of postings; divide by the n column for shares" + ("; NO shares are to be quoted for this weak year" if N < WEAK else "") + ")\n")
    A("Degree-line fields named (lines that ARE the degree requirement, counted by regex; denominators = postings in the row):\n")
    A("| group | n | 'computer science' | 'engineering' | 'mathematics' | 'related' |"); A("|---|---|---|---|---|---|")
    def degtxt(j): return " ".join(l for l in (P[j]["sections"][REQ] + "\n" + P[j]["sections"][PREF]).split("\n") if is_degree_line(l)).lower()
    for name, sel in groups:
        A(f"| {name}{wk(len(sel))} | {len(sel)} | " + " | ".join(cell(sum(1 for j in sel if re.search(pat, degtxt(j))), len(sel)) for pat in (r"computer science", r"engineering", r"mathematic", r"related")) + " |")
    A(f"\n## Table {tb}. Section length (words, median) and duplicate text\n"); tb += 1
    def med(xs): xs = sorted(xs); return xs[len(xs) // 2] if xs else 0
    A("| group | n | required | preferred | responsibilities |"); A("|---|---|---|---|---|")
    for name, sel in groups: A(f"| {name}{wk(len(sel))} | {len(sel)} | " + " | ".join(str(med([len(P[j]['sections'][s].split()) for j in sel])) for s in SECS) + " |")
    A("\nPostings whose parsed section is EMPTY (parser found no text): " + ", ".join(f"{lab}: {sum(1 for j in ids if not P[j]['sections'][sk].strip())}/{N}" for lab, sk in (("about", "about"), ("required", REQ), ("preferred", PREF), ("responsibilities", RESP))) + ".")
    dup = Counter(P[j]["sections"][REQ].strip() + "||" + P[j]["sections"][RESP].strip() for j in ids)
    A(f"\nDistinct (required + responsibilities) texts: {len(dup)} of {N} postings; {sum(1 for x in dup.values() if x > 1)} texts appear more than once (largest group {max(dup.values())} postings). Distinct titles: {len({P[j]['title'] for j in ids})} of {N}. Repeated texts are counted once per posting in every table.\n")
    # reconciliation phrase-term vs regex
    A(f"## Table {tb}. Reconciliation: phrase-term count vs regex count for the same concept (ALL postings, denominator {N})\n"); tb += 1
    A("| concept | phrase-term count (section) | regex count | regex-only postings (job_id: context) | term-only postings |"); A("|---|---|---|---|---|")
    pairs = [("security clearance", "clearance_req", REQ), ("incident response", "ir_req", REQ), ("certifications", "cert_pref", PREF), ("certifications", "cert_req", REQ),
             ("python", "python_req", REQ), ("c++", "cpp_req", REQ), ("java", "java_req", REQ), ("network forensics", "netforensics_req", REQ), ("malware", "malware_req", REQ)]
    lab2k = {label[k]: k for k in keys}
    for term, mk, sec in pairs:
        k = lab2k.get(term)
        if k is None: A(f"| {term} | not retained | {mcount(c, mk)} | | |"); continue
        tset = {j for j in ids if k in c["sets"][sec][j]}; rset = {j for j in ids if has_metric(P[j], mk)}
        ro = []
        for j in sorted(rset - tset):
            txt = _apos(P[j]["sections"][sec]).lower(); m = re.search(METRIC[mk][2], txt); a = max(0, m.start() - 35)
            ro.append(f"{j}: ...{txt[a:m.end()+25]!r}")
        A(f"| {term} | {len(tset)} ({SHORT[sec]}) | {len(rset)} | " + ("; ".join(ro[:6]) + (f"; (+{len(ro)-6} more)" if len(ro) > 6 else "") if ro else "none") + f" | {', '.join(sorted(tset - rset)[:6]) or 'none'} |")
    A("\n(reasons phrase-term and regex counts can differ: the phrase term needs its words adjacent inside one clause after stemming and hyphen-splitting, and lines that are degree requirements are removed first; the regex runs on the raw section text. Headline numbers in findings say which method produced them.)\n")
    A(f"## Table {tb}. What the extraction dropped (see c4_method.md)\n")
    db, ds = c["dropped_boiler"], c["dropped_sub"]
    A(f"- Boilerplate rule (terms in >{int(BOILER*100)}% of the {N} postings, df>{BOILER*N:.0f}), applied AFTER the corrected degree-line rule: {len(db)} terms dropped" + (": " + "; ".join(f"{c['surf'][k].most_common(1)[0][0]} ({x})" for k, x in db[:25]) if db else "") + f". Highest remaining term share: {max(c['df_any'][k] for k in keep)}/{N}.")
    A(f"- Subsumed by a longer phrase (covers >= {int(SUBSUME*100)}% of the shorter term's postings): {len(ds)} terms. Retained terms after all rules: {len(keep)} (candidate threshold: >= {MIN_DF} postings).")
    return L, dict(keys=keys, T=T, dist=dist, yrs=yrs, groups=groups)

def qnorm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"'); t = re.sub(r"^\s*-\s+", "", t, flags=re.M)
    return re.sub(r"\s+", " ", t).strip().lower()
def verify_quotes(text, c):
    P, theme = c["P"], c["theme"]; bad, ok = [], 0
    for q, jid, th in re.findall(r'"([^"]{8,})"\s*\((\d{10,}),\s*([a-z_]+)\)', text):
        if jid not in P: bad.append((jid, "job_id not in this year's shard", q)); continue
        if len(q.split()) > 25: bad.append((jid, "over 25 words", q)); continue
        if qnorm(q) not in qnorm(P[jid]["description_text"]): bad.append((jid, "not verbatim", q)); continue
        if theme[jid] != th: bad.append((jid, f"theme is {theme[jid]}", q)); continue
        ok += 1
    return ok, bad
def resolve(text, c, ex):
    """[[term|section|theme]] phrase-term count; [[re:metric|theme]] regex count (theme optional); [[yrs:bucket|theme]] years bucket count."""
    N, TN = c["N"], c["TN"]; ns = N < WEAK
    cell = (lambda n, d: f"{n}/{d}") if ns else (lambda n, d: f"{n}/{d} ({100*n/d:.0f}%)" if d else f"{n}/{d}")
    def rep(m):
        parts = m.group(1).split("|")
        if parts[0].startswith("re:"):
            key = parts[0][3:]; th = parts[1] if len(parts) > 1 and parts[1] else None
            d = TN[th] if th else N; n = mcount(c, key, th); return cell(n, d) + wk(d) + " [regex]"
        if parts[0].startswith("yrs:"):
            lo, hi = parts[0][4:].split("-"); th = parts[1] if len(parts) > 1 and parts[1] else None
            sel = [j for j in c["ids"] if th is None or c["theme"][j] == th]; y = ex["yrs"]
            n = sum(1 for j in sel if y[j] is not None and int(lo) <= y[j] <= int(hi)); d = len(sel); return cell(n, d) + wk(d) + " [regex]"
        term, sec = parts[0], parts[1]; th = parts[2] if len(parts) > 2 and parts[2] else None
        ks = [k for k in ex["keys"] if c["label"][k] == term]
        if not ks: raise SystemExit(f"placeholder term not retained in {c['year']}: {term}")
        d = TN[th] if th else N; return cell(dfk(c, ks[0], sec, th), d) + wk(d) + " [phrase-term]"
    return re.sub(r"\[\[([^\]]+)\]\]", rep, text)

def run_year(year):
    c = analyse(year); L, ex = build_tables(c); N, P, ids, theme, THEMES, TN = c["N"], c["P"], c["ids"], c["theme"], c["THEMES"], c["TN"]
    atomic(D / f"c5_terms_{year}.md", "\n".join(L) + "\n")
    keys, label = ex["keys"], c["label"]
    js = {"year": year, "n": N, "theme_n": dict(TN), "rules": {"boiler": BOILER, "min_df": MIN_DF, "subsume": SUBSUME, "weak_n": WEAK, "degree_rule": "drop lines that START with bachelor/master/phd/doctorate/degree/associate or contain bachelor(')s degree / master(')s degree"},
          "terms": {label[k]: ex["T"][k] for k in keys},
          "terms_by_theme": {label[k]: {th: {s: dfk(c, k, s, th) for s in SECS + ["any"]} for th in THEMES} for k in keys},
          "regex_metrics": {m[0]: {gn: mcount(c, m[0], None, s) for gn, s in ex["groups"]} for m in METRICS},
          "dropped_boilerplate": [[c["surf"][k].most_common(1)[0][0], x] for k, x in c["dropped_boiler"]]}
    atomic(D / f"c5_terms_{year}.json", json.dumps(js, indent=1))
    rnd = random.Random(int(year)); sample = []
    for th in THEMES:
        pool = [j for j in ids if theme[j] == th]; sample += rnd.sample(pool, min(QUOTAS[year].get(th, 1), len(pool)))
    out = [f"# c5 sample for qualitative reading ({year}; seed {year}; {len(sample)} postings of {N}); 'about' cut to 250 chars\n"]
    for j in sample:
        r = P[j]; out.append(f"=== {j} | {theme[j]} | {r['title']} | capture {r['capture_timestamp']}\nABOUT: {r['sections']['about'][:250]}...\nMIN:\n{r['sections'][REQ]}\nPREF:\n{r['sections'][PREF]}\nRESP:\n{r['sections'][RESP]}\n")
    atomic(D / f"c5_sample_{year}.txt", "\n".join(out))
    report = [f"year {year}: n={N} themes={dict(TN)} terms kept={len(keys)} boiler dropped={len(c['dropped_boiler'])} subsumed={len(c['dropped_sub'])}", f"sample: {[(j, theme[j]) for j in sample]}"]
    nar = D / f"c5_narrative_{year}.md"; qual = D / f"c5_qualitative_{year}.md"
    for p in (nar, qual):
        if p.exists():
            ok, bad = verify_quotes(p.read_text(), c); report.append(f"{p.name}: {ok} quotes verified verbatim (<=25 words, right job_id and theme); problems: {bad or 'none'}")
            if bad: atomic(D / f"c5_quote_check_{year}.txt", "\n".join(report) + "\n"); raise SystemExit("QUOTE PROBLEMS " + repr(bad))
        else: report.append(f"{p.name}: not written yet")
    if nar.exists():
        joined = "\n".join(L)
        def block(title):
            m = re.search(r"(## Table \d+\. " + re.escape(title) + r".*?)(?=\n## Table|\Z)", joined, re.S); return m.group(1) if m else ""
        txt = resolve(nar.read_text(), c, ex)
        for tag, title in (("TOP40", "Top 40 terms overall"), ("DISTINCTIVE", "Theme-distinctive terms"), ("YEARS", "Stated years"), ("REGEX", "Regex metrics"), ("RECON", "Reconciliation")):
            txt = txt.replace("{{" + tag + "}}", block(title))
        if qual.exists(): txt += "\n\n## Qualitative notes (what the term counts miss)\n\n" + qual.read_text().split("\n", 1)[1]
        (D / "findings").mkdir(exist_ok=True); atomic(D / "findings" / f"{year}.md", txt); report.append(f"findings/{year}.md written")
    atomic(D / f"c5_quote_check_{year}.txt", "\n".join(report) + "\n"); print("\n".join(report))
    return c, ex

# ------------------------------------------------------------------ drift
def run_drift():
    YS = ["2024", "2025", "2026"]; C = {y: analyse(y) for y in YS}
    PAIRS = [("2024", "2025"), ("2025", "2026"), ("2024", "2026")]
    L = []; A = L.append
    A("# C5 drift: wording changes 2024 -> 2025 -> 2026 (description-capture years)\n")
    A("**Scope and limits.** Postings are only those Wayback archived; each year's postings are the ones archived with a new-format page in that year, so the years are NOT random samples of Google's security roles and their theme mix differs. "
      "2019-2022 postings are title-based only (no recoverable descriptions); descriptions start mid-2023. **2023 (n = 26) is weak and is NOT compared.** Text is a snapshot at capture date; causes are inference and none is claimed. Term counts are phrase matching (heuristic); regex rows are documented regexes (c4_years.py).\n")
    A("**Rule (entry [10]).** A group is compared only if it has n>=30 in EVERY year of the comparison. A difference is listed only if it is >= 10 percentage points AND the posting count behind the higher share is >= 8 (my reading of '>= 8 postings'; counts are printed so any other reading can be applied). "
      "Shares are with denominators. Many terms are tested (counts below), so some listed differences will arise by chance; treat the list as candidates to read, not as proven change.\n")
    A("### Group sizes and theme mix\n"); A("| year | ALL | security_engineering | threat_intel_and_response | sales_and_consulting | other_security | physical_corporate_security |"); A("|---|---|---|---|---|---|---|")
    ths = ["security_engineering", "threat_intel_and_response", "sales_and_consulting", "other_security", "physical_corporate_security"]
    for y in YS: A(f"| {y} | {C[y]['N']} | " + " | ".join(f"{C[y]['TN'][t]}{wk(C[y]['TN'][t])}" for t in ths) + " |")
    A("\nGroups compared: **ALL** (n = " + ", ".join(str(C[y]['N']) for y in YS) + ") and **security_engineering** (n = " + ", ".join(str(C[y]['TN']['security_engineering']) for y in YS) + "). "
      "**threat_intel_and_response is NOT compared** (n = " + ", ".join(str(C[y]['TN']['threat_intel_and_response']) for y in YS) + "; 2024 and 2026 are below 30, W); only 2025 has n>=30 for it. sales_and_consulting (n = " + ", ".join(str(C[y]['TN']['sales_and_consulting']) for y in YS) + ") is also below 30 in 2024 and 2026. "
      "Because the theme mix changes (the ALL level mixes different proportions of engineering, threat and sales roles), an ALL-level difference may reflect the archive's mix rather than a change in wording; the security_engineering comparison is the like-for-like one.\n")
    def dedup_ids(c, ids):
        seen, out = set(), []
        for j in ids:
            key = c["P"][j]["sections"][REQ].strip() + "||" + c["P"][j]["sections"][RESP].strip()
            if key not in seen: seen.add(key); out.append(j)
        return out
    allkeys = set().union(*[C[y]["keep"] for y in YS])
    lab = {}
    for k in allkeys:
        best = max(YS, key=lambda y: C[y]["df_any"].get(k, 0)); lab[k] = C[best]["surf"][k].most_common(1)[0][0] if C[best]["surf"][k] else " ".join(k)
    summary = {}
    for gname in ("ALL", "security_engineering"):
        gids = {y: [j for j in C[y]["ids"] if gname == "ALL" or C[y]["theme"][j] == gname] for y in YS}
        gd = {y: dedup_ids(C[y], gids[y]) for y in YS}
        A(f"## Group: {gname} (n = " + ", ".join(f"{y}: {len(gids[y])}" for y in YS) + "; distinct-text postings " + ", ".join(f"{y}: {len(gd[y])}" for y in YS) + ")\n")
        rows = []; tested = 0; stable = []
        for k in sorted(allkeys, key=lambda k: lab[k]):
            for sc in ("any", REQ, PREF, RESP):
                cnt = {y: dfk(C[y], k, sc, None, gids[y]) for y in YS}
                if max(cnt.values()) < 5: continue
                tested += 1
                sh = {y: 100 * cnt[y] / len(gids[y]) for y in YS}
                fl = []
                for a, b in PAIRS:
                    d = sh[b] - sh[a]; hi = cnt[b] if d > 0 else cnt[a]
                    if abs(d) >= 10 and hi >= 8:
                        dd = {y: 100 * dfk(C[y], k, sc, None, gd[y]) / len(gd[y]) for y in (a, b)}
                        fl.append((a, b, d, dd[b] - dd[a]))
                if fl: rows.append((max(abs(f[2]) for f in fl), lab[k], sc, cnt, sh, fl))
                elif sc == "any" and max(sh.values()) >= 20 and max(sh.values()) - min(sh.values()) < 5: stable.append((max(sh.values()), lab[k], cnt, sh))
        rows.sort(key=lambda r: (-r[0], r[1])); summary[gname] = (tested, len(rows))
        A(f"Terms x sections tested (a term must reach >=5 postings in some year): {tested}. Listed (>=10 pp and >=8 postings in at least one pair): {len(rows)}; shown: top 45 by size of difference.\n")
        A("| term | section | " + " | ".join(f"{y} (n={len(gids[y])})" for y in YS) + " | flagged pairs: change in pp [same on distinct-text postings] |"); A("|---|---|---|---|---|---|")
        for _, l, sc, cnt, sh, fl in rows[:45]:
            A(f"| {l} | {SHORT[sc]} | " + " | ".join(f"{cnt[y]}/{len(gids[y])} ({sh[y]:.0f}%)" for y in YS) + " | " + "; ".join(f"{a}->{b}: {d:+.0f} [{dd:+.0f}]" for a, b, d, dd in fl) + " |")
        A("")
        # regex metrics
        A(f"**Regex metrics, {gname}** (documented regexes; * = meets both thresholds in at least one pair)\n"); A("| metric | " + " | ".join(f"{y} (n={len(gids[y])})" for y in YS) + " | flagged pairs (pp) |"); A("|---|---|---|---|---|---|")
        for key, desc, rx, sec in METRICS:
            cnt = {y: mcount(C[y], key, None, gids[y]) for y in YS}; sh = {y: 100 * cnt[y] / len(gids[y]) for y in YS}; fl = []
            for a, b in PAIRS:
                d = sh[b] - sh[a]; hi = cnt[b] if d > 0 else cnt[a]
                if abs(d) >= 10 and hi >= 8: fl.append(f"{a}->{b}: {d:+.0f}")
            A(f"| {desc}{' *' if fl else ''} | " + " | ".join(f"{cnt[y]}/{len(gids[y])} ({sh[y]:.0f}%)" for y in YS) + " | " + ("; ".join(fl) or "-") + " |")
        A("")
        stable.sort(key=lambda r: -r[0])
        A(f"**Stayed the same, {gname}** (term in >=20% of postings in at least one year, any section, and highest minus lowest share across the three years < 5 pp; top 25)\n")
        A("| term | " + " | ".join(f"{y}" for y in YS) + " |"); A("|---|---|---|---|")
        for _, l, cnt, sh in stable[:25]: A(f"| {l} | " + " | ".join(f"{cnt[y]}/{len(gids[y])} ({sh[y]:.0f}%)" for y in YS) + " |")
        A("")
    notes = D / "c5_drift_notes.md"
    if notes.exists():
        allP = {}; allT = {}
        for yy in ("2023", "2024", "2025", "2026"):
            for j, r in load(yy).items(): allP[j] = r; allT[j] = r["theme"]
        ok, bad = verify_quotes(notes.read_text(), dict(P=allP, theme=allT))
        if bad: raise SystemExit("DRIFT NOTE QUOTE PROBLEMS " + repr(bad))
        print(f"c5_drift_notes.md: {ok} quotes verified verbatim")
        A("## Reading of the tables (hand-written after reading the postings behind the flagged terms; no causal claims)\n"); A(notes.read_text())
    atomic(D / "c5_drift.md", "\n".join(L) + "\n"); print("drift written", summary)

if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "all"
    todo = ["2025", "2024", "2026", "2023", "drift"] if a == "all" else [a]
    for t in todo:
        run_drift() if t == "drift" else run_year(t)
