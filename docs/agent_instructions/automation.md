# Automation Instructions

Purpose: Define required automated Git / CI behaviors ensuring zero margin for error in repository traceability.

## Core Automation Responsibilities
- Prompt detection → branch creation (if artifact change) or log-only classification.
- Commit template enforcement (prompt ID, tags, hash field).
- PR auto-generation with standardized body sections.
- CI validation: instruction file presence, chatlog format, branch naming patterns.
- Conditional auto-merge for docs/log-only prompt branches when green.
- Post-merge cleanup (delete branch, optional hash finalize).

## Command Sequence (Conceptual)
1. `detect_prompt()`
2. `create_branch()`
3. `stage_changes()`
4. `run_pre_commit_checks()` (secrets scan, file presence)
5. `commit_and_push()`
6. `open_pull_request()`
7. `run_ci_pipeline()`
8. `auto_merge_if_eligible()`
9. `finalize_hash()` (future)

## Auto-Merge Eligibility Criteria
- Branch type: prompt or docs.
- Diff scope: restricted to `docs/`, `chatlog/`, or instruction files; no backend/frontend code.
- CI status: success.
- No `hold` label present.

## Conflict & Retry Policy
- Single automated rebase attempt on master or phase branch.
- If second attempt needed: abort; apply `manual-intervention` label; no force-push.

## Branch Naming Validation
Regex examples:
- Prompt: `^prompt/\d{3}-[a-z0-9-]+$`
- Phase: `^phase/[a-z0-9-]+$`
- Feature: `^feature/[a-z0-9-]+$`
Fail CI on mismatch.

## Required PR Body Sections
```
Summary:
<concise description>

Prompt Reference:
ID <XXX> – link to response file.

Changed Files:
<List or count>

Verification:
<Tests / validation summary>

Risks & Rollback:
<Clear steps>
```

## Labels Applied Automatically
- prompt (if prompt branch)
- docs-only (if only docs/log changes)
- phase:<phase-name>
- automation

## Auto-Merge Implementation Notes
Use GitHub Actions or bot account:
- Validate criteria → call merge endpoint (fast-forward). Fallback to manual if API rate limit or permission error; apply `manual-intervention`.

## Security Controls
- Block merge when secrets scan fails.
- Verify `.env` not staged.

## Extensibility Hook
Future script names (planned):
- `scripts/new_prompt_branch.py`
- `scripts/prepare_commit.py`
- `scripts/open_pull_request.py`
- `scripts/merge_prompt_branch.py`
- `scripts/validate_chatlog.py`

## OVERRIDES
None.
