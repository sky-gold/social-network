from fastapi.testclient import TestClient
from app.main import app
import pytest
import respx
from httpx import Response

client = TestClient(app)


@pytest.mark.asyncio
@respx.mock
async def test_proxy_with_valid_session():
    user_service_url = "http://user_service:8001"

    auth_mock = respx.get(f"{user_service_url}/api/v1/auth/user").mock(
        return_value=Response(200, json={"user_id": "123"})
    )

    profile_mock = respx.request(
        method="GET", url=f"{user_service_url}/api/v1/profile/123"
    ).mock(return_value=Response(200, json={"data": "ok"}))

    response = client.get("/api/v1/profile/123", headers={"Session-ID": "valid"})

    assert response.status_code == 200
    assert response.json() == {"data": "ok"}

    assert auth_mock.called

    assert profile_mock.called
    last_request = profile_mock.calls.last.request
    assert last_request.headers.get("x-user-id") == "123"
