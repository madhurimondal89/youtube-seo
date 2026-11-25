# API Provider Setup & Integration Guide
### YouTube SEO & Creator Intelligence Platform (`seo.freeyoutubetools.com`)

The platform features a multi-provider AI adapter and official YouTube Data API integration. All providers are **100% optional**; the platform functions deterministically with zero paid API keys.

---

## 1. Supported AI Providers

### A. Google Gemini API (Recommended for Free Cloud Tier)
- **Official Portal:** [Google AI Studio](https://aistudio.google.com/)
- **Recommended Model:** `gemini-1.5-flash`
- **Setup:**
  ```ini
  AI_ENABLED=True
  AI_PROVIDER=gemini
  GEMINI_API_KEY=your_gemini_api_key_here
  GEMINI_MODEL=gemini-1.5-flash
  ```

### B. Groq Fast Inference (Recommended for Ultra-Fast Inference)
- **Official Portal:** [Groq Console](https://console.groq.com/)
- **Recommended Model:** `llama-3.3-70b-versatile`
- **Setup:**
  ```ini
  AI_ENABLED=True
  AI_PROVIDER=custom
  CUSTOM_AI_BASE_URL=https://api.groq.com/openai/v1
  CUSTOM_AI_MODEL=llama-3.3-70b-versatile
  CUSTOM_AI_API_KEY=gsk_your_groq_api_key
  ```

### C. DeepSeek AI
- **Official Portal:** [DeepSeek Platform](https://platform.deepseek.com/)
- **Recommended Model:** `deepseek-chat`
- **Setup:**
  ```ini
  AI_ENABLED=True
  AI_PROVIDER=custom
  CUSTOM_AI_BASE_URL=https://api.deepseek.com/v1
  CUSTOM_AI_MODEL=deepseek-chat
  CUSTOM_AI_API_KEY=your_deepseek_api_key
  ```

### D. OpenRouter (Access to Claude, Llama, Mistral & Qwen)
- **Official Portal:** [OpenRouter](https://openrouter.ai/)
- **Setup:**
  ```ini
  AI_ENABLED=True
  AI_PROVIDER=custom
  CUSTOM_AI_BASE_URL=https://openrouter.ai/api/v1
  CUSTOM_AI_MODEL=meta-llama/llama-3.3-70b-instruct
  CUSTOM_AI_API_KEY=sk-or-v1-your_openrouter_key
  ```

### E. Local Ollama (Zero Cost, 100% Offline, CPU Capable)
- **Website:** [Ollama.com](https://ollama.com/)
- **Pull Model:** `ollama pull qwen2.5:3b`
- **Setup:**
  ```ini
  AI_ENABLED=True
  AI_PROVIDER=ollama
  OLLAMA_BASE_URL=http://127.0.0.1:11434
  OLLAMA_MODEL=qwen2.5:3b
  ```

### F. Local LM Studio (Local Desktop GUI)
- **Website:** [LM Studio](https://lmstudio.ai/)
- **Setup:** Start Local Server in LM Studio (port 1234), then:
  ```ini
  AI_ENABLED=True
  AI_PROVIDER=custom
  CUSTOM_AI_BASE_URL=http://localhost:1234/v1
  CUSTOM_AI_MODEL=local-model
  ```

---

## 2. YouTube Official APIs

### A. YouTube Data API v3
- **Google Cloud Console:** [console.cloud.google.com](https://console.cloud.google.com/)
- **Enable API:** Enable **YouTube Data API v3**.
- **Credentials:** Create an API Key.
- **Setup:**
  ```ini
  YOUTUBE_PROVIDER=api
  YOUTUBE_API_KEY=AIzaSy...
  ```
- **Fallback Note:** If no API key is provided, the platform automatically uses the public RSS and HTML scraper without crashing.

### B. YouTube Analytics API (Authorized Channels)
- **Scopes Required:** `https://www.googleapis.com/auth/yt-analytics.readonly`
- **Setup:** Configurable via Google OAuth 2.0 client ID and client secret.

---

## 3. Security Guarantee
- All API keys are loaded strictly server-side through Pydantic `BaseSettings`.
- In the frontend Settings page (`/settings`), API keys are masked (`••••••••`) and never echoed back in full.
- No client-side JavaScript bundle ever contains your API keys.
