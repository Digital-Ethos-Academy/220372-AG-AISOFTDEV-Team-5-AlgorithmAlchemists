from typing import List
from fastapi import FastAPI
import os

from app.models import (
    FallbackQAResponse,
    GapsResponse,
    GapsSummary,
    MetricsResponse,
    OrgResponse,
    OverviewResponse,
    QAResponse,
    QuizListResponse,
    QuizQuestionModel,
    QuizSubmitResponse,
    RecommendationBreakdown,
    RecommendationResponse,
    RolesLookupResponse,
    RolesMatch,
    TeamModel,
)

app = FastAPI(title="POI Compass API", version="1.0.0")

from app.observability import init_observability  # noqa E402

if os.getenv("POI_OBSERVABILITY", "1") == "1":  # enabled by default
    init_observability(app)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "version": "1.0.0"}

# Mock data (simplified)
TEAMS: List[TeamModel] = [
    TeamModel(id=f"T{i}", name=f"Team {i}", mission="Deliver quality features", responsibilities=["API", "Docs"], parent_team_id=None if i == 1 else "T1")
    for i in range(1, 11)
]
FACTS = {"F1": "Project reduces orientation time", "F2": "Team 1 owns core APIs"}
QUIZ_QUESTIONS = [QuizQuestionModel(id=f"Q{i}", question_text=f"Question {i}") for i in range(1, 16)]

@app.get("/overview", response_model=OverviewResponse, tags=["overview"])
def get_overview():
    return OverviewResponse(
        mission="Accelerate orientation clarity for large projects",
        problem="Context loss and slow onboarding reduce early productivity",
        value="Compression of orientation time and retention of core facts",
        team_count=len(TEAMS),
        rationale="Orientation compression unlocks faster time-to-impact"
    )

@app.get("/org", response_model=OrgResponse, tags=["org"])
def get_org():
    return OrgResponse(teams=TEAMS)

@app.get("/roles", response_model=RolesLookupResponse, tags=["roles"])
def role_lookup(query: str):
    # Simple match: include all teams with score 1.0 if query in name else 0.5 baseline
    matches = []
    for t in TEAMS:
        score = 1.0 if query.lower() in t.name.lower() else 0.5
        if score >= 0.5:
            matches.append(RolesMatch(team_id=t.id, team_name=t.name, score=score))
    return RolesLookupResponse(query=query, matches=matches)

@app.post("/qa", response_model=QAResponse, tags=["qa"])
def qa(question: str):
    # naive mapping: if 'api' in question -> fact F2 else F1
    source_id = "F2" if "api" in question.lower() else "F1"
    answer = FACTS[source_id]
    confidence = 0.9
    return QAResponse(question=question, answer=answer, confidence=confidence, source_fact_id=source_id, explanation="keyword match", escalation=None)

@app.post("/recommendation", response_model=RecommendationResponse, tags=["recommendation"])
def recommend(user_id: str):
    # return first team with breakdown
    selected = TEAMS[0]
    breakdown = [
        RecommendationBreakdown(factor="role_match", weight=50, description="General alignment"),
        RecommendationBreakdown(factor="responsibility_overlap", weight=30, description="API focus"),
        RecommendationBreakdown(factor="need_score", weight=20, description="Vacancy simulation")
    ]
    return RecommendationResponse(
        selected_team_id=selected.id,
        confidence=0.9,
        rationale=f"User {user_id} aligned to {selected.name} due to API ownership",
        explanation_breakdown=breakdown,
        tie_break=None
    )

@app.get("/quiz", response_model=QuizListResponse, tags=["quiz"])
def get_quiz():
    return QuizListResponse(questions=QUIZ_QUESTIONS)

@app.post("/quiz/submit", response_model=QuizSubmitResponse, tags=["quiz"])
def submit_quiz(answers: str):
    """Submit quiz answers.

    Accepts a single comma-separated string of answer IDs via query param `answers`.
    Example: /quiz/submit?answers=Q1,Q2,Q3
    """
    provided_ids = [a.strip() for a in answers.split(",") if a.strip()]
    correct_ids = [q.id for q in QUIZ_QUESTIONS]
    # Score is number of correct IDs present in provided set
    score = sum(1 for cid in correct_ids if cid in provided_ids)
    return QuizSubmitResponse(score=score, correct=correct_ids, total=len(QUIZ_QUESTIONS))

@app.get("/metrics", response_model=MetricsResponse, tags=["metrics"])
def get_metrics():
    baseline = 56.0
    tool = 20.0
    compression = round(((baseline - tool) / baseline) * 100, 2)
    return MetricsResponse(baseline_hours=baseline, tool_hours=tool, compression_pct=compression, quiz_accuracy=1.0, confidence_coverage=0.98)

@app.get("/gaps", response_model=GapsResponse, tags=["gaps"])
def get_gaps():
    # simplistic: no gaps demo
    summary = GapsSummary(total_teams=len(TEAMS), gap_count=0, stale_threshold_days=180)
    return GapsResponse(gaps=[], summary=summary)

@app.get("/qa/fallback", response_model=FallbackQAResponse, tags=["qa"])
def qa_fallback(question: str):
    return FallbackQAResponse(question=question, escalation="Consult Mentor", confidence=0.5)
