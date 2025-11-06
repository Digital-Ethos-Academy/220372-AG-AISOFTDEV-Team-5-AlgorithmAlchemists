import json
from pathlib import Path

from app.recommendation_engine import score_candidates

GOLDEN = Path("data/golden/recommendation_tie.json")


def test_recommendation_tie_golden():
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    candidates = score_candidates(data["user"], data["candidates"])
    top = candidates[0]
    expected = data["expected"]
    assert top["team_id"] == expected["selected_team_id"], "Tie-break selection mismatch"
    # Confidence derived from total/100
    confidence = min(top["total"] / 100.0, 1.0)
    assert confidence == expected["confidence"]
