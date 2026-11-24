import httpx
from typing import Optional
from app.ai.base import AIProvider
from app.core.config import settings

class LocalOllamaProvider(AIProvider):
    """
    Adapter for local Ollama server running quantized, CPU-friendly models
    such as Qwen 2.5 0.5B / 4B or Gemma 3 4B on Hostinger KVM 4.
    """
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self.model = model or settings.ollama_model
        self.timeout = settings.ollama_timeout

    async def is_available(self) -> bool:
        if not settings.ai_enabled:
            return False
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 500) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt or "You are TubePilot AI, an expert YouTube SEO strategist. Give concise, actionable advice.",
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7,
            }
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(f"{self.base_url}/api/generate", json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("response", "").strip()
                return f"Ollama Error: Status {resp.status_code}"
        except Exception as e:
            return f"Ollama connection error: {str(e)}"

    def get_provider_name(self) -> str:
        return f"Local Ollama ({self.model})"
