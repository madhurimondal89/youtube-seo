# Architectural & Repository Audit Report

**Date**: 2026-09-11  
**Project**: TubePilot AI  
**Scope**: Comprehensive analysis of 4 reference projects (Open-Tube-SEO, youtube-seo-skills, youtube-marketing-skills, Aurora) to inform clean-room independent implementation.

---

## 1. Open-Tube-SEO
- **Source Repository**: `BizMapper/Open-Tube-SEO`
- **License**: MIT
- **Primary Tech Stack**: JavaScript / TypeScript, Chrome Extension Manifest V3, WebGPU, WebLLM (`@mlc-ai/web-llm`).
- **Data Sources**: Chrome DOM injection on `youtube.com/watch` and `studio.youtube.com`, local Chrome storage.
- **AI Dependencies**: Browser-local LLM inference (e.g. Llama 3 8B or Phi-3 running in-browser via WebGPU).
- **Database Dependencies**: None (uses `chrome.storage.local`).
- **Useful Modules & Concepts**:
  - 18-point heuristic SEO checklist (title length, keyword position in title, description first 3 lines, tag counts, capitalization, punctuation).
  - Client-side keyword tag extraction.
  - Video tags inspection directly from page JSON/DOM.
- **Potential Conflicts & Risks**:
  - Chrome Extension Manifest V3 runtime limits.
  - WebGPU requires client device hardware support (modern GPU with WebGPU drivers); will fail on headless VPS or machines without WebGPU.
  - Fragile DOM scraping if YouTube changes internal CSS classes.
- **Independent Reimplementation Decision**:
  - Reimplement the 18-point audit checklist in pure Python for backend verification, and in TypeScript for instant client-side audit.
  - Provide server-side public HTML / JSON extraction that parses public initial data safely with regex/json rather than relying on browser extension DOM.
- **What Must NOT Be Reused**:
  - Do not reuse browser-extension-only DOM hooks for our standalone web application.
  - Do not make WebGPU/WebLLM mandatory.

---

## 2. youtube-seo-skills
- **Source Repository**: `deeployCO/youtube-seo-skills`
- **License**: MIT
- **Primary Tech Stack**: Markdown skill specifications, prompt templates, Claude Code / MCP integration.
- **Data Sources**: YouTube Data API v3 (when configured), user-supplied channel metadata.
- **AI Dependencies**: Anthropic Claude (agentic tool calls).
- **Database Dependencies**: None.
- **Useful Modules & Concepts**:
  - Strict 9-category search intent classification taxonomy:
    1. Informational ("what is...", "history of...")
    2. Tutorial / How-To ("how to...", "guide", "step by step")
    3. Commercial Investigation ("best...", "top 10...", "review")
    4. Transactional ("buy...", "discount", "course")
    5. Navigational ("channel name", "brand login")
    6. Entertainment / Storytelling ("vlog", "challenge", "story")
    7. News / Trending ("update", "announcement", "2026")
    8. Comparison ("X vs Y", "alternative to")
    9. Problem / Fix / Troubleshooting ("error", "not working", "fix")
  - Topic clustering: Pillar page -> Cluster nodes -> Supporting videos.
  - Channel authority and niche-fit heuristic rules.
- **Potential Conflicts & Risks**:
  - Built as Claude prompt instructions; lacks a deterministic scoring backend. If the LLM hallucinates numbers, the scores are untrustworthy.
- **Independent Reimplementation Decision**:
  - Translate the intent taxonomy into deterministic keyword rule engines (regex patterns + token dictionaries) with multi-label support.
  - Use deterministic graph clustering for keyword clustering.
- **What Must NOT Be Reused**:
  - Do not rely on Claude/LLM prompts to invent competition numbers or search volume.

---

## 3. youtube-marketing-skills
- **Source Repository**: `adityaarsharma/youtube-marketing-skills`
- **License**: MIT
- **Primary Tech Stack**: Python, MCP (Model Context Protocol) servers, CLI tools, Markdown templates.
- **Data Sources**: YouTube Data API v3, Google Analytics / YouTube Studio export files.
- **AI Dependencies**: Agent-agnostic LLMs (Cursor, Windsurf, Claude Code, Gemini CLI).
- **Database Dependencies**: None (stateless file generation).
- **Useful Modules & Concepts**:
  - Video hook anatomy: 3-second visual + 15-second contextual setup + open loop.
  - Structured content calendar matrices (7-day, 30-day, 60-day, 90-day) balancing evergreen, trend, and hero content.
  - Title psychology heuristics: Curiosity gap, numbers/lists, power words, readability score.
- **Potential Conflicts & Risks**:
  - Over-reliance on paid AI models for content generation.
  - High token cost if prompts are unoptimized.
- **Independent Reimplementation Decision**:
  - Build a deterministic title analyzer that scores titles against known clickability rules (length 40-70 chars, front-loaded keywords, emotional triggers, absence of repetitive words).
  - Create an AI Studio interface that uses local small models (Qwen 0.6B/4B) or heuristic templates when AI is disabled.
- **What Must NOT Be Reused**:
  - Do not require MCP servers or specific proprietary AI agent hosts.

---

## 4. Aurora
- **Concept Scope**: Evidence-first YouTube keyword research methodology.
- **License**: Clean-room conceptual reference.
- **Primary Tech Stack**: Autocomplete expansion trees, SERP harvesting, statistical aggregation.
- **Data Sources**: YouTube search suggestions, public SERP data.
- **AI Dependencies**: External paid LLMs in original designs.
- **Database Dependencies**: SQLite local persistence.
- **Useful Modules & Concepts**:
  - Recursive alphabet expansion: `[seed] + 'a'...'z'` and modifier prefixes (`how to [seed]`, `best [seed]`, `[seed] vs`).
  - Channel baseline calculation: Median views across recent 20-50 videos.
  - Outlier multiplier formula: $\text{Multiplier} = \frac{\text{Video Views}}{\text{Channel Median Views}}$.
  - Content gap discovery between target channel and competitor SERPs.
- **Potential Conflicts & Risks**:
  - Heavy database persistence and niche lock-in.
  - Aggressive recursive scraping can trigger IP rate-limits or temporary blocks if unthrottled.
- **Independent Reimplementation Decision**:
  - Completely decouple from SQLite. Use an in-memory job store with TTL caching and client-side JSON/CSV export.
  - Implement strict request pacing, jitter, token-bucket rate limiting, and graceful fallback.
  - Generalize to any niche or keyword topic.
- **What Must NOT Be Reused**:
  - Do not use SQLite database schemas as a mandatory runtime requirement.
  - Do not use unbounded recursive scraping.

---

## Summary Matrix

| Metric / Dimension | Open-Tube-SEO | youtube-seo-skills | youtube-marketing-skills | Aurora | TubePilot AI (Our Implementation) |
|---|---|---|---|---|---|
| **License** | MIT | MIT | MIT | Conceptual | **MIT** |
| **Backend** | None (Ext V3) | Claude MCP | Python MCP | Python CLI | **FastAPI (Python 3.11+)** |
| **Frontend** | Browser Popup | CLI / Chat | CLI / Chat | Web/Desktop | **Next.js (TS, Tailwind, SaaS UI)** |
| **Mandatory DB** | None | None | None | SQLite | **None (Stateless / In-Memory / TTL)** |
| **Mandatory Paid AI**| None (WebLLM) | Yes (Claude) | Yes (Agent) | Yes | **None (Works 100% with AI=false)** |
| **Local AI Target** | WebGPU (Client) | None | None | None | **Ollama CPU (Qwen 0.6B-4B) + Browser** |
| **Scoring Basis** | Heuristic (DOM)| LLM Prompt | LLM Prompt | Statistical | **Strict Mathematical & Statistical Heuristics** |
| **Deployment** | Browser Store | Dev CLI | Dev CLI | Local PC | **Docker Compose + Nginx (Hostinger KVM 4)** |
