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

## AI Prompt Governance
- All prompt modifications must bump `version` field and update changelog in each `.prompt.md`.
- High risk prompts (recommendation, metrics) require rationale line.

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

## Revision Notes
- This file defines global instructions; specialized instructions will live in additional `.instructions.md` files.
