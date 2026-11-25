import time
import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.models.common import SystemStatus
from app.core.config import settings
from app.core.cache import cache
from app.ai.ollama_provider import LocalOllamaProvider

router = APIRouter(prefix="/system", tags=["System"])
START_TIME = time.time()

class SettingsUpdateRequest(BaseModel):
    ai_enabled: Optional[bool] = None
    ai_provider: Optional[str] = None
    ollama_base_url: Optional[str] = None
    ollama_model: Optional[str] = None
    custom_ai_base_url: Optional[str] = None
    custom_ai_model: Optional[str] = None
    custom_ai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    gemini_model: Optional[str] = None
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    groq_api_key: Optional[str] = None
    groq_model: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    deepseek_model: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    openrouter_model: Optional[str] = None
    localai_base_url: Optional[str] = None
    localai_model: Optional[str] = None
    lmstudio_base_url: Optional[str] = None
    lmstudio_model: Optional[str] = None
    database_url: Optional[str] = None
    youtube_provider: Optional[str] = None
    youtube_api_key: Optional[str] = None

@router.get("/status", response_model=SystemStatus)
async def get_system_status():
    from app.api.routes.ai import get_current_ai_provider
    ai_status = "Disabled"
    if settings.ai_enabled:
        prov = get_current_ai_provider()
        if await prov.is_available():
            ai_status = f"Active ({prov.get_provider_name()})"
        else:
            ai_status = f"Configured ({prov.get_provider_name()}) but Offline"

    return SystemStatus(
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        ai_enabled=settings.ai_enabled,
        ai_provider=settings.ai_provider,
        ai_status=ai_status,
        youtube_provider=settings.youtube_provider,
        cache_size=cache.size(),
        uptime_seconds=round(time.time() - START_TIME, 2),
    )

@router.get("/settings")
async def get_settings():
    def mask_key(k: Optional[str]) -> str:
        if not k:
            return ""
        if len(k) <= 6:
            return "***"
        return f"{k[:3]}...{k[-3:]}"

    return {
        "ai_enabled": settings.ai_enabled,
        "ai_provider": settings.ai_provider,
        "ollama_base_url": settings.ollama_base_url,
        "ollama_model": settings.ollama_model,
        "custom_ai_base_url": settings.custom_ai_base_url,
        "custom_ai_model": settings.custom_ai_model,
        "custom_ai_api_key_masked": mask_key(settings.custom_ai_api_key),
        "has_custom_ai_api_key": bool(settings.custom_ai_api_key),
        "gemini_model": settings.gemini_model,
        "gemini_api_key_masked": mask_key(settings.gemini_api_key),
        "has_gemini_api_key": bool(settings.gemini_api_key),
        "openai_model": settings.openai_model,
        "openai_api_key_masked": mask_key(settings.openai_api_key),
        "has_openai_api_key": bool(settings.openai_api_key),
        "groq_model": settings.groq_model,
        "groq_api_key_masked": mask_key(settings.groq_api_key),
        "has_groq_api_key": bool(settings.groq_api_key),
        "deepseek_model": settings.deepseek_model,
        "deepseek_api_key_masked": mask_key(settings.deepseek_api_key),
        "has_deepseek_api_key": bool(settings.deepseek_api_key),
        "openrouter_model": settings.openrouter_model,
        "openrouter_api_key_masked": mask_key(settings.openrouter_api_key),
        "has_openrouter_api_key": bool(settings.openrouter_api_key),
        "localai_base_url": settings.localai_base_url,
        "localai_model": settings.localai_model,
        "lmstudio_base_url": settings.lmstudio_base_url,
        "lmstudio_model": settings.lmstudio_model,
        "database_url": settings.database_url,
        "youtube_provider": settings.youtube_provider,
        "youtube_api_key_masked": mask_key(settings.youtube_api_key),
        "has_youtube_api_key": bool(settings.youtube_api_key),
    }

@router.post("/settings")
async def update_settings(req: SettingsUpdateRequest):
    if req.ai_enabled is not None:
        settings.ai_enabled = req.ai_enabled
    if req.ai_provider is not None:
        settings.ai_provider = req.ai_provider.lower().strip()
    if req.ollama_base_url is not None:
        settings.ollama_base_url = req.ollama_base_url.strip()
    if req.ollama_model is not None:
        settings.ollama_model = req.ollama_model.strip()
    if req.custom_ai_base_url is not None:
        settings.custom_ai_base_url = req.custom_ai_base_url.strip()
    if req.custom_ai_model is not None:
        settings.custom_ai_model = req.custom_ai_model.strip()
    if req.custom_ai_api_key is not None and req.custom_ai_api_key != "***":
        settings.custom_ai_api_key = req.custom_ai_api_key.strip() or None
    if req.gemini_api_key is not None and req.gemini_api_key != "***":
        settings.gemini_api_key = req.gemini_api_key.strip() or None
    if req.gemini_model is not None:
        settings.gemini_model = req.gemini_model.strip()
    if req.openai_api_key is not None and req.openai_api_key != "***":
        settings.openai_api_key = req.openai_api_key.strip() or None
    if req.openai_model is not None:
        settings.openai_model = req.openai_model.strip()
    if req.groq_api_key is not None and req.groq_api_key != "***":
        settings.groq_api_key = req.groq_api_key.strip() or None
    if req.groq_model is not None:
        settings.groq_model = req.groq_model.strip()
    if req.deepseek_api_key is not None and req.deepseek_api_key != "***":
        settings.deepseek_api_key = req.deepseek_api_key.strip() or None
    if req.deepseek_model is not None:
        settings.deepseek_model = req.deepseek_model.strip()
    if req.openrouter_api_key is not None and req.openrouter_api_key != "***":
        settings.openrouter_api_key = req.openrouter_api_key.strip() or None
    if req.openrouter_model is not None:
        settings.openrouter_model = req.openrouter_model.strip()
    if req.localai_base_url is not None:
        settings.localai_base_url = req.localai_base_url.strip()
    if req.localai_model is not None:
        settings.localai_model = req.localai_model.strip()
    if req.lmstudio_base_url is not None:
        settings.lmstudio_base_url = req.lmstudio_base_url.strip()
    if req.lmstudio_model is not None:
        settings.lmstudio_model = req.lmstudio_model.strip()
    if req.database_url is not None:
        settings.database_url = req.database_url.strip()
    if req.youtube_provider is not None:
        settings.youtube_provider = req.youtube_provider.lower().strip()
    if req.youtube_api_key is not None and req.youtube_api_key != "***":
        settings.youtube_api_key = req.youtube_api_key.strip() or None

    # Persist changes to .env file if it exists
    env_path = ".env"
    try:
        env_lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                env_lines = f.readlines()

        keys_to_update = {
            "AI_ENABLED": str(settings.ai_enabled).lower(),
            "AI_PROVIDER": settings.ai_provider,
            "OLLAMA_BASE_URL": settings.ollama_base_url,
            "OLLAMA_MODEL": settings.ollama_model,
            "CUSTOM_AI_BASE_URL": settings.custom_ai_base_url,
            "CUSTOM_AI_MODEL": settings.custom_ai_model,
            "CUSTOM_AI_API_KEY": settings.custom_ai_api_key or "",
            "GEMINI_API_KEY": settings.gemini_api_key or "",
            "GEMINI_MODEL": settings.gemini_model,
            "OPENAI_API_KEY": settings.openai_api_key or "",
            "OPENAI_MODEL": settings.openai_model,
            "GROQ_API_KEY": settings.groq_api_key or "",
            "GROQ_MODEL": settings.groq_model,
            "DEEPSEEK_API_KEY": settings.deepseek_api_key or "",
            "DEEPSEEK_MODEL": settings.deepseek_model,
            "OPENROUTER_API_KEY": settings.openrouter_api_key or "",
            "OPENROUTER_MODEL": settings.openrouter_model,
            "LOCALAI_BASE_URL": settings.localai_base_url,
            "LOCALAI_MODEL": settings.localai_model,
            "LMSTUDIO_BASE_URL": settings.lmstudio_base_url,
            "LMSTUDIO_MODEL": settings.lmstudio_model,
            "DATABASE_URL": settings.database_url,
            "YOUTUBE_PROVIDER": settings.youtube_provider,
            "YOUTUBE_API_KEY": settings.youtube_api_key or "",
        }

        updated_keys = set()
        new_lines = []
        for line in env_lines:
            stripped = line.strip()
            if "=" in stripped and not stripped.startswith("#"):
                k = stripped.split("=")[0].strip()
                if k in keys_to_update:
                    new_lines.append(f"{k}={keys_to_update[k]}\n")
                    updated_keys.add(k)
                    continue
            new_lines.append(line)

        for k, v in keys_to_update.items():
            if k not in updated_keys:
                new_lines.append(f"{k}={v}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except Exception:
        pass

    return {"status": "success", "message": "Settings updated and saved to runtime and .env."}

@router.post("/test-ai")
async def test_ai_connection():
    from app.ai.registry import provider_registry
    if not settings.ai_enabled:
        return {
            "success": False,
            "provider": "Disabled",
            "message": "AI is currently disabled. Toggle 'Enable AI Layer' to test."
        }
    return await provider_registry.test_connection(provider_type=settings.ai_provider)

@router.post("/cache/clear")
async def clear_cache():
    cache.clear()
    return {"status": "success", "message": "In-memory cache cleared."}
