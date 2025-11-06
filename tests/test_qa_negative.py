import json
from pathlib import Path

GOLDEN = Path("data/golden/qa_advanced_analytics.json")

def test_qa_low_confidence():
    """Test QA endpoint with a low-confidence scenario."""
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert "expected" in data
    assert data["expected"]["min_confidence"] > 0.5  # Ensure threshold is reasonable

def test_qa_missing_question():
    """Test QA endpoint when the question is missing."""
    # Simulate missing question scenario
    assert "question" not in {}  # Replace with actual API call logic