from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, email: str, hashed_password: str, username: str, phone: str) -> User:
        user = User(email=email, hashed_password=hashed_password, username=username, phone=phone)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self):
        return self.db.query(User).all()
    
    def update_user(self, payload:UserUpdate):
        user = self.db.query(User).filter(User.id == payload.id).first()
        if user:
            if payload.phone:
                user.phone = payload.phone
            if payload.is_admin:
                user.is_admin = payload.is_admin
            self.db.commit()
            self.db.refresh(user)
            return user
        else:
            return None  # Handle case where user doesn't exist.