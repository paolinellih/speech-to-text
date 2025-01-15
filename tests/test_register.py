from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from api.api import app
from infrastructure.database.connection import get_db

# Mock database session
def override_get_db():
    mock_db = MagicMock(spec=Session)  # Mock a session with SQLAlchemy's interface

    # Mock the add and commit operations
    def mock_add(instance):
        # Simulate auto-generating an ID for the user
        instance.id = 1

    mock_db.add.side_effect = mock_add
    
    # Mock database query and commit behavior
    mock_db.query.return_value.filter.return_value.first.return_value = None  # Simulate no existing user
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None  # Prevent errors if refresh() is called
    yield mock_db

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_user_success():
    # Define the test payload
    test_payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
    }

    # Call the endpoint
    response = client.post("/users/register", json=test_payload)

    # Assertions
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
