# TubePilot AI — Research Engine Specification

The Research Engine collects, expands, and normalizes public YouTube data lawfully and respectfully without circumventing protections.

---

## 1. Provider Abstraction

All data access is mediated through the `YouTubeProvider` abstract base class:

```python
class YouTubeProvider(ABC):
    @abstractmethod
    async def get_autocomplete_suggestions(self, query: str) -> list[str]: ...
    
    @abstractmethod
    async def search_videos(self, query: str, limit: int = 20) -> list[VideoSearchResult]: ...
    
    @abstractmethod
    async def get_video_details(self, video_id: str) -> VideoMetadata | None: ...
    
    @abstractmethod
    async def get_channel_details(self, channel_id_or_handle: str) -> ChannelMetadata | None: ...
    
    @abstractmethod
    async def get_channel_recent_videos(self, channel_id: str, limit: int = 30) -> list[VideoMetadata]: ...
```

Three concrete implementations are provided:
1. `MockYouTubeProvider`: Zero network dependencies; generates realistic, mathematically coherent data for offline testing and continuous integration.
2. `PublicYouTubeProvider`: Uses YouTube public suggest endpoints and lightweight initial-data parsers with strict token-bucket rate limiting and randomized user-agent headers.
3. `OfficialAPIYouTubeProvider`: Activated when `YOUTUBE_API_KEY` is provided; uses official Google YouTube Data API v3 endpoints.

---

## 2. Autocomplete & Alphabet Expansion

To discover long-tail and high-opportunity keywords, the engine executes:
- **Root Suggestions**: `[seed]`
- **Alphabet Suffix Expansion**: `[seed] + 'a'`, `[seed] + 'b'`, ..., `[seed] + 'z'`
- **Question & Intent Prefixes**:
  - `how to [seed]`
  - `best [seed] for`
  - `why [seed]`
  - `[seed] vs`
  - `[seed] tutorial`
  - `[seed] for beginners`
  - `[seed] 2026`

Each expanded candidate is normalized:
- Lowercase conversion
- Whitespace stripping
- Deduplication via token set matching
- Stopword preservation for exact intent matching

---

## 3. Data Provenance & Ethical Scraping Rules

- **No CAPTCHA Bypassing**: If YouTube serves a bot verification challenge, the job immediately halts gracefully, reports `CHALLENGE_DETECTED`, and serves cached or fallback results.
- **Strict Pacing**: Calls to public endpoints are spaced with randomized jitter (250ms–750ms) to ensure non-disruptive, polite querying.
- **Clear Labeling**: Every returned field includes a `provenance` property (`Official`, `Public`, `Calculated`, `Estimated`, `Relative`, or `Unavailable`).
