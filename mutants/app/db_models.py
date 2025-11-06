"""SQLModel ORM models for persistence layer.

Each model contains a `tenant_id` column (default "default") to allow
future multi-tenant partitioning without schema changes.
Lists (e.g. responsibilities) stored as JSON for clarity.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Team(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    name: str
    mission: str
    responsibilities: List[str] = Field(sa_column=Column(JSON), default_factory=list)
    parent_team_id: Optional[str] = Field(default=None, foreign_key="team.id")
    tenant_id: str = Field(default="default", index=True)


class ProjectFact(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    category: str
    fact_text: str
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: str = Field(default="default", index=True)


class QuizQuestion(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    fact_id: str = Field(foreign_key="projectfact.id")
    question_text: str
    correct_answer: str
    tenant_id: str = Field(default="default", index=True)


class User(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    role: str
    tenure_days: int = Field(default=0, ge=0)
    activity_state: str = Field(default="active")  # active | drifting | idle
    tenant_id: str = Field(default="default", index=True)
