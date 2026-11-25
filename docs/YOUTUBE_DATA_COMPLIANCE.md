# YouTube Data Compliance & Provenance Audit
### TubePilot AI / FreeYouTubeTools SEO Architecture

This document audits and details every data collection method used within the TubePilot AI / YouTube SEO platform. It details endpoint URLs, rate limiting, data limitations, and verification of policy compliance.

---

## 1. Compliance Principles & Core Policy

1. **Zero CAPTCHA / Bot Defense Bypass:**  
   TubePilot AI never executes automated CAPTCHA solving, IP rotators to bypass rate blocks, or headers designed to evade anti-bot security. If Google or YouTube returns an HTTP 429, `consent.youtube.com`, or `sorry/index` challenge page, all modules immediately halt with a structured error.
2. **No Private Data Harvesting:**  
   The application exclusively parses information that is either:
   - Officially provided by Google via the YouTube Data API v3.
   - Publicly accessible via standards-compliant RSS Atom feeds.
   - Publicly indexed via oEmbed or open meta tags on public watch pages.
   - Publicly returned by Google Suggest queries.
3. **Transparent Data Provenance:**  
   Every payload returned by backend endpoints tags its data origin using `DataProvenance`:
   - `OFFICIAL`: Verified from YouTube Data API v3.
   - `PUBLIC_SCRAPED`: Parsed from public oEmbed / OpenGraph / meta tags.
   - `ESTIMATED`: Algorithmic approximation (clearly labeled; never claims to be actual private analytics).
   - `MOCK`: Synthetic test data for testing/offline environments.

---

## 2. Detailed Data Source Audit

| Data Source | Exact Endpoint / Protocol | Authentication | Used For | Limitations & Fallback |
|---|---|---|---|---|
| **Google Public Suggest** | `https://suggestqueries.google.com/complete/search?client=firefox&ds=yt` | None (Public) | Search suggestion matrix, keyword seed expansion, alphabetical & prepositional discovery. | Rate-limited. If network drops or times out, falls back to deterministic rule-based modifier expansion. |
| **YouTube oEmbed API** | `https://www.youtube.com/oembed?url=...&format=json` | None (Official Google oEmbed) | High-accuracy video title, channel name, and default thumbnail resolution. | Only provides basic embed metadata. Does not provide view counts, tags, or descriptions. |
| **Public Watch Metadata** | `https://www.youtube.com/watch?v={id}` | None (Public HTML) | Video description, meta keywords/tags, chapter markers. | Halts if `consent.youtube.com` or `sorry/index` appears. Never attempts to bypass challenges. |
| **Channel RSS Atom Feed** | `https://www.youtube.com/feeds/videos.xml?channel_id={id}` | None (Official Atom Feed) | Recent 15 videos, publication cadence, video IDs, titles, and timestamps. | Limited to the 15 most recent uploads. |
| **YouTube Data API v3** | `https://www.googleapis.com/youtube/v3/*` | Google API Key (`YOUTUBE_API_KEY`) | Exact video statistics (views, likes, comments), comprehensive search lists, channel statistics. | Subject to Google Developer quota (10,000 units/day). Configurable and completely optional. |
| **Deterministic Heuristic Engine** | In-Memory Mathematics | None (Local CPU) | Relative Demand Index, Competition Estimation, Opportunity Score (0-100), Outlier Multiplier (MAD). | Clearly documented in `docs/DATA_ACCURACY_FORMULAS.md`. Never claims to represent private search volume. |

---

## 3. Rate Limiting & Safety Measures

- **Jittered Asynchronous Delay:**  
  Public requests in `PublicYouTubeProvider` execute a randomized jitter (`asyncio.sleep(0.15 to 0.45s)`) to prevent burst requests.
- **In-Memory Cache (900s TTL):**  
  Every query (keyword research, channel audit, video audit) is cached in-memory (`app.core.cache`) for 15 minutes. Repeated searches for the same keyword do not hit external endpoints.
- **Circuit Breaker:**  
  If any external endpoint fails 3 consecutive times, downstream calls are throttled and fallback heuristics are activated.

---

## 4. Verification Checklist

- [x] No undocumented or private internal YouTube RPC endpoints (`/youtubei/v1/*`) are used.
- [x] No cookie hijacking, account credential harvesting, or OAuth token spoofing.
- [x] All metrics generated mathematically are clearly stamped with estimation disclaimers in the UI.
- [x] System operates 100% deterministically and stably even when completely offline using the Mock Provider.
