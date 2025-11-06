---
applyTo: "tests/**/*.py"
description: "Testing determinism, naming, coverage, negative paths"
---
# Testing Instructions

## Naming & Structure
- Functional requirement tests: `test_fr<ID>_<scenario>` (e.g., `test_fr4_qa_fallback_low_confidence`).
- Other tests must have descriptive scenario names; avoid generic `test_placeholder` except as temporary.

## Determinism
- Use central fixtures for random seed + time freeze.
- Stable ordering: sort lists before equality assertions.

## Coverage & Guardrails
- Target minimum coverage: 85%; fail CI if delta < -0.5% vs previous baseline.
- Each new endpoint adds: success test + negative test (404/401/409/503 as applicable) + schema conformance.

## Golden Fixtures
- Store in `data/golden/`; tests must not mutate fixture data.
- Recommendation outputs compared against golden expected JSON.

## Logging & Observability
- For endpoints with audit logging, assert presence of required fields in at least one log line.

## Negative Test Matrix (Apply Where Relevant)
| Case | Expectation |
|------|-------------|
| Missing resource update/delete | 404 JSON error envelope |
| Duplicate create | 409 error_code `duplicate` |
| Unauthorized admin action | 401 error_code `unauthorized` |
| Feature disabled flag | 503 error_code `feature_disabled` |

## Fallback Confidence
- When confidence < 0.85 in QA or recommendation rationale, assert escalation JSON from helper function.

## Prohibited
- Network calls to external services during tests.
- Reliance on execution timing for pass conditions.
