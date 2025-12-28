from sqlalchemy.orm import Session
from app.models.user import Regions
from typing import Optional

class RegionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, code: str) -> Optional[Regions]:
        return self.db.query(Regions).filter(Regions.code == code).first()

    def get_by_id(self, region_id: int) -> Optional[Regions]:
        return self.db.query(Regions).filter(Regions.id == region_id).first()

    def create(self, region: Regions) -> Regions:
        self.db.add(region)
        self.db.commit()
        self.db.refresh(region)
        return region

    def list(self, skip: int = 0, limit: int = 100):
        return self.db.query(Regions).offset(skip).limit(limit).all()
