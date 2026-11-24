import math
from typing import Optional
from app.models.video import VideoMetadata, OutlierVideoItem
from app.models.common import DataProvenance

def calculate_median(values: list[float | int]) -> float:
    if not values:
        return 0.0
    sorted_v = sorted(values)
    n = len(sorted_v)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_v[mid])
    return float(sorted_v[mid - 1] + sorted_v[mid]) / 2.0

def calculate_mad(values: list[float | int], median: float) -> float:
    """Median Absolute Deviation (MAD): median(|x_i - median|)."""
    if not values:
        return 0.0
    deviations = [abs(v - median) for v in values]
    return calculate_median(deviations)

def detect_outliers_for_channel(
    videos: list[VideoMetadata],
    channel_name: Optional[str] = None
) -> tuple[int, float, list[OutlierVideoItem]]:
    """
    Computes statistical outliers using Median and MAD.
    Never relies solely on arithmetic mean.
    Returns: (median_views, mad_views, list_of_outliers)
    """
    valid_videos = [v for v in videos if v.views_count is not None and v.views_count > 0]
    if not valid_videos:
        return 0, 0.0, []

    views_list = [v.views_count for v in valid_videos]
    med_views = calculate_median(views_list)
    baseline_median = max(1.0, med_views)
    mad = calculate_mad(views_list, med_views)

    outliers: list[OutlierVideoItem] = []

    for v in valid_videos:
        views = v.views_count
        multiplier = round(views / baseline_median, 2)
        
        # Robust z-score approximation
        z_score = round(0.6745 * (views - med_views) / max(1.0, mad), 2)

        # Classification thresholds
        if multiplier >= 10.0 or z_score >= 5.0:
            tier = "Viral Outlier"
        elif multiplier >= 5.0 or z_score >= 3.0:
            tier = "High Outlier"
        elif multiplier >= 2.5:
            tier = "Solid Outlier"
        elif multiplier >= 0.5:
            tier = "Expected"
        else:
            tier = "Underperforming"

        # Record items with multiplier >= 2.0 as notable outliers
        if multiplier >= 2.0:
            outliers.append(
                OutlierVideoItem(
                    video_id=v.video_id,
                    title=v.title,
                    channel_name=v.channel_name or (channel_name or "Creator"),
                    views=views,
                    channel_median_views=int(baseline_median),
                    multiplier=multiplier,
                    multiplier_text=f"{multiplier}x channel average",
                    tier=tier,
                    z_score=z_score,
                    published_date=v.published_date,
                    thumbnail_url=v.thumbnail_url,
                    primary_topic=v.tags[0] if v.tags else None,
                    provenance=DataProvenance.CALCULATED,
                )
            )

    # Sort outliers descending by multiplier
    outliers.sort(key=lambda o: o.multiplier, reverse=True)
    return int(baseline_median), mad, outliers
