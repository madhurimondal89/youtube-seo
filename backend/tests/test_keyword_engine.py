import pytest
from app.seo.keyword_engine import normalize_keyword, calculate_specificity_score, expand_keywords
from app.youtube.mock_provider import MockYouTubeProvider

def test_normalize_keyword():
    assert normalize_keyword("  YouTube Automation  2026! ") == "youtube automation 2026"
    assert normalize_keyword("HOW-TO RANK #1") == "how-to rank 1"

def test_specificity_score():
    assert calculate_specificity_score("seo") == 20
    assert calculate_specificity_score("youtube seo") == 40
    assert calculate_specificity_score("youtube seo guide") == 65
    assert calculate_specificity_score("youtube seo guide 2026") == 80
    assert calculate_specificity_score("best youtube seo guide for beginners") >= 86

@pytest.mark.asyncio
async def test_expand_keywords():
    provider = MockYouTubeProvider()
    results = await expand_keywords("youtube automation", provider=provider, max_keywords=20)
    assert len(results) > 5
    assert "youtube automation" in results
    assert any("tutorial" in kw for kw in results)
