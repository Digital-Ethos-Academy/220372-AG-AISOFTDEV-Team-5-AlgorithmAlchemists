"""Global test fixtures enforcing determinism and time freeze.

Best practice guardrail: all tests share fixed random seed & frozen timestamp
to eliminate flakiness and enable reproducible agent evaluation.
"""
from __future__ import annotations

import os
import random
import time
from datetime import datetime, timezone

import pytest

FIXED_TS = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
FIXED_EPOCH = int(FIXED_TS.timestamp())
SEED = 1337


@pytest.fixture(autouse=True)
def _deterministic_seed() -> None:
    """Set deterministic random seeds for python's random & time dependent code."""
    random.seed(SEED)
    # If libraries rely on PYTHONHASHSEED for dict ordering variations
    os.environ["PYTHONHASHSEED"] = str(SEED)


@pytest.fixture(autouse=True)
def _freeze_time(monkeypatch: pytest.MonkeyPatch) -> None:
    """Freeze time.time() to ensure deterministic latency calculations.

    Note: Patching datetime.datetime methods directly is not supported (immutable C-API);
    relying on time.time() stability is sufficient for current audit log & metrics logic.
    """
    monkeypatch.setattr(time, "time", lambda: float(FIXED_EPOCH))

@pytest.fixture(autouse=True)
def _ensure_db() -> None:
    """Ensure database tables exist before tests that hit API endpoints.

    Startup events sometimes are bypassed in certain TestClient patterns; creating
    tables idempotently here removes ordering sensitivity.
    """
    try:
        from sqlmodel import Session, select

        from app.db import engine, init_db
        from app.db_models import Team
        init_db()
        # Seed if empty (mirrors startup seeding)
        with Session(engine) as s:  # type: ignore
            if s.exec(select(Team)).first() is None:
                from app.main import _startup_seed  # import here to reuse logic
                _startup_seed()
            # Remove transient test artifacts to keep idempotent runs (tenant isolation test)
            alpha_existing = s.exec(select(Team).where(Team.id == "TA1").where(Team.tenant_id == "alpha")).first()
            if alpha_existing:
                s.delete(alpha_existing)
                s.commit()
    except Exception as e:  # pragma: no cover - fail fast if truly broken
        pytest.fail(f"Database init/seed failed: {e}")
