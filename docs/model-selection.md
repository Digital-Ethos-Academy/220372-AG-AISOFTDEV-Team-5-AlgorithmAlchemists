# Model Selection Strategy

| Task Category | Primary Model | Secondary (Cost-Saving) | Escalation Trigger |
|---------------|---------------|-------------------------|--------------------|
| CRUD scaffolding / boilerplate | GPT-5 mini | GPT-4o (complex validation) | High complexity or performance concerns → GPT-4.1 |
| Complex refactor / performance review | GPT-4o | GPT-4.1 (deep reasoning) | Algorithmic risk, > O(n log n) complexity |
| Security review / prompt risk audit | GPT-4.1 | (none) | Always enforce GPT-4.1 |
| Recommendation logic modifications | GPT-4o | GPT-4.1 (tie-breaking / scoring changes) | High-risk prompt change → GPT-4.1 |
| Metrics / analytical explanation | GPT-4o | GPT-5 mini (simple copy edits) | High-risk wording change → GPT-4.1 |
| Visual regression governance | GPT-5 mini | GPT-4o (policy updates) | Snapshot methodology shift → GPT-4.1 |
| Planning (read-only mode) | GPT-5 mini | GPT-4o (bigger scope) | Multi-service integration plan → GPT-4.1 |

## Principles
- Prefer smallest sufficient model to conserve premium quota.
- Auto-selection allowed only for low-risk conversational prompts; guardrails escalate high/critical tasks.
- High & critical prompts: enforced GPT-4.1 regardless of manual selection.

## Enforcement Hooks (Planned)
- CI script inspects prompt diffs; if `risk_level: high|critical` → verify GPT-4.1 usage annotation or override instruction.
- Chat modes embed default models; override only with explicit reviewer label present.

## Conservation Policy
When overall premium usage > 50% of allocation:
- Downgrade medium-risk tasks from GPT-4o → GPT-5 mini.
- Maintain GPT-4.1 only for high/critical categories.

## Future Extensions
- Add latency vs cost metrics per task category after instrumentation.
- Integrate per-prompt outcome validation (semantic diff) to detect unintended reasoning drift.
