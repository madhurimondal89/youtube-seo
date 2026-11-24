from typing import Optional
from app.models.channel import ChannelMetadata, ChannelPerformanceMetrics
from app.models.video import VideoMetadata
from app.analytics.outliers import detect_outliers_for_channel, calculate_median
from app.models.common import DataProvenance

def analyze_channel_performance(
    channel: ChannelMetadata,
    recent_videos: list[VideoMetadata]
) -> ChannelPerformanceMetrics:
    """
    Computes statistical channel overview without accessing private analytics.
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
        provenance=DataProvenance.CALCULATED,
    )
