from app.confidence import THRESHOLD, evaluate_confidence


def test_confidence_ok():
    # Edge just above threshold
    edge = THRESHOLD + 0.01
    result = evaluate_confidence(edge, {"trace_id": "abc", "entity": "qa"})
    assert result["status"] == "ok"
    assert result["confidence"] == round(edge, 4)


def test_confidence_escalate():
    low = THRESHOLD - 0.01
    result = evaluate_confidence(low, {"trace_id": "t1", "entity": "qa"})
    assert result["status"] == "escalate"
    assert result["confidence"] == round(low, 4)
    assert "next_action" in result
    assert result["reason"].startswith("Confidence below threshold")
