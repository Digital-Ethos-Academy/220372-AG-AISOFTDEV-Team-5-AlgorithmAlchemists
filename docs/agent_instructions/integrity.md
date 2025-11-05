# Integrity & Security Instructions

Purpose: Guarantee immutability, consistency, and secret hygiene across all agent-managed operations.

## File Presence Invariants
The following MUST always exist:
- `docs/agent_instructions/execution_order.md`
- `docs/agent_instructions/branching_instructions.md`
- `docs/agent_instructions/agent-workflow.md`
- `docs/agent_instructions/automation.md`
- `docs/agent_instructions/integrity.md`
- `docs/agent_instructions/chatlog.md`
- `docs/agent_instructions/multi-agent-coordination.md` (placeholder allowed but not empty)

## Hashing (Phase 1 Placeholder)
- Each instruction file will later receive a SHA256 hash stored in `docs/agent_instructions/index.json`.
- Until the hashing script is implemented, use `HASH_PENDING` placeholders.
- Hash scope (best practice): entire file content normalized (LF endings, trimmed trailing spaces).

## Secrets Scan (Must Pass Before Commit)
Reject commit if any pattern matches:
- `API_KEY=`
- `SECRET=`
- `PRIVATE_KEY` or `-----BEGIN`
- Raw 64+ character high-entropy strings (heuristic optional phase 2)

## Chatlog Consistency Check
- Ensure latest ID increments by 1.
- Ensure top row hash = `HASH_PENDING` or valid 64-char hex.
- Ensure timestamp matches regex: `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`.

## Deletion Policy
- Deleting any required instruction file triggers CI failure until a prompt branch documents rationale and `execution_order.md` updated.

## Conflict Handling
- If instruction file diff conflicts: resolve via rebase once; failing → label `manual-intervention`.

## OVERRIDES Procedure
- Any override MUST specify prior file + section replaced.
- Invalid override (missing target reference) → CI failure.

## Index File (index.json) Rules
- Must list each required instruction file with a `hash` field.
- Missing or extra entries → CI failure.

## Error Escalation
1. Attempt auto-correction of trivial format issues (whitespace, trailing spaces).
2. Re-run validation.
3. If still failing → halt; output remediation instructions.

## Security Note
Never embed full model responses containing secrets. If detected, redact and annotate `[REDACTED_SECRET]`.

## OVERRIDES
None.
