from abc import ABC, abstractmethod
from typing import Optional
from app.models.video import VideoSearchResult, VideoMetadata
from app.models.channel import ChannelMetadata

class YouTubeProvider(ABC):
    """
    Abstract interface for YouTube data operations.
    Ensures that mock, public scraping, and official API providers
    are interchangeable and decoupled from business logic.
    """

    @abstractmethod
    async def get_autocomplete_suggestions(self, query: str, hl: str = "en", gl: str = "US") -> list[str]:
        """Fetch real-time search suggestions for a query with optional language and country."""
        pass

    @abstractmethod
    async def search_videos(self, query: str, limit: int = 20) -> list[VideoSearchResult]:
        """Search public YouTube videos for a query and return structured results."""
        pass

    @abstractmethod
    async def get_video_details(self, video_id: str) -> Optional[VideoMetadata]:
        """Retrieve public metadata for a specific YouTube video."""
        pass

    @abstractmethod
    async def get_channel_details(self, channel_id_or_handle: str) -> Optional[ChannelMetadata]:
        """Retrieve public profile and stats for a channel."""
        pass

    @abstractmethod
    async def get_channel_recent_videos(self, channel_id: str, limit: int = 30) -> list[VideoMetadata]:
        """Fetch the most recent public videos for a channel."""
        pass
