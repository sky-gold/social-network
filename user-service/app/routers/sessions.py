from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas import SessionResponse
from app.dependencies import get_current_user, get_repository
from app.models import User
import uuid

router = APIRouter(prefix="/api/v1/sessions")

@router.get("/", response_model=list[SessionResponse])
async def get_my_sessions(
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_repository)
):
    return current_user.sessions

@router.post("/logout")
async def logout(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_repository)
):
    session = next((s for s in current_user.sessions if s.session_id == session_id), None)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    repo.db.delete(session)
    repo.db.commit()
    
    return {"status": "success"}