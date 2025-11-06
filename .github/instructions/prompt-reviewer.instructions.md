---
applyTo: "**/.github/prompts/*.prompt.md"
description: "Designated prompt reviewer checklist for high/critical risk prompts"
---
# Prompt Reviewer Instructions

## Mandatory Frontmatter Fields
- id, name, version, owners, description, (risk_level if high/critical), rationale (if high/critical).

## Versioning
- Increment `version` for any substantive change (logic, wording that affects output, risk level change).
- Document change summary inline or in `prompts.md` changelog section.

## Risk Assessment
- High: influences recommendation, metrics, escalation behaviors.
- Critical: impacts security, data exposure, or compliance messaging.

## Output Format
- If JSON specified: prompt must direct model to output ONLY JSON (no prose, no markdown wrappers).
- Placeholders must be clearly delimited; avoid ambiguous tokens.

## Secret Hygiene
- No inline secrets or tokens; only refer to env variable names.

## Determinism & Stability
- Tie-breaking rules explicit (e.g., list order, score equality). Avoid implicit randomness.

## Validation Steps
1. Parse frontmatter; confirm required fields.
2. Check presence of `risk_level` + `rationale` when risk_level high/critical.
3. Ensure no forbidden words: `API_KEY=`, real credential patterns.
4. Confirm JSON keys match schemas where applicable.
5. Confirm version bump vs repository baseline.

## Prohibited
- Grep-based search instructions.
- Non-specific fallback instructions (must specify escalation path).

## Reviewer Action
- Apply label `prompt-reviewed` on PR after all checks pass.
- If any check fails, request changes; do NOT merge.
