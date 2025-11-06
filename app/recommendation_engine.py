"""Recommendation engine module (rule-based placeholder)."""
from __future__ import annotations

from typing import List, Tuple
from app.models import RecommendationBreakdown, RecommendationResponse, TeamModel

DESIRED_RESPONSIBILITIES = {"API", "Docs"}


def _score_team(team: TeamModel) -> Tuple[int, List[RecommendationBreakdown]]:
    # Simple scoring: role_match always 50 for demo, overlap proportional up to 30, need_score static 20
    overlap = len(DESIRED_RESPONSIBILITIES.intersection(set(team.responsibilities)))
    responsibility_overlap_score = int((overlap / len(DESIRED_RESPONSIBILITIES)) * 30)
    role_match_score = 50  # placeholder until user role introduced
    need_score = 20  # static simulation
    total = role_match_score + responsibility_overlap_score + need_score
    breakdown = [
        RecommendationBreakdown(factor="role_match", weight=role_match_score, description="Demo static role alignment"),
        RecommendationBreakdown(factor="responsibility_overlap", weight=responsibility_overlap_score, description="Overlap with API/Docs"),
        RecommendationBreakdown(factor="need_score", weight=need_score, description="Simulated vacancy"),
    ]
    return total, breakdown


def recommend_for_user(user_id: str, teams: List[TeamModel]) -> RecommendationResponse:
    scored = [(team, *_score_team(team)) for team in teams]
    # sort by total descending
    scored.sort(key=lambda t: t[1], reverse=True)
    selected, total_score, breakdown = scored[0]
    confidence = round(total_score / 100, 2)
    return RecommendationResponse(
        selected_team_id=selected.id,
        confidence=confidence,
        rationale=f"User {user_id} aligned to {selected.name} (score {total_score})",
        explanation_breakdown=breakdown,
        tie_break=None,
    )