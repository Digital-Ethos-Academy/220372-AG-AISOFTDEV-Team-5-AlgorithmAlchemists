---
applyTo: "**/*.py"
description: "Python deterministic, type-safe implementation guardrails"
---
# Python Implementation Instructions

## Determinism
- Always set fixed random seeds (`random.seed(0)`, `numpy.random.seed(0)` if used) in tests.
- Freeze time in tests needing timestamps using a fixture (target timestamp: `2025-01-01T00:00:00Z`).

## Style & Types
- Follow PEP8; maximum function length ~60 lines unless justified.
- Public functions MUST have type hints (parameters + return) and docstring summarizing behavior + error cases.
- Prefer explicit imports; avoid wildcard.

## Error Handling
- Raise domain-specific exceptions only when recoverable; otherwise let FastAPI exception handler wrap.
- All error responses must conform to JSON envelope: `{"error_code": <string>, "message": <string>, "trace_id": <string|null>}`.

## Logging
- Use structured logger ensuring fields: ts, trace_id, user_id (nullable), method, path, status_code, latency_ms, confidence (if relevant).

## Performance Review Trigger
- Flag algorithms exceeding O(n log n) for review; add comment `# PERF_REVIEW` with complexity rationale.

## Security
- Never log secrets or tokens; environment variable names only.

## Testing
- Each new endpoint: add unit test + schema conformance test stub.
- Test names follow pattern `test_fr<ID>_<scenario>` if tied to functional requirement.

## Prohibited
- Inline timing sleeps in tests (use fixtures/mocks).
- Non-deterministic ordering reliance (explicitly sort when comparing sets/lists).
