"""Generate a local .env file from .env.example (idempotent).

Safeguards:
- Will NOT overwrite an existing .env (exit code 1 with JSON message).
- Copies only non-comment, non-empty lines preserving ordering.
- Appends a trailing newline.

Usage:
  python scripts/generate_dotenv.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

EXAMPLE = Path(".env.example")
TARGET = Path(".env")


def main() -> int:
    if not EXAMPLE.exists():
        print(json.dumps({"error_code": "ENV_EXAMPLE_MISSING", "message": ".env.example not found", "trace_id": None}))
        return 1
    if TARGET.exists():
        print(json.dumps({"error_code": "ENV_ALREADY_EXISTS", "message": ".env already exists; aborting", "trace_id": None}))
        return 1
    lines: list[str] = []
    for raw in EXAMPLE.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        if raw.strip().startswith("#"):
            continue
        lines.append(raw)
    TARGET.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "created", "file": str(TARGET)}))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
