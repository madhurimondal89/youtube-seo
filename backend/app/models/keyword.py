from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from .common import DataProvenance

class SearchIntent(str, Enum):
    INFORMATIONAL = "Informational"
    TUTORIAL = "Tutorial"
    COMMERCIAL = "Commercial"
    TRANSACTIONAL = "Transactional"
    NAVIGATIONAL = "Navigational"
    ENTERTAINMENT = "Entertainment"
    NEWS_TRENDING = "News/Trending"
    COMPARISON = "Comparison"
    PROBLEM_FIX = "Problem/Fix"

class KeywordMetricItem(BaseModel):
    keyword: str
    intents: list[SearchIntent]
    search_surface: str = "YouTube Autocomplete"
    relative_demand: int = Field(ge=0, le=100, description="0-100 Relative demand index (not fake monthly volume)")
    estimated_competition: int = Field(ge=0, le=100, description="0-100 Estimated saturation index")
    opportunity_score: int = Field(ge=0, le=100, description="0-100 Transparent deterministic score")
    freshness_score: int = Field(ge=0, le=100)
    specificity_score: int = Field(ge=0, le=100)
    word_count: int
    char_count: int
    provenance: DataProvenance = DataProvenance.CALCULATED
    score_breakdown: dict[str, float] = Field(default_factory=dict)
    reasons: list[str] = Field(default_factory=list)

class TopicCluster(BaseModel):
    cluster_name: str
    main_keyword: str
    supporting_keywords: list[str]
    related_entities: list[str] = Field(default_factory=list)
    recommended_pillar_title: str
    supporting_video_ideas: list[str]
    playlist_suggestion: str
    avg_opportunity_score: int

class KeywordResearchRequest(BaseModel):
    seed: str = Field(min_length=1, max_length=120)
    include_alphabet_expansion: bool = True
    include_modifiers: bool = True
    include_questions: bool = True
    include_comparisons: bool = True
    max_keywords: int = 50

class KeywordResearchResponse(BaseModel):
    seed: str
    total_found: int
    keywords: list[KeywordMetricItem]
    clusters: list[TopicCluster] = Field(default_factory=list)
    top_opportunity_keywords: list[KeywordMetricItem] = Field(default_factory=list)
    data_provenance: DataProvenance = DataProvenance.CALCULATED
    execution_time_ms: float
