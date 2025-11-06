# POIT Demo Walkthrough (≤10 Minutes)

Source Reference: See `prd.md` (version 1.0.4) for rationale, metrics, and acceptance criteria.
Environment: Docker Compose (backend FastAPI) + local React dev server + Storybook.
Goal: Demonstrate orientation compression, 100% quiz accuracy, confidence coverage, recommendation rationale, gaps detection, and observability (trace & error panels).

---
## 0. Prerequisites
- Docker & Docker Compose v2
- Node >= 18, npm installed
- Python (optional only if running tests locally)
- Sanitized `.env` already present (placeholders; no real secrets). If not:
  - Copy `.env.example` → `.env` and set `FORCE_RESEED=1`, `ADMIN_API_KEY=demo-admin`, `INTERNAL_ACCESS_TOKEN=internal-demo`.

## 1. Start Backend via Docker Compose
```bash
# From repo root
docker compose build --pull
docker compose up -d
# Verify health
docker compose ps
```
Expected: `poi-app` healthy (Health starts after seed). Health endpoint returns `{status: "ok"}`.

## 2. Start Frontend Dev Server
```bash
cd frontend
npm install --no-fund --no-audit
npm start
```
Browser: Open http://localhost:3000 (Firefox preferred).
Proxy redirects API calls to backend at :8000.

## 3. (Parallel) Start Storybook for UI Showcases
```bash
cd frontend
npm run storybook
```
Open http://localhost:6006 to show isolated components (ProviderStatus, HealthIndicator, ErrorBanner, TracePanel) if needed.

## 4. Overview Page
Navigate to `/`.
- Confirm Mission, Problem, Value, Team Count.
- Verify Seed Integrity badge shows "Healthy".
- HealthIndicator displays API ✓ and version.
- ProviderStatus shows all placeholders enabled.
- Gaps panel lists at least 1 simulated gap.
Acceptance criteria: FR1 + seed health visual + gap presence.

## 5. Org Explorer (`/org`)
- Hierarchical team list (≥10 teams). Parent relationship visible (T1 root).
Acceptance: FR2 satisfied.

## 6. Roles Lookup (`/roles`)
- Enter query: `Team 3` → results include Team 3 with score 1.0.
- Enter partial: `Team` → multiple matches (scores ≥0.5).
Acceptance: FR3 satisfied.

## 7. Quiz Flow (`/quiz`)
- 15 canonical questions load (skeletons minimal if delay).
- Submit answers (demo form: IDs aggregated). Score must return 15/15.
Acceptance: FR6 (100% correctness) + PRD zero tolerance accuracy.

## 8. Metrics Dashboard (`/metrics`)
- Shows baseline_hours=56, tool_hours≈20, compression_pct ≥60%, quiz_accuracy=1.0, confidence_coverage ≥0.98.
Acceptance: FR7 + North Star compression criteria.

## 9. Q&A (`/qa`)
- Ask canonical fact question: "What does Team 1 own?" → Answer sourced; confidence ≥0.85.
- Simulate low confidence: ask a vague question "misc"; if <0.85, fallback banner appears with escalation suggestion.
Features: Request cancellation (rapid second submit); skeleton shows while loading; ErrorBanner stays empty if success.
Acceptance: FR4 + FR9 (fallback on low confidence).

## 10. Recommendation (`/recommendation`)
- Enter user id: `u2` (drifting) → Recommendation returned with `selected_team_id`, confidence, rationale & explanation breakdown.
- Observe TracePanel: latest request shows latency and trace_id.
Acceptance: FR5 + rationale transparency.

## 11. Admin Page (`/admin`)
- Enter admin token: `demo-admin` (matches `ADMIN_API_KEY`).
- Load data: Teams, Facts, Quiz Questions lists populate.
- Create new Team (e.g. ID `TX`), appears instantly.
- Delete Team `TX` (confirmation modal). Team removed.
- Attempt unauthorized change: Clear admin token, reload → ErrorBanner shows structured error; trace recorded.
Security demonstration: token gating & dismissal of errors.

## 12. Runtime Metrics (`/runtime`)
- (If internal token required) Provide `internal-demo` in localStorage as `internalToken` (DevTools > Console):
  ```js
  localStorage.setItem('internalToken','internal-demo')
  ```
- Navigate `/runtime` to display per-endpoint counters & latency aggregates.
Acceptance: FR10 (snapshot metrics) & observability.

## 13. Gaps Validation (`/` again)
- Point out simulated gap (e.g. missing mission). Connect to PRD FR8 (gap detection) and persona "Knowledge Curator".

## 14. Observability & Resilience
- Open TracePanel (toggle): review recent requests (status codes, latency_ms, trace_id).
- Trigger controlled error (clear token on admin then load) → ErrorBanner collects structured error (error_code, status, trace_id).
- Show retry logic: temporarily disable network (Firefox DevTools) then reload Gaps panel; first failure, automatic single retry.

## 15. Storybook Spotlight (Optional ≤1 min)
- In Storybook, open ProviderStatus story to illustrate component isolation and consistent tokens (contrast & accessibility).

## 16. Cleanup
```bash
# Stop services
docker compose down --remove-orphans
# Remove local database (optional reset)
rm -f poit.db
# Clear tokens
localStorage.clear()
```

## 17. Key Talking Points Mapping (PRD)
- Orientation Compression (Metrics page) → PRD §3 & §26.
- Confidence Coverage (Metrics + Q&A) → PRD §3.2 & §13.
- Recommendation Transparency → PRD §12 & scoring schema.
- Quiz Determinism → PRD §14 (canonical + 100% accuracy).
- Gap Detection & Data Integrity → PRD §8 (FR8) & persona alignment.
- Observability (Trace IDs, Error Banner, Runtime Metrics) → PRD §§34, 36.
- Seed Integrity + FORCE_RESEED → Reliability & deterministic startup.

## 18. Timeboxing Template
| Segment | Target Time |
|---------|------------|
| Setup (compose + npm) | 2:00 |
| Overview + Org + Roles | 2:00 |
| Quiz + Metrics | 2:00 |
| Q&A + Recommendation | 1:30 |
| Admin + Runtime Metrics | 1:30 |
| Observability & Wrap | 1:00 |
Total ≤ 10:00 minutes.

## 19. Demo Success Criteria Quick Checklist
- Compression ≥ 60% (Metrics) ✅
- Quiz 15/15 ✅
- Q&A canonical answer ≥ 0.85 confidence ✅
- Fallback path triggers on low-confidence ✅
- Recommendation rationale shows breakdown ✅
- Gap list present ✅
- TracePanel latency + trace_id visible ✅
- ErrorBanner captures structured error (unauthorized admin) ✅
- Seed Integrity badge = Healthy ✅

## 20. Risks & Disclaimers
- All data mock (see PRD §7 assumptions & §18 guardrails).
- Recommendation deterministic; not ML-based yet.
- Provider keys placeholders: functionality limited to status display.
- Security model: token gating only; no full RBAC in demo.

## 21. Follow-Up (Post-Demo)
- Replace mock dataset with real onboarding metrics (PRD §24 roadmap).
- Add embeddings for semantic Q&A (PRD §24 Phase 2).
- Harden license allowlist & pre-commit compliance before broader sharing.

---
Prepared for concise, reproducible orientation compression demonstration aligned with PRD v1.0.4.
