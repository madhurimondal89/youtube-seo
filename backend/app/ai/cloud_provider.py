import httpx
from typing import Optional
from app.ai.base import AIProvider
from app.core.config import settings

class CustomOpenAICompatibleProvider(AIProvider):
    """
    Universal adapter for ANY OpenAI-compatible endpoint:
    Local: LM Studio, LocalAI, vLLM, Ollama (/v1), TextGenWebUI.
    Cloud: Groq, DeepSeek, OpenRouter, Mistral, Together, Perplexity, etc.
    """
    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None, timeout: float = 45.0):
        clean_url = base_url.strip().rstrip("/")
        if clean_url.endswith("/chat/completions"):
            self.endpoint = clean_url
        elif clean_url.endswith("/v1"):
            self.endpoint = f"{clean_url}/chat/completions"
        else:
            self.endpoint = f"{clean_url}/v1/chat/completions" if "/v1" not in clean_url else f"{clean_url}/chat/completions"
        self.base_url = clean_url
        self.model = model.strip() if model else "default"
        self.api_key = api_key.strip() if api_key else None
        self.timeout = timeout

    async def is_available(self) -> bool:
        if not settings.ai_enabled:
            return False
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(self.base_url, headers=headers)
                return resp.status_code in [200, 404, 401, 403, 405]
        except Exception:
            return False

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 500) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(self.endpoint, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices and "message" in choices[0]:
                        return choices[0]["message"].get("content", "").strip()
                    elif choices and "text" in choices[0]:
                        return choices[0].get("text", "").strip()
                    return str(data)
                return f"AI Provider Error: HTTP {resp.status_code} - {resp.text[:150]}"
        except Exception as e:
            return f"Custom AI Connection Error: {str(e)}"

    def get_provider_name(self) -> str:
        return f"Custom ({self.model} @ {self.base_url})"


class GoogleGeminiProvider(AIProvider):
    """Direct adapter for Google Gemini API."""
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", timeout: float = 30.0):
        self.api_key = api_key.strip() if api_key else ""
        self.model = model.strip() if model else "gemini-1.5-flash"
        self.timeout = timeout

    async def is_available(self) -> bool:
        return bool(self.api_key and settings.ai_enabled)

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 500) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.7
            }
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "").strip()
                    return "No output from Gemini."
                return f"Gemini Error: HTTP {resp.status_code} - {resp.text[:150]}"
        except Exception as e:
            return f"Gemini Connection Error: {str(e)}"

    def get_provider_name(self) -> str:
        return f"Google Gemini ({self.model})"


class OptionalOpenAIProvider(AIProvider):
    """
    Optional cloud adapter if user desires to supply their own OpenAI key.
    Never mandatory.
    """
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    async def is_available(self) -> bool:
        return bool(self.api_key and settings.ai_enabled)

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 500) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
                return f"OpenAI Error: {resp.status_code}"
        except Exception as e:
            return f"OpenAI error: {str(e)}"

    def get_provider_name(self) -> str:
        return f"OpenAI ({self.model})"

class DisabledAIProvider(AIProvider):
    """Default fallback when AI is disabled or offline."""
    async def is_available(self) -> bool:
        return False

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 500) -> str:
        return "AI layer is currently disabled. Core research and deterministic SEO engines remain fully operational."

    def get_provider_name(self) -> str:
        return "AI Inactive (Deterministic Mode)"
