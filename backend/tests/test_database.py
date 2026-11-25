import pytest
from app.db import repositories

def test_database_keyword_project_crud():
    # 1. Save
    sample_data = {
        "seed": "davinci resolve tutorial",
        "keywords": [{"keyword": "davinci resolve fusion tutorial", "opportunity_score": 85}]
    }
    proj_id = repositories.save_keyword_project("DaVinci Project", "davinci resolve tutorial", sample_data)
    assert proj_id.startswith("kw_")

    # 2. List
    projects = repositories.list_keyword_projects()
    assert any(p["id"] == proj_id for p in projects)

    # 3. Get
    loaded = repositories.get_keyword_project(proj_id)
    assert loaded is not None
    assert loaded["seed"] == "davinci resolve tutorial"
    assert len(loaded["data"]["keywords"]) == 1

    # 4. Delete
    deleted = repositories.delete_keyword_project(proj_id)
    assert deleted is True
    assert repositories.get_keyword_project(proj_id) is None

def test_database_competitor_watchlist_crud():
    item_id = repositories.add_competitor_watchlist(
        channel_id="UC1234567890",
        channel_name="Tech Creator Hub",
        median_views=45000,
        subscriber_count="120K",
        notes="High outlier count on tutorials"
    )
    assert item_id.startswith("comp_")

    watchlists = repositories.list_competitor_watchlists()
    assert any(w["id"] == item_id for w in watchlists)

    deleted = repositories.delete_competitor_watchlist(item_id)
    assert deleted is True

def test_database_audit_crud():
    audit_id = repositories.save_audit(
        video_title="How to Rank #1 on YouTube in 2026",
        video_url="https://youtube.com/watch?v=sample",
        overall_score=92,
        audit_data={"overall_score": 92, "categories": []}
    )
    assert audit_id.startswith("aud_")

    audits = repositories.list_saved_audits()
    assert any(a["id"] == audit_id for a in audits)

    deleted = repositories.delete_saved_audit(audit_id)
    assert deleted is True

def test_database_calendar_crud():
    cal_id = repositories.save_calendar_strategy(
        niche="Bengali Mystery",
        strategy={"weeks": []},
        channel_name="Rahasya Golpo",
        language="Bengali"
    )
    assert cal_id.startswith("cal_")

    calendars = repositories.list_calendar_strategies()
    assert any(c["id"] == cal_id for c in calendars)

    deleted = repositories.delete_calendar_strategy(cal_id)
    assert deleted is True
