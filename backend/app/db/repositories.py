import uuid
import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from app.db.database import get_connection

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# --- Keyword Projects ---
def save_keyword_project(title: str, seed: str, data: Dict[str, Any]) -> str:
    proj_id = f"kw_{uuid.uuid4().hex[:12]}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO keyword_projects (id, title, seed, total_keywords, data_json, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        proj_id,
        title.strip() or f"Research: {seed}",
        seed.strip(),
        len(data.get("keywords", [])),
        json.dumps(data),
        now_iso(),
        now_iso()
    ))
    conn.commit()
    conn.close()
    return proj_id

def list_keyword_projects() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, seed, total_keywords, created_at FROM keyword_projects ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_keyword_project(proj_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keyword_projects WHERE id = ?", (proj_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    res = dict(row)
    res["data"] = json.loads(res["data_json"])
    return res

def delete_keyword_project(proj_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keyword_projects WHERE id = ?", (proj_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- Competitor Watchlists ---
def add_competitor_watchlist(channel_id: str, channel_name: str, median_views: int = 0, subscriber_count: str = "N/A", notes: str = "") -> str:
    item_id = f"comp_{uuid.uuid4().hex[:12]}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO competitor_watchlists (id, channel_id, channel_name, median_views, subscriber_count, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (item_id, channel_id, channel_name, median_views, subscriber_count, notes, now_iso()))
    conn.commit()
    conn.close()
    return item_id

def list_competitor_watchlists() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM competitor_watchlists ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_competitor_watchlist(item_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM competitor_watchlists WHERE id = ?", (item_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- Saved Video Audits ---
def save_audit(video_title: str, video_url: str, overall_score: int, audit_data: Dict[str, Any]) -> str:
    audit_id = f"aud_{uuid.uuid4().hex[:12]}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO saved_audits (id, video_title, video_url, overall_score, audit_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (audit_id, video_title, video_url, overall_score, json.dumps(audit_data), now_iso()))
    conn.commit()
    conn.close()
    return audit_id

def list_saved_audits() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, video_title, video_url, overall_score, created_at FROM saved_audits ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_saved_audit(audit_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_audits WHERE id = ?", (audit_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    res = dict(row)
    res["audit"] = json.loads(res["audit_json"])
    return res

def delete_saved_audit(audit_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_audits WHERE id = ?", (audit_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- Content Calendars & Growth Plans ---
def save_calendar_strategy(niche: str, strategy: Dict[str, Any], channel_name: Optional[str] = None, language: str = "English") -> str:
    cal_id = f"cal_{uuid.uuid4().hex[:12]}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO content_calendars (id, niche, channel_name, language, strategy_json, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (cal_id, niche, channel_name, language, json.dumps(strategy), now_iso()))
    conn.commit()
    conn.close()
    return cal_id

def list_calendar_strategies() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, niche, channel_name, language, created_at FROM content_calendars ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_calendar_strategy(cal_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM content_calendars WHERE id = ?", (cal_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    res = dict(row)
    res["strategy"] = json.loads(res["strategy_json"])
    return res

def delete_calendar_strategy(cal_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM content_calendars WHERE id = ?", (cal_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- AI History Logging ---
def log_ai_generation(feature: str, prompt: str, response_text: str, provider: str = "Unknown") -> str:
    entry_id = f"ai_{uuid.uuid4().hex[:12]}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO ai_history (id, feature, prompt, response_text, provider, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (entry_id, feature, prompt, response_text, provider, now_iso()))
    conn.commit()
    conn.close()
    return entry_id

def get_recent_ai_history(limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ai_history ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
