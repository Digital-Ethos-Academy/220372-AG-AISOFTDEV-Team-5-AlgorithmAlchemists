"""Recommendation engine module (rule-based placeholder)."""
from __future__ import annotations

from typing import List, Tuple, Optional
from app.models import RecommendationBreakdown, RecommendationResponse, TeamModel

class UserContext:
    def __init__(self, user_id: str, role: str = "Generalist", tenure_days: int = 0, activity_state: str = "active") -> None:
        self.user_id = user_id
        self.role = role
        self.tenure_days = tenure_days
        self.activity_state = activity_state

DESIRED_RESPONSIBILITIES = {"API", "Docs"}


def _score_team(team: TeamModel, user: UserContext) -> Tuple[int, List[RecommendationBreakdown]]:
    overlap = len(DESIRED_RESPONSIBILITIES.intersection(set(team.responsibilities)))
    responsibility_overlap_score = int((overlap / len(DESIRED_RESPONSIBILITIES)) * 30)
    # role match boosted if any responsibility token appears in user role
    role_match = any(r.lower() in user.role.lower() for r in team.responsibilities)
    role_match_score = 50 if role_match else 30
    # tenure: prefer earlier tenure to teams with docs (simulate onboarding friendly)
    tenure_bonus = 5 if user.tenure_days < 30 and "Docs" in team.responsibilities else 0
    # activity state influence
    activity_modifier = 5 if user.activity_state == "drifting" else 0
    need_score = 15 + activity_modifier  # base plus possible modifier
    total = role_match_score + responsibility_overlap_score + need_score + tenure_bonus
    breakdown = [
        RecommendationBreakdown(factor="role_match", weight=role_match_score, description="Role to responsibility alignment"),
        RecommendationBreakdown(factor="responsibility_overlap", weight=responsibility_overlap_score, description="Overlap with API/Docs"),
        RecommendationBreakdown(factor="need_score", weight=need_score, description="Simulated vacancy & activity adjustment"),
        RecommendationBreakdown(factor="tenure_bonus", weight=tenure_bonus, description="Early tenure docs preference"),
    ]
    return total, breakdown


def recommend_for_user(user_id: str, teams: List[TeamModel], user: Optional[UserContext] = None) -> RecommendationResponse:
    user_ctx = user or UserContext(user_id=user_id)
    scored = [(team, *_score_team(team, user_ctx)) for team in teams]
    # sort by total descending
    scored.sort(key=lambda t: t[1], reverse=True)
    selected, total_score, breakdown = scored[0]
    # Cap theoretical max at 100 for normalization
    confidence = round(min(total_score, 100) / 100, 2)
    return RecommendationResponse(
        selected_team_id=selected.id,
        confidence=confidence,
        rationale=f"User {user_id} aligned to {selected.name} (score {total_score})",
        explanation_breakdown=breakdown,
        tie_break=None,
    )

def debug_candidates(user_id: str, teams: List[TeamModel], user: Optional[UserContext] = None):
    user_ctx = user or UserContext(user_id=user_id)
    out = []
    for team in teams:
        total, breakdown = _score_team(team, user_ctx)
        out.append({
            "team_id": team.id,
            "total": total,
            "confidence": round(min(total,100)/100, 2),
            "breakdown": [b.model_dump() for b in breakdown],
        })
    out.sort(key=lambda x: x["total"], reverse=True)
    return out