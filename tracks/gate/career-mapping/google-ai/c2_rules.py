"""SCRATCH (checkpoint 2): approved CORE-AI / DATA-SCIENCE / AI-ADJACENT / DEEPMIND / FAMILY rules."""
import re

_PHRASE = re.compile(r"\b(machine learning|artificial intelligence|deep learning|reinforcement learning|computer vision|"
                     r"language models?|generative|neural|gemini|gemma|notebooklm|bard|natural language|agentic|"
                     r"autonomous agents?|agent platform|tensor processing|vertex|tpus?|aiml|genai|mlops|aimachine)\b", re.I)
_ACRO = re.compile(r"\b(AI|ML|LLMs?|NLP|GenAI)\b")              # case-sensitive on the re-cased slug title
_ADJ = re.compile(r"\b(google assistant|recommendations?|ranking|personalization|perception|robotics?|sensing|"
                  r"translate|translation|speech|research (scientist|engineer))\b", re.I)

def flags(title):
    t = re.sub(r"\bquantum ai\b", " ", title, flags=re.I)          # org name; rescued if separate ML words remain
    ds = bool(re.search(r"\bdata scien\w+", t, re.I))
    t = re.sub(r"\bdata scien\w+", " ", t, flags=re.I)
    core = bool(_PHRASE.search(t) or _ACRO.search(t))
    dm = bool(re.search(r"\bdeepmind\b", title, re.I))
    adj = (not core) and (not dm) and bool(_ADJ.search(re.sub(r"\bhate speech\b", " ", t, flags=re.I)))
    return {"core": core, "ds_only": ds and not core, "deepmind": dm, "dm_only": dm and not core, "adjacent": adj}

FAMILIES = [  # first match wins; 'performance' removed (it sent ML engineers to infra)
 ("ai_safety_responsible", r"responsible ai|ai safety|safety.*\bai\b|\bai\b.*safety|alignment|ai ethics"),
 ("sales_consulting_gtm",  r"sales|customer engineer|consult\w+|specialist|account|solutions? architect|go to market|\bgtm\b|partner|pursuit|business development|customer success|practice lead|advisor|field"),
 ("product_program_mgmt",  r"product manag\w+|program manag\w+|\btpm\b|product lead|product owner|product operations"),
 ("research",              r"research scientist|research engineer|researcher|ai resident|research (lead|manager)|research staff"),
 ("infra_hardware",        r"infrastructure|\btpus?\b|tensor|silicon|asic|accelerator|hardware|data center|compiler|\bsre\b|site reliability|platform"),
 ("ml_ai_engineering",     r"engineer|developer|architect|software|swe|scientist|analyst"),
 ("management_other",      r"manager|director|head of|\blead\b|vice president|president"),
]
def family(title):
    for name, rx in FAMILIES:
        if re.search(rx, title, re.I): return name
    return "other_functions"
