---
applyTo: "**/*.py,frontend/src/**/*.js,frontend/src/**/*.jsx,frontend/src/**/*.ts,frontend/src/**/*.tsx"
description: "Security boundaries, secret hygiene, headers enforcement"
---
# Security Instructions

## Secrets & Tokens
- Never hardcode API keys or tokens. Reference environment variables only.
- Do not print secret values in logs or prompts.

## Input Validation
- Validate request payload shapes against JSON Schemas where defined.
- Reject unexpected fields with clear error_code `validation_error`.

## Headers & Protection
- Internal endpoints (runtime metrics, future admin) must check header token if configured.
- Security headers test must remain green (see `test_security_headers.py`).

## Logging
- Audit log lines must not include full PII; only anonymized IDs.
- Ensure trace_id present for every request line; generate if missing.

## Recommendation & QA
- Rationale text must avoid sensitive personal info beyond provided mock identifiers.

## Error Responses
- Uniform envelope: `error_code`, `message`, `trace_id` (nullable).

## Review Triggers
- Dependency added → run vulnerability scan and update `SECURITY_EXCEPTIONS.md` if needed.
- High-risk prompt changes → require rationale frontmatter line + reviewer confirmation label.

## Prohibited
- Storing raw secrets in version control.
- Disabling audit logging for performance tweaks without ADR.
