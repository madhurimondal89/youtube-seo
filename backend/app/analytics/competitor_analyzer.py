from typing import Optional
from datetime import datetime
from app.models.channel import ChannelMetadata, ChannelPerformanceMetrics, PublishingPatternAnalysis
from app.models.video import VideoMetadata
from app.analytics.outliers import detect_outliers_for_channel, calculate_median
from app.models.common import DataProvenance

def analyze_channel_performance(
    channel: ChannelMetadata,
    recent_videos: list[VideoMetadata]
) -> ChannelPerformanceMetrics:
    """
    Computes statistical channel overview and publishing patterns without accessing private analytics.
    """
    views_list = [v.views_count for v in recent_videos if v.views_count is not None]
    median_views, mad, outliers = detect_outliers_for_channel(recent_videos, channel.channel_title)
    
    mean_views = int(sum(views_list) / len(views_list)) if views_list else 0
    
    # Calculate durations
    durations = [v.duration_seconds for v in recent_videos if v.duration_seconds is not None]
    avg_duration = int(sum(durations) / len(durations)) if durations else 720

    # Upload frequency heuristic (assuming recent_videos span approx 2-4 months)
    upload_freq = round(min(30.0, max(1.0, len(recent_videos) / 2.5)), 1)

    # Extract top performing topics from titles
    topic_scores: dict[str, int] = {}
    for v in recent_videos:
        words = [w.lower() for w in v.title.split() if len(w) > 4]
        for w in words:
            topic_scores[w] = topic_scores.get(w, 0) + (v.views_count or 0)

    top_topics = sorted(topic_scores.keys(), key=lambda t: topic_scores[t], reverse=True)[:5]

    # Publishing Pattern Analysis
    day_counts: dict[str, int] = {
        "Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0
    }
    shorts_count = 0
    total_with_dur = len(durations)
    for d in durations:
        if d <= 60:
            shorts_count += 1
            
    shorts_ratio = int((shorts_count / max(1, total_with_dur)) * 100)
    longform_ratio = 100 - shorts_ratio

    # Approximate days based on published dates
    for v in recent_videos:
        if v.published_date:
            try:
                # Handle ISO timestamps or standard dates
                clean_date = v.published_date.split("T")[0]
                dt = datetime.strptime(clean_date, "%Y-%m-%d")
                day_name = dt.strftime("%A")
                if day_name in day_counts:
                    day_counts[day_name] += 1
            except Exception:
                pass

    # Find highest publishing day
    most_active = max(day_counts.keys(), key=lambda d: day_counts[d]) if any(day_counts.values()) else "Thursday"

    publishing_patterns = PublishingPatternAnalysis(
        most_active_day=most_active,
        day_distribution=day_counts,
        average_days_between_uploads=round(30.0 / max(1.0, upload_freq), 1),
        shorts_ratio_percent=shorts_ratio,
        longform_ratio_percent=longform_ratio
    )

    return ChannelPerformanceMetrics(
        median_views=median_views,
        mean_views=mean_views,
        mad_views=round(mad, 1),
        upload_frequency_per_month=upload_freq,
        average_duration_seconds=avg_duration,
        outlier_count=len(outliers),
        top_performing_topics=top_topics,
        recent_videos=recent_videos[:10],
        outliers=outliers,
        publishing_patterns=publishing_patterns,
        provenance=DataProvenance.CALCULATED,
    )
