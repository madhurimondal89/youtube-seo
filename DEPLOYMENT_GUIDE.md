# Production Deployment Guide
### YouTube SEO & Creator Intelligence Platform (`seo.freeyoutubetools.com`)

This guide covers complete deployment on Ubuntu 22.04 / 24.04 LTS (Hostinger KVM VPS) serving `seo.freeyoutubetools.com`.

---

## 1. Prerequisites
- Ubuntu VPS with Python 3.11+ and Node.js 20+
- Domain DNS access to add an `A` record for `seo.freeyoutubetools.com`
- Nginx and Certbot installed

---

## 2. Server Installation Commands

```bash
# 1. Clone repository
git clone https://github.com/madhurimondal89/youtube-seo.git
cd youtube-seo

# 2. Setup Python Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# 3. Setup Next.js Frontend
cd frontend
npm install
npm run build
cd ..

# 4. Configure Environment
cp .env.example .env
nano .env # configure desired settings
```

---

## 3. Process Management via PM2

```bash
npm install -g pm2

# Start Backend
pm2 start ".venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000" --name "yt-seo-backend"

# Start Frontend
cd frontend
pm2 start "npm start" --name "yt-seo-frontend"
cd ..

# Auto-start on system reboot
pm2 save
pm2 startup
```

---

## 4. Nginx Reverse Proxy Configuration

Create `/etc/nginx/sites-available/seo.freeyoutubetools.com`:

```nginx
server {
    listen 80;
    server_name seo.freeyoutubetools.com;

    client_max_body_size 15M;

    # API Routing
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

    # Frontend Routing
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

Enable and secure with free SSL:
```bash
sudo ln -s /etc/nginx/sites-available/seo.freeyoutubetools.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d seo.freeyoutubetools.com
```
