# YouTube SEO 🚀
### Advanced AI-Powered YouTube SEO & Creator Intelligence Platform
**Designed for:** `seo.freeyoutubetools.com` | **GitHub:** `madhurimondal89/youtube-seo`

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2016-000000.svg)](https://nextjs.org/)
[![Design: Hallmark](https://img.shields.io/badge/Design-Hallmark%20Console-D97706.svg)](docs/HALLMARK.md)
[![Subdomain Ready](https://img.shields.io/badge/Subdomain-seo.freeyoutubetools.com-3B82F6.svg)](DEPLOYMENT_SUBDOMAIN.md)

**YouTube SEO** is an independent, production-grade creator research and search optimization platform designed to operate on `seo.freeyoutubetools.com`. It delivers transparent, verifiable intelligence for YouTube creators without mandatory paid APIs, without fabricated analytics, and with complete self-hosted control.

---

## 🌟 Core Modules

1. **AI Keyword Intelligence (`/keywords`)**
   - Multi-vector autocomplete expansion with root query, A-Z letter trees, question modifiers (How to, Why does, Can you), and comparison matrices (vs, alternative).
   - 0-100 Opportunity Scoring and Relative Demand Index based on actual SERP ranking evidence.

2. **Thumbnail Vision & Mobile Readability (`/thumbnail-analyzer`)**
   - Drag-and-drop image analysis evaluating 16:9 framing, resolution standard (1280x720 HD), luminance, and RMS contrast.
   - Live SERP simulation preview comparing desktop feed vs mobile feed truncation.
   - Permanent overlay safety zone checks (protecting the bottom-right timestamp zone).

3. **AI Creator Growth Coach (`/growth-coach`)**
   - 30-Day tailored content roadmap for high-growth niches (e.g. *Bengali Mystery and History*, *Faceless AI Channels*, *Tech Tutorials*).
   - 4-week structured milestones: Foundation Pillars -> Curiosity Retention -> Browse Algorithms -> Authority Anchor.
   - Video retention hook scripts (first 10 seconds), thumbnail concept briefs, and step-by-step narrative structures.

4. **18-Point Video & Channel SEO Audit (`/video-audit` & `/channel-audit`)**
   - Deterministic mathematical audits checking title length, keyword placement, 500-char tag bounds, closed captions (CC), timestamp chapter markers, and description link formatting.

5. **Competitor & Outlier Multipliers (`/competitors` & `/outliers`)**
   - Median Absolute Deviation (MAD) outlier detection discovering breakout videos (2.5x to 30x channel median).
   - Content gap matrix detecting unmet keyword demand in competitor SERP results.

6. **Universal AI Model Adapter (`/settings`)**
   - Connect any AI model: Local small models via Ollama (Qwen, Llama), LM Studio, LocalAI, or cloud providers (Google Gemini, OpenAI, Groq, DeepSeek, OpenRouter) with 1-click connection health tests.
   - Deterministic offline fallback mode: Calculates all scores with 0% AI and 0 GPU/RAM requirements.

---

## 📐 Architecture

```
                          [ User Browser ]
                                 │
                                 ▼
                     [ Nginx Reverse Proxy ]
                     (seo.freeyoutubetools.com)
                      ├── /       ──► [ Next.js 16 Frontend ] (Port 3000)
                      └── /api/   ──► [ FastAPI Backend ] (Port 8000)
                                              │
        ┌─────────────────────────────────────┼──────────────────────────────────┐
        ▼                                     ▼                                  ▼
[ YouTube Data Layer ]               [ SEO & Stat Engine ]             [ Multi-AI Adapter ]
├── Public Suggest Matrix            ├── Multi-Vector Expansion        ├── Local Ollama / LM Studio
├── Public RSS & SERP Parser         ├── 9-Category Intent Classifier  ├── Optional Gemini / OpenAI / Groq
├── Optional Official API v3         ├── Estimated Competition (0-100) └── Deterministic Math Fallback
└── Offline Mock Provider            ├── 10-Signal Opportunity Scorer       (100% Offline Capable)
                                     ├── Thumbnail Vision & Contrast
                                     └── 30-Day Creator Growth Coach
```

---

## 🚀 Local Development Setup

### 1. Backend (FastAPI - Python 3.14+)
```bash
# In project root
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On Linux/macOS: source .venv/bin/activate
pip install -r backend/requirements.txt

# Run server
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend (Next.js 16 - Node 20+)
```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:3000
```

---

## 🌐 Production Subdomain Deployment (`seo.freeyoutubetools.com`)

The platform is engineered to deploy cleanly on `seo.freeyoutubetools.com` without touching the main website `freeyoutubetools.com`:
- **Coolify + Traefik (Hostinger KVM 4 VPS):** Deploy using [`docker-compose.coolify.yml`](docker-compose.coolify.yml) for zero host port collisions and private internal API routing.
- **Bare-Metal Ubuntu (PM2 & Nginx):** Consult [`DEPLOYMENT_SUBDOMAIN.md`](DEPLOYMENT_SUBDOMAIN.md) and [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for automated process management and Nginx reverse proxy configs.
- **Data Compliance Audit:** Read [`docs/YOUTUBE_DATA_COMPLIANCE.md`](docs/YOUTUBE_DATA_COMPLIANCE.md) for data source provenance and zero-CAPTCHA policies.
- **Formulas & Heuristics:** Read [`docs/DATA_ACCURACY_FORMULAS.md`](docs/DATA_ACCURACY_FORMULAS.md) for mathematical definitions of all scoring algorithms.

---

## 📜 License
MIT License. Free for personal, commercial, and agency use.
