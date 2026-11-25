#!/bin/bash
set -e

echo "[TubePilot] Starting FastAPI Backend on 127.0.0.1:8000..."
cd /app/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 &
BACKEND_PID=$!

echo "[TubePilot] Waiting for FastAPI Backend to initialize..."
for i in $(seq 1 30); do
  if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
    echo "[TubePilot] FastAPI Backend is healthy and ready!"
    break
  fi
  sleep 0.5
done

echo "[TubePilot] Starting Next.js Frontend on 0.0.0.0:3000..."
cd /app/frontend
node server.js &
FRONTEND_PID=$!

cleanup() {
  echo "[TubePilot] Stopping services..."
  kill -TERM "$BACKEND_PID" 2>/dev/null || true
  kill -TERM "$FRONTEND_PID" 2>/dev/null || true
  exit 0
}

trap cleanup SIGINT SIGTERM

while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$FRONTEND_PID" 2>/dev/null; do
  sleep 2
done

echo "[TubePilot] Process terminated unexpectedly. Cleaning up..."
cleanup
