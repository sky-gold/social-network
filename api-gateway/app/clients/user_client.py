import httpx
import os
from fastapi import HTTPException, status

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")

class UserClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=USER_SERVICE_URL)

    async def get_user(self, session_id: str):
        try:
            return await self.client.get(
                "/api/v1/auth/user",
                headers={"Session-ID": session_id}
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service unavailable"
            )

    async def proxy_request(self, method: str, path: str, headers: dict, **kwargs):
        try:
            response = await self.client.request(
                method=method,
                url=path,
                headers=headers,
                **kwargs
            )
            return response
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service unavailable"
            )

user_client = UserClient()