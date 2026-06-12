.PHONY: start stop build generate-types

start:
	docker compose up --build

stop:
	docker compose down

build:
	docker compose build

generate-types:
	docker compose exec backend /code/.venv/bin/python -c "import json,sys; from main import app; sys.stdout.write(json.dumps(app.openapi()))" > /tmp/openapi.json
	npx openapi-typescript /tmp/openapi.json -o frontend/types/api.ts --immutable
