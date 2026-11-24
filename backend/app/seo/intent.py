import re
from app.models.keyword import SearchIntent

INTENT_PATTERNS: dict[SearchIntent, list[re.Pattern]] = {
    SearchIntent.TUTORIAL: [
        re.compile(r"\b(how\s+to|tutorial|guide|step\s+by\s+step|walkthrough|setup|install|learn|build|coding|configure)\b", re.I),
    ],
    SearchIntent.INFORMATIONAL: [
        re.compile(r"\b(what\s+is|why|explained|meaning|history\s+of|overview|definition|concept|understanding|docs)\b", re.I),
    ],
    SearchIntent.COMMERCIAL: [
        re.compile(r"\b(best|top\s+\d+|review|reviews|worth\s+it|recommended|features|pricing|buyer'?s?\s+guide)\b", re.I),
    ],
    SearchIntent.COMPARISON: [
        re.compile(r"\b(vs|versus|difference\s+between|or|comparison|compared\s+to|alternative\s+to)\b", re.I),
    ],
    SearchIntent.PROBLEM_FIX: [
        re.compile(r"\b(fix|error|issue|problem|not\s+working|solved|troubleshoot|debug|failed|crash|bug)\b", re.I),
    ],
    SearchIntent.TRANSACTIONAL: [
        re.compile(r"\b(buy|discount|coupon|deal|purchase|cheap|order|course|template|download)\b", re.I),
    ],
    SearchIntent.NEWS_TRENDING: [
        re.compile(r"\b(2026|update|new|latest|announcement|release|future\s+of|breaking|leaks)\b", re.I),
    ],
    SearchIntent.ENTERTAINMENT: [
        re.compile(r"\b(vlog|reaction|challenge|funny|storytime|prank|gaming|meme|highlight)\b", re.I),
    ],
    SearchIntent.NAVIGATIONAL: [
        re.compile(r"\b(login|sign\s+in|official|website|portal|channel|dashboard)\b", re.I),
    ],
}

def classify_search_intent(keyword: str) -> list[SearchIntent]:
    """
    Deterministically classifies keyword into one or more search intents
    based on lexical patterns. Defaults to Informational if no pattern matches.
    """
    matched: list[SearchIntent] = []
    text = keyword.lower().strip()
    
    for intent, patterns in INTENT_PATTERNS.items():
        if any(p.search(text) for p in patterns):
            matched.append(intent)
            
    if not matched:
        # Default fallback
        matched.append(SearchIntent.INFORMATIONAL)
        
    return matched
