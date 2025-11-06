# Guardrails Best Practices (Comprehensive)

This document codifies implementation-ready best practices for zero-margin-of-error agent development across 20 domains.

## 1. Scope & Agent Boundaries
- Read-only by default outside approved modes. Editing allowed only in implementation mode.
- Protected paths: `app/security.py`, `schemas/*`, `.github/instructions/*`, `requirements.txt` (needs review label).
- Agents may create tests, docs, schemas only after plan approval.

## 2. Model Selection Matrix
| Task | Default | Escalate If | Escalation Model |
|------|---------|-------------|------------------|
| Simple refactor | GPT-5 mini | Ambiguous types | GPT-4o |
| Planning | GPT-4o | High risk feature | GPT-4.1 |
| Security review | GPT-4.1 | Always | GPT-4.1 |
| Schema evolution | GPT-4.1 | Always | GPT-4.1 |
| Recommendation algo | GPT-4.1 | Confidence <0.85 | GPT-4.1 |
| Docs generation | GPT-5 mini | Domain complexity | GPT-4o |

## 3. Deterministic Harness
- Seed: 1337; freeze datetime & epoch.
- All randomness routed through helper if needed.
- Golden fixtures under `data/golden/*` versioned; no in-place edits.

## 4. Coverage & Mutation
- Minimum coverage 85% (pyproject fail_under) trending to 90%.
- No negative diff beyond 0.25%. Mutation testing (future) target > 70% survived mutants.

## 5. Structured Logging Validation
- Required fields: ts, trace_id, user_id/null, method, path, status_code, latency_ms, confidence/null.
- p95 latency thresholds defined per endpoint (stub). Validation test ensures schema conformance & latency < budget in smoke run.

## 6. Prompt Governance
- Frontmatter: id, name, version, owners, description, risk_level, rationale (high/critical), last_reviewed.
- Automated version bump on semantic change (script TBD). High/critical require golden output check.

## 7. Security Enforcement
- Run `bandit`, `pip-audit` in CI; fail on HIGH severity.
- Secret scanning with patterns (AWS key, generic token) before merge.
- Security headers test mandatory (already present).

## 8. Performance Budgets (Initial Targets)
| Endpoint | p95 Latency ms | Max Payload KB |
|----------|----------------|----------------|
| /recommendation | 120 | 32 |
| /qa | 150 | 48 |
| /metrics | 180 | 128 |

## 9. Chat Modes
- planning, implementation, review, security, data created.
- Tool whitelists restrict actions; review/security read-only.

## 10. Rollback & Drift Detection
- Golden fixture diff fails CI; auto-create revert branch suggestion.
- Schema version increments require compatibility test vs previous N=2 versions.

## 11. Golden Fixture Expansion
- Add: recommendation_tie.json, qa_high_confidence.json, metrics_snapshot_basic.json.
- Each includes expected result + confidence band.

## 12. Visual Regression & Accessibility
- Adopt Playwright + Axe; baseline snapshots committed with rationale.
- Enforce contrast >=4.5:1; aria-label required for interactive elements.

## 13. Negative Path & Fuzz Tests
- Systematic invalid inputs: type mismatch, boundary, malicious string.
- Lightweight deterministic fuzz (seed 1337) for selected endpoints.

## 14. Agent Action Audit Trail
- Log: timestamp, model, mode, tools invoked, changed files, confidence, rationale.
- Stored in audit log with agent_action flag.

## 15. Dependency & License Governance
- `pip-licenses` to generate license report; allowlist MIT, Apache-2.0, BSD, ISC.
- Fail on GPL, AGPL, LGPL additions.

## 16. Schema Evolution Policy
- Add `version` property; semantic versioning (MAJOR breaking). Migration test ensures backward compatibility for minor/patch.

## 17. Environment & Config Lock
- `.env.example` validated vs loaded env keys; new keys require schema doc & security review label.

## 18. Pre-commit & CI Hooks
- Pre-commit: ruff, mypy, pytest (fast subset), prompt_lint, coverage guard.
- CI stages: Lint → Type → Unit+Coverage → Schema Conformance → Security → Performance Smoke.

## 19. Risk Matrix Refinement
- Scoring: impact(1-5)*data_sensitivity(1-5)*change_scope(1-3). High >=40, Critical >=50.
- Maps to mandatory GPT-4.1 usage.

## 20. Confidence Escalation Integration
- Standard envelope: {status, data?, fallback?, trace_id, confidence, next_action?}.
- Below threshold returns fallback + next_action guidance; above threshold returns data only.

## Implementation Roadmap (Next)
1. Integrate confidence helper into endpoints.
2. Add schema version field & compatibility test.
3. Expand golden fixtures.
4. Add coverage guard to CI pipeline.
5. Create license allowlist enforcement script.
6. Implement prompt version bump detector.
7. Add audit trail extension for agent actions.
