import httpx
from typing import Optional
from app.ai.base import AIProvider
from app.core.config import settings

class LocalOllamaProvider(AIProvider):
    """
    Adapter for local, remote, or containerized Ollama server running quantized models
    such as Qwen 2.5 0.5B / 3B or Gemma 2 / Llama 3.
    """
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        raw_url = (base_url or settings.ollama_base_url).rstrip("/")
        if not raw_url.startswith("http://") and not raw_url.startswith("https://"):
            raw_url = f"http://{raw_url}"
        self.base_url = raw_url
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
                return f"Ollama Error (HTTP {resp.status_code}): Could not generate text with model '{self.model}'."
        except httpx.ConnectError:
            docker_hint = " (Hint: from inside Docker containers, use 'http://host.docker.internal:11434' instead of localhost/127.0.0.1)" if ("127.0.0.1" in self.base_url or "localhost" in self.base_url) else ""
            return f"Ollama Connection Error: Unable to connect to Ollama at {self.base_url}{docker_hint}."
        except httpx.TimeoutException:
            return f"Ollama Timeout: Model inference at {self.base_url} timed out after {self.timeout}s."
        except Exception as e:
            return f"Ollama Connection Error: {str(e)}"

    def get_provider_name(self) -> str:
        return f"Local Ollama ({self.model})"
