# API Provider Setup & Integration Guide
### YouTube SEO & Creator Intelligence Platform (`seo.freeyoutubetools.com`)

The platform features a resilient multi-provider AI adapter and official YouTube Data API integration. All providers are **100% optional**; the platform functions deterministically with zero paid API keys and zero GPU footprint when providers are disabled.

---

## 1. Supported AI Providers

### A. Google Gemini API (Recommended for Free Cloud Tier)
- **Official Portal:** [Google AI Studio](https://aistudio.google.com/)
- **Recommended Model:** `gemini-1.5-flash`
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=gemini
  GEMINI_API_KEY=your_gemini_api_key_here
  GEMINI_MODEL=gemini-1.5-flash
  ```

### B. Groq Fast Inference (Ultra-Fast Inference)
- **Official Portal:** [Groq Console](https://console.groq.com/)
- **Recommended Model:** `llama-3.3-70b-versatile`
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=groq
  GROQ_API_KEY=gsk_your_groq_api_key
  GROQ_MODEL=llama-3.3-70b-versatile
  ```

### C. DeepSeek AI
- **Official Portal:** [DeepSeek Platform](https://platform.deepseek.com/)
- **Recommended Model:** `deepseek-chat`
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=deepseek
  DEEPSEEK_API_KEY=your_deepseek_api_key
  DEEPSEEK_MODEL=deepseek-chat
  ```

### D. OpenRouter (Multi-Model Gateway: Claude, Llama, Mistral, Qwen)
- **Official Portal:** [OpenRouter](https://openrouter.ai/)
- **Recommended Model:** `meta-llama/llama-3.3-70b-instruct`
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=openrouter
  OPENROUTER_API_KEY=sk-or-v1-your_openrouter_key
  OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
  ```

### E. OpenAI (Cloud)
- **Official Portal:** [OpenAI Platform](https://platform.openai.com/)
- **Recommended Model:** `gpt-4o-mini`
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=openai
  OPENAI_API_KEY=sk-proj-your_openai_key
  OPENAI_MODEL=gpt-4o-mini
  ```

### F. Local Ollama (Zero Cost, 100% Offline, CPU/GPU)
- **Website:** [Ollama.com](https://ollama.com/)
- **Pull Model:** `ollama pull qwen2.5:3b`
- **Docker Connectivity Note:** When running inside Docker, never use `127.0.0.1` to refer to the host. Use `http://host.docker.internal:11434` (mapped automatically via `extra_hosts` in `docker-compose.coolify.yml`), or `http://ollama:11434` if running Ollama as a Docker service.
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=ollama
  # For Docker -> Host Ollama:
  OLLAMA_BASE_URL=http://host.docker.internal:11434
  # For Bare-Metal:
  # OLLAMA_BASE_URL=http://127.0.0.1:11434
  OLLAMA_MODEL=qwen2.5:3b
  ```

### G. Local LM Studio (Local Desktop GUI)
- **Website:** [LM Studio](https://lmstudio.ai/)
- **Setup:** Start Local Server in LM Studio (default port 1234), then:
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=lmstudio
  LMSTUDIO_BASE_URL=http://localhost:1234/v1
  LMSTUDIO_MODEL=local-model
  ```

### H. LocalAI (Self-Hosted OpenAI Alternative)
- **Website:** [LocalAI.io](https://localai.io/)
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=localai
  LOCALAI_BASE_URL=http://localhost:8080/v1
  LOCALAI_MODEL=gpt-4
  ```

### I. Custom OpenAI-Compatible Endpoints (vLLM, Text-Gen WebUI, Any Proxy)
- **Configuration:**
  ```ini
  AI_ENABLED=true
  AI_PROVIDER=custom
  CUSTOM_AI_BASE_URL=http://your-server:port/v1
  CUSTOM_AI_MODEL=your-model-name
  CUSTOM_AI_API_KEY=optional_key
  ```

---

## 2. Resilient AI Features
- **Exponential Backoff & Retries:** Transient 429 and 503 HTTP errors automatically retry with backoff.
- **Deterministic Fallback:** If cloud AI endpoints fail or are rate-limited, all SEO scoring and content roadmaps gracefully fall back to deterministic algorithms with zero user crashes.
- **One-Click Connection Testing:** The `/settings` page allows creators to test connectivity to any selected provider with live diagnostic feedback.

---

## 3. YouTube Official & Permitted Data Providers

### A. Public Research Engine (Default — Zero Key Required)
- Uses public suggestion endpoints (`suggestqueries.google.com`), official oEmbed (`youtube.com/oembed`), public HTML metadata tags, and channel Atom RSS feeds (`youtube.com/feeds/videos.xml`).
- Fully rate-paced with randomized jitter delays.
- Details in `docs/YOUTUBE_DATA_COMPLIANCE.md`.

### B. YouTube Data API v3 (Optional)
- **Google Cloud Console:** [console.cloud.google.com](https://console.cloud.google.com/)
- **Setup:**
  ```ini
  YOUTUBE_PROVIDER=api
  YOUTUBE_API_KEY=AIzaSy...
  ```
- Yields exact view counts, like counts, comment counts, and official tag lists.

---

## 4. Security & Privacy Guarantee
- All API keys are loaded strictly server-side through Pydantic `BaseSettings`.
- In the frontend Settings page (`/settings`), API keys are masked (`••••••••`) and never exposed to the client browser.
