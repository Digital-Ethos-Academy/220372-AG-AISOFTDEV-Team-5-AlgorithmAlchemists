---
applyTo: "**"
description: "Global coding, testing, AI prompt governance, accessibility, and security instructions for POIT project"
---
# Global Copilot Instructions

## Code Style
- Python: PEP8, explicit imports, type hints for all public functions.
- React/TS: Functional components, hooks only, no legacy class components.
- Avoid premature optimization; prefer clarity first.

## Error Handling
- Return structured JSON errors: {"error_code", "message", "trace_id"}.
- FastAPI handlers must not swallow exceptions—use exception handlers.

## Security & Secrets
- Never output demo secrets (TAVILY_API_KEY, OPENAI_API_KEY, etc.). Use environment variable names only.
- No hardcoded tokens in code or prompts.
- Run `scripts/secret_scan.py` in CI; fail on detections. Use allowlist file for justified false positives (future enhancement).
- Run `scripts/license_allowlist.py` to enforce approved licenses (MIT, Apache-2.0, BSD-2/3, ISC). Block GPL/AGPL/LGPL.

## AI Prompt Governance
- All prompt modifications must bump `version` field and update changelog in each `.prompt.md`.
- High risk prompts (recommendation, metrics) require rationale line.
 - Disallow any use of grep-based or raw full-repo search tools by agents; operate only on explicitly provided file paths & curated context. If broader discovery is required, escalate to human review.
 - Each high/critical risk prompt must list `risk_level` and a one-line `rationale:` explaining safeguards.

## Testing
- New endpoint: add unit test + integration test stub at creation time.
- Test name pattern: test_fr{ID}_{scenario}.

## Accessibility
- Provide aria-labels for interactive elements.
- Ensure color contrast >= 4.5:1.

## Output Formatting (Chat Responses)
- Summaries: concise bullet lists.
- Code: minimal snippet solving the task; no extraneous commentary unless asked.

## Prohibited
- Generating unreviewed production deployment scripts.
- Speculative architecture beyond roadmap versions unless explicitly requested.

## Performance
- Highlight any algorithm with > O(n log n) complexity for review if dataset may scale.

## Fallback Behavior
- If confidence < 0.85 in Q&A design spec: return escalation suggestion.

## Tool & Model Restrictions
- NEVER invoke grep-style codebase search utilities ("grep_search") or undisclosed tooling that can produce partial / ambiguous context. Rely on enumerated file listings and explicit reads only.
- High or critical risk tasks (security review, recommendation algorithm changes, metrics calculations, schema evolution) must use GPT-4.1 unless cost threshold exceeded AND human override granted. Routine scaffolding may use GPT-5 mini. Balanced tasks use GPT-4o.
- Auto model selection acceptable only for low-risk conversational queries; do not rely on Auto for migrations or security-sensitive edits.

## Determinism & Reproducibility
- Tests must be deterministic: fixed random seed, frozen timestamp when applicable.
- Confidence evaluation centralized; endpoints must call `evaluate_confidence` before returning model-derived scores.
- Recommendation & QA logic changes require golden fixture validation prior to merge.
- Visual regression updates must include rationale in commit message and avoid unrelated PNG churn.

## Log & Schema Guarantees
- All request audit log lines must include: ts, trace_id, user_id (or null), method, path, status_code, latency_ms, confidence (or null) aligned with `schemas/audit-log-entry.schema.json`.
- New endpoints require JSON Schema addition + schema conformance test before merge.

## Reviewer Checklist (High/Critical Prompts)
1. Frontmatter contains id, name, version, owners, description, risk_level.
2. Version incremented relative to prior commit.
3. Rationale line present for risk_level high/critical.
4. No secrets or tokens embedded.
5. Output format instructions unambiguous (JSON-only if required).
6. References to existing schema files use correct filenames.
7. Model escalation rule followed (GPT-4.1 for high/critical unless documented exception).

## Prohibited (Extended)
- grep-based codebase scanning by AI agents.
- Non-deterministic test artifacts (time-dependent outputs without freeze).
- Silent snapshot updates (PNG changes without commit rationale).

## Revision Notes
- This file defines global instructions; specialized instructions will live in additional `.instructions.md` files.
 - Integrated MCP, prompt files, chat modes, model selection & audit schema alignment best practices.
