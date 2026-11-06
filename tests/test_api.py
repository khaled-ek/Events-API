import pytest
import requests
import time

BASE_URL = "http://localhost:5000/api/"

def test_health_check():

    response = requests.get(f"{BASE_URL}/health")

    # Assert
    # check status code
    assert response.status_code == 200

    # check the returned data
    assert response.json()["status"] == "healthy"

def test_user_registration():
    # create a unique user
    username = f"user{time.time() * 1000}"
    user = {
        "username": username,
        "password": "pass123"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=user)

    # Assert
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

    assert response.json()["user"]["username"] == user["username"]

    assert response.status_code != 401


def test_create_event(auth_token):
    "Test creating a public event"
    event_data = {
        "title": "Project brainstorming Meetup",
        "description": "Brainstorming and proposal writing Meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 20,
        "is_public": True,
        "requires_admin": False
    }

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
        headers=headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]
    assert data["description"] == event_data["description"]
    assert "requires_admin" in data
