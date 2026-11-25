import io
import math
from typing import List, Tuple, Optional
from PIL import Image, ImageStat, ImageFilter
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
    r_mean, g_mean, b_mean = stat.mean[:3]
    avg_brightness = (0.299 * r_mean + 0.587 * g_mean + 0.114 * b_mean)
    
    r_std, g_std, b_std = stat.stddev[:3]
    contrast_std = (0.299 * r_std + 0.587 * g_std + 0.114 * b_std)
    
    if contrast_std < 25:
        contrast_score = int((contrast_std / 25) * 50)
    elif contrast_std > 85:
        contrast_score = 82  # Overly busy/noisy
    else:
        contrast_score = min(100, int(60 + ((contrast_std - 25) / 50) * 40))
        
    contrast_ratio = round(contrast_std / 10.0, 2)
    
    # 3. 3x3 Grid Spatial Analysis for Composition & Hierarchy
    cell_w = max(1, width // 3)
    cell_h = max(1, height // 3)
    grid_energies: list[float] = []
    
    for row in range(3):
        for col in range(3):
            box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
            cell_stat = ImageStat.Stat(image_rgb.crop(box))
            cell_energy = sum(cell_stat.stddev[:3]) / 3
            grid_energies.append(cell_energy)
            
    # Visual Hierarchy: ratio of peak focal cell to average background cells
    max_energy = max(grid_energies) if grid_energies else 1.0
    mean_energy = (sum(grid_energies) / len(grid_energies)) if grid_energies else 1.0
    energy_ratio = max_energy / max(1.0, mean_energy)
    visual_hierarchy_score = min(100, int(energy_ratio * 45 + (contrast_score * 0.4)))
    
    # Subject Visibility: center cell + left/right rule of thirds cells
    focal_cells = [grid_energies[1], grid_energies[3], grid_energies[4], grid_energies[5]]
    avg_focal = sum(focal_cells) / len(focal_cells) if focal_cells else 0
    subject_visibility_score = min(100, int((avg_focal / 45.0) * 60 + (contrast_score * 0.4)))
    
    # Composition: rule of thirds alignment
    # Check if primary focal energy sits at col 0 or 1 rather than completely centered or edge-stuck
    col_energies = [
        grid_energies[0] + grid_energies[3] + grid_energies[6],
        grid_energies[1] + grid_energies[4] + grid_energies[7],
        grid_energies[2] + grid_energies[5] + grid_energies[8],
    ]
    composition_score = 85
    if col_energies[0] > col_energies[2] * 1.2 or col_energies[2] > col_energies[0] * 1.2:
        composition_score = 92  # Asymmetric rule of thirds balance
    elif max(col_energies) / max(1.0, min(col_energies)) < 1.15:
        composition_score = 72  # Too uniformly flat
        
    # Background Complexity: peripheral noise level
    peripheral_energies = [grid_energies[0], grid_energies[2], grid_energies[6]]
    avg_periph = sum(peripheral_energies) / len(peripheral_energies)
    if avg_periph > 65:
        background_complexity_score = 60  # Overly cluttered background
    elif avg_periph < 25:
        background_complexity_score = 95  # Clean, minimal background with strong pop
    else:
        background_complexity_score = int(95 - (avg_periph - 25) * 0.8)
        
    # Text Readability: upper & middle canvas contrast
    upper_crop = image_rgb.crop((0, 0, width, int(height * 0.65)))
    upper_stat = ImageStat.Stat(upper_crop)
    upper_contrast = sum(upper_stat.stddev[:3]) / 3
    text_readability_score = min(100, int((upper_contrast / 50.0) * 55 + (contrast_score * 0.45)))
    
    # 4. Mobile Readability Simulation (downsampled to 160x90 mobile feed card)
    mobile_thumb = image_rgb.resize((160, 90), Image.Resampling.BILINEAR)
    mobile_stat = ImageStat.Stat(mobile_thumb)
    mobile_contrast = sum(mobile_stat.stddev[:3]) / 3
    mobile_readability_score = min(100, int((mobile_contrast / 45.0) * 65 + (25 if is_16_9 else 5)))
    
    # Bottom-right timestamp safety zone check
    br_box = (int(width * 0.7), int(height * 0.7), width, height)
    br_crop = image_rgb.crop(br_box)
    br_stat = ImageStat.Stat(br_crop)
    br_contrast = sum(br_stat.stddev[:3]) / 3
    
    # 5. Dominant Colors
    small_img = image_rgb.resize((50, 50))
    palette_colors = small_img.getcolors(maxcolors=2500)
    dominant_hex: List[str] = []
    if palette_colors:
        palette_colors.sort(key=lambda x: x[0], reverse=True)
        for _, rgb in palette_colors[:4]:
            dominant_hex.append(f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
            
    # Composite Score across 7 Core Dimensions
    overall_score = int(
        visual_hierarchy_score * 0.18 +
        text_readability_score * 0.18 +
        subject_visibility_score * 0.16 +
        contrast_score * 0.16 +
        mobile_readability_score * 0.14 +
        composition_score * 0.10 +
        background_complexity_score * 0.08
    )
    overall_score = max(0, min(100, overall_score))
    
    breakdown = VisualScoreBreakdown(
        visual_hierarchy_score=visual_hierarchy_score,
        text_readability_score=text_readability_score,
        subject_visibility_score=subject_visibility_score,
        contrast_score=contrast_score,
        mobile_readability_score=mobile_readability_score,
        composition_score=composition_score,
        background_complexity_score=background_complexity_score,
        aspect_ratio_score=aspect_score,
        clarity_score=text_readability_score,
        focal_hierarchy_score=visual_hierarchy_score,
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
        
    if background_complexity_score < 70:
        issues.append(VisualIssue(
            severity="warning",
            category="Background Complexity",
            issue="High background visual noise and clutter detected.",
            suggestion="Apply a subtle background blur or radial vignette to push the background back and separate the primary subject."
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
    recommendations.append("Limit thumbnail typography to 3-5 bold words maximum to avoid mobile cognitive overload.")
    recommendations.append("Ensure primary subject occupies at least 35-40% of the canvas area for rapid visual recognition in browse feeds.")
    recommendations.append("Verify your thumbnail pop in both YouTube dark mode (#0f0f0f) and light mode (#ffffff) backgrounds.")
    recommendations.append("Heuristic evaluation disclaimer: Metrics assess graphic legibility standards and do not guarantee actual user click-through rate.")
    
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
        data_provenance="Calculated",
        vision_ai_status="Deterministic Vision Mode",
    )
