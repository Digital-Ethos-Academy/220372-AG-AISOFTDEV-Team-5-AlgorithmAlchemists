import json
from pathlib import Path

GOLDEN = Path("data/golden/qa_high_confidence.json")


def test_qa_high_confidence_fixture():
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    # Fixture defines only a minimum confidence threshold expectation.
    assert "expected" in data
    assert data["expected"]["min_confidence"] >= 0.85
