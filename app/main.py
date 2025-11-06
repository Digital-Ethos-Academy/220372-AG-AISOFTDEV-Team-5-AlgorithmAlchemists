from typing import List
from fastapi import FastAPI, HTTPException, Header

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

from app.observability import init_observability  # noqa: E402
from app.security import SecurityHeadersMiddleware  # noqa: E402
from app.audit import AuditMiddleware  # noqa: E402
from app.flags import is_enabled  # noqa: E402
from app.settings import settings  # noqa: E402
from app.runtime_metrics import aggregator  # noqa: E402
from app.recommendation_engine import recommend_for_user  # noqa: E402

if settings.poi_observability:  # enabled by default via settings
    init_observability(app)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditMiddleware)

from fastapi.responses import JSONResponse  # noqa: E402
from fastapi import Request  # noqa: E402


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    trace_id = request.headers.get("X-Trace-Id", "unknown")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "UNEXPECTED_ERROR",
            "message": str(exc),
            "trace_id": trace_id,
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    trace_id = request.headers.get("X-Trace-Id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "trace_id": trace_id,
        },
    )

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/internal/runtime-metrics", tags=["internal"])
def runtime_metrics(x_internal_token: str | None = Header(default=None)):
    if not settings.internal_metrics_enabled:
        raise HTTPException(status_code=404, detail="Not found")
    import os  # local import to avoid top-level dependency ordering
    expected = os.getenv("INTERNAL_ACCESS_TOKEN")
    if expected and x_internal_token != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return aggregator.snapshot()

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
    import re
    tokens = set(re.sub(r'[^a-z0-9 ]', '', question.lower()).split())
    if "api" in tokens:
        source_id = "F2"
        confidence = 0.92
        escalation = None
        explanation = "keyword match: api"
    elif "orientation" in tokens or "time" in tokens:
        source_id = "F1"
        confidence = 0.9
        escalation = None
        explanation = "keyword match: orientation/time"
    else:
        source_id = "F1"
        confidence = 0.6
        escalation = "Consult Mentor"
        explanation = "low token overlap"
    answer = FACTS[source_id]
    return QAResponse(question=question, answer=answer, confidence=confidence, source_fact_id=source_id, explanation=explanation, escalation=escalation)

@app.post("/recommendation", response_model=RecommendationResponse, tags=["recommendation"])
def recommend(user_id: str):
    if settings.rec_disable:
        raise HTTPException(status_code=503, detail="Recommendation feature disabled")
    return recommend_for_user(user_id, TEAMS)

@app.get("/quiz", response_model=QuizListResponse, tags=["quiz"])
def get_quiz():
    if settings.quiz_disable:
        raise HTTPException(status_code=503, detail="Quiz feature disabled")
    return QuizListResponse(questions=QUIZ_QUESTIONS)

@app.post("/quiz/submit", response_model=QuizSubmitResponse, tags=["quiz"])
def submit_quiz(answers: str):
    if settings.quiz_disable:
        raise HTTPException(status_code=503, detail="Quiz feature disabled")
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
    gap_items = [
        {"team_id": "T5", "type": "missing_mission", "detail": "Mission statement not defined"}
    ]
    summary = GapsSummary(total_teams=len(TEAMS), gap_count=len(gap_items), stale_threshold_days=180)
    return GapsResponse(gaps=gap_items, summary=summary)

@app.get("/qa/fallback", response_model=FallbackQAResponse, tags=["qa"])
def qa_fallback(question: str):
    return FallbackQAResponse(question=question, escalation="Consult Mentor", confidence=0.5)
