import pytest
from app.ai.coach import generate_growth_strategy
from app.ai.cloud_provider import DisabledAIProvider

@pytest.mark.asyncio
async def test_growth_coach_deterministic_strategy():
    provider = DisabledAIProvider()
    strategy = await generate_growth_strategy(
        niche="Bengali Mystery and History",
        channel_name="Rahasya Golpo",
        language="Bengali",
        ai_provider=provider
    )
    
    assert strategy.niche == "Bengali Mystery and History"
    assert len(strategy.weeks) == 4
    assert len(strategy.weeks[0].videos) >= 2
    assert strategy.weeks[0].videos[0].hook_script != ""
    assert strategy.weeks[0].videos[0].thumbnail_concept != ""
    assert len(strategy.publishing_checklist) > 0
    assert len(strategy.weekly_review_metrics) > 0
