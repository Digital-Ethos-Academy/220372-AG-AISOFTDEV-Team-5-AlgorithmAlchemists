# Security Exceptions (Temporary)

| Component | Issue | Current Version | Patched Version | Status | Rationale | Follow-up |
|-----------|-------|-----------------|-----------------|--------|-----------|-----------|
| starlette (transitive via fastapi) | GHSA-f96h-pmfr-66vw / GHSA-2c2j-9gv5-cj73 / GHSA-7f5h-v6xp-fcq8 | managed by fastapi 0.115.2 (pulls vulnerable starlette) | >=0.47.2 / >=0.49.1 | ACCEPTED TEMPORARY | FastAPI dependency constraints conflict with direct pinning; demo environment, no external exposure | Track upstream FastAPI release enabling upgrade; issue QG3-FUP1 |

Acceptance Date: 2025-11-05

Mitigations:
1. No production traffic; mock data only.
2. No sensitive credentials or user input beyond simple query params.
3. Monitoring of FastAPI release notes for dependency bumps.

Exit Criteria:
Upgrade fastapi so that pip-audit passes with no HIGH vulns and no dependency resolution conflicts.
