from app.seo.competition import calculate_estimated_competition
from app.seo.opportunity import calculate_relative_demand, calculate_opportunity_score
from app.models.keyword import SearchIntent
from app.models.video import VideoSearchResult

def test_relative_demand_range():
    score = calculate_relative_demand("youtube automation", "youtube automation", autocomplete_rank=1)
    assert 0 <= score <= 100
    assert score > 60

def test_competition_scoring():
    serp = [
        VideoSearchResult(
            video_id=f"vid_{i}", title=f"YouTube Automation Guide {i}",
            channel_name=f"Channel {i}", views_count=100000 + i * 20000,
            rank_position=i + 1
        ) for i in range(10)
    ]
    comp_score, breakdown, reasons = calculate_estimated_competition("youtube automation", serp)
    assert 0 <= comp_score <= 100
    assert "channel_authority_saturation" in breakdown
    assert len(reasons) > 0

def test_opportunity_score_transparent_breakdown():
    opp_score, breakdown, reasons = calculate_opportunity_score(
        keyword="youtube automation for beginners",
        relative_demand=80,
        estimated_competition=40,
        specificity=75,
        intents=[SearchIntent.TUTORIAL],
    )
    assert 0 <= opp_score <= 100
    assert "demand_signal" in breakdown
    assert "competition_opportunity" in breakdown
    assert len(reasons) > 0
