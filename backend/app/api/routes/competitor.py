from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.youtube.factory import get_youtube_provider
from app.models.channel import ChannelPerformanceMetrics, CompetitorComparisonResult
from app.models.video import OutlierVideoItem
from app.analytics.competitor_analyzer import analyze_channel_performance
from app.analytics.content_gap import detect_content_gaps
from app.analytics.outliers import detect_outliers_for_channel
from app.core.security import extract_channel_identifier
from app.models.common import DataProvenance

router = APIRouter(prefix="/competitor", tags=["Competitor"])

class ChannelAnalyzeRequest(BaseModel):
    channel_url_or_handle: str

class CompetitorCompareRequest(BaseModel):
    user_channel: str
    competitor_channels: list[str]

@router.post("/analyze", response_model=ChannelPerformanceMetrics)
async def analyze_channel(req: ChannelAnalyzeRequest):
    provider = get_youtube_provider()
    c_id = extract_channel_identifier(req.channel_url_or_handle)
    if not c_id:
        raise HTTPException(status_code=400, detail="Invalid channel URL or handle.")

    meta = await provider.get_channel_details(c_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Channel not found.")

    recent = await provider.get_channel_recent_videos(c_id, limit=25)
    return analyze_channel_performance(meta, recent)

@router.post("/compare", response_model=CompetitorComparisonResult)
async def compare_competitors(req: CompetitorCompareRequest):
    provider = get_youtube_provider()
    
    # 1. User channel
    u_id = extract_channel_identifier(req.user_channel) or req.user_channel
    u_meta = await provider.get_channel_details(u_id)
    u_vids = await provider.get_channel_recent_videos(u_id, limit=20)

    channels_list = [u_meta] if u_meta else []
    metrics_by_chan: dict[str, ChannelPerformanceMetrics] = {}
    
    if u_meta:
        metrics_by_chan[u_meta.channel_title] = analyze_channel_performance(u_meta, u_vids)

    # 2. Competitors
    all_comp_vids = []
    for comp in req.competitor_channels[:4]:
        c_id = extract_channel_identifier(comp) or comp
        c_meta = await provider.get_channel_details(c_id)
        if c_meta:
            channels_list.append(c_meta)
            c_vids = await provider.get_channel_recent_videos(c_id, limit=20)
            all_comp_vids.extend(c_vids)
            metrics_by_chan[c_meta.channel_title] = analyze_channel_performance(c_meta, c_vids)

    # 3. Detect content gaps
    user_median = metrics_by_chan[u_meta.channel_title].median_views if u_meta and u_meta.channel_title in metrics_by_chan else 20000
    gaps = detect_content_gaps(u_vids, all_comp_vids, channel_median_views=user_median)

    # Shared and unique topics
    user_topics = set(metrics_by_chan[u_meta.channel_title].top_performing_topics) if u_meta and u_meta.channel_title in metrics_by_chan else set()
    shared = []
    unique_by_chan: dict[str, list[str]] = {}

    for c_title, metrics in metrics_by_chan.items():
        comp_topics = set(metrics.top_performing_topics)
        unique_by_chan[c_title] = list(comp_topics)
        if c_title != (u_meta.channel_title if u_meta else ""):
            shared.extend(list(user_topics.intersection(comp_topics)))

    return CompetitorComparisonResult(
        channels=channels_list,
        metrics_by_channel=metrics_by_chan,
        shared_topics=list(set(shared)),
        unique_topics_by_channel=unique_by_chan,
        content_gaps=gaps,
        provenance=DataProvenance.CALCULATED,
    )

@router.get("/outliers", response_model=list[OutlierVideoItem])
async def get_outlier_videos(channel: str):
    provider = get_youtube_provider()
    c_id = extract_channel_identifier(channel) or channel
    videos = await provider.get_channel_recent_videos(c_id, limit=30)
    _, _, outliers = detect_outliers_for_channel(videos)
    return outliers
