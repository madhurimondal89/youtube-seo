from app.core.config import settings
from app.youtube.base import YouTubeProvider
from app.youtube.mock_provider import MockYouTubeProvider
from app.youtube.scraper import PublicYouTubeProvider
from app.youtube.api_client import OfficialAPIYouTubeProvider

def get_youtube_provider() -> YouTubeProvider:
    """
    Returns configured YouTube data provider.
    Defaults to PublicYouTubeProvider, supports OfficialAPI if key present,
    or MockYouTubeProvider for offline/testing/dev.
    """
    provider_type = settings.youtube_provider.lower().strip()
    
    if provider_type == "mock":
        return MockYouTubeProvider()
    
    if provider_type == "api" and settings.youtube_api_key:
        return OfficialAPIYouTubeProvider(api_key=settings.youtube_api_key)
        
    # Default to public lawful scraper with graceful fallback to mock if completely unreachable
    return PublicYouTubeProvider()
