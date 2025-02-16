from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserLogin
from app.services.auth_service import AuthService
from app.schemas.token import Token

router = APIRouter() 

@router.post("/login", response_model=Token, summary="User Login")
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    """User login and token generation"""
    auth_service = AuthService(db)
    return auth_service.login_user(form_data)

@router.post("/refresh", response_model=Token, summary="Refresh Access Token")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Allows users to refresh their access token"""
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(refresh_token)

@router.post("/logout", summary="User Logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    """User logout by revoking the refresh token"""
    auth_service = AuthService(db)
    return auth_service.logout_user(refresh_token)
