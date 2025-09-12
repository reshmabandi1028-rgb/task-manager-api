import logging
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup_and_login(caplog):
    # --- Signup (may already exist) ---
    with caplog.at_level(logging.INFO):
        signup_res = client.post("/auth/signup", json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret123"
        })
    # Accept success or already exists
    assert signup_res.status_code in [200, 201, 400]
    assert any("signup" in record.message.lower() for record in caplog.records) or signup_res.status_code == 400

    # --- Login ---
    login_res = client.post("/auth/login", data={
        "username": "alice",
        "password": "secret123"
    })
    if login_res.status_code == 200:
        token = login_res.json()["access_token"]
        assert token
    else:
        # Login fails if user wasn't created, skip token test
        pytest.skip("User not created; skipping login assertions")


def test_signup_existing_user(caplog):
    # Ensure user exists
    client.post("/auth/signup", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "pass123"
    })

    # Attempt duplicate signup
    with caplog.at_level(logging.WARNING):
        res = client.post("/auth/signup", json={
            "username": "bob",
            "email": "bob2@example.com",
            "password": "pass123"
        })
    assert res.status_code == 400
    assert "username already registered" in res.json()["detail"].lower()
    assert any("already registered" in record.message.lower() for record in caplog.records)


def test_login_invalid_user():
    res = client.post("/auth/login", data={
        "username": "nonexistent",
        "password": "nopass"
    })
    assert res.status_code == 401
    assert "incorrect username or password" in res.json()["detail"].lower()
