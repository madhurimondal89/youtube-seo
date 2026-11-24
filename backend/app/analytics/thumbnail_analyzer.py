import io
import math
from typing import List, Tuple
from PIL import Image, ImageStat
from app.models.thumbnail import ThumbnailAnalysisResponse, VisualScoreBreakdown, VisualIssue

def analyze_thumbnail_bytes(image_bytes: bytes, filename: str = "thumbnail.jpg") -> ThumbnailAnalysisResponse:
    image = Image.open(io.BytesIO(image_bytes))
    image_rgb = image.convert("RGB")
    width, height = image_rgb.size
    
    # 1. Aspect Ratio Analysis
    ratio = width / height if height > 0 else 0
    is_16_9 = abs(ratio - (16 / 9)) < 0.05
    aspect_label = "16:9" if is_16_9 else f"{ratio:.2f}:1"
    is_standard_hd = (width >= 1280 and height >= 720 and is_16_9)
    
    aspect_score = 100 if is_16_9 else max(20, int(100 - abs(ratio - 1.777) * 80))
    
    # 2. Brightness & Contrast Analysis
    stat = ImageStat.Stat(image_rgb)
    # Perceived luminance: 0.299*R + 0.587*G + 0.114*B
    r_mean, g_mean, b_mean = stat.mean[:3]
    avg_brightness = (0.299 * r_mean + 0.587 * g_mean + 0.114 * b_mean)
    
    # Standard deviation of luminance indicates contrast
    r_std, g_std, b_std = stat.stddev[:3]
    contrast_std = (0.299 * r_std + 0.587 * g_std + 0.114 * b_std)
    # Normalize contrast to 0-100 scale (stddev 40-75 is ideal for click-through)
    if contrast_std < 25:
        contrast_score = int((contrast_std / 25) * 50)
    elif contrast_std > 85:
        contrast_score = 85  # Overly noisy
    else:
        contrast_score = min(100, int(60 + ((contrast_std - 25) / 50) * 40))
        
    contrast_ratio = round(contrast_std / 10.0, 2)
    
    # 3. Quadrant & Focal Analysis (YouTube timestamp sits at bottom-right)
    # Crop bottom-right quadrant
    br_box = (int(width * 0.7), int(height * 0.7), width, height)
    br_crop = image_rgb.crop(br_box)
    br_stat = ImageStat.Stat(br_crop)
    br_contrast = sum(br_stat.stddev[:3]) / 3
    
    # 4. Color Palette Extraction (Top 3 dominant tones)
    small_img = image_rgb.resize((50, 50))
    palette_colors = small_img.getcolors(maxcolors=2500)
    dominant_hex: List[str] = []
    if palette_colors:
        palette_colors.sort(key=lambda x: x[0], reverse=True)
        for _, rgb in palette_colors[:4]:
            dominant_hex.append(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
            
    # 5. Mobile Readability & Clarity Scoring
    # At mobile SERP size, high contrast and clear focal areas are paramount
    clarity_score = min(100, int(contrast_score * 0.6 + (aspect_score * 0.4)))
    mobile_readability_score = min(100, int(contrast_score * 0.7 + (40 if is_16_9 else 10)))
    focal_hierarchy_score = min(100, int(50 + (contrast_std * 0.6)))
    
    # Overall Composite Score
    overall_score = int(
        aspect_score * 0.20 +
        contrast_score * 0.30 +
        clarity_score * 0.20 +
        mobile_readability_score * 0.15 +
        focal_hierarchy_score * 0.15
    )
    overall_score = max(0, min(100, overall_score))
    
    breakdown = VisualScoreBreakdown(
        aspect_ratio_score=aspect_score,
        contrast_score=contrast_score,
        clarity_score=clarity_score,
        mobile_readability_score=mobile_readability_score,
        focal_hierarchy_score=focal_hierarchy_score
    )
    
    # 6. Issues & Recommendations
    issues: List[VisualIssue] = []
    recommendations: List[str] = []
    
    if not is_16_9:
        issues.append(VisualIssue(
            severity="critical",
            category="Aspect Ratio",
            issue=f"Aspect ratio is {aspect_label} instead of standard 16:9 (1280x720).",
            suggestion="Resize and crop canvas to 1280x720 or 1920x1080 to prevent black pillarboxing in YouTube search feeds."
        ))
    elif width < 1280:
        issues.append(VisualIssue(
            severity="warning",
            category="Resolution",
            issue=f"Resolution {width}x{height} is below recommended 1280x720 HD standard.",
            suggestion="Export at 1280x720 minimum to ensure crispness on Retina & 4K displays."
        ))
        
    if avg_brightness < 40:
        issues.append(VisualIssue(
            severity="warning",
            category="Luminance",
            issue="Overall image is dark/underexposed (luminance < 40/255).",
            suggestion="Increase exposure or add a rim-light highlight to the main subject so it pops against dark mode YouTube backgrounds."
        ))
    elif avg_brightness > 220:
        issues.append(VisualIssue(
            severity="warning",
            category="Luminance",
            issue="Overall image is blown out/overexposed (luminance > 220/255).",
            suggestion="Lower highlights and increase saturation to maintain visual weight."
        ))
        
    if contrast_std < 30:
        issues.append(VisualIssue(
            severity="critical",
            category="Contrast",
            issue="Low contrast distribution across the thumbnail.",
            suggestion="Apply a dark-to-light gradient or stroke to key foreground elements so text and subjects stay readable at mobile thumbnail scale."
        ))
        
    if br_contrast > 45:
        issues.append(VisualIssue(
            severity="info",
            category="Overlay Safety Zone",
            issue="High visual activity in the bottom-right corner.",
            suggestion="Keep critical faces and text away from the bottom-right corner where YouTube video duration badge (e.g. '12:45') is permanently overlaid."
        ))
        
    # Recommendations
    if overall_score >= 80:
        recommendations.append("Thumbnail displays strong visual contrast and adheres to standard 16:9 framing.")
    recommendations.append("Ensure any thumbnail text is restricted to 3-5 bold words maximum to avoid mobile cognitive overload.")
    recommendations.append("Verify primary focal subject occupies at least 35-40% of the canvas area for rapid visual recognition in browse feeds.")
    recommendations.append("Test your thumbnail in both YouTube dark mode and light mode environments.")
    
    mobile_advisory = (
        "Mobile Safe: High contrast ensures foreground subject remains legible at 120px feed width."
        if mobile_readability_score >= 70
        else "Mobile Warning: Elements may blur together on smaller phone screens. Increase subject scale and text stroke thickness."
    )
    
    return ThumbnailAnalysisResponse(
        filename=filename,
        width=width,
        height=height,
        aspect_ratio_label=aspect_label,
        is_standard_hd=is_standard_hd,
        overall_score=overall_score,
        breakdown=breakdown,
        dominant_colors=dominant_hex,
        average_brightness=round(avg_brightness, 1),
        contrast_ratio=contrast_ratio,
        issues=issues,
        recommendations=recommendations,
        mobile_preview_advisory=mobile_advisory,
        data_provenance="Calculated"
    )
