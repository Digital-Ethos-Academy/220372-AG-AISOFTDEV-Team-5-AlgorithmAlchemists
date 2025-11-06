from typing import List, Optional

from pydantic import BaseModel, Field
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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
    tenant_id: Optional[str] = None

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
    # Allow None when no candidates are available (negative path)
    selected_team_id: Optional[str] = None
    confidence: float = Field(ge=0, le=1)
    rationale: str
    explanation_breakdown: List[RecommendationBreakdown]
    tie_break: Optional[str] = None

class QuizQuestionModel(BaseModel):
    id: str
    question_text: str

class TeamCreate(BaseModel):
    id: str
    name: str
    mission: str
    responsibilities: List[str] = []
    parent_team_id: Optional[str] = None
    tenant_id: Optional[str] = None

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    mission: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    parent_team_id: Optional[str] = None

class FactModel(BaseModel):
    id: str
    category: str
    fact_text: str
    tenant_id: Optional[str] = None

class FactCreate(BaseModel):
    id: str
    category: str
    fact_text: str
    tenant_id: Optional[str] = None

class FactUpdate(BaseModel):
    category: Optional[str] = None
    fact_text: Optional[str] = None

class QuizQuestionCreate(BaseModel):
    id: str
    fact_id: str
    question_text: str
    correct_answer: str
    tenant_id: Optional[str] = None

class QuizQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    correct_answer: Optional[str] = None

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
