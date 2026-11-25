# Database Architecture & Setup Guide
### YouTube SEO & Creator Intelligence Platform (`seo.freeyoutubetools.com`)

The platform supports a dual-tier persistence architecture designed for high performance, zero mandatory maintenance, and seamless enterprise scaling:

1. **Lightweight Local Tier (Default):** Embedded SQLite database (`backend/data/youtube_seo.db`). Requires zero extra servers, zero Docker containers, and takes < 1 MB storage.
2. **Enterprise Tier (Optional):** PostgreSQL with async connection pooling for multi-tenant and agency deployments.

---

## 1. Schema & Data Models

### A. `keyword_projects`
Stores multi-vector keyword research runs and topic clusters.
- `id` (VARCHAR / TEXT, PK): Unique project ID (e.g., `kw_a1b2c3d4e5f6`)
- `title` (TEXT): User-defined project title
- `seed` (TEXT): Root seed search term
- `total_keywords` (INT): Count of saved keyword metrics
- `data_json` (TEXT / JSONB): Full structured response payload
- `created_at` (TIMESTAMP ISO)
- `updated_at` (TIMESTAMP ISO)

### B. `competitor_watchlists`
Tracks competitor channels and benchmark performance.
- `id` (VARCHAR / TEXT, PK): Unique watchlist entry ID
- `channel_id` (TEXT): YouTube Channel ID (e.g. `UC...`)
- `channel_name` (TEXT): Channel title
- `median_views` (INT): Baseline median view hurdle
- `subscriber_count` (TEXT): Public subscriber count
- `notes` (TEXT): Custom creator/agency notes
- `created_at` (TIMESTAMP ISO)

### C. `saved_audits`
Stores 18-point video SEO audit checklists.
- `id` (VARCHAR / TEXT, PK): Audit report ID (e.g. `aud_...`)
- `video_title` (TEXT): Title of audited video
- `video_url` (TEXT): Video link
- `overall_score` (INT): 0-100 composite SEO score
- `audit_json` (TEXT / JSONB): Detailed 7-category diagnostic results
- `created_at` (TIMESTAMP ISO)

### D. `content_calendars`
Stores 30-day AI Growth Coach production schedules.
- `id` (VARCHAR / TEXT, PK): Calendar ID (e.g. `cal_...`)
- `niche` (TEXT): Target niche & focus
- `channel_name` (TEXT): Channel title
- `language` (TEXT): Production language (Bengali, English, Hindi, etc.)
- `strategy_json` (TEXT / JSONB): 4-week structured video plans, hooks & scripts
- `created_at` (TIMESTAMP ISO)

### E. `ai_history`
Audit log of all AI prompts and generation responses.
- `id` (VARCHAR / TEXT, PK)
- `feature` (TEXT): Feature used (`title`, `coach`, `description`, `hooks`)
- `prompt` (TEXT): Prompt submitted
- `response_text` (TEXT): Result returned
- `provider` (TEXT): Model and provider used
- `created_at` (TIMESTAMP ISO)

---

## 2. PostgreSQL Migration Setup (Optional for VPS)

To connect PostgreSQL instead of the default SQLite on your VPS:

### Step 1: Install PostgreSQL Driver
```bash
pip install psycopg2-binary
```

### Step 2: Configure Environment
In `backend/.env`:
```ini
DATABASE_URL=postgresql://user:password@localhost:5432/youtubeseo
```

### Step 3: Run Initialization
The database schema will automatically initialize upon backend startup.
