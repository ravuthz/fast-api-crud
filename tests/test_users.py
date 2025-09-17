import os
import sys

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def get_auth_headers(client, username="admin", password="admin123"):
    """Get JWT auth headers"""
    res = client.post("/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def assert_result(response, username, status=200):
    assert response.status_code == status
    data = response.json()
    assert data["username"] == username


@pytest.fixture(scope="module")
def auth_client():
    """
    Returns a TestClient with Authorization header already set.
    """
    # Add Authorization header to every request
    client.headers.update(get_auth_headers(client))
    return client

def mock_user(auth_client, username: str = None):
    # today = datetime.now().strftime("%Y%m%d%H%M%S")
    today = datetime.now().timestamp()
    unique_name = username if username else f"test_user_{today}"

    payload = {
        "email": f"{unique_name}@gm.com",
        "username": unique_name,
        "password": "password123"
    }

    res = auth_client.post("/users/", json=payload)
    data = res.json()

    return data['id'], unique_name, res


def test_show_user(auth_client):
    user_id, username, _res = mock_user(auth_client)

    res = auth_client.get(f"/users/{user_id}")
    assert_result(res, username)


def test_list_user(auth_client):
    res = auth_client.get("/users/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any("test_user_" in user["username"] for user in data)


def test_create_user(auth_client):
    _, unique_name, res = mock_user(auth_client)
    assert_result(res, unique_name, 201)


def test_update_user(auth_client):
    user_id, username, _res = mock_user(auth_client)

    payload = {"username": f"{username}_updated"}

    res = auth_client.put(f"/users/{user_id}", json=payload)
    assert_result(res, f"{username}_updated")


def test_delete_user(auth_client):
    user_id, username, _res = mock_user(auth_client)

    res = auth_client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "User deleted successfully"

    res = auth_client.get(f"/users/{user_id}")
    assert res.status_code == 404