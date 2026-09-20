"""C4 pilot, 2025 description-capture year. OFFLINE (no network). Regenerates every number in
c4_terms_2025.md / c4_terms_2025.json / c4_sample_2025.txt / findings/2025.md (narrative files are hand-written;
[[term|section(|theme)]] placeholders in them are resolved from the data, and every quote is verified verbatim).
Run:  ../no-github-remote/web-scrap/.venv/bin/python3 c4_pilot_2025.py
Scope: postings first seen 2019-2022 are title-based only; descriptions cover postings archived from mid-2023."""
import sys, os, re, json, random
from pathlib import Path
from collections import Counter, defaultdict
sys.path.insert(0, "../no-github-remote/web-scrap")
from plugins.job_search import wayback_google_details as g
D = Path("./tracks/gate/career-mapping/google-jd")
REPO = Path("../no-github-remote/scraper-data")
YEAR = "2025"
SECS = ["minimum_qualifications", "preferred_qualifications", "responsibilities"]
SECNAME = {"minimum_qualifications": "required (minimum)", "preferred_qualifications": "preferred", "responsibilities": "responsibilities", "any": "any section"}
BOILER = 0.90       # drop terms in more than 90% of postings
MIN_DF = 5          # candidate needs >= 5 postings (any section)
SUBSUME = 0.80      # drop shorter term if a longer phrase containing it covers >= 80% of its postings
WEAK = 30
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
COMPANY = {"google", "alphabet", "mandiant"}   # company names dropped from terms
FILLER_OK_INTERNAL = {"of"}
# Generic single words dropped as UNIGRAMS only (phrases containing them stay). Chosen after inspecting the first-pass top list (kept in c4_method.md).
GENERIC_UNI_RAW = """technical field develop lead drive collaborate practices strategies solutions reviews tools technologies languages project services management systems design
development analysis information support business environments environment level implement identify manage build create ensure maintain perform provide partner
key major complex large scale communication communicate stakeholders organization organizations process processes application applications""".split()
DEGREE_RE = re.compile(r"\b(bachelor|master|ph\.?d|degree|doctorate)\b", re.I)
def strip_degree(text):
    return "\n".join(l for l in text.split("\n") if not DEGREE_RE.search(l))

def norm_text(t):
    t = t.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"cyber[\s-]security", "cybersecurity", t)
    t = re.sub(r"'s\b", "", t)
    t = re.sub(r"(?<=[a-z0-9])-(?=[a-z0-9])", " ", t)
    return t
def stem(w):
    if len(w) > 4 and w.endswith("ies"): return w[:-3] + "y"
    if len(w) > 5 and w.endswith("sses"): return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is")): return w[:-1]
    return w
GENERIC_UNI = set()
def _init_generic():
    GENERIC_UNI.update(stem(w) for w in GENERIC_UNI_RAW)
def clauses(text):
    t = norm_text(text)
    out = []
    for part in re.split(r"[\n,;:()\[\]!?\"]|\.(?:\s|$)|\s[-–—]\s|\s/\s|&", t):
        toks = [x.strip(".'/") for x in re.findall(r"[a-z0-9][a-z0-9+#./']*", part)]
        toks = [x for x in toks if len(x) >= 2 or x == "c"]
        if toks: out.append(toks)
    return out
def ngrams(text):
    """yield (stemmed_tuple, surface_string) for valid 1-3-grams"""
    for toks in clauses(text):
        for n in (1, 2, 3):
            for i in range(len(toks) - n + 1):
                w = toks[i:i + n]
                if w[0] in STOP or w[-1] in STOP or w[0].isdigit() or w[-1].isdigit(): continue
                if any((x in STOP and x not in FILLER_OK_INTERNAL) or x.isdigit() for x in w[1:-1]): continue
                if any(x in COMPANY for x in w): continue
                if n == 1 and stem(w[0]) in GENERIC_UNI: continue
                yield tuple(stem(x) for x in w), " ".join(w)

def load():
    shards, ledger = g._load_state(REPO)
    return shards[YEAR]
def main():
    _init_generic()
    P = load(); ids = sorted(P); N = len(ids)
    assert N == 194, N
    theme = {j: P[j]["theme"] for j in ids}
    THEMES = sorted(set(theme.values())); TN = Counter(theme.values())
    surf = defaultdict(Counter); sets = {s: {} for s in SECS}; anyset = {}
    for j in ids:
        u = set()
        for s in SECS:
            st = set()
            for k, sf in ngrams(strip_degree(P[j]["sections"].get(s, ""))):
                st.add(k); surf[k][sf] += 1
            sets[s][j] = st; u |= st
        anyset[j] = u
    df_any = Counter(k for j in ids for k in anyset[j])
    cand = {k for k, c in df_any.items() if c >= MIN_DF}
    dropped_boiler = sorted(((k, df_any[k]) for k in cand if df_any[k] > BOILER * N), key=lambda x: -x[1])
    cand -= {k for k, _ in dropped_boiler}
    # subsumption
    sub_of = defaultdict(list)
    for T in cand:
        if len(T) >= 2:
            for n in range(1, len(T)):
                for i in range(len(T) - n + 1): sub_of[T[i:i + n]].append(T)
    dropped_sub = []
    keep = set(cand)
    for t in sorted(cand, key=lambda k: -len(k)):
        for T in sub_of.get(t, []):
            if T in cand and df_any[T] >= SUBSUME * df_any[t]:
                keep.discard(t); dropped_sub.append((t, T)); break
    # (compare against candidates, not survivors: chains collapse to the longest phrase)
    label = {k: surf[k].most_common(1)[0][0] for k in keep}
    def df(k, s, th=None):
        S = anyset if s == "any" else sets[s]
        return sum(1 for j in ids if k in S[j] and (th is None or theme[j] == th))
    T = {k: {s: df(k, s) for s in SECS + ["any"]} for k in keep}
    def cell(n, d): return f"{n} ({100*n/d:.0f}%)" if d else "0"
    def wk(d): return " W" if d < WEAK else ""
    L = []; A = L.append
    A(f"# C4 pilot: data-driven terms, {YEAR} description-capture year (n = {N} postings)\n")
    A("**Scope:** postings are only those Wayback archived. 2019-2022 postings are title-based only; descriptions cover postings archived from mid-2023 (capture years 2023-2026). This file covers the 2025 capture year only. "
      "Denominators: all = 194; " + ", ".join(f"{t} = {TN[t]}{wk(TN[t])}" for t in THEMES) + ". W = n<30 (weak). physical_corporate_security is NOT cybersecurity and is shown separately (its cell is weak).\n")
    A("**Reading the counts:** a cell 'n (p%)' = postings whose text in that section contains the term / posting denominator. Extraction is phrase matching on text (heuristic, see c4_method.md); a posting counts once per term; near-identical postings (same job in several locations) each count.\n")
    def top(lst_keys, sec, th=None, n=40, ranker=None):
        rows = []
        for k in lst_keys:
            c = df(k, sec, th)
            if c: rows.append((c, k))
        rows.sort(key=lambda x: (-x[0], label[x[1]]))
        return rows[:n]
    keys = sorted(keep, key=lambda k: label[k])
    # Table 1 overall
    A(f"## Table 1. Top 40 terms overall (any of the 3 sections; denominator {N})\n")
    A("| # | term | any section | required | preferred | responsibilities |"); A("|---|---|---|---|---|---|")
    for i, (c, k) in enumerate(top(keys, "any", None, 40), 1):
        A(f"| {i} | {label[k]} | {cell(c, N)} | {cell(T[k]['minimum_qualifications'], N)} | {cell(T[k]['preferred_qualifications'], N)} | {cell(T[k]['responsibilities'], N)} |")
    A(f"\n## Table 1b. Top 40 PHRASES (2-3 words) overall (denominator {N})\n")
    A("| # | term | any section | required | preferred | responsibilities |"); A("|---|---|---|---|---|---|")
    for i, (c, k) in enumerate(top([k for k in keys if len(k) >= 2], "any", None, 40), 1):
        A(f"| {i} | {label[k]} | {cell(c, N)} | {cell(T[k]['minimum_qualifications'], N)} | {cell(T[k]['preferred_qualifications'], N)} | {cell(T[k]['responsibilities'], N)} |")
    # Table 2 by section
    for si, s in enumerate(SECS, 2):
        A(f"\n## Table {si}. Top 30 terms in {SECNAME[s].upper()} (denominator {N})\n")
        A("| # | term | in this section | any section |"); A("|---|---|---|---|")
        for i, (c, k) in enumerate(top(keys, s, None, 30), 1):
            A(f"| {i} | {label[k]} | {cell(c, N)} | {cell(T[k]['any'], N)} |")
    # Table 5.. per theme with n>=30
    tbl = 5; big = [t for t in THEMES if TN[t] >= WEAK]
    theme_top = {}
    for th in big:
        for s in SECS:
            rest_n = N - TN[th]
            A(f"\n## Table {tbl}. {th} (n = {TN[th]}): top 15 terms in {SECNAME[s].upper()}\n"); tbl += 1
            A(f"| # | term | in {th} | in all other themes (n={rest_n}) |"); A("|---|---|---|---|")
            rows = top(keys, s, th, 15); theme_top[(th, s)] = [(label[k], c) for c, k in rows]
            for i, (c, k) in enumerate(rows, 1):
                rest = df(k, s, None) - c
                A(f"| {i} | {label[k]} | {cell(c, TN[th])} | {cell(rest, rest_n)} |")
    # distinctive
    A(f"\n## Table {tbl}. Most theme-distinctive terms (any section; term in >=15% of the theme's postings and >= 5 postings; ranked by share in theme minus share elsewhere, percentage points)\n"); tbl += 1
    dist = {}
    for th in big:
        rest_n = N - TN[th]; rows = []
        for k in keys:
            c = df(k, "any", th)
            if c >= max(5, 0.15 * TN[th]):
                r = df(k, "any", None) - c; rows.append((100 * c / TN[th] - 100 * r / rest_n, c, r, k))
        rows.sort(key=lambda x: (-x[0], label[x[3]])); dist[th] = rows[:12]
        A(f"**{th} (n = {TN[th]}; others n = {rest_n})**\n"); A("| term | in theme | elsewhere | diff (pp) |"); A("|---|---|---|---|")
        for d, c, r, k in dist[th]: A(f"| {label[k]} | {cell(c, TN[th])} | {cell(r, rest_n)} | {d:+.0f} |")
        A("")
    # weak themes
    A(f"## Table {tbl}. Weak themes (n<30, ANECDOTAL, no share should be generalised): top 10 terms, any section\n"); tbl += 1
    for th in [t for t in THEMES if TN[t] < WEAK]:
        note = " (physical/corporate security: NOT cybersecurity)" if th.startswith("physical") else ""
        A(f"**{th}, n = {TN[th]} W{note}**\n"); A("| term | any section | required | preferred | responsibilities |"); A("|---|---|---|---|---|")
        for c, k in top(keys, "any", th, 10):
            A(f"| {label[k]} | {cell(c, TN[th])} | {cell(df(k,'minimum_qualifications',th), TN[th])} | {cell(df(k,'preferred_qualifications',th), TN[th])} | {cell(df(k,'responsibilities',th), TN[th])} |")
        A("")
    # years / degree
    A(f"## Table {tbl}. Stated years of experience and degree level (regex heuristic on the text; denominators = postings in the row)\n"); tbl += 1
    def maxyears(txt):
        v = [int(x) for x in re.findall(r"(\d{1,2})\+?\s*(?:or more\s*)?years", txt.lower())]
        return max(v) if v else None
    buckets = [("none stated", lambda y: y is None), ("1-2", lambda y: y is not None and 1 <= y <= 2), ("3-4", lambda y: y is not None and 3 <= y <= 4), ("5-6", lambda y: y is not None and 5 <= y <= 6), ("7-9", lambda y: y is not None and 7 <= y <= 9), ("10+", lambda y: y is not None and y >= 10)]
    yrs = {j: maxyears(P[j]["sections"]["minimum_qualifications"]) for j in ids}
    A("Highest 'N years' figure in the MINIMUM qualifications:\n"); A("| group | n | " + " | ".join(b[0] for b in buckets) + " |"); A("|---|---|" + "---|" * len(buckets))
    for name, sel in [("ALL", ids)] + [(t, [j for j in ids if theme[j] == t]) for t in THEMES]:
        A(f"| {name}{wk(len(sel))} | {len(sel)} | " + " | ".join(str(sum(1 for j in sel if b[1](yrs[j]))) for b in buckets) + " |")
    A("\nDegree wording:\n"); A("| group | n | 'bachelor' in required | 'master' or 'phd' or 'doctor' or 'advanced degree' in preferred | same in required |"); A("|---|---|---|---|---|")
    adv = re.compile(r"master|ph\.?d|doctor|advanced degree")
    for name, sel in [("ALL", ids)] + [(t, [j for j in ids if theme[j] == t]) for t in THEMES]:
        A(f"| {name}{wk(len(sel))} | {len(sel)} | {cell(sum(1 for j in sel if 'bachelor' in P[j]['sections']['minimum_qualifications'].lower()), len(sel))} | {cell(sum(1 for j in sel if adv.search(P[j]['sections']['preferred_qualifications'].lower())), len(sel))} | {cell(sum(1 for j in sel if adv.search(P[j]['sections']['minimum_qualifications'].lower())), len(sel))} |")
    A("\nDegree-line fields named (the degree lines were removed from term extraction and are counted here by regex; denominators = postings in the row):\n")
    A("| group | n | 'computer science' | 'engineering' | 'mathematics' | 'related' field/experience wording |"); A("|---|---|---|---|---|---|")
    def degtxt(j): return " ".join(l for l in (P[j]["sections"]["minimum_qualifications"] + "\n" + P[j]["sections"]["preferred_qualifications"]).split("\n") if DEGREE_RE.search(l)).lower()
    for name, sel in [("ALL", ids)] + [(t, [j for j in ids if theme[j] == t]) for t in THEMES]:
        A(f"| {name}{wk(len(sel))} | {len(sel)} | " + " | ".join(cell(sum(1 for j in sel if re.search(pat, degtxt(j))), len(sel)) for pat in (r"computer science", r"engineering", r"mathematic", r"related")) + " |")
    # length + duplicates
    A(f"\n## Table {tbl}. Section length (words, median) and duplicate text\n"); tbl += 1
    def med(xs): xs = sorted(xs); return xs[len(xs) // 2] if xs else 0
    A("| group | n | required | preferred | responsibilities |"); A("|---|---|---|---|---|")
    for name, sel in [("ALL", ids)] + [(t, [j for j in ids if theme[j] == t]) for t in THEMES]:
        A(f"| {name}{wk(len(sel))} | {len(sel)} | " + " | ".join(str(med([len(P[j]['sections'][s].split()) for j in sel])) for s in SECS) + " |")
    dup = Counter(P[j]["sections"]["minimum_qualifications"].strip() + "||" + P[j]["sections"]["responsibilities"].strip() for j in ids)
    A(f"\nDistinct (required + responsibilities) texts: {len(dup)} of {N} postings; {sum(1 for c in dup.values() if c > 1)} texts appear more than once (largest group {max(dup.values())} postings). Distinct titles: {len({P[j]['title'] for j in ids})} of {N}. Repeated texts are counted once per posting in every table above.\n")
    A("## Table " + str(tbl) + ". What the extraction dropped (see c4_method.md)\n")
    A(f"- Boilerplate: {len(dropped_boiler)} candidate terms in >{int(BOILER*100)}% of the {N} postings (df>{BOILER*N:.0f}): " + "; ".join(f"{surf[k].most_common(1)[0][0]} ({c})" for k, c in dropped_boiler[:25]) + ("; ..." if len(dropped_boiler) > 25 else ""))
    A(f"- Subsumed by a longer phrase (longer phrase covers >= {int(SUBSUME*100)}% of the shorter term's postings): {len(dropped_sub)} terms. Retained terms after all rules: {len(keep)} (candidate threshold: >= {MIN_DF} postings).")
    atomic(D / "c4_terms_2025.md", "\n".join(L) + "\n")
    js = {"year": YEAR, "n": N, "theme_n": dict(TN), "rules": {"boiler": BOILER, "min_df": MIN_DF, "subsume": SUBSUME, "weak_n": WEAK},
          "terms": {label[k]: T[k] for k in keys},
          "terms_by_theme": {label[k]: {th: {s: df(k, s, th) for s in SECS + ["any"]} for th in THEMES} for k in keys},
          "dropped_boilerplate": [[surf[k].most_common(1)[0][0], c] for k, c in dropped_boiler]}
    atomic(D / "c4_terms_2025.json", json.dumps(js, indent=1))
    # ---- qualitative sample dump
    rnd = random.Random(2025); quota = {"security_engineering": 4, "threat_intel_and_response": 4, "sales_and_consulting": 3, "other_security": 2, "physical_corporate_security": 2}
    sample = []
    for th in THEMES:
        pool = [j for j in ids if theme[j] == th]; sample += rnd.sample(pool, min(quota.get(th, 2), len(pool)))
    out = [f"# c4 sample for qualitative reading (seed 2025, {len(sample)} postings of {N}); 'about' cut to 350 chars\n"]
    for j in sample:
        r = P[j]; out.append(f"=== {j} | {theme[j]} | {r['title']} | capture {r['capture_timestamp']}\nABOUT: {r['sections']['about'][:350]}...\nMIN:\n{r['sections']['minimum_qualifications']}\nPREF:\n{r['sections']['preferred_qualifications']}\nRESP:\n{r['sections']['responsibilities']}\n")
    atomic(D / "c4_sample_2025.txt", "\n".join(out))
    # ---- context for placeholders / verification
    ctx = dict(P=P, ids=ids, theme=theme, TN=TN, N=N, keys=keys, label=label, df=df, T=T, surf=surf, sets=sets, anyset=anyset, top=top, theme_top=theme_top, dist=dist, L=L, yrs=yrs)
    build_findings(ctx)
    print("N", N, "themes", dict(TN), "terms kept", len(keep), "dropped boiler", len(dropped_boiler), "dropped subsumed", len(dropped_sub))
    print("sample:", [(j, theme[j]) for j in sample])

def qnorm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"^\s*-\s+", "", t, flags=re.M)
    return re.sub(r"\s+", " ", t).strip().lower()
def verify_quotes(text, P, theme, name):
    bad, ok = [], 0
    for q, jid, th in re.findall(r'"([^"]{8,})"\s*\((\d{10,}),\s*([a-z_]+)\)', text):
        full = qnorm(P[jid]["description_text"]) if jid in P else None
        if full is None: bad.append((jid, "job_id not in 2025 shard", q)); continue
        if len(q.split()) > 25: bad.append((jid, "over 25 words", q)); continue
        if qnorm(q) not in full: bad.append((jid, "not verbatim", q)); continue
        if theme[jid] != th: bad.append((jid, f"theme is {theme[jid]}", q)); continue
        ok += 1
    return ok, bad
def resolve(text, ctx):
    def rep(m):
        parts = m.group(1).split("|"); term, sec = parts[0], parts[1]; th = parts[2] if len(parts) > 2 else None
        ks = [k for k in ctx["keys"] if ctx["label"][k] == term]
        if not ks: raise SystemExit(f"placeholder term not retained: {term}")
        d = ctx["TN"][th] if th else ctx["N"]; c = ctx["df"](ks[0], sec, th)
        return f"{c}/{d} ({100*c/d:.0f}%)" + (" W" if d < WEAK else "")
    return re.sub(r"\[\[([^\]]+)\]\]", rep, text)
def build_findings(ctx):
    P, theme = ctx["P"], ctx["theme"]; report = []
    ok_all = 0
    for fn in ("c4_narrative_2025.md", "c4_qualitative_2025.md"):
        p = D / fn
        if not p.exists(): report.append(f"{fn}: not written yet"); continue
        raw = p.read_text(); ok, bad = verify_quotes(raw, P, theme, fn); ok_all += ok
        report.append(f"{fn}: {ok} quotes verified verbatim; problems: {bad if bad else 'none'}")
        if bad: raise SystemExit("QUOTE PROBLEMS: " + repr(bad))
        if fn == "c4_qualitative_2025.md": atomic(D / fn.replace(".md", "_resolved.md"), resolve(raw, ctx)) if "[[" in raw else None
    nar = D / "c4_narrative_2025.md"
    if nar.exists():
        txt = resolve(nar.read_text(), ctx)
        L = ctx["L"]; joined = "\n".join(L)
        def block(title):  # extract one table from the terms md
            m = re.search(r"(## Table \d+\. " + re.escape(title) + r".*?)(?=\n## Table|\Z)", joined, re.S); return m.group(1) if m else ""
        txt = txt.replace("{{TOP40}}", block("Top 40 terms overall")).replace("{{DISTINCTIVE}}", block("Most theme-distinctive terms")).replace("{{YEARS}}", block("Stated years"))
        (D / "findings").mkdir(exist_ok=True); atomic(D / "findings" / "2025.md", txt)
        report.append("findings/2025.md written")
    atomic(D / "c4_quote_check.txt", "\n".join(report) + "\n"); print("\n".join(report))
if __name__ == "__main__":
    main()
