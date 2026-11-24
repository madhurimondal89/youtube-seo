import pytest
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "TubePilot AI"

def test_system_status():
    resp = client.get("/api/system/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["app_name"] == "TubePilot AI"

def test_keyword_research_api():
    payload = {
        "seed": "youtube automation",
        "include_alphabet_expansion": True,
        "include_modifiers": True,
        "max_keywords": 15
    }
    resp = client.post("/api/research/keyword", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["seed"] == "youtube automation"
    assert len(data["keywords"]) > 0
    assert "opportunity_score" in data["keywords"][0]
    assert "estimated_competition" in data["keywords"][0]
    assert "relative_demand" in data["keywords"][0]

def test_video_audit_api():
    payload = {
        "title": "Mastering YouTube Keyword Research (Step by Step Guide)",
        "description": "Comprehensive tutorial on youtube keyword research with chapters and tips.\n00:00 - Intro\n03:00 - Setup",
        "tags": ["youtube keyword research", "youtube seo"],
        "target_keyword": "youtube keyword research"
    }
    resp = client.post("/api/audit/video", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert 0 <= data["overall_score"] <= 100
    assert len(data["categories"]) == 7

def test_ai_studio_title_generation():
    payload = {
        "topic": "YouTube SEO",
        "target_keyword": "YouTube SEO",
        "count": 5
    }
    resp = client.post("/api/ai/title", json=payload)
    assert resp.status_code == 200
    titles = resp.json()
    assert len(titles) == 5
    assert "seo_relevance_heuristic" in titles[0]
    assert "curiosity_heuristic" in titles[0]
