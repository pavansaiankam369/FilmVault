from sqlalchemy.orm import Session
from app.models.user import Watchlist, Movies
from sqlalchemy import desc
from typing import Optional

class WatchlistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_and_movie(self, user_id: int, movie_id: int) -> Optional[Watchlist]:
        return self.db.query(Watchlist).filter(Watchlist.user_id == user_id, Watchlist.movie_id == movie_id).first()

    def create(self, item: Watchlist) -> Watchlist:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: Watchlist):
        self.db.delete(item)
        self.db.commit()

    def list(self, user_id: int, skip: int = 0, limit: int = 20):
        # Eager load movie details
        return self.db.query(Watchlist).filter(Watchlist.user_id == user_id)\
            .order_by(desc(Watchlist.created_at))\
            .offset(skip).limit(limit).all()
