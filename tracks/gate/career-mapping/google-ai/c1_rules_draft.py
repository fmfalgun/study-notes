"""SCRATCH (checkpoint 1): proposed CORE-AI / DATA-SCIENCE / FAMILY rules. Not a deliverable."""
import re

def _strip(t):
    t = re.sub(r"\bquantum ai\b", " ", t, flags=re.I)          # Google Quantum AI = quantum-computing org, not AI/ML
    ds = bool(re.search(r"\bdata scien\w+", t, re.I))
    return re.sub(r"\bdata scien\w+", " ", t, flags=re.I), ds

_PHRASE = re.compile(r"\b(machine learning|artificial intelligence|deep learning|reinforcement learning|computer vision|"
                     r"language models?|generative|neural|gemini|gemma|notebooklm|bard|natural language|agentic|"
                     r"autonomous agents?|agent platform|tensor processing|vertex|tpus?|aiml|genai|mlops|aimachine)\b", re.I)
_ACRO = re.compile(r"\b(AI|ML|LLMs?|NLP|GenAI)\b")               # case-sensitive on the re-cased title

def classify(title):
    """-> (core_ai: bool, data_science: bool)"""
    stripped, ds = _strip(title)
    core = bool(_PHRASE.search(stripped) or _ACRO.search(stripped))
    return core, ds

FAMILIES = [  # first match wins
 ("ai_safety_responsible", r"responsible ai|ai safety|safety.*\bai\b|\bai\b.*safety|alignment|ai ethics"),
 ("sales_consulting_gtm",  r"sales|customer engineer|consult\w+|specialist|account|solutions? architect|go to market|\bgtm\b|partner|pursuit|business development|customer success|practice lead|advisor|field"),
 ("product_program_mgmt",  r"product manag\w+|program manag\w+|\btpm\b|product lead|product owner|product operations"),
 ("research",              r"research scientist|research engineer|researcher|ai resident|research (lead|manager)|research staff"),
 ("infra_hardware",        r"infrastructure|\btpus?\b|tensor|silicon|asic|accelerator|hardware|data center|compiler|\bsre\b|site reliability|performance|platform"),
 ("ml_ai_engineering",     r"engineer|developer|architect|software|swe|scientist|analyst"),
 ("management_other",      r"manager|director|head of|\blead\b|vice president|president"),
]
def family(title):
    for name, rx in FAMILIES:
        if re.search(rx, title, re.I): return name
    return "other_functions"
