"""Observability setup: structured logging and optional OpenTelemetry tracing."""
from __future__ import annotations

import logging
import os
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.runtime_metrics import aggregator

try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
except ImportError:  # Optional dependency
    trace = None  # type: ignore


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )


def setup_tracing() -> None:
    """Configure OTEL tracing if enabled.

    Env:
      POIT_OTEL_ENABLE=1 to enable
      POIT_OTEL_EXPORTER_OTLP_ENDPOINT=https://collector:4318/v1/traces (optional)
    Fallback: if endpoint omitted, tracing disabled to avoid silent failures.
    """
    if not trace or os.getenv("POIT_OTEL_ENABLE") != "1":
        return
    endpoint = os.getenv("POIT_OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        logging.warning("OTEL enabled but no POIT_OTEL_EXPORTER_OTLP_ENDPOINT set; skipping tracer init")
        return
    provider = TracerProvider(resource=Resource.create({"service.name": "poi-compass"}))
    exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    logging.info({"event": "otel_tracing_enabled", "endpoint": endpoint})


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:  # type: ignore[override]
        start = time.time()
        trace_id = str(uuid.uuid4())
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)
        response.headers["X-Trace-Id"] = trace_id
        aggregator.record(request.url.path, duration_ms)
        # Attempt to surface confidence from response model if present
        confidence = None
        try:
            if hasattr(response, 'body') and response.body:
                import json as _json
                parsed = _json.loads(response.body.decode())
                confidence = parsed.get('confidence')
        except Exception:  # pragma: no cover
            confidence = None
        logging.info({
            "trace_id": trace_id,
            "method": request.method,
            "endpoint": request.url.path,
            "status": response.status_code,
            "success": response.status_code < 400,
            "duration_ms": duration_ms,
            "confidence": confidence,
            "user_id": None,  # placeholder until user concept added
        })
        return response


def init_observability(app) -> None:
    setup_logging()
    setup_tracing()
    app.add_middleware(LoggingMiddleware)
