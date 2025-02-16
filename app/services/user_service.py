# app/services/user_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse,UserUpdate
from app.core.security import hash_password

class UserService:
    def __init__(self, db: Session): 
        self.user_repository = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """Handles user registration by creating a new user in the database"""
        existing_user = self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        hashed_password = hash_password(user_data.password)
        user = self.user_repository.create_user(
            email=user_data.email,
            hashed_password=hashed_password,
            username=user_data.username,
            phone=user_data.phone
        )

        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            phone=user.phone,
            is_admin=user.is_admin
        )
    
    def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)

    def get_user_by_id(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
    
    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def update_user(self,payload:UserUpdate):
        user = self.get_user_by_id(payload.id)
        if not user:
            raise ValueError("User not found")
        user = self.user_repository.update_user(
       payload=payload,
        )
        return user
