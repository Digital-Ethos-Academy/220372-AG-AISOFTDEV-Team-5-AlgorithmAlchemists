"""Recommendation engine module (rule-based placeholder)."""
from __future__ import annotations

from typing import List
from app.models import RecommendationBreakdown, RecommendationResponse, TeamModel


def recommend_for_user(user_id: str, teams: List[TeamModel]) -> RecommendationResponse:
    selected = teams[0]
    breakdown = [
        RecommendationBreakdown(factor="role_match", weight=50, description="General alignment"),
        RecommendationBreakdown(factor="responsibility_overlap", weight=30, description="API focus"),
        RecommendationBreakdown(factor="need_score", weight=20, description="Vacancy simulation"),
    ]
    return RecommendationResponse(
        selected_team_id=selected.id,
        confidence=0.9,
        rationale=f"User {user_id} aligned to {selected.name} due to API ownership",
        explanation_breakdown=breakdown,
        tie_break=None,
    )