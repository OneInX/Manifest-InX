# engine.py
# MicroInX Engine v1.0 — minimal deterministic skeleton (Sprint 1, low-compute)

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# --- Canonical template surface (v0.3) ---
TEMPLATES: Dict[str, str] = {
    "T01": "You defer by widening input until signal collapses. Narrow input doesn’t prevent single-channel collapse.",
    "T02": "You degrade reference by letting definition expand without constraint. A frozen frame doesn’t stop scope creep.",
    "T03": "You gate action behind unreachable precision. A minimum gate still blocks action.",
    "T04": "You displace the primary node into secondary output. Primary node lock is absent.",
    "T05": "You hold control bandwidth fixed and leave output uncapped. Uncapped output guarantees spillover.",
    "T06": "You prioritize the milestone while prerequisites remain unverified. Unverified prerequisites produce rework.",
    "T07": "You hold a pathway open; a trigger re-enters and recurrence persists. An unbroken trigger keeps recurrence alive.",
    "T08": "You loop because the stop condition is undefined or unstable. An undefined stop condition sustains recurrence.",
    "T09": "You hold competing constraints and adjacent decisions diverge. A competing constraint rule drives divergence.",
    "T10": "You diverge interpretations under one label. Coherence degrades when one label carries multiple interpretations.",
    "T11": "You defer by letting a weak definition trigger repeated interpretation. An unfrozen definition regenerates recurrence.",
    "T12": "You gate entry above the minimum; recurrence persists. An entry gate above minimum sustains recurrence.",
    "T13": "You prioritize parallel output; constraints diverge. Without one rule, divergence is guaranteed.",
    "T14": "You hold scope open and the primary node degrades; action defers. A hard boundary doesn’t release action.",
    "T15": "You prioritize output without a lock window; rework is the default. Without a lock window and rate limit, rework persists.",
}

VECTORS = ("drift", "avoidance", "drive", "loop", "fracture")
TIEBREAK = ("fracture", "avoidance", "loop", "drift", "drive")

COMPOSITE_ALLOWED = {
    ("drift", "loop"): "drift+loop",
    ("avoidance", "loop"): "avoidance+loop",
    ("drive", "fracture"): "drive+fracture",
    ("drift", "avoidance"): "drift+avoidance",
    ("drive", "loop"): "drive+loop",
}
COMPOSITE_TO_TEMPLATE = {
    "drift+loop": "T11",
    "avoidance+loop": "T12",
    "drive+fracture": "T13",
    "drift+avoidance": "T14",
    "drive+loop": "T15",
}
DOMINANT_TO_TEMPLATE = {
    "drift": ("T01", "T02"),
    "avoidance": ("T03", "T04"),
    "drive": ("T06", "T05"),
    "loop": ("T08", "T07"),
    "fracture": ("T10", "T09"),
}


@dataclass(frozen=True)
class ExtractedSignals:
    markers: Dict[str, List[str]]
    counts: Dict[str, int]
    scores: Dict[str, int]


@dataclass(frozen=True)
class MappedVectors:
    dominant: str
    secondary: Optional[str]
    composite: Optional[str]
    confidence: float


_WORD = re.compile(r"\b[\w']+\b", re.UNICODE)
_WS = re.compile(r"\s+")
_SENT_SPLIT = re.compile(r"[.!]")
_INTERROG_START = re.compile(r"^\s*(why|how|what|when|where|who)\b", re.I)
_BULLET = re.compile(r"(^|\n)\s*(?:[-*]|\d+\.)\s+", re.M)
_BECAUSE = re.compile(r"\bbecause\b", re.I)
_PROFANITY = re.compile(r"\b(damn|shit|fuck)\b", re.I)  # proxy only


def _tokenize(text: str) -> List[str]:
    return _WORD.findall(text)


def _count_sentences(text: str) -> int:
    segs = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    return len(segs)


def _find_phrases(text_l: str, phrases: List[str]) -> List[str]:
    return [p for p in phrases if re.search(p, text_l, re.I)]


def _count_word_hits(tokens_l: List[str], wordset: set[str]) -> int:
    return sum(1 for t in tokens_l if t in wordset)


def _detect_contradictions(text_l: str) -> int:
    pairs = 0
    if re.search(r"\bi want\b", text_l) and re.search(r"\bi (do not|don't) want\b", text_l):
        pairs += 1
    if re.search(r"\balways\b", text_l) and re.search(r"\bnever\b", text_l):
        pairs += 1
    if re.search(r"\bi will\b", text_l) and re.search(r"\bi can't\b", text_l):
        pairs += 1
    return pairs


# Phrase markers (+2 each)
DRIFT_PHRASES = [
    r"\bnot now\b",
    r"\bnext week\b",
    r"\bneed more context\b",
    r"\bkeep thinking\b",
    r"\bmore research\b",
    r"\bopen ended\b",
    r"\bfigure out everything\b",
]
AVOID_PHRASES = [
    r"\bno risk\b",
    r"\bcannot fail\b",
    r"\bbefore i start\b",
    r"\bonly if\b",
    r"\bneed all\b",
    r"\bi will just\b",
]
DRIVE_PHRASES = [
    r"\bjust do it\b",
    r"\bfix later\b",
    r"\bdoesn't matter\b",
    r"\bin parallel\b",
    r"\bsimultaneously\b",
]
LOOP_PHRASES = [
    r"\bevery time\b",
    r"\bback to\b",
    r"\bno end\b",
    r"\bnever done\b",
    r"\bcan't finish\b",
]
FRACTURE_PHRASES = [
    r"\bdefinition changes\b",
    r"\btwo meanings\b",
]

# Word markers (+1 per token hit)
DRIFT_WORDS = {"later", "eventually", "someday", "after", "tomorrow", "once", "when", "scope", "depends", "context", "research"}
AVOID_WORDS = {"perfect", "exact", "certainty", "guarantee", "proof", "until", "must", "instead", "secondary"}
DRIVE_WORDS = {"asap", "now", "today", "ship", "launch", "push", "fast", "rush", "deadline", "skip", "ignore"}
LOOP_WORDS = {"again", "keep", "still", "same", "repeat", "restart", "revisit", "stuck"}
FRACTURE_WORDS = {"but", "however", "yet", "although", "call", "label", "means"}


def extract_signals(minimal_user_signal: Dict[str, Any]) -> ExtractedSignals:
    raw = (minimal_user_signal or {}).get("raw_text", "") or ""
    text = _WS.sub(" ", raw).strip()
    text_l = text.lower()
    tokens = _tokenize(text)
    tokens_l = [t.lower() for t in tokens]

    counts = {
        "tokens": len(tokens),
        "sentences": _count_sentences(text),
        "question_marks": text.count("?"),
        "bullets": len(_BULLET.findall(raw)),
        "profanity": 1 if _PROFANITY.search(text) else 0,
        "contradiction_pairs": _detect_contradictions(text_l),
    }

    markers: Dict[str, List[str]] = {v: [] for v in VECTORS}
    scores: Dict[str, int] = {v: 0 for v in VECTORS}

    # phrase hits
    markers["drift"] = _find_phrases(text_l, DRIFT_PHRASES)
    markers["avoidance"] = _find_phrases(text_l, AVOID_PHRASES)
    markers["drive"] = _find_phrases(text_l, DRIVE_PHRASES)
    markers["loop"] = _find_phrases(text_l, LOOP_PHRASES)
    markers["fracture"] = _find_phrases(text_l, FRACTURE_PHRASES)

    scores["drift"] += 2 * len(markers["drift"])
    scores["avoidance"] += 2 * len(markers["avoidance"])
    scores["drive"] += 2 * len(markers["drive"])
    scores["loop"] += 2 * len(markers["loop"])
    scores["fracture"] += 2 * len(markers["fracture"])

    # word hits
    scores["drift"] += _count_word_hits(tokens_l, DRIFT_WORDS)
    scores["avoidance"] += _count_word_hits(tokens_l, AVOID_WORDS)
    scores["drive"] += _count_word_hits(tokens_l, DRIVE_WORDS)
    scores["loop"] += _count_word_hits(tokens_l, LOOP_WORDS)
    scores["fracture"] += _count_word_hits(tokens_l, FRACTURE_WORDS)

    # structural bonuses
    if len(_BECAUSE.findall(text_l)) >= 3:
        scores["drift"] += 2
    if counts["bullets"] >= 3:
        scores["drift"] += 1

    if re.search(r"\b(perfect|100%|guarantee)\b", text_l):
        scores["avoidance"] += 2
    if re.search(r"\b(until|only if|before i)\b", text_l):
        scores["avoidance"] += 2

    if re.search(r"\b(asap|today|deadline|rush|ship|launch|now)\b", text_l):
        scores["drive"] += 2
    if re.search(r"\b(skip|ignore|fix later|doesn't matter)\b", text_l):
        scores["drive"] += 2

    unique_loop = {w for w in ("again", "restart", "repeat", "revisit", "every", "still", "same", "keep") if w in tokens_l}
    if len(unique_loop) >= 2:
        scores["loop"] += 2
    if (("restart" in tokens_l) or ("again" in tokens_l)) and ("still" in tokens_l):
        scores["loop"] += 2

    contrast = sum(1 for w in ("but", "however", "yet", "although") if w in tokens_l)
    if contrast >= 2:
        scores["fracture"] += 2
    if counts["contradiction_pairs"] > 0:
        scores["fracture"] += 3

    return ExtractedSignals(markers=markers, counts=counts, scores=scores)


def score_vectors(signals: ExtractedSignals, raw_text: str) -> MappedVectors:
    scores = signals.scores

    if all(scores[v] == 0 for v in VECTORS):
        return MappedVectors(dominant="drift", secondary=None, composite=None, confidence=0.0)

    top = max(scores.values())
    top_candidates = [v for v in VECTORS if scores[v] == top]
    if len(top_candidates) > 1:
        dominant = next(v for v in TIEBREAK if v in top_candidates)
    else:
        dominant = top_candidates[0]

    remaining = sorted([(v, s) for v, s in scores.items() if v != dominant], key=lambda x: (-x[1], x[0]))
    secondary = None
    second_score = remaining[0][1] if remaining else 0
    if remaining and second_score >= (scores[dominant] - 1) and second_score >= 3:
        secondary = remaining[0][0]

    short = len((raw_text or "").strip()) < 20
    if short:
        secondary = None

    composite = None
    if secondary is not None and scores[dominant] >= 3 and scores[secondary] >= 3:
        key = (dominant, secondary)
        if key in COMPOSITE_ALLOWED:
            composite = COMPOSITE_ALLOWED[key]
    if short:
        composite = None

    sorted_vals = sorted(scores.values(), reverse=True)
    top_v = sorted_vals[0]
    second_v = sorted_vals[1] if len(sorted_vals) > 1 else 0
    confidence = (top_v - second_v + 1) / (top_v + 1)
    confidence = max(0.0, min(1.0, confidence))
    if short:
        confidence = min(confidence, 0.4)

    return MappedVectors(dominant=dominant, secondary=secondary, composite=composite, confidence=confidence)


def select_template(vectors: MappedVectors, signals: ExtractedSignals) -> str:
    if vectors.composite:
        return COMPOSITE_TO_TEMPLATE[vectors.composite]

    primary, _fallback = DOMINANT_TO_TEMPLATE[vectors.dominant]
    if signals.scores.get(vectors.dominant, 0) < 3:
        return "T02"
    return primary


def render_output(template_id: str) -> str:
    return TEMPLATES[template_id]


# --- SDT gate v1.0 (minimum set) ---
_HARD_BAN_PATTERNS = [
    r"\bmaybe\b",
    r"\bfeel(ing|ings)?\b",
    r"\bunderstand\b",
    r"\bokay\b",
    r"\bok\b",
    r"\bsorry\b",
    r"it\s*(is|'s)\s*okay",
    r"\bempathy\b",
    r"\bcompassion\b",
    r"\bcomfort(ing)?\b",
    r"\breassur(e|ing|ance)\b",
    r"\bsupport(ive)?\b",
    r"\bheal(ing)?\b",
    r"\byou\s*'?re\s*not\s*alone\b",
    r"\bshould(n'?t)?\b",
    r"\btry\b",
    r"\bconsider\b",
    r"\bsuggest\b",
    r"\brecommend\b",
    r"\badvisable\b",
    r"\btips?\b",
    r"\bguidance\b",
    r"\bhelp(ful)?\b",
    r"\bneed\s*to\b",
    r"\banxiety\b",
    r"\bdepress(ed|ion)?\b",
    r"\bstress(ed)?\b",
    r"\btrauma\b",
    r"\bptsd\b",
    r"\btherap(y|ist)\b",
    r"\bmental\b",
    r"\bemotion\w*\b",
    r"\bmindset\b",
    r"\bmotivation\b",
    r"\bself-esteem\b",
    r"\bego\b",
    r"\bcoping\b",
    r"\bsubconscious\b",
    r"\bdisclaimer\b",
    r"\bnot\s*medical\b",
    r"\bnot\s*legal\b",
    r"\bnot\s*financial\b",
    r"\bconsult\b",
    r"\bprofessional\b",
    r"\bhotline\b",
    r"\bcrisis\b",
    r"\bpolicy\b",
    r"\blet\s*'?s\b",
    r"\bbuddy\b",
    r"\blol\b",
    r"\bhaha\b",
    r"ㅋㅋ",
]
_REVIEW_FLAG_PATTERNS = [r"\bmust\b", r"\bbest\b", r"\bbetter\b", r"\bworse\b", r"\bideal(ly)?\b", r"\bgood\b", r"\bbad\b", r"\bwe\b", r"\bi\b"]
_EMOTICONS = (":)", ":(", ";)")


def _contains_emoji(s: str) -> bool:
    for ch in s:
        o = ord(ch)
        if (0x1F300 <= o <= 0x1FAFF) or (0x2600 <= o <= 0x26FF) or (0x2700 <= o <= 0x27BF):
            return True
    return False


def sdt_gate(output_text: str, template_id: str) -> Dict[str, Any]:
    violations: List[str] = []

    if template_id not in TEMPLATES:
        return {"pass": False, "violations": ["TEMPLATE_ID_UNKNOWN"]}

    if output_text != TEMPLATES[template_id]:
        violations.append("EXACT_TEMPLATE_MISMATCH")

    sent_n = _count_sentences(output_text)
    if sent_n < 1 or sent_n > 2:
        violations.append("SENTENCE_COUNT")

    if len(_tokenize(output_text)) > 40:
        violations.append("WORD_COUNT")

    if "?" in output_text:
        violations.append("QUESTION_MARK")
    if _INTERROG_START.search(output_text):
        violations.append("INTERROGATIVE_START")

    out_l = output_text.lower()
    for pat in _HARD_BAN_PATTERNS:
        if re.search(pat, out_l, re.I):
            violations.append(f"FORBIDDEN:{pat}")
            break

    for pat in _REVIEW_FLAG_PATTERNS:
        if re.search(pat, out_l, re.I):
            violations.append(f"FLAG:{pat}")

    if _contains_emoji(output_text):
        violations.append("EMOJI")
    if any(e in output_text for e in _EMOTICONS):
        violations.append("EMOTICON")

    hard_fail = any(
        v.startswith(
            (
                "EXACT_TEMPLATE_MISMATCH",
                "SENTENCE_COUNT",
                "WORD_COUNT",
                "QUESTION_MARK",
                "INTERROGATIVE_START",
                "FORBIDDEN:",
                "EMOJI",
                "EMOTICON",
                "TEMPLATE_ID_UNKNOWN",
            )
        )
        for v in violations
    )
    return {"pass": (not hard_fail), "violations": violations}


def generate_blade_insight(minimal_user_signal: Dict[str, Any]) -> Dict[str, Any]:
    signals = extract_signals(minimal_user_signal)
    raw = (minimal_user_signal or {}).get("raw_text", "") or ""
    vectors = score_vectors(signals, raw_text=raw)
    template_id = select_template(vectors, signals)
    output_text = render_output(template_id)
    sdt = sdt_gate(output_text, template_id)
    return {
        "template_id": template_id,
        "output_text": output_text,
        "mapped_vectors": {
            "dominant": vectors.dominant,
            "secondary": vectors.secondary,
            "composite": vectors.composite,
            "confidence": vectors.confidence,
        },
        "sdt": sdt,
        "debug": {"signals": {"markers": signals.markers, "counts": signals.counts, "scores": signals.scores}},
    }