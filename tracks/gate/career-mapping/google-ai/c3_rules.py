"""SCRATCH (checkpoint 3): mutually-exclusive families (documented first-match order) and ONE rule for AI-as-domain vs AI-as-work."""
import re

FAMILY_ORDER = [  # first match wins => mutually exclusive; each year's shares sum to 100%
 ("1 ai_safety_responsible", r"responsible ai|ai safety|safety.*\bai\b|\bai\b.*safety|alignment|ai ethics|ai principles"),
 ("2 sales_consulting_gtm",  r"sales|customer engineer|consult\w+|specialist|account|solutions? architect|go to market|\bgtm\b|partner|pursuit|business development|customer success|practice lead|advisor|field"),
 ("3 product_program_mgmt",  r"product manag\w+|program manag\w+|\btpm\b|product lead|product owner|product operations"),
 ("4 business_functions",    r"marketing|communications|comms\b|brand|policy|government affairs|counsel|legal|finance|accountant|recruit\w*|people (operations|partner)|\bhr\b|talent|designer|\bdesign\b|\bux\b|interaction|writer|content (strategist|specialist|writer|designer)|operations manager|escalations?|enforcement|strategist|strategy|support\b"),
 ("5 research",              r"research scientist|research engineer|researcher|ai resident|research (lead|manager)|research staff"),
 ("6 infra_hardware",        r"infrastructure|\btpus?\b|tensor|silicon|asic|accelerator|hardware|data center|compiler|\bsre\b|site reliability|platform"),
 ("7 ml_ai_engineering",     r"engineer|developer|architect|software|swe|scientist|analyst"),
 ("8 management_other",      r"manager|director|head of|\blead\b|vice president|president"),
 ("9 other_functions",       r".*"),
]
def family(title):
    for name, rx in FAMILY_ORDER:
        if re.search(rx, title, re.I): return name

_DOMAIN_FUNC = re.compile(r"marketing|\bcommunications\b|comms\b|brand|policy|government affairs|counsel|legal|finance|accountant|recruit\w*|\bhr\b|talent|designer|\bux\b|interaction design|writer|escalations?|enforcement|strategist|operations manager|support\b", re.I)
_ML_SPECIFIC = re.compile(r"machine learning|aiml|genai|generative|language models?|neural|deep learning|reinforcement|computer vision|natural language|agentic|tensor|mlops|\btpus?\b", re.I)
_ML_CASE = re.compile(r"\b(ML|LLMs?|NLP)\b")
_FRONT = re.compile(r"front ?end|full ?stack|\bmobile\b|\bandroid\b|\bios\b|\bweb\b", re.I)

def nature(title):
    """-> (verdict 'work'|'domain', borderline: bool).
    AI-as-domain = the role's function is unrelated to AI expertise (marketing, comms, legal, policy/government affairs, HR/recruiting,
    finance, design/UX/writing, ops/support/escalations/enforcement) OR a generic front-end/full-stack/mobile/web engineering role whose only AI
    evidence is the acronym 'AI'/a product name (no ML-specific term). Everything else = AI-as-work.
    Borderline = a domain function word AND an ML-specific term both present (conflict), or the generic-engineering rule fired."""
    ml = bool(_ML_SPECIFIC.search(title) or _ML_CASE.search(title))
    func = bool(_DOMAIN_FUNC.search(title)); front = bool(_FRONT.search(title)) and not ml
    return ("domain" if (func or front) else "work"), bool((func and ml) or front)
