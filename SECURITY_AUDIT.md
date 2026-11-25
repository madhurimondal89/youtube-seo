# Security & Production Hardening Audit Report
### TubePilot AI / YouTube SEO Platform (`seo.freeyoutubetools.com`)

**Audit Date:** November 25, 2026  
**Auditor:** Senior Security & Quality Engineering  
**Scope:** Final Production Hardening & Compliance Pass  
**Overall Status:** PASSED (Zero High/Critical Vulnerabilities)  

---

## 1. P0 – Production Secrets & Startup Hardening

### A. Secret Strength Enforcement (`validate_secret_strength`)
- **Vulnerability Addressed:** Insecure default or placeholder secrets left in production `.env` files.
- **Controls Implemented:**
  - Added `validate_secret_strength()` in `backend/app/core/security.py`.
  - Blocks all known default placeholders:
    `INSECURE_SECRET_PLACEHOLDERS = {"youtube-seo-insecure-secret-key-change-me", "change-this-secret-key-in-production-random-hex-string", "change-me", "secret", "password", "default", "123456"}`
  - Blocks any key containing keywords: `change-this`, `insecure`, `change-me`, `example`, `placeholder`, `dev-`.
  - Enforces minimum length of **32 characters**.
- **Startup Lifespan Guard:**
  - In `backend/app/main.py`, FastAPI's `lifespan` handler checks `APP_ENV`. If `APP_ENV=production` or `APP_ENV=prod`, startup immediately raises `RuntimeError` if `SECRET_KEY` is missing, short, or placeholder.
  - In `docker-compose.coolify.yml`, variable substitution syntax `${SECRET_KEY:?SECRET_KEY must be set in environment}` causes Docker Compose itself to fail immediately if the secret is omitted.

### B. Secret Masking & Response Protection
- **Zero Leakage:** `SECRET_KEY` is strictly used server-side and never returned in `/api/system/settings`, `/api/system/status`, or any response payload.
- **Provider API Keys:** All API keys (`GROQ_API_KEY`, `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `YOUTUBE_API_KEY`) are masked (`gsk_••••••••` or `AIza••••••••`) before being serialized in JSON.

### C. OAuth Token Security Architecture
- If users connect channel analytics via OAuth 2.0:
  - Scopes are restricted strictly to read-only (`https://www.googleapis.com/auth/yt-analytics.readonly`).
  - Refresh tokens are encrypted at rest using AES-GCM-256 with key derivation from `SECRET_KEY`.
  - OAuth tokens are never logged or exposed in client-side responses or query strings.

---

## 2. P0 – Ollama Connectivity & Docker Isolation

### A. URL Resolution Audit
- **Problem Addressed:** Inside Docker containers, `127.0.0.1` refers to the container itself, failing when trying to connect to Ollama running on the VPS host.
- **Controls Implemented:**
  - Added `extra_hosts: ["host.docker.internal:host-gateway"]` in `docker-compose.coolify.yml`.
  - Mapped default `OLLAMA_BASE_URL` to `http://host.docker.internal:11434` for Docker environments.
  - Added URL normalization in `LocalOllamaProvider` (automatically prepends `http://` if missing and strips trailing slashes).
  - Added helpful diagnostic hint in `test_connection()` and error handling if `127.0.0.1` or `localhost` is used inside Docker.
  - Added an optional companion `ollama` Docker service (`profile: local-ai`) for self-contained deployments.

### B. Graceful Degradation
- If Ollama server is unreachable, offline, or times out, `ResilientAIProvider` automatically falls back to deterministic mathematical SEO scoring without crashing the user's session or throwing HTTP 500 errors.

---

## 3. P0 – YouTube Developer Policy Compliance

### A. Data Collection Method Review
- **Public Suggest:** Uses browser-standard suggestion endpoint (`suggestqueries.google.com/complete/search?client=firefox&ds=yt`).
- **oEmbed:** Uses Google's official public oEmbed standard (`youtube.com/oembed`).
- **RSS:** Uses official channel Atom feeds (`youtube.com/feeds/videos.xml`).
- **Public Watch Metadata:** Reads only open OpenGraph & HTML `<meta>` tags.
- **Official API:** Fully supports Google YouTube Data API v3 when configured.

### B. Anti-Bot & CAPTCHA Compliance
- **Zero Bypass:** No CAPTCHA solvers, cloudflare bypass tools, headless browser spoofing, or residential proxy rotators are present in the codebase.
- **Immediate Halt:** If `consent.youtube.com` or `sorry/index` is returned by Google, the scraper immediately and gracefully halts.
- **Provenance Stamping:** Every metric returned indicates its provenance (`OFFICIAL`, `PUBLIC`, `CALCULATED`, `ESTIMATED`, `RELATIVE`, or `UNAVAILABLE`).

---

## 4. P1 – 9-Provider Consistency & Deployment Hardening

### A. Provider Uniformity
All 9 advertised AI providers are supported across config, registry, settings API, frontend UI, and documentation:
1. Google Gemini
2. OpenAI
3. Groq Fast Inference
4. DeepSeek AI
5. OpenRouter
6. Local Ollama
7. Local LM Studio
8. LocalAI
9. Custom OpenAI-compatible endpoints

### B. Coolify & Traefik Infrastructure Security
- **No Host Port 80/443 Conflicts:** Traefik binds ports 80/443; containers bind zero host ports.
- **No Public Backend Port:** FastAPI port 8000 is internal-only to Docker network `coolify`.
- **Internal Reverse Proxy:** Next.js rewrites `/api/*` to `http://backend:8000/api/*` internally, eliminating external CORS and proxy exposure.
- **Data Persistence:** SQLite database volume `tubepilot_data` prevents data loss during rebuilds.

---

## 5. Audit Conclusion
The TubePilot AI codebase meets all P0 and P1 security, compliance, and production readiness requirements for deployment on `seo.freeyoutubetools.com`.
