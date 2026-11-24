# TubePilot AI — REST API Documentation

The TubePilot AI backend is powered by FastAPI and exposes structured endpoints for creator intelligence, deterministic SEO scoring, public YouTube data analysis, and modular AI assistance.

Base URL: `http://localhost:8000/api`

---

## 1. System & Health

### `GET /health`
Returns basic health check status.
- **Response**:
```json
{
  "status": "ok",
  "service": "TubePilot AI",
  "version": "1.0.0",
  "ai_enabled": false,
  "youtube_provider": "public"
}
```

### `GET /api/system/status`
Returns complete telemetry including uptime, cache item count, provider mode, and AI engine status.

---

## 2. Keyword Research

### `POST /api/research/keyword`
Executes multi-vector keyword expansion (root autocomplete, intent modifiers, and alphabet tree), computes Relative Demand, Estimated Competition, and 0-100 Opportunity scores, and groups keywords into Topic Clusters.

- **Request Body**:
```json
{
  "seed": "youtube automation",
  "include_alphabet_expansion": true,
  "include_modifiers": true,
  "max_keywords": 35
}
```

- **Response Body**:
```json
{
  "seed": "youtube automation",
  "total_found": 35,
  "keywords": [
    {
      "keyword": "youtube automation for beginners",
      "intents": ["Tutorial"],
      "search_surface": "YouTube Autocomplete",
      "relative_demand": 82,
      "estimated_competition": 38,
      "opportunity_score": 86,
      "freshness_score": 75,
      "specificity_score": 80,
      "word_count": 4,
      "char_count": 32,
      "provenance": "Calculated",
      "score_breakdown": {
        "demand_signal": 82.0,
        "competition_opportunity": 62.0,
        "small_creator_success": 85.0
      },
      "reasons": [
        "Favorable creator landscape: moderate-sized channels ranking",
        "Clear actionable intent (high viewer satisfaction potential)"
      ]
    }
  ],
  "clusters": [
    {
      "cluster_name": "Automation Mastery",
      "main_keyword": "youtube automation for beginners",
      "supporting_keywords": ["youtube automation tools", "youtube automation without code"],
      "recommended_pillar_title": "The Ultimate Guide to Automation (Complete Blueprint)",
      "supporting_video_ideas": ["5 Costly Mistakes When Doing Automation"],
      "playlist_suggestion": "Automation Step-by-Step Series",
      "avg_opportunity_score": 82
    }
  ],
  "data_provenance": "Calculated",
  "execution_time_ms": 420.5
}
```

---

## 3. SEO Audits

### `POST /api/audit/video`
Runs an 18-point deterministic audit across 7 categories (Title, Description, Keyword Relevance, Tags, Intent, Readability, Context) totaling exactly 100 points.

- **Request Body**:
```json
{
  "title": "How to Rank YouTube Videos Fast: Complete Step-by-Step Guide",
  "description": "Comprehensive tutorial covering keyword research, titles, and chapters...\n00:00 - Intro\n03:00 - Walkthrough",
  "tags": ["youtube seo", "how to rank youtube videos fast"],
  "target_keyword": "how to rank youtube videos fast"
}
```

- **Response Body**:
```json
{
  "title": "How to Rank YouTube Videos Fast: Complete Step-by-Step Guide",
  "overall_score": 88,
  "verdict": "Excellent",
  "categories": [
    {
      "category_name": "Title Optimization",
      "earned_score": 25.0,
      "max_score": 25.0,
      "percentage": 100,
      "items": [
        {
          "id": "title_length",
          "title": "Title Length (45-70 chars)",
          "passed": true,
          "score_earned": 8.0,
          "max_score": 8.0,
          "feedback": "Great title length (63 chars).",
          "severity": "optimal"
        }
      ]
    }
  ],
  "action_plan": ["Metadata is well optimized; focus on thumbnail contrast and viewer retention."],
  "provenance": "Calculated"
}
```

---

## 4. Competitor & Outliers

### `POST /api/competitor/compare`
Compares baseline median views, MAD (Median Absolute Deviation), and upload cadence between a user channel and competitor channels, detecting actionable content gaps.

### `GET /api/competitor/outliers?channel=@channel`
Computes statistical outliers performing 2.5x to 30x above the channel baseline views.

---

## 5. AI Studio

### `POST /api/ai/title`
Generates title variations with heuristic clickability metrics (SEO relevance, curiosity score, character length, and style). Works offline using deterministic heuristic templates when AI is disabled.

### `POST /api/ai/description`
Builds structured descriptions with hook, chapter placeholders, CTA, and relevant hashtags.

### `POST /api/ai/calendar`
Generates 7, 30, 60, or 90-day publishing roadmaps balancing evergreen, pillar, and trend topics.
