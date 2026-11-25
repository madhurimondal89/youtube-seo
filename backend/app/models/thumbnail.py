from pydantic import BaseModel, Field
from typing import List, Optional

class VisualScoreBreakdown(BaseModel):
    visual_hierarchy_score: int = Field(..., ge=0, le=100)
    text_readability_score: int = Field(..., ge=0, le=100)
    subject_visibility_score: int = Field(..., ge=0, le=100)
    contrast_score: int = Field(..., ge=0, le=100)
    mobile_readability_score: int = Field(..., ge=0, le=100)
    composition_score: int = Field(..., ge=0, le=100)
    background_complexity_score: int = Field(..., ge=0, le=100)
    # Legacy compatibility fields
    aspect_ratio_score: Optional[int] = 100
    clarity_score: Optional[int] = 80
    focal_hierarchy_score: Optional[int] = 80

class VisualIssue(BaseModel):
    severity: str = "warning"  # "critical", "warning", "info"
    category: str
    issue: str
    suggestion: str

class ThumbnailAnalysisResponse(BaseModel):
    filename: str
    width: int
    height: int
    aspect_ratio_label: str
    is_standard_hd: bool
    overall_score: int = Field(..., ge=0, le=100)
    breakdown: VisualScoreBreakdown
    dominant_colors: List[str] = []
    average_brightness: float
    contrast_ratio: float
    issues: List[VisualIssue] = []
    recommendations: List[str] = []
    mobile_preview_advisory: str
    data_provenance: str = "Calculated"
    ctr_disclaimer: str = (
        "CTR Disclaimer: Vision heuristics evaluate graphic legibility, contrast, and layout composition standards. "
        "They do not and cannot predict actual real-world click-through rate (CTR), which depends on topic interest, audience targeting, and packaging synergy."
    )
    vision_ai_status: str = "Deterministic Vision Mode"
    vision_ai_insights: Optional[List[str]] = None
