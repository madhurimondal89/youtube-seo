import re
from typing import Optional
from app.models.video import VideoMetadata
from app.models.common import DataProvenance

def extract_keywords_from_titles(videos: list[VideoMetadata]) -> set[str]:
    """Extracts cleaned 2-3 word phrases and key terms from a set of video titles."""
    tokens = set()
    stop = {"how", "to", "the", "in", "and", "for", "with", "a", "of", "on", "is", "this", "my", "why"}
    for v in videos:
        clean = re.sub(r"[^\w\s]", " ", v.title.lower())
        words = [w for w in clean.split() if w and w not in stop and len(w) > 2]
        # Single keywords
        for w in words:
            tokens.add(w)
        # Bi-grams
        for i in range(len(words) - 1):
            tokens.add(f"{words[i]} {words[i+1]}")
    return tokens

def detect_content_gaps(
    user_videos: list[VideoMetadata],
    competitor_videos: list[VideoMetadata],
    channel_median_views: int = 20000
) -> list[dict]:
    """
    Finds topics present in high-performing competitor videos that are absent
    or under-served in the user's channel.
    Categorizes into HIGH, MEDIUM, LOW opportunity with explanations.
    """
    user_topics = extract_keywords_from_titles(user_videos)
    gaps: list[dict] = []

    seen_gap_titles = set()

    for cv in competitor_videos:
        views = cv.views_count or 0
        multiplier = views / max(1, channel_median_views)
        
        # Check if title has significant overlap with user topics
        cv_clean = re.sub(r"[^\w\s]", " ", cv.title.lower())
        cv_words = [w for w in cv_clean.split() if len(w) > 3]
        overlap_count = sum(1 for w in cv_words if w in user_topics)
        is_covered = overlap_count >= max(2, len(cv_words) // 2)

        if not is_covered and cv.title not in seen_gap_titles:
            seen_gap_titles.add(cv.title)

            # Determine opportunity tier
            if multiplier >= 3.0 or views > 100_000:
                tier = "HIGH OPPORTUNITY"
                explanation = f"Competitor achieved {multiplier:.1f}x views on this topic while your channel has zero direct coverage."
            elif multiplier >= 1.5 or views > 30_000:
                tier = "MEDIUM OPPORTUNITY"
                explanation = "Solid competitor traction detected; presents an attractive supporting topic to capture search traffic."
            else:
                tier = "LOW OPPORTUNITY"
                explanation = "Competitor covered this topic with average performance; consider testing if it fits a specific series."

            gaps.append({
                "topic_title": cv.title,
                "competitor_channel": cv.channel_name,
                "competitor_views": views,
                "opportunity_tier": tier,
                "multiplier": round(multiplier, 2),
                "explanation": explanation,
                "recommended_action": f"Create a comprehensive video titled: 'Mastering {cv.title.split(':')[0]} (Updated Guide)'",
                "provenance": DataProvenance.CALCULATED.value
            })

    # Sort gaps by multiplier descending
    gaps.sort(key=lambda g: g["multiplier"], reverse=True)
    return gaps[:12]
