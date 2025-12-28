from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import Platforms
from app.repositories.platform_repository import PlatformRepository
from app.schemas.platform import PlatformCreate, PlatformUpdate

class PlatformService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PlatformRepository(db)

    def create_platform(self, platform_data: PlatformCreate):
        if self.repo.get_by_name(platform_data.name):
            raise HTTPException(status_code=400, detail="Platform with this name already exists")
        
        # Validate type
        valid_types = ['OTT', 'Theater', 'TV', 'Other']
        if platform_data.type not in valid_types:
             raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of {valid_types}")

        new_platform = Platforms(
            name=platform_data.name,
            type=platform_data.type,
            website=platform_data.website
        )
        return self.repo.create(new_platform)

    def get_platform(self, platform_id: int):
        platform = self.repo.get_by_id(platform_id)
        if not platform:
            raise HTTPException(status_code=404, detail="Platform not found")
        return platform

    def update_platform(self, platform_id: int, platform_data: PlatformUpdate):
        platform = self.get_platform(platform_id)
        
        if platform_data.name:
            existing = self.repo.get_by_name(platform_data.name)
            if existing and existing.id != platform_id:
                raise HTTPException(status_code=400, detail="Platform name already in use")
            platform.name = platform_data.name
        
        if platform_data.type:
             valid_types = ['OTT', 'Theater', 'TV', 'Other']
             if platform_data.type not in valid_types:
                raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of {valid_types}")
             platform.type = platform_data.type
        
        if platform_data.website:
            platform.website = platform_data.website

        return self.repo.update(platform)

    def delete_platform(self, platform_id: int):
        platform = self.get_platform(platform_id)
        self.repo.delete(platform)
        return {"message": "Platform deleted successfully"}

    def list_platforms(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)
