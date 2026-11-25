import os
import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

DB_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_PATH = DB_DIR / "youtube_seo.db"

def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes schema and tables for persistent workspace data."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. User Profiles & Preferences
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        username TEXT,
        niche TEXT,
        language TEXT DEFAULT 'English',
        preferences_json TEXT,
        created_at TEXT
    )
    """)

    # 2. Keyword Projects & Research
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS keyword_projects (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        seed TEXT NOT NULL,
        total_keywords INTEGER DEFAULT 0,
        data_json TEXT NOT NULL,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    # 3. Competitor Watchlists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS competitor_watchlists (
        id TEXT PRIMARY KEY,
        channel_id TEXT NOT NULL,
        channel_name TEXT NOT NULL,
        median_views INTEGER DEFAULT 0,
        subscriber_count TEXT,
        notes TEXT,
        created_at TEXT
    )
    """)

    # 4. Saved Video SEO Audits
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_audits (
        id TEXT PRIMARY KEY,
        video_title TEXT NOT NULL,
        video_url TEXT,
        overall_score INTEGER NOT NULL,
        audit_json TEXT NOT NULL,
        created_at TEXT
    )
    """)

    # 5. Content Calendars & Growth Plans
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS content_calendars (
        id TEXT PRIMARY KEY,
        niche TEXT NOT NULL,
        channel_name TEXT,
        language TEXT,
        strategy_json TEXT NOT NULL,
        created_at TEXT
    )
    """)

    # 6. AI Conversation & Generation History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_history (
        id TEXT PRIMARY KEY,
        feature TEXT NOT NULL,
        prompt TEXT NOT NULL,
        response_text TEXT NOT NULL,
        provider TEXT,
        created_at TEXT
    )
    """)

    # 7. Connected Channels & Analytics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS connected_channels (
        id TEXT PRIMARY KEY,
        channel_id TEXT UNIQUE NOT NULL,
        channel_title TEXT NOT NULL,
        custom_url TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# Auto-initialize tables upon module import
init_db()
