<div align="center">

# POI Compass
**Project Orientation Intelligence Tool** – Compresses onboarding time and eliminates context drift for large (500+) project teams.

[![Status](https://img.shields.io/badge/status-demo-blue)](./prd.md) [![Python](https://img.shields.io/badge/Python-3.11+-yellow)]() [![FastAPI](https://img.shields.io/badge/FastAPI-enabled-green)]() [![React](https://img.shields.io/badge/React-latest-61dafb)]() [![License](https://img.shields.io/badge/License-Internal--Use--Only-lightgrey)]()

</div>

## 1. Executive Snapshot
POI Compass provides an authoritative, queryable project overview, org structure explorer, role responsibility lookup, high‑accuracy Q&A, team placement recommendations, and a canonical quiz ensuring 100% factual alignment. Demo targets a ≥60% reduction in orientation time (Baseline 56h → Tool 20h) with zero tolerance for quiz inaccuracies.

## 2. Why It Matters
Large programs suffer onboarding drag and context decay. New contributors become busy yet misaligned. POI Compass accelerates time-to-context and provides measurable compression, improving early productivity and leadership confidence.

## 3. North Star Metric
**Orientation Compression (%)** = `(Baseline_Time - Tool_Time) / Baseline_Time * 100`  
Demo Example: `(56 - 20) / 56 * 100 = 64.29%` → PASS (≥60%).  
Supporting Metrics: Comprehension Score (quiz accuracy), Confidence Coverage (answers ≥0.85), Recommendation Accuracy.

## 4. Core Features (Implemented v1.0.4 + UI Scaffold)
| Feature | Endpoint | Description | UI Page |
|---------|----------|-------------|---------|
| Project Overview | `GET /overview` | Mission, problem, strategic summary | Overview |
| Org Explorer | `GET /org` | Hierarchical team + responsibilities | Org |
| Role Lookup | `GET /roles?query=` | Fuzzy responsibility search | Roles (search bar) |
| Q&A | `POST /qa` | Deterministic fact retrieval + confidence + fallback if <0.85 | (Planned UI Panel) |
| Recommendation Engine | `POST /recommendation` | Team placement + rationale scoring (role, overlap, need) | Recommendation |
| Canonical Quiz | `GET /quiz`, `POST /quiz/submit` | 15 questions, must be 100% accurate | Quiz |
| Metrics Dashboard | `GET /metrics` | Compression %, quiz accuracy, coverage | Metrics |
| Runtime Metrics (FR10) | `GET /internal/runtime-metrics` | p95 latency, counts, uptime (header‑protected) | Runtime Metrics |
| Audit Log (FR11) | JSONL file per request | Traceability of actions | (Download link future) |
| Gap Detection | `GET /gaps` | Simulated missing / stale fact(s) | Gaps (embedded on Overview) |
| Fallback Escalation | `POST /qa/fallback` | Escalation when confidence insufficient | (Auto-trigger planned) |

## 5. Demo Success Criteria (Zero Tolerance)
1. Compression ≥ 60%.  
2. Quiz Score = 15/15 (100%).  
3. All canonical Q&A answers confidence ≥ 0.85.  
Failure on any → demo goal not met.

## 6. Architecture Overview
Monolithic FastAPI backend + React frontend consuming REST endpoints over a mock data layer. Retrieval uses keyword overlap heuristic (upgrade path to embeddings). Recommendation engine rule-based with transparent scoring.

```plantuml
@startuml
skinparam componentStyle rectangle
[React Frontend] --> [FastAPI API]
[FastAPI API] --> [Retrieval Module]
[FastAPI API] --> [Recommendation Engine]
[FastAPI API] --> [Metrics Calculator]
[Retrieval Module] --> [Mock Data Store]
[Recommendation Engine] --> [Mock Data Store]
[Metrics Calculator] --> [Mock Data Store]
@enduml
```

## 7. Data Model (Mock)
Entities (stored as JSON / optional SQLite): `User`, `Team`, `ProjectFact`, `QuizQuestion`, `InteractionEvent`, `Recommendation`.
Example Team object:
```json
{
  "id": "T12",
  "name": "Identity & Access",
  "mission": "Secure authentication and authorization services",
  "responsibilities": ["SSO integration", "IAM policy reviews"],
  "parent_team_id": "T01"
}
```

docker compose up --build
## 8. Installation & Setup (Current Demo Stack)
Prerequisites: Python 3.11+, Node.js 18+, npm 9+, (Optional) Docker. Windows users: commands shown in bash—use Git Bash or adapt to PowerShell.

### Backend (FastAPI)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows Git Bash; or .venv/Scripts/activate
pip install -e .  # installs local package if setup present, else: pip install -r requirements.txt
pytest -q         # all tests (should pass)
uvicorn app.main:app --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```
Dev server proxy forwards API calls to `http://localhost:8000`.

### Concurrent Run (one‑liner suggestion)
Run backend in one terminal, frontend in another. Navigate to http://localhost:3000.

### Protected Runtime Metrics Endpoint
Add header when calling `/internal/runtime-metrics`:
```
X-Internal-Token: <INTERNAL_ACCESS_TOKEN>
```
If `INTERNAL_ACCESS_TOKEN` env var is unset, endpoint still works (demo mode). Set it for stricter demos.

### Environment Variables (.env)
```
# Feature flags (set to 1 to DISABLE)
REC_DISABLE=0
QUIZ_DISABLE=0

# Optional internal token
INTERNAL_ACCESS_TOKEN=changeme

# Reserved for future external AI providers
LLM_API_KEY=
EMBEDDING_API_KEY=
```

### Lint & Quality
```bash
ruff check .           # if ruff configured (Python)
mypy .                 # type checking
pytest -q              # backend tests
cd frontend && npm run lint && npm test -- --watchAll=false
```

### Docker (Optional Future)
`docker compose` definition pending; current Dockerfile (backend) can be built manually.

## 9. Testing (Implemented Set)
Current suite (non‑exhaustive) covers: quiz scoring, recommendation scoring & ordering, fallback escalation (<0.85), runtime metrics snapshot, audit log write, gap detection simulation, feature flag disable behavior, schema conformance.

Run everything:
```bash
pytest -q
```
Add new endpoint? Provide: unit test, (if applicable) integration test stub, and schema update.

## 10. AI Usage & Guardrails
Allowed: summary phrasing, rationale templates, quiz question refinement, alternative wording.  
Prohibited: real employee data, PHI, unlicensed external code, speculative facts.  
Confidence < 0.85 → fallback response: "Consult Mentor" (canonical dataset avoids triggering).  
Prompt templates versioned in `prompts.md`.

### Example Prompt (Overview Summarizer)
```
You are a technical product analyst. Using the mission:<mission_statement> and problem:<problem_statement> plus team count <team_count> and key responsibilities list <responsibilities_list> ... (see prompts.md)
```
More prompts: see `prompts.md`.

## 11. ADRs
- ADR 0001: Metric Choice & Baseline Simulation (`adr-0001-metric-choice.md`)
Future ADRs: Retrieval Upgrade, Data Ingestion Strategy, Access Control Model.

## 12. Roadmap (High-Level)
Phase 2: Real HRIS & ticketing ingestion.  
Phase 3: Adaptive learning paths + personalized gap analysis.  
Phase 4: Embeddings / semantic retrieval + calibrated confidence.  
Phase 5: Integration with time-to-first-productive-commit KPI.

## 13. Demo Scenario Narrative & UI Flow
"New hire joins a sprawling program. Previously took a week of scattered chats and doc spelunking. With POI Compass: overview (2 min), org exploration (3 min), quiz (100% in 4 min), team recommendation with rationale—orientation compressed to under half-day equivalent."  
Visual: Metrics dashboard bar (Baseline 56h vs Tool 20h) + quiz completion badge.

### Live Click Path (Prototype)
1. Overview → skim mission/problem; note gaps badge.
2. Org → expand teams; inspect responsibilities.
3. Roles → search keyword (e.g., "auth") to validate discoverability.
4. Quiz → answer deterministic questions (all visible in code for demo) → submit.
5. Recommendation → view top 3 teams with score breakdown (role_match / overlap / need).
6. Metrics → confirm compression %, coverage, quiz accuracy.
7. Runtime Metrics → (optional) show p95 latencies; refresh after traffic.

See `docs/UI_MOCKUPS.md` for wireframes & persona overlays.

## 14. Known Limitations / Open Items
- Baseline time simulated; real-world recalibration needed.
- Heuristic retrieval may mis-rank semantically similar phrasing.
- Rule-based recommendations lack dynamic skill inference (skills inventory pending).
- No real authentication / RBAC; internal token is coarse.
- Scaling model (500 concurrent) not stress-validated beyond synthetic smoke.
- Frontend lacks dedicated Q&A interactive panel (coming).
- Accessibility automation minimal (need jest-axe or pa11y pipeline).

## 15. Data Privacy & Compliance (Forward-Looking)
Demo excludes PHI and personal identifiers. Future phases will incorporate HIPAA review, RBAC, audit logging, and encryption at rest for sensitive metadata.

## 16. Contribution Policy
Internal use only; external contributions disabled. New decisions require ADR with: Context, Options, Decision, Consequences, Review Date.

## 17. Traceability
Canonical quiz questions map directly to `ProjectFact` IDs; tests will enforce deterministic linkage. Full matrix in `prd.md`.

## 18. Glossary (Excerpt)
- Canonical Fact: Authoritative statement forming quiz & Q&A basis.
- Orientation Compression: % reduction in time to validated project understanding.
- Confidence Coverage: Portion of answers above heuristic threshold.

## 19. Resources
| Artifact | Purpose |
|----------|---------|
| `prd.md` | Detailed product specification & acceptance criteria |
| `prompts.md` | Versioned AI prompt library |
| `adr-0001-metric-choice.md` | Metric selection rationale |
| `CAPSTONE_README.md` | Archived original capstone instructions |

## 20. License
Internal Use Only – Not for external distribution.

## 21. Status & Revision
| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2025-11-05 | Initial project README creation |
| 1.0.4 | 2025-11-06 | Backend FR1–FR11 complete (runtime metrics, audit) |
| 1.0.5 | 2025-11-06 | React UI scaffold, lint config, updated docs |

---
For deeper context: consult `prd.md`. For prompt updates: amend `prompts.md` and increment version header.
