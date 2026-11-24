from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.models.audit import VideoAuditResult, ChannelAuditResult
from app.youtube.factory import get_youtube_provider
from app.seo.audit_engine import audit_video_seo, audit_channel_seo
from app.core.security import extract_video_id, extract_channel_identifier

router = APIRouter(prefix="/audit", tags=["Audit"])

class VideoAuditRequest(BaseModel):
    video_url_or_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = Field(default_factory=list)
    target_keyword: Optional[str] = None
    has_captions: Optional[bool] = False

class ChannelAuditRequest(BaseModel):
    channel_url_or_handle: str

@router.post("/video", response_model=VideoAuditResult)
async def audit_video(req: VideoAuditRequest):
    provider = get_youtube_provider()

    title = req.title or ""
    description = req.description or ""
    tags = req.tags or []
    vid_id = None
    has_chapters = False
    has_captions = req.has_captions or False

    # If a URL or ID is given, attempt to fetch live metadata
    if req.video_url_or_id:
        vid_id = extract_video_id(req.video_url_or_id)
        if vid_id:
            meta = await provider.get_video_details(vid_id)
            if meta:
                title = title or meta.title
                description = description or meta.description
                tags = tags or meta.tags
                has_chapters = meta.has_chapters
                has_captions = meta.has_captions or has_captions

    if not title:
        if vid_id:
            raise HTTPException(
                status_code=400,
                detail=f"Video '{vid_id}' is unavailable or private on YouTube. Please verify the URL, or switch to 'Manual Metadata Input' to audit your video drafts."
            )
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid YouTube video URL or enter the title and description manually."
        )


    return audit_video_seo(
        title=title,
        description=description,
        tags=tags,
        target_keyword=req.target_keyword,
        video_id=vid_id,
        has_chapters=has_chapters,
        has_captions=has_captions
    )

@router.post("/channel", response_model=ChannelAuditResult)
async def audit_channel(req: ChannelAuditRequest):
    provider = get_youtube_provider()
    c_id = extract_channel_identifier(req.channel_url_or_handle)
    if not c_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube channel URL or handle.")

    meta = await provider.get_channel_details(c_id)
    title = meta.channel_title if meta else c_id
    subscribers = meta.subscriber_count if meta else None

    # Fetch recent videos for analysis
    recent_videos_meta = await provider.get_channel_recent_videos(c_id, limit=20)
    videos_dicts = [
        {"title": v.title, "views_count": v.views_count}
        for v in recent_videos_meta
    ]

    return audit_channel_seo(
        channel_id=c_id,
        channel_title=title,
        recent_videos=videos_dicts,
        subscriber_count=subscribers
    )
