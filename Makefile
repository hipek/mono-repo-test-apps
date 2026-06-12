.PHONY: start stop build ci ci-backend ci-frontend

start:
	docker compose up --build

stop:
	docker compose down

build:
	docker compose build

ci: ci-backend ci-frontend

ci-backend:
	@echo "=== Backend: format ==="
	@cd backend && .venv/bin/ruff format --check .
	@echo "=== Backend: lint ==="
	@cd backend && .venv/bin/ruff check .
	@echo "=== Backend: typecheck ==="
	@cd backend && .venv/bin/mypy .
	@echo "=== Backend: tests ==="
	@cd backend && .venv/bin/pytest tests/ -q

ci-frontend:
	@echo "=== Frontend: format ==="
	@cd frontend && ./node_modules/.bin/prettier --check "**/*.{ts,tsx,js,json,css}"
	@echo "=== Frontend: lint ==="
	@cd frontend && ./node_modules/.bin/eslint .
	@echo "=== Frontend: typecheck ==="
	@cd frontend && ./node_modules/.bin/tsc --noEmit
	@echo "=== Frontend: tests ==="
	@cd frontend && ./node_modules/.bin/jest --verbose
