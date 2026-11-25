import asyncio
import httpx
from typing import Optional, Dict, Any, List
from app.ai.base import AIProvider
from app.core.config import settings
from app.ai.cloud_provider import (
    CustomOpenAICompatibleProvider,
    GoogleGeminiProvider,
    OptionalOpenAIProvider,
    DisabledAIProvider,
)
from app.ai.ollama_provider import LocalOllamaProvider

PROVIDER_PRESETS = {
    "gemini": {
        "name": "Google Gemini",
        "type": "native_gemini",
        "default_model": "gemini-1.5-flash",
        "default_url": "https://generativelanguage.googleapis.com/v1beta",
        "requires_key": True,
    },
    "openai": {
        "name": "OpenAI",
        "type": "openai_compatible",
        "default_model": "gpt-4o-mini",
        "default_url": "https://api.openai.com/v1",
        "requires_key": True,
    },
    "groq": {
        "name": "Groq Fast Inference",
        "type": "openai_compatible",
        "default_model": "llama-3.3-70b-versatile",
        "default_url": "https://api.groq.com/openai/v1",
        "requires_key": True,
    },
    "deepseek": {
        "name": "DeepSeek AI",
        "type": "openai_compatible",
        "default_model": "deepseek-chat",
        "default_url": "https://api.deepseek.com/v1",
        "requires_key": True,
    },
    "openrouter": {
        "name": "OpenRouter",
        "type": "openai_compatible",
        "default_model": "meta-llama/llama-3.3-70b-instruct",
        "default_url": "https://openrouter.ai/api/v1",
        "requires_key": True,
    },
    "ollama": {
        "name": "Local Ollama",
        "type": "ollama",
        "default_model": "qwen2.5:3b",
        "default_url": "http://127.0.0.1:11434",
        "requires_key": False,
    },
    "lmstudio": {
        "name": "Local LM Studio",
        "type": "openai_compatible",
        "default_model": "local-model",
        "default_url": "http://localhost:1234/v1",
        "requires_key": False,
    },
    "localai": {
        "name": "LocalAI",
        "type": "openai_compatible",
        "default_model": "gpt-4",
        "default_url": "http://localhost:8080/v1",
        "requires_key": False,
    },
    "custom": {
        "name": "Custom OpenAI-Compatible",
        "type": "openai_compatible",
        "default_model": "custom-model",
        "default_url": "http://localhost:1234/v1",
        "requires_key": False,
    },
}

class ResilientAIProvider(AIProvider):
    """
    Wraps an underlying AIProvider with:
    - Automatic exponential backoff retries (for transient 429/500/503/timeout)
    - Fallback provider cascade (falls back to deterministic if cloud fails)
    - Standardized error logging without leaking API keys
    """
    def __init__(self, primary: AIProvider, fallback: Optional[AIProvider] = None, max_retries: int = 2):
        self.primary = primary
        self.fallback = fallback or DisabledAIProvider()
        self.max_retries = max_retries

    async def is_available(self) -> bool:
        return await self.primary.is_available()

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 500) -> str:
        last_error = ""
        for attempt in range(self.max_retries + 1):
            try:
                res = await self.primary.generate_text(prompt, system_prompt=system_prompt, max_tokens=max_tokens)
                if not ("Error" in res or "Connection Error" in res):
                    return res
                last_error = res
            except Exception as e:
                last_error = str(e)
            
            # Wait before retry
            if attempt < self.max_retries:
                await asyncio.sleep(0.5 * (2 ** attempt))

        # Primary failed after retries -> trigger fallback
        if self.fallback and await self.fallback.is_available():
            try:
                return await self.fallback.generate_text(prompt, system_prompt=system_prompt, max_tokens=max_tokens)
            except Exception:
                pass

        return last_error or "AI generation failed after retries."

    def get_provider_name(self) -> str:
        return f"{self.primary.get_provider_name()} (with resilient fallback)"

class ProviderRegistry:
    """Central registry and factory for all AI and YouTube providers."""

    @staticmethod
    def get_provider(provider_type: Optional[str] = None) -> AIProvider:
        if not settings.ai_enabled:
            return DisabledAIProvider()

        ptype = (provider_type or settings.ai_provider).lower().strip()

        primary: AIProvider
        if ptype == "gemini":
            primary = GoogleGeminiProvider(
                api_key=settings.gemini_api_key or "",
                model=settings.gemini_model,
            )
        elif ptype == "openai":
            primary = OptionalOpenAIProvider(
                api_key=settings.openai_api_key or "",
                model=settings.openai_model,
            )
        elif ptype == "ollama":
            primary = LocalOllamaProvider(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
            )
        elif ptype == "groq":
            primary = CustomOpenAICompatibleProvider(
                base_url=PROVIDER_PRESETS["groq"]["default_url"],
                model=settings.groq_model or PROVIDER_PRESETS["groq"]["default_model"],
                api_key=settings.groq_api_key or settings.custom_ai_api_key or "",
            )
        elif ptype == "deepseek":
            primary = CustomOpenAICompatibleProvider(
                base_url=PROVIDER_PRESETS["deepseek"]["default_url"],
                model=settings.deepseek_model or PROVIDER_PRESETS["deepseek"]["default_model"],
                api_key=settings.deepseek_api_key or settings.custom_ai_api_key or "",
            )
        elif ptype == "openrouter":
            primary = CustomOpenAICompatibleProvider(
                base_url=PROVIDER_PRESETS["openrouter"]["default_url"],
                model=settings.openrouter_model or PROVIDER_PRESETS["openrouter"]["default_model"],
                api_key=settings.openrouter_api_key or settings.custom_ai_api_key or "",
            )
        elif ptype == "lmstudio":
            primary = CustomOpenAICompatibleProvider(
                base_url=settings.lmstudio_base_url or PROVIDER_PRESETS["lmstudio"]["default_url"],
                model=settings.lmstudio_model or PROVIDER_PRESETS["lmstudio"]["default_model"],
                api_key=settings.custom_ai_api_key or "",
            )
        elif ptype == "localai":
            primary = CustomOpenAICompatibleProvider(
                base_url=settings.localai_base_url or PROVIDER_PRESETS["localai"]["default_url"],
                model=settings.localai_model or PROVIDER_PRESETS["localai"]["default_model"],
                api_key=settings.custom_ai_api_key or "",
            )
        elif ptype == "custom":
            primary = CustomOpenAICompatibleProvider(
                base_url=settings.custom_ai_base_url,
                model=settings.custom_ai_model,
                api_key=settings.custom_ai_api_key,
            )
        else:
            primary = DisabledAIProvider()

        return ResilientAIProvider(primary=primary, fallback=DisabledAIProvider())

    @staticmethod
    async def test_connection(provider_type: str, base_url: Optional[str] = None, model: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Performs a live connectivity test with timeout trapping."""
        ptype = provider_type.lower().strip()
        
        test_prov: AIProvider
        if ptype == "gemini":
            test_prov = GoogleGeminiProvider(api_key=api_key or settings.gemini_api_key or "", model=model or settings.gemini_model)
        elif ptype == "openai":
            test_prov = OptionalOpenAIProvider(api_key=api_key or settings.openai_api_key or "", model=model or settings.openai_model)
        elif ptype == "ollama":
            test_prov = LocalOllamaProvider(base_url=base_url or settings.ollama_base_url, model=model or settings.ollama_model)
        elif ptype == "groq":
            target_url = base_url or PROVIDER_PRESETS["groq"]["default_url"]
            target_model = model or settings.groq_model or PROVIDER_PRESETS["groq"]["default_model"]
            target_key = api_key or settings.groq_api_key or settings.custom_ai_api_key
            test_prov = CustomOpenAICompatibleProvider(base_url=target_url, model=target_model, api_key=target_key)
        elif ptype == "deepseek":
            target_url = base_url or PROVIDER_PRESETS["deepseek"]["default_url"]
            target_model = model or settings.deepseek_model or PROVIDER_PRESETS["deepseek"]["default_model"]
            target_key = api_key or settings.deepseek_api_key or settings.custom_ai_api_key
            test_prov = CustomOpenAICompatibleProvider(base_url=target_url, model=target_model, api_key=target_key)
        elif ptype == "openrouter":
            target_url = base_url or PROVIDER_PRESETS["openrouter"]["default_url"]
            target_model = model or settings.openrouter_model or PROVIDER_PRESETS["openrouter"]["default_model"]
            target_key = api_key or settings.openrouter_api_key or settings.custom_ai_api_key
            test_prov = CustomOpenAICompatibleProvider(base_url=target_url, model=target_model, api_key=target_key)
        elif ptype == "lmstudio":
            target_url = base_url or settings.lmstudio_base_url or PROVIDER_PRESETS["lmstudio"]["default_url"]
            target_model = model or settings.lmstudio_model or PROVIDER_PRESETS["lmstudio"]["default_model"]
            target_key = api_key or settings.custom_ai_api_key
            test_prov = CustomOpenAICompatibleProvider(base_url=target_url, model=target_model, api_key=target_key)
        elif ptype == "localai":
            target_url = base_url or settings.localai_base_url or PROVIDER_PRESETS["localai"]["default_url"]
            target_model = model or settings.localai_model or PROVIDER_PRESETS["localai"]["default_model"]
            target_key = api_key or settings.custom_ai_api_key
            test_prov = CustomOpenAICompatibleProvider(base_url=target_url, model=target_model, api_key=target_key)
        else:
            target_url = base_url or settings.custom_ai_base_url
            target_model = model or settings.custom_ai_model
            target_key = api_key or settings.custom_ai_api_key
            test_prov = CustomOpenAICompatibleProvider(base_url=target_url, model=target_model, api_key=target_key)

        try:
            reply = await test_prov.generate_text(
                prompt="Say hello in 5 words or less.",
                system_prompt="You are YouTube SEO. Respond concisely.",
                max_tokens=25
            )
            if "Error" in reply or "connection error" in reply.lower():
                return {"success": False, "provider": test_prov.get_provider_name(), "message": reply}
            return {"success": True, "provider": test_prov.get_provider_name(), "response": reply}
        except Exception as e:
            return {"success": False, "provider": ptype, "message": f"Connection failed: {str(e)}"}

provider_registry = ProviderRegistry()
