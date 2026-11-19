import pytest
import requests
import time

BASE_URL = "http://localhost:5000/api/"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def auth_token():
    """
        Registers a new user, authenticates the user, and returns an access token.

        A unique username is generated using the current timestamp. The user is registered and then
        authenticated through the API.

        Returns:
            str: The access token obtained after successful authentication.
    """

    # create a unique user
    username = f"user{time.time() * 1000}"
    user = {
        "username": username,
        "password": "pass123"
    }

    requests.post(f"{BASE_URL}/auth/register", json=user)

    # login the user
    response = requests.post(f"{BASE_URL}/auth/login", json=user)

    # return a token
    return response.json()["access_token"]

