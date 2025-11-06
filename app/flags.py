"""Simple feature flag registry with env overrides."""
from __future__ import annotations

import os

_DEFAULT_FLAGS = {
    "REC_DISABLE": "0",  # set to '1' to disable recommendation endpoint
    "QUIZ_DISABLE": "0",  # set to '1' to disable quiz endpoints
}

def is_enabled(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(name, "0"))
    return val != "1"
