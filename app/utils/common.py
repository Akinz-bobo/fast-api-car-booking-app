from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.services.auth_service import AuthService
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    """
    Dependency to retrieve the authenticated user from a valid token.
    """
    auth_service = AuthService(db)
    return auth_service.get_user_from_token(token)

def get_current_admin(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
    Dependency to ensure only admins can access certain routes.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user