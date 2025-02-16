from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.common import get_current_admin, get_current_user
router = APIRouter() 

@router.post("/register", response_model=UserResponse, summary="Register a new user")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account"""
    user_service = UserService(db)
    return user_service.register_user(user_data)
@router.get("/", response_model=list[UserResponse], summary="Get all users")
def list_users(
    db: Session = Depends(get_db), 
    current_admin: UserResponse = Depends(get_current_admin)
):
    """Only admins can retrieve all users."""
    user_service = UserService(db)
    return user_service.get_all_users()

@router.patch("/{user_id}", response_model=UserResponse, summary="Update user profile")
def update_user(
    user_id: int, 
    user_data: UserUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
):
    """Users can only update their own profile, while admins can update anyone."""
    user_service = UserService(db)

    if current_user.is_admin or current_user.id == user_id:
        return user_service.update_user(user_data)
    
    raise HTTPException(status_code=403, detail="Access forbidden")

@router.get("/me", response_model=UserResponse, summary="Get own profile")
def get_own_profile(
    current_user: UserResponse = Depends(get_current_user)
):
    """Users can only access their own profile."""
    return current_user

@router.get("/{user_id}", response_model=UserResponse, summary="Get user by id")
def get_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
):
    """Admins can get any user, regular users can only get their own profile."""
    user_service = UserService(db)

    # Allow if admin OR if user is requesting their own profile
    if current_user.is_admin or current_user.id == user_id:
        return user_service.get_user_by_id(user_id)
    
    raise HTTPException(status_code=403, detail="Access forbidden")
   
   
# @router.delete("/{user_id}", summary="Delete a user (Admin Only)")
# def delete_user(
#     user_id: int, 
#     db: Session = Depends(get_db), 
#     current_admin: UserResponse = Depends(get_current_admin)
# ):
#     """Only admins can delete users."""
#     user_service = UserService(db)
#     user_service.delete_user(user_id)
#     return {"message": "User deleted successfully"}
