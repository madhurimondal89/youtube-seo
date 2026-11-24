import re
import json
from typing import Optional, Any
from app.models.video import VideoSearchResult, VideoMetadata
from app.models.channel import ChannelMetadata
from app.models.common import DataProvenance

INITIAL_DATA_REGEX = re.compile(r"var ytInitialData = ({.*?});</script>", re.DOTALL)
INITIAL_PLAYER_REGEX = re.compile(r"var ytInitialPlayerResponse = ({.*?});</script>", re.DOTALL)

def parse_views_string(views_str: str) -> Optional[int]:
    """Parses strings like '1.2M views', '45K views', '12,345 views' to integer."""
    if not views_str:
        return None
    clean = views_str.lower().replace("views", "").replace(",", "").strip()
    try:
        if "m" in clean:
            return int(float(clean.replace("m", "").strip()) * 1_000_000)
        elif "k" in clean:
            return int(float(clean.replace("k", "").strip()) * 1_000)
        elif "b" in clean:
            return int(float(clean.replace("b", "").strip()) * 1_000_000_000)
        return int(clean)
    except (ValueError, TypeError):
        return None

def parse_duration_string(duration_str: str) -> Optional[int]:
    """Parses '12:34' or '1:02:45' into seconds."""
    if not duration_str:
        return None
    parts = duration_str.strip().split(":")
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except (ValueError, TypeError):
        return None
    return None

def extract_search_results_from_html(html_text: str, limit: int = 25) -> list[VideoSearchResult]:
    """
    Safely parses public YouTube search page HTML to extract public video search cards.
    """
    results: list[VideoSearchResult] = []
    match = INITIAL_DATA_REGEX.search(html_text)
    if not match:
        return results

    try:
        data = json.loads(match.group(1))
        # Navigate through standard YouTube initial data structure
        contents = (
            data.get("contents", {})
            .get("twoColumnSearchResultsRenderer", {})
            .get("primaryContents", {})
            .get("sectionListRenderer", {})
            .get("contents", [])
        )
        
        rank = 1
        for section in contents:
            item_section = section.get("itemSectionRenderer", {}).get("contents", [])
            for item in item_section:
                video_render = item.get("videoRenderer")
                if not video_render:
                    continue
                
                vid_id = video_render.get("videoId")
                if not vid_id:
                    continue

                title_obj = video_render.get("title", {})
                title = ""
                if "runs" in title_obj and title_obj["runs"]:
                    title = title_obj["runs"][0].get("text", "")
                elif "simpleText" in title_obj:
                    title = title_obj["simpleText"]

                # Channel info
                owner_obj = video_render.get("ownerText", {})
                chan_name = ""
                chan_id = None
                if "runs" in owner_obj and owner_obj["runs"]:
                    chan_name = owner_obj["runs"][0].get("text", "")
                    nav = owner_obj["runs"][0].get("navigationEndpoint", {}).get("browseEndpoint", {})
                    chan_id = nav.get("browseId")

                # Views
                view_obj = video_render.get("viewCountText", {})
                view_text = view_obj.get("simpleText") or ""
                views_count = parse_views_string(view_text)

                # Duration
                length_obj = video_render.get("lengthText", {})
                duration_text = length_obj.get("simpleText") or ""
                duration_sec = parse_duration_string(duration_text)

                # Publish time
                pub_obj = video_render.get("publishedTimeText", {})
                pub_text = pub_obj.get("simpleText") or ""

                # Snippet
                desc_snippets = video_render.get("detailedMetadataSnippets", [])
                snippet = ""
                if desc_snippets and "snippetText" in desc_snippets[0]:
                    snippet_runs = desc_snippets[0]["snippetText"].get("runs", [])
                    snippet = "".join([r.get("text", "") for r in snippet_runs])

                # Thumbnail
                thumbs = video_render.get("thumbnail", {}).get("thumbnails", [])
                thumb_url = thumbs[-1].get("url") if thumbs else f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"

                results.append(
                    VideoSearchResult(
                        video_id=vid_id,
                        title=title,
                        channel_name=chan_name or "YouTube Creator",
                        channel_id=chan_id,
                        published_time_text=pub_text,
                        views_count=views_count,
                        views_text=view_text,
                        duration_text=duration_text,
                        duration_seconds=duration_sec,
                        thumbnail_url=thumb_url,
                        description_snippet=snippet,
                        rank_position=rank,
                        provenance=DataProvenance.PUBLIC,
                    )
                )
                rank += 1
                if len(results) >= limit:
                    return results

    except Exception:
        pass

    return results
