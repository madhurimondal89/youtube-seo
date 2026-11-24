from pydantic import BaseModel, Field
from typing import Optional
from .common import DataProvenance

class AuditChecklistItem(BaseModel):
    id: str
    title: str
    passed: bool
    score_earned: float
    max_score: float
    feedback: str
    actionable_fix: Optional[str] = None
    severity: str  # "critical", "warning", "optimal"

class AuditCategoryScore(BaseModel):
    category_name: str
    earned_score: float
    max_score: float
    percentage: int
    items: list[AuditChecklistItem]

class VideoAuditResult(BaseModel):
    video_id: Optional[str] = None
    title: str
    overall_score: int = Field(ge=0, le=100)
    verdict: str  # "Excellent", "Good", "Needs Optimization", "Critical Issues"
    categories: list[AuditCategoryScore]
    action_plan: list[str]
    keywords_detected: list[str]
    estimated_readability: str
    curiosity_score: int
    provenance: DataProvenance = DataProvenance.CALCULATED

class ChannelAuditResult(BaseModel):
    channel_id: str
    channel_title: str
    overall_health_score: int = Field(ge=0, le=100)
    topic_consistency_score: int
    title_quality_score: int
    upload_cadence_score: int
    outlier_ratio: float
    recommendations: list[str]
    next_best_video_topics: list[str]
    provenance: DataProvenance = DataProvenance.CALCULATED
