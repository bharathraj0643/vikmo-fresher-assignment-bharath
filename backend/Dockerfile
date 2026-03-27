FROM python:3.14.3-slim-trixie

ENV PYTHONUNBUFFERED=1 \
PYTHONDONTWRITEBYTECODE=1 \
UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml .

RUN uv sync

COPY  src/ .

EXPOSE 8000

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
