# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off

WORKDIR /workspace

# System deps (gcc only if needed by certain packages; keep lean)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifests first for layer caching
COPY requirements.txt* ./
COPY pyproject.toml* ./
COPY setup.cfg ./

# Install project deps if manifests present; always install mutmut + pytest
RUN --mount=type=cache,target=/root/.cache/pip bash -c "\
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi; \
    if [ -f pyproject.toml ]; then pip install . || true; fi; \
    pip install mutmut pytest coverage; \
    pip check || true"

# Copy source (kept minimal; mutation occurs in ephemeral container)
COPY app ./app
COPY tests ./tests

# Entrypoint script
COPY mutation/docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh
RUN chmod +x /usr/local/bin/docker_entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker_entrypoint.sh"]
