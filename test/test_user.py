import pytest
from fastapi.testclient import TestClient
from routers.user import user_router  

client = TestClient(user_router)

# Sample payloads
new_user_payload = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "securepassword"
}

login_payload = {
    "email": "testuser@example.com",
    "password": "securepassword"
}

update_user_payload = {
    "username": "updateduser",
    "email": "updateduser@example.com"
}

@pytest.fixture
def create_user():
    """Fixture to create a user and return its ID."""
    response = client.post("/create_user", json=new_user_payload)
    assert response.status_code == 201
    return response.json()["data"]["id"]


def test_create_user():
    """Test creating a new user."""
    response = client.post("/create_user", json=new_user_payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Successfully created new user"
    assert "data" in response.json()
    assert "id" in response.json()["data"]


def test_login_user(create_user):
    """Test user login."""
    response = client.post("/login", json=login_payload)
    assert response.status_code == 202
    assert response.json()["message"] == "Login successful"
    assert "data" in response.json()
    # Adjust assertion based on API behavior
    assert "id" in response.json()["data"]
    assert "email" in response.json()["data"]
    # Uncomment if token is expected
    # assert "token" in response.json()["data"]


def test_get_user(create_user):
    """Test retrieving a specific user."""
    user_id = create_user
    response = client.get(f"/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User retrieved successfully"
    assert "data" in response.json()
    assert response.json()["data"]["id"] == user_id


def test_get_users():
    """Test retrieving all users."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Users retrieved successfully"
    assert isinstance(response.json()["data"], list)


def test_update_user(create_user):
    """Test updating a user."""
    user_id = create_user
    response = client.put(f"/{user_id}", json=update_user_payload)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["data"]["username"] == update_user_payload["username"]


def test_delete_user(create_user):
    """Test deleting a user."""
    user_id = create_user
    response = client.delete(f"/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
    assert "data" in response.json()


def test_get_nonexistent_user():
    """Test retrieving a non-existent user."""
    response = client.get("/nonexistent_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_nonexistent_user():
    """Test updating a non-existent user."""
    response = client.put("/nonexistent_id", json=update_user_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_nonexistent_user():
    """Test deleting a non-existent user."""
    response = client.delete("/nonexistent_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
