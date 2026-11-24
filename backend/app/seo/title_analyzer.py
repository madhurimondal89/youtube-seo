import re
from typing import Optional

POWER_WORDS = {
    "secret", "proven", "blueprint", "mastery", "ultimate", "essential",
    "mistakes", "fast", "simple", "hack", "step-by-step", "insane", "stop",
    "never", "warning", "guide", "framework", "revealed", "truth"
}

def analyze_title_heuristics(title: str, target_keyword: Optional[str] = None) -> dict:
    """
    Evaluates title structure, readability, and clickability heuristics deterministically.
    Never claims to guarantee CTR.
    """
    clean_title = title.strip()
    char_len = len(clean_title)
    words = clean_title.split()
    word_count = len(words)

    # 1. Length Score (45-70 chars is optimal on YouTube desktop/mobile)
    if 45 <= char_len <= 70:
        length_score = 100
        length_feedback = "Optimal character length for mobile and desktop display (45-70 characters)."
    elif 30 <= char_len < 45:
        length_score = 75
        length_feedback = "Slightly short; you could add a curiosity hook or qualifier."
    elif 70 < char_len <= 90:
        length_score = 70
        length_feedback = "Slightly long; may be truncated on mobile search screens."
    else:
        length_score = 40
        length_feedback = "Suboptimal length; keep titles between 45 and 70 characters for best visibility."

    # 2. Keyword Placement
    has_keyword = False
    frontloaded = False
    if target_keyword and target_keyword.strip():
        kw = target_keyword.lower().strip()
        if kw in clean_title.lower():
            has_keyword = True
            pos = clean_title.lower().find(kw)
            if pos <= 30:
                frontloaded = True

    # 3. Numbers presence
    has_number = bool(re.search(r"\b\d+\b", clean_title))

    # 4. Power / Emotional words
    power_matches = [w for w in words if re.sub(r"[^\w]", "", w.lower()) in POWER_WORDS]

    # 5. Question or curiosity indicator
    has_question = "?" in clean_title or any(clean_title.lower().startswith(q) for q in ["how", "why", "what", "can", "will", "is"])

    # 6. All-caps shouting check
    upper_count = sum(1 for c in clean_title if c.isupper())
    is_spammy_caps = upper_count > len(clean_title) * 0.45 and len(clean_title) > 20

    # Composite curiosity heuristic
    curiosity_score = 40
    if has_question:
        curiosity_score += 20
    if has_number:
        curiosity_score += 15
    if power_matches:
        curiosity_score += min(25, len(power_matches) * 15)
    curiosity_score = min(100, curiosity_score)

    return {
        "title": clean_title,
        "character_count": char_len,
        "word_count": word_count,
        "length_score": length_score,
        "length_feedback": length_feedback,
        "has_keyword": has_keyword,
        "frontloaded_keyword": frontloaded,
        "has_number": has_number,
        "power_words": power_matches,
        "curiosity_score": curiosity_score,
        "is_spammy_caps": is_spammy_caps,
    }
