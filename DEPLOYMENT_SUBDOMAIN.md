# Production Subdomain Deployment: seo.freeyoutubetools.com
### TubePilot AI — Advanced YouTube SEO & Creator Intelligence Platform

This document is the authoritative production deployment guide for running TubePilot AI on the **`seo.freeyoutubetools.com`** subdomain. The primary website `freeyoutubetools.com` remains completely untouched on its existing infrastructure.

---

## 1. Production Architecture Overview (Coolify + Traefik)

The recommended production architecture utilizes **Coolify** and **Traefik** on Ubuntu 22.04 / 24.04 LTS (e.g. Hostinger KVM 4 VPS):

```
                        [ User Web Browser ]
                                 │
                                 ▼
                    [ seo.freeyoutubetools.com ]
                                 │
                                 ▼
                     [ Traefik (Coolify Proxy) ]
                      Ports: 80 (HTTP) & 443 (HTTPS)
                      Managed Let's Encrypt SSL
                                 │
                         (Internal Network: 'coolify')
                                 │
                                 ▼
                    [ tubepilot_frontend (Next.js 16) ]
                    Port: 3000 (Internal Only)
                                 │
                         (Next.js Rewrite: /api/*)
                                 │
                                 ▼
                    [ tubepilot_backend (FastAPI) ]
                    Port: 8000 (Internal Only — Shielded from Public)
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
         [ SQLite Persistent DB ]    [ AI Engine (Optional) ]
         Volume: tubepilot_data      - Host Ollama (host.docker.internal)
                                     - Container Ollama (profile: local-ai)
                                     - Cloud (Gemini, Groq, DeepSeek, etc.)
                                     - Deterministic (Zero GPU/AI fallback)
```

### Key Security & Isolation Guarantees
- **No Host Port Conflicts:** Containers do **NOT** bind host ports 80, 443, or 8000. Traefik routes traffic dynamically using Docker labels over the external `coolify` network.
- **Backend Shielding:** Backend port 8000 is **never exposed to the public Internet**. All API calls pass through the internal Next.js rewrite proxy.
- **Fail-Fast Production Secrets:** If `APP_ENV=production` and `SECRET_KEY` is missing, weak (<32 characters), or contains a default placeholder, the backend safely terminates on startup.
- **Data Persistence:** SQLite database (`/app/data/youtube_seo.db`) is stored on a named Docker volume (`tubepilot_data`) preserving all saved keywords, watchlists, calendars, and preferences across rebuilds.

---

## 2. DNS Setup (Required)

In your DNS manager (Hostinger, Cloudflare, Namecheap, etc.) for `freeyoutubetools.com`:

| Type | Name / Host | Target / IP Address | TTL | Proxy Status |
|---|---|---|---|---|
| **A** | `seo` | `YOUR_HOSTINGER_VPS_IP` | 300 / Auto | DNS Only (or Proxied) |

---

## 3. Recommended Deployment: Coolify + Traefik

### Step 1: Generate Cryptographically Secure Secret
Before deploying, generate a strong 32-byte hexadecimal secret key on your local terminal or VPS:
```bash
openssl rand -hex 32
```
Copy this output for the `SECRET_KEY` environment variable.

### Step 2: Create Application in Coolify
1. In your Coolify dashboard, navigate to **Projects** -> **Add Resource** -> **Docker Compose**.
2. Connect your GitHub repository:
   - **Repository:** `https://github.com/madhurimondal89/youtube-seo.git`
   - **Branch:** `main`
3. In the Compose configuration:
   - **Compose File Path:** `docker-compose.coolify.yml`
   - **Domains for Frontend:** `https://seo.freeyoutubetools.com`

### Step 3: Configure Environment Variables in Coolify
Set the following environment variables in Coolify's Environment settings:

```ini
# Required Security Keys
APP_ENV=production
SECRET_KEY=paste_your_openssl_generated_hex_key_here

# Internal & External Network
NEXT_PUBLIC_API_URL=/api
INTERNAL_BACKEND_URL=http://backend:8000
DATABASE_URL=sqlite:///./data/youtube_seo.db

# YouTube Data (Default: public; key is 100% optional)
YOUTUBE_PROVIDER=public
YOUTUBE_API_KEY=

# Multi-AI Configuration (Optional — Set AI_ENABLED=false for deterministic mode)
AI_ENABLED=false
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=qwen2.5:3b

# Optional Cloud AI Keys
GEMINI_API_KEY=
GROQ_API_KEY=
DEEPSEEK_API_KEY=
OPENROUTER_API_KEY=
OPENAI_API_KEY=
```

### Step 4: Deploy & Verify
1. Click **Deploy**.
2. Coolify builds the Next.js standalone frontend and FastAPI backend containers.
3. Traefik automatically provisions a Let's Encrypt SSL certificate for `seo.freeyoutubetools.com`.
4. Verify by accessing `https://seo.freeyoutubetools.com/health` (should return HTTP 200 `{"status":"ok"}`).

---

## 4. Ollama Configuration in Docker

When running inside Docker, connecting to `http://127.0.0.1:11434` attempts to connect inside the backend container itself, where Ollama is not running. Choose one of the three verified setups:

1. **Ollama running directly on the VPS Host (Recommended):**
   - In `docker-compose.coolify.yml`, `extra_hosts` maps `host.docker.internal:host-gateway`.
   - Set `OLLAMA_BASE_URL=http://host.docker.internal:11434`.
   - Ensure Ollama on the host listens on `0.0.0.0:11434` (set `OLLAMA_HOST=0.0.0.0:11434` in host environment).
2. **Containerized Ollama Service:**
   - In Coolify or Docker Compose, enable the companion `ollama` service by passing the profile `--profile local-ai`.
   - Set `OLLAMA_BASE_URL=http://ollama:11434`.
3. **Remote Ollama Server:**
   - Set `OLLAMA_BASE_URL=http://your-gpu-server-ip:11434`.

---

## 5. Alternative Setup: Bare-Metal Ubuntu (Non-Docker / PM2)

If you are not using Coolify or Docker, you can deploy bare-metal on Ubuntu using PM2 and Nginx:

```bash
# 1. Clone repository
git clone https://github.com/madhurimondal89/youtube-seo.git
cd youtube-seo

# 2. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# 3. Setup Next.js Frontend
cd frontend
npm install
npm run build
cd ..

# 4. Generate production .env
cp .env.example .env
# Edit .env with your generated SECRET_KEY and settings

# 5. Start with PM2
npm install -g pm2
pm2 start ".venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000" --name "yt-seo-backend"
cd frontend
pm2 start "npm start" --name "yt-seo-frontend"
cd ..
pm2 save
pm2 startup
```

### Nginx Virtual Host for Bare-Metal (`/etc/nginx/sites-available/seo.freeyoutubetools.com`)
```nginx
server {
    listen 80;
    server_name seo.freeyoutubetools.com;

    client_max_body_size 15M;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/seo.freeyoutubetools.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d seo.freeyoutubetools.com
```

---

## 6. Verification & Health Checklist

- [x] Backend responds to `GET /health` with `{"status":"ok"}`.
- [x] Backend enforces `SECRET_KEY` validation (startup aborts if missing or weak in production).
- [x] Backend port 8000 is internal-only (not mapped to host).
- [x] Next.js rewrites proxy `/api/*` to `backend:8000` with 0 CORS errors.
- [x] Ollama connects cleanly via `http://host.docker.internal:11434` or container `http://ollama:11434`.
- [x] Main domain `freeyoutubetools.com` remains 100% untouched.
