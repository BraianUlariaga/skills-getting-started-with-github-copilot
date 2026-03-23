from src import app as app_module


def test_get_activities_returns_all_activities(test_client):
    # Arrange
    # (Fixture handles setup / reset)

    # Act
    response = test_client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == app_module.activities["Chess Club"]["max_participants"]


def test_signup_for_activity_success(test_client):
    # Arrange
    email = "aaa-test@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = test_client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_for_activity_already_signed_up_fails(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = test_client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_for_missing_activity_fails(test_client):
    # Arrange
    activity_name = "No Such Activity"
    email = "test@mergington.edu"

    # Act
    response = test_client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = test_client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_remove_nonexistent_participant_fails(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "does-not-exist@mergington.edu"

    # Act
    response = test_client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_inexistent_activity_fails(test_client):
    # Arrange
    activity_name = "No Such Activity"
    email = "test@mergington.edu"

    # Act
    response = test_client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
