from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_repository
import pytest
from unittest.mock import Mock, create_autospec, patch, ANY
from app.repositories.user_repository import UserRepository
import uuid
from datetime import datetime, timezone

@pytest.fixture
def mock_repo():
    mock = create_autospec(UserRepository)
    mock.get_user_by_username.return_value = None
    return mock


@pytest.fixture(autouse=True)
def override_dependency(mock_repo):
    app.dependency_overrides[get_repository] = lambda: mock_repo
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_register_user(mock_repo):
    mock_repo.create_user.return_value = Mock(
        id="550e8400-e29b-41d4-a716-446655440000",
        username="testuser",
        email="test@example.com",
    )

    mock_repo.create_session.return_value = Mock(
        session_id="550e8400-e29b-41d4-a716-446655440001",
        expires_at="2024-01-01T00:00:00Z",
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "password": "testpass",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 200
    mock_repo.get_user_by_username.assert_called_once_with("testuser")
    mock_repo.create_user.assert_called_once()
    mock_repo.create_session.assert_called_once()


def test_login_user(mock_repo):
    test_user_id = uuid.uuid4()
    test_session_id = uuid.uuid4()

    mock_user = Mock(id=test_user_id, password_hash="hashed_password")
    mock_repo.get_user_by_username.return_value = mock_user

    mock_session = Mock(
        session_id=test_session_id, expires_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )
    mock_repo.create_session.return_value = mock_session

    with patch("app.routers.auth.verify_password") as mock_verify:
        mock_verify.return_value = True

        response = client.post(
            "/api/v1/auth/login", json={"username": "testuser", "password": "testpass"}
        )

    assert response.status_code == 200
    assert response.json()['session_id'] == str(test_session_id)

    mock_repo.get_user_by_username.assert_called_once_with("testuser")
    mock_verify.assert_called_once_with("testpass", "hashed_password")
    mock_repo.create_session.assert_called_once_with(
        test_user_id,
        ANY,
        ANY,
    )
