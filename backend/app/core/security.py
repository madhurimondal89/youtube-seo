import re
from urllib.parse import urlparse, parse_qs
from typing import Optional

YOUTUBE_VIDEO_ID_REGEX = re.compile(r"^[a-zA-Z0-9_-]{11}$")
YOUTUBE_CHANNEL_ID_REGEX = re.compile(r"^UC[a-zA-Z0-9_-]{22}$")
YOUTUBE_HANDLE_REGEX = re.compile(r"^@[a-zA-Z0-9_.-]{3,30}$")

def sanitize_keyword(keyword: str) -> str:
    """Strip dangerous characters and trim length."""
    clean = re.sub(r"[\r\n\t\x00-\x1f]", " ", keyword)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean[:120]

def extract_video_id(url_or_id: str) -> Optional[str]:
    """
    Safely extracts an 11-character YouTube video ID from various URL formats or returns the ID if valid.
    Protects against SSRF and invalid inputs.
    """
    text = url_or_id.strip()
    if YOUTUBE_VIDEO_ID_REGEX.match(text):
        return text

    try:
        parsed = urlparse(text)
        if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
            if parsed.path == "/watch":
                qs = parse_qs(parsed.query)
                v_list = qs.get("v")
                if v_list and YOUTUBE_VIDEO_ID_REGEX.match(v_list[0]):
                    return v_list[0]
            elif parsed.path.startswith("/shorts/"):
                potential_id = parsed.path.split("/")[2]
                if YOUTUBE_VIDEO_ID_REGEX.match(potential_id):
                    return potential_id
            elif parsed.path.startswith("/live/"):
                potential_id = parsed.path.split("/")[2]
                if YOUTUBE_VIDEO_ID_REGEX.match(potential_id):
                    return potential_id
        elif parsed.hostname in ("youtu.be",):
            potential_id = parsed.path.lstrip("/").split("?")[0]
            if YOUTUBE_VIDEO_ID_REGEX.match(potential_id):
                return potential_id
    except Exception:
        return None
    return None

def extract_channel_identifier(url_or_handle: str) -> Optional[str]:
    """
    Safely extracts channel ID, handle (@username), or custom URL from input string.
    """
    text = url_or_handle.strip()
    if YOUTUBE_CHANNEL_ID_REGEX.match(text) or YOUTUBE_HANDLE_REGEX.match(text):
        return text
    
    if text.startswith("@") and len(text) <= 32:
        return text

    try:
        parsed = urlparse(text)
        if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
            parts = [p for p in parsed.path.split("/") if p]
            if not parts:
                return None
            if parts[0].startswith("@"):
                return parts[0]
            if parts[0] == "channel" and len(parts) > 1 and YOUTUBE_CHANNEL_ID_REGEX.match(parts[1]):
                return parts[1]
            if parts[0] == "c" and len(parts) > 1:
                return parts[1]
    except Exception:
        return None
    return None
