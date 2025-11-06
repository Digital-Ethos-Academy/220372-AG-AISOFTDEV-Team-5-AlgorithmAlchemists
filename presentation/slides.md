---
# Algorithm Alchemists
## Adaptive Role Gap Intelligence & Confidence Scoring
Tagline: Compressing workforce skill gap analysis from 56h to 20h (64% faster) with transparent AI confidence.
Audience: Mixed (technical + leadership + product)
Format: Minimal, high-signal, accessible.
---
## 1. Problem & Opportunity
- Manual role/skill gap assessments: fragmented spreadsheets & subjective scoring
- Slow cycle: ~56 hours elapsed per full analysis round (baseline)
- Low confidence: opaque logic → stakeholder hesitation
- Opportunity: Accelerate + add trustworthy, explainable metrics
---
## 2. Solution Overview
- FastAPI backend + React frontend delivering role gap, quiz, recommendation & metrics endpoints
- Confidence & recommendation engines (deterministic, auditable)
- Mutation-tested core logic (infrastructure stable; quality baseline established)
- Resource governance: schemas/, data golden fixtures, prompt versioning
- Outcome: 56h → 20h process time (64% reduction); structured confidence output
---
## 3. Architecture & Data Flow
```
[User Browser]
    ↓ (HTTPS)
[React Pages]
 Overview | Roles | Quiz | Recommendation | Metrics
    ↓ API calls
[FastAPI Service]
 Endpoints: /overview /roles /quiz /recommendation /metrics /runtime_metrics
    ↓ internal modules
[confidence.py]   [recommendation_engine.py]
    ↓ schemas validation (schemas/)
[data/golden fixtures]
    ↘ audit log (trace_id, latency, confidence)
[Mutation Pipeline]
  docker_entrypoint.sh → mutmut (356 mutants) → results artifact
```
- Determinism: global seed, frozen timestamps
- Governance: prompt versioning & audit schema alignment
---
## 4. Metrics & Validation
- Time Compression: 56h baseline → 20h optimized (∆ = 36h saved | 64%)
```
Time (h)
56 |████████████████████████████████████████████|
20 |███████████████                             |
```
- Tests: 42 passing unit/integration (baseline gate green)
- Mutation Testing: 356 mutants total
  - Killed: 221 (62.1%)
  - Survived: 123 (34.6%)
  - Pending (no tests): remainder lines flagged
- Interpretation: Infrastructure robust; targeted logic hard-to-kill → post-demo refinement
---
## 5. Live Demo Flow (Static Deck Guidance)
1. Landing (Overview) – brief mission & metric banner (64% faster)
2. Roles & Gaps – show structured gap schema
3. Quiz Submission – trigger loading skeleton → result
4. Recommendation View – score breakdown (bars/badges) + confidence explanation
5. Metrics Panel – latency & compression figure
6. Mutation Summary – show killed vs survived (#221 / #123) transparency
---
## 6. Quality, Governance & Accessibility
- No secrets in code; env var placeholders only
- Prompt governance: versioned .prompt.md, rationale for high-risk
- Audit logging: ts, trace_id, user_id, path, latency_ms, confidence
- Security: no hardcoded tokens; approved license enforcement (MIT/Apache/BSD/ISC)
- Accessibility: semantic headings, aria-labels, high contrast (≥ 4.5:1), keyboard focus ring, planned skip link
- Determinism: seeded tests & frozen time
---
## 7. Roadmap & Wow Factor
Near-Term Enhancements (pre/post demo):
- Score Breakdown Component (horizontal bars / badges with aria-label)
- Loading Skeletons (quiz submit, recommendation generation)
- Targeted Tests: kill top 10 surviving mutants (confidence & recommendation branches)
- Dark / High-Contrast Toggle
- Animated Confidence Trend (ASCII or lightweight SVG)
- Post-Demo: reduce survivors <15% threshold; expand audit analytics
---
## 8. Call to Action
- Adopt for pilot role analysis next sprint
- Provide 3 sample role profiles for rapid ingestion
- Feedback on confidence thresholds to tune early wins
"Turning scattered skill data into actionable, explainable intelligence." 
---
## Pitch (60–90 sec Script)
Organizations waste days consolidating spreadsheets and subjective opinions to understand role skill gaps. Algorithm Alchemists compresses that cycle from fifty-six hours to twenty by combining a FastAPI backend, a React experience layer, and deterministic confidence and recommendation engines. Every response is schema-validated, audited with trace IDs, and mutation-tested for resilience: we generated 356 code mutants and killed over sixty percent, transparently reporting survivors for post-demo improvement. The result is faster insight you can trust—clear role gap mapping, explainable recommendation scores, and measurable time savings. Today we’ll walk through the optimized flow, highlight the metrics behind the 64% compression, and show where we’re heading—visual score breakdowns, accessibility refinements, and continued test hardening. After the demo, we invite you to pilot with three real roles so we can tune confidence thresholds and accelerate adoption. This is explainable intelligence for workforce upskilling—efficient, governed, and ready to expand.
---
## Design & Export Notes
- Minimal Theme: light background (#FFFFFF), primary text #1A1A1A, accent #005BBB (contrast OK), secondary accent #FFB400 for highlight bars.
- Fonts: System sans (Segoe UI / Arial) for accessibility & performance.
- Slide Separation: Markdown `---` compatible with Marp / Reveal / Deckset.
- Export Options:
  - Marp CLI: `marp presentation/slides.md --html --output presentation/slides.html`
  - PDF: `marp presentation/slides.md --pdf --output presentation/slides.pdf`
- Alt Text: ASCII diagram describes flow; add `alt="System architecture data flow"` if converting to HTML.
- Accessibility Checklist: ensure focus order: Nav → Skip Link → Main content; add `role="progressbar"` with `aria-valuenow` for score bars.
---
## Optional Wow Factor Implementation Targets
- Animated ASCII confidence evolution (precomputed frames) in terminal demo
- Real-time mutation snippet: show top 3 surviving mutant diffs (read-only) for transparency
- Quick toggle: high-contrast mode button (`aria-pressed` stateful)
---
## Appendix: Mutation Glossary (For Mixed Audience)
- Mutant: an auto-generated small code change
- Killed: existing test caught behavioral change
- Survived: test suite missed it (potential blind spot)
- Value: exposes silent gaps early → increases trust in recommendations
---
