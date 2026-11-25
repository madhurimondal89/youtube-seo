# =================================================================
# TubePilot AI — Unified Production Dockerfile (Coolify / Single Container)
# Serves Next.js 16 (Port 3000) & FastAPI Backend (Port 8000 internally)
# =================================================================

# -----------------------------------------------------------------
# Stage 1: Build Next.js 16 Frontend
# -----------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
RUN npm run build

# -----------------------------------------------------------------
# Stage 2: Production Unified Image (Python 3.11 + Node.js 20 Runtime)
# -----------------------------------------------------------------
FROM python:3.11-slim

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Backend dependencies & source
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY backend/ ./backend/
ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

# Frontend standalone assets
WORKDIR /app/frontend
COPY --from=frontend-builder /app/frontend/public ./public
COPY --from=frontend-builder /app/frontend/.next/standalone ./
COPY --from=frontend-builder /app/frontend/.next/static ./.next/static

# Persistent data directory for SQLite
RUN mkdir -p /app/backend/data

# Setup entrypoint
WORKDIR /app
COPY entrypoint.sh ./entrypoint.sh
RUN sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh

# Environment bindings
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV INTERNAL_BACKEND_URL="http://127.0.0.1:8000"
ENV DATABASE_URL="sqlite:///./backend/data/youtube_seo.db"
ENV APP_ENV="production"
ENV SECRET_KEY=""

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:3000/api/system/status || curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["./entrypoint.sh"]
