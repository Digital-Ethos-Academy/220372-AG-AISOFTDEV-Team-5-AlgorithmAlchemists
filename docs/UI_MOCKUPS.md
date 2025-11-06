# POI Compass UI Mockups & Interaction Notes

Version: 0.1 (increment when altering structural layout)
Status: Prototype reference (not pixel-perfect)

## Legend
- [A] Primary Action / Button
- [C] Content Panel
- [M] Metrics / Status Widget
- [N] Navigation
- [S] Search / Input
- [T] Table / Structured Data
- (*) Conditional / Future element

Monospace ASCII approximations emphasize layout zones & information hierarchy. Color, spacing, and responsive breakpoints to be refined in a design system phase.

---
## Global Frame
```
+--------------------------------------------------------------------------------+
| POI Compass                              | Metrics | Runtime Metrics |  Quiz  |
+--------------------------------------------------------------------------------+
|                                                                              |
| <Route Content>                                                               |
|                                                                              |
+--------------------------------------------------------------------------------+
| © 2025 Orientation Intelligence (internal)                                    |
+--------------------------------------------------------------------------------+
```
Navigation is keyboard reachable (tab order left→right). Future: add skip link ("Skip to main content").

---
## 1. Overview Page
```
+--------------------------------------------------------------------------------+
| [N] Overview | Org | Roles | Quiz | Recommendation | Metrics | Runtime Metrics |
+--------------------------------------------------------------------------------+
| Mission: Accelerate orientation & eliminate context drift.                    |
| Problem: New contributors spend 56h to reach confident baseline.             |
|                                                                              |
| [C] Key Facts (grid)                                                          |
|  - Teams: 12                  - Canonical Facts: 45                           |
|  - Avg Onboard Time: 56h      - Target Time: 20h                              |
|                                                                              |
| [M] Orientation Compression: 64.3%  (Bar ████████████░░░ )                    |
| [M] Quiz Accuracy: 100%  | Confidence Coverage: 92%                          |
|                                                                              |
| Gaps Detected: 1  -> [View Gap Details]                                       |
|  * Missing canonical fact: 'Third-party risk intake SLA'                     |
+--------------------------------------------------------------------------------+
```
Keyboard Focus Order: Nav → Mission → Problem → Key Facts → Compression bar → Gap link.

---
## 2. Org Page
```
+--------------------------------------------------------------------------------+
| Org Explorer                                                                  |
+--------------------------------------------------------------------------------+
| [S] Filter teams: [ auth             ] (Enter filters by substring)           |
|                                                                              |
| [T] Teams Hierarchy                                                           |
|  - Platform (T01)                                                             |
|     - Identity & Access (T12)  (Responsibilities: SSO integration, IAM policy)|
|     - Observability (T13)                                                     |
|  - Product (T02)                                                              |
|     - Payments (T21)                                                          |
|     - Pricing (T22)                                                           |
|                                                                              |
| (Future: Expand/Collapse all, ARIA tree roles)                                |
+--------------------------------------------------------------------------------+
```
Accessibility: Table replaced later by semantic tree with role="tree"/"treeitem".

---
## 3. Roles Page
```
+--------------------------------------------------------------------------------+
| Role Responsibility Lookup                                                    |
+--------------------------------------------------------------------------------+
| [S] Search responsibilities: [ identity provisioning             ] [Search]   |
|                                                                              |
| Results (3):                                                                  |
| 1. Identity & Access Engineer  | Key: "SSO integration", "Provisioning"      |
| 2. Platform Security Lead      | Key: "IAM policy"                           |
| 3. Compliance Analyst (*)      | Key: "Access review" (simulated future)     |
|                                                                              |
| (Confidence heuristics optional future column)                                |
+--------------------------------------------------------------------------------+
```
Edge Cases: Empty results → non-intrusive message with guidance.

---
## 4. Quiz Page
```
+--------------------------------------------------------------------------------+
| Canonical Quiz (All questions required – goal 100% accuracy)                  |
+--------------------------------------------------------------------------------+
| Q1. What is the primary mission?                                              |
|    [___________________________]                                              |
| Q2. Which team owns SSO integration?                                          |
|    [___________________________]                                              |
| ...                                                                           |
| Q15. (Final)                                                                  |
|                                                                              |
| [A] Submit Answers  |  Progress: 15 / 15 answered ✓                           |
|                                                                              |
| After submit: [Result Badge: PERFECT SCORE]  | Time: 3m 42s                   |
+--------------------------------------------------------------------------------+
```
Validation: Inline required; final submission disabled until all filled.

---
## 5. Recommendation Page
```
+--------------------------------------------------------------------------------+
| Team Placement Recommendation                                                 |
+--------------------------------------------------------------------------------+
| Candidate Profile (input placeholder)                                         |
|  - Desired impact: Authentication scaling                                    |
|  - Skills: Go, OAuth2, Policy modeling                                        |
|                                                                              |
| Top Matches:                                                                  |
| 1. Identity & Access (Score 91, Confidence 0.91)                               |
|    Breakdown: role_match 50 | overlap 25 | need 16                             |
|    Rationale: Strong alignment with SSO/OAuth roadmap.                        |
|                                                                              |
| 2. Platform Security (Score 74, Confidence 0.74)                              |
| 3. Observability (Score 52, Confidence 0.52)                                  |
|                                                                              |
| (Future: Action buttons: Request Intro, View Charter)                        |
+--------------------------------------------------------------------------------+
```
Sorting: Desc by total score, deterministic tie-breaker by team name.

---
## 6. Metrics Page
```
+--------------------------------------------------------------------------------+
| Metrics & Outcomes                                                            |
+--------------------------------------------------------------------------------+
| Orientation Compression                                                       |
|  Baseline 56h | Tool 20h  -> 64.3% (Target ≥ 60%)                             |
|  [██████████████████░░░]                                                      |
|                                                                              |
| Quiz Accuracy: 100%  | Confidence Coverage: 92%                               |
| Recommendation Top-1 Precision: (placeholder)                                 |
|                                                                              |
| (Future: Sparkline of latency, adoption funnel)                               |
+--------------------------------------------------------------------------------+
```
Performance: Keep initial payload <10KB JSON.

---
## 7. Runtime Metrics Page
```
+--------------------------------------------------------------------------------+
| Internal Runtime Metrics (Demo)                                              |
+--------------------------------------------------------------------------------+
| Uptime: 0h 12m 05s                                                           |
| Requests: total=148  | distinct endpoints=9                                  |
|                                                                              |
| Endpoint Latencies (p95 ms)                                                  |
|  /overview ............. 12                                                  |
|  /org .................. 15                                                  |
|  /recommendation ....... 38                                                  |
|  /qa ................... 42                                                  |
|  /quiz/submit .......... 20                                                  |
|                                                                              |
| (Auto-refresh toggle *)                                                      |
+--------------------------------------------------------------------------------+
```
Security: Header gate with `X-Internal-Token` when configured.

---
## 8. Fallback Escalation (Flow Sketch)
```
User enters Q&A query -> Retrieval heuristic scores tokens.
If confidence >= 0.85: show answer (green badge) + rationale snippet.
Else: auto POST /qa/fallback -> Show advisory panel: "Consult Mentor" and log audit entry.
```
Future: Add CTA to capture clarification for improving fact base.

---
## Personas Overlay
- New Engineer: Prioritizes Overview → Org → Quiz → Recommendation.
- Engineering Manager: Org → Metrics → Gaps.
- Program Lead: Metrics → Runtime Metrics → Audit export.
- Knowledge Steward: Gaps → Quiz → Q&A low-confidence review.

---
## Accessibility Notes
- All nav items focus-visible outline retained.
- Color contrast target ≥ 4.5:1 (verify after theming tokens defined).
- Landmarks planned: <header>, <nav>, <main>, <footer> + skip link.
- Future automation: jest-axe integration; CI gate on critical violations.

---
## Future Enhancements (UI)
| Area | Enhancement | Rationale |
|------|-------------|-----------|
| Q&A Panel | Inline confidence badge & fallback escalation banner | Transparency & trust |
| Org Tree | ARIA tree roles, collapsible branches | Accessibility & scale |
| Recommendation | Skill input form + weight sliders | User control & experimentation |
| Metrics | Historical trend charts (sparklines) | Longitudinal improvement tracking |
| Audit | Download & filter by trace_id | Governance compliance |
| Theming | Tokenized design system (dark/light) | Consistent customization |

---
## Change Log (UI Document Only)
| Version | Date | Summary |
|---------|------|---------|
| 0.1 | 2025-11-06 | Initial ASCII mockups & interaction notes |

---
Questions / refinements: open an issue with label `ui` + include persona impact.
