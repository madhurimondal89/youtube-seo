# Production Deployment Guide: seo.freeyoutubetools.com
## Advanced AI-Powered YouTube SEO & Creator Intelligence Platform

This document describes how to deploy and serve this application on the **`seo.freeyoutubetools.com`** subdomain alongside your main website `freeyoutubetools.com`.

---

### 1. Architecture Overview

```
                      [User Requests]
                             │
                             ▼
              [DNS: seo.freeyoutubetools.com]
                             │
                             ▼
          [Nginx Reverse Proxy on Hostinger VPS]
               │                         │
               │ (Proxy to /api/*)       │ (Proxy to /*)
               ▼                         ▼
      [FastAPI Backend]          [Next.js 16 Frontend]
       Port: 127.0.0.1:8000       Port: 127.0.0.1:3000
```

- **Main domain (`freeyoutubetools.com`):** Remains untouched on your primary web root / PHP / WordPress or existing server.
- **Subdomain (`seo.freeyoutubetools.com`):** Points to this full-stack Next.js + FastAPI platform.

---

### 2. DNS Configuration (DNS Records)

In your domain registrar / Cloudflare / DNS Manager for `freeyoutubetools.com`:

| Type | Name / Host | Value / Target IP | TTL |
|---|---|---|---|
| **A** | `seo` | `YOUR_SERVER_IP` | Auto / 300 |

*(If using Cloudflare, you can enable the orange proxy cloud for free DDoS protection & edge SSL).*

---

### 3. Production Environment Variables

#### Backend: `backend/.env`
```ini
APP_NAME="YouTube SEO"
APP_ENV=production
DEBUG=False
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
FRONTEND_PORT=3000

# YouTube Data Providers (Optional API Key - works without key via lawful public scraper/RSS)
YOUTUBE_PROVIDER=public
YOUTUBE_API_KEY=

# Multi-AI Engine Configuration (Optional - works deterministically with zero GPU/RAM if disabled)
AI_ENABLED=True
AI_PROVIDER=custom
CUSTOM_AI_BASE_URL=http://localhost:1234/v1
CUSTOM_AI_MODEL=qwen2.5-coder-7b-instruct
CUSTOM_AI_API_KEY=

# Cloud Fallbacks (Optional)
GEMINI_API_KEY=
OPENAI_API_KEY=
```

#### Frontend: `frontend/.env.production`
```ini
NEXT_PUBLIC_API_URL=https://seo.freeyoutubetools.com/api
```

---

### 4. Running with PM2 / Systemd

#### Option A: PM2 (Recommended for Bare-Metal Ubuntu)
```bash
# 1. Install PM2 globally
npm install -g pm2

# 2. Build Frontend
cd frontend
npm install
npm run build

# 3. Start Backend with PM2
cd ../backend
pm2 start "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000" --name "yt-seo-backend"

# 4. Start Frontend with PM2
cd ../frontend
pm2 start "npm start" --name "yt-seo-frontend"

# 5. Save PM2 processes to auto-restart on server reboot
pm2 save
pm2 startup
```

#### Option B: Coolify + Traefik (Hostinger KVM 4 VPS with Coolify)
If your Hostinger VPS is running Coolify with Traefik:
1. In Coolify Dashboard, click **Add Resource** -> **Docker Compose**.
2. Select your repository `https://github.com/madhurimondal89/youtube-seo.git` on branch `main`.
3. Set the Compose file path to: `docker-compose.coolify.yml`.
4. Ensure the domain is set to `seo.freeyoutubetools.com`.
5. Benefits of `docker-compose.coolify.yml`:
   - Connects seamlessly to Coolify's external `coolify` network.
   - Zero port conflicts with Traefik: host ports 80/443 and 8000 are **NOT** bound on the host.
   - Backend port 8000 is internal-only to Docker, fully isolated from public internet.
   - Next.js automatically rewrites `/api/*` to `http://backend:8000/api/*` internally.
   - Automatic SSL termination via Let's Encrypt managed by Traefik.

---

### 5. Nginx Virtual Host Configuration

Create `/etc/nginx/sites-available/seo.freeyoutubetools.com`:

```nginx
server {
    listen 80;
    server_name seo.freeyoutubetools.com;

    client_max_body_size 15M;

    # Backend API routing
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
    }

    # Next.js Frontend routing
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

Enable the site and obtain a free SSL certificate:
```bash
sudo ln -s /etc/nginx/sites-available/seo.freeyoutubetools.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d seo.freeyoutubetools.com
```

---

### 6. Verification Checklist
- [x] Backend responds to `curl http://127.0.0.1:8000/health`
- [x] Thumbnail analyzer handles up to 10MB images with 16:9 & contrast scores
- [x] AI Growth Coach generates 30-day custom niche strategies (English/Bengali/Hindi)
- [x] Frontend compiles with zero TypeScript errors
- [x] Zero external mandatory database setup required
