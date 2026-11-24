# TubePilot AI — Production, SEO & GEO Roadmap

This roadmap documents the audit findings and the step-by-step implementation plan for taking TubePilot AI from localhost to a public-facing domain.

---

## 📋 1. Current Audit & Tool Status

| Tool / Module | Endpoint | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Keyword Research** | `POST /api/research/keyword` | ✅ Working (100%) | Multi-vector expansion, search intent classification, opportunity & competition scoring. |
| **Video SEO Audit** | `POST /api/audit/video` | ✅ Working (100%) | 18-point audit engine, 500-char tag check, CC check, SERP & thumbnail simulator. |
| **AI Creator Studio** | `POST /api/ai/*` | ✅ Working (100%) | Offline deterministic heuristic fallbacks + optional Ollama/OpenAI/Gemini. |
| **Content Calendar** | `POST /api/ai/calendar` | ✅ Working (100%) | Weekly roadmap generation and schedule planning. |
| **Channel Audit** | `POST /api/audit/channel` | ✅ Working (100%) | Metadata and recent video performance extraction via RSS / API v3. |
| **Outlier Finder** | `GET /api/competitor/outliers` | ✅ Working (100%) | Live MAD outlier detection and Z-score multiplier calculation. |
| **Competitor Comparison** | `POST /api/competitor/compare` | ✅ Working (100%) | Channel metrics, shared/unique topics, and content gap matrix. |

### 🔧 Implemented Architecture:
- **`get_channel_recent_videos`:**
  - Public Scraper: YouTube Public RSS Feed (`https://www.youtube.com/feeds/videos.xml?channel_id=...`) with Atom XML parsing for fast, rate-limit-free retrieval of videos and views.
  - Official API: YouTube Data API v3 `playlistItems` via the channel's uploads playlist (`UU...`) with full video statistics hydration.

---

## 🌐 2. Public Domain & SEO / AEO / GEO Strategy

### A. Technical & Traditional SEO
1. **Public Marketing Pages (Pre-rendered / SSR):**
   - Create dedicated public landing pages:
     - `/youtube-keyword-tool`
     - `/youtube-video-seo-checker`
     - `/youtube-title-generator`
2. **Metadata & OpenGraph:**
   - Dynamic meta tags (`title`, `description`, `canonical`, `og:image`, `twitter:card`).
3. **Structured Data (Schema.org JSON-LD):**
   - `WebApplication` / `SoftwareApplication`
   - `FAQPage`
   - `HowTo`
4. **Indexing Files:**
   - Auto-generated `sitemap.xml` and `robots.txt`.

### B. AEO (Answer Engine Optimization)
- **Direct Answer Blocks:** 40-60 word concise answers under H2 headers for Google AI Overviews and Featured Snippets.
- **Comparison Pages:** e.g., "TubePilot vs vidIQ", "TubePilot vs TubeBuddy".
- **Structured Tables:** 18-point SEO checklist tables and MAD outlier benchmark reference.

### C. GEO (Generative Engine Optimization)
- **`llms.txt` & `llms-full.txt`:** Place at the root of the domain (`/llms.txt`) detailing the platform capabilities, algorithms, and APIs for AI search engines.
- **AI Crawler Whitelist (`robots.txt`):** Allow `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`.
- **E-E-A-T & Primary Source Authority:** Publish documentation on the mathematical formulas (Median Absolute Deviation, 10-signal Opportunity Scorer).

---

## 🛡️ 3. Production Deployment Checklist

- [ ] Reverse proxy with Nginx & Let's Encrypt SSL.
- [ ] Redis or in-memory leaky-bucket Rate Limiter (max 30-60 req/min per IP).
- [ ] Production CORS policy restriction (lock down to public domain).
- [ ] Process management via Docker Compose or Systemd.

