import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: Prepare test client (already done)
    # Act: Call the /activities endpoint
    response = client.get("/activities")
    # Assert: Check response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    # Arrange: Pick an activity and email
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act: Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert: Signup successful
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]
    # Act: Unregister
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert: Unregister successful
    assert unregister_resp.status_code == 200
    assert f"Unregistered {email}" in unregister_resp.json()["message"]


def test_signup_duplicate():
    # Arrange: Use existing participant
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act: Try to sign up again
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert: Should fail with 400
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]


def test_unregister_nonparticipant():
    # Arrange: Use non-participant
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act: Try to unregister
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert: Should fail with 400
    assert resp.status_code == 400
    assert "not registered" in resp.json()["detail"]
