"""Database setup and session management.

Uses SQLModel (SQLAlchemy + Pydantic) with a lightweight SQLite backend.
Future-proofed with `tenant_id` column support on all domain tables.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("POIT_DATABASE_URL", "sqlite:///./poit.db")

# echo can be toggled via env for debugging
engine = create_engine(DATABASE_URL, echo=bool(int(os.getenv("POIT_DB_ECHO", "0"))), connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})


def init_db() -> None:
    """Create tables (idempotent). Migrations are overkill for demo scope."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:  # FastAPI dependency style generator
    with Session(engine) as session:
        yield session


@contextmanager
def session_ctx() -> Iterator[Session]:
    """Context manager variant for scripts / seeding."""
    with Session(engine) as s:
        yield s
