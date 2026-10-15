"""Shared pytest fixtures.

Tests run against a separate MySQL database (TEST_DATABASE_URL). At the start
of every test run it is dropped, recreated and migrated with Alembic, so the
schema always matches the migrations. Each test runs inside a transaction that
is rolled back afterwards, so tests don't see each other's data.
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, make_url, text
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.main import create_app

BACKEND_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings = get_settings()
    if not settings.test_database_url:
        pytest.exit("TEST_DATABASE_URL is not set. Copy .env.example to .env.", returncode=1)

    test_db = make_url(settings.test_database_url).database or ""
    # The test database is wiped on every run: refuse anything that doesn't
    # look like a test database, so the dev database can't be dropped by accident.
    if not test_db.endswith("_test"):
        pytest.exit(f"Refusing to use {test_db!r} as test database: name must end in '_test'.")

    return settings.model_copy(update={"database_url": settings.test_database_url})


def _recreate_database(url: str) -> None:
    db_url = make_url(url)
    server_engine = create_engine(db_url.set(database=None))
    with server_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS `{db_url.database}`"))
        conn.execute(
            text(
                f"CREATE DATABASE `{db_url.database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
    server_engine.dispose()


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Iterator[Engine]:
    _recreate_database(settings.database_url)
    engine = create_engine(settings.database_url)

    alembic_cfg = Config(toml_file=str(BACKEND_DIR / "pyproject.toml"))
    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, "head")

    yield engine
    engine.dispose()


@pytest.fixture
def db_session(engine: Engine) -> Iterator[Session]:
    """A database session whose changes are rolled back after the test.

    Code under test may call `session.commit()`: with "create_savepoint" the
    commit only releases a savepoint, and the outer transaction is still
    rolled back at the end.
    """
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()
            transaction.rollback()


@pytest.fixture
def app(settings: Settings, db_session: Session) -> FastAPI:
    app = create_app(settings)
    # Endpoints get the test session, so they see data a test adds via `db_session`.
    app.dependency_overrides[get_db] = lambda: db_session
    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client
