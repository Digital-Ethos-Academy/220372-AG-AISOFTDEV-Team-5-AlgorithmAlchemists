import json
from pathlib import Path

SNAPSHOT = Path("data/golden/metrics_snapshot_basic.json")


def test_metrics_snapshot_basic():
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    assert "expected" in snap
    expected = snap["expected"]
    # Validate presence of core ratio metrics
    for key in ["baseline_hours", "tool_hours", "compression_pct", "quiz_accuracy", "confidence_coverage"]:
        assert key in expected, f"Missing expected metric '{key}'"
    assert 0 < expected["compression_pct"] <= 100
    assert expected["quiz_accuracy"] <= 1.0
