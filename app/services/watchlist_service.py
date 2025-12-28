from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import Watchlist
from app.repositories.watchlist_repository import WatchlistRepository

class WatchlistService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = WatchlistRepository(db)

    def add_to_watchlist(self, user_id: int, movie_id: int):
        if self.repo.get_by_user_and_movie(user_id, movie_id):
            raise HTTPException(status_code=400, detail="Movie already in watchlist")

        new_item = Watchlist(user_id=user_id, movie_id=movie_id)
        return self.repo.create(new_item)

    def remove_from_watchlist(self, user_id: int, movie_id: int):
        item = self.repo.get_by_user_and_movie(user_id, movie_id)
        if not item:
            raise HTTPException(status_code=404, detail="Movie not found in watchlist")
        
        self.repo.delete(item)
        return {"message": "Movie removed from watchlist"}

    def list_watchlist(self, user_id: int, skip: int, limit: int):
        return self.repo.list(user_id, skip, limit)
    
    def check_status(self, user_id: int, movie_id: int):
         item = self.repo.get_by_user_and_movie(user_id, movie_id)
         return {"in_watchlist": item is not None}
