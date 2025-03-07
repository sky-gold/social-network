from fastapi import APIRouter, Depends, Header, HTTPException, Request
from app.clients.user_client import user_client
from fastapi.responses import JSONResponse

router = APIRouter()

async def get_user_id(session_id: str = Header(None, alias="Session-ID")):
    if not session_id:
        return None
    
    response = await user_client.get_user(session_id)
    if response.status_code == 200:
        return response.json().get("user_id")
    return None

@router.api_route("/{path:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def proxy_request(
    request: Request,
    path: str,
    user_id: str = Depends(get_user_id)
):
    headers = {
        "X-User-ID": str(user_id) if user_id else "null",
        **{k: v for k, v in request.headers.items() if k.lower() != "host"}
    }
    
    response = await user_client.proxy_request(
        method=request.method,
        path=f"/{path}",
        headers=headers,
        content=await request.body()
    )
    
    return JSONResponse(
        content=response.json(),
        status_code=response.status_code,
        headers=dict(response.headers)
    )