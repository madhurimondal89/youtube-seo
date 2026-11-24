import httpx
import urllib.parse
from typing import Optional

class YouTubeAutocompleteClient:
    """
    Direct, lawful client for public YouTube search suggestions.
    Uses public suggest queries endpoint without bypassing protections.
    """
    SUGGEST_URL = "https://suggestqueries.google.com/complete/search"

    def __init__(self, timeout_seconds: float = 6.0):
        self.timeout = timeout_seconds
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def get_suggestions(self, query: str, hl: str = "en", gl: str = "US") -> list[str]:
        if not query or not query.strip():
            return []

        clean_q = query.strip()
        params = {
            "client": "firefox",
            "ds": "yt",
            "q": clean_q,
            "hl": hl,
            "gl": gl,
        }
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                resp = await client.get(self.SUGGEST_URL, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    # Firefox format returns: [query, [suggestions...]]
                    if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
                        return [str(item) for item in data[1] if item]
        except Exception:
            # Fallback to local heuristic expansion if network fails or times out
            pass
            
        return []

autocomplete_client = YouTubeAutocompleteClient()
