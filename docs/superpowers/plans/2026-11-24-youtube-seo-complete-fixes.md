# YouTube SEO Complete Suite Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

This plan addresses all identified incomplete features and gaps in TubePilot AI:
1. Live channel recent video extraction via YouTube public RSS feeds and channel ID resolution.
2. Official YouTube API v3 `playlistItems` uploads playlist (`UU...`) retrieval.
3. 500-character tag limit and Closed Captions (CC) SEO checks in the 18-point audit engine.
4. YouTube Search & Mobile Feed SERP Simulator with Thumbnail Preview in the frontend.
5. Unit tests validating all new capabilities.

---

### Task 1: Public YouTube Provider Recent Videos via RSS Feed
- [ ] In `backend/app/youtube/scraper.py`:
  - Enhance `get_channel_details` to extract `channel_id` (the `UC...` ID) from HTML meta tags or link tags even when given an `@handle`.
  - Implement `get_channel_recent_videos` using YouTube's public RSS feed: `https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}`.
  - Parse Atom XML entries (`<yt:videoId>`, `<title>`, `<media:group>`, `<media:community><media:statistics views="...">`, `<published>`).
  - Fallback gracefully to search query if RSS is not available.

### Task 2: Official YouTube API v3 Recent Videos via Uploads Playlist
- [ ] In `backend/app/youtube/api_client.py`:
  - Implement `get_channel_recent_videos` using the channel's `UU...` playlist (replacing `UC` with `UU`).
  - Call `playlistItems.list` to get video IDs.
  - Call `videos.list` to get snippet, statistics (views, likes, comments), and tags.

### Task 3: Enhance Video Audit Engine with 500-Character Tag Validator and CC Checks
- [ ] In `backend/app/seo/audit_engine.py` and `backend/app/models/audit.py`:
  - Add tag cumulative character length check (max 500 characters allowed by YouTube).
  - Add Closed Captions / Subtitles SEO check in `Engagement & Context Signals`.
  - Keep 7 categories and 100-point total score mathematically balanced.
- [ ] In `backend/app/api/routes/audit.py`:
  - Accept `has_captions: Optional[bool] = False` in `VideoAuditRequest`.

### Task 4: Interactive SERP & Thumbnail Preview in Frontend
- [ ] Create `frontend/src/components/common/SerpThumbnailPreview.tsx`:
  - Realistic YouTube dark theme search card and mobile feed card.
  - Toggle between "Desktop Search Result" and "Mobile Feed Preview".
  - Dynamic title truncation visualizer (showing where YouTube cuts off the title on mobile vs desktop).
  - Thumbnail URL input or file upload preview, duration badge, view count, published time, and channel avatar.
- [ ] Integrate into `frontend/src/app/video-audit/page.tsx` and `frontend/src/app/ai-studio/page.tsx`.

### Task 5: Verification & Tests
- [ ] Add unit tests in `backend/tests/test_audit.py` for 500-char tag limit and CC checks.
- [ ] Add unit tests in `backend/tests/test_channel_recent.py` for RSS XML parsing and uploads playlist.
- [ ] Verify frontend compiles cleanly with `tsc --noEmit`.
- [ ] Run pytest on all unit tests.
