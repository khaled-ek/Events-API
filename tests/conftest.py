import pytest
import requests
import time

BASE_URL = "http://localhost:5000/api/"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def auth_token():
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

