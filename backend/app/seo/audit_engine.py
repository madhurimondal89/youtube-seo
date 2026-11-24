import re
from typing import Optional
from app.models.audit import (
    VideoAuditResult,
    ChannelAuditResult,
    AuditCategoryScore,
    AuditChecklistItem,
)
from app.models.common import DataProvenance
from app.seo.title_analyzer import analyze_title_heuristics

def audit_video_seo(
    title: str,
    description: str = "",
    tags: Optional[list[str]] = None,
    target_keyword: Optional[str] = None,
    video_id: Optional[str] = None,
    has_chapters: bool = False,
    has_captions: bool = False,
) -> VideoAuditResult:
    """
    18-point transparent deterministic Video SEO audit.
    Evaluates 7 categories totaling exactly 100 points:
    1. Title: 25 pts
    2. Description: 20 pts
    3. Keyword Relevance: 20 pts
    4. Tags: 10 pts
    5. Search Intent: 10 pts
    6. Readability: 5 pts
    7. Engagement / Context: 10 pts
    """
    tags = tags or []
    t_clean = title.strip()
    d_clean = description.strip()
    categories: list[AuditCategoryScore] = []
    action_plan: list[str] = []

    # Heuristics analysis
    t_analysis = analyze_title_heuristics(t_clean, target_keyword)

    # -------------------------------------------------------------
    # 1. TITLE OPTIMIZATION (25 points)
    # -------------------------------------------------------------
    t_items: list[AuditChecklistItem] = []
    
    # Item 1.1: Optimal Length (8 pts)
    c_len = t_analysis["character_count"]
    if 45 <= c_len <= 70:
        t_items.append(AuditChecklistItem(
            id="title_length", title="Title Length (45-70 chars)", passed=True,
            score_earned=8.0, max_score=8.0, feedback=f"Great title length ({c_len} chars).",
            severity="optimal"
        ))
    elif 30 <= c_len <= 85:
        t_items.append(AuditChecklistItem(
            id="title_length", title="Title Length (45-70 chars)", passed=False,
            score_earned=5.0, max_score=8.0, feedback=f"Title length is {c_len} chars. Aim for 45-70.",
            actionable_fix="Adjust title to between 45 and 70 characters so it fits desktop and mobile previews.",
            severity="warning"
        ))
        action_plan.append("Optimize title character count to 45-70 characters.")
    else:
        t_items.append(AuditChecklistItem(
            id="title_length", title="Title Length (45-70 chars)", passed=False,
            score_earned=2.0, max_score=8.0, feedback=f"Title is severely short or long ({c_len} chars).",
            actionable_fix="Rewrite title with clear keyword and compelling hook (45-70 chars).",
            severity="critical"
        ))
        action_plan.append("Rewrite title to avoid search truncation.")

    # Item 1.2: Front-loaded Keyword or Main Concept (8 pts)
    if t_analysis["frontloaded_keyword"] or target_keyword is None:
        t_items.append(AuditChecklistItem(
            id="title_frontload", title="Front-Loaded Keyword", passed=True,
            score_earned=8.0, max_score=8.0, feedback="Core topic appears early in title.",
            severity="optimal"
        ))
    elif t_analysis["has_keyword"]:
        t_items.append(AuditChecklistItem(
            id="title_frontload", title="Front-Loaded Keyword", passed=False,
            score_earned=5.0, max_score=8.0, feedback="Keyword found but placed near the end.",
            actionable_fix="Shift your main target keyword into the first 35 characters.",
            severity="warning"
        ))
        action_plan.append("Move your primary keyword closer to the start of the title.")
    else:
        t_items.append(AuditChecklistItem(
            id="title_frontload", title="Front-Loaded Keyword", passed=False,
            score_earned=1.0, max_score=8.0, feedback="Target keyword not detected in title.",
            actionable_fix=f"Include '{target_keyword}' naturally in the title.",
            severity="critical"
        ))
        action_plan.append("Incorporate the target keyword in the video title.")

    # Item 1.3: Curiosity & Power Words (5 pts)
    p_words = t_analysis["power_words"]
    if p_words:
        t_items.append(AuditChecklistItem(
            id="title_power_words", title="Power & Emotional Hook Words", passed=True,
            score_earned=5.0, max_score=5.0, feedback=f"Contains compelling words: {', '.join(p_words)}.",
            severity="optimal"
        ))
    else:
        t_items.append(AuditChecklistItem(
            id="title_power_words", title="Power & Emotional Hook Words", passed=False,
            score_earned=2.0, max_score=5.0, feedback="No emotional hook or power word detected.",
            actionable_fix="Add a power word (e.g. 'Step-by-Step', 'Blueprint', 'Mistakes', 'Simple') to spark interest.",
            severity="warning"
        ))

    # Item 1.4: No Capitalization Spam (4 pts)
    if not t_analysis["is_spammy_caps"]:
        t_items.append(AuditChecklistItem(
            id="title_caps", title="Clean Capitalization", passed=True,
            score_earned=4.0, max_score=4.0, feedback="Title uses natural, readable capitalization.",
            severity="optimal"
        ))
    else:
        t_items.append(AuditChecklistItem(
            id="title_caps", title="Clean Capitalization", passed=False,
            score_earned=0.0, max_score=4.0, feedback="Excessive all-caps detected.",
            actionable_fix="Avoid all-caps shouting; use Title Case or sentence case.",
            severity="warning"
        ))
        action_plan.append("Remove excessive all-caps shouting from the title.")

    t_earned = sum(it.score_earned for it in t_items)
    categories.append(AuditCategoryScore(
        category_name="Title Optimization", earned_score=t_earned, max_score=25.0,
        percentage=int((t_earned / 25.0) * 100), items=t_items
    ))

    # -------------------------------------------------------------
    # 2. DESCRIPTION OPTIMIZATION (20 points)
    # -------------------------------------------------------------
    d_items: list[AuditChecklistItem] = []
    words_desc = d_clean.split()
    w_count = len(words_desc)

    # 2.1 Description Length (6 pts)
    if w_count >= 150:
        d_items.append(AuditChecklistItem(
            id="desc_length", title="Description Depth (150+ words)", passed=True,
            score_earned=6.0, max_score=6.0, feedback=f"Rich description ({w_count} words).",
            severity="optimal"
        ))
    elif w_count >= 50:
        d_items.append(AuditChecklistItem(
            id="desc_length", title="Description Depth (150+ words)", passed=False,
            score_earned=3.5, max_score=6.0, feedback=f"Description is brief ({w_count} words).",
            actionable_fix="Expand description to 150-300 words explaining key concepts and takeaways.",
            severity="warning"
        ))
        action_plan.append("Expand the description with a comprehensive summary.")
    else:
        d_items.append(AuditChecklistItem(
            id="desc_length", title="Description Depth (150+ words)", passed=False,
            score_earned=1.0, max_score=6.0, feedback=f"Description is critically short ({w_count} words).",
            actionable_fix="Add at least 2 detailed paragraphs describing the video contents.",
            severity="critical"
        ))
        action_plan.append("Write a detailed 200+ word video description.")

    # 2.2 First 3 Lines Hook (5 pts)
    first_lines = "\n".join(d_clean.split("\n")[:3])
    if target_keyword and target_keyword.lower() in first_lines.lower():
        d_items.append(AuditChecklistItem(
            id="desc_first_lines", title="Keyword in Above-The-Fold Hook", passed=True,
            score_earned=5.0, max_score=5.0, feedback="Target keyword appears in the first 3 lines.",
            severity="optimal"
        ))
    elif target_keyword:
        d_items.append(AuditChecklistItem(
            id="desc_first_lines", title="Keyword in Above-The-Fold Hook", passed=False,
            score_earned=2.0, max_score=5.0, feedback="First 3 lines do not contain the primary keyword.",
            actionable_fix="Mention the primary topic within the first 2 sentences before the 'Show more' fold.",
            severity="warning"
        ))
        action_plan.append("Place primary keyword in the first two sentences of description.")
    else:
        d_items.append(AuditChecklistItem(
            id="desc_first_lines", title="Keyword in Above-The-Fold Hook", passed=True,
            score_earned=4.0, max_score=5.0, feedback="Opening lines set video context.",
            severity="optimal"
        ))

    # 2.3 Chapters & Timestamps (5 pts)
    has_timestamps = has_chapters or bool(re.search(r"\b\d{1,2}:\d{2}\b", d_clean))
    if has_timestamps:
        d_items.append(AuditChecklistItem(
            id="desc_timestamps", title="Video Chapters / Timestamps", passed=True,
            score_earned=5.0, max_score=5.0, feedback="Timestamped chapters detected (boosts Google Key Moments).",
            severity="optimal"
        ))
    else:
        d_items.append(AuditChecklistItem(
            id="desc_timestamps", title="Video Chapters / Timestamps", passed=False,
            score_earned=0.0, max_score=5.0, feedback="No video chapters or timestamps found.",
            actionable_fix="Add timestamp chapters starting with '00:00 - Introduction' to enhance viewer retention.",
            severity="warning"
        ))
        action_plan.append("Add timestamp chapters to enable Google Key Moments indexing.")

    # 2.4 Call to Action & Links (4 pts)
    has_cta = any(term in d_clean.lower() for term in ["subscribe", "link", "http", "follow", "comment", "resource"])
    if has_cta:
        d_items.append(AuditChecklistItem(
            id="desc_cta", title="Call-to-Action (CTA) & Links", passed=True,
            score_earned=4.0, max_score=4.0, feedback="Clear CTA or resource links present.",
            severity="optimal"
        ))
    else:
        d_items.append(AuditChecklistItem(
            id="desc_cta", title="Call-to-Action (CTA) & Links", passed=False,
            score_earned=1.0, max_score=4.0, feedback="Missing explicit CTA or helpful links.",
            actionable_fix="Add links to related videos and invite viewers to subscribe or comment.",
            severity="warning"
        ))

    d_earned = sum(it.score_earned for it in d_items)
    categories.append(AuditCategoryScore(
        category_name="Description Optimization", earned_score=d_earned, max_score=20.0,
        percentage=int((d_earned / 20.0) * 100), items=d_items
    ))

    # -------------------------------------------------------------
    # 3. KEYWORD RELEVANCE (20 points)
    # -------------------------------------------------------------
    k_items: list[AuditChecklistItem] = []
    # Title & description keyword alignment (10 pts)
    title_words = set(w.lower() for w in t_clean.split() if len(w) > 3)
    desc_words = set(w.lower() for w in d_clean.split() if len(w) > 3)
    shared_kw = title_words.intersection(desc_words)
    
    if len(shared_kw) >= 3:
        k_items.append(AuditChecklistItem(
            id="kw_title_desc_match", title="Title & Description Keyword Alignment", passed=True,
            score_earned=10.0, max_score=10.0, feedback=f"Strong semantic alignment ({len(shared_kw)} key terms shared).",
            severity="optimal"
        ))
    else:
        k_items.append(AuditChecklistItem(
            id="kw_title_desc_match", title="Title & Description Keyword Alignment", passed=False,
            score_earned=4.0, max_score=10.0, feedback="Few core title keywords repeated in description.",
            actionable_fix="Reinforce main title keywords naturally within the description body.",
            severity="warning"
        ))
        action_plan.append("Reinforce title keywords within the description paragraphs.")

    # Supporting semantic variation (10 pts)
    if len(desc_words) > 30:
        k_items.append(AuditChecklistItem(
            id="kw_semantic_variety", title="Semantic Vocabulary Breadth", passed=True,
            score_earned=10.0, max_score=10.0, feedback="Rich vocabulary helps YouTube understand context.",
            severity="optimal"
        ))
    else:
        k_items.append(AuditChecklistItem(
            id="kw_semantic_variety", title="Semantic Vocabulary Breadth", passed=False,
            score_earned=5.0, max_score=10.0, feedback="Limited vocabulary detected in metadata.",
            actionable_fix="Include synonyms, related terms, and problem descriptions.",
            severity="warning"
        ))

    k_earned = sum(it.score_earned for it in k_items)
    categories.append(AuditCategoryScore(
        category_name="Keyword Relevance", earned_score=k_earned, max_score=20.0,
        percentage=int((k_earned / 20.0) * 100), items=k_items
    ))

    # -------------------------------------------------------------
    # 4. TAGS OPTIMIZATION (10 points)
    # -------------------------------------------------------------
    tag_items: list[AuditChecklistItem] = []
    tag_count = len(tags)
    
    # 4.1 Tag Count (5 pts)
    if 5 <= tag_count <= 25:
        tag_items.append(AuditChecklistItem(
            id="tags_count", title="Focused Tag Count (5-25 tags)", passed=True,
            score_earned=5.0, max_score=5.0, feedback=f"Optimal tag quantity ({tag_count} tags).",
            severity="optimal"
        ))
    elif tag_count > 0:
        tag_items.append(AuditChecklistItem(
            id="tags_count", title="Focused Tag Count (5-25 tags)", passed=False,
            score_earned=2.5, max_score=5.0, feedback=f"Suboptimal tag quantity ({tag_count} tags).",
            actionable_fix="Add 5 to 15 relevant primary and long-tail tags.",
            severity="warning"
        ))
    else:
        tag_items.append(AuditChecklistItem(
            id="tags_count", title="Focused Tag Count (5-25 tags)", passed=False,
            score_earned=0.5, max_score=5.0, feedback="No tags detected.",
            actionable_fix="Include 8-12 tags covering your main keyword, variations, and brand.",
            severity="warning"
        ))
        action_plan.append("Generate and insert 8-12 targeted video tags.")

    # 4.2 500-Character Cumulative Limit Check (5 pts)
    # YouTube counts characters of each tag plus comma separators between tags
    total_tag_chars = sum(len(t) for t in tags) + max(0, len(tags) - 1)
    if total_tag_chars > 500:
        tag_items.append(AuditChecklistItem(
            id="tags_char_limit", title="500-Character Tag Limit", passed=False,
            score_earned=0.0, max_score=5.0,
            feedback=f"Tag limit exceeded ({total_tag_chars}/500 chars). YouTube Studio will reject saving these tags.",
            actionable_fix=f"Remove redundant tags to reduce total length by {total_tag_chars - 500} characters.",
            severity="critical"
        ))
        action_plan.append(f"Trim tags by {total_tag_chars - 500} chars to stay within YouTube's 500-char limit.")
    elif 300 <= total_tag_chars <= 500:
        tag_items.append(AuditChecklistItem(
            id="tags_char_limit", title="500-Character Tag Limit", passed=True,
            score_earned=5.0, max_score=5.0,
            feedback=f"Optimal tag allowance utilization ({total_tag_chars}/500 chars).",
            severity="optimal"
        ))
    elif 100 <= total_tag_chars < 300:
        tag_items.append(AuditChecklistItem(
            id="tags_char_limit", title="500-Character Tag Limit", passed=True,
            score_earned=4.0, max_score=5.0,
            feedback=f"Good tag usage ({total_tag_chars}/500 chars). You have room for additional long-tail tags.",
            severity="optimal"
        ))
    elif total_tag_chars > 0:
        tag_items.append(AuditChecklistItem(
            id="tags_char_limit", title="500-Character Tag Limit", passed=False,
            score_earned=2.0, max_score=5.0,
            feedback=f"Underutilized tag allowance ({total_tag_chars}/500 chars).",
            actionable_fix="Add relevant synonyms, common misspellings, and keyword variations up to ~400 chars.",
            severity="warning"
        ))
    else:
        tag_items.append(AuditChecklistItem(
            id="tags_char_limit", title="500-Character Tag Limit", passed=False,
            score_earned=0.5, max_score=5.0,
            feedback="No tag characters used (0/500 chars).",
            actionable_fix="Fill tag budget with targeted keywords (aim for 300-450 chars).",
            severity="warning"
        ))

    tag_earned = sum(it.score_earned for it in tag_items)
    categories.append(AuditCategoryScore(
        category_name="Tags Optimization", earned_score=tag_earned, max_score=10.0,
        percentage=int((tag_earned / 10.0) * 100), items=tag_items
    ))

    # -------------------------------------------------------------
    # 5. SEARCH INTENT ALIGNMENT (10 points)
    # -------------------------------------------------------------
    intent_items: list[AuditChecklistItem] = []
    has_clear_intent = any(w in t_clean.lower() for w in ["how", "guide", "tutorial", "best", "vs", "fix", "review", "tips"])
    if has_clear_intent:
        intent_items.append(AuditChecklistItem(
            id="intent_match", title="Clear Intent Phrasing", passed=True,
            score_earned=10.0, max_score=10.0, feedback="Title explicitly signals clear viewer intent.",
            severity="optimal"
        ))
    else:
        intent_items.append(AuditChecklistItem(
            id="intent_match", title="Clear Intent Phrasing", passed=False,
            score_earned=5.0, max_score=10.0, feedback="Title is ambiguous in search intent.",
            actionable_fix="Frame title around a specific action (e.g. 'How to...', 'Best Ways to...', 'Fixing...').",
            severity="warning"
        ))

    intent_earned = sum(it.score_earned for it in intent_items)
    categories.append(AuditCategoryScore(
        category_name="Search Intent", earned_score=intent_earned, max_score=10.0,
        percentage=int((intent_earned / 10.0) * 100), items=intent_items
    ))

    # -------------------------------------------------------------
    # 6. READABILITY (5 points)
    # -------------------------------------------------------------
    read_items: list[AuditChecklistItem] = []
    # Check punctuation and clean syntax
    has_clean_punct = not re.search(r"([!?.,])\1{2,}", t_clean)
    if has_clean_punct:
        read_items.append(AuditChecklistItem(
            id="readability_punct", title="Clean Readability & Punctuation", passed=True,
            score_earned=5.0, max_score=5.0, feedback="Clean typography without punctuation spam.",
            severity="optimal"
        ))
    else:
        read_items.append(AuditChecklistItem(
            id="readability_punct", title="Clean Readability & Punctuation", passed=False,
            score_earned=2.0, max_score=5.0, feedback="Excessive duplicate punctuation detected (e.g. '!!!').",
            actionable_fix="Remove repetitive exclamation points and characters.",
            severity="warning"
        ))

    read_earned = sum(it.score_earned for it in read_items)
    categories.append(AuditCategoryScore(
        category_name="Readability", earned_score=read_earned, max_score=5.0,
        percentage=int((read_earned / 5.0) * 100), items=read_items
    ))

    # -------------------------------------------------------------
    # 7. ENGAGEMENT & CONTEXT SIGNALS (10 points)
    # -------------------------------------------------------------
    ctx_items: list[AuditChecklistItem] = []
    has_hashtags = "#" in d_clean
    if has_hashtags:
        ctx_items.append(AuditChecklistItem(
            id="ctx_hashtags", title="Relevant Hashtags in Description", passed=True,
            score_earned=3.5, max_score=3.5, feedback="Hashtags detected for search discovery.",
            severity="optimal"
        ))
    else:
        ctx_items.append(AuditChecklistItem(
            id="ctx_hashtags", title="Relevant Hashtags in Description", passed=False,
            score_earned=1.5, max_score=3.5, feedback="No hashtags found in description.",
            actionable_fix="Add 2-3 specific hashtags at the bottom of the description (e.g. #YouTubeSEO).",
            severity="warning"
        ))

    # Curiosity / Hook index (3.5 pts)
    if t_analysis["curiosity_score"] >= 65:
        ctx_items.append(AuditChecklistItem(
            id="ctx_curiosity", title="Packaging Curiosity Factor", passed=True,
            score_earned=3.5, max_score=3.5, feedback="Strong title curiosity spark.",
            severity="optimal"
        ))
    else:
        ctx_items.append(AuditChecklistItem(
            id="ctx_curiosity", title="Packaging Curiosity Factor", passed=False,
            score_earned=1.5, max_score=3.5, feedback="Moderate packaging curiosity.",
            actionable_fix="Inject curiosity or contrast into the title hook.",
            severity="warning"
        ))

    # Closed Captions / Subtitles (3.0 pts)
    if has_captions:
        ctx_items.append(AuditChecklistItem(
            id="ctx_captions", title="Closed Captions & Subtitles (CC)", passed=True,
            score_earned=3.0, max_score=3.0,
            feedback="Closed Captions (CC) active. YouTube NLP indexes spoken audio keywords.",
            severity="optimal"
        ))
    else:
        ctx_items.append(AuditChecklistItem(
            id="ctx_captions", title="Closed Captions & Subtitles (CC)", passed=False,
            score_earned=1.0, max_score=3.0,
            feedback="No verified custom subtitles or CC detected.",
            actionable_fix="Upload accurate subtitles (.srt) or verify English CC so YouTube search crawls spoken dialogue.",
            severity="warning"
        ))
        action_plan.append("Upload accurate closed captions (.srt) to boost spoken keyword indexing.")

    ctx_earned = sum(it.score_earned for it in ctx_items)
    categories.append(AuditCategoryScore(
        category_name="Engagement & Context", earned_score=ctx_earned, max_score=10.0,
        percentage=int((ctx_earned / 10.0) * 100), items=ctx_items
    ))

    # Overall 0-100 score
    total_score = int(round(sum(c.earned_score for c in categories)))
    if total_score >= 85:
        verdict = "Excellent"
    elif total_score >= 70:
        verdict = "Good"
    elif total_score >= 50:
        verdict = "Needs Optimization"
    else:
        verdict = "Critical Issues"

    return VideoAuditResult(
        video_id=video_id,
        title=t_clean,
        overall_score=total_score,
        verdict=verdict,
        categories=categories,
        action_plan=action_plan or ["Metadata is well optimized; focus on thumbnail contrast and viewer retention."],
        keywords_detected=list(shared_kw)[:6],
        estimated_readability="Easy to Read" if total_score > 65 else "Moderate",
        curiosity_score=t_analysis["curiosity_score"],
        provenance=DataProvenance.CALCULATED,
    )

def audit_channel_seo(
    channel_id: str,
    channel_title: str,
    recent_videos: list[dict],
    subscriber_count: Optional[int] = None
) -> ChannelAuditResult:
    """
    Evaluates channel SEO health, upload consistency, topic focus, and title quality.
    """
    total_videos = len(recent_videos)
    if total_videos == 0:
        return ChannelAuditResult(
            channel_id=channel_id,
            channel_title=channel_title,
            overall_health_score=50,
            topic_consistency_score=50,
            title_quality_score=50,
            upload_cadence_score=50,
            outlier_ratio=0.0,
            recommendations=["Upload at least 5-10 videos to establish a reliable baseline."],
            next_best_video_topics=["Beginner Tutorial", "Ultimate Guide", "Common Mistakes"],
            provenance=DataProvenance.CALCULATED
        )

    # 1. Title Quality Average
    title_scores = []
    for v in recent_videos:
        t = v.get("title", "")
        heuristics = analyze_title_heuristics(t)
        title_scores.append(heuristics["length_score"] * 0.5 + heuristics["curiosity_score"] * 0.5)
    avg_title_quality = int(sum(title_scores) / len(title_scores)) if title_scores else 60

    # 2. Topic Consistency
    words_all = []
    for v in recent_videos:
        words_all.extend([w.lower() for w in v.get("title", "").split() if len(w) > 4])
    unique_words = len(set(words_all))
    # Ratio of repeated vocabulary to unique words
    repeat_ratio = (len(words_all) - unique_words) / max(1, len(words_all))
    topic_consistency = min(100, int(repeat_ratio * 140 + 35))

    # 3. Upload Cadence (Score 0-100)
    upload_cadence_score = 80 if total_videos >= 10 else 55

    # 4. Outlier Ratio
    views = [v.get("views_count") or 0 for v in recent_videos if v.get("views_count")]
    if views:
        sorted_views = sorted(views)
        median_v = sorted_views[len(sorted_views) // 2]
        outliers_count = sum(1 for v in views if v >= median_v * 2.5)
        outlier_ratio = round(outliers_count / max(1, len(views)), 2)
    else:
        outlier_ratio = 0.0

    # Overall Health Score
    overall_health = int(round(
        0.35 * avg_title_quality +
        0.30 * topic_consistency +
        0.25 * upload_cadence_score +
        0.10 * min(100, outlier_ratio * 200)
    ))

    recs = []
    if avg_title_quality < 70:
        recs.append("Improve video packaging: standardise title lengths to 45-70 characters.")
    if topic_consistency < 60:
        recs.append("Tighten channel topic focus: group videos into 2-3 core content pillars.")
    if outlier_ratio < 0.10:
        recs.append("Test bolder, curiosity-driven video concepts to spark breakout views.")
    else:
        recs.append(f"Strong topic breakout performance ({int(outlier_ratio * 100)}% of recent videos are outliers). Double down on top formats.")

    return ChannelAuditResult(
        channel_id=channel_id,
        channel_title=channel_title,
        overall_health_score=overall_health,
        topic_consistency_score=topic_consistency,
        title_quality_score=avg_title_quality,
        upload_cadence_score=upload_cadence_score,
        outlier_ratio=outlier_ratio,
        recommendations=recs,
        next_best_video_topics=["Step-by-Step Practical Blueprint", "Top 5 Tools Compared", "Case Study: What Worked"],
        provenance=DataProvenance.CALCULATED
    )

