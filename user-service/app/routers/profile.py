from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas import ProfileResponse, ProfileUpdate
from app.dependencies import get_current_user, get_repository
from app.models import User

router = APIRouter(prefix="/api/v1/profile")

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_repository)
):
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return ProfileResponse(
        username=current_user.username,
        email=current_user.email,
        **current_user.profile.__dict__
    )

@router.patch("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_repository)
):
    try:
        updated_profile = repo.update_profile(current_user.id, profile_data)
        return ProfileResponse(
            username=current_user.username,
            email=current_user.email,
            **updated_profile.__dict__
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
