from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserLogin
from app.dependencies import get_repository
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/api/v1/auth")

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

async def get_client_ip(request: Request):
    return request.client.host

@router.post("/register")
async def register(
    request: Request,
    user: UserCreate,
    repo: UserRepository = Depends(get_repository)
):
    existing_user = repo.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    try:
        new_user = repo.create_user(user, hashed_password)
        repo.create_profile(new_user.id)
        expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        session = repo.create_session(
            new_user.id,
            await get_client_ip(request),
            expires_at
        )
        return {
            "user_id": new_user.id,
            "session_id": session.session_id,
            "expires_at": session.expires_at
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login")
async def login(
    request: Request,
    user: UserLogin,
    repo: UserRepository = Depends(get_repository)
):
    db_user = repo.get_user_by_username(user.username)
    
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    session = repo.create_session(
        db_user.id,
        await get_client_ip(request),
        expires_at
    )
    
    return {
        "user_id": db_user.id,
        "session_id": session.session_id,
        "expires_at": expires_at
    }
