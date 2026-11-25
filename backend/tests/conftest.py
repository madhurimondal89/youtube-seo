import os
os.environ["YOUTUBE_PROVIDER"] = "mock"
os.environ["AI_ENABLED"] = "false"

import pytest
from app.core.config import settings

settings.youtube_provider = "mock"
settings.ai_enabled = False

@pytest.fixture(autouse=True)
def configure_test_environment(monkeypatch):
    monkeypatch.setattr(settings, "youtube_provider", "mock")
    monkeypatch.setattr(settings, "ai_enabled", False)
