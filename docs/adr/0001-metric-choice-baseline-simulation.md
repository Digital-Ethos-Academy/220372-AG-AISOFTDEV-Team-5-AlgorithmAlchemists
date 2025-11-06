# ADR 0001: Metric Choice & Baseline Simulation

Status: Accepted
Date: 2025-11-05
Decision Makers: Product, Engineering Lead, Data Engineer

## Context
Orientation clarity must be measured prior to real data integration. We require a deterministic baseline and a compressible target metric for demo validation.

## Decision
Adopt "Onboarding Orientation Compression" as the North Star metric: percentage reduction in hours required to reach full recall of canonical project facts and organizational structure.

Baseline (A1) fixed at 56 working hours (7 days * 8h) representing typical enterprise ramp. Tool target demo value: 20 hours (≥60% compression). Long-term stretch: ≤ 16.8 hours (≥70%).

## Rationale
* Simple to explain to stakeholders.
* Directly tied to productivity and value realization.
* Deterministic simulation prevents noisy early measurements.

## Consequences
* Must clearly label simulation; real measurement pipeline needed post integrations (HRIS, Slack, Jira).
* Risk of misrepresentation if actual baseline deviates; mitigation via future empirical study issue.
* Drives engineering prioritization toward clarity endpoints and quiz accuracy.

## Alternatives Considered
| Option | Pro | Con |
|--------|-----|-----|
| Time-to-first-commit | Direct developer output measure | Hard to attribute to orientation exclusively |
| Number of clarification tickets | Operational friction view | Requires ticket system integration (out-of-scope) |
| Self-assessed confidence survey | Qualitative nuance | Subjective; harder to automate |

## Validation Plan
* Provide static metrics via `/metrics` endpoint.
* Ensure quiz accuracy = 100% in demo dataset.
* Future ADR will refine metric using real interaction telemetry.

## Follow-ups
1. Issue: Empirical baseline study after SSO/HRIS integration.
2. Issue: Add telemetry schema for orientation steps.
