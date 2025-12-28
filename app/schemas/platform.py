from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

# ----------------- Platform Base -----------------
class PlatformBase(BaseModel):
    name: str
    type: str
    website: Optional[str] = None

# ----------------- Platform Create -----------------
class PlatformCreate(PlatformBase):
    pass

# ----------------- Platform Update -----------------
class PlatformUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    website: Optional[str] = None

# ----------------- Platform Response -----------------
class PlatformResponse(PlatformBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
