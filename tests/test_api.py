from time import sleep

import pytest
import requests
import time

BASE_URL = "http://localhost:5000/api/"

def test_health_endpoint_returns_healthy():

    """
        Tests the health endpoint to verify that the API is running correctly.

        Sends a GET request to the /health endpoint and checks that the response
        has a 200 status code and that the returned status is 'healthy'.
    """

    response = requests.get(f"{BASE_URL}/health")

    # Assert
    # check status code
    assert response.status_code == 200

    # check the returned data
    assert response.json()["status"] == "healthy"

def test_register_user_creates_new_user():
    """
        Tests the user registration endpoint to verify that a new user can
        be successfully registered.

        A unique username is generated as before. The test sends a registration request
        and verifies that the API returns the expected status code, success
        message
    """

    # Creating a unique user
    username = f"user{time.time() * 1000}"
    user = {
        "username": username,
        "password": "pass123"
    }

    # Registering the user
    response = requests.post(f"{BASE_URL}/auth/register", json=user)




    # Assert
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

    assert response.json()["user"]["username"] == user["username"]

    assert response.status_code != 401

def test_login_returns_jwt_token():
    """
        Tests the login endpoint to verify that a registered user can
        successfully log in and receive a JWT access token.

        A unique user is created. The test then sends
        a login request using the same credentials and verifies that the
        API returns a 200 status code and a non-null access token.
    """

    # 1. Create a unique user
    username = f"user{time.time() * 1000}"
    user = {
        "username": username,
        "password": "pass123"
    }

    # 2. Register the user first
    reg_response = requests.post(f"{BASE_URL}/auth/register", json=user)

    # 3. Log in with the same credentials
    response = requests.post(f"{BASE_URL}/auth/login", json=user)


    # Asserting
    assert response.status_code == 200
    assert response.json()["access_token"] is not None

def test_create_public_event_requires_auth_and_succeeds_with_token(auth_token):

    """
        Tests the event creation endpoint to verify that an authenticated user
        can successfully create a public event.

        The test uses the auth_token fixture to obtain a JWT access token,
        which is included in the Authorization header of the request.
        It sends a POST request with the event data and verifies that the API
        returns a 201 status code and that the response contains the expected
        event details.
    """

    # Creating a public event (with auth)
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

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]
    assert data["description"] == event_data["description"]
    assert data["date"] == event_data["date"]
    assert data["location"] == event_data["location"]
    assert "requires_admin" in data

def test_rsvp_to_public_event_succeeds_without_auth(auth_token):
    """
       Tests the RSVP endpoint to verify that an unauthenticated user can
       successfully RSVP to a public event.

       First, an authenticated user creates a public event. The test then
       sends an RSVP request to that event without an Authorization header
       and verifies that the API returns a 201 status code and the expected
       RSVP data, including the event ID and attendance status.
    """

    # 1. Creating a public event (with auth)
    event_data = {
        "title": "Public Community Meetup",
        "description": "An open event for everyone.",
        "date": "2026-01-15T18:00:00",
        "location": "Civic Center, Room 101",
        "capacity": 100,
        "is_public": True,
        "requires_admin": False
    }

    headers = {"Authorization": f"Bearer {auth_token}"}
    event_res = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
        headers=headers
    )

    assert event_res.status_code in [200, 201]

    event_id = event_res.json().get("id")

    # 2. Call the RSVP endpoint WITHOUT a token

    rsvp_payload = {
        "attending": True
    }

    response = requests.post(f"{BASE_URL}/rsvps/event/{event_id}", json=rsvp_payload)

    # Assertions

    # The endpoint returns 201 Created for a new RSVP
    assert response.status_code == 201

    response_data = response.json()
    # Verify the event_id matches what we expect
    assert response_data["event_id"] == event_id

    assert response_data["attending"] is True

# -------------------------------------------------------------
# -------------------------------------------------------------

# Error / Edge‑Case Tests

def test_duplicate_username_registration():

    # Creating a unique user
    username = f"user{time.time() * 1000}"
    user = {
        "username": username,
        "password": "pass123"
    }

    # Registering the user
    response = requests.post(f"{BASE_URL}/auth/register", json=user)

    # Asserts
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"
    assert response.json()["user"]["username"] == user["username"]

    response = requests.post(f"{BASE_URL}/auth/register", json=user)

    # Assert

    assert response.status_code == 400


def test_create_event_without_auth():

    event_data = {
        "title": "Project brainstorming Meetup",
        "description": "Brainstorming and proposal writing Meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 20,
        "is_public": True,
        "requires_admin": False
    }

    response = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
    )

    assert response.status_code == 401

def test_rsvp_to_non_public_event_without_auth(auth_token):
    
    headers = {"Authorization": f"Bearer {auth_token}"}

    # 1. Creating a public event (with auth)
    event_data = {
        "title": "Public Community Meetup",
        "description": "An open event for everyone.",
        "date": "2026-01-15T18:00:00",
        "location": "Civic Center, Room 101",
        "capacity": 100,
        "is_public": False,
        "requires_admin": False
    }

    event_res = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
        headers=headers
    )

    assert event_res.status_code in [200, 201]

    event_id = event_res.json().get("id")

    # 2. Call the RSVP endpoint WITHOUT a token

    rsvp_payload = {
        "attending": True
    }

    response = requests.post(f"{BASE_URL}/rsvps/event/{event_id}", json=rsvp_payload)

    # Assert
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["error"] == "Authentication required for this event"
