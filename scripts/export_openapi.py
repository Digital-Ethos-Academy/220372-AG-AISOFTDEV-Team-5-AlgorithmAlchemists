"""Export the FastAPI OpenAPI schema to openapi.json."""
from __future__ import annotations

import json
from pathlib import Path
from app.main import app

def main() -> None:
    schema = app.openapi()
    Path("openapi.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print("openapi.json written")

if __name__ == "__main__":
    main()
