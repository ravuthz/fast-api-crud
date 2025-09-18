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


def assert_result(response, name, status=200):
    assert response.status_code == status
    data = response.json()

    if response.status_code != status:
        print(json.dumps(data, indent=2, ensure_ascii=False))

    assert data["name"] == name


@pytest.fixture(scope="module")
def auth_client():
    """
    Returns a TestClient with Authorization header already set.
    """
    # Add Authorization header to every request
    client.headers.update(get_auth_headers(client))
    return client


def mock_data(auth_client, name: str = None):
    today = datetime.now().timestamp()
    unique_name = name if name else f"test_role_{today}"

    payload = {
        "name": unique_name,
        "description": f"Description of {unique_name}",
        # "permission_ids": [],
    }

    res = auth_client.post("/roles/", json=payload)
    data = res.json()

    return data["id"], unique_name, res


def test_show_role(auth_client):
    role_id, unique_name, _res = mock_data(auth_client)

    res = auth_client.get(f"/roles/{role_id}")
    assert_result(res, unique_name)


def test_list_role(auth_client):
    res = auth_client.get("/roles/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any("test_role_" in user["name"] for user in data)


def test_create_role(auth_client):
    _, unique_name, res = mock_data(auth_client)
    assert_result(res, unique_name, 201)


def test_update_role(auth_client):
    role_id, unique_name, _res = mock_data(auth_client)
    payload = {"name": f"{unique_name}_updated"}

    res = auth_client.put(f"/roles/{role_id}", json=payload)
    assert_result(res, f"{unique_name}_updated")


def test_delete_role(auth_client):
    role_id, unique_name, _res = mock_data(auth_client)

    res = auth_client.delete(f"/roles/{role_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "Roles deleted successfully"

    res = auth_client.get(f"/roles/{role_id}")
    assert res.status_code == 404
