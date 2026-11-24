import pytest
import io
from PIL import Image, ImageDraw
from app.analytics.thumbnail_analyzer import analyze_thumbnail_bytes
from app.models.thumbnail import ThumbnailAnalysisResponse

def create_sample_thumbnail(width=1280, height=720, bg_color=(20, 25, 40)):
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Draw high contrast focal element
    draw.rectangle([100, 100, 500, 400], fill=(255, 200, 0))
    # Draw contrasting shape
    draw.ellipse([700, 200, 1100, 600], fill=(220, 20, 60))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=90)
    return buffer.getvalue()

def test_thumbnail_deterministic_analysis():
    image_bytes = create_sample_thumbnail(1280, 720)
    result = analyze_thumbnail_bytes(image_bytes, filename="test_thumb.jpg")
    
    assert isinstance(result, ThumbnailAnalysisResponse)
    assert result.overall_score >= 0 and result.overall_score <= 100
    assert result.aspect_ratio_label == "16:9"
    assert result.breakdown.contrast_score > 0
    assert result.breakdown.aspect_ratio_score == 100
    assert len(result.recommendations) > 0
    assert result.data_provenance in ["Calculated", "AI-Generated Vision"]

def test_thumbnail_bad_aspect_ratio_detected():
    # Square 800x800 image
    image_bytes = create_sample_thumbnail(800, 800)
    result = analyze_thumbnail_bytes(image_bytes, filename="square.jpg")
    
    assert result.aspect_ratio_label != "16:9"
    assert result.breakdown.aspect_ratio_score < 100
    # Should flag an issue about aspect ratio
    aspect_issues = [i for i in result.issues if "aspect ratio" in i.issue.lower()]
    assert len(aspect_issues) > 0
