# Prompt Risk Matrix

| Prompt File | Purpose | Risk Level | Rationale | Review Requirement |
|-------------|---------|-----------|-----------|--------------------|
| `overview.prompt.md` | Summarize high-level project overview | medium | Influence onboarding messaging | 1 reviewer if wording changes |
| `qa.prompt.md` | Generate Q&A responses with confidence | high | Affects factual correctness & escalation | 1 reviewer + rationale line |
| `recommendation.prompt.md` | Team placement rationale JSON | high | Drives recommendation transparency | 1 reviewer + rationale line |
| `metrics-explainer.prompt.md` | Explain metrics calculations | high | Impacts interpretation of KPIs | 1 reviewer + rationale line |
| `gap-detection.prompt.md` | Describe detected knowledge gaps | medium | User guidance but limited downstream logic | Reviewer optional |

## Risk Level Definitions
- Low: Cosmetic wording; no functional or decision impact.
- Medium: Influences user perception; minimal functional consequences.
- High: Impacts decision-making logic (recommendations, metrics, escalation).
- Critical: Security, compliance, or data exposure implications.

## Review Workflow
1. Author updates prompt → bump version.
2. If risk_level high/critical → add `rationale:` line.
3. CI lint checks frontmatter & rationale.
4. Designated reviewer applies `prompt-reviewed` label.
5. Merge allowed only after label & green lint/tests.

## Escalation
- Critical prompts (none yet) will require two reviewers and GPT-4.1 enforcement.

## Future Additions
Add new rows with classification and rationale; keep table sorted alphabetically by file name.
