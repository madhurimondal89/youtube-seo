from app.seo.audit_engine import audit_video_seo, audit_channel_seo

def test_video_seo_audit_100_points():
    res = audit_video_seo(
        title="How to Edit YouTube Videos Fast: Complete Step-by-Step Guide",
        description=(
            "In this video we reveal how to edit youtube videos fast with practical shortcuts and workflow tips.\n"
            "00:00 - Intro\n02:30 - Timeline Setup\n05:45 - Speed Shortcuts\n"
            "Subscribe for weekly creator tutorials! #VideoEditing #YouTubeTips"
        ),
        tags=["how to edit youtube videos fast", "video editing", "youtube tutorial", "premiere pro"],
        target_keyword="how to edit youtube videos fast",
        has_chapters=True
    )
    assert 0 <= res.overall_score <= 100
    assert len(res.categories) == 7
    total_max = sum(c.max_score for c in res.categories)
    assert total_max == 100.0
    assert res.overall_score > 70
    assert res.verdict in ["Excellent", "Good"]

def test_tags_500_char_limit_exceeded():
    long_tags = ["super detailed keyword " + str(i) * 20 for i in range(15)]
    res = audit_video_seo(
        title="Test Title Here",
        description="Test description here with chapters 00:00 - intro",
        tags=long_tags
    )
    tag_cat = next(c for c in res.categories if c.category_name == "Tags Optimization")
    char_limit_item = next(it for it in tag_cat.items if it.id == "tags_char_limit")
    assert not char_limit_item.passed
    assert char_limit_item.severity == "critical"
    assert "Tag limit exceeded" in char_limit_item.feedback

def test_closed_captions_check():
    res_with_cc = audit_video_seo(
        title="Test Title Here",
        description="Test description here with chapters 00:00 - intro",
        has_captions=True
    )
    eng_cat = next(c for c in res_with_cc.categories if "Engagement" in c.category_name)
    cc_item = next(it for it in eng_cat.items if it.id == "ctx_captions")
    assert cc_item.passed
    assert cc_item.score_earned == 3.0

    res_no_cc = audit_video_seo(
        title="Test Title Here",
        description="Test description here with chapters 00:00 - intro",
        has_captions=False
    )
    eng_cat_no = next(c for c in res_no_cc.categories if "Engagement" in c.category_name)
    cc_item_no = next(it for it in eng_cat_no.items if it.id == "ctx_captions")
    assert not cc_item_no.passed

def test_channel_audit():
    recent = [
        {"title": "How to Automate YouTube in 2026", "views_count": 25000},
        {"title": "Top 10 YouTube Automation Tools", "views_count": 28000},
        {"title": "Faceless YouTube Channel Blueprint", "views_count": 350000}, # outlier
    ]
    res = audit_channel_seo("UCtest", "Test Channel", recent)
    assert 0 <= res.overall_health_score <= 100
    assert len(res.recommendations) > 0
