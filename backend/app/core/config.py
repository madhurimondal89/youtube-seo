from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "YouTube SEO"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "youtube-seo-insecure-secret-key-change-me"
    
    # Bindings
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_port: int = 3000
    
    # AI (Optional)
    ai_enabled: bool = False
    ai_provider: str = "ollama"  # "ollama", "openai", "gemini", "custom", "mock"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:3b"
    ollama_timeout: int = 60
    
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-1.5-flash"

    # Custom / Any OpenAI-Compatible Endpoint (LM Studio, LocalAI, Groq, DeepSeek, OpenRouter, vLLM, etc.)
    custom_ai_base_url: str = "http://localhost:1234/v1"
    custom_ai_model: str = "custom-model"
    custom_ai_api_key: Optional[str] = None
    
    # YouTube Data
    youtube_provider: str = "public"  # "public", "api", "mock"
    youtube_api_key: Optional[str] = None
    max_search_results: int = 25
    request_timeout_seconds: int = 15
    rate_limit_per_minute: int = 60
    
    # In-memory Cache & Jobs
    cache_enabled: bool = True
    cache_ttl_seconds: int = 900
    max_concurrent_jobs: int = 3

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

settings = Settings()

