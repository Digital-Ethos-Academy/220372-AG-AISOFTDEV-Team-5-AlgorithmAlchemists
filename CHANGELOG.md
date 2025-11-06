# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-11-05
### Added
- Initial PRD, governance expansion, integration roadmap, risk playbooks, traceability matrix.
- JSON Schemas for FR1-FR9 endpoints; Pydantic models; mock implementations.
- Prompt library scaffolding and agent execution checklist.
- Foundational test suite (schema + positive path).

### Security
- Secret governance placeholders, no real keys.

### Pending
- CI workflow, logging, Docker, performance harness (shipped in later versions).

## [1.0.1] - 2025-11-05
### Added
- CI pipeline: lint (ruff), type (mypy), security scans (bandit, pip-audit), coverage gate.
- ADR 0001 baseline metric choice; backlog & issue templates; branch protection doc.

## [1.0.2] - 2025-11-05
### Added
- Structured logging middleware (trace IDs), optional OpenTelemetry tracing.
- Dockerfile multi-stage build base.
- Performance harness (locust) & OpenAPI export script.
- Security exception register & SBOM generation.

## [1.0.3] - 2025-11-05
### Added
- Security headers middleware; standardized JSON error envelope.
- Feature flag system (REC_DISABLE, QUIZ_DISABLE) with negative tests.
- License scan integration.

## [1.0.4] - 2025-11-06
### Added
- Settings layer with dynamic env flags (observability, feature toggles, internal metrics).
- Audit logging middleware (JSONL) & internal runtime metrics endpoint (FR10, FR11).
- Modular recommendation engine with weighted scoring (role_match, responsibility_overlap, need_score).
- Nightly scheduled load test job in CI.
- QA confidence logic with automatic fallback escalation for low token overlap.
- Simulated gap detection (demo placeholder) and runtime/audit JSON Schemas.
- Enhanced structured logging (endpoint, success, confidence fields).
- Frontend React UI (Overview, Org, Roles, Quiz, Recommendation, Metrics, Runtime Metrics) with accessibility labels.
- Additional tests: internal runtime metrics, audit log write, QA fallback, gap simulation.

### Changed
- Recommendation endpoint now delegates to scoring engine, confidence derived from total score.
- QA endpoint now computes token overlap and escalates when confidence < 0.85.
- /gaps now returns a simulated gap item for demo realism.

### Security
- Optional internal token header check for /internal/runtime-metrics.

### Notes
- User, ProjectFact, and persistence layers deferred to post-demo (v1.0.5+).

## [1.0.5] - 2025-11-06
### Added
- Design token system (`tokens.css`) and documented palette, spacing, typography (`DESIGN_TOKENS.md`).
- Storybook scaffolding (React Webpack 5) with initial component/page stories.
- Component library primitives: `NavBar`, `PageShell`, `MetricsCard`, `ScoreBar`, `GapBadge`, `TeamTree`, `RecommendationList`.
- Playwright-based mockup screenshot pipeline (`mockups:screenshots`).
- Org Explorer upgraded to collapsible hierarchical tree (improved FR2 usability & accessibility).
- Recommendation page refactored to transparent factor breakdown (supports FR5 rationale clarity).

### Changed
- App layout refactored to consistent shell + sticky navigation for improved discoverability.
- Recommendation UI now surfaces weighted factors in structured grid.
- Org view replaced table with semantic tree & disclosure buttons.

### Planned (Not Yet Implemented in UI but scaffolded via stories roadmap)
- QA high vs low-confidence visual states / fallback panel.
- Quiz form improvement (inline validation, post-submit perfect state badge).
- Metrics dashboard card cluster and degraded coverage scenario.

### Tooling
- Added Storybook CRA preset for JSX transpilation and MDX docs.
- Added Playwright dependency for deterministic visual captures.

### Accessibility
- Tree view introduces keyboard-discoverable disclosure controls; focus outlines standardized via tokens.
- Future: add jest-axe checks & skip link.

### Notes
- Visual regression baseline to be established after adding remaining state stories.

## [1.0.6] - 2025-11-06
### Added
- New components: `QuizForm`, `QAResultPanel`, `MetricsDashboard` and supporting styles.
- Q&A page (`/qa`) with automated low-confidence fallback call (FR9 visualized).
- Metrics page refactored to card + bar dashboard.
- Org page tree and recommendation breakdown integrated into navigation shell.
- Storybook stories for QA high/low confidence, quiz placeholder, metrics/overview cluster.
- Extended screenshot capture script with QA stories.

### Changed
- Replaced legacy quiz checkbox form with token-based input form enabling inline validation.
- Navigation updated to include Q&A.

### Tooling
- Playwright capture list extended for new component states.

### Upcoming
- Add Roles search panel & runtime metrics table stories.
- Add degraded metrics scenario & quiz perfect score static story.

## [1.0.7] - 2025-11-06 (Unreleased)
### Added
- Storybook visual states: `RolesSearchPanel` (results, none), `RuntimeMetricsTable` (authorized snapshot, unauthorized), `MetricsDashboard` (healthy, degraded), `QuizForm` (perfect score, validation hints), `QAResultPanel` escalated no-answer variant.
- Metrics degradation scenario to support performance/coverage risk communication (FR observability alignment).

### Changed
- Expanded visual state coverage enabling comprehensive Playwright screenshot set for mockup embedding.

### Documentation
- Pending: regenerate screenshots and embed into `UI_MOCKUPS.md` replacing ASCII placeholders.

### Next
- Visual regression baseline commit after screenshot generation.
- Accessibility audit pass (axe) & skip link addition.
