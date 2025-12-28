from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------- Region Base -----------------
class RegionBase(BaseModel):
    name: str
    code: str

# ----------------- Region Create -----------------
class RegionCreate(RegionBase):
    pass

# ----------------- Region Update -----------------
class RegionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None

# ----------------- Region Response -----------------
class RegionResponse(RegionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
