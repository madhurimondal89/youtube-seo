from pydantic import BaseModel, Field
from typing import Optional
from .common import DataProvenance
from .video import VideoMetadata, OutlierVideoItem

class ChannelMetadata(BaseModel):
    channel_id: str
    channel_title: str
    handle: Optional[str] = None
    description: Optional[str] = None
    subscriber_count: Optional[int] = None
    video_count: Optional[int] = None
    view_count: Optional[int] = None
    avatar_url: Optional[str] = None
    banner_url: Optional[str] = None
    provenance: DataProvenance = DataProvenance.PUBLIC

class PublishingPatternAnalysis(BaseModel):
    most_active_day: str = "Thursday"
    day_distribution: dict[str, int] = Field(default_factory=dict)
    average_days_between_uploads: float = 4.2
    shorts_ratio_percent: int = 20
    longform_ratio_percent: int = 80

class ChannelPerformanceMetrics(BaseModel):
    median_views: int
    mean_views: int
    mad_views: float  # Median Absolute Deviation
    upload_frequency_per_month: float
    average_duration_seconds: int
    outlier_count: int
    top_performing_topics: list[str] = Field(default_factory=list)
    recent_videos: list[VideoMetadata] = Field(default_factory=list)
    outliers: list[OutlierVideoItem] = Field(default_factory=list)
    publishing_patterns: Optional[PublishingPatternAnalysis] = None
    provenance: DataProvenance = DataProvenance.CALCULATED

class CompetitorComparisonResult(BaseModel):
    channels: list[ChannelMetadata]
    metrics_by_channel: dict[str, ChannelPerformanceMetrics]
    shared_topics: list[str]
    unique_topics_by_channel: dict[str, list[str]]
    content_gaps: list[dict]
    provenance: DataProvenance = DataProvenance.CALCULATED
