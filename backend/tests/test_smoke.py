from fastapi.testclient import TestClient


def test_app_starts_and_serves_openapi_schema(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
