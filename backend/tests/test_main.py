"""
test_main.py
------------
Simple pytest tests using FastAPI's TestClient (built on httpx).

Run with:  pytest
(from inside the backend/ directory, with dependencies installed)

Note: these tests hit whatever DATABASE_URL is configured in your
environment. For a learning project it's fine to run them against
your local/dev Postgres. In a more advanced setup you'd point tests
at a separate test database.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    payload = {"title": "Buy groceries", "description": "Milk, eggs, bread"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data


def test_get_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
