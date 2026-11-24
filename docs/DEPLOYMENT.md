# TubePilot AI — Production VPS Deployment Guide

**Target Environment**: Hostinger KVM 4 VPS  
**Specifications**: 4 vCPU, 16 GB RAM, 200 GB NVMe Storage, No GPU  
**Operating System**: Ubuntu 24.04 LTS (or Debian 12)

---

## 1. Prerequisites on Clean VPS

Update system packages and install Docker with Compose plugin:

```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install essential utilities
sudo apt install -y curl git ufw fail2ban htop

# 3. Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# 5. Verify Docker Compose
docker compose version
```

---

## 2. Firewall Configuration (UFW)

Protect internal container ports and only expose standard web ports:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 3. Clone Repository and Configure Environment

```bash
cd /opt
git clone <your-repository-url> tubepilot
cd tubepilot

# Copy production environment file
cp .env.example .env
nano .env
```

Ensure production variables:
```ini
APP_ENV=production
DEBUG=false
AI_ENABLED=false           # Start with AI disabled for ultra-lightweight footprint (< 300MB RAM)
YOUTUBE_PROVIDER=public    # Or supply YOUTUBE_API_KEY if desired
CACHE_ENABLED=true
CACHE_TTL_SECONDS=900
```

---

## 4. Launching the Platform

### Option A: Standard Production (Lightweight, No AI, < 500 MB RAM)
```bash
docker compose up -d --build
```
This builds and launches:
- `tubepilot_backend` (FastAPI on Port 8000 internal)
- `tubepilot_frontend` (Next.js production build on Port 3000 internal)
- `tubepilot_nginx` (Reverse proxy on Port 80 external)

Verify status:
```bash
docker compose ps
curl http://localhost/health
```

### Option B: Enabling Local AI on KVM 4 (CPU Inference)
If you wish to enable the optional local AI model on your 16 GB RAM VPS:

1. Update `.env`:
```ini
AI_ENABLED=true
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=qwen2.5:0.5b
```

2. Start with the `ai` profile:
```bash
docker compose --profile ai up -d
```

3. Download the small, CPU-friendly quantized model inside the Ollama container:
```bash
docker exec -it tubepilot_ollama ollama run qwen2.5:0.5b
# Or for higher reasoning capacity within 16GB RAM:
# docker exec -it tubepilot_ollama ollama run qwen2.5:4b
```

---

## 5. SSL / TLS Setup with Let's Encrypt (Certbot)

If pointing your own domain name (e.g. `seo.yourdomain.com`):

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seo.yourdomain.com
```

---

## 6. Resource Monitoring on KVM 4

Inspect real-time RAM and CPU consumption:
```bash
docker stats
```
Expected idle memory usage:
- Backend: ~75 MB
- Frontend: ~90 MB
- Nginx: ~15 MB
- **Total without AI**: **< 200 MB RAM**! (Leaving 15.8 GB free on your KVM 4 server).
- **With Qwen 2.5 0.5B**: ~1.1 GB RAM.
