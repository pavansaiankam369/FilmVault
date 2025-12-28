from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ----------------- Review Base -----------------
class ReviewBase(BaseModel):
    rating: float = Field(..., ge=0, le=10, description="Rating must be between 0 and 10")
    comment: Optional[str] = None

# ----------------- Review Create -----------------
class ReviewCreate(ReviewBase):
    movie_id: int

# ----------------- Review Update -----------------
class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0, le=10)
    comment: Optional[str] = None

# ----------------- Review Response -----------------
class ReviewResponse(ReviewBase):
    id: int
    movie_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
