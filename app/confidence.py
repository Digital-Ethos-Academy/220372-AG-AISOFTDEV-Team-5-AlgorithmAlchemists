"""Confidence fallback helper utilities.

Provides a consistent escalation JSON when model-derived confidence scores
fall below the required threshold (default 0.85).
"""
from __future__ import annotations

from typing import Any, Dict

THRESHOLD = 0.85


def evaluate_confidence(confidence: float, context: Dict[str, Any]) -> Dict[str, Any]:
    """Return either a pass structure or escalation suggestion.

    Parameters
    ----------
    confidence: float
        Model or heuristic confidence score in [0, 1] (may exceed 1 if upstream total > 100; clamp applied).
    context: Dict[str, Any]
        Supplemental context such as entity id, operation or question.

    Returns
    -------
    Dict[str, Any]
        If confidence >= THRESHOLD: {"status": "ok", "confidence": <float>, **context}
        Else escalation envelope:
                {
                    "status": "escalate",
                    "confidence": <float>,
                    "next_action": "Consult Mentor",
                    "reason": "Confidence below threshold 0.85",
          "trace_id": context.get("trace_id"),
          "context": { ... filtered context ... }
        }
    """
    # Clamp for any accidental upstream scoring > 1
    safe_conf = round(min(max(confidence, 0.0), 1.0), 4)
    if safe_conf >= THRESHOLD:
        return {"status": "ok", "confidence": safe_conf, **context}
    filtered_ctx = {k: v for k, v in context.items() if k not in {"sensitive", "secret"}}
    return {
        "status": "escalate",
        "confidence": safe_conf,
        "next_action": "Consult Mentor",
        "reason": f"Confidence below threshold {THRESHOLD}",
        "trace_id": context.get("trace_id"),
        "context": filtered_ctx,
    }
