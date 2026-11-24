from pydantic import BaseModel, Field
from typing import Optional
from .common import DataProvenance

class VideoSearchResult(BaseModel):
    video_id: str
    title: str
    channel_name: str
    channel_id: Optional[str] = None
    published_time_text: Optional[str] = None
    published_timestamp: Optional[int] = None
    views_count: Optional[int] = None
    views_text: Optional[str] = None
    duration_text: Optional[str] = None
    duration_seconds: Optional[int] = None
    thumbnail_url: Optional[str] = None
    description_snippet: Optional[str] = None
    rank_position: int
    provenance: DataProvenance = DataProvenance.PUBLIC

class VideoMetadata(BaseModel):
    video_id: str
    url: str
    title: str
    description: str
    channel_id: Optional[str] = None
    channel_name: str
    channel_subscribers: Optional[int] = None
    published_date: Optional[str] = None
    views_count: Optional[int] = None
    likes_count: Optional[int] = None
    comments_count: Optional[int] = None
    duration_seconds: Optional[int] = None
    tags: list[str] = Field(default_factory=list)
    thumbnail_url: Optional[str] = None
    has_chapters: bool = False
    has_captions: bool = False
    provenance: DataProvenance = DataProvenance.PUBLIC

class OutlierVideoItem(BaseModel):
    video_id: str
    title: str
    channel_name: str
    views: int
    channel_median_views: int
    multiplier: float
    multiplier_text: str  # e.g., "14.5x channel average"
    tier: str             # "Viral Outlier", "High Outlier", "Solid Outlier", "Expected"
    z_score: float
    published_date: Optional[str] = None
    thumbnail_url: Optional[str] = None
    primary_topic: Optional[str] = None
    provenance: DataProvenance = DataProvenance.CALCULATED
