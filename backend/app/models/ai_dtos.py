from pydantic import BaseModel, Field
from typing import Optional

class TitleIdea(BaseModel):
    title: str
    seo_relevance_heuristic: int = Field(ge=0, le=100)
    curiosity_heuristic: int = Field(ge=0, le=100)
    character_count: int
    has_number: bool
    frontloaded_keyword: bool
    style: str  # "How-to", "Contrarian", "Case Study", "Numbered List"

class DescriptionRequest(BaseModel):
    topic: str
    target_keywords: list[str]
    call_to_action: Optional[str] = "Subscribe for more practical guides"
    chapters_requested: bool = True
    tone: Optional[str] = "Professional and engaging"

class DescriptionResponse(BaseModel):
    full_description: str
    hook_first_lines: str
    chapters_placeholder: str
    suggested_hashtags: list[str]
    keyword_coverage: list[str]

class TagGenerationRequest(BaseModel):
    title: str
    topic: str
    target_keyword: Optional[str] = None

class TagGenerationResponse(BaseModel):
    primary_tags: list[str]
    secondary_tags: list[str]
    long_tail_tags: list[str]
    total_tags: int
    char_count: int

class HookGenerationRequest(BaseModel):
    topic: str
    target_audience: str = "Beginner to intermediate creators"
    format_type: str = "Tutorial"

class VideoHookItem(BaseModel):
    hook_type: str  # "Story/Curiosity", "Bold Claim", "Problem First", "Contrarian"
    first_3_seconds: str
    next_15_seconds: str
    open_loop: str

class ContentCalendarDay(BaseModel):
    day: int
    title: str
    target_keyword: str
    intent: str
    content_type: str  # "Evergreen", "Trend", "Hero Pillar", "Quick Win"
    production_effort: str  # "Low", "Medium", "High"

class ContentCalendarResponse(BaseModel):
    duration_days: int
    schedule: list[ContentCalendarDay]
    strategy_summary: str
