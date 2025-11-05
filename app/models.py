from pydantic import BaseModel, Field
from typing import List, Optional

class OverviewResponse(BaseModel):
    mission: str
    problem: str
    value: str
    team_count: int = Field(ge=1)
    rationale: str

class TeamModel(BaseModel):
    id: str
    name: str
    mission: str
    responsibilities: List[str]
    parent_team_id: Optional[str] = None

class OrgResponse(BaseModel):
    teams: List[TeamModel]

class RolesMatch(BaseModel):
    team_id: str
    team_name: str
    score: float = Field(ge=0, le=1)

class RolesLookupResponse(BaseModel):
    query: str
    matches: List[RolesMatch]

class QAResponse(BaseModel):
    question: str
    answer: str
    confidence: float = Field(ge=0, le=1)
    source_fact_id: str
    explanation: str
    escalation: Optional[str] = None

class RecommendationBreakdown(BaseModel):
    factor: str
    weight: int = Field(ge=0, le=100)
    description: str

class RecommendationResponse(BaseModel):
    selected_team_id: str
    confidence: float = Field(ge=0, le=1)
    rationale: str
    explanation_breakdown: List[RecommendationBreakdown]
    tie_break: Optional[str] = None

class QuizQuestionModel(BaseModel):
    id: str
    question_text: str

class QuizListResponse(BaseModel):
    questions: List[QuizQuestionModel]

class QuizSubmitResponse(BaseModel):
    score: int
    correct: List[str]
    total: int

class MetricsResponse(BaseModel):
    baseline_hours: float
    tool_hours: float
    compression_pct: float
    quiz_accuracy: float
    confidence_coverage: float

class GapItem(BaseModel):
    team_id: str
    type: str
    detail: str

class GapsSummary(BaseModel):
    total_teams: int
    gap_count: int
    stale_threshold_days: int

class GapsResponse(BaseModel):
    gaps: List[GapItem]
    summary: GapsSummary

class FallbackQAResponse(BaseModel):
    question: str
    escalation: str
    confidence: Optional[float] = None
