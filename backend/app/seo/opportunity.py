from typing import Optional
from app.models.keyword import KeywordMetricItem, SearchIntent
from app.models.video import VideoSearchResult
from app.models.common import DataProvenance
from app.seo.intent import classify_search_intent
from app.seo.competition import calculate_estimated_competition
from app.seo.keyword_engine import calculate_specificity_score

def calculate_relative_demand(
    keyword: str,
    root_query: str,
    autocomplete_rank: Optional[int] = None,
    serp_results: Optional[list[VideoSearchResult]] = None
) -> int:
    """
    Computes Relative Demand Index (0-100).
    Never fabricates monthly search volumes.
    """
    # 1. Suggestion position score (rank 1 -> 100, rank 10 -> 10, not found -> 25)
    if autocomplete_rank is not None and autocomplete_rank >= 1:
        s_rank = max(10, 105 - (autocomplete_rank * 10))
    else:
        s_rank = 30

    # 2. Query brevity bonus (shorter, high-intent phrases generally have higher search volume)
    words = len(keyword.split())
    if words <= 2:
        s_brevity = 90
    elif words <= 4:
        s_brevity = 75
    else:
        s_brevity = max(30, 75 - (words - 4) * 8)

    # 3. Match in root query
    s_root = 90 if root_query.lower() in keyword.lower() else 50

    # 4. SERP views presence
    if serp_results:
        views = [v.views_count for v in serp_results if v.views_count]
        if views:
            avg_v = sum(views) / len(views)
            if avg_v > 500_000:
                s_views = 95
            elif avg_v > 100_000:
                s_views = 80
            elif avg_v > 20_000:
                s_views = 65
            else:
                s_views = 45
        else:
            s_views = 50
    else:
        s_views = 50

    score = int(round(0.40 * s_rank + 0.25 * s_brevity + 0.20 * s_root + 0.15 * s_views))
    return min(100, max(0, score))

def calculate_opportunity_score(
    keyword: str,
    relative_demand: int,
    estimated_competition: int,
    specificity: int,
    intents: list[SearchIntent],
    serp_results: Optional[list[VideoSearchResult]] = None
) -> tuple[int, dict[str, float], list[str]]:
    """
    Computes transparent 10-component Opportunity Score (0-100).
    Formula from docs/SEO_SCORING.md:
    1. Demand: 15%
    2. Competition Opportunity: 15% (100 - Competition)
    3. Small Creator Success: 10%
    4. Freshness Signal: 10%
    5. Content Gap Signal: 10%
    6. Search Intent Specificity: 10%
    7. Long-Tail Specificity: 10%
    8. Channel Fit / Broad Applicability: 10%
    9. Outlier Evidence: 5%
    10. Trend Persistence: 5%
    """
    reasons: list[str] = []

    # 1. Demand signal (15%)
    s_demand = float(relative_demand)

    # 2. Competition opportunity (15%)
    s_comp_opp = float(100 - estimated_competition)

    # 3. Small creator success (10%)
    # Checks if non-mega channels are getting meaningful views in SERP
    if serp_results:
        small_success = sum(
            1 for v in serp_results
            if (v.views_count and v.views_count > 15_000) and ("official" not in v.channel_name.lower())
        )
        s_small_creator = min(100.0, (small_success / max(1, len(serp_results))) * 150.0)
    else:
        s_small_creator = 60.0

    # 4. Freshness signal (10%)
    if serp_results:
        fresh_count = sum(
            1 for v in serp_results
            if any(term in (v.published_time_text or "").lower() for term in ["day", "week", "month", "2026"])
        )
        s_freshness = min(100.0, (fresh_count / max(1, len(serp_results))) * 160.0)
    else:
        s_freshness = 55.0

    # 5. Content gap signal (10%)
    # High if competition is low or titles don't closely match
    s_gap = min(100.0, max(20.0, float(100 - (estimated_competition * 0.8))))

    # 6. Search intent specificity (10%)
    # High-action intents like Tutorial, Comparison, Problem/Fix score higher than vague
    high_intent = any(i in intents for i in [SearchIntent.TUTORIAL, SearchIntent.PROBLEM_FIX, SearchIntent.COMPARISON, SearchIntent.COMMERCIAL])
    s_intent = 85.0 if high_intent else 55.0

    # 7. Long-tail specificity (10%)
    s_longtail = float(specificity)

    # 8. Channel fit / Applicability (10%)
    s_fit = 70.0

    # 9. Outlier evidence (5%)
    # Checks if any breakout videos exist in results
    if serp_results:
        has_breakout = any(v.views_count and v.views_count > 250_000 for v in serp_results)
        s_outlier = 90.0 if has_breakout else 45.0
    else:
        s_outlier = 50.0

    # 10. Trend persistence (5%)
    s_trend = 65.0

    score = (
        0.15 * s_demand +
        0.15 * s_comp_opp +
        0.10 * s_small_creator +
        0.10 * s_freshness +
        0.10 * s_gap +
        0.10 * s_intent +
        0.10 * s_longtail +
        0.10 * s_fit +
        0.05 * s_outlier +
        0.05 * s_trend
    )
    final_score = int(round(min(100.0, max(0.0, score))))

    breakdown = {
        "demand_signal": round(s_demand, 1),
        "competition_opportunity": round(s_comp_opp, 1),
        "small_creator_success": round(s_small_creator, 1),
        "freshness": round(s_freshness, 1),
        "content_gap": round(s_gap, 1),
        "intent_alignment": round(s_intent, 1),
        "long_tail_specificity": round(s_longtail, 1),
        "channel_fit": round(s_fit, 1),
        "outlier_evidence": round(s_outlier, 1),
        "trend_persistence": round(s_trend, 1),
    }

    if final_score >= 75:
        reasons.append("High opportunity: Strong creator demand with accessible competition.")
    elif final_score >= 50:
        reasons.append("Moderate opportunity: Solid demand; needs distinctive packaging to rank.")
    else:
        reasons.append("Low opportunity: Heavy saturation or low long-tail specificity.")

    if s_comp_opp >= 60:
        reasons.append("Competition level is favorable for new creators.")
    if high_intent:
        reasons.append("Clear actionable intent (high viewer satisfaction potential).")
    if s_longtail >= 75:
        reasons.append("Specific long-tail query with focused audience reach.")

    return final_score, breakdown, reasons
