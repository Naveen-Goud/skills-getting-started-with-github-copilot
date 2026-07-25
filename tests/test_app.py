import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_state():
    # Arrange
    original = copy.deepcopy(app_module.activities)
    yield

    # Cleanup
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


client = TestClient(app_module.app)


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200

    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_participant_returns_error():
    # Arrange
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found in activity"
