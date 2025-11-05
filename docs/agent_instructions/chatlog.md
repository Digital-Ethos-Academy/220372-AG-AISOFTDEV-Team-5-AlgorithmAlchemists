# Chatlog Instructions (Pointer)

Canonical chat logging protocol lives at `chatlog/chatlog_instructions.md`.
This pointer ensures agents integrate logging rules into the unified instruction load sequence without duplicating full content.

## Required Invariants (Imported)
- IDs strictly increment, never renumbered.
- New entries: update index, create response file, append transcript.
- Summaries: single sentence ≤200 chars ending with a period.
- Hash field: `HASH_PENDING` until hashing routine implemented.
- Corrections: overwrite file + update index row (add `correction` tag) without ID change.

## Load Directive
Agents MUST fully parse and honor all sections of `chatlog/chatlog_instructions.md` after prior files in `execution_order.md`.

## OVERRIDES
None here; any override must appear in a later file with explicit references.
