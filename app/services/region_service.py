from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import Regions
from app.repositories.region_repository import RegionRepository
from app.schemas.region import RegionCreate

class RegionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RegionRepository(db)

    def create_region(self, region_data: RegionCreate):
        if self.repo.get_by_code(region_data.code):
            raise HTTPException(status_code=400, detail="Region with this code already exists")
        
        new_region = Regions(name=region_data.name, code=region_data.code)
        return self.repo.create(new_region)

    def get_region(self, region_id: int):
        region = self.repo.get_by_id(region_id)
        if not region:
            raise HTTPException(status_code=404, detail="Region not found")
        return region

    def list_regions(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)
