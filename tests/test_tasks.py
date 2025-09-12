import logging
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_user_and_token(username="testuser"):
    """Helper: create a user and return headers with JWT token"""
    client.post("/auth/signup", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "pass123"
    })
    login_res = client.post("/auth/login", data={
        "username": username,
        "password": "pass123"
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_task_crud_flow(caplog):
    headers = create_user_and_token("charlie")

    # --- Create task ---
    with caplog.at_level(logging.INFO):
        create_res = client.post("/tasks/", json={"title": "First Task", "description": "demo"}, headers=headers)
    assert create_res.status_code == 200
    task_id = create_res.json()["id"]
    assert any("created" in record.message.lower() for record in caplog.records)

    # --- Get task ---
    get_res = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_res.status_code == 200

    # --- Delete task ---
    delete_res = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_res.status_code == 204
    assert delete_res.content == b''


def test_task_unauthorized_access():
    # Try to get a task without authentication
    res = client.get("/tasks/1")
    assert res.status_code == 403  # FastAPI returns 403 for missing token


def test_task_not_found(caplog):
    headers = create_user_and_token("delta")
    with caplog.at_level(logging.WARNING):
        res = client.get("/tasks/9999", headers=headers)  # Non-existent task
    assert res.status_code == 404
    assert any("not found" in record.message.lower() for record in caplog.records)
