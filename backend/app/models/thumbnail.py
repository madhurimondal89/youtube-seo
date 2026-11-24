from pydantic import BaseModel, Field
from typing import List, Optional

class VisualScoreBreakdown(BaseModel):
    aspect_ratio_score: int = Field(..., ge=0, le=100)
    contrast_score: int = Field(..., ge=0, le=100)
    clarity_score: int = Field(..., ge=0, le=100)
    mobile_readability_score: int = Field(..., ge=0, le=100)
    focal_hierarchy_score: int = Field(..., ge=0, le=100)

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
