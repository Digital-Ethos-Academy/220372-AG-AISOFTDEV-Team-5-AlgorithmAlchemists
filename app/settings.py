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

    # --- Provider Availability (never return secret values) ---
    @property
    def openai_enabled(self) -> bool:  # presence only
        return bool(os.getenv("OPENAI_API_KEY"))

    @property
    def anthropic_enabled(self) -> bool:
        return bool(os.getenv("ANTHROPIC_API_KEY"))

    @property
    def huggingface_enabled(self) -> bool:
        return bool(os.getenv("HUGGINGFACE_API_KEY"))

    @property
    def tavily_enabled(self) -> bool:
        return bool(os.getenv("TAVILY_API_KEY"))

    @property
    def google_enabled(self) -> bool:
        return bool(os.getenv("GOOGLE_API_KEY"))

    def provider_status(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }


settings = Settings()