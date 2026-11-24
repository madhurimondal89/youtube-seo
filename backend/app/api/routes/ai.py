from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import httpx
import base64
from app.analytics.thumbnail_analyzer import analyze_thumbnail_bytes
from app.models.thumbnail import ThumbnailAnalysisResponse
from app.ai.coach import generate_growth_strategy, GrowthStrategyResponse
from app.ai.studio import ai_studio
from app.ai.ollama_provider import LocalOllamaProvider
from app.ai.cloud_provider import (
    OptionalOpenAIProvider,
    DisabledAIProvider,
    CustomOpenAICompatibleProvider,
    GoogleGeminiProvider,
)
from app.core.config import settings
from app.models.ai_dtos import (
    TitleIdea,
    DescriptionRequest,
    DescriptionResponse,
    TagGenerationRequest,
    TagGenerationResponse,
    HookGenerationRequest,
    VideoHookItem,
    ContentCalendarResponse,
)

router = APIRouter(prefix="/ai", tags=["AI Studio"])

def get_current_ai_provider():
    if not settings.ai_enabled:
        return DisabledAIProvider()
    
    provider_type = settings.ai_provider.lower().strip()
    
    if provider_type == "ollama":
        return LocalOllamaProvider(base_url=settings.ollama_base_url, model=settings.ollama_model)
    elif provider_type == "custom":
        return CustomOpenAICompatibleProvider(
            base_url=settings.custom_ai_base_url,
            model=settings.custom_ai_model,
            api_key=settings.custom_ai_api_key,
        )
    elif provider_type == "gemini":
        return GoogleGeminiProvider(
            api_key=settings.gemini_api_key or "",
            model=settings.gemini_model,
        )
    elif provider_type == "openai" and settings.openai_api_key:
        return OptionalOpenAIProvider(api_key=settings.openai_api_key, model=settings.openai_model)
        
    return DisabledAIProvider()

class TitleRequest(BaseModel):
    topic: str
    target_keyword: Optional[str] = None
    count: int = 12

@router.post("/title", response_model=list[TitleIdea])
async def generate_titles(req: TitleRequest):
    provider = get_current_ai_provider()
    kw = req.target_keyword or req.topic
    return await ai_studio.generate_title_ideas(
        topic=req.topic,
        keyword=kw,
        ai_provider=provider,
        count=req.count
    )

@router.post("/description", response_model=DescriptionResponse)
async def generate_description(req: DescriptionRequest):
    return await ai_studio.generate_description(
        topic=req.topic,
        target_keywords=req.target_keywords,
        call_to_action=req.call_to_action or "Subscribe for more practical creator guides",
        chapters_requested=req.chapters_requested
    )

@router.post("/tags", response_model=TagGenerationResponse)
async def generate_tags(req: TagGenerationRequest):
    return ai_studio.generate_tags(
        title=req.title,
        topic=req.topic,
        target_keyword=req.target_keyword
    )

@router.post("/hooks", response_model=list[VideoHookItem])
async def generate_hooks(req: HookGenerationRequest):
    return ai_studio.generate_hooks(
        topic=req.topic,
        target_audience=req.target_audience
    )

class CalendarRequest(BaseModel):
    topic: str
    duration_days: int = 30

@router.post("/calendar", response_model=ContentCalendarResponse)
async def generate_content_calendar(req: CalendarRequest):
    return ai_studio.generate_content_calendar(
        topic=req.topic,
        duration_days=req.duration_days
    )

class ThumbnailUrlRequest(BaseModel):
    url: str

class ThumbnailBase64Request(BaseModel):
    image_base64: str
    filename: Optional[str] = "uploaded_thumbnail.jpg"

@router.post("/thumbnail/analyze-upload", response_model=ThumbnailAnalysisResponse)
async def analyze_thumbnail_upload(req: ThumbnailBase64Request):
    raw_b64 = req.image_base64
    if "," in raw_b64:
        raw_b64 = raw_b64.split(",", 1)[1]
    try:
        content = base64.b64decode(raw_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image data.")
        
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Thumbnail image size exceeds 10MB limit.")
    try:
        return analyze_thumbnail_bytes(content, filename=req.filename or "uploaded_thumbnail.jpg")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")

@router.post("/thumbnail/analyze-url", response_model=ThumbnailAnalysisResponse)
async def analyze_thumbnail_url(req: ThumbnailUrlRequest):
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(req.url)
            if resp.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Failed to fetch image from URL: HTTP {resp.status_code}")
            content = resp.content
            return analyze_thumbnail_bytes(content, filename="remote_thumbnail.jpg")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving image: {str(e)}")

class CoachRequest(BaseModel):
    niche: str
    channel_name: Optional[str] = None
    language: str = "English"

@router.post("/growth-coach", response_model=GrowthStrategyResponse)
async def run_growth_coach(req: CoachRequest):
    provider = get_current_ai_provider()
    return await generate_growth_strategy(
        niche=req.niche,
        channel_name=req.channel_name,
        language=req.language,
        ai_provider=provider
    )

