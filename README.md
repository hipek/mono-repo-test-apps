# mono-repo-test-apps

Monorepo with FastAPI backend + Next.js frontend.

## Structure

```
backend/     – FastAPI HTTP API (port 8000)
  main.py    – app factory, CORS, lifespan seed
  routes/    – auth (login/register) + user routes
  services/  – business logic (token, user)
  repositories/ – DB access
  database.py – SQLite init / connection
frontend/    – Next.js React app (port 3000)
  pages/index.tsx – login page
e2e_tests/   – Playwright E2E tests (auth + API)
```

## Quick start

```bash
make start
```

Uses pnpm for frontend package management.

Open http://localhost:3000

```bash
make stop
```

## CI

```bash
make ci
```

Runs format, lint, typecheck, and tests for both backend and frontend.

## E2E tests

```bash
make e2e
```

Runs Playwright E2E tests against running containers. Requires `make start` first.

```bash
cd e2e_tests && npx playwright test --ui   # interactive UI mode
cd e2e_tests && npx playwright test --headed  # browser visible
```

## API endpoints

| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | `/api/register` | `{ username, password, full_name }` | Register new user |
| POST | `/api/token` | form-data (`username`, `password`) | Login — returns `{ access_token, token_type }` |
| GET | `/api/me` | — (JWT Bearer required) | Get current user — returns `{ username, full_name }` |

## Demo credentials

`admin` / `admin123` or `user` / `pass123`

## Dev notes

Next.js rewrites proxy `/api/*` to backend container during dev.

SQLite database stored in Docker volume `mono_repo_data`.
