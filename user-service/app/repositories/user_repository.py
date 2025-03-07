from sqlalchemy.orm import Session
from app.models import User, Profile, Session as DBSession
from app.schemas import UserCreate, ProfileUpdate
from typing import Optional
import uuid
from datetime import datetime

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate, hashed_password: str) -> User:
        user = User(
            id=uuid.uuid4(),
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
        except:
            self.db.rollback()
            raise
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_profile(self, user_id: uuid.UUID) -> Profile:
        profile = Profile(user_id=user_id)
        self.db.add(profile)
        try:
            self.db.commit()
            self.db.refresh(profile)
        except:
            self.db.rollback()
            raise
        return profile

    def get_profile_by_user_id(self, user_id: uuid.UUID) -> Optional[Profile]:
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()

    def update_profile(self, user_id: uuid.UUID, profile_data: ProfileUpdate) -> Profile:
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        user = self.get_user_by_id(user_id)
        
        if not profile or not user:
            raise ValueError("User or profile not found")
        
        update_data = profile_data.dict(exclude_unset=True)
        
        if "email" in update_data:
            user.email = update_data["email"]
            del update_data["email"]
        
        for key, value in update_data.items():
            setattr(profile, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(profile)
        except:
            self.db.rollback()
            raise
            
        return profile

    def create_session(self, user_id: uuid.UUID, ip_address: str, expires_at: datetime) -> DBSession:
        session = DBSession(
            user_id=user_id,
            ip_address=ip_address,
            expires_at=expires_at
        )
        self.db.add(session)
        try:
            self.db.commit()
            self.db.refresh(session)
        except:
            self.db.rollback()
            raise
        return session

    def get_valid_session(self, session_id: uuid.UUID) -> Optional[DBSession]:
        return self.db.query(DBSession).filter(
            DBSession.session_id == session_id,
            DBSession.expires_at > datetime.utcnow()
        ).first()
