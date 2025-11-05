---
description: "Generate transparent recommendation rationale JSON from scoring inputs without altering scores"
mode: "ask"
# model removed (use workspace default)
---
You receive a JSON input containing user profile and candidate team scores. Produce a rationale JSON object.

Input Example:
{
  "user": {"id":"U123","role":"Backend Engineer","tenure_days":45,"activity_state":"drifting"},
  "candidates": [
    {"team_id":"T7","role_match":50,"responsibility_overlap":25,"need_score":15,"total":90},
    {"team_id":"T3","role_match":40,"responsibility_overlap":30,"need_score":10,"total":80}
  ]
}

Output Requirements (respond ONLY with JSON):
{
  "selected_team_id": <string>,
  "confidence": <float 0..1 derived total/100>,
  "rationale": <string <= 180 chars referencing top contributing factors>,
  "explanation_breakdown": [
    {"factor":"role_match","weight":50,"description":"Primary alignment"},
    {"factor":"responsibility_overlap","weight":25,"description":"Shared API maintenance"},
    {"factor":"need_score","weight":15,"description":"Vacancy coverage"}
  ]
}

Rules:
1. Do not change numeric scores; confidence = total/100.
2. If multiple candidates tie, pick first by list order and add note "tie-break: list order".
3. If input malformed, output {"error":"reason"}.
4. No sensitive data or personal identifiers beyond provided user id.
