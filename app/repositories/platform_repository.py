from sqlalchemy.orm import Session
from app.models.user import Platforms
from typing import Optional

class PlatformRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Optional[Platforms]:
        return self.db.query(Platforms).filter(Platforms.name == name).first()

    def get_by_id(self, platform_id: int) -> Optional[Platforms]:
        return self.db.query(Platforms).filter(Platforms.id == platform_id).first()

    def create(self, platform: Platforms) -> Platforms:
        self.db.add(platform)
        self.db.commit()
        self.db.refresh(platform)
        return platform

    def update(self, platform: Platforms) -> Platforms:
        self.db.commit()
        self.db.refresh(platform)
        return platform

    def delete(self, platform: Platforms):
        self.db.delete(platform)
        self.db.commit()

    def list(self, skip: int = 0, limit: int = 100):
        return self.db.query(Platforms).offset(skip).limit(limit).all()
