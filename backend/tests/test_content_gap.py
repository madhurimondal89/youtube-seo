from app.analytics.content_gap import detect_content_gaps
from app.models.video import VideoMetadata

def test_detect_content_gaps():
    user_vids = [
        VideoMetadata(
            video_id="u1", url="u1", title="Basics of Premiere Pro",
            description="desc", channel_name="UserChan", views_count=15000
        )
    ]
    comp_vids = [
        VideoMetadata(
            video_id="c1", url="c1", title="DaVinci Resolve Color Grading Mastery",
            description="desc", channel_name="CompChan", views_count=220000 # gap topic!
        ),
        VideoMetadata(
            video_id="c2", url="c2", title="Basics of Premiere Pro Tutorial",
            description="desc", channel_name="CompChan", views_count=18000
        )
    ]
    gaps = detect_content_gaps(user_vids, comp_vids, channel_median_views=15000)
    assert len(gaps) >= 1
    # First gap should be DaVinci Resolve
    assert "davinci" in gaps[0]["topic_title"].lower()
    assert gaps[0]["opportunity_tier"] == "HIGH OPPORTUNITY"
