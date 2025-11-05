---
description: "Identify gaps or outdated fields in team missions and responsibilities, output list of gap objects"
mode: "ask"
---
Input Context: current Team entities with fields: id, name, mission, responsibilities[], last_updated.

Output JSON Format:
{
  "gaps": [
    {"team_id": "T1", "type": "missing_mission", "detail": "Mission empty"},
    {"team_id": "T5", "type": "stale_responsibility", "detail": "Responsibility >180d old"}
  ],
  "summary": {
    "total_teams": <int>,
    "gap_count": <int>,
    "stale_threshold_days": 180
  }
}

Rules:
1. A mission is a gap if blank or < 10 chars.
2. A responsibility is stale if last_updated > 180 days ago (simulation: treat provided hint flag).
3. Do not propose new content—only flag issues.
4. If no gaps: {"gaps":[],"summary":{...}} still required.
