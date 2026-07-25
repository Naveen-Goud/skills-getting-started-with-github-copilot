import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_state():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


client = TestClient(app_module.app)


def test_unregister_participant_removes_email():
    response = client.post(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_error():
    response = client.post(
        "/activities/Chess Club/unregister?email=ghost@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found in activity"
