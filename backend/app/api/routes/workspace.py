from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.db import repositories

router = APIRouter(prefix="/workspace", tags=["Workspace Projects"])

# --- Models ---
class SaveKeywordProjectRequest(BaseModel):
    title: Optional[str] = None
    seed: str
    data: Dict[str, Any]

class SaveCompetitorWatchlistRequest(BaseModel):
    channel_id: str
    channel_name: str
    median_views: int = 0
    subscriber_count: Optional[str] = "N/A"
    notes: Optional[str] = ""

class SaveAuditRequest(BaseModel):
    video_title: str
    video_url: Optional[str] = None
    overall_score: int
    audit_data: Dict[str, Any]

class SaveCalendarRequest(BaseModel):
    niche: str
    strategy: Dict[str, Any]
    channel_name: Optional[str] = None
    language: str = "English"

# --- Keyword Projects ---
@router.post("/keywords")
def save_keywords(req: SaveKeywordProjectRequest):
    proj_id = repositories.save_keyword_project(req.title or f"Research: {req.seed}", req.seed, req.data)
    return {"status": "success", "id": proj_id, "message": "Keyword project saved to workspace."}

@router.get("/keywords")
def list_keywords():
    return repositories.list_keyword_projects()

@router.get("/keywords/{project_id}")
def get_keywords(project_id: str):
    proj = repositories.get_keyword_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found.")
    return proj

@router.delete("/keywords/{project_id}")
def delete_keywords(project_id: str):
    success = repositories.delete_keyword_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found.")
    return {"status": "success", "message": "Project deleted."}

# --- Competitor Watchlists ---
@router.post("/competitors")
def add_competitor(req: SaveCompetitorWatchlistRequest):
    item_id = repositories.add_competitor_watchlist(
        channel_id=req.channel_id,
        channel_name=req.channel_name,
        median_views=req.median_views,
        subscriber_count=req.subscriber_count or "N/A",
        notes=req.notes or ""
    )
    return {"status": "success", "id": item_id, "message": "Channel added to competitor watchlist."}

@router.get("/competitors")
def list_competitors():
    return repositories.list_competitor_watchlists()

@router.delete("/competitors/{item_id}")
def delete_competitor(item_id: str):
    success = repositories.delete_competitor_watchlist(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Competitor not found.")
    return {"status": "success", "message": "Competitor removed from watchlist."}

# --- Audits ---
@router.post("/audits")
def save_audit(req: SaveAuditRequest):
    audit_id = repositories.save_audit(req.video_title, req.video_url or "", req.overall_score, req.audit_data)
    return {"status": "success", "id": audit_id, "message": "SEO audit saved."}

@router.get("/audits")
def list_audits():
    return repositories.list_saved_audits()

@router.get("/audits/{audit_id}")
def get_audit(audit_id: str):
    audit = repositories.get_saved_audit(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit report not found.")
    return audit

@router.delete("/audits/{audit_id}")
def delete_audit(audit_id: str):
    success = repositories.delete_saved_audit(audit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Audit not found.")
    return {"status": "success", "message": "Audit deleted."}

# --- Content Calendars ---
@router.post("/calendars")
def save_calendar(req: SaveCalendarRequest):
    cal_id = repositories.save_calendar_strategy(req.niche, req.strategy, req.channel_name, req.language)
    return {"status": "success", "id": cal_id, "message": "Content strategy saved."}

@router.get("/calendars")
def list_calendars():
    return repositories.list_calendar_strategies()

@router.get("/calendars/{cal_id}")
def get_calendar(cal_id: str):
    cal = repositories.get_calendar_strategy(cal_id)
    if not cal:
        raise HTTPException(status_code=404, detail="Content strategy not found.")
    return cal

@router.delete("/calendars/{cal_id}")
def delete_calendar(cal_id: str):
    success = repositories.delete_calendar_strategy(cal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Strategy not found.")
    return {"status": "success", "message": "Strategy deleted."}

# --- AI History ---
@router.get("/ai-history")
def list_ai_history():
    return repositories.get_recent_ai_history()
