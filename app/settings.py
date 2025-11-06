"""Lightweight settings loader (avoids pydantic-settings dependency)."""
from __future__ import annotations

import os


def _flag(name: str, default: str) -> bool:
    return os.getenv(name, default) == "1"


class Settings:
    # dynamic properties so tests (monkeypatch env) reflect instantly
    @property
    def poi_tracing(self) -> bool:
        return _flag("POI_TRACING", "0")

    @property
    def poi_observability(self) -> bool:
        return _flag("POI_OBSERVABILITY", "1")

    @property
    def rec_disable(self) -> bool:
        return _flag("REC_DISABLE", "0")

    @property
    def quiz_disable(self) -> bool:
        return _flag("QUIZ_DISABLE", "0")

    @property
    def internal_metrics_enabled(self) -> bool:
        return _flag("POI_INTERNAL_METRICS_ENABLED", "1")


settings = Settings()