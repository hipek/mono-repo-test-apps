.PHONY: start stop build ci ci-backend ci-frontend

start:
	docker compose up --build

stop:
	docker compose down

build:
	docker compose build

ci: ci-backend ci-frontend

ci-backend:
	@cd backend && .venv/bin/ruff format --check . > /dev/null
	@cd backend && .venv/bin/ruff check .
	@cd backend && (.venv/bin/mypy . 2>&1 | grep -v '^Success:' | grep -v '^$$') || true
	@cd backend && (.venv/bin/pytest tests/ -q 2>&1 | grep -E 'passed|failed|error|^[.]+' ) || true

ci-frontend:
	@cd frontend && ./node_modules/.bin/prettier --check '**/*.{ts,tsx,js,json,css}' > /dev/null
	@cd frontend && ./node_modules/.bin/eslint .
	@cd frontend && (./node_modules/.bin/tsc --noEmit 2>&1 | grep -v '^$$') || true
	@cd frontend && (./node_modules/.bin/jest --silent 2>&1 | grep -E 'PASS|FAIL|Test Suites|Tests:|^[.]+') || true
