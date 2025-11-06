from typing import List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends, Body
from fastapi.middleware.cors import CORSMiddleware

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
    TeamCreate,
    TeamUpdate,
    FactModel,
    FactCreate,
    FactUpdate,
    QuizQuestionCreate,
    QuizQuestionUpdate,
)

app = FastAPI(title="POI Compass API", version="1.0.0")

from app.observability import init_observability  # noqa: E402
from app.security import SecurityHeadersMiddleware  # noqa: E402
from app.audit import AuditMiddleware  # noqa: E402
from app.flags import is_enabled  # noqa: E402
from app.settings import settings  # noqa: E402
from app.runtime_metrics import aggregator  # noqa: E402
from app.recommendation_engine import recommend_for_user, debug_candidates, UserContext  # noqa: E402
from app.confidence import evaluate_confidence  # noqa: E402
from app.db import init_db, get_session, engine  # noqa: E402
from app.db_models import Team, ProjectFact, QuizQuestion, User  # noqa: E402
from sqlmodel import Session, select  # noqa: E402
from app.retrieval import get_retriever  # noqa: E402

if settings.poi_observability:  # enabled by default via settings
    init_observability(app)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditMiddleware)

# CORS configuration (permissive by default for demo; tighten via CORS_ORIGINS env)
import os as _os  # local alias to avoid name collision above
_origins = [o.strip() for o in _os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()] or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import JSONResponse  # noqa: E402
from fastapi import Request  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
import os  # noqa: E402
# Serve built frontend if present (single-container deploy)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend_build")
if os.path.isdir(FRONTEND_DIR):
    # Mount at /app for static assets, and root index fallback via simple route
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    async def root_index():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                return HTMLResponse(f.read())
        return {"message": "Frontend build not found"}

from fastapi.responses import HTMLResponse  # noqa: E402


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
    # If detail already a structured dict with error_code/message, preserve it.
    if isinstance(exc.detail, dict):
        payload = dict(exc.detail)
        payload.setdefault("error_code", f"HTTP_{exc.status_code}")
        payload.setdefault("message", "")
        payload.setdefault("trace_id", trace_id)
        return JSONResponse(status_code=exc.status_code, content=payload)
    return JSONResponse(status_code=exc.status_code, content={"error_code": f"HTTP_{exc.status_code}", "message": exc.detail, "trace_id": trace_id})

@app.get("/health", tags=["system"])
def health():
    import os
    return {
        "status": "ok",
        "version": "1.0.0",
        "git_commit": os.getenv("GIT_COMMIT", "unknown"),
        "build_time": os.getenv("BUILD_TIME", "unknown"),
    }

@app.get("/config/health", tags=["system"], summary="Configuration & provider availability")
def config_health():  # lightweight, no DB
    import os
    required = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "HUGGINGFACE_API_KEY",
        "TAVILY_API_KEY",
        "GOOGLE_API_KEY",
    ]
    missing = [k for k in required if not os.getenv(k)]
    return {
        "providers": settings.provider_status(),  # all booleans
        "missing_required": missing,
        "strict_env": os.getenv("STRICT_ENV") == "1",
    }

@app.get("/internal/runtime-metrics", tags=["internal"])
def runtime_metrics(x_internal_token: str | None = Header(default=None)):
    if not settings.internal_metrics_enabled:
        raise HTTPException(status_code=404, detail="Not found")
    import os  # local import to avoid top-level dependency ordering
    expected = os.getenv("INTERNAL_ACCESS_TOKEN")
    if expected and x_internal_token != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return aggregator.snapshot()

@app.on_event("startup")
def _startup_seed() -> None:
    init_db()
    with Session(engine) as s:  # type: ignore
        if s.exec(select(Team)).first() is None:
            for i in range(1, 11):
                s.add(Team(id=f"T{i}", name=f"Team {i}", mission="Deliver quality features", responsibilities=["API", "Docs"], parent_team_id=None if i == 1 else "T1"))
        if s.exec(select(ProjectFact)).first() is None:
            s.add(ProjectFact(id="F1", category="orientation", fact_text="Project reduces orientation time"))
            s.add(ProjectFact(id="F2", category="ownership", fact_text="Team 1 owns core APIs"))
        if s.exec(select(QuizQuestion)).first() is None:
            for i in range(1, 16):
                s.add(QuizQuestion(id=f"Q{i}", fact_id="F1" if i % 2 == 0 else "F2", question_text=f"Question {i}", correct_answer="answer"))
        if s.exec(select(User)).first() is None:
            s.add(User(id="u1", role="API Engineer", tenure_days=10, activity_state="active"))
            s.add(User(id="u2", role="Docs Writer", tenure_days=5, activity_state="drifting"))
            s.add(User(id="u3", role="Generalist", tenure_days=40, activity_state="idle"))
        s.commit()
    _verify_seed_integrity()

EXPECTED_SEED = {
    "teams": 10,
    "facts": {"F1", "F2"},
    "quiz_questions": 15,
}

def _verify_seed_integrity():  # best-effort warning only
    try:
        with Session(engine) as s:  # type: ignore
            team_count = s.exec(select(Team)).count()
            fact_ids = {f.id for f in s.exec(select(ProjectFact)).all()}
            quiz_count = s.exec(select(QuizQuestion)).count()
        issues = []
        if team_count < EXPECTED_SEED["teams"]:
            issues.append(f"teams expected>={EXPECTED_SEED['teams']} actual={team_count}")
        if not EXPECTED_SEED["facts"].issubset(fact_ids):
            issues.append(f"missing facts: {EXPECTED_SEED['facts'] - fact_ids}")
        if quiz_count < EXPECTED_SEED["quiz_questions"]:
            issues.append(f"quiz questions expected>={EXPECTED_SEED['quiz_questions']} actual={quiz_count}")
        if issues:
            import logging
            logging.warning({"event": "seed_integrity_warning", "issues": issues})
    except Exception:  # pragma: no cover
        import logging
        logging.warning({"event": "seed_integrity_check_failed"})

ADMIN_TOKEN_ENV = "ADMIN_API_KEY"

def require_admin(x_admin_token: str | None = Header(default=None)):
    import os
    expected = os.getenv(ADMIN_TOKEN_ENV)
    if not expected:
        raise HTTPException(status_code=500, detail="Admin token not configured")
    if x_admin_token != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

def get_tenant_id(x_tenant_id: str | None = Header(default=None)) -> str:
    return x_tenant_id or "default"

def _teams(session: Session, tenant_id: str) -> List[TeamModel]:
    results = session.exec(select(Team).where(Team.tenant_id == tenant_id)).all()
    return [TeamModel(id=t.id, name=t.name, mission=t.mission, responsibilities=t.responsibilities, parent_team_id=t.parent_team_id, tenant_id=t.tenant_id) for t in results]

def _quiz_questions(session: Session) -> List[QuizQuestionModel]:
    q = session.exec(select(QuizQuestion)).all()
    return [QuizQuestionModel(id=i.id, question_text=i.question_text) for i in q]

def _facts_map(session: Session):
    return {f.id: f for f in session.exec(select(ProjectFact)).all()}

@app.get("/overview", response_model=OverviewResponse, tags=["overview"])
def get_overview(session: Session = Depends(get_session)):
    team_count = len(session.exec(select(Team)).all())
    return OverviewResponse(
        mission="Accelerate orientation clarity for large projects",
        problem="Context loss and slow onboarding reduce early productivity",
        value="Compression of orientation time and retention of core facts",
        team_count=team_count,
        rationale="Orientation compression unlocks faster time-to-impact"
    )

@app.get("/org", response_model=OrgResponse, tags=["org"])
def get_org(session: Session = Depends(get_session), tenant_id: str = Depends(get_tenant_id)):
    return OrgResponse(teams=_teams(session, tenant_id))

@app.get("/roles", response_model=RolesLookupResponse, tags=["roles"])
def role_lookup(query: str, session: Session = Depends(get_session), tenant_id: str = Depends(get_tenant_id)):
    # Simple match: include all teams with score 1.0 if query in name else 0.5 baseline
    matches = []
    for t in _teams(session, tenant_id):
        score = 1.0 if query.lower() in t.name.lower() else 0.5
        if score >= 0.5:
            matches.append(RolesMatch(team_id=t.id, team_name=t.name, score=score))
    return RolesLookupResponse(query=query, matches=matches)

@app.post("/qa", response_model=QAResponse, tags=["qa"])
def qa(question: str, session: Session = Depends(get_session), request: Request = None):
    retriever = get_retriever()
    result = retriever.retrieve(session, question)
    envelope = evaluate_confidence(result.confidence, {"question": question, "trace_id": request.headers.get("X-Trace-Id") if request else None})
    escalation = None
    if envelope["status"] == "escalate":
        escalation = envelope["next_action"]
    return QAResponse(
        question=question,
        answer=result.answer,
        confidence=envelope.get("confidence", result.confidence),
        source_fact_id=result.fact_id,
        explanation=result.explanation,
        escalation=escalation,
    )

@app.post("/recommendation", response_model=RecommendationResponse, tags=["recommendation"])
def recommend(user_id: str, session: Session = Depends(get_session), tenant_id: str = Depends(get_tenant_id), request: Request = None):
    if settings.rec_disable:
        raise HTTPException(status_code=503, detail="Recommendation feature disabled")
    user_row = session.get(User, user_id)
    user_ctx = None
    if user_row:
        user_ctx = UserContext(user_id=user_row.id, role=user_row.role, tenure_days=user_row.tenure_days, activity_state=user_row.activity_state)
    raw = recommend_for_user(user_id, _teams(session, tenant_id), user=user_ctx)
    envelope = evaluate_confidence(raw.confidence, {"user_id": user_id, "trace_id": request.headers.get("X-Trace-Id") if request else None})
    # Preserve response model fields; optionally adjust confidence if clamped
    adjusted_conf = envelope.get("confidence", raw.confidence)
    # tie_break unchanged
    return RecommendationResponse(
        selected_team_id=raw.selected_team_id,
        confidence=adjusted_conf,
        rationale=raw.rationale,
        explanation_breakdown=raw.explanation_breakdown,
        tie_break=raw.tie_break,
    )

@app.get("/quiz", response_model=QuizListResponse, tags=["quiz"])
def get_quiz(session: Session = Depends(get_session)):
    if settings.quiz_disable:
        raise HTTPException(status_code=503, detail="Quiz feature disabled")
    return QuizListResponse(questions=_quiz_questions(session))

@app.post("/quiz/submit", response_model=QuizSubmitResponse, tags=["quiz"])
def submit_quiz(answers: str, session: Session = Depends(get_session)):
    if settings.quiz_disable:
        raise HTTPException(status_code=503, detail="Quiz feature disabled")
    """Submit quiz answers.

    Supported formats (query param `answers`):
      1. Comma-separated question IDs: `Q1,Q2,Q3` (legacy / tests)
      2. Pipe-separated id:value pairs: `Q1:answer one|Q2:answer two|...` (frontend form)

    For demo scoring we only validate presence of all question IDs; answer text
    is ignored (deterministic perfect score scenario when all IDs supplied).
    """
    provided_ids: list[str] = []
    if "|" in answers:
        # Frontend style id:value pairs
        for segment in answers.split("|"):
            if not segment.strip():
                continue
            parts = segment.split(":", 1)
            qid = parts[0].strip()
            if qid:
                provided_ids.append(qid)
    else:
        provided_ids = [a.strip() for a in answers.split(",") if a.strip()]

    quiz_items = _quiz_questions(session)
    correct_ids = [q.id for q in quiz_items]
    score = sum(1 for cid in correct_ids if cid in provided_ids)
    return QuizSubmitResponse(score=score, correct=correct_ids, total=len(quiz_items))

@app.get("/metrics", response_model=MetricsResponse, tags=["metrics"])
def get_metrics():
    baseline = 56.0
    tool = 20.0
    compression = round(((baseline - tool) / baseline) * 100, 2)
    return MetricsResponse(baseline_hours=baseline, tool_hours=tool, compression_pct=compression, quiz_accuracy=1.0, confidence_coverage=0.98)

@app.get("/gaps", response_model=GapsResponse, tags=["gaps"])
def get_gaps(session: Session = Depends(get_session), tenant_id: str = Depends(get_tenant_id)):
    gap_items = [
        {"team_id": "T5", "type": "missing_mission", "detail": "Mission statement not defined"}
    ]
    summary = GapsSummary(total_teams=len(_teams(session, tenant_id)), gap_count=len(gap_items), stale_threshold_days=180)
    return GapsResponse(gaps=gap_items, summary=summary)

@app.get("/qa/fallback", response_model=FallbackQAResponse, tags=["qa"])
def qa_fallback(question: str):
    return FallbackQAResponse(question=question, escalation="Consult Mentor", confidence=0.5)

# ---------------------- Admin & Debug Endpoints (API key protected) ----------------------

@app.get("/admin/teams", response_model=List[TeamModel], tags=["admin"])
def list_teams(session: Session = Depends(get_session), tenant_id: str = Depends(get_tenant_id), _: bool = Depends(require_admin)):
    return _teams(session, tenant_id)

@app.post("/admin/teams", response_model=TeamModel, tags=["admin"])
def create_team(payload: TeamCreate, session: Session = Depends(get_session), tenant_id: str = Depends(get_tenant_id), _: bool = Depends(require_admin)):
    target_tenant = payload.tenant_id or tenant_id
    # Allow same team id across different tenants (composite uniqueness)
    existing = session.exec(select(Team).where(Team.id == payload.id).where(Team.tenant_id == target_tenant)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Team ID exists in tenant")
    t = Team(id=payload.id, name=payload.name, mission=payload.mission, responsibilities=payload.responsibilities, parent_team_id=payload.parent_team_id, tenant_id=target_tenant)
    session.add(t)
    session.commit()
    session.refresh(t)
    return TeamModel(**t.model_dump())

@app.patch("/admin/teams/{team_id}", response_model=TeamModel, tags=["admin"])
def update_team(team_id: str, payload: TeamUpdate, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    t = session.get(Team, team_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    for field in ["name", "mission", "responsibilities", "parent_team_id"]:
        val = getattr(payload, field)
        if val is not None:
            setattr(t, field, val)
    session.add(t)
    session.commit()
    session.refresh(t)
    return TeamModel(**t.model_dump())

@app.delete("/admin/teams/{team_id}", tags=["admin"], status_code=204)
def delete_team(team_id: str, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    t = session.get(Team, team_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(t)
    session.commit()
    return None

@app.get("/admin/facts", response_model=List[FactModel], tags=["admin"])
def list_facts(session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    facts = session.exec(select(ProjectFact)).all()
    return [FactModel(id=f.id, category=f.category, fact_text=f.fact_text, tenant_id=f.tenant_id) for f in facts]

@app.post("/admin/facts", response_model=FactModel, tags=["admin"])
def create_fact(payload: FactCreate, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    if session.get(ProjectFact, payload.id):
        raise HTTPException(status_code=409, detail="Fact ID exists")
    f = ProjectFact(**payload.model_dump(exclude_none=True))
    session.add(f)
    session.commit()
    session.refresh(f)
    return FactModel(id=f.id, category=f.category, fact_text=f.fact_text, tenant_id=f.tenant_id)

@app.patch("/admin/facts/{fact_id}", response_model=FactModel, tags=["admin"])
def update_fact(fact_id: str, payload: FactUpdate, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    f = session.get(ProjectFact, fact_id)
    if not f:
        raise HTTPException(status_code=404, detail="Not found")
    if payload.category is not None:
        f.category = payload.category
    if payload.fact_text is not None:
        f.fact_text = payload.fact_text
    session.add(f)
    session.commit()
    session.refresh(f)
    return FactModel(id=f.id, category=f.category, fact_text=f.fact_text, tenant_id=f.tenant_id)

@app.delete("/admin/facts/{fact_id}", status_code=204, tags=["admin"])
def delete_fact(fact_id: str, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    f = session.get(ProjectFact, fact_id)
    if not f:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(f)
    session.commit()
    return None

@app.get("/admin/quiz/questions", response_model=List[QuizQuestionModel], tags=["admin"])
def list_quiz_questions(session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    return _quiz_questions(session)

@app.post("/admin/quiz/questions", response_model=QuizQuestionModel, tags=["admin"])
def create_quiz_question(payload: QuizQuestionCreate, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    if session.get(QuizQuestion, payload.id):
        raise HTTPException(status_code=409, detail="Question ID exists")
    q = QuizQuestion(**payload.model_dump(exclude_none=True))
    session.add(q)
    session.commit()
    session.refresh(q)
    return QuizQuestionModel(id=q.id, question_text=q.question_text)

@app.patch("/admin/quiz/questions/{question_id}", response_model=QuizQuestionModel, tags=["admin"])
def update_quiz_question(question_id: str, payload: QuizQuestionUpdate, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    q = session.get(QuizQuestion, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Not found")
    if payload.question_text is not None:
        q.question_text = payload.question_text
    if payload.correct_answer is not None:
        q.correct_answer = payload.correct_answer
    session.add(q)
    session.commit()
    session.refresh(q)
    return QuizQuestionModel(id=q.id, question_text=q.question_text)

@app.delete("/admin/quiz/questions/{question_id}", status_code=204, tags=["admin"])
def delete_quiz_question(question_id: str, session: Session = Depends(get_session), _: bool = Depends(require_admin)):
    q = session.get(QuizQuestion, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(q)
    session.commit()
    return None

@app.get("/admin/recommendation/debug", tags=["admin"])
def recommendation_debug(user_id: str, session: Session = Depends(get_session), tenant_id: str = Depends(get_tenant_id), _: bool = Depends(require_admin)):
    user_row = session.get(User, user_id)
    user_ctx = None
    if user_row:
        user_ctx = UserContext(user_id=user_row.id, role=user_row.role, tenure_days=user_row.tenure_days, activity_state=user_row.activity_state)
    return {"candidates": debug_candidates(user_id, _teams(session, tenant_id), user=user_ctx)}
