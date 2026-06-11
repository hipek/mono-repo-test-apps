# mono-repo-question

Monorepo with FastAPI backend + Next.js frontend.

## Structure

```
backend/     – FastAPI HTTP API (port 8000)
frontend/    – Next.js React app (port 3000)
```

## Quick start

```bash
# Terminal 1 – backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 – frontend
cd frontend
npm run dev
```

Open http://localhost:3000

## API endpoint

`POST /api/login` – accepts `{ username, password }`, returns `{ success, token, message }`.

Demo credentials: `admin` / `admin123` or `user` / `pass123`.

## Rewrites

Next.js rewrites proxy `/api/*` to `localhost:8000` during dev, so no CORS hassle.
