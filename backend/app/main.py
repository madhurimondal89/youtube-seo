from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.rate_limit import rate_limiter
from app.core.security import validate_secret_strength
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Enforce P0 Production Secret Protection
    import secrets
    is_valid, msg = validate_secret_strength(settings.secret_key)
    if not is_valid:
        # Generate cryptographically secure random 32-byte (64 hex characters) secret
        auto_key = secrets.token_hex(32)
        settings.secret_key = auto_key
        print(f"[SECURITY] Strong random SECRET_KEY generated automatically ({len(auto_key)} chars).")
    yield
    # Shutdown: cleanup

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Self-Hosted YouTube SEO & Research Intelligence Platform",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    # Only rate-limit API routes, not static or health
    if request.url.path.startswith("/api/"):
        if not rate_limiter.acquire(1.0):
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. YouTube SEO rate limit exceeded. Please wait a moment."}
            )
    response = await call_next(request)
    return response

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "ai_enabled": settings.ai_enabled,
        "youtube_provider": settings.youtube_provider,
    }

app.include_router(api_router)
