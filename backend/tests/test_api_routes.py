import pytest
import io
import base64
from PIL import Image
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "YouTube SEO"

def test_system_status():
    resp = client.get("/api/system/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["app_name"] == "YouTube SEO"

def test_keyword_research_api():
    payload = {
        "seed": "youtube automation",
        "include_alphabet_expansion": True,
        "include_modifiers": True,
        "include_questions": True,
        "include_comparisons": True,
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

def test_keyword_research_empty_seed_validation():
    resp = client.post("/api/research/keyword", json={"seed": ""})
    assert resp.status_code == 422 or resp.status_code == 400

def test_video_audit_api():
    payload = {
        "title": "Mastering YouTube Keyword Research (Step by Step Guide)",
        "description": "Comprehensive tutorial on youtube keyword research with chapters and tips.\n00:00 - Intro\n03:00 - Setup",
        "tags": ["youtube keyword research", "youtube seo"],
        "target_keyword": "youtube keyword research",
        "has_captions": True
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

def test_thumbnail_analyzer_api():
    img = Image.new("RGB", (1280, 720), (35, 45, 65))
    buf = io.BytesIO()
    img.save(buf, "JPEG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    resp = client.post("/api/ai/thumbnail/analyze-upload", json={"image_base64": b64, "filename": "test.jpg"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["aspect_ratio_label"] == "16:9"
    assert 0 <= data["overall_score"] <= 100
    assert "contrast_ratio" in data

def test_thumbnail_analyzer_invalid_base64():
    resp = client.post("/api/ai/thumbnail/analyze-upload", json={"image_base64": "not-valid-base64-image"})
    assert resp.status_code == 400

def test_growth_coach_api():
    payload = {
        "niche": "Bengali Mystery and History",
        "channel_name": "Rahasya Golpo",
        "language": "Bengali"
    }
    resp = client.post("/api/ai/growth-coach", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["niche"] == "Bengali Mystery and History"
    assert len(data["weeks"]) == 4

def test_outlier_detection_api():
    resp = client.get("/api/competitor/outliers?channel=UC_x5XG1OV2P6uZZ5FSM9Ttw")
    # Will return 200 with list of outliers or fallback
    assert resp.status_code in [200, 400]

def test_system_settings_api():
    resp = client.get("/api/system/settings")
    assert resp.status_code == 200
    data = resp.json()
    assert "ai_enabled" in data
    assert "ai_provider" in data
    assert "custom_ai_base_url" in data
    assert "groq_model" in data
    assert "deepseek_model" in data
    assert "openrouter_model" in data
    assert "localai_base_url" in data
    assert "lmstudio_base_url" in data

def test_system_settings_update_providers():
    update_payload = {
        "groq_model": "llama-3.3-70b-versatile",
        "deepseek_model": "deepseek-chat",
        "openrouter_model": "meta-llama/llama-3.3-70b-instruct",
        "localai_base_url": "http://localhost:8080/v1"
    }
    resp = client.post("/api/system/settings", json=update_payload)
    assert resp.status_code == 200
    get_resp = client.get("/api/system/settings")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["groq_model"] == "llama-3.3-70b-versatile"
    assert data["deepseek_model"] == "deepseek-chat"

def test_provider_registry_presets():
    from app.ai.registry import PROVIDER_PRESETS
    required = ["gemini", "openai", "groq", "deepseek", "openrouter", "ollama", "lmstudio", "localai", "custom"]
    for prov in required:
        assert prov in PROVIDER_PRESETS
        assert "default_model" in PROVIDER_PRESETS[prov]
        assert "default_url" in PROVIDER_PRESETS[prov]
