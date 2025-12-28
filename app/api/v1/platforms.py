from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.schemas.platform import PlatformCreate, PlatformResponse, PlatformUpdate
from app.services.platform_service import PlatformService
from app.api.v1.auth import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/platforms", tags=["Platforms"])

# Dependency to check admin role
def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.post("/", response_model=PlatformResponse, status_code=201)
def create_platform(platform: PlatformCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = PlatformService(db)
    return service.create_platform(platform)

@router.get("/", response_model=List[PlatformResponse])
def list_platforms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = PlatformService(db)
    return service.list_platforms(skip, limit)

@router.get("/{id}", response_model=PlatformResponse)
def get_platform(id: int, db: Session = Depends(get_db)):
    service = PlatformService(db)
    return service.get_platform(id)

@router.put("/{id}", status_code=204)
def update_platform(id: int, platform: PlatformUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = PlatformService(db)
    service.update_platform(id, platform)
    return

@router.delete("/{id}", status_code=204)
def delete_platform(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = PlatformService(db)
    service.delete_platform(id)
    return
