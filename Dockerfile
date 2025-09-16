# ===== BUILDER =====
FROM python:3.12-slim AS builder

ENV POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --only main

COPY . /app

# ===== FINAL =====
FROM python:3.12-slim AS final

WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /usr/local /usr/local

EXPOSE 8080
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]