import httpx
from typing import Optional
from app.youtube.base import YouTubeProvider
from app.models.video import VideoSearchResult, VideoMetadata
from app.models.channel import ChannelMetadata
from app.models.common import DataProvenance

class OfficialAPIYouTubeProvider(YouTubeProvider):
    """
    Official Google YouTube Data API v3 provider.
    Used when YOUTUBE_API_KEY is supplied.
    """
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str, timeout_seconds: float = 10.0):
        self.api_key = api_key
        self.timeout = timeout_seconds

    async def get_autocomplete_suggestions(self, query: str) -> list[str]:
        # YouTube Data API v3 does not have autocomplete endpoint, fallback to public suggest
        from app.youtube.autocomplete import autocomplete_client
        return await autocomplete_client.get_suggestions(query)

    async def search_videos(self, query: str, limit: int = 20) -> list[VideoSearchResult]:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": min(limit, 50),
            "key": self.api_key,
        }
        results = []
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(f"{self.BASE_URL}/search", params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    rank = 1
                    for item in data.get("items", []):
                        vid_id = item["id"]["videoId"]
                        snippet = item["snippet"]
                        results.append(
                            VideoSearchResult(
                                video_id=vid_id,
                                title=snippet.get("title", ""),
                                channel_name=snippet.get("channelTitle", ""),
                                channel_id=snippet.get("channelId"),
                                published_time_text=snippet.get("publishedAt", "")[:10],
                                thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url"),
                                description_snippet=snippet.get("description", ""),
                                rank_position=rank,
                                provenance=DataProvenance.OFFICIAL,
                            )
                        )
                        rank += 1
        except Exception:
            pass
        return results

    async def get_video_details(self, video_id: str) -> Optional[VideoMetadata]:
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": video_id,
            "key": self.api_key,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(f"{self.BASE_URL}/videos", params=params)
                if resp.status_code == 200:
                    items = resp.json().get("items", [])
                    if items:
                        item = items[0]
                        snip = item["snippet"]
                        stats = item.get("statistics", {})
                        tags = snip.get("tags", [])
                        return VideoMetadata(
                            video_id=video_id,
                            url=f"https://www.youtube.com/watch?v={video_id}",
                            title=snip.get("title", ""),
                            description=snip.get("description", ""),
                            channel_id=snip.get("channelId"),
                            channel_name=snip.get("channelTitle", ""),
                            views_count=int(stats.get("viewCount", 0)) if "viewCount" in stats else None,
                            likes_count=int(stats.get("likeCount", 0)) if "likeCount" in stats else None,
                            comments_count=int(stats.get("commentCount", 0)) if "commentCount" in stats else None,
                            tags=tags,
                            thumbnail_url=snip.get("thumbnails", {}).get("high", {}).get("url"),
                            provenance=DataProvenance.OFFICIAL,
                        )
        except Exception:
            pass
        return None

    async def get_channel_details(self, channel_id_or_handle: str) -> Optional[ChannelMetadata]:
        params = {
            "part": "snippet,statistics",
            "key": self.api_key,
        }
        if channel_id_or_handle.startswith("UC"):
            params["id"] = channel_id_or_handle
        else:
            params["forHandle"] = channel_id_or_handle

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(f"{self.BASE_URL}/channels", params=params)
                if resp.status_code == 200:
                    items = resp.json().get("items", [])
                    if items:
                        item = items[0]
                        snip = item["snippet"]
                        stats = item.get("statistics", {})
                        return ChannelMetadata(
                            channel_id=item["id"],
                            channel_title=snip.get("title", ""),
                            handle=snip.get("customUrl"),
                            description=snip.get("description", ""),
                            subscriber_count=int(stats.get("subscriberCount", 0)) if "subscriberCount" in stats else None,
                            video_count=int(stats.get("videoCount", 0)) if "videoCount" in stats else None,
                            view_count=int(stats.get("viewCount", 0)) if "viewCount" in stats else None,
                            avatar_url=snip.get("thumbnails", {}).get("high", {}).get("url"),
                            provenance=DataProvenance.OFFICIAL,
                        )
        except Exception:
            pass
        return None

    async def get_channel_recent_videos(self, channel_id: str, limit: int = 30) -> list[VideoMetadata]:
        cid = channel_id.strip()
        if not cid.startswith("UC"):
            channel_meta = await self.get_channel_details(cid)
            if channel_meta and channel_meta.channel_id.startswith("UC"):
                cid = channel_meta.channel_id

        if not cid.startswith("UC"):
            return []

        # YouTube uploads playlist replaces 'UC' prefix with 'UU'
        uploads_playlist_id = "UU" + cid[2:]
        video_ids: list[str] = []

        # 1. Fetch playlist items from uploads playlist
        try:
            params = {
                "part": "snippet,contentDetails",
                "playlistId": uploads_playlist_id,
                "maxResults": min(limit, 50),
                "key": self.api_key,
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(f"{self.BASE_URL}/playlistItems", params=params)
                if resp.status_code == 200:
                    items = resp.json().get("items", [])
                    for it in items:
                        vid_id = it.get("contentDetails", {}).get("videoId") or it.get("snippet", {}).get("resourceId", {}).get("videoId")
                        if vid_id:
                            video_ids.append(vid_id)
        except Exception:
            pass

        if not video_ids:
            return []

        # 2. Hydrate full statistics and details for those videos
        results: list[VideoMetadata] = []
        try:
            params = {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(video_ids[:50]),
                "key": self.api_key,
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(f"{self.BASE_URL}/videos", params=params)
                if resp.status_code == 200:
                    items = resp.json().get("items", [])
                    for item in items:
                        vid_id = item["id"]
                        snip = item.get("snippet", {})
                        stats = item.get("statistics", {})
                        desc = snip.get("description", "")
                        has_ch = "00:00" in desc or "0:00" in desc

                        results.append(
                            VideoMetadata(
                                video_id=vid_id,
                                url=f"https://www.youtube.com/watch?v={vid_id}",
                                title=snip.get("title", ""),
                                description=desc,
                                channel_id=snip.get("channelId", cid),
                                channel_name=snip.get("channelTitle", "Creator"),
                                published_date=snip.get("publishedAt", "")[:10] or None,
                                views_count=int(stats.get("viewCount", 0)) if "viewCount" in stats else None,
                                likes_count=int(stats.get("likeCount", 0)) if "likeCount" in stats else None,
                                comments_count=int(stats.get("commentCount", 0)) if "commentCount" in stats else None,
                                tags=snip.get("tags", []),
                                thumbnail_url=snip.get("thumbnails", {}).get("high", {}).get("url"),
                                has_chapters=has_ch,
                                provenance=DataProvenance.OFFICIAL,
                            )
                        )
        except Exception:
            pass

        return results[:limit]
