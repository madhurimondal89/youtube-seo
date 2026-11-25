import httpx
import asyncio
import random
import re
from typing import Optional

from app.youtube.base import YouTubeProvider
from app.youtube.autocomplete import autocomplete_client
from app.youtube.parser import (
    extract_search_results_from_html,
    parse_views_string,
    parse_duration_string,
    INITIAL_DATA_REGEX,
)
from app.models.video import VideoSearchResult, VideoMetadata
from app.models.channel import ChannelMetadata
from app.models.common import DataProvenance

class PublicYouTubeProvider(YouTubeProvider):
    """
    Lawful, rate-limited public research provider.
    Scrapes only publicly accessible HTML/metadata without bypassing protections.
    Halts gracefully if a CAPTCHA/challenge is encountered.
    """

    SEARCH_URL = "https://www.youtube.com/results"
    WATCH_URL = "https://www.youtube.com/watch"

    def __init__(self, timeout_seconds: float = 10.0):
        self.timeout = timeout_seconds
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def _safe_delay(self):
        """Randomized jitter to avoid burst traffic."""
        await asyncio.sleep(random.uniform(0.15, 0.45))

    async def get_autocomplete_suggestions(self, query: str, hl: str = "en", gl: str = "US") -> list[str]:
        await self._safe_delay()
        return await autocomplete_client.get_suggestions(query, hl=hl, gl=gl)

    async def search_videos(self, query: str, limit: int = 20) -> list[VideoSearchResult]:
        await self._safe_delay()
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(self.SEARCH_URL, params={"search_query": query})
                if resp.status_code == 200:
                    if "consent.youtube.com" in str(resp.url) or "sorry/index" in str(resp.url):
                        # Gracefully halt if challenge page is detected
                        return []
                    return extract_search_results_from_html(resp.text, limit=limit)
        except Exception:
            pass
        return []

    async def get_video_details(self, video_id: str) -> Optional[VideoMetadata]:
        await self._safe_delay()
        title = ""
        description = ""
        channel_name = "Creator"
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        tags: list[str] = []
        has_chapters = False

        # Stage 1: Official public oEmbed API for guaranteed title and channel name
        try:
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                o_resp = await client.get(oembed_url)
                if o_resp.status_code == 200:
                    o_data = o_resp.json()
                    title = o_data.get("title", "")
                    channel_name = o_data.get("author_name", "Creator")
                    if o_data.get("thumbnail_url"):
                        thumbnail_url = o_data.get("thumbnail_url")
        except Exception:
            pass

        # Stage 2: Public Watch Page for description, tags, and chapter markers
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(self.WATCH_URL, params={"v": video_id})
                if resp.status_code == 200:
                    html = resp.text
                    if not title:
                        title_match = re.search(r'<title>(.*?)( - YouTube)?</title>', html)
                        if title_match:
                            title = title_match.group(1).replace(" - YouTube", "").strip()

                    desc_match = re.search(r'<meta name="description" content="(.*?)">', html)
                    if desc_match:
                        description = desc_match.group(1)

                    keywords_match = re.search(r'<meta name="keywords" content="(.*?)">', html)
                    if keywords_match:
                        tags = [k.strip() for k in keywords_match.group(1).split(",") if k.strip()]

                    chan_match = re.search(r'<link itemprop="name" content="(.*?)">', html)
                    if chan_match and channel_name == "Creator":
                        channel_name = chan_match.group(1)

                    has_chapters = "00:00" in description or "0:00" in description
        except Exception:
            pass

        # Stage 3: yt-dlp fallback if title is still missing
        if not title:
            try:
                import yt_dlp
                ydl_opts = {
                    "quiet": True,
                    "skip_download": True,
                    "extract_flat": True,
                    "no_warnings": True,
                }
                loop = asyncio.get_event_loop()
                def extract_yt():
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        return ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                info = await loop.run_in_executor(None, extract_yt)
                if info:
                    title = info.get("title") or title
                    description = info.get("description") or description
                    channel_name = info.get("channel") or info.get("uploader") or channel_name
                    tags = info.get("tags") or tags
                    thumbnail_url = info.get("thumbnail") or thumbnail_url
            except Exception:
                pass

        if not title:
            return None

        return VideoMetadata(
            video_id=video_id,
            url=f"https://www.youtube.com/watch?v={video_id}",
            title=title,
            description=description,
            channel_id=None,
            channel_name=channel_name,
            channel_subscribers=None,
            published_date=None,
            views_count=None,
            likes_count=None,
            comments_count=None,
            duration_seconds=None,
            tags=tags,
            thumbnail_url=thumbnail_url,
            has_chapters=has_chapters,
            provenance=DataProvenance.PUBLIC,
        )


    async def get_channel_details(self, channel_id_or_handle: str) -> Optional[ChannelMetadata]:
        await self._safe_delay()
        handle_or_id = channel_id_or_handle.strip()
        url = f"https://www.youtube.com/{handle_or_id}" if handle_or_id.startswith("@") else f"https://www.youtube.com/channel/{handle_or_id}"
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    html = resp.text
                    title_match = re.search(r'<meta property="og:title" content="(.*?)">', html)
                    title = title_match.group(1) if title_match else handle_or_id
                    
                    desc_match = re.search(r'<meta property="og:description" content="(.*?)">', html)
                    desc = desc_match.group(1) if desc_match else ""

                    image_match = re.search(r'<meta property="og:image" content="(.*?)">', html)
                    avatar = image_match.group(1) if image_match else None

                    # Extract the canonical UC... channel ID
                    cid_match = (
                        re.search(r'itemprop="channelId" content="(UC[\w\-]+)"', html)
                        or re.search(r'itemprop="identifier" content="(UC[\w\-]+)"', html)
                        or re.search(r'["\']channelId["\']:\s*["\'](UC[\w\-]+)["\']', html)
                        or re.search(r'/channel/(UC[\w\-]+)', html)
                    )
                    canonical_cid = cid_match.group(1) if cid_match else (handle_or_id if handle_or_id.startswith("UC") else handle_or_id)

                    return ChannelMetadata(
                        channel_id=canonical_cid,
                        channel_title=title,
                        handle=handle_or_id if handle_or_id.startswith("@") else None,
                        description=desc,
                        subscriber_count=None,
                        video_count=None,
                        view_count=None,
                        avatar_url=avatar,
                        provenance=DataProvenance.PUBLIC,
                    )
        except Exception:
            pass
        return None

    async def get_channel_recent_videos(self, channel_id: str, limit: int = 30) -> list[VideoMetadata]:
        """
        Retrieves recent videos for a channel using YouTube's public RSS feed:
        https://www.youtube.com/feeds/videos.xml?channel_id=...
        Falls back to channel videos page or search if RSS is not directly resolved.
        """
        await self._safe_delay()
        cid = channel_id.strip()

        # If given a handle or username instead of a UC... ID, resolve channel details first
        if not cid.startswith("UC"):
            channel_meta = await self.get_channel_details(cid)
            if channel_meta and channel_meta.channel_id.startswith("UC"):
                cid = channel_meta.channel_id

        videos: list[VideoMetadata] = []

        # 1. Attempt YouTube public RSS feed (fast, rate-limit friendly, returns 15 most recent videos)
        if cid.startswith("UC"):
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
            try:
                async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                    resp = await client.get(rss_url)
                    if resp.status_code == 200 and resp.text:
                        videos = self._parse_rss_entries(resp.text, channel_id=cid)
            except Exception:
                pass

        if len(videos) >= min(limit, 10):
            return videos[:limit]

        # 2. Fallback: Parse /videos page HTML for initialData if RSS yielded insufficient results
        try:
            page_url = f"https://www.youtube.com/channel/{cid}/videos" if cid.startswith("UC") else f"https://www.youtube.com/{cid}/videos"
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(page_url)
                if resp.status_code == 200:
                    page_vids = extract_search_results_from_html(resp.text, limit=limit)
                    existing_ids = {v.video_id for v in videos}
                    for pv in page_vids:
                        if pv.video_id not in existing_ids:
                            videos.append(
                                VideoMetadata(
                                    video_id=pv.video_id,
                                    url=f"https://www.youtube.com/watch?v={pv.video_id}",
                                    title=pv.title,
                                    description=pv.description_snippet or "",
                                    channel_id=cid if cid.startswith("UC") else None,
                                    channel_name=pv.channel_name,
                                    views_count=pv.views_count,
                                    thumbnail_url=pv.thumbnail_url,
                                    provenance=DataProvenance.PUBLIC,
                                )
                            )
        except Exception:
            pass

        return videos[:limit]

    def _parse_rss_entries(self, xml_text: str, channel_id: str) -> list[VideoMetadata]:
        """Parses Atom XML feed entries from YouTube RSS."""
        import xml.etree.ElementTree as ET

        videos: list[VideoMetadata] = []
        try:
            root = ET.fromstring(xml_text)
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "yt": "http://www.youtube.com/xml/schemas/2015",
                "media": "http://search.yahoo.com/mrss/",
            }

            for entry in root.findall("atom:entry", ns):
                vid_id_elem = entry.find("yt:videoId", ns)
                if vid_id_elem is None or not vid_id_elem.text:
                    continue
                vid_id = vid_id_elem.text.strip()

                title_elem = entry.find("atom:title", ns)
                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

                published_elem = entry.find("atom:published", ns)
                published_date = published_elem.text[:10] if published_elem is not None and published_elem.text else None

                author_elem = entry.find("atom:author/atom:name", ns)
                channel_name = author_elem.text.strip() if author_elem is not None and author_elem.text else "Creator"

                media_group = entry.find("media:group", ns)
                description = ""
                thumbnail_url = f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"
                views_count = None

                if media_group is not None:
                    desc_elem = media_group.find("media:description", ns)
                    if desc_elem is not None and desc_elem.text:
                        description = desc_elem.text

                    thumb_elem = media_group.find("media:thumbnail", ns)
                    if thumb_elem is not None and "url" in thumb_elem.attrib:
                        thumbnail_url = thumb_elem.attrib["url"]

                    community = media_group.find("media:community", ns)
                    if community is not None:
                        stats = community.find("media:statistics", ns)
                        if stats is not None and "views" in stats.attrib:
                            try:
                                views_count = int(stats.attrib["views"])
                            except (ValueError, TypeError):
                                pass

                has_chapters = "00:00" in description or "0:00" in description

                videos.append(
                    VideoMetadata(
                        video_id=vid_id,
                        url=f"https://www.youtube.com/watch?v={vid_id}",
                        title=title,
                        description=description,
                        channel_id=channel_id,
                        channel_name=channel_name,
                        published_date=published_date,
                        views_count=views_count,
                        thumbnail_url=thumbnail_url,
                        has_chapters=has_chapters,
                        provenance=DataProvenance.PUBLIC,
                    )
                )
        except Exception:
            pass

        return videos
