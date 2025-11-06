"""Environment variable validation script.

Ensures required API provider keys and internal tokens are present (non-empty)
before running sensitive operations (e.g., production deploy, CI critical path).

Design:
- Does NOT print actual secret values (only variable names).
- Allows blank values in local/dev context unless STRICT_ENV=1.
- Fails fast with structured JSON error output for CI consumption.

Exit Codes:
0 -> All good
1 -> Missing or blank required keys

Usage:
  python scripts/validate_env.py            # permissive (local)
  STRICT_ENV=1 python scripts/validate_env.py  # strict (CI/prod)
"""
from __future__ import annotations

import json
import os
import sys
from typing import List, Dict, Any


REQUIRED_KEYS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "HUGGINGFACE_API_KEY",
    "TAVILY_API_KEY",
    "GOOGLE_API_KEY",
]

OPTIONAL_KEYS = [
    "INTERNAL_ACCESS_TOKEN",  # placeholder allowed but flagged when strict
]

PLACEHOLDER_VALUES = {"change_me_internal_token", "your_key_here", ""}


def _is_strict() -> bool:
    return os.getenv("STRICT_ENV", "0") == "1"


def validate() -> Dict[str, Any]:
    strict = _is_strict()
    missing: List[str] = []
    placeholder: List[str] = []

    for key in REQUIRED_KEYS:
        val = os.getenv(key)
        if not val:
            # Always missing in both strict and non-strict (hard requirement)
            missing.append(key)
    for key in OPTIONAL_KEYS:
        val = os.getenv(key, "")
        if strict and (val in PLACEHOLDER_VALUES):
            placeholder.append(key)

    status = "pass"
    if missing or placeholder:
        status = "fail"

    return {
        "status": status,
        "strict": strict,
        "missing_keys": missing,
        "placeholder_keys": placeholder,
        "required_count": len(REQUIRED_KEYS),
    }


def main() -> int:
    result = validate()
    if result["status"] == "fail":
        error = {
            "error_code": "ENV_VALIDATION_FAILED",
            "message": "Environment variable validation failed",
            "trace_id": None,
            "details": result,
        }
        print(json.dumps(error, separators=(",", ":")))
        return 1
    print(json.dumps({"status": "ok", "details": result}, separators=(",", ":")))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    sys.exit(main())
