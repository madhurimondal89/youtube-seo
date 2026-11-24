from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime, timezone

class DataProvenance(str, Enum):
    OFFICIAL = "Official"            # Direct from YouTube Data API v3
    PUBLIC = "Public"                # Publicly observable on YouTube web surface
    CALCULATED = "Calculated"        # Derived mathematically from public/official signals
    ESTIMATED = "Estimated"          # Statistical/heuristic estimate
    RELATIVE = "Relative"            # Relative comparative scale (0-100)
    UNAVAILABLE = "Unavailable"      # Signal cannot be reliably sourced

class ProvenanceValue(BaseModel):
    value: Any
    provenance: DataProvenance
    confidence: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)
    explanation: Optional[str] = None

class SystemStatus(BaseModel):
    app_name: str
    version: str
    environment: str
    ai_enabled: bool
    ai_provider: str
    ai_status: str
    youtube_provider: str
    cache_size: int
    uptime_seconds: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

