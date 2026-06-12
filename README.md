# mono-repo-question

Monorepo with FastAPI backend + Next.js frontend.

## Structure

```
backend/     – FastAPI HTTP API (port 8000)
frontend/    – Next.js React app (port 3000)
```

## Quick start

```bash
make start
```

Open http://localhost:3000

```bash
make stop
```

## API endpoint

`POST /api/login` – accepts `{ username, password }`, returns `{ success, token, message }`.

Demo credentials: `admin` / `admin123` or `user` / `pass123`.

## Rewrites

Next.js rewrites proxy `/api/*` to backend container during dev.
