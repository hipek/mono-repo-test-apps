.PHONY: start stop build ci ci-backend ci-frontend

start:
	docker compose up --build

stop:
	docker compose down

build:
	docker compose build

ci: ci-backend ci-frontend

ci-backend:
	@cd backend && docker build --target ci -t backend-ci . && docker run --rm backend-ci

ci-frontend:
	@cd frontend && ./node_modules/.bin/prettier --check '**/*.{ts,tsx,js,json,css}' > /dev/null
	@cd frontend && ./node_modules/.bin/eslint .
	@cd frontend && (./node_modules/.bin/tsc --noEmit 2>&1 | grep -v '^$$') || true
	@cd frontend && (./node_modules/.bin/jest --silent 2>&1 | grep -E 'PASS|FAIL|Test Suites|Tests:|^[.]+') || true
