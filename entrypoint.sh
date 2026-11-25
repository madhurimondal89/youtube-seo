#!/bin/bash
set -e

# Dedicated private internal port for FastAPI (avoids any collision with public PORT=8000 or PORT=3000)
BACKEND_PORT=8001

# Determine frontend port: if Coolify sets PORT, use it; otherwise default to 3000
FRONTEND_PORT=${PORT:-3000}
if [ "$FRONTEND_PORT" = "$BACKEND_PORT" ]; then
  FRONTEND_PORT=3000
fi

export PORT=$FRONTEND_PORT
export HOSTNAME="0.0.0.0"
export INTERNAL_BACKEND_URL="http://127.0.0.1:${BACKEND_PORT}"

echo "[TubePilot] Starting FastAPI Backend on 127.0.0.1:${BACKEND_PORT}..."
cd /app/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port ${BACKEND_PORT} --workers 2 &
BACKEND_PID=$!

echo "[TubePilot] Waiting for FastAPI Backend to initialize on port ${BACKEND_PORT}..."
for i in $(seq 1 30); do
  if curl -s http://127.0.0.1:${BACKEND_PORT}/health > /dev/null 2>&1; then
    echo "[TubePilot] FastAPI Backend is healthy and ready!"
    break
  fi
  sleep 0.5
done

echo "[TubePilot] Starting Next.js Frontend on 0.0.0.0:${FRONTEND_PORT}..."
cd /app/frontend
PORT=${FRONTEND_PORT} node server.js &
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
