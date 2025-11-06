# Backlog (Initial Extraction from PRD v1.0.1)

## Functional Requirements
| Issue Key | FR | Summary | Acceptance Criteria Reference | Owner | Status |
|-----------|----|---------|-------------------------------|-------|--------|
| FR1 | Overview | Implement /overview endpoint (done) | PRD §8 FR1 | Product | DONE |
| FR2 | Org Explorer | Implement /org endpoint (done) | PRD §8 FR2 | Eng Lead | DONE |
| FR3 | Role Lookup | Implement /roles endpoint (done) | PRD §8 FR3 | Eng Lead | DONE |
| FR4 | Q&A | Implement /qa endpoint (done) | PRD §8 FR4 | Data Engineer | DONE |
| FR5 | Recommendation | Implement /recommendation endpoint (done) | PRD §8 FR5 | Eng Lead | DONE |
| FR6 | Quiz | Implement /quiz + /quiz/submit endpoints (done) | PRD §8 FR6 | Product | DONE |
| FR7 | Metrics | Implement /metrics endpoint (done) | PRD §8 FR7 | Product | DONE |
| FR8 | Gap Detection | Implement /gaps endpoint (done) | PRD §8 FR8 | Knowledge Curator | DONE |
| FR9 | Fallback | Implement /qa/fallback endpoint (done) | PRD §8 FR9 | Engineering | DONE |

## Quality Gate Enhancements
| Key | Category | Description | Owner | Status |
|-----|----------|-------------|-------|--------|
| QG1 | Lint | Add ruff configuration & CI step | Engineering | TODO |
| QG2 | Types | Add mypy config & CI step | Engineering | TODO |
| QG3 | Security | Add bandit + pip-audit to CI | Security | TODO |
| QG4 | Coverage | Enforce ≥80% line coverage threshold | Engineering | TODO |
| QG5 | Prompt Lint | Implement prompt governance script | Product | TODO |
| QG6 | SBOM | Generate CycloneDX SBOM artifact in CI | Engineering | TODO |

## Governance & Documentation
| Key | Item | Description | Status |
|-----|------|-------------|--------|
| GOV1 | ADR 0001 | Record metric choice decision | DONE |
| GOV2 | Branch Protection Doc | Define required checks | DONE |
| GOV3 | Issue Templates | Standardize issue creation | TODO |
| GOV4 | Backlog File | Provide consolidated mapping | DONE |

## Future Work (Next Minor Versions)
| Key | Version Target | Item | Notes |
|-----|----------------|------|-------|
| FUT1 | 1.1.0 | Embeddings retrieval upgrade | Replace keyword heuristic |
| FUT2 | 1.2.0 | Personalization + i18n | Adaptive quiz ordering |
| FUT3 | 1.3.0 | SSO + HRIS integration | Real user/role data |
| FUT4 | 1.4.0 | Slack/Jira signals | Engagement metrics |
| FUT5 | 1.5.0 | Compliance hardening | SOC2 control drafts |
