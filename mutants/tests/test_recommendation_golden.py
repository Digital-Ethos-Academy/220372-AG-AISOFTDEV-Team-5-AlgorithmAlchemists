import json
from pathlib import Path

from app.recommendation_engine import score_candidates  # assuming function exists; adjust if name differs

GOLDEN_PATH = Path("data/golden/recommendation_case1.json")


def test_recommendation_golden_case1():
    data = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    user = data["user"]
    candidates = data["candidates"]
    scored = score_candidates(user, candidates)  # expected to return list with 'total'
    assert scored, "No candidates scored"
    top = scored[0]
    expected = data["expected"]
    assert top["team_id"] == expected["selected_team_id"], "Top team mismatch"
    # Confidence defined as total/100; clamp above 1
    confidence = min(top["total"] / 100.0, 1.0)
    assert confidence == min(expected["confidence"], 1.0)
