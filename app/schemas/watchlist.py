from pydantic import BaseModel
from datetime import datetime
from app.schemas.movie import MovieResponse

# ----------------- Watchlist Response -----------------
class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    movie: MovieResponse
    created_at: datetime

    class Config:
        orm_mode = True
