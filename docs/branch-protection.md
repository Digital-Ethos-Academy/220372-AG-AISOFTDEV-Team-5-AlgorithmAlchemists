# Branch Protection Policy (Initial)

## Protected Branches
* `master` (main trunk)

## Required Status Checks (post-merge of quality gates)
1. Ruff Lint — no errors.
2. Mypy Type Check — no fatal errors.
3. PyTest + Coverage — all tests pass; line coverage ≥ 80%.
4. Bandit Security Scan — no HIGH severity findings.
5. Pip-Audit Dependency Scan — no HIGH vulnerabilities.
6. Prompt Lint — all prompt files pass governance checklist.

## Additional Rules
* Require 1 review (Engineering Lead) for feature changes; 2 reviews for prompt or metric modifications.
* Enforce signed commits (DCO sign-off).
* Disallow force pushes & deletions of protected branches.
* Require linear history (rebase merges) when feasible.

## Labels Mapping
* `feat` — new endpoint or significant capability.
* `nfr` — non-functional enhancement.
* `security` — security-related changes.
* `governance` — prompt / PRD / traceability updates.
* `adr` — architectural decision records.

## Change Review Escalation
High impact (metric logic, recommendation scoring, prompt risk_level=High) requires Product + Engineering + Compliance approval before merge.
