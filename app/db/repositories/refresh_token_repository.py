from sqlalchemy.orm import Session
from app.db.models.refresh_token import RefreshToken
import uuid
from datetime import timedelta,datetime
from app.core.config import settings

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(self, user_id: str, token: str):
        """Stores a refresh token in the database"""
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        new_token = RefreshToken(
            id=str(uuid.uuid4()),
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        self.db.add(new_token)
        self.db.commit()
        self.db.refresh(new_token)
        return new_token

    def get_valid_token(self, token: str):
        """Retrieves a valid refresh token"""
        return self.db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()

    def get_valid_token_by_user(self, user_id: str):
        """Find a valid refresh token by user"""
        return self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()

    def revoke_token(self, token: str):
        """Revokes a refresh token (used for logout)"""
        stored_token = self.db.query(RefreshToken).filter(
            RefreshToken.token == token
        ).first()
        if stored_token:
            stored_token.is_revoked = True
            self.db.commit()
            return True
        return False

    def cleanup_expired_tokens(self):
        """Deletes all expired refresh tokens"""
        self.db.query(RefreshToken).filter(RefreshToken.expires_at < datetime.utcnow()).delete()
        self.db.commit()
