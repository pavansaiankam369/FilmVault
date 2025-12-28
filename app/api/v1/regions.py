from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.schemas.region import RegionCreate, RegionResponse
from app.services.region_service import RegionService
from app.api.v1.auth import get_current_user, get_db
from app.models.user import User
from app.api.v1.platforms import get_current_admin

router = APIRouter(prefix="/regions", tags=["Regions"])

@router.post("/", response_model=RegionResponse, status_code=201)
def create_region(region: RegionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    service = RegionService(db)
    return service.create_region(region)

@router.get("/", response_model=List[RegionResponse])
def list_regions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = RegionService(db)
    return service.list_regions(skip, limit)

@router.get("/{id}", response_model=RegionResponse)
def get_region(id: int, db: Session = Depends(get_db)):
    service = RegionService(db)
    return service.get_region(id)
