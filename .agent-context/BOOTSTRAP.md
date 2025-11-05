# Agent Context Bootstrap Capsule

This file provides a minimal, machine-friendly capsule for agents to ensure they always ingest the authoritative project context before any action.

## Load Sequence (Hard Requirement)
1. Read `.agent-context/index.json`.
2. Verify `prd_path` exists and hash field is not empty.
3. Read the PRD at `prd_path`.
4. Read and process each file listed under `instruction_files` in the order defined by `execution_order.md`.
5. If any file missing, HALT and report.

## Hash & Version
- `prd_hash` must match recomputed SHA256 of `docs/RAG_Navigator_PRD.md`.
- `prd_version` must match a line `Version: X.Y.Z` inside the PRD (manual bump via prompt branch).
- Hash mismatch protocol: create `HASH_ALERT.md`, open issue, apply label `hash-mismatch` on active PR (if exists), halt.

## Embedding / RAG Enrichment (Phase 1 Stub)
- Chunk size target: 1000 chars, overlap: 150.
- Store embeddings in SQLite at `.agent-context/agent_context.db` (table: `chunks(prd_section TEXT, content TEXT, vector BLOB)` — vectors stub until implemented).
- Retrieval: top_k=6 for semantic queries.

## Mandatory Checks
- Instruction files non-empty.
- No secret patterns: `API_KEY=` `SECRET=` `PRIVATE_KEY` `-----BEGIN`.
- Chatlog invariants hold (ID incremental, timestamp format correct).

## On Failure Conditions
HALT and report via issue + `HASH_ALERT.md` if:
- Missing file.
- Hash mismatch.
- Empty required instruction file.
- PRD version line missing.

## Attention Capsule Summary
PRD: docs/RAG_Navigator_PRD.md | Version: 1.0.0 | Hash: HASH_PENDING | Instructions Count: 7 | Embeddings: pending

## Do Not Modify
Any modification must come through a prompt branch with an updated hash and version bump as required.
