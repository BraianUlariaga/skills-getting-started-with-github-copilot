import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)

INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_api_activities():
    """Smoke test: API returns activities JSON"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_html_page_loads():
    """Smoke test: HTML page loads and contains key elements"""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert '<div id="activities-list">' in html
    assert '<form id="signup-form">' in html
    assert 'id="activity"' in html


def test_signup_and_remove_flow():
    """Smoke test: Full signup and remove flow works"""
    email = "smoke-test@mergington.edu"
    activity = "Chess Club"

    # Initial state
    resp = client.get("/activities")
    initial_participants = resp.json()[activity]["participants"]
    assert email not in initial_participants

    # Signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json()["message"]

    # Verify added
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]

    # Remove
    remove_resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert remove_resp.status_code == 200
    assert "Removed" in remove_resp.json()["message"]

    # Verify removed
    resp3 = client.get("/activities")
    assert email not in resp3.json()[activity]["participants"]


def test_duplicate_signup_fails():
    """Smoke test: Duplicate signup is rejected"""
    email = "michael@mergington.edu"  # Already in Chess Club
    response = client.post("/activities/Chess Club/signup?email=" + email)
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_remove_nonexistent_fails():
    """Smoke test: Removing nonexistent participant fails"""
    response = client.delete("/activities/Chess Club/participants/nonexistent@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()