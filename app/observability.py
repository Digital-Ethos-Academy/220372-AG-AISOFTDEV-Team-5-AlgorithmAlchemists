"""Observability setup: structured logging and optional OpenTelemetry tracing."""
from __future__ import annotations

import logging
import os
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
except ImportError:  # Optional dependency
    trace = None  # type: ignore


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )


def setup_tracing() -> None:
    if not trace or not os.getenv("POI_TRACING"):
        return
    provider = TracerProvider(resource=Resource.create({"service.name": "poi-compass"}))
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:  # type: ignore[override]
        start = time.time()
        trace_id = str(uuid.uuid4())
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)
        response.headers["X-Trace-Id"] = trace_id
        logging.info({
            "trace_id": trace_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": duration_ms,
        })
        return response


def init_observability(app) -> None:
    setup_logging()
    setup_tracing()
    app.add_middleware(LoggingMiddleware)
