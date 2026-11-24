from app.analytics.outliers import detect_outliers_for_channel, calculate_median, calculate_mad
from app.models.video import VideoMetadata

def test_median_and_mad():
    data = [10, 12, 11, 13, 12, 100]  # with severe outlier 100
    med = calculate_median(data)
    assert med == 12.0
    mad = calculate_mad(data, med)
    assert mad == 1.0

def test_detect_outliers():
    videos = [
        VideoMetadata(
            video_id=f"v_{i}", url=f"https://youtube.com/watch?v=v_{i}",
            title=f"Video {i}", description="desc", channel_name="TestChan",
            views_count=20000 if i != 5 else 300000  # 15x outlier
        ) for i in range(15)
    ]
    median_v, mad, outliers = detect_outliers_for_channel(videos)
    assert median_v == 20000
    assert len(outliers) == 1
    assert outliers[0].multiplier >= 15.0
    assert outliers[0].tier == "Viral Outlier"
