import math
from typing import Optional
from app.models.video import VideoSearchResult

def calculate_estimated_competition(
    keyword: str,
    search_results: list[VideoSearchResult]
) -> tuple[int, dict[str, float], list[str]]:
    """
    Computes deterministic Estimated Competition Score (0-100)
    using observable public SERP signals.
    Never claims proprietary YouTube insider data.
    """
    if not search_results:
        # Default baseline when SERP is empty
        return 50, {"baseline": 50.0}, ["Default median estimate: No SERP evidence available"]

    k_tokens = set(keyword.lower().split())
    n = len(search_results)
    reasons: list[str] = []

    # 1. Channel Authority Saturation (30%)
    # Large channels (views > 500k or verified presence)
    large_channels = 0
    for v in search_results:
        if (v.views_count and v.views_count > 500_000) or ("Official" in v.channel_name):
            large_channels += 1
    c_authority = (large_channels / n) * 100.0

    # 2. Median Views Density (25%)
    views_list = [v.views_count for v in search_results if v.views_count is not None]
    if views_list:
        sorted_views = sorted(views_list)
        med_views = sorted_views[len(sorted_views) // 2]
        # Log scale mapping: 100 views -> 0, 10,000 views -> 50, 1M+ views -> 100
        log_v = math.log10(max(1.0, float(med_views)))
        c_views = min(100.0, max(0.0, (log_v - 2.0) / 4.0 * 100.0))
    else:
        med_views = 25000
        c_views = 45.0

    # 3. Exact Keyword Density in Top 10 Titles (20%)
    top_10 = search_results[:10]
    matched_titles = 0
    for v in top_10:
        t_tokens = set(v.title.lower().split())
        overlap = len(k_tokens.intersection(t_tokens)) / max(1, len(k_tokens))
        if overlap >= 0.75:
            matched_titles += 1
    c_density = (matched_titles / max(1, len(top_10))) * 100.0

    # 4. Age Barrier / Incumbency (15%)
    # Look for older dominating videos vs fresh ranking
    recent_videos = sum(1 for v in search_results if "day" in (v.published_time_text or "").lower() or "week" in (v.published_time_text or "").lower())
    c_age = max(10.0, 100.0 - (recent_videos / n * 100.0))

    # 5. Content Saturation (10%)
    c_sat = min(100.0, float(n) * 5.0)

    # Weighted aggregate
    raw_score = (
        0.30 * c_authority +
        0.25 * c_views +
        0.20 * c_density +
        0.15 * c_age +
        0.10 * c_sat
    )
    final_score = int(round(min(100.0, max(0.0, raw_score))))

    breakdown = {
        "channel_authority_saturation": round(c_authority, 1),
        "median_views_density": round(c_views, 1),
        "title_keyword_density": round(c_density, 1),
        "incumbency_age_barrier": round(c_age, 1),
        "serp_saturation": round(c_sat, 1),
    }

    if c_authority > 60:
        reasons.append(f"Dominated by high-authority channels ({large_channels} of top {n} have high authority)")
    else:
        reasons.append(f"Favorable creator landscape: {n - large_channels} of top {n} are moderate-sized channels")

    if c_density > 60:
        reasons.append("Top ranking videos explicitly optimize for exact keyword")
    else:
        reasons.append("Weak title optimization detected in top search results (content gap)")

    if med_views > 100_000:
        reasons.append(f"High median view hurdle (~{med_views:,} views)")
    else:
        reasons.append(f"Accessible view benchmark: median {med_views:,} views in SERP")

    return final_score, breakdown, reasons
