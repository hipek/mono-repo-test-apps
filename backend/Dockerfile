FROM python:3.14-slim AS base

WORKDIR /code

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

FROM base AS ci

CMD ["sh", "-c", "uv run ruff format --check . && uv run ruff check . && uv run mypy . && uv run pytest tests/ -q"]

FROM base AS runtime

EXPOSE 8000

CMD ["sh", "-c", "PYTHONPATH=/app /code/.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000"]
