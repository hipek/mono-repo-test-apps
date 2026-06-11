#!/usr/bin/env bash
# Start both backend & frontend in dev mode
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "==> Starting backend (FastAPI)"
cd "$ROOT/backend"
uv run uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

echo "==> Starting frontend (Next.js)"
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

echo ""
echo "Backend  → http://localhost:8000"
echo "Frontend → http://localhost:3000"
echo ""

wait
