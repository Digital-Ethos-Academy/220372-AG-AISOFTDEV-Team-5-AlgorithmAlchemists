# Multi-stage Dockerfile for POI Compass
##### Stage 1: Frontend build #####
FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json frontend/.
RUN npm --prefix frontend install --omit=dev && npm --prefix frontend cache clean --force || true
COPY frontend frontend
RUN npm --prefix frontend run build

##### Stage 2: Backend #####
FROM python:3.11-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY app app
COPY scripts scripts

# Copy built frontend static assets into backend image
COPY --from=frontend-build /frontend/build ./frontend_build

# Optional: expose environment variables (documented in .env.example)
ENV PORT=8000

# Minimal health check script (optional future)
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
