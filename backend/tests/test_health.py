from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db


def test_health_ok(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_db_error(client: TestClient, app):
    class BrokenSession:
        def execute(self, *args, **kwargs):
            raise SQLAlchemyError("Database connection failed")

    app.dependency_overrides[get_db] = lambda: BrokenSession()

    try:
        response = client.get("/api/health")
        assert response.status_code == 503
        assert response.json() == {"status": "error", "database": "unavailable"}
    finally:
        app.dependency_overrides.clear()
