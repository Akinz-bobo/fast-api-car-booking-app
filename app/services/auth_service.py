from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.security import create_access_token, create_refresh_token, verify_password, verify_refresh_token, verify_access_token
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.token import Token
from app.schemas.user import UserLogin
from datetime import timedelta

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)

    def login_user(self, user_data:UserLogin, remember_me: bool = False):
        """Authenticate user and return access + refresh token"""
        user = self.user_repository.get_user_by_email(user_data.email)
        print(user)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Token payload
        token_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin,
            "phone": user.phone
        }

        # Generate access token
        access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=30))

        # Check if user already has a valid refresh token
        existing_refresh_token = self.refresh_token_repo.get_valid_token_by_user(user.id)

        if existing_refresh_token:
            refresh_token = existing_refresh_token.token  # Use the existing valid token
        else:
            refresh_expiry = timedelta(days=30) if remember_me else timedelta(days=7)
            refresh_token = create_refresh_token(data={"sub": str(user.id)},expires_delta=refresh_expiry)
            self.refresh_token_repo.create_refresh_token(user.id, refresh_token)

        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    def refresh_access_token(self, refresh_token: str):
        """Refresh the access token using a valid refresh token"""
        payload = verify_refresh_token(refresh_token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Check if token exists in the database
        stored_token = self.refresh_token_repo.get_valid_token(refresh_token)
        if not stored_token:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        # Check if user still exists (security measure)
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate new tokens
        token_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin,
            "phone": user.phone
        }
        new_access_token = create_access_token(data=token_data)
        new_refresh_token = create_refresh_token({"sub": user_id})

        # Store new refresh token & revoke old one
        self.refresh_token_repo.revoke_token(refresh_token)
        self.refresh_token_repo.create_refresh_token(user_id, new_refresh_token)

        return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

    def logout_user(self, refresh_token: str):
        """Revoke a refresh token to log the user out"""
        if not self.refresh_token_repo.revoke_token(refresh_token):
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return {"message": "Successfully logged out"}
    
    def get_user_from_token(self, token: dict):
        """Extract user from the provided access token."""
        user_from_token = verify_access_token(token)
        user_id = user_from_token.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token or user not found")

        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
