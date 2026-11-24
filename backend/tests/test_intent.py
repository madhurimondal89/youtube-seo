from app.seo.intent import classify_search_intent
from app.models.keyword import SearchIntent

def test_intent_classification():
    assert SearchIntent.TUTORIAL in classify_search_intent("how to edit youtube videos fast")
    assert SearchIntent.COMMERCIAL in classify_search_intent("best microphones for youtube 2026")
    assert SearchIntent.COMPARISON in classify_search_intent("vidiq vs tubebuddy honest review")
    assert SearchIntent.PROBLEM_FIX in classify_search_intent("fix youtube video upload error")
    assert SearchIntent.TRANSACTIONAL in classify_search_intent("buy premiere pro presets discount")
    assert SearchIntent.INFORMATIONAL in classify_search_intent("what is youtube impressions click through rate")
    assert SearchIntent.NEWS_TRENDING in classify_search_intent("youtube algorithm update 2026 announcement")
