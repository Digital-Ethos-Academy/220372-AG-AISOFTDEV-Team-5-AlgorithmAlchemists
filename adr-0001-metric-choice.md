# ADR 0001: Metric Choice & Baseline Simulation

## Status
Accepted (Draft demo scope)

## Context
We must show measurable, high-impact productivity improvement for a 500-person project with limited access to real operational data. Stakeholders desire a credible, quantifiable orientation improvement with near-zero tolerance for failure in the demo. Real systems (HRIS, ticketing) are unavailable; mock data will be used.

Multiple candidate metrics were considered:
1. Orientation Compression (time reduction)
2. Context Retention Rate (accuracy after delay)
3. Org Navigation Efficiency (click reduction)
4. Engagement Lift (interaction count increase)
5. Misalignment Incident Reduction (ticket routing errors)

Constraints:
- Must be demonstrable in 6–8 human hours.
- Deterministic and reproducible with mock data.
- Easily explainable to senior leaders.

## Decision
Adopt Orientation Compression as North Star metric with supporting Comprehension Score and Confidence Coverage. Baseline orientation duration set to 56 working hours (7 days) derived from assumed manual multi-step workflow. Target demo reduction ≥ 60% (≤ 22.4 hours equivalent) with 100% factual quiz accuracy (15 canonical questions).

## Rationale
- Time-based outcomes resonate with leadership and productivity framing.
- Straightforward formula and simulation; avoids ambiguous interpretations.
- Combines well with accuracy gating to avoid superficial gains.
- Other metrics (misrouted tickets, engagement) depend on real telemetry not currently available.

## Consequences
Positive:
- Clear narrative: "From 7 days to under 3 days." Easy to visualize.
- Enables deterministic automated test harness.
Negative:
- Real baseline may diverge from assumed numbers; requires recalibration post-integration.
- Risk stakeholders challenge assumption validity.

## Alternatives Considered
- Context Retention Rate: Harder without real delayed observation.
- Org Navigation Efficiency: Requires interaction telemetry instrumentation.
- Misalignment Incident Reduction: Needs actual ticketing history.

## Implementation Notes
- Baseline simulation defined in PRD Appendix A.
- Metrics service calculates compression on startup.
- Quiz engine ensures 100% canonical accuracy.

## Risk Mitigation
- Explicit assumptions documented (PRD Assumptions A1–A6).
- Future re-validation planned once real data ingestion available.

## Review Date
Revisit after Phase 2 (real data integration) or within 60 days of initial demo.

## Tags
Metric, Orientation, Productivity, Baseline Simulation
