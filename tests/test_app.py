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


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_and_remove_participant():
    email = "test-student@mergington.edu"
    activity_name = "Chess Club"

    # signup
    signup_res = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_res.status_code == 200
    assert "Signed up" in signup_res.json()["message"]

    # now participant should be in the list
    act_res = client.get("/activities")
    assert email in act_res.json()[activity_name]["participants"]

    # remove participant
    remove_res = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert remove_res.status_code == 200
    assert "Removed" in remove_res.json()["message"]

    # participant should no longer exist
    act_res2 = client.get("/activities")
    assert email not in act_res2.json()[activity_name]["participants"]


def test_signup_duplicate_fails():
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400


def test_remove_missing_participant_fails():
    response = client.delete("/activities/Chess Club/participants/does-not-exist@mergington.edu")
    assert response.status_code == 404
