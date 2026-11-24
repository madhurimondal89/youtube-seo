import re
import asyncio
from typing import Optional
from app.models.keyword import KeywordMetricItem, SearchIntent
from app.seo.intent import classify_search_intent
from app.youtube.base import YouTubeProvider
from app.core.security import sanitize_keyword

MODIFIER_PREFIXES = [
    "how to", "best", "top", "why", "what is", "learn", "complete guide to"
]

QUESTION_PREFIXES = [
    "how to", "why does", "what is", "can you", "where to", "when to", "is it safe to", "how do I"
]

COMPARISON_MODIFIERS = [
    "vs", "or", "alternative", "compared to", "better than"
]

MODIFIER_SUFFIXES = [
    "tutorial", "for beginners", "2026", "review", "vs", "tips", "workflow", "tools", "without code", "setup"
]

def normalize_keyword(keyword: str) -> str:
    """Normalize keyword casing, spacing, and punctuation."""
    text = keyword.lower().strip()
    text = re.sub(r"[^\w\s\-\.]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def calculate_specificity_score(keyword: str) -> int:
    """
    Long-tail specificity score 0-100 based on word count and semantic depth.
    1-2 words: 20-40 (broad)
    3-4 words: 50-80 (focused)
    5+ words: 85-100 (high long-tail specificity)
    """
    words = keyword.split()
    count = len(words)
    if count <= 1:
        return 20
    elif count == 2:
        return 40
    elif count == 3:
        return 65
    elif count == 4:
        return 80
    else:
        return min(100, 80 + (count - 4) * 6)

async def expand_keywords(
    seed: str,
    provider: YouTubeProvider,
    include_alphabet: bool = True,
    include_modifiers: bool = True,
    include_questions: bool = True,
    include_comparisons: bool = True,
    max_keywords: int = 50
) -> list[str]:
    """
    Performs deterministic multi-vector expansion:
    1. Root suggestions
    2. Modifiers (prefixes and suffixes)
    3. Questions ("how to", "why does", "what is", etc.)
    4. Comparisons ("vs", "alternative", "or", etc.)
    5. Alphabet expansion (a through z)
    """
    clean_seed = normalize_keyword(sanitize_keyword(seed))
    if not clean_seed:
        return []

    collected: dict[str, int] = {clean_seed: 100}  # keyword -> priority score

    # 1. Fetch root autocomplete
    root_suggs = await provider.get_autocomplete_suggestions(clean_seed)
    for idx, s in enumerate(root_suggs):
        norm = normalize_keyword(s)
        if norm and norm not in collected:
            collected[norm] = max(10, 95 - (idx * 5))

    tasks = []

    # 2. Modifiers expansion
    if include_modifiers:
        for prefix in MODIFIER_PREFIXES[:3]:
            tasks.append(provider.get_autocomplete_suggestions(f"{prefix} {clean_seed}"))
        for suffix in MODIFIER_SUFFIXES[:3]:
            tasks.append(provider.get_autocomplete_suggestions(f"{clean_seed} {suffix}"))

    # 3. Question expansion
    if include_questions:
        for q in QUESTION_PREFIXES[:4]:
            tasks.append(provider.get_autocomplete_suggestions(f"{q} {clean_seed}"))

    # 4. Comparison expansion
    if include_comparisons:
        for c in COMPARISON_MODIFIERS[:3]:
            tasks.append(provider.get_autocomplete_suggestions(f"{clean_seed} {c}"))

    # 5. Alphabet expansion (sample high-yield letters to stay fast and polite)
    if include_alphabet:
        high_yield_letters = ["a", "b", "c", "f", "h", "i", "p", "s", "t", "v", "w"]
        for letter in high_yield_letters:
            tasks.append(provider.get_autocomplete_suggestions(f"{clean_seed} {letter}"))

    if tasks:
        # Run in bounded batches
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for sub_list in results:
            if isinstance(sub_list, list):
                for idx, s in enumerate(sub_list):
                    norm = normalize_keyword(s)
                    if norm and norm not in collected:
                        # Prioritize keywords containing the seed
                        relevance = 75 if clean_seed in norm else 50
                        collected[norm] = max(10, relevance - (idx * 3))

    # Sort candidates by discovery priority and length
    sorted_keywords = sorted(
        collected.keys(),
        key=lambda k: (-collected[k], len(k))
    )
    return sorted_keywords[:max_keywords]
