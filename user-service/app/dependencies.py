from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.database import get_db
import uuid

def get_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_current_user(
    session_id: str = Header(..., alias="Session-ID"),
    repo: UserRepository = Depends(get_repository)
):
    try:
        session = repo.get_valid_session(uuid.UUID(session_id))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session ID format"
        )
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    return repo.get_user_by_id(session.user_id)


def get_current_user_profile(
    session_id: str = Header(..., alias="Session-ID"),
    repo: UserRepository = Depends(get_repository)
):
    try:
        session = repo.get_valid_session(uuid.UUID(session_id))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session ID format"
        )
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    return repo.get_profile_by_user_id(session.user_id)