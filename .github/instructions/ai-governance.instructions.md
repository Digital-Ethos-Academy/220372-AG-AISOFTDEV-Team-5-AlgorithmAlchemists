---
applyTo: "**"
description: "AI governance, chat modes, MCP, prompt files usage policy"
---
# AI Governance & Tooling Policy

## Chat Modes
Use workspace chat modes under `.github/chatmodes/`:
- planning: read-only (analysis only)
- implementation: test-first edits
- review: no edits, risk & coverage analysis
- security: high-risk, model escalation enforced
- data: read-only metrics & schema analysis

## Prompt Files
- Must reside in `.github/prompts/` with `.prompt.md` extension.
- Frontmatter required: id, name, version, owners, description, risk_level (if high/critical), rationale (if high/critical), last_reviewed.
- Version bump on any output-impacting change.

## MCP Servers
- Allow registry-only servers; require explicit trust review.
- No MCP server that executes arbitrary shell without curated allowlist.
- Configuration kept in `.vscode/mcp.json` (no secrets; use env vars).

## Model Selection
- Security & schema evolution: GPT-4.1 mandatory.
- Planning & complex reasoning: GPT-4o default; escalate if ambiguity.
- Routine refactors & docs: GPT-5 mini unless risk score >= 20.

## Confidence & Escalation
- All QA/recommendation responses pass through confidence helper; escalate below threshold with next_action guidance.

## Audit & Trace
- Audit lines must validate against `schemas/audit-log-entry.schema.json`.
- Include `trace_id` header on requests; agents generate if missing.

## Determinism
- Tests rely on global seed 1337 and frozen timestamp (see `tests/conftest.py`).

## Prohibited
- grep-style repository searches.
- Unversioned schema changes.
- Secret exposure; only env var names.

## Review Checklist (Summary)
1. Frontmatter fields present & version incremented.
2. Risk matrix score consistent with model selection.
3. Golden fixture updated when logic changes.
4. Coverage guard passes (no regression >0.25%).
5. Audit log schema test green.
