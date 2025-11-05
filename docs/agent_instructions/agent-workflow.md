# Agent Workflow Instructions

Purpose: Define the invariant lifecycle every agent must follow for each user prompt and resulting artifact change.

## Scope
Applies to ALL AI agents operating in this repository (logging, branching, automation, integrity checks).

## Lifecycle Steps (Prompt → Merge)
1. Detect new prompt (logged in chatlog/index.md).
2. Verify chatlog entry integrity (ID sequential, timestamp ISO8601, summary ≤200 chars).
3. Determine if artifacts will change; if yes → create prompt branch per branching_instructions.md.
4. Apply minimal, isolated changes (docs/code/tests) following current phase context.
5. Run integrity pre-flight (hash placeholder insertion, secrets scan).
6. Prepare commit using commit template (include prompt ID, tags, hash field `HASH_PENDING`).
7. Open PR with required body sections and labels (prompt, phase:<name>, automation if applicable).
8. Execute CI (validation + tests). If docs/log only and CI green → eligible for auto-merge.
9. Merge (fast-forward for prompt branch; squash only if multiple commits unexpectedly created).
10. Delete ephemeral branch (prompt/feature/docs).
11. Update hash if hashing routine available (post-merge validation).
12. Record completion in future audit index (optional extension).

## Invariants
- Never skip branch creation for prompt-driven changes unless explicitly classified as no-op (no artifact change).
- Never renumber chatlog IDs.
- Never push commits containing secrets (see integrity.md patterns).
- Always base prompt branch on active phase branch if it is ahead of master; else base on master.
- Always ensure one commit per prompt branch unless iterative development was explicitly requested.

## OVERRIDES Mechanism
This file does NOT override branching rules; it composes with them. Any future workflow override must be declared in a later file with `## OVERRIDES`.

## Error Handling
- If integrity pre-flight fails: abort prior to commit; log reason.
- If rebase conflicts occur: attempt auto-resolution once; on failure add label `manual-intervention` and halt.

## Labels (Minimum Set)
- prompt
- phase:<phase-name>
- docs-only (if no code outside docs/chatlog)
- automation (if an automation script performed majority of steps)

## Required Commit Footer
```
Co-authored-by: Automation Bot <bot@example.com>
[automation]
```
(Replace email when dedicated bot identity established.)

## Transition to Multi-Agent Coordination
Agents implementing specialized tasks (e.g., retrieval tuning) MUST still execute or respect this workflow before merging.
