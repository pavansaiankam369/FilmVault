from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.api.v1.auth import get_current_user, get_db
from app.models.user import User
from app.api.v1.platforms import get_current_admin

router = APIRouter(prefix="/users", tags=["[Admin] User Management"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user_admin(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = UserService(db)
    return service.create_user(user.username, user.email, user.role, user.password)

@router.get("/all", response_model=List[UserResponse])
def list_users_admin(
    skip: int = 0, 
    limit: int = 20, 
    role: Optional[str] = None, 
    status: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_admin)
):
    service = UserService(db)
    # Basic filtering logic could be moved to Service/Repo if complexity grows
    users = service.list_users() # This gets all, filtering in memory for MVP speed
    
    if role:
        users = [u for u in users if u.role == role]
    if status:
        users = [u for u in users if u.status == status]
        
    return users[skip : skip + limit]

@router.get("/{id}", response_model=UserResponse)
def get_user_admin(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = UserService(db)
    # Using specific repo method if exists, or finding in list
    repo = service.repo
    user = repo.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}", status_code=204)
def update_user_admin(id: int, role: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = UserService(db)
    user = service.repo.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if role:
        user.role = role
    if status:
        user.status = status
        
    service.repo.update(user)
    return

@router.delete("/{id}", status_code=204)
def delete_user_admin(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = UserService(db)
    user = service.repo.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.status = 'suspended'
    service.repo.update(user)
    return
