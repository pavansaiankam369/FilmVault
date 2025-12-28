from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from datetime import date

# ----------------- Movie Availability Schema -----------------
class MovieAvailabilityBase(BaseModel):
    platform_id: int
    region_id: int
    availability_type: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    url: Optional[str] = None

class MovieAvailabilityCreate(MovieAvailabilityBase):
    pass

class MovieAvailabilityResponse(MovieAvailabilityBase):
    id: int
    movie_id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ----------------- Movie Base -----------------
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    director: Optional[str] = None
    cast: Optional[str] = None
    release_year: Optional[int] = None
    poster_url: Optional[str] = None

# ----------------- Movie Create -----------------
class MovieCreate(MovieBase):
    pass

# ----------------- Movie Update -----------------
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    director: Optional[str] = None
    cast: Optional[str] = None
    release_year: Optional[int] = None
    poster_url: Optional[str] = None
    approved: Optional[bool] = None

# ----------------- Movie Response -----------------
class MovieResponse(MovieBase):
    id: int
    rating: float
    approved: bool
    created_by: int
    created_at: datetime
    updated_at: datetime
    availability: List[MovieAvailabilityResponse] = []

    class Config:
        orm_mode = True
