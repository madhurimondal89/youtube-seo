# TubePilot — System Architecture

> **Guiding Principle**: Build for scale, but do not pay for scale until scale exists.

TubePilot is engineered as a **DATA + STATISTICS + SEO ENGINE FIRST, AI SECOND** platform.
AI enhances results; it never generates, calculates, or replaces deterministic scores.

---

## 1. Architectural Principles

| # | Principle | Implementation |
|---|-----------|----------------|
| 1 | **Deterministic Core** | All SEO/research metrics are computed by reproducible mathematical formulas (see `docs/SEO_SCORING.md`). LLMs never produce numerical scores. |
| 2 | **AI Optional** | The entire platform — research, keyword scoring, auditing, competitor analysis, outlier detection — functions with `AI_ENABLED=false`. |
| 3 | **Local-First User Data** | User-owned data (projects, research results, keyword lists, reports, settings) lives in the browser's IndexedDB by default. The VPS stores no user research data permanently. |
| 4 | **Provider Abstractions** | Every external dependency (YouTube data, AI inference, embeddings, cache, storage, jobs, database) is accessed through a formal interface/ABC. Providers are swappable without changing business logic. |
| 5 | **No Fake Metrics** | Every metric has documented provenance: `Official`, `Public`, `Calculated`, `Estimated`, `Relative`, or `Unavailable`. |
| 6 | **Docker-First, Coolify-Compatible** | The application is deployed via GitHub → Coolify → Docker → Hostinger KVM 4. No Kubernetes, AWS, or GCP required for MVP. |
| 7 | **Stateless VPS** | The application container can be recreated at any time without data loss. In-memory TTL cache is deliberately volatile. |
| 8 | **Graceful Degradation** | Every external dependency can fail. The UI provides meaningful messages; core features continue operating. |

---

## 2. Deployment Model

```
Developer Workstation
        │
        │  git push
        ▼
   GitHub Repository
        │
        │  Webhook
        ▼
     Coolify
        │
        │  docker build + deploy
        ▼
  Hostinger KVM 4 VPS
  (4 vCPU, 16 GB RAM, 200 GB NVMe)
        │
  ┌─────┼─────┐
  │     │     │
  ▼     ▼     ▼
Nginx Next.js FastAPI
(80)  (3000) (8000)
              │
      ┌───────┼───────┐
      ▼       ▼       ▼
  YouTube   SEO     AI Layer
  Engine   Engine  (Optional)
```

**Future (when load demands it):**
```
Cloudflare CDN / WAF
        │
  Load Balancer
        │
 ┌──────┴──────┐
 │             │
App Server 1  App Server 2
        │
      Redis
        │
   PostgreSQL
        │
  Worker Cluster
```

---

## 3. Provider Abstraction Map

All external dependencies are accessed exclusively through these interfaces:

### 3.1 ResearchProvider (`YouTubeProvider`)

```python
class YouTubeProvider(ABC):
    async def get_autocomplete_suggestions(query: str) -> list[str]
    async def search_videos(query: str, limit: int) -> list[VideoSearchResult]
    async def get_video_details(video_id: str) -> VideoMetadata | None
    async def get_channel_details(channel_id_or_handle: str) -> ChannelMetadata | None
    async def get_channel_recent_videos(channel_id: str, limit: int) -> list[VideoMetadata]
```

**Active implementations:**
- `MockYouTubeProvider` — offline testing, CI
- `PublicYouTubeProvider` — scraper with rate limiting, jitter, CAPTCHA detection
- `OfficialAPIYouTubeProvider` — YouTube Data API v3
- `YouTubeStudioCSVProvider` — user-uploaded Studio export *(Phase 7)*

**Selection:** `YOUTUBE_PROVIDER` env var → `factory.py`

---

### 3.2 AIProvider

```python
class AIProvider(ABC):
    async def is_available() -> bool
    async def generate_text(prompt, system_prompt, max_tokens) -> str
    def get_provider_name() -> str
```

**Active implementations:**
- `DisabledAIProvider` — default; all AI calls return deterministic fallback
- `OllamaProvider` — local CPU inference (Qwen 2.5 0.5B–4B)
- `OmniRouteProvider` — internal AI gateway *(Phase 5)*
- `FreeLLMAPIProvider` — free AI gateway *(Phase 5)*
- `GeminiProvider` — Google Gemini direct *(Phase 5)*
- `GroqProvider` — Groq direct *(Phase 5)*
- `OptionalOpenAIProvider` — user-supplied OpenAI key

**Fallback chain (configurable via `AI_PROVIDER_CHAIN` env):**
```
OmniRoute → FreeLLMAPI → Gemini → Groq → Ollama → Disabled
```

**Selection:** `AIProviderFactory` reads `AI_PROVIDER_CHAIN` and wraps providers in `AIProviderChain`.

---

### 3.3 EmbeddingProvider

```python
class EmbeddingProvider(ABC):
    async def is_available() -> bool
    async def embed(texts: list[str]) -> list[list[float]]
    def get_provider_name() -> str
```

**Active implementations:**
- `TFIDFEmbeddingProvider` — deterministic fallback using TF-IDF (default)
- `OmniRouteEmbeddingProvider` — via OmniRoute gateway *(Phase 6)*
- `JinaEmbeddingProvider` — Jina AI *(Phase 6)*
- `OllamaEmbeddingProvider` — local embedding model *(Phase 6)*

---

### 3.4 CacheProvider

```python
class CacheProvider(ABC):
    def get(key: str) -> Any | None
    def set(key: str, value: Any, ttl_seconds: int | None) -> None
    def delete(key: str) -> bool
    def clear() -> None
```

**Active implementations:**
- `MemoryCacheProvider` — in-process TTL dict (current `InMemoryTTLCache`, wrapped)
- `RedisCacheProvider` — future, when horizontal scaling requires shared cache

**Cache key conventions:**
```
youtube:search:{query}:{region}:{language}
youtube:video:{video_id}
youtube:channel:{channel_id}
keyword:suggestions:{query}:{language}
video:analysis:{video_id}
```

---

### 3.5 StorageProvider

```python
class StorageProvider(ABC):
    async def save(namespace: str, key: str, data: dict) -> None
    async def load(namespace: str, key: str) -> dict | None
    async def list(namespace: str) -> list[str]
    async def delete(namespace: str, key: str) -> None
```

**Namespaces:** `projects`, `keywords`, `research`, `competitors`, `reports`, `settings`

**Active implementations:**
- `BrowserStorageProvider` — IndexedDB (TypeScript, frontend) — **default**
- `GoogleDriveStorageProvider` — optional OAuth sync *(Phase 7)*
- `ServerStorageProvider` — future, for team/enterprise use *(Post-MVP)*

---

### 3.6 DatabaseProvider

```python
class DatabaseProvider(ABC):
    async def get_user(user_id: str) -> UserRecord | None
    async def upsert_user(record: UserRecord) -> None
    async def get_quota(user_id: str) -> QuotaRecord | None
    async def upsert_quota(record: QuotaRecord) -> None
```

**Active implementations:**
- `NullDatabaseProvider` — stateless no-op (MVP default; no DB required)
- `SQLiteProvider` — local/single-user deployments *(Phase 9)*
- `PostgreSQLProvider` — production multi-user deployments *(Post-MVP)*

---

### 3.7 JobQueueProvider

```python
class JobQueueProvider(ABC):
    async def enqueue(job_type: str, payload: dict) -> str  # returns job_id
    async def get_status(job_id: str) -> JobStatus
    async def get_result(job_id: str) -> dict | None
    async def cancel(job_id: str) -> bool
```

**Active implementations:**
- `InProcessJobQueue` — asyncio.Queue + background tasks *(Phase 8)*
- `RedisJobQueue` — future, for distributed workers *(Post-MVP)*

**Job flow:**
```
POST /api/research/bulk  →  JobQueue.enqueue()
                              │
                         Background worker
                              │
                         StorageProvider.save()
                              │
                         GET /api/jobs/{id}  →  poll status
```

---

## 4. User Data Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      User's Browser                         │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                IndexedDB (Local-First)               │   │
│  │  projects/ · keywords/ · research/ · competitors/   │   │
│  │  reports/ · settings/ · cached_results/             │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │ optional sync                     │
└─────────────────────────┼───────────────────────────────── ┘
                          │
                          ▼ (Google Drive OAuth — Phase 7)
                ┌──────────────────┐
                │  User's Google   │
                │  Drive Account   │
                │  TubePilot/      │
                │  ├─ Projects/    │
                │  ├─ Research/    │
                │  ├─ Keywords/    │
                │  └─ Reports/     │
                └──────────────────┘
```

**Server stores only:**
- Authentication tokens / session metadata
- Subscription / quota state (when auth is enabled)
- Job metadata (job_id, status, expiry)
- Application configuration

**Server never stores:** user research results, keyword lists, competitor data, generated reports, preferences.

---

## 5. AI Architecture

```
TubePilot API Request
        │
        ▼
AIProviderChain
        │
   ┌────┴────────────────────────────┐
   │  try #1: OmniRoute              │
   │  try #2: FreeLLMAPI             │
   │  try #3: Direct Gemini          │
   │  try #4: Direct Groq            │
   │  try #5: Local Ollama           │
   │  fallback: DisabledAIProvider   │
   └─────────────────────────────────┘
        │
        ▼
Deterministic heuristic templates
(title formulas, description templates,
 content calendar matrices)
```

OmniRoute and FreeLLMAPI are **internal gateways** — never exposed as public unauthenticated APIs.
TubePilot controls rate limiting, quotas, and model selection for all AI traffic.

---

## 6. Directory Layout

```
tubepilot/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py                  # FastAPI app, health/ready, CORS
│       ├── ai/
│       │   ├── base.py              # AIProvider ABC
│       │   ├── chain.py             # AIProviderChain (fallback logic)  [NEW]
│       │   ├── factory.py           # builds chain from env config       [NEW]
│       │   ├── ollama_provider.py
│       │   ├── omniroute_provider.py  [NEW]
│       │   ├── freellm_provider.py    [NEW]
│       │   ├── gemini_provider.py     [NEW]
│       │   ├── groq_provider.py       [NEW]
│       │   ├── cloud_provider.py    # OpenAI + DisabledAIProvider
│       │   └── studio.py            # title/desc/tag generators
│       ├── embeddings/              [NEW]
│       │   ├── base.py              # EmbeddingProvider ABC
│       │   ├── tfidf_provider.py    # deterministic fallback
│       │   └── factory.py
│       ├── youtube/
│       │   ├── base.py              # YouTubeProvider ABC
│       │   ├── factory.py
│       │   ├── mock_provider.py
│       │   ├── scraper.py           # PublicYouTubeProvider
│       │   ├── api_client.py        # OfficialAPIYouTubeProvider
│       │   ├── autocomplete.py
│       │   ├── parser.py
│       │   └── csv_provider.py      [NEW - Phase 7]
│       ├── seo/
│       │   ├── keyword_engine.py
│       │   ├── intent.py
│       │   ├── clustering.py
│       │   ├── competition.py
│       │   ├── opportunity.py
│       │   ├── audit_engine.py
│       │   └── title_analyzer.py
│       ├── analytics/
│       │   └── (outlier, competitor, content-gap engines)
│       ├── core/
│       │   ├── cache.py             # InMemoryTTLCache (concrete)
│       │   ├── cache_provider.py    # CacheProvider ABC               [NEW]
│       │   ├── config.py            # Settings (pydantic)
│       │   ├── rate_limit.py
│       │   └── security.py
│       ├── db/                      [NEW]
│       │   ├── base.py              # DatabaseProvider ABC
│       │   └── null_provider.py     # NullDatabaseProvider (MVP default)
│       ├── jobs/                    [NEW]
│       │   ├── base.py              # JobQueueProvider ABC
│       │   └── inprocess_queue.py   # asyncio-backed implementation
│       ├── api/
│       │   ├── router.py
│       │   └── routes/
│       │       ├── research.py
│       │       ├── audit.py
│       │       ├── competitor.py
│       │       ├── ai.py
│       │       ├── jobs.py          [NEW]
│       │       └── system.py        # /health, /ready
│       └── models/
│           ├── video.py
│           ├── channel.py
│           └── provenance.py        [NEW - provenance field standards]
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx             # Dashboard
│   │   │   ├── keywords/
│   │   │   ├── video-audit/
│   │   │   ├── channel-audit/
│   │   │   ├── competitors/
│   │   │   ├── outliers/
│   │   │   ├── content-gaps/
│   │   │   ├── topics/
│   │   │   ├── ai-studio/
│   │   │   ├── calendar/
│   │   │   ├── projects/            [NEW - IndexedDB backed]
│   │   │   ├── reports/
│   │   │   └── settings/
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── types.ts
│   │   │   ├── export.ts
│   │   │   └── storage/             [NEW]
│   │   │       ├── provider.ts      # StorageProvider interface
│   │   │       ├── browser.ts       # BrowserStorageProvider (IndexedDB)
│   │   │       ├── gdrive.ts        # GoogleDriveStorageProvider [Phase 7]
│   │   │       └── index.ts         # factory / active provider export
│   │   └── components/
├── nginx/
│   └── default.conf
├── docs/
│   ├── ARCHITECTURE.md              # this file
│   ├── ARCHITECTURE_GAP_ANALYSIS.md
│   ├── AI.md
│   ├── API.md
│   ├── AUDIT_REPORT.md
│   ├── CONTRIBUTING.md
│   ├── DEPLOYMENT.md
│   ├── RESEARCH_ENGINE.md
│   ├── SEO_SCORING.md
│   ├── SCALING.md                   [NEW]
│   └── DATA_PRIVACY.md              [NEW]
├── docker-compose.yml
├── .env.example
├── LICENSE
└── README.md
```

---

## 7. Health & Readiness Endpoints

| Endpoint | Purpose | Response |
|----------|---------|---------|
| `GET /health` | Liveness — is the process alive? | `{"status":"ok","version":"...","ai_enabled":bool}` |
| `GET /ready` | Readiness — is the app ready to serve traffic? | `{"ready":true,"providers":{"youtube":"ok","ai":"disabled","cache":"ok"}}` |

Coolify uses `/health` for liveness and `/ready` for readiness gating.

---

## 8. Environment Configuration Reference

All secrets and provider configurations must be supplied through environment variables.
See `.env.example` for the full reference. Key categories:

| Category | Key Variables |
|----------|--------------|
| **App** | `APP_ENV`, `DEBUG`, `SECRET_KEY`, `ALLOWED_ORIGINS` |
| **Ports** | `BACKEND_PORT`, `FRONTEND_PORT` |
| **AI** | `AI_ENABLED`, `AI_PROVIDER_CHAIN` |
| **OmniRoute** | `OMNIROUTE_BASE_URL`, `OMNIROUTE_API_KEY` |
| **FreeLLMAPI** | `FREELLM_BASE_URL`, `FREELLM_API_KEY` |
| **Ollama** | `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT` |
| **Gemini** | `GEMINI_API_KEY`, `GEMINI_MODEL` |
| **Groq** | `GROQ_API_KEY`, `GROQ_MODEL` |
| **YouTube** | `YOUTUBE_PROVIDER`, `YOUTUBE_API_KEY`, `MAX_SEARCH_RESULTS` |
| **Cache** | `CACHE_ENABLED`, `CACHE_TTL_SECONDS`, `REDIS_URL` (future) |
| **Jobs** | `MAX_CONCURRENT_JOBS`, `JOB_RESULT_TTL_SECONDS` |
| **Database** | `DATABASE_PROVIDER`, `DATABASE_URL` (future) |
| **Google Drive** | `GDRIVE_CLIENT_ID`, `GDRIVE_CLIENT_SECRET` (Phase 7) |

---

## 9. Security Model

- All API keys are **server-side only** — never exposed to browser JavaScript
- CORS is restricted to `ALLOWED_ORIGINS` in production (not `*`)
- Rate limiting: token-bucket per IP at the API middleware layer
- OmniRoute and FreeLLMAPI are internal gateways — no public unauthenticated access
- Health endpoints do not expose internal system details
- No secrets committed to git — enforced by `.gitignore` and `.env.example` pattern

---

## 10. Data Provenance Model

Every quantitative metric returned by the API must carry a `provenance` field:

```json
{
  "metric": "relative_demand",
  "value": 78,
  "source_type": "calculated",
  "method": "autocomplete_frequency_normalized",
  "confidence": "medium",
  "label": "Relative Demand"
}
```

| `source_type` | Meaning |
|--------------|---------|
| `official` | Directly from YouTube Data API v3 |
| `public` | Publicly observable on YouTube web surface |
| `calculated` | Derived deterministically from official/public signals |
| `estimated` | Heuristic approximation from observable indicators |
| `relative` | Comparative normalized scale |
| `unavailable` | Signal absent; excluded from formula |

The UI must visually distinguish these categories with clear labels.

---

## 11. Scaling Triggers

See `docs/SCALING.md` for full detail. Summary:

| Metric | Threshold | Action |
|--------|-----------|--------|
| API p95 latency | > 2s | Profile + optimize; add Redis cache |
| Memory usage | > 12 GB | Add second app instance |
| CPU sustained | > 80% | Upgrade VPS or add horizontal node |
| Cache hit ratio | < 60% | Increase `CACHE_TTL_SECONDS` |
| Queue depth | > 50 jobs | Add worker process / Redis queue |
| DB connections | > 80% pool | Add read replica or connection pooler |

---

## 12. Implementation Phases

| Phase | Focus | Status |
|-------|-------|--------|
| 0 | Repo audit, architecture, SEO scoring spec | ✅ Complete |
| 1 | Project skeleton, Docker, Next.js, FastAPI, Coolify | ✅ Complete |
| 2 | YouTube ResearchProvider, public data, caching, rate limiting | ✅ Complete |
| 3 | Deterministic SEO/keyword/competitor/outlier/content-gap engines | ✅ Complete |
| 4 | Browser IndexedDB StorageProvider, Projects, saved research | 🔲 Next |
| 5 | AIProvider chain: OmniRoute, FreeLLM, Gemini, Groq, Ollama fallback | 🔲 Next |
| 6 | EmbeddingProvider: TF-IDF default + remote providers | 🔲 Next |
| 7 | Google Drive OAuth + sync, YouTube Studio CSV import | 🔲 Planned |
| 8 | Async JobQueue, bulk research jobs, job status API | 🔲 Planned |
| 9 | Production hardening: security, observability, retries, circuit breakers | 🔲 Planned |
| 10 | Load testing, Coolify deployment test, failure testing, docs | 🔲 Planned |

---

## 13. Deviations from Requirements

| Requirement | Deviation | Reason |
|-------------|-----------|--------|
| REQ 12: yt-dlp provider | Deferred to post-MVP | Legal/compliance review needed; public scraper covers MVP use cases |
| REQ 14: Redis job queue | In-process queue for MVP | Redis adds operational complexity without benefit at MVP scale |
| REQ 5: PostgreSQL | NullDatabaseProvider for MVP | No auth/accounts implemented yet; will be introduced with user accounts |
