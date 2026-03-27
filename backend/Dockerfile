FROM python:3.14.3-slim-trixie

ENV PYTHONUNBUFFERED=1 \
PYTHONDONTWRITEBYTECODE=1 \
UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY  . .

EXPOSE 8000
