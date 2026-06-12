FROM python:3.14-slim

WORKDIR /code

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "PYTHONPATH=/app /code/.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000"]
